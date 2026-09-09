#!/usr/bin/env python3
"""Read probe-flip-counters: does the cell survive being alone, and what moves.

Two readings, and the first is the control for the second.

ALONE. In Run 27's 35-bench process, `flip-last-rows/lib-stage1` reads a RAW
per-call slope of 2.5438 ms on the 9.12.4 binary and 2.2948 ms on the HEAD
one, a raw ratio of 0.9021 (0.8284 once the forcing term is out). An alone leg
runs the one bench in a fresh process, so the 15 benches that preceded it are
gone. If the ratio stays near 0.9021 the gap belongs to the binary; if it goes
to 1 the gap was the process history, and the block pool is where to look.
The alone leg cannot be corrected -- no `sum-only` bench runs beside it -- so
everything here is RAW and is compared with the raw figure above, never with
the corrected one.

COUNTERS. Per call, `-n 200` minus `-n 100` over 100, each in a fresh process.
Instructions are the control: they are already known equal across the
compilers to 1.5 ppm, so a differencing that does not reproduce that is a
differencing that went wrong, and this says so rather than reporting the cache
lines beside it.

Exit 0 clean, 1 with a reading that fires, 2 when the run did not happen.
"""
import argparse, json, os, re, sys

RAW_REFERENCE = {            # Run 27, in-group RAW slopes, ms per call
    ('g912', 'lib-stage1'): 2.5438, ('ghead', 'lib-stage1'): 2.2948,
    ('g912', 'lib-stage2-lean'): 2.4929, ('ghead', 'lib-stage2-lean'): 2.5079,
    ('g912', 'mut-odo-vecdims-add-in-leaf-u2'): 2.4981,
    ('ghead', 'mut-odo-vecdims-add-in-leaf-u2'): 2.3062,
    ('g912', 'mut-odo-vecdims-add-in-leaf-u2-last'): 2.2822,
    ('ghead', 'mut-odo-vecdims-add-in-leaf-u2-last'): 2.4712,
    ('g912', 'mut-odo-vecdims'): 2.6510, ('ghead', 'mut-odo-vecdims'): 2.7515,
}


def perf_counts(path):
    """event -> count from a `perf stat -x,` file, skipping what it refused."""
    out = {}
    for line in open(path):
        if line.startswith('#') or not line.strip():
            continue
        f = line.rstrip('\n').split(',')
        if len(f) < 3:
            continue
        val, ev = f[0], f[2]
        if not re.fullmatch(r'\d+(\.\d+)?', val):
            continue                      # <not supported>, <not counted>
        out[ev] = float(val)
    return out


def alone_slope(path, arm):
    """The one report an alone leg must hold, refusing a leg holding more.

    Criterion's positional selector is a PREFIX, so a leg named for one arm
    can carry several and a reader taking the first quotes whichever ran
    first: on 2026-09-09 `mut-odo-vecdims` brought ten and
    `-add-in-leaf-u2` four, and three arms' figures were published as one
    arm's. Counting the reports is the only check on a selector here --
    `--list` prints nothing at all once one is given -- so it is done, not
    trusted, and a contaminated leg is refused rather than averaged.
    """
    d = json.load(open(path))[2]
    if not d:
        return None, 'no reports'
    got = [r['reportName'].split('/', 1)[-1] for r in d]
    if len(d) != 1:
        return None, ('%d reports, not 1; the selector took %s'
                      % (len(d), ', '.join(got)))
    if got[0] != arm:
        return None, 'holds %s, not %s' % (got[0], arm)
    return (d[0]['reportAnalysis']['anRegress'][0]['regCoeffs']['iters']
            ['estPoint'] * 1e3), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('outdir')
    a = ap.parse_args()
    if not os.path.isdir(a.outdir):
        print('no such directory: %s' % a.outdir)
        return 2

    arms, halves = [], ('g912', 'ghead')
    for f in sorted(os.listdir(a.outdir)):
        m = re.fullmatch(r'alone-(g912|ghead)-(.+)\.json', f)
        if m and m.group(2) not in arms:
            arms.append(m.group(2))
    if not arms:
        print('no alone legs; the probe did not run')
        return 2

    rc = 0
    print('1. alone legs, RAW ms per call, against Run 27 in-group RAW')
    print('   %-38s %9s %9s %8s %10s' % ('arm', 'g912', 'ghead', 'ratio', 'in-group'))
    for arm in arms:
        v, why = {}, {}
        for h in halves:
            p = os.path.join(a.outdir, 'alone-%s-%s.json' % (h, arm))
            if not os.path.exists(p):
                v[h], why[h] = None, 'no leg'
            else:
                v[h], why[h] = alone_slope(p, arm)
        if None in v.values():
            bad = '; '.join('%s: %s' % (h, why[h]) for h in halves if why[h])
            print('   %-38s REFUSED -- %s' % (arm, bad))
            rc = max(rc, 2)
            continue
        ratio = v['ghead'] / v['g912']
        ref = RAW_REFERENCE.get(('ghead', arm), 0) / RAW_REFERENCE.get(('g912', arm), 1) \
            if ('g912', arm) in RAW_REFERENCE else float('nan')
        print('   %-38s %9.4f %9.4f %8.4f %10.4f'
              % (arm, v['g912'], v['ghead'], ratio, ref))
        if ('g912', arm) in RAW_REFERENCE and abs(ratio - ref) > 0.03:
            print('       ^ more than 3 points off the in-group ratio. ONE LEG'
                  ' IS ONE DRAW, not a verdict: the first draw of 2026-09-09'
                  ' read 0.9908 here and the two after it 0.9143 and 0.9170,'
                  ' the first being a cold binary. Read it beside its'
                  ' repetitions.')
            rc = max(rc, 1)

    print('\n2. per-call counters, (n=200 minus n=100) over 100')
    for arm in arms:
        rows = {}
        for h in halves:
            c = {}
            ok = True
            for n in (100, 200):
                p = os.path.join(a.outdir, 'perf-%s-%s-n%d.txt' % (h, arm, n))
                if not os.path.exists(p):
                    ok = False
                    break
                c[n] = perf_counts(p)
            rows[h] = {e: (c[200][e] - c[100][e]) / 100
                       for e in c[200] if e in c[100]} if ok else None
        if any(v is None for v in rows.values()):
            print('   %-38s incomplete' % arm)
            rc = max(rc, 2)
            continue
        print('   %s' % arm)
        for e in sorted(set(rows['g912']) & set(rows['ghead'])):
            x, y = rows['g912'][e], rows['ghead'][e]
            r = y / x if x else float('nan')
            note = ''
            if e.startswith('instructions') and abs(r - 1) > 0.01:
                note = '   <- CONTROL FAILED, the differencing is not clean'
                rc = max(rc, 2)
            print('      %-24s %14.1f %14.1f %8.4f%s' % (e, x, y, r, note))
    return rc


if __name__ == '__main__':
    sys.exit(main())
