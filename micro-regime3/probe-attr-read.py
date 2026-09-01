#!/usr/bin/env python3
"""Bucket a probe-attr histogram by ROLE, and difference the two arms.

    ./probe-attr-read.py probe-attr-<shape>.txt

perf gives instructions per source line; the question item 4 asks is
whether the excess sits in the element loop or in the loop nest around
it, which is a question about spans of lines and not about lines.  The
spans are derived from Main.hs by anchor phrase rather than written down,
so an edit that moves the file moves them with it and a phrase that stops
being unique fails loudly instead of silently mapping to the wrong span.

The two arms are not symmetric in source -- stage one carries its run
loop inside `go` where stage two has it in `runsWith` -- so the roles
compared are `fill`, the innermost element loop of each, and `driver`,
everything else inside the same function.  `harness` is the shared
forcing pass, which is the control: it must come out equal, both arms
being timed through it.

Exit 2 on usage, a lost anchor or a file with no arm sections, 1 if a file
names an arm this does not know, 0 clean.
"""
import re
import sys


def die(msg):
    """Exit 2 -- did not run -- rather than `sys.exit(str)`'s 1, which is
    the code a finding gets."""
    sys.stderr.write(msg.rstrip('\n') + '\n')
    sys.exit(2)

# arm -> (the function's own name, which IS unique, then the sub-anchors
# searched from it). The sub-anchors must NOT be required unique in the
# file: `let writeRun !outPos !baseOff =` occurs seventeen times, the
# whole add-in-leaf family sharing that text, which is what a first
# version of this asserted and what it refused on. Unique WITHIN the
# function is the property that holds and the one checked.
FUNCS = {
    'lib-stage1': 'fbMutOdoVecdimsAddInLeafU2 sh (T (Strides ats) ao v)',
    'lib-stage2': 'fillStage2 sh ats !ao !l !v = VS.create',
}
# FOUR ROLES AND NOT TWO, because the short-run residue is not where the
# long-run one was: an inner run of three does ONE unrolled pair and then
# the epilogue, so the loop's ends are paid once a run where its body is
# paid once a pair, and lumping them hides exactly the term that matters
# on a conv-shaped view. `ends` is the per-run prologue and epilogue,
# `loop` the unrolled body, `run` the loop over runs, `odo` the odometer
# levels above it. The two arms are not symmetric in source -- stage one
# writes its run loop into `go` where stage two reaches it through
# `runsWith` -- so `run` is each arm's own way of doing that, which is the
# comparison the question wants.
SPANS = {
    ('lib-stage1', 'ends'): ('  let writeRun !outPos !baseOff =',
                             '                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)'),
    ('lib-stage1', 'loop'): ('              | otherwise = do',
                             '        in  inner outPos baseOff'),
    ('lib-stage1', 'run'): ('      go !lev !outPos !baseOff',
                            '            in  run n outPos baseOff'),
    ('lib-stage1', 'odo'): ('        | otherwise =',
                            '  _ <- go 0 0 ao'),
    ('lib-stage2', 'ends'): ('  let {-# INLINE writeRunStep #-}',
                             '                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)'),
    ('lib-stage2', 'loop'): ('              | otherwise = do',
                             '        in  inner outPos baseOff'),
    ('lib-stage2', 'run'): ('      {-# INLINE writeRunSet #-}',
                            '            in  run n outPos baseOff'),
    ('lib-stage2', 'odo'): ('      go !lev !outPos !baseOff',
                            '  _ <- go 0 0 ao'),
}
ROLES = ['ends', 'loop', 'run', 'odo']

# The shared forcing pass, `VS.sum . f sh`, which both arms are timed
# through: it is the control, and it must come out equal.
HARNESS = re.compile(r'^\s*arm sh a \(n, (Fill|Term)')


