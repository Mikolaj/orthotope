#!/usr/bin/env python3
"""Difference two probe-fetches.sh files cell by cell: where one binary's
placement crosses more windows than the other's, and by how much.

    ./probe-fetches-read.py A.txt B.txt [--min PCT]

Joins on (population, shape, arm), prints every cell whose fetches per
iteration differ by at least --min percent (default 0.2), B against A,
sorted by the percentage difference, and a summary: cells in both files,
cells moved, cells in one file only, cells that could not be counted. A cell that moved
is one the pair of the two placements can differ on; a cell that did not
cannot, whatever the timing says. Exit 0 with output, 1 when a file
carries no cells, 2 on usage.
"""
import argparse
import signal
import sys


def load(path):
    cells, bad = {}, []
    for line in open(path):
        if line.startswith('#'):
            continue
        if line.startswith('!!'):
            bad.append(line[2:].strip())
            continue
        p = line.split()
        if len(p) == 5:
            cells[(p[0], p[1], p[2])] = int(p[4])
    return cells, bad


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # `| head` is a normal use
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('a')
    ap.add_argument('b')
    ap.add_argument('--min', type=float, default=0.2,
                    help='percent difference a cell must reach to be listed')
    args = ap.parse_args()
    a, abad = load(args.a)
    b, bbad = load(args.b)
    if not a or not b:
        print('probe-fetches-read: %s carries no cells'
              % (args.a if not a else args.b), file=sys.stderr)
        return 1
    both = sorted(set(a) & set(b))
    rows = []
    for k in both:
        d = b[k] - a[k]
        rows.append((100.0 * d / a[k] if a[k] else 0.0, d, k))
    rows.sort(key=lambda r: -abs(r[0]))
    moved = [r for r in rows if abs(r[0]) >= args.min]
    print('%-9s %-24s %-36s %12s %12s %9s %8s'
          % ('pop', 'shape', 'arm', 'A/iter', 'B/iter', 'B-A', 'pct'))
    for pct, d, (p, s, arm) in moved:
        print('%-9s %-24s %-36s %12d %12d %9d %+7.2f%%'
              % (p, s, arm, a[(p, s, arm)], b[(p, s, arm)], d, pct))
    print('%d cells in both files, %d moved by %.2f%% or more, %d in one file'
          ' only, %d uncountable (%d in A, %d in B)'
          % (len(both), len(moved), args.min, len(set(a) ^ set(b)),
             len(abad) + len(bbad), len(abad), len(bbad)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
