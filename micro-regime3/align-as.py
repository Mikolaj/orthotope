#!/usr/bin/env python3
"""A stand-in assembler for GHC's -pgma that aligns loop heads to a cache line.

GHC's native backend emits `.align 8` at procedure starts and nothing inside
them, so a hot loop lands wherever its procedure's code puts it, and
README.md's floor section prices that at 1.22x best to worst for the 28-byte
run-fill. `-fproc-alignment=64` does not reach a loop -- it pins the procedure
and so freezes the offset rather than choosing it. This does choose it: it
sits between GHC and the real assembler and puts a `.p2align` in front of
every loop head, which is a local label that a later instruction jumps
backwards to.

    cabal build micro --ghc-options="-pgma /path/to/align-as.py -fforce-recomp"

`-fforce-recomp` or a fresh `--builddir` is not optional. GHC does not count
`-pgma` or `-fproc-alignment` as a flag change, so an incremental build keeps
the old object code and reports nothing (README.md, same section).

  LOOP_ALIGN   log2 of the boundary, default 6 (64 bytes)
  REAL_AS      the real assembler, default /usr/bin/gcc

The published copy of this is in horde-ad's
`docs/ghc-issue-no-loop-alignment.md`, filed as GHC work item 27668
(https://gitlab.haskell.org/ghc/ghc/-/work_items/27668), which gives it as
that issue's workaround and adds a LOOP_SKEW variable for stepping one loop
through the eight positions of a line. This copy is the one the suite builds
with; keep the two in step if either changes.

This is what Run 10's aligned half is built with, against an unaligned half
from the same source; README.md's run procedure has the build and check
sequence, and the two must not be rebuilt between the halves.

Measured on the suite (2026-08-10, `Main.hs` at the Run 10 roster,
-fspec-constr): 395 loop heads aligned in the assembly, which in the binary
leaves 100 of 101 short self-loops of Main's own code at offset 0 and none of
them straddling, against 50 straddling of 115 without it -- `loop-offsets.py
--survey` counts that population, and the shim's own 395 counts labels rather
than loops. `.text` up 0.13%, and `micro check` green: 45 shapes at
agree=True and none at agree=False.

**Pad only between two instructions.** The first version of this aligned every
`.L` label a backward jump targeted, which is 928 of them, and the binary it
produced failed `check` on the first shape with `index out of bounds
(-1378,324)`. GHC's tables-next-to-code puts an info table immediately before
a return point, which is also a local label, and a `.p2align` inserted there
separates the table from the code it belongs to. Requiring the preceding line
to be an instruction drops the count to 395 and fixes it. Loops whose head
follows a table are therefore left unaligned -- and the survey above says
that costs nothing here, none of the skipped heads being a short loop that
would have straddled. That failure is also this script's non-vacuity proof: the
suite's own `check` distinguishes a working build from a broken one, so a
green `check` here means something.
"""
import os
import re
import subprocess
import sys

REAL = os.environ.get('REAL_AS', '/usr/bin/gcc')
ALIGN = os.environ.get('LOOP_ALIGN', '6')
LABEL = re.compile(r'^(\.L\w+):')
JUMP = re.compile(r'^j\w*\s+(\.L\w+)\b')
INSTR = re.compile(r'^[a-z][a-z0-9.]*\s')   # a mnemonic, not a directive or label


def rewrite(path):
    with open(path) as f:
        src = f.read().split('\n')

    seen, heads = set(), set()
    for line in src:
        s = line.strip()
        m = LABEL.match(s)
        if m:
            seen.add(m.group(1))
            continue
        m = JUMP.match(s)
        if m and m.group(1) in seen:     # jumps back: its target is a loop head
            heads.add(m.group(1))
    if not heads:
        return 0

    out, prev, n = [], '', 0
    for line in src:
        m = LABEL.match(line.strip())
        if m and m.group(1) in heads and INSTR.match(prev):
            out.append(f'\t.p2align\t{ALIGN}, 0x90')
            n += 1
        out.append(line)
        s = line.strip()
        if s and not s.startswith('#'):
            prev = s
    with open(path, 'w') as f:
        f.write('\n'.join(out))
    return n


def main():
    args = sys.argv[1:]
    n = 0
    for a in args:
        if a.endswith('.s') and os.path.exists(a):
            try:
                n += rewrite(a)
            except Exception as e:           # never break a build over this
                print(f'align-as: {a}: {e}', file=sys.stderr)
    if os.environ.get('ALIGN_AS_VERBOSE'):
        print(f'align-as: aligned {n} loop head(s)', file=sys.stderr)
    return subprocess.call([REAL] + args)


if __name__ == '__main__':
    sys.exit(main())
