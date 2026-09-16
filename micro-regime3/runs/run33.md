# Run 33 (GHC HEAD against ghc-9.12.4, both at plain -O1 under the exit span)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach.

**Run 33 (GHC HEAD against ghc-9.12.4, both at plain -O1 under the exit span): the two compilers part by up to 3.54 points on an arm, HEAD the faster on every arm that moves past a point, and they part FURTHER with the exit span than Run 32 read without it.** The pair is Run 32's recipe with `LOOP_EXITSPAN=1` added to both halves --- the shim switch that charges a loop head's fall-through exit with its body, a second span running from the head through the first jump after its last back edge, which [the placement section][floor] prices and which the shim's own header calls a basis change and keeps off by default --- one source at `f31bd1c`, one shim at `f31bd1c`, one shim environment, one regime, one roster and one bench order, the 9.12.4 half `run33-exit` publishing and the in-tree stage1 `10.1.20260803` half `run33-gheadexit` the candidate, so `the basis` below is the 9.12.4 half and every `cross` figure reads basis over control, ABOVE 1 meaning the control is the faster. Over the sixteen main-set arms that carry a cross-half figure, TEN sit within 1% of 1 and the six outside reach 3.54 points: `lib-stage2-lean` at **1.0354**, `lib-stage1` at **1.0298**, `lib-stage2-lean-u1` at **1.0209**, and the shipped leaf with its two A/A copies at 1.0111, 1.0127 and 1.0108 --- every one of the six from the fill family, two of them its A/A copies, and every one faster under HEAD. **The bar an arm has to clear to be the compiler's rather than the run's is 0.16 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, `bq-expand-aa-adjacent` against `bq-expand`, which `--compare` prints under every table and which is NOT this population's floor, that being 0.47% and measured WITHIN one half --- and ALL EIGHT strategies clear it, where Run 32's bar was 0.81 points and three of eight cleared it. One arm moves past 3%, `lib-stage2-lean`, where Run 32's `--movers` named none, and the geomean over the arms is **1.0068** against Run 32's 0.9985.

**Registration (1) is KILLED, and the counted work says what killed it is not the code generator.** The item predicted the lean fill level between the compilers within 2% on the main set, on the argument that the exit span removes the one placement defect these arms had --- HEAD's head at residue 9 with its exit astride the line, which Run 32 read at 1.0134 without the switch. With the switch on both halves it reads **1.0354**, two points FURTHER from level than Run 32 and in the same direction, HEAD ahead; its twin `lib-stage2-lean-u1` reads 1.0209 against the same 2% bar. **The counts then split the gap into its two terms**: over the nineteen main-set shapes the basis executes **0.62%** more instructions on the lean fill and takes **3.54%** more time, so `time/counts` is **1.0290** and four fifths of the gap is not instructions at all. It is that residue the switch was aimed at and did not take. Where the item's own `runs` clause is read, at a 3% band, the fill comes back level at **1.0028** and that span HOLDS.

**The sharpest reading of the same shape is on `runs`, where one arm takes 29.5% longer on 9.12.4 having been handed the identical instruction count.** `lib-stage2-lean-u1` reads **1.2954** across the halves over the fourteen `runs` shapes --- the basis slower on all fourteen of them, from 1.013 to 1.473 --- and its counted work reads **1.0000**, so `time/counts` is the whole 1.2954. No registration names that arm on that population and the run reports it because it moved: it is the widest cross-half figure in the file, against a class A/A bar of 0.66 points, and its unrolled twin `lib-stage2-lean` sits at 1.0028 beside it. Whatever HEAD does for the un-unrolled lean dispatch on runs of short extent, it does without changing what the machine is asked to execute.

**The roster is 33 timed arms over 19 main-set shapes and 627 benches, with 58 class views over ten classes for 1914 more, and it is NOT Run 32's.** `./roster-delta.py run32-nospec run33-exit` reads 32 arms to 33 over 19 shapes to 19: ONE in and NONE out, the 32 survivors in the same order, no shape moved and no class view moved --- `runs` stays at fourteen, `window` at eight, `bcast` and `flip` at six, `block` and `small` at five, `bcastmid` and `compose` at four, `rev` and `scaled` at three. In, landing at `f46867f`, is `libunord-stage11-sum`, stage ten with its zero-stride move guarded. The L1 roster pass was therefore OWED, step 12's condition asking for a membership change, and it was taken whole --- eleven legs over all ten classes and the main set, every one `pass clean`. **And the shim moved under this pair, which it had not since Run 25**: `align-as.py` goes from `b3a1aca` to `f31bd1c` in NINE commits, `3b49356` adding `LOOP_EXITSPAN` and the entry count beside it and `f1a5adb` fixing the first of them, so a distance from Run 32 carries a shim term as well as a source one --- and that term is wider than the switch, two of the nine being large.

**NOT ONE CELL SINKS BELOW THE SHARED FORCING PASS ON EITHER HALF**, as on Runs 28 to 32 and for the same two reasons: the ruling of 2026-09-10 that a reducing consumer has no corrected time, so the `-sum` rows read `--` in `time` and `worst` by design, and the retirement of every Fill arm over a list to `check`. `read-all.sh --brief-facts` reports an empty sunk list for both halves, so every row that carries a corrected time at all is a geomean over all nineteen shapes.

**The gate read SOUND, the machine check did not fire, and the one cross-run step this chapter allows agrees with both.** The two palindrome passes agree to **0.08**, **0.30** and **0.16** points on `list`, `bq-expand` and `mut-odo-vecdims` --- narrower than Run 32's 1.42, 0.89 and 0.48 and than Run 27's 1.36, 0.93 and 0.44, arm for arm --- with no arm crossing 1 between the passes, where Run 32's `list` did. **The machine check** reads `list`'s net at a geomean of **-0.25%** against the fingerprint `runs/run32.md` keeps, inside the 3% bar, worst `gather48-src-50` at -1.96% and 0 of 19 shapes past 5%; this one is NOT like-for-like, Run 32's published half being this basis less `LOOP_EXITSPAN=1` and `Main.hs` having moved at `f46867f` and `f31bd1c` under it, so it carries a switch term and a source term together. **That distance is registration (6)'s**, and read arm by arm with `--compare run32-nospec run33-exit` --- `run32-nospec` being Run 32's published basis half, this recipe less the switch --- the item HOLDS on all three of its spans: the lean fill at **0.9983**, its un-unrolled twin at **0.9817** and `list` at **1.0014**, against 2%, 2% and 1%. So the switch reaches neither fill arm across the two builds, and it reaches the reference by fourteen hundredths of a point.

**Every one of the twenty-two processes gated clean, the plateau did not fire, and three A/A worst cells sit above 5%, all of them on the control half.** The preamble's victim spans 21.0636 to 21.7295 ms/iter across the run, a **3.16%** spread against a 5% band, and all twenty-two processes assert ONE `keep` and ONE `inuse`, as a compiler pair should and as the pair note declined to gate. Within the halves the two do not resolve alike: the control's eleven processes span 3.16% and the basis's 1.37%. The three A/A cells above 5% are `gheadexit-flip` at **7.15%** on `flip-last-rows`, `gheadexit-main` at **5.36%** on `lenet-L1-28-c1-k5` and `gheadexit-runs` at **5.32%** on `runs-512`; the first and third are wild cells, `--wild` clearing their logs with no bench at 0.25 of a core. The second is not, and it has a paragraph of its own.

**ONE PROCESS OF THE TWENTY-TWO WAS INTRUDED ON, BY THIS SESSION, AND THE RERUN THE PROCEDURE ORDERS WAS STOPPED AT THE OWNER'S WORD --- so this run publishes with a disclosure and the check that stands in for the rerun.** `run33-gheadexit-main` carries 3 of its 627 benches at or above 0.25 of a core, peak **0.35**: `lenet-L1-28-c1-k5/mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.35, `cnn-L1-6x6-c1/lib-stage2-lean` at 0.33 and `cnn-L1-6x6-c1/mut-odo-vecdims-add-in-leaf-u2-aa` at 0.26. The intruder was this session reading documents and spawning the readings carrier, which run list step 15 put *after `sequence: start`* and which therefore landed inside the sequence's first process --- the same failure Run 32 met inside its GATE, one step earlier, and the reason that line had been scoped to the sequence in the first place. **The chapter has since moved every reading out of the evening**: they are step 13a now, taken before `run-evening.sh` is launched, the carrier with them, because the exposure is per command and not per minute --- the two reads step 15 named cost 0.08 s and 0.37 s of CPU, and a bench's samples are milliseconds. **What it is worth is measured and not estimated.** Dropping `cnn-L1-6x6-c1` and `lenet-L1-28-c1-k5` from BOTH halves, all fifteen `predict:` spans keep the verdict the main-set sweep gives them --- six HELD and nine KILLED in that sweep either way --- and the widest moves 0.75 of a point, `lib-stage2-lean-u1`, which moves AWAY from its prediction. That sweep reads every span against the main set, which is not how the items are adjudicated below: read on the populations each item names, the fifteen are NINE held and six killed. What the sensitivity check asks of it is only that no span change sides, and none does. The population floor reads 0.62% over nineteen shapes and **0.66%** over seventeen, so the floor is not the intrusion's either. **One figure it did move is the one its cells belong to**: the A/A pair `mut-odo-vecdims-add-in-leaf-u2-aa-distant` against its original reads a published-column 1.0373 on that half where its PAIRED figure --- the statistic a `pair` span is judged on, and the one the floor is defined in --- reads **0.9983** over nineteen shapes and 1.0013 over the seventeen that exclude the intruded pair. One cell drags the column and leaves the paired geomean where it was. Every other process of the run is clean, the four gate processes and all 88 alone-leg rider logs included, and the superseded attempt is kept beside the artifacts under a `probe-` prefix.

**The sequence ran in ONE window with no hole in it.** Twenty-two processes from 2026-09-16T01:05:22+02:00 to 08:26:08+02:00, every one exiting 0 at the count its population asks for, the largest gap between one process finishing and the next starting **0m**, no complaint and no `!!` line anywhere in the wall-clock record; the control half ran first throughout, as the driver orders it.

**This run's two columns MAY be differenced on eight of the eleven populations**, which is one more than Run 32 could say and what a pair whose variable does not reach the reference looks like. It rests on `list` having moved **0.45 points** on this run's main set, and on `read-all.sh --brief-facts` putting `runs` (0.9951), `window` (1.0016), `bcast` (0.9982), `block` (1.0048), `flip` (1.0051), `small` (1.0068) and `bcastmid` (0.9931) inside the 0.7% bar beside it. THREE are past it: `compose` at 1.0081, `rev` at 0.9918 and `scaled` at 1.0109. On those three every arm-by-arm figure across the halves in this file is an ORDERING and not a subtraction, and each says so in its own cross-half line.

**The fastest timed arm on the main set is `lib-stage2-lean` at 0.025, and this run adds a second instance of the published column moving a row by more than the arm moved.** The shipped leaf and its two A/A copies read 0.027, `lib-stage2-lean-u1` and `mut-odo-vecdims-add-in-leaf-u1` and `lib-stage1` 0.029, `mut-odo-vecdims` 0.045 and `bq-expand` 0.127. **Between Run 32's published table and this one `lib-stage2-lean-u1` moves from 0.02514 to 0.02865, fourteen points**, while the same two binaries read **1.0186** paired, Run 33 the slower --- the same direction, and a seventh of the movement. `--winsor` says why: that row's plain per-shape geomean is **0.03038** where the published figure is 0.02865, four of its nineteen cells capped, and the cap band is what moved. Seven of the eight uncapped rows moved by nothing at all, `list-aa-adjacent` being the exception at 1.001 against 1.003, and eleven of the sixteen read the same three decimals in both runs.

**Four registrations held, two were killed and one cannot be adjudicated against these builds.** (2) HOLDS everywhere it is read --- `list` at 0.9955 on the main set inside 2% and between 0.9918 and 1.0109 on all ten classes inside 3%. (4) HOLDS: the shipped leaf reads 1.0111 across the halves inside its 2%, and its fusion over the odometer **0.6428** on the basis and **0.6371** on the control against a registered 0.64 within 4%, the ninth and tenth readings of that span, every one of the ten between 0.6358 and 0.6525 across five runs. (5) HOLDS in all forty-four readings --- the shipped leaf's two A/A copies, `-aa` and `-aa-distant`, against `mut-odo-vecdims-add-in-leaf-u2` itself, on both halves of all eleven populations --- each paired figure inside that population's own floor. (6) HOLDS on all three spans, above. **(1) and (3) are the kills.** (1) is the lean fill at 1.0354 and its twin at 1.0209 against 2% bars. (3) predicted the shared per-run loop of stages 7, 9, 10 and 11 at **0.81 within 6%** on `runs`, on the strength of a branch-and-fetch reading of one tree, and the three consumers come back at **0.9593**, **0.9574** and **0.9583** --- fifteen points away, and level rather than nine tenths; its `window` clause splits, stage nine HOLDING at 0.8889 inside its 6% and stage ten missing 1.0 within 3% at 0.9686. The preparation flagged that item to the owner before the run on exactly this ground, Run 32 having read those arms at 0.969 on the same population. **(7) cannot be adjudicated**: it predicts eight exit spans astride and its kill wants a ninth, where the shim this pair is built with reports **0 astride** on all four emissions, the population that could straddle being what `f1a5adb` removes.

**The three class properties hold in all ten classes on both halves, and on the main set property 1's `bq-expand` clause changes sides for the fourth run running.** `mut-odo-vecdims`'s `worst` stays under 1 everywhere, it is ahead of `bq-expand` on every shape of every class on both halves, both allocation clauses of property 2 hold with their 1% margin on every population, and property 3's tiers are identical between the halves --- the fills at the result vector, `bq-expand` at 2.78x and `list` at 25.20x on the main set, and every one of the ten class triples reading the same on the control as on the basis. **What moves is the one main-set cell that was already a tie**: on `stretch-pow2stride` the plain arm is BEHIND `bq-expand` at **1.0007** on the basis and AHEAD at **0.9961** on the control, where Run 31 read 1.0009, Run 32 0.9934 on its basis and 1.0003 on its control. Each margin is far inside the floor it is read against --- 0.07 of a point against 0.47% on the basis --- so the cell keeps saying what it has said for four runs, which is nothing either way. **And allocation agrees between the halves where it can be fitted at all**: 456 of the 589 allocating cells to 1e-4 and the other 95 to 2.17e-02 at worst, on `stretch-tall-Mx2/libunord-stage11-sum`, with the 38 cells under 100 bytes a call set aside as a property of fitting a near-zero allocation rather than of this pair.

**Across the halves no population's geomean is more than 1.84 points from level, and the vote has something to attribute for once.** The ten classes run from **1.0001** on `bcastmid` to **1.0184** on `runs`, with the main set at 1.0068; over the 160 class arm-comparisons 62 put the basis faster and 98 slower, none degenerate. The extremes are `mut-odo-vecdims-add-in-leaf-u1` at **0.9361** on `compose` and `lib-stage2-lean-u1` at **1.2954** on `runs` --- so where 9.12.4 wins on this roster it wins on the shipped leaf's un-unrolled form, which is the low extreme in 5 of the 10 populations, and where it loses it loses on the lean dispatch's un-unrolled twin.

