# Handoff: the fill's prologue tables on a one-level view

Written 2026-09-22 at the end of the session that landed `b781c63`, `78c5521`
and `c652c57` in `~/r/orthotope` and `80b6f6a` in `~/r/orthotope.toVectorListT`,
on `pr-mikolaj-toVectorListT`. It records one candidate those commits left
unmeasured, measured in both fills and kept as the arm
`lib-stage3-lean-onelevel` (`fe430cf`), with the recipes to price it. Everything
below the observation was a plan, and each experiment's result closes
its section. The words: the harness is `Main.hs` in `micro-regime3` of the first
checkout, whose roster of benchmark arms this file names by their roster names;
the library is `Data/Array/Internal.hs` in the second; a run is one evening
over the whole roster, written up under `runs/`, and a probe is anything
smaller; a pair is two binaries, its halves, built from one recipe and differing
in one thing; the floor of a population is the spread its A/A copies show, which
`read-run.py --aa` prints. `micro-regime3/CLAUDE.md` and the README's run
chapter hold the rules the recipes below lean on.

## Where things stand

`fillStage2Axes` in the harness is the library's `genericFillStrided`
to the line, its odometer levels (the loops over the axes outside the innermost
run) numbered outermost first over `outerFirst outerAxes`, one reversal per
call; `fillStage2` was the same loop with the levels numbered innermost first
and no reversal, and since `2aa607a` walks them as the nest of the second
experiment below. Arms 2, 4 and 13 (`lib-stage2-lean`, `liblist-stage4`,
`libunord-stage13` and their sums) read through the first, arms 3, 5 and 14
through the second, each the other's one-change twin until that commit. Item (6)
of Run 38's registration, in `runs/run38.md` under *What this run was built
to answer*, read the numbering as worth nothing outside the floor, so which fill
ships is the library's call and the other set of twins retires with it.

## The observation

Both fills, and the library's copy, spend the same prologue on every call:
`rOuter = length levels`, then two unboxed tables, `oshV` and `oatsV`, built
by `VU.fromList` over a `map` each, which the odometer indexes by level. A view
whose canonical rank is two has one outer level, the fused level that `runsWith`
walks as a row of runs, and needs no table at all:
`Axes t n (InnerFirst [(st, d)])` can go to `runsWith` directly, and the tables
be built only where a level sits above it. That holds of both fills alike,
a list of one axis reading the same in either orientation; the inward order
shows only from two levels up, where `fillStage2Axes` still reverses the list
for its tables and `fillStage2` takes it as it is. Few views take
those branches. On the main set only the three rank-two stretch shapes,
`stretch-wide-2xM`, `stretch-square-1341` and `stretch-tall-Mx2`, have one outer
level; the other sixteen, the convolution-derived ones among them, canonicalize
to rank three, two levels, and take the tables. On `small`, the stride class
of the smallest views, `small-bcast32` has one level, `small-patch-k5`
and `small-patch-r5` have two and three, `small-row96` has one on the arms whose
reader fills the runs route, the lean ones through `routeVector`, where the list
and sum arms slice it, and `small-flat64` is a slice and never reaches the fill.
So the sketch is read on those few, and the second experiment below is the one
that reaches the rest; the prologue is most of an arm's cost on `small`:
`lib-stage3-lean` retires 3243 to 9147 instructions a call there where its sum
consumer retires 2390 to 8315.

## The candidate

In `fillStage2` (and the same in `fillStage2Axes` and in the library's
`genericFillStrided`, which share the prologue), match the outer axes before
building anything: no level, the run alone; one level, `runsWith`
with that level's extent and stride; two or more, the tables as now. The loop
bodies do not change. `check`, the harness binary's own mode that compares every
arm against a reference on every view, holds the equivalence, the `degenerate-*`
views included, since a fill that mishandles the one-level case fails there
at once.

## Recipes

All from `micro-regime3`, unsandboxed where they write here. The build is Run
39's recipe, Run 38's basis as `run38-pair.txt` records it with `LOOP_SETTLED=1`
added (`9261030`), Run 38's being broken on `stretch-wide-2xM`; a rebuild of one
source reproduced Run 38's binary byte for byte on 2026-09-22, the md5
of a fresh build of `bb6f0fc` matching `run38-gheadnospec`'s, so half A can
be a fresh build of the tree at the commit before the change and half B the tree
with it.

