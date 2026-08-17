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
A stored copy of the page would rot silently as the page moved, which is
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
page, which is sound wherever the defect is in the code and the fixture is
merely an input of the right shape -- which is every case here. It would
not be sound for a case whose defect is about the page's own shape, where
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
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

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

def readme_lines():
    return open(README).read().split('\n')


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
    cell = re.compile(r'\| `[a-z0-9-]+` \| \d+ \| \d+ \| [\d.]+ [nµm]?s \|')
    fp = [i for i, l in enumerate(lines) if cell.match(l)]
    assert fp, 'no fingerprint row to plant a `?` in'
    lines[fp[0]] = re.sub(r'\| [\d.]+ [nµm]?s \|', '| ? |', lines[fp[0]], 1)
    return write(os.path.join(tmp, 'R.md'), '\n'.join(lines))


def readme_goal_above_open(tmp):
    """The goal section moved above the open list: nothing renamed.

    The case the first repair missed -- renaming a heading trips a
    neighbouring check, where reordering trips none.
    """
    lines = readme_lines()
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


def readme_without_class_leads(tmp):
    """Every class block lead unbackticked, so the grep finds none.

    `install-tables.sh` checks that no class is silently skipped by holding
    the JSONs on disk to the page's leads, and the check was itself silent
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
    a page worked on before it is added had every hit called old.
    """
    doc = here_file('zz-case-untracked.md')
    write(doc, open(README).read()
          + '\nThe fastest arm of every population is the one this planted'
            ' sentence pretends to name, which makes it the biggest'
            ' superlative on the page.\n')
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


def doctored(tmp, src, mutate, name='x.json'):
    d = json.load(open(run_json(src)))
    n = mutate(d[2])
    assert n, 'the mutation matched no bench in %s' % src
    p = os.path.join(tmp, name)
    with open(p, 'w') as f:
        json.dump(d, f)
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
if [ -n "$CLS" ]; then SRC="$D/run14-@HALF@-$CLS.json"
else SRC="$D/run14-@HALF@-main.json"; fi
if [ "$1" = classes ] && [ "$2" = --list ]; then
  exec python3 -c "
import glob, json, os, sys
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'run14-@HALF@-*.json'))):
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
    """A stand-in per half, named as a run's binaries are."""
    return [(n, FAKE_RUN.replace('@HALF@', n.split('-', 1)[1]))
            for n in names]

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