**The counted work covers every population, no cell was refused anywhere, and its finding is that the two compilers emit very nearly the same work --- which is what makes the times interesting.** The counts geomean over the sixteen timed arms runs **0.9986** on `small` to **1.0098** on `window`, the main set at 1.0053, with the ten fill-family arms running **0.9996 to 1.0081** on that main set, so neither half executes even a percent more instructions than the other on average. Against that, `time/counts` on the main set puts `lib-stage2-lean` at **1.0290**, `lib-stage1` at 1.0221 and `lib-stage2-lean-u1` at 1.0148, while `list` and its two A/A copies sit at 0.9855 to 0.9857 --- the basis executing about one percent MORE instructions on the reference and still running it 0.45% faster, and executing about half a percent more on the fill family and losing three and a half. The whole of `runs`'s 1.2954 on `lib-stage2-lean-u1` sits in that column, its counts being level to four decimals. So the compiler term this pair measures is a placement-and-runtime term almost everywhere it is large, and the exit span, which both halves carry, did not remove it.

**And the arm that landed this run is read here, because the open list asked this run for it.** `libunord-stage11-sum` is stage ten with its zero-stride move guarded, so it should be stage seven where no axis has a zero stride and stage ten where one does. It is: over stage seven it reads **1.0012** on the main set, **1.0002** on `runs` and **1.0009** on `window`, every one inside those populations' floors, and **0.5501** on `bcast`, where the move fires and stage seven does not; over stage ten it reads **0.9820** on the main set, 0.9989 on `runs`, 0.9959 on `window` and **1.0000** on `bcast`, the two dispatches identical to four decimals where a zero stride is there to move. So the guard costs nothing it was not meant to cost, and the main set's 0.9820 is the one figure of the four outside a floor --- 15 of 19 shapes favouring stage eleven, at sign p 0.019, which is the guard paying on the main set's own mixture rather than on either extreme.

**The correction sits on the same footing in both halves, the two resolve alike, and not one cell of either half is one the reader distrusts.** The two `sum-only` halves agree to within **0.13%** on every population and both halves --- 0.9987 to 1.0010 across the twenty-two --- so the term subtracted from one half is the term subtracted from the other. `CI%` reads a geomean of **1.03** over the 33 arms, 16 wider on the basis and 17 narrower. The A/A floors are **0.47%** on the basis and **0.62%** on the control, both carried by `bq-expand-aa-distant`, which is the same pair naming the floor on both halves where Run 32's two halves named different pairs. **And NOT ONE cell of any of the twenty-two populations sits below R2 0.99 or under ten samples**, the reader's warning channel silent across the whole run --- which it is not for want of a voice: run on Run 32's control `window` it names that run's one cell at 0.9867.

**The straddling loops stand at EIGHT on each half, as they did on Run 32, and the offset-0 column is where the exit span shows.** `loop-offsets.py --survey` reads **305** self-loops of at most 64 B in the basis's own compiled code, 184 of them at offset 0 and 8 straddling, against **325** on the control, 195 at offset 0 and 8 straddling. Run 32 read 134 of 292 and 130 of 311 in that column, under a half; this run reads about three fifths on BOTH halves, which is the switch and is recorded without a mechanism. Within the pair its `--library` mode reads **136** self-loops in common in the LINKED libraries --- a different population from the survey's, which counts Main's own --- **11.0%** of them at the same offset in line and **65.4%** in the same straddle state --- RUN 32'S THREE FIGURES TO THE DIGIT, under a shim that moved and a source that moved, and this file offers no account of that either. **Post-run step 0's naming was taken off the binaries that were timed**, with two `-g3` twins built from the same two recipes: six of the basis's eight straddlers are named by byte identity --- `fillStage2Short`, `fbMutOdoVecdimsAddInLeafU2` twice, and its `Down`, `Last` and `Ptr` forms --- and three of the control's, one of those three off the OTHER half's twin, which is what giving both twins buys. The fill groups name the same six and two arms on each half. **And the count check refuses the population comparison on the control half**, its twin holding 324 self-loops against the timed binary's 325, so every name there rests on its own byte match alone.

**The regime was confirmed in this run's own binaries before the hours were spent, and both halves read the same side of it.** `diag` reads `baseOffsetsScan` against `baseOffsetsMut` on `vgg-14-c512` at **24066407** against **2408530** on the basis and 24066455 against 2408530 on the control --- **9.992** times apart on each, the ten times this README has attributed to plain -O1 since Run 8 --- so both halves are plain -O1 and SpecConstr is off under HEAD at that level as it is under 9.12.4, which is the one thing this recipe had to get right. The version comes out of the binaries rather than off a project file: `ghc-internal-9.1204.0` on the basis and `ghc-internal-10.100.0` on the control, which is Run 32's HEAD to the day.

**The decomposition reproduces on both halves and its two columns do not part.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, and the state the preamble puts on a process comes back at a geomean of **1.1127** on the basis and **1.1154** on the control, 0.27 of a point apart. What the roster adds on top of that state is **1.0234** on the basis, 10 of 19 shapes above 1, and **1.0210** on the control, 8 of 19; the basis's rest runs 0.9735 on `stretch-bigstride` to 1.2345 on `stretch-r5-8x432`, the control's 0.9704 on `alexnet-L1-55-c3-k11` to 1.2159 on that same worst shape.

**There is NO repetition this run and none was available**, `Main.hs` having moved from `f95795a` to `f31bd1c` and the shim from `b3a1aca` to `f31bd1c`, so neither half's inputs are an earlier binary's and an unequal md5 names nothing: the basis is `2f750355da01b25cfdc3e81134c01fec` and the control `59e0ee343c245ede5b0f02e2a0160cdd`. What the two md5s DO say is that they differ from each other, which is the least two compilers can be asked for. **`.text` says the halves are not one build either**, 20787397 bytes on the basis against 20940607 on the control, the HEAD half larger by **153210** --- Run 32's difference TO THE BYTE, its halves having read 20766917 and 20920127 --- with each half sitting exactly **20480** bytes, five pages, above its Run 32 counterpart. Their load addresses differ as Run 32's did and are that run's two unchanged, 4218880 against 4214784. This file offers no mechanism for either coincidence.

