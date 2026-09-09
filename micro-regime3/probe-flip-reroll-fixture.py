#!/usr/bin/env python3
"""Build a known-answer fixture for probe-flip-reroll-read.py out of Run 27.

The reader is a new instrument and its silence is worth nothing until it has
been shown to speak. Run 27's two flip processes already carry a
`flip-last-rows` group apiece, and the cells in them were derived by hand on
2026-09-09: `lib-stage1` 1.4637 basis and 1.2125 HEAD, `lib-stage2-lean`
1.4128 and 1.4256, the mut-odo-vecdims A/A triple 0.89% wide on the basis and
6.14% on HEAD. So slicing those two groups out gives two legs whose every
printed number is known in advance, and the reader has to reproduce them
before it is pointed at a leg nobody has read.

    ./probe-flip-reroll-fixture.py [-d MICRO_REGIME3] [-o FIXTUREDIR]
    ./probe-flip-reroll-read.py FIXTUREDIR

The two legs are named `-r0` so that a fixture can never be mistaken for a
measurement: the probe numbers its own repetitions from 1.
"""
import argparse, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument('-d', default='/home/mikolaj/r/orthotope/micro-regime3')
ap.add_argument('-o', default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           'reroll-fixture'))
ap.add_argument('-g', default='flip-last-rows')
a = ap.parse_args()

os.makedirs(a.o, exist_ok=True)
for half in ('g912', 'ghead'):
    src = os.path.join(a.d, 'run27-%s-flip.json' % half)
    if not os.path.exists(src):
        print('missing %s; Run 27 artifacts are deleted with the run' % src)
        sys.exit(2)
    d = json.load(open(src))
    kept = [r for r in d[2] if r['reportName'].startswith(a.g + '/')]
    if not kept:
        print('no %s group in %s' % (a.g, src))
        sys.exit(2)
    out = os.path.join(a.o, 'reroll-%s-default-r0.json' % half)
    json.dump([d[0], d[1], kept], open(out, 'w'))
    print('%s  %d benches' % (out, len(kept)))
print('\nnow: ./probe-flip-reroll-read.py %s' % a.o)
