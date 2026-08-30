#!/usr/bin/env python3
"""Where each stage's toUnorderedVectorListT one-block test fires.

    ./probe-oneblock.py run22-g912          # runs `check` and reads it
    ./probe-oneblock.py --check-log FILE    # or reads a `check` log you have

Registration 4 of Run 22 turns on this and nothing else computes it: the
two `libunord-*` arms put each stage's one-block test in front of its
liblist body, so a view the test fires on costs one `VS.slice` and the
arm goes degenerate there.  The tests differ in two moves and both
matter -- stage one compares the SIGNED strides of the raw dims against
the sorted shape's natural ones, stage two the ABSOLUTE values of the
canonical ones -- so `rev`, whose every stride is negated, is one block
for stage two and is not for stage one.

Both predicates are ports of `fbLibUnordStage1` and `fbLibUnordStage2`
in Main.hs, `canonView` and `getStridesT` with them.  THAT IS THE ONE
THING TO RE-READ WHEN EITHER MOVES: this file is a copy of four
definitions and nothing warns it if the originals change.  It is a probe
and not a checker for that reason -- it answers a question, it does not
gate anything, and a run quotes its output rather than its exit status.

WHAT IT CANNOT SAY, and the reason is `check`'s output and not this
code: the MAIN SET's rows are printed as `normalSh ... -> strided ...`
with no strides, so neither test can be evaluated on them here.  The L1
roster pass answers that half instead, by which arms sink under the
forcing term -- on Run 22, eight cells over `stretch-wide-2xM`,
`-bigstride`, `-tall-Mx2`, `-inner256` and `-inner1`.

Read on Run 22, 2026-08-30, for the record: stage two fires on TEN of
the 37 rostered class views -- every view of `rev`, `revsome` and
`reshape1`, `reshape1-strided-r3` included, an unordered consumer not
minding a permutation -- and stage one on NONE of the 38 that print
strides, the thirty-eighth being the check-only `reshape1-slice-off7`.
"""

import re
import subprocess
import sys

VIEW = re.compile(r'^(\S+): view \[([-\d, ]*)\], strides \[([-\d, ]*)\]')
NOSTRIDE = re.compile(r'^(\S+): normalSh \[')


def strides_of(shape):                      # getStridesT = scanr (*) 1
    out = [1]
    for n in reversed(shape):
        out.insert(0, out[0] * n)
    return out


def canon_view(shape, ats):                 # canonView, foldr merge []
    acc = []
    for n, st in reversed([(n, st) for n, st in zip(shape, ats) if n != 1]):
        if acc and st == acc[0][0] * acc[0][1]:
            acc[0] = (n * acc[0][0], acc[0][1])
        else:
            acc.insert(0, (n, st))
    return [p[0] for p in acc], [p[1] for p in acc]


def desc(pairs):                            # sortBy (flip compare)
    return sorted(pairs, key=lambda p: (p[0], p[1]), reverse=True)


def one_block_stage1(shape, ats):
    pairs = desc(list(zip(ats, shape)))
    return [p[0] for p in pairs] == strides_of([p[1] for p in pairs])[1:]


def one_block_stage2(shape, ats):
    csh, cats = canon_view(shape, ats)
    pairs = desc(list(zip([abs(x) for x in cats], csh)))
    return [p[0] for p in pairs] == strides_of([p[1] for p in pairs])[1:]


def main(argv):
    if len(argv) == 3 and argv[1] == '--check-log':
        text = open(argv[2]).read()
    elif len(argv) == 2 and not argv[1].startswith('-'):
        run = subprocess.run(['./' + argv[1].lstrip('./'), 'check'],
                             capture_output=True, text=True)
        if run.returncode != 0:
            print('!! `%s check` exited %d' % (argv[1], run.returncode))
            return 2
        text = run.stdout + run.stderr
    else:
        print(__doc__.strip().split('\n\n')[1])
        return 2

    fires1, fires2, unread = [], [], []
    seen = 0
    for line in text.split('\n'):
        m = VIEW.match(line)
        if m:
            seen += 1
            shape = [int(x) for x in m.group(2).split(',')]
            ats = [int(x) for x in m.group(3).split(',')]
            if one_block_stage1(shape, ats):
                fires1.append(m.group(1))
            if one_block_stage2(shape, ats):
                fires2.append(m.group(1))
        elif NOSTRIDE.match(line):
            unread.append(NOSTRIDE.match(line).group(1))

    if not seen:
        print('!! no view printed its strides -- wrong log, or `check` changed')
        return 2
    print('views printing strides: %d' % seen)
    print('stage ONE fires on %d: %s' % (len(fires1), ' '.join(fires1) or '--'))
    print('stage TWO fires on %d: %s' % (len(fires2), ' '.join(fires2) or '--'))
    print('NOT EVALUATED, no strides printed (%d): the main set, whose rows'
          % len(unread))
    print('  `check` gives as normalSh -> strided; the L1 roster pass answers')
    print('  that half, by which arms sink under the forcing term')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