**Everything in this file is replaced by the next run, which is what makes it a file.** What a run replaces OUTSIDE it, in README.md and in the sources, is [README's own Provenance](../README.md#provenance). None of it is portable: a run on another machine is a different measurement rather than a repetition. **What this run leaves the next one is a compiler term that is not the code generator's.** Run 32 asked the same two compilers at the same level without the exit span and read a null --- no arm past 3%, an arm geomean of 0.9985, three of eight strategies clearing an 0.81-point bar. With the switch on both halves the same pair reads an arm geomean of 1.0068, eight of eight strategies clearing a 0.16-point bar, one arm past 3% and one class arm at 1.2954 --- and the counts put nearly all of it outside the instruction stream. **What the kills teach is the lesson the chapter has been recording since Run 28, with its exception intact**: (1) and (3) are as unlike as two kills can be: (3) predicted a MAGNITUDE, 0.81 on arms Run 32 had read at 0.969, and died where the preparation said it would, while (1) predicted LEVEL on the very arms the switch was added to level and died because the two compilers part further under it. So the no-op clause this chapter distrusts was right four times out of five here, and the once it failed it failed on the arms the run was built for.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table**, as Runs 30's, 31's and 32's were and for the reason Run 30 was moved onto it: it is the regime `Data/Array/Internal.hs` actually compiles under. **What is new in it is the exit span**, `LOOP_EXITSPAN=1` on both halves, so this basis is a recipe no run here has published before and a row's distance from the last published column carries that switch as well as the box. **Read against it anyway, the distance is small and the reference barely moves**: over the 16 arms that carry a corrected time and stand in both rosters, Run 32's basis half over this one runs **0.9817 to 1.0017** with `list` itself at **1.0014** --- below 1 meaning this run is the slower, and read as a ratio to `list` within each run --- which cancels a box term exactly, and which drops `list` as its own denominator --- the geomean over the other fifteen is **0.9961**, none of them outside the 3.3% drift band --- Run 11's reading, the wider of the two [the floor section][floor] carries, and the widest arm here is inside Run 23's narrower 2.1% as well. That span carries a SHIM term and a SOURCE term besides the box's: `align-as.py` moved from `b3a1aca` to `f31bd1c` and `Main.hs` from `f95795a` to `f31bd1c` between the two builds. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run33-exit`, as every published table here is from Run 11 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-three rows. That the published half is the ghc-9.12.4 one is the re-declaration of 2026-09-15 inherited rather than this run's to make --- 9.12.4 is what a default build takes on this machine and what a cross-run absolute is read against, and HEAD is the candidate reading. **Thirty-two of the thirty-three rows are not first readings**: every one of them has a twin in Run 32's file, and most have twins in Runs 30's and 31's besides. The thirty-third, `libunord-stage11-sum`, landed at `f46867f` --- stage ten with its zero-stride move guarded --- and is read here for the first time.

**Comparing runs?** The table below is Run 33's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.47%** from 1 on the basis half or **0.62%** on the control, read over the eight pairs this roster carries, and over the four pairs that carry back to Run 10 at **0.47%** and **0.62%** --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **Both halves name ONE pair this run**, `bq-expand-aa-distant`'s, where Run 32's two halves named different pairs and its control named the family root's for the first time; that is the fifth reading of the open question of which pair carries the whole-set floor and the first since Run 31 in which the two halves agree. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **3.75%** on `stretch-wide-2xM` on the basis and **5.36%** on `lenet-L1-28-c1-k5` on the control --- are not floors at all and are not to be quoted as any, and the second of them is the intruded cell the head discloses. **And what this run has that Run 32 had less of**: its two columns may be differenced on eight of the eleven populations, `list` having moved 0.45 points on the main set, so a cross-half figure here is a measurement on those eight and an ordering on the three past the bar.

**It is the main set's table**, and every column below is a statistic of that population: each stride class has a table of its own, on the same rows and in the same columns but its own basis, in [The stride classes, run by run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns, the `needs` column's own gloss being under [the properties](#the-properties-the-next-run-should-test) with the tier it splits:

- **time** is the geomean over **every** shape of the per-shape OLS *slope*, less that shape's forcing term, over `list`'s slope less the same term, with the per-shape log-ratios *winsorized* first --- capped at the row's own median plus or minus three MADs, the MAD scaled by 1.4826 so the cap is in standard deviations. Nothing is dropped by the estimator, so winsorizing costs no row its population and a cell far enough out to distort the mean has its influence bounded instead of its evidence deleted. **What cost a row its population on Run 27 was the correction, not the estimator, and on THIS run nothing does**: that run had nine rows on each half carrying cells the shared forcing pass is not smaller than --- seventy such cells on its basis and forty-three on its HEAD half, all of them `libunord` arms --- and this roster has none, so every row here that carries a corrected time is a geomean over all nineteen shapes. What replaced those rows is the `no_net` ruling and the retirement of the Fill arms over a list, named in the head and in *What the next run compares against*, and every other row covers all 19. The `CI%`, `smp` and `alloc` columns stay raw: subtracting a shared term moves a point estimate, it does not make a cell better measured. `worst` is a ratio of nets, as `time` is, just per shape and unwinsorized.

  **This replaced a trim** --- drop each strategy's single highest-CI shape --- and the ruling is worth keeping because the trim looks obviously right and is not. It selected on CI, and criterion spends a *time* budget, so a slow cell buys fewer samples and a wider CI: measured on Run 6, the cell it removed was above its own row's geomean in **30 of 41** rows, p about 0.003. It therefore deleted each strategy's worst evidence, differentially, and a catastrophic shape is exactly the shape it would remove: `bq-expand-lemire-out` loses on one shape of 33, and that shape was the one trimmed from its column. Because the cell removed differed by row, two published columns were also geomeans over different shape sets, which is why a published A/A ratio used to disagree with its paired one. Swapping estimators costs a median 2% and moves one row (`mut-offsets`) by 14%, that row having been flattered all along; it buys back exact comparability, and `--selftest` now asserts published == paired for every uncapped pair.

  **Don't reach for inverse-variance weighting**, which is the standard-looking repair and is worse than what it repairs. It assumes every shape estimates one ratio and differs only in precision, where here the between-shape variance runs a median 5,000x the within-shape kind --- the heterogeneity is the README's finding, not its error --- so weighting by precision collapses the effective shape count from 33 to about nine and hands a quarter of the weight to the smallest shape in the set. Worse for the purpose: a catastrophically slow cell buys fewer samples, so it has a wider CI, so IVW discounts precisely the cells the trim used to delete --- the same failure made continuous, not a repair of it.

  **The *slope* rather than criterion's mean, because criterion never times one call**: it times batches --- one call, then four, then twenty --- and every batch also pays for starting the timer and for the first pass through cold code and cold data. A mean divides each batch's time by its calls, so that fixed cost is smeared across them and weighs most in the small batches. The slope is the line through those points: how much more time one *additional* call adds, leaving the fixed part behind as the line's height at zero. On the microsecond shapes, hundreds of samples and no warm-up worth speaking of, the two agree. They part on the slow shapes, where the early batches run cold: there the mean reads high, and by different amounts for different strategies --- which is exactly the part that dividing by `list` cannot cancel. It also keeps `CI%` and R^2 describing the number the table shows, both being properties of that same fitted line.
- **worst** is the row's largest per-shape ratio to `list` --- the shape on which that strategy does least well against the baseline. It is what property 1 is about, and it is raw rather than winsorized.
- **CI%** is the median across shapes of the slope's confidence half-width as a percentage of the slope --- "how many digits are real". 0.5% is three; 5% is one.
- **smp** is the median sample count. Criterion spends a time budget, so a slow call buys fewer samples; this is where that shows.
- **alloc** is bytes per call as a multiple of the result vector (`8*l`), the median over shapes of the `allocated` fit the harness now runs on every bench of every shape. The multiples were held to be shape-independent --- refitted on a different shape, every one reproduced to within 0.4% --- so that the median was a formality rather than a smoothing and the column did not move with what it was fitted on. **That is wrong**, and Run 6 (-O1) reproduced the refutation at full budget where a rough pass had found it. Re-derived on Run 9's cells and roster it is unanimous: **every one of the 32 benched rows** varies by more than 5% from shape to shape, the median row by 2.00x and the worst by 5.10x (`bq-expand-b`, 1.00x to 5.10x), and the four shapes of identical `l` = 1800000 give `bq-expand` 2.000x, 2.111x, 1.000x and 2.639x. The spread narrowed as the roster was cut --- Run 6's worst was an arm nothing times any more --- and the property it measures did not. Every allocated fit sat at R^2 1.000 on Run 6, so the spread is the quantity and not the measurement, and allocation being deterministic per call the budget does not bear on it either way. What does survive is the column: a median over a *pinned* shape set reproduces, every allocation tier returning on its own level across a roster change. So read `alloc` as a statistic of a strategy **and** a shape set, and pin the shape set before comparing it across runs, exactly as the `time` column already asks. It is the one column the correction does not touch.

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.59* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.60 | 69 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage2-sum | -- | -- | 0.56 | 70 | 1.00x | the same, over the port's base-offset table |
| liblist-stage3-sum | -- | -- | 0.54 | 70 | 1.00x | the same, over the lazy odometer under the natural-strides dispatch |
| liblist-stage4-list-sum | -- | -- | 0.57 | 70 | 1.00x | the same, base's `sum` over stage four's list -- the fold a library user brings, over the lazy odometer under the lean dispatch |
| liblist-stage4-sum | -- | -- | 0.58 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| libunord-stage1-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage10-list-sum | -- | -- | 0.01 | 83 | 0.00x | the same, base's `sum` over stage ten's list -- the fold a library user brings, over the two reorderings composed |
| libunord-stage10-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's tie-break with stage nine's zero-stride axes moved outermost -- the two reorderings composed |
| libunord-stage11-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage eleven's list --- stage ten with its zero-stride move guarded, so the move fires only where a zero stride is there to move |
| libunord-stage6-loop-sum | -- | -- | 0.01 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.42* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage2-lean | 0.025 | 0.113 | 0.53 | 69 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.113* | *0.48* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.113 | 0.48 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.113* | *0.60* | *69* | *1.00x* | *A/A control* |
| lib-stage2-lean-u1 | 0.029 | 0.110 | 0.57 | 67 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| mut-odo-vecdims-add-in-leaf-u1 | 0.029 | 0.111 | 0.52 | 69 | 1.00x | new mutating `Vector` method -- the shipped fill's leaf with the bound merged in and the body not unrolled |
| lib-stage1 | 0.029 | 0.113 | 0.49 | 69 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| *mut-odo-vecdims-aa* | *0.045* | *0.112* | *0.39* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.112 | 0.41 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.112* | *0.43* | *66* | *1.00x* | *A/A control* |
| *bq-expand-aa-adjacent* | *0.127* | *0.250* | *0.72* | *50* | *2.78x* | *A/A control* |
| bq-expand | 0.127 | 0.253 | 0.73 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-distant* | *0.128* | *0.252* | *0.35* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.74 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.002* | *1.013* | *0.75* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.003* | *1.009* | *0.57* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run, as on Run 32, two pairs part in SIGN between the two statistics. `mut-odo-vecdims-add-in-leaf-u2-aa` against its base divides to **0.9959** on the published column, saying the adjacent copy is the faster, where the paired figure is **1.0005** at 12 of 19 wins, saying it is the slower; the distant copy does the same the other way, **1.0022** against **0.9980** at 11 of 19. Both sit inside this half's 0.47% floor, so nothing turns on them. **The widest disagreements are at the head of the table.** `lib-stage2-lean` against `lib-stage1` divides to **0.8438** on the column where the paired figure is **0.9442**, ten points apart; against the shipped leaf **0.9168** against **1.0017**, eight and a half, and in the opposite SIGN; against its own unrolling twin **0.8601** against **0.9508**, nine. Those column ratios are `--pair`'s own `published-column ratio` and not the printed table divided: three decimals put two different pairs at the same 0.862. **And the third way the column misleads, which Run 32 was the first to record, reproduces here with the same arm**: a SINGLE row's movement between runs is not the arm's either. `lib-stage2-lean-u1` prints 0.02865 here and 0.02514 on Run 32's basis half, fourteen points from level, where the cross-run paired reading is **1.0186**, one and nine tenths the same way; its plain per-shape geomean is 0.03038 against that run's 0.02978, and four of its nineteen cells are capped in each. A margin between two arms is `--pair`'s paired figure, which is also the statistic the floor is defined in; the column is for reading the table, not for differencing it, and not for tracking a row across runs either.

`concat-runs` has no row, and neither do the other 85 arms the roster holds and checks without timing --- **86 of its 119** in all, where Run 32 checked 85 of 117: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). **One arm was added to the timed roster this run and NONE was parked**, as on Run 32, where Run 31 parked six and added one. `libunord-stage11-sum`, stage ten with its zero-stride move guarded, landed at `f46867f` with the untimed `libunord-stage11` beside it; the six parked on 2026-09-13 stay parked, the two pointer leaves among them, so nothing on this roster times the ceiling Run 27 made readable; and the thirteen Fill arms over a list that went to `check` on 2026-09-09 stay where they are. So a movement against Run 32's basis column is a movement on the **16 shared arms that carry a corrected time**, with a shim term and a source term between the two runs and no roster term on those sixteen.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is `lib-stage2-lean` at 0.025**, with the shipped leaf and its two A/A copies at 0.027 and `lib-stage2-lean-u1`, `mut-odo-vecdims-add-in-leaf-u1` and `lib-stage1` at 0.029 --- **five timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result, the same five Runs 31 and 32 had. **The column and the pair DISAGREE about the order behind the leader**, as on Run 32: paired on the basis, `lib-stage2-lean` over `lib-stage1` is **0.9442** at 16 of 19 and p 0.0044, over its own unrolling twin **0.9508** at 12 of 19 and p 0.36, and over the shipped leaf **1.0017** at 15 of 19 and p 0.019 --- a geomean saying the leaf is a shade ahead while fifteen of nineteen shapes say the lean fill is --- while the column puts the lean fill three thousandths clear of the leaf and four clear of `lib-stage1`. The disagreement is the winsorizing and not an arm: `lib-stage2-lean-u1`'s published figure is 0.02865 where its plain per-shape geomean is 0.03038, four of its nineteen cells capped. **The third is that the leaf fusion is unmoved by the compiler**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6428** on the basis and **0.6371** on the control, six tenths of a point apart, where eight readings across Runs 29 to 32 lay between 0.6358 and 0.6525 under two flags, a whole level, two rosters and two compilers --- and now under the exit span as well.

**The two standing placement controls are still gone with the prune, the straddlers stand at eight on each half, and this pair --- like Run 32's --- DOES move tracked fill copies.** Within the pair `./loop-offsets.py run33-gheadexit run33-exit` puts the tracked six-copy group at **[0, 0, 0, 8, 4, 0]** on the basis and **[18, 0, 0, 0, 9, 2]** on the control, while the two-copy group reads **[0, 0]** on both; both halves carry 34 self-loops of 28 B in 27 distinct byte-sequences. So a compiler displaces fill copies as an optimisation level does, which is what `--library` says over the whole library too: 136 self-loops in common at **11.0%** the same offset in line. Against the nearest build of the basis's own recipe --- Run 32's basis half, which is this recipe LESS the exit span, no build of this one existing before --- `--delta` reads the two-copy group's offsets PRESERVED, `[0, 0]`, and the six-copy group's NOT: `[0, 0, 8, 0, 4, 0]` becomes `[0, 0, 0, 8, 4, 0]`, its third and fourth heads exchanging offsets, with no address surviving to the byte on either group. So the two comparisons this run can make agree again, both saying a tracked head's offset moves; and what moved under the second of them is wider than under Run 32's --- a source commit, a comment commit AND the shim, where Run 32 had six source commits and an unmoved shim.


## What the next run compares against

**Run 34's pair is the one declared 2026-09-15 morning and deferred whole when Run 33 was re-declared that evening: the two `-O2` passes against neither, on ghc-9.12.4, one variable and nothing else.** The basis half is the dead-spot form at plain `-O1`, `nospec` naming what that half is, and the other is that same recipe with `-fspec-constr` and `-fliberate-case` added by hand, `twopass`, so that `--compare` reads nospec over twopass and every `cross` below is what the two passes together do to one arm. One source, one shim, one shim environment, one roster, one shape set, one class list and one bench order, with the two command lines differing in three flags on one of them. **The one thing the executing session has to settle first is the shim environment**, this run having moved the published basis onto `LOOP_EXITSPAN=1`: the declaration predates that switch, both halves must carry the same answer, and which answer is taken decides only which basis Run 34's absolutes are read against. What the pair answers, and what a `cross` reading of it costs, is the registration's to state before it runs. The recipes, spelled out as a pair note wants them, with the exit span shown on both lines and to be dropped from both if the owner so decides:

    run34-nospec      cd here, then
                        LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 \
                        cabal build micro --builddir=db-r34a \
                          --ghc-options="-fobject-determinism" \
                          --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
                      then
                        cp $(cabal list-bin micro --builddir=db-r34a) run34-nospec
                        rm -rf db-r34a
    run34-twopass     the same source, then
                        LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 \
                        cabal build micro --builddir=db-r34b \
                          --ghc-options="-fspec-constr -fliberate-case -fobject-determinism" \
                          --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
                      then
                        cp $(cabal list-bin micro --builddir=db-r34b) run34-twopass
                        rm -rf db-r34b

`LOOP_MAXSKIP` and `LOOP_LOOKTHROUGH` are inert under the dead-spot form and stay on both lines so that the lines differ in the project file alone, as Run 32's did; `LOOP_ENTRIES`, `LOOP_BLOCKRULES`, `LOOP_PIN` and `LOOP_TRACE` are unset on both. Every build wants `-fforce-recomp` and a fresh `--builddir`, the switch being an environment change cabal does not see. **Under the exit span the shim's verbose line reads differently from what the declaration expected, and the difference is the fix that shipped with the switch.** `f1a5adb` stops an unconditional back edge's tail being read as the exit and charged, so on this run's own recipe all four emissions read `verified: 8 short loop(s) straddling (8 planned), 0 exit span(s) astride`, where the declaration expected eight astride and sixteen planned --- figures the PRE-FIX shim gives and which this run reproduced on that shim to check. The heads it places differently from the plain form are **398 on 9.12.4 and 287 on HEAD** under this run's recipe, where the declaration's 637 was the pre-stage-11, pre-fix tree's. **The pair declared that morning is deferred whole and not withdrawn**: Run 34 varies whether `-O2` is its two passes, one half plain `-O1` in the dead-spot form on ghc-9.12.4 --- `nospec` still naming what that half is --- against the same recipe with `--ghc-options="-fspec-constr -fliberate-case -fobject-determinism"` and nothing else changed, `twopass`, so that `--compare` reads nospec over twopass and every `cross` is what the two passes together do to one arm. **What the owner has to settle before it is built is whether both halves carry `LOOP_EXITSPAN=1`**: the declaration was written against Run 32's basis, which had no such switch, and the published basis is now this run's, which does. Either answer leaves the pair's variable alone --- both halves take the same shim environment, as every pair here does --- so this is a question about which basis Run 34's absolutes are read against and not about what it measures. **It is the pair Run 31's arithmetic wanted and neither Run 32 nor this run could supply.** Run 31 read `-O2` worth **1.2974** on `list` where `-fspec-constr` and `-fliberate-case`, measured one at a time on Runs 29 and 30, multiply to 1.3325 --- a 2.7-point overshoot that is either the level's other passes handing `list` back or an artefact of composing two runs' readings, and a pair with both passes on one half and neither on the other is the only thing here that tells them apart. **And what this run changes about the case for it is that the compiler question at plain -O1 is no longer nearly spent.** Run 32 read an arm geomean of 0.9985 with no arm past 3% and concluded a further compiler pair at this level had little left to find; under the exit span the same two compilers read **1.0068**, one arm past 3%, EIGHT of eight strategies past the run's own A/A bar, and a class arm at **1.2954** whose counted work is level to four decimals. So the compiler and the placement cost are entangled in a way neither Run 32 nor this run separates, and Run 34's `-O2` pair is not the only thing now waiting.

**The COMPILER variable has now been asked EIGHT times, and this run is the second to ask it at the level the library ships and the first to ask it under the exit span.** Runs 19 and 24 to 28 all varied it with `-fspec-constr` on BOTH halves: Run 24 read the two 5.7% and 6.8% apart on the instructions of two pure arms; Run 25 read `list` 1.10% apart in time and 0.33% in counts; Run 26 found twenty-four of twenty-six arms inside a percent in counts and the two `Ptr` arms outside at 0.6219 and 0.9295, which was GHC #27778; Run 27 worked it around and read every arm inside a percent; Run 28 confirmed it at a counted geomean of 1.0027. **Run 32 asked it at plain -O1 and got the cleanest null of them all; this run asks it again with the exit span on both halves and does not.** Run 32's arm geomean was 0.9985 with no arm past 3% and three of eight strategies clearing its A/A bar; this run reads **1.0068**, one arm past 3%, EIGHT of eight strategies clearing a bar of 0.16 points, and a class arm at **1.2954** whose counted work is level. The two runs share both compilers to the day and differ in one shim switch and two `Main.hs` commits, so what parts them is the switch, the source, or the interaction of the switch with what the compilers do --- and nothing in this pair separates those three. **The REGIME variable, meanwhile, has been asked three times and the arithmetic it left is still open.** Put in one orientation --- the unflagged half over the flagged --- Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**; on `bq-expand` the two passes MULTIPLY to 1.2967 against a measured 1.2943, 0.24 of a point apart, while on `list` they multiply to 1.3325 against 1.2974, 3.5 points apart on that same absolute reading. That arithmetic is an observation and not a subtraction, and Run 34's pair is what settles it.

**What Run 33 leaves the next run to read against, and the first item is a check that did NOT fire. The box is where Runs 28 to 32 left it**, and this run's gate says so: the machine check reads `list`'s net at **-0.25%** against the fingerprint Run 32 installed, worst `gather48-src-50` at -1.96%, 0 of 19 shapes past 5% and the geomean inside the 3% bar. **That reading is NOT like-for-like this run**, Run 32's published half being this basis less `LOOP_EXITSPAN=1` and `Main.hs` having moved at `f46867f` and `f31bd1c` under it, so it carries a switch term and a source term as well as the box's. Against `run32-nospec` itself the sixteen shared timed arms span **0.9817 to 1.0017** with `list` at **1.0014**, and the fifteen that are not `list` give a `--bridge` geomean of **0.9961**, none outside the 3.3% drift band Run 11 measured and none outside Run 23's narrower 2.1% either. So this run publishes INSIDE the third machine era rather than opening a fourth, an absolute crosses between it and Run 32's basis unadjusted, and the fingerprint below is the one a Run 34 machine check reads against. **What a Run 34 reading must not take from those sixteen arms is a box figure**: the shim moved and `Main.hs` moved between the two builds, so their 1.8% is the box's, the switch's and those commits' together and nothing here separates them. Only a pair whose halves share a source and a shim does that, which is what every pair here is for.

**Registered with the pair.** Run 33's seven registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. FOUR held, TWO were killed and ONE cannot be adjudicated against these builds. **What a next registration should take from this one is that an item may be unadjudicable before it is wrong, and that the preparation can see it coming.** (7) predicted what the shim's verbose line would say and was written against a shim that had since been fixed, so its kill condition --- a ninth exit span astride --- cannot fire where the shipped shim reports none at all; the preparation measured that a day early, reproduced both figures on the pre-fix shim to prove the reading, and flagged the item to the owner rather than amending it. (3) was flagged the same way and on the same evidence: its 0.81 sat sixteen points from the only reading this chapter had of those arms on that population, and it died at 0.9593. **So two of this run's seven were known to be in trouble before the machine was booked**, which is what a preparation that re-derives a registration's figures buys, and neither was silently repaired. So (3) died on its arithmetic, which the preparation had already priced, and (1) died on the measurement: it predicted level on the arms the switch was added to level, and they parted further. The four that held --- (2), (4), (5) and (6) --- are every other item that predicted level.

**The position term was the candidate Run 15 promoted, and the probes have since spent it.** What Run 14 first saw and Run 15 confirmed is resolved as small-pinned churn --- selector found, ladder re-sized, no poison set --- in [the position-term entry][open] and `small-pinned-churn-investigation/nursery-position-findings2.txt`, so the roster-order pair this paragraph used to ask for is not owed: the corrected scans priced the term per shape in filtered processes, without a pair and without a layout term to argue about.

**The allocation area has now been priced twice and does not want a third pair** --- a ruling superseded in scope, 2026-08-19, and kept because what it refused stays refused. Run 14 took the area at `-A1G` and could not subtract its halves' absolutes; Run 15 took it at `-A32m` and found the cost at about 6% of the roster's time --- so re-PRICING default-against-enlarged is spent, and Run 16's pair does not do that: it changes the published basis to `-A32m` and reads `-A64m` against it, the one comparison neither earlier pair made and the one the churn findings' recommendation turns on, in the saturated in-process state both halves share. On 2026-08-21 the area was fixed at `-A32m` outright, here and in every horde-ad suite, so the one-binary runner this section used to ask for is not owed, and no further `-A` question is the README's.

**Where a run changes basis, the new basis is checked against the half at its OWN allocation area and against no other**, which is the rule the Run 15 to Run 16 change settled and the one place *against the previous run* can still be ambiguous. **The six figures that follow are Run 16's, are no longer checkable, and are stamped so that no later run reads them as its own**, `run15-*` and `run16-*` having been deleted; they are kept as the evidence the ruling was taken on. Against `run15-a32m` Run 16's three anchors read **-0.66%, -1.01% and -0.06%**, every one well inside the 2.32% floor it measured; against `run15-lookrts` the same three would have read **+8.81%, -9.57% and +7.74%**, which is the allocation area and not the shapes, and would have put all three outside that floor for a reason that is not theirs. Distance from a half at another area is that area plus whatever else moved; only distance from the half at a run's OWN area is drift.

**A pair's two halves are never folded into one.** Merging them puts back, in the record built to outlive every artifact, exactly the term the pairing exists to separate --- and what a given pair's two columns price is that run's own file's to say, not this section's. `--check-doc` catches one half of it: a run named aligned must also be named unaligned. Pruning an aligned column, merging two, and naming a second half accurately are the reading's to catch --- the check cannot demand an unaligned half of every pair without failing the last two runs, which have none, nor an aligned column of every run without failing Runs 6 through 9, which had none either.

**The next run compares against Run 33 and against nothing before it.** Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it, and walking that chain here is what this section stopped doing. So an older run is read by opening its file, and the one step this run records is Run 32 to Run 33 --- **and it is a step between PUBLISHED bases that are NOT the same recipe**, this run having added `LOOP_EXITSPAN=1` to the one Run 32 published on. So that step is a bridge and not a subtraction, and it carries a shim term and a source term with it. Over the **16 arms both rosters time and both give a corrected time** --- not all of them, one having been added --- Run 32's basis over this one runs from **0.9817** on `lib-stage2-lean-u1` to **1.0017** on the shipped leaf --- below 1 meaning this run is the slower --- FIFTEEN of the sixteen inside 1% of 1 and that one outside, with `list` itself at **1.0014**. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one, and the two differing in ONE COMPILER and in nothing else. Its two columns MAY be differenced, `list` having moved 0.45 points between them, which is the second such table in this file in a row.
| strategy | Run 33 (plain -O1, dead-spot, exit span, -A32m, 9.12.4) | Run 33 (plain -O1, dead-spot, exit span, -A32m, GHC HEAD) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.045 |
| `mut-odo-vecdims-add-in-leaf-u1` | **0.029** | 0.027 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.027** | 0.026 |
| `lib-stage1` | **0.029** | 0.027 |
| `lib-stage2-lean` | **0.025** | 0.023 |
| `lib-stage2-lean-u1` | **0.029** | 0.025 |
| `bq-expand` | **0.127** | 0.127 |

**READ THE SECOND COLUMN AS A RATIO AND NOT AS A SPEED.** Every entry is that arm's net over `list`'s net in ITS OWN half, and `list` is 0.45 points faster under 9.12.4 --- so a control entry reading lower is very nearly the arm and not the denominator this run, which is what an unmoved reference buys. **That is still not an identity**: each entry is winsorized per row within its own half, so dividing an arm's two entries does not reproduce its `--compare` figure and is not meant to --- on `lib-stage2-lean` the two entries divide to about 0.92 where the cross reads 1.0354, which is the capping and not a disagreement, the control half capping five of that row's nineteen cells against the basis's four. The arm-by-arm reading of what the compiler is worth is in the head, off `--compare`, where the reference is not divided out.

**A published geomean is over the same 19 shapes, and two halves of one run usually share a denominator too**, `list` moving under 0.7% between them --- so such a pair may be subtracted and not merely ordered. **THE TABLE ABOVE IS SUCH A PAIR**, `list` having moved **0.45 points** on this run's main set, the second run running that this section's table could say so. **But the two columns do NOT print alike this time.** Five of the seven rows print lower on the control --- `lib-stage2-lean` 0.025 against 0.023, `lib-stage2-lean-u1` 0.029 against 0.025, `lib-stage1` and `mut-odo-vecdims-add-in-leaf-u1` 0.029 against 0.027, the shipped leaf 0.027 against 0.026 --- while `mut-odo-vecdims` prints 0.045 and `bq-expand` 0.127 on both. Read down a column and the ordering is nearly the same on both, head and foot alike: `lib-stage2-lean` leads each at 0.025 and 0.023, `mut-odo-vecdims` sits between at 0.045 twice, and `bq-expand` is at the foot at 0.127 twice. What differs is the middle of the basis column, where `lib-stage2-lean-u1` prints level with `lib-stage1` at 0.029 and the control puts it about half the way back to the leader. **That gap is the winsorizing and not the arms**: each half caps four of that row's nineteen cells, and the plain per-shape geomeans behind the two entries are 0.03038 and 0.02962, two and a half points apart where the printed figures are sixteen.

**The control half's own standings on the arms this run's roster carries, which no table here holds, every published table being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over all 19 main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `-u1` **0.9584** (0.9613) and against `mut-odo-vecdims` **0.6371** (0.6428); `lib-stage1` against `-u2` **1.0417** (1.0609); `lib-stage2-lean` against `-u2` **0.9782** at 14 of 19 (1.0017 at 15 of 19) and against `lib-stage1` **0.9391** at 15 of 19 (0.9442 at 16 of 19). **Four of the five hold their direction across the halves and the fifth changes it**: the lean fill is ahead of the shipped leaf by 2.2 points under HEAD and a shade behind it under 9.12.4, which is the one within-half ordering this pair's variable touches --- and it touches it by less than either half's own floor away from a tie, fifteen and fourteen shapes of nineteen favouring the lean fill on the two halves alike. Every other ordering this run publishes is the same under both compilers, which is the half of the run the 0.7% bar leaves standing on every population, the three past the bar included.

**Each stride class has its own table below.** Run 8 re-ran every class with the populations pinned, and every run since has again, so each class's paragraph carries what the last change moved and the table above it is what Run 13 reads against. **A class figure compared across the Run 11/Run 12 boundary is not compared on one build**: Run 11's class tables are its *aligned* half's and Run 12's its *max-skip* basis half's, and the main set prices that difference at nothing below 0.99 and up to 1.06, so a point or two of movement across that boundary is the shim rather than the class. From Run 13 on, every run's class tables are its own basis half's, this run's included.

**Two tables in this file are NOT installed and are edited by hand: the two-column one above and the cross-class summary below.** Every other table a run publishes comes from `install-tables.sh` and is replaced whole. The one above is replaced whole too, being this run's own halves and no earlier run's; the summary gains a row per run instead. A hand-edited table is edited with the whole line named, never with a prefix anchor. On Run 17 an insertion anchored on ``| `arm` | `` matched an earlier table and put two cells into the element-type probe's header and a loop-offsets row; `--check-doc`'s width pass caught it in the same call, which is the only reason it cost minutes. Name the whole row, assert it occurs exactly once, and read the width check's verdict afterwards.

And because a geomean cannot say *where* it moved, the **fingerprint** below is kept so a future disagreement can be localised rather than only noticed; its membership rule, the column heads and the rulings on dropping a column are [in the README's per-shape section][pershape]. The two tables below are installed from this run's own JSONs in the per-shape form the README describes, which replaced a fourteen-column one on 2026-09-04.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.29 us | 0.078 | `lib-stage2-lean-u1` 0.077 | `mut-odo-vecdims-add-in-leaf-u2` 0.054 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.69 us | 0.088 | `lib-stage2-lean-u1` 0.071 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 120 us | 0.062 | `lib-stage2-lean-u1` 0.033 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 386 us | 0.044 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `gather48-src-50` | 3 | 22500 | 459 us | 0.049 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.1 ms | 0.030 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.7 ms | 0.052 | `lib-stage2-lean` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `stretch-primes` | 89 | 250357 | 4.35 ms | 0.025 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 17.1 ms | 0.040 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.8 ms | 0.053 | `lib-stage2-lean` 0.031 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 20.1 ms | 0.031 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44.6 ms | 0.023 | `lib-stage2-lean-u1` 0.019 | `mut-odo-vecdims-add-in-leaf-u1` 0.019 |
| `stretch-pow2stride` | 64 | 1769472 | 31.2 ms | 0.112 | `lib-stage2-lean-u1` 0.110 | `mut-odo-vecdims-add-in-leaf-u1` 0.111 |
| `stretch-r5-8x432` | 8 | 1769472 | 48.6 ms | 0.021 | `lib-stage2-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 30.8 ms | 0.087 | `lib-stage1` 0.077 | `mut-odo-vecdims-add-in-leaf-u2` 0.078 |
| `stretch-bigstride` | 3 | 1800000 | 50.7 ms | 0.033 | `lib-stage2-lean` 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 39.5 ms | 0.058 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u1` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 41 ms | 0.021 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.7 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 939 us | 0.028 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29.2 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.5 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29.2 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35.4 ms | 0.016 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.5 ms | 0.057 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.66 ms | 0.052 | `lib-stage1` 0.010 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.24 ms | 0.019 | `lib-stage2-lean` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.9 ms | 0.034 | `lib-stage1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42 ms | 0.022 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u1` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.22 ms | 0.020 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.25 ms | 0.024 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.25 ms | 0.024 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-page` | `block` | 64 | 131072 | 2.34 ms | 0.028 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.45 ms | 0.020 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 949 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 938 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.7 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 29.8 ms | 0.021 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.35 ms | 0.026 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.34 ms | 0.026 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.72 ms | 0.052 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.6 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 30.2 ms | 0.024 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.4 ms | 0.047 | `lib-stage2-lean` 0.043 | `mut-odo-vecdims-add-in-leaf-u1` 0.037 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 120 us | 0.064 | `lib-stage2-lean-u1` 0.032 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 457 us | 0.048 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.35 ms | 0.025 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28.1 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.3 ms | 0.025 | `lib-stage1` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.7 ms | 0.025 | `lib-stage1` 0.024 | `mut-odo-vecdims` 0.025 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.7 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-512` | `runs` | 512 | 1799680 | 28.8 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-256` | `runs` | 256 | 1799936 | 28.9 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-7` | `runs` | 7 | 1799994 | 32.9 ms | 0.032 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-2` | `runs` | 2 | 1800000 | 39.6 ms | 0.057 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u1` 0.024 |
| `runs-3` | `runs` | 3 | 1800000 | 35.7 ms | 0.047 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.1 ms | 0.041 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u1` 0.023 |
| `runs-5` | `runs` | 5 | 1800000 | 33.2 ms | 0.038 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-9` | `runs` | 9 | 1800000 | 31.8 ms | 0.030 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-96` | `runs` | 96 | 1800000 | 29.2 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.5 ms | 0.026 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 271 us | 0.029 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.06 ms | 0.023 | `lib-stage1` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.15 ms | 0.028 | `lib-stage2-lean-u1` 0.030 | `mut-odo-vecdims` 0.028 |
| `small-patch-k5` | `small` | 5 | 150 | 2.93 us | 0.077 | `lib-stage1` 0.098 | `mut-odo-vecdims-add-in-leaf-u2` 0.057 |
| `small-bcast32` | `small` | 32 | 256 | 4.43 us | 0.049 | `lib-stage1` 0.063 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `small-flat64` | `small` | 64 | 256 | 4.42 us | 0.059 | `lib-stage2-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.055 |
| `small-patch-r5` | `small` | 4 | 256 | 5.34 us | 0.087 | `lib-stage2-lean-u1` 0.096 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `small-row96` | `small` | 96 | 384 | 6.46 us | 0.041 | `lib-stage2-lean` 0.055 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `window-28x28-k5` | `window` | 5 | 14400 | 279 us | 0.040 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 953 us | 0.084 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.42 ms | 0.052 | `lib-stage1` 0.031 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.73 ms | 0.050 | `lib-stage1` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.029 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.83 ms | 0.051 | `lib-stage1` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.029 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.6 ms | 0.052 | `lib-stage1` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.3 ms | 0.054 | `lib-stage1` 0.032 | `mut-odo-vecdims-add-in-leaf-u1` 0.031 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.8 ms | 0.031 | `lib-stage2-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-three rows is a geomean over fewer shapes than the rest, as on Run 32 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the THIRTEEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, `libunord-stage11-sum` being the thirteenth and landing this run --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside family` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names `lib-stage2-lean` on EIGHT and `lib-stage1` on two --- `rev` and `scaled` --- where Run 32 named `lib-stage1` on three, `bcastmid` having moved to the lean fill this run. The cross-class summary's `best outside family` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 33's verdicts** over ten classes, the details beside each class's table:

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **The first held in every one of the eleven populations on both halves; the second held in all ten classes on both halves and PARTED BETWEEN THE HALVES on the main set again**, as on Run 32 and where Run 31 broke it on both. On the MAIN SET `mut-odo-vecdims` is BEHIND `bq-expand` on `stretch-pow2stride` by **0.07 of a point** on the basis, at **1.0007**, and ahead by 0.39 on the control, at **0.9961** --- which is Run 32's reading with the halves exchanged, that run having been ahead at 0.9934 on its basis and behind at 1.0003 on its control. Run 31 read the cell at 1.0009 and 1.0109 and Run 30 at 0.9997, so four runs have now read it within a point and a quarter of a tie and which side of 1 it lands on has changed four times; every one of those margins is inside the floor of the half it was read on, 0.07 against 0.47% here. The `worst` clause holds in every regime, roster, compiler and layout the README has run, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population. The `bq-expand` clause folded in on 2026-09-06 from the ordering that was property 2 until then, strengthened from a geomean to every shape, and is read that way here for the sixth time.

Beside property 1, and the case has simplified twice --- the prune of 2026-09-04 parked the arm that used to be half of it, and the retirement of 2026-09-09 took four of the five arms that broke the rest: **exactly ONE arm now breaks the WIDER statement this class set is really read for --- that no arm the library would ship is slower than `list` on any shape --- and it is the route the library ships.** `lib-stage1` carries a `worst` of **1.118** on `runs` on the basis and **1.066** on the control, and one cell does it on each: `runs-2`, at those same two figures. **The two halves part by five points on that cell**, where Run 32's read 1.1058 and 1.1071 and parted by one thousandth, so what the compiler is worth to the shortest run is the one place this property's break is not compiler-blind. `gen-unsafe` and its twins carried a `worst` above 1 in seven of ten populations and were the baseline's own controls rather than the property failing; every one of them is parked. Of the five library-shaped arms Run 27 found breaking it at `runs-2` --- `libunord-stage1` 1.237, `liblist-stage1` 1.214, `lib-stage1` 1.198, `liblist-stage2` 1.078 and `libunord-stage2` 1.076 --- four are retired to `check` and are not timed here. Those five figures are RECOMPUTED from Run 27's own cells, that run's prose and its own installed table having printed different ones, and the five are FIVE of NINE library-shaped arms over `list` there rather than the largest five.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries, registered strict on 2026-09-06 and given the margin on 2026-09-07 at its first reading: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves, which is the third run running that this property is the one left entirely alone.** The `list` clause is closest at `small-patch-k5`, 0.05918, with the other four `small` shapes between 0.0530 and 0.0592 and every shape outside `small` under 0.048. The `bq-expand` clause is closest at `scaled-rank1-m1`, 1.00003, then `bcast-src8` at 0.99999 and `flip-whole-square` at 0.99703 --- the same cells Runs 30 to 32 read, inside the margin the strict form would have failed on, which is why the margin is there and why it is not widened further.

3. **The allocation tiers survive, their ORDER is unbroken in all ten classes and on the main set, and this run their LEVELS are again identical on the two halves cell for cell; what `small` is outside is the LEVEL clause and not the order one**, by the ruling of 2026-09-07, it being the class built to break it and read here for what it shows: the mutable fills at the result vector, `bq-expand` between 1.00x and 3.86x it, `list` an order of magnitude above at 20.99x to 27.66x. On the main set the fills read 1.00x, `bq-expand` **2.78x** and `list` **25.20x**, which are a plain -O1 half's levels as Runs 30's, 31's and 32's were --- **and the control half reads the same 2.78x and 25.20x, and the same triple in every one of the ten classes**, `small`'s 1.27x family included. NO REGISTRATION OF THIS RUN NAMES ALLOCATION, Run 32's item (10) having been the last; the reading is taken anyway because it is free and because it is what would show a compiler changing what an arm allocates rather than how fast it runs. It shows none: `--alloc` puts 456 of the 589 allocating cells inside 1e-4 between the halves, worst 2.17e-02 on `stretch-tall-Mx2/libunord-stage11-sum`, with the 38 cells under 100 bytes a call set aside as a property of fitting a near-zero allocation. The fills and the `liblist` consumers read 1.00x and the `libunord` consumers 0.00x on both halves, unmoved. **What this roster removes is the 2.00x tier**, whose members were the list Fill arms now checked and not timed.

`--pair` works within a class JSON exactly as within the main one, and is still the way to compare two arms; its bootstrap interval, over three shapes, is worth less there than its win count.

Two notes on the columns. The `needs` column splits the class-method tier in two. A **new pure `Vector` method** delegates to a pure function the vector package already ships for every carrier --- `unfoldrExactN`, `backpermute`, the `concatMap`/`enumFromStepN` pipeline --- so it fights only *minimal* in orthotope's pure-and-minimal API rule; the **new mutating `Vector` method** the direct fills need is the [mutable ceiling](../README.md#the-mutable-ceiling-taken)'s ask, which *pure* barred outright until the amendment there turned the bar into a weight, and which the decision of 2026-08-22 takes. `offtab` is the `Vector`-class-expressible shape of these gathers --- output by plain `vGenerate` over a concrete offset table --- so its own cell names only its mutable `Int` scratch. And the geomean weights every benchmarked shape **equally**, so a figure here is a ranking statistic, not a claim about total work saved: the small shapes count as much as the largest.


## The stride classes, run by run

**Run 33 (GHC HEAD against ghc-9.12.4, both at plain -O1, dead-spot, exit span, -A32m) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. **This run those lines say more than usual, and they say why.** `list` moved between the halves by 0.16 of a point on `window` at narrowest and 1.09 on `scaled` at widest, so SEVEN of the ten classes sit INSIDE the 0.7% that lets two columns be differenced and their cross-half readings are readings of the pair's variable rather than orderings --- where every one of Runs 29's, 30's and 31's was disqualified and six of Run 32's were not. The three past the bar are `rev` at 0.9918, `compose` at 1.0081 and `scaled` at 1.0109. Over the ten classes the reader counts **160 arm-comparisons, 62 putting the basis faster and 98 slower**, with no degenerate arm excluded, at geomeans from **1.0001** on `bcastmid` to **1.0184** on `runs` and extremes of `mut-odo-vecdims-add-in-leaf-u1` at 0.9361 on `compose` and `lib-stage2-lean-u1` at 1.2954 on `runs`; the low extreme is that leaf arm in 5 of the 10. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control is the faster, as the head's do. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **Two items read EVERY class** --- (2) and (5) --- so each block below has those two whatever else it carries, and (1) and (3) name `runs` and `window` alone.

First, one table over all of them, so that an inversion is visible without reading every class's table. Every figure in it is transcribed from a class's own table below --- none is computed here, and none is an average across classes, there being no such population to average over. Its header, fixed here so a run fills rows and never reshapes columns:

    | class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |

That header line is written out twice in this file, once here as the spec and once as the table's own, and the two are the same text --- so a session pasting a run's rows must anchor at the line start and check that it landed on the unindented one. Getting that wrong put Run 8's rows under this paragraph and left Run 7's standing in the table, both checks passing, because the check looked the table up the same wrong way the paste did.

`mut-odo-vecdims` and `worst` are that arm's two columns in that class's table; *best outside family* is the leading arm outside the vecdims family, what the dropped stride-conditioned redirect would have taken, and *ceiling* the leading arm OF the family, each with its name --- and both are read over the POPULATION, so the arm named here may lead on no single shape and the per-shape fingerprint below may name another, which is [the README's per-shape section][pershape]'s own point and not a disagreement --- a column of this table and not the eight-run ratio the head calls the ceiling, which is `mut-odo-vecdims` against the fastest arm needing nothing at all and which this run cannot read --- since which arm leads is half of what the column says --- so where an arm outside the family leads, the two name different arms and the gap between them is what the lead is worth, and Run 21's table, which repeated one arm in both columns on `bcastmid` and `reshape1`, was wrong to; *floor* is the largest deviation from 1 among that process's A/A controls. A cell that breaks property 1, or that leads `mut-odo-vecdims` --- what broke the ordering that was property 2 until 2026-09-06 ([the properties](#the-properties-the-next-run-should-test)) --- is bolded. **In practice that marks the FASTER of the two named arms, one cell a row**: the arm outside the family on FIVE of the ten --- `rev` and `scaled`, where `lib-stage1` leads, and `bcast`, `bcastmid` and `flip`, where `lib-stage2-lean` does --- and the family's own ceiling on the other FIVE, `window`, `runs`, `block`, `small` and `compose`, where the ceiling is faster. **The two pointer leaves held five of Run 30's six bolded ceilings and are parked**, so every bolded ceiling here is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` itself, which is the form the family would ship. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

**And the aggregate figures in the paragraph above the blocks are the reader's, emitted rather than assembled.** `./read-run.py --cross-classes --classes BASIS... --others CONTROL...` prints every one of them --- the comparison count, the faster/slower split, the range of the geomeans with the class at each end, the arm holding each extreme and how many populations share it, the degenerate arms it kept out, and the classes whose `list` is past the 0.7% bar --- from the same per-class rows the cross-half lines below print, so the intro and the blocks cannot part. The comparison count, the faster/slower split, the range of the geomeans and the extreme arms are each an aggregate over the `--block --compare` lines below, one per class, so they are read off those lines and never off a population assembled for the purpose: Run 20 assembled its own twice and was wrong both times --- once on the split, once on a low end that excluded a class the sentence said it covered. Where a figure genuinely cannot come off those lines, because a class's own maximum is a degenerate cell, the paragraph says so rather than quoting it as though it could.

Then one block per class, in `classViews`' order --- which `Main.hs` fixes and this file follows, so a class landing or retiring moves the blocks and not a list here --- each carrying the same six things and nothing else:

1. a bolded lead naming the class, the mechanism it models in a clause, and its shapes with their `l` and `sInner`, which is what makes the table under it readable without `Main.hs` open;
2. the table `--block --in-place` installs from `$R-<basis>-$c.json`, whole and never edited --- six columns, with the emphasis carried over from the main table so the `mut-odo-vecdims` row is found at a glance, and `needs` left to that table as a property of a strategy rather than of a population;
3. its own controls, off `--aa`: the A/A deviations with their spans, the two `sum-only` halves, and the in-situ term from the `-nosum` arms --- this process's own floor and its own three gates, neither inherited nor lent --- and where the paragraph quotes the OTHER half's figure, it says so in the form `the other half's own six pairs span N%` and never with the word *floor* beside the number, which `--check-doc` holds to this table's column (Run 23 was refused four times before it learned the shape);
4. its provenance and its anchor: elapsed time and the two heap peaks from that process's stderr line, its population's size from the reader's first line ([why not both from one place](../README.md#making-a-major-benchmark-run)), and `list`'s absolute per-call time on one of its shapes, raw and net. The main set's three anchors guard a baseline that moves for every population at once; this one guards a baseline that could move for this mechanism alone, which is the case a table of ratios hides completely. A three-shape class adds one line here --- the bolded rows' per-shape net ratios, in the lead's shape order --- because its table under-determines its cells, where a two-shape table carried them already, `time` and `worst` jointly fixing both; every class is three shapes or more now, so the line always prints;
5. the cross-half reading, one line, which `--block --compare` against the other half's JSON now emits and `install-tables.sh` writes in with the other three --- how many of the population's arms move, which way, and the spread; a margin on this line is judged against the WIDER of the two halves' floors ([README, the floor section][floor]). Both halves have run every class since 2026-08-14 and this is where that is read: a pair's variable can act on a class and not on the main set, which is how Run 14 answered its `scaled` question. A run whose halves differ in nothing a class can see says so in a clause;
6. one paragraph of what the class says, and none where it says nothing: an ordering that inverted, a `worst` above 1, an allocation tier that moved, a mechanism showing through a single cell. A class that reproduces the main ordering gets one sentence saying so, that being a result and reading as one.

`./read-run.py RUN.json --block --compare OTHER.json` assembles items 3 through 5's mechanical parts, and `install-tables.sh` writes them in in one call --- table, controls, the provenance and anchor skeleton, a three-shape population's per-shape line, and the cross-half line; the lead and the paragraph stay the author's, a skeleton writing no findings. Item 2's own table is NOT among what that call prints, which is why the list above starts where it does: it comes from the separate `--block --in-place` call item 2 itself names. **The cross-half line carries its own disqualification**: where `list` moves more than 0.7% between the halves the line says so and says it is not read for the pair's variable --- a reading Run 18 needed, and which no other output showed.

The blocks carry no headings of their own. One per class would crowd the contents and the replace list alike, where a bolded lead reads the same and lets one link cover the section --- which is what `--check-doc`'s coverage check counts.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.042 | 0.064 | **`lib-stage1`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 0.64% |
| `bcast` | 6 | 0.021 | 0.057 | **`lib-stage2-lean`** 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 0.82% |
| `bcastmid` | 4 | 0.029 | 0.052 | **`lib-stage2-lean`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 0.96% |
| `window` | 8 | 0.051 | 0.084 | `lib-stage2-lean` 0.028 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.028 | 0.55% |
| `scaled` | 3 | 0.026 | 0.029 | **`lib-stage1`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 | 0.70% |
| `runs` | 14 | 0.027 | 0.057 | `lib-stage2-lean` 0.024 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.024 | 3.11% |
| `flip` | 6 | 0.028 | 0.052 | **`lib-stage2-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 0.71% |
| `block` | 5 | 0.023 | 0.028 | `lib-stage2-lean` 0.021 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.021 | 0.17% |
| `small` | 5 | 0.060 | 0.087 | `lib-stage2-lean` 0.056 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.052 | 0.14% |
| `compose` | 4 | 0.024 | 0.029 | `lib-stage2-lean` 0.015 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.015 | 0.67% |

The floor-movement paragraph that stood here was cut on 2026-08-22, having read Run 16's column against Run 15's while Run 17 installed this one over it --- the defect `--check-doc` now holds every such movement to. What moves these floors is [an open question](../README.md#what-is-open) and not a sentence under a table.

The pure slot this table carried until 2026-08-22, and the paragraph that read it, retired with the pure/impure distinction when the decision shipped the mutable family's arm; the column now carries the best arm outside the family, which the table above gives per class and which is ahead of `mut-odo-vecdims` in every one of the ten --- the lead that broke the ordering property 2 carried until 2026-09-06. **On FIVE rows --- `window`, `runs`, `block`, `small` and `compose` --- the bold sits in the CEILING column instead**, and this run it names ONE arm on all five, the shipped leaf `mut-odo-vecdims-add-in-leaf-u2`, where Run 30's six named three; `scaled` moved out of that set this run and `bcastmid` changed the arm it names outside the family. The reader's convention counts a `mut-odo-vecdims` sibling as the family's and so as no break; this file overrides it for the two pointer fills, which the dead-ideas ruling refuses as a design rather than as a form the family could ship --- an override no row here exercises, both of them having been parked on 2026-09-13. **FOUR rows tie at three decimals** --- `window` at 0.028, `runs` at 0.024, `block` at 0.021 and `compose` at 0.015 --- and the bold on each is `--block`'s own, computed on the unrounded values where the printed ones cannot separate: 0.02819 against 0.02751, 0.02428 against 0.02421, 0.02123 against 0.02121 and 0.01469 against 0.01452, every one of the four falling to the ceiling.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.10* | *127* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.09 | 147 | 1.01x |
| liblist-stage2-sum | -- | -- | 0.08 | 147 | 1.01x |
| liblist-stage3-sum | -- | -- | 0.14 | 147 | 1.01x |
| liblist-stage4-list-sum | -- | -- | 0.13 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.10 | 147 | 1.01x |
| libunord-stage1-sum | -- | -- | 0.09 | 146 | 1.03x |
| libunord-stage10-list-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage10-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage11-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.04 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.17* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage1 | 0.021 | 0.047 | 0.09 | 147 | 1.01x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.043* | *0.13* | *147* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.043 | 0.09 | 147 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.043* | *0.06* | *147* | *1.00x* |
| lib-stage2-lean | 0.022 | 0.033 | 0.15 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.025 | 0.032 | 0.09 | 147 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.027 | 0.044 | 0.17 | 146 | 1.00x |
| *mut-odo-vecdims-aa* | *0.042* | *0.063* | *0.09* | *138* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.063* | *0.09* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.042** | 0.064 | 0.08 | 138 | 1.00x |
| *bq-expand-aa-adjacent* | *0.138* | *0.229* | *0.10* | *122* | *3.22x* |
| bq-expand | 0.138 | 0.230 | 0.12 | 122 | 3.22x |
| *bq-expand-aa-distant* | *0.138* | *0.231* | *0.12* | *122* | *3.22x* |
| *list-aa-adjacent* | *0.997* | *1.002* | *0.18* | *86* | *26.11x* |
| *list-aa-distant* | *0.999* | *1.003* | *0.23* | *85* | *26.11x* |
| list (baseline) | 1.000 | 1.000 | 0.30 | 85 | 26.11x |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa` at 0.9936, worst cell 1.76% on `rev-cnn-L1-24x24-c1`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9991 on a worst cell of 0.22% on `rev-gather48-src-50`, its interval missing 1. The in-situ term reads 0.9983, 1.0130 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9955, which the correction amplifies by 1.71x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m36s, peak 96 MiB in use, 25 MiB max residency; the reader reads 33 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.5 ms per call raw, 4.35 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.064/0.048/0.025

**Across the halves:** 7 of the 16 arms are faster on this half and 9 slower, at a geomean of 1.0086, from `list-aa-adjacent` at 0.9835 to `lib-stage1` at 1.0508, with `list` itself at 0.9918. **The baseline moved 0.82% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.064, tiers at 1.00x, 3.22x and 26.11x, identical on the control --- and `lib-stage1` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.6468 over 3 of 3 shapes at sign p 0.25, a margin of 35.32% against this class's 0.64% floor (`mut-odo-vecdims-aa`), the fourth tightest of the ten. **What is this class's own is the extra pass over the axes, visible here for the sixth run running.** `rev` negates every stride and carries no zero stride and no pair of axes tied on stride, so `zerosOutermost` hands its list back unchanged, `routeUnord10` is `routeUnord7` to the byte, and only the walk over the axes separates the dispatches. **This class is one of the three whose two columns may NOT be differenced**, `list` having moved **0.82 points** between the halves against a 0.7% bar, so its cross-half line is an ordering. Its counted work is level at 1.0066 over the sixteen timed arms, and its widest cross-half figure is `lib-stage1` at 1.0508 against an A/A bar of 0.83 points --- four of the eight strategies clearing that bar here.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it; this run reads the class for stage ten instead, at item (6).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.60* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.51 | 62 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.50 | 62 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.50 | 62 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.51 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.41* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage2-lean | 0.015 | 0.020 | 0.50 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.51* | *62* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.42* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.42 | 62 | 1.00x |
| lib-stage1 | 0.016 | 0.020 | 0.40 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.024 | 0.51 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.018 | 0.020 | 0.44 | 61 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.057* | *0.32* | *61* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.021* | *0.057* | *0.34* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.021** | 0.057 | 0.10 | 61 | 1.00x |
| bq-expand | 0.091 | 0.141 | 0.67 | 46 | 1.00x |
| *bq-expand-aa-adjacent* | *0.091* | *0.140* | *0.72* | *46* | *1.00x* |
| *bq-expand-aa-distant* | *0.092* | *0.143* | *0.24* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.17 | 17 | 20.99x |
| *list-aa-distant* | *1.008* | *1.028* | *0.91* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.008* | *1.016* | *0.83* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0082, worst cell 1.63% on `bcast-src8`, and 2 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.06% on `bcast-src8`, its interval covering 1. The in-situ term reads 1.0182, 1.0167 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0079, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h17m10s, peak 169 MiB in use, 42 MiB max residency; the reader reads 33 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.5 ms per call raw, 29.5 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.028/0.019/0.057/0.016/0.019/0.019

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0025, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9949 to `mut-odo-vecdims-aa-distant` at 1.0136, with `list` itself at 0.9982.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.057, tiers at 1.00x, 1.00x and 20.99x, identical on the control --- and `lib-stage2-lean` leads outside the family at 0.015, priced against `mut-odo-vecdims` at 0.6522 over 6 of 6 shapes at sign p 0.031, a margin of 34.78% against this class's 0.82% floor (`list-aa-adjacent`). **What is this class's own is that both routes fill**, an innermost stride of 0 sending the lean dispatch and stage one down the same path, which is why `bq-expand` sits at the fills' own 1.00x tier here and nowhere else. **Its two columns MAY be differenced**, `list` having moved 0.18 of a point, and they say very little: the class geomean is 1.0025, fourth tightest of the ten, and only two of the eight strategies clear an A/A bar of 0.40 points.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.41* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.33 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.34 | 82 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.33 | 82 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.35 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.36 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.32 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.29 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.33 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 96 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.39* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *88* | *0.00x* |
| lib-stage2-lean | 0.012 | 0.017 | 0.36 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.018 | 0.35 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.019 | 0.31 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.35* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.030* | *0.30* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.030 | 0.29 | 80 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.022 | 0.030 | 0.39 | 78 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.052* | *0.26* | *76* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.27* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.052 | 0.22 | 76 | 1.00x |
| *bq-expand-aa-adjacent* | *0.098* | *0.181* | *0.43* | *61* | *1.92x* |
| bq-expand | 0.098 | 0.181 | 0.44 | 61 | 1.92x |
| *bq-expand-aa-distant* | *0.099* | *0.180* | *0.35* | *61* | *1.92x* |
| *list-aa-adjacent* | *0.999* | *1.001* | *0.77* | *28* | *23.56x* |
| list (baseline) | 1.000 | 1.000 | 0.82 | 28 | 23.56x |
| *list-aa-distant* | *1.003* | *1.008* | *0.81* | *28* | *23.56x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0096, worst cell 3.48% on `bcastmid-b200k`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.06% on `bcastmid-block150k`, its interval missing 1. The in-situ term reads 1.0184, 1.0598 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0077, which the correction amplifies by 1.29x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h11m30s, peak 123 MiB in use, 35 MiB max residency; the reader reads 33 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 48.9 ms per call raw, 47.9 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.052/0.019/0.034/0.022

**Across the halves:** 8 of the 16 arms are faster on this half and 8 slower, at a geomean of 1.0001, from `list-aa-adjacent` at 0.9897 to `mut-odo-vecdims-add-in-leaf-u2` at 1.0110, with `list` itself at 0.9931.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.052, tiers at 1.00x, 1.92x and 23.56x, identical on the control --- and `lib-stage2-lean` leads outside the family at 0.012, priced against `mut-odo-vecdims` at 0.4157 over 4 of 4 shapes at sign p 0.12, a margin of 58.43% against this class's 0.96% floor (`bq-expand-aa-distant`), the widest margin of the ten. **THE LEADER OUTSIDE THE FAMILY CHANGED HERE**, `lib-stage1` having held it on Run 32 and the lean fill taking it this run, which is the only one of the ten summary rows whose named arm moved. **Its two columns MAY be differenced**, `list` having moved 0.69 of a point, and this is the class closest to level of all eleven populations: a cross-half geomean of **1.0001**, with three of eight strategies past a 0.72-point A/A bar.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.34* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.18 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.18 | 82 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.17 | 82 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.17 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.17 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.19 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.04 | 102 | 0.03x |
| libunord-stage10-sum | -- | -- | 0.05 | 102 | 0.03x |
| libunord-stage11-sum | -- | -- | 0.04 | 102 | 0.03x |
| libunord-stage6-loop-sum | -- | -- | 1.67 | 89 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.08 | 101 | 0.03x |
| libunord-stage7-sum | -- | -- | 0.06 | 102 | 0.03x |
| libunord-stage9-sum | -- | -- | 0.08 | 101 | 0.03x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.28* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *97* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.031* | *0.16* | *82* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.031* | *0.18* | *82* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.028 | 0.031 | 0.16 | 82 | 1.00x |
| lib-stage2-lean | 0.028 | 0.032 | 0.21 | 82 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.028 | 0.031 | 0.18 | 82 | 1.00x |
| lib-stage1 | 0.028 | 0.032 | 0.17 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.029 | 0.033 | 0.22 | 82 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.084* | *0.17* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.084 | 0.15 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.051* | *0.084* | *0.17* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.174* | *0.217* | *0.37* | *57* | *3.86x* |
| bq-expand | 0.174 | 0.215 | 0.33 | 57 | 3.86x |
| *bq-expand-aa-distant* | *0.174* | *0.215* | *0.30* | *57* | *3.86x* |
| *list-aa-distant* | *0.998* | *1.010* | *0.47* | *30* | *27.66x* |
| list (baseline) | 1.000 | 1.000 | 0.46 | 30 | 27.66x |
| *list-aa-adjacent* | *1.002* | *1.013* | *0.40* | *30* | *27.66x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9945, worst cell 1.59% on `window-224x224-k3`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.08% on `window-28x28-k5`, its interval covering 1. The in-situ term reads 1.0048, 1.1463 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9971, which the correction amplifies by 2.01x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h22m50s, peak 130 MiB in use, 52 MiB max residency; the reader reads 33 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.8 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.084/0.031/0.052/0.050/0.054/0.052

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0172, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9949 to `lib-stage1` at 1.0658, with `list` itself at 1.0016.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.084, the second highest of the ten behind `small`'s, and tiers at 1.00x, 3.86x and 27.66x, identical on the control --- and the family's ceiling and the best arm outside it TIE at 0.028, `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2`, the bolding going to the ceiling on the unrounded figures. The lean fill is priced against `mut-odo-vecdims` at 0.4851 over 8 of 8 shapes at sign p 0.0078, a margin of 51.49% against this class's 0.55% floor. **What is this class's own is that it carries the pair's second largest movement**: a cross-half geomean of **1.0172**, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9949 to `lib-stage1` at 1.0658, five of the eight strategies past a 0.36-point A/A bar, and a counted geomean of 1.0098 --- the largest of the eleven populations and still under a percent, so most of that movement is not instructions either. **Its two columns MAY be differenced**, `list` having moved 0.16 of a point. Registration (3)'s `window` clauses split here: stage nine holds at 0.8889 inside its 6%, stage ten misses 1.0 within 3% at 0.9686.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.07* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.11 | 128 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.17 | 127 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.13 | 127 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.16 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.18 | 127 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.13 | 127 | 1.01x |
| libunord-stage10-list-sum | -- | -- | 0.11 | 128 | 1.00x |
| libunord-stage10-sum | -- | -- | 0.14 | 128 | 1.00x |
| libunord-stage11-sum | -- | -- | 0.15 | 127 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.15 | 127 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.18 | 127 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.10 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.14 | 127 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *146* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *138* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.030* | *0.15* | *128* | *1.00x* |
| lib-stage1 | 0.022 | 0.030 | 0.15 | 128 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.023 | 0.030 | 0.18 | 127 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.023* | *0.030* | *0.22* | *127* | *1.00x* |
| lib-stage2-lean | 0.024 | 0.030 | 0.14 | 127 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.025 | 0.030 | 0.14 | 127 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.030 | 0.17 | 126 | 1.00x |
| *mut-odo-vecdims-aa* | *0.026* | *0.029* | *0.10* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.026** | 0.029 | 0.10 | 127 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.029* | *0.08* | *127* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.090* | *0.099* | *0.07* | *111* | *1.21x* |
| bq-expand | 0.090 | 0.099 | 0.07 | 111 | 1.21x |
| *bq-expand-aa-distant* | *0.090* | *0.099* | *0.07* | *111* | *1.21x* |
| list (baseline) | 1.000 | 1.000 | 0.22 | 69 | 21.49x |
| *list-aa-adjacent* | *1.000* | *1.004* | *0.15* | *69* | *21.49x* |
| *list-aa-distant* | *1.003* | *1.003* | *0.25* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9930, worst cell 1.73% on `scaled-super-r3`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9990 on a worst cell of 0.26% on `scaled-super-r3`, its interval covering 1. The in-situ term reads 1.0243, 1.0037 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9972, which the correction amplifies by 2.43x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m37s, peak 109 MiB in use, 28 MiB max residency; the reader reads 33 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.33 ms per call raw, 5.15 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.028/0.029

**Across the halves:** 9 of the 16 arms are faster on this half and 7 slower, at a geomean of 1.0005, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9817 to `lib-stage2-lean-u1` at 1.0506, with `list` itself at 1.0109. **The baseline moved 1.09% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.029, joint second lowest of the ten with `compose`'s, and tiers at 1.00x, 1.21x and 21.49x, identical on the control --- and `lib-stage1` leads outside the family at 0.022, priced against `mut-odo-vecdims` at 0.9203 over 2 of 3 shapes at sign p 1, a margin of 7.97% against this class's 0.70% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). **What is this class's own is how little separates anything in it**: the plain arm reads 0.026 and the leader 0.022, and the class's cross-half geomean is **1.0005** with only two of eight strategies past an A/A bar of 1.32 points, the joint widest of the ten with `flip`'s. **This class is one of the three whose two columns may NOT be differenced**, `list` having moved **1.09 points**, so its cross-half line is an ordering. Its A/A slot on `scaled-super-r3` is the hazard the README's own entry describes and is not read as a figure here.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven and on Run 24 to fourteen.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.47* | *52* | *1.13x* |
| liblist-stage1-sum | -- | -- | 0.13 | 65 | 0.19x |
| liblist-stage2-sum | -- | -- | 0.11 | 69 | 0.16x |
| liblist-stage3-sum | -- | -- | 0.03 | 71 | 0.00x |
| liblist-stage4-list-sum | -- | -- | 0.02 | 71 | 0.00x |
| liblist-stage4-sum | -- | -- | 0.02 | 71 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.18 | 65 | 0.19x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 71 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.03 | 71 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 71 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.05 | 69 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 71 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 71 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 71 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *78* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.50* | *59* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.025* | *0.09* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.025 | 0.11 | 59 | 1.00x |
| lib-stage2-lean | 0.024 | 0.026 | 0.12 | 59 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.025 | 0.026 | 0.14 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.057* | *0.09* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.027** | 0.057 | 0.09 | 59 | 1.00x |
| *mut-odo-vecdims-aa* | *0.027* | *0.057* | *0.09* | *59* | *1.00x* |
| lib-stage2-lean-u1 | 0.033 | 0.038 | 0.12 | 56 | 1.00x |
| lib-stage1 | 0.093 | 1.118 | 0.18 | 55 | 1.19x |
| *bq-expand-aa-distant* | *0.097* | *0.143* | *0.03* | *46* | *1.13x* |
| bq-expand | 0.097 | 0.141 | 0.42 | 46 | 1.13x |
| *bq-expand-aa-adjacent* | *0.097* | *0.141* | *0.54* | *46* | *1.13x* |
| list (baseline) | 1.000 | 1.000 | 2.49 | 16 | 21.32x |
| *list-aa-distant* | *1.030* | *1.047* | *0.39* | *17* | *21.32x* |
| *list-aa-adjacent* | *1.031* | *1.047* | *0.19* | *17* | *21.32x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0311, worst cell 4.68% on `runs-r3-48x30`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0003 on a worst cell of 0.30% on `runs-r3-48x30`, its interval covering 1. The in-situ term reads 1.0266, 1.0230 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0300, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h39m58s, peak 565 MiB in use, 247 MiB max residency; the reader reads 33 benchmarks over 14 shapes of the runs class. Anchor: `runs-2`, `list` at 40.7 ms per call raw, 39.6 ms net.

