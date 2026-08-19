#!/usr/bin/env python3
"""Reduce a t22/t23 interleaved-null run: per cell, the two per-pair B/A
ratios off the criterion time-line slope, units asserted equal within a
cell. Usage: t2x-reduce.py DIR PREFIX (e.g. ... goal4 t22). Cells are
discovered from DIR/PREFIX-*-a-r1.log, so the script and the driver
share no hand-kept list."""
import glob
import os
import re
import sys

d, t = sys.argv[1], sys.argv[2]
UNITS = {"s": 1.0, "ms": 1e-3, "us": 1e-6, "ns": 1e-9,
         "μs": 1e-6}

def val(path):
    for ln in open(path):
        m = re.match(r"time\s+([0-9.]+) (\S+)", ln)
        if m:
            return float(m.group(1)) * UNITS[m.group(2)]
    raise SystemExit(f"no time line in {path}")

cells = sorted(os.path.basename(p)[len(t) + 1:-len("-a-r1.log")]
               for p in glob.glob(f"{d}/{t}-*-a-r1.log"))
if not cells:
    raise SystemExit(f"no {t}-*-a-r1.log cells under {d}")
print(f"{'cell':24} {'B/A r1':>8} {'B/A r2':>8} {'mean':>8}")
for c in cells:
    r = [val(f"{d}/{t}-{c}-b-r{i}.log") / val(f"{d}/{t}-{c}-a-r{i}.log")
         for i in (1, 2)]
    print(f"{c:24} {r[0]:8.4f} {r[1]:8.4f} {(r[0]+r[1])/2:8.4f}")
