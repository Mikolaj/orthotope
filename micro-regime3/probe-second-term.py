#!/usr/bin/env python3
"""The second term, per shape and per population: time over counted work.

[The ceiling]'s seventh reading names this quantity and leaves it open --
"time over instructions runs 1.16 to 1.67 on those five and never
approaches 1, so the branch's fill also retires fewer instructions per
cycle" -- and the ninth reading retires the FIRST term and says outright
that the second is untouched.  It is a ratio of two ratios, so it has no
mode in read-run.py and no counts file holds it: the time side is a run's
and the counted side is a sweep's.

    ./probe-second-term.py A B TIMES.json COUNTS.txt [COUNTS2.txt ...]

prints, per shape, the time ratio A/B, the instruction ratio A/B, and
their quotient, then the geomean of each over the shapes both sides hold.
More than one counts file may be given so that the main set's and a
class's can be handed over together; a shape in one and not the other is
reported and dropped rather than silently skipped.

BOTH SIDES ARE NET AND BOTH ARE THE SAME NET.  The time side is
`slope_net_s` out of `read-run.py --cells`, which is the reader's own
slope minus its own correction, so this script neither re-fits nor
re-corrects; the counted side subtracts `sum-only-early` per shape, which
is what the counts files' own readings subtract.  What this does NOT
reproduce is the reader's winsorizing: its geomean caps a cell at 3 MADs
and this one does not, which on the main set's counted work is a 0.669
against the 0.978 the ninth reading published, the difference being
`stretch-inner1` alone, where canonicalization removes the work
altogether.  So the per-shape column is the honest one here and the
geomean at the foot is a plain geomean, said so rather than dressed as
the published convention.

Exit 2 on a usage or input failure, 1 if any shape was dropped, 0 clean --
the convention every script in this directory keeps.
"""
import collections
import math
import statistics as stats
import subprocess
import sys


def cells(path):
    """shape -> arm -> net seconds, from the reader rather than the JSON"""
    r = subprocess.run(['./read-run.py', path, '--cells'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('read-run.py --cells failed on %s:\n%s' % (path, r.stderr))
    out = collections.defaultdict(dict)
    head = None
    for ln in r.stdout.splitlines():
        f = ln.split('\t')
        if len(f) < 4:
            continue
        if head is None:
            head = f
            continue
        try:
            out[f[0]][f[1]] = float(f[head.index('slope_net_s')])
        except (ValueError, IndexError):
            pass
    return out


def counts(paths):
    """shape -> arm -> instructions an iteration, sum-only-early not removed"""
    out = collections.defaultdict(dict)
    for p in paths:
        for ln in open(p):
            if ln.startswith('#') or ln.startswith('!!'):
                continue
            f = ln.split()
            if len(f) == 4:
                out[f[0]][f[1]] = float(f[3])
    return out


def wgm(rows, i):
    logs = [math.log(r[i]) for r in rows]
    m = stats.median(logs)
    mad = stats.median([abs(x - m) for x in logs])
    lo, hi = m - 3 * mad, m + 3 * mad
    return math.exp(sum(min(max(x, lo), hi) for x in logs) / len(logs))


def med(rows, i):
    return stats.median([r[i] for r in rows])


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    a, b, times = sys.argv[1], sys.argv[2], sys.argv[3]
    t, c = cells(times), counts(sys.argv[4:])
    dropped, removed = [], []
    rows = []
    for sh in sorted(t):
        td, cd = t[sh], c.get(sh, {})
        if not all(k in td for k in (a, b)) or \
           not all(k in cd for k in (a, b, 'sum-only-early')):
            dropped.append(sh)
            continue
        corr = cd['sum-only-early']
        # A NON-POSITIVE NET IS A CELL WITH THE WORK REMOVED, not a cell
        # measured small: `reshape1` canonicalizes to regime 1 under stage
        # two, so the arm returns the vector and its net time sits at or
        # below the forcing term it is corrected by. The reader prints such
        # a cell as `--` rather than a number; this drops it by the same
        # rule and says which, where taking its logarithm merely crashed.
        if min(td[a], td[b], cd[a] - corr, cd[b] - corr) <= 0:
            removed.append(sh)
            continue
        ci = (cd[a] - corr) / (cd[b] - corr)
        ti = td[a] / td[b]
        rows.append((sh, ti, ci, ti / ci))
    if not rows:
        print('no shape carries both arms with work left in both files')
        if removed:
            print('every one had the work removed: ' + ', '.join(removed))
        return 1
    print('%-22s %10s %10s %10s' % ('shape', 'time', 'counted', 'time/cnt'))
    for sh, ti, ci, q in rows:
        print('%-22s %10.4f %10.4f %10.4f' % (sh, ti, ci, q))
    gm = lambda i: math.exp(sum(math.log(r[i]) for r in rows) / len(rows))
    print('%-22s %10.4f %10.4f %10.4f   (plain geomean over %d shape(s))'
          % ('geomean', gm(1), gm(2), gm(3), len(rows)))
    # AND THE READER'S OWN CONVENTION BESIDE IT, which caps a cell at 3
    # MADs of the log before averaging: `stretch-inner1` reads 29.7 in the
    # quotient column because canonicalization removes the work there, so
    # the plain geomean of the main set is that one cell and the winsorized
    # one is the other twenty-three. Both are printed because neither is
    # right for every question -- the plain one for a claim about the
    # population as it stands, the capped one for a rate -- and quoting
    # either without naming it is what this file exists to make hard.
    print('%-22s %10.4f %10.4f %10.4f   (winsorized at 3 MADs, which is'
          ' read-run.py\'s published convention)'
          % ('geomean, capped', wgm(rows, 1), wgm(rows, 2), wgm(rows, 3)))
    print('%-22s %10.4f %10.4f %10.4f   (median)'
          % ('median', med(rows, 1), med(rows, 2), med(rows, 3)))
    if dropped:
        print('dropped, absent from one side: ' + ', '.join(dropped))
    if removed:
        print('dropped, the work removed rather than measured small: '
              + ', '.join(removed))
    return 1 if (dropped or removed) else 0


sys.exit(main())