**Per shape, in the run's shape order (runs-2, runs-3, runs-4, runs-5, runs-7, runs-9, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.047/0.041/0.038/0.032/0.030/0.025/0.025/0.025/0.025/0.025/0.025/0.024/0.026

**Across the halves:** 7 of the 16 arms are faster on this half and 9 slower, at a geomean of 1.0184, from `list-aa-distant` at 0.9949 to `lib-stage2-lean-u1` at 1.2954, with `list` itself at 0.9951.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.057, tiers at 1.00x, 1.13x and 21.32x, identical on the control --- and the family's ceiling and the best arm outside it TIE at 0.024, `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2`, the bolding going to the ceiling. The lean fill is priced against `mut-odo-vecdims` at 0.7990 over 8 of 14 shapes at sign p 0.79, a margin of 20.10% against this class's **3.11%** floor (`list-aa-adjacent`), by far the widest floor of the ten and the reason margins here are read with more room than anywhere else. **THIS CLASS CARRIES THE RUN'S LARGEST CROSS-HALF FIGURE AND THE COUNTS SAY IT IS NOT CODEGEN**: `lib-stage2-lean-u1` reads **1.2954**, the basis slower on all fourteen shapes, with a counted ratio of **1.0000** --- while the class geomean is 1.0184 and its counted geomean 1.0025. No registration names that arm here. **Its two columns MAY be differenced**, `list` having moved 0.49 of a point. Registration (3) DIES on this population: its three consumers, predicted at 0.81 within 6%, read 0.9593, 0.9574 and 0.9583.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes, in the order they run: `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.40* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.13 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.16 | 88 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.12 | 92 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.10 | 92 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.10 | 92 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.15 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 96 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *90* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *93* | *0.00x* |
| lib-stage2-lean | 0.023 | 0.043 | 0.28 | 84 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.043* | *0.34* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.044 | 0.12 | 80 | 1.00x |
| lib-stage2-lean-u1 | 0.026 | 0.047 | 0.31 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.044* | *0.14* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.027 | 0.037 | 0.18 | 80 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.052* | *0.07* | *77* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.028* | *0.052* | *0.09* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.052 | 0.07 | 77 | 1.00x |
| lib-stage1 | 0.034 | 0.048 | 0.24 | 80 | 1.00x |
| bq-expand | 0.090 | 0.178 | 0.42 | 61 | 1.05x |
| *bq-expand-aa-adjacent* | *0.090* | *0.179* | *0.42* | *61* | *1.05x* |
| *bq-expand-aa-distant* | *0.091* | *0.179* | *0.08* | *61* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.81 | 31 | 21.18x |
| *list-aa-distant* | *1.005* | *1.019* | *0.48* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.007* | *1.021* | *0.30* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0071, worst cell 2.13% on `flip-last-rows`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.05% on `flip-whole-square`, its interval covering 1. The in-situ term reads 1.0196, 1.0199 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0069, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h17m10s, peak 209 MiB in use, 76 MiB max residency; the reader reads 33 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 31.3 ms per call raw, 30.2 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.052/0.047/0.026/0.026

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0063, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9590 to `lib-stage2-lean-u1` at 1.0774, with `list` itself at 1.0051.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.052, fourth lowest of the ten and level with `bcastmid`'s, and tiers at 1.00x, 1.05x and 21.18x, identical on the control --- and `lib-stage2-lean` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.7607 over 6 of 6 shapes at sign p 0.031, a margin of 23.93% against this class's 0.71% floor (`list-aa-adjacent`). **What is this class's own is the widest single A/A cell of the run**, 7.15% on `flip-last-rows` in the control half's process, which `--wild` clears of any foreign CPU and which is therefore a wild cell rather than an intrusion. **Its two columns MAY be differenced**, `list` having moved 0.51 of a point; the class geomean is 1.0063 and three of the eight strategies clear an A/A bar of 1.32 points, the joint widest of the ten.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.16 | 113 | 0.42x |
| liblist-stage2-sum | -- | -- | 0.19 | 122 | 0.34x |
| liblist-stage3-sum | -- | -- | 0.02 | 129 | 0.00x |
| liblist-stage4-list-sum | -- | -- | 0.02 | 129 | 0.00x |
| liblist-stage4-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 113 | 0.42x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.04 | 127 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 129 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.18* | *129* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.024* | *0.08* | *111* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.024 | 0.12 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.024* | *0.09* | *111* | *1.00x* |
| lib-stage2-lean | 0.021 | 0.024 | 0.13 | 111 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.022 | 0.026 | 0.09 | 111 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.029* | *0.08* | *111* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.09* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.028 | 0.12 | 111 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.026 | 0.12 | 111 | 1.00x |
| lib-stage1 | 0.050 | 0.058 | 0.14 | 103 | 1.42x |
| *bq-expand-aa-adjacent* | *0.086* | *0.087* | *0.11* | *96* | *1.06x* |
| *bq-expand-aa-distant* | *0.086* | *0.087* | *0.09* | *96* | *1.06x* |
| bq-expand | 0.086 | 0.087 | 0.13 | 96 | 1.06x |
| list (baseline) | 1.000 | 1.000 | 0.25 | 54 | 21.22x |
| *list-aa-distant* | *1.000* | *1.005* | *0.27* | *54* | *21.22x* |
| *list-aa-adjacent* | *1.001* | *1.005* | *0.20* | *54* | *21.22x* |

