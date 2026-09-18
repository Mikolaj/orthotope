#!/usr/bin/env python3
"""Per-view A/A floor, beside the per-class one a run publishes.

A run's floor is a class-level figure: `read-run.py` names the widest A/A pair
over a class and its worst cell, and a registration is then adjudicated
"past the class's floor". That is right wherever a class's views behave alike
and wrong where one does not, and Run 27 has such a view. On `flip` the
published floor is `list-aa-distant` at 0.9959 with a worst cell of 1.21%,
while on `flip-last-rows` alone the three byte-identical copies of
`mut-odo-vecdims` spread 0.89% on the basis and 6.14% on the HEAD half -- so a
clause adjudicated at 1.21% is being read against a floor five times too
narrow on one half.

This prints, per view, the spread of every A/A group the roster carries, so
that a clause about a view is read against that view's own floor. It changes
no published table and replaces no reader: it is one more question asked of
the same JSONs.

Groups are found by name rather than declared, `X-aa`, `X-aa-adjacent` and
`X-aa-distant` beside their `X`, so a roster that gains an A/A twin is picked
up with no edit here -- which is the point, the twin of item 13 being the
thing this most wants to read.

    ./view-floor.py RUN [-d DIR] [-c CLASS]... [--factor F] [--csv FILE]

RUN is the prefix the artifacts carry, `run27`. Reads
`RUN-<half>-<class>.json` for whichever halves and classes are on disk.
Exit 0 when no view exceeds its class floor by more than --factor (default 2),
1 when one does, and 2 when the run did not happen -- no JSONs, or a class
whose views carry no A/A group at all.
"""
import argparse, collections, glob, json, os, statistics, sys

SUFFIXES = ('-aa', '-aa-adjacent', '-aa-distant')


def read(path):
    d = json.load(open(path))
    return {r['reportName']:
            r['reportAnalysis']['anRegress'][0]['regCoeffs']['iters']['estPoint']
            for r in d[2]}


def groups_of(arms):
    """base arm -> its A/A copies, read off the names the roster uses."""
    out = collections.defaultdict(list)
    for a in arms:
        for s in SUFFIXES:
            if a.endswith(s) and a[:-len(s)] in arms:
                out[a[:-len(s)]].append(a)
    return {b: [b] + sorted(v) for b, v in out.items()}


def spread(xs):
    return (max(xs) / min(xs) - 1) * 100


