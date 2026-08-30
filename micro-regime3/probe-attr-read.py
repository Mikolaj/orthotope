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

Exit 2 on usage or a lost anchor, 1 if a file names an arm this does not
know, 0 clean.
"""
import re
import sys

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
SPANS = {
    ('lib-stage1', 'fill'): ('  let writeRun !outPos !baseOff =',
                             '        in  inner outPos baseOff'),
    ('lib-stage1', 'driver'): ('      go !lev !outPos !baseOff',
                               '  _ <- go 0 0 ao'),
    ('lib-stage2', 'fill'): ('  let {-# INLINE writeRunStep #-}',
                             '      {-# INLINE writeRunSet #-}'),
    ('lib-stage2', 'driver'): ('      {-# INLINE writeRunSet #-}',
                               '  _ <- go 0 0 ao'),
}
# The shared forcing pass, `VS.sum . f sh`, which both arms are timed
# through: it is the control, and it must come out equal.
HARNESS = re.compile(r'^\s*arm sh a \(n, (Fill|Term)')


def spans(main_hs):
    src = open(main_hs).read()
    lines = src.splitlines()
    starts = {}
    for arm, name in FUNCS.items():
        if src.count(name) != 1:
            sys.exit('%s does not name one definition in %s (%d matches)'
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
            sys.exit('span %s/%s not found after line %d of %s'
                     % (arm, role, i + 1, main_hs))
        out[(arm, role)] = (lo, hi)
    # The driver span opens on the fill span's closing anchor for stage
    # two, so trim the overlap rather than counting those lines twice.
    for arm in FUNCS:
        f, d = out[(arm, 'fill')], out[(arm, 'driver')]
        if d[0] <= f[1]:
            out[(arm, 'driver')] = (f[1] + 1, d[1])
    harness = [i + 1 for i, l in enumerate(lines) if HARNESS.match(l)]
    return out, set(harness)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
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
        sys.exit('no arm sections in that file')

    def bucket(arm, counts):
        out = {'fill': 0, 'driver': 0, 'harness': 0, 'elsewhere': 0}
        for site, n in counts.items():
            m = re.match(r'^Main\.hs:(\d+)$', site)
            if not m:
                out['elsewhere'] += n
                continue
            k = int(m.group(1))
            if k in harness:
                out['harness'] += n
            elif (arm, 'fill') in sp and sp[(arm, 'fill')][0] <= k <= sp[(arm, 'fill')][1]:
                out['fill'] += n
            elif (arm, 'driver') in sp and sp[(arm, 'driver')][0] <= k <= sp[(arm, 'driver')][1]:
                out['driver'] += n
            else:
                out['elsewhere'] += n
        return out

    print('%-16s %12s %12s %12s %12s %12s'
          % ('arm', 'fill', 'driver', 'harness', 'elsewhere', 'total'))
    got, unknown = {}, 0
    for arm, counts in arms.items():
        if (arm, 'fill') not in sp:
            print('%-16s   -- no spans known for this arm, counted whole: %d'
                  % (arm, sum(counts.values())))
            unknown = 1
            continue
        b = bucket(arm, counts)
        got[arm] = b
        print('%-16s %12d %12d %12d %12d %12d'
              % (arm, b['fill'], b['driver'], b['harness'], b['elsewhere'],
                 sum(b.values())))
    if 'lib-stage1' in got and 'lib-stage2' in got:
        a, b = got['lib-stage2'], got['lib-stage1']
        print('%-16s %12d %12d %12d %12d %12d   <-- stage two minus stage one'
              % ('difference', a['fill'] - b['fill'], a['driver'] - b['driver'],
                 a['harness'] - b['harness'], a['elsewhere'] - b['elsewhere'],
                 sum(a.values()) - sum(b.values())))
    return unknown


sys.exit(main())
