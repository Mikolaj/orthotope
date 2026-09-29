#!/usr/bin/env python3
"""Fold one rider set's legs into one JSON and one log.

    ./merge-alonelegs.py run43 gheadnospec          # the clean set
    ./merge-alonelegs.py --sat run43 gheadnospec    # the saturated one
    ./merge-alonelegs.py --dir D --out O RUN HALF   # legs in D, set in O

A rider leg is one bench in its own process, which is the measurement,
and each used to leave its own JSON and log beside a driver log: 45
names a set, 180 a run. This writes the set as `$R-al-<half>[-sat].json`
and `.log` and removes the files it folded in, which the owner asked
for on 2026-09-29. run-alonelegs.sh calls it when a set ends, over the
set's working directory, and it converts a set a run up to Run 43 left
in the per-leg form in place.

THE JSON IS CRITERION'S OWN FORM, `[name, version, reports]`, over the
set's FIRST repetitions, one `list` report a shape, so `load` and every
reader of `raw[2]` read it unchanged. The anchors' second repetitions
carry the same report names and so cannot share that list: they go in a
fourth element, `{"later repetitions": [{"leg": ..., "rep": N,
"report": ...}]}`, which no reader of `raw[2]` sees and nothing is
dropped for.

THE LOG is the driver's lines first, its DONE line among them, and then
every leg's log whole under a `=== leg SHAPE rN ===` line, in the order
the legs ran, which is the order of their JSONs' modification times.

Refuses, exit 1, over a set whose merged files already exist or whose
legs do not each hold one report, and leaves every source file in
place; exit 2 where no leg is found at all.
"""
import argparse
import glob
import json
import os
import re
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('run')
    ap.add_argument('half')
    ap.add_argument('--sat', action='store_true',
                    help='the saturated set, `-sat` on the names')
    ap.add_argument('--dir', default='.', help='where the legs are')
    ap.add_argument('--out', default='.', help='where the set is written')
    a = ap.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    stem = '%s-al-%s%s' % (a.run, a.half, '-sat' if a.sat else '')
    out_json = os.path.join(a.out, stem + '.json')
    out_log = os.path.join(a.out, stem + '.log')
    for p in (out_json, out_log):
        if os.path.exists(p):
            print('%s exists already: this set is merged, or a previous'
                  ' attempt left it; nothing was touched' % p)
            return 1
    pre = stem + '-'
    legs = []
    for p in glob.glob(os.path.join(a.dir, pre + '*.json')):
        name = os.path.basename(p)[len(pre):-len('.json')]
        # `-sat` is a suffix on the half's name, so the clean set's
        # prefix takes the saturated legs too; they are not this set's.
        if not a.sat and name.startswith('sat-'):
            continue
        m = re.match(r'^(.+)-r(\d+)$', name)
        if m:
            legs.append((os.path.getmtime(p), m.group(1), int(m.group(2)),
                         p))
    if not legs:
        print('no %s*-rN.json in %s: no leg of this set to merge'
              % (pre, a.dir))
        return 2
    legs.sort()
    head, first, later, bad = None, [], [], []
    for _, shape, rep, p in legs:
        try:
            d = json.load(open(p))
            reports = d[2]
        except (OSError, ValueError, IndexError, KeyError, TypeError) as e:
            bad.append('%s: unreadable (%s)' % (p, str(e)[:60]))
            continue
        if len(reports) != 1:
            bad.append('%s: %d reports, where a leg is one bench'
                       % (p, len(reports)))
            continue
        head = head or d[:2]
        if rep == 1:
            first.append(reports[0])
        else:
            later.append({'leg': shape, 'rep': rep, 'report': reports[0]})
    names = [r['reportName'] for r in first]
    if len(set(names)) != len(names):
        bad.append('a shape carries two first repetitions')
    if bad or not first:
        print('refused, every source kept:')
        for b in bad or ['no first repetition among the legs']:
            print('  ' + b)
        return 1
    merged = head + [first]
    if later:
        merged.append({'later repetitions': later})
    parts = []
    driver = os.path.join(a.dir, stem + '-driver.log')
    if os.path.exists(driver):
        parts.append(open(driver, errors='replace').read())
    for _, shape, rep, p in legs:
        lg = p[:-len('.json')] + '.log'
        parts.append('=== leg %s r%d ===\n' % (shape, rep))
        parts.append(open(lg, errors='replace').read() if os.path.exists(lg)
                     else '!! no log beside this leg\'s JSON\n')
    for path, text in ((out_json, json.dumps(merged)),
                       (out_log, ''.join(parts))):
        with open(path + '.tmp', 'w') as f:
            f.write(text)
        os.replace(path + '.tmp', path)
    gone = 0
    for _, _, _, p in legs:
        for q in (p, p[:-len('.json')] + '.log'):
            if os.path.exists(q):
                os.remove(q)
                gone += 1
    if os.path.exists(driver):
        os.remove(driver)
        gone += 1
    if os.path.abspath(a.dir) != os.path.abspath(a.out):
        try:
            os.rmdir(a.dir)
        except OSError:
            pass
    print('merged %d leg(s), %d first repetition(s) and %d later, into %s'
          ' and %s; %d file(s) folded in and removed'
          % (len(legs), len(first), len(later), out_json, out_log, gone))
    return 0


if __name__ == '__main__':
    sys.exit(main())