def legs_mode(a):
    """A floor read off one leg is one draw, and on some views that matters.

    Eighteen legs of `flip-last-rows` on 2026-09-09 put its own A/A spread
    anywhere from 0.46% to 11.31%, median 4.27%, with nothing changed
    between legs but the process. Run 27's two readings of that view, 0.89%
    and 6.14%, are two draws from that spread and neither is the floor. So
    where repeated legs exist this mode reports the distribution, and a
    single-leg figure is quoted as a draw.
    """
    files = sorted(glob.glob(os.path.join(a.legs, '*.json')))
    if not files:
        print('no legs under %s' % a.legs)
        return 2
    per_group = collections.defaultdict(list)
    view = None
    for f in files:
        try:
            R = read(f)
        except Exception as e:                       # a leg still being written
            print('!! %s unreadable (%s)' % (os.path.basename(f), type(e).__name__))
            continue
        arms = {k.split('/', 1)[1] for k in R}
        views = {k.split('/')[0] for k in R}
        if len(views) != 1:
            print('!! %s holds %d views; this mode wants one'
                  % (os.path.basename(f), len(views)))
            return 2
        view = views.pop()
        so = (R.get(view + '/sum-only-early', 0)
              + R.get(view + '/sum-only-late', 0)) / 2
        for base, copies in groups_of(arms).items():
            net = [R[view + '/' + c] - so for c in copies]
            if min(net) > 0:
                per_group[base].append(spread(net))
    if not per_group:
        print('no A/A group in those legs')
        return 2
    print('== %s, the A/A floor over %d legs' % (view, len(files)))
    print('   %-26s %6s %8s %8s %8s' % ('A/A group', 'legs', 'min', 'median', 'max'))
    for base, v in sorted(per_group.items()):
        print('   %-26s %6d %7.2f%% %7.2f%% %7.2f%%'
              % (base, len(v), min(v), statistics.median(v), max(v)))
    print('\n   A clause about this view is read against the MAX, not the'
          ' median: a run takes one leg and cannot know which draw it got.')
    return 1 if max(max(v) for v in per_group.values()) > 2.0 else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run')
    ap.add_argument('-d', default='.')
    ap.add_argument('-c', action='append', default=None, dest='classes')
    ap.add_argument('--factor', type=float, default=2.0)
    ap.add_argument('--legs', help='a directory of repeated legs of ONE view '
                    '(probe-flip-reroll\'s output): report the floor as the '
                    'distribution it is rather than as one draw')
    ap.add_argument('--csv')
    a = ap.parse_args()

    if a.legs:
        return legs_mode(a)
    files = sorted(glob.glob(os.path.join(a.d, '%s-*-*.json' % a.run)))
    legs = []
    for f in files:
        stem = os.path.basename(f)[:-len('.json')]
        # strip the run prefix rather than splitting on every dash, so a run
        # name carrying one does not silently become a half named after its
        # own second word.
        rest = stem[len(a.run) + 1:]
        parts = rest.split('-', 1)
        if len(parts) < 2:
            continue
        half, cls = parts
        if a.classes and cls not in a.classes:
            continue
        # NOT CLASS LEGS: the main set, whose floor the run publishes,
        # and the alone legs and gate processes, which put `al` and
        # `gate` where a half's name sits. `if ...: pass` skipped nothing
        # and tested the class for a marker the half carries, so every
        # such leg raised the exit to 2 with a `carries no A/A group`
        # line apiece -- 92 on Run 32 (2026-09-18, by review). The main
        # set named with -c is read.
        if half in ('al', 'gate', 'counts') or (cls == 'main'
                                                 and not a.classes):
            continue
        legs.append((half, cls, f))
    if not legs:
        print('no %s-<half>-<class>.json under %s' % (a.run, a.d))
        return 2

    rows, worst_flag = [], 0
    for half, cls, f in legs:
        R = read(f)
        arms = {k.split('/', 1)[1] for k in R}
        gs = groups_of(arms)
        if not gs:
            print('!! %s carries no A/A group; nothing to read' % os.path.basename(f))
            worst_flag = max(worst_flag, 2)
            continue
        views = sorted({k.split('/')[0] for k in R})
        per_view = {}
        for v in views:
            best = {}
            for base, copies in gs.items():
                xs = [R.get(v + '/' + c) for c in copies]
                if any(x is None for x in xs):
                    continue
                so = (R.get(v + '/sum-only-early', 0) + R.get(v + '/sum-only-late', 0)) / 2
                net = [x - so for x in xs]
                if min(net) <= 0:
                    continue
                best[base] = spread(net)
            if best:
                per_view[v] = best
        if not per_view:
            continue
        # A class floor PER A/A GROUP, and a view read against the group
        # whose cost structure resembles the arm the clause is about. Taking
        # the widest group instead lets `list` -- twenty to forty times the
        # fills' cost on some classes, and 4% wide on every `runs` view --
        # speak for a clause about a fill, which is the mistake this tool
        # exists to stop rather than one to repeat in it.
        hdr = sorted(gs)
        floor = {}
        for b in hdr:
            xs = [per_view[v][b] for v in per_view if b in per_view[v]]
            if xs:
                floor[b] = statistics.median(xs)
        print('\n== %s %s' % (a.run + '-' + half, cls))
        print('   %-24s %s' % ('view', ' '.join('%22s' % b[-22:] for b in hdr)))
        print('   %-24s %s   <- class floor, per group'
              % ('(median over views)',
                 ' '.join('%21.2f%%' % floor[b] if b in floor else '%22s' % '-'
                          for b in hdr)))
        for v in views:
            if v not in per_view:
                continue
            cells, loud = [], []
            for b in hdr:
                if b not in per_view[v]:
                    cells.append('%22s' % '-')
                    continue
                sp = per_view[v][b]
                over = b in floor and sp > a.factor * floor[b]
                cells.append('%20.2f%%%s' % (sp, '*' if over else ' '))
                if over:
                    loud.append('%s %.2f%% against %.2f%%' % (b, sp, floor[b]))
                    worst_flag = max(worst_flag, 1)
                rows.append((a.run, half, cls, v, b, sp, floor.get(b, float('nan'))))
            print('   %-24s %s%s'
                  % (v, ' '.join(cells), ('  <- ' + '; '.join(loud)) if loud else ''))

    if a.csv:
        with open(a.csv, 'w') as fh:
            fh.write('run,half,class,view,aa_group,view_spread_pct,'
                     'class_floor_pct\n')
            for r in rows:
                fh.write('%s,%s,%s,%s,%s,%.4f,%.4f\n' % r)
    if worst_flag == 1:
        print('\nStarred cells are more than %gx their group\'s class floor.'
              ' A clause about such a view is read against the view, and'
              ' against the A/A group whose arm the clause is about.'
              % a.factor)
    return worst_flag


if __name__ == '__main__':
    sys.exit(main())
