#!/usr/bin/env python3
"""Find a binary's copies of a hot loop and report where each lands in its
cache line -- the cheap half of the placement question.

README.md's floor section prices a straddled copy of the 28-byte run-fill at
1.19 against a resident one, so before crediting any margin under about a
fifth to a strategy, ask this first: it is one objdump against a
quiet-machine window. Ask it first, but do not assume the answer: Run 10 read
three arms of one family at four placements each, none of them straddling in
two of the three, and their 16% stayed. Placement is the cheapest
explanation to rule out, not the likeliest to be right.

A loop copy is found structurally rather than by symbol -- a backward branch
whose target is exactly LEN bytes back, with the intervening instructions
accounting for those bytes -- and copies are then grouped by their raw bytes,
so "N byte-identical copies of one loop" is something this reads rather than
assumes. That matters because the interesting arms compile to the same worker:
the group, not the symbol, is what identifies them.

Reading the output: the copies are listed in address order, and for the
`build`/`mut-odo` group in this suite's binaries that order is
[dead, mut-odo, dead, build] -- one copy per arm is the mismatched-length
`fail` join, which cannot run on a well-formed shape, and it is the executed
one that the penalty applies to.

Non-vacuity, and it is a known-answer control rather than an assertion. It
was settled against the pad probe's binaries, reproducing every offset README
records for them -- micro-pad0 [3, 53, 59, 45], micro-pad1 [27, 13, 19, 5],
micro-pad6 [19, 5, 11, 61], whose second and fourth entries are the
documented `mut-odo` and `build` offsets -- before it was pointed at a binary
whose answer was unknown, which is the whole of its warrant. Those binaries
are deleted, and so is `micro-unaligned`, which stood as the control after
them: binaries are named `<run>-<half>` from Run 12 on, and each run's are
deleted with it, so no *binary* can hold this role for long. The live control
is the current pair's recorded fills -- for Run 12, `run12-maxskip`
[11, 0, 4, 0] and [24, 8, 0, 0] against `run12-maxskippa` [4, 0, 4, 0] and
[8, 8, 4, 4] -- which this tool must reproduce before it is read for anything
new. They are in README's open list and in the pair's own `<prefix>-pair.txt`,
which `make-pair.py` writes beside the binaries where it built them, so the
check outlives the binaries it was born on. **Those binaries are deleted with
their run**, which is how the previous control died, so what has to survive
is the recipe: `make-pair.py` is deterministic, the commit is recorded, and
a rebuild that reproduces the two md5s reproduces the offsets above. Re-prove
this against a known answer before pointing it at a new one.

**`--survey`'s population size is not comparable between binaries whose
layout differs**, which is the one way to misuse the mode. It counts loops
this tool can *resolve*, and `objdump -d` sweeps linearly over
tables-next-to-code, so shifting code by arbitrary padding changes where the
sweep mis-decodes: measured 2026-08-11, Main's backward jumps hold at 1580
against 1583 between the aligned and unaligned halves while targets not
decoded as an instruction start go 613 to 777, which is the whole of why one
reads 115 short loops and the other 101. The straddle count *within* one
binary is sound; a difference in the totals between two is the disassembler.

    ./loop-offsets.py BINARY...          # 28-byte loop, the one this page prices
    ./loop-offsets.py --len 24 BINARY    # e.g. the count-down form
    ./loop-offsets.py --survey BINARY    # every loop that could fit a line
"""
import argparse
import collections
import re
import subprocess

INSN = re.compile(r'^\s*([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*\t?(\S+)\s*(.*)$')
SYM = re.compile(r'^([0-9a-f]+) <(.+)>:$')
JMP = re.compile(r'^j')
TARGET = re.compile(r'^([0-9a-f]+)\b')
LINE = 64  # the cache line, and the op cache's window on this Zen 3


