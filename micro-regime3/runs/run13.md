# Run 13 (SpecConstr, max-skip / SpecConstr, max-skip +lookrts)

**A back-filled record and not a write-up.** It carries this run's published
per-strategy geomeans against `list` and nothing else. What the run measured,
which half published its tables, and what its delta was are in [README's
Provenance](../README.md#provenance); the findings are in the topical sections
that cite the run by number. Back-filled 2026-08-29 out of the yardstick table
Run 21's file carried, which until then was the only record of these figures.

| strategy | SpecConstr, max-skip | SpecConstr, max-skip +lookrts |
|---|---:|---:|
| `mut-odo-vecdims` | 0.049 | 0.049 |
| `mut-flat-gm` | 0.082 | 0.082 |
| `bq-mut-runs-gm-mulback` | 0.087 | 0.087 |
| `bq-odo-gm-mulback` | 0.090 | 0.090 |
| `bq-scan-rem-gm-mulback` | 0.091 | 0.090 |
| `bq-expand` | 0.103 | 0.102 |
| `build` | 0.099 | 0.099 |
| `offtab` | 0.125 | 0.121 |


## Its delta against the run before

Moved here verbatim from README's Provenance delta chain on 2026-09-23.

- Run 13 measured 840 benches, timing 35 arms and leaving 24 untimed, winsorized
  per the estimator under `time`. **Its delta against RUN 12
  is `mut-flat-gm-nosum` in**, the shapes, class lists and order unchanged. What
  a reader has to carry besides is which half a figure came from: everything
  it published was `run13-maxskip`, and `run13-lookrts` contributed the second
  column of `runs/run13.md` and the arm-by-arm comparison at the head of Run
  13's own write-up, and its class tables are a max-skip half's as Run 12's are,
  which is the one thing that makes the two runs' class figures
  a same-kind-of-build comparison.
