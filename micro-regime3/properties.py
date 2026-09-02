#!/usr/bin/env python3
"""The properties: claims quantified over every run on disk, not over fixtures.

A case is MEMORY -- one defect already found, planted again, and it can only
ever re-catch that one; the cases are `defects.py`, run by `defect-run.py`.
A property is DISCOVERY: a claim quantified over every real input, which
fails on inputs nobody anticipated. They compose in one direction -- the
property finds the unknown defect, you reduce it by hand, and it becomes a
case with a revision pinned to it.

What makes a property cheap enough to quantify over everything is that it
wants no expected output: each below relates two runs of the reader to each
other -- what it writes against what it reads back -- so there is nothing
to label. That is the test of where a claim belongs. If it needs an
expected answer it is a case; if it only relates runs, ask it of the whole
corpus.

    ./properties.py              # every property, over every run here
    ./properties.py --warnings   # with the reader's own stderr verbatim

`CORPUS` in the environment names another directory of runs, which is how
a case hands these an empty one, or one run built for them. Exit 0 when
every property holds over something, 1 when one fails or the corpus holds
nothing a property reads. Each property's non-vacuity is a mutant in
`mutants.py`, replayed by `selftest-mutants.py`.
"""

import collections
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(HERE, 'README.md')
MAIN = os.path.join(HERE, 'Main.hs')


def _newest_run_doc():
    """The run's own file, which is where everything a run publishes is.

    HALF THE FIXTURES HERE PLANT INTO IT and not into README.md: the
    Results table, the run's own geomeans, the fingerprint, the claims
    verdicts,
    the eight class blocks and the run's own provenance all live in
    `runs/run<N>.md`. An absent one is a
    fixture that cannot be built, so it is an assertion and not a fallback
    to README.md -- which would build every one of them against a
    document that carries none of what they edit, and pass.
    """
    at = os.path.join(HERE, 'runs')
    got = []
    for name in os.listdir(at) if os.path.isdir(at) else []:
        m = re.match(r'^run(\d+)\.md$', name)
        if m:
            got.append((int(m.group(1)), os.path.join(at, name)))
    if not got:
        # BLOCKED at 2, not an assert: a missing corpus is "the run did
        # not happen", and the traceback hit --list too. 2026-09-01.
        print('BLOCKED: no runs/run<N>.md in %s -- the Results table, the'
              ' claims verdicts and the class blocks are all in one, so'
              ' every fixture that plants against them is unbuildable' % at)
        raise SystemExit(2)
    return max(got)[1]


RUNDOC = _newest_run_doc()
# Where the properties look for runs: this directory, or what a case names,
# which is how an empty corpus is handed to them.
CORPUS = os.environ.get('CORPUS', HERE)


def write(path, text):
    with open(path, 'w') as f:
        f.write(text)
    return path


