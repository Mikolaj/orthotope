#!/usr/bin/env python3
"""Steady-state reader for MixedLoad logs: mean round wall over the last
20% of rounds (min/max of that tail beside it), one line per log given."""
import sys

for path in sys.argv[1:]:
    rows = []
    header = ""
    with open(path) as f:
        for line in f:
            if line.startswith("MixedLoad "):
                header = line.strip()
            parts = line.split()
            if len(parts) == 5 and parts[0].isdigit():
                rows.append(float(parts[1]))
    if not rows:
        print(f"{path}: NO ROWS")
        continue
    tail = rows[-max(1, len(rows) // 5):]
    mean = sum(tail) / len(tail)
    print(f"{path}: steady {mean:8.2f} ms/round  "
          f"(tail n={len(tail)}, min {min(tail):.2f}, max {max(tail):.2f}) "
          f" [{header.split('variant=')[1] if 'variant=' in header else '?'}]")