Build a half, one per source state, the binary copied aside under a `probe-`
name:

    LOOP_SETTLED=1 LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 \
    cabal build micro --project-file=cabal.project.ghead --builddir=db-x \
      --ghc-options="-fobject-determinism" \
      --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
    cp "$(cabal list-bin micro --project-file=cabal.project.ghead --builddir=db-x)" probe-x-ghead
    rm -rf db-x

Correctness, about six minutes, exit 0 or nothing else matters:

    ./probe-x-ghead check

Counts on `small`, no quiet machine needed, differenced over fifty iterations
as `run-counts.sh` does; the arms are the twins, `lib-stage1`, which fills
through `fillStage2` by `axesOfDims` and so moves with them, and two controls
the change cannot reach:

    cnt() { c1=$(perf stat -x, -e instructions:u -o /tmp/p1 $1 classes -m glob "$2/$3" -n 100 >/dev/null 2>&1; grep instructions /tmp/p1 | cut -d, -f1)
            c2=$(perf stat -x, -e instructions:u -o /tmp/p2 $1 classes -m glob "$2/$3" -n 50 >/dev/null 2>&1; grep instructions /tmp/p2 | cut -d, -f1)
            echo $(( (c1 - c2) / 50 )); }
    for S in small-bcast32 small-flat64 small-patch-k5 small-patch-r5 small-row96; do
      for A in lib-stage2-lean lib-stage3-lean liblist-stage4-sum liblist-stage5-sum \
               libunord-stage13-sum libunord-stage14-sum lib-stage1 lib-stage2-lean-u1 sum-only-early; do
        printf '%-15s %-22s A %6d  B %6d\n' $S $A $(cnt ./probe-a-ghead $S $A) $(cnt ./probe-b-ghead $S $A)
      done
    done

Time on `small`, about fifteen minutes a half on a quiet machine, under the two
environment switches every run launches with, which `probe-times.sh` asserts:

    WILDLOG=1 SATURATE=1 BIN=./probe-a-ghead OUT=probe-a ./probe-times.sh small
    WILDLOG=1 SATURATE=1 BIN=./probe-b-ghead OUT=probe-b ./probe-times.sh small

Read within each half and never across, the rule `probe-fillpair-read.sh`
states: two builds differ in layout, so an arm's time on one half over the other
prices the layout, and the sound reading is the changed arm over a control
the change cannot reach inside one binary, with the population floor beside it;
then allocation across the halves, which is deterministic and agrees to 1e-4
where nothing moved. All four are modes of `read-run.py`, whose `--help` names
the rest:

    python3 read-run.py probe-b-small.json --pair lib-stage3-lean lib-stage2-lean-u1 --per-shape
    python3 read-run.py probe-a-small.json --pair lib-stage3-lean lib-stage2-lean-u1 --per-shape
    python3 read-run.py probe-b-small.json --aa
    python3 read-run.py probe-b-small.json --compare probe-a-small.json --alloc --per-shape

The main set is where the conv shapes are, at about a hundred minutes a half;
a one-level change reaches only its three rank-two stretch shapes, which
a `-m glob` selection of them times in minutes.

**Mixed, 2026-09-22 and 23.** On `small`, under Run 38's basis, the lean,
liblist sum and `lib-stage1` arms retired 671 to 728 instructions a call fewer
on `small-bcast32` and the lean arms 250 and 308 fewer on `small-row96`,
and `lib-stage3-lean` over `lib-stage2-lean-u1` read 0.533 where the basis read
0.805 on `small-bcast32` and 0.718 against 0.795 on `small-row96`. On the three
stretch shapes the inlined one-level branch reloads and stores a stack slot
every two elements, which the same loop inside `go` does not: 6.5 to 13 percent
more instructions under either recipe, and, timed under Run 39's, 1.248 against
1.032 on `stretch-wide-2xM`, 0.954 against 0.868 on `stretch-square-1341`
and 1.000 against 0.933 on `stretch-tall-Mx2`, a loss of 7 to 21 percent. Taking
the branch out of line with `NOINLINE` cost 19 to 30 times the instructions.
On 2026-09-23 it moved out of both fills into `fillStage2OneLevel` and that arm,
whose header carries the TODO on the spill; the library's copy is untouched.

## A second experiment: the loop nest over the list

