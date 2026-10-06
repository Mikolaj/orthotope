"""The expensive checks of this directory, run by `check-all checks-deep.py`.

The properties over every run on disk, the case suite in both directions and
the mutants. Until 2026-10-04 they were `check-all .`'s last steps, which
made each run of it after an edit ten to twenty minutes, by the owner's
account, that stopped all other work; since then `check-all .` is `checks.py`'s
static steps alone, and these run once per run preparation, as `preflight.sh
--corpus`'s 8c to 8e, and otherwise when the owner asks -- daily is the
suggestion, rather than after each edit:

    check-all checks-deep.py      # from this directory, in the background

RUN IT ALONE: the cases plant files in this directory and diff the working
tree, so a file created anywhere in it while they run -- a log, a scratch
redirect, an edit committed or not -- makes them report PARTIAL and settle
nothing; and it wants an unsandboxed seat, the fixtures being written here.
Between runs of it, `defect-run.py --changed .` and `--audit --changed .` are
what an edit owes, a script's or a data file's.

SCAN is empty: which programs a step or a case names is `checks.py`'s
question, asked by every `check-all .`. UNCOVERED is `checks.py`'s own, read
from it, because check-all scans every program the records name whatever
SCAN says, and without it those with no case read as checks that did not
run, exiting 2 on four green steps (2026-10-04).
"""

import os
import runpy

SCAN = []
UNCOVERED = runpy.run_path(os.path.join(os.path.dirname(__file__),
                                        'checks.py'))['UNCOVERED']

STEPS = [
    # EVERY RUN ON DISK, as the pre-run list's 8c has always read them: a
    # property that fails only on an older run is caught by this sweep and by
    # nothing else. `check-all .` ran the same file under CORPUS_RUN=newest
    # from 2026-09-09 to keep itself quick, which this file no longer needs.
    ('properties, every run',  ['bash', '-c',
                                'cd "{root}" && python3 properties.py']),
    # Seven at once since 2026-09-18, and not the box's sixteen, so that a
    # run and the session beside it keep their cores; and READ_JOBS=1, since
    # post-run-readings.sh otherwise runs six readers under each of the
    # seven. The cases defects.py's CONFIG names `serial` build here and
    # run alone after the rest.
    ('cases, ok direction',    ['env', 'READ_JOBS=1', 'python3', '{bin}/defect-run.py', '-j', '7', '{root}']),
    ('cases, bug direction',   ['env', 'READ_JOBS=1', 'python3', '{bin}/defect-run.py', '--audit', '-j', '7', '{root}']),
    ('selftest mutants',       ['env', 'READ_JOBS=1', 'python3', '{bin}/selftest-mutants.py', '-j', '7', '{root}']),
]
