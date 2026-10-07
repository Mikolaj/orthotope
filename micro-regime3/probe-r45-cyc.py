#!/usr/bin/env python3
"""A over B per shape, in instructions, cycles and (where the sweep has
them) bytes, off probe-stalls.sh sweeps -- the cycle and byte readings no
other reader takes off a two-event sweep. Written for Run 45's
preparation, whose file quotes it.

A fill arm is net of the mean of the two sum-only arms, the subtraction
`--counts --pair` makes; a -sum arm is raw, having no corrected time, and
so are bytes.  NONLINEAR cells are KEPT, at the published (2N-N)/N figure,
and counted, where `--counts --pair` drops one nonlinear in instructions;
a shape whose net is not positive on either arm is DROPPED and named.

    probe-r45-cyc.py A B FILE [FILE ...]           one block a file
    SHAPE=stretch-wide-2xM probe-r45-cyc.py A B FILE ...   adds that
                                                   shape's own ratios"""
import math
import os
import sys


def read(path):
    cells, order, nonlin = {}, None, set()
    for ln in open(path):
        f = ln.split()
        if ln.startswith('# shape arm N '):
            order = f[4:]
            continue
        if len(f) >= 4 and f[0] == '#' and f[1] == 'NONLINEAR':
            nonlin.add((f[2], f[3].rstrip(':')))
            continue
        if ln.startswith('#') or ln.startswith('!!') or not order:
            continue
        if len(f) == 3 + len(order):
            cells[(f[0], f[1])] = dict(zip(order, map(float, f[3:])))
    return cells, order, nonlin


def net(cells, sh, arm, ev):
    v = cells[(sh, arm)][ev]
    if arm.endswith('-sum') or ev == 'bytes' \
            or (sh, 'sum-only-early') not in cells:
        return v
    terms = [cells[(sh, k)][ev] for k in ('sum-only-early', 'sum-only-late')
             if (sh, k) in cells]
    return v - sum(terms) / len(terms)


def gm(xs):
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


a, b = sys.argv[1], sys.argv[2]
one = os.environ.get('SHAPE')
for path in sys.argv[3:]:
    cells, order, nonlin = read(path)
    shapes = sorted({s for s, _ in cells
                     if (s, a) in cells and (s, b) in cells})
    print('%s: %s over %s, %d shapes carry both' % (path, a, b, len(shapes)))
    for ev in [e for e in ('instructions:u', 'cycles:u', 'bytes')
               if e in order]:
        r, gone = [], []
        for s in shapes:
            x, y = net(cells, s, a, ev), net(cells, s, b, ev)
            if x > 0 and y > 0:
                r.append((x / y, s))
            else:
                gone.append(s)
        if one:
            hit = [x for x, s in r if s == one]
            print('  %-15s %s: %s' % (ev, one,
                                      '%.4f' % hit[0] if hit else 'not read'))
        if not r:
            continue
        lo, hi = min(r), max(r)
        nl = sum(1 for _, s in r if (s, a) in nonlin or (s, b) in nonlin)
        print('  %-15s geomean %.4f over %d  lowest %.4f on %s  highest %.4f'
              ' on %s  (%d touch a NONLINEAR cell)%s'
              % (ev, gm([x for x, _ in r]), len(r), lo[0], lo[1], hi[0],
                 hi[1], nl,
                 '; dropped, net not positive: ' + ', '.join(gone)
                 if gone else ''))
