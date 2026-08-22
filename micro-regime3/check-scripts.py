#!/usr/bin/env python3
"""Every defect these scripts have had, planted again and refused again.

    ./check-scripts.py              # every case against the working tree
    ./check-scripts.py --audit      # every case against the code before its
                                    #   own fix, where it MUST fail
    ./check-scripts.py -k install   # the cases whose name matches
    ./check-scripts.py --list       # what is covered, and by which fix
    ./check-scripts.py --against REV  # diagnose some other revision
    ./check-scripts.py --properties # the properties, over every run on disk

TWO HALVES, and they are not the same instrument. A case is MEMORY: one
defect already found, planted again, and it can only ever re-catch that
one. A property is DISCOVERY: a claim quantified over every real input,
which fails on inputs nobody anticipated. They compose in one direction --
the property finds the unknown defect, you reduce it by hand, and it
becomes a case with a revision pinned to it.

What makes a property cheap enough to quantify over everything is that it
wants no expected output: each below relates two runs of the reader to each
other -- what it writes against what it reads back -- so there is nothing
to label. That is the test of where a claim belongs. If it needs an
expected answer it is a case; if it only relates runs, ask it of the whole
corpus.

EVERY PROGRAM HERE OWES ONE WAY TO BE DRIVEN, checked in, so that vetting a
claim costs a line rather than a harness. Four sessions of review here
built four harnesses and threw all four away, which is why two of these
scripts reached this week never once executed by anything but a real run.
The seams, in the order worth having them: `read-run.py`, `align-as.py`,
`loop-offsets.py` and this file guard `main()` behind `__name__`, so they
import clean and `--unit` evaluates against them (through `importlib`, the
hyphen in the name being no module name at all -- a decision made years
ago that decides testability). `install-tables.sh`, `read-all.sh`,
`run-gate.sh`, `run-major.sh` and `smoke-sweep.sh` take every path and
constant they need from the environment with a default -- `DOC`, `BASIS`,
`OTHER`, `SHAPE`, `CLASS` -- which is the second seam, and it is what lets
a case point them at a copy. And where a driver wants a BINARY, the
stand-in is checked in here: `FAKE_HALF` for the gate's listing,
`FAKE_RUN` for the two that want a whole run's cells.

--audit REPLAYS TODAY'S FIXTURES AGAINST YESTERDAY'S CODE, so a change to
the README's own conventions can put a case beyond its own history: code
from before it cannot read a fixture built after. That is expected, it is
not a defect, and the handling is to drop the case's `bug` verdict, which
takes it out of --audit and leaves it guarding forward. Four install cases
went that way at the 2026-08-20 Basic Latin pass. Do not pin the
convention into the fixtures instead: that is the second copy of it.

A REVIEW CLAIM IS SUBMITTED IN THE CASE FORMAT, or it costs a harness to
vet. `(name, plant, argv, ok, bug)` is already a probe: running it IS
vetting the claim, and a claim that survives is already a case with no
translation step. Two claims this week were right about a symptom and
wrong about its trigger, and each cost an implementation to find out; one
execution apiece would have said so.

WHY THIS EXISTS, since `read-run.py` says to extend it rather than write a
second reader and this is the exception. Two reviews of these scripts on
2026-08-17 found thirty defects between them, and `--selftest` -- 34
assertions -- caught none: it calls no checker, no installer, no doc sweep
and no flag guard, asserting the numeric path instead, so three of the
thirty were even in code it executes. The one seam it did cover, `fmt_abs`
against `FINGERPRINT_ABS_RE`, it covered vacuously, sampling four values and
none near the boundary the defect was at. Meanwhile each fix was proved by
running the new file beside `git show HEAD:...` -- a proof that EXPIRES the
moment the fix is committed, because HEAD is then the fixed version. Thirty
proofs were made that day and none of them could be re-run the next.

So this is not a second reader; it drives the ones there are, from outside,
and its subject is their behaviour rather than any run's numbers. It belongs
beside `--selftest` and not inside it: a case is a whole invocation, exit
code and stderr included, which is exactly what a function-level check
cannot see and is where the defects were.

WHAT A CASE IS. Both directions, always: `ok` is what the fixed code must
do and `bug` is what the code before the fix did. The default run asserts
`ok`; `--audit` re-materialises the script as of the commit BEFORE its fix
and asserts `bug`, which is how this suite proves it is not vacuous -- the
rule the rest of this directory already follows, turned on the tests
themselves. A case whose `bug` is None is a control rather than a defect,
and `--audit` says so instead of checking it.

HOW TO ADD ONE, and the answer is before you fix anything. A review claim
becomes a case first, red; then the fix turns it green. The `fix` field is
filled in afterwards and cannot be otherwise -- a case naming the commit
that carries it would change that commit's hash by being written into it --
so the order of WORK is case, fix, case-green, while the order of COMMITS
is the fix and then the case that guards it, one behind. Two claims in the
second review were partly wrong and a case would have shown it for nothing,
where finding out cost a full implementation each time. The rule the other
way round matters more: a fix with no case here is a fix that will come
back, and it has -- `--in-place` was accepted-but-never-read in one review
and `--brief` was the same defect six commits later, while a dropped
`objdump` status was found once and was sitting in two other functions.

FIXTURES ARE DERIVED, NEVER STORED. Every plant below reads the live
README.md or a live run JSON and edits a copy, and every anchor it edits is
either found structurally (the yardstick header by the rule `check_doc`
uses, a class table by its block lead) or asserted to occur exactly once.
A stored copy of the README would rot silently as the README moved, which is
the same reason the checkers themselves read the live document. When an
anchor does go, the case FAILS saying which -- loudly, as a fixture that
cannot be built, never as a pass.

IT LEAVES THE TREE AS IT FOUND IT. Cases write into a temp directory; the
few that cannot -- `read-all.sh` globs its own directory -- write `zz-`
files here and remove them, and the run ends by comparing `git status
--porcelain` against what it saw at the start and failing on any
difference. Nothing here stages, commits, or edits a tracked file: the one
case that needs a STAGED file builds a throwaway index with GIT_INDEX_FILE
and leaves the real one alone.

WHAT IT DOES NOT COVER, so its silence is not read as a clean bill.
Every defect either review found, and every one found beside them, has a
case here but one: the correction's positivity test in `selftest`, which is
subsumed by the malformed-cell check above it and so cannot fail on its own
-- untestable by construction rather than untested, and `read-run.py` says
as much where the code is. The other absence is whole files. `run-major.sh`,
`run-major.sh` and `smoke-sweep.sh` have no case. `run-gate.sh` now has
one, and how it got there is what those two want too: a shadow directory
with a stand-in for `$PREFIX-$half` that answers `--list` and runs no
bench, which takes the whole gate -- four processes and its verdict -- to
a second. The drivers had no finding in either of the first two reviews
and one in the third, which was never evidence that they are clean: they
are what commits the machine for hours, a defect in one is the most
expensive kind here, and the two shell scripts anyone did read closely
yielded the highest defect density in the tree -- 1.9 and 0.9 per hundred
lines against `read-run.py`'s 0.47. What is left is to write their
stand-ins, `run-major.sh` wanting `check`, `diag` and a JSON per process
where the gate wanted only a listing.

WHAT `--audit` STILL PAIRS LOOSELY, recorded rather than fixed. It reads
the script as of the commit before its fix and the fixture from TODAY's
README, which is sound wherever the defect is in the code and the fixture is
merely an input of the right shape -- which is every case here. It would
not be sound for a case whose defect is about the README's own shape, where
the anchor's form at the old revision is part of what is being reproduced:
such a case should pin the document's revision alongside the script's.
None does yet. What is in place is the cheaper half, and it is what makes
the gap visible rather than quiet: the outcome is three-valued, so a plant
that will not build is neither a pass nor a failure but says so, where it
used to be counted as a defect that did not reproduce -- which happened
here, to a case stamped with an unexpanded shell substitution.

THREE INSTRUMENTS, and each finds what the other two cannot. A case is
memory, over one input someone has already met. A property is discovery
over DATA, quantified across every run on disk. `--families` is discovery
over CODE: the shapes these defects keep returning in, counted rather than
guessed -- a dropped subprocess status (four instances across the three
reviews), an argparse flag accepted and never read (three), a value parsed
out of the environment at import (two), a positional `zip` against a
filtered list (three). It is the only one of the three that can name a
site nobody has looked at.

It was written and thrown away once before it was checked in, which is
this file's own complaint about harnesses made against itself. The fifth
family that used to be listed here -- a check reporting in one branch with
no else -- is deliberately absent, and `family_lint` carries the
measurement that ruled it out.

NOT BUILT YET, and recorded here so it is not re-derived. Making the two
rules above bite: a
commit that fixes a defect naming the case that guards it, and a claim
settled by a red case before any code moves. Neither is coded here because
neither needs code -- what they need is for this file to be read, which is
why `read-run.py`, `README.md` and every script with a case in it point at
it.
"""

import argparse
import ast
import atexit
import collections
import contextlib
import importlib.util
import io
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(HERE, 'README.md')
MAIN = os.path.join(HERE, 'Main.hs')
CLASS_HDR = '| strategy | time | worst | CI% | smp | alloc |'

# Files a case had to write into this directory rather than into its temp
# dir, removed however the run ends.
STRAY = []


def here_file(name):
    """A path in this directory, registered for removal."""
    p = os.path.join(HERE, name)
    STRAY.append(p)
    return p


def sweep():
    for p in STRAY:
        try:
            os.remove(p)
        except OSError:
            pass
    del STRAY[:]


atexit.register(sweep)


def git(*args):
    return subprocess.run(('git',) + args, cwd=HERE, capture_output=True,
                          text=True)


def tree_delta(before, after):
    """What changed between two `git status` readings, BOTH directions.

    It printed `set(after) - set(before)` -- additions only -- so a run that
    REMOVED something tripped the comparison and then reported an empty
    list under `!! this run changed the working tree`, which is a headline
    with nothing beneath it and the reader left to guess what went. A
    fixture deleted rather than left behind is exactly the direction this
    suite errs in, so it was the likelier half. Found 2026-08-17 by a
    walker reading the source.
    """
    was, now = set(before.split('\n')), set(after.split('\n'))
    return (['   + %s' % l for l in sorted(now - was) if l.strip()]
            + ['   - %s (gone)' % l for l in sorted(was - now) if l.strip()])


def tree_state():
    """What `git status` says, or None if it could not say anything.

    The run ends by comparing this against what it saw at the start, and
    the comparison read `.stdout` alone -- so a `git` that failed gave the
    empty string both times, the two matched, and the ONE guarantee this
    file makes about itself passed without being checked. That is the
    empty-search defect it carries cases about, in the file that carries
    them. Found 2026-08-17 by asking what this suite covers.
    """
    got = git('status', '--porcelain')
    return None if got.returncode else got.stdout


# ---------------------------------------------------------------- fixtures

def readme_lines(rev=None):
    """This README, as of `rev` when a revision is being replayed.

    `--check-doc` resolves the `README.md#` anchors it finds in the
    READER'S OWN source, so a replayed revision carries the anchors of its
    day -- and post-run step 5 renames four headings every write-up. Run
    against today's README, an old reader therefore fails on dead anchors of
    its own, which is not the defect any case here is about: it is what
    took `checkdoc-without-a-roster` and `checkdoc-open-list-out-of-order`
    out of --audit, both wanting exit 0 and both getting 1. Replaying the
    code means replaying the README.
    """
    return (open(README).read() if rev is None
            else at_rev('README.md', rev)).split('\n')


def era_readme(tmp, rev, name='era-README.md'):
    """This README as of `rev`, as a file a case can point `--readme` at."""
    p = os.path.join(tmp, name)
    write(p, '\n'.join(readme_lines(rev)))
    return p


def write(path, text):
    with open(path, 'w') as f:
        f.write(text)
    return path


def edited_readme(tmp, *edits, **kw):
    """A copy of the live README with each (old, new) applied exactly once.

    The count is asserted rather than assumed, and a miss raises here --
    where it reads as a fixture that could not be built -- rather than
    producing a copy the case then passes over.
    """
    text = open(README).read()
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            raise AssertionError('anchor occurs %d times, need 1: %r'
                                 % (n, old[:60]))
        text = text.replace(old, new, 1)
    return write(os.path.join(tmp, kw.get('name', 'R.md')), text)


def class_table_span(lines, cls):
    """(first, last) line indices of a class block's table, found its way.

    By the block's bolded lead and then the shared six-column header, which
    is how `--in-place` narrows and how a reader would look.
    """
    lead = [i for i, l in enumerate(lines) if l.startswith('**`%s`' % cls)]
    assert len(lead) == 1, 'lead `%s`: %d line(s)' % (cls, len(lead))
    i = next(j for j in range(lead[0], len(lines)) if lines[j] == CLASS_HDR)
    j = i
    while j < len(lines) and lines[j].startswith('|'):
        j += 1
    return i, j


