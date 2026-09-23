# Run 16 (SpecConstr, max-skip +lookrts, -A32m / SpecConstr, max-skip +lookrts, -A64m)

**A back-filled record and not a write-up.** It carries this run's published
per-strategy geomeans against `list` and nothing else. What the run measured,
which half published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr, max-skip +lookrts, -A32m | SpecConstr, max-skip +lookrts, -A64m |
|---|---:|---:|
| `mut-odo-vecdims` | 0.054 | 0.047 |
| `mut-flat-gm` | 0.087 | 0.076 |
| `bq-mut-runs-gm-mulback` | 0.093 | 0.080 |
| `bq-odo-gm-mulback` | 0.100 | 0.087 |
| `bq-scan-rem-gm-mulback` | 0.096 | 0.082 |
| `bq-expand` | 0.114 | 0.101 |
| `build` | 0.109 | 0.097 |
| `offtab` | 0.136 | 0.124 |


## Its delta against the run before

Moved here verbatim from README's Provenance delta chain on 2026-09-23.

- Run 16 measured Run 15's shapes, class lists, membership and order,
  so its delta against RUN 15 is empty too. What a reader has to carry there
  is which half a figure came from: everything it published was `run16-a32m`
  and `run16-a64m` contributed the second column of `runs/run16.md`,
  and **its basis moved off the default nursery**, to the area of `run15-a32m`,
  the half it is checked against, so a row's distance from any column before Run
  16 carries the allocation area with it.