**Controls:** The largest A/A pair is `bq-expand-aa-adjacent` at 0.9983, worst cell 0.25% on `block-r3-vol64`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.01% on `block-run64-gap1`, its interval missing 1. The in-situ term reads 1.0189, 1.0230 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9988, which the correction amplifies by 1.40x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m15s, peak 133 MiB in use, 36 MiB max residency; the reader reads 33 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.6 ms per call raw, 4.45 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.020/0.024/0.028/0.024/0.020

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0089, from `lib-stage1` at 0.9917 to `lib-stage2-lean-u1` at 1.1370, with `list` itself at 1.0048.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.028, the lowest of the ten, and tiers at 1.00x, 1.06x and 21.22x, identical on the control --- and the family's ceiling and the best arm outside it TIE at 0.021, `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2`, the bolding going to the ceiling. The lean fill is priced against `mut-odo-vecdims` at 0.9234 over 5 of 5 shapes at sign p 0.062, a margin of 7.66% against this class's **0.17%** floor (`bq-expand-aa-adjacent`), the second tightest of the ten --- so a margin under eight points is read here with more confidence than a margin of thirty is on `runs`. **Its two columns MAY be differenced**, `list` having moved 0.48 of a point, and its cross-half geomean of 1.0089 is carried by one arm: `lib-stage2-lean-u1` at 1.1370, where the next widest is under three points.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.15* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.20 | 228 | 1.64x |
| liblist-stage2-sum | -- | -- | 0.22 | 230 | 1.55x |
| liblist-stage3-sum | -- | -- | 0.23 | 227 | 1.69x |
| liblist-stage4-list-sum | -- | -- | 0.19 | 230 | 1.51x |
| liblist-stage4-sum | -- | -- | 0.13 | 230 | 1.51x |
| libunord-stage1-sum | -- | -- | 0.33 | 223 | 2.07x |
| libunord-stage10-list-sum | -- | -- | 0.30 | 233 | 0.57x |
| libunord-stage10-sum | -- | -- | 0.32 | 233 | 0.55x |
| libunord-stage11-sum | -- | -- | 0.32 | 233 | 0.55x |
| libunord-stage6-loop-sum | -- | -- | 0.34 | 235 | 0.81x |
| libunord-stage6-sum | -- | -- | 0.24 | 234 | 0.83x |
| libunord-stage7-sum | -- | -- | 0.28 | 234 | 0.83x |
| libunord-stage9-sum | -- | -- | 0.28 | 234 | 0.55x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.12* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.09* | *249* | *0.01x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.052 | 0.068 | 0.28 | 230 | 1.27x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.052* | *0.069* | *0.24* | *230* | *1.27x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.052* | *0.067* | *0.29* | *230* | *1.27x* |
| lib-stage2-lean | 0.056 | 0.102 | 0.29 | 228 | 1.46x |
| lib-stage2-lean-u1 | 0.056 | 0.099 | 0.22 | 227 | 1.46x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.056 | 0.068 | 0.42 | 228 | 1.27x |
| *mut-odo-vecdims-aa-distant* | *0.060* | *0.087* | *0.33* | *229* | *1.27x* |
| **mut-odo-vecdims** | **0.060** | 0.087 | 0.36 | 229 | 1.27x |
| *mut-odo-vecdims-aa* | *0.060* | *0.087* | *0.34* | *229* | *1.27x* |
| lib-stage1 | 0.090 | 0.105 | 0.27 | 221 | 2.32x |
| *bq-expand-aa-adjacent* | *0.138* | *0.202* | *0.18* | *217* | *1.44x* |
| *bq-expand-aa-distant* | *0.138* | *0.202* | *0.13* | *217* | *1.44x* |
| bq-expand | 0.138 | 0.203 | 0.20 | 217 | 1.44x |
| *list-aa-adjacent* | *1.000* | *1.004* | *0.15* | *180* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.18 | 180 | 21.57x |
| *list-aa-distant* | *1.001* | *1.007* | *0.17* | *179* | *21.57x* |

