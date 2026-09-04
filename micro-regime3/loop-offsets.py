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

**Which arm owns a copy is a property of the binary, and only a `-g3` one has
it.** A plain build prints every copy under one mangled symbol, because these
arms compile to one worker and nothing per-arm survives: all eight sit inside
`Main_zdWT_info`, which spans 271 KB, and the assembly GHC hands
`align-as.py` carries 11 named labels, every one a string literal, against
18829 anonymous `.L` ones. The names are not there to emit. A `-g3` build
emits a per-block symbol (`Main_zdwgo7_svYG_entry` and siblings) with DWARF
line info, and **this tool then names each copy itself** -- `addr2line` for
the source line, the source file for the top-level binding containing it --
so the symbol column reads `fbMutOdoVecdims (Main.hs:1669)` instead. Nothing
changes for a binary carrying no line info, which is every build this README
timed before Run 13.

Read that way 2026-08-13, at `-fspec-constr` with `LOOP_MAXSKIP=1`: the
four-copy vecdims group is, in address order, `fbMutOdoVecdims`,
`fbMutOdoVecdimsAddIn`, `fbMutOdoVecdimsAddOut` and `fbMutOdoVecdimsAddBoth`,
and the pair beside it is `fbMutOdo` then `fbBuild`.
`fbMutOdoVecdimsAddBothDown` is in neither group because its loop is 24 bytes
and not 28, the count-down form's; `--len 24` finds it, and in that build it
is a singleton at offset 0.

**The two copies a `-g3` build lacks are the dead ones**, which is what the
naming establishes rather than assumes: the plain build's `build`/`mut-odo`
group has four copies and the `-g3` build's has two, and those two are the
two live arms. That confirms the `[dead, mut-odo, dead, build]` reading above
by a second route, and it is this tool's non-vacuity control for naming --
any scheme that names them must put `fbMutOdo` before `fbBuild` and must
reproduce the vecdims group in roster order.

**A `-g` build is a different program at every level, so it is a twin to read
and never a binary to time.** On the assembly GHC hands the assembler at
`-g3`, stripped of every `.loc`,
debug label and `.debug_*` section: 60056 instructions against the plain
build's 59991, of which +63 are `movq`, with register assignments differing
throughout -- register allocation and block order, not different arithmetic.
The timed loops themselves come out byte-identical, all three 28-byte groups
sharing a body across the two builds, but every offset differs and two copies
are gone. It was gated against a plain half of the same source and lost, at
5% on `build` and 3% on `mut-odo` against a 1.4% floor, which is why building
everything this way is refused, and `-g1` is no way round it -- README's open
list has both readings and what they rest on. The twin
is built beside the binary it explains, from the same source and shim:

    LOOP_MAXSKIP=1 cabal build micro --builddir=db-g3 \
      --ghc-options="-fspec-constr" --ghc-options="-g3" \
      --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"

and `rm -rf db-g3` with the binary afterwards, `.gitignore` covering the
builddir but not a copied-out probe binary. **Matching its copies to the
timed binary's is by proximity and by the instruction window around each
head**, and the window half is not reliable everywhere: it separates the
vecdims copies at 73 to 75 of 80, and falls to 10 to 13 on the
`build`/`mut-odo` group, whose surroundings `-g3` restructured when it
dropped the two dead copies.

Non-vacuity, and it is a known-answer control rather than an assertion. It
was settled against the pad probe's binaries, reproducing every offset
README records for them -- micro-pad0 [3, 53, 59, 45], micro-pad1 [27, 13,
19, 5], micro-pad6 [19, 5, 11, 61], whose second and fourth entries are
the documented `mut-odo` and `build` offsets -- before it was pointed at a
binary whose answer was unknown, which is the whole of its warrant. Those
binaries are deleted, and so is `micro-unaligned`, which stood as the
control after them: binaries are named `<run>-<half>` from Run 12 on, and
each run's are deleted with it, so no *binary* can hold this role for
long. The live control is the current pair's recorded fills -- for Run 12,
`run12-maxskip` [11, 0, 4, 0] and [24, 8, 0, 0] against `run12-maxskippa`
[4, 0, 4, 0] and [8, 8, 4, 4] -- which this tool must reproduce before it
is read for anything new. They are in README's open list and in the pair's
own `<prefix>-pair.txt` -- written by hand, with the recipe for each half
-- so the check outlives the binaries it was born on. **Those binaries are
deleted with their run**, which is how the previous control died, so what
has to survive is the recipe the note carries: the commit is recorded, and a
rebuild that reproduces the two md5s reproduces the offsets above. Re-prove
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

