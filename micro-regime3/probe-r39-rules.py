#!/usr/bin/env python3
"""Adjudicate Run 39's item (2): the arms slower past the mover bar on BOTH
halves against Run 38, over every population both runs have, which are
the candidates a hand reading with LOOP_TRACE then sorts.

    ./probe-r39-rules.py run39 run38   # exit 0 none, 1 candidates, 2 did not run

`LOOP_SETTLED=1` moves loop heads on both halves alike, so an arm slower
on one half against the previous run is that half's instance or build,
which post-run step 4a's `--half-movers` names, and an arm slower on BOTH
halves is where the switch's bet is read --- the back edge's three rules
charged to loops they were not read on. `--half-movers` lists one-half
movers by construction, so this reads `--compare` of each half against
the previous run's same half and keeps the arms past the bar in the
slower direction on both. The bar is the chapter's mover bar, 3 percent,
or the population's floor where that is higher: at the floor alone Run
38 against Run 37, the same recipes with the source moved, names nine
arms, and at 3 percent three, `flip` and `small` cells of loops no rule
touched, so a cross-run reading at the floor is the box's and not the
rules'. Each candidate is read by hand: `LOOP_TRACE` on its hot loop's
head says whether the settled cost moved it and for which rule, and a
candidate moved for the first-eight or last-four rule alone is the kill.
Reads only, from the directory it sits in. 2026-09-22.
"""
BAR = 0.03
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HALVES = ('gheadnospec', 'gheadtwopass')
POPS = ('main', 'bcast', 'bcastmid', 'block', 'compose', 'flip', 'rev',
        'runs', 'scaled', 'small', 'window')
ROW = re.compile(r'^(\S+)\s+([0-9.]+)\s+([0-9.]+)\s+(\d+)/(\d+)\s')
FLOOR = re.compile(r'^(\S+) -- floors ([0-9.]+)% on (\S+), ([0-9.]+)% on (\S+)')


def reader(*args):
    got = subprocess.run(['python3', os.path.join(HERE, 'read-run.py')] + list(args),
                         capture_output=True, text=True, cwd=HERE)
    if got.returncode not in (0, 1):
        sys.exit('probe-r39-rules: read-run.py %s exited %d: %s'
                 % (' '.join(args), got.returncode, got.stderr.strip()[-200:]))
    return got.stdout


def json_of(run, half, pop):
    return os.path.join(HERE, f'{run}-{half}-{"main" if pop == "main" else pop}.json')


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.split('\n')[3].strip())
    run, prev = sys.argv[1], sys.argv[2]
    main_json = json_of(run, HALVES[0], 'main')
    if not os.path.exists(main_json):
        sys.exit(f'probe-r39-rules: {os.path.basename(main_json)} is not here; nothing ran')
    floors = {}
    for line in reader(main_json, '--half-movers', run, prev).split('\n'):
        m = FLOOR.match(line)
        if m:
            floors[m.group(1)] = {m.group(3): float(m.group(2)) / 100,
                                  m.group(5): float(m.group(4)) / 100}
    killed, read = [], 0
    for pop in POPS:
        if pop not in floors:
            continue
        ratios = {}
        for half in HALVES:
            a, b = json_of(run, half, pop), json_of(prev, half, pop)
            if not (os.path.exists(a) and os.path.exists(b)):
                break
            for line in reader(a, '--compare', b).split('\n'):
                m = ROW.match(line)
                if m:
                    ratios.setdefault(m.group(1), {})[half] = float(m.group(2))
        else:
            read += 1
            for arm, r in sorted(ratios.items()):
                if len(r) == 2 and all(r[h] > 1 + max(BAR, floors[pop][h])
                                       for h in HALVES):
                    killed.append((pop, arm, r[HALVES[0]], r[HALVES[1]]))
    if not read:
        sys.exit('probe-r39-rules: no population had both halves of both runs; nothing ran')
    for pop, arm, x, y in killed:
        print(f'  {pop:9s} {arm:40s} {x:.4f} {y:.4f}  slower past the bar on both')
    print(f'{len(killed)} candidate(s) slower past the bar on both halves against'
          f' {prev}, over {read} population(s)'
          + (': read each with LOOP_TRACE on its hot loop\'s head' if killed
             else ''))
    return 1 if killed else 0


if __name__ == '__main__':
    sys.exit(main())