**Controls:** The largest A/A pair is `list-aa-distant` at 1.0014, worst cell 0.71% on `small-flat64`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0008 on a worst cell of 0.31% on `small-flat64`, its interval covering 1. The in-situ term reads 0.9707, 0.9921 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0014, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m20s, peak 141 MiB in use, 57 MiB max residency; the reader reads 33 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.68 us per call raw, 6.46 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.041/0.077/0.049/0.059/0.087

**Across the halves:** 8 of the 16 arms are faster on this half and 8 slower, at a geomean of 1.0017, from `lib-stage1` at 0.9848 to `lib-stage2-lean` at 1.0236, with `list` itself at 1.0068.

**What the class says:** properties 1, 2 and 3 hold on both halves, and this is the one class where property 3's level clause is read off a `mut-odo-vecdims` family at 1.27x rather than at the result vector --- the per-call constants showing through a call under a microsecond, which is the reservation this class has carried since 2026-09-07; the order clause is unbroken, the tiers reading 1.27x, 1.44x and 21.57x and identical on the control. `worst` is 0.087, the highest of the ten. **The family's ceiling leads the class outright at 0.052**, `lib-stage2-lean` being the best arm outside it at 0.056 and priced against `mut-odo-vecdims` at 0.9232 over 1 of 5 shapes at sign p 0.38, a margin of 7.68% against this class's **0.14%** floor (`list-aa-distant`), the tightest of the ten. **Its two columns MAY be differenced**, `list` having moved 0.68 of a point, and it is the one population where the basis executes FEWER instructions than the control: a counts geomean of **0.9986**, against 1.0007 to 1.0098 everywhere else, with a time geomean of 1.0017.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.35* | *86* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.31 | 98 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.35 | 98 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.31 | 98 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.31 | 98 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.32 | 98 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.31 | 98 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 110 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 110 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.32 | 98 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.30 | 98 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.30 | 98 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 110 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.24* | *112* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *105* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.014* | *0.016* | *0.30* | *98* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.015 | 0.016 | 0.25 | 98 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.015* | *0.016* | *0.34* | *98* | *1.00x* |
| lib-stage2-lean | 0.015 | 0.017 | 0.28 | 98 | 1.00x |
| lib-stage1 | 0.015 | 0.017 | 0.32 | 97 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.017 | 0.28 | 97 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.018 | 0.018 | 0.35 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.024* | *0.028* | *0.24* | *94* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.024* | *0.029* | *0.26* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.024** | 0.029 | 0.19 | 94 | 1.00x |
| bq-expand | 0.094 | 0.102 | 0.36 | 79 | 1.35x |
| *bq-expand-aa-adjacent* | *0.094* | *0.102* | *0.37* | *79* | *1.35x* |
| *bq-expand-aa-distant* | *0.094* | *0.102* | *0.24* | *79* | *1.35x* |
| list (baseline) | 1.000 | 1.000 | 0.66 | 44 | 22.01x |
| *list-aa-distant* | *1.001* | *1.006* | *0.71* | *44* | *22.01x* |
| *list-aa-adjacent* | *1.002* | *1.006* | *0.65* | *44* | *22.01x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0067, worst cell 1.24% on `compose-rev-bcast`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.45% on `compose-zero-mid`, its interval covering 1. The in-situ term reads 1.0102, 1.0124 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0049, which the correction amplifies by 1.37x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h11m34s, peak 126 MiB in use, 33 MiB max residency; the reader reads 33 benchmarks over 4 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 30.9 ms per call raw, 29.8 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar):** `mut-odo-vecdims` 0.029/0.029/0.021/0.019