The sketch leaves the third branch, two or more outer levels, as it was:
the levels numbered, two tables indexed by number, `length levels` to size them.
With the list innermost first the nest can be built over the list itself, each
level a loop wrapping the one inside it, so that the tables and the `length` go
at every rank and not only at rank two: fold the outer axes from the fused level
outward, `runsWith` at the head, then for each `(st, n)` above it a `dim` loop
of `n` steps of stride `st` around the loop built so far, and run the result
at offset 0 and `ao`. `fillStage2` alone affords it; `fillStage2Axes` would
reverse first.

The precedent is against the shape: the runs walker was written this way
on 2026-09-09, a fold per level with the inner loop passed down, and lost
to its flat loop because the fused fold met a lambda-bound continuation it could
not see and boxed its accumulator per run, 80 bytes, read off the Core.
The fill's loops are `ST` actions and not a fold's continuation, so that reading
does not decide it, but it is the shape to expect to lose, and the views
with two or more outer levels are the majority: sixteen of the nineteen main-set
views canonicalize to rank three, and `small-patch-k5` and `small-patch-r5`
on `small`.

The recipes are those above, with the arms narrowed: `lib-stage3-lean`,
`liblist-stage5-sum` and `libunord-stage14-sum` are the only timed arms
on `fillStage2`, and `lib-stage2-lean`, `liblist-stage4-sum`
and `libunord-stage13-sum` are the controls the change cannot reach, being
on `fillStage2Axes`. Read the counts on `small-patch-k5` and `small-patch-r5`
first, then on any main-set shape but the three rank-two stretch ones;
those three and `small-bcast32` must not move at all, the fast branch being
untouched. A loss is recorded here and the section kept, so that the shape
is not proposed again.

