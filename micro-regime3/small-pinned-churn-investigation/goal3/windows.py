#!/usr/bin/env python3
"""Window means over a MixedLoad log's per-round table: the instrument
behind every 'windows lo-hi' figure in findings2 items 34-41.

  windows.py LOG [LO HI]...    mean round-wall ms over rounds [LO, HI)
                               per pair; no pairs = 20-120 and the last
                               fifth (the steady tail).
The log's own per-call table (printed at its end) needs no script."""
import sys

path = sys.argv[1]
rows = [float(l.split()[1]) for l in open(path)
        if l.split() and l.split()[0].isdigit()]
bounds = [(int(a), int(b))
          for a, b in zip(sys.argv[2::2], sys.argv[3::2])]
if not bounds:
    bounds = [(20, 120), (len(rows) - len(rows) // 5, len(rows))]
print(f"{path}: {len(rows)} rounds")
for lo, hi in bounds:
    w = rows[lo:hi]
    print(f"  rounds {lo:>5}-{hi:<5}: {sum(w)/len(w):8.2f} ms/round")