def spans(main_hs):
    src = open(main_hs).read()
    lines = src.splitlines()
    starts = {}
    for arm, name in FUNCS.items():
        if src.count(name) != 1:
            die('%s does not name one definition in %s (%d matches)'
                     % (arm, main_hs, src.count(name)))
        starts[arm] = src[:src.index(name)].count('\n')
    out = {}
    for (arm, role), (a, b) in SPANS.items():
        i = starts[arm]
        lo = hi = None
        for k in range(i, len(lines)):
            if lo is None and lines[k] == a:
                lo = k + 1
            elif lo is not None and lines[k] == b:
                hi = k + 1
                break
        if lo is None or hi is None:
            die('span %s/%s not found after line %d of %s'
                     % (arm, role, i + 1, main_hs))
        out[(arm, role)] = (lo, hi)
    # Spans are trimmed against each other in ROLE order, an opening
    # anchor being allowed to sit on the previous role's closing line --
    # which is how the source reads and would otherwise count those lines
    # twice. Overlap that survives the trim is a defect and refuses.
    for arm in FUNCS:
        prev = None
        for role in ROLES:
            k = (arm, role)
            if k not in out:
                continue
            lo, hi = out[k]
            if prev is not None and lo <= prev:
                # ONE LINE OF OVERLAP IS THE SOURCE READING AND MORE IS A
                # MIS-SPECIFIED SPAN. Trimming whatever it finds looks like
                # tolerance and is not: give two roles the same opening
                # anchor and an unbounded trim hands back a table that reads
                # exactly like a correct one, which is the failure shape this
                # directory refuses everywhere else. Proved 2026-08-30 by
                # giving `odo` the `run` anchor, which the unbounded form
                # passed silently.
                if prev - lo >= 1:
                    die('spans %s/%s and the role before it overlap by %d'
                             ' line(s), so one of the two anchors is wrong;'
                             ' only the shared boundary line is trimmed'
                             % (arm, role, prev - lo + 1))
                lo = prev + 1
                out[k] = (lo, hi)
            if lo > hi:
                die('span %s/%s is empty after trimming: %d..%d'
                         % (arm, role, lo, hi))
            prev = hi
    seen = {}
    for (arm, role), (lo, hi) in out.items():
        for k in range(lo, hi + 1):
            if (arm, k) in seen:
                die('line %d of %s is in both %s and %s'
                         % (k, arm, seen[(arm, k)], role))
            seen[(arm, k)] = role
    harness = [i + 1 for i, l in enumerate(lines) if HARNESS.match(l)]
    return out, set(harness)


def main():
    if len(sys.argv) != 2:
        die(__doc__)
    sp, harness = spans('Main.hs')
    arms, cur = {}, None
    for ln in open(sys.argv[1]):
        m = re.match(r'^=== (\S+) ', ln)
        if m:
            cur = m.group(1)
            arms[cur] = {}
            continue
        m = re.match(r'^\s+[0-9.]+%\s+(\d+)\s+(\S+)', ln)
        if m and cur:
            arms[cur][m.group(2)] = arms[cur].get(m.group(2), 0) + int(m.group(1))
    if not arms:
        die('no arm sections in that file')

    def bucket(arm, counts):
        out = dict.fromkeys(ROLES, 0)
        out['harness'] = out['elsewhere'] = 0
        for site, n in counts.items():
            m = re.match(r'^Main\.hs:(\d+)$', site)
            if not m:
                out['elsewhere'] += n
                continue
            k = int(m.group(1))
            if k in harness:
                out['harness'] += n
                continue
            for role in ROLES:
                sp_k = (arm, role)
                if sp_k in sp and sp[sp_k][0] <= k <= sp[sp_k][1]:
                    out[role] += n
                    break
            else:
                out['elsewhere'] += n
        return out

    hdr = ROLES + ['harness', 'elsewhere', 'total']
    print(('%-16s' + '%11s' * len(hdr)) % tuple(['arm'] + hdr))
    got, unknown = {}, 0
    for arm, counts in arms.items():
        if (arm, ROLES[0]) not in sp:
            print('%-16s   -- no spans known for this arm, counted whole: %d'
                  % (arm, sum(counts.values())))
            unknown = 1
            continue
        b = bucket(arm, counts)
        got[arm] = b
        print(('%-16s' + '%11d' * len(hdr))
              % tuple([arm] + [b[c] for c in hdr[:-1]] + [sum(b.values())]))
    if 'lib-stage1' in got and 'lib-stage2' in got:
        a, b = got['lib-stage2'], got['lib-stage1']
        hdr = ROLES + ['harness', 'elsewhere']
        print(('%-16s' + '%11d' * (len(hdr) + 1) + '   <-- stage two minus one')
              % tuple(['difference'] + [a[c] - b[c] for c in hdr]
                      + [sum(a.values()) - sum(b.values())]))
    return unknown


sys.exit(main())