def readme_with_ragged_row(tmp):
    """A copy whose yardstick table has one row two cells short.

    This is the defect exactly as it arose: the four bottom rows of the
    yardstick were written when the table had two columns, and every run
    since prepended one or two more without padding them, so their values
    drifted left and came to sit under the wrong runs' headers. Nothing
    read it -- markdown renders a short row without complaint, every
    anchor and figure check passed over it, and the prose went on saying
    the values were Run 8's while the table put them five columns away.
    Recovered from git (`f42ef4a`, where the table was two columns wide)
    rather than guessed, 2026-08-20.
    """
    lines = open(README).read().split('\n')
    h = next(i for i, l in enumerate(lines) if l.startswith('| strategy |')
             and '(' in l)
    for i in range(h + 2, len(lines)):
        if not lines[i].startswith('|'):
            raise AssertionError('no data row found under the yardstick')
        cells = lines[i].split('|')[1:-1]
        if len(cells) > 4:
            lines[i] = '|' + '|'.join(cells[:1] + cells[3:]) + '|'
            break
    return write(os.path.join(tmp, 'R.md'), '\n'.join(lines))


def readme_without_class_table(tmp, cls='slice'):
    lines = readme_lines()
    i, j = class_table_span(lines, cls)
    del lines[i:j]
    return write(os.path.join(tmp, 'R.md'), '\n'.join(lines))


def readme_yardstick_renamed_with_qmark(tmp):
    """The yardstick header renamed, and a `?` left in a published cell.

    The header is found by `check_doc`'s own rule, so this fixture cannot
    drift from the check it provokes.
    """
    lines = readme_lines()
    yard = [i for i, l in enumerate(lines)
            if l.startswith('| strategy |') and '(' in l]
    assert len(yard) == 1, 'yardstick header: %d line(s)' % len(yard)
    lines[yard[0]] = lines[yard[0]].replace('| strategy |', '| stratXgy |', 1)
    cell = re.compile(r'\| `[a-z0-9-]+` \| \d+ \| \d+ \| [\d.]+ [num]?s \|')
    fp = [i for i, l in enumerate(lines) if cell.match(l)]
    assert fp, 'no fingerprint row to plant a `?` in'
    lines[fp[0]] = re.sub(r'\| [\d.]+ [num]?s \|', '| ? |', lines[fp[0]], 1)
    return write(os.path.join(tmp, 'R.md'), '\n'.join(lines))


def readme_goal_above_open(tmp, rev=None):
    """The goal section moved above the open list: nothing renamed.

    The case the first repair missed -- renaming a heading trips a
    neighbouring check, where reordering trips none.
    """
    lines = readme_lines(rev)
    lo = next(i for i, l in enumerate(lines)
              if l.startswith('## What is open'))
    hi = next(i for i, l in enumerate(lines) if l.startswith('## The goal'))
    end = next((j for j in range(hi + 1, len(lines))
                if lines[j].startswith('## ')), len(lines))
    goal, rest = lines[hi:end], lines[:hi] + lines[end:]
    return write(os.path.join(tmp, 'R.md'),
                 '\n'.join(rest[:lo] + goal + rest[lo:]))


def readme_summary_row_short(tmp, cls='slice'):
    lines = readme_lines()
    at = [i for i, l in enumerate(lines) if l.startswith('| `%s` |' % cls)]
    assert len(at) == 1, 'summary row `%s`: %d line(s)' % (cls, len(at))
    cells = lines[at[0]].rstrip().rstrip('|').split('|')
    lines[at[0]] = '|'.join(cells[:-1]) + '|'
    return write(os.path.join(tmp, 'R.md'), '\n'.join(lines))


def readme_with_trailing_buried_action(tmp):
    return write(os.path.join(tmp, 'R.md'), open(README).read()
                 + '\n## A trailing checklist\n\n'
                   '    # then run ./read-run.py --survey to see it\n'
                   '    echo hello\n')


def readme_current_run_sentence(tmp):
    """A verdict sentence attributing a figure to the run in hand.

    Its own PARAGRAPH, under the claim's lead, because the sweep reads a
    paragraph at a time and splits it into sentences: appended to the lead
    LINE, which is where this fixture started, the sentence lands inside
    another one and the figure is never reached.
    """
    doc = open(README).read()
    run = re.search(r'^## About the last run \(Run (\d+)\)$', doc, re.M)
    assert run, 'no run chapter heading to take the run number from'
    paras = doc.split('\n\n')
    at = [i for i, p in enumerate(paras) if p.startswith('**Claim 3 ')]
    assert len(at) == 1, 'claim 3 lead: %d paragraph(s)' % len(at)
    paras.insert(at[0] + 1, 'In Run %s, `bq-expand` reads 0.9312 against'
                            ' it.' % run.group(1))
    return write(os.path.join(tmp, 'R.md'), '\n\n'.join(paras))


def readme_citing_dotfile(tmp):
    return edited_readme(tmp, ('\n## What is open',
                               '\nhorde-ad keeps its hlint exceptions in'
                               ' `.hlint.yaml`.\n\n## What is open'))


def readme_stale_basis_in_results(tmp):
    """The Results section naming a half of the run BEFORE this chapter's.

    Run 14's write-up shipped exactly this -- `run13-maxskip` standing in
    that lead while run14-lookrts's tables were installed under it -- past
    --lint, --check-doc, --selftest and --aa, none of which read the name.
    The plant is derived from the README rather than spelled out, so it keeps
    working when the chapter's run number moves, and it asserts what it
    swept: a Results section naming no run, or naming two, would leave the
    check passing for its own reasons.
    """
    lines = open(README).read().split('\n')
    start = next(i for i, l in enumerate(lines)
                 if l.startswith('### Results'))
    end = next(j for j in range(start + 1, len(lines))
               if re.match(r'#{1,6} ', lines[j]))
    seg = '\n'.join(lines[start:end])
    runs = set(re.findall(r'\brun(\d+)-[a-z0-9]+', seg))
    if len(runs) != 1:
        raise AssertionError('Results names %d run(s), not one: %s'
                             % (len(runs), sorted(runs)))
    cur = runs.pop()
    lines[start:end] = seg.replace('run%s-' % cur,
                                   'run%d-' % (int(cur) - 1)).split('\n')
    return write(os.path.join(tmp, 'R.md'), '\n'.join(lines))


def readme_without_class_leads(tmp):
    """Every class block lead unbackticked, so the grep finds none.

    `install-tables.sh` checks that no class is silently skipped by holding
    the JSONs on disk to the README's leads, and the check was itself silent
    when its own search came back empty.
    """
    src = open(README).read()
    doc, n = re.subn(r'(?m)^\*\*`([a-z0-9]+)`', r'**\1', src)
    # A sweep, so it says what it swept: a plant that quietly matches
    # nothing -- or matches something else -- leaves the old script failing
    # for its own reasons and the audit certifying a non-vacuity nobody
    # demonstrated. The property is that leads existed and that none is
    # left, not how many there were.
    if not n or re.search(r'(?m)^\*\*`[a-z0-9]+`', doc):
        raise AssertionError('unbackticked %d lead(s) and %s remain' %
                             (n, 'some' if n else 'all'))
    return write(os.path.join(tmp, 'R.md'), doc)


def readme_chapter_renamed(tmp):
    return edited_readme(tmp, ('\n## About the last run (Run',
                               '\n## About the previous run (Run'))


def readme_heading_between_blocks(tmp):
    """A section, with a `Provenance:` paragraph, between two class blocks.

    `install-tables.sh` gives each block the range up to the next LEAD and
    stops at a heading for the last block only, so anything of that shape
    standing between two blocks is inside the range of the one above it.
    """
    paras = open(README).read().split('\n\n')
    at = [i for i, x in enumerate(paras) if x.startswith('**`revsome`')]
    assert len(at) == 1, 'revsome lead: %d paragraph(s)' % len(at)
    paras[at[0]:at[0]] = ['### A section standing between two class blocks',
                          'Provenance: ZZMARKER, and this paragraph is'
                          ' nobody\'s to rewrite.']
    return write(os.path.join(tmp, 'R.md'), '\n\n'.join(paras))


def untracked_doc(tmp):
    """A document in this directory that no index knows about.

    The sibling of `staged_doc`: `git diff` says nothing about an untracked
    path AND exits 0, which is the empty set rather than the sentinel, so
    a README worked on before it is added had every hit called old.
    """
    doc = here_file('zz-case-untracked.md')
    write(doc, open(README).read()
          + '\nThe fastest arm of every population is the one this planted'
            ' sentence pretends to name, which makes it the biggest'
            ' superlative in the README.\n')
    return {'doc': os.path.basename(doc)}


def bad_alloc_fit(benches, want):
    """One cell's ALLOCATED fit made unreadable, its time fit left alone."""
    hit = 0
    for b in benches:
        if b['reportName'] != want:
            continue
        for r in b['reportAnalysis']['anRegress']:
            if 'allocated' in str(r.get('regResponder')):
                r['regRSquare']['estPoint'] = 0.5
                hit += 1
    assert hit == 1, '%s: %d allocated fit(s)' % (want, hit)
    return hit


def mangled_main(tmp):
    """A Main.hs whose roster the parser cannot find."""
    return write(os.path.join(tmp, 'Main.hs'),
                 open(MAIN).read().replace('roster', 'r0ster'))


def run_json(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        raise AssertionError('no %s to build a fixture from' % name)
    return p


def synth_json(tmp, pop='main', name=None, **kw):
    """One population as a file: `main`, or a class by name."""
    shapes = main_shapes() if pop == 'main' else class_shapes(pop)
    return synth_run(os.path.join(tmp, name or '%s.json' % pop), shapes, **kw)


def doctored(tmp, pop, mutate, name='x.json'):
    """A BUILT run with one mutation applied, and the mutation asserted.

    `pop` is a population rather than a captured `run14-*` filename, so
    these fixtures outlive the artifacts the procedure offers for deletion
    after every write-up. The assertion is unchanged and is the point: a
    mutation that matched nothing would otherwise hand the case a pristine
    run and let it pass having tested the opposite of what it names.
    """
    p = synth_json(tmp, pop, name)
    d = json.loads(open(p).read())
    n = mutate(d[2])
    assert n, 'the mutation matched no bench in the built %s run' % pop
    with open(p, 'w') as f:
        f.write(json.dumps(d))
    return p


def drop(benches, want):
    """Every bench of one name gone, as an interrupted run leaves it."""
    hit = [b for b in benches if b['reportName'] == want]
    assert len(hit) == 1, '%s: %d bench(es)' % (want, len(hit))
    for b in hit:
        benches.remove(b)
    return len(hit)


def scale(benches, want, factor):
    hit = 0
    for b in benches:
        if b['reportName'] == want:
            for r in b['reportAnalysis']['anRegress']:
                if 'iters' in r['regCoeffs']:
                    r['regCoeffs']['iters']['estPoint'] *= factor
            b['reportAnalysis']['anMean']['estPoint'] *= factor
            hit += 1
    assert hit == 1, '%s: %d bench(es)' % (want, hit)
    return hit


FAKE_HALF = """\
#!/bin/sh
# A stand-in for `$PREFIX-$half`, answering the one question a driver asks
# before it commits the machine: what benches are there. It runs none.
if [ "$1" = --list ]; then
  for s in shape-a shape-b shape-c; do
    for a in list build mut-odo sum-only-early sum-only-late; do
      echo "$s/$a"
    done
  done
fi
exit 0
"""

# The fuller stand-in, and the reason it is CHECKED IN. Every claim vetted
# by hand this week wanted a harness, and every one of those harnesses was
# thrown away with the session that built it -- so the next reader builds
# it again, which is what kept `smoke-sweep.sh` and `run-major.sh`
# unexercised for their whole lives. This one answers `--list`, `classes
# --list`, `check` and `diag`, and for a benchmark call hands back the
# benches a previous run really produced for the population asked for, one
# `benchmarking` line each as criterion writes them. Both drivers then run
# their whole sequence in seconds against real cells: eighteen processes
# for `run-major.sh`, and for `smoke-sweep.sh` every reader mode, both
# installers and its own refusal checks.
#
# `@HALF@` is filled in per half -- a token and not a `%` field, the shell
# below being full of `${a%-}` -- and `$D` is the shadow it runs in, so it
# reads the JSONs symlinked beside it.
FAKE_RUN = """\
#!/bin/sh
D=$(dirname "$0")
# Which population is being asked for, in either spelling the drivers use:
# `run-major.sh` passes a class PREFIX (`rev-`) and `smoke-sweep.sh` passes
# one of that class's SHAPES (`window-28x28-k5`). The leading token is the
# class in both.
CLS=""
for a in "$@"; do
  case "$a" in classes) CLS=pending ;;
    -*) ;;
    *) [ "$CLS" = pending ] && CLS=$(printf %s "$a" | cut -d- -f1) ;;
  esac
done
[ "$CLS" = pending ] && CLS=""
if [ -n "$CLS" ]; then SRC="$D/@RUN@-@HALF@-$CLS.json"
else SRC="$D/@RUN@-@HALF@-main.json"; fi
if [ "$1" = classes ] && [ "$2" = --list ]; then
  exec python3 -c "
import glob, json, os, sys
for f in sorted(glob.glob(os.path.join(sys.argv[1], '@RUN@-@HALF@-*.json'))):
    if f.endswith('-main.json'): continue
    for b in json.load(open(f))[2]: print(b['reportName'])" "$D"
fi
if [ "$1" = --list ]; then
  exec python3 -c "import json,sys
[print(b['reportName']) for b in json.load(open(sys.argv[1]))[2]]" "$SRC"
fi
[ "$1" = check ] && { echo "agree=True on every shape"; exit 0; }
[ "$1" = diag ] && { echo "diag: the regime, in the binary"; exit 0; }
OUT=""; SHAPE=""; want=0
for a in "$@"; do
  [ "$want" = 1 ] && { OUT="$a"; want=0; continue; }
  case "$a" in --json) want=1 ;; -*|classes) ;; *) SHAPE="$a" ;; esac
done
python3 - "$SRC" "$OUT" "$SHAPE" <<'ENDPY'
import json, sys
src, out, shape = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(src))
if shape.endswith('-'):        # a prefix over a class's shapes, not a shape
    pass
elif shape:
    d[2] = [b for b in d[2] if b['reportName'].startswith(shape + '/')]
for b in d[2]:
    print('benchmarking ' + b['reportName'])
if out:
    json.dump(d, open(out, 'w'))
ENDPY
echo "elapsed 0h00m01s; peak 1 MiB in use, 1 MiB max residency" >&2
exit 0
"""


UNDERPRINT = FAKE_RUN.replace(
    "for b in d[2]:\n    print('benchmarking ' + b['reportName'])",
    "for b in d[2][:-1]:\n    print('benchmarking ' + b['reportName'])")
assert 'd[2][:-1]' in UNDERPRINT, 'the under-printing stub lost its anchor'


def halves(*names):
    """A stand-in per half, named as a run's binaries are, and the run it
    reads.

    The stand-in used to answer out of the live `run14-*` JSONs, reached
    through the shadow's symlinks -- so four driver cases were tied to
    artifacts the procedure offers for deletion after every write-up, and
    failed by blaming the BINARY for a missing JSON when they went. The run
    is built now and shipped beside the stand-ins, so the fixture carries
    its own data and the cases answer for the drivers alone.
    """
    return [(n, FAKE_RUN.replace('@HALF@', n.split('-', 1)[1])
                        .replace('@RUN@', SRC))
            for n in names] + whole_run([n.split('-', 1)[1] for n in names])

ASM_HEAD_AFTER_RET = """\
\t.text
\t.globl\tgo
go:
\tmovq\t%rdi, %rax
\tret
.Lloop:
\taddq\t$1, %rax
\tcmpq\t$10, %rax
\tjne\t.Lloop
\tret
"""


def asm(tmp, text=ASM_HEAD_AFTER_RET):
    """A synthetic assembly, and a stand-in for the real assembler.

    `align-as.py` ends by execing REAL_AS, so a case that only wants to see
    what the shim emitted hands it one that does nothing.
    """
    a = write(os.path.join(tmp, 'a.s'), text)
    g = write(os.path.join(tmp, 'as'), '#!/bin/sh\nexit 0\n')
    os.chmod(g, 0o755)
    return {'asm': a, 'as': g, 'obj': os.path.join(tmp, 'a.o')}


_READER = None


def _reader():
    """The live read-run.py, imported once, for its own parsers.

    A synthetic run has two things it cannot invent: the roster's arm names
    and the shapes' dims. Both come from Main.hs, and they come through the
    READER'S parsers rather than a second copy here -- a second parser is a
    second thing to keep in step, which is the defect family this suite
    exists over. `main` is guarded there, so importing runs no CLI.
    """
    global _READER
    if _READER is None:
        spec = importlib.util.spec_from_file_location(
            'read_run', os.path.join(HERE, 'read-run.py'))
        _READER = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_READER)
    return _READER


