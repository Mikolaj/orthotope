#!/usr/bin/env python3
"""The probe66-conv reduction (findings2 item 42): per-cell victim rate
by fixed-n two-point differencing, ms/iter = (wall(2n) - wall(n)) / n,
over the goal3/p66-<bench>-<arm>-r<rep>-n<n>.time files."""
import os

here = os.path.dirname(os.path.abspath(__file__))
n1 = {'cnn24': 20, 'cnn48': 8, 'cnnbig': 10}
print(f"{'bench':<8} {'arm':<7} {'r1':>8} {'r2':>8}   ms/iter")
for b in ['cnn24', 'cnn48', 'cnnbig']:
    for arm in ['baked', 'a64m', 'a32m', 'al']:
        vals = []
        for r in (1, 2):
            try:
                w = [float(open(os.path.join(
                        here, f'p66-{b}-{arm}-r{r}-n{n}.time')).read())
                     for n in (n1[b], 2 * n1[b])]
                vals.append((w[1] - w[0]) / n1[b] * 1000)
            except FileNotFoundError:
                vals.append(float('nan'))
        print(f"{b:<8} {arm:<7} {vals[0]:8.1f} {vals[1]:8.1f}")
