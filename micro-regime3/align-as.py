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
  LOOP_MAXSKIP pad only a loop that would cross a boundary it need not,
               default off
  LOOP_LOOKTHROUGH  read past byte-free lines when deciding whether a head
               follows an info table, which a `-g` assembly gets anyway;
               on a plain one it finds 27 heads more and so is a basis
               change, which is why it is a switch and off by default
  PAD_BYTES    dead bytes appended after the first module's text, default 0
  REAL_AS      the real assembler, default /usr/bin/gcc
  ALIGN_AS_VERBOSE  report the budgets emitted and the heads fallen back on

**Pad only a loop that would cross a boundary it need not, and only by what
it needs** -- `LOOP_MAXSKIP=1`, and off by default because a default is the
one thing a pair's note cannot record: every half is built by a recipe that
sets what it wants explicitly, so a default that moved would rebuild some
other binary under the name the note gives. Run 11 priced the two forms and
the basis has been max-skip since Run 12, which is a fact about the recipes
and not about this file. A loop of length `L` at
`p = addr mod 64` occupies `(p + L - 1) div 64 - p div 64 + 1` cache lines,
and holds that at its least `ceil(L/64)` for every `p` up to `s = 64 *
ceil(L/64) - L`, the free room in its last line. So

    spans a line it need not  <=>  p > s  <=>  padding <= 63 - s

and `63 - s` is `(L-1) mod 64`, which makes `.p2align 6, 0x90, (L-1) mod 64`
move exactly the heads that would cross an extra boundary and no others --
exactly, GNU `as` skipping the alignment altogether when it would need more
than `max_skip` bytes. A head so treated either stays byte for byte where it
fell or goes to offset 0, there being no third outcome, and none is moved for
nothing. `p` is left to the assembler because padding upstream moves it; `L`
is measured here because the assembler will not say, and can be, being
layout-invariant for these loops: padding before a head does not change
intra-loop distances, so a short loop's backward branch keeps its `rel8`
encoding.

**The criterion is lines spanned and not straddling**, and the two are the
same question only for a loop that fits a line, where `s = 64 - L` and the
budget is the plain `L-1`. Above that the straddle reading says a loop
crosses a boundary wherever it sits and so cannot be helped, which is true
and beside the point: a 68-byte loop occupies 2 lines at offset 60 and 3 at
offset 61. **Taking the narrow reading is a ruling this file now records
against itself.** The first max-skip form dropped every head with `L > 64`
and left **137** of the 395 heads spanning a line more than they need, where
the unconditional form leaves none -- and this code is mostly such loops,
only 120 heads carrying a loop that fits a line, the median 144 bytes and the
longest 18097. Nor did it leave them alone: 134 long heads span an extra line
with no shim at all and 137 after that one, the padding for the short heads
having shifted them. Under the rule above, 148 of the 275 long heads end at
offset 0, the other 127 stay where they fell, and every one of the 127 is
already spanning the least its length allows.