**Across the halves:** 5 of the 16 arms are faster on this half and 11 slower, at a geomean of 1.0035, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9361 to `mut-odo-vecdims` at 1.0370, with `list` itself at 1.0081. **The baseline moved 0.81% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.029, joint second lowest of the ten, and tiers at 1.00x, 1.35x and 22.01x, identical on the control --- and the family's ceiling and the best arm outside it TIE at 0.015, `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2`, the bolding going to the ceiling. The lean fill is priced against `mut-odo-vecdims` at 0.6097 over 4 of 4 shapes at sign p 0.12, a margin of 39.03% against this class's 0.67% floor (`bq-expand-aa-distant`). **What is this class's own is the run's lowest cross-half figure**, `mut-odo-vecdims-add-in-leaf-u1` at **0.9361**, the basis faster by six and a half points, where the next widest reading of that arm is `flip`'s 0.9590 and the other nine populations put it within two --- the low extreme in 5 of the 10 classes but nowhere else this wide. **This class is one of the three whose two columns may NOT be differenced**, `list` having moved **0.81 of a point** against a 0.7% bar, so its cross-half line is an ordering.


## Provenance

What this run's figures have to be read against, and it is a section of this file because a run replaces every word of it. What does NOT move with a run --- the delta chain that says which shape set and roster each run measured, and the list of what a run replaces outside this file --- is [README's own Provenance][prov].

**Run 33's halves differ in ONE COMPILER and in nothing else.** One source, `Main.hs` at `f31bd1c`, one shim at `f31bd1c` and one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1` in front of the assembler, one roster, one shape set, one class list and one bench order, both run under `WILDLOG=1 SATURATE=1`, both with `-A32m -I0 -T -M8G` baked and read back by `+RTS --info`. What differs is the compiler and everything a compiler brings with it: the basis takes ghc-9.12.4 through `cabal.project` and its freeze, the control the in-tree stage1 of the GHC checkout, `10.1.20260803`, through `cabal.project.ghead` and its own freeze --- TWO stores, TWO plans and TWO sets of boot libraries, which the binaries carry back as `ghc-internal-9.1204.0` and `ghc-internal-10.100.0`. **Neither half adds a regime flag**: `-O1` is micro.cabal's own `ghc-options` and no `--ghc-options` here overrides it, so both halves are plain -O1 and `diag` reads the ten-times-apart row on each. **And both halves carry `LOOP_EXITSPAN=1`, which no earlier pair did**, so the switch is not this pair's variable and what it is worth is readable only across runs, which is registration (6)'s one step. So this pair is Run 32's recipe with one shim switch added, built by two compilers, and every figure that moves between the halves moved because one of them emitted it.

**The sequence was launched once and ran to the end in ONE window; ONE population was rerun and the rerun was stopped.** The window is 2026-09-16T01:05:22 to 08:26:08, twenty-two processes --- the main set on each half and 20 class processes, one per class per half --- with no hole between one finishing and the next starting. The gate's four ran before them from 00:31:59 to 01:05:20, the four rider stages after them to 08:39:08, and the counted work followed on a box already handed back, 08:40:32 to 09:22:55. Every process exited 0 at the count its population asks for, with no complaint and no `!!` line in the wall-clock record, and the gheadexit half ran first throughout. `--wild` reads the hundred and nineteen logs this run wrote and finds one bench above 0.25 of a core in one of them, which this paragraph discloses below. The two main-set processes are the only ones whose stderr line no block below carries: `run33-gheadexit-main` took 0h54m11s at a peak of 191 MiB in use and 60 MiB max residency and `run33-exit-main` 0h54m7s at 179 MiB and 62 MiB, four seconds and 12 MiB apart. **ONE OF THE TWENTY-TWO WAS INTRUDED ON, BY THIS SESSION, AND THE RERUN POST-RUN STEP 3 ORDERS WAS LAUNCHED AND THEN STOPPED AT THE OWNER'S WORD.** `run33-gheadexit-main` carries 3 of its 627 benches at or above 0.25 of a core, peak **0.35** --- `lenet-L1-28-c1-k5/mut-odo-vecdims-add-in-leaf-u2-aa-distant`, `cnn-L1-6x6-c1/lib-stage2-lean` and `cnn-L1-6x6-c1/mut-odo-vecdims-add-in-leaf-u2-aa` --- and the intruder was this session reading documents and spawning the readings carrier after `sequence: start`, which run list step 15 licensed and which therefore landed inside the sequence's first process; the chapter now takes every reading at step 13a, before the launch. The rerun of `main` on both halves was launched at 09:23:55 and stopped four minutes in; its artifacts are parked under a `probe-` prefix, out of the namespace the readers glob, with the truncated JSON given a `.partial` suffix besides --- the corpus properties read every `*.json` in this directory and a half-written one fails three of them --- and the wall-clock log carries none of its stamps, and the figures this file publishes are the first window's throughout. **What stands in for the rerun is a sensitivity reading**, in the head: with both intruded shapes dropped from both halves every main-set span keeps its verdict, the widest moving 0.75 of a point, and the population floor widens from 0.62% to 0.66% rather than narrowing. `--wild` over the hundred and nineteen logs this run wrote clears every other one of them: the twenty-one remaining sequence processes, the four gate processes and all 88 alone-leg riders read NO bench at 0.25 of a core --- the other four `run33-al-*` logs being the riders' own drivers, which carry no samples to read.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run33-exit`, md5 `2f750355da01b25cfdc3e81134c01fec`, and `run33-gheadexit`, md5 `59e0ee343c245ede5b0f02e2a0160cdd`, with `.text` at **20787397** bytes on the basis and **20940607** on the control --- the HEAD half larger by **153210**, which is Run 32's gap TO THE BYTE and no multiple of 4096, as no compiler pair's gap here has been, Runs 24 to 28 reading 140922, 140922, 145018, 140922 and 145018 --- and their load addresses differ too, 4218880 against 4214784, which are Run 32's two unchanged. **Each half also sits exactly 20480 bytes, five pages, above its Run 32 counterpart**, the same figure on both, and this file offers no mechanism for either coincidence. **NEITHER md5 is two-sided this run**: `Main.hs` moved from `f95795a` to `f31bd1c` and the shim from `b3a1aca` to `f31bd1c`, so neither half's inputs are an earlier binary's, no md5 here can reproduce one and an unequal one names nothing. What they do say is that they differ from each other, which is two compilers having emitted two binaries. The commit the pair was built at is `f31bd1c`, transcribed from the pair note while that note is still here; the tree it ran on was `8409ceb`.

