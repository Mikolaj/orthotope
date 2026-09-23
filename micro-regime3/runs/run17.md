# Run 17 (SpecConstr, max-skip +lookrts, -A32m, instrumented / SpecConstr, max-skip +lookrts, -A32m, plain)

**A back-filled record and not a write-up.** It carries this run's published
per-strategy geomeans against `list` and nothing else. What the run measured,
which half published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr, max-skip +lookrts, -A32m, instrumented | SpecConstr, max-skip +lookrts, -A32m, plain |
|---|---:|---:|
| `mut-odo-vecdims` | 0.055 | 0.055 |
| `mut-flat-gm` | 0.084 | 0.084 |
| `bq-mut-runs-gm-mulback` | 0.093 | 0.092 |
| `bq-odo-gm-mulback` | 0.101 | 0.100 |
| `bq-scan-rem-gm-mulback` | 0.099 | 0.099 |
| `bq-expand` | 0.117 | 0.115 |
| `build` | 0.105 | 0.106 |
| `offtab` | 0.135 | 0.141 |


## Its delta against the run before

Moved here verbatim from README's Provenance delta chain on 2026-09-23.

- Run 17 measured Run 16's shapes, class lists, membership and order,
  so its delta against RUN 16 is empty too. What a reader has to carry there
  is which half a figure came from: everything it published was `run17-wildlog`,
  the instrumented half, and `run17-det` contributed the second column
  of `runs/run17.md` and a class comparison on all eight populations. **And one
  thing that is not a delta**: its two halves differed in `.text` size,
  so a figure crossing them carries a layout term where Runs 14 to 16 carried
  a runtime setting.