**Measured out of band, one extra assembly per module, and from the symbol
table rather than from a disassembly.** A probe copy of the source carries an
ordinary local symbol at each head and one after each backward jump that
targets it -- symbols occupy no bytes, so the probe lays out as the real
assembly will -- and `L` is the shortest head-to-end distance the assembled
probe's symbol table reports. **The disassembly this was first written as is
what the symbol table replaced, and the reason is a measurement**: on
`Main.hs` at 2b41e53 `objdump` can attribute a backward jump to only **141**
of the 395 heads, tables-next-to-code being what its linear sweep loses
sync on (`loop-offsets.py`'s own docstring prices the same effect), so 254
heads would have fallen back to the unconditional directive and most of the
change would not have happened. The two routes **agree on `L` at every one of
the 141 both can read**, which is what warrants the exact one; the symbol
table prices all 395, so the fallback count here is **0** and nothing rests
on it (2026-08-11, -fspec-constr, GHC 9.12.4).

Both forms emit a directive at all 395 heads, and what differs is the budget:
without one the assembler always pads, with one it declines wherever the loop
already spans the least it can. The costs the unconditional form charged fall
accordingly. `.text` is
20385989 bytes under it against the plain build's 20373701, up 12288 or
0.060% -- the 0.13% recorded here before does not reproduce at any of the
three sizes it could have been a ratio of -- and 20377797 under max-skip, up
4096 or 0.020%, a third of it for the same zero heads spanning a line they
need not. And arms whose loops were already line-resident read 1.0069 to
1.0378 *slower* aligned in Run 10, having fallen through into aligned heads
and executed the NOPs; those loops now keep their own offset, 58 of the 112
short loops `--survey` reads in this binary sitting at 0 against 100 of 101
in the unconditional one, and **none straddling in either**. What the
max-skip form gives up is membership invariance -- adding an arm can move a
fitting loop onto a boundary, where the unconditional form relocates
nothing -- which is why Run 11 pairs the two rather than replacing one with
the other.

The published copy of this is in horde-ad's
`docs/ghc-issue-no-loop-alignment.md`, filed as
[GHC work item 27668](https://gitlab.haskell.org/ghc/ghc/-/work_items/27668),
which gives it as that issue's workaround and adds a LOOP_SKEW variable for
stepping one loop through the eight positions of a line. **The two have
diverged and are not to be re-synced by editing the filed record**: what is
filed is what was filed,
and the max-skip form above postdates it. A reproducer wanting the smaller
`.text` can take this file; the issue text stands as posted.

`PAD_BYTES` is a trailing pad, here because only one `-pgma` reaches a build
and Run 11's pair needed both: its two halves are the unconditional shim and
this one, whose `.text` sizes differ by the 8192 the two growths above leave
between them, and the pad is what puts the libraries back in phase. It goes
at the end of the first module's text, so the module's own code keeps every
offset it had.

How the number is derived, since the script that once did it is gone: a pair
must not move the libraries, no shim on `-pgma` reaching them, so anything
that changes `.text`'s size displaces everything linked after it -- aligning
grew it by 12 KB and moved 856 of 867 library loops. Matching the size alone
does not repair that: it left the delta at 32 mod 64, which is the worst
shift a line admits. The pad is therefore derived in two steps, the size
difference and then the residual phase, and the result is checked rather
than assumed -- `./loop-offsets.py --library A B`, which is what reports how
far two halves agree about where the libraries sit. Here PAD_BYTES=8192
needs neither correction: it shifts the libraries rigidly, by 256 or four whole lines, on
29318 of the 29449 `.text` symbols the two halves share, 100.0% of them in
phase. **Read that off `nm`, symbol by symbol, and not off the loop-based
phase.** An earlier max-skip build wanted a correction the two steps do not
cover -- equalising the size left the libraries in two populations 8 bytes
apart, the linker aligning an input section between them, so the pad's own
size mod 16 decided whether they moved together. The loop-based figure said
only that something was wrong (86%); the symbol tables said what, two
populations with the boundary at one address, which is what a third step
would have to be derived from.

This is what Run 10's aligned half was built with, unconditionally, and what
Run 11's `micro-maxskip` half is built with at the max-skip form above;
README.md's run procedure has the build and check sequence, and the halves
must not be rebuilt between them.

Measured on the suite (2026-08-10, `Main.hs` at the Run 10 roster,
-fspec-constr) in the unconditional form: 395 loop heads aligned in the
assembly, which in the binary leaves 100 of 101 short self-loops of Main's own
code at offset 0 and none of them straddling, against 50 straddling of 115
without it -- `loop-offsets.py --survey` counts that population, and the
shim's own 395 counts labels rather than loops. `micro check` green in both
forms: 45 shapes at agree=True and none at agree=False, and the two halves'
`check` logs byte-identical, agreement being a property of the strategies and
not of where their loops landed.

**Those two survey populations differ in size for a reason that is the
disassembler's, not the shim's** (2026-08-11). 115 against 101 is not fourteen
loops removed: Main carries 1580 backward jumps unaligned and 1583 aligned,
so the loop structure is untouched, while targets that `objdump -d` fails to
decode as an instruction start go 613 to 777. A linear sweep over
tables-next-to-code re-synchronises differently once code shifts by arbitrary
NOP runs, so the aligned binary is simply harder to read; lifting the survey's
64-byte cap shows the loss spread across every span bucket, which rules out
padding having inflated loops past a line. So *none straddling* is a
statement about a sample alignment makes smaller. The claim is sound in the
form this script can make it -- unconditionally every head it aligned is at
offset 0 by construction and the only ones it skips are the INSTR guard's,
and under max-skip every head it left alone was measured not to need moving
-- and that is where completeness should be argued, with the survey as
corroboration. README.md's floor section carries the same correction.

**Pad only between two instructions -- looking through the lines that emit
none.** The first version of this aligned every `.L` label a backward jump
targeted, which is 928 of them, and the binary it produced failed `check` on
the first shape with `index out of bounds (-1378,324)`. GHC's
tables-next-to-code puts an info table immediately before a return point,
which is also a local label, and a `.p2align` inserted there separates the
table from the code it belongs to. Requiring the preceding line to be an
instruction drops the count to 395 and fixes it. Requiring it *literally*
made this blind under `-g`, which is the second half of the rule and was
found on 2026-08-13: GHC then closes every basic block with `_end` and
`_proc_end` labels, so a head follows a label rather than an instruction and
every site was dropped -- **0 of a `-g3` assembly's heads against 395 of the
plain one's**, and the build came out unaligned in silence, no short loop at
offset 0, 41 straddling, two of them timed fills. A table's last line is a
`.quad` or a `.long`, so a label and a `.loc` are read past and the guard
asks its question of the last line that emits a byte. That form fires only
where the file carries `.loc`, for the reason `sites` records: it is not
inert on a plain build, and moving one is a basis change this is not the
place to make. The control is two fresh builddirs -- a shim change reaches
nothing without one, `-fforce-recomp` included -- and the max-skip half
comes out md5-identical under the two forms, each printing 395, while the
`-g3` build goes from 0 to 421. Loops whose head
follows a table are therefore left unaligned -- and the survey above says
that costs nothing here, none of the skipped heads being a short loop that
would have straddled. That failure is also this script's non-vacuity proof: the
suite's own `check` distinguishes a working build from a broken one, so a
green `check` here means something -- and it is the gate for the max-skip form
too, offsets alone being what a mispadded binary still gets right.
"""
import collections
import os
import re
import subprocess
import sys
import tempfile

REAL = os.environ.get('REAL_AS', '/usr/bin/gcc')
ALIGN = os.environ.get('LOOP_ALIGN', '6')
MAXSKIP = bool(os.environ.get('LOOP_MAXSKIP'))
LOOKTHROUGH = bool(os.environ.get('LOOP_LOOKTHROUGH'))
PAD = int(os.environ.get('PAD_BYTES', '0'))
BOUND = 1 << int(ALIGN)
LABEL = re.compile(r'^(\.L\w+):')
JUMP = re.compile(r'^j\w*\s+(\.L\w+)\b')
INSTR = re.compile(r'^[a-z][a-z0-9.]*\s')   # a mnemonic, not a directive or label
BYTELESS = re.compile(r'^(?:[\w.$]+:|\.(?:loc|file|cfi_\w+)\b.*)$')  # no bytes
PROBE = 'apLoop'          # apLoopHead_<line>, apLoopEnd_<line>_<k>_<n>


def heads_of(src):
    """The `.L` labels some later instruction jumps backwards to."""
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
    return heads


def sites(src, heads):
    """Where a directive would go: (line index, label), in source order.

    The INSTR guard is the correctness half of this script rather than a
    tuning knob -- the docstring above has the `check` failure that put it
    here -- so the sites are settled before any length is measured, and the
    probe carries a symbol at exactly these and no others.

    What it asks is whether an info table ends immediately before this head,
    and a table's last line is a `.quad` or a `.long`, so the lines to read
    past are the ones that emit no bytes at all: another label, and the `.loc`
    a `-g` build interleaves. That is what makes the guard readable under
    `-g`, where every head follows the previous block's `_end`/`_proc_end`
    labels rather than an instruction.

    **The look-through is switched on by the file, and a `-g`-less assembly
    keeps the literal form byte for byte.** On the plain assembly the two
    forms differ: 422 heads against 395, and the extra 27 are one shape of
    loop rather than a scattering -- a pre-tested loop, whose head carries
    the block's label as well as its own, two labels at one address. What
    that does to the binary is **one pad**, a directive being a budget rather
    than a padding: of the 395 the assembler pads 156, 3941 bytes at a median
    of three multi-byte NOPs each, and with the 27 it pads 157, 3988 bytes.
    Twenty-six are declined; one fires and moves everything after it by 47
    bytes. So the cost is not the NOPs, it is that re-rolling placement
    re-bases every figure this page has published for a reason no strategy
    changed, and what the extra alignment buys is unmeasured. So it is not
    taken on the way past, and `LOOP_LOOKTHROUGH=1` is how a run asks for it
    -- Run 13's other half, which is what prices it. An
    assembly carrying `.loc` is a `-g` one, is nobody's basis (README's open
    list has why a `-g3` build is never timed), and gets the correct form;
    everything else is left exactly as it was.
    """
    out, prev = [], ''
    look = LOOKTHROUGH or any(l.lstrip().startswith('.loc') for l in src)
    for i, line in enumerate(src):
        s = line.strip()
        m = LABEL.match(s)
        if m and m.group(1) in heads and INSTR.match(prev):
            out.append((i, m.group(1)))
        if s and not s.startswith('#') and not (look and BYTELESS.match(s)):
            prev = s
    return out


def probe_cmd(args, path, ps, po):
    """The invocation we were handed, aimed at the probe copy instead."""
    cmd = [ps if a == path else a for a in args]
    if '-o' in cmd:
        cmd[cmd.index('-o') + 1] = po
    else:
        cmd += ['-o', po]
    return [REAL] + cmd


def symbols(obj, want):
    out = {}
    dis = subprocess.run(['objdump', '-t', obj],
                         capture_output=True, text=True).stdout
    for line in dis.split('\n'):
        f = line.split()
        if len(f) >= 2 and f[-1].startswith(want):
            try:
                out[f[-1]] = int(f[0], 16)
            except ValueError:
                pass
    return out


def lengths(src, st, args, path):
    """Each site's loop length, by assembling a probe copy and measuring it.

    A probe carries an ordinary local symbol at each head and one after each
    backward jump that targets it; `L` is then the smallest head-to-end
    distance the symbol table reports, which is the innermost loop at that
    head and is exactly what a disassembler would have to reconstruct.
    Symbols occupy no bytes, so the probe lays out as the real assembly will
    -- and `L` would survive a shift anyway, which is why it is the quantity
    measured here and `p` is left to the assembler.

    Returns {label: L}; a label absent from it is one the probe could not
    price, and the caller falls back to the unconditional directive for it.
    """
    if not MAXSKIP:
        return {}
    with tempfile.TemporaryDirectory(prefix='align-as-') as tmp:
        ps, po = os.path.join(tmp, 'probe.s'), os.path.join(tmp, 'probe.o')
        at = dict(st)
        back = {lab: i for i, lab in st}
        ends = collections.defaultdict(list)
        for j, line in enumerate(src):
            m = JUMP.match(line.strip())
            if m and m.group(1) in back:
                ends[j].append(m.group(1))
        out = []
        for i, line in enumerate(src):
            if i in at:
                out.append(f'{PROBE}Head_{i}:')
            out.append(line)
            for k, lab in enumerate(ends.get(i, ())):
                out.append(f'{PROBE}End_{back[lab]}_{i}_{k}:')
        with open(ps, 'w') as f:
            f.write('\n'.join(out))
        if subprocess.call(probe_cmd(args, path, ps, po),
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL):
            return {}
        sym = symbols(po, PROBE)
        span = {}
        for name, a in sym.items():
            if not name.startswith(f'{PROBE}End_'):
                continue
            i = name.split('_')[1]
            h = sym.get(f'{PROBE}Head_{i}')
            if h is None or a <= h:      # a jump that does not run backwards
                continue
            if i not in span or a - h < span[i]:
                span[i] = a - h
        return {lab: span[str(i)] for i, lab in st if str(i) in span}


def rewrite(path, args):
    """-> (emitted with a budget, fallen back on)."""
    global PAD
    with open(path) as f:
        src = f.read().split('\n')

    st = sites(src, heads_of(src))
    if not st:
        return 0, 0

    L = lengths(src, st, args, path)
    at, n, back = dict(st), 0, 0
    out = []
    for i, line in enumerate(src):
        if i in at:
            ln = L.get(at[i])
            if ln is None:
                out.append(f'\t.p2align\t{ALIGN}, 0x90')
                back += 1
            else:
                # (L-1) mod BOUND, so a loop longer than a line is moved when
                # -- and only when -- it would otherwise span one line more
                # than its length forces. It is L-1 whenever L fits a line.
                out.append(f'\t.p2align\t{ALIGN}, 0x90, {(ln - 1) % BOUND}')
                n += 1
        out.append(line)
    if PAD:
        out += ['\t.section .text', '\t.p2align 3', f'\t.space {PAD}, 0x90', '']
        PAD = 0        # one module's worth an invocation
    with open(path, 'w') as f:
        f.write('\n'.join(out))
    return n, back


def main():
    args = sys.argv[1:]
    n = back = 0
    for a in args:
        if a.endswith('.s') and os.path.exists(a):
            try:
                dn, db = rewrite(a, args)
                n, back = n + dn, back + db
            except Exception as e:           # never break a build over this
                print(f'align-as: {a}: {e}', file=sys.stderr)
    if os.environ.get('ALIGN_AS_VERBOSE'):
        if MAXSKIP:
            print(f'align-as: {n} loop head(s) given a max-skip budget, {back} '
                  f'without a measured length and so aligned unconditionally',
                  file=sys.stderr)
        else:
            print(f'align-as: aligned {back} loop head(s) unconditionally',
                  file=sys.stderr)
    return subprocess.call([REAL] + args)


if __name__ == '__main__':
    sys.exit(main())