**The source moved, a timed function landed and the shim moved too, so this run's fills read the pinning claim in a form no earlier reading took --- and they REOPEN its strong form again.** The tracked 28-byte loops were read at the build against the NEAREST build of the basis's recipe --- `run32-nospec`, which is this recipe less `LOOP_EXITSPAN=1`, no build of this one existing before --- with `--delta`, and re-read here off the same two binaries: the two-copy group keeps every mod-64 offset, `[0, 0]`, and **the six-copy group does NOT** --- `[0, 0, 8, 0, 4, 0]` becomes `[0, 0, 0, 8, 4, 0]`, its third and fourth heads exchanging offsets --- with NO address surviving to the byte on either, five displacements on the six-copy group of which `0x3438` and `0x3448` are not whole lines, and two on the two-copy group. README's ruling is that under the dead-spot form the strong form holds for the tracked heads' OFFSETS, and says outright that what would reopen it is a tracked head's offset moving. This moves one, under a source commit, a comment commit AND nine commits to the shim, where Run 32's reading had six source commits and an unmoved shim and Runs 24's and 25's had a roster change alone; the verdict is [that section][floor]'s to write. **Within the pair the layout moved too.** `./loop-offsets.py run33-gheadexit run33-exit` puts the six-copy group at `[0, 0, 0, 8, 4, 0]` on the basis and `[18, 0, 0, 0, 9, 2]` on the control, the two-copy group at `[0, 0]` on both, and post-run step 0's twins name those six as `fbMidCopy`, `fbCanonVecdims`, `fbMutOdoVecdimsAddIn`, `fbMutOdoVecdims`, `fbMutOdoVecdimsAddOut` and `fbMutOdoVecdimsAddBoth` on each half, with `fbBuild` and `fbMutOdo` the two.

**The three main-set anchors** read **6.29 us** on `cnn-slice-c32`, **3.70 ms** on `cnn-L2-24x24-c32` and **39.7 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm:
| shape | `l` | `list`, per call | net | `gheadexit`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.46 us | 6.29 us | 6.32 us |
| `cnn-L2-24x24-c32` | 165888 | 3.80 ms | 3.70 ms | 3.76 ms |
| `stretch-wide-2xM` | 1800000 | 40.8 ms | 39.7 ms | 40.4 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's shapes, raw and net.** The main set's three guard a baseline that moves for every population at once; a class anchor guards one that could move for that mechanism alone, which is the case a table of ratios hides completely. The `runs` anchor is `runs-2` at **40.72 ms** raw and **39.65 ms** net on the basis, against Run 32's 40.71 ms and 39.63 ms on that run's basis --- three hundredths of a percent apart raw and net alike, computed from the cells, and it carries the switch, the shim and two commits as well as the box. **The control half reads 41.87 ms and 40.79 ms on the same shape**, 2.8% above the basis, where Run 32's two halves read alike here; that is the compiler moving the reference on the class whose floor is the widest of the ten, 3.11%, and it is why `runs`'s cross-half figures are read against that floor and not against the main set's. **No class population moved this run at all**: `roster-delta.py` reads 58 class views to 58 with every one of the ten classes unmoved.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0003** on the basis and **1.0003** on the control, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0272** and **1.1139** on the basis and **1.0259** and **1.1096** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs a few percent over the term it stands for, by nearly the same few percent on both halves, which is where it has run since Run 17. So the compiler does not move the correction, and no ratio in this file is an artefact of a forcing pass that parted between the halves.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance
[open-list-33]: ../README.md#what-is-open


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

Declared 2026-09-15 evening by request, the recipes in [Run 32's file](run32.md#what-the-next-run-compares-against). The pair is Run 32's with `LOOP_EXITSPAN=1` on both halves, `run33-exit` the basis on ghc-9.12.4 and `run33-gheadexit` on GHC HEAD, both at plain `-O1` in the dead-spot form, the shim at f1a5adb and `Main.hs` at the tip at build time (the registration's own words; the shim the pair was built with is `f31bd1c`, of which f1a5adb is one commit and the fix rather than the switch --- the head and the note carry the correction), which carries stage 11 and so is not Run 32's source. Every `cross` below is basis over control between this run's own halves unless it says `--compare`, which is `run32-nospec` against `run33-exit`, the one step the chapter allows and one that carries a source term. Each prediction is its own kill condition; a `predict:` line that fails is KILLED.

(1) *The compiler on the lean fill, the one placement defect these arms had, now removed on both halves.* Run 32 read the fill 1.0134 on the main set with HEAD's head at residue 9, its exit astride the line, and the interleaved readings of the afternoon put the fixed half level with the basis. On the main set: `predict: cross lib-stage2-lean 1.0 within 2%`; on `runs`: `predict: cross lib-stage2-lean 1.0 within 3%`; and its twin, whose head the exit span leaves at 0 on both compilers: on the main set `predict: cross lib-stage2-lean-u1 1.0 within 2%`.

(2) *The compiler on the reference.* Run 32 read 1.0043, inside the differencing bar, and the exit span moves `list`'s loops on neither half. On the main set: `predict: cross list 1.0 within 2%`; on every class: `predict: cross list 1.0 within 3%`.

(3) *The compiler on the shared per-run loop of stages 7, 9, 10 and 11, which placement cannot mend.* HEAD retires six taken branches and seven fetch blocks a run against 9.12.4's five and five on `runs-3`, the outer head's test a taken `jl` and the exit block laid inside the cycle, and inside one tree residues 0, 3 and 30 of its head read level. So the penalty is the compiler's and the exit span leaves it: on `runs`: `predict: cross libunord-stage9-sum 0.81 within 6%`, `predict: cross libunord-stage7-sum 0.81 within 6%`, `predict: cross libunord-stage10-sum 0.81 within 6%`; on `window`: `predict: cross libunord-stage9-sum 0.85 within 6%`, and stage 10 on its long runs, latency-bound and placement-blind, `predict: cross libunord-stage10-sum 1.0 within 3%`.

(4) *The shipped leaf, unmoved by either half's placement.* On the main set: `predict: cross mut-odo-vecdims-add-in-leaf-u2 1.0 within 2%`; and its fusion over the odometer, read 0.6459 and 0.6358 on Run 32's halves: on the main set, both halves, `predict: pair mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims 0.64 within 4%`.

(5) *The floor pair.* The A/A copies against their originals within the class floor on both halves, the standing registration every run carries, read as Run 32 read it.

(6) *The exit span against Run 32's basis, one step, same compiler, a moved source.* `--compare run32-nospec run33-exit`: the fill's loops sit at residue 0 in both, so `predict: cross lib-stage2-lean 1.0 within 2%` and `predict: cross lib-stage2-lean-u1 1.0 within 2%` on the main set, and `predict: cross list 1.0 within 1%`; the stage arms are excluded from this item, `Main.hs` having gained stage 11 between the builds and the afternoon's reading of that step on those arms being the trees parting. What KILLS this item is a fill arm past 2%, which would say the heads the exit span moves, 637 on the afternoon's tree, include one of theirs.

(7) *The shim's own claim.* The verbose line of each build reads eight exit spans astride and no short loop straddling but the rotated pairs' sixteen planned, as the afternoon's builds did; post-run step 0's twins name the eight. A ninth astride, or a straddler outside the pairs, KILLS it.

**FOUR of the seven held, TWO were killed and ONE cannot be adjudicated against these builds --- and the two kills and the unadjudicable item were all three flagged before the machine was booked.** Every item's verdict below is its KILL CONDITION applied across the populations that item names, never one sweep of the main set; every figure is re-derived from this run's own JSONs, by `--predictions` over the populations each item names on the pair's two halves, by `--pair` where a span is read within a half, and by `--compare run32-nospec run33-exit` for item (6), which is a cross-run item and which the per-population sweep therefore does not adjudicate. **Two things govern how the whole list reads.** The first is that the pair's variable reaches the fill family and almost nothing else: every item predicting level on `list`, on the leaf or on an A/A copy held, and both items predicting a magnitude on the fill family or on the stage consumers missed. The second is the disclosure the head carries: `run33-gheadexit-main` was intruded on for 3 of its 627 benches, and with both intruded shapes dropped from both halves every span below keeps its verdict, the widest moving 0.75 of a point.

(1) *The compiler on the lean fill, the one placement defect these arms had, now removed on both halves.* **KILLED on both its main-set spans, and by more than Run 32 read without the switch.** `cross lib-stage2-lean 1.0 within 2%` reads **1.0354**, 3.54 points off, and `cross lib-stage2-lean-u1 1.0 within 2%` reads **1.0209**, 2.09 off; the third span, `cross lib-stage2-lean 1.0 within 3%` on `runs`, HOLDS at **1.0028**. So the exit span did not bring the two compilers level on the arms it was added for: Run 32 read the fill at 1.0134 with HEAD's head at residue 9 and its exit astride the line, and with that cost charged on both halves the two part by half again as much. **The counts say the residue is not the code generator's**: the basis executes 0.62% more instructions on the lean fill and takes 3.54% more time, `time/counts` **1.0290**, and on `lib-stage2-lean-u1` over `runs` the counted ratio is **1.0000** against a time of 1.2954.

(2) *The compiler on the reference.* **HELD everywhere it is read, and it governs the whole file.** `cross list 1.0 within 2%` reads **0.9955** on the main set, 0.45 of a point off, and the class clause, `1.0 within 3%`, holds on all ten: `bcast` 0.9982, `bcastmid` 0.9931, `block` 1.0048, `compose` 1.0081, `flip` 1.0051, `rev` 0.9918, `runs` 0.9951, `scaled` 1.0109, `small` 1.0068 and `window` 1.0016. **What the item's own clause then delivers is the differencing bar**: the main set and seven of the ten classes sit inside the 0.7% that lets two columns be subtracted, so eight of this run's eleven populations carry cross-half readings that are measurements rather than orderings --- one more than Run 32 and more than any run since Run 28.

(3) *The compiler on the shared per-run loop of stages 7, 9, 10 and 11, which placement cannot mend.* **KILLED on `runs`, and the preparation said so before the run.** The three `runs` spans, each `0.81 within 6%`, read **0.9593** on `libunord-stage9-sum`, **0.9574** on `-stage7-sum` and **0.9583** on `-stage10-sum` --- about fifteen points away, and level rather than nine tenths. The item's 0.81 came from a branch-and-fetch reading of one tree; Run 32 had read those arms at 0.969 on that population and the preparation flagged the item to the owner on exactly that ground, without amending it. **Its `window` clauses split**: `cross libunord-stage9-sum 0.85 within 6%` HOLDS at **0.8889**, so the one span that predicted a magnitude and got it is the one on the class where no view has a zero stride, while `cross libunord-stage10-sum 1.0 within 3%` misses at **0.9686**, 3.14 points off and 0.14 outside its band.

(4) *The shipped leaf, unmoved by either half's placement.* **HELD on both spans.** `cross mut-odo-vecdims-add-in-leaf-u2 1.0 within 2%` reads **1.0111** on the main set, and the fusion over the odometer, `pair mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims 0.64 within 4%`, reads **0.6428** on the basis and **0.6371** on the control. That is the ninth and tenth readings of that span across five runs, all of them between 0.6358 and 0.6525, under two flags, a whole level, two rosters, two compilers and now the exit span. **The leaf is the one fill arm the switch left level**, its two A/A copies moving 1.27 and 1.08 points across the halves beside its own 1.11.

(5) *The floor pair.* **HELD in all forty-four readings** --- both fill-family A/A copies against their original, on both halves of all eleven populations, each paired geomean inside that population's own floor. The widest is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` on `compose`'s control half at 1.20 points, against the 1.20% floor that same pair carries there, with `flip`'s control next at 1.15; on the main set the four read 1.0005 and 0.9980 on the basis and 0.9989 and 0.9983 on the control, against floors of 0.47% and 0.62%. **One of those forty-four is the intrusion's own cell and it is still inside**: the distant copy on the control main set reads a published-column 1.0373, dragged by the one intruded cell, where the paired figure the span is judged on reads 0.9983 over nineteen shapes and 1.0013 over the seventeen that exclude it.

(6) *The exit span against Run 32's basis, one step, same compiler, a moved source.* **HELD on all three spans, which is the one cross-run reading this chapter allows.** `--compare run32-nospec run33-exit` reads `cross lib-stage2-lean 1.0 within 2%` at **0.9983**, `cross lib-stage2-lean-u1 1.0 within 2%` at **0.9817** and `cross list 1.0 within 1%` at **1.0014**. The item's kill wants a fill arm past 2% --- which would say the heads the exit span moves include one of theirs --- and neither is: 0.17 of a point and 1.83. So on the compiler this chapter publishes on, the switch is worth nothing to either fill arm and fourteen hundredths of a point to the reference, across a distance that also carries two `Main.hs` commits. **Read beside (1), that is the finding of the pair**: the exit span does not move these arms on 9.12.4, and the two compilers part further under it than without it.

(7) *The shim's own claim.* **NOT ADJUDICABLE against these builds, as the preparation reported before the run and did not amend.** The item predicts eight exit spans astride, no short loop straddling and sixteen planned, and its kill is a ninth astride or a straddler outside the pairs. Under the shim this pair is built with, `f31bd1c`, all four emissions --- two modules on each half --- read `verified: 8 short loop(s) straddling (8 planned), 0 exit span(s) astride`, so the astride count is 0 and cannot reach nine. **Two of the item's three figures are the PRE-FIX shim's and this run reproduced them**: built once more on this tree with `align-as.py` at `f1a5adb^`, a diagnostic build kept out of the pair, the line reads `8 short loop(s) straddling (16 planned), 8 exit span(s) astride`. `f1a5adb` stops an unconditional back edge's tail being read as the exit and charged, so it removes the population that could straddle --- 8 astride becomes 0 and 16 planned becomes 8 --- while the straddling column reads 8 under both shims and the item's *no short loop straddling* matches neither. **What post-run step 0 could still do is name the eight**, and it does: six of the basis's eight straddlers by byte identity and three of the control's, `fbMutOdoVecdimsAddInLeafU2` and its `Down`, `Last` and `Ptr` forms among them.