def synthetic_run(tmp, killed=False, no_twins=False, no_starts=False):
    """A whole run in this directory: JSONs, and the log that describes it.

    `read-all.sh` cds to its own directory and globs, so this is one of the
    two fixtures that cannot live in a temp directory.
    """
    tag = 'runzz'
    log = ['=== 2026-01-01T00:00:00+01:00 major run begins; tree at 0000000,'
           ' Main.hs at 0000000; roster is 1 benches',
           '=== 2026-01-01T00:00:00+01:00 halves: a1g lookrts, in that order;'
           ' lookrts is the basis, and every class runs on both halves']
    for cls in ('rev', 'slice'):
        src = run_json('run14-lookrts-%s.json' % cls)
        dst = here_file('%s-lookrts-%s.json' % (tag, cls))
        if no_twins:
            d = json.load(open(src))
            drop = ('mut-odo-vecdims', 'build', 'mut-odo', 'offtab',
                    'bq-scan-rem-gm-mulback', 'bq-odo-gm-mulback',
                    'bq-expand', 'list', 'gen-unsafe', 'sum-only-late')
            d[2] = [b for b in d[2]
                    if b['reportName'].split('/')[-1] not in drop]
            with open(dst, 'w') as f:
                json.dump(d, f)
        else:
            shutil.copyfile(src, dst)
        if not no_starts:
            log += ['=== 2026-01-01T00:00:01+01:00 start %s-lookrts-%s'
                    % (tag, cls),
                    '=== 2026-01-01T00:10:00+01:00 done  %s-lookrts-%s rc=0'
                    ' benchmarking=47' % (tag, cls)]
    if killed:
        log.append('=== 2026-01-01T00:10:01+01:00 start %s-lookrts-window'
                   % tag)
    write(here_file('%s-wallclock.log' % tag), '\n'.join(log) + '\n')
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
            ' superlative on the page.\n')
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
    the page becomes a `has`/`hasnt` like any other.
    """
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
                          'run': run_json('run14-lookrts-slice.json')},
         argv=['{run}', '--block', '--in-place', '--readme', '{readme}'],
         ok=V(exit=1, has=['refusing to write there'],
              hasnt=['installed at']),
         bug=V(exit=0, has=['installed at'])),

    case('block-brief-cannot-install', 'read-run.py', '045ca63',
         '--brief dropped the table --in-place had to install',
         plant=lambda t: {'readme': edited_readme(t),
                          'run': run_json('run14-lookrts-slice.json')},
         argv=['{run}', '--block', '--in-place', '--brief',
               '--readme', '{readme}'],
         ok=V(exit=0, has=['installed at']),
         bug=V(exit=1, has=['emitted no table'])),

    case('buried-action-at-eof', 'read-run.py', '045ca63',
         'the last indented block of a document was never swept',
         plant=lambda t: {'readme': readme_with_trailing_buried_action(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(has=['--survey to see it']),
         bug=V(hasnt=['--survey to see it'])),

    case('worst-beside-a-sunk-time', 'read-run.py', '045ca63',
         'a plausible `worst` published beside `time --`',
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
             lambda bs: scale(bs, 'slice-primes/mut-odo-vecdims', 0.01))},
         argv=['{run}'],
         ok=V(has=['mut-odo-vecdims                   --      --']),
         bug=V(has=['mut-odo-vecdims                   --  0.063'])),

    case('claims-arm-counted-per-registration', 'read-run.py', '045ca63',
         'one filtered arm reported as eight',
         plant=lambda t: {'run': run_json('run14-lookrts-main.json')},
         argv=['{run}', '--claims', '--exclude', 'bq-expand'],
         ok=V(has=['1 arm(s) of the claims list']),
         bug=V(has=['8 arm(s) of the claims list'])),

    case('added-lines-over-head', 'read-run.py', '045ca63',
         'a STAGED document emptied the freshness sweeps',
         plant=staged_doc,
         env={'GIT_INDEX_FILE': '{index}'},
         argv=['--check-doc', '--readme', '{doc}'],
         ok=V(has=['NEW ']),
         bug=V(has=['none added by this diff'], hasnt=['NEW '])),

    case('population-main-hs-does-not-define', 'read-run.py', '4086ab8',
         'a population Main.hs no longer defines died unpacking',
         plant=lambda t: {'run': run_json('run14-lookrts-slice.json')},
         argv=['{run}', '--markdown', '--main', '/dev/null'],
         ok=V(exit=1, has=['a population Main.hs does not define']),
         bug=V(has=['not enough values to unpack'])),

    case('ragged-gate-after-exclude', 'read-run.py', '4086ab8',
         'excluding the arm with the missing cells still refused the run',
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
             lambda bs: drop(bs, 'slice-primes/bq-expand'))},
         argv=['{run}', '--exclude', 'bq-expand'],
         ok=V(exit=0, hasnt=['did not happen']),
         bug=V(exit=2, has=['0 cell(s) missing'])),

    case('in-place-alone', 'read-run.py', '4086ab8',
         '--in-place with no installing mode printed a table and wrote none',
         plant=lambda t: {'readme': edited_readme(t),
                          'run': run_json('run14-lookrts-main.json')},
         argv=['{run}', '--in-place', '--readme', '{readme}'],
         ok=V(exit=2, has=['--in-place is a modifier']),
         bug=V(exit=0)),

    # ---- read-run.py, the second review's ------------------------------
    case('checkdoc-without-a-roster', 'read-run.py', 'a6c32e8',
         'a roster it could not parse skipped five checks at exit 0',
         plant=lambda t: {'main': mangled_main(t)},
         argv=['--check-doc', '--main', '{main}'],
         ok=V(exit=1, has=['BLOCKED: no roster parsed']),
         bug=V(exit=0)),

    case('checkdoc-open-list-out-of-order', 'read-run.py', 'a6c32e8',
         'the goal section above the open list killed the sweep in silence',
         plant=lambda t: {'readme': readme_goal_above_open(t)},
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
         plant=lambda t: {'readme': readme_current_run_sentence(t),
                          'run': run_json('run14-lookrts-main.json')},
         argv=['{run}', '--claims', '--readme', '{readme}'],
         ok=V(has=['0.9312']),
         bug=V(hasnt=['0.9312'])),

    case('path-token-dotfile', 'read-run.py', 'a6c32e8',
         "lstrip('./') ate the leading dot of a cited dotfile",
         plant=lambda t: {'readme': readme_citing_dotfile(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(hasnt=['do not resolve: .hlint.yaml']),
         bug=V(has=['do not resolve: .hlint.yaml'])),

    case('insitu-worst-cell-label', 'read-run.py', 'a6c32e8',
         'a dropped shape renamed every later ratio',
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
             lambda bs: scale(
                 bs, 'slice-cnn-L2-24x24-c32/mut-odo-vecdims-nosum', 3.0))},
         argv=['{run}', '--aa', '--brief'],
         ok=V(has=['worst cell 1.63% on slice-coprime-r7',
                   'over 2 of 3 shape(s)']),
         bug=V(has=['worst cell 1.63% on slice-primes'])),

    case('pair-refuses-a-sunk-cell', 'read-run.py', 'a6c32e8',
         'a sunk cell gave --pair a math domain error',
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
             lambda bs: scale(bs, 'slice-primes/mut-odo-vecdims', 0.01))},
         argv=['{run}', '--pair', 'mut-odo-vecdims', 'list'],
         ok=V(exit=2, has=['not readable']),
         bug=V(has=['math domain error'])),

    case('compare-refuses-a-partial-other', 'read-run.py', 'a6c32e8',
         'an interrupted other half raised KeyError',
         plant=lambda t: {'run': run_json('run14-lookrts-main.json'),
                          'other': doctored(
                              t, 'run14-lookrts-main.json',
                              lambda bs: drop(bs,
                                              'stretch-primes/bq-expand'),
                              'other.json')},
         argv=['{run}', '--compare', '{other}'],
         ok=V(exit=2, has=['cell(s) missing, so the comparison did not']),
         bug=V(has=['KeyError'])),

    case('summary-row-width', 'read-run.py', 'a6c32e8',
         'a row that lost a column had its tail compared against nothing',
         plant=lambda t: {'readme': readme_summary_row_short(t),
                          'run': run_json('run14-lookrts-slice.json')},
         argv=['{run}', '--block', '--readme', '{readme}'],
         ok=V(has=['not checked: it has 5 column(s)']),
         bug=V(hasnt=['not checked: it has 5 column(s)'])),

    case('brief-alone', 'read-run.py', 'a6c32e8',
         '--brief outside --aa/--block printed everything and said nothing',
         plant=lambda t: {'run': run_json('run14-lookrts-main.json')},
         argv=['{run}', '--markdown', '--brief'],
         ok=V(exit=2, has=['--brief is a modifier']),
         bug=V(exit=0)),

    case('two-modes-at-once', 'read-run.py', 'a6c32e8',
         'the if/elif dispatch dropped the second mode without a word',
         plant=lambda t: {'run': run_json('run14-lookrts-main.json')},
         argv=['{run}', '--markdown', '--fingerprint'],
         ok=V(exit=2, has=['one mode at a time']),
         bug=V(exit=0)),

    case('fmt-abs-above-its-top-unit', 'read-run.py', '0fe535b',
         'a time past a thousand seconds wrote an exponent nothing parses',
         argv=['--unit', 'fmt_abs(1500.0)'],
         ok=V(has=["'1500 s'"]),
         bug=V(has=['e+03'])),

    case('fmt-abs-at-the-unit-boundary', 'read-run.py', 'a6c32e8',
         '999.7 µs printed as `1e+03 µs`, which --machine cannot parse',
         argv=['--unit', 'fmt_abs(9.997e-4)'],
         ok=V(has=["'1 ms'"]),
         bug=V(has=['e+03'])),

    case('added-lines-untracked', 'read-run.py', '045ca63',
         'an untracked page had every hit called old',
         plant=untracked_doc,
         argv=['--check-doc', '--readme', '{doc}'],
         ok=V(hasnt=['none added by this diff']),
         bug=V(has=['none added by this diff'])),

    case('alloc-fit-on-an-unknown-shape', 'read-run.py', 'a6c32e8',
         'a missing alloc read as "allocated nothing", silencing the warning',
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
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
                          'run': run_json('run14-lookrts-rev.json')},
         argv=['{run}', '--markdown', '--in-place', '--main', '/dev/null',
               '--readme', '{readme}'],
         ok=V(exit=1, hasnt=['installed at']),
         bug=V(exit=0, has=['installed at'])),

    case('selftest-survives-a-sunk-cell', 'read-run.py', 'febc2bd',
         'a sunk cell gave the gate a traceback and no verdict at all',
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
             lambda bs: scale(bs, 'slice-primes/mut-odo-vecdims', 0.01))},
         argv=['{run}', '--selftest'],
         ok=V(hasnt=['math domain error'], has=['FAIL']),
         bug=V(has=['math domain error'])),

    case('aa-survives-a-sunk-cell', 'read-run.py', 'febc2bd',
         '--aa died where --claims refuses, on the same file',
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
             lambda bs: scale(bs, 'slice-primes/mut-odo-vecdims', 0.01))},
         argv=['{run}', '--aa', '--brief'],
         ok=V(hasnt=['math domain error']),
         bug=V(has=['math domain error'])),

    case('aa-lists-controls-under-no-controls', 'read-run.py', 'febc2bd',
         '--no-controls made --aa report a file of controls as having none',
         plant=lambda t: {'run': run_json('run14-lookrts-slice.json')},
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
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
             lambda bs: scale(bs, 'slice-primes/mut-odo-vecdims', 0.01))},
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
             t, 'run14-lookrts-slice.json',
             lambda bs: scale(bs, 'slice-primes/mut-odo-vecdims', 0.01)),
             'readme': edited_readme(t)},
         argv=['{run}', '--block', '--readme', '{readme}'],
         ok=V(has=['control pair(s) not readable']),
         bug=V(has=['14 of 16 intervals'],
               hasnt=['control pair(s) not readable'])),

    case('controls-survive-a-negative-term', 'read-run.py', '38a963a',
         "the sum-only pair is computed twice and was guarded once",
         plant=lambda t: {'run': doctored(
             t, 'run14-lookrts-slice.json',
             lambda bs: scale(bs, 'slice-primes/sum-only-early', -1.0)),
             'readme': edited_readme(t)},
         argv=['{run}', '--block', '--readme', '{readme}'],
         ok=V(hasnt=['math domain error']),
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
         ok=V(exit=1, hasnt=['every process gated clean']),
         bug=V(exit=0, has=['every process gated clean'])),

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
         env={'SHAPE': 'cnn-slice-c32', 'CLASS': 'window-28x28-k5',
              'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzsw'],
         ok=V(exit=0, has=['sweep clean'], hasnt=['!!'])),

    case('major-run-runs-clean', 'run-major.sh', None,
         'CONTROL: the whole sequence, eighteen processes, on stand-ins',
         shadow=dict(extra=halves('zzmj-lookrts', 'zzmj-a1g')
                     + [('zzmj-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzmj'],
         ok=V(exit=0, hasnt=['!!'])),

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
         shadow=dict(extra=[('zzmj-lookrts',
                             UNDERPRINT.replace('@HALF@', 'lookrts'))]
                     + halves('zzmj-a1g')
                     + [('zzmj-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzmj'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzmj-wallclock.log')).read(),
         ok=V(exit=1, has=['zzmj-lookrts-main: expected']),
         bug=V(exit=1, has=['expected 1128 benches'],
               hasnt=['zzmj-lookrts-main: expected'])),

    # ---- install-tables.sh ---------------------------------------------
    case('lead-patterns-disagree', 'install-tables.sh', '5ca3513',
         'a lead one pattern missed was overwritten by the block above it',
         plant=lambda t: {'doc': edited_readme(
             t, ('**`window` — overlapping', '**`window` - overlapping'))},
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['run14'],
         ok=V(exit=1, has=['the two ways this file finds a class block']),
         bug=V(exit=0, has=['across 7 class block(s)'])),

    case('no-class-block-leads', 'install-tables.sh', '4086ab8',
         'the guard against a silently skipped class was itself silent',
         plant=lambda t: {'doc': readme_without_class_leads(t)},
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['run14'],
         ok=V(exit=1, has=['no class block leads'], hasnt=['REFUSED']),
         bug=V(has=['REFUSED'], hasnt=['no class block leads'])),

    case('heading-between-two-class-blocks', 'install-tables.sh', 'febc2bd',
         "a paragraph between blocks took the block above it's figures",
         plant=lambda t: {'doc': readme_heading_between_blocks(t)},
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['run14'],
         probe=lambda subs: open(subs['doc']).read(),
         ok=V(exit=0, has=['ZZMARKER']),
         bug=V(hasnt=['ZZMARKER'])),

    case('placeholder-that-outlived-its-wording', 'install-tables.sh',
         'febc2bd',
         'a reworded emit installed a literal `___` into the page',
         plant=lambda t: {'doc': edited_readme(t)},
         shadow=dict(mutate=[
             ('read-run.py',
              "print('Provenance: elapsed ___, peak ___ MiB in use, ___ MiB"
              " max'",
              "print('Provenance: elapsed ___, peak of ___ MiB in use, ___"
              " MiB max'")]),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['run14'],
         probe=lambda subs: open(subs['doc']).read(),
         ok=V(has=['placeholder survived'], hasnt=['peak of ___ MiB']),
         bug=V(has=['peak of ___ MiB'])),

    case('install-is-idempotent', 'install-tables.sh', None,
         'CONTROL: a full pass over an untouched page rewrites no table',
         plant=lambda t: {'doc': edited_readme(t)},
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['run14'],
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
    src = open(path).read()
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
    src = open(path).read()
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
    """The emitted table as a page `readme_rows` can be pointed at."""
    p = os.path.join(tempfile.gettempdir(), 'zz-prop-page.md')
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


def properties():
    """Every property, over the live corpus, naming what failed."""
    m = reader()
    bad = 0
    for prop in PROPERTIES:
        n, what, off = prop(m)
        if off:
            bad += 1
            print('  FAIL %-28s over %d %s' % (prop.__name__, n, what))
            for line in off:
                print('       %s' % line)
        else:
            print('  ok   %-28s over %d %s' % (prop.__name__, n, what))
    return bad


# ------------------------------------------------------------------ runner

UNIT = """\
import importlib.util, sys
spec = importlib.util.spec_from_file_location('under_test', sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print(repr(eval(sys.argv[2], vars(m))))
"""


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
    derived from today's page meets a script from before the fix: an
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
                subs = (c.plant(tmp) if c.plant else {}) or {}
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
        bad, skipped, unbuilt = properties(), 0, 0
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
