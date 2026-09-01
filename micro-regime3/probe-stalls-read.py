#!/usr/bin/env python3
"""Read a probe-stalls sweep: the second term off the counters, and what it is.

    ./probe-stalls-read.py A B FILE.txt [FILE.txt ...]

The second term this file is for is time over counted work, and at a
fixed clock that IS a ratio of cycles per instruction -- so the cycles
column of a stall sweep measures the same quantity the clock measures,
by an instrument that owes criterion nothing.  Printing the two beside
each other is the point: agreement says the term is real and not an
artefact of the timing, and the three event columns beside them say
what the cycles went on.

Every column is net of `sum-only-early` on the same shape, as the time
column and the counted-work column both are, and every ratio is A over B
on that shape.  `cpi` is the second term as the counters read it;
`front`, `bmiss` and `cmiss` are per-INSTRUCTION rates, A over B, so a
figure above 1 means A meets that hazard more often per instruction it
executes, which is the only form in which they explain a CPI gap.

Exit 2 on usage or an input this cannot read, 1 if a shape was dropped,
0 clean.
"""
import collections
import math
import statistics as stats
import sys

EVENTS = ['instructions:u', 'cycles:u', 'stalled-cycles-frontend:u',
          'branch-misses:u', 'cache-misses:u']
FRONT, BMISS, CMISS = EVENTS[2:]
def die(msg):
    """Exit 2 -- did not run -- rather than `sys.exit(str)`'s 1, which is
    the code a finding gets."""
    sys.stderr.write(msg.rstrip('\n') + '\n')
    sys.exit(2)


def read(paths):
    """shape -> arm -> {event: value}, and the header's own event order"""
    out = collections.defaultdict(dict)
    order = None
    for p in paths:
        for ln in open(p):
            if ln.startswith('# shape arm N '):
                seen = ln.split()[4:]
                if order is None:
                    order = seen
                elif order != seen:
                    die('event columns differ between files: %s vs %s'
                        % (order, seen))
                continue
            if ln.startswith('#') or ln.startswith('!!'):
                continue
            f = ln.split()
            if order and len(f) == 3 + len(order):
                out[f[0]][f[1]] = dict(zip(order, map(float, f[3:])))
    return out, order


def main():
    if len(sys.argv) < 4:
        die(__doc__)
    a, b = sys.argv[1], sys.argv[2]
    t, order = read(sys.argv[3:])
    if order is None:
        die('no header line naming the events in any file given')
    # BY NAME, not by column: a sweep taken under another `EVENTS` puts
    # other counters in columns 2 to 4, and a positional read labelled them
    # front/bmiss/cmiss regardless, or crashed short. 2026-09-01.
    missing = [e for e in EVENTS if e not in order]
    if missing:
        die('the header names %s, which lacks %s -- a sweep taken under'
            ' another EVENTS, which this does not read'
            % (' '.join(order), ', '.join(missing)))
    rows, dropped = [], []
    for sh in sorted(t):
        d = t[sh]
        if not all(k in d for k in (a, b, 'sum-only-early')):
            dropped.append(sh)
            continue
        c = d['sum-only-early']
        net = {arm: {e: d[arm][e] - c[e] for e in order} for arm in (a, b)}
        if min(net[a]['instructions:u'], net[b]['instructions:u'],
               net[a]['cycles:u'], net[b]['cycles:u']) <= 0:
            dropped.append(sh)
            continue
        cpi = [net[x]['cycles:u'] / net[x]['instructions:u'] for x in (a, b)]
        rate = lambda e: [net[x][e] / net[x]['instructions:u'] for x in (a, b)]
        fr, bm, cm = rate(FRONT), rate(BMISS), rate(CMISS)
        rows.append((sh,
                     net[a]['instructions:u'] / net[b]['instructions:u'],
                     cpi[0] / cpi[1],
                     fr[0] / fr[1] if fr[1] else float('nan'),
                     bm[0] / bm[1] if bm[1] else float('nan'),
                     cm[0] / cm[1] if cm[1] else float('nan')))
    if not rows:
        print('no shape carries both arms with work left')
        return 1
    print('%-22s %8s %8s %8s %8s %8s' %
          ('shape', 'counted', 'cpi', 'front', 'bmiss', 'cmiss'))
    for r in rows:
        print('%-22s %8.4f %8.4f %8.4f %8.4f %8.4f' % r)

    def wgm(i):
        v = [r[i] for r in rows if r[i] == r[i] and r[i] > 0]
        if not v:
            return float('nan')
        logs = [math.log(x) for x in v]
        m = stats.median(logs)
        # Scaled by 1.4826 and uncapped at a zero MAD, as read-run.py's
        # `winsorize` is: unscaled, "3 MADs" here meant about two of the
        # reader's. 2026-09-01.
        mad = stats.median([abs(x - m) for x in logs]) * 1.4826
        if mad <= 0:
            return math.exp(sum(logs) / len(logs))
        lo, hi = m - 3 * mad, m + 3 * mad
        return math.exp(sum(min(max(x, lo), hi) for x in logs) / len(logs))
    print('%-22s %8.4f %8.4f %8.4f %8.4f %8.4f   (geomean over %d, capped at'
          ' 3 MADs)' % ('geomean, capped', wgm(1), wgm(2), wgm(3), wgm(4),
                        wgm(5), len(rows)))
    if dropped:
        print('dropped, absent or with the work removed: ' + ', '.join(dropped))
    return 1 if dropped else 0


sys.exit(main())