def main_shapes(n=None):
    """A few main-set shapes, from Main.hs rather than written out here.

    The main set is `convShapes` and `stretchShapes`; every other list is a
    stride class. Naming the LISTS rather than the shapes is what keeps
    this from rotting -- a shape can be renamed or dropped between runs,
    and a list going empty is loud where a stale shape name is a KeyError
    in a fixture nobody was reading.
    """
    dims, _ = _reader().dims_by_shape(os.path.join(HERE, 'Main.hs'))
    # Both lists represented whatever `n` is, rather than the first `n` of
    # a sort: the main set is conv AND stretch shapes, the two have
    # different (l, sInner) rules, and a fixture of one kind reads as the
    # main set to every mode while being half of it.
    conv = sorted(sh for sh, d in dims.items() if d['lst'] == 'convShapes')
    stretch = sorted(sh for sh, d in dims.items()
                     if d['lst'] == 'stretchShapes')
    ms = [sh for pair in zip(conv, stretch) for sh in pair]
    ms += [sh for sh in conv + stretch if sh not in ms]
    # ALL of it by default, because `--claims --in-place` refuses a main
    # set that is not the whole one -- the claims are registered over the
    # population, and a fixture short of it makes install-tables.sh refuse
    # for a reason the case is not about. `n` is for the cases that only
    # need a couple of shapes and would rather build less.
    assert len(ms) >= (n or 1), 'the main set parsed as %d shape(s)' % len(ms)
    return ms[:n] if n else ms


def _sunk_slice(t):
    """The `slice` class with one cell sunk -- five cases' shared fixture.

    Written once because it was written five times, as three lines of
    `doctored(... 'run14-lookrts-slice.json' ...)` apiece: five copies of
    one incantation, and five cases tied to an artifact the procedure
    offers for deletion after every write-up. The cell is named rather
    than defaulted because two of the five assert the shape by name.
    """
    return {'run': sunk_json(t, class_shapes('slice'), 'mut-odo-vecdims',
                             shape='slice-primes')}


def sunk_json(tmp, shapes, arm, shape=None, name='sunk.json'):
    """A run carrying a cell the forcing term did not leave positive.

    NO RUN ON DISK HAS ONE, which is exactly why the sites that divided
    without checking went unseen for so long, and why this cannot be a
    captured fixture: it has to be built, because what makes it is the
    slopes. The cell sunk is the first shape's, the arm being the caller's.
    """
    return synth_run(os.path.join(tmp, name), shapes,
                     sunk=[(shape or shapes[0], arm)])


def sunk_shape_json(tmp, name='sunk-shape.json'):
    """A run with EVERY arm of one shape sunk, the baseline among them.

    Sinking the two `Term` halves alongside `list` leaves the baseline's
    own net at EXACTLY zero, which is a different state from one sunk cell
    and the one a divide-before-the-guard needs: `<= 0` had always
    included 0, and only the order of the two lines kept it unreachable.
    Not doctorable out of a captured run either -- the cells have to move
    together, which is what building them affords.
    """
    shapes = main_shapes()
    roster = _reader().roster_of(open(os.path.join(HERE, 'Main.hs')).read())
    arms = [n for n, role, fn in roster if role != 'Only']
    return synth_run(os.path.join(tmp, name), shapes,
                     sunk=[(shapes[0], a) for a in arms])


def class_names():
    """The stride classes, from Main.hs rather than from a literal.

    A class is a shape list that is not the main set, and its name is the
    shape prefix before the first hyphen -- the same derivation
    run-major.sh makes, and the one whose hyphen assumption it now refuses
    to let a class name break.
    """
    dims, _ = _reader().dims_by_shape(os.path.join(HERE, 'Main.hs'))
    return sorted({sh.split('-')[0] for sh, d in dims.items()
                   if d['lst'] not in ('convShapes', 'stretchShapes')})


_WHOLE = {}


SRC = 'srcrun'      # the stand-ins' data, named OUTSIDE any run's own glob


def whole_run(halves_of, samples=2, prefix=SRC, short_class=None):
    """Every population of a paired run, as `extra` entries for a shadow.

    Named `srcrun-<half>-<pop>` and NOT after the case's run: `$R-*.json`
    is exactly what run-major.sh's relaunch guard refuses to start on top
    of, so a fixture carrying the run's own prefix reads as a previous
    attempt and the control case never runs at all.

    Nine files a half -- the main set and each class -- because that is
    what a driver enumerates rather than assumes: `classes --list` globs
    the class files for its roster, and every expected bench count is read
    back from a listing. A `.log` rides with each, carrying the provenance
    line install-tables.sh parses for its Provenance paragraph.

    Two samples a bench, the drivers reading counts and names and never a
    figure. Memoised per tag, building it being the only slow thing here.
    """
    key = (tuple(halves_of), samples, prefix, short_class)
    if key not in _WHOLE:
        out = []
        for half in halves_of:
            pops = [('main', main_shapes())]
            # `short_class` leaves one class two shapes wide, which is a
            # state the reader is right to emit no per-shape line for and
            # the installers have to refuse BEFORE writing. Every class has
            # been three shapes since 2026-08-14, so nothing on disk
            # carries it and it has to be built.
            pops += [(c, class_shapes(c)[:2 if c == short_class else None])
                     for c in class_names()]
            for pop, shapes in pops:
                out.append(('%s-%s-%s.json' % (prefix, half, pop),
                            synth_text(shapes, samples=samples)))
                out.append(('%s-%s-%s.log' % (prefix, half, pop),
                            'benchmarking %s/x\nProvenance: elapsed 1m2s;'
                            ' peak 300 MiB in use, 100 MiB max residency\n'
                            % shapes[0]))
        _WHOLE[key] = out
    return _WHOLE[key]


def class_shapes(cls):
    """One stride class's shapes, from Main.hs rather than from a literal.

    The prefixes are disjoint by construction -- `rev-` does not match
    `revsome-`, the hyphen doing it -- which is the property run-major.sh
    selects on and the one run-major.sh now refuses to let a class name
    break.
    """
    dims, _ = _reader().dims_by_shape(os.path.join(HERE, 'Main.hs'))
    return sorted(sh for sh in dims if sh.startswith(cls + '-'))


def _est(point, rel=0.01):
    d = abs(point) * rel
    return {'estPoint': point,
            'estError': {'confIntCL': 0.95, 'confIntLDX': -d, 'confIntUDX': d}}


def _regress(responder, slope):
    return {'regResponder': responder, 'regRSquare': _est(0.9995, 0.0005),
            'regCoeffs': {'iters': _est(slope), 'y': _est(0.0, 0.0)}}


def _synth_report(name, slope, alloc, samples):
    # `reportMeasured` is a list of LISTS, [0] the time and [3] the iteration
    # count. That array shape is the one thing about this format a generator
    # can get wrong in silence: the reader's step scan is the only consumer,
    # so a dict here would surface as `samples that are not Measured arrays`
    # from --steps and --block alone, long after every other mode passed.
    meas = [[slope * 8 * k, slope * 8 * k, 0, 8 * k, alloc * 8 * k,
             0, 0, 0, 0, 0, 0, 0] for k in range(1, samples + 1)]
    return {'reportName': name, 'reportNumber': 0, 'reportKeys': [],
            'reportKDEs': [], 'reportOutliers': {}, 'reportMeasured': meas,
            'reportAnalysis': {
                'anRegress': [_regress('time', slope),
                              _regress('allocated', alloc)],
                'anMean': _est(slope), 'anStdDev': _est(slope * 0.01),
                'anOutlierVar': {'ovDesc': 'moderate', 'ovEffect': 'Moderate',
                                 'ovFraction': 0.1}}}


def _spread(fn, lo, hi):
    """A per-function factor, stable ACROSS PROCESSES.

    `hash()` is salted per process, so a fixture built with it would differ
    between two runs of the same case -- and a case whose fixture moves
    under it proves whatever that run happened to draw.
    """
    return lo + (hi - lo) * (zlib.crc32((fn or '').encode()) / 2 ** 32)


TERM = 4e-10        # the forcing term per element: one pass, so it scales


def synth_run(path, shapes, samples=8, no_twins=False, sunk=()):
    """A criterion run over `shapes`, built rather than captured.

    Kilobytes where a real run's JSON is megabytes, and DERIVED: the arms
    are Main.hs's roster through `roster_of` and the sizes are its dims
    through `dims_by_shape`, so a roster change moves this with it. That is
    what the opening asks of every fixture here, and what a captured run
    could not give -- the suite's fixtures used to be the live `run14-*`
    JSONs, which tied 34 cases to artifacts the procedure offers for
    deletion after every write-up.

    The model is the correction's own, so the reader's gates have
    something true to find: the two `Term` halves are the forcing term and
    are identical; a timed arm is that term plus per-function work, so its
    net is positive; a `Twin` shares its base arm's function and so reads
    A/A at exactly 1; a `Force` arm is the work without the term, so the
    in-situ reading recovers it. The term is a constant per element, which
    is what `--selftest` checks when it asks that it scale with `l`.

    `sunk` names (shape, arm) cells to drive NON-positive, which no real
    run on disk carries -- the state the fingerprint, `--block` and
    `machine_check` refuse, and which had to be constructed to test at all.
    """
    m = _reader()
    main_hs = os.path.join(HERE, 'Main.hs')
    dims, _ = m.dims_by_shape(main_hs)
    roster = m.roster_of(open(main_hs).read())
    timed = [(n, role, fn) for n, role, fn in roster if role != 'Only']
    if no_twins:
        # EVERY A/A pair gone, which is more than the Twin role: the two
        # `Term` halves are an A/A pair of the forcing term itself, and the
        # captured fixture this replaces dropped `sum-only-late` by name for
        # exactly that reason -- a literal that said nothing about why. One
        # half is kept, the correction having nothing to subtract without
        # it.
        # What goes is each twin's BASE, not the twin: an A/A pair needs
        # both, so the pair cannot form, while the twin and the in-situ
        # `-nosum` rows stay -- which is the state the defect needs, an
        # in-situ row being what got read as the A/A. Dropping the twins
        # instead leaves nothing for the old code to misread and the case
        # passes against the very revision it exists to fail, which is what
        # --audit caught when this fixture was first built that way. A
        # `Force` arm shares its base's function too and is kept for the
        # same reason. One `Term` half goes with them, the two halves being
        # an A/A pair of the forcing term.
        bases = {fn for _, role, fn in timed if role == 'Twin'}
        kept, first_term = [], True
        for n, role, fn in timed:
            if role not in ('Twin', 'Force') and fn in bases:
                continue
            if role == 'Term':
                if not first_term:
                    continue
                first_term = False
            kept.append((n, role, fn))
        timed = kept
    reports = []
    for sh in shapes:
        l = dims[sh]['l']
        for name, role, fn in timed:
            work = 0.0 if role == 'Term' else _spread(fn, 0.6, 6.0) * TERM * l
            if role == 'Term':
                slope = TERM * l
            elif role == 'Force':
                slope = work
            else:
                slope = TERM * l + work
            # A per-cell wobble under half a percent, so that a ratio, an
            # A/A worst cell and a spread are WELL DEFINED. Without it every
            # twin equalled its base exactly, every A/A pair read 0.00%, and
            # which shape came out `worst` was a tie broken by iteration
            # order -- so a case about attributing the worst cell to the
            # right shape passed or failed on nothing at all. `Term` stays
            # exact: its two halves are one measurement made twice, and
            # --selftest reads their spread as the term's own.
            if role != 'Term':
                slope *= 1.0 + _spread(name + '@' + sh, -0.004, 0.004)
            if (sh, name) in sunk:
                slope = TERM * l * 0.5      # below the term: net goes negative
            alloc = 0.0 if role == 'Term' else 8.0 * l * _spread(fn, 0.9, 1.4)
            reports.append(_synth_report('%s/%s' % (sh, name), slope, alloc,
                                         samples))
    with open(path, 'w') as f:
        f.write(json.dumps(['criterion', '1.6.5.0', reports]))
    return path