The code measured, in place of the third branch of `fillStage2` as sketched,
the other two branches and `fillStage2Axes` as committed:

        (st0, n0) : outer ->
          -- EXPERIMENT 2: the nest built over the list, innermost first, the
          -- fused level's runs at the head and each level above a loop
          -- around the nest below it; no table and no count.
          let fused | tInner == 0 = runsWith writeRunSet n0 st0
                    | otherwise   = runsWith writeRunStep n0 st0
              wrap inner (st, n)
                | st == 0 = \ !outPos !baseOff -> do
                    op' <- inner outPos baseOff
                    copies n (op' - outPos) outPos
                | otherwise = \ !outPos !baseOff ->
                    let dim !k !op !boff
                          | k <= 0    = return op
                          | otherwise = inner op boff
                                        >>= \op' -> dim (k - 1) op' (boff + st)
                    in  dim n outPos baseOff
          in  foldl' wrap fused outer 0 ao

**Lost, 2026-09-23**, under Run 39's recipe against a build of the sketch
in both fills: `check` passed, and the changed arms retired 1.3 to 1.5 times
the instructions on `small-patch-k5` and `small-patch-r5` and 1.9 to 2.5 times
on the four conv shapes counted, `cnn-L1-24x24-c1` 133732 against 292936
for `lib-stage3-lean`, every control within a few instructions on `small`
and 1e-4 on the main set. Timed within each half, `lib-stage3-lean`
over `lib-stage2-lean` read 1.512 where the basis read 0.993 on `small-patch-k5`
and 1.697 against 0.966 on `small-patch-r5`, floors under 0.6 percent.
`small-bcast32` moved 24 to 27 instructions on the changed arms where it should
not have moved at all, the fast branch's code having shifted with its neighbour.

**Rescued, 2026-09-24**, the fold kept, as read off the Core and assembly
of a copy of the fill in `nest-probe/Nest.hs`, which rebuilds in seconds. None
of the loss was the fold's. `runsWith writeRunStep n0 st0` is a partial
application, so `runsWith` did not inline and called `writeRun` as an unknown
function once a run, its arguments boxed; each level returned its next output
position as a boxed `Int`; each nest was a lazy tuple field, entered through
an indirection; and `st0` and `n0` came from a lazy pattern, so every closure
entry saved its free variables to a frame in case they wanted evaluating. What
stays with closures however they are banged is an unknown call on every
iteration of the level above the fused one, whose callee sets up that frame
for the boxed arguments an unknown caller passes, so the nest is built
as a value and walked by one known function:

    data Nest = Fused | Dim !Int !Int !Int !Nest | Rep !Int !Int !Nest

        -- beside writeRunStep, writeRunSet, copies and runsWith:
        wrap :: (Nest, Int) -> (Int, Int) -> (Nest, Int)
        wrap (inner, !blk) (!st, !n) =
          let !nest | st == 0   = Rep n blk inner
                    | otherwise = Dim n st blk inner
              !blkNext = n * blk
          in  (nest, blkNext)

        (!st0, !n0) : outer ->
          let {-# NOINLINE fused #-}
              fused :: Int -> Int -> ST s ()
              fused !outPos !baseOff =
                (if tInner == 0
                 then runsWith writeRunSet n0 st0 outPos baseOff
                 else runsWith writeRunStep n0 st0 outPos baseOff) >> return ()
              run :: Nest -> Int -> Int -> ST s ()
              run Fused !outPos !baseOff = fused outPos baseOff
              run (Rep n blk inner) !outPos !baseOff =
                run inner outPos baseOff >> copies n blk outPos >> return ()
              run (Dim n st blk inner) !outPos !baseOff =
                let dim :: Int -> Int -> Int -> ST s ()
                    dim !k !op !boff
                      | k <= 0    = return ()
                      | otherwise = run inner op boff
                                    >> dim (k - 1) (op + blk) (boff + st)
                in  dim n outPos baseOff
          in  run (fst (foldl' wrap (Fused, n0 * sInner) outer)) 0 ao

`blk` is the block one iteration of a level writes, so no level returns
a position; the strict `Nest` fields spare each call an evaluation of the level
below; and `fused` is out of line because, inlined into `run`, its stepping loop
spills `sInner`, reloading and storing it every two elements, the spill
the one-level branch above met. Built in place of `fillStage2`'s odometer
under Run 39's recipe (`Main-nest9.hs`, the binary `probe-nest9-ghead`) and read
against a build of `cdb007d`, `check` passed. Counted by `probe-stalls.sh`,
every control within 0.08 percent, the changed arms retired 4 to 13 percent
fewer instructions on `small-bcast32`, `small-patch-k5`, `small-patch-r5`,
`cnn-L1-6x6-c1` and, `lib-stage3-lean` alone, `small-row96`; the lean
and liblist arms were within 0.5 percent on the larger conv shapes, where
`lib-stage1` read between 0.4 percent more and 4 percent fewer, and level
on the three stretch shapes. In cycles, `lib-stage3-lean` over `lib-stage2-lean`
within each half in two legs read 0.79 and 0.79 against 0.94 and 0.90
on `small-patch-k5`, 0.83 and 0.84 against 0.93 and 0.94 on `small-patch-r5`,
0.82 and 0.82 against 0.95 and 1.00 on `small-row96` and 0.78 and 0.76 against
1.02 and 0.97 on `cnn-L1-6x6-c1`, and level within the legs' spread on the rest
but `stretch-wide-2xM`, 1.07 and 1.07 against 1.00 and 1.01 at the same
instructions and with no more branch or cache misses, read in the section after
this one. The cycles are `probe-stalls.sh`'s differenced `cycles:u` at an N
sized to each shape, legs A, B, A, B (`nest-probe/sweeps-time.sh`), a minute
and a half of quiet machine where `probe-times.sh` over `small` takes up to half
an hour a half. In `fillStage2` since `2aa607a`. Its first form, committed
as `2f0bc35` and since amended, passed `check` built by the same recipe
(`probe-fs2-ghead`); the signatures on `wrap` and `dim` shown here and the names
`blkNext` and `srcNext` retire the same instructions as it to within three
a call, the counter's own spread, on every cell counted (`probe-fs3-ghead`,
`check` passing), and `wrap`'s move beside `runsWith` builds `probe-fs3-ghead`
byte for byte (`probe-fs4-ghead`, `2aa607a`'s source). Not in `fillStage2Axes`
or the library.

Refuted on the way, in instructions, so not to be proposed again: the closures
with the four fixes, 6 to 17 percent over the table on the conv shapes
for the unknown call; closures taking `Int#`, dearer still, the RTS having
no apply pattern for two words and a state token, so each call goes through
`stg_ap_n` and two stack frames; the data form with `fused` inlined into `run`,
measured with lazy fields, 6 to 11 percent over on the stretch shapes, strict
fields leaving the spill in the probe; and a recursive runs function in place
of the `NOINLINE`, which stays out of `run` but whose self-call is a call
and not a jump, re-entering once a run, 1.24 of the table on a probe view
of runs of 2.

No committed fill has the first cause: every under-applied use of an `INLINE`
name in `Main.hs` at `cdb007d` and in the library at `8f7d7d1`, read against
both modules' Core, is inlined but `runRank`, a sort comparator called in tail
position, `magicOf` in `map magicOf nts` and the `baseOffsets*`
of the `offsetBuilders` table, none of which takes a function argument.

## The `stretch-wide-2xM` cell, read after `2aa607a`

The view `[2, 900000]` is 900000 runs of 2 elements a call into a 14 MiB output,
so what turns over is the whole per-run path: head, two elements, the two exit
tests, the run tail and its jump back, as the gdb breakpoint below counted.
Every figure is an iteration of `probe-stalls.sh`'s differenced form on a quiet
machine unless it says otherwise, the changed arm being `lib-stage3-lean`, which
runs the nest, and the controls `lib-stage2-lean` and `lib-stage2-lean-u1`,
which run `fillStage2Axes`.

Where the time goes. `perf record -e cycles:u` works on the harness halves,
where on `nest-probe`'s binary it segfaults the process. It splits an iteration
between the fill's run loop and the sum consumer's loop, which sits at offset 3
on both halves and costs about 5.4M cycles on both by the samples' shares;
the fill goes from about 3.5M to about 4.5M, its samples bunching on the store
after the first load.

Placement, first. `loop-offsets.py --delta run38-gheadnospec run39-gheadnospec`
reproduced Run 39's recorded `[18, 15, 0, 0, 9, 2] -> [0, 0, 0, 0, 0, 0]`,
and `--delta probe-nestA-ghead probe-nest9-ghead` then kept every offset
of the 28-byte groups. The run loop's head is at residue 0 on both, `0x431600`
on half A and `0x4317c0` on nest9. The nest's copy is the odometer's
instructions under other registers, and one of them,
`movsd %xmm0,(%rax,%r14,8)`, is a byte longer than the odometer's
`(%rcx,%rsi,8)` for its REX prefix, so everything after it sits a byte later
and the run tail starts at +0x40, on the next line, where the odometer's starts
at +0x3e.

Heap and file. Under `+RTS -A8m`, `-A31m`, `-A32m`, `-A33m` and `-A40m`, two
readings each, the changed arm over `lib-stage2-lean` read 1.004 to 1.037
on half A and 1.033 to 1.078 on nest9. The copy test
in `probe-r39-instance.sh`'s form, three passes interleaved over each half
and a fresh copy of it (`nest-probe/log-copy-test.txt`), read nest9 at 1.048
to 1.078 on the original and 1.064 to 1.074 on the copy, 10.22M to 10.32M cycles
on either, against half A's 0.953 to 0.992 and 0.983 to 1.010.
On `cnn-L1-6x6-c1` the half-A copy moved the CONTROL, `lib-stage2-lean` reading
up to 10 percent slower there, an instance effect on the control and not
on the change.

Counters, the raw codes from `perf-codes-0920.txt` and perf's Zen 3 names.
`de_dis_dispatch_token_stalls1.int_sched_misc_token_stall` (`r8ae`) reads 3.0M
to 3.1M on every file and arm, so this is not the 2026-09-20 instance term.
`ic_fetch_stall.ic_stall_any` (`r487`) reads 5.74M to 5.85M on the nest's copy
against 3.97M to 4.56M everywhere else. Op-cache lookups (`r20000078f`, 0x28F
all) read 4.50M against 5.41M, all hits (`r20000038f`), the misses
(`r20000048f`) at 4 to 6 thousand everywhere, about Run 39's 3 to 5 thousand
at residue 0. The store-queue, load-queue, physical-register-file
and taken-branch-buffer token stalls (`r4ae`, `r2ae`, `r1ae`, `r10ae`)
are at noise. The `r428f` column in `probe-tok-g2-*` is event 0x08F with unit
mask 0x42, not 0x28F, and is uninterpreted.

Swaps. Swapping the two fills' definitions in the source (`Main-swapA.hs`
over `cdb007d`, `Main-swap9.hs` over nest9) moved neither loop by a byte,
nor the sum loop, the md5s differing only for the `assert` locations, so source
order is no lever on placement. Renaming both definitions and every call
together (`Main-names9.hs`) built nest9's binary byte for byte, which tests
nothing. Exchanging the fifteen call sites alone (`Main-calls9.hs`, `check`
passing) moved both loops, the nest's to `0x431880` and the odometer's
to `0x43dc00`, each keeping its own encoding, and carried both the wins
and the cost to `lib-stage2-lean`: 9.99M to 10.06M cycles, 4.50M lookups
and 5.48M to 5.55M stall there, `lib-stage3-lean` reading clean at 9.55M
to 9.61M. The win cells' ratios inverted, `small-patch-k5` 0.787 to 1.256,
`small-patch-r5` 0.818 to 1.377, `small-row96` 0.834 to 1.119
and `cnn-L1-6x6-c1` 0.783 to 1.267.

Residue. The head's label, `.LQ5DD`, came off a `-pgma` wrapper that keeps each
`.s` before running the shim (`nest-probe/keep-as.sh`), whose build reproduced
`probe-fs2-ghead`'s md5. `LOOP_PIN=.LQ5DD:R` at 8, 16, 24 and 32
(`nest-probe/build-pins.sh`), each confirmed in the binary and each passing
`check`, read, over `lib-stage2-lean-u1` in two passes, 1.073 and 1.080 at 0,
1.076 and 1.087 at 8, 1.080 and 1.083 at 16, 1.345 and 1.366 at 24 and 1.088
and 1.093 at 32, the controls 0.985 to 1.028. The lookups were 4.50M at 0 and 8,
5.40M at 16 and 32 and 6.30M at 24, and the fetch stall 5.7M, 5.7M, 4.8M, 4.6M
to 4.7M and 4.9M. So at 16 and 32 the copy takes the odometer's lookup count
and less stall and keeps its cycles, and 24 is a band of its own.

Data. gdb on each run tail (`0x431800` on `probe-fs2-ghead` with the output base
in `%rax` and the source in `%rdi`, `0x43163e` on half A
and the `fillStage2Axes` copies at `0x449c3e` and `0x449ebe` with them in `%rcx`
and `%r8`) read every run of both arms on both binaries writing `0x4203d04010`
and reading `0x4202f04010`, 14 MiB apart at page offset 0x010, the breakpoint
hit about 885000 times before the 200-second timeout stopped each run.

So the cost follows the nest's copy of the loop, its encoding and whatever comes
with its sitting in `fused`, through address, residue, file instance, nursery
and data, and its fetch-block count moves with the residue while its cycles do
not. It is not explained. Two things would read further: scoring both copies'
per-run path with `probe-fetch-model.py`, offline; and a code shape that gives
the nest's copy the odometer's registers, to see whether that copy reads clean.

Left in the tree by this reading, all untracked and for deletion once read:
the binaries
`probe-{nestA,nest6,nest7,nest9,swapA,swap9,names9,calls9,fs2,fs3,pin8,pin16,pin24,pin32}-ghead`
and `probe-copy-{nestA,nest9}-ghead`; the sources
`Main-{nest6,nest7,nest9,swapA,swap9,names9,calls9}.hs`, `Main.hs.nest-base`
and `Main.hs.build-save`; `nest-probe/`, which holds the standalone probe,
the drivers, the profiles and the kept assembly; the readings
`probe-stalls-{nestA,nest6,nest7,nest9}*`, `probe-cyc*`, `probe-fe-*`,
`probe-tok-*`, `probe-sw*`, `probe-sc{1,2}-*`, `probe-sc-{fs2,calls9}-*`,
`probe-pn*` and `probe-ic-*`; and the logs `log-build-X.txt`
and `log-check-X.txt` for X each binary above bar the copies, there being
no `log-check-nestA.txt`, with `log-build-keep.txt`,
but not `log-build-inlscan*.txt`, which are another session's. Two comments
in `Main.hs` went stale with `2aa607a` and are left for the owner:
`fillStage2Axes`'s header, which still calls it `fillStage2` with the numbering
flipped, one change, and the twins pricing the numbering;
and `fillStage2OneLevel`'s header, which prices it against `lib-stage3-lean`,
now on the nest. hlint's one new hint, *Use void* on `fused`'s `>> return ()`,
was left as measured.

## What decides

Counts first: a change that moves no instruction on the twins and every control
is a rename. Then the pair against `lib-stage2-lean-u1` past the population
floor on `small`, which read 0.8 to 1.6 percent on 2026-09-22, and on the three
stretch shapes, where the candidate lost. A win goes into both fills here
and the library's copy in one step each, with the counts in the message
as `b781c63`'s carries them; a loss is recorded against this file's candidate
and the file deleted. The nest went into `fillStage2` alone, by the owner's
decision of 2026-09-24, with `stretch-wide-2xM` the one cell it loses;
`fillStage2Axes` and the library wait on that cell.
