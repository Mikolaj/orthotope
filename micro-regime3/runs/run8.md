# Run 8 (SpecConstr)

**A back-filled record and not a write-up.** It carries this run's published
per-strategy geomeans against `list` and nothing else. What the run measured,
which half published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr |
|---|---:|
| `mut-odo-vecdims` | 0.053 |
| `bq-mut-runs-gm-mulback` | 0.086 |
| `bq-scan-rem-gm-mulback` | 0.090 |
| `bq-expand` | 0.102 |
| `build` | 0.095 |
| `offtab` | 0.146 |
| `mut-flat` | 0.074 |
| `bq-mut-runs-mulback` | 0.078 |
| `bq-odo-mulback` | 0.089 |
| `bq-scan-packed-mulback` | 0.108 |


## Why the hand-packed arms lose under `-fspec-constr`

**`bq-scan-packed-mulback` gets worse because SpecConstr gives its control,
for free, exactly what the packing was hand-rolled to buy --- and the packing
keeps charging for it.** Dumped in both regimes from Run 8's commit (2026-08-08,
`-dsuppress-all -dsuppress-uniques`), the two arms' table builds differ like
this. At -O1 the control's loop carries its state as a boxed `Either` of a boxed
pair of a boxed `Int`, allocating a `Right` per step --- the 72-bytes-an-entry
the law at `baseOffsetsScanPacked` records --- while the packed arm unwraps one
`I#` and is otherwise unboxed, which is the 21% lead it held there.
Under `-fspec-constr` both loops specialise to four raw arguments and *neither*
boxes: the control's `Either`, pair, `I#` and its per-step allocation all
vanish, and the packed arm loses only its one `I#` unwrap. What survives on one
side and not the other is the packing's own arithmetic ---
`uncheckedIShiftRA# ... 32#` and `andI# ... 4294967295#` on every element,
against the control's two plain `+#` --- so the flag pays off the debt
the packing existed to avoid and leaves the packing's interest still due. Hence
cheaper (1.33x on both) and slower (1.11x on 24 shapes of 24).

**Two consequences. The law at `baseOffsetsScanPacked` is confirmed
in its constructive half and its corollary refuted**: every state shape does
unbox under the flag, but "indistinguishable from its control" does not follow,
because unboxing removes the control's cost and not the packed arm's. The `diag`
behind all of this was re-measured in Run 8's own regime and every figure quoted
above reproduces, including the controls that say the instrument did not move;
what it adds is that `baseOffsetsScanPacked` goes 3.00x to 1.00x, so
under the flag even the boxed `Int` in `unfoldrExactN`'s emit pair --- which
the -O1 reading called out of reach of any state shape --- is gone.
And the packed representation is now known to be a **-O1-only** optimisation:
wherever SpecConstr runs it is strictly dominated by the plainer arm
it was built to beat. That was written as a thing to settle before the flag
question, and the flag question has since been answered against it --- every
claim here is read under `-fspec-constr`, so the packed form is not a candidate
here at all. **The Core account above is the only copy, and there is nowhere
to move it:** the dead-ideas list takes ideas that died on paper and this one
was built, rostered and measured, and the roster entry in `Main.hs` records
the arm's size precondition rather than this ruling. Recorded so the move
is not proposed a second time.

**It does not generalise to the other hand-packed arms, and why not
is the useful half.** Three benchmarked pairs differ from their control
in a hand-managed compact representation and in nothing else, and the flag moves
all three differently. The -O1 column is a ratio of published columns,
that run's artifact being gone; Run 8's is paired, and the last two columns
are each arm's own absolute per-call move:

| arm / its control | hand-packed how | -O1 | Run 8 | arm | control |
|---|---|---:|---:|---:|---:|
| `bq-scan-packed-mulback` / `bq-scan-mulback` | loop state, two fields in one `Int` | 0.789 | **1.113** | 1.022 | 0.724 |
| `bq-expand32-lemire-mulback` / `bq-expand-lemire-mulback` | the `m`-length table at `Int32` | 0.983 | **0.949** | 0.729 | 0.756 |
| `offtab32` / `offtab` | the `l`-length table at `Int32` | 1.136 | **0.877** | 0.940 | 1.218 |

**Hand-packing survives the flag exactly when what it buys is something
the specialiser cannot buy.** The packed state buys unboxed loop state, which
is SpecConstr's own job, so the flag hands the control the same thing
for nothing and leaves the packing holding its shift and mask. The two `Int32`
tables buy heap footprint, which SpecConstr has no opinion about, and the Core
says so: their distinguishing operations --- two `intToInt32#`,
a `writeInt32Array#`, no boxing --- are identical in the two regimes,
as are their controls', so the `expand32` pair barely moves. The `offtab32` pair
moves furthest of the three and not for its packing at all: its arm improves 6%
while its *control* regresses 22%.
