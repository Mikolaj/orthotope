#!/usr/bin/env python3
"""The gradbench matrix reduction (findings2 items 43-44) over the
harness jsonl logs, which are NOT tracked (gigabytes: the eval inputs
are embedded) -- regenerate them with probe66-gb.sh / probe66-gb2.sh,
then run this beside them.

Per eval and arm: the one-pass seconds -- each evaluate response's
repeats averaged (min-runs/min-seconds pin the repeat TOTAL to the
budget, so summing raw repeats would measure the budget), the means
summed over the eval's workload set -- plus the evaluate-message count,
the truncation tell (item 43's correction: a validation crash ends an
eval early while the harness still exits 0).

  analyze-gb.py PREFIX [EVAL]...   e.g. analyze-gb.py p66gb2 det ode"""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
prefix = sys.argv[1] if len(sys.argv) > 1 else 'p66gb'
evals = sys.argv[2:] or ['det', 'gmm', 'hello', 'kmeans', 'llsq', 'lse',
                         'lstm', 'ode', 'particle', 'saddle']
arms = ['baked', 'a64m', 'a32m', 'al']

def onepass(path):
    tot, nmsg = 0.0, 0
    with open(path) as f:
        for line in f:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = obj.get('message') or {}
            if m.get('kind') == 'evaluate':
                nmsg += 1
            r = obj.get('response') or {}
            ts = [t['nanoseconds'] for t in (r.get('timings') or [])
                  if t.get('name') == 'evaluate']
            if ts:
                tot += sum(ts) / len(ts)
    return tot / 1e9, nmsg

print(f"{'eval':<9}" + "".join(f"{a:>16}" for a in arms)
      + "   one-pass s r1/r2 (evaluate msgs r1)")
for e in evals:
    row = f"{e:<9}"
    n1 = None
    for a in arms:
        v = []
        for r in (1, 2):
            p = os.path.join(here, f'{prefix}-{e}-{a}-r{r}.jsonl')
            if os.path.exists(p):
                s, n = onepass(p)
                v.append(s)
                if a == 'baked' and r == 1:
                    n1 = n
            else:
                v.append(float('nan'))
        row += f"{v[0]:7.3f}/{v[1]:<7.3f} "
    print(row + (f"  ({n1} msgs)" if n1 is not None else ""))
