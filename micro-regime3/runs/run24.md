# Run 24 (SpecConstr)

One run's write-up: its head, its Results, what the next run compares against, the claims that run should test, the nine class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach.

**Run 24 (SpecConstr), and what a second compiler does to a roster whose layout is the dead-spot form's: every registered ordering that can still be read holds on both halves, and the codegen splits the roster in two --- ghc-9.12.4 emits 5.7% and 6.8% FEWER instructions than GHC HEAD on the two pure mul-back arms and about one percent MORE on the branch's own fill family, the times following the counts on both sides.** Criterion, **`--ghc-options=-fspec-constr`**; the dead-spot form on BOTH halves, one source, one shim commit, one shim environment, one roster and one shape set, and **what moved is the compiler and nothing else a freeze, a source diff or a shim switch can see**: 1352 benches, 52 timed arms over 26 main-set shapes, and 2132 more over 41 class views in **nine** classes. **The basis is `run24-g912`**, ghc-9.12.4, the default on PATH here and the lineage every figure in this README was measured through, built `-fspec-constr -fobject-determinism` with `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1` in front of `align-as.py`; md5 `0ea817d7761de51b5faecf48cb24c00f`, `.text` 20533445 B. **The other half is `run24-ghead`**, the same source and the same shim environment through `cabal.project.ghead`, which selects the in-tree stage1 of the GHC checkout --- `10.1.20260803`, and the binaries carry `ghc-internal-9.1204.0` against `ghc-internal-10.100.0` --- md5 `8eb43268b618d27665140d38b9506bd6`, `.text` 20674367 B, 140922 B the larger. So the halves differ in the compiler and in the boot libraries that come with it, and in nothing else; both under `WILDLOG=1 SATURATE=1`; `Main.hs` at `7dd094e`, `align-as.py` at `38bb3bb`, the tree at launch `4e2e60a` with twelve untracked scratch paths and nothing modified. The same desktop, Zen 3, a Ryzen 7 5800X, and the same BIOS Run 18 re-baselined onto. The two main processes read *1h56m36s* and *1h57m4s*, at *395 MiB* in use and *120 MiB* max residency on the basis against *496 MiB* and *216 MiB* on the HEAD half.

**There is NO repetition this run, and what stands in its place is a cross-run reading that carries a roster term.** `Main.hs` moved between Run 23 and this run, by the two roster commits of 2026-09-02, so neither half reproduces an earlier binary and the exact repetition Runs 19 and 23 could take is unavailable. What can be read is `run24-g912` against `run23-spot`, the previous build of THIS recipe: over the 24 shapes the two runs share, **33 of the 45 arms they share read within 1%**, and the twelve outside divide in two. Two are the `libunord` arms, degenerate on cells that are their own forcing term. The other ten are the placement-exposed families and their twins --- `mut-odo` 0.9714 with its twins at 0.9599 and 0.9698, `build` 1.0186 with its twins at 1.0329 and 1.0348, `gen-unsafe` 0.9841 with its twins at 1.0158 and 1.0188, and `liblist-stage1` 0.9893 --- every one of them an arm whose figure is where its bytes landed --- and note that a family moves without converging: `gen-unsafe` reads 0.9841 where its two twins read 1.0158 and 1.0188, on the same code. **So the band this run's cross-run column is read against is not Run 23's under-a-point one**: a roster change puts a layout term back where a repetition had none, and it lands on exactly the arms Run 23 warned it would.

**What holds the build to something is the gate and two machine checks, there being no repetition to do it.** The gate ran both halves twice in a palindrome and read SOUND on both passes: no arm separated between the halves, `build` 0.9934 and 1.0061 and `mut-odo` 1.0064 and 0.9910 changing sign between the passes, which is what a tie read twice looks like. Its machine check read **+0.56%** on `list`'s net against the fingerprint Run 23 kept, over 24 of 26 shapes --- the two shapes added 2026-09-02 having no kept row --- worst `stretch-pow2stride` +2.67% and none past 5%; the run's own two main-set processes read the same comparison at **-0.20%** and **-0.39%**, worst `conv1d-24` -1.78% and `alexnet-L2-27-c48-k5` -2.80%. Three readings against the same kept fingerprint, all inside 3%, so the box measures as it did and no absolute is re-baselined. Each half's own sixteen A/A pairs give it a floor, and the counted work, taken over every population on both halves, is what separates a compiler's instructions from a slot its bytes landed in throughout what follows.

**The manifest's one surviving claim held on both halves, for a seventh clean sweep, and the second compiler widens two of its links.** Claim 1's four registered links all hold on the basis: `mut-odo-vecdims` / `mut-flat-gm` **0.6462** at 22 of 26 and sign p 0.00053, `mut-flat-gm` / `bq-mut-runs-gm-mulback` **0.9102** at 26 of 26 and p 3e-08, `bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` **0.9252** at 21 of 26, and `bq-mut-runs-gm-mulback` / `bq-scan-rem-gm-mulback` **0.9337** at 19 of 26 --- 4 of 4 --- and on the HEAD half at **0.6429, 0.9017, 0.8780 and 0.8883**, 4 of 4 again. The top link is three thousandths apart between the halves; the two links below it are four and a half to five points wider on HEAD, and the counted work says why: 9.12 executes 6.8% fewer instructions on `bq-odo-gm-mulback` and 5.7% fewer on `bq-scan-rem-gm-mulback` while `bq-mut-runs-gm-mulback` moves 0.1%, so what widens those links on HEAD is one compiler's codegen on the two arms needing nothing at all and not anything the ladder is about.

**What the second compiler is worth, and the counted work says it is instructions on one family and placement on another.** Read as `--compare` prints it, basis over HEAD, the roster's geomean is **0.9935** over 46 arms, 26 of them below 1 --- and that near-tie hides a split the counted work makes plain. **9.12 is decisively better on the pure mul-back family**: `bq-odo-gm-mulback` reads **0.9345** in time at a count ratio of **0.9325**, `bq-scan-rem-gm-mulback` 0.9368 at 0.9426, and their four A/A twins land within five thousandths of their bases, so time over counts is 0.994 to 1.007 --- the whole of a six-to-seven-percent win is instructions 9.12 does not emit and HEAD does. **And HEAD is better on the branch's own fills**: the six `lib-stage2*` arms read 1.0165 to 1.0255 in time at count ratios of 1.0084 to 1.0097, so 9.12 executes about a percent more work there and loses about two, the rest being where it put the code. `list` moves 1.0025 at a count ratio of 0.9968, `mut-odo-vecdims` 0.9992 at 0.9994, and the counts geomean over the 46 arms with a corrected time is **0.9931**.

**The placement-exposed workers move as far as any arm here and their counts do not move at all, which is the cleanest reading of that term this file has had.** `gen-unsafe` reads **1.0451** across the halves at a count ratio of **1.0000** exactly, and its two twins 1.0462 and 1.0606 at 1.0000 apiece; `build` 1.0068 and `mut-odo` 0.9870 at 0.9999. So `gen-unsafe`, whose adjacent twin at 1.0606 is the roster's widest reading above 1 --- HEAD the faster on all three --- executes, to four figures, the same instructions on both halves, and every one of those four to six points is where its bytes landed. The twins moved with their bases and not to their figures --- `gen-unsafe`'s three spread 1.5 points, `build`'s 1.0068 against 0.9896 and 1.0182 --- which is the term a slot owns and its arm does not, and it is the same shape Run 23 read across two layouts of one compiler. **A change of compiler is a change of layout as well as of codegen**, and the counted work is the only thing here that tells the two apart.

**`build` against `mut-odo` is a tie on both halves, which is the third answer that pair has given in three runs.** It reads **0.9920 at 15 of 25, sign p 0.42** on the basis and **0.9782 at 15 of 25, p 0.42** on HEAD, both intervals covering 1, where Run 23 read 0.9998 on its max-skip half and 0.9449 on its dead-spot one and Run 22 read 1.0125. Both arms' instruction counts are equal between the halves to four figures, and the gate read the pair straddling 1 on each half across its own two passes --- 1.0054 and 0.9991 on the basis, 1.0185 and 0.9841 on HEAD --- so nothing here separates them and the five-and-a-half-point gap Run 23 opened with the dead-spot switch does not reappear when the compiler is what varies. The 3% [the open list][open] has asked about since Run 10 is not on today's basis either.

**The classes break property 2 in all nine, where Run 23 broke it outright in seven, and the arms that break it are the roster's new ones.** `libunord-stage2` leads `rev`, `revsome` and `reshape1` at 0.001, 0.000 and 0.000 of `mut-odo-vecdims`, its one-block test firing on every view of those classes and collapsing them to a single slice, so it prices dispatch and not filling; `lib-stage2-short-lean`, the arm that landed this run, leads `bcast`, `slice` and `window` at margins of 39.79%, 28.42% and 63.79% against those populations' floors of 5.43%, 2.76% and 6.94%; `lib-stage2-lean` leads `bcastmid` by 47.28% against 2.80%; `lib-stage1`, the shipped route, leads `scaled` by 9.07% against 2.09%; and `lib-stage2-disp`, the arm task 9's probe re-cut to 2048, leads `runs` by 22.87% against 3.07%. **Five of the nine are led by a stage-two arm, one by stage one and three by the unordered entry point** --- where a run ago the leads were candidates and `mut-odo-vecdims` siblings. `scaled`'s is `lib-stage1`, which this file keeps apart from the stage-two family everywhere else, so it is counted apart here. Property 3 holds in all nine on both halves, and property 1 holds in all nine OF THE FIX --- which is what it is stated of; the library-shaped arms break it on `runs`, `lib-stage1` among them, and the claims section says so.

**Across the halves the classes read as the main set does, and the split is even.** Of the 414 arm-comparisons the nine classes carry, nine are degenerate and not voted --- on `reshape1`, the six `lib-stage2*` arms, both `canon-*` arms and `libunord-stage2`, whose cells are their own forcing term --- and **206 put the basis faster against 199 the HEAD half**, the nine geomeans running **0.9855 on `scaled` to 1.0006 on `slice`**, eight of them below 1. The extremes over all nine are `bcast-set` at 0.8519 on `reshape1` and `libunord-stage2` at 1.1967 on `rev`. **The low extreme is `bq-odo-gm-mulback-aa-distant` in three of the nine** --- `bcast` 0.8963, `runs` 0.8988 and `rev` 0.9135 --- and some arm of that family holds it in five, `bcastmid`'s 0.9200 and `scaled`'s 0.9065 with them, which is 9.12's codegen win on the pure family showing through class by class. **Five classes disqualify their own cross-half line**, where Run 23 had three: `rev` at 1.0078, `revsome` 1.0149, `bcast` 1.0124, `reshape1` 1.0327 and `runs` 1.0104 move `list` past the 0.7% bar, so those five are ordered and not subtracted, and the four that are inside it are `bcastmid`, `slice`, `window` and `scaled`.

**The six registrations came back four HELD, one HELD on its orderings and not on one of its figures, and one SPLIT --- and a clause of the fifth could not be read at all, which is the finding.** (1) the short bodies: **SPLIT** --- ahead past both floors on every k3 and k5 main-set shape and on `runs-2` to `runs-4`, `window-28x28-k5` and `window-224x224-k3`, and killed by its own count clause on `stretch-coprime-r7`, where the short body does not fire and the count ratio reads 1.0105 on the basis and 1.0107 on HEAD. (2) the lean dispatch: **HELD**, at or below `lib-stage2` on every population of both halves and ahead by 8.7% to 23% on the four smallest main-set shapes. (3) the composite: **HELD**, at or below the better parent on every population of both halves. (4) the straddlers: **HELD**, four on each half at the two body lengths registered, and post-run step 0's `-g3` twin names all four on the basis as the outer loops of `fillStage2`, `fillStage2Short` and the two `-u2` leaf fills. (5) HEAD: **HELD on its orderings and not on one of its figures**, no ordering in (1) to (3) reversing past HEAD's floor. (6) the threshold: **HELD**, `lib-stage2-disp` at or below the better of `lib-stage2` and `lib-stage2-concat` at every `runs` length within that class's floor on both halves. **And (5)'s remaining clause could not be read at all**: it predicts `-u2` ahead of `-down` in every population, and `mut-odo-vecdims-add-in-leaf-down`, the arm that comparison turns on, was parked to `Only` by the same commit the registration was written beside, so no process this run times it.

**Every one of the twenty processes gated clean**, `--selftest` and both `--aa` gates, so no time column here is uncorrected, and the plateau gate puts all twenty inside **19.594 to 20.1976 ms/iter, a 3.08% spread** against the 5% band, where Run 23 read 4.63%. **This run's floor is 1.26% on the basis half and 2.11% on the control**, against Run 23's 2.03% and 2.80%, the basis figure carried by `gen-unsafe-aa-distant` and the control's by `build-aa-adjacent`; the worst A/A cell of either main set is **16.66%** on `stretch-inner1` on the basis against **18.37%** on `gather48-src-50` on the other. Restricted to the six pairs that carry back to Run 10 the two read **0.34%** and **0.19%**, against Run 23's 0.39% and 0.40%. **Which of the two a margin is judged against depends on what it compares**: an arm against its own duplicate against 1.26% and 2.11%; two different arms against the six-pair figures. Neither is inherited --- the basis figure is the fifth consecutive run of this lineage whose floor moved for no isolated reason, 1.51%, 2.92%, 2.12%, 2.03%, 1.26%, and it is the tightest of them.

**The two halves' cells resolve alike, for the third run running.** `CI%` --- the median half-width of a cell's own fit --- runs a geomean of **1.00** on the basis against the HEAD half across the roster, **31 arms wider here and 21 narrower**, where Run 23 read 1.01 at 31 and 24 and Run 22 1.01 at 28 and 27: an even split again, on two halves that differ in compiler as Run 22's did. It remains a different quantity from the floor: sampling error inside one bench against agreement between two placements of one strategy.

**The sequence ran in ONE window and nothing happened on the machine during it.** Twenty processes from 02:54:41 to 12:58:25, every one exiting 0 at its roster's count --- 1352 twice, 728 twice, 208 six times and 156 ten times --- the HEAD half first throughout, which is the driver's order, and no process reported a selection it did not ask for. The per-sample instrument's foreign-CPU column, read over each main process's own 1352 benches, puts **not one bench at or above 0.25** on either --- the two main sets are what it was read over, the eighteen class processes being covered by their exit codes and the plateau gate instead --- so nothing else was running during any sample of either, post-run step 3 did not fire and no population was rerun. The gate that preceded it was launched twice: a first attempt at 02:06 was stopped by hand two minutes in when the machine was wanted, its four partial artifacts moved out of the tree, and the recorded gate is the relaunch of 02:09 on a box reading 0.7% non-idle.

**The cells that sink below the shared forcing pass are far fewer than last run, and the two halves sink on different shapes.** On the basis five cells sink --- both `libunord` arms on `stretch-inner1` and on `stretch-wide-2xM`, and `libunord-stage2` on `stretch-square-1341` --- so two rows are geomeans over 24 and 23 shapes of 26 and every other row covers all 26. On the HEAD half six sink across three rows: the two `libunord` arms on `stretch-pow2stride` and `vgg-14-c512-k3`, `libunord-stage2` on `stretch-square-1341`, and `lib-stage2-lean` alone on `stretch-inner1`. **So the `lib-stage2` family no longer sinks on `stretch-inner1` at all on the basis**, where Run 23's dead-spot half sank fifteen cells across eleven rows and nine of them were that family on that shape; what changed is the roster, the canonicalizing arms that sank with them having been parked. On `reshape1` nine arms are degenerate on each half and **the shape they sink on differs between the halves** --- `reshape1-500k` on the basis, and on HEAD `reshape1-r3` for eight of them with `lib-stage2-short-lean` on `reshape1-500k` --- which is why that class's family readings are taken over the two shapes neither half sinks on. It is a structural fact about the table and not a defect in it, and it is why every main-set registration figure here is taken over the 25 shapes that exclude `stretch-inner1`, so that the two halves are read over one population.

**The counted work covers every population, and on this pair it reads the compiler rather than a pad.** Twenty sweeps, both halves over all ten populations, 156, 208, 728 or 1352 cells apiece and no cell perf refused anywhere in the twenty files. **Across the halves every class reads as the main set does**: the counts geomean over the arms with a corrected time runs **0.9889 on `bcast` to 1.0031 on `reshape1`**, against 0.9931 on the main set, so 9.12 executes about a percent less work than HEAD over the roster as a whole on eight of the nine classes and a little more on the ninth. Within that the same split holds everywhere: the pure mul-back arms carry that count difference in 9.12's favour and the `lib-stage2*` family the one percent in HEAD's, while `build`, `mut-odo`, `gen-unsafe` and their twins read 0.9999 to 1.0000 in every population, so every point those move anywhere is placement. **What the counts decide on this pair is not what they decided on the last one**: Run 23 was a layout pair, where an arm must not move its instructions except where a pad was executed; here the compiler moves, so a count MAY move on any arm, and a count that does not is the finding.

**The correction sits on the same footing in both halves, as it has on every run since Run 17.** The in-situ forcing term --- an arm minus its `-nosum` twin, against the `sum-only` the correction actually subtracts, read off `--aa`'s `ratio` column --- reads 1.0198, 1.0174, 1.0071 and 1.0683 on the basis and 1.0217, 1.0168, 0.9927 and 1.0687 on the HEAD half, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm` and `bq-expand`; the two `sum-only` halves agree at 1.0001 on the basis and 1.0000 on the other, on worst cells of 0.48% and less. Seven of the eight tilt the same way and the two halves are within a point and a half on each, so a margin between these halves is not carrying a correction bias.

