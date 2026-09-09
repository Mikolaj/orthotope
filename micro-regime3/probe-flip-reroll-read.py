#!/usr/bin/env python3
"""Read probe-flip-reroll's legs and answer the question they were run for.

One leg is one process of one binary over one shape's whole roster, so a leg
is what a cell belongs to. What this prints, in the order the registration
asks it:

  1. the per-leg floor -- the spread of the three byte-identical copies of
     `mut-odo-vecdims` in that leg, which is the only number that says how
     much a cell may move for nothing;
  2. every arm's net cell per leg, and its spread across the repetitions of
     one binary at one RTS setting, which decides (a) against (b);
  3. the fill family's ORDERING per leg, since that is what re-rolled between
     Run 25, 26 and 27 -- the ceiling arm on this view was `-u2`, then `-u1`,
     then `-u2-last`, three arms of one loop family;
  4. the -A legs against the default ones, which decides (c).

`--csv` writes one row per (leg, arm) if the numbers are wanted elsewhere.
Exit 0 clean, 1 with a verdict that fires, 2 when the run did not happen --
no legs, a missing forcing term, a leg whose JSON criterion never wrote.
"""
import argparse, collections, json, os, statistics, sys

FAMILY = ['mut-odo-vecdims', 'mut-odo-vecdims-add-in-leaf-u1',
          'mut-odo-vecdims-add-in-leaf-u2',
          'mut-odo-vecdims-add-in-leaf-u2-down',
          'mut-odo-vecdims-add-in-leaf-u2-last',
          'mut-odo-vecdims-add-in-leaf-u1-ptr',
          'mut-odo-vecdims-add-in-leaf-u2-ptr',
          'lib-stage1', 'lib-stage2-lean', 'lib-stage2-lean-u1']
AA = ['mut-odo-vecdims', 'mut-odo-vecdims-aa', 'mut-odo-vecdims-aa-distant']


def leg_cells(path):
    """Net per-call slope in ms for every arm of one leg, forcing term out."""
    d = json.load(open(path))
    rep = {r['reportName']:
           r['reportAnalysis']['anRegress'][0]['regCoeffs']['iters']['estPoint']
           for r in d[2]}
    if not rep:
        return None, 'no benchmarks in %s' % path
    group = sorted({k.split('/')[0] for k in rep})
    if len(group) != 1:
        return None, '%s holds %d groups, expected one' % (path, len(group))
    g = group[0]
    early, late = g + '/sum-only-early', g + '/sum-only-late'
    if early not in rep or late not in rep:
        return None, '%s carries no forcing term' % path
    so = (rep[early] + rep[late]) / 2
    return {k.split('/', 1)[1]: (v - so) * 1e3 for k, v in rep.items()}, None


