# Run 12 (SpecConstr, max-skip / SpecConstr, max-skip +procalign)

**A back-filled record and not a write-up.** It carries this run's published
per-strategy geomeans against `list` and nothing else. What the run measured,
which half published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr, max-skip | SpecConstr, max-skip +procalign |
|---|---:|---:|
| `mut-odo-vecdims` | 0.049 | 0.049 |
| `mut-flat-gm` | 0.081 | 0.082 |
| `bq-mut-runs-gm-mulback` | 0.087 | 0.088 |
| `bq-odo-gm-mulback` | 0.090 | 0.090 |
| `bq-scan-rem-gm-mulback` | 0.090 | 0.091 |
| `bq-expand` | 0.102 | 0.102 |
| `build` | 0.098 | 0.098 |
| `offtab` | 0.125 | 0.131 |


## Its delta against the run before

Moved here verbatim from README's Provenance delta chain on 2026-09-23.

- Run 12 measured Run 11's shapes, class lists, order and roster, so its delta
  against RUN 11 is empty --- 816 benches, timing 34 arms, winsorized likewise.
  Everything it published was `run12-maxskip`, `run12-maxskippa` contributing
  the second column of `runs/run12.md`, and its class tables are a max-skip
  half's.
