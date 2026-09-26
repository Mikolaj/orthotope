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
module runs, so the step tries both, runs whichever it found, and their
joint silence fails the step by name.
"""

# Every tracked shebang file here, the subdirectories being investigations
# and scratch of their own, is a program a step or a case must name, or an
# entry of UNCOVERED.
SCAN = ['*.py', '*.sh']

STEPS = [
    ('records validate',       ['python3', '{bin}/defect-cases.py', '{root}']),
    ('source lint',            ['python3', '{bin}/defect-lint.py', '{root}']),
    ('pyflakes',               ['bash', '-c',
                                'cd "{root}" && if command -v pyflakes >/dev/null; then pyflakes *.py; elif python3 -m pyflakes --version >/dev/null 2>&1; then python3 -m pyflakes *.py; else echo "pyflakes is not on PATH (command -v pyflakes finds nothing) and python3 -m pyflakes does not import, so the Python here went unlinted"; exit 1; fi']),
    ('shellcheck',             ['bash', '-c',
                                'cd "{root}" && { command -v shellcheck >/dev/null || { echo "shellcheck is not on PATH (command -v shellcheck finds nothing), so the shell scripts here went unlinted"; exit 1; }; } && shellcheck -S warning -f gcc *.sh']),
    # EVERY TRACKED FILE OPENING WITH #! IS COMMITTED 100755, the
    # subdirectories included, since 2026-09-23: Run 39's registration told its
    # reader to run `./probe-r39-rules.py`, committed 100644, and the command
    # answered `Permission denied`; probe-r38-sweep.py and other shebang files
    # here were committed the same way. The INDEX mode and not the disk's,
    # a chmod that was never added being the case that reaches every other
    # checkout. Watched both ways that day: 25 files named before the chmod,
    # none after.
    ('executable bits',        ['bash', '-c',
                                'cd "{root}" && bad=$(git ls-files -s -- . | awk -F"\\t" \'{ split($1, a, " "); if (a[1] == "100644") print $2 }\' | while IFS= read -r f; do [ "$(head -c2 "$f" 2>/dev/null)" = "#!" ] && printf "%s\\n" "$f"; done); if [ -n "$bad" ]; then printf "committed without the executable bit, each opening with #!:\\n%s\\n" "$bad"; exit 1; fi; echo "every tracked file opening with #! is committed 100755"']),
    # The bang checker is horde-ad's, reached through the sibling checkout
    # as the twin-sync check reaches its twin, and BLOCKED with exit 2 when
    # that checkout is not mounted, so an unrun step is never a pass. It
    # exits 0 on whatever it prints unless given --allow, so the allow
    # file is what makes this a gate: a candidate not listed there fails
    # the step, and a listed one prints as read. Added 2026-09-13, the day
    # two lazy binders in the walker were read back out of a flag's worth
    # on Run 30; it names one of them STRONG, the carry's empty clause.
    ('bang shapes',            ['bash', '-c',
                                'cd "{root}" && t=../../horde-ad/tools/bang-lazy-check.py && '
                                '{ [ -f "$t" ] || { echo "BLOCKED: $t is not mounted, so Main.hs went unread for bang shapes"; exit 2; }; } && '
                                'python3 "$t" --allow bang-lazy-allow.txt Main.hs']),
    # CORPUS_RUN=newest, since 2026-09-09: the properties are quantified
    # over every run on disk, and several written-up runs make that sweep
    # minutes. What it buys is about a tenth of this suite's time and not
    # a different order -- the case suites and the mutant replay are the
    # bulk, measured after the change rather than assumed before it, and
    # the first note here said the sweep was what made the suite rare.
    # It narrows the
    # corpus and not the proof -- each property still sweeps everything it
    # is handed and still prints what it covered, so the narrowing is
    # visible in the output rather than silent. Ask for the wider sweep by
    # hand, `./properties.py`, when a run is deleted or added.
    ('properties',             ['bash', '-c',
                                'cd "{root}" && CORPUS_RUN=newest'
                                ' python3 properties.py']),
    # Seven at once since 2026-09-18: run one at a time, these three were
    # nine tenths of a suite of some seventeen minutes, and the whole now
    # runs in some five. Seven and not the box's sixteen, so that a run
    # and the session beside it keep their cores; and READ_JOBS=1, since
    # post-run-readings.sh otherwise runs six readers under each of the
    # seven. The cases defects.py's CONFIG names `serial` build here and
    # run alone after the rest.
    ('cases, ok direction',    ['env', 'READ_JOBS=1', 'python3', '{bin}/defect-run.py', '-j', '7', '{root}']),
    ('cases, bug direction',   ['env', 'READ_JOBS=1', 'python3', '{bin}/defect-run.py', '--audit', '-j', '7', '{root}']),
    ('selftest mutants',       ['env', 'READ_JOBS=1', 'python3', '{bin}/selftest-mutants.py', '-j', '7', '{root}']),
]

# Programs with no check, each with its reason: said on every run and never
# counted as a check that did not happen.
UNCOVERED = {
    'preflight.sh': 'its steps are this suite and the reader\'s gates, so a '
                    'case would run them twice; what is its own is proved '
                    'on stub halves in its header -- and what that costs is '
                    'the record preflight-names-a-retired-callee, three of '
                    'its steps having called a retired script from the '
                    'retirement until the next preparation ran them, with '
                    'nothing here able to see it. THAT REASON COVERS STEPS '
                    'AND NOT REPORTERS: --fill-in, added 2026-09-07, derives '
                    'the pair note\'s fill-in block and runs no step of its '
                    'own, so "a case would run them twice" says nothing '
                    'about it; its control is in the header, every derived '
                    'row read against the same figure taken by hand, and a '
                    'row it gets wrong is caught by nothing else. '
                    '--figures, added 2026-09-10, is the second reporter '
                    'and runs no step either: it re-derives the fill-in '
                    'rows from the artifacts and holds each figure to the '
                    "note's row of its own label and its own half's "
                    'place. Its control is the record '
                    'note-figures-reads-a-row-only-as-present, and not '
                    "the header, since it reads the two binaries and the "
                    'mutants copy holds tracked files alone',
    'machine-busy.sh': 'read by run-gate.sh, whose cases reach it; no case '
                       'of its own yet',
    'copy-test.sh': 'post-run step 4a\'s copy test, which spends the quiet '
                    'box on real binaries under perf; its cells are '
                    '--copy-cells\'s and its log --copy-test\'s, each with '
                    'a case',
    'half-bin.sh': 'the launch path of a half, read by every driver that '
                   'spends the machine, whose cases exercise its no-mount '
                   'branch on stub halves; the mount branch is a box\'s '
                   'and a run\'s to exercise, the corpus copy having no '
                   'tmpfs under it',
    'smoke-l1.sh': 'the reader\'s smoke sweep, driven by the run chapter; '
                   'no case yet',
    'check-scripts.py': 'retired into defects.py and the shared tools on '
                        '2026-09-02; the records naming it are memory',
}
# The probes: inputs to README rather than drivers, each run by hand for
# the question it is named for.
for _name in ('probe-pageflags.py', 'probe-r33-instance.sh',
              'probe-hugebin.sh', 'probe-ibs.sh',
              'probe-attr-build.sh', 'probe-attrnoshim-build.sh',
              'probe-attr-read.py', 'probe-attr.sh', 'probe-cache-build.sh',
              'probe-flip-counters.sh', 'probe-flip-counters-read.py',
              'probe-flip-reroll.sh', 'probe-flip-reroll-read.py',
              'probe-flip-reroll-fixture.py',
              'probe-cache-run.sh', 'probe-disp-build.sh',
              'probe-disp-ghead-build.sh', 'probe-entries-sweep.py',
              'probe-fetches.sh', 'probe-fetches-read.py',
              'probe-fetch-model.py',
              'probe-interleave.sh', 'probe-evening-a.sh',
              'probe-evening-b.sh', 'probe-evening-chain.sh',
              'probe-evening-c.sh', 'probe-fillpair-build.sh',
              'probe-fillpair-read.sh', 'probe-fillpair-run.sh',
              'probe-gate3.py',
              'probe-llvmpair.sh', 'probe-noov-build.sh', 'probe-noov-run.sh',
              'probe-noshim-build.sh', 'probe-nospill-build.sh',
              'probe-oneblock.py', 'probe-order-reversal.sh',
              'probe-r23-g3-twins.sh', 'probe-r32-g3-twins.sh',
              'probe-r34-instance.sh', 'probe-r34-instance2.sh',
              'probe-r38-sweep.py', 'probe-r39-instance.sh',
              'probe-r39-rules.py',
              'probe-read.sh', 'probe-second-term.py',
              'probe-smoke-runs.sh', 'probe-stalls-read.py', 'probe-stalls.sh',
              'probe-tail-build.sh', 'probe-times.sh',
              'probe-within-evening.sh'):
    UNCOVERED[_name] = 'a probe: an input to README, run by hand'