def spread(xs):
    return (max(xs) / min(xs) - 1) * 100 if xs and min(xs) > 0 else float('nan')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('outdir')
    ap.add_argument('--csv')
    a = ap.parse_args()

    if not os.path.isdir(a.outdir):
        print('no such directory: %s; the probe did not run' % a.outdir)
        return 2
    legs, bad = {}, []
    for f in sorted(os.listdir(a.outdir)):
        if not (f.startswith('reroll-') and f.endswith('.json')):
            continue
        tag = f[len('reroll-'):-len('.json')]
        cells, err = leg_cells(os.path.join(a.outdir, f))
        if err:
            bad.append(err)
        else:
            legs[tag] = cells
    for e in bad:
        print('!! ' + e)
    if not legs:
        print('no legs read; the probe did not run')
        return 2
    order = sorted(legs)

    print('== %d legs' % len(legs))
    print('\n1. per-leg floor, the three byte-identical mut-odo-vecdims copies')
    floors = {}
    for t in order:
        v = [legs[t][x] for x in AA if x in legs[t]]
        floors[t] = spread(v)
        print('   %-22s %s   spread %5.2f%%'
              % (t, ' '.join('%8.4f' % x for x in v), floors[t]))
    med_floor = statistics.median(floors.values())

    print('\n2. net ms per arm per leg')
    print('   %-38s %s' % ('arm', ' '.join('%10s' % t[:10] for t in order)))
    for arm in FAMILY:
        row = [legs[t].get(arm) for t in order]
        if any(x is None for x in row):
            continue
        print('   %-38s %s' % (arm, ' '.join('%10.4f' % x for x in row)))

    # (a) against (b): repetitions of one binary at one setting.
    groups = collections.defaultdict(list)
    for t in order:
        half, cond = t.split('-')[0], t.split('-')[1]
        groups[(half, cond)].append(t)
    print('\n   repeat spread within one binary at one setting'
          ' (floor above is %5.2f%%)' % med_floor)
    worst_repeat = 0.0
    for key, ts in sorted(groups.items()):
        if len(ts) < 2:
            continue
        for arm in FAMILY:
            v = [legs[t][arm] for t in ts if arm in legs[t]]
            if len(v) < 2:
                continue
            s = spread(v)
            worst_repeat = max(worst_repeat, s)
            if s > 3 * med_floor:
                print('   %-10s %-34s %5.2f%%  LOUD' % ('-'.join(key), arm, s))
    print('   worst repeat spread over the family: %5.2f%%' % worst_repeat)

    print('\n3. fill-family ordering per leg (fastest first)')
    seen = {}
    for t in order:
        rank = tuple(sorted((x for x in FAMILY if x in legs[t]),
                            key=lambda x: legs[t][x]))
        seen.setdefault(rank, []).append(t)
        print('   %-22s %s' % (t, ' < '.join(x.replace('mut-odo-vecdims', 'modo')
                                             for x in rank[:4])))
    print('   %d distinct orderings over %d legs' % (len(seen), len(order)))

    print('\n4. the allocator knob, g912 only, each against its default leg')
    base = [t for t in order if t.startswith('g912-default')]
    for cond in ('A16m', 'A64m'):
        ts = [t for t in order if t.startswith('g912-' + cond)]
        if not ts or not base:
            continue
        for arm in FAMILY:
            b = [legs[t][arm] for t in base if arm in legs[t]]
            k = [legs[t][arm] for t in ts if arm in legs[t]]
            if not b or not k:
                continue
            r = statistics.median(k) / statistics.median(b)
            flag = '  MOVED' if abs(r - 1) * 100 > 3 * med_floor else ''
            print('   %-6s %-34s %6.4f%s' % (cond, arm, r, flag))

    print('\n== verdict, PER ARM')
    # Taking the worst arm and letting it speak for the roster was this
    # reader's own defect, corrected 2026-09-09 on the run that exposed it:
    # `lib-stage1` and `-u2` reproduced inside 4% while `-u1-ptr` spread 30%
    # in one binary at one setting, and a single verdict called all ten (b).
    repeated = any(len(ts) >= 2 for ts in groups.values())
    if not repeated:
        print('   NOT READ: no binary was run twice at one setting, and one'
              ' leg cannot say whether a cell reproduces.')
        return 2
    fixed, rolling = [], []
    for arm in FAMILY:
        sp = [spread([legs[t][arm] for t in ts if arm in legs[t]])
              for ts in groups.values()
              if len([t for t in ts if arm in legs[t]]) >= 2]
        if not sp:
            continue
        w = max(sp)
        (rolling if w > 3 * med_floor else fixed).append((arm, w))
    for arm, w in sorted(fixed, key=lambda x: x[1]):
        print('   (a) fixed per binary  %-38s worst repeat %5.2f%%' % (arm, w))
    for arm, w in sorted(rolling, key=lambda x: -x[1]):
        print('   (b) re-rolls          %-38s worst repeat %5.2f%%' % (arm, w))
    print('   --- %d of %d arms reproduce inside 3x the %.2f%% median floor;'
          ' the split is per arm and not per run.'
          % (len(fixed), len(fixed) + len(rolling), med_floor))
    rc = 1 if rolling else 0
    if len(seen) > 1:
        print('   the fill family orders itself %d ways across these legs,'
              ' so no ordering on this view is a property of the code.'
              % len(seen))
        rc = max(rc, 1)
    if a.csv:
        with open(a.csv, 'w') as fh:
            fh.write('leg,arm,net_ms\n')
            for t in order:
                for arm, v in sorted(legs[t].items()):
                    fh.write('%s,%s,%.6f\n' % (t, arm, v))
    return rc


if __name__ == '__main__':
    sys.exit(main())
