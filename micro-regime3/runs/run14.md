# Run 14 (SpecConstr, max-skip +lookrts / SpecConstr, max-skip +lookrts +A1G)

**A back-filled record and not a write-up.** It carries this run's published
per-strategy geomeans against `list` and nothing else. What the run measured,
which half published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr, max-skip +lookrts | SpecConstr, max-skip +lookrts +A1G |
|---|---:|---:|
| `mut-odo-vecdims` | 0.049 | 0.051 |
| `mut-flat-gm` | 0.081 | 0.083 |
| `bq-mut-runs-gm-mulback` | 0.087 | 0.088 |
| `bq-odo-gm-mulback` | 0.090 | 0.095 |
| `bq-scan-rem-gm-mulback` | 0.091 | 0.090 |
| `bq-expand` | 0.102 | 0.107 |
| `build` | 0.103 | 0.097 |
| `offtab` | 0.121 | 0.121 |


## Its delta against the run before

Moved here verbatim from README's Provenance delta chain on 2026-09-23.

- Run 14 measured 47 timed arms over 24 main-set shapes and 24 class views
  in eight classes, 1128 benches. **Its delta against RUN 13** is **twelve A/A
  twins in** (`offtab`, `bq-odo-gm-mulback`, `build`, `mut-odo`, `list`
  and `gen-unsafe`, each in both positions) and a third shape in the **five
  class views** Run 13 ran short of one, the shapes, class lists and roster
  **order** otherwise unchanged. What a reader has to carry there is
  that its control was `run14-a1g`, at two hundred and fifty-six times
  the default nursery, and that its halves' absolutes were not subtractable.