Its defects are kept as cases in `defects.py` -- objdump's status
and addr2line's -- and a fix here wants one there first.

    ./loop-offsets.py BINARY...          # 28-byte loop, the one this README prices
    ./loop-offsets.py --len 24 BINARY    # e.g. the count-down form
    ./loop-offsets.py --survey BINARY    # every loop that could fit a line
    ./loop-offsets.py --library A B      # do the two halves move the libraries
    ./loop-offsets.py --delta OLD NEW    # how far a rebuild moved the tracked
                                         #   loops: the pinning claim's reading
    ./loop-offsets.py B --match TWIN     # name B's straddlers off a -g3 twin
"""
import argparse
import collections
import os
import re
import subprocess
import sys

INSN = re.compile(r'^\s*([0-9a-f]+):\t((?:[0-9a-f]{2} )+)\s*\t?(\S+)\s*(.*)$')
SYM = re.compile(r'^([0-9a-f]+) <(.+)>:$')
JMP = re.compile(r'^j')
TARGET = re.compile(r'^([0-9a-f]+)\b')
LOC = re.compile(r'^(.*):(\d+)$')
TOP = re.compile(r'^([a-z]\w*)\s*(?:::|[^=]*=)')   # a top-level binding
KEYWORD = {'type', 'data', 'newtype', 'class', 'instance', 'import', 'module',
           'infix', 'infixl', 'infixr', 'foreign', 'pattern'}
LINE = 64  # the cache line, and the op cache's window on this Zen 3


def span_label(want):
    """What a report scanned, for its own header.

    `at most LINE B` and not `any length`: `--len 0` lifts the exact-size
    filter and NOT the cache-line cap, `scan` dropping every loop wider
    than a line whatever `want` is. The old wording read as this binary's
    whole loop count, which it is not -- `--len 128` finds loops the `any
    length` report did not contain. Same phrasing as --survey's header, and
    a function rather than an expression so that saying it wrong is
    checkable without a binary to scan.
    """
    return 'at most %d B' % LINE if want is None else '%d B' % want


def innermost(path):
    """{head address: the shortest loop starting there}.

    Every mode wants a binary's loops one per head rather than one per
    jump, an outer loop and the inner one it contains sharing a head, and
    each mode built the dict for itself in the same five lines.
    """
    heads = {}
    for f in scan(path, None):
        cur = heads.get(f['start'])
        if cur is None or f['len'] < cur['len']:
            heads[f['start']] = f
    return heads


def listing(path):
    """`objdump -d -j .text` over `path` -- or `path` itself, where it is a
    saved listing: a text file rather than ELF, carrying objdump's own
    `Disassembly of section` header. A run's binary dies at the deletion
    offer, so a case that holds one of its sites holds the listing of that
    site instead, which is the one form of it that can be tracked. Anything
    else goes to objdump, whose refusal is the answer for a file that is
    neither.
    """
    try:
        with open(path, 'rb') as f:
            head = f.read(4096)
    except OSError:
        head = b''
    if head[:4] != b'\x7fELF' and b'Disassembly of section' in head:
        with open(path) as f:
            return f.read()
    # objdump's verdict and not merely its stdout. A mistyped or missing
    # binary, or one with no `.text`, left `dis` empty and every mode then
    # read it as a binary with no loops: `--survey no-such-binary` printed
    # `0 self-loops ... at offset 0: 0, still straddling: 0` and exited 0,
    # a placement report reading as a perfect result for a file that was
    # never opened. Found 2026-08-17 by review.
    cmd = ['objdump', '-d', '-j', '.text', path]
    try:
        got = subprocess.run(cmd, capture_output=True, text=True)
    except OSError as exc:
        sys.exit('%s: %s' % (' '.join(cmd), exc))
    if got.returncode != 0:
        sys.exit('%s exited %d: %s' % (' '.join(cmd), got.returncode,
                                       got.stderr.strip() or '(no stderr)'))
    return got.stdout


def reaches(insns, k, n, targets):
    """Whether straight-line flow from the head at `k` reaches the closing
    branch at `n`: fall-through past anything but an unconditional
    transfer, plus any instruction some direct branch targets.

    A backward branch whose bytes sum is not yet a loop. `objdump -d`
    sweeps tables-next-to-code linearly, so an info table decodes as
    instructions, and a word of one can decode as a backward `js` whose
    span the bytes before it happen to fill: `run25-g912`'s survey read
    FIVE straddling self-loops in Main-compiled code where its `-g3` twin
    and every other binary read four, the fifth closed by the SRT word of
    the table in front of `$wrun` -- `0x013dd878`, low byte `0x78 0xd8`,
    `js -40` -- over a body that was a continuation's tail, a heap-check
    jump, a pad and twenty bytes of table, which control leaves at its
    second instruction. Read 2026-09-04 and named by the twin refusing it.
    Every self-loop this removes from the four real binaries and two twins
    of that day is such a word behind a `jmp` and a pad, one to four per
    binary; the blanket form, refusing any unconditional transfer inside
    the body, took fourteen real loops with them, so this one follows the
    flow instead. Survey totals recorded before 2026-09-04 are higher than
    this reads by that few, and stand as taken.
    """
    live = False
    for i in range(k, n + 1):
        addr, _nb, _raw, mnem, _op, _sym = insns[i]
        if i == k or addr in targets:
            live = True
        if i == n:
            return live
        if live and (mnem in ('jmp', 'jmpq') or mnem.startswith('ret')):
            live = False
    return False


def scan(path, length):
    dis = listing(path)
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
    targets = set()
    for _addr, _nb, _raw, mnem, op, _sym in insns:
        if JMP.match(mnem) or mnem.startswith('call'):
            t = TARGET.match(op.strip())
            if t:
                targets.add(int(t.group(1), 16))
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
        if not reaches(insns, k, n, targets):
            continue
        found.append({'start': tgt, 'bytes': body, 'sym': insns[k][5],
                      'len': span, 'ninsn': n - k + 1, 'mod': tgt % LINE,
                      'straddles': tgt % LINE + span > LINE})
    return found


def bindings(src):
    """(line, name) for every top-level binding of a Haskell source file."""
    out = []
    with open(src) as f:
        for n, line in enumerate(f, 1):
            m = TOP.match(line)
            if m and m.group(1) not in KEYWORD:
                out.append((n, m.group(1)))
    return out


def arms(path, addrs):
    """{addr: 'fbMutOdoVecdims (Main.hs:1669)'}, or {} without line info.

    The arm is the top-level binding the line falls in, read off the source
    file `addr2line` names, so this is the source's own vocabulary rather
    than a table kept here that a rename could rot. One `addr2line` for every
    address asked about; a build with no DWARF answers `??` to all of them
    and the caller falls back to the mangled symbol.

    That fallback is the ANSWER to a question addr2line took, and it exits 0
    giving it, so the two ways it can fail to take the question at all are
    told apart from it here and said on stderr rather than read as a build
    without DWARF. Neither refuses, unlike `scan` above: what a name buys is
    legibility, and the mangled symbol is already the documented substitute.
    Measured 2026-08-17: no DWARF is `??:0` at exit 0, an unreadable file is
    exit 1, and an absent addr2line raises.
    """
    if not addrs:
        return {}
    cmd = ['addr2line', '-e', path] + [f'0x{a:x}' for a in addrs]
    try:
        got = subprocess.run(cmd, capture_output=True, text=True)
    except OSError as exc:
        sys.stderr.write('addr2line: %s; arms are named by their mangled'
                         ' symbol\n' % exc)
        return {}
    if got.returncode != 0:
        sys.stderr.write('addr2line -e %s exited %d: %s; arms are named by'
                         ' their mangled symbol\n'
                         % (path, got.returncode,
                            got.stderr.strip() or '(no stderr)'))
        return {}
    out = got.stdout.split('\n')
    src, named = {}, {}
    for a, loc in zip(addrs, out):
        m = LOC.match(loc.strip())
        if not m or not os.path.exists(m.group(1)):
            continue
        f, n = m.group(1), int(m.group(2))
        if f not in src:
            src[f] = bindings(f)
        name = None
        for ln, nm in src[f]:
            if ln > n:
                break
            name = nm
        where = f'{os.path.basename(f)}:{n}'
        named[a] = f'{name} ({where})' if name else where
    return named


def survey(path, want='_Main_'):
    """Every self-loop of any length, and how many can still straddle.

    Only a loop no longer than a line can be rescued by an offset outright,
    so that is the population the count is about: the loops an alignment
    takes from two lines to one. Everything longer spans several lines in
    any build, but fewest from a line boundary, and one line fewer crossed
    is worth having too -- which is why the shim aligns every head it can
    regardless of the loop's length; that gain is real and not one this
    count certifies. The default `want` restricts this to code GHC compiled
    here rather than to the libraries linked in, which no shim on -pgma
    reaches.
    """
    mine = [f for f in innermost(path).values() if want in (f['sym'] or '')]
    at0 = [f for f in mine if f['mod'] == 0]
    strad = [f for f in mine if f['straddles']]
    print(f'{path}: {len(mine)} self-loops of at most {LINE} B in '
          f'{want}-compiled code')
    print(f'   at offset 0        : {len(at0)}')
    print(f'   still straddling   : {len(strad)}')
    worst = sorted(strad, key=lambda x: -x['len'])[:10]
    named = arms(path, [f['start'] for f in worst])
    for f in worst:
        print(f'      0x{f["start"]:x}  mod {LINE} = {f["mod"]:2d}, '
              f'{f["len"]} B  {named.get(f["start"]) or f["sym"]}')


def match(timed, twin, want='_Main_'):
    """Name the timed binary's straddling loops off a -g3 twin, by BYTE
    IDENTITY and never by address or proximity.

    Post-run step 0 owes this and did it by hand for two runs: `objdump`
    over both binaries at addresses guessed from the survey, compared by
    eye (Run 23, 2026-09-02). The rule the step states is that a loop is
    named from the twin only where the twin holds a byte-identical copy,
    and refused where it holds none or fewer copies than the timed binary
    -- which is what makes a negative honest. So: every loop the survey
    counts as straddling in `timed` is looked up by its bytes among the
    twin's loops as the survey counts them, at most a line long, which a
    byte-identical copy of one always is; a unique match is named through the
    twin's DWARF, several matches are listed, and none is a refusal said
    aloud. The count check is printed first, twin against timed, as the
    survey counts them.
    """
    mine = [f for f in innermost(timed).values() if want in (f['sym'] or '')]
    theirs = [f for f in innermost(twin).values() if want in (f['sym'] or '')]
    strad = sorted((f for f in mine if f['straddles']), key=lambda f: f['start'])
    print(f'{timed}: {len(mine)} self-loops of at most {LINE} B in '
          f'{want}-compiled code, {len(strad)} straddling; the twin {twin} '
          f'holds {len(theirs)}, '
          f'{sum(1 for f in theirs if f["straddles"])} straddling')
    if len(theirs) < len(mine):
        print('   the twin carries FEWER loops than the timed binary, so a'
              ' name below rests on its own byte match and the population'
              ' comparison is refused')
    by_bytes = collections.defaultdict(list)
    for f in theirs:
        by_bytes[f['bytes']].append(f)
    named = arms(twin, sorted({f['start'] for fs in by_bytes.values()
                               for f in fs}))
    for f in strad:
        hits = by_bytes.get(f['bytes'], [])
        where = (f'0x{f["start"]:x}  mod {LINE} = {f["mod"]:2d}, '
                 f'{f["len"]} B')
        if not hits:
            print(f'      {where}  NOT NAMED: the twin holds no byte-identical'
                  f' copy')
        elif len(hits) == 1:
            h = hits[0]
            print(f'      {where}  {named.get(h["start"]) or h["sym"]}  '
                  f'(twin 0x{h["start"]:x}, mod {h["mod"]}, '
                  f'{"straddles" if h["straddles"] else "fits"} there)')
        else:
            print(f'      {where}  {len(hits)} byte-identical copies in the'
                  f' twin: '
                  + '; '.join(f'{named.get(h["start"]) or h["sym"]} at '
                              f'0x{h["start"]:x}' for h in hits))


def delta(old, new, length, min_copies, want='_Main_'):
    """How far a rebuild moved the tracked loops, group by group.

    The pinning claim is read at every build that brings a new timed
    function -- the fills on one build either side, before anything else
    changes -- and reading it means answering three questions of the
    tracked groups: are the mod-64 offsets preserved, does any address
    survive to the byte, and do the heads move by one constant. Nothing
    here subtracted the two address lists until 2026-09-04. Run 24's
    preparation did that arithmetic by hand and recorded the improvisation
    in its note; Run 25's improvised it again, which is two runs paying for
    a subtraction, on the reading the claim's whole record rests on.

    Groups are matched by the loop body's BYTES, which is the identity
    `--match` uses and the only one that survives a relink moving every
    address. A group on one side alone is reported as such rather than
    dropped: that is what a change of compiler produces, and Run 24's HEAD
    half grew a third group the basis did not have. WITHIN a group the
    copies are paired by address order, the i-th old head with the i-th
    new, which is what `survive to the byte` and the displacements are
    read over: a group that keeps its count while one arm's copy leaves
    and another's lands reads as displacements, and can read as an address
    surviving, with nothing here to say the pairing slipped. The `-g3`
    twins of post-run step 0 are what name a copy; this mode only counts.

    The population is `want`'s, Main-compiled code as `--match` and
    `--survey` take it, and the linked libraries' groups are left to
    `--library`: read without the filter, the statistics Quantile pair
    stood among the tracked groups on both halves of Run 25 and in the
    summary line a note would copy (2026-09-04).

    This is a reading and not a gate. It exits 0 whatever it finds, because
    what a given displacement MEANS is the README's to say (*Why the build's
    three rules are what they are*), and a threshold here would be this
    file asserting a claim the runs are still measuring.
    """
    sides = []
    left = 0
    for path in (old, new):
        groups = collections.defaultdict(list)
        for f in scan(path, length):
            if want in (f['sym'] or ''):
                groups[f['bytes']].append(f)
            else:
                left += 1
        for fs in groups.values():
            fs.sort(key=lambda f: f['start'])
        sides.append(groups)
    og, ng = sides
    span = span_label(length)
    print(f'== {old} -> {new}: {span} loops in {want}-compiled code, '
          f'matched by body bytes; {left} library loop(s) left to --library')
    # EITHER SIDE meeting the threshold is enough. Taking it of the OLD
    # side alone dropped, in silence, exactly the group whose copy count is
    # the finding: one that grew from a copy or two to six is below the
    # threshold in `og` and present in it, so it failed the first test and
    # was excluded from the second by `k not in og`.
    keys = [k for k in og
            if len(og[k]) >= min_copies or len(ng.get(k, ())) >= min_copies]
    keys += [k for k in ng if k not in og and len(ng[k]) >= min_copies]
    preserved = moved = one_sided = recount = compared = 0
    for k in sorted(keys, key=lambda k: -max(len(og.get(k, ())),
                                             len(ng.get(k, ())))):
        a, b = og.get(k, []), ng.get(k, [])
        if not a or not b:
            where = new if b else old
            fs = b or a
            one_sided += 1
            print(f'   {len(fs)} copies, {fs[0]["len"]} B, '
                  f'{fs[0]["ninsn"]} insns, offsets '
                  f'{[f["mod"] for f in fs]} -- IN {where} ONLY')
            continue
        oo = [f['mod'] for f in a]
        nn = [f['mod'] for f in b]
        print(f'   {len(a)} -> {len(b)} copies, {a[0]["len"]} B, '
              f'{a[0]["ninsn"]} insns')
        if len(a) != len(b):
            recount += 1
            print(f'      copy COUNT moved: offsets {oo} -> {nn}')
            continue
        compared += 1
        if oo == nn:
            preserved += 1
            print(f'      every mod-{LINE} offset preserved: {oo}')
        else:
            print(f'      offsets MOVED: {oo} -> {nn}')
        kept = [f['start'] for f, g in zip(a, b) if f['start'] == g['start']]
        disp = [g['start'] - f['start'] for f, g in zip(a, b)]
        if kept:
            print('      %d address(es) survive to the byte: %s'
                  % (len(kept), ', '.join('0x%x' % v for v in kept)))
        else:
            print('      NO address survives to the byte')
        # The displacement SET and not the list: what the README's readings
        # turn on is how many constants the heads moved by, one being the
        # weakest disturbance on record and none of them a constant the
        # strongest.
        uniq = sorted(set(d for d in disp if d))
        if not uniq:
            print('      nothing moved')
        else:
            moved += 1
            print('      %d displacement(s): %s'
                  % (len(uniq), ', '.join(
                      '0x%x%s' % (v, '' if v % LINE == 0
                                  else ' (NOT a whole line)')
                      for v in uniq)))
    # TWO LINES AND NOT ONE, because the four numbers are of two kinds and
    # a single `of N group(s): ...` invited reading them as a partition
    # summing to N -- which they do not, a group both keeping its offsets
    # and moving being counted in each. The first line partitions; the
    # second states two properties over the part it makes sense of.
    # The unmatched groups are in the summary at all because without them
    # a run where nothing matched printed `0 kept every offset; 0 moved at
    # all`, which reads as `nothing moved` and means `nothing was
    # compared` -- measured on /bin/sh against /bin/cat, whose every group
    # is one-sided (2026-09-04, both faults).
    print(f'   {len(keys)} group(s) read = {compared} compared + '
          f'{recount} changed copy count + {one_sided} matched nothing '
          f'on the other side')
    if compared:
        print(f'   of the {compared} compared: {preserved} kept every '
              f'offset, {moved} moved at all')


def library(a, b):
    """How much the two halves agree about where the LIBRARIES' loops sit.

    A pair is meant to differ in the code compiled here and nowhere else,
    and this is the half of that nothing else measures: `--survey` and the
    default mode are scoped to `_Main_`, which is exactly the code a pair is
    allowed to move. The libraries are what must sit still, and a shim on
    `-pgma` never reaches them, so where they have moved it is because
    everything after a size change was displaced.

    That is not hypothetical and it is why the aligned/unaligned pairing
    needed a padding step at all: aligning grew `.text` by 12 KB, and of
    867 library symbols carrying a short loop, 856 landed at a different
    address. Matching the size alone left the delta at 32 mod 64, the worst
    shift available; matching size AND phase left 95% of the library loops
    at the same offset and 98% in the same straddle state. A pair of two
    shims, which is what is built now, has no padding step and no guarantee
    -- it has whatever its two recipes happen to give, and this is how to
    know which.

    Non-vacuous 2026-08-14 on Run 13's pair: 899 common loops, 96.8% phase
    and 98.8% straddle agreement, the same figures reached through
    the pair builder's own reading, before that script was deleted. A
    binary compared with
    itself reads 100.0% both ways, and the two counts differ from `--survey`
    because that one reports Main's loops and this one everything else.

    **Those counts were SYMBOLS**, one per symbol however many loops it
    carried, which is the keying corrected below on 2026-08-16. Run 14's
    pair reads 1723 common loops at 100.0% and 100.0% where the symbol
    keying said 953, so a count from before that date is not comparable
    with one after it, and the percentages before it covered about half
    the library.

    The self-comparison proves nothing about the percentages, reading
    100.0% by construction, and neither does an unrelated build:
    `run14-lookrts` against a `-g3` twin shares 1013 loops and still reads
    100.0% both ways, the libraries genuinely sitting still. What does
    discriminate, 2026-08-16: shifting one half's loops by a byte inside
    the reader takes the same pair to 0.0% phase and 97.8% straddle.
    """
    def heads(path):
        # Keyed by the LOOP and not by the symbol carrying it. Keying by
        # symbol collapsed every symbol holding more than one short loop
        # to whichever address iterated last -- 268 of 953 symbols here,
        # 776 of 1729 loops dropped -- so the percentages below covered
        # 55% of the library and said 953 where they had found 1729. The
        # body pairs the same code across the two halves, which is what
        # the comparison is for, and the repeat counter separates two
        # identical loops in one symbol; a loop present in one half only
        # falls out of `common` and is visible in the count.
        out, seen = {}, collections.Counter()
        for f in sorted(innermost(path).values(), key=lambda f: f['start']):
            sym = f['sym'] or ''
            if '_Main_' in sym:
                continue
            seen[sym, f['bytes']] += 1
            out[sym, f['bytes'], seen[sym, f['bytes']]] = f
        return out
    A, X = heads(a), heads(b)
    common = set(A) & set(X)
    if not common:
        sys.exit('no library symbol carries a short loop in both binaries')
    phase = 100.0 * sum(1 for s in common if A[s]['mod'] == X[s]['mod'])
    strad = 100.0 * sum(1 for s in common
                        if A[s]['straddles'] == X[s]['straddles'])
    print(f'{a} vs {b}: {len(common)} library self-loops in both')
    print(f'   same offset in line: {phase / len(common):.1f}%')
    print(f'   same straddle state: {strad / len(common):.1f}%')


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('binary', nargs='+')
    p.add_argument('--len', type=int, default=28,
                   help='loop length in bytes, or 0 for every length a cache '
                        'line can hold (default 28)')
    p.add_argument('--min-copies', type=int, default=2,
                   help='only report groups with at least this many copies')
    p.add_argument('--survey', action='store_true',
                   help='every self-loop of any length in this binary\'s own '
                        'compiled code, and how many can still straddle')
    p.add_argument('--delta', action='store_true',
                   help='how far a rebuild moved the tracked loops: OLD NEW,'
                        ' matched by body bytes -- the pinning claim\'s'
                        ' reading, which the run chapter asks for at every'
                        ' build bringing a new timed function')
    p.add_argument('--code', default='_Main_', metavar='SUBSTR',
                   help='--delta\'s population: loops in code whose symbol'
                        ' carries SUBSTR, _Main_ by default as --survey and'
                        ' --match take it; --code \'\' is every loop')
    p.add_argument('--library', action='store_true',
                   help='how far two halves agree about where the LINKED '
                        'libraries\' loops sit, which a pair must not move')
    p.add_argument('--match', metavar='TWIN',
                   help='name the binary\'s straddling loops off this -g3 '
                        'twin by byte identity, refusing where the twin '
                        'holds no identical copy -- post-run step 0')
    args = p.parse_args()

    # ONE REPORT an invocation. The dispatch below is an if/return
    # chain, so `--survey --library A B` printed the library report and
    # dropped --survey without a word -- read-run.py's one-mode family,
    # found 2026-08-23 by hunting that family here. And the two
    # grouped-report knobs are refused where nothing reads them:
    # --survey scans every length up to the line by design and
    # --library keys on the loop bytes, so under either a --len or
    # --min-copies was accepted and honoured by nobody --
    # `--survey --len 24` answered with the at-most-64 report.
    if args.delta:
        # Its own mode and not a flavour of the plain report: that one takes
        # any number of binaries and prints each alone, where this one is a
        # subtraction and wants exactly two, in the order OLD NEW.
        if sum((args.survey, args.library, bool(args.match))):
            sys.exit('--delta is its own mode: not with --survey, --library'
                     ' or --match')
        if len(args.binary) != 2:
            sys.exit('--delta takes exactly two binaries, OLD then NEW')
        delta(args.binary[0], args.binary[1],
              None if args.len == 0 else args.len, args.min_copies,
              args.code)
        return
    if args.survey and args.library:
        p.error('--survey and --library are two reports, not one: the'
                ' dispatch runs --library and drops --survey without a'
                ' word')
    unread = [n for n, v, d in (('--len', args.len, 28),
                                ('--min-copies', args.min_copies, 2),
                                ('--code', args.code, '_Main_'))
              if v != d]
    if '--code' in unread:
        p.error('--code is read by --delta alone')
    if unread and (args.survey or args.library):
        p.error('%s %s read only by the grouped report: under --survey or'
                ' --library it would be accepted and honoured by nobody'
                % (' and '.join(unread),
                   'is' if len(unread) == 1 else 'are'))

    if args.match and (args.survey or args.library):
        p.error('--match is a report of its own and takes one timed binary')
    if args.match:
        if len(args.binary) != 1:
            p.error('--match TWIN takes exactly one timed binary')
        if unread:
            p.error('%s read only by the grouped report' % ' and '.join(unread))
        match(args.binary[0], args.match)
        return

    if args.library:
        if len(args.binary) != 2:
            p.error('--library compares two binaries')
        library(*args.binary)
        return

    if args.survey:
        for path in args.binary:
            survey(path)
        return

    # `--len 0` widens the grouped report to every loop a line can hold.
    # The 28 the default names is the run-fill loop this README prices, and
    # for four runs it was also the whole tracked set -- which is what the
    # NOPs question tripped over on 2026-08-14: the arms that lose most to
    # an unconditional shim carry no 28-byte loop at all, so the report
    # that would attribute the loss could not see them
    # (README.md#what-is-open). The length then varies within the report,
    # so each group prints its own.
    want = None if args.len == 0 else args.len
    for path in args.binary:
        found = scan(path, want)
        # One pass gives the count and the members together, where a
        # Counter gave the count and every group then rescanned `found`
        # for its own. Insertion order is first-encountered either way, so
        # the sort below prints what `most_common` printed.
        groups = collections.defaultdict(list)
        for f in found:
            groups[f['bytes']].append(f)
        named = arms(path, [f['start'] for f in found])
        span = span_label(want)
        print(f'== {path}: {len(found)} self-loops of {span} in '
              f'{len(groups)} distinct byte-sequences')
        # A group under the threshold is COUNTED, not merely skipped: the
        # docstring's own `--len 24` example reports a singleton, which at
        # the default of 2 printed the header and nothing else, with nothing
        # saying a group had been suppressed. Found 2026-08-17 by review.
        suppressed = 0
        for body, fs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            count = len(fs)
            if count < args.min_copies:
                suppressed += 1
                continue
            print(f'   {count} copies, {fs[0]["len"]} B, '
                  f'{fs[0]["ninsn"]} insns, '
                  f'offsets {[f["mod"] for f in fs]}')
            for f in fs:
                print(f'      0x{f["start"]:x}  mod {LINE} = {f["mod"]:2d}  '
                      f'{"STRADDLES" if f["straddles"] else "fits     "}  '
                      f'{named.get(f["start"]) or f["sym"]}')
        if suppressed:
            print(f'   {suppressed} group(s) suppressed, having fewer than '
                  f'{args.min_copies} copies: --min-copies 1 lists them')


if __name__ == '__main__':
    main()