def synth_text(shapes, **kw):
    """The same run as TEXT, for a fixture that must reach a shadow.

    `shadow_dir` symlinks this directory before a case's plant runs, so a
    file written here afterwards is not in the shadow and a stand-in
    reading its own directory cannot see it. An `extra` entry is written
    INTO the shadow, and takes a string -- so a fixture a driver has to
    find is built as text and handed over that way, never through disk
    here. It also means nothing is created in this directory at all, which
    the run's own tree check would otherwise have to be trusted to forgive.
    """
    tmp = tempfile.mkdtemp(prefix='zz-synth-')
    try:
        p = synth_run(os.path.join(tmp, 'r.json'), shapes, **kw)
        return open(p).read()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def synthetic_run(tmp, killed=False, no_twins=False, no_starts=False,
                  complained=False, note_block=False, riders=False,
                  into=None):
    """A whole run in this directory: JSONs, and the log that describes it.

    `read-all.sh` cds to its own directory and globs, so this is one of the
    two fixtures that cannot live in a temp directory.

    `into` names that directory when the case runs a SHADOW. `shadow_dir`
    symlinks this one BEFORE a plant runs, so a file written here
    afterwards is not in the shadow, and a driver globbing its own
    directory finds nothing at all -- which reads as a fixture that would
    not build rather than as the state the case wanted. Pointed at the
    shadow, the run lands where the driver will look.
    """
    place = (here_file if into is None
             else lambda name: os.path.join(into, name))
    tag = 'runzz'
    log = ['=== 2026-01-01T00:00:00+01:00 major run begins; tree at 0000000,'
           ' Main.hs at 0000000; roster is 1 benches',
           '=== 2026-01-01T00:00:00+01:00 halves: a1g lookrts, in that order;'
           ' lookrts is the basis, and every class runs on both halves']
    for cls in ('rev', 'slice'):
        # Built rather than copied from `run14-lookrts-<cls>.json`, which
        # tied this fixture to artifacts the procedure offers for deletion
        # after every write-up. `no_twins` was ten arm names written out
        # here, with no assertion on what they matched, so an A/A pair
        # added or renamed left twins in the file and failed
        # `aa-worst-cell-is-not-an-insitu-row` for a reason that has
        # nothing to do with the defect it guards; it is the roster's own
        # Twin role now, and moves with the roster.
        dst = place('%s-lookrts-%s.json' % (tag, cls))
        synth_run(dst, class_shapes(cls), no_twins=no_twins)
        if not no_starts:
            log += ['=== 2026-01-01T00:00:01+01:00 start %s-lookrts-%s'
                    % (tag, cls),
                    '=== 2026-01-01T00:10:00+01:00 done  %s-lookrts-%s rc=0'
                    ' benchmarking=47' % (tag, cls)]
    if complained:
        # run-major.sh's own complaint about a process that nonetheless
        # exited 0 and left a JSON: it moves none of STARTED, FINE or
        # LANDED, so every test read-all.sh runs reads this run as whole.
        log.append('=== 2026-01-01T00:10:00+01:00   !! %s-lookrts-rev:'
                   ' expected 141 benches, got 94 -- the selection is not'
                   ' what was asked for' % tag)
    if killed:
        log.append('=== 2026-01-01T00:10:01+01:00 start %s-lookrts-window'
                   % tag)
    if riders:
        # The alone-leg riders a paired run leaves: one bench per process on
        # a half's own binary, named `$R-al-<half>-<shape>-r1.json`. They are
        # not populations -- no A/A pair, no sum-only, one shape -- so gating
        # them as such buries the eighteen this driver exists to count.
        synth_run(place('%s-al-lookrts-cnn-slice-c32-r1.json' % tag),
                  class_shapes('rev')[:1])
    if note_block:
        # run-major.sh copies the pair note's gate lines into the log,
        # indented and with no `===` stamp of its own. run-gate.sh writes
        # `!!` into that note whenever the machine check fires, so a run
        # whose gate tripped it carries a `!!` that NO PROCESS emitted --
        # and one that survives every later reading of the log.
        log += ['=== 2026-01-01T00:00:00+01:00 %s-pair.txt says, about the'
                ' gate:' % tag,
                '      GATE: run 2026-01-01. Mechanically FAILED,'
                ' 1 complaint(s):',
                '        !! the machine check FAILED -- read it before the'
                ' evening',
                '      That is exit codes and counts; the reading is still'
                ' to do.']
    write(place('%s-wallclock.log' % tag), '\n'.join(log) + '\n')
    return {'tag': tag}


def staged_doc(tmp):
    """A document STAGED in a throwaway index, the real one untouched.

    `added_lines` promises what the working tree adds over HEAD, and the
    defect was that it asked `git diff` -- index against worktree -- so a
    staged document came back empty. Reproducing that wants something
    staged and nothing of the author's disturbed, which is what
    GIT_INDEX_FILE buys: a new file, added to an index this case creates
    and deletes, with the repository's own index never opened for writing.
    """
    doc = here_file('zz-case-doc.md')
    write(doc, open(README).read()
          + '\nThe fastest arm of every population is the one this planted'
            ' sentence pretends to name, which makes it the biggest'
            ' superlative in the README.\n')
    idx = os.path.join(tmp, 'index')
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    for cmd in (('git', 'read-tree', 'HEAD'),
                ('git', 'add', os.path.basename(doc))):
        r = subprocess.run(cmd, cwd=HERE, env=env, capture_output=True,
                           text=True)
        assert r.returncode == 0, '%s: %s' % (cmd, r.stderr.strip())
    return {'doc': os.path.basename(doc), 'index': idx}


# ------------------------------------------------------------------- cases

CASE = collections.namedtuple('CASE', 'name prog fix gist plant argv env '
                                      'ok bug probe shadow')


def case(name, prog, fix, gist, argv, ok, bug=None, plant=None, env=None,
         probe=None, shadow=None):
    """One defect, both ways round.

    `probe` is for a defect whose evidence is a FILE the invocation wrote
    rather than anything it said: it returns text that is judged alongside
    the output, which is how a paragraph silently overwritten in a copy of
    the README becomes a `has`/`hasnt` like any other.

    A `bug` verdict says what the defect looked like, and --audit replays
    the case against `fix^` to see it. Without a `fix` there is nothing to
    replay against, and the runner computed `None + '^'` -- a TypeError out
    of the middle of the audit, naming no case, where the case had simply
    been written before its fix was committed. Refused at import instead,
    which is where the author is standing.
    """
    assert bug is None or fix, (
        '%s: a bug verdict wants the commit that fixed it, or --audit has'
        ' nothing to replay -- drop the bug to make it a control' % name)
    return CASE(name, prog, fix, gist, plant, argv, env or {}, ok, bug,
                probe, shadow)


def V(exit=None, has=(), hasnt=()):
    """A verdict: the exit code, what must be said, what must not."""
    return {'exit': exit, 'has': list(has), 'hasnt': list(hasnt)}


