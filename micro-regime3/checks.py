"""The checks of this directory, run by `check-all .` in this order.

`{bin}` is the shared bin directory (`~/.claude/bin`), `{root}` this
directory. Ordered cheapest first, so a broken tree says so before the slow
steps run; the case suite in both directions and the mutants are minutes
each, and `defect-run.py --changed .` is what one edit owes. The two linters
stand since 2026-09-02: pyflakes over the Python here and shellcheck over
the shell drivers, which the AST families cannot reach. An absent linter is
a finding and not a skip, and absent means every invocation the step can
run fails: pyflakes was once reported absent after one failed import while
a `pyflakes` script sat on PATH, and today the script is gone while the
module runs, so the step tries both, and their joint silence fails the step
by name.
"""

# Every tracked shebang file here, the subdirectories being investigations
# and scratch of their own, is a program a step or a case must name, or an
# entry of UNCOVERED.
SCAN = ['*.py', '*.sh']

STEPS = [
    ('records validate',       ['python3', '{bin}/defect-cases.py', '{root}']),
    ('source lint',            ['python3', '{bin}/defect-lint.py', '{root}']),
    ('pyflakes',               ['bash', '-c',
                                'cd "{root}" && { command -v pyflakes >/dev/null || python3 -m pyflakes --version >/dev/null 2>&1 || { echo "pyflakes is not on PATH (command -v pyflakes finds nothing), so the Python here went unlinted"; exit 1; }; } && python3 -m pyflakes *.py']),
    ('shellcheck',             ['bash', '-c',
                                'cd "{root}" && { command -v shellcheck >/dev/null || { echo "shellcheck is not on PATH (command -v shellcheck finds nothing), so the shell scripts here went unlinted"; exit 1; }; } && shellcheck -S warning -f gcc *.sh']),
    ('properties',             ['python3', '{root}/properties.py']),
    ('cases, ok direction',    ['python3', '{bin}/defect-run.py', '{root}']),
    ('cases, bug direction',   ['python3', '{bin}/defect-run.py', '--audit', '{root}']),
    ('selftest mutants',       ['python3', '{bin}/selftest-mutants.py', '{root}']),
]

# Programs with no check, each with its reason: said on every run and never
# counted as a check that did not happen.
UNCOVERED = {
    'preflight.sh': 'its steps are this suite and the reader\'s gates, so a '
                    'case would run them twice; what is its own is proved '
                    'on stub halves in its header',
    'machine-busy.sh': 'read by run-gate.sh, whose cases reach it; no case '
                       'of its own yet',
    'smoke-l1.sh': 'the reader\'s smoke sweep, driven by the run chapter; '
                   'no case yet',
    'check-scripts.py': 'retired into defects.py and the shared tools on '
                        '2026-09-02; the records naming it are memory',
}
# The probes: inputs to README rather than drivers, each run by hand for
# the question it is named for, and none with a case.
for _name in ('probe-attr-build.sh', 'probe-attrnoshim-build.sh',
              'probe-attr-read.py', 'probe-attr.sh', 'probe-disp-build.sh',
              'probe-disp-ghead-build.sh', 'probe-evening-a.sh',
              'probe-evening-b.sh', 'probe-evening-chain.sh',
              'probe-evening-c.sh', 'probe-fillpair-build.sh',
              'probe-fillpair-read.sh', 'probe-fillpair-run.sh',
              'probe-llvmpair.sh', 'probe-noov-build.sh', 'probe-noov-run.sh',
              'probe-noshim-build.sh', 'probe-nospill-build.sh',
              'probe-nospill-fills.py', 'probe-oneblock.py',
              'probe-r23-g3-twins.sh', 'probe-read.sh', 'probe-second-term.py',
              'probe-smoke-runs.sh', 'probe-stalls-read.py', 'probe-stalls.sh',
              'probe-tail-build.sh', 'probe-times.sh'):
    UNCOVERED[_name] = 'a probe: an input to README, run by hand'
