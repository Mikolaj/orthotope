# Run 18 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4 / SpecConstr, max-skip +lookrts, -A32m, 9.14.1)

**A back-filled record and not a write-up.** It carries this run's published
per-strategy geomeans against `list` and nothing else. What the run measured,
which half published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr, max-skip +lookrts, -A32m, 9.12.4 | SpecConstr, max-skip +lookrts, -A32m, 9.14.1 |
|---|---:|---:|
| `mut-odo-vecdims` | 0.055 | 0.055 |
| `mut-flat-gm` | 0.084 | 0.083 |
| `bq-mut-runs-gm-mulback` | 0.089 | 0.091 |
| `bq-odo-gm-mulback` | 0.100 | 0.100 |
| `bq-scan-rem-gm-mulback` | 0.096 | 0.098 |
| `bq-expand` | 0.115 | 0.117 |
| `build` | 0.103 | 0.102 |
| `offtab` | 0.134 | 0.143 |


## What this run was built to answer, and what it answered

Its pair was `run18-g912`, the basis, against `run18-g914`, settled 2026-08-21
and run 2026-08-23: GHC 9.14.1 against 9.12.4, on one source carrying
`-fobject-determinism`, the per-sample instrument and a saturating preamble.
Five registrations. **Three held, one broke narrowly and one failed
to the machine rather than to the pair.** The basis is Run 17's basis recipe
over `saturate-preamble.patch` (applied after `wildlog-instrument.patch`, whose
`lookupEnv` it uses); the other half is the same source and shim on 9.14.1
through `cabal.project.ghc914`, whose freeze resolves the same `vector`,
`criterion` and `criterion-measurement` versions at the one index-state,
so the halves differ in the compiler and its boot libraries and in nothing
a freeze can see --- which prices the consumer's 9.14 build, library code
recompiled included, and is to be read as such. The preamble is the state made
an input: `SATURATE=<dose>` sprays dose x 1.15M short-lived pinned buffers
of 2304 B before criterion sees the roster, collects, and prints one
`@@saturate` line carrying a fixed-iteration reading of `vgg-14-c512-k3/list`
and the heap peak; on for every recorded process and every probe read against
a recorded cell, off for the clean alone legs, skipped by `check`, `diag`
and `--list`. **Its non-vacuity and its dose are measured, on a quiet machine**
(2026-08-22, `sat-probe`, the basis recipe's binary, loadavg under 1; a first
evening's figures at loadavg 1.5 to 2.0 had read +31% and scattered,
and were the load). `vgg-14-c512-k3/list` alone reads 16.6 to 16.8 ms clean;
after the reproducer's pure pinned burst 18.2 to 18.7 at dose 1 and 18.0 to 18.3
at dose 2, +9 to +11%; after the roster's own sprayer --- `cnn-slice-c32/list`'s
fill for a fixed million iterations, each a 288-cell cons list and a 2304 B
pinned result, both formation routes at once --- 19.1 to 19.3 at dose 1 and 19.2
at dose 2, +14 to +15%; and with that sprayer run as a criterion bench ahead
of the victim in one process, no preamble, 18.6 to 19.0, where Run 16's roster
cell read 18.45 against its alone leg's 16.38. So the plateau holds for both
doses, dose zero is the clean level, and on that shape the roster's own sprayer
reproduces the roster's state where the pure burst falls some three points short
--- which is why `SATURATE_BY` defaults to `list` and keeps `spray`
as the control. The 9.14 binary reads the same, 19.04 against 16.96. **Over five
more shapes the picture is flatter** (`probe-decomp-dryrun.log`, the same binary
and evening): the `list` dose lifts `list` by 12 to 16% and the `spray` dose
by 10 to 14.5%, against Run 16's roster-over-alone-leg deflations of 9 to 13.5%
on the same shapes, so both doses land in the roster's band within a few points,
the `list` dose erring about two points high on average and the `spray` dose
about half a point low, with the sign varying by shape --- `stretch-inner256`'s
roster cell sits five points under both. The default stands, both routes being
in it, and what changes is how registration 3 reads: the rest is a few points
of either sign and not a constant. Registrations, each with what kills it: (1)
*the bridge*, the 9.12 basis against `run17-wildlog` across the preamble's
source change, every arm inside the drift band and the fills where Run 17 held
them, killed by an arm outside it --- **but the placement-exposed arms
are outside that condition and were put there 2026-08-22, on Run 17's own
measurement**: this is a `.text`-changing comparison and by a long way, the two
source changes between the halves adding **24576 bytes** to `run17-wildlog`'s
20381893 --- 12288 for the preamble and 12288 again for the load fields, three
pages each, measured at 20394181 and 20406469 --- where the instrument patch Run
17 priced added 4096, and 4096 was worth up to 8% on `gen-unsafe`,
`gen-quotrem`, `build`, `mut-odo`, `offtab` and `bq-mut` with no strategy
changed. Six times that shift is what the bridge is read across. So a movement
on those six families is layout and kills nothing; the other arms are what
the registration is over --- **less one more, `bq-expand-zf`, exempted
2026-08-22 on a measurement taken because it could not be taken afterwards.**
Two builds of the basis recipe either side of the load fields, differing
in nothing else, put the tracked fills at `[0, 24, 0, 4]` and `[0, 0]` on both,
every copy fitting --- so the fields do not move the fills, which
is the question Run 18 had to ask --- but the second carries **one straddling
loop where the first carries none**, 38 bytes at offset 32, and a `-g3` twin
names it `fbBQexpandZF`, which is `bq-expand-zf` and a timed arm rather
than the instrument's own code. Run 17's basis straddled nowhere, so Run 18's
basis carries a straddle its predecessor had not, on an arm [Run 10 priced
a straddle at 12 to 14%](#what-moves-a-figure-when-no-strategy-changed).
It is in BOTH halves, one source building them, so the compiler registration
is untouched and only the bridge sees it. **Not chased, and the ruling
is this README's own**: layout is not hand-tuned here, which is what the shim
is for --- moving the new functions about the module until the straddle lands
elsewhere is a lottery the next source change re-rolls, no claim rests
on `bq-expand-zf`, whose series closed at Run 13, and raising the shim's skip
budget would be a regime change that confounds the compiler. **And it is a weak
answer to the pinning claim rather than the strong one [the floor section asks
for](../README.md#what-moves-a-figure-when-no-strategy-changed)**: all six
tracked copies moved by 3200 bytes, a whole multiple of 64, so nothing forced
the shim to re-pin anything. **And the fills half of it is already answered
and answers nothing**: `sat-probe` read `[0, 24, 0, 4]` and `[0, 0]`, Run 17's
exactly, so that clause is measured rather than predicted --- and Run 17's
twelve arms moved while its own two halves' fills were identical, which is why
a fill match is not evidence the arms held still; (2) *the compiler*,
the registered orderings holding on 9.14.1, killed by a BROKE that clears
that half's floor --- a margin moving is the finding and not a break, as claim
4's history says --- with claim 7's allocation levels read per compiler,
a compiler being able to change allocation where a slot cannot. **Which
orderings, read off `--claims` and not off this sentence, which was written
before Run 17 ran and said thirteen**: Run 17 broke two of that thirteen ---
claim 4's second half, now twice running, and claim 9's first --- and *restated*
claim 4, so what Run 18 inherits is an ordering where the manifest had a tie.
Re-read the count and the content out of the manifest before the evening; (3)
*the decomposition*, every shape's `list` alone leg twice on the basis, `SAT=`
off and on through `run-alonelegs.sh`, against its roster cell: the state
is saturated minus clean and the rest is roster minus saturated. The dry run
over six shapes puts the rest between -1.4 and +5 points with no constant sign,
so the registration is the distribution over the 24 shapes and not a cell:
its median inside the floor, its tails named and read per shape, a median past
the floor naming what the state is not, criterion's own interleaving between
samples the first suspect. The `spray` dose's legs, a third column if the budget
allows, price the burst route's share, some ten of the thirteen points
on `vgg-14-c512-k3` and within two points of the `list` dose elsewhere.
The alone legs themselves are sound: ten processes of `cifar-L2-16-c64-k3/list`
land within 0.9%, so `list` is immune to the per-process placement term
that unreads `offtab` and `build`; (4) *counted work*, `run-counts.sh` on both
halves, instructions an iteration for every arm and shape from two fixed-`-n`
processes a cell --- not for the orderings, which the pilot on Run 16 refused
it (the TODO list's ruling), but per arm the count ratio 9.14/9.12 beside
the time ratio: time moving with counts is codegen, time moving without counts
is the runtime or memory, layout being pinned --- a compiler's codegen term
and runtime term separated for the first time; (5) *the plateau*, every recorded
process's `@@saturate` victim reading inside a band of the run's own, a process
outside it read before its figures are. **What is built**:
`saturate-preamble.patch`, with its two doses, proved to build and to fire
on both compilers; `sat-probe` and `sat-probe-914`, its binaries
for the between-run probes, deleted after their read-backs and rebuilt
from `run18-pair.txt`'s recipes when wanted; `cabal.project.ghc914`
and its freeze; `run-counts.sh`, proved on one cell (`vgg-14-c512-k3/list`
260.6M instructions an iteration, `mut-odo` 54.4M, `sum-only-early` 8.1M, `N` =
5); the `SAT=` mode of `run-alonelegs.sh`, which refuses a binary without
the preamble. **Both patches landed in `Main.hs` by commit on 2026-08-22**, Run
17's pair being spent, so every recipe lost its apply step and each patch file
stays as the record of what it was as one diff, refusing a second application
in its own header. **The one pre-run risk is retired**: the shim reads back
on 9.14's assembly --- `sat-probe-914`, the other half's recipe, has 113
self-loops in `Main`-compiled code, 61 at offset 0 and none straddling, the 9.12
probe 110, 56 and none, the tracked 28 B groups reading `[0, 24, 0, 0]`
and `[0, 0]` against `[0, 24, 0, 4]` and `[0, 0]`; its `--list` and its `check`
output are byte-identical to the 9.12 probe's, and the preamble fires there
alike. One trap for the read-back: on 9.14 the baked RTS line is stored
with a byte before it, so `strings | grep -x` misses it while `+RTS --info`
reports it and the heap peak shows it in effect --- the notes
and `run-alonelegs.sh` read it by `--info` now. **What was owed before
the evening was taken 2026-08-22, before any build, and only the `-g3` twins per
compiler are left, which belong at the write-up.** The stamp carries its load
fields: the `@@wild` line gains `load=` (the 1-minute average
from `/proc/loadavg`), `run=` (that line's instantaneous count of runnable
tasks) and `cpu=` (the machine-wide busy jiffies from `/proc/stat`'s first line,
in USER_HZ, which the kernel fixes at 100 whatever it ticks at), read
in the same hooks outside the timed block; `./read-run.py --wild LOG`
differences a bench's `pre` and `post` stamps and prints the CPU something else
consumed during its samples, the `cpu` delta less the process's own
mutator-plus-collector delta the line already carries. The reason is the wild
cell: from inside a process its signature --- a non-reproducing mutator step
at flat RTS totals --- is exactly an external intrusion's, and Run 16's updater
cell was told apart only by a wall-clock window; these fields tell the two
apart, foreign CPU during a bench's samples being the updater class and none
the machine's own. The 1-minute average alone dates a multi-minute intruder
and barely marks a ten-second one (it is damped over 60 s and updated every 5
s), which is why the other two ride with it. Stamped per sample with the rest
of the line and *reported* per bench, /proc/stat's 10 ms jiffy saying nothing
inside one short sample. The plateau is counted per process in `run-major.sh`,
exactly as bench counts are, and banded across them in `read-all.sh`, at 5% ---
loose against the 0.9% ten alone-leg processes span, tight against the 14%
an unsaturated process reads below a saturated one --- with `check-scripts.py`
cases behind all of it, controls among them; and `run-alonelegs.sh`
and `run-counts.sh` have cases now, each written against a defect it turned out
to have. **Not in Run 18**: a roster change, which would confound the compiler.
The 24m/48m probe, which could have reopened the area, was taken ahead of Run 17
and killed. And the `add-in` placement question, deferred by [its own
entry](../README.md#what-is-open) to a run that has the compilers measured.

**THE VERDICTS, 2026-08-23.** (1) *The bridge*: **BROKEN, and narrowly.** Read
as it has to be on this run --- per shape as a ratio to `list`, because the box
moved 4.8% between the two runs and `--compare` across runs reads absolutes,
so its own output puts `list` at +5.52% and every arm with it --- the 26 arms
the registration covers give a geomean of 0.9867 with **two outside the 3.3%
drift band**: `bq-gen` at 0.9545 and `bq-mut-runs-gm-mulback` at 0.9639.
The kill condition was an arm outside the band, and two are. `mut-odo-vecdims`
reads 1.0062, `mut-flat-gm` 1.0022, `bq-scan-rem-gm-mulback` 0.9825
and `bq-expand` 0.9803, so the arms the claims rest on are inside it
and the break is at the edges of the roster. The exempted placement-exposed
families run 0.9333 to 1.0216, which is why they are exempted. (2)
*The compiler*: **HELD, and it is the run's headline.** All thirteen registered
orderings hold on 9.14.1 and all thirteen on 9.12.4, no BROKE on either half,
and claim 7's allocation reads per compiler at 1072 of 1080 cells agreeing
to 1e-4. (3) *The decomposition*: **HELD.** The total in-process deflation
is +12.76% on the basis and +12.53% on the control, and the preamble splits it:
the **state** is +11.43% and the **rest** the roster adds on top is **+1.20%**,
whose median sits inside this run's 1.36% floor, which is what the registration
asked. Twenty of the 24 shapes put the rest above 1 and the tails are named ---
0.9905 on `stretch-bigstride` and **1.1004** on `stretch-tall-Mx2`, the one
shape where the roster adds ten points beyond the saturated state.
So the preamble reproduces the roster's state to within the floor and the dose
is right. (4) *Counted work*: **DELIVERED, and it separates the two terms
for the first time.** Instructions an iteration on both halves, over 42 arms,
split the roster cleanly in two. The `bq-expand` family moves in counts and time
**together** --- counts 0.9889 and time 0.9884 on `bq-expand` itself,
with its twins, `-b`, `-qr-prim`, `-zf` and `-gm-mulback` all at counts 0.988
to 0.991 --- and `mut-odo-vecdims-add-both-down` likewise at counts 1.0278
against time 1.0361. That is codegen, and it is the whole of the codegen
this pair found. The arms with the **largest** time differences move at count
ratios of **1.0000**: `bq-gen` +9.26% in time, `offtab` -5.76%, `gen-unsafe`
-6.29% and `gen-quotrem` -3.14%, every one of them emitting the same number
of instructions on both compilers to four decimal places. Time without counts
is the runtime or memory rather than the code, and the correlation of the log
ratios over all 42 arms is 0.213, weak as the Run 16 pilot found.
**So the placement-exposed family's seven percent is not 9.14 emitting different
code for it**, which is the sharpest thing this instrument has said and
is a second, independent line on the same conclusion the `-g3` twins reach. (5)
*The plateau*: **FAILED, and the failure is the machine rather than the pair.**
The eighteen processes read the preamble's victim from 20.0411 to 21.7604 ms
an iteration, an 8.58% spread against the 5% band `read-all.sh` gates at.
The nine that ran before 10:52 span 20.04 to 20.38 --- **1.7%**, well inside
the band --- and every reading above 21 belongs to a process that started after
it, `g912-reshape1` at 21.76 and `g914-slice` at 21.73 leading them. So the gate
is reading the intrusion it was built to notice, the band is the right band,
and what a future run should not conclude from this is that the preamble
is unstable.
