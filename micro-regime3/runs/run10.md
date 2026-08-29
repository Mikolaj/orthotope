# Run 10 (SpecConstr / SpecConstr, aligned)

**A back-filled record, and one section that is this run's own.** It carries
this run's published per-strategy geomeans against `list`, and below them
the five alignment registrations it made and how each was decided, moved here
from README's open list on 2026-08-29. What the run measured, which half
published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr | SpecConstr, aligned |
|---|---:|---:|
| `mut-odo-vecdims` | 0.048 | 0.049 |
| `mut-flat-gm` | 0.083 | 0.081 |
| `bq-mut-runs-gm-mulback` | 0.085 | 0.088 |
| `bq-odo-gm-mulback` | 0.090 | 0.090 |
| `bq-scan-rem-gm-mulback` | 0.090 | 0.089 |
| `bq-expand` | 0.102 | 0.102 |
| `build` | 0.110 | 0.096 |
| `offtab` | 0.123 | 0.124 |


## The five alignment registrations, and how each was decided

The run's roster order was chosen for heap state --- `sum-only-early` above
`list`, so nothing is measured on an ungrown pool --- and the layout it happens
to give was then read off the binary rather than shopped for, which
is the distinction that keeps the run from being confirmatory. **Run 10 is now
two binaries rather than one**, differing only in the assembler shim, so each
prediction below says which half it is read on and the last two exist only
because there are two ([the run's
plan](../README.md#making-a-major-benchmark-run) has why, and the build
and check sequence). Against Run 9's offsets, both of the straddle hypothesis's
arms move, in opposite directions:

1. **The FastReshape three go straddling to resident** (mod 40, 44, 44 to mod 0,
   36, 36) while their control stays resident (24 to 16). The hypothesis
   predicts 1.1552, 1.1795 and 1.1645 collapse toward 1.00. If they hold near
   1.16, the hypothesis is dead and [the suspension of those axis
   figures](#the-mutable-ceiling-taken) is withdrawn --- which is the outcome
   this README has the most reason to want detectable, the suspension being
   its own. **Sharpened by the pad probe**, which prices each offset instead
   of each side of the boundary: their present values are what a deep straddle
   over a resident control predicts, 1.18, and after the move all four copies
   sit resident, where the probe's own resident offsets span 0.904 to 0.956.
   So the collapse should be to between 1.00 and 1.05, and anything near 1.16
   still kills it. Do not interpolate the 36 across the boundary --- the penalty
   steps between 36 and 37 rather than ramping. **Read on the unaligned half**,
   which is the half these offsets belong to; on the aligned half all four
   copies sit at 0, so the same three ratios must read 1.00 outright,
   and that is the stronger form of the same test --- a 1.16 surviving alignment
   would kill the hypothesis where a 1.05 could still be argued.
2. **`mut-odo` goes resident to straddling** (29 to 53) while `build` stays
   straddling (53 to 45). The hypothesis predicts their 1.13 closes toward 1.0,
   and **the pad probe makes that a point prediction, 0.998**: two deep
   straddles, whose penalties cancel, so the pair should land on 1.0 rather
   than merely approach it. The same penalties reproduce Run 9's own 1.13,
   at 1.144. If it holds or widens, the hypothesis is dead by the other route.
   **Read on both halves, and it is the weaker of the two arms precisely because
   they agree**: the unaligned half predicts 1.00 because 45 and 53 happen
   to carry near-equal penalties, and the aligned half predicts 1.00
   by construction, so the two halves cannot disagree here and the pair's own
   value is not what makes this run worth two binaries. Prediction 1
   and prediction 4 are.
3. **The anchors move, and one of them is a control.** Warming `list`
   is the object of the swap, so the absolute anchors should fall and every
   ratio rise with them --- but not uniformly, and the excess-allocation rule
   says which. Ten of the eleven anchor cells carry 27 to 336 MB of excess
   and should move; `cnn-slice-c32`, at 0.05 MB, sits under the nursery
   and should hold, which makes it a control inside the anchor table.
   If it moves too, what warming does is not the nursery; if the other ten do
   not, warming does not reach the baseline and the swap bought nothing.
   And a fall shared by all nine populations is one effect rather than nine
   findings, so read the anchors together before reading any class paragraph.
   **Read on the aligned half alone.** Warming is heap state and not layout,
   `list` carries no layout term worth the name, so the anchors read the same
   on both halves and reading them twice would enter one effect as two findings.
   That last step is prediction 5's to establish, not this one's to assume: read
   5 first, and if `list` does move between the halves then this prediction has
   no fixed anchor to be read against and waits. The nine populations' anchors
   are commensurable as printed, the fingerprint this run publishes being
   the aligned one and the eight class blocks aligned with it,
   so the reading-together above can be done off the run's file. That
   is a ruling and not a coincidence: had the unaligned fingerprint
   been the published one, exactly one of the nine would have crossed a basis,
   and the run's plan says why it is not.
4. **The two halves differ, and for six arms by how much is registered here.**
   This is what the second binary is for. It was to have been a per-arm
   prediction over the whole roster, and **that is not available**: attributing
   a loop to an arm needs source information, every build that carries
   it relocates the code, and no bridge survives. `-g3` moves the fills
   from `[3, 53, 59, 45]` to `[8, 56, 4, 4]`; `-finfo-table-map` dissolves
   the groups altogether; matching the two builds by loop order fails
   at the first loop, and only 30 of 957 release loops have a body unique enough
   in both to match by bytes. The release binary keeps four `zdwgo7` symbols
   where the debug build has 47 and carries 98 `Main` symbols in all, none named
   for an arm, so its own symbol table cannot do it either --- and `NOINLINE`,
   the obvious fix, is already on these arms: adding it a second time
   is a compile error and the symbols are absent regardless, GHC emitting
   the module's code under a handful of workers. Measured 2026-08-10,
   and recorded so the routes are not retried.

   What *did* work is the case-by-case form, and it is why six arms can
   be registered at all: take a loop's bytes from a `-g3` build, where
   `addr2line` names the `Main.hs` line and so the arm, then find the same bytes
   in the release binary. It succeeds when a loop is distinctive and fails when
   it is not --- the 30-of-957 figure is the wholesale version of this,
   and a loop shared by two arms is ambiguous by construction, which for `build`
   and `mut-odo` is the very fact being measured. So attribution is available
   one arm at a time, at the price of a second build and a hand check,
   and is not available as a sweep.

   **What is registrable is the six arms whose loops this README has already
   identified, read off `micro-unaligned` with `loop-offsets.py`**: the fills
   sit at `[3, 53, 59, 45]` and `[16, 0, 36, 36]`, and all eight copies go
   to offset 0 in `micro-aligned`. So **`build` and `mut-odo` should each run
   about 0.85 of their unaligned selves** --- from 45 and 53, both deep
   straddles at about 1.10, to the resident level near 0.93 --- while their
   *ratio* stays at 1.00, which is what makes this a different measurement
   from prediction 2 rather than a restatement of it. The four `mut-odo-vecdims`
   arms are resident already, at 16, 0, 36 and 36, so they should move by a few
   percent at most, and the three ratios by less. An arm here that moves
   the wrong way, or the pair moving apart, is a finding.

   **For the rest of the roster the prediction is aggregate and weaker, and says
   so**: the moves falling in two groups rather than smeared, and the count
   that can move bounded by the short loops the shim rescues --- 50
   of `micro-unaligned`'s 115 straddle where none of `micro-aligned`'s do, so 50
   loop heads' worth of penalty is removed and how many arms that touches
   is exactly what the run finds out. An arm reading *slower* aligned is
   not by itself a refutation: the padding is NOPs, and an arm that falls
   through into an aligned head executes them every time it does, so a small
   loss where no loop was straddling is the shim's own cost and not evidence
   against the penalty.
5. **`list` does not move between the halves**, which is the pairing's control
   and the one result that would invalidate the rest. It is the insusceptible
   arm, 0.5% across four rebuilds, so alignment should leave it alone;
   if it moves, the baseline may have been carrying layout too, every published
   ratio in this README divided by a moving denominator, and that is a larger
   finding than anything the run was built to get. *May*, because `list`'s hot
   loop is **library code and not Main's**: `fbList` is one line
   over `VS.fromListN` and `toListT`, and no loop in a `-g3` build resolves
   to its source lines, so the shim cannot align it and only the phase-matching
   keeps it still. Its expected stillness therefore rests on measurement
   and not on mechanism --- 0.5% across four rebuilds, which rerolled
   the libraries too --- which is weaker ground than the six arms stand
   on and worth saying before the number is read.

   **Three things rest on this one, and no other prediction here carries more
   than itself** --- which is why it is read first and why a failure is not one
   prediction lost but the run's arrangement to reconsider. Prediction 3 has
   no fixed anchor without it and says so. Run 10's mixed basis, its main table
   unaligned and its eight class blocks aligned, is tolerable only while the two
   halves' baselines agree. And the transition to Run 11 turns on Run 11's
   second column succeeding Run 10's unaligned table, which a moving denominator
   would put in doubt as well. The gate below already reads it on every shape
   and at the ordinary budget, so what the run adds is not coverage but company:
   `list` there shares a process with 33 other arms instead of four, and heap
   state and code position are exactly what this README has measured moving
   a figure when no strategy changed. That is the reading all three wait on.

**The gate has been run and the three testable predictions hold** (2026-08-10,
five benches over the 24 shapes, two passes per half in the order unaligned,
aligned, aligned, unaligned, so both binaries carry the same mean position).
Prediction 4: `build` reads **0.8836** of its unaligned self and `mut-odo`
**0.8778**, so alignment is worth **12%** to each and the two agree to 0.7%,
which is what one worker in two places should do. Prediction 5: `list` moves
**0.3%**, so the baseline is still, the denominator holds, and the library
reroll does not reach the one arm whose loop is library code ---
the phase-matching earning its keep. Prediction 2: the pair reads 0.9754
and 0.9805 unaligned, 0.9610 and 1.0082 aligned, nowhere near the 1.13 or 0.86
earlier runs saw. Run 10 is worth its evening on this; what a gate of five
benches and two passes cannot say is anything about the rest of the roster.

**Two corrections come with it.** The registered 1.00 for prediction 2 was too
strong: the pair sits at ~0.98 on both halves, where the pad probe's own
both-resident binaries sat, so the arms' intrinsic ratio is **0.98 rather
than the 0.9973** [the floor section][floor] carries --- an estimate
that assumed the two arms share one penalty curve, which their 5.9% disagreement
at offset 13 already contradicted. It costs the arms nothing, since they share
a worker but not a call path, `build` being `mut-odo` driven through `vBuildVS`.
And **offset 0 is measured for the first time**: the probe's eight offsets
were all congruent to 5 mod 8, so the 0.85 predicted here was an extrapolation
from the resident mean, and the gain at 0 is 12% rather than the 15.6%
that implied.

**The gain is not a constant, which prediction 4's aggregate form should say.**
Read shape by shape it runs 0.719 to 1.031 for `build` and 0.763 to 1.033
for `mut-odo` --- 28% at the best shape and a slight loss at the worst ---
against a per-shape noise floor this gate puts at 6.3%, that being the median
disagreement between the two arms' own gains where identical code says they
should agree. So the extremes are real and the middle is not resolvable on two
passes: the 12% is a geomean over a structured distribution and not a factor
every arm pays. **Asked over 24 shapes and answered, so it retires**
(2026-08-14, arithmetic over Run 10's two kept main sets, no machine time).
The gain spans 0.773 to 1.025 on `build` and 0.697 to 1.018 on `mut-odo`,
at geomeans 0.877 and 0.863, while the arms whose loops did not straddle sit
flat --- `list` 1.006, `mut-odo-vecdims` 1.007, `bq-expand` 1.002 --- which
is the instrument saying it works. Against the four variables this entry named,
the Spearman of log gain reaches |0.38| at most, and the two largest, `mut-odo`
against `l` at -0.36 and against `m` at -0.38, fall to -0.04 and -0.02
on `build`, which no size law could do. The two shapes showing no gain at all,
`stretch-pow2stride` at 1.007 and `stretch-square-1341` at 1.025, are mid-range
in every dimension. So the 12% is a geomean over an unordered distribution:
there is no shape ordering to find, and the question is closed rather
than parked.

**The correction term moves too, by 0.6%.** Both `sum-only` halves read 0.9939
and 0.9938 aligned over unaligned, agreeing to a digit over a range of 0.990
to 0.998, so the forcing pass is itself slightly faster in the aligned build ---
its own loop presumably being among the fifty the shim rescues. It is subtracted
from every figure, so it is not a term that cancels between the halves; at 0.6%
of a fraction of each cell it cannot reach the 12%, but a later reading
that needs the halves to share a correction should know they do not quite.
Allocation, by contrast, is identical to 2.5e-6.

**The gate read the aligned half as the noisier one and the full budget says
it is not.** Over the gate's five benches its median CI% was 0.532 against
the unaligned half's 0.218, and its two passes disagreed more (`mut-odo`
at 1.0224 against 0.9859), which left open whether alignment widens the per-cell
interval structurally. Over Run 10's 816 cells a side the two halves
are indistinguishable: median CI% **0.138 against 0.134**, median R^2 0.99997
on both, and the aligned cell is the wider one 389 times of 816. So the widening
was the gate's own sample size, and alignment removes a systematic term
at no cost in precision. That closes the question the gate raised, which is what
the full budget was wanted for.

The first two were arms of one prediction, either of which could kill it,
on arms already rostered and at no extra machine time; the third priced what
the order change was for and carried its own control; the fourth is why the run
was two binaries and the fifth is what made the fourth readable. The pad probe
having answered the hypothesis first, the first two were replications carrying
point predictions rather than the evidence --- which is what that probe's window
was spent to buy, and why the run's own weight sat on 4.


## The queue of experiments this run was ordered against

**The queue of experiments that want a quiet machine**, ranked, so that the next
quiet window is not spent deciding what to spend it on. Written down 2026-08-09
with Run 9's artifacts still alive, and the ranking turns on one thing worth
stating: *the binary must not be rebuilt between the arms of a comparison*,
since a rebuild is worth up to 18% on a susceptible arm and swamps most of what
is being asked.

**Ordered against Run 10 rather than by value, 2026-08-10, now that its regime
and roster are fixed.** One entry goes before it and the rest after,
and the reasons are the schedule rather than the ranking: an experiment whose
answer changes how Run 10 is *read* is worth its window first, while one Run 10
supplies half of for nothing is worth waiting for. Durations below
are quiet-machine costs, derived from the elapsed time and bench count a run's
own provenance line reports --- about five seconds a bench-shape cell, criterion
spending its budget whether the call is fast or slow --- and nothing here
measures what contention does to them. **The gate entry below has since
been folded into Run 10 rather than queued behind it**, alignment having turned
out to be the thing that decides whether the rest of the queue is measuring
anything; what stays there is the cheap gate that runs before the run does.
Entries are referred to by name and not by number, two having been removed
from under a reference already. **Nothing below is outstanding**: each has
been run or closed, and what the list holds now is what each bought
and the ordering rule above, which is what a later queue would be built on.
1. **The pad probe done properly --- run 2026-08-10, and the hypothesis
   survives.** Eight binaries differing only in inert pad arms, two interleaved
   passes over all eight, 2h12m, with `build` and `mut-odo` both timed this time
   (the first attempt lost them to a shell glob) and each stepped through all
   eight 8-byte offsets --- the step being all GHC aligns the loop to ---
   with membership fixed throughout. A straddled copy costs 1.19, or 1.10 where
   only three bytes precede the boundary, and the two discriminating binaries
   invert as predicted: [the floor
   section](../README.md#what-moves-a-figure-when-no-strategy-changed) carries
   the verdict, the graded penalty and the controls. Placement and the allocator
   are separate effects, which is why this wanted a window of its own rather
   than being shrunk by 1: the `build`/`mut-odo` gap was measured across
   the nursery change and did not move.

   **Two pad designs relocate nothing, so they are not retried** --- measured
   on 2026-08-10 rather than reasoned about, and recorded here because
   the directory that first held them is to be deleted. Module-level inert pads
   that nothing rosters left both arms exactly where they were, across six
   variants. So did permuting two untimed roster entries deep in the list, which
   relocates only each other. What works is a pad rostered *before* the arm
   it must displace, emission order tracking first reference from `roster`;
   a pad kept inert by rostering it `Only` is checked on every shape and timed
   on none, so the selection stays what it was. Nothing else in that file
   was load-bearing, which was checked before deleting it: its shell-glob trap,
   its rule about counting what a filtered run selected and its correction
   caveat were already in [the reader](../README.md#the-reader-read-runpy)
   and [the procedure](#making-a-major-benchmark-run), and what went with
   it was a per-binary offset map for binaries that are themselves gone.

   **It went before Run 10, which makes Run 10 a replication rather
   than the evidence** --- the point of that ordering, two of Run 10's
   registered predictions being the straddle hypothesis, and Run 10 testing
   it while moving roster order, heap warmth and code layout together where
   these binaries moved one thing and held the rest. It did more than replicate,
   in the end: answering the hypothesis is what turned Run 10 from one binary
   into two, since an effect this size is worth removing once it is no longer
   in doubt. The asymmetric risk it was run against did not materialise: [the
   floor section](../README.md#what-moves-a-figure-when-no-strategy-changed)'s
   loop table and [the suspension of two FastReshape axis
   figures](../README.md#the-mutable-ceiling-taken) both rested on a correlation
   inside one binary, and both stand, the suspension now with an out-of-sample
   check of its own. The binaries and the sixteen run files were untracked
   in `pad-probe/`, ~280 MB, and are deleted: this README carries what they
   showed, and the effect has a self-contained public reproducer in the filed
   issue.
2. **A third `-nosum` arm, on a flat fill** --- the one probe that separates
   *the read is biased* from *those two arms are*. Landed as `mut-flat-gm-nosum`
   (2026-08-13) after waiting out two runs, membership having had to stay pinned
   through Run 11's repetition and unconfounded with Run 12's change of shim;
   its readings are with gate 3 and the roster entry. Two things
   from its scheduling outlive it. **The run's question goes in the second
   half**: Run 10 paired against an unaligned build and priced layout, Run 11
   against max-skip and priced the padding, Run 12 against `-fproc-alignment=64`
   and priced the flag --- the new variable rides the control half and the basis
   stays comparable. And **`micro-both` was the obvious candidate for Run 12's
   pair and the wrong one**: it carries the *unconditional* shim with the flag
   because it was built hours before the max-skip form existed --- a composition
   that is chronology and not design, and a name that invites being read
   as design. Nor can such a pair separate the flag from the offsets
   it produces, pinning procedures being *how* it works; the resident offset's
   own price stays a probe on the pad-probe model.
3. **The five-bench gate before Run 10's aligned half --- run 2026-08-10
   and it passes**, its verdicts and two corrections being in [Run 10's
   file](runs/run10.md) with the predictions above. Kept because a later paired
   run wants the same gate before its own evening:

       ./run-gate.sh $R     # the two-process form this entry used to spell
                            # out is superseded: the script runs four, in a
                            # palindrome, and names its files
                            # $R-gate-<half>-<pass>.json -- the unprefixed
                            # form it used once silently overwrote Run 10's
                            # two aligned gate files

   run against `micro-unaligned` too, and expect 120 `benchmarking` lines each,
   then `--compare` one against the other, which is the reader's mode for an arm
   across two runs of one population and what [Run 10's prediction
   4](runs/run10.md) is read with. `*/list` is in it for two reasons: it gives
   prediction 5 an early reading, and without a baseline `--selftest` has
   no ratios to check. With both executed copies resident at 0,
   `build`/`mut-odo` must read **1.00** and both arms must run at the resident
   level, which against Run 9's placement is 10 to 19% faster rather than merely
   equal. A pair that reads 1.00 while neither arm moves would refute
   the penalty while confirming the symmetry, and that is a distinction no run
   so far can draw. Minutes, and it is the cheapest place to find out
   that the aligned binary is wrong before an hour of main set is spent on it.
   The dear half of this entry --- a main set aligned against one unaligned ---
   is no longer a queue item at all: it *is* Run 10, whose fourth prediction
   is that comparison read arm by arm.
And three things **not** worth a quiet window, recorded so they are not reached
for. The *how many preceding benches warm it* sweep, which the nursery finding
supersedes --- the bench count is the symptom and the allocation area
is the cause. The element-type re-probe, whose trigger is a run that moves
the ordering at `Storable Double`, which Run 9 does only through layout
and membership rather than anything an element type would feel. And **an A/B
of the pre-swap binary against the post-swap one, to price the roster swap
on its own** --- proposed and refuted the same day: that swap moved heap warmth
*and* relocated every worker by ~40 KB, so binary against binary conflates
exactly the two things Run 10's unaligned half conflates, and buys a number Run
10 supplies anyway at the price of a quiet hour and a false sense that one
variable had been pinned. **Half of that refutation has since expired
and the other half has not.** In an aligned build a roster swap relocates
no loop, so such a pairing would no longer conflate the two --- but it would
still buy a number Run 10's third prediction supplies for nothing, which
was always the stronger of the two reasons. Recorded because the expiry
of a premise is exactly what makes a dead idea look alive again.