CASES = [
    # ---- read-run.py, the first review's ------------------------------
    case('install-lands-in-next-block', 'read-run.py', '045ca63',
         'a class whose own table is absent took the next class\'s',
         plant=lambda t: {'readme': readme_without_class_table(t),
                          'run': synth_json(t, 'slice')},
         argv=['{run}', '--block', '--in-place', '--readme', '{readme}'],
         ok=V(exit=1, has=['refusing to write there'],
              hasnt=['installed at']),
         bug=V(exit=0, has=['installed at'])),

    case('block-brief-cannot-install', 'read-run.py', '045ca63',
         '--brief dropped the table --in-place had to install',
         plant=lambda t: {'readme': edited_readme(t),
                          'run': synth_json(t, 'slice')},
         argv=['{run}', '--block', '--in-place', '--brief',
               '--readme', '{readme}'],
         ok=V(exit=0, has=['installed at']),
         bug=V(exit=1, has=['emitted no table'])),

    case('buried-action-at-eof', 'read-run.py', '045ca63',
         'the last indented block of a document was never swept',
         plant=lambda t: {'readme': readme_with_trailing_buried_action(t)},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(has=['--survey to see it']),
         bug=V(hasnt=['--survey to see it'])),

    case('worst-beside-a-sunk-time', 'read-run.py', '045ca63',
         'a plausible `worst` published beside `time --`',
         plant=_sunk_slice,
         argv=['{run}'],
         # The verdict is the two columns and not the figure that used to
         # stand in the second: `--  0.063` was this arm's real published
         # number, so the case could only ever run on the captured JSON it
         # came from. What it is really about is a `worst` printed beside a
         # `time` that reads `--`, which is what these two spellings say.
         ok=V(has=['mut-odo-vecdims                   --      --']),
         bug=V(has=['mut-odo-vecdims                   --  '],
               hasnt=['mut-odo-vecdims                   --      --'])),

    case('withheld-line-names-a-flag-that-is-not-one', 'read-run.py',
         'eeb5d24',
         'the withheld count sent a run to `--quiet`, which withholds too',
         # --check-doc --quiet ends by saying how many lines it kept back
         # and how to get them. It said "rerun without --quiet", and plain
         # --check-doc withholds as well -- `--worklists` is what promotes
         # them -- so following the message returns the same line. Met on
         # Run 17 at post-run step 7, the one step whose whole content is
         # reading those lists, and read there as the tool being broken.
         # The check is the message, not the flag: the flag worked all
         # along.
         plant=lambda t: {'readme': edited_readme(t)},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(has=['rerun with --worklists']),
         bug=V(has=['without --quiet'], hasnt=['rerun with --worklists'])),

    case('deflation-with-no-legs-answers-anyway', 'read-run.py', 'eeb5d24',
         'a deflation printed over no alone legs at all',
         # --deflation divides each shape's roster cell by that shape's
         # alone leg. A run whose riders were never taken -- or a name the
         # legs do not belong to -- has none, and the shape this guards is
         # the one an empty aggregate always has here: a header, a geomean
         # over nothing, and exit 0, which reads as an answer. It refuses
         # instead and says which of the two it is. A class run reaches the
         # same door by another route, its legs being the main set's.
         plant=lambda t: {'run': synth_json(t, 'main',
                                            name='run99-half-main.json')},
         argv=['{run}', '--deflation'],
         ok=V(exit=2, has=['the riders were not taken']),
         bug=V(exit=2, hasnt=['the riders were not taken'])),

    case('claims-arm-counted-per-registration', 'read-run.py', '045ca63',
         'one filtered arm reported as eight',
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--claims', '--exclude', 'bq-expand'],
         ok=V(has=['1 arm(s) of the claims list']),
         bug=V(has=['8 arm(s) of the claims list'])),

    case('added-lines-over-head', 'read-run.py', None,
         'a STAGED document emptied the freshness sweeps',
         # No --audit: this case now passes a flag that postdates the
         # default it guards, so code from before cannot take it. Removal
         # is the handling; it goes on guarding forward.
         plant=staged_doc,
         env={'GIT_INDEX_FILE': '{index}'},
         argv=['--check-doc', '--worklists', '--readme', '{doc}'],
         ok=V(has=['NEW '])),

    case('population-main-hs-does-not-define', 'read-run.py', '4086ab8',
         'a population Main.hs no longer defines died unpacking',
         plant=lambda t: {'run': synth_json(t, 'slice')},
         argv=['{run}', '--markdown', '--main', '/dev/null'],
         ok=V(exit=1, has=['a population Main.hs does not define']),
         bug=V(has=['not enough values to unpack'])),

    case('ragged-gate-after-exclude', 'read-run.py', '4086ab8',
         'excluding the arm with the missing cells still refused the run',
         plant=lambda t: {'run': doctored(
             t, 'slice',
             lambda bs: drop(bs, 'slice-primes/bq-expand'))},
         argv=['{run}', '--exclude', 'bq-expand'],
         ok=V(exit=0, has=['slice class'], hasnt=['did not happen']),
         bug=V(exit=2, has=['0 cell(s) missing'])),

    case('in-place-alone', 'read-run.py', '4086ab8',
         '--in-place with no installing mode printed a table and wrote none',
         plant=lambda t: {'readme': edited_readme(t),
                          'run': synth_json(t, 'main')},
         argv=['{run}', '--in-place', '--readme', '{readme}'],
         ok=V(exit=2, has=['--in-place is a modifier']),
         bug=V(exit=0)),

    # ---- a comparison narrowed in silence, which wants two runs --------
    case('chapter-names-the-shapes-it-dropped', 'read-run.py', 'a78555e',
         'a control half short of a shape read as a full comparison',
         # Two BUILT runs, the second a shape shorter -- which is what a
         # half killed at a shape boundary leaves, and what `load_other`'s
         # hole gate does not catch, that one asking after a shape PARTLY
         # there. `--compare` has always named its residue; these two
         # computed the same intersection and said nothing, under the mode
         # whose geomeans are the chapter's headline figures.
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json'),
                          'other': synth_run(os.path.join(t, 'b.json'),
                                             main_shapes()[:-1])},
         argv=['{run}', '--compare', '{other}', '--chapter'],
         ok=V(has=['shapes in one run only, skipped']),
         bug=V(hasnt=['shapes in one run only, skipped'])),

    case('alloc-names-the-shapes-it-dropped', 'read-run.py', 'a78555e',
         'the allocation comparison named its arms and not its shapes',
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json'),
                          'other': synth_run(os.path.join(t, 'b.json'),
                                             main_shapes()[:-1])},
         argv=['{run}', '--compare', '{other}', '--alloc'],
         ok=V(has=['shapes in one run only, skipped']),
         bug=V(hasnt=['shapes in one run only, skipped'])),

    # ---- the sunk cell, which only a built fixture can carry -----------
    case('selftest-survives-a-sunk-baseline', 'read-run.py', '50efffe',
         'a baseline net of exactly 0 divided before the guard could look',
         plant=lambda t: {'run': sunk_shape_json(t)},
         argv=['{run}', '--selftest'],
         ok=V(exit=1, has=['no geomean to bracket'],
              hasnt=['ZeroDivisionError', 'Traceback']),
         bug=V(has=['ZeroDivisionError'])),

    case('fingerprint-refuses-a-sunk-cell', 'read-run.py', 'e2d6604',
         'a sunk cell was divided and INSTALLED, outliving its own run',
         plant=lambda t: {'run': sunk_json(t, main_shapes(),
                                           'mut-odo-vecdims')},
         argv=['{run}', '--fingerprint'],
         ok=V(has=['| -- |']),
         bug=V(hasnt=['| -- |'])),

    case('block-per-shape-refuses-a-sunk-cell', 'read-run.py', 'e2d6604',
         "a sunk cell was divided into the block's installed per-shape line",
         plant=lambda t: {'run': sunk_json(t, class_shapes('scaled'),
                                           'mut-odo-vecdims')},
         argv=['{run}', '--block', '--brief'],
         ok=V(has=['--/']),
         bug=V(hasnt=['--/'])),

    case('machine-check-drops-a-sunk-baseline', 'read-run.py', 'e2d6604',
         'a non-positive `list` net raised, and run-gate.sh files stderr'
         ' verbatim into the pair note',
         plant=lambda t: {'run': sunk_json(t, main_shapes(), 'list')},
         argv=['{run}', '--machine'],
         ok=V(exit=1, has=['net not positive'], hasnt=['Traceback']),
         bug=V(has=['Traceback'])),

    # ---- read-run.py, the second review's ------------------------------
    case('checkdoc-without-a-roster', 'read-run.py', 'a6c32e8',
         'a roster it could not parse skipped five checks at exit 0',
         plant=lambda t, rev: {'main': mangled_main(t),
                               'readme': era_readme(t, rev)},
         argv=['--check-doc', '--main', '{main}', '--readme', '{readme}'],
         ok=V(exit=1, has=['BLOCKED: no roster parsed']),
         bug=V(exit=0)),

    case('checkdoc-open-list-out-of-order', 'read-run.py', 'a6c32e8',
         'the goal section above the open list killed the sweep in silence',
         plant=lambda t, rev: {'readme': readme_goal_above_open(t, rev)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['BLOCKED: the open list']),
         bug=V(exit=0)),

    case('checkdoc-qmark-under-renamed-yardstick', 'read-run.py', 'a6c32e8',
         'a renamed yardstick header disabled the published-`?` gate',
         plant=lambda t: {'readme': readme_yardstick_renamed_with_qmark(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(has=['still carry the `?`']),
         bug=V(hasnt=['still carry the `?`'])),

    case('claims-current-run-not-exempt', 'read-run.py', 'a6c32e8',
         '`Run N` exempted the run in hand, the one kind that matters',
         # THE ONE CASE STILL ON A CAPTURED RUN, and it is stated rather
         # than left to be noticed. Its verdict is a published reading,
         # 0.9312, and the defect is that the sentence exempted the run in
         # hand from being read at all -- so what separates the two
         # revisions is whether that figure appears. Over a built run they
         # print byte-identical output, measured 2026-08-17, so the case
         # would pass while testing nothing. If run14's artifacts go, this
         # reports FIXTURE DID NOT BUILD, which is the honest failure and
         # not a false pass; re-aim it at whatever run is then on disk.
         plant=lambda t: {'readme': readme_current_run_sentence(t),
                          'run': run_json('run14-lookrts-main.json')},
         argv=['{run}', '--claims', '--readme', '{readme}'],
         ok=V(has=['0.9312']),
         bug=V(hasnt=['0.9312'])),

    case('results-names-an-older-basis-half', 'read-run.py', None,
         "the Results lead named the PREVIOUS run's half under this run's"
         ' tables',
         # A control and not a defect replay: the check was written the day
         # this case was, so there is no `fix^` to replay it against. What
         # it holds is the property, which is what the next reader needs --
         # the fixture is the Run 14 defect built out of the current README.
         plant=lambda t: {'readme': readme_stale_basis_in_results(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['while this chapter is Run'])),

    case('path-token-dotfile', 'read-run.py', None,
         "lstrip('./') ate the leading dot of a cited dotfile",
         plant=lambda t: {'readme': readme_citing_dotfile(t)},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         # No --audit: this case now passes a flag that postdates the
         # default it guards, so code from before cannot take it. Removal
         # is the handling; it goes on guarding forward.
         ok=V(has=['ok:'], hasnt=['do not resolve: .hlint.yaml'])),

    case('insitu-worst-cell-label', 'read-run.py', 'a6c32e8',
         'a dropped shape renamed every later ratio',
         plant=lambda t: {'run': doctored(
             t, 'slice',
             lambda bs: scale(
                 bs, 'slice-cnn-L2-24x24-c32/mut-odo-vecdims-nosum', 3.0))},
         argv=['{run}', '--aa', '--brief'],
         # The coverage line and not the label's figure: `worst cell 1.63%
         # on slice-coprime-r7` was a captured run's own arithmetic, so the
         # verdict only held while the fixture was that run. The defect is
         # that a dropped shape went unaccounted for -- the pre-fix reader
         # prints no coverage line at all here and attributes the worst
         # cell to the dropped shape's neighbour -- and the shape named
         # below is the one this case itself drops, so it is fixed by
         # construction rather than by whatever the data happened to say.
         ok=V(has=['over 2 of 3 shape(s): slice-cnn-L2-24x24-c32 dropped']),
         bug=V(hasnt=['over 2 of 3 shape(s)'])),

    case('pair-refuses-a-sunk-cell', 'read-run.py', 'a6c32e8',
         'a sunk cell gave --pair a math domain error',
         plant=_sunk_slice,
         argv=['{run}', '--pair', 'mut-odo-vecdims', 'list'],
         ok=V(exit=2, has=['not readable']),
         bug=V(has=['math domain error'])),

    case('compare-refuses-a-partial-other', 'read-run.py', 'a6c32e8',
         'an interrupted other half raised KeyError',
         plant=lambda t: {'run': synth_json(t, 'main'),
                          'other': doctored(
                              t, 'main',
                              lambda bs: drop(bs,
                                              main_shapes()[1] + '/bq-expand'),
                              'other.json')},
         argv=['{run}', '--compare', '{other}'],
         ok=V(exit=2, has=['cell(s) missing, so the comparison did not']),
         bug=V(has=['KeyError'])),

    case('summary-row-width', 'read-run.py', 'a6c32e8',
         'a row that lost a column had its tail compared against nothing',
         plant=lambda t: {'readme': readme_summary_row_short(t),
                          'run': synth_json(t, 'slice')},
         argv=['{run}', '--block', '--readme', '{readme}'],
         ok=V(has=['not checked: it has 5 column(s)']),
         bug=V(hasnt=['not checked: it has 5 column(s)'])),

    case('verbose-alone', 'read-run.py', None,
         '--verbose outside the modes that drop prose said nothing',
         # No --audit: this case now passes a flag that postdates the
         # default it guards, so code from before cannot take it. Removal
         # is the handling; it goes on guarding forward.
         # Was `--brief`, which is now the DEFAULT and kept only as a
         # compatibility pin; the guard it tested moved to --verbose with it.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--markdown', '--verbose'],
         ok=V(exit=2, has=['--verbose restores'])),

    case('two-modes-at-once', 'read-run.py', 'a6c32e8',
         'the if/elif dispatch dropped the second mode without a word',
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--markdown', '--fingerprint'],
         ok=V(exit=2, has=['one mode at a time']),
         bug=V(exit=0)),

    # A CONTROL and not a replay, which is a property of the repair rather
    # than a gap in it: `--len 0` said `any length` for a report `scan`
    # caps at one cache line, and what made that checkable without a
    # binary was extracting `span_label` -- which did not exist before the
    # fix, so replaying 281ad73^ raises NameError instead of printing the
    # old wording. It can still fail, which is what a control is for: say
    # `any length` again and it goes red.
    case('len-zero-lifts-the-size-filter-not-the-cap', 'loop-offsets.py',
         None,
         'CONTROL: the header names the cap, not the lifted size filter',
         argv=['--unit', 'span_label(None)'],
         ok=V(has=["'at most 64 B'"], hasnt=['any length'])),

    case('fmt-abs-above-its-top-unit', 'read-run.py', '0fe535b',
         'a time past a thousand seconds wrote an exponent nothing parses',
         argv=['--unit', 'fmt_abs(1500.0)'],
         ok=V(has=["'1500 s'"]),
         bug=V(has=['e+03'])),

    case('fmt-abs-at-the-unit-boundary', 'read-run.py', 'a6c32e8',
         '999.7 us printed as `1e+03 us`, which --machine cannot parse',
         argv=['--unit', 'fmt_abs(9.997e-4)'],
         ok=V(has=["'1 ms'"]),
         bug=V(has=['e+03'])),

    case('added-lines-untracked', 'read-run.py', None,
         'an untracked README had every hit called old',
         # No --audit: this case now passes a flag that postdates the
         # default it guards, so code from before cannot take it. Removal
         # is the handling; it goes on guarding forward.
         plant=untracked_doc,
         argv=['--check-doc', '--worklists', '--readme', '{doc}'],
         # untracked means `added is EVERYTHING`, so the headline prints
         # bare -- neither wording. The positive is that the sweep ran
         # and reported at all, which a no-op would not.
         ok=V(has=['superseded figure(s) quoted'],
              hasnt=['none added by this diff'])),

    case('alloc-fit-on-an-unknown-shape', 'read-run.py', 'a6c32e8',
         'a missing alloc read as "allocated nothing", silencing the warning',
         plant=lambda t: {'run': doctored(
             t, 'slice',
             lambda bs: bad_alloc_fit(bs, 'slice-primes/offtab'))},
         argv=['{run}', '--main', '/dev/null'],
         ok=V(has=['allocated R2 < 0.99']),
         bug=V(hasnt=['allocated R2 < 0.99'])),

    case('checkdoc-chapter-heading-gone', 'read-run.py', 'a6c32e8',
         'the chapter-link sweep lost its own boundary in silence',
         plant=lambda t: {'readme': readme_chapter_renamed(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(has=['BLOCKED: no `## About the last run` heading']),
         bug=V(hasnt=['BLOCKED: no `## About the last run` heading'])),

    case('markdown-installs-into-the-main-table', 'read-run.py', 'febc2bd',
         "a class run whose shapes Main.hs lost installed into Results",
         plant=lambda t: {'readme': edited_readme(t),
                          'run': synth_json(t, 'rev')},
         argv=['{run}', '--markdown', '--in-place', '--main', '/dev/null',
               '--readme', '{readme}'],
         ok=V(exit=1, has=['a population Main.hs does not define'],
              hasnt=['installed at']),
         bug=V(exit=0, has=['installed at'])),

    case('selftest-survives-a-sunk-cell', 'read-run.py', 'febc2bd',
         'a sunk cell gave the gate a traceback and no verdict at all',
         plant=_sunk_slice,
         argv=['{run}', '--selftest'],
         ok=V(hasnt=['math domain error'], has=['FAIL']),
         bug=V(has=['math domain error'])),

    case('aa-survives-a-sunk-cell', 'read-run.py', 'febc2bd',
         '--aa died where --claims refuses, on the same file',
         plant=_sunk_slice,
         argv=['{run}', '--aa', '--brief'],
         ok=V(has=['calibration:'], hasnt=['math domain error']),
         bug=V(has=['math domain error'])),

    case('aa-lists-controls-under-no-controls', 'read-run.py', 'febc2bd',
         '--no-controls made --aa report a file of controls as having none',
         plant=lambda t: {'run': synth_json(t, 'slice')},
         argv=['{run}', '--aa', '--brief', '--no-controls'],
         ok=V(exit=2, has=['--no-controls drops the controls'],
              hasnt=['no control pairs in this run']),
         bug=V(has=['no control pairs in this run'])),

    case('blocked-message-names-the-file', 'read-run.py', 'febc2bd',
         'the roster BLOCKED line printed Main.hs\'s CONTENTS as its name',
         plant=lambda t: {'main': mangled_main(t)},
         argv=['--check-doc', '--main', '{main}'],
         ok=V(has=['no roster parsed out of Main.hs']),
         bug=V(hasnt=['no roster parsed out of Main.hs'])),

    case('pair-refusal-names-shape-first', 'read-run.py', 'febc2bd',
         'the refusal printed arm/shape where every other line is shape/arm',
         plant=_sunk_slice,
         argv=['{run}', '--pair', 'mut-odo-vecdims', 'list'],
         ok=V(has=['The first: slice-primes/mut-odo-vecdims']),
         bug=V(has=['The first: mut-odo-vecdims/slice-primes'])),

    case('alloc-ceiling-over-the-named-cells', 'read-run.py', 'febc2bd',
         'the ceiling was a max over agreeing cells the sentence excludes',
         argv=['--unit', 'small_ceiling([(2e-4, "s1", "a", 500.0),'
                         ' (1e-5, "s2", "b", 5000.0)])'],
         ok=V(has=['500']),
         bug=V(hasnt=['500.0'])),

    case('dropped-control-pairs-are-named', 'read-run.py', 'de79a95',
         'a pair dropped for a sunk cell narrowed a PUBLISHED figure quietly',
         plant=lambda t: {'run': doctored(
             t, 'slice',
             lambda bs: scale(bs, 'slice-primes/mut-odo-vecdims', 0.01)),
             'readme': edited_readme(t)},
         argv=['{run}', '--block', '--readme', '{readme}'],
         # `14 of 16 intervals` was a captured run's own coverage count --
         # the built one reads 13 of 16, the 16 being the roster's control
         # pairs and stable, the 14 not. The defect is that the calibration
         # narrowed silently, so what the verdict is about is an intervals
         # line printed with no notice beside it.
         ok=V(has=['control pair(s) not readable']),
         bug=V(has=['intervals cover 1'],
               hasnt=['control pair(s) not readable'])),

    case('controls-survive-a-negative-term', 'read-run.py', '38a963a',
         "the sum-only pair is computed twice and was guarded once",
         plant=lambda t: {'run': doctored(
             t, 'slice',
             lambda bs: scale(bs, 'slice-primes/sum-only-early', -1.0)),
             'readme': edited_readme(t)},
         argv=['{run}', '--block', '--readme', '{readme}'],
         ok=V(has=['Controls:'], hasnt=['math domain error']),
         bug=V(has=['math domain error'])),

    case('tree-check-that-could-not-run', 'check-scripts.py', 'ea4ab06',
         'this suite\'s one guarantee about itself passed unchecked',
         argv=['--unit', "tree_state.__doc__ and (git('rev-parse')"
                         ".returncode, tree_state() is None)"],
         ok=V(has=['(0, False)']),
         bug=V(hasnt=['(0, False)'])),

    case('tree-change-in-both-directions', 'check-scripts.py', 'ea1a3e6',
         'a file REMOVED tripped the alarm and printed nothing beneath it',
         argv=['--unit', "tree_delta('?? a\\n?? b\\n', '?? b\\n')"],
         ok=V(has=['gone']),
         bug=V(hasnt=['gone'])),

    # ---- align-as.py ---------------------------------------------------
    case('maxskip-zero-is-off', 'align-as.py', '437ce00',
         'LOOP_MAXSKIP=0 built the max-skip form',
         plant=asm,
         env={'REAL_AS': '{as}', 'LOOP_MAXSKIP': '0',
              'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(has=['unconditionally'], hasnt=['max-skip budget']),
         bug=V(has=['max-skip budget'])),

    case('head-after-a-zero-operand-instruction', 'align-as.py', '437ce00',
         'a loop head following `ret` was dropped in silence',
         plant=asm,
         env={'REAL_AS': '{as}', 'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(has=['aligned 1 loop head']),
         bug=V(has=['aligned 0 loop head'])),

    case('pad-is-announced', 'align-as.py', '437ce00',
         'the pad is per invocation, so a second line is the only tell',
         plant=asm,
         env={'REAL_AS': '{as}', 'PAD_BYTES': '8192'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(has=['8192 pad byte(s) appended']),
         bug=V(hasnt=['pad byte(s) appended'])),

    case('empty-pad-bytes', 'align-as.py', '09782f7',
         "PAD_BYTES= killed the compile with int('') at import",
         plant=asm,
         env={'REAL_AS': '{as}', 'PAD_BYTES': '', 'LOOP_ALIGN': ''},
         argv=['-c', '-o', '{obj}', '{asm}'],
         # The one verdict here with no positive assertion, and it is at
         # its floor rather than overlooked: the stand-in assembler does
         # nothing, so there is no artifact to probe and a clean run says
         # nothing at all. What bounds it is --audit, which raises
         # ValueError on the code before the fix.
         ok=V(exit=0, hasnt=['ValueError']),
         bug=V(has=['ValueError'])),

    case('probe-that-did-not-assemble', 'align-as.py', '437ce00',
         'a failed probe made the max-skip half the unconditional one',
         plant=asm,
         env={'REAL_AS': '{as}', 'LOOP_MAXSKIP': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(has=['objdump -t', 'not the max-skip form']),
         bug=V(hasnt=['not the max-skip form'])),

    # ---- loop-offsets.py -----------------------------------------------
    case('objdump-status', 'loop-offsets.py', '0a1bc60',
         'a binary that was never opened read as one with no loops',
         argv=['--survey', 'no-such-binary'],
         ok=V(exit=1, has=['objdump'], hasnt=['0 self-loops']),
         bug=V(exit=0, has=['0 self-loops'])),

    case('addr2line-status', 'loop-offsets.py', '9832f0b',
         'an unreadable -e file read as a build without DWARF',
         argv=['--unit', "arms('no-such-binary', [4096])"],
         ok=V(has=['addr2line', 'mangled symbol']),
         bug=V(hasnt=['mangled symbol'])),

    case('suppressed-groups-are-counted', 'loop-offsets.py', 'febc2bd',
         'a group under --min-copies vanished, the docstring\'s own example',
         argv=['--len', '24', '/usr/bin/objdump'],
         ok=V(has=['suppressed']),
         bug=V(hasnt=['suppressed'])),

    # ---- read-all.sh ---------------------------------------------------
    case('aa-worst-cell-is-not-an-insitu-row', 'read-all.sh', '8ee1e5b',
         'with every twin filtered out an in-situ row was read as the A/A',
         plant=lambda t: synthetic_run(t, no_twins=True),
         argv=['{tag}'],
         ok=V(has=['(no A/A pair in this file)']),
         bug=V(hasnt=['(no A/A pair in this file)'])),

    case('killed-run-does-not-gate-clean', 'read-all.sh', '95527c5',
         'a run killed mid-process gated what landed and called it clean',
         plant=lambda t: synthetic_run(t, killed=True),
         argv=['{tag}'],
         ok=V(exit=1, has=['not all here']),
         bug=V(exit=0, has=['every process gated clean'])),

    case('log-with-no-start-lines', 'read-all.sh', 'febc2bd',
         'a log the awk matched nothing in gated one JSON and called it clean',
         plant=lambda t: synthetic_run(t, no_starts=True),
         argv=['{tag}'],
         ok=V(exit=1, has=['no `start` line in'],
              hasnt=['every process gated clean']),
         bug=V(exit=0, has=['every process gated clean'])),

    case('aa-refusal-is-not-no-A-A-pair', 'read-all.sh', 'c2cfefc',
         'a reader that REFUSED read as a file with no A/A pair, at exit 0',
         # `--aa` broken outright, which `2>/dev/null` and an unread `$?`
         # turned into an assertion ABOUT THE FILE. The run is planted into
         # the SHADOW because the mutation lives there and read-all.sh
         # globs its own directory; planted here it would not be in the
         # shadow at all, `shadow_dir` having symlinked this directory
         # before the plant ran.
         plant=lambda t: synthetic_run(t, into=os.path.join(t, 'shadow')),
         shadow=dict(mutate=[('read-run.py', 'def aa_table(',
                              'def aa_table_BROKEN(')]),
         argv=['{tag}'],
         ok=V(exit=1, has=['--aa REFUSED'],
              hasnt=['every process gated clean']),
         bug=V(exit=0, has=['(no A/A pair in this file)',
                            'every process gated clean'])),

    case('run-that-complained-does-not-gate-clean', 'read-all.sh', 'cc8abfd',
         "the run's own `!!` lines were stepped over, rc=0 hiding them",
         plant=lambda t: synthetic_run(t, complained=True),
         argv=['{tag}'],
         ok=V(exit=1, has=['complaint(s) from the run itself'],
              hasnt=['every process gated clean']),
         bug=V(exit=0, has=['every process gated clean'])),

    case('quoted-note-block-is-not-a-run-complaint', 'read-all.sh',
         'bf9acf2',
         'the pair note run-major.sh quotes carried `!!`, read as the run\'s',
         plant=lambda t: synthetic_run(t, note_block=True),
         argv=['{tag}'],
         # run-major.sh's own complaints are stamped `=== <date>  !! ...`;
         # the note it quotes is indented and unstamped. Counting bare `!!`
         # made every run whose gate tripped the machine check report a
         # complaint no process made, at exit 1, for ever after -- which is
         # exactly the noise-for-signal failure that stops a gate being
         # read. Found on Run 16, whose gate fired for a basis-area change.
         ok=V(exit=0, has=['every process gated clean'],
              hasnt=['complaint(s) from the run itself']),
         bug=V(exit=1, has=['complaint(s) from the run itself'],
               hasnt=['every process gated clean'])),

    case('table-row-narrower-than-its-header', 'read-run.py', '0e2934c',
         'a row two cells short put its values under the wrong runs',
         plant=lambda t: {'readme': readme_with_ragged_row(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['narrower than its header']),
         bug=V(exit=0, hasnt=['narrower than its header'])),

    case('machine-check-names-the-control-it-leaves', 'read-run.py',
         '0e2934c',
         'a failing machine check named no way to tell the box from the area',
         # Run 16 moved the published basis to `-A32m` while the kept
         # fingerprint is a default-area half's, so `list` net had to differ
         # and the check had to fire -- correctly, and with nothing in its
         # message to separate a changed box from a changed area. The answer
         # costs no build (`-rtsopts` is live) and no pair: run the gate's own
         # selection on any binary at the fingerprint's area. Written as a
         # capability rather than a caveat, per README's rule that a
         # limitation is recorded with what it still leaves possible.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--machine'],
         ok=V(exit=1, has=['PAST', 'at the fingerprint']),
         bug=V(exit=1, has=['PAST'], hasnt=['at the fingerprint'])),

    case('alone-leg-riders-are-not-populations', 'read-all.sh', 'bf9acf2',
         'the riders a paired run leaves were gated as populations',
         plant=lambda t: synthetic_run(t, riders=True),
         argv=['{tag}'],
         # `$R-al-*` is one bench on one shape, with no A/A pair and no
         # sum-only: gating it says nothing and pushes the eighteen this
         # driver counts off the top of the screen. Excluded exactly as
         # `$R-gate-*` is, and for the same reason. Run 16 left 54 of them.
         ok=V(exit=0, has=['every process gated clean', 'lookrts-rev'],
              hasnt=['al-lookrts-cnn-slice-c32-r1']),
         bug=V(exit=0, has=['al-lookrts-cnn-slice-c32-r1'])),

    case('six-pair-floor-disagrees-across-sites', 'read-run.py', '054f3f1',
         'the six-pair figure was quoted three ways, two in one paragraph',
         # The eighteen-pair floor has been held across its sites since
         # 2026-08-14 and caught Run 16's own write-up. The six-pair figure
         # beside it was held nowhere, and a comprehension read of Run 16
         # found it quoted 0.39%/0.24% in four places, 0.50% in a fifth --
         # a run stale -- and rounded to "half a percent" in a sixth, two
         # of them inside one paragraph. Same shape of defect, same check.
         # THE ANCHOR IS RUN-SCOPED and has to be re-aimed by every run: it
         # is a six-pair quote, and a six-pair quote is one of the figures
         # a run replaces. Run 17 re-aimed it off Run 16's floor-section
         # sentence, which its own write-up had rewritten, and the fixture
         # reported FIXTURE DID NOT BUILD until it was --- which is the
         # loud failure this case wants rather than a silent pass. Aim it
         # at whatever sentence the floor section then quotes.
         plant=lambda t: {'readme': edited_readme(t, (
             'the same run gives 1.31% and 0.56%',
             'the same run gives 1.51% and 0.56%'))},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['six-pair figure is quoted differently']),
         bug=V(exit=0, hasnt=['six-pair figure is quoted differently'])),

    case('calibration-base-disagrees-across-sites', 'read-run.py', '054f3f1',
         'the A/A population read six pairs in one section and eighteen in another',
         # The twelve twins took the A/A population from six pairs to
         # eighteen on 2026-08-14, and two sites kept saying six for three
         # runs -- the reader's own section and the floor section's
         # per-population rule -- while every class block printed
         # "N of 18". Nothing compared them.
         plant=lambda t: {'readme': edited_readme(t, (
             'as an order of magnitude: it rests on eighteen pairs.',
             'as an order of magnitude: it rests on six pairs.'))},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['A/A population is quoted as']),
         bug=V(exit=0, hasnt=['A/A population is quoted as'])),

    case('gate-arms-track-the-selection', 'run-gate.sh', 'febc2bd',
         'the expected bench count was a literal that had to equal SEL',
         shadow=dict(
             mutate=[('run-gate.sh',
                      "'*/sum-only-early' '*/sum-only-late')",
                      "'*/sum-only-early' '*/sum-only-late' '*/offtab')")],
             extra=[('zzgate-a1g', FAKE_HALF), ('zzgate-lookrts', FAKE_HALF),
                    ('zzgate-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzgate'],
         ok=V(has=['expecting 18 benches a process']),
         bug=V(has=['expecting 15 benches a process'])),

    case('smoke-sweep-runs-clean', 'smoke-sweep.sh', None,
         'CONTROL: every reader mode, both installers and its own refusals',
         shadow=dict(extra=halves('zzsw-lookrts', 'zzsw-a1g')),
         # Both taken from the fixture rather than named: the sweep's own
         # defaults are chosen for how long a real -L1 process takes, which
         # a stand-in does not, and a shape the fixture does not carry
         # stops it at `--list has no <shape>` before any mode is swept.
         env={'SHAPE': main_shapes()[0], 'CLASS': class_shapes('window')[0],
              'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzsw'],
         ok=V(exit=0, has=['sweep clean'], hasnt=['!!'])),

    case('pair-halves-must-differ', 'run-major.sh', '0431efe',
         'one name in both halves wrote nine JSONs twice and gated clean',
         shadow=dict(extra=halves('zzhh-lookrts')
                     + [('zzhh-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'lookrts', 'BASIS': 'lookrts'},
         argv=['zzhh'],
         ok=V(exit=1, has=['a pair is two halves']),
         bug=V(exit=0)),

    case('class-name-carries-no-hyphen', 'run-major.sh', '8cb5eb7',
         'a hyphenated class merged with the one before its hyphen',
         shadow=dict(mutate=[('run-major.sh', 'reshape1 slice window scaled"',
                              'reshape1 slice window scaled bcast-mid"')],
                     extra=halves('zzhy-lookrts', 'zzhy-a1g')
                     + [('zzhy-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzhy'],
         ok=V(exit=1, has=['carries a hyphen']),
         bug=V(hasnt=['carries a hyphen'])),

    case('smoke-exercises-the-shape-filter', 'smoke-sweep.sh', 'd852517',
         'the shape filter could only pass, naming a shape not in the run',
         # The reader's refusal is turned into a zero exit, which is the one
         # thing the sweep's check is there to catch: a filter told to
         # empty a one-shape run and not refusing. Before the fix the sweep
         # named a main-set shape this run does not carry, so the filter
         # matched nothing, the mode passed, and this mutation was
         # invisible to it.
         shadow=dict(mutate=[('read-run.py',
                              "sys.exit('nothing left after --exclude')",
                              'sys.exit(0)')],
                     extra=halves('zzxf-lookrts', 'zzxf-a1g')),
         env={'SHAPE': main_shapes(1)[0], 'CLASS': class_shapes('window')[0],
              'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzxf'],
         ok=V(exit=1, has=['did NOT refuse']),
         bug=V(exit=0, has=['sweep clean'])),

    case('major-run-runs-clean', 'run-major.sh', None,
         'CONTROL: the whole sequence, eighteen processes, on stand-ins',
         shadow=dict(extra=halves('zzmj-lookrts', 'zzmj-a1g')
                     + [('zzmj-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzmj'],
         ok=V(exit=0, has=['major run complete'], hasnt=['!!'])),

    case('provenance-git-could-not-read', 'run-major.sh', '845c8d0',
         'a run whose git failed recorded a commitless, CLEAN-looking tree',
         shadow=dict(extra=halves('zzmj-lookrts', 'zzmj-a1g')
                     + [('zzmj-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzmj'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzmj-wallclock.log')).read(),
         ok=V(has=['GIT DID NOT ANSWER'],
              hasnt=['tree at , Main.hs at']),
         bug=V(has=['tree at , Main.hs at',
                    '0 path(s) untracked or modified'])),

    case('bench-count-complaint-names-its-process', 'run-major.sh', '845c8d0',
         'nine identical complaints in one log, none naming its process',
         # UNDERPRINT is FAKE_RUN with its printing loop shortened, so it
         # carries the same @RUN@ token and needs the same substitution --
         # left out, the stub reads a path with `@RUN@` still in it and the
         # run dies before writing the log this case probes. Its half's
         # data comes separately, `halves` shipping only what it stands in
         # for.
         shadow=dict(extra=[('zzmj-lookrts',
                             UNDERPRINT.replace('@HALF@', 'lookrts')
                                       .replace('@RUN@', SRC))]
                     + halves('zzmj-a1g')
                     + whole_run(['lookrts'])
                     + [('zzmj-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzmj'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzmj-wallclock.log')).read(),
         # `expected 1128 benches` was the live roster's own count, so the
         # verdict only held while the fixture was a captured run of that
         # roster. What the case is about is whether the complaint NAMES
         # its process, which both spellings say without a figure.
         ok=V(exit=1, has=['zzmj-lookrts-main: expected']),
         bug=V(exit=1, has=['benches, got'],
               hasnt=['zzmj-lookrts-main: expected'])),

    # ---- install-tables.sh ---------------------------------------------
    case('lead-patterns-disagree', 'install-tables.sh', None,
         'a lead one pattern missed was overwritten by the block above it',
         plant=lambda t: {'doc': edited_readme(
             t, ('**`window` --- overlapping', '**`window` - overlapping'))},
         shadow=dict(extra=whole_run(['lookrts'], prefix='zzit')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzit'],
         # No --audit: this fixture is built from the live README, which
         # the Basic Latin pass reworded under it. Removal is the handling.
         ok=V(exit=1, has=['the two ways this file finds a class block',
                           'missing from the pattern: window'],
              hasnt=['matched by the pattern only'])),

    case('no-class-block-leads', 'install-tables.sh', '4086ab8',
         'the guard against a silently skipped class was itself silent',
         plant=lambda t: {'doc': readme_without_class_leads(t)},
         shadow=dict(extra=whole_run(['lookrts'], prefix='zzit')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzit'],
         ok=V(exit=1, has=['no class block leads'], hasnt=['REFUSED']),
         bug=V(has=['REFUSED'], hasnt=['no class block leads'])),

    case('heading-between-two-class-blocks', 'install-tables.sh', None,
         "a paragraph between blocks took the block above it's figures",
         plant=lambda t: {'doc': readme_heading_between_blocks(t)},
         shadow=dict(extra=whole_run(['lookrts'], prefix='zzit')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzit'],
         probe=lambda subs: open(subs['doc']).read(),
         # No --audit: this fixture is built from the live README, which
         # the Basic Latin pass reworded under it. Removal is the handling.
         ok=V(exit=0, has=['ZZMARKER',
                           'across 8 class block(s)'])),

    case('placeholder-that-outlived-its-wording', 'install-tables.sh',
         None,
         'a reworded emit installed a literal `___` into the README',
         plant=lambda t: {'doc': edited_readme(t)},
         shadow=dict(mutate=[
             ('read-run.py',
              "print('**Provenance:** elapsed ___, peak ___ MiB in use, ___ MiB"
              " max'",
              "print('**Provenance:** elapsed ___, peak of ___ MiB in use, ___"
              " MiB max'")],
             extra=whole_run(['lookrts'], prefix='zzit')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzit'],
         probe=lambda subs: open(subs['doc']).read(),
         # No --audit: this fixture is built from the live README, which
         # the Basic Latin pass reworded under it. Removal is the handling.
         ok=V(has=['placeholder survived'], hasnt=['peak of ___ MiB'])),

    case('two-shape-class-refused-before-writing', 'install-tables.sh',
         None,
         'a two-shape class aborted AFTER eleven tables were already in',
         plant=lambda t: {'doc': edited_readme(t)},
         shadow=dict(extra=whole_run(['lookrts'], prefix='zzts',
                                     short_class='scaled')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzts'],
         # No --audit: this fixture is built from the live README, which
         # the Basic Latin pass reworded under it. Removal is the handling.
         ok=V(exit=1, has=['fewer than three shapes',
                           'NOTHING HAS BEEN WRITTEN'],
              hasnt=['table(s) installed'])),

    case('basis-glob-catches-no-other-half', 'install-tables.sh', '440b22d',
         'a control half named <basis>-pa was installed as the basis',
         plant=lambda t: {'doc': edited_readme(t)},
         shadow=dict(extra=whole_run(['lookrts'], prefix='zzhg')
                     + [('zzhg-lookrts-pa-rev.json', '["criterion","x",[]]')]),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzhg'],
         ok=V(exit=1, has=['is not a class name']),
         bug=V(hasnt=['is not a class name'])),

    case('install-is-idempotent', 'install-tables.sh', None,
         'CONTROL: a full pass over an untouched README rewrites no table',
         plant=lambda t: {'doc': edited_readme(t)},
         shadow=dict(extra=whole_run(['lookrts'], prefix='zzit')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzit'],
         ok=V(exit=0, has=['11 table(s) installed'])),
]


def shadow_dir(tmp, prog, text, mutate=(), extra=()):
    """This directory in symlink, with some files real and changed.

    Two defects here are LATENT: a literal that must equal the globs above
    it, and four replaces against wording another script owns. Neither can
    be provoked by any input -- only by changing the thing it depends on,
    which for a case would mean editing the tree. So the case gets a
    directory of symlinks instead, with the files it changes written real
    inside it, and every script runs there: each of them either cds to its
    own directory or resolves README.md and Main.hs from `__file__`, so a
    shadow is the one place a driver can be exercised against something
    other than what is committed. Nothing here is written; the shadow goes
    when the case does.

    `extra` is how a driver that wants a BINARY gets one. `run-gate.sh`
    refuses without two executables and a pair note, and its whole verdict
    path runs in seconds against a stand-in that answers `--list` -- which
    is what stood between the run drivers and any coverage at all.
    """
    d = os.path.join(tmp, 'shadow')
    os.mkdir(d)
    for name in os.listdir(HERE):
        if name.startswith('zz-') or name == '__pycache__':
            continue
        os.symlink(os.path.join(HERE, name), os.path.join(d, name))
    real = os.path.join(d, prog)
    os.remove(real)
    write(real, text)
    os.chmod(real, 0o755)
    for name, body in extra:
        at = os.path.join(d, name)
        if os.path.lexists(at):
            os.remove(at)
        os.chmod(write(at, body), 0o755)
    for name, was, now in mutate:
        at = os.path.join(d, name)
        src = open(at).read()
        n = src.count(was)
        if n != 1:
            raise AssertionError('%s: mutation anchor occurs %d times, need'
                                 ' 1: %r' % (name, n, was[:50]))
        if os.path.islink(at):
            os.remove(at)
        os.chmod(write(at, src.replace(was, now, 1)), 0o755)
    return d


# ---------------------------------------------------------------- families

def _scopes(tree):
    """{lineno: the function it is in}, and None for module scope."""
    at = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for n in ast.walk(fn):
                at.setdefault(getattr(n, 'lineno', 0), fn)
    return at


def family_lint(path):
    """The shapes these defects keep coming back in, over one file's source.

    A case is memory and a property is discovery over DATA; this is
    discovery over CODE, and it is the only one of the three that can find
    an instance nobody has met yet. Every family below was counted rather
    than guessed -- seven, four, three, three and two instances across the
    three reviews of 2026-08-17 -- and each is decidable enough to be worth
    asking of the tree on every run.

    The zip LISTS rather than fails, as the sweeps in `check_doc` do,
    because whether a positional zip is wrong is a reading.

    All four broken deliberately, 2026-08-17, on a planted file carrying
    one of each: the import-time parse, the dropped status, the unread
    flag and the filtered zip were each named with their line. Its first
    false positive is recorded at the site -- a helper that RETURNS a
    completed process has handed the status on rather than dropped it.
    """
    src = open(os.path.join(HERE, path)).read()
    tree = ast.parse(src)
    at, bad, note = _scopes(tree), [], []

    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        called = ast.unparse(n.func)
        if called.endswith('subprocess.run'):
            if any(k.arg == 'check' for k in n.keywords):
                continue
            scope = at.get(n.lineno)
            body = scope if scope is not None else tree
            # A call whose result is RETURNED has not dropped anything: it
            # has handed the status to whoever asked. `git()` here is that,
            # and was this lint's first false positive.
            handed = any(isinstance(x, ast.Return) and x.value is n
                         for x in ast.walk(body))
            if not handed and not any(
                    isinstance(x, ast.Attribute) and x.attr == 'returncode'
                    for x in ast.walk(body)):
                bad.append('%s:%d a subprocess whose status is never read and'
                           ' that has no check=True' % (path, n.lineno))
        if (getattr(n.func, 'id', None) == 'int' and n.args
                and 'environ' in ast.unparse(n.args[0])
                and at.get(n.lineno) is None):
            bad.append('%s:%d a value parsed out of the environment at'
                       ' import, outside any handler' % (path, n.lineno))
        if (getattr(n.func, 'id', None) == 'zip' and len(n.args) == 2
                and ast.unparse(n.args[1]) in ('shapes', 'strategies')):
            first = ast.unparse(n.args[0])
            scope = at.get(n.lineno)
            for a in ast.walk(scope if scope is not None else tree):
                if (isinstance(a, ast.Assign) and len(a.targets) == 1
                        and ast.unparse(a.targets[0]) == first
                        and isinstance(a.value, (ast.ListComp,
                                                 ast.GeneratorExp))
                        and any(g.ifs for g in a.value.generators)):
                    note.append('%s:%d `%s` is zipped against `%s` and was'
                                ' built by a FILTERED comprehension'
                                % (path, n.lineno, first,
                                   ast.unparse(n.args[1])))

    # The fifth family -- a check reporting in one branch with no else --
    # is NOT swept, and the ruling is measured rather than assumed. It was
    # written, run, and came back with fifteen sites in this directory of
    # which every one is the ordinary `if lost: bad.append(...)`, which
    # reports on purpose. The seven real instances were all found by
    # reading, and each was an `if` guarding a whole CHECK rather than a
    # report -- which this shape cannot tell apart. A list that never
    # empties is one nobody reads, and it would have cost the four families
    # above their credibility. 2026-08-17.
    return bad, note


def family_flags(path):
    """An argparse flag the program accepts and never reads.

    Three of these in one review: a flag taken and ignored is a request
    the program answers by doing something else, at exit 0.
    """
    src = open(os.path.join(HERE, path)).read()
    dests = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and getattr(n.func, 'attr', '') \
                == 'add_argument':
            named = [k.value.value for k in n.keywords if k.arg == 'dest']
            if named:
                dests.add(named[0])
                continue
            for a in n.args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    dests.add(a.value.lstrip('-').replace('-', '_'))
    return ['%s: --%s is accepted and never read' % (path, d)
            for d in sorted(dests)
            if not re.search(r'args\.%s\b|getattr\(args, .%s.' % (d, d), src)]


def families():
    """Every family, over every program here. Names the site, not a count."""
    bad, note = [], []
    for f in sorted(os.listdir(HERE)):
        if not f.endswith('.py') or f.startswith('zz'):
            continue
        b, n = family_lint(f)
        bad += b + family_flags(f)
        note += n
    for line in bad:
        print('  FAIL %s' % line)
    if note:
        print('  note: %d site(s) of a shape worth a look, listed rather'
              ' than failed:' % len(note))
        for line in note:
            print('        %s' % line)
    if not bad:
        print('  ok   no dropped status, no unread flag and no import-time'
              ' environment parse, over %d file(s)'
              % len([f for f in os.listdir(HERE) if f.endswith('.py')
                     and not f.startswith('zz')]))
    return len(bad)


# ------------------------------------------------------------- properties

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
    which is why each property PRINTS what it covered.
    """
    return sorted(f for f in os.listdir(HERE)
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
            d = json.load(open(os.path.join(HERE, f)))
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
            cells, shapes, strategies, meta = m.load(os.path.join(HERE, f),
                                                     MAIN)
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
                              f, '--selftest'], cwd=HERE,
                             capture_output=True, text=True, timeout=300)
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


# ------------------------------------------------------------------ runner

UNIT = """\
import importlib.util, sys
spec = importlib.util.spec_from_file_location('under_test', sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print(repr(eval(sys.argv[2], vars(m))))
"""


def _takes_rev(fn):
    """Whether a plant wants the revision as well as the temp directory.

    REQUIRED positionals only. Counting every parameter called `asm(tmp)`
    and `edited_readme(t, pair=None)` rev-taking too, because their
    optional arguments made the count two, and five fixtures stopped
    building at once -- reported honestly as `did not build` rather than as
    failures, which is what made it obvious rather than subtle.
    """
    try:
        ps = inspect.signature(fn).parameters.values()
    except (TypeError, ValueError):
        return False
    return len([p for p in ps if p.default is p.empty
                and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
               ) >= 2


def at_rev(prog, rev):
    """`prog`'s text as of `rev`, or an error naming what could not be read."""
    got = git('show', '%s:micro-regime3/%s' % (rev, prog))
    if got.returncode != 0:
        raise AssertionError('%s at %s: %s' % (prog, rev, got.stderr.strip()))
    return got.stdout


def materialise(prog, rev):
    """`prog` as of `rev`, written HERE so its own path lookups still work.

    Both readers resolve Main.hs and README.md from `__file__`, and both
    shell drivers cd to their own directory, so a copy run from anywhere
    else answers a different question -- which is how one proof was made
    worthless before this file existed. The substitution is one file: a
    driver under test still calls today's `./read-run.py`, exactly as the
    proofs did.
    """
    p = here_file('zz-against-' + prog)
    write(p, at_rev(prog, rev))
    os.chmod(p, 0o755)
    return p


def invoke(prog_path, c, subs):
    argv = [a.format(**subs) for a in c.argv]
    env = dict(os.environ)
    env.update({k: v.format(**subs) for k, v in c.env.items()})
    if argv[:1] == ['--unit']:
        cmd = [sys.executable, '-c', UNIT, prog_path, argv[1]]
    elif prog_path.endswith('.py'):
        cmd = [sys.executable, prog_path] + argv
    else:
        cmd = ['bash', prog_path] + argv
    r = subprocess.run(cmd, cwd=HERE, env=env, capture_output=True,
                       text=True, timeout=600)
    return r.returncode, r.stdout + r.stderr


def judge(want, code, out):
    off = []
    if want['exit'] is not None and code != want['exit']:
        off.append('exit %d, wanted %d' % (code, want['exit']))
    for s in want['has']:
        if s not in out:
            off.append('did not say %r' % s)
    for s in want['hasnt']:
        if s in out:
            off.append('said %r and should not' % s)
    return off


def run(cases, rev, want_key):
    """-> (failed, skipped, unbuilt), and the third is not the first.

    A fixture that would not build is its own outcome. It used to be
    counted with the failures, so `--audit` said `did NOT reproduce their
    defect, so they prove nothing` about a case whose PLANT had raised --
    which reads as a vacuous case where the truth is that nothing was
    tried, and it is the audit's own value that the sentence spends. It
    happened here on 2026-08-17, to a case stamped with an unexpanded
    shell substitution: the revision lookup failed and the run reported a
    defect that had not reproduced.

    The distinction matters most in the audit direction, where a plant
    derived from today's README meets a script from before the fix: an
    anchor that moved between the two makes the plant misapply, and the
    one thing that must not happen is for that to read as a verdict about
    the case. THREE-VALUED, so it cannot.
    """
    bad = skipped = unbuilt = 0
    for c in cases:
        want = getattr(c, want_key)
        if want is None:
            print('  --   %-42s control, no defect to replay' % c.name)
            skipped += 1
            continue
        at = c.fix + '^' if rev == 'BEFORE' else rev
        off = broke = None
        try:
            with tempfile.TemporaryDirectory(prefix='check-scripts-') as tmp:
                if c.shadow is None:
                    prog = (os.path.join(HERE, c.prog) if at is None
                            else materialise(c.prog, at))
                else:
                    # The revision under test goes INTO the shadow, and the
                    # mutations are applied on top of it, so `--audit` reads
                    # the same latent defect the case was written for.
                    text = (open(os.path.join(HERE, c.prog)).read()
                            if at is None else at_rev(c.prog, at))
                    prog = os.path.join(
                        shadow_dir(tmp, c.prog, text, **c.shadow), c.prog)
                # A plant taking a second parameter is handed the REVISION
                # under test -- None for the live tree -- because a fixture
                # derived from this README is only right for the code of its
                # own era. `readme_lines` says what goes wrong otherwise.
                subs = ({} if not c.plant else
                        (c.plant(tmp, at) if _takes_rev(c.plant)
                         else c.plant(tmp))) or {}
                # Where the case runs matters to a probe: a driver writes
                # its log beside itself, which for a shadowed case is the
                # shadow and not this directory.
                subs.setdefault('prog', prog)
                subs.setdefault('at', os.path.dirname(prog))
                code, out = invoke(prog, c, subs)
                if c.probe:
                    out += '\n' + c.probe(subs)
                off = judge(want, code, out)
        except Exception as e:
            broke = '%s: %s' % (type(e).__name__, e)
        finally:
            sweep()
        if broke is not None:
            unbuilt += 1
            print('  ??   %-42s FIXTURE DID NOT BUILD: %s' % (c.name, broke))
            print('       %s -- nothing was tried, so this is no verdict'
                  % c.gist)
        elif off:
            bad += 1
            print('  FAIL %-42s %s' % (c.name, '; '.join(off)))
            print('       %s' % c.gist)
        else:
            print('  ok   %-42s %s' % (c.name, c.gist))
    return bad, skipped, unbuilt


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('-k', dest='pattern', help='only cases matching this')
    p.add_argument('--list', action='store_true',
                   help='what is covered, and by which fix')
    p.add_argument('--audit', action='store_true',
                   help='replay each case against the commit before its own'
                        ' fix, where it must fail')
    p.add_argument('--against', metavar='REV',
                   help='run every case against some other revision')
    p.add_argument('--properties', action='store_true',
                   help='the properties, over every run on disk rather than'
                        ' over any fixture')
    p.add_argument('--warnings', action='store_true',
                   help='with --properties: the reader\'s own stderr'
                        ' verbatim, which is withheld and counted by kind')
    p.add_argument('--families', action='store_true',
                   help='the shapes these defects keep returning in, over'
                        ' the source of every program here')
    args = p.parse_args()

    cases = [c for c in CASES
             if not args.pattern or args.pattern in c.name]
    if not cases:
        sys.exit('no case matches %r' % args.pattern)

    if args.list:
        for c in cases:
            print('%-44s %-18s %-9s %s'
                  % (c.name, c.prog, c.fix or 'control', c.gist))
        print('\n%d case(s) over %d script(s)'
              % (len(cases), len(set(c.prog for c in cases))))
        return 0

    before = tree_state()
    if args.families:
        print('the defect families, over this directory\'s source:')
        bad, skipped, unbuilt = families(), 0, 0
        verdict = '%d site(s) of a known family' % bad if bad else ''
    elif args.properties:
        print('properties over the live corpus:')
        bad, skipped, unbuilt = properties(args.warnings), 0, 0
        verdict = '%d propert(ies) FAILED' % bad if bad else ''
    elif args.audit:
        print('replaying %d case(s) against the code before each fix, where'
              ' each MUST fail:' % len(cases))
        bad, skipped, unbuilt = run(cases, 'BEFORE', 'bug')
        verdict = ('%d case(s) did NOT reproduce their defect, so they prove'
                   ' nothing' % bad if bad else '')
    else:
        rev = args.against
        print('%d case(s) against %s:'
              % (len(cases), rev or 'the working tree'))
        bad, skipped, unbuilt = run(cases, rev, 'ok')
        verdict = '%d case(s) FAILED' % bad if bad else ''
        # The families come with the default run because they cost a tenth
        # of a second and are the half that can name a site nobody has met.
        # The properties do not, at fifteen seconds, so the line below is
        # what keeps them from being forgotten.
        if not args.pattern and rev is None:
            print('and the families over this directory\'s source:')
            fam = families()
            if fam:
                bad += fam
                verdict = ((verdict + ', and ') if verdict else '') + (
                    '%d site(s) of a known family' % fam)
    after = tree_state()
    if before is None or after is None:
        print('!! `git status` did not answer, so whether this run left the'
              ' tree as it found it was NOT checked')
        bad += 1
    elif after != before:
        # It cannot know WHOSE change this is, and it said it could. The
        # tree moved under a run on 2026-08-17 because another session
        # committed to the same checkout while the audit was replaying, and
        # the report accused this suite of a write it had not made. Naming
        # both explanations costs a line and keeps the alarm worth reading:
        # a suite that cries wolf about a colleague's commit is one whose
        # next real leak gets waved past.
        print('!! the working tree changed during this run. If a case did'
              ' it, that is a defect here -- this suite must leave the tree'
              ' as it found it. A concurrent edit to the same checkout is'
              ' the other explanation, and the delta below says which:')
        print('\n'.join(tree_delta(before, after)))
        bad += 1
    if unbuilt:
        # Its own line and its own exit, because a fixture that would not
        # build says nothing either way about the code it was aimed at.
        verdict = ((verdict + ', and ') if verdict else '') + (
            '%d fixture(s) did not build, which is neither a pass nor a'
            ' failure: the anchor each plants against has moved, or the'
            ' revision it wanted is not there' % unbuilt)
    if bad or unbuilt:
        print('\n%s' % verdict)
        return 1
    if not (args.audit or args.properties or args.families or args.against):
        print('\n(--properties asks the reader\'s own invariants, and two'
              ' more, of every run\n on disk rather than of any fixture:'
              ' fifteen seconds, and not run here)')
    print('\nevery %s%s'
          % ('family comes back clean' if args.families
             else 'property holds over every run on disk' if args.properties
             else 'case reproduced its defect' if args.audit
             else 'case holds',
             ', %d control(s) not replayed' % skipped if skipped else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