**The ceiling reproduced for an eighth run, and reading it took a pinned shape set to see.** `mut-odo-vecdims` against `bq-scan-rem-gm-mulback`, the fastest arm needing nothing at all, reads **0.5469 at 23 wins of 24** on the basis over Run 23's own 24 shapes --- against Run 23's basis 0.5466, its dead-spot half's 0.5527, Run 22's 0.5449, Run 21's 0.5424, Run 20's 0.5479, Run 19's 0.5572, Run 18's 0.5577 and Run 17's 0.5446 --- three ten-thousandths from the run before it. **Over this run's own shape set the same pair reads 0.5493 over 26 shapes and 0.5312 over the 25 that exclude `stretch-inner1`**, so the figure that looked to have left its eight-run band had only changed population: pin the shape set, as [the `alloc` bullet](#results) asks of allocation, and the ceiling is where it has been since Run 17. **On HEAD it reads 0.5119 over the same 24**, three and a half points lower --- and the counted work names the cause rather than the ceiling moving: HEAD emits 6.1% MORE instructions on `bq-scan-rem-gm-mulback`, the denominator, while `mut-odo-vecdims` reads 0.9994, so the ratio falls because the arm it is measured against got slower.

**This run's two columns MAY be differenced.** `list` moves **0.25%** between the halves on the main set against the 0.7% bar --- over all 26 shapes --- where Run 23 read 0.33% and Run 22 0.81% and refused; so the cross-half figures here may be read as subtractions, and the counted work carries the claim about *why*. Five of the nine classes are past the bar --- `rev` at 1.0078, `revsome` 1.0149, `bcast` 1.0124, `reshape1` 1.0327 and `runs` 1.0104 --- where Run 23 had three, and their blocks say in their cross-half lines that they are ordered and not subtracted.

**The straddling loops are the outer loops of the branch's fills on both halves, and the basis's twin names all four, as Run 23's dead-spot twin did.** Each half carries four self-loops straddling a cache line in `Main`-compiled code, at the two body lengths Run 23's dead-spot half had. On the basis post-run step 0's `-g3` twin names **all four** by byte identity --- `fillStage2Short` at `0x4205aa`, `fillStage2` at `0x422b2a` and `fbMutOdoVecdimsAddInLeafU2` at `0x429b6a`, 55-byte bodies at offset 42, and `fbMutOdoVecdimsAddInLeafU2Down` at `0x428b2f`, 53 bytes at offset 47 --- the branch's own fill, its short-body variant and the two leaf fills the library ports. **All four are the OUTER, per-run loop of a rotated pair, and on the basis no fill's inner loop straddles** --- read, all four being named. On HEAD it is inferred and not read: four straddle there too, the twin names two and refuses the other two, and what says the refused pair are the leaf fills' outer loops is their body lengths, 53 and 55 bytes, and nothing else. That the outer loop is the one left to straddle is that is the dead-spot form's own order and not this build's luck, its containment test placing the inner head of a rotated pair and letting the outer yield, so every dead-spot binary should carry these four and no run should read them as the fill loop straddling. On HEAD the twin names two --- `fillStage2Short` at `0x41edaa` and `fillStage2` at `0x4212aa` --- and REFUSES the other two, at `0x4272f1` (53 bytes, offset 49) and `0x42826c` (55 bytes, offset 44), holding no byte-identical copy of either; their two body lengths are the leaf fills' own, and the count check saying so rather than guessing is what makes the negative honest, as Run 22's did on three of four. [What moves a figure when no strategy changed](../README.md#what-moves-a-figure-when-no-strategy-changed) prices a straddling loop as a per-element term, which is the wrong rate for these; what remains is a per-run term, paid once per exit of the inner loop.

**The regime was confirmed in the binary before the hours were spent**, which nothing afterwards can: a `diag` in the run's own regime puts `baseOffsetsScan` at 2408930 bytes against `baseOffsetsMut`'s 2408530 on `vgg-14-c512` on the basis, Run 23's two halves' figures to the byte, where plain -O1 separates the two tenfold. With no rebuild between the gate and the sequence, that is the only check standing between a mistyped regime and the hours.

**Run 24 records every population twice** --- the main set and all nine stride classes from each half, one process each --- **in one window**, as Run 23 did. Every one of the twenty exited 0 at the bench count its roster holds --- 1352 twice, 728 twice, 208 six times and 156 ten times --- and no process reported a selection it did not ask for. The eighteen class processes span **0h13m29s to 1h3m22s**, the two `runs` processes accounting for the whole top of that range at 1h3m22s and 1h3m7s. **The HEAD half ran first throughout**, `ghead` before `g912` on the main set and on each class in turn, which is the driver's order. **The alone-leg riders followed the sequence**, 116 single-bench processes over four invocations of 29 --- 26 main-set shapes and the three anchors on a second reps pass --- each half clean and saturated, every invocation exiting 0.

**The decomposition reproduces on both halves for a sixth run.** The riders time each shape's `list` by itself, one bench per process on that half's own binary, `SAT=` off and on: the saturated legs split the deflation into the state the preamble puts on a clean process --- **+11.83%** on the basis and **+11.33%** on the HEAD half --- and the rest the roster adds on top of it, **-0.99%** and **+0.20%**. Run 23 read +11.70% and +12.37% for the state and +0.39% and -0.28% for the rest, Run 22 +12.12% and +12.37% and +0.15% and +0.22%. So the state term has now reproduced across six runs inside a point and a half, while the roster's own contribution has stayed under a point on every half of every run that measured it. **The tail is the same shape on both halves and it is the shape Runs 19 to 23 all named**, `stretch-tall-Mx2` at 1.0867 and 1.0798 --- a roster effect on one shape, now on five rosters and three compilers.

**Everything in this file is replaced by the next run, which is what makes it a file.** What a run replaces OUTSIDE it, in README.md and in the sources, is [README's own Provenance](../README.md#provenance). None of it is portable: a run on another machine is a different measurement rather than a repetition, which Run 19 was in a position to be firm about, having repeated one binary on one box and moved its floor by 1.7x. **What this run cannot repeat, and says so rather than implying otherwise, is that demonstration**: its roster moved, so neither half reproduces an earlier binary and the floor series 1.51%, 2.92%, 2.12%, 2.03%, 1.26% has a roster change inside its last step. What the cross-run column does carry is the same lesson in the other direction --- 33 of 45 arms within a point of the previous build of this recipe, and of the twelve outside, ten are arms whose figure is where their bytes landed and two are the degenerate `libunord` pair.

## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a `-fspec-constr` table**: it is not the regime `Data/Array/Internal.hs` compiles under. **A row's distance from Run 23's dead-spot column carries a roster term as well as an evening's drift**, which is what a roster change costs and what Run 23's own repetition did not have to say: `Main.hs` moved by two commits of 2026-09-02, so the basis half is Run 23's dead-spot recipe with the source moved and not its binary, and over the 24 shapes the two runs share 33 of their 45 shared arms read within 1% while the placement-exposed families move up to 3.5%. **This pair's halves differ in the compiler and in nothing else** --- one source, one shim, one shim environment, one roster --- so a cross-half distance is codegen and layout together, and the counted work is what separates them: where an arm's instruction count moved between the halves the compiler emitted different work, and where it did not the difference is where that work landed.

**And it is the basis half's**, `run24-g912`, as every published table here is from Run 11 on: the HEAD half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these forty-odd rows. That the published half is the 9.12 one is this pair's own decision --- it keeps the lineage, being the compiler every figure in README was measured through, and the dead-spot form it now carries is the basis recipe decided on 2026-09-02 --- and the HEAD half is the reading a form about to be published is owed on a second compiler. **Two rows here are first readings**, which is new this run: `lib-stage2-short-lean` is an arm no run has timed, and `lib-stage2-disp` is the same name re-cut from 256 to 2048, so its row has a predecessor that is not the same arm.

**Comparing runs?** The table below is Run 24's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the claims to test are [the ones after it](#the-claims-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than 1.26% from 1 on the basis half or 2.11% on the control, the HEAD half, and 0.34% and 0.19% read on the six pairs that carry across runs, beside which the worst SINGLE cells of 16.66% and 18.37% are not floors at all and are not to be quoted as any --- is [in the floor section][floor], which is where the three figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule.

**It is the main set's table**, and every column below is a statistic of that population: each stride class has a table of its own, on the same rows and in the same columns but its own basis, in [The stride classes, run by run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns:

- **time** is the geomean over **every** shape of the per-shape OLS *slope*, less that shape's forcing term, over `list`'s slope less the same term, with the per-shape log-ratios *winsorized* first --- capped at the row's own median plus or minus three MADs, the MAD scaled by 1.4826 so the cap is in standard deviations. Nothing is dropped by the estimator, so winsorizing costs no row its population and a cell far enough out to distort the mean has its influence bounded instead of its evidence deleted. **What DOES cost a row its population on this run is the correction, not the estimator**: two rows on the basis and three on the HEAD half carry cells the shared forcing pass is not smaller than, and such a cell cannot be corrected at all --- so on those rows the geomean is over 25, 24 or 23 shapes of 26, they are named in the head, and every other row covers all 26. The `CI%`, `smp` and `alloc` columns stay raw: subtracting a shared term moves a point estimate, it does not make a cell better measured. `worst` is a ratio of nets, as `time` is, just per shape and unwinsorized.

  **This replaced a trim** --- drop each strategy's single highest-CI shape --- and the ruling is worth keeping because the trim looks obviously right and is not. It selected on CI, and criterion spends a *time* budget, so a slow cell buys fewer samples and a wider CI: measured on Run 6, the cell it removed was above its own row's geomean in **30 of 41** rows, p about 0.003. It therefore deleted each strategy's worst evidence, differentially, and a catastrophic shape is exactly the shape it would remove: `bq-expand-lemire-out` loses on one shape of 33, and that shape was the one trimmed from its column. Because the cell removed differed by row, two published columns were also geomeans over different shape sets, which is why a published A/A ratio used to disagree with its paired one. Swapping estimators costs a median 2% and moves one row (`mut-offsets`) by 14%, that row having been flattered all along; it buys back exact comparability, and `--selftest` now asserts published == paired for every uncapped pair.

  **Don't reach for inverse-variance weighting**, which is the standard-looking repair and is worse than what it repairs. It assumes every shape estimates one ratio and differs only in precision, where here the between-shape variance runs a median 5,000x the within-shape kind --- the heterogeneity is the README's finding, not its error --- so weighting by precision collapses the effective shape count from 33 to about nine and hands a quarter of the weight to the smallest shape in the set. Worse for the purpose: a catastrophically slow cell buys fewer samples, so it has a wider CI, so IVW discounts precisely the cells the trim used to delete --- the same failure made continuous, not a repair of it.

  **The *slope* rather than criterion's mean, because criterion never times one call**: it times batches --- one call, then four, then twenty --- and every batch also pays for starting the timer and for the first pass through cold code and cold data. A mean divides each batch's time by its calls, so that fixed cost is smeared across them and weighs most in the small batches. The slope is the line through those points: how much more time one *additional* call adds, leaving the fixed part behind as the line's height at zero. On the microsecond shapes, hundreds of samples and no warm-up worth speaking of, the two agree. They part on the slow shapes, where the early batches run cold: there the mean reads high, and by different amounts for different strategies --- which is exactly the part that dividing by `list` cannot cancel. It also keeps `CI%` and R^2 describing the number the table shows, both being properties of that same fitted line.
- **worst** is the row's largest per-shape ratio to `list` --- the shape on which that strategy does least well against the baseline. It is what claim 1 is about, and it is raw rather than winsorized.
- **CI%** is the median across shapes of the slope's confidence half-width as a percentage of the slope --- "how many digits are real". 0.5% is three; 5% is one.
- **smp** is the median sample count. Criterion spends a time budget, so a slow call buys fewer samples; this is where that shows.
- **alloc** is bytes per call as a multiple of the result vector (`8*l`), the median over shapes of the `allocated` fit the harness now runs on every bench of every shape. The multiples were held to be shape-independent --- refitted on a different shape, every one reproduced to within 0.4% --- so that the median was a formality rather than a smoothing and the column did not move with what it was fitted on. **That is wrong**, and Run 6 (-O1) reproduced the refutation at full budget where a rough pass had found it. Re-derived on Run 9's cells and roster it is unanimous: **every one of the 32 benched rows** varies by more than 5% from shape to shape, the median row by 2.00x and the worst by 5.10x (`bq-expand-b`, 1.00x to 5.10x), and the four shapes of identical `l` = 1800000 give `bq-expand` 2.000x, 2.111x, 1.000x and 2.639x. The spread narrowed as the roster was cut --- Run 6's worst was an arm nothing times any more --- and the property it measures did not. Every allocated fit sat at R^2 1.000 on Run 6, so the spread is the quantity and not the measurement, and allocation being deterministic per call the budget does not bear on it either way. What does survive is the column: a median over a *pinned* shape set reproduces, which claim 7 now carries on a live basis, every allocation tier returning on its own level across a roster change. So read `alloc` as a statistic of a strategy **and** a shape set, and pin the shape set before comparing it across runs, exactly as the `time` column already asks. It is the one column the correction does not touch.

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.63* | *88* | *2.40x* | *its base arm, forced with one element* |
| *canon-full-nosum* | *--* | *--* | *0.57* | *108* | *1.00x* | *the same, on a write pattern that varies by shape* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.71* | *94* | *1.33x* | *the same, on a third write pattern* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.54* | *104* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *112* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *112* | *0.00x* | *the same, at the other end* |
| libunord-stage1 | 0.000 | 0.068 | 0.01 | 112 | 0.00x | new mutating `Vector` method -- stage one behind the unordered one-block test |
| libunord-stage2 | 0.000 | 0.116 | 0.02 | 112 | 0.00x | new mutating `Vector` method -- the branch's driver behind the unordered one-block test |
| lib-stage2-short | 0.029 | 0.126 | 0.65 | 100 | 1.00x | new mutating `Vector` method -- the branch's driver, a short canonical run written by a body of its length |
| lib-stage2-short-lean | 0.029 | 0.126 | 0.59 | 100 | 1.00x | new mutating `Vector` method -- the branch's driver, both of the above: a short canonical run written by a body of its length, and dispatch without the strides comparison |
| lib-stage2-lean | 0.032 | 0.126 | 0.62 | 100 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage2-concat | 0.032 | 0.128 | 0.59 | 100 | 1.00x | new mutating `Vector` method -- the branch's driver, runs sent back to a concat |
| lib-stage2 | 0.032 | 0.129 | 0.59 | 100 | 1.00x | new mutating `Vector` method -- the branch's driver |
| lib-stage2-disp | 0.032 | 0.131 | 0.58 | 100 | 1.00x | new mutating `Vector` method -- the branch's driver, slice route above a run-length threshold |
| mut-odo-vecdims-add-in-leaf-u2 | 0.034 | 0.126 | 0.58 | 100 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.034 | 0.126 | 0.60 | 100 | 1.00x | new mutating `Vector` method |
| lib-stage1 | 0.036 | 0.126 | 0.61 | 100 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| liblist-stage2 | 0.051 | 0.158 | 0.96 | 95 | 2.00x | new mutating `Vector` method -- the branch at the list entry point |
| canon-vecdims | 0.052 | 0.147 | 0.66 | 96 | 1.00x | new mutating `Vector` method |
| liblist-stage1 | 0.054 | 0.157 | 0.94 | 95 | 2.00x | new mutating `Vector` method -- stage one at the list entry point |
| canon-full | 0.056 | 0.149 | 0.68 | 94 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in | 0.056 | 0.125 | 0.61 | 96 | 1.00x | new mutating `Vector` method |
| *mut-odo-vecdims-aa* | *0.056* | *0.125* | *0.52* | *96* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.056** | 0.125 | 0.59 | 96 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *mut-odo-vecdims-aa-distant* | *0.056* | *0.126* | *0.53* | *96* | *1.00x* | *A/A control* |
| mid-copy | 0.056 | 0.125 | 0.66 | 96 | 1.00x | new mutating `Vector` method |
| bcast-set | 0.059 | 0.125 | 0.69 | 94 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.087 | 0.182 | 0.65 | 87 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.095 | 0.195 | 0.66 | 85 | 1.33x | mutable `Int` scratch |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.168* | *0.60* | *84* | *1.33x* | *A/A control* |
| **bq-scan-rem-gm-mulback** | **0.101** | 0.169 | 0.56 | 84 | 1.33x | nothing (pure) |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.101* | *0.169* | *0.40* | *84* | *1.33x* | *A/A control* |
| bq-odo-gm-mulback | 0.103 | 0.180 | 0.61 | 83 | 1.58x | nothing (pure) |
| *bq-odo-gm-mulback-aa-adjacent* | *0.103* | *0.180* | *0.50* | *83* | *1.58x* | *A/A control* |
| *bq-odo-gm-mulback-aa-distant* | *0.104* | *0.179* | *0.45* | *83* | *1.58x* | *A/A control* |
| *mut-odo-aa-distant* | *0.106* | *0.256* | *0.87* | *82* | *1.00x* | *A/A control* |
| build | 0.106 | 0.267 | 0.95 | 82 | 1.00x | new mutating `Vector` method |
| *mut-odo-aa-adjacent* | *0.106* | *0.272* | *0.91* | *82* | *1.00x* | *A/A control* |
| mut-odo | 0.106 | 0.273 | 1.24 | 82 | 1.00x | new mutating `Vector` method |
| *build-aa-distant* | *0.108* | *0.270* | *1.36* | *82* | *1.00x* | *A/A control* |
| *build-aa-adjacent* | *0.108* | *0.262* | *1.31* | *82* | *1.00x* | *A/A control* |
| bq-expand-gm-mulback | 0.108 | 0.223 | 0.60 | 84 | 2.52x | nothing (pure) |
| bq-expand | 0.119 | 0.229 | 0.57 | 82 | 2.40x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.119* | *0.229* | *0.56* | *82* | *2.40x* | *A/A control* |
| *bq-expand-aa-distant* | *0.119* | *0.229* | *0.49* | *82* | *2.40x* | *A/A control* |
| offtab-scan-rem | 0.132 | 0.222 | 0.85 | 80 | 2.00x | nothing (pure) |
| *list-aa-distant* | *0.999* | *1.011* | *0.31* | *46* | *23.50x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.38 | 46 | 23.50x | -- |
| *list-aa-adjacent* | *1.001* | *1.012* | *0.30* | *46* | *23.50x* | *A/A control* |
| gen-unsafe | 1.094 | 3.031 | 1.66 | 42 | 1.00x | -- |
| *gen-unsafe-aa-adjacent* | *1.100* | *2.988* | *1.80* | *42* | *1.00x* | *A/A control* |
| *gen-unsafe-aa-distant* | *1.108* | *3.035* | *1.76* | *42* | *1.00x* | *A/A control* |

`concat-runs` has no row, and neither do the other 43 arms the roster holds and checks without timing --- 44 of its 96 in all: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). So a movement below is a movement on the 46 arms this run and Run 23 both give a corrected time, on two builds of one recipe two days apart, and it is a roster change and an evening and not a code change.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table lost five of its rows to the parking and gained one to the roster**: `mut-odo-vecdims` reads 0.056 with **fourteen** timed arms below it and **three** level --- where Run 23 printed nineteen below and one level --- and the arithmetic is the roster's, four of the nineteen having been parked to `Only` on 2026-09-02 (`lib-stage2-u4`, `mut-odo-vecdims-add-in-leaf`, its `-down` twin and `canon-memcpy-r2`), `lib-stage2-short-lean` having landed, and `canon-full` and `mut-odo-vecdims-add-in` reading level where they read below. The fourteen are the two `libunord` arms at 0.000, `lib-stage2-short` and the new composite at 0.029, four `lib-stage2*` arms at 0.032, the two `-u2` leaf arms at 0.034, `lib-stage1` at 0.036, `liblist-stage2` at 0.051, `canon-vecdims` at 0.052 and `liblist-stage1` at 0.054. **The ceiling reproduced on the arm the class property names, for an eighth run, once the shape set is pinned**: `mut-odo-vecdims` against `bq-scan-rem-gm-mulback` reads **0.5469 at 23 wins of 24** over Run 23's own 24 shapes against Run 23's 0.5466, where over this run's 26 it reads 0.5493 and over the 25 excluding `stretch-inner1` 0.5312. **And the `alloc` column is Run 23's to the digit on the basis once the shape set is pinned**: the fills at 1.00x, the two `libunord` arms at 0.00x, `list` at 23.50x, and the eight rows that read above Run 23's here, at three distinct values --- `bq-odo-gm-mulback` and its two twins 1.58x against 1.51x, `bq-expand` with its three twins and its `-nosum` 2.40x against 2.35x, and `bq-expand-gm-mulback` 2.52x against 2.35x --- read Run 23's figures exactly, every one of the eight, over Run 23's own 24 shapes, the median having moved with its population and not with what any arm allocates --- while across the halves 1118 of the 1300 allocating main-set cells agree to 1e-4, where Run 23's one-compiler pair agreed on 1245 of 1272 and Run 22's two-compiler pair on 1123.

**The leaf block's ordering is unchanged and its widest gap is gone with the arm that carried it.** `genericFillStrided` in `Data/Array/Internal.hs` is a bang-for-bang port of `mut-odo-vecdims-add-in-leaf-u2`. Against `mut-odo-vecdims` that arm reads **0.6404 at 24 of 25, sign p 1.5e-06** on the basis and **0.6395 at 24 of 25** on the HEAD half --- a thousandth apart --- so the shipped code is 36% ahead of the code it was refined from on both compilers alike, against Run 23's 0.6342 on its basis and 0.5999 on its dead-spot half. **The count-down variant is now level with it**, `-u2` reading 0.9992 of `-add-in-leaf-u2-down` on the basis at 14 of 25 and 0.9958 on HEAD at 19 of 25 --- so `-u2` is the faster of the two by a hair on both halves, both readings inside their halves' floors --- and the same pair read 0.9970 at 15 of 23 on Run 23's dead-spot half, so this is a reproduction and not a movement. What has gone is the twenty-point deficit Run 23 published for `-add-in-leaf-down`, the NON-`-u2` count-down arm, which was parked to `Only` the same day and no process this run times. **What the dispatch around the fill costs moved and moved on both halves**: `lib-stage1`, that same fill reached through the library's own regime test, reads **1.0640** of the bare arm on the basis and **1.0702** on HEAD, against Run 23's 1.0389 and 1.0430 --- so a user's `toVectorT` pays six to seven percent over the kernel on this roster where it paid four on the last, on both compilers alike, which makes it the roster's doing and not HEAD's.

**The two standing placement controls read alike on both halves, which is not what either read a run ago.** `mut-odo-vecdims-add-in` against the arm it varies reads **0.9975 at 14 of 25, sign p 0.69** on the basis and **0.9996 at 12 of 25, p 1** on HEAD, where Run 23 read 0.9901 at 19 of 24 and 0.9896 at 21 of 24: a tie on both halves this run, and neither figure clears its half's six-pair threshold of 0.34% and 0.19% --- 0.25% and 0.04% --- so the ordering Run 23 read three runs running is not readable here. `build` against `mut-odo` is the other, and it is a tie on both halves too --- 0.9920 at 15 of 25 and 0.9782 at 15 of 25, both intervals covering 1 --- where the dead-spot switch opened five and a half points between Run 23's halves. Both pairs' loops sit where post-run step 0's twin names them, `fbBuild` and `fbMutOdo` at offset 0 on the basis, so nothing in their placement separates them either.


## What the next run compares against

**Run 25's regime, pair, roster and shape set are all open: nothing about the next run was decided when this one ran, and this section says only what it must be read against.** The regime is `-fspec-constr`, as every run since Run 8, and it is the regime the claims decide in; the shipped file does not set the flag ([the ceiling](../README.md#the-mutable-ceiling-taken)). **What this run settles about the basis is that it survived a change of compiler**: the dead-spot form is the published basis as of Run 24, and its orderings hold on HEAD --- (1) to (3) of the registration read the same way on both halves, no ordering reversing past HEAD's floor --- so the form is not one compiler's accident and the next pair need not re-ask it. **What it leaves live** is the threshold work: `lib-stage2-disp` re-cut to 2048 now leads the `runs` class outright and reads at or below the better of `lib-stage2` and `lib-stage2-concat` at every length on both halves, where Run 23 read the dispatch killed at `runs-1024` on both halves, and the three probe arms `lib-stage2-disp-2048`, `-8192` and `-32768` sit parked in the roster for a run that wants to cut it finer. **What is NOT a candidate** is unchanged: a pair varying the allocation area, closed 2026-08-21, and one varying the roster between its halves, refused because it would break `preflight`'s `check` comparison and both drivers' bench counts.

**The compiler variable was asked once more and it paid this time, for a reason Runs 19 to 22 could not have found.** Those four each varied the compiler on a roster whose layout the shim had not placed off the execution path, and the last three read the same answer. This pair varies it on the dead-spot form and the counted work is what makes it new: the two compilers differ by 5.7% and 6.8% of the INSTRUCTIONS on the two pure mul-back arms and by about one percent on the branch's fills, in opposite directions, and every arm whose count ratio is 1.0000 --- `build`, `mut-odo`, `gen-unsafe` and their six twins --- still moves up to six percent in time. So a compiler pair prices two things at once and only the counted work separates them, which is the reading Run 23 could not take with one compiler on both halves and Runs 19 to 22 could not take without the counts on every population.

**What Run 24 leaves the next run to read against, and the first item is not a figure.** **The box did not change**, its gate machine check reading +0.56% against the fingerprint Run 23 kept over 24 of 26 shapes and the run's own two main-set processes reading -0.20% and -0.39% against that same fingerprint, worst +2.67%, -1.78% and -2.80% and none past 5%; so absolutes cross from Run 23 to Run 24 freely and the boundary that matters is still the BIOS change before Run 18. **The floor is 1.26% on the basis and 2.11% on the control**, with the restricted six at 0.34% and 0.19%. A Run 25 margin is judged on both and they answer different questions: the six-pair figure is what two rows of one table must clear, the sixteen-pair one is how far an arm differs from its own duplicate. **And it is not inherited**: this run's basis floor is the tightest of the last five, 1.51%, 2.92%, 2.12%, 2.03%, 1.26%, and its roster moved, so a Run 25 margin is judged against Run 25's own. **The two columns below MAY be differenced**: `list` moved **0.25%** between the halves over all 26 shapes, against the 0.7% bar, where Run 23 read 0.33% and Run 22 0.81% and was refused. Five of the nine classes are past that bar and their blocks say so. What the columns price is the compiler, and the counted-work column says which movements that reaches: the two pure mul-back arms 5.7% and 6.8% apart ON their instruction counts, the `lib-stage2*` family about one, and the placement-exposed arms apart at count ratios of 1.0000, so a movement on one of those is layout or runtime and nothing else.

**Registered with the pair.** Run 24's six registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, transcribed into Provenance below before that note goes with the pair. **What Run 25 inherits is the same five riders, routine, and one instrument used for the first time in anger**: the alone legs, the counted-work sweeps over every population, the saturating preamble, the per-sample load fields and `--counts` all ran to form, and post-run step 0's `-g3` twin named every straddling loop on the basis half and refused two of four on HEAD, so the count check both spoke and refused inside one run. **What it inherits as a warning** is about registrations, not about arms: registration 5's second clause named `mut-odo-vecdims-add-in-leaf-down`, an arm parked to `Only` by the same commit the registration was written beside, so a clause of a registered prediction was unreadable before the run started and nothing checked it. `--lint` refuses a live CLAIM that names a parked arm; it does not read a registration.

**The position term was the candidate Run 15 promoted, and the probes have since spent it.** What Run 14 first saw and Run 15 confirmed is resolved as small-pinned churn --- selector found, ladder re-sized, no poison set --- in [the position-term entry][open] and `small-pinned-churn-investigation/nursery-position-findings2.txt`, so the roster-order pair this paragraph used to ask for is not owed: the corrected scans priced the term per shape in filtered processes, without a pair and without a layout term to argue about.

**The allocation area has now been priced twice and does not want a third pair** --- a ruling superseded in scope, 2026-08-19, and kept because what it refused stays refused. Run 14 took the area at `-A1G` and could not subtract its halves' absolutes; Run 15 took it at `-A32m` and found the cost at about 6% of the roster's time --- so re-PRICING default-against-enlarged is spent, and Run 16's pair does not do that: it changes the published basis to `-A32m` and reads `-A64m` against it, the one comparison neither earlier pair made and the one the churn findings' recommendation turns on, in the saturated in-process state both halves share. On 2026-08-21 the area was fixed at `-A32m` outright, here and in every horde-ad suite, so the one-binary runner this section used to ask for is not owed, and no further `-A` question is the README's.

**Where a run changes basis, the new basis is checked against the half at its OWN allocation area and against no other**, which is the rule the Run 15 to Run 16 change settled and the one place *against the previous run* can still be ambiguous. **The six figures that follow are Run 16's, are no longer checkable, and are stamped so that no later run reads them as its own**, `run15-*` and `run16-*` having been deleted; they are kept as the evidence the ruling was taken on. Against `run15-a32m` Run 16's three anchors read **-0.66%, -1.01% and -0.06%**, every one well inside the 2.32% floor it measured; against `run15-lookrts` the same three would have read **+8.81%, -9.57% and +7.74%**, which is the allocation area and not the shapes, and would have put all three outside that floor for a reason that is not theirs. Distance from a half at another area is that area plus whatever else moved; only distance from the half at this run's own area is drift.

**A pair's two halves are never folded into one.** Merging them puts back, in the record built to outlive every artifact, exactly the term the pairing exists to separate --- and what a given pair's two columns price is that run's own file's to say, not this section's. `--check-doc` catches one half of it: a run named aligned must also be named unaligned. Pruning an aligned column, merging two, and naming a second half accurately are the reading's to catch --- the check cannot demand an unaligned half of every pair without failing the last two runs, which have none, nor an aligned column of every run without failing Runs 6 through 9, which had none either.

**The next run compares against Run 24 and against nothing before it.** Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it, and walking that chain here is what this section stopped doing. So an older run is read by opening its file, not by reading a column across. This run's own two halves, on the rows nearest the decisions --- `dead-spot +lookrts` in the column heads being this run's basis recipe, on the basis half since 2026-09-02, and the compiler being this pair's only variable:

| strategy | Run 24 (SpecConstr, dead-spot +lookrts, -A32m, 9.12.4) | Run 24 (SpecConstr, dead-spot +lookrts, -A32m, GHC HEAD) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.056** | 0.056 |
| `mut-flat-gm` | **0.087** | 0.088 |
| `bq-mut-runs-gm-mulback` | **0.095** | 0.097 |
| `bq-odo-gm-mulback` | **0.103** | 0.111 |
| `bq-scan-rem-gm-mulback` | **0.101** | 0.107 |
| `bq-expand` | **0.119** | 0.120 |
| `build` | **0.106** | 0.106 |

**A published geomean is over the same 26 shapes, and two halves of one SpecConstr run usually share a denominator too**, `list` moving under 0.7% between them --- so such a pair may be subtracted and not merely ordered, which is what an -O1 reading cannot do at an 8% baseline shift. **THE TABLE ABOVE IS SUCH A PAIR**, `list` having moved 0.25% on this run's main set, so the two columns may be differenced --- and what the difference reads is nothing on `mut-odo-vecdims` and `build`, a thousandth on `mut-flat-gm` and `bq-expand`, two on `bq-mut-runs-gm-mulback` and **six and eight thousandths on the two arms needing nothing at all**, which is the pair's whole story in two rows and is instructions rather than placement, the counted work reading 0.9426 and 0.9325 on them. **A pair that varies the allocation area is the exception, and its two halves may never be subtracted from each other.** `list` moved **9.20%** between Run 14's halves, **5.13%** between Run 15's and **16.51%** between Run 16's. **Run 16's is the largest of the three and was registered to be the smallest**, on the reasoning that its two halves both sit at enlarged areas where the earlier two each crossed the default --- a prediction refuted by its own run, and the refutation is the finding: what moves the baseline is not the distance from the default but the in-process deflation, which at roster scale is worse at 64 MB than at 32 MB by more than the whole default-to-32 MB step was worth. So the exception widens rather than narrowing, and it covers every pair that varies the area at all. Every cell of such a pair's second column is scaled by a denominator the pairing moved: read it for the pairing's direction, take no strategy quality off it, and read the arm-by-arm comparison at the head of this file instead, which divides absolutes rather than ratios.

**The HEAD half's own standings on the arms this run's roster changed, which no table here carries, every published table being the basis half's.** Read off `run24-ghead-*.json` with `--pair`, paired geomeans, the main set over the 25 shapes that exclude `stretch-inner1` and the basis half's reading in brackets: `lib-stage2-short` against `lib-stage2` **0.9140** at 20 of 25 on the main set (0.9184), 0.9249 on `window` (0.9095), 0.9766 on `runs` with `runs-2` at 0.898 (0.9813, and 0.890 there) and 0.9651 on `slice` (0.9422); `lib-stage2-lean` against `lib-stage2` 0.9648 on the main set (0.9695), with `lenet-slice-c6-k5` at 0.788 and `cnn-slice-c32` at 0.793 (0.771 and 0.847); the new `lib-stage2-short-lean` against `lib-stage2-short` 0.9718 on the main set (0.9693) and against `lib-stage2-lean` 0.9207 (0.9182); `lib-stage2` against `lib-stage1` 0.9376 on the main set (0.9533) and 0.9929 on `slice` (1.0146); `lib-stage2-disp` against `lib-stage2` on `runs` 0.9710 with `runs-16384` at 0.870 (0.9716, and 0.871 there); and `lib-stage1` against the bare `-add-in-leaf-u2` 1.0702 (1.0640). So on the second compiler every ordering the basis half reads holds in direction: the short arm's margins are a few points wider on `slice` and narrower on `runs`, the composite's are within three thousandths of the basis's on both parents, and `lib-stage2` moves ahead of `lib-stage1` on `slice`, where the basis has it a point and a half behind.

**Each stride class has its own table below.** Run 8 re-ran every class with the populations pinned, and every run since has again, so each class's paragraph carries what the last change moved and the table above it is what Run 13 reads against. **The two sides of a class comparison across the Run 11/Run 12 boundary are not the same build**, and this is the one place that bites: Run 11's class tables are its *aligned* half's, Run 12's are its *max-skip* basis half's, and the main set prices that difference at nothing below 0.99 and up to 1.06. So read a class figure that moved a point or two across that boundary as the shim rather than as the class, and take the two Run 12 columns above as what a same-build comparison looks like. From Run 13 on, both sides are max-skip again.

**Two tables in this file are NOT installed and are edited by hand: the two-column one above and the cross-class summary below.** Every other table a run publishes comes from `install-tables.sh` and is replaced whole. The one above is replaced whole too, being this run's own halves and no earlier run's; the summary gains a row per run instead. A hand-edited table is edited with the whole line named, never with a prefix anchor. On Run 17 an insertion anchored on ``| `arm` | `` matched an earlier table and put two cells into the element-type probe's header and a loop-offsets row; `--check-doc`'s width pass caught it in the same call, which is the only reason it cost minutes. Name the whole row, assert it occurs exactly once, and read the width check's verdict afterwards.

And because a geomean cannot say *where* it moved, the **fingerprint** below is kept so a future disagreement can be localised rather than only noticed; its membership rule, the column heads and the rulings on dropping a column are [in the README's per-shape section](../README.md#per-shape-where-the-geomean-hides-the-ordering). Run 24 adds none, and the installer's membership note names eleven candidates rather than four: `libunord-stage2` and `libunord-stage1` are best outside the family on 17 and 15 shapes, which is their one-block test returning a slice and not a fill leading anything; `lib-stage2-short-lean` on 13, `lib-stage1` on 4, `lib-stage2-lean`, `liblist-stage2`, `lib-stage2-short` and `canon-full` on 3 apiece, and `lib-stage2`, `lib-stage2-concat` and `lib-stage2-disp` on 1 each --- a spread that is itself the roster's news, the library's own family having taken the shapes the candidates used to win. Every one of them is a column the basis decision's to grant, and none is granted here, so the fourteen stand.

| shape | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `lenet-slice-c6-k5` | 5 | 150 | 2.74 us | 0.081 | 0.152 | 0.169 | 0.134 | 0.124 | 0.158 | 0.153 | 0.147 | 0.083 | 0.086 |
| `cnn-slice-c32` | 3 | 288 | 5.97 us | 0.084 | 0.142 | 0.154 | 0.181 | 0.176 | 0.150 | 0.168 | 0.115 | 0.085 | 0.090 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.13 us | 0.095 | 0.181 | 0.148 | 0.205 | 0.199 | 0.188 | 0.163 | 0.104 | 0.100 | 0.098 |
| `cnn-L1-12x12-c1` | 3 | 1296 | 28.6 us | 0.074 | 0.144 | 0.107 | 0.189 | 0.184 | 0.154 | 0.132 | 0.067 | 0.076 | 0.077 |
| `stretch-rank12` | 2 | 4096 | 109 us | 0.094 | 0.182 | 0.134 | 0.267 | 0.273 | 0.195 | 0.171 | 0.072 | 0.102 | 0.100 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 114 us | 0.068 | 0.128 | 0.097 | 0.177 | 0.174 | 0.138 | 0.124 | 0.058 | 0.070 | 0.072 |
| `conv1d-24` | 3 | 5184 | 99.2 us | 0.058 | 0.071 | 0.100 | 0.125 | 0.125 | 0.077 | 0.136 | 0.058 | 0.057 | 0.061 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 364 us | 0.048 | 0.092 | 0.094 | 0.106 | 0.107 | 0.102 | 0.121 | 0.044 | 0.049 | 0.052 |
| `gather48-src-50` | 3 | 22500 | 429 us | 0.054 | 0.067 | 0.098 | 0.118 | 0.118 | 0.076 | 0.129 | 0.053 | 0.053 | 0.057 |
| `stretch-rank10` | 3 | 59049 | 1.27 ms | 0.066 | 0.108 | 0.105 | 0.155 | 0.164 | 0.118 | 0.138 | 0.055 | 0.066 | 0.070 |
| `stretch-coprime-r7` | 13 | 60060 | 1 ms | 0.035 | 0.083 | 0.094 | 0.059 | 0.060 | 0.095 | 0.124 | 0.033 | 0.035 | 0.038 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.06 ms | 0.058 | 0.090 | 0.099 | 0.136 | 0.144 | 0.099 | 0.128 | 0.057 | 0.058 | 0.061 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.46 ms | 0.058 | 0.091 | 0.100 | 0.136 | 0.135 | 0.099 | 0.128 | 0.057 | 0.058 | 0.061 |
| `stretch-primes` | 89 | 250357 | 4 ms | 0.029 | 0.074 | 0.093 | 0.030 | 0.030 | 0.086 | 0.131 | 0.029 | 0.028 | 0.030 |
| `stretch-inner1` | 1 | 500000 | 12.9 ms | 0.091 | 0.030 | 0.071 | 0.219 | 0.201 | 0.030 | 0.072 | 0.000 | 0.090 | 0.098 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 15.9 ms | 0.045 | 0.076 | 0.095 | 0.090 | 0.095 | 0.086 | 0.126 | 0.044 | 0.045 | 0.051 |
| `vgg-14-c512-k3` | 3 | 903168 | 18.6 ms | 0.058 | 0.089 | 0.099 | 0.138 | 0.142 | 0.098 | 0.130 | 0.058 | 0.058 | 0.061 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 18.4 ms | 0.035 | 0.071 | 0.090 | 0.054 | 0.055 | 0.082 | 0.131 | 0.033 | 0.035 | 0.037 |
| `stretch-inner256` | 256 | 1750784 | 32.9 ms | 0.032 | 0.068 | 0.085 | 0.033 | 0.033 | 0.074 | 0.117 | 0.032 | 0.032 | 0.031 |
| `stretch-pow2stride` | 64 | 1769472 | 28.3 ms | 0.125 | 0.121 | 0.147 | 0.125 | 0.126 | 0.133 | 0.222 | 0.125 | 0.125 | 0.125 |
| `stretch-r5-8x432` | 8 | 1769472 | 33.6 ms | 0.033 | 0.061 | 0.083 | 0.055 | 0.053 | 0.069 | 0.117 | 0.032 | 0.032 | 0.034 |
| `stretch-square-1341` | 1341 | 1798281 | 29.7 ms | 0.087 | 0.131 | 0.154 | 0.087 | 0.089 | 0.140 | 0.203 | 0.085 | 0.088 | 0.087 |
| `stretch-bigstride` | 3 | 1800000 | 49 ms | 0.035 | 0.045 | 0.067 | 0.080 | 0.079 | 0.051 | 0.094 | 0.035 | 0.035 | 0.038 |
| `stretch-tab7MB` | 2 | 1800000 | 37.4 ms | 0.063 | 0.063 | 0.101 | 0.142 | 0.146 | 0.070 | 0.143 | 0.063 | 0.063 | 0.068 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 39.2 ms | 0.023 | 0.051 | 0.063 | 0.023 | 0.023 | 0.058 | 0.095 | 0.023 | 0.023 | 0.023 |
| `stretch-wide-2xM` | 2 | 1800000 | 37.6 ms | 0.063 | 0.061 | 0.099 | 0.139 | 0.154 | 0.070 | 0.140 | 0.062 | 0.062 | 0.067 |

| shape | class | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bcast-inner8` | `bcast` | 8 | 51200 | 879 us | 0.032 | 0.066 | 0.089 | 0.060 | 0.053 | 0.080 | 0.118 | 0.032 | 0.032 | 0.030 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 27.8 ms | 0.021 | 0.070 | 0.086 | 0.021 | 0.022 | 0.087 | 0.121 | 0.022 | 0.021 | 0.018 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 37.1 ms | 0.063 | 0.062 | 0.099 | 0.147 | 0.149 | 0.071 | 0.139 | 0.063 | 0.062 | 0.058 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.41 ms | 0.059 | 0.094 | 0.099 | 0.142 | 0.142 | 0.102 | 0.128 | 0.059 | 0.012 | 0.062 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 3.92 ms | 0.022 | 0.070 | 0.087 | 0.023 | 0.023 | 0.087 | 0.123 | 0.022 | 0.013 | 0.024 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 46.8 ms | 0.036 | 0.046 | 0.069 | 0.080 | 0.082 | 0.055 | 0.094 | 0.036 | 0.033 | 0.039 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 41.6 ms | 0.023 | 0.054 | 0.067 | 0.024 | 0.024 | 0.061 | 0.090 | 0.023 | 0.019 | 0.023 |
| `reshape1-rank10` | `reshape1` | 1 | 59049 | 1.95 ms | 0.105 | 0.122 | 0.089 | 0.295 | 0.287 | 0.124 | 0.090 | 0.000 | 0.108 | 0.100 |
| `reshape1-r3` | `reshape1` | 1 | 180000 | 4.94 ms | 0.087 | 0.031 | 0.070 | 0.237 | 0.233 | 0.031 | 0.070 | 0.000 | 0.086 | 0.080 |
| `reshape1-strided-r3` | `reshape1` | 1 | 180000 | 4.91 ms | 0.091 | 0.032 | 0.072 | 0.220 | 0.231 | 0.032 | 0.072 | 0.015 | 0.089 | 0.084 |
| `reshape1-500k` | `reshape1` | 1 | 500000 | 13.5 ms | 0.086 | 0.029 | 0.069 | 0.213 | 0.219 | 0.029 | 0.069 | -- | 0.085 | 0.079 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 114 us | 0.068 | 0.128 | 0.096 | 0.167 | 0.175 | 0.135 | 0.122 | 0.056 | 0.070 | 0.073 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 431 us | 0.052 | 0.066 | 0.097 | 0.126 | 0.119 | 0.075 | 0.128 | 0.052 | 0.053 | 0.056 |
| `rev-primes` | `rev` | 89 | 250357 | 3.99 ms | 0.029 | 0.073 | 0.092 | 0.031 | 0.031 | 0.085 | 0.131 | 0.029 | 0.029 | 0.030 |
| `revsome-outer-g48` | `revsome` | 3 | 22500 | 443 us | 0.053 | 0.067 | 0.098 | 0.116 | 0.115 | 0.075 | 0.127 | 0.053 | 0.052 | 0.056 |
| `revsome-mid-cnn-L2` | `revsome` | 3 | 165888 | 3.51 ms | 0.057 | 0.088 | 0.097 | 0.134 | 0.139 | 0.097 | 0.126 | 0.055 | 0.057 | 0.061 |
| `revsome-inner-primes` | `revsome` | 89 | 250357 | 4.01 ms | 0.030 | 0.080 | 0.103 | 0.031 | 0.031 | 0.093 | 0.132 | 0.030 | 0.030 | 0.031 |
| `runs-65536` | `runs` | 65536 | 1769472 | 26.1 ms | 0.027 | 0.075 | 0.093 | 0.027 | 0.027 | 0.088 | 0.134 | 0.028 | 0.027 | 0.028 |
| `runs-16384` | `runs` | 16384 | 1785856 | 26 ms | 0.029 | 0.077 | 0.093 | 0.029 | 0.029 | 0.090 | 0.138 | 0.029 | 0.028 | 0.028 |
| `runs-4096` | `runs` | 4096 | 1798144 | 26.6 ms | 0.028 | 0.075 | 0.091 | 0.028 | 0.028 | 0.088 | 0.135 | 0.029 | 0.028 | 0.029 |
| `runs-1024` | `runs` | 1024 | 1799168 | 26.6 ms | 0.028 | 0.074 | 0.090 | 0.028 | 0.028 | 0.088 | 0.137 | 0.028 | 0.028 | 0.030 |
| `runs-512` | `runs` | 512 | 1799680 | 26.6 ms | 0.029 | 0.074 | 0.090 | 0.028 | 0.029 | 0.088 | 0.134 | 0.029 | 0.028 | 0.030 |
| `runs-256` | `runs` | 256 | 1799936 | 26.8 ms | 0.028 | 0.074 | 0.091 | 0.028 | 0.028 | 0.087 | 0.134 | 0.029 | 0.028 | 0.030 |
| `runs-7` | `runs` | 7 | 1799994 | 29.5 ms | 0.038 | 0.071 | 0.096 | 0.064 | 0.063 | 0.082 | 0.138 | 0.038 | 0.037 | 0.041 |
| `runs-2` | `runs` | 2 | 1800000 | 37.6 ms | 0.063 | 0.063 | 0.101 | 0.146 | 0.146 | 0.069 | 0.146 | 0.062 | 0.063 | 0.068 |
| `runs-3` | `runs` | 3 | 1800000 | 33.9 ms | 0.052 | 0.066 | 0.099 | 0.112 | 0.114 | 0.075 | 0.142 | 0.052 | 0.052 | 0.055 |
| `runs-4` | `runs` | 4 | 1800000 | 31.9 ms | 0.046 | 0.068 | 0.098 | 0.091 | 0.094 | 0.078 | 0.138 | 0.045 | 0.045 | 0.050 |
| `runs-5` | `runs` | 5 | 1800000 | 31.5 ms | 0.042 | 0.068 | 0.094 | 0.078 | 0.083 | 0.077 | 0.134 | 0.042 | 0.042 | 0.045 |
| `runs-9` | `runs` | 9 | 1800000 | 29.7 ms | 0.034 | 0.070 | 0.092 | 0.055 | 0.055 | 0.081 | 0.133 | 0.034 | 0.034 | 0.037 |
| `runs-96` | `runs` | 96 | 1800000 | 26.8 ms | 0.028 | 0.074 | 0.091 | 0.031 | 0.031 | 0.087 | 0.139 | 0.028 | 0.029 | 0.029 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 27 ms | 0.030 | 0.075 | 0.093 | 0.034 | 0.034 | 0.088 | 0.137 | 0.028 | 0.030 | 0.031 |
| `scaled-r5` | `scaled` | 13 | 15015 | 246 us | 0.033 | 0.074 | 0.095 | 0.050 | 0.050 | 0.084 | 0.130 | 0.031 | 0.034 | 0.036 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 959 us | 0.028 | 0.072 | 0.091 | 0.032 | 0.033 | 0.081 | 0.126 | 0.028 | 0.028 | 0.029 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 4.83 ms | 0.032 | 0.071 | 0.088 | 0.032 | 0.032 | 0.080 | 0.132 | 0.032 | 0.033 | 0.032 |
| `slice-coprime-r7` | `slice` | 13 | 60060 | 1.02 ms | 0.036 | 0.083 | 0.095 | 0.062 | 0.061 | 0.094 | 0.127 | 0.037 | 0.036 | 0.039 |
| `slice-cnn-L2-24x24-c32` | `slice` | 3 | 165888 | 3.53 ms | 0.058 | 0.089 | 0.098 | 0.138 | 0.142 | 0.094 | 0.129 | 0.058 | 0.059 | 0.061 |
| `slice-primes` | `slice` | 89 | 250357 | 3.95 ms | 0.030 | 0.082 | 0.106 | 0.032 | 0.032 | 0.094 | 0.134 | 0.031 | 0.030 | 0.031 |
| `window-28x28-k5` | `window` | 5 | 14400 | 260 us | 0.044 | 0.078 | 0.095 | 0.096 | 0.094 | 0.088 | 0.122 | 0.045 | 0.045 | 0.048 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 884 us | 0.094 | 0.047 | 0.073 | 0.270 | 0.232 | 0.047 | 0.073 | 0.020 | 0.095 | 0.103 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.16 ms | 0.056 | 0.087 | 0.096 | 0.150 | 0.133 | 0.098 | 0.126 | 0.057 | 0.058 | 0.061 |
| `window-128x128-k7` | `window` | 7 | 729316 | 12.4 ms | 0.036 | 0.073 | 0.092 | 0.076 | 0.070 | 0.087 | 0.123 | 0.037 | 0.036 | 0.041 |

**One row to read first, and it is a property of the shape and not of any arm**: `stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension behaves differently there by construction. **This run the correction gives out on far fewer cells than last**, and on different ones per half: five cells sink below the shared forcing pass on the basis --- both `libunord` arms on `stretch-inner1` and `stretch-wide-2xM`, and `libunord-stage2` on `stretch-square-1341` --- so two rows are geomeans over 24 and 23 shapes of 26 and every other row covers all 26, where Run 23's dead-spot half sank fifteen cells across eleven rows. On the HEAD half six sink across three rows: the two `libunord` arms on `stretch-pow2stride` and `vgg-14-c512-k3`, `libunord-stage2` on `stretch-square-1341`, and `lib-stage2-lean` alone on `stretch-inner1`. **So the `lib-stage2` family no longer sinks on `stretch-inner1` at all on the basis**, which is what a roster whose fills are all dead-spot builds looks like, and the registration figures in the last section are still taken over the 25 shapes that exclude it, so that the two halves are read over one population. The two rows this paragraph used to name are retired with the arms that derived them.


## The claims the next run should test

**Run 24's verdicts first**, since a run reports breaks rather than re-deriving the table. **The one manifest claim left held on both halves**, all four of claim 1's links on the 9.12 basis and all four on the HEAD half --- no BROKE on either, a **seventh** clean sweep running, and the first read across two compilers since Run 22. What this run adds to the sweep is the second compiler's own answer: the top link is a thousandth apart between the halves, and the two links below it are four and five points WIDER on HEAD, which the counted work attributes to the two arms needing nothing at all rather than to anything the ladder prices. Every arm claim 1 names is still timed, and `--pair` recovers any retired ordering in one call whenever it is wanted.

**The six retired claims are not re-read here.** Claims 3, 4, 5 and 9 left the manifest at Run 19's write-up, on a sweep in which all thirteen held on both of that run's halves; claims 2 and 6 left on 2026-08-28 with the parking of the arms their surviving links turned on, and their last readings are Run 20's, in that run's own file. The numbered items below say what each was in a clause. Run 23 does not re-derive any of them and quotes none as its own: of the arms they named, those still rostered and timed put any of those orderings one `--pair` call away, and the parked ones would want a run that re-times them --- which is the whole of what retiring them gave up.

**Claim 1 held on all four links, on both halves, and the second compiler widens the bottom of the ladder.** The four links are what the `needs` column draws: what a mutating `Vector` method buys (**0.6462** on the basis), what one more mutable write pattern buys (0.9102), and what a mutable `Int` scratch buys against the two fastest arms needing nothing (0.9252 and 0.9337). On the HEAD half the same four hold at **0.6429, 0.9017, 0.8780 and 0.8883** --- the top link three thousandths from the basis's, the second under a point, and the third and fourth four and a half to five points wider, 4.72 and 4.54. Against Run 23's basis readings of 0.6521, 0.9180, 0.9133 and 0.9130 the four moved by 0.0059, 0.0078, 0.0119 and 0.0207; the first three sit inside this run's 1.26% floor as movements of a ratio near 1 do not, so read them against the two-day-old build of this recipe rather than as drift, the roster having moved between them.

**Readings:** `mut-odo-vecdims` / `mut-flat-gm` 0.6462, 22 of 26, sign p 0.00053; `mut-flat-gm` / `bq-mut-runs-gm-mulback` 0.9102, 26 of 26, sign p 3e-08; `bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` 0.9252, 21 of 26, sign p 0.0025; `bq-mut-runs-gm-mulback` / `bq-scan-rem-gm-mulback` 0.9337, 19 of 26, sign p 0.029. 4 of 4 registered orderings held.

**The first link's top rung still understates what a mutating method buys by a factor.** Claim 1 reads `mut-odo-vecdims` against `mut-flat-gm`, and **fourteen** arms read below `mut-odo-vecdims` with **three** more level with it, at 0.000 to 0.054 against its 0.056 --- Run 23's nineteen and one, less the four parked to `Only` on 2026-09-02 and plus the composite arm that landed. **Two of the fourteen are not fills at all**, `libunord-stage1` and `libunord-stage2` at 0.000, which return a single `VS.slice` where their one-block test fires and so measure dispatch; the other twelve do the work. **And the shipped library route sits well inside the group**, `lib-stage1` at 0.036, as does every one of the candidates. Whether the claim should be re-aimed at the family's leader is a question for the next run and is [under the recommended tasks](../README.md#recommended-tasks-after-run-24); it is not re-aimed here, a claim being re-aimed on a decision and not on one reading.

**Claim 7 held on every level, on both halves --- and two of the published levels moved with the SHAPE SET and not with the code, which is the second reading this run takes of that lesson.** The levels are the mutable fills at 1.00x, the scan family 1.33x, `bq-odo-gm-mulback` 1.58x, `offtab-scan-rem` 2.00x, `bq-expand` 2.40x, `list` 23.50x, and the floor under the floor, `libunord-stage1` and `libunord-stage2` at **0.00x**. Eight rows read differently from Run 23, at three distinct values: `bq-odo-gm-mulback` and its two twins at 1.58x where Run 23 published 1.51x, `bq-expand` with its three twins and its `-nosum` at 2.40x against 2.35x, and `bq-expand-gm-mulback` at 2.52x against 2.35x --- and **over Run 23's own 24 shapes every one of the eight reads Run 23's figure to the digit**, so what moved is the median's population and not what either arm allocates. The `alloc` column is a statistic of a strategy AND a shape set, as [its own bullet](#results) says, and this is what that costs a run that adds two shapes: pin the shape set before comparing a level across runs, exactly as the ceiling above wants pinning. The class blocks read the tiers unbroken in all nine, `bq-expand` running 1.08x on `runs` to 4.91x on `reshape1` where that class's own `m` shows through, and `list` 19.27x to 32.29x. **The cross-half agreement is a two-compiler figure this run and reads as one**: **1118 of the 1300** main-set cells that allocate in earnest agree to 1e-4, where Run 23's one-compiler pair agreed on 1245 of 1272 and Run 22's two-compiler pair on 1123 of its own roster's, and the worst disagreement is **1.08e-02 on `lenet-slice-c6-k5/mut-flat-gm`**. Allocation is deterministic per call, so what the 182 cells apart are is one compiler allocating differently within a tier, which is exactly what Run 19 separated from a tier moving and what no level moving here confirms.

Restated as the predicates the next run checks, and carrying no reading of its own: the figures each was last measured at are in the `Readings:` paragraphs above, so an entry here changes when a claim is re-aimed and not when a run moves a margin. **All of them are `-fspec-constr` claims, the regime they are read in** --- the shipped file does not set the flag, measured irrelevant to the shipped family --- so they are the set that decides, and a run at -O1 would test Run 7's instead, the two differing in more than their numbers. **They are read in the caller's allocation regime now**, every figure here being taken at the `-A32m` Run 16 promoted to the basis and every horde-ad test and benchmark bakes since 2026-08-21; the gap Runs 14, 15 and 16 priced against a prevailing `-A1G` is closed, and no claim below needs qualifying by it. **And all of them are read against a measured drift band rather than a layout span**, which is what the last three runs bought. A roster *order* change alone moved arms 0.966 to 1.142 between Run 9 and Run 10, and that is what a margin used to have to clear; with the layout pinned, a repetition moves an arm by at most 3.3% on Run 11's reading and 2.1% on Run 23's, most of them by under a point, so a margin above a few percent is now evidence of a strategy. **Run 13 is the first pair here to hold every tracked loop at one offset in both halves**, which is what lets its arm-by-arm comparison be read as the package costing nothing rather than as two terms cancelling. A claim resting on an arm whose own loop the shim skipped --- `list`'s, which is library code --- is still decidable nowhere until that loop is read. **And the pinning claim is measured only in its weak form**: adding `mut-flat-gm-nosum` left every tracked loop at the same address, but a `Force` arm reuses a rostered function and emits no code for emission order to move. The strong form wants an arm that emits its own, and until one is added the claim covers additions that cost nothing to place.

**The list DID need reading against a moved roster this run, and nothing in it changed.** Four arms went to `Only` and one landed, so five of claim 1's neighbours in the table are not the ones Run 23 read, but claim 1's own four links all name arms that are still timed and none of them moved. **What the roster raises is the question Run 22 raised**, smaller by five: fourteen arms read below `mut-odo-vecdims` where nineteen did, and the shipped library route is still among them. That is left to the next run rather than re-aimed here, and it is [under the recommended tasks](../README.md#recommended-tasks-after-run-24).

1. `mut-odo-vecdims` < `mut-flat-gm` < `bq-mut-runs-gm-mulback` < each of `bq-scan-rem-gm-mulback` and `bq-odo-gm-mulback`, the whole ordering read on unconditional arms --- **the ladder the `needs` column draws**, each link pricing one thing the implementation is allowed to ask for. **The foot rung retired 2026-08-29**, on a decision rather than on a reading: it registered the two arms needing nothing at all as a tie, so that either was what would ship if the mutating `Vector` method were refused upstream, and it had read as a tie on every run that carried it. Both arms stay rostered and stay in the rung above, `--pair bq-scan-rem-gm-mulback bq-odo-gm-mulback` recovers the reading whenever the upstream answer wants it, and its last is Run 21's, above. The middle link is the one the README has seen a layout term move --- 0.9708 at 15 of 24 on Run 10's unaligned half against 0.9293 at 22 on its aligned one --- and on a placed layout it has now read the aligned figure five runs running. The ordering has survived nine runs, two changes of basis, two repetitions and three compilers.
2. **Retired 2026-08-28** with the parking of `offtab`, the arm its surviving link turned on --- the other, `bq-scan-rem-gm-mulback`, is timed still. What it asked, since the settlement of 2026-08-24 re-aimed it, was where the arms needing something other than the fix sit --- `offtab` behind `bq-scan-rem-gm-mulback`, a mutable `Int` scratch priced against needing nothing --- and its last reading is Run 20's, above. **Its second link, `bq-expand` behind `mut-odo-vecdims`, had gone already, 2026-08-26** on the reading above, its condition having been spent since 2026-08-24 --- what it priced was the branch's own code against its replacement, and the replacement is now the branch's own code. It was the widest ordering the manifest carried, and `--pair` recovers it, both arms staying rostered and timed.
3, 4, 5. **Retired at Run 19's write-up**, on a last reading in which all three held on both compilers, and for the reasons in the settlement paragraph at the foot of this section. Their numbers are left standing here rather than reused: a verdict recorded against *claim 4* in an earlier run's file still means what it said. What they were, in a clause each, so that nothing is recoverable only from a manifest diff --- claim 3, that a mul-back output pays on the `bq-expand` build; claim 4, that the scan build ties its own build control while beating `bq-expand`, a tie Run 17 promoted to an ordering and three runs then read as one; claim 5, that `bq-expand` beats `bq-gen`, whose refutation of the generate-per-element build stands on Runs 7 and 8. **What none of the three could still foreclose is the point**: every one asks where `bq-expand` sits among arms nothing ships, on a branch whose fix is the `mut-odo-vecdims` family. The arms all stay rostered and timed, so any of these orderings is one `--pair` call away.
6. **Retired 2026-08-28** with the parking of `gen-quotrem`, the arm its only link turned on. What it asked: `gen-quotrem` ties `list`, the first attempt's arithmetic ceasing to be dearer than the list's allocation once the flag takes its own allocation to 1.00x against the list's 23.5x --- the mixed picture this suite exists to have refuted, arriving by a route nobody proposed. Its last reading is Run 20's, above; the `cm-gather` < `list` half was untimed throughout and stands as Run 8's. What goes with it is the standing advice to check `list` as an anchor before blaming a strategy, which is now nobody's claim and is why the machine check reads `list` net per shape every run.
7. Allocation, median multiples of the result **over a pinned shape set**: the mutable fills 1.00x, the scan family 1.33x, `bq-odo-gm-mulback` 1.51x, `offtab-scan-rem` 2.00x, `bq-expand` 2.35x, `list` 23.5x, every one of them read over the 24 main-set shapes Runs 15 to 23 shared --- re-listed 2026-08-28, three of the arms that carried these levels having gone with the parking and every level having kept one. Every level has reproduced over that shape set since Run 15, which is what makes this the claim to check first when anything else moves. **The pinning is the predicate and not a caveat on it, which Run 24 is the run that had to say**: its published column reads 1.58x and 2.40x for `bq-odo-gm-mulback` and `bq-expand` over its own 26 shapes, and 1.51x and 2.35x over the 24 --- so a level compared across two shape sets moves for a reason that is neither a code change nor a slot, and only a level that moves ON ONE POPULATION is a code change. **Read the levels and the cells as two questions**, which Run 19 is the run that separated: its levels all returned while the cross-half cell agreement fell to 1016 of 1080, where the 9.14 pair had 1072 --- so a compiler can reallocate within a tier without moving any tier, and only the cell count sees it.
8. **Retired 2026-08-29**, on a decision and one day after its last re-aiming. What it asked: that every pure arm in the fast tier run its output through the single in-order `vGenerate` over an `m`-length table, so a `bq-*` arm falling behind loses on its table build and not on its output. Its last reading is Run 21's, which found it true and its subject smaller again --- nine arms at or below `mut-odo-vecdims` and not one of them a `bq-*`, so the structure it described governed a tier starting a third of the way down. What retires it is that subject: the pure tier is no longer what ships, and a claim quantified over it was being re-aimed and re-read every run to say so. It was also the one claim with no named invocation, read off the table by eye throughout, so nothing mechanical goes with it.
9. **Retired at Run 19's write-up with 3, 4 and 5**, and for a reason of its own worth keeping: its per-shape half was answered rather than abandoned. `bq-expand-b`'s two best cells were `stretch-inner1` and `stretch-wide-2xM` in every run from Run 8 to Run 16 --- the rank-2 views with one huge outer dimension where seeding from `enumFromStepN` replaces the whole `concatMap` build --- until **Run 17 read `stretch-inner1` and `stretch-square-1341` instead**, which registered the follow-up. Runs 18 and 19 both read the original pair back, on four compilers between them, so the excursion was one run's and the mechanism is cleared of picking the wrong shapes. The geomeans were never the stable part, and the series is why: across Runs 8 to 13 `bq-expand-b` / `bq-expand` read 0.996, 0.9678, 0.9943, 0.9819, 0.9923 and 0.9909, its sign test crossing into significance only on the last of them, while `bq-expand-zf` / `bq-expand` went 3.6% behind, then level at 1.0028, then 1.0325, 1.0197, 1.0256 and 1.0265. Both series were closed at Run 13 and not extended per run, and a closed series in a live manifest is maintenance without a question --- which, with the follow-up spent, is the whole case for retiring it.

**What the parking of 2026-08-28 did to this set**, recorded in prose because a live item carries a predicate and no reading, and because naming a parked arm inside one is now a `--lint` failure. Claims 2 and 6 retired with `offtab` and `gen-quotrem`, the arms their surviving links turned on. Claim 7 lost three of the arms that carried its levels --- `gen-quotrem` at 1.00x, `bq-mut` at 1.33x and `offtab` at 2.00x, every figure of theirs ending at Run 20 --- but no level with them: `offtab-scan-rem` carries the 2.00x tier, the mutable fills the 1.00x and the scan family the 1.33x, so the list is the same six levels it was. Claim 8 was re-aimed off `bq-expand-zf` and `bq-gen`, its span running from the leading tier to `offtab-scan-rem` instead; the readings above are the last that name the two. Nothing was retired on a reading here, the parking being a decision about what is worth a bench, and the two claims that went had no link left that a run could measure.

**Two homes, and which carries what.** Each live claim has a prose paragraph here and a numbered predicate at the foot, and they divide: the PROSE carries this run's figures and what moved, the ITEM carries the predicate the next run checks and no reading at all. A RETIRED claim keeps its numbered item, which says in a clause what it was, and gets no prose paragraph --- Run 20 wrote two and they restated their own items clause for clause, because stripping the figures had removed the only thing that distinguished them. Each ordering is one line of `--claims`, whose manifest now carries the registered expectation --- the direction of the geomean, a tie by sign test, or claim 9's two best shapes --- and prints HELD or BROKE beside the paired geomean, interval and sign test. `--claims --in-place` then installs that arithmetic as each claim's `Readings:` paragraph above, so a run no longer transcribes it at all; what stays the reading's is whether a HELD margin moved and whether a movement clears the floor, and a BROKE is what obliges the paragraph above its reading to be rewritten rather than requoted. **A claim with no named invocation is a gap in this list, not a claim to be checked by hand**: where a session has to invent the computation it will invent a wrong one, which is how claim 7 came to be read off the raw fitted bytes, explained by a mechanism the previous pair refutes, and then "corrected" onto a rounded print. It has `--compare --alloc` now, and no live claim is without one since claim 8 retired. **The general form, and it is a standing instruction rather than an observation: if a write-up hand-rolls a script to answer something the reader should answer, that is a defect report against the reader** --- fix it there, before the sentence it was written for, or the next run invents its own wrong version. **Two riders, both bought on Run 19.** A new MODE joins the guards its siblings already have, and is checked against them rather than written beside them: `--counts` shipped able to be given without the `--compare` it reads, silently printing the default table and exiting 0 --- the unread-flag family exactly, added next to four sibling readings of `--compare` that were every one of them already guarded, and joining none. **And an instrument may be BACKED OUT, which is not a failure of the write-up but a result of it.** Measure what it flags before shipping it: the obvious mechanical repair for stale paragraphs was built and returned 100 for the four that mattered, so it went, and the refutation with its numbers is under the tasks heading --- worth more than the mode, since it stops the next session building the same thing. A report that never empties is one nobody reads, which this file already knows about hints.

**And for each stride class, the same three properties, now carrying Run 24's verdicts** over nine classes, the details beside each class's table:

1. **`mut-odo-vecdims`'s `worst` stays under 1.** Held in every one of the ten populations, on both halves, in every regime, roster and layout the README has run --- so it was never slower than the `list` it replaced, on any shape of any class the library can produce. This is the property the classes exist to test, no geomean can state it, and a break would be the one result here to bear on `Data/Array/Internal.hs` directly. Read for `mut-odo-vecdims` since 2026-08-22: **on Run 24 its worst is 0.125 on the main set and 0.105 in a class (`reshape1`), both read on the basis half, with the HEAD half at 0.124 and 0.108** --- so the property holds for the arm decided, on both compilers, and neither end is within a tenth of 1: the main-set end is a factor of 8.0 inside it and the class end 9.5. Both halves are quoted because one is not enough: Run 18's entry here read a floor-level figure from whichever half happened to be lower, which is the defect this phrasing exists to prevent. **Two different things break it, and only one of them is a baseline control.** `gen-unsafe` carries a `worst` above 1 in seven of the ten populations on the basis --- `bcast` at 0.991 and `runs` at 0.921 are the two it does not --- and it, its twins and the `list` twins that cross 1 are the baseline's own controls, which is why they are not read as the property failing. What IS a fill the library would ship is the other break, below. **The library-shaped arms break it on `runs` alone and all at `runs-2`**, the same six of eleven as Run 23 and on both halves: `libunord-stage1` at **1.337**, `liblist-stage1` 1.326, `lib-stage2-concat` 1.319, `lib-stage1` --- the shipped route --- at **1.314**, `libunord-stage2` 1.126 and `liblist-stage2` 1.123 on the basis, and 1.331, 1.308, 1.297, 1.303, 1.106 and 1.109 on HEAD. So on 900000 runs of two elements SIX of the eleven library-shaped arms are slower than the `list` baseline they replace --- every route that takes a slice per run at that length --- while `lib-stage2`, its short and lean variants, the composite and the dispatch built on it fill every run whatever its length and are the five that are not. **The property is stated of `mut-odo-vecdims` and holds of it; it does NOT hold of what the library actually calls.** `lib-stage1` is the shipped route and is among the six, at 1.314 and 1.303 --- so a reader taking property 1 as clearance for the code that ships is reading it wider than it is stated, and the class that catches the difference is `runs`.

2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest, `bq-expand` behind it. **The first clause breaks outright in all nine CLASS populations --- the main set is the tenth and is counted separately throughout this section --- where Run 23 broke it outright in seven and read the other two led by a `mut-odo-vecdims` sibling, which it counted as the family's and not as a break.** No class is led by a sibling this run; every one is led by an arm of the library's own stage-two family or by the unordered entry point, and the nine divide three ways. **Three are degenerate**: `libunord-stage2` leads `rev`, `revsome` and `reshape1` at 0.001, 0.000 and 0.000 of `mut-odo-vecdims`, its one-block test firing on every view of those classes and collapsing them to a single slice, so it prices dispatch and not filling. **Four are the new composite and the lean fill**: `lib-stage2-short-lean` leads `bcast`, `slice` and `window` by 39.79%, 28.42% and 63.79% against those populations' floors of 5.43%, 2.76% and 6.94%, and `lib-stage2-lean` leads `bcastmid` by 47.28% against 2.80%. **Two are the shipped route and the re-cut dispatch**: `lib-stage1` leads `scaled` by 9.07% against 2.09%, and `lib-stage2-disp` leads `runs` by 22.87% against 3.07%. So where a run ago the classes were led by candidates and siblings, they are now led by arms the library either ships or is one decision from shipping. The third clause reads the last candidate `bq-expand` behind `mut-odo-vecdims` and holds in all nine on both halves.

3. **The allocation tiers survive, and every level is Run 15's through Run 23's once the shape set is pinned**: the mutable fills at the result vector, `bq-expand` between 1.08x and 4.91x it, `list` an order of magnitude above. On the main set eight rows read above Run 23's at three distinct values, 1.58x, 2.40x and 2.52x against 1.51x, 2.35x and 2.35x, and over Run 23's own 24 shapes every one of them reads Run 23's figure exactly --- the median's population moved, not the allocation. Where a level moves it is the class's own `m` showing through, exactly as this property warned --- `bq-expand` at 1.08x on `runs` (`m` of 2 to 65536) and 4.91x on `reshape1` (`m = l`) --- with the ordering of tiers unbroken in all nine and `list` running 19.27x to 32.29x across them, on both halves and to the digit. The two `libunord` arms sit below the result vector at 0.00x on the MAIN SET, and in the classes they mostly do not: on five --- `bcast`, `bcastmid`, `slice`, `window` and `scaled` --- both read about 2.00x; on three, `libunord-stage1` reads about 2.00x while `libunord-stage2` stays under the vector, 0.01x on `rev` and 0.00x on `revsome` and `reshape1`; and on `runs` they read 1.19x and 1.14x. So the one-block test's 0.00x tier is the main set's alone, `libunord-stage1` never reaching it in any class, and a class reading of that tier is a different quantity. On a pair whose two halves are two compilers' code this is the property that says the difference is not a change of what gets allocated: every tier is identical on both halves, and the 182 main-set cells of 1300 that disagree past 1e-4 are one compiler allocating differently INSIDE a tier, which is the distinction Run 19 is the run that separated.

**SETTLED 2026-08-24 and APPLIED 2026-08-25, at Run 19's write-up rather than at the settlement**, so that the retiring orderings got one last cross-compiler reading and the retirement is recorded with it --- which is how Run 17 retired claim 4's tie, in prose at its write-up with the manifest taking it the same day. **They got it**: all thirteen held on both of Run 19's halves, and the eight that remain hold on both too, so each of the four retires on a reading rather than on a decision. `CLAIMS` in `read-run.py` carried claims 1, 2 and 6 alone after that settlement, and **claim 1 alone since 2026-08-28**, `offtab` and `gen-quotrem` having been parked. The test applied: an ordering stays only if it forecloses something anyone would propose again *and* can still break. What fails both is a figure, and figures live in the tables above. **Claims 3, 5 and 9 retire outright.** Claim 3 sets one output form against another on a build nothing ships, where every leading pure arm is a `-gm-mulback` already; claim 5's `bq-expand` / `bq-gen` says of itself that the refutation stands on Runs 7 and 8, and claim 6 keeps that family guarded through `gen-quotrem`; claim 9's two series are closed at Run 13 by this section's own words, and a closed series in a live manifest is maintenance without a question. **Claim 4 retires with them, its tie moving into claim 1** --- and what goes with it is the one place the manifest reads a *builder* apart from its output, which `--pair` recovers whenever it is wanted, both arms staying rostered. **Claim 1 becomes the ladder the `needs` column already draws**, gaining `bq-scan-rem-gm-mulback`, the best arm needing nothing at all, between `bq-mut-runs-gm-mulback` and `bq-odo-gm-mulback`: the first ahead of it at **0.9060** and **0.9171** on Run 18's two halves, 19 and 17 of 24, which is what a mutable `Int` scratch buys; and the second **tied** with it at **0.9902** and **0.9936**, 13 and 12 of 24 at p 0.84 and 1, so the two fastest pure arms were indistinguishable and either was what would ship if the mutating method were refused --- the rung this installed, and retired again on 2026-08-29. Its three existing links stay, the middle one redundant with the two new ones and carrying seven runs of history they do not. **Claim 2 keeps its number and changes its question** to where the arms needing something other than the fix sit: `offtab`, which needs only that `Int` scratch, behind `bq-scan-rem-gm-mulback` at **1.36** and **1.44**; and `bq-expand` behind `mut-odo-vecdims` at **2.09** and **2.13**, kept only while `Data/Array/Internal.hs` carried `bq-expand`, and to retire with the three `TODO: retarget` markers, which were one decision with it. **That condition was spent the same day and the link outlived it by two runs**: the file went to `vFillStrided` on 2026-08-24 and the markers went with the prose they marked, but nothing read the condition back, so Run 20 registered and read the link like any other and it retired only on 2026-08-26. Thirteen registered orderings become eight here, and seven when that second link finally goes; claims 7 and 8 stayed unmanifested prose. **The rewriting the ask paired with this was already done**: the eight *What the class says* paragraphs were written to the re-aimed properties at Run 18's write-up, and only the sentence asking for it survived.

`--pair` works within a class JSON exactly as within the main one, and is still the way to compare two arms; its bootstrap interval, over three shapes, is worth less there than its win count.

Two notes on the columns. The `needs` column splits the class-method tier in two. A **new pure `Vector` method** delegates to a pure function the vector package already ships for every carrier --- `unfoldrExactN`, `backpermute`, the `concatMap`/`enumFromStepN` pipeline --- so it fights only *minimal* in orthotope's pure-and-minimal API rule; the **new mutating `Vector` method** the direct fills need is the [mutable ceiling](../README.md#the-mutable-ceiling-taken)'s ask, which *pure* barred outright until the amendment there turned the bar into a weight, and which the decision of 2026-08-22 takes. `offtab` is the `Vector`-class-expressible shape of these gathers --- output by plain `vGenerate` over a concrete offset table --- so its own cell names only its mutable `Int` scratch. And the geomean weights every benchmarked shape **equally**, so a figure here is a ranking statistic, not a claim about total work saved: the small shapes count as much as the largest.


## The stride classes, run by run

**Run 24 (SpecConstr, dead-spot +lookrts, -A32m, 9.12.4) records every class on BOTH halves**, one process each, in [the sequence](../README.md#making-a-major-benchmark-run), all twenty processes in one window. Every table below is the **basis half**'s, the 9.12 one, the half that keeps the lineage; what the second half buys is that the pair's variable --- the compiler --- can be read on a class, which no compiler pair before this one could do with the counted work beside it on every population. **Read across the halves and the two compilers are close and split.** Of the 414 arm-comparisons the nine classes carry, nine (on `reshape1`, the six `lib-stage2*` arms, both `canon-*` arms and `libunord-stage2`, a cell of each not left positive by the correction) sit out the vote and the geomeans as degenerate; **206 put the basis half faster and 199 the HEAD half**, and the nine geomeans run **0.9855 on `scaled` to 1.0006 on `slice`**, eight of them below 1. **The high extreme is a `gen-unsafe` A/A control in seven of the nine**, between 1.0568 on `runs` and 1.1353 on `reshape1` --- the placement-exposed arm, at count ratios of 1.0000 --- and the two exceptions are `rev`, whose high extreme is `libunord-stage2` at 1.1967, and `scaled`, whose is `gen-unsafe` itself at 1.0561, the timed arm rather than one of its twins. **The low extreme is `bq-odo-gm-mulback-aa-distant` in three of the nine**, 0.8963 to 0.9135, and some arm of that family holds it in five, `bcastmid`'s 0.9200 and `scaled`'s 0.9065 with them --- which is 9.12's codegen win on the pure family showing through class by class. **Five classes disqualify their own cross-half line**, where Run 23 had three: `rev` at 1.0078, `revsome` 1.0149, `bcast` 1.0124, `reshape1` 1.0327 and `runs` 1.0104 move `list` past the 0.7% bar, so their lines say so and are not read for the compiler --- and `bcastmid`, `slice`, `window` and `scaled` are inside it, as is the main set at 1.0025.

First, one table over all of them, so that an inversion is visible without reading every class's table. Every figure in it is transcribed from a class's own table below --- none is computed here, and none is an average across classes, there being no such population to average over. Its header, fixed here so a run fills rows and never reshapes columns:

    | class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |

That header line is written out twice in this file, once here as the spec and once as the table's own, and the two are the same text --- so a session pasting a run's rows must anchor at the line start and check that it landed on the unindented one. Getting that wrong put Run 8's rows under this paragraph and left Run 7's standing in the table, both checks passing, because the check looked the table up the same wrong way the paste did.

`mut-odo-vecdims` and `worst` are that arm's two columns in that class's table; *best outside family* is the leading arm outside the vecdims family, what the dropped stride-conditioned redirect would have taken, and *ceiling* the leading arm OF the family, each with its name, since which arm leads is half of what the column says --- so where property 2 breaks the two name different arms and the gap between them is what the break is worth, and Run 21's table, which repeated one arm in both columns on `bcastmid` and `reshape1`, was wrong to; *floor* is the largest deviation from 1 among that process's sixteen A/A controls. A cell that breaks one of [the three properties](#the-claims-the-next-run-should-test) is bolded, and the class's own paragraph says what broke.

**And the aggregate figures in the paragraph above the blocks are the reader's, emitted rather than assembled.** `./read-run.py --cross-classes --classes BASIS... --others CONTROL...` prints every one of them --- the comparison count, the faster/slower split, the range of the nine geomeans with the class at each end, the arm holding each extreme and how many populations share it, the degenerate arms it kept out, and the classes whose `list` is past the 0.7% bar --- from the same per-class rows the nine cross-half lines below print, so the intro and the blocks cannot part. The comparison count, the faster/slower split, the range of the nine geomeans and the extreme arms are each an aggregate over the nine `--block --compare` lines below, so they are read off those lines and never off a population assembled for the purpose: Run 20 assembled its own twice and was wrong both times --- once on the split, once on a low end that excluded a class the sentence said it covered. Where a figure genuinely cannot come off those lines, because a class's own maximum is a degenerate cell, the paragraph says so rather than quoting it as though it could.

Then one block per class, in `classViews`' order --- `rev`, `revsome`, `bcast`, `bcastmid`, `reshape1`, `slice`, `window`, `scaled`, `runs` --- each carrying the same six things and nothing else:

1. a bolded lead naming the class, the mechanism it models in a clause, and its shapes with their `l` and `sInner`, which is what makes the table under it readable without `Main.hs` open;
2. the table `--block --in-place` installs from `$R-<basis>-$c.json`, whole and never edited --- six columns, with the emphasis carried over from the main table so the `mut-odo-vecdims` row is found at a glance, and `needs` left to that table as a property of a strategy rather than of a population;
3. its own controls, off `--aa`: the A/A deviations with their spans, the two `sum-only` halves, and the in-situ term from the `-nosum` arms --- this process's own floor and its own three gates, neither inherited nor lent --- and where the paragraph quotes the OTHER half's figure, it says so in the form `the other half's own sixteen pairs span N%` and never with the word *floor* beside the number, which `--check-doc` holds to this table's column (Run 23 was refused four times before it learned the shape);
4. its provenance and its anchor: elapsed time and the two heap peaks from that process's stderr line, its population's size from the reader's first line ([why not both from one place](../README.md#making-a-major-benchmark-run)), and `list`'s absolute per-call time on one of its shapes, raw and net. The main set's three anchors guard a baseline that moves for every population at once; this one guards a baseline that could move for this mechanism alone, which is the case a table of ratios hides completely. A three-shape class adds one line here --- the bolded rows' per-shape net ratios, in the lead's shape order --- because its table under-determines its cells, where a two-shape table carried them already, `time` and `worst` jointly fixing both; every class is three shapes or more now --- six at three, `bcastmid` and `reshape1` at four and `runs` at eleven --- so the line always prints;
5. the cross-half reading, one line, which `--block --compare` against the other half's JSON now emits and `install-tables.sh` writes in with the other three --- how many of the population's arms move, which way, and the spread; a margin on this line is judged against the WIDER of the two halves' floors ([README, the floor section][floor]). Both halves have run every class since 2026-08-14 and this is where that is read: a pair's variable can act on a class and not on the main set, which is how Run 14 answered its `scaled` question. A run whose halves differ in nothing a class can see says so in a clause;
6. one paragraph of what the class says, and none where it says nothing: an ordering that inverted, a `worst` above 1, an allocation tier that moved, a mechanism showing through a single cell. A class that reproduces the main ordering gets one sentence saying so, that being a result and reading as one.

`./read-run.py RUN.json --block --compare OTHER.json` assembles items 2 through 5's mechanical parts, and `install-tables.sh` writes them in in one call --- table, controls, the provenance and anchor skeleton, a three-shape population's per-shape line, and the cross-half line; the lead and the paragraph stay the author's, a skeleton writing no findings. **The cross-half line carries its own disqualification**: where `list` moves more than 0.7% between the halves the line says so and says it is not read for the pair's variable --- a reading Run 18 needed, and which no other output showed.

The blocks carry no headings of their own. One per class would crowd the contents and the replace list alike, where a bolded lead reads the same and lets one link cover the section --- which is what `--check-doc`'s coverage check counts.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.047 | 0.068 | **`libunord-stage2`** 0.001 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 5.07% |
| `revsome` | 3 | 0.047 | 0.057 | **`libunord-stage2`** 0.000 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 | 3.28% |
| `bcast` | 3 | 0.035 | 0.063 | **`lib-stage2-short-lean`** 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 5.43% |
| `bcastmid` | 4 | 0.032 | 0.059 | **`lib-stage2-lean`** 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 2.80% |
| `reshape1` | 4 | 0.091 | 0.105 | **`libunord-stage2`** 0.000 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.023 | 2.17% |
| `slice` | 3 | 0.040 | 0.058 | **`lib-stage2-short-lean`** 0.029 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 | 2.76% |
| `window` | 4 | 0.054 | 0.094 | **`lib-stage2-short-lean`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.026 | 6.94% |
| `scaled` | 3 | 0.031 | 0.033 | **`lib-stage1`** 0.026 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.027 | 2.09% |
| `runs` | 14 | 0.032 | 0.063 | **`lib-stage2-disp`** 0.027 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.027 | 3.07% |

The floor-movement paragraph that stood here was cut on 2026-08-22, having read Run 16's column against Run 15's while Run 17 installed this one over it --- the defect `--check-doc` now holds every such movement to. What moves these floors is [an open question](../README.md#what-is-open) and not a sentence under a table.

The pure slot this table carried until 2026-08-22, and the paragraph that read it, retired with the pure/impure distinction when the decision shipped the mutable family's arm; the column now carries the best arm outside the family, which the table above gives per class and which is ahead of `mut-odo-vecdims` on `reshape1` alone.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.13* | *134* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.07* | *145* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.28* | *142* | *1.34x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *157* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *157* | *0.00x* |
| libunord-stage2 | 0.001 | 0.003 | 0.07 | 157 | 0.01x |
| lib-stage2-short-lean | 0.023 | 0.029 | 0.11 | 148 | 1.01x |
| lib-stage2-short | 0.024 | 0.029 | 0.15 | 148 | 1.01x |
| lib-stage1 | 0.026 | 0.047 | 0.09 | 146 | 1.01x |
| lib-stage2-lean | 0.026 | 0.034 | 0.10 | 146 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.045 | 0.11 | 146 | 1.00x |
| lib-stage2 | 0.027 | 0.035 | 0.09 | 146 | 1.01x |
| lib-stage2-concat | 0.027 | 0.035 | 0.10 | 146 | 1.01x |
| lib-stage2-disp | 0.027 | 0.035 | 0.10 | 146 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.027 | 0.046 | 0.13 | 146 | 1.00x |
| liblist-stage2 | 0.040 | 0.046 | 0.26 | 143 | 2.01x |
| liblist-stage1 | 0.043 | 0.058 | 0.24 | 142 | 2.01x |
| libunord-stage1 | 0.045 | 0.061 | 0.25 | 142 | 2.03x |
| **mut-odo-vecdims** | **0.047** | 0.068 | 0.10 | 137 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.047* | *0.067* | *0.10* | *137* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.047* | *0.067* | *0.11* | *137* | *1.00x* |
| mut-odo-vecdims-add-in | 0.047 | 0.068 | 0.07 | 137 | 1.00x |
| mid-copy | 0.047 | 0.070 | 0.12 | 137 | 1.00x |
| canon-vecdims | 0.048 | 0.056 | 0.12 | 137 | 1.01x |
| bcast-set | 0.050 | 0.073 | 0.44 | 136 | 1.00x |
| canon-full | 0.054 | 0.063 | 0.05 | 136 | 1.01x |
| *build-aa-distant* | *0.082* | *0.166* | *0.63* | *126* | *1.00x* |
| mut-flat-gm | 0.083 | 0.128 | 0.19 | 134 | 1.34x |
| *build-aa-adjacent* | *0.085* | *0.172* | *1.15* | *126* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.085* | *0.171* | *0.79* | *126* | *1.00x* |
| *mut-odo-aa-distant* | *0.085* | *0.173* | *0.51* | *126* | *1.00x* |
| mut-odo | 0.086 | 0.175 | 0.80 | 126 | 1.00x |
| bq-expand-gm-mulback | 0.089 | 0.167 | 0.17 | 130 | 2.52x |
| build | 0.091 | 0.167 | 1.09 | 125 | 1.00x |
| **bq-scan-rem-gm-mulback** | **0.095** | 0.097 | 0.09 | 129 | 1.34x |
| bq-mut-runs-gm-mulback | 0.095 | 0.135 | 0.13 | 132 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.095* | *0.098* | *0.12* | *128* | *1.34x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.095* | *0.097* | *0.13* | *129* | *1.34x* |
| *bq-odo-gm-mulback-aa-distant* | *0.096* | *0.116* | *0.10* | *131* | *1.41x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.096* | *0.116* | *0.13* | *131* | *1.41x* |
| bq-odo-gm-mulback | 0.096 | 0.116 | 0.15 | 131 | 1.41x |
| *bq-expand-aa-adjacent* | *0.101* | *0.175* | *0.13* | *129* | *2.52x* |
| *bq-expand-aa-distant* | *0.101* | *0.175* | *0.19* | *128* | *2.52x* |
| bq-expand | 0.102 | 0.175 | 0.12 | 129 | 2.52x |
| offtab-scan-rem | 0.127 | 0.131 | 0.07 | 124 | 2.00x |
| *list-aa-adjacent* | *0.998* | *1.001* | *0.37* | *87* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.20 | 87 | 23.43x |
| *list-aa-distant* | *1.001* | *1.007* | *0.35* | *87* | *23.43x* |
| *gen-unsafe-aa-distant* | *1.179* | *1.271* | *1.23* | *83* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *1.197* | *1.364* | *1.46* | *83* | *1.00x* |
| gen-unsafe | 1.203 | 1.352 | 0.74 | 83 | 1.00x |

**Controls:** The largest A/A pair is `build-aa-distant` at 0.9493, worst cell 13.51% on `rev-gather48-src-50`, and 10 of 16 intervals cover 1. The `sum-only` halves agree at 0.9990 on a worst cell of 0.31% on `rev-cnn-L1-24x24-c1`, its interval covering 1. The in-situ term reads 1.0030, 1.0070, 1.0110, 1.0143 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9600, which the correction amplifies by 1.44x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m31s, peak 96 MiB in use, 26 MiB max residency; the reader reads 52 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.14 ms per call raw, 3.99 ms net.

**Per shape, in the lead's order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.068/0.052/0.029 `bq-scan-rem-gm-mulback` 0.096/0.097/0.092

**Across the halves:** 21 of the 46 arms are faster on this half and 25 slower, at a geomean of 0.9975, from `bq-odo-gm-mulback-aa-distant` at 0.9135 to `libunord-stage2` at 1.1967, with `list` itself at 1.0078. **The baseline moved 0.78% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** properties 1 and 3 hold for `mut-odo-vecdims` --- `worst` 0.068 against a `list` it never loses to, and the tiers at 1.00x, 2.52x and 23.43x --- and property 2 breaks outright to `libunord-stage2` at 0.001, **0.0157 of `mut-odo-vecdims` on 3 of 3 shapes**, a 98.43% margin against a 5.07% floor: the unordered one-block test firing on every view of the class and collapsing it to a single `VS.slice`, so the break prices dispatch and not filling, as on Runs 22 and 23. What the class adds is across the halves, and it is the pure family at one end and the unordered arm at the other: the range runs from `bq-odo-gm-mulback-aa-distant` at 0.9135 to `libunord-stage2` at 1.1967, at a geomean of 0.9975 --- on a class whose `list` moved 0.78%, so the line is ordered and not subtracted.

**`revsome` --- a strict subset of axes reversed, so the signs are mixed.** Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89), `revsome-outer-g48` (`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l` 165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.19* | *90* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.06* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.23* | *94* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| libunord-stage2 | 0.000 | 0.001 | 0.02 | 116 | 0.00x |
| lib-stage2-short-lean | 0.023 | 0.028 | 0.17 | 103 | 1.00x |
| lib-stage2-short | 0.023 | 0.028 | 0.11 | 103 | 1.00x |
| lib-stage2-concat | 0.025 | 0.033 | 0.07 | 101 | 1.00x |
| lib-stage2 | 0.025 | 0.033 | 0.14 | 101 | 1.00x |
| lib-stage1 | 0.025 | 0.032 | 0.15 | 101 | 1.00x |
| lib-stage2-disp | 0.025 | 0.033 | 0.09 | 101 | 1.00x |
| lib-stage2-lean | 0.025 | 0.033 | 0.13 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.025 | 0.032 | 0.11 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.026 | 0.032 | 0.10 | 101 | 1.00x |
| liblist-stage1 | 0.040 | 0.045 | 0.56 | 97 | 2.00x |
| libunord-stage1 | 0.040 | 0.044 | 0.24 | 97 | 2.00x |
| liblist-stage2 | 0.040 | 0.045 | 0.19 | 97 | 2.00x |
| mid-copy | 0.047 | 0.057 | 0.07 | 96 | 1.00x |
| mut-odo-vecdims-add-in | 0.047 | 0.058 | 0.11 | 96 | 1.00x |
| **mut-odo-vecdims** | **0.047** | 0.057 | 0.13 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.048* | *0.057* | *0.09* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.048* | *0.057* | *0.10* | *96* | *1.00x* |
| canon-vecdims | 0.051 | 0.055 | 0.10 | 96 | 1.00x |
| bcast-set | 0.052 | 0.061 | 0.44 | 96 | 1.00x |
| canon-full | 0.056 | 0.063 | 0.12 | 96 | 1.00x |
| mut-flat-gm | 0.078 | 0.088 | 0.15 | 88 | 1.33x |
| bq-mut-runs-gm-mulback | 0.089 | 0.097 | 0.17 | 87 | 1.33x |
| *mut-odo-aa-adjacent* | *0.091* | *0.137* | *0.16* | *96* | *1.00x* |
| *build-aa-distant* | *0.091* | *0.137* | *0.33* | *96* | *1.00x* |
| *mut-odo-aa-distant* | *0.092* | *0.140* | *1.22* | *96* | *1.00x* |
| mut-odo | 0.092 | 0.139 | 0.89 | 96 | 1.00x |
| bq-expand-gm-mulback | 0.096 | 0.120 | 0.13 | 83 | 2.52x |
| *bq-expand-aa-adjacent* | *0.097* | *0.130* | *0.14* | *83* | *2.52x* |
| build | 0.098 | 0.134 | 0.83 | 96 | 1.00x |
| *bq-expand-aa-distant* | *0.098* | *0.128* | *0.15* | *83* | *2.52x* |
| *build-aa-adjacent* | *0.099* | *0.134* | *0.76* | *96* | *1.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.099* | *0.103* | *0.11* | *87* | *1.33x* |
| **bq-scan-rem-gm-mulback** | **0.099** | 0.103 | 0.09 | 87 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.103* | *0.10* | *86* | *1.33x* |
| bq-expand | 0.100 | 0.130 | 0.14 | 83 | 2.52x |
| *bq-odo-gm-mulback-aa-distant* | *0.102* | *0.121* | *0.13* | *83* | *1.41x* |
| bq-odo-gm-mulback | 0.102 | 0.122 | 0.11 | 83 | 1.41x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.102* | *0.122* | *0.11* | *83* | *1.41x* |
| offtab-scan-rem | 0.128 | 0.132 | 0.13 | 82 | 2.00x |
| *list-aa-distant* | *0.995* | *1.002* | *0.32* | *46* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.17 | 46 | 23.43x |
| *list-aa-adjacent* | *1.003* | *1.006* | *0.29* | *46* | *23.43x* |
| *gen-unsafe-aa-adjacent* | *1.148* | *1.375* | *2.08* | *44* | *1.00x* |
| gen-unsafe | 1.155 | 1.255 | 1.59 | 43 | 1.00x |
| *gen-unsafe-aa-distant* | *1.193* | *1.374* | *0.91* | *43* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0328, worst cell 9.46% on `revsome-mid-cnn-L2`, and 13 of 16 intervals cover 1. The `sum-only` halves agree at 0.9998 on a worst cell of 0.34% on `revsome-outer-g48`, its interval covering 1. The in-situ term reads 1.0187, 1.0120, 1.0127, 1.0357 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0320, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m31s, peak 121 MiB in use, 26 MiB max residency; the reader reads 52 benchmarks over 3 shapes of the revsome class. Anchor: `revsome-inner-primes`, `list` at 4.16 ms per call raw, 4.01 ms net.

**Per shape, in the lead's order (revsome-inner-primes, revsome-outer-g48, revsome-mid-cnn-L2):** `mut-odo-vecdims` 0.030/0.053/0.057 `bq-scan-rem-gm-mulback` 0.103/0.098/0.097

**Across the halves:** 22 of the 46 arms are faster on this half and 24 slower, at a geomean of 0.9956, from `bq-scan-rem-gm-mulback-aa-distant` at 0.9406 to `gen-unsafe-aa-distant` at 1.1120, with `list` itself at 1.0149. **The baseline moved 1.49% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** it reproduces `rev` in every respect --- properties 1 and 3 hold, `worst` 0.057, the tiers at 1.00x, 2.52x and 23.43x, and property 2 breaks to `libunord-stage2` at 0.000 on 3 of 3 shapes against a 3.28% floor --- which is what a class differing from `rev` only in that a subset of axes is reversed should do. Its `list` moved **1.49%**, the widest of the nine after `reshape1`, so its cross-half line is the least readable of the set and is ordered alone.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.62* | *52* | *1.38x* |
| *canon-full-nosum* | *--* | *--* | *0.63* | *83* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.90* | *58* | *1.13x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.48* | *82* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| lib-stage2-short-lean | 0.019 | 0.027 | 0.49 | 61 | 1.00x |
| lib-stage2-lean | 0.019 | 0.027 | 0.52 | 61 | 1.00x |
| lib-stage2-short | 0.019 | 0.027 | 0.48 | 61 | 1.00x |
| lib-stage2-disp | 0.019 | 0.027 | 0.48 | 61 | 1.00x |
| lib-stage2 | 0.020 | 0.027 | 0.47 | 61 | 1.00x |
| lib-stage2-concat | 0.020 | 0.027 | 0.48 | 61 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.023 | 0.54 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.021 | 0.023 | 0.53 | 60 | 1.00x |
| lib-stage1 | 0.021 | 0.023 | 0.52 | 60 | 1.00x |
| bcast-set | 0.032 | 0.058 | 0.53 | 61 | 1.00x |
| canon-full | 0.033 | 0.062 | 0.53 | 61 | 1.00x |
| mid-copy | 0.035 | 0.062 | 0.54 | 60 | 1.00x |
| **mut-odo-vecdims** | **0.035** | 0.063 | 0.43 | 60 | 1.00x |
| mut-odo-vecdims-add-in | 0.035 | 0.063 | 0.49 | 60 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.035* | *0.063* | *0.35* | *60* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.035* | *0.063* | *0.53* | *60* | *1.00x* |
| canon-vecdims | 0.035 | 0.063 | 0.58 | 60 | 1.00x |
| libunord-stage2 | 0.041 | 0.048 | 1.04 | 54 | 2.00x |
| liblist-stage2 | 0.041 | 0.048 | 0.90 | 54 | 2.00x |
| libunord-stage1 | 0.042 | 0.047 | 0.87 | 53 | 2.00x |
| liblist-stage1 | 0.044 | 0.045 | 0.81 | 54 | 2.00x |
| mut-odo | 0.055 | 0.149 | 1.07 | 60 | 1.00x |
| *mut-odo-aa-adjacent* | *0.056* | *0.148* | *0.54* | *60* | *1.00x* |
| *build-aa-adjacent* | *0.057* | *0.141* | *0.69* | *60* | *1.00x* |
| *build-aa-distant* | *0.057* | *0.153* | *3.03* | *60* | *1.00x* |
| *mut-odo-aa-distant* | *0.057* | *0.149* | *1.42* | *60* | *1.00x* |
| build | 0.057 | 0.147 | 0.54 | 60 | 1.00x |
| mut-flat-gm | 0.066 | 0.070 | 0.67 | 49 | 1.13x |
| bq-expand-gm-mulback | 0.078 | 0.080 | 0.67 | 48 | 1.38x |
| bq-mut-runs-gm-mulback | 0.079 | 0.087 | 0.62 | 47 | 1.13x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.082* | *0.086* | *0.73* | *47* | *1.14x* |
| bq-odo-gm-mulback | 0.082 | 0.086 | 0.81 | 47 | 1.14x |
| *bq-odo-gm-mulback-aa-distant* | *0.082* | *0.085* | *0.39* | *47* | *1.14x* |
| bq-expand | 0.090 | 0.094 | 0.69 | 46 | 1.38x |
| *bq-expand-aa-adjacent* | *0.090* | *0.094* | *0.68* | *46* | *1.38x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.091* | *0.099* | *0.80* | *47* | *1.13x* |
| **bq-scan-rem-gm-mulback** | **0.091** | 0.099 | 0.71 | 47 | 1.13x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.091* | *0.100* | *0.05* | *47* | *1.13x* |
| *bq-expand-aa-distant* | *0.092* | *0.095* | *0.37* | *46* | *1.38x* |
| offtab-scan-rem | 0.125 | 0.139 | 1.08 | 43 | 2.00x |
| *gen-unsafe-aa-distant* | *0.779* | *1.020* | *1.95* | *22* | *1.00x* |
| gen-unsafe | 0.896 | 0.991 | 2.02 | 22 | 1.00x |
| *gen-unsafe-aa-adjacent* | *0.983* | *0.991* | *1.77* | *21* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.16 | 17 | 20.62x |
| *list-aa-distant* | *1.001* | *1.010* | *1.22* | *17* | *20.62x* |
| *list-aa-adjacent* | *1.011* | *1.021* | *0.73* | *17* | *20.62x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 1.0543, worst cell 12.36% on `bcast-tall-Mx2`, and 9 of 16 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.04% on `bcast-tall-Mx2`, its interval covering 1. The in-situ term reads 1.0092, 1.0175, 1.0079, 1.0137 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0515, which the correction amplifies by 1.04x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m32s, peak 151 MiB in use, 45 MiB max residency; the reader reads 52 benchmarks over 3 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 28.9 ms per call raw, 27.8 ms net.

**Per shape, in the lead's order (bcast-inner8, bcast-inner900, bcast-tall-Mx2):** `mut-odo-vecdims` 0.032/0.021/0.063 `bq-scan-rem-gm-mulback` 0.089/0.086/0.099

**Across the halves:** 24 of the 46 arms are faster on this half and 22 slower, at a geomean of 0.9902, from `bq-odo-gm-mulback-aa-distant` at 0.8963 to `gen-unsafe-aa-adjacent` at 1.1053, with `list` itself at 1.0124. **The baseline moved 1.24% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** the composite arm that landed this run leads it. `lib-stage2-short-lean` reads 0.019 of the `list` baseline against `mut-odo-vecdims`'s 0.035, a **39.79%** margin on a 5.43% floor, and property 2 breaks to it rather than to `lib-stage2-u4`, which led this class a run ago by 40.1% and is parked. Properties 1 and 3 hold --- `worst` 0.063, and the tiers at 1.00x, 1.38x and 20.62x, `bq-expand`'s level being this class's own `m` of 8 and 900 showing through. Across the halves the range is carried by the pure family and the baseline, `bq-odo-gm-mulback-aa-distant` at 0.8963 against `gen-unsafe-aa-adjacent` at 1.1053, at a geomean of 0.9902 on a `list` that moved 1.24%, so the line is ordered and not subtracted.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.48* | *69* | *1.57x* |
| *canon-full-nosum* | *--* | *--* | *0.53* | *104* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.74* | *75* | *1.17x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.27* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *88* | *0.00x* |
| lib-stage2-lean | 0.017 | 0.033 | 0.37 | 80 | 1.00x |
| lib-stage2-concat | 0.017 | 0.033 | 0.33 | 80 | 1.00x |
| lib-stage2 | 0.017 | 0.033 | 0.33 | 80 | 1.00x |
| lib-stage2-disp | 0.017 | 0.033 | 0.34 | 80 | 1.00x |
| lib-stage2-short-lean | 0.017 | 0.035 | 0.33 | 80 | 1.00x |
| lib-stage2-short | 0.017 | 0.035 | 0.36 | 80 | 1.00x |
| mid-copy | 0.017 | 0.033 | 0.34 | 80 | 1.00x |
| canon-full | 0.018 | 0.033 | 0.41 | 80 | 1.00x |
| lib-stage1 | 0.021 | 0.033 | 0.33 | 79 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.033 | 0.36 | 79 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.022 | 0.033 | 0.36 | 79 | 1.00x |
| mut-odo-vecdims-add-in | 0.032 | 0.059 | 0.34 | 75 | 1.00x |
| *mut-odo-vecdims-aa* | *0.032* | *0.059* | *0.33* | *75* | *1.00x* |
| **mut-odo-vecdims** | **0.032** | 0.059 | 0.31 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.059* | *0.22* | *76* | *1.00x* |
| canon-vecdims | 0.032 | 0.059 | 0.36 | 75 | 1.00x |
| liblist-stage2 | 0.032 | 0.047 | 0.59 | 74 | 2.00x |
| libunord-stage2 | 0.033 | 0.048 | 0.59 | 74 | 2.00x |
| bcast-set | 0.034 | 0.062 | 0.35 | 75 | 1.00x |
| libunord-stage1 | 0.037 | 0.045 | 0.54 | 74 | 2.00x |
| liblist-stage1 | 0.038 | 0.044 | 0.62 | 74 | 2.00x |
| *build-aa-adjacent* | *0.050* | *0.140* | *0.73* | *68* | *1.00x* |
| build | 0.050 | 0.142 | 1.08 | 68 | 1.00x |
| *mut-odo-aa-distant* | *0.050* | *0.143* | *0.28* | *68* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.050* | *0.143* | *0.36* | *68* | *1.00x* |
| mut-odo | 0.050 | 0.142 | 0.29 | 68 | 1.00x |
| *build-aa-distant* | *0.051* | *0.139* | *0.59* | *68* | *1.00x* |
| mut-flat-gm | 0.063 | 0.094 | 0.70 | 68 | 1.17x |
| bq-mut-runs-gm-mulback | 0.074 | 0.102 | 0.42 | 65 | 1.17x |
| bq-expand-gm-mulback | 0.078 | 0.122 | 0.43 | 64 | 1.57x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.080* | *0.099* | *0.41* | *64* | *1.17x* |
| **bq-scan-rem-gm-mulback** | **0.080** | 0.099 | 0.44 | 64 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.080* | *0.099* | *0.27* | *64* | *1.17x* |
| bq-odo-gm-mulback | 0.080 | 0.125 | 0.41 | 64 | 1.17x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.080* | *0.125* | *0.43* | *64* | *1.17x* |
| *bq-odo-gm-mulback-aa-distant* | *0.080* | *0.124* | *0.34* | *64* | *1.17x* |
| *bq-expand-aa-distant* | *0.086* | *0.132* | *0.24* | *64* | *1.57x* |
| bq-expand | 0.086 | 0.132 | 0.49 | 64 | 1.57x |
| *bq-expand-aa-adjacent* | *0.086* | *0.132* | *0.45* | *64* | *1.57x* |
| offtab-scan-rem | 0.108 | 0.128 | 0.66 | 60 | 2.00x |
| *gen-unsafe-aa-distant* | *0.920* | *1.414* | *2.56* | *30* | *1.00x* |
| gen-unsafe | 0.922 | 1.399 | 2.13 | 30 | 1.00x |
| *gen-unsafe-aa-adjacent* | *0.929* | *1.390* | *2.26* | *30* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.11 | 29 | 21.22x |
| *list-aa-distant* | *1.000* | *1.002* | *1.01* | *29* | *21.22x* |
| *list-aa-adjacent* | *1.003* | *1.016* | *1.02* | *29* | *21.22x* |

**Controls:** The largest A/A pair is `build-aa-distant` at 1.0280, worst cell 13.59% on `bcastmid-b200k`, and 15 of 16 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.03% on `bcastmid-block150k`, its interval missing 1. The in-situ term reads 1.0201, 1.0362, 1.0176, 1.0483 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0218, which the correction amplifies by 1.63x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h18m0s, peak 149 MiB in use, 38 MiB max residency; the reader reads 52 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 47.9 ms per call raw, 46.8 ms net.

**Per shape, in the lead's order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.059/0.022/0.036/0.023 `bq-scan-rem-gm-mulback` 0.099/0.087/0.069/0.067

**Across the halves:** 20 of the 46 arms are faster on this half and 26 slower, at a geomean of 0.9925, from `bq-odo-gm-mulback` at 0.9200 to `gen-unsafe-aa-adjacent` at 1.1081, with `list` itself at 1.0041.

**What the class says:** the lean dispatch leads it, which is registration 2's prediction met on a whole population. `lib-stage2-lean` reads 0.017 against `mut-odo-vecdims`'s 0.032, a **47.28%** margin on a 2.80% floor, and against `lib-stage2` it reads 0.9961 at 3 of 4 shapes on the basis and 0.9922 at 4 of 4 on HEAD. Properties 1 and 3 hold, `worst` 0.059 and the tiers at 1.00x, 1.57x and 21.22x. This is one of the four classes whose `list` stayed inside the 0.7% bar, at 1.0041, so its cross-half line may be subtracted: 20 arms faster on the basis and 26 on HEAD at a geomean of 0.9925, the range running from `bq-odo-gm-mulback` at 0.9200 to `gen-unsafe-aa-adjacent` at 1.1081 --- the pure family and the baseline again, with the fills between them.

**`reshape1` --- the `[n] -> [n, 1]` trap: innermost extent 1 on a stride-0 axis.** Shapes: `reshape1-500k` (`l` 500000, `sInner` 1), `reshape1-r3` (`l` 180000, `sInner` 1), `reshape1-rank10` (`l` 59049, `sInner` 1), `reshape1-strided-r3` (`l` 180000, `sInner` 1). The fourth landed 2026-08-25 and is the one cell of this class that prices a fill: it is `reshape1-r3`'s dense shape viewed with its innermost two dimensions transposed before the size-1 dim is appended, so dropping that dim leaves a strided view where the other three leave a contiguous run.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.32* | *84* | *4.91x* |
| *canon-full-nosum* | *--* | *--* | *0.36* | *254* | *0.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.30* | *104* | *2.00x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.20* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *115* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *115* | *0.00x* |
| libunord-stage2 | 0.000 | 0.000 | 0.02 | 115 | 0.00x |
| lib-stage2-short-lean | 0.000 | 0.014 | 0.01 | 110 | 0.00x |
| lib-stage2-lean | 0.000 | 0.014 | 0.01 | 110 | 0.00x |
| lib-stage2-concat | 0.000 | 0.014 | 0.01 | 110 | 0.00x |
| lib-stage2 | 0.000 | 0.014 | 0.01 | 110 | 0.00x |
| lib-stage2-disp | 0.000 | 0.014 | 0.01 | 110 | 0.00x |
| lib-stage2-short | 0.000 | 0.014 | 0.01 | 110 | 0.00x |
| canon-full | 0.000 | 0.015 | 0.04 | 110 | 0.00x |
| canon-vecdims | 0.000 | 0.015 | 0.02 | 110 | 0.00x |
| liblist-stage2 | 0.011 | 0.023 | 0.23 | 104 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.023 | 0.056 | 0.11 | 100 | 1.00x |
| lib-stage1 | 0.024 | 0.056 | 0.13 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.056 | 0.15 | 100 | 1.00x |
| liblist-stage1 | 0.032 | 0.062 | 0.20 | 97 | 2.00x |
| mut-flat-gm | 0.033 | 0.122 | 0.22 | 96 | 2.00x |
| bq-mut-runs-gm-mulback | 0.033 | 0.124 | 0.29 | 96 | 2.00x |
| libunord-stage1 | 0.033 | 0.062 | 0.34 | 96 | 2.00x |
| *bq-odo-gm-mulback-aa-distant* | *0.047* | *0.137* | *0.13* | *93* | *2.26x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.047* | *0.138* | *0.19* | *92* | *2.26x* |
| bq-odo-gm-mulback | 0.047 | 0.138 | 0.20 | 92 | 2.26x |
| bq-expand-gm-mulback | 0.071 | 0.163 | 0.49 | 87 | 4.91x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.072* | *0.088* | *0.13* | *86* | *2.00x* |
| **bq-scan-rem-gm-mulback** | **0.072** | 0.089 | 0.27 | 86 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.072* | *0.089* | *0.14* | *86* | *2.00x* |
| offtab-scan-rem | 0.072 | 0.090 | 0.13 | 86 | 2.00x |
| bcast-set | 0.084 | 0.100 | 0.13 | 84 | 1.00x |
| mid-copy | 0.090 | 0.108 | 0.12 | 82 | 1.00x |
| mut-odo-vecdims-add-in | 0.091 | 0.106 | 0.10 | 82 | 1.00x |
| **mut-odo-vecdims** | **0.091** | 0.105 | 0.09 | 82 | 1.00x |
| *mut-odo-vecdims-aa* | *0.091* | *0.105* | *0.14* | *82* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.091* | *0.106* | *0.19* | *82* | *1.00x* |
| *bq-expand-aa-distant* | *0.110* | *0.192* | *0.26* | *80* | *4.91x* |
| bq-expand | 0.110 | 0.194 | 0.33 | 80 | 4.91x |
| *bq-expand-aa-adjacent* | *0.111* | *0.194* | *0.28* | *80* | *4.91x* |
| *build-aa-distant* | *0.224* | *0.295* | *2.01* | *67* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.230* | *0.296* | *1.56* | *67* | *1.00x* |
| *mut-odo-aa-distant* | *0.230* | *0.296* | *1.55* | *66* | *1.00x* |
| *build-aa-adjacent* | *0.236* | *0.286* | *1.91* | *67* | *1.00x* |
| mut-odo | 0.236 | 0.287 | 2.20 | 66 | 1.00x |
| build | 0.238 | 0.295 | 2.11 | 66 | 1.00x |
| *gen-unsafe-aa-adjacent* | *0.859* | *2.003* | *2.49* | *44* | *1.00x* |
| gen-unsafe | 0.863 | 2.081 | 2.59 | 44 | 1.00x |
| *gen-unsafe-aa-distant* | *0.882* | *2.080* | *1.35* | *44* | *1.00x* |
| *list-aa-distant* | *0.996* | *0.999* | *0.37* | *41* | *32.29x* |
| *list-aa-adjacent* | *0.998* | *1.003* | *0.39* | *41* | *32.29x* |
| list (baseline) | 1.000 | 1.000 | 0.43 | 41 | 32.29x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0217, worst cell 6.96% on `reshape1-strided-r3`, and 13 of 16 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.09% on `reshape1-strided-r3`, its interval covering 1. The in-situ term reads 1.0025, 1.0035, 1.0112, 1.1145 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0214, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h18m2s, peak 150 MiB in use, 38 MiB max residency; the reader reads 52 benchmarks over 4 shapes of the reshape1 class. Anchor: `reshape1-500k`, `list` at 13.8 ms per call raw, 13.5 ms net.

**Per shape, in the lead's order (reshape1-500k, reshape1-r3, reshape1-rank10, reshape1-strided-r3):** `mut-odo-vecdims` 0.086/0.087/0.105/0.091 `bq-scan-rem-gm-mulback` 0.069/0.070/0.089/0.072

**Across the halves:** 22 of the 37 voting arms are faster on this half and 15 slower, at a geomean of 0.9903, from `bcast-set` at 0.8519 to `gen-unsafe-aa-distant` at 1.1353, `canon-full`, `canon-vecdims`, `lib-stage2`, `lib-stage2-concat`, `lib-stage2-disp`, `lib-stage2-lean`, `lib-stage2-short`, `lib-stage2-short-lean`, `libunord-stage2` sitting out as degenerate, a basis cell of theirs not left positive by the correction, with `list` itself at 1.0327. **The baseline moved 3.27% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** it is the class the correction gives out on, and this run it gives out differently on each half. Nine arms are degenerate here --- the six `lib-stage2*` arms, both `canon-*` arms and `libunord-stage2` --- and the shape they sink on is `reshape1-500k` on the basis, where on HEAD eight sink on `reshape1-r3` and `lib-stage2-short-lean` on `reshape1-500k`, so the cross-half line votes 37 arms and not 46 and a family reading is only available over the two shapes neither half sinks on. Over those two the orderings hold: `lib-stage2-lean` 0.9215 of `lib-stage2` on the basis and 0.9711 on HEAD, `lib-stage2-short` 0.9507 and 1.0086. Properties 1 and 3 hold for `mut-odo-vecdims` --- `worst` 0.105, the widest of the nine, and the tiers at 1.00x, 4.91x and 32.29x, where `m = l` puts `bq-expand` at nearly five times the result --- and property 2 breaks to `libunord-stage2` at 0.000. Its `list` moved **3.27%**, far the widest of the nine, so nothing here is subtracted.

**`slice` --- a view of a larger source: non-zero offset, positive strides.** Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes` (`l` 250357, `sInner` 89), `slice-coprime-r7` (`l` 60060, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *90* | *1.58x* |
| *canon-full-nosum* | *--* | *--* | *0.08* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.18* | *94* | *1.08x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| lib-stage2-short-lean | 0.029 | 0.031 | 0.13 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.029 | 0.034 | 0.08 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.029 | 0.034 | 0.13 | 101 | 1.00x |
| lib-stage2-short | 0.030 | 0.031 | 0.08 | 102 | 1.00x |
| lib-stage1 | 0.030 | 0.034 | 0.11 | 100 | 1.00x |
| lib-stage2-lean | 0.030 | 0.036 | 0.08 | 100 | 1.00x |
| lib-stage2-concat | 0.030 | 0.036 | 0.22 | 100 | 1.00x |
| lib-stage2-disp | 0.030 | 0.036 | 0.13 | 100 | 1.00x |
| lib-stage2 | 0.030 | 0.036 | 0.10 | 100 | 1.00x |
| mut-odo-vecdims-add-in | 0.040 | 0.058 | 0.07 | 96 | 1.00x |
| **mut-odo-vecdims** | **0.040** | 0.058 | 0.08 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.040* | *0.058* | *0.08* | *96* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.040* | *0.058* | *0.08* | *96* | *1.00x* |
| mid-copy | 0.040 | 0.059 | 0.09 | 96 | 1.00x |
| canon-vecdims | 0.040 | 0.058 | 0.11 | 96 | 1.00x |
| bcast-set | 0.042 | 0.061 | 0.10 | 96 | 1.00x |
| canon-full | 0.042 | 0.065 | 0.09 | 96 | 1.00x |
| libunord-stage2 | 0.043 | 0.050 | 0.14 | 96 | 2.01x |
| libunord-stage1 | 0.043 | 0.048 | 0.17 | 96 | 2.00x |
| liblist-stage2 | 0.044 | 0.050 | 0.12 | 96 | 2.00x |
| liblist-stage1 | 0.044 | 0.048 | 0.20 | 96 | 2.00x |
| *mut-odo-aa-distant* | *0.065* | *0.136* | *0.84* | *96* | *1.00x* |
| build | 0.065 | 0.138 | 1.25 | 96 | 1.00x |
| *mut-odo-aa-adjacent* | *0.065* | *0.138* | *0.23* | *96* | *1.00x* |
| mut-odo | 0.065 | 0.142 | 0.95 | 96 | 1.00x |
| *build-aa-adjacent* | *0.066* | *0.143* | *1.16* | *96* | *1.00x* |
| *build-aa-distant* | *0.066* | *0.144* | *1.01* | *96* | *1.00x* |
| mut-flat-gm | 0.084 | 0.089 | 0.15 | 88 | 1.08x |
| bq-mut-runs-gm-mulback | 0.094 | 0.094 | 0.10 | 87 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.105* | *0.12* | *86* | *1.08x* |
| **bq-scan-rem-gm-mulback** | **0.100** | 0.106 | 0.13 | 86 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.106* | *0.10* | *86* | *1.08x* |
| bq-expand-gm-mulback | 0.104 | 0.120 | 0.10 | 83 | 1.58x |
| *bq-odo-gm-mulback-aa-distant* | *0.110* | *0.123* | *0.09* | *83* | *1.50x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.111* | *0.123* | *0.11* | *83* | *1.50x* |
| *bq-expand-aa-adjacent* | *0.111* | *0.129* | *0.11* | *83* | *1.58x* |
| bq-expand | 0.111 | 0.130 | 0.11 | 83 | 1.58x |
| bq-odo-gm-mulback | 0.111 | 0.123 | 0.24 | 83 | 1.50x |
| *bq-expand-aa-distant* | *0.112* | *0.131* | *0.10* | *83* | *1.58x* |
| offtab-scan-rem | 0.130 | 0.134 | 0.15 | 82 | 2.00x |
| *list-aa-distant* | *0.999* | *1.009* | *0.24* | *47* | *20.54x* |
| list (baseline) | 1.000 | 1.000 | 0.22 | 46 | 20.54x |
| *list-aa-adjacent* | *1.003* | *1.009* | *0.16* | *46* | *20.54x* |
| gen-unsafe | 1.484 | 2.471 | 1.63 | 43 | 1.00x |
| *gen-unsafe-aa-distant* | *1.531* | *2.530* | *2.25* | *43* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *1.532* | *2.404* | *1.14* | *43* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 1.0276, worst cell 11.76% on `slice-cnn-L2-24x24-c32`, and 15 of 16 intervals cover 1. The `sum-only` halves agree at 1.0003 on a worst cell of 0.04% on `slice-cnn-L2-24x24-c32`, its interval missing 1. The in-situ term reads 1.0088, 1.0111, 1.0213, 1.0422 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0270, which the correction amplifies by 1.02x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m32s, peak 124 MiB in use, 37 MiB max residency; the reader reads 52 benchmarks over 3 shapes of the slice class. Anchor: `slice-primes`, `list` at 4.11 ms per call raw, 3.95 ms net.

**Per shape, in the lead's order (slice-cnn-L2-24x24-c32, slice-primes, slice-coprime-r7):** `mut-odo-vecdims` 0.058/0.030/0.036 `bq-scan-rem-gm-mulback` 0.098/0.106/0.095

**Across the halves:** 21 of the 46 arms are faster on this half and 25 slower, at a geomean of 1.0006, from `bq-scan-rem-gm-mulback-aa-adjacent` at 0.9407 to `gen-unsafe-aa-adjacent` at 1.1206, with `list` itself at 1.0008.

**What the class says:** the composite leads it and the `mut-odo-vecdims` family is level with it. `lib-stage2-short-lean` reads 0.029 against `mut-odo-vecdims`'s 0.040, a **28.42%** margin on a 2.76% floor, with `mut-odo-vecdims-add-in-leaf-u2` at the same 0.029 --- so property 2's break and the family's ceiling name the same figure and the class does not separate them. Properties 1 and 3 hold, `worst` 0.058 and the tiers at 1.00x, 1.58x and 20.54x. It is the one class of the nine whose cross-half geomean sits above 1, at 1.0006, on a `list` that moved 0.08% --- and with `window`'s 0.9995 it is one of the two that sit within a thousandth of 1, which is the clearest statement this run makes that the two compilers are, on a whole population, the same speed.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-128x128-k7` (`l` 729316, `sInner` 7 --- landed on Run 24, the k7 patch the short bodies do not fire on).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.26* | *92* | *2.48x* |
| *canon-full-nosum* | *--* | *--* | *0.42* | *120* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.44* | *104* | *1.27x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *103* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *123* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *123* | *0.00x* |
| lib-stage2-short-lean | 0.020 | 0.028 | 0.17 | 112 | 1.00x |
| lib-stage2-short | 0.020 | 0.028 | 0.18 | 112 | 1.00x |
| lib-stage2-lean | 0.022 | 0.033 | 0.14 | 111 | 1.00x |
| lib-stage2 | 0.022 | 0.033 | 0.17 | 111 | 1.00x |
| lib-stage2-disp | 0.022 | 0.033 | 0.16 | 111 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.026 | 0.031 | 0.19 | 108 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.031 | 0.15 | 107 | 1.00x |
| lib-stage1 | 0.026 | 0.031 | 0.14 | 107 | 1.00x |
| lib-stage2-concat | 0.035 | 0.144 | 0.22 | 95 | 1.01x |
| canon-vecdims | 0.037 | 0.057 | 0.12 | 106 | 1.00x |
| canon-full | 0.039 | 0.064 | 0.29 | 106 | 1.00x |
| liblist-stage1 | 0.039 | 0.045 | 0.30 | 104 | 2.00x |
| libunord-stage1 | 0.039 | 0.044 | 0.50 | 104 | 2.01x |
| liblist-stage2 | 0.048 | 0.092 | 0.24 | 97 | 2.01x |
| libunord-stage2 | 0.049 | 0.092 | 0.25 | 97 | 2.03x |
| mut-odo-vecdims-add-in | 0.054 | 0.095 | 0.13 | 96 | 1.00x |
| **mut-odo-vecdims** | **0.054** | 0.094 | 0.17 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.054* | *0.094* | *0.12* | *96* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.054* | *0.095* | *0.13* | *96* | *1.00x* |
| mid-copy | 0.055 | 0.095 | 0.15 | 96 | 1.00x |
| bcast-set | 0.059 | 0.103 | 0.19 | 94 | 1.00x |
| mut-flat-gm | 0.070 | 0.087 | 0.23 | 98 | 1.27x |
| bq-mut-runs-gm-mulback | 0.084 | 0.098 | 0.29 | 97 | 1.27x |
| **bq-scan-rem-gm-mulback** | **0.092** | 0.096 | 0.17 | 94 | 1.27x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.092* | *0.096* | *0.19* | *94* | *1.27x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.092* | *0.096* | *0.16* | *94* | *1.27x* |
| *bq-odo-gm-mulback-aa-distant* | *0.093* | *0.122* | *0.21* | *92* | *2.10x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.094* | *0.122* | *0.29* | *92* | *2.10x* |
| bq-odo-gm-mulback | 0.094 | 0.123 | 0.27 | 92 | 2.10x |
| bq-expand-gm-mulback | 0.096 | 0.119 | 0.23 | 92 | 2.48x |
| *bq-expand-aa-distant* | *0.115* | *0.128* | *0.18* | *88* | *2.48x* |
| bq-expand | 0.115 | 0.129 | 0.25 | 88 | 2.48x |
| *bq-expand-aa-adjacent* | *0.116* | *0.129* | *0.21* | *88* | *2.48x* |
| mut-odo | 0.119 | 0.232 | 1.83 | 82 | 1.00x |
| offtab-scan-rem | 0.121 | 0.126 | 0.22 | 92 | 2.00x |
| *build-aa-distant* | *0.122* | *0.266* | *1.43* | *82* | *1.00x* |
| *mut-odo-aa-distant* | *0.124* | *0.250* | *2.01* | *82* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.124* | *0.249* | *1.02* | *82* | *1.00x* |
| *build-aa-adjacent* | *0.130* | *0.272* | *1.65* | *82* | *1.00x* |
| build | 0.131 | 0.270 | 1.42 | 81 | 1.00x |
| *list-aa-distant* | *0.992* | *1.013* | *0.37* | *52* | *23.44x* |
| list (baseline) | 1.000 | 1.000 | 0.45 | 52 | 23.44x |
| *list-aa-adjacent* | *1.006* | *1.020* | *0.56* | *52* | *23.44x* |
| gen-unsafe | 1.092 | 1.293 | 1.45 | 53 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.118* | *1.346* | *1.46* | *53* | *1.00x* |
| *gen-unsafe-aa-distant* | *1.127* | *1.347* | *2.65* | *53* | *1.00x* |

**Controls:** The largest A/A pair is `build-aa-distant` at 0.9306, worst cell 9.25% on `window-224x224-k3`, and 9 of 16 intervals cover 1. The `sum-only` halves agree at 1.0008 on a worst cell of 0.35% on `window-224x224-k3`, its interval covering 1. The in-situ term reads 1.0039, 1.0018, 0.9988, 1.0306 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9471, which the correction amplifies by 1.27x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h17m59s, peak 130 MiB in use, 32 MiB max residency; the reader reads 52 benchmarks over 4 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 12.8 ms per call raw, 12.4 ms net.

**Per shape, in the lead's order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7):** `mut-odo-vecdims` 0.044/0.056/0.094/0.036 `bq-scan-rem-gm-mulback` 0.095/0.096/0.073/0.092

**Across the halves:** 22 of the 46 arms are faster on this half and 24 slower, at a geomean of 0.9995, from `canon-full` at 0.9328 to `gen-unsafe-aa-adjacent` at 1.1132, with `list` itself at 1.0062.

**What the class says:** the composite leads it by the widest margin of the three classes it leads. `lib-stage2-short-lean` reads 0.020 against `mut-odo-vecdims`'s 0.054, a **63.79%** margin on this class's 6.94% floor --- the widest floor of the nine, which is why the margin is quoted against it and still clears it ninefold. Properties 1 and 3 hold, `worst` 0.094 and the tiers at 1.00x, 2.48x and 23.44x. The class gained `window-128x128-k7` this run, a k7 patch on which the short bodies do not fire, and it does what registration 1 predicted: `lib-stage2-short` reads 1.0179 of `lib-stage2` there on the basis and 1.0150 on HEAD, both inside the floor, where on `window-28x28-k5` and `window-224x224-k3` it reads 0.8045 and 0.8331. Across the halves the class is a near-tie at 0.9995 on a `list` that moved 0.62%, inside the bar.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *118* | *1.14x* |
| *canon-full-nosum* | *--* | *--* | *0.11* | *144* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.13* | *124* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *144* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *137* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *137* | *0.00x* |
| lib-stage1 | 0.026 | 0.034 | 0.11 | 127 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.027 | 0.033 | 0.11 | 127 | 1.00x |
| lib-stage2-short-lean | 0.028 | 0.034 | 0.18 | 126 | 1.00x |
| lib-stage2-lean | 0.028 | 0.034 | 0.14 | 126 | 1.00x |
| lib-stage2-disp | 0.028 | 0.034 | 0.14 | 126 | 1.00x |
| lib-stage2-concat | 0.028 | 0.034 | 0.14 | 126 | 1.00x |
| lib-stage2 | 0.028 | 0.034 | 0.12 | 126 | 1.00x |
| lib-stage2-short | 0.028 | 0.034 | 0.15 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.028 | 0.034 | 0.20 | 126 | 1.00x |
| canon-vecdims | 0.030 | 0.032 | 0.07 | 126 | 1.00x |
| canon-full | 0.031 | 0.033 | 0.09 | 126 | 1.00x |
| mut-odo-vecdims-add-in | 0.031 | 0.033 | 0.10 | 126 | 1.00x |
| *mut-odo-vecdims-aa* | *0.031* | *0.033* | *0.09* | *126* | *1.00x* |
| **mut-odo-vecdims** | **0.031** | 0.033 | 0.08 | 126 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.031* | *0.033* | *0.10* | *126* | *1.00x* |
| bcast-set | 0.032 | 0.036 | 0.07 | 125 | 1.00x |
| mid-copy | 0.033 | 0.034 | 0.15 | 126 | 1.00x |
| build | 0.033 | 0.050 | 0.12 | 125 | 1.00x |
| *build-aa-distant* | *0.033* | *0.050* | *0.19* | *125* | *1.00x* |
| *build-aa-adjacent* | *0.033* | *0.049* | *0.17* | *125* | *1.00x* |
| mut-odo | 0.034 | 0.050 | 0.16 | 124 | 1.00x |
| *mut-odo-aa-distant* | *0.034* | *0.050* | *0.12* | *124* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.035* | *0.049* | *0.19* | *124* | *1.00x* |
| libunord-stage2 | 0.039 | 0.062 | 0.15 | 123 | 2.01x |
| liblist-stage2 | 0.039 | 0.061 | 0.23 | 123 | 2.00x |
| liblist-stage1 | 0.041 | 0.061 | 0.17 | 123 | 2.00x |
| libunord-stage1 | 0.043 | 0.061 | 0.28 | 123 | 2.01x |
| mut-flat-gm | 0.072 | 0.074 | 0.07 | 116 | 1.03x |
| bq-mut-runs-gm-mulback | 0.081 | 0.084 | 0.14 | 114 | 1.03x |
| bq-expand-gm-mulback | 0.085 | 0.089 | 0.10 | 113 | 1.14x |
| bq-odo-gm-mulback | 0.090 | 0.093 | 0.08 | 113 | 1.04x |
| *bq-odo-gm-mulback-aa-distant* | *0.090* | *0.093* | *0.06* | *113* | *1.04x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.090* | *0.093* | *0.08* | *113* | *1.04x* |
| **bq-scan-rem-gm-mulback** | **0.091** | 0.095 | 0.07 | 112 | 1.04x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.091* | *0.095* | *0.08* | *112* | *1.04x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.091* | *0.095* | *0.05* | *112* | *1.04x* |
| *bq-expand-aa-adjacent* | *0.096* | *0.100* | *0.07* | *111* | *1.14x* |
| bq-expand | 0.096 | 0.100 | 0.10 | 111 | 1.14x |
| *bq-expand-aa-distant* | *0.096* | *0.100* | *0.07* | *111* | *1.14x* |
| offtab-scan-rem | 0.129 | 0.132 | 0.09 | 107 | 2.00x |
| *gen-unsafe-aa-adjacent* | *0.853* | *1.840* | *0.94* | *69* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.858* | *1.827* | *0.82* | *69* | *1.00x* |
| gen-unsafe | 0.872 | 1.800 | 1.96 | 69 | 1.00x |
| *list-aa-distant* | *0.995* | *1.000* | *0.30* | *71* | *19.43x* |
| *list-aa-adjacent* | *0.998* | *1.002* | *0.27* | *71* | *19.43x* |
| list (baseline) | 1.000 | 1.000 | 0.32 | 71 | 19.43x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 0.9791, worst cell 10.13% on `scaled-rank1-m1`, and 14 of 16 intervals cover 1. The `sum-only` halves agree at 0.9994 on a worst cell of 0.45% on `scaled-rank1-m1`, its interval covering 1. The in-situ term reads 1.0278, 1.0119, 1.0158, 1.0158 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9823, which the correction amplifies by 1.06x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m29s, peak 124 MiB in use, 54 MiB max residency; the reader reads 52 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.02 ms per call raw, 4.83 ms net.

**Per shape, in the lead's order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.028/0.032/0.033 `bq-scan-rem-gm-mulback` 0.091/0.088/0.095

**Across the halves:** 30 of the 46 arms are faster on this half and 16 slower, at a geomean of 0.9855, from `bq-odo-gm-mulback` at 0.9065 to `gen-unsafe` at 1.0561, with `list` itself at 1.0067.

**What the class says:** the shipped route leads it outright, where a run ago it was the best arm outside the family here too and the class's lead was a `mut-odo-vecdims` sibling read as the family's. `lib-stage1` reads 0.026 against `mut-odo-vecdims`'s 0.031, a **9.07%** margin on a 2.09% floor --- the tightest floor of the nine --- so the arm the library actually calls is the best arm outside the vecdims family on this population. Properties 1 and 3 hold: `worst` 0.033, the narrowest of the nine and a factor of 30 inside 1, and the tiers at 1.00x, 1.14x and 19.43x, `bq-expand` sitting at its second-lowest level of the nine here, behind `runs`'s 1.08x, because this class's `m` is 1 and 2000. Across the halves it is the most one-sided of the nine, **30 arms faster on the basis and 16 on HEAD at a geomean of 0.9855**, on a `list` that moved 0.67% and so just inside the bar: the class where 9.12's codegen win is widest, `bq-odo-gm-mulback` at 0.9065.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven and on Run 24 to fourteen.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.43* | *52* | *1.08x* |
| *canon-full-nosum* | *--* | *--* | *0.58* | *76* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.33* | *57* | *1.02x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.19* | *76* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| lib-stage2-disp | 0.027 | 0.028 | 0.14 | 58 | 1.00x |
| lib-stage2-short | 0.027 | 0.029 | 0.19 | 58 | 1.00x |
| lib-stage2-short-lean | 0.027 | 0.029 | 0.28 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.027 | 0.029 | 0.13 | 59 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.029 | 0.19 | 58 | 1.00x |
| lib-stage2 | 0.027 | 0.029 | 0.18 | 58 | 1.00x |
| lib-stage2-lean | 0.027 | 0.029 | 0.27 | 58 | 1.00x |
| canon-vecdims | 0.031 | 0.062 | 0.27 | 58 | 1.00x |
| mid-copy | 0.032 | 0.063 | 0.31 | 58 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.063* | *0.10* | *58* | *1.00x* |
| mut-odo-vecdims-add-in | 0.032 | 0.063 | 0.12 | 58 | 1.00x |
| canon-full | 0.032 | 0.088 | 0.58 | 58 | 1.00x |
| *mut-odo-vecdims-aa* | *0.032* | *0.063* | *0.10* | *58* | *1.00x* |
| **mut-odo-vecdims** | **0.032** | 0.063 | 0.15 | 58 | 1.00x |
| bcast-set | 0.034 | 0.068 | 0.31 | 58 | 1.00x |
| *build-aa-adjacent* | *0.039* | *0.138* | *0.47* | *58* | *1.00x* |
| *mut-odo-aa-distant* | *0.039* | *0.149* | *0.21* | *58* | *1.00x* |
| *build-aa-distant* | *0.040* | *0.153* | *0.72* | *58* | *1.00x* |
| mut-odo | 0.041 | 0.146 | 0.34 | 58 | 1.00x |
| build | 0.041 | 0.146 | 0.54 | 58 | 1.00x |
| *mut-odo-aa-adjacent* | *0.042* | *0.152* | *0.27* | *58* | *1.00x* |
| libunord-stage2 | 0.067 | 1.126 | 0.51 | 56 | 1.14x |
| liblist-stage2 | 0.068 | 1.123 | 0.53 | 56 | 1.14x |
| mut-flat-gm | 0.072 | 0.077 | 0.37 | 49 | 1.02x |
| bq-expand-gm-mulback | 0.084 | 0.088 | 0.40 | 47 | 1.08x |
| bq-mut-runs-gm-mulback | 0.085 | 0.090 | 0.37 | 47 | 1.02x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.088* | *0.093* | *0.48* | *47* | *1.03x* |
| bq-odo-gm-mulback | 0.088 | 0.093 | 0.40 | 47 | 1.03x |
| *bq-odo-gm-mulback-aa-distant* | *0.089* | *0.092* | *0.04* | *47* | *1.03x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.094* | *0.102* | *0.04* | *46* | *1.02x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.094* | *0.101* | *0.44* | *46* | *1.02x* |
| **bq-scan-rem-gm-mulback** | **0.094** | 0.101 | 0.40 | 46 | 1.02x |
| bq-expand | 0.097 | 0.102 | 0.56 | 46 | 1.08x |
| *bq-expand-aa-adjacent* | *0.097* | *0.102* | *0.50* | *46* | *1.08x* |
| *bq-expand-aa-distant* | *0.097* | *0.102* | *0.04* | *46* | *1.08x* |
| lib-stage1 | 0.106 | 1.314 | 0.51 | 54 | 1.19x |
| libunord-stage1 | 0.106 | 1.337 | 0.51 | 54 | 1.19x |
| liblist-stage1 | 0.107 | 1.326 | 0.81 | 54 | 1.19x |
| lib-stage2-concat | 0.109 | 1.319 | 0.49 | 54 | 1.21x |
| offtab-scan-rem | 0.137 | 0.146 | 0.67 | 41 | 2.00x |
| *gen-unsafe-aa-adjacent* | *0.639* | *1.066* | *3.98* | *22* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.644* | *0.977* | *4.21* | *22* | *1.00x* |
| gen-unsafe | 0.647 | 0.921 | 3.88 | 22 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 2.71 | 17 | 19.27x |
| *list-aa-distant* | *1.017* | *1.051* | *2.04* | *17* | *19.27x* |
| *list-aa-adjacent* | *1.031* | *1.052* | *0.26* | *18* | *19.27x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0307, worst cell 5.17% on `runs-r3-48x30`, and 13 of 16 intervals cover 1. The `sum-only` halves agree at 1.0003 on a worst cell of 0.52% on `runs-4096`, its interval covering 1. The in-situ term reads 1.0343, 1.0302, 1.0310, 1.0266 of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0295, which the correction amplifies by 1.04x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 1h3m7s, peak 571 MiB in use, 251 MiB max residency; the reader reads 52 benchmarks over 14 shapes of the runs class. Anchor: `runs-2`, `list` at 38.7 ms per call raw, 37.6 ms net.

**Per shape, in the lead's order (runs-2, runs-3, runs-4, runs-5, runs-7, runs-9, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.063/0.052/0.046/0.042/0.038/0.034/0.028/0.028/0.029/0.028/0.028/0.029/0.027/0.030 `bq-scan-rem-gm-mulback` 0.101/0.099/0.098/0.094/0.096/0.092/0.091/0.091/0.090/0.090/0.091/0.093/0.093/0.093

**Across the halves:** 24 of the 46 arms are faster on this half and 22 slower, at a geomean of 0.9886, from `bq-odo-gm-mulback-aa-distant` at 0.8988 to `gen-unsafe-aa-adjacent` at 1.0568, with `list` itself at 1.0104. **The baseline moved 1.04% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** the re-cut dispatch leads it, which is registration 6's whole point, where Run 23 read the dispatch killed at `runs-1024` on both halves. `lib-stage2-disp` reads 0.027 against `mut-odo-vecdims`'s 0.032, a **22.87%** margin on a 3.07% floor, and against the routes it chooses between it is at or below the better at every one of the fourteen lengths on both halves: against `lib-stage2` it runs 0.8705 to 1.0015 on the basis and 0.8696 to 1.0181 on HEAD, every reading above 1 inside the floor, and its win is concentrated where the threshold now sends work to the slice route, 0.8705, 0.8919 and 0.8953 at `runs-16384`, `runs-65536` and `runs-4096`. Property 1 BREAKS here and only here, as it has every run: six of the eleven library-shaped arms carry a `worst` above 1, all at `runs-2`, `lib-stage1` --- the shipped route --- among them at 1.314 and 1.303. Property 3 holds, the tiers at 1.00x, 1.08x and 19.27x. The class gained `runs-7`, `runs-4096` and `runs-16384` this run; `runs-7` is the length one past the short bodies, and `lib-stage2-short` reads 0.9986 of `lib-stage2` there against 0.8900 at `runs-2`, which is the short body switching off exactly where it was registered to. Its `list` moved 1.04%, so the cross-half line is ordered and not subtracted.



## Provenance

What this run's figures have to be read against, and it is a section of this file because a run replaces every word of it. What does NOT move with a run --- the delta chain that says which shape set and roster each run measured, and the list of what a run replaces outside this file --- is [README's own Provenance][prov].

**Run 24's halves differ in the compiler and in the boot libraries that come with it, and in nothing else.** One source, `Main.hs` at `7dd094e`, one shim, `align-as.py` at `38bb3bb`, set the same way on both halves, and one shim environment --- `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1`, under which `rewrite()` returns through `plan_dead()` before either of the first two is read, so both binaries carry the dead-spot layout and the two command lines differ in nothing the shim can see. The basis is built through the default project file and freeze against ghc-9.12.4, the default on PATH here; the other half through `cabal.project.ghead`, which selects the in-tree stage1 of the GHC checkout under `~/r/horde-ad/ghc` and pins its plan at the same index-state, so the halves differ in the compiler and in the boot libraries that come with it and in nothing a freeze can see. There is no such compiler on PATH, so the version is read out of the BINARY and not off the project file: `ghc-internal-9.1204.0` against `ghc-internal-10.100.0`, the project file reporting `10.1.20260803`. Both carry `-fspec-constr -fobject-determinism`, `LOOP_NOOVERLAP` unset, and both ran under `WILDLOG=1 SATURATE=1`. What the pair prices is a change of codegen over a roster whose layout is already the dead-spot form's --- the first run to read that form on a second compiler, and the reason a form about to be published is owed such a reading.

**The sequence was launched once and ran to the end in one window**, 2026-09-03T02:54:41 to 2026-09-03T12:58:25, twenty processes, every one exiting 0 at the count its roster holds --- 1352 twice, 728 twice, 208 six times and 156 ten times --- each carrying its one `@@saturate` line and its `@@wild` stamps, and the driver recording no complaint and no `!!` line. The HEAD half ran first throughout, `ghead` before `g912` on the main set and on each class in turn, which is the driver's order; the eighteen class processes span 0h13m29s to 1h3m22s, the two `runs` processes taking the whole top of that range. The plateau gate reads every process's preamble victim inside **19.594 to 20.1976 ms/iter, a 3.08% spread** against the 5% band, where Run 23 read 4.63%. **Nothing happened on the machine during the window**: the per-sample instrument's foreign-CPU column, read over all 1352 benches of each of the two main processes, puts NOT ONE bench at or above 0.25 on either half, so post-run step 3 did not fire and no population was rerun. **What did happen was before the window**: the gate was launched at 02:06 and stopped by hand two minutes in, when the machine was wanted; its four partial artifacts were moved out of the tree and the recorded gate is the relaunch of 02:09:17, which ran to 02:54:39 on a box reading 0.7% non-idle and passed on both passes.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run24-g912`, md5 `0ea817d7761de51b5faecf48cb24c00f`, and `run24-ghead`, md5 `8eb43268b618d27665140d38b9506bd6`, with `.text` of 20533445 and 20674367 bytes --- the HEAD half 140922 bytes larger. **Neither reproduces an earlier binary and neither was meant to**: `Main.hs` moved between Run 23 and this run by two commits of 2026-09-02, `6d7689a` and `7dd094e`, so no md5 here matches one on record and the repetition reading Runs 19 and 23 could take is not available. Both report criterion 1.6.5.0, both bake `-A32m -I0 -T -M8G` read back by `+RTS --info`, both carry exactly one `@@wild` and one `@@saturate` string, their `--list` outputs are identical at 1352 and their `classes --list` at 2132 over 41 views, and their `check` logs are byte-identical --- which two compilers did not have to be, a float-printing difference being the one thing such a difference could innocently have been. The tree at launch was `4e2e60a` with twelve untracked scratch paths and nothing modified; two commits landed on the branch during the evening, `8d0848d` and `a499d8f`, and both touch only `preflight.sh`, `smoke-l1.sh` and `smoke-sweep.sh`, none of which is an input to either binary.

**The roster and the source moved, which is what puts a layout term in the cross-run column**, and the fills say how much. The eight tracked 28-byte loops were read at the build against `run23-spot`, the previous build of this recipe: **every mod-64 offset is preserved in both groups, the first address of each group survives to the byte, and the other six all moved by ONE constant, 0x940** --- which neither Run 20's nor Run 21's roster change did, both of those reading no address surviving and none moved by a constant. Post-run step 0's `-g3` twins then named all eight on the basis: the six-copy group is `fbMidCopy` 0x425540, `fbMutOdoVecdimsAddIn` 0x42e980, `fbMutOdoVecdims` 0x42f898 at offset 24, `fbMutOdoVecdimsAddOut` 0x456180, `fbMutOdoVecdimsAddBoth` 0x4574c4 at offset 4 and `fbCanonVecdims` 0x459ad8 at offset 24, and the two-copy group `fbBuild` 0x424b00 and `fbMutOdo` 0x430880. On the HEAD half no tracked address is shared with the basis, the group offsets read `[18, 31, 7, 9, 26, 7]`, and a third group appears which the twin names as the `bq-mut` family and not a fill --- `fbBQmutRunsGmMulback`, `fbBQmutLemireMulback` and `fbBQmutRunsMulback`. **And the `-g3` twin is a different program on one compiler and not on the other**: on 9.12 the twin's `.text` is the timed binary's to the byte and it sits 0x180 to 0x1c0 below it with every offset preserved, where on HEAD its `.text` is 98304 bytes larger and its own six-copy group reads `[18, 0, 0, 0, 21, 0]` at addresses up to 0x8661 away. Four self-loops straddle a cache line on each half, at the two body lengths Run 23's dead-spot half had; on the basis the twin names all four --- `fillStage2Short` 0x4205aa, `fillStage2` 0x422b2a, `fbMutOdoVecdimsAddInLeafU2` 0x429b6a and `fbMutOdoVecdimsAddInLeafU2Down` 0x428b2f --- and on HEAD it names two and refuses the other two, holding no byte-identical copy, which is the count check doing what Run 22's did on three of four.

**The three main-set anchors** read **5.97 us** on `cnn-slice-c32`, **3.06 ms** on `cifar-L2-16-c64-k3` and **37.6 ms** on `stretch-wide-2xM`, net of the forcing pass, on the basis half, against **5.92 us**, **3.05 ms** and **38.2 ms** on the HEAD half --- the two compilers within a percent on the two small anchors and one and a half apart on the large one, the HEAD half the slower there. They are what says the box has not moved under the run, and the machine check reads them against the fingerprint Run 23 kept at -0.20% and -0.39% over 24 of 26 shapes.

| shape | `l` | `list`, per call | net | HEAD, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.14 us | 5.97 us | 5.92 us |
| `cifar-L2-16-c64-k3` | 147456 | 3.15 ms | 3.06 ms | 3.05 ms |
| `stretch-wide-2xM` | 1800000 | 38.7 ms | 37.6 ms | 38.2 ms |

**Each stride class carries an anchor of its own, beside its table, and all nine are `list` on one of that class's shapes, raw and net.** The main set's three guard a baseline that moves for every population at once; a class anchor guards one that could move for that mechanism alone, which is the case a table of ratios hides completely. The `runs` anchor is `runs-2` at 38.7 ms raw and 37.6 ms net, against Run 23's 38.2 ms and 37.1 ms --- 1.3% apart on a class whose own floor is 3.07%, across a roster change and two builds. Read a class anchor against the same class's anchor in an earlier run and against nothing else, and against that class's own floor rather than the main set's.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0001** on the basis and **1.0000** on the HEAD half, both within a hundredth of a point of 1 --- so a reader wanting a raw figure can recover it, and a reader comparing against a run that corrected differently can say by how much. The in-situ check, which is a different instrument and not the correction, reads 1.0198, 1.0174, 1.0071 and 1.0683 on the basis and 1.0217, 1.0168, 0.9927 and 1.0687 on the HEAD half, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm` and `bq-expand`.

[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

Registered 2026-09-02, on the pair [the next-run section](#what-the-next-run-compares-against) settles, ghc-9.12.4 and GHC HEAD both under `LOOP_DEADSPOT=1`, over the roster and shapes task 9 adds and the parkings of the same day: `lib-stage2-u4`, `lib-stage2-disp` at 256, `mut-odo-vecdims-add-in-leaf`, `mut-odo-vecdims-add-in-leaf-down` and `canon-memcpy-r2` to `Only`, each on a verdict Run 23 read on both halves. Each with a prediction and a kill condition, and the verdicts move to Run 24's file with them. (1) *The short bodies.* `lib-stage2-short` reads ahead of `lib-stage2` past each population's floor wherever the canonical inner run is 2 to 5 --- the k3 and k5 main-set shapes, `window-28x28-k5`, `window-224x224-k3` and `runs-2` to `runs-5` --- on both halves, and at count ratio 1.0000 against it with its time inside the floor on every shape where the body does not fire, `runs-7` and `window-128x128-k7` among them; killed by a shape where the body fires reading it behind past the floor on both halves, or by a count ratio off 1.0000 where it does not. (2) *The lean dispatch.* `lib-stage2-lean` reads at or below `lib-stage2` within the floor on every population, and ahead past the floor on the four smallest main-set shapes, `lenet-slice-c6-k5`, `cnn-slice-c32`, `cnn-L1-6x6-c1` and `cnn-L1-12x12-c1`; killed by any shape reading it behind past the floor on both halves. (3) *The composite.* `lib-stage2-short-lean` reads at or below the better of its two parents on every population within the floor; killed by reading behind either parent past the floor on both halves. (4) *The straddlers.* The survey names four straddling self-loops on each half, the outer loops of `fillStage2`, `fillStage2Short` and the two `-u2` leaf fills, their inner loops at offset 0, as Run 23's dead-spot half had them; killed by a fill's inner loop straddling on either half. (5) *HEAD.* The HEAD half reads (1) to (3) with the 9.12 half's verdicts, and Run 23's dead-spot standings within two points --- `lib-stage2` against `lib-stage1` 0.95 on the main set and 1.01 on `slice`, `-u2` ahead of `-down` in every population, the shipped route about four percent over the bare fill; killed by any ordering in (1) to (3) reversing past HEAD's floor. (6) *The threshold.* The dispatch arm task 9's probe picks reads at or below the better of `lib-stage2` and `lib-stage2-concat` at every `runs` length within that class's floor, on both halves; killed by reading behind the better route past the floor at any length. The probe landed the same evening and picked 2048 (task 9), so the arm is `lib-stage2-disp` re-cut to it.

**Four held, one held on its orderings and not on one of its figures, one split, and one clause of that fifth could not be read at all --- and that last is the finding.** Every figure below is re-derived from this run's own JSONs and counts files rather than carried from the registration, the main-set ones over the 25 shapes that exclude `stretch-inner1`, where `lib-stage2-lean`'s cell is its own forcing term on the HEAD half; margins are judged against the population's own sixteen-pair floor on the half they are read on --- 1.26% and 2.11% on the main set and the nine class figures in the summary table above --- because that is the threshold every one of the six registrations states for itself, `past each population's floor`. It is NOT the six-pair figure, which is what two rows of the published table must clear and which the Results section applies to the standing controls; a registration written against the wrong one of those two would be judged against the wrong one here.

(1) *The short bodies.* **SPLIT.** Where the canonical inner run is 2 to 5 the arm is ahead past both halves' floors on every shape the registration names: the k3 and k5 main-set shapes read **0.8536, 0.8361, 0.8715, 0.8911 and 0.9422** on the basis (`cifar-L2-16-c64-k3`, `vgg-14-c512-k3`, `lenet-L1-28-c1-k5`, `alexnet-L2-27-c48-k5`, `lenet-slice-c6-k5`) and 0.8487, 0.8528, 0.8825, 0.9041 and 0.9661 on HEAD; `window-28x28-k5` **0.8045** and 0.8289 and `window-224x224-k3` 0.8331 and 0.8559 against that class's floor on the two halves, 6.94% and 3.19%; and `runs-2`, `runs-3` and `runs-4` 0.8900, 0.9644 and 0.9519 against `runs`'s basis floor of 3.07%, and 0.8982, 0.9393 and 0.9480 against its HEAD floor of 3.40%. **`runs-5` is the one named shape where the prediction is not met**: 0.9903 and 0.9932, ahead but inside both floors. Where the body does not fire the time clause holds --- `runs-7` 0.9986 and 0.9957, `window-128x128-k7` 1.0179 and 1.0150, all inside --- and the count clause is exact on the four large-`sInner` main-set shapes these figures are read over, 1.0000 on both halves. **It is KILLED by its own count clause on `stretch-coprime-r7`**, whose `sInner` is 13 so the short body cannot fire, and where the instruction ratio reads **1.0105 on the basis and 1.0107 on HEAD** rather than 1.0000, with `alexnet-L1-55-c3-k11` at 1.0025 beside it; the time agrees, 1.0240 and 1.0234, the arm behind past both floors. So the short arm does what it was built to do and its dispatch costs a percent of the instructions on an inner run it cannot use, which is a smaller and more specific answer than the registration asked for.

(2) *The lean dispatch.* **HELD.** `lib-stage2-lean` reads at or below `lib-stage2` on every population of both halves that can be read at all --- 0.9695 on the main set and 0.9921, 0.9984, 0.9991, 0.9961, 0.9934, 0.9961, 0.9958 and 1.0007 on the basis's eight readable classes, `reshape1` excepted because `lib-stage2-lean` is degenerate there on both halves, and 0.9648 on HEAD's main set with 0.9827, 0.9962, 0.9979, 0.9922, 0.9994, 0.9946, 0.9957 and 0.9951 on its eight --- the single reading above 1 being `runs` on the basis at seven ten-thousandths against a 3.07% floor. On the four smallest main-set shapes it is ahead past both floors by large margins: **0.7711, 0.8468, 0.8624 and 0.9133** on the basis and 0.7875, 0.7934, 0.7981 and 0.9047 on HEAD, on `lenet-slice-c6-k5`, `cnn-slice-c32`, `cnn-L1-6x6-c1` and `cnn-L1-12x12-c1`. The kill wants a shape behind past the floor on BOTH halves and there is none: the basis has `stretch-primes` at 1.0168 past its 1.26%, HEAD has `stretch-inner256` at 1.0220 past its 2.11%, and neither shape is past the floor on the other half.

(3) *The composite.* **HELD**, and it is the arm this roster change was for. `lib-stage2-short-lean` reads at or below the better of its two parents on every population of both halves: against `lib-stage2-short` 0.9693 on the main set and 0.9863 to 1.0006 across the classes on the basis, 0.9718 and 0.9909 to 1.0042 on HEAD; against `lib-stage2-lean` 0.9182 and 0.8740 to 1.0179 on the basis, 0.9207 and 0.8847 to 1.0056 on HEAD. Every reading above 1 is inside its population's floor, the widest being `bcastmid` at 1.0179 against 2.80%. **What it inherits is each parent's win where that parent has one**: it takes `short`'s margin on `runs` and `rev` and `lean`'s on `bcastmid` and the small main-set shapes, and it leads three whole classes outright --- `bcast`, `slice` and `window` --- which no arm of this family did a run ago.

(4) *The straddlers.* **HELD**, and post-run step 0's `-g3` twins settle it by name rather than by count. Four self-loops straddle a cache line in `Main`-compiled code on each half, at the two body lengths Run 23's dead-spot half had --- 55 bytes at offset 42 and 53 bytes at offset 47 on the basis, 55 at 42 and 44 and 53 at 49 on HEAD. On the basis the twin names **all four** by byte identity, and they are exactly the four registered: `fillStage2Short` at 0x4205aa, `fillStage2` at 0x422b2a, `fbMutOdoVecdimsAddInLeafU2` at 0x429b6a and `fbMutOdoVecdimsAddInLeafU2Down` at 0x428b2f --- the branch's own fill, its short-body variant and the two leaf fills, every one of them the OUTER loop of a rotated pair. On HEAD the twin names two and refuses the other two, holding no byte-identical copy of them, which is the count check making a negative honest as Run 22's did on three of four. **No fill's inner loop straddles on either half**, there being four straddlers on each and all four accounted for on the half where the twin can speak, so the kill does not fire.

(5) *HEAD.* **HELD on its orderings, not on one of its figures, and one of its clauses could not be read at all.** No ordering in (1) to (3) reverses past HEAD's floor: (2) and (3) hold on the HEAD half exactly as on the basis, and (1)'s split is the same split on both halves, its kill firing on the same shape with the same count ratio. Of the standings it predicted within two points, `lib-stage2` against `lib-stage1` reads **0.9376** on HEAD's main set against a predicted 0.95, and **0.9929** on `slice` against a predicted 1.01 --- 1.2 and 1.7 points off, both inside the two the registration allowed. **The third is outside it and on both halves**: the shipped route was predicted about four percent over the bare fill and reads **1.0640** on the basis and **1.0702** on HEAD, against Run 23's 1.0389 and 1.0430. Since both halves moved together the two-and-a-half points are the roster's and not the compiler's, which is what a prediction quoting a previous run's magnitude across a roster change buys. **And the remaining clause is unreadable**: it predicts `-u2` ahead of `-down` in every population, and the arm that comparison turns on, `mut-odo-vecdims-add-in-leaf-down`, was parked to `Only` by the same commit the registration was written beside, so no process this run times it. The pair that IS still timed, `-u2` against `-u2-down`, is a tie in every population on both halves --- 0.9927 to 1.0264 on the basis and 0.9958 to 1.0034 on HEAD, every one inside its population's floor but `reshape1` on the basis, whose 1.0264 is half a point past that class's 2.17% --- and it was a tie on Run 23's dead-spot half too, 0.9928 to 1.0283, so what can be read reproduces and what was registered cannot be.

(6) *The threshold.* **HELD**, and it is the first registration here that a dispatch arm has cleared. `lib-stage2-disp`, re-cut from 256 to 2048 by task 9's probe, reads at or below the better of `lib-stage2` and `lib-stage2-concat` at every one of the fourteen `runs` lengths on both halves, within that class's floor of 3.07% and 3.40%. Against `lib-stage2` it runs **0.8705 to 1.0015** on the basis and 0.8696 to 1.0181 on HEAD, every reading above 1 inside the floor and the wins concentrated exactly where the new threshold sends work to the slice route --- 0.8705, 0.8919 and 0.8953 at `runs-16384`, `runs-65536` and `runs-4096` on the basis. Against `lib-stage2-concat` it is ahead by a factor at short lengths, 0.0207 at `runs-2`, and behind by 1.9% at `runs-65536`, inside the floor. The arm leads the whole `runs` class at 0.027 against `mut-odo-vecdims`'s 0.032, a 22.87% margin, where Run 23 read the dispatch killed at `runs-1024` on both halves: so the threshold was the defect and the cut fixed it.
