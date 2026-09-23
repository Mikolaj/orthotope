# Run 15 (SpecConstr, max-skip +lookrts / SpecConstr, max-skip +lookrts +A32m)

**A back-filled record and not a write-up.** It carries this run's published
per-strategy geomeans against `list` and nothing else. What the run measured,
which half published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr, max-skip +lookrts | SpecConstr, max-skip +lookrts +A32m |
|---|---:|---:|
| `mut-odo-vecdims` | 0.048 | 0.054 |
| `mut-flat-gm` | 0.081 | 0.088 |
| `bq-mut-runs-gm-mulback` | 0.086 | 0.094 |
| `bq-odo-gm-mulback` | 0.090 | 0.100 |
| `bq-scan-rem-gm-mulback` | 0.091 | 0.096 |
| `bq-expand` | 0.102 | 0.114 |
| `build` | 0.102 | 0.110 |
| `offtab` | 0.126 | 0.138 |


## Its delta against the run before

Moved here verbatim from README's Provenance delta chain on 2026-09-23.

- Run 15 measured Run 14's shapes, class lists, membership and order,
  so its delta against RUN 14 is empty too. What a reader has to carry there
  is which half a figure came from: everything it published was `run15-lookrts`,
  the default-nursery half, and `run15-a32m` contributed the second column
  of `runs/run15.md`. **And one input that is not a delta and not a half**:
  the dependency store, whose 48 packages were rebuilt between the two runs
  at unchanged versions, so Run 14's binary and this one share no package ABI
  hash. The assembler shim also moved, `9a70576` against `89c7ae8`,
  and is emission-neutral.