def scan(path, length):
    dis = subprocess.run(['objdump', '-d', '-j', '.text', path],
                         capture_output=True, text=True).stdout
    cur = None
    insns = []
    for line in dis.split('\n'):
        m = SYM.match(line)
        if m:
            cur = m.group(2)
            continue
        m = INSN.match(line)
        if m:
            insns.append((int(m.group(1), 16), len(m.group(2).split()),
                          ''.join(m.group(2).split()), m.group(3),
                          m.group(4), cur))

    at = {i[0]: n for n, i in enumerate(insns)}
    found = []
    for n, (addr, nb, _raw, mnem, op, _sym) in enumerate(insns):
        if not JMP.match(mnem):
            continue
        t = TARGET.match(op.strip())
        if not t:
            continue
        tgt = int(t.group(1), 16)
        if tgt >= addr:
            continue
        span = (addr + nb) - tgt
        # length=None surveys every loop that could fit a line; otherwise the
        # span must be exactly the length asked for.
        if length is None:
            if span > LINE:
                continue
        elif span != length:
            continue
        k = at.get(tgt)
        if k is None:
            continue
        body = ''.join(i[2] for i in insns[k:n + 1])
        if len(body) != 2 * span:     # a jump into the middle of an instruction
            continue
        found.append({'start': tgt, 'bytes': body, 'sym': insns[k][5],
                      'len': span, 'ninsn': n - k + 1, 'mod': tgt % LINE,
                      'straddles': tgt % LINE + span > LINE})
    return found


def survey(path, want='_Main_'):
    """Every self-loop of any length, and how many can still straddle.

    Only a loop no longer than a line can be rescued by an offset at all, so
    that is the population the count is about; everything longer spans several
    lines in any build. The default `want` restricts this to code GHC compiled
    here rather than to the libraries linked in, which no shim on -pgma
    reaches.
    """
    heads = {}
    for f in scan(path, None):
        cur = heads.get(f['start'])
        if cur is None or f['len'] < cur['len']:   # innermost loop at a head
            heads[f['start']] = f
    found = list(heads.values())
    mine = [f for f in found if want in (f['sym'] or '')]
    at0 = [f for f in mine if f['mod'] == 0]
    strad = [f for f in mine if f['straddles']]
    print(f'{path}: {len(mine)} self-loops of at most {LINE} B in '
          f'{want}-compiled code')
    print(f'   at offset 0        : {len(at0)}')
    print(f'   still straddling   : {len(strad)}')
    for f in sorted(strad, key=lambda x: -x['len'])[:10]:
        print(f'      0x{f["start"]:x}  mod {LINE} = {f["mod"]:2d}, '
              f'{f["len"]} B  {f["sym"]}')


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('binary', nargs='+')
    p.add_argument('--len', type=int, default=28,
                   help='loop length in bytes (default 28)')
    p.add_argument('--min-copies', type=int, default=2,
                   help='only report groups with at least this many copies')
    p.add_argument('--survey', action='store_true',
                   help='every self-loop of any length in this binary\'s own '
                        'compiled code, and how many can still straddle')
    args = p.parse_args()

    if args.survey:
        for path in args.binary:
            survey(path)
        return

    for path in args.binary:
        found = scan(path, args.len)
        groups = collections.Counter(f['bytes'] for f in found)
        print(f'== {path}: {len(found)} self-loops of {args.len} B in '
              f'{len(groups)} distinct byte-sequences')
        for body, count in groups.most_common():
            if count < args.min_copies:
                continue
            fs = [f for f in found if f['bytes'] == body]
            print(f'   {count} copies, {fs[0]["ninsn"]} insns, '
                  f'offsets {[f["mod"] for f in fs]}')
            for f in fs:
                print(f'      0x{f["start"]:x}  mod {LINE} = {f["mod"]:2d}  '
                      f'{"STRADDLES" if f["straddles"] else "fits     "}  '
                      f'{f["sym"]}')


if __name__ == '__main__':
    main()