def reader():
    """`read-run.py` as a module, which is the seam it already offers.

    It guards `main()` behind `__name__`, so importing it runs nothing --
    the first of the three seams a program can offer, and the cheapest.
    The hyphen in the name is why this goes through `importlib` rather
    than `import`.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'reader_under_test', os.path.join(HERE, 'read-run.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def runs_on_disk():
    """Every criterion JSON here, which is the live corpus.

    Live rather than pinned, for the reason the fixtures are derived: a
    frozen corpus stops representing what the reader actually meets. The
    properties below are quantified over this, so what they cover grows
    with the directory and a run deleted takes its coverage with it --
    which is why each property PRINTS what it covered. `CORPUS` in the
    environment names another directory, which is how a case hands them
    an empty one, or one run built for them.
    """
    return sorted(f for f in os.listdir(CORPUS)
                  if f.endswith('.json') and not f.startswith('zz'))


def prop_abs_round_trip(m):
    """Every absolute time the reader can write, it can read back.

    Metamorphic: it relates the emitter to the parser and wants no
    expected output, so it can be asked of every figure in every run here
    rather than of a handful of fixtures. That is the whole point --
    `selftest` states this same property over four values chosen by hand,
    and passed while `1e+03 us` was live, because none of the four sat at
    the boundary where `%.3g` rolls a unit over.
    """
    bad, n = [], 0
    for f in runs_on_disk():
        try:
            d = json.load(open(os.path.join(CORPUS, f)))
            benches = d[2]
        except Exception:
            continue
        for b in benches:
            for r in b['reportAnalysis']['anRegress']:
                # The TIME fit alone. Quantified over every responder this
                # asked `fmt_abs` to write allocated BYTES as seconds and
                # then complained that it could not read them back -- a
                # property about something the function is not for, which
                # is the way one of these goes wrong.
                if r.get('regResponder') != 'time':
                    continue
                v = r['regCoeffs'].get('iters', {}).get('estPoint')
                if not isinstance(v, float) or v <= 0:
                    continue
                n += 1
                cell = '| `s` | 3 | 288 | %s | 0.152 |' % m.fmt_abs(v)
                got = m.FINGERPRINT_ABS_RE.match(cell)
                if not got:
                    bad.append('%s: %s writes %r, which --machine cannot'
                               ' parse' % (f, v, m.fmt_abs(v)))
                elif abs(float(got.group(2)) * m.UNIT[got.group(3)] / v
                         - 1) > 0.005:
                    bad.append('%s: %s writes %r, read back as %g'
                               % (f, v, m.fmt_abs(v),
                                  float(got.group(2)) * m.UNIT[got.group(3)]))
    return n, 'per-call time(s) in %d run(s)' % len(runs_on_disk()), bad[:5]


def prop_table_reads_back(m):
    """Every row `--markdown` writes, `readme_rows` finds again.

    The emitter and the reader of one table are a seam the code names in
    so many words -- one literal for the header, so the two cannot drift
    -- and a drift would show as a run's rows installing as new. Relating
    the two runs of the pair needs no expected table, so it is asked of
    every population on disk.
    """
    bad, n = [], 0
    for f in runs_on_disk():
        try:
            cells, shapes, strategies, meta = m.load(
                os.path.join(CORPUS, f), MAIN)
        except SystemExit:
            continue
        except Exception:
            continue
        # The MAIN SET's table only. A class table drops the editorial
        # column deliberately, so that `readme_rows` does not match it and
        # every population's table stops competing to be the one a later
        # run copies from -- asking the read-back of a class table is
        # asking the reader to break a rule it is keeping.
        if m.population_of(shapes, meta['dims'])[0] != 'main':
            continue
        m.apply_correction(cells, shapes, strategies)

        class A:                      # the reader's own argument object
            readme, main, run = README, MAIN, f
            # The Results table the carry-forward reads is the RUN's, and
            # `markdown_table` refuses rather than falling back, so this
            # stand-in has to carry it as the real argument object does.
            run_doc = RUNDOC
        text = m.capture(m.markdown_table, cells, shapes, strategies, meta,
                         A, {})
        rows = [l for l in text.split('\n') if l.startswith('| ')
                and not l.startswith('| strategy |')]
        n += 1
        for line in rows:
            name = re.sub(r'[*`]', '', line.split('|')[1]).strip()
            name = name.replace('(baseline)', '').strip()
            if name and name not in strategies:
                bad.append('%s: emitted a row for %r, which is not an arm of'
                           ' the run' % (f, name))
        got = m.readme_rows(_as_page(text), set(strategies), set(strategies))
        for st in strategies:
            if st not in got:
                bad.append('%s: `%s` was written and not read back'
                           % (f, st))
    return n, 'population(s) on disk', bad[:5]


def _as_page(text):
    """The emitted table as a README `readme_rows` can be pointed at."""
    p = os.path.join(tempfile.gettempdir(), 'zz-prop-README.md')
    return write(p, text)


def prop_selftest_over_the_corpus(m):
    """Every invariant the reader already states, asked of every run here.

    The change this makes is not a new claim -- `--selftest` states
    thirty-four, each of them a property in the same sense -- but WHAT THEY
    ARE QUANTIFIED OVER. They are asked of whatever single file a session
    hands in; asked of the whole directory instead they answer for eighty-
    odd runs across five run numbers, two probes and every smoke artifact
    still on disk, at nine seconds. That is the cheapest of these to have
    and the last one anybody thinks of, the properties being written
    already.

    A subprocess apiece rather than a call, so what is quantified is the
    invocation a reader actually makes: its refusals -- a ragged file, a
    population Main.hs cannot name -- are part of what must hold.
    """
    bad, n = [], 0
    for f in runs_on_disk():
        n += 1
        got = subprocess.run([sys.executable, os.path.join(HERE,
                                                           'read-run.py'),
                              os.path.join(CORPUS, f), '--selftest'],
                             cwd=HERE, capture_output=True, text=True,
                             timeout=300)
        if got.returncode:
            first = [l for l in (got.stdout + got.stderr).split('\n')
                     if l.startswith('FAIL') or 'Traceback' in l]
            bad.append('%s: exit %d%s' % (f, got.returncode,
                                          ' -- ' + first[0] if first else ''))
    return n, 'run(s) on disk, every invariant of each', bad[:5]


PROPERTIES = [prop_abs_round_trip, prop_table_reads_back,
              prop_selftest_over_the_corpus]

# All three broken deliberately, 2026-08-17, because a property that has
# never failed has proved nothing: labelling seconds `ns` fails the
# round-trip on every figure it reaches, widening `readme_rows`' column
# test by one fails the read-back on every row, and a reader that refuses
# everything fails the third on every run. Each was green again on
# reverting, and each named the file it failed on rather than a count.
# The first attempt at the first proved nothing: the formatter it
# substituted looked wrong and was arithmetically right, so the property
# held -- a break has to break the property, not merely the code.
#
# Three cautions, all paid for here. The first is that these are not new
# claims so much as old ones asked of more: `--selftest` had thirty-four
# invariants and asked them of one file at a time, and the whole of the
# third property is asking them of every file instead. Reach for that
# before writing a property.
#
# A property has to be about what the
# thing is FOR: quantified over every regression this asked `fmt_abs` to
# write allocated bytes as seconds, and quantified over every population it
# asked a class table to be read back, which the reader declines on
# purpose. Both read as defects and neither was one. And a property gate
# DETECTS without localising -- it named a run and a figure, and which of
# `%.3g`'s two exponent thresholds was at fault was a question for the
# person, not the gate.


def properties(warnings=False):
    """Every property, over the live corpus, naming what failed.

    WITHHOLDS THE READER'S OWN STDERR BY DEFAULT, and says how much and of
    what kinds. These properties drive `read-run.py` over every run on
    disk, so the reader warns once per run per table about rows a later
    roster no longer carries -- correct, expected, and on 2026-08-22
    **198 KB over 258 lines against six lines of verdict**. A pass whose
    signal is outnumbered thirty to one is a pass that gets piped through
    `tail`, and a pipe throws away the exit code this whole file is.

    The kinds are kept and counted rather than dropped: what is withheld
    is the repetition, not the fact, so a warning the corpus has never
    shown before still appears -- as a kind with a count of one. `
    --warnings` restores them verbatim, which is the flag to reach for
    when a kind is new or a count moves.

    Nothing a property itself says is touched. Their verdicts and the
    `off` lines behind a FAIL are stdout and print after the loop, so a
    failure reads the same either way.
    """
    m = reader()
    bad, buf = 0, io.StringIO()
    keep = contextlib.nullcontext() if warnings else contextlib.redirect_stderr(buf)
    with keep:
        got = [(prop, prop(m)) for prop in PROPERTIES]
    for prop, (n, what, off) in got:
        if not n:
            # An empty search proves nothing, and the guards against one
            # in read-all.sh and install-tables.sh are cases here; this
            # had none, and over a directory with no run in it said `every
            # property holds` over 0. Found 2026-08-22 by review. Case:
            # `properties-refuse-an-empty-corpus`.
            off = ['0 %s under %s: an empty corpus proves nothing, and so'
                   ' does one holding nothing this property reads'
                   % (what, CORPUS)]
        if off:
            bad += 1
            print('  FAIL %-28s over %d %s' % (prop.__name__, n, what))
            for line in off:
                print('       %s' % line)
        else:
            print('  ok   %-28s over %d %s' % (prop.__name__, n, what))
    held = [l for l in buf.getvalue().split('\n') if l.strip()]
    if held:
        kinds = collections.Counter(
            re.sub(r'\d+', 'N', l.split(';')[0].strip())[:96] for l in held)
        print('\n  %d line(s) of reader warning withheld, in %d kind(s);'
              ' --warnings for them verbatim:' % (len(held), len(kinds)))
        for k, c in kinds.most_common():
            print('    %5d x %s' % (c, k))
    return bad


def main():
    args = sys.argv[1:]
    if args in (['-h'], ['--help']):
        sys.stdout.write(__doc__)
        return 0
    if args not in ([], ['--warnings']):
        sys.exit('properties.py: --warnings or nothing (see --help)')
    print('properties over the live corpus:')
    bad = properties(warnings=bool(args))
    if bad:
        print('\n%d propert(ies) FAILED' % bad)
        print('VERDICT: FAIL (exit 1)')
        return 1
    print('\nevery property holds')
    return 0


if __name__ == '__main__':
    sys.exit(main())
