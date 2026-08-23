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
do and `bug` is what the code before the fix did -- what it DID, not only
what it did not say: a `hasnt` alone holds when the old script crashed on
something else, which reproduces nothing, and twenty-two verdicts stood
that way until 2026-08-23. The default run asserts
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
as much where the code is. The other absence is one whole file,
`preflight.sh`, by its own design: its steps are this suite and the
reader's gates, so a case would run them twice, and what is its own is
proved on stub halves in its header. Every other program here has cases,
the drivers on the stand-ins above -- and the drivers are where a defect
is the most expensive kind here, being what commits the machine for
hours: the two shell scripts anyone first read closely yielded the
highest defect density in the tree, 1.9 and 0.9 per hundred lines against
`read-run.py`'s 0.47.

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
# Where --properties looks for runs: this directory, or what a case names,
# which is how an empty corpus is handed to it.
CORPUS = os.environ.get('CORPUS', HERE)
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


def a_registration_lead():
    """The lead line of some ANSWERED run registration in the README.

    Named dynamically rather than pinned to a run, because registrations
    are RETIRED to MARGINALIA once answered and two further runs have
    reported -- so a fixture naming one dies at the retirement it should
    have outlived, which is what happened to Run 12's the hour this check
    was written.
    """
    with open(README) as f:
        for line in f:
            m = re.match(r'^- `ANSWERED` \*\*What Run \d+ was built to'
                         r' answer', line)
            if m:
                return m.group(0)
    raise AssertionError('no ANSWERED run registration in the README to'
                         ' plant against')


# Run 18's registration in miniature: items numbered INLINE, `(N) *label*`,
# each stated twice -- registering with its kill condition, adjudicating
# with a bolded verdict -- where Run 17's are numbered lines. Synthetic
# and planted BESIDE a live entry rather than doctored out of one: the
# live inline registration retires with its run, and these cases must
# not retire with it. The kill condition's `BROKE` stands outside any
# bolded span on purpose -- it is the word the span pairing must refuse.
# One LINE per paragraph too, not wrapped by this file's hand: the copy
# inherits the README's wrap gate, which fails a hand-wrapped paragraph
# and passes a wholly-unwrapped one as mid-edit.
INLINE_REG = ('- `%s` **What Run 99 was built to answer, registered'
              ' before it ran.** Two questions, each with what kills it:'
              ' (1) *the knob*, killed by a BROKE that clears the floor;'
              ' (2) *the dial*, likewise. THE VERDICTS, 2026-08-23.'
              ' (1) *The knob*: **HELD.** (2) *The dial*: %s\n\n')


def an_across_paragraph():
    """One class block's `Across the halves:` paragraph, wrapped form.

    Named dynamically like a_registration_lead above: its figures are
    reinstalled with every run, so a pinned copy dies at the next
    install.
    """
    for p in open(README).read().split('\n\n'):
        if p.lstrip().lstrip('*').startswith('Across the halves:'):
            return p
    raise AssertionError('no `Across the halves:` paragraph in the README'
                         ' to delete')


def deflation_leg_zero_slope(tag='runzzq', half='h'):
    """The rider set with one clean leg's time slope written zero.

    The slope is raw and criterion's own, so no roster state produces
    this; a doctored or truncated leg does, and the mode divides by it
    and logs the ratio. Rewritten after synth_run the way `doctored`
    rewrites, on the first shape's clean leg.
    """
    run = deflation_legs(tag=tag, half=half)
    leg = here_file('%s-al-%s-%s-r1.json' % (tag, half, main_shapes()[0]))
    d = json.load(open(leg))
    hit = 0
    for b in d[2]:
        for r in b['reportAnalysis']['anRegress']:
            if r.get('regResponder') == 'time':
                r['regCoeffs']['iters']['estPoint'] = 0.0
                hit += 1
    assert hit, 'no time fit in the leg to zero'
    with open(leg, 'w') as f:
        json.dump(d, f)
    return run


def class_pair_with_log(tmp, cls='rev', slow=1.0):
    """A class run, its other half, and the `.log` a process leaves.

    `--block --compare` is item 5 of the class-block form and
    `--chapter` reads the provenance line out of the log beside the JSON,
    so a fixture for either needs both files. `slow` scales the second
    half wholesale, which is what moves the BASELINE and so what the
    differencing threshold is about.
    """
    a = synth_run(os.path.join(tmp, 'a.json'), class_shapes(cls))
    b = synth_run(os.path.join(tmp, 'b.json'), class_shapes(cls), slow=slow)
    write(os.path.join(tmp, 'a.log'),
          '=== roster 47 benchmarks over 3 shapes; elapsed 0h12m14s;'
          ' peak 88 MiB in use, 19 MiB max residency\n')
    write(os.path.join(tmp, 'b.log'),
          '=== roster 47 benchmarks over 3 shapes; elapsed 0h12m15s;'
          ' peak 90 MiB in use, 20 MiB max residency\n')
    return a, b


def deflation_legs(tag='runzzd', half='h', n=3, clean=True, sat=True):
    """A run with BOTH rider sets beside it, clean and saturated.

    `--deflation` globs the legs out of the CWD rather than out of the
    run's directory, so these go in HERE and are swept with the rest.
    Run 18 takes each shape's `list` alone twice -- `SAT=` off and on --
    because its registration 3 is a decomposition and not one ratio: the
    state is the saturated leg over the clean one and the rest is the
    roster cell over the saturated one. Two legs a shape is what makes
    that readable, and one is what makes it a hand-rolled subtraction in
    a write-up.
    """
    shapes = main_shapes()[:n]
    run = here_file('%s-%s-main.json' % (tag, half))
    synth_run(run, shapes)
    for sh in shapes:
        if clean:
            synth_run(here_file('%s-al-%s-%s-r1.json' % (tag, half, sh)), [sh])
        if sat:
            synth_run(here_file('%s-al-%s-sat-%s-r1.json'
                                % (tag, half, sh)), [sh])
    return run


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


def null_bound(benches, want):
    """One cell's lower CI bound written null, as a starved fit leaves it."""
    hit = 0
    for b in benches:
        if b['reportName'] == want:
            for r in b['reportAnalysis']['anRegress']:
                if r.get('regResponder') == 'time':
                    r['regCoeffs']['iters']['estError']['confIntLDX'] = None
                    hit += 1
    assert hit == 1, '%s: %d time fit(s)' % (want, hit)
    return hit


def zero_ci(benches, arm=None):
    """CI bounds written zero -- an exact fit -- on one arm or on all.

    `arm` matches the bench name's arm half over EVERY shape, because
    `--ci` reads medians across shapes: one zeroed shape moves no
    median, so the case that wants a zero arm zeroes it everywhere.
    """
    hit = 0
    for b in benches:
        if arm is None or b['reportName'].endswith('/' + arm):
            for r in b['reportAnalysis']['anRegress']:
                if r.get('regResponder') == 'time':
                    e = r['regCoeffs']['iters']['estError']
                    e['confIntLDX'] = e['confIntUDX'] = 0.0
                    hit += 1
    assert hit, 'no time fit matched %r' % (arm,)
    return hit


def empty_corpus(tmp):
    """A directory with no run in it, for the properties to be aimed at."""
    d = os.path.join(tmp, 'corpus')
    os.mkdir(d)
    return {'corpus': d}


def corpus_of_one(tmp):
    """A directory holding one built main run and nothing else."""
    d = empty_corpus(tmp)['corpus']
    synth_json(d, 'main')
    return {'corpus': d}


FAKE_HALF = """\
#!/bin/sh
# A stand-in for `$PREFIX-$half`, answering the two questions a driver asks
# before it commits the machine: what benches are there, and what RTS line
# is baked in. It runs none.
if [ "$1" = --list ]; then
  for s in shape-a shape-b shape-c; do
    for a in list build mut-odo sum-only-early sum-only-late; do
      echo "$s/$a"
    done
  done
fi
if [ "$1" = +RTS ] && [ "$2" = --info ]; then
  echo ' ,("Flag -with-rtsopts", "-A32m -I0 -T -M8G")'
fi
exit 0
"""

# The same stand-in built without the baked line, which is what a half
# from before 2026-08-21, or from a recipe that dropped it, answers.
FAKE_HALF_UNBAKED = FAKE_HALF.replace(
    'if [ "$1" = +RTS ] && [ "$2" = --info ]; then\n'
    '  echo \' ,("Flag -with-rtsopts", "-A32m -I0 -T -M8G")\'\nfi\n', '')
assert 'with-rtsopts' not in FAKE_HALF_UNBAKED, 'the unbaked stand-in kept it'

# And one listing nothing, which is the other wrong binary.
FAKE_HALF_LISTLESS = FAKE_HALF.replace(
    'if [ "$1" = --list ]; then\n'
    '  for s in shape-a shape-b shape-c; do\n'
    '    for a in list build mut-odo sum-only-early sum-only-late; do\n'
    '      echo "$s/$a"\n    done\n  done\nfi\n', '')
assert 'shape-a' not in FAKE_HALF_LISTLESS, 'the listless stand-in kept it'

# A stand-in that RUNS: one `benchmarking` line per bench of the gate's own
# five-arm selection, for a driver that counts them against `--list`.
FAKE_AREA = """\
#!/bin/sh
for s in shape-a shape-b shape-c; do
  for a in list build mut-odo sum-only-early sum-only-late; do
    if [ "$1" = --list ]; then echo "$s/$a"; else echo "benchmarking $s/$a"; fi
  done
done
exit 0
"""

# Two planted files for the import-time family. The first carries what
# runs at import: a helper called at module scope, which parses at import
# as surely as a module-scope line does, and a parse in a class body. The
# second carries the forms that do not -- a parse under a `try`, a helper
# reached only from under a module-level `try`, from a lambda, or from the
# `__main__` block, and a nested def its parent merely returns.
ZZ_FAM_HELPER = """\
import os


def number(name, default):
    return int(os.environ.get(name) or default)


class Knobs:
    pad = int(os.environ.get('ZZ_PAD2') or 0)


PAD = number('ZZ_PAD', 0)
"""

ZZ_FAM_HANDLED = """\
import os
import sys


def number(name, default):
    try:
        return int(os.environ.get(name) or default)
    except ValueError:
        sys.exit('no')


def later(name):
    return int(os.environ.get(name) or 0)


try:
    PAD = number('ZZ_PAD', 0)
    PAD2 = later('ZZ_PAD2')
except ValueError:
    PAD = PAD2 = 0

f = lambda: later('ZZ_LAMBDA')


def outer():
    def inner(name):
        return int(os.environ.get(name) or 0)
    return inner


OUTER = outer()


def main():
    return later('ZZ_MAIN')


if __name__ == '__main__':
    main()
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


# Two stand-ins for `perf`, for the guard that says the counting machine
# is present before a sweep spends its hours proving otherwise. The
# machine's own perf is deliberately NOT used by either case:
# kernel.perf_event_paranoid is not persistent here -- 1, then 4, then 1
# again inside two days -- so a case leaning on it would pass or fail on
# the state the guard exists to catch.
PERF_BLOCKED = """\
#!/bin/sh
echo "Access to performance monitoring and observability operations is\
 limited." >&2
exit 255
"""

# `perf stat -x,` writes one CSV line per event, to the file `-o` names
# and to stderr when it names none -- and the guard probe passes no `-o`
# where `count()` does, so the stub has to honour both or it exercises
# only one of the two calls the script makes. It answers proportionally
# to `-n`, so the script's own 2N-minus-N differencing comes out exact.
PERF_ANSWERS = """\
#!/bin/sh
out=""; n=200000; want_o=0; want_n=0
for a in "$@"; do
  if [ "$want_o" = 1 ]; then out=$a; want_o=0; continue; fi
  if [ "$want_n" = 1 ]; then n=$((100000 * a)); want_n=0; continue; fi
  case $a in -o) want_o=1 ;; -n) want_n=1 ;; esac
done
line="$n,,instructions:u,257660,100.00,,"
if [ -n "$out" ]; then echo "$line" > "$out"; else echo "$line" >&2; fi
exit 0
"""


def stub_dir(tmp, body, name='perf'):
    """A directory holding one executable stand-in, for PATH.

    A shadow cannot carry this: `perf` is resolved off PATH and not out
    of the script's own directory, so the case prepends a directory
    instead of replacing a file.
    """
    d = os.path.join(tmp, 'stub')
    os.makedirs(d, exist_ok=True)
    os.chmod(write(os.path.join(d, name), body), 0o755)
    return d


# A log with samples on BOTH sides of the load fields, and a trailing
# `pre` with no `post`: the two branches of `--wild` that no run on disk
# exercises, one being an instrument change mid-log and the other what a
# killed process leaves. Written out rather than captured, a captured log
# being thousands of lines of which two matter.
WILD_MIXED = """\
@@wild a/b pre iters=1 alloc=1 mut=1 gc=0 gcs=1/0 inuse=1
@@wild a/b post iters=1 alloc=2 mut=3 gc=0 gcs=1/0 inuse=1
@@wild a/b pre iters=1 alloc=3 mut=4 gc=0 gcs=1/0 inuse=1 load=0.1 run=1 cpu=100
@@wild a/b post iters=1 alloc=4 mut=6 gc=0 gcs=1/0 inuse=1 load=0.1 run=1 cpu=200
@@wild a/c pre iters=1 alloc=1 mut=1 gc=0 gcs=1/0 inuse=1 load=0.1 run=1 cpu=100
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


def run_order_shapes(cls):
    """One class's shapes in the order they RUN, not sorted.

    `class_shapes` sorts, which is right for every fixture that only wants
    a population and wrong for the three lead cases: the block's lead
    lists its shapes in run order, the per-shape line under it is
    installed in run order and labelled as the lead's, and a sorted
    fixture makes those two disagree for a reason no defect caused. The
    order is Main.hs's own -- `dims_by_shape` yields the lists as it read
    them -- which is what criterion then emits.
    """
    dims, _ = _reader().dims_by_shape(os.path.join(HERE, 'Main.hs'))
    return [sh for sh in dims if sh.startswith(cls + '-')]


def lead_of(cls):
    """A class block's bolded lead paragraph, the whole of it.

    Found by the pattern `install-tables.sh` and `lead_shapes` both use,
    and asserted unique here so a fixture built on it cannot silently
    edit the wrong paragraph.
    """
    hit = [p for p in open(README).read().split('\n\n')
           if p.lstrip().startswith('**`%s` ---' % cls)]
    assert len(hit) == 1, 'lead `%s`: %d paragraph(s)' % (cls, len(hit))
    return hit[0]


def relead(tmp, cls, rewrite, name='R.md'):
    """A copy of the README with one class lead rewritten by `rewrite`.

    The lead is handed over UNWRAPPED, one line, because `lead_shapes`
    normalises whitespace before it reads and a plant that had to
    reproduce the wrap would be testing the wrapper. What comes back is
    written as the paragraph, and `edited_readme` asserts it replaced
    exactly one.
    """
    old = lead_of(cls)
    new = rewrite(' '.join(old.split()))
    assert new != ' '.join(old.split()), 'the rewrite changed nothing'
    return edited_readme(tmp, (old, new), name=name)


LAST = object()   # `task_anchor(LAST)`: the list's last item, whatever
                  # its number. A spent task leaves the subsection and
                  # the rest renumber, so a case naming task 3 stops
                  # building the day one goes -- which it did.


def task_anchor(n):
    """The opening of task `n` of `Recommended tasks after Run N`.

    DERIVED, because the two `--replace` cases below stored it: they
    quoted `1. **WHICH SHAPES POISON` and `3. **Between Run 17 and Run
    18` as literals and both broke the day those items took status
    tokens, which is a stored anchor into live prose and the one thing
    the opening of this file forbids a fixture. What they are about is
    the list's SHAPE -- that `--replace`'s unit is a paragraph and a list
    with no blank lines is one -- so the item's own words were never the
    subject.

    Uniqueness is asserted here rather than left to `--replace`, whose
    refusal for a repeated anchor reads the same as its refusal for a
    missing one.
    """
    lines = readme_lines()
    i = next(k for k, l in enumerate(lines)
             if l.startswith('### Recommended tasks after Run '))
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith('### '))
    if n is LAST:
        n = max(int(re.match(r'^(\d+)\. ', l).group(1))
                for l in lines[i:j] if re.match(r'^\d+\. ', l))
    hit = [l for l in lines[i:j] if re.match(r'^%d\. ' % n, l)]
    assert len(hit) == 1, 'task %d: %d line(s)' % (n, len(hit))
    anchor = ' '.join(hit[0].split())[:44]
    doc = '\n'.join(lines)
    assert doc.count(anchor) == 1, ('task %d anchor %r occurs %d times'
                                    % (n, anchor, doc.count(anchor)))
    return anchor


def open_list_span(lines):
    """(first, last) line indices of the open list, found its own way.

    The same two headings `check_doc` delimits the section with, so a
    fixture cannot be built against a range the check does not read.
    """
    lo = next(i for i, l in enumerate(lines) if l.startswith('## What is open'))
    hi = next(i for i, l in enumerate(lines) if l.startswith('## The goal'))
    assert lo < hi, 'the open list runs from %d to %d' % (lo, hi)
    return lo, hi


def readme_entry_without_status(tmp):
    """A copy carrying an open-list entry that opens with no status.

    ADDED and not stripped, which the first draft did and which is the
    trap worth recording: taking the token off an existing entry
    shortens that line and leaves its paragraph half-wrapped, so the
    copy then failed the WRAP gate as well -- exit 1 for a reason this
    case is not about, and the case was passing on it. A fresh entry on
    one long line is what any edit leaves, and the wrap pass reports
    that as mid-edit rather than failing it.
    """
    lines = readme_lines()
    lo, hi = open_list_span(lines)
    i = next(k for k in range(lo, hi) if lines[k].startswith('- `'))
    entry = ('- **zz-planted-tokenless, an entry written without its'
             ' status.** It says nothing about the run and is here to be'
             ' classified by a grep that cannot classify it.')
    return edited_readme(tmp, (lines[i], entry + '\n' + lines[i]))


def readme_open_list_reshaped(tmp):
    """A copy whose open-list entries are all indented out of sight.

    The vacuity control: a section reshaped so the check's pattern finds
    nothing must FAIL as unlocatable rather than pass over an empty list,
    which is the shape this suite refuses everywhere else.

    BOTH ENTRY FORMS, and the second is why this is worth a comment. The
    fixture indented `- ` lines alone while the check counted those
    alone, and the two were widened to numbered items a commit apart:
    the day the check learned to count `Recommended tasks after Run N`'s
    three, this fixture went on leaving them behind, so the list it
    handed over was not empty and the branch under test never ran. A
    fixture and the check it aims at have to be widened together.
    """
    lines = readme_lines()
    lo, hi = open_list_span(lines)
    out = list(lines)
    hit = 0
    for k in range(lo, hi):
        if re.match(r'^(?:- |\d+\. )', out[k]):
            out[k] = '  ' + out[k]
            hit += 1
    assert hit, 'no top-level entry to indent'
    return write(os.path.join(tmp, 'R.md'), '\n'.join(out))


def readme_answered_account(tmp, lead=None, tail=''):
    """An ANSWERED entry over the sweep's threshold, planted in the list.

    BUILT rather than borrowed. The live list's own long entries are the
    backlog the rule was written over, so a case keyed on one of those
    would pass on the backlog and say nothing about the sweep -- and
    would go quiet the day that entry is shortened, which is the outcome
    the rule is for.

    The filler is deliberately free of figures, superlatives, absolute
    times and prospective verbs: `check_doc`'s other sweeps run over the
    same copy, and a fixture that tripped one of them would be judged on
    the wrong line. The entry has to clear the word count and nothing
    else: the pointer clause the sweep once carried is gone, length
    being the whole test, and the filler is sized off the threshold
    rather than off a number written here twice.
    """
    lines = readme_lines()
    i = next(k for k, l in enumerate(lines) if l.startswith('- `ANSWERED`'))
    reader = _reader()
    n = reader.ANSWERED_ACCOUNT // 10 + 10        # 11 words a repetition
    filler = 'This entry is a fixture and says nothing about the run. ' * n
    lead = lead or '**zz-planted-account, an answer grown into an account.**'
    # The marker rides in the BODY as well as in the default lead, since
    # the registration variants replace the lead and still have to be
    # identifiable in what the checker prints.
    entry = ('- `ANSWERED` ' + lead + ' On zz-planted-account. '
             + filler.strip() + tail)
    return edited_readme(tmp, (lines[i], entry + '\n' + lines[i]))


CLASS_SECTION = '### The stride classes, run by run'


def floor_movement_para(bend=None, joiner=' to '):
    """A floor-movement paragraph BUILT from the class table's own column.

    Constructed and not found: the README carried such a paragraph until
    2026-08-22 and carries none now -- a run owes one only when its
    halves can be read against the previous run's -- so a fixture that
    edited the live one could be built on one document and not on the
    next. The figures come off the table the check reads, so the
    paragraph is right by construction and `bend` is the only thing
    wrong with it.

    `bend` moves one class's landing figure off the column; `joiner`
    rewrites the shape the check matches on. One each is what the two
    cases want.
    """
    rows = re.findall(r'^\| `([a-z0-9]+)` \|.*\| ([\d.]+)% \|$',
                      open(README).read(), re.M)
    assert len(rows) >= 4, 'class table floor column: %d row(s)' % len(rows)
    said = []
    for i, (cls, now) in enumerate(rows):
        if bend is not None and i == bend:
            now = now + '9'
        said.append('`%s` 1.11%%%s%s%%' % (cls, joiner, now))
    return ('**The floor column can be read against its predecessor\'s.**'
            ' All of them moved: ' + ', '.join(said) + '.')


def readme_with_floor_movement(tmp, **kw):
    """A copy carrying that paragraph, under the class section's heading.

    Placed right under the heading so it is inside the section the check
    reads and outside every class block, which is where the real one
    stood.
    """
    return edited_readme(tmp, (CLASS_SECTION + '\n',
                               CLASS_SECTION + '\n\n'
                               + floor_movement_para(**kw) + '\n'))


def readme_floor_movement_off_column(tmp):
    """One movement landing off the column, the rest right."""
    return readme_with_floor_movement(tmp, bend=0)


def readme_floor_movement_reshaped(tmp):
    """Every figure right and the shape the check matches on rewritten.

    What must not happen is a silent pass: keying the vacuity guard on
    the sentence's opening phrase was the first attempt, and rewording
    that phrase turned the whole check off.
    """
    return readme_with_floor_movement(tmp, joiner=' -> ')


def _scale_arm(benches, arm, factor):
    """Every bench of one ARM, across the shapes, scaled together.

    `scale` above takes a whole `shape/arm` report name, which is one
    cell; a floor is a pair over the whole population, so widening one
    wants all of its cells at once.
    """
    hit = 0
    for b in list(benches):
        if b['reportName'].split('/')[-1] == arm:
            hit += scale(benches, b['reportName'], factor)
    assert hit, 'no bench of arm %s' % arm
    return hit


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
    # Both deviations POSITIVE, as criterion writes them: `-d` here made
    # the reader's CI% -- their mean over the slope -- exactly 0 in every
    # synthetic cell, and the noise column nan off it, so no case could
    # assert either. Case: `fixture-ci-bounds-are-criterion-shaped`.
    d = abs(point) * rel
    return {'estPoint': point,
            'estError': {'confIntCL': 0.95, 'confIntLDX': d, 'confIntUDX': d}}


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


def synth_run(path, shapes, samples=8, no_twins=False, sunk=(), skew=(),
              slow=1.0, drop_arms=(), fingerprint=None):
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

    `drop_arms` leaves named arms out of the run entirely, which is how
    a run WITHOUT `list` is built -- the shape a filtered probe has, and
    the one that made `--bridge` raise a KeyError instead of refusing.

    `slow` scales EVERY cell of the run by one factor, which is what a box
    change looks like from inside: Run 18's BIOS moved between it and Run
    17 and lifted every absolute about 4.9%, leaving every ratio alone.
    That is the one shape `skew` cannot make, being per cell, and it is
    what the bridge exists to divide out.

    `skew` scales named (shape, arm, factor) cells, which is how a `Term`
    half is made to disagree with its twin on one shape: the exact halves
    read 0.00% as a pair, and a case about WHICH pair's cell gets printed
    needs that one wider than every A/A cell.
    """
    m = _reader()
    main_hs = os.path.join(HERE, 'Main.hs')
    dims, _ = m.dims_by_shape(main_hs)
    roster = m.roster_of(open(main_hs).read())
    timed = [(n, role, fn) for n, role, fn in roster
             if role != 'Only' and n not in drop_arms]
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
    reports, fp_net = [], {}
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
            # EVERY cell, `Term` halves included: a box that got slower
            # slowed the forcing pass too, which is exactly why dividing
            # by `list` cancels it and subtracting the correction does
            # not.
            # Captured BEFORE `slow` and `skew`, which is what makes a
            # written fingerprint exact: `slow` scales the `Term` halves
            # too, so net scales with it, and a run built at `slow=f`
            # against this fingerprint reads f on every shape. Against
            # THIS README's fingerprint a synthetic run reads -95%, its
            # absolutes being nowhere near the real ones, and no `slow` is
            # visible through that -- which is why the level-shift branch
            # could not be cased until this existed.
            if name == 'list':
                fp_net[sh] = slope - TERM * l
            slope *= slow
            if (sh, name) in sunk:
                slope = TERM * l * 0.5      # below the term: net goes negative
            for s_sh, s_name, factor in skew:
                if (sh, name) == (s_sh, s_name):
                    slope *= factor
            alloc = 0.0 if role == 'Term' else 8.0 * l * _spread(fn, 0.9, 1.4)
            reports.append(_synth_report('%s/%s' % (sh, name), slope, alloc,
                                         samples))
    with open(path, 'w') as f:
        f.write(json.dumps(['criterion', '1.6.5.0', reports]))
    if fingerprint:
        # A README carrying nothing but the fingerprint table, in the four
        # columns FINGERPRINT_ABS_RE reads, at more precision than the real
        # one prints -- three significant figures is half a percent a cell,
        # which is most of the band a level-shift case has to resolve. The
        # header row carries no backticks, so it is not itself a row.
        with open(fingerprint, 'w') as f:
            f.write('| shape | . | . | `list` net |\n|---|---|---|---:|\n')
            for sh in shapes:
                f.write('| `%s` | . | . | %.9f us |\n' % (sh,
                                                          fp_net[sh] * 1e6))
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
                  into=None, plateau=None, skew=()):
    """A whole run in this directory: JSONs, and the log that describes it.

    `read-all.sh` cds to its own directory and globs, so this is one of the
    two fixtures that cannot live in a temp directory.

    `into` names that directory when the case runs a SHADOW. `shadow_dir`
    symlinks this one BEFORE a plant runs, so a file written here
    afterwards is not in the shadow, and a driver globbing its own
    directory finds nothing at all -- which reads as a fixture that would
    not build rather than as the state the case wanted. Pointed at the
    shadow, the run lands where the driver will look.

    `plateau` is a list of victim readings, one per process, written into
    the per-process logs as the preamble's `@@saturate` line -- the only
    thing in this fixture that is a LOG and not a JSON, `read-all.sh`'s
    plateau gate being the only one of its gates read off a log. A rider
    and a gate log get one too, both at absurd readings, so that a gate
    counting them would say so rather than pass with a wider band. A
    reading of `None` is a process that asserted nothing: its log is
    there, as every process's is, and carries no such line; a list is
    several lines in one log, which no process writes.

    `skew` is `synth_run`'s, applied to both class runs.
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
        synth_run(dst, class_shapes(cls), no_twins=no_twins, skew=skew)
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
    if plateau is not None:
        sat = ('@@saturate dose=1x by=list sprayed=1000000 in 6.0 s; victim'
               ' vgg-14-c512-k3/list %s ms/iter over 20; inuse=1 keep=1')
        for cls, ms in zip(('rev', 'slice'), plateau):
            # A list is several lines in one log, which no process writes
            # and a count of lines against logs cannot tell from one each.
            lines = ([] if ms is None else ms if isinstance(ms, list)
                     else [ms])
            write(place('%s-lookrts-%s.log' % (tag, cls)),
                  'benchmarking x/y\n'
                  + ''.join(sat % m + '\n' for m in lines))
        # A rider's and a gate half's, at readings no band could hold: both
        # are excluded by name, so a gate that counted either would fail
        # loudly here instead of passing over a wider set.
        for other in ('al-lookrts-cnn-slice-c32-r1', 'gate-lookrts-a'):
            write(place('%s-%s.log' % (tag, other)), sat % '999.0' + '\n')
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

    case('buried-action-at-eof', 'read-run.py', None,
         'the last indented block of a document was never swept',
         plant=lambda t: {'readme': readme_with_trailing_buried_action(t)},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         # No --audit: `--worklists` is younger than the fix, so the code
         # before it rejects the argv as an unknown flag, which is no
         # reproduction of anything. Removal is the handling.
         ok=V(has=['--survey to see it'])),

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

    case('deflation-ignores-the-saturated-legs', 'read-run.py', '9b45089',
         'both rider sets on disk and only the clean one read',
         # THE GLOB TAKES BOTH AND THE MODE USED ONE. `$R-al-<half>-*`
         # matches `$R-al-<half>-sat-<shape>` as readily as the clean leg,
         # and the saturated ones came back keyed `sat-<shape>`, which
         # matches no shape of the run and was dropped without a word --
         # so a run that paid for two rider sets got one column, and the
         # decomposition its registration was written for had to be
         # subtracted by hand in the write-up. That is the shape this
         # README calls a defect report against the reader rather than a
         # script to keep: Run 18 registered the state and the rest as
         # separate quantities, and the mode that reads the total is the
         # mode that owes them.
         #
         # The silent half is what makes it worth a case. A missing leg is
         # reported -- `missing` names it -- while a leg the glob took and
         # the keying discarded looked exactly like a leg that was never
         # taken, and the geomean printed over the clean ones was correct,
         # which is why nothing downstream could notice.
         # It was a CONTROL while the fix sat uncommitted, and non-vacuity
         # was shown by hand then (2026-08-23): with the `sat-` split
         # removed from `deflation_table`, so that the saturated legs key
         # as `sat-<shape>` and match nothing again, it FAILS on both
         # strings. It has its hash and its `bug` verdict now, so --audit
         # replays that by itself and the hand proof is only the record.
         plant=lambda t: {'run': deflation_legs()},
         argv=['{run}', '--deflation'],
         ok=V(has=['sat/clean', 'roster/sat']),
         bug=V(hasnt=['sat/clean'])),

    case('broke-names-the-manifest', 'read-run.py', None,
         'a retirement made in prose left the manifest predicting the old',
         # THE MANIFEST IS THE OTHER HALF OF A RETIREMENT. Run 17's chapter
         # retired claim 4's tie in prose -- *the next run inherits an
         # ordering rather than re-reading a tie* -- and CLAIMS went on
         # registering the tie for a day, so Run 18 would have broken it a
         # third time and a session rediscovered a decision already taken.
         # The rewrite obligation was stated and was the half that got
         # done; this names the half that did not, at the moment a BROKE
         # is read and the decision is being made.
         #
         # The silent branch has no case, a synthetic population breaking
         # eleven of thirteen and no cheap filter leaving none: measured
         # instead on run17-det, 13 of 13 held and the paragraph absent.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--claims'],
         ok=V(has=['`CLAIMS` in this script is where that lands'])),

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
         bug=V(exit=0, has=['chapter skeleton'],
               hasnt=['shapes in one run only, skipped'])),

    case('block-writes-the-cross-half-line', 'read-run.py', None,
         "item 5 of the class-block form left to be written by hand",
         # The form's item 5 is "how many of the population's arms move,
         # which way, and the spread" -- mechanical to the word, and
         # written by hand eight times a run until this. --block took one
         # class JSON and had no way to see the other half, so it could
         # not write the one part of the form that is about the pair.
         plant=lambda t: dict(zip(('run', 'other'),
                                  class_pair_with_log(t))),
         argv=['{run}', '--block', '--compare', '{other}', '--brief'],
         ok=V(has=['**Across the halves:**', 'with `list` itself at'])),

    case('block-flags-a-baseline-past-differencing', 'read-run.py', None,
         'a class whose halves cannot be differenced said so nowhere',
         # THE READING THAT DISQUALIFIES ITSELF. Two columns may be
         # subtracted only while `list` holds still between them -- 0.7%
         # is this README's figure -- and on Run 18 four of the eight
         # classes moved past it, because the machine got busy partway
         # through and the halves of those four straddled the boundary.
         # Nothing said so: the elapsed times spanned seven seconds, the
         # A/A floors were no looser than the clean ones, and it took a
         # hand comparison of `list` across each pair to find. A mode
         # that writes the cross-half line is the mode that owes the
         # warning, so the fixture moves the baseline and asks for it.
         plant=lambda t: dict(zip(('run', 'other'),
                                  class_pair_with_log(t, slow=1.05))),
         argv=['{run}', '--block', '--compare', '{other}', '--brief'],
         ok=V(has=['past the 0.7%', 'NOT read for the pair'])),

    case('chapter-reads-the-logs-it-said-it-could-not', 'read-run.py', None,
         'a chapter asked for figures its own process had already stamped',
         # It printed `elapsed, heap peaks, wall-clock window: ___ (from
         # the pair note and the logs -- this mode reads neither)`, and
         # Run 18 copied eighteen such triples by hand. The logs are
         # beside the JSONs and the driver stamps the window; only the
         # regime, the md5s and the commit are the note's, and those are
         # what the placeholder is now for.
         plant=lambda t: dict(zip(('run', 'other'),
                                  class_pair_with_log(t))),
         argv=['{run}', '--compare', '{other}', '--chapter'],
         ok=V(has=['elapsed 0h12m14s', 'elapsed 0h12m15s'],
              hasnt=['heap peaks, wall-clock window: ___'])),

    case('registration-open-with-every-verdict-in', 'read-run.py', None,
         'a registration marked OPEN whose every question was answered',
         # Run 12's registered four questions, one of them "as a gap
         # rather than a question", and item 3 records in its own body
         # that the debt was PAID on 2026-08-13 -- while the entry's
         # status stayed `OPEN` and its lead went on saying `one still a
         # gap`. Six runs walked the open list past it, and the retirement
         # of spent registrations then skipped it BECAUSE of the marker,
         # which is the second cost: a stale status does not merely
         # mislead, it exempts.
         #
         # The family always ends ANSWERED, so the sound form of the
         # check is: an OPEN one all of whose numbered items carry a
         # verdict is a marker nobody updated. The fixture takes whatever
         # ANSWERED registration the README still carries and puts the
         # bad marker on it -- named dynamically because registrations
         # RETIRE, and a fixture pinned to Run 12's died the hour this
         # check retired Run 12's.
         #
         # THE FIRST DRAFT OF THE PATTERN MISSED IT, and that is why the
         # pattern is keyed on the verdict WORD and not on capitalisation:
         # three of Run 12's four items shout (`ANSWERED:`, `REFUTED,`,
         # `THE RUN IS CLEAN`) and the fourth does not (`the debt is
         # PAID`), so an all-caps rule passed the one case it existed for.
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(),
             a_registration_lead().replace('`ANSWERED`', '`OPEN`', 1)))},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1, has=["registration is marked OPEN"])),

    case('registration-answered-is-not-flagged', 'read-run.py', None,
         'CONTROL: the same entry, correctly marked, says nothing',
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(), a_registration_lead()))},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=0, hasnt=['registration is marked OPEN'])),

    case('registration-inline-items-are-read', 'read-run.py', None,
         "a stale OPEN marker over inline `(N)` items, Run 18's form",
         # The check's first draft knew only the line form `  5. `,
         # parsed Run 18's registration -- inline items, stated twice in
         # one paragraph -- to zero items and held its marker to
         # nothing: the very registration the README's verdict paragraph
         # cites, and its verdicts used two words (BROKEN, FAILED) the
         # vocabulary did not hold. A control until the fix has a hash;
         # non-vacuous by removal the day it was written -- with the
         # inline alternative cut from the item pattern, this reads
         # `exit 0` on the silent skip itself, and the two cases above
         # stay green, which is why they could not have caught it.
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(),
             INLINE_REG % ('OPEN', '**BROKEN, and narrowly.**')
             + a_registration_lead()))},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1, has=["Run 99's registration is marked OPEN"])),

    case('registration-inline-unadjudicated-item-is-named', 'read-run.py',
         None,
         'an ANSWERED marker over an inline item with no verdict',
         # The other arm on the same form, and the discriminator with
         # it: item 1's kill condition says `BROKE` outside any bolded
         # span and its verdict span says `HELD`, so only item 2 -- a
         # dial still out with the jury -- may be named.
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(),
             INLINE_REG % ('ANSWERED', 'still out with the jury.')
             + a_registration_lead()))},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1,
              has=["Run 99's registration is ANSWERED and item(s) 2"])),

    case('registration-inline-answered-is-not-flagged', 'read-run.py',
         None,
         'CONTROL: the same inline entry, correctly marked, says nothing',
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(),
             INLINE_REG % ('ANSWERED', '**BROKEN, and narrowly.**')
             + a_registration_lead()))},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=0, hasnt=["Run 99's registration"])),

    case('bridge-refuses-a-run-without-list', 'read-run.py', None,
         'the mode that divides by `list` met a run that has none',
         # A filtered probe is the ordinary way to have one, and this
         # raised a bare KeyError three frames down rather than refusing.
         # Found 2026-08-23 by trying to break the mode rather than by
         # reading it, which is how five of its six siblings were found.
         # A control until the fix has a hash, and non-vacuous by
         # removal the same day: with the guard cut, this reads `exit 1,
         # wanted 2` on the KeyError's own traceback.
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json',
                                            drop_arms=('list',)),
                          'other': synth_json(t, 'main', 'b.json')},
         argv=['{run}', '--compare', '{other}', '--bridge'],
         ok=V(exit=2, has=['nothing to divide by'])),

    case('bridge-refuses-two-populations', 'read-run.py', None,
         'a bridge taken between a class run and the main set',
         # The mode's OWN empty-overlap guard is unreachable and says so
         # in the source: two runs of one population share their shapes
         # by construction, and two of different ones are stopped by the
         # population check before the guard is reached. What IS
         # reachable is that check, and this pins it for --bridge, the
         # newest caller of `load_other` and the one whose figures would
         # otherwise be a geomean over nothing.
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json'),
                          'other': synth_json(t, 'rev', 'b.json')},
         argv=['{run}', '--compare', '{other}', '--bridge'],
         ok=V(exit=1, has=['different populations'])),

    case('block-refuses-a-second-mode', 'read-run.py', None,
         'the one-mode guard, relaxed for --compare, let a mode through',
         # --block takes --compare as a sub-flag, and relaxing the guard
         # for it put back exactly what the guard exists to stop:
         # `--block --compare X --chapter` ran the block and dropped
         # --chapter without a word, --chapter not itself being in
         # `modes`. The relaxation has to name what it still refuses.
         # Non-vacuous by removal, 2026-08-23: with the clash check cut
         # the case reads `exit 0, wanted 2`, which is the silent drop
         # itself.
         plant=lambda t: {'run': synth_json(t, 'rev', 'a.json'),
                          'other': synth_json(t, 'rev', 'b.json')},
         argv=['{run}', '--block', '--compare', '{other}', '--chapter'],
         ok=V(exit=2, has=['--block takes --compare and nothing else'])),

    case('compare-refuses-a-second-reading', 'read-run.py', None,
         'two --compare sub-flags at once, the second dropped in silence',
         # `--compare X --alloc --ci` ran --alloc and dropped --ci
         # without a word, the dispatch being an if/elif chain: the same
         # drop the one-mode guard refuses one level up and the --block
         # clash check one level down, while the pairwise guards that
         # stood here covered every sub-flag pair but --ci's. A control
         # until the fix has a hash; non-vacuous by removal the day it
         # was written -- with the guard cut this reads `exit 0, wanted
         # 2` over an --alloc table that never mentions CI%.
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json'),
                          'other': synth_json(t, 'main', 'b.json')},
         argv=['{run}', '--compare', '{other}', '--alloc', '--ci'],
         ok=V(exit=2, has=['readings of --compare, not one'])),

    case('ci-drops-a-zero-arm-from-the-geomean', 'read-run.py', None,
         "a zero CI% in THIS run took --ci down with a ValueError",
         # a6067af guarded the geomean against an all-zero OTHER run; the
         # mirror -- an arm of this run at zero, ratio 0, log(0) -- was
         # found 2026-08-23 by flipping that state's two files, and it
         # crashed three frames down where the sibling had been refused.
         # A control until the fix has a hash.
         plant=lambda t: {'run': doctored(t, 'main', lambda b: zero_ci(
                              b, 'build'), 'a.json'),
                          'other': synth_json(t, 'main', 'b.json')},
         argv=['{run}', '--compare', '{other}', '--ci'],
         ok=V(exit=0, has=['out of the geomean', 'wider here'],
              hasnt=['Traceback'])),

    case('ci-says-when-no-ratio-exists', 'read-run.py', None,
         'every arm zero on a side, and the geomean owed a refusal',
         # The whole run zeroed on this side leaves nothing to take a
         # ratio of, which is the state a6067af met in the other run's
         # direction and this fix widened to both.
         plant=lambda t: {'run': doctored(t, 'main', zero_ci, 'a.json'),
                          'other': synth_json(t, 'main', 'b.json')},
         argv=['{run}', '--compare', '{other}', '--ci'],
         ok=V(exit=0, has=['no arm has a non-zero CI% on both sides'],
              hasnt=['Traceback', 'wider here'])),

    case('deflation-names-which-leg-set-is-missing', 'read-run.py', None,
         'saturated legs on disk, told the riders were never taken',
         # An interrupted rider evening leaves exactly this: the `SAT=`
         # invocations ran and the plain ones did not. The old wording
         # said the riders were not taken, which the directory disproves.
         # A control until the fix has a hash: non-vacuity was shown by
         # hand (2026-08-23), the pre-fix wording answering `the riders
         # were not taken` over a directory holding three saturated legs.
         plant=lambda t: {'run': deflation_legs(clean=False)},
         argv=['{run}', '--deflation'],
         ok=V(exit=2, has=['and no CLEAN one'],
              hasnt=['the riders were not taken'])),

    case('deflation-skips-a-leg-with-no-positive-slope', 'read-run.py',
         None,
         'a zeroed leg slope took the decomposition down bare',
         # The mode divides this run's `list` slope by the leg's and
         # logs the ratio, so a leg at zero was a ZeroDivisionError
         # three frames deep -- the zero-CI% family of --ci, on the
         # deflation's own inputs. The slope is criterion's own and no
         # roster state reaches it; a doctored or truncated leg does.
         # A control until the fix has a hash; non-vacuous by removal
         # the day it was written -- with the intake guard cut, this
         # reads the traceback itself.
         plant=lambda t: {'run': deflation_leg_zero_slope()},
         argv=['{run}', '--deflation'],
         ok=V(exit=0, has=['not positive', 'have NO alone leg'],
              hasnt=['Traceback'])),

    case('install-says-it-skipped-the-cross-half-line',
         'install-tables.sh', None,
         'a cross-half line left standing under this run, in silence',
         # An absent other-half JSON is correct for a run that recorded
         # one half and is a WRONG `OTHER` otherwise, and the two look
         # identical -- so the skip has to say which it might be, or the
         # previous run's cross-half line stays under this run's tables.
         plant=lambda t: {'doc': edited_readme(t)},
         shadow=dict(extra=whole_run(['lookrts'], prefix='zzxh')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'nosuchhalf'},
         argv=['zzxh'],
         ok=V(exit=0, has=['no cross-half line is installed'])),

    case('install-refuses-a-block-without-item-5', 'install-tables.sh',
         None,
         'a block with no item-5 slot, and the owed cross-half line'
         ' dropped in silence',
         # With the other half on disk the line is owed and --block emits
         # it, but a block pasted from the pre-item-5 form has no
         # paragraph to fill: the fill loop matched nothing and moved on,
         # between the ADDED branch that repairs a missing per-shape line
         # and the note that names a skipped line. A control until the
         # fix has a hash.
         plant=lambda t: {'doc': edited_readme(t, (
             '\n\n' + an_across_paragraph(), ''))},
         shadow=dict(extra=whole_run(['lookrts', 'ovhalf'],
                                     prefix='zzx5')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzx5'],
         ok=V(exit=1, has=['REFUSED', 'no `Across the halves:`'])),

    case('chapter-head-carries-a-previous-run', 'read-run.py', None,
         "paragraphs of the last run's chapter left standing in this one",
         # THE CHAPTER HEAD IS REPLACED WHOLE and its own closing
         # paragraph says so, but a write-up is done a paragraph at a
         # time and nothing enumerated them. Run 18 left FOUR of Run 17's
         # standing inside it -- the correction paragraph, the fill
         # groups, the process window and the alone legs -- one of them
         # contradicting two paragraphs the same session had just
         # written. An independent checker found them by set-differencing
         # the document, which is this script's job and one comparison.
         #
         # The fixture renumbers the chapter heading and changes nothing
         # else, so every paragraph under it is verbatim the committed
         # run's while the heading claims a new one -- which is precisely
         # the state a write-up that renamed its headings and stopped is
         # in. Measured 2026-08-23: it names 15 paragraphs.
         #
         # A CONTROL, the check being new. Its non-vacuity is that the
         # unmodified document passes the same call, the two differing
         # only in the run number, so a check that reported regardless
         # would fail the control beside it.
         plant=lambda t: {'readme': edited_readme(t, (
             '## About the last run (Run 18)',
             '## About the last run (Run 19)'))},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1, has=['chapter head are unchanged from Run'])),

    case('chapter-head-committed-says-nothing', 'read-run.py', None,
         'CONTROL: a chapter already committed has no previous run to hold',
         plant=lambda t: {'readme': edited_readme(t, (
             '## About the last run (Run 18)',
             '## About the last run (Run 18)'))},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(hasnt=['chapter head are unchanged from Run'])),

    case('bridge-divides-out-the-baseline', 'read-run.py', None,
         'a cross-run comparison a moved box made unreadable',
         # --compare divides one arm's net by the same arm's net in the
         # other run, which is right while the machine holds still and
         # useless the moment it does not. Run 18 met that: a BIOS idle
         # setting moved between it and Run 17 and took every absolute
         # about 4.9% with it, so --compare put `list` at +5.52% and every
         # arm with it, and the bridge that run's registration 1 was
         # written on had to be computed by hand -- which this README
         # calls a defect report against the reader.
         #
         # The fixture is the disease: `b.json` is `a.json` slowed by a
         # flat factor on EVERY arm and shape, which is what a box change
         # looks like. --compare must then read that factor on every arm,
         # and --bridge must read 1, the factor cancelling per shape.
         #
         # A CONTROL rather than a replay, the mode being new and having
         # no pre-fix revision to audit against. Non-vacuity MEASURED
         # 2026-08-23 on this fixture: --compare reads 0.9524, which is
         # 1/1.05, on every arm INCLUDING `list`, while --bridge reads
         # 1.0000 on every one of the 41 and a geomean of 1.0000 with
         # none outside the band. So the two modes disagree exactly by
         # the planted factor, and a --bridge that forgot to divide by
         # `list` would read 0.9524 here and fail.
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json'),
                          'other': synth_json(t, 'main', 'b.json',
                                              slow=1.05)},
         argv=['{run}', '--compare', '{other}', '--bridge'],
         ok=V(has=['ratio to `list` in its own'],
              hasnt=['outside the 3.3% drift band\n  '])),

    case('compare-ci-reads-the-published-median', 'read-run.py', None,
         'a question about the CI% column answered in the wrong statistic',
         # Run 18 asked what a saturating preamble does to `CI%`,
         # computed the MEAN over --cells because the reader had no mode,
         # and got the opposite sign on two arms of three: `build` reads
         # 1.58 to 1.84 as means and 1.55 to 1.42 as medians, and the
         # column publishes the median. The statistic a column is asked
         # about has to be the statistic it publishes.
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json'),
                          'other': synth_json(t, 'main', 'b.json')},
         argv=['{run}', '--compare', '{other}', '--ci'],
         ok=V(has=['MEDIAN half-width'])),

    case('bridge-wants-a-second-run', 'read-run.py', None,
         'CONTROL: --bridge and --ci are readings ACROSS two runs',
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json')},
         argv=['{run}', '--bridge'],
         ok=V(exit=2, has=['ACROSS two runs'])),

    case('alloc-names-the-shapes-it-dropped', 'read-run.py', 'a78555e',
         'the allocation comparison named its arms and not its shapes',
         plant=lambda t: {'run': synth_json(t, 'main', 'a.json'),
                          'other': synth_run(os.path.join(t, 'b.json'),
                                             main_shapes()[:-1])},
         argv=['{run}', '--compare', '{other}', '--alloc'],
         ok=V(has=['shapes in one run only, skipped']),
         bug=V(exit=0, has=['agree to 1e-4'],
               hasnt=['shapes in one run only, skipped'])),

    # ---- the sunk cell, which only a built fixture can carry -----------
    case('selftest-survives-a-sunk-baseline', 'read-run.py', '50efffe',
         'a baseline net of exactly 0 divided before the guard could look',
         plant=lambda t: {'run': sunk_shape_json(t)},
         argv=['{run}', '--selftest'],
         ok=V(exit=1, has=['no geomean to bracket'],
              hasnt=['ZeroDivisionError', 'Traceback']),
         bug=V(has=['ZeroDivisionError'])),

    case('selftest-names-a-zero-slope-cell', 'read-run.py', '468dc06',
         'a zero time slope divided in load(), before --selftest could name it',
         # The malformed-cell check exists to report exactly this cell and
         # could not reach it: `load` divides the CI bounds by the slope
         # for every cell with `lo is None` as its only guard, so a slope
         # of exactly 0 raised out of the middle of load() in every mode.
         # The two sunk-baseline cases above are the same family one stage
         # later, on net rather than on slope.
         plant=lambda t: {'run': doctored(t, 'main', lambda b: scale(
             b, main_shapes()[0] + '/build', 0.0))},
         argv=['{run}', '--selftest'],
         ok=V(exit=1, has=['non-positive slope'],
              hasnt=['ZeroDivisionError', 'Traceback']),
         bug=V(has=['ZeroDivisionError'])),

    case('table-survives-a-zero-list-slope', 'read-run.py', 'ba56d23',
         "a zero `list` slope divided in the table's share line, the default",
         # The family's last site, found by sweeping for it the day after
         # the selftest's: the share of the forcing term in `list` and the
         # shipped arm divides by their slopes, and a cell with none took
         # the default mode down with a traceback where the health warning
         # beside it names the cell.
         plant=lambda t: {'run': doctored(t, 'main', lambda b: scale(
             b, main_shapes()[0] + '/list', 0.0))},
         argv=['{run}'],
         ok=V(exit=0, has=['forcing term is not smaller than the cell'],
              hasnt=['ZeroDivisionError', 'Traceback']),
         bug=V(has=['ZeroDivisionError'])),

    case('fingerprint-refuses-a-sunk-cell', 'read-run.py', 'e2d6604',
         'a sunk cell was divided and INSTALLED, outliving its own run',
         plant=lambda t: {'run': sunk_json(t, main_shapes(),
                                           'mut-odo-vecdims')},
         argv=['{run}', '--fingerprint'],
         ok=V(has=['| -- |']),
         bug=V(has=['| shape |'], hasnt=['| -- |'])),

    case('block-per-shape-refuses-a-sunk-cell', 'read-run.py', 'e2d6604',
         "a sunk cell was divided into the block's installed per-shape line",
         plant=lambda t: {'run': sunk_json(t, class_shapes('scaled'),
                                           'mut-odo-vecdims')},
         argv=['{run}', '--block', '--brief'],
         ok=V(has=['--/']),
         bug=V(has=['summary row'], hasnt=['--/'])),

    case('machine-check-drops-a-sunk-baseline', 'read-run.py', 'e2d6604',
         'a non-positive `list` net raised, and run-gate.sh files stderr'
         ' verbatim into the pair note',
         # The exit moved from 1 to 0 on 2026-08-23 and this case's subject
         # did not: SOME shapes sunk are dropped BY NAME and the rest are
         # compared, and what is asserted here is that naming and the
         # absence of a traceback. The 1 it used to read was the box
         # verdict underneath, which no longer stops anything.
         plant=lambda t: {'run': sunk_json(t, main_shapes(), 'list')},
         argv=['{run}', '--machine'],
         ok=V(exit=0, has=['net not positive'], hasnt=['Traceback']),
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
         bug=V(exit=1, has=['the yardstick table is gone'],
               hasnt=['still carry the `?`'])),

    case('claims-current-run-not-exempt', 'read-run.py', 'a6c32e8',
         '`Run N` exempted the run in hand, the one kind that matters',
         # THE ONE CASE STILL ON A CAPTURED RUN, and it is stated rather
         # than left to be noticed. Its verdict is a published reading,
         # 0.9312, and the defect is that the sentence exempted the run in
         # hand from being read at all -- so what separates the two
         # revisions is whether that figure appears. Over a built run they
         # print byte-identical output, measured 2026-08-17, so the case
         # would pass while testing nothing. If the captured run's artifacts
         # go, this reports FIXTURE DID NOT BUILD, which is the honest
         # failure and not a false pass; re-aim it at whatever run is then
         # on disk. RE-AIMED 2026-08-23 from run14-lookrts to run18-g912,
         # the artifacts up to Run 16 having been deleted that day. The
         # figure is the FIXTURE's, planted into the README copy rather
         # than read from the run, so it does not move with the run; what
         # the run has to be is CAPTURED rather than built.
         plant=lambda t: {'readme': readme_current_run_sentence(t),
                          'run': run_json('run18-g912-main.json')},
         argv=['{run}', '--claims', '--readme', '{readme}'],
         ok=V(has=['0.9312']),
         bug=V(has=['HELD'], hasnt=['0.9312'])),

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
         bug=V(has=['in-situ forcing term'],
               hasnt=['over 2 of 3 shape(s)'])),

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
         bug=V(has=['six columns'],
               hasnt=['not checked: it has 5 column(s)'])),

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
         bug=V(has=['alloc missing for'], hasnt=['allocated R2 < 0.99'])),

    case('checkdoc-chapter-heading-gone', 'read-run.py', 'a6c32e8',
         'the chapter-link sweep lost its own boundary in silence',
         plant=lambda t: {'readme': readme_chapter_renamed(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(has=['BLOCKED: no `## About the last run` heading']),
         bug=V(exit=1, has=['dead anchor(s)'],
               hasnt=['BLOCKED: no `## About the last run` heading'])),

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
         bug=V(exit=1, has=['did not happen'],
               hasnt=['no roster parsed out of Main.hs'])),

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
         bug=V(has=["name 'small_ceiling' is not defined"], hasnt=['500.0'])),

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

    case('properties-buries-its-verdict-in-the-readers-stderr',
         'check-scripts.py', '7a68237',
         'six lines of verdict under 198 KB of expected warning',
         # These properties drive the reader over every run on disk, so it
         # warns once per run per table about rows a later roster dropped.
         # Correct and expected, and it buried the pass: 258 lines against
         # six, which is a pass a session pipes through `tail` -- and a
         # pipe throws away the exit code this whole file is. Withheld and
         # counted BY KIND, so a warning the corpus has never shown before
         # is still visible as a kind with a count of one. The check is the
         # withheld line, not the size: a summary that named only a total
         # would pass this and hide a new kind.
         argv=['--properties'],
         ok=V(exit=0, has=['line(s) of reader warning withheld',
                           'kind(s)']),
         bug=V(exit=0, hasnt=['line(s) of reader warning withheld'])),

    case('tree-check-that-could-not-run', 'check-scripts.py', 'ea4ab06',
         'this suite\'s one guarantee about itself passed unchecked',
         argv=['--unit', "tree_state.__doc__ and (git('rev-parse')"
                         ".returncode, tree_state() is None)"],
         ok=V(has=['(0, False)']),
         bug=V(has=["name 'tree_state' is not defined"],
               hasnt=['(0, False)'])),

    case('tree-change-in-both-directions', 'check-scripts.py', 'ea1a3e6',
         'a file REMOVED tripped the alarm and printed nothing beneath it',
         argv=['--unit', "tree_delta('?? a\\n?? b\\n', '?? b\\n')"],
         ok=V(has=['gone']),
         bug=V(has=["name 'tree_delta' is not defined"], hasnt=['gone'])),

    case('shadow-refuses-an-absolute-cd', 'check-scripts.py', '77fd51b',
         'a program cd-ing to an absolute path ran for real from a shadow',
         # The overwrite of 2026-08-23, as a case: a shadow holds a program
         # only if the program stays in it, and probe-areacurve.sh's old
         # `cd /home/...` put it back here, on the real binary, writing the
         # real artifacts. Asked of shadow_dir directly; the old one built
         # the shadow and handed it back.
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'cd /nowhere-zz\\n')"],
         ok=V(has=['cds to an absolute path']),
         bug=V(has=['/shadow'], hasnt=['cds to an absolute path'])),

    case('shadow-refuses-a-quoted-absolute-cd', 'check-scripts.py', '9a51f3a',
         'the same cd in quotes slipped the guard',
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'cd \"/nowhere-zz\"\\n')"],
         ok=V(has=['cds to an absolute path']),
         bug=V(has=['/shadow'], hasnt=['cds to an absolute path'])),

    case('shadow-holds-its-own-directory', 'check-scripts.py', None,
         'CONTROL: `cd "$(dirname "$0")"` is what a shadow can hold',
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'cd \"$(dirname \"$0\")\"\\n')"],
         ok=V(has=['/shadow'], hasnt=['cds to an absolute path'])),

    # ---- this file's own instruments ------------------------------------
    case('fixture-ci-bounds-are-criterion-shaped', 'check-scripts.py', '40f7a37',
         'the fixture wrote a negative lower CI bound, which criterion never does',
         # Criterion writes both deviations positive (`confIntLDX`
         # 9.649e-11 beside `confIntUDX` 1.154e-10 in run10-aligned-main),
         # and the reader's CI% is their mean over the slope. `_est` wrote
         # `-d` and `d`, a mean of exactly 0, so every synthetic cell read
         # CI% 0.00, every row's noise was nan off a falsy typical, and no
         # case could assert a CI or noise figure: that column was untested
         # by every fixture here, and a regression in it passed the suite.
         argv=['--unit', "_est(1.0)['estError']['confIntLDX'] > 0"],
         ok=V(has=['True']),
         bug=V(has=['False'])),

    case('ci-column-reads-the-fixture', 'read-run.py', None,
         "CONTROL: a built run reads CI% 1.0000 in every cell, the fixture's 1%",
         # The other half of the case above, on the reader: `--cells`
         # prints ci_pct and ci_hi_pct, and both are the fixture's 1% now
         # where they were 0.0000 and 1.0000. A control, the defect being
         # in this file's fixture, which --audit does not replay.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--cells'],
         ok=V(has=['\t1.0000\t1.0000\t'], hasnt=['\t0.0000\t1.0000\t'])),

    case('health-warns-on-a-null-bound', 'read-run.py', None,
         'CONTROL: one null CI bound is one cell with no confidence interval',
         # `health`'s no_ci path fires on `ci is None` alone, which no
         # fixture reached while every bound was written; a bound written
         # null, as a starved fit leaves it, is what reaches it.
         plant=lambda t: {'run': doctored(t, 'main', lambda b: null_bound(
             b, main_shapes()[0] + '/build'))},
         argv=['{run}'],
         ok=V(exit=0, has=['1 cell(s) with no confidence interval'])),

    case('env-parse-through-a-helper', 'check-scripts.py', '40f7a37',
         'an import-time parse in a helper called at import went unflagged',
         # The family's guard read the line's own scope -- `at.get(n.lineno)
         # is None` is a module-scope line and nothing else -- so a helper
         # called at module scope, align-as.py's `number()` and the form
         # the family was counted from, passed, and the family had no live
         # site in the tree: a silent search. A helper called at import
         # parses at import.
         plant=lambda t: {'py': write(here_file('zz-fam.py'), ZZ_FAM_HELPER)},
         argv=['--unit', "family_lint('zz-fam.py')"],
         # Both sites by line: the helper's parse and a class body's, the
         # second flagged by the old lint too, which is what keeps the bug
         # verdict from holding on a crash.
         ok=V(has=['zz-fam.py:5 ', 'zz-fam.py:9 ']),
         bug=V(has=['zz-fam.py:9 '], hasnt=['zz-fam.py:5 '])),

    case('env-parse-under-a-handler-is-not-flagged', 'check-scripts.py',
         None,
         'CONTROL: under a try, or reached only from one, a lambda or main',
         # What the family is about is a parse OUTSIDE any handler, at
         # import: the handled form is align-as.py's own now, and a helper
         # reached only from under a module-level try, from a lambda, or
         # from the `__main__` block does not run at import. The control
         # that the case above is no ban on reading the environment.
         plant=lambda t: {'py': write(here_file('zz-fam.py'),
                                      ZZ_FAM_HANDLED)},
         argv=['--unit', "family_lint('zz-fam.py')"],
         ok=V(has=['([], [])'])),

    case('families-name-their-reach', 'check-scripts.py', None,
         'CONTROL: --families says what it swept, and that it is Python only',
         # Its ok line, the docstring, README's step 8b and preflight's
         # step said "every program here" for an AST lint over the Python
         # files alone, the shell scripts never touched. The one shell
         # family this review wanted was measured and refused; `families`
         # has the measurement.
         argv=['--families'],
         ok=V(exit=0, has=['Python file(s)', 'shell scripts'])),

    case('properties-refuse-an-empty-corpus', 'check-scripts.py', None,
         'every property held over zero runs, and said so as a pass',
         # The empty-search trap this file carries cases about, in the
         # file that carries them: `runs_on_disk` over a directory with no
         # JSON -- a corpus deleted after a write-up, or a CORPUS aimed
         # wrong -- quantified every property over nothing and printed
         # `every property holds over every run on disk`. A control and
         # not a replay: CORPUS is the seam the fix added, and the code
         # before it cannot be pointed at an empty directory at all.
         plant=empty_corpus,
         env={'CORPUS': '{corpus}'},
         argv=['--properties'],
         ok=V(exit=1, has=['empty corpus proves nothing'],
              hasnt=['every property holds'])),

    case('properties-over-one-built-run', 'check-scripts.py', None,
         'CONTROL: a corpus of one built run holds every property',
         plant=corpus_of_one,
         env={'CORPUS': '{corpus}'},
         argv=['--properties'],
         ok=V(exit=0, has=['every property holds', 'over 1 '])),

    # ---- the write-up's derived sources --------------------------------
    # Three readings a run used to take by eye and one it took twice: the
    # class lead against the run standing under it, a class property's
    # break against that population's own floor, and the extremes across
    # every class at once. Each is a hand-written line over installed
    # content, which is this suite's oldest family.
    #
    # THREE OF THEM ARE CONTROLS and have no `bug` to replay.
    # `lead-in-run-order-is-silent` and
    # `answered-pointer-may-be-reference-style` both assert an ABSENCE, so
    # they pass at the fix and before it alike -- which is the point of
    # them, each saying that the plant beside it is what fires its
    # siblings and not the fixture they share.
    # `floor-movement-built-clean-passes` would fail before the fix, the
    # line it asserts being the new check's own, and is a control of the
    # BUILT paragraph rather than of the check: the two cases beside it
    # bend that paragraph, and this is it unbent.
    #
    # The rest carry both verdicts and split over two fixes -- the
    # reader's and the drivers' -- which is why the hashes differ down the
    # list. `classes-without-a-mode-that-reads-it` is the one worth
    # naming: before the fix it came back `exit 0, wanted 2`, the files
    # named by `--classes` read by nobody and the mode printing as though
    # they had not been given.
    case('lead-drops-a-shape', 'read-run.py', '3596ba2',
         'a class lead named two shapes over a run carrying three',
         # The five class views that gained a third shape on 2026-08-14
         # still had two-shape leads after Run 14's write-up, while the
         # per-shape line --block installs beneath them named three.
         # --block knew both all along and compared neither.
         plant=lambda t: {
             'readme': relead(t, 'slice', lambda s: s.replace(
                 ', `slice-coprime-r7` (`l` 60060, `sInner` 13)', '')),
             'run': synth_run(os.path.join(t, 'slice.json'),
                              run_order_shapes('slice'))},
         argv=['{run}', '--block', '--readme', '{readme}'],
         ok=V(exit=0, has=['does not name `slice-coprime-r7`']),
         bug=V(exit=0, hasnt=['does not name `slice-coprime-r7`'])),

    case('lead-order-mislabels-the-per-shape-line', 'read-run.py', '3596ba2',
         'a lead listed its shapes in an order the installed line is not in',
         # The per-shape paragraph is installed IN RUN ORDER and labelled
         # *in the lead's order*, so a lead that lists them differently
         # does not go stale -- it mislabels three live ratios, which is
         # the one of the three readings no reading of the block catches.
         plant=lambda t: {
             'readme': relead(t, 'slice', lambda s: s.replace(
                 '`slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3),'
                 ' `slice-primes` (`l` 250357, `sInner` 89)',
                 '`slice-primes` (`l` 250357, `sInner` 89),'
                 ' `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3)')),
             'run': synth_run(os.path.join(t, 'slice.json'),
                              run_order_shapes('slice'))},
         argv=['{run}', '--block', '--readme', '{readme}'],
         ok=V(exit=0, has=['it lists them `slice-primes`,'
                           ' `slice-cnn-L2-24x24-c32`']),
         bug=V(exit=0, hasnt=['it lists them `slice-primes`,'
                             ' `slice-cnn-L2-24x24-c32`'])),

    case('lead-figures-disagree-with-main-hs', 'read-run.py', '3596ba2',
         'a lead\'s hand-copied `l` had no source but the lead',
         plant=lambda t: {
             'readme': relead(t, 'slice', lambda s: s.replace(
                 '`slice-primes` (`l` 250357', '`slice-primes` (`l` 250358')),
             'run': synth_run(os.path.join(t, 'slice.json'),
                              run_order_shapes('slice'))},
         argv=['{run}', '--block', '--readme', '{readme}'],
         ok=V(exit=0, has=['is written (`l` 250358, `sInner` 89) where'
                           ' Main.hs gives (`l` 250357, `sInner` 89)']),
         bug=V(exit=0, hasnt=['is written (`l` 250358, `sInner` 89)'])),

    case('lead-in-run-order-is-silent', 'read-run.py', None,
         'CONTROL: the lead as written, over the run it stands over',
         # The three above plant into the same lead, so this is what says
         # they are firing on the plant and not on the fixture: same
         # class, same built run, the README untouched.
         plant=lambda t: {'run': synth_run(os.path.join(t, 'slice.json'),
                                           run_order_shapes('slice'))},
         argv=['{run}', '--block'],
         ok=V(exit=0, hasnt=['lead `slice`'])),

    case('break-priced-against-its-population-floor', 'read-run.py', '3596ba2',
         'a class property break was reported as a sort, with no width',
         # Run 15 published seven breaks off the sort and five were ties
         # inside their own population's floor. THE SAME BREAK, against a
         # floor twice as wide, has to read the other way -- which is what
         # this and the case below are: one built run, one A/A pair driven
         # wide in the second, and the verdict flipping on the floor alone.
         plant=lambda t: {'run': synth_json(t, 'revsome')},
         argv=['{run}', '--block'],
         ok=V(exit=0, has=['priced:', 'OUTSIDE the floor'],
              hasnt=['INSIDE the floor']),
         bug=V(exit=0, hasnt=['priced:', 'OUTSIDE the floor'])),

    case('a-wide-floor-swallows-the-same-break', 'read-run.py', '3596ba2',
         'nothing said whether a break was wider than the run could see',
         plant=lambda t: {'run': doctored(
             t, 'revsome',
             lambda bs: _scale_arm(bs, 'offtab-aa-distant', 2.5),
             'wide-floor.json')},
         argv=['{run}', '--block'],
         ok=V(exit=0, has=['priced:', 'INSIDE the floor'],
              hasnt=['OUTSIDE the floor']),
         bug=V(exit=0, hasnt=['priced:', 'INSIDE the floor'])),

    case('open-list-entry-without-a-status', 'read-run.py', '3596ba2',
         'an entry a grep could not classify sat in the list to be read',
         # The section's preamble states that every entry opens with its
         # status and offers a grep for the live ones as the use of it.
         # That was true of the parent list and false of the sublists:
         # seven of thirteen carried no token, four of them closed in the
         # ten days before 2026-08-22, their closure a phrase inside the
         # bolded lead. FAILED rather than listed, alone among this
         # section's checks -- which token an entry takes is the author's
         # and is decided before this runs, so nothing is left to judge.
         plant=lambda t: {'readme': readme_entry_without_status(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['open with no status',
                           'cannot find the live ones among them',
                           'zz-planted-tokenless']),
         bug=V(exit=0, hasnt=['open with no status'])),

    case('open-list-status-check-does-not-pass-empty', 'read-run.py', '3596ba2',
         'a reshaped list would have passed the status check over nothing',
         # Every entry indented into a sub-bullet, which is what a reshape
         # of the section would look like to this pattern. The check has
         # to say it did not run: a list of no entries is trivially all
         # statused, and that silence reads exactly like a clean one.
         plant=lambda t: {'readme': readme_open_list_reshaped(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['no top-level entry found',
                           'the status check did not run']),
         bug=V(exit=0, hasnt=['no top-level entry found'])),

    case('answered-account-fails-the-document', 'read-run.py', '3596ba2',
         'an answer grew into the chapter it should have pointed at',
         # The open list is a question register and `What is settled, and
         # where` is the pointer layer, which says of itself that it
         # carries no figures by design. An ANSWERED entry that runs to a
         # chapter is the account in the one place that does not move when
         # a run does, and the topical section it duplicates goes on
         # moving without it.
         #
         # IT GATES, and that took two goes to earn: it listed while the
         # test was length AND the absence of a pointer, which could not
         # tell an account from an entry that had earned its length, and
         # then while the run registrations sat in every list it made.
         # Length alone decides now, the two exemptions are mechanical,
         # and what is left is a defect with three truthful ways out --
         # which the failure names, the third of them being the escape
         # the case below this one is about.
         plant=lambda t: {'readme': readme_answered_account(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['ANSWERED entry(s) past 500 words',
                           'zz-planted-account', 'only copy']),
         bug=V(exit=0, hasnt=['ANSWERED entry(s) past 500 words'])),

    case('answered-only-copy-ruling-is-exempt', 'read-run.py', None,
         'a gate with no true way out for an answer nothing else records',
         # WHAT MAKES THE GATE HONEST. `bq-scan-packed-mulback`'s Core
         # account is the only copy there is -- the dead-ideas list takes
         # ideas that died on paper and that one was built, rostered and
         # measured -- so a long one of its kind would be failed with no
         # true way to pass. A bolded clause carrying `only copy` is the
         # ruling and the exemption at once.
         plant=lambda t: {'readme': readme_answered_account(
             t, tail=' **The account above is the only copy, and there is'
                     ' nowhere to move it.**')},
         # `--worklists`, because the quiet form withholds the `ok:` line
         # this reads and an absence would pass whether the check ran or
         # not.
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(exit=0, has=['1 only-copy ruling(s)'])),

    case('answered-registration-is-exempt', 'read-run.py', None,
         'the registrations were adjudicated by hand every run',
         # Six entries a reader cleared by hand each time the list was
         # printed, all of them long for the same recorded reason: a
         # registration is the only copy, the run chapter being replaced
         # every run and the yardstick keeping one geomean per strategy
         # per half. Exempt by the lead the family shares, and COUNTED.
         plant=lambda t: {'readme': readme_answered_account(
             t, lead='**What Run 99 was built to answer, registered before'
                     ' it ran --- and what it answered.**')},
         # The `ok:` line is asserted as well as the absence, so a check
         # that did not run cannot pass this by saying nothing.
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(exit=0, has=['run registration(s) and'],
              hasnt=['What Run 99'])),

    case('answered-registration-lead-must-match', 'read-run.py', None,
         'an exemption a drifted lead would have kept in silence',
         # The exemption is keyed on the phrasing, so a member that drifts
         # out of it LOSES the exemption and is failed -- which is the
         # failure a reader can see, and the reason Run 10's lead was
         # normalised back rather than the pattern widened to admit it.
         # Its own text called them registrations while its lead said
         # `predictions`.
         plant=lambda t: {'readme': readme_answered_account(
             t, lead="**Run 99's predictions, and how they came out.**")},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=["Run 99's predictions"])),
    case('floor-movement-reads-the-previous-column', 'read-run.py', '3596ba2',
         "a run installed a class table and left the last run's movements",
         # The paragraph under the class table reads each class's floor
         # against its predecessor's, so its second figure is a claim
         # about the column right above it -- and it is written by hand
         # under a table install-tables.sh writes. Run 17 installed the
         # column and left Run 16's paragraph standing: all eight `to`
         # figures were the previous run's, with --lint, --check-doc and
         # both installers green over them.
         #
         # The plant is the OPPOSITE of the live document's state, one
         # figure of the paragraph moved off the column, so that the case
         # keeps meaning this when the paragraph is repaired.
         plant=lambda t: {'readme': readme_floor_movement_off_column(t)},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(exit=1, has=["reading the PREVIOUS run's column"]),
         bug=V(exit=0, hasnt=["reading the PREVIOUS run's column"])),

    case('floor-movement-built-clean-passes', 'read-run.py', None,
         'CONTROL: the same built paragraph with every figure right',
         # The two cases beside this one both plant into a paragraph this
         # fixture constructs, so this is what says they fire on the
         # plant and not on the construction.
         plant=lambda t: {'readme': readme_with_floor_movement(t)},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(exit=0, has=["floor movement(s) land on the class table's own"
                           ' column'])),

    case('floor-movement-reworded-does-not-pass-empty', 'read-run.py', '3596ba2',
         'a reworded movement sentence would have turned the check off',
         # Keying the vacuity guard on the sentence's opening phrase was
         # the first attempt and is what this refuses: rewording that
         # phrase turned the check off in silence. The guard is the
         # paragraph's SHAPE now -- four or more classes with a figure
         # apiece -- so a rewording that keeps the content still parses
         # and one that does not fails loudly.
         plant=lambda t: {'readme': readme_floor_movement_reshaped(t)},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(exit=1, has=['if that sentence was reworded']),
         bug=V(exit=0, hasnt=['if that sentence was reworded'])),

    case('extremes-ranks-and-says-where-the-two-readings-differ',
         'read-run.py', '3596ba2',
         'a superlative about the eight classes had no derived source',
         # Run 15 got three wrong in one draft, every one caught by an
         # independent reader. `--block` sees one class and the sort was
         # left to the eye.
         plant=lambda t: {
             'a': synth_run(os.path.join(t, 'rev.json'),
                            run_order_shapes('rev')),
             'b': synth_run(os.path.join(t, 'slice.json'),
                            run_order_shapes('slice'))},
         argv=['--extremes', '--classes', '{a}', '{b}'],
         ok=V(exit=0, has=['2 class population(s)', 'tightest floor',
                           'widest gap, paired']),
         bug=V(exit=2, hasnt=['class population(s)'])),

    case('extremes-counts-one-class-twice', 'read-run.py', '3596ba2',
         'the same class named twice would rank one population as two',
         plant=lambda t: {'a': synth_run(os.path.join(t, 'rev.json'),
                                         run_order_shapes('rev')),
                          'b': synth_run(os.path.join(t, 'rev2.json'),
                                         run_order_shapes('rev'))},
         argv=['--extremes', '--classes', '{a}', '{b}'],
         ok=V(exit=1, has=['a class is named twice']),
         bug=V(exit=2, hasnt=['a class is named twice'])),

    case('extremes-is-not-for-the-main-set', 'read-run.py', '3596ba2',
         'the main set has no class row and would have been ranked as one',
         plant=lambda t: {'a': synth_json(t, 'main')},
         argv=['--extremes', '--classes', '{a}'],
         ok=V(exit=1, has=['ranks the stride classes']),
         bug=V(exit=2, hasnt=['ranks the stride classes'])),

    case('extremes-with-no-classes', 'read-run.py', '3596ba2',
         'a mode whose whole input is a modifier, given without it',
         argv=['--extremes'],
         ok=V(exit=2, has=['none were given']),
         bug=V(exit=2, hasnt=['none were given'])),

    case('classes-without-a-mode-that-reads-it', 'read-run.py', '3596ba2',
         'the files named by --classes were read by nobody, at exit 0',
         plant=lambda t: {'a': synth_json(t, 'rev'),
                          'run': synth_json(t, 'main')},
         argv=['{run}', '--markdown', '--classes', '{a}'],
         ok=V(exit=2, has=['does nothing alone']),
         bug=V(exit=0, hasnt=['does nothing alone'])),

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
         bug=V(exit=0, hasnt=['pad byte(s) appended'])),

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

    case('non-number-refused-in-one-line', 'align-as.py', '40f7a37',
         'PAD_BYTES=abc killed the compile with a traceback out of the shim',
         plant=asm,
         env={'REAL_AS': '{as}', 'PAD_BYTES': 'abc'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         # It should kill the compile -- the recipe asked for something
         # this shim cannot do -- and did, with a ValueError traceback at
         # import, outside any handler: the import-time family's own
         # shape, in the file the family was counted from, which the lint
         # could not see through the helper. One line naming the variable
         # and its value now, at exit 1, under a handler the lint sees.
         ok=V(exit=1, has=["PAD_BYTES='abc' is not a number"],
              hasnt=['Traceback']),
         bug=V(has=['Traceback', 'ValueError'])),

    case('probe-that-did-not-assemble', 'align-as.py', '437ce00',
         'a failed probe made the max-skip half the unconditional one',
         plant=asm,
         env={'REAL_AS': '{as}', 'LOOP_MAXSKIP': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(has=['objdump -t', 'not the max-skip form']),
         bug=V(exit=0, hasnt=['not the max-skip form'])),

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
         bug=V(has=['{}'], hasnt=['mangled symbol'])),

    case('suppressed-groups-are-counted', 'loop-offsets.py', 'febc2bd',
         'a group under --min-copies vanished, the docstring\'s own example',
         argv=['--len', '24', '/usr/bin/objdump'],
         ok=V(has=['suppressed']),
         bug=V(has=['self-loops of 24 B'], hasnt=['suppressed'])),

    # ---- read-all.sh ---------------------------------------------------
    case('aa-worst-cell-is-not-an-insitu-row', 'read-all.sh', '8ee1e5b',
         'with every twin filtered out an in-situ row was read as the A/A',
         plant=lambda t: synthetic_run(t, no_twins=True),
         argv=['{tag}'],
         ok=V(has=['(no A/A pair in this file)']),
         bug=V(has=['ok        worst cell'],
               hasnt=['(no A/A pair in this file)'])),

    case('aa-worst-cell-is-not-the-sum-only-pair', 'read-all.sh', 'bd88db5',
         "the sum-only pair's raw worst cell was printed as the A/A worst",
         # `--aa` prints the `sum-only` pair among the A/A pairs, above the
         # in-situ header this column stops at, and compares it RAW -- its
         # raw ratio being the position test -- where `aa_pairs` keeps it
         # out of the floor. So a shape on which the two halves disagree by
         # more than any A/A cell was the figure printed under A/A, and on
         # Run 11's slice process it tied the widest A/A cell at 0.61% and
         # the tie went to it. One half skewed 2% on one shape is that
         # state, wider than the wobble every A/A pair is built with.
         plant=lambda t: synthetic_run(
             t, skew=[(class_shapes('rev')[0], 'sum-only-late', 1.02)]),
         argv=['{tag}'],
         ok=V(exit=0, has=['every process gated clean'],
              hasnt=['worst cell 2.00%']),
         bug=V(has=['worst cell 2.00% on'])),

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
         # selection on a binary at whatever condition the fingerprint was
         # taken under. Written as a capability rather than a caveat, per
         # README's rule that a limitation is recorded with what it still
         # leaves possible.
         #
         # THE ASSERTION MOVED 2026-08-23 with the message it reads. It
         # pinned `at the fingerprint's own allocation area`, which was the
         # only condition Run 16 had varied; Run 18 met the same check with
         # the area UNCHANGED and a preamble, a source patch and a compiler
         # between it and the fingerprint, and had to invent the control
         # the message should have named. What is asserted now is the
         # generalisation and the second control the message gained --
         # the previous run's own binary, which produced the fingerprint.
         # AND THE EXIT MOVED 2026-08-23 too, from 1 to 0, with the ruling
         # that the box question never stops a run. The control this case
         # is about is unaffected -- it is what the message names, not what
         # it returns -- so the assertion keeps the two controls and reads
         # the new marker in place of the old `PAST`.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--machine'],
         ok=V(exit=0, has=['BOX MOVED', 'CONDITION THE FINGERPRINT',
                           "previous run's own binary"]),
         bug=V(exit=1, has=['PAST'], hasnt=['CONDITION THE FINGERPRINT'])),

    case('machine-check-does-not-stop-a-moved-box', 'read-run.py', 'bc2f884',
         'a box that got faster or slower failed the gate, leaving a quiet'
         ' machine idle until a person woke to be asked',
         # Run 18 met this at +4.81%: the gate exited 1, the evening did not
         # start, and it ended in `run anyway, re-baseline` -- the answer
         # that was always going to be given, since every claim this README
         # publishes is a within-run comparison and a box that moved BETWEEN
         # runs cannot reach one. The reading was worth having and the stop
         # was not: an idle night cannot be recovered and a reading can.
         plant=lambda t: {'run': synth_json(t, 'main', slow=1.30,
                                            name='moved.json',
                                            fingerprint=os.path.join(
                                                t, 'fp-moved.md')),
                          'readme': os.path.join(t, 'fp-moved.md')},
         argv=['{run}', '--machine', '--readme', '{readme}'],
         ok=V(exit=0, has=['BOX MOVED', 'moved TOGETHER',
                           'GOES AHEAD EITHER WAY'], hasnt=['STOP']),
         bug=V(exit=1, has=['STOP'])),

    case('machine-check-tells-a-level-shift-from-a-skewed-shape',
         'read-run.py', 'bc2f884',
         'a moved box was one verdict, so a move the shapes disagreed on'
         ' read exactly like one they agreed on',
         # The two cost different things. Shapes moving together is a single
         # number and every cross-run ORDERING survives it; shapes moving
         # apart puts the orderings in question as well as the level, which
         # is the half worth carrying into a write-up. The band is the 7%
         # the mode's own docstring already calls an ordinary single-shape
         # wander, so it is not a second arbitrary threshold.
         plant=lambda t: {'run': synth_json(
                              t, 'main', slow=1.10, name='skewed.json',
                              skew=[(main_shapes()[0], 'list', 1.30)],
                              fingerprint=os.path.join(t, 'fp-skewed.md')),
                          'readme': os.path.join(t, 'fp-skewed.md')},
         argv=['{run}', '--machine', '--readme', '{readme}'],
         ok=V(exit=0, has=['did NOT move together', 'ORDERING is in question'],
              hasnt=['moved TOGETHER']),
         bug=V(exit=1)),

    case('machine-check-passes-an-unmoved-box', 'read-run.py', None,
         'CONTROL: a run built to match its own fingerprint reads inside the'
         ' band, so the two cases above are not passing on the fixture',
         plant=lambda t: {'run': synth_json(t, 'main', name='same.json',
                                            fingerprint=os.path.join(
                                                t, 'fp-same.md')),
                          'readme': os.path.join(t, 'fp-same.md')},
         argv=['{run}', '--machine', '--readme', '{readme}'],
         ok=V(exit=0, has=['inside 3%'], hasnt=['BOX MOVED'])),

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

    case('counts-refuses-a-blocked-perf', 'run-counts.sh', None,
         'a blocked perf spent the whole sweep writing NaN',
         # Every cell is two `perf stat` processes, so a machine that
         # refuses the counter does not fail the sweep -- it writes a `!!`
         # line per cell and takes the same forty minutes a half to do it.
         # And the setting is not persistent: kernel.perf_event_paranoid
         # read 1 on 2026-08-21, 4 on 2026-08-22 and 1 again that evening,
         # so it is a state to assert at the moment of use.
         #
         # Both sides use a STUB perf and not the machine's, or the case
         # would pass or fail on the box's current setting -- which is the
         # very thing that moves.
         shadow=dict(extra=[('zzct3-g912', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_BLOCKED)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzct3', 'g912'],
         ok=V(exit=1, has=['perf will not count instructions here',
                           'Nothing ran'])),

    case('counts-refuses-an-unwritable-tmp', 'run-counts.sh', None,
         'a broken temp path bought the same forty minutes of NaN',
         # The second route to an all-NaN sweep, and the quieter one:
         # `count()` hands perf a `mktemp` file per cell, so where that
         # fails -- a sandbox permitting only some of /tmp, which
         # read-all.sh records having met -- perf writes nowhere, the grep
         # reads nothing, and the cell is NaN with the path named nowhere.
         # A perf that answers is not enough on its own, which is why this
         # rides beside the perf guard rather than inside it.
         shadow=dict(extra=[('zzct5-g912', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_ANSWERS)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'TMPDIR': '/nonexistent-zz',
              'ONLY': 'shape-a', 'ARMS': 'list', 'N': '1'},
         argv=['zzct5', 'g912'],
         ok=V(exit=1, has=['mktemp gives no writable file', 'Nothing ran'])),

    case('counts-runs-under-a-perf-that-answers', 'run-counts.sh', None,
         'CONTROL: the guard passes and the sweep writes its counts',
         # The other side of both guards, and what says neither is simply
         # a ban:
         # with a perf that answers, the same invocation gets through and
         # the differenced count lands in the file.
         shadow=dict(extra=[('zzct4-g912', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_ANSWERS)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzct4', 'g912'],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzct4-counts-g912.txt')).read(),
         ok=V(exit=0, has=['shape-a list 1'], hasnt=['perf could not'])),

    case('wild-partial-load-fields', 'read-run.py', None,
         'a foreign figure over half a bench read as the whole bench',
         # A log spanning an instrument change -- or two concatenated --
         # has samples with the load fields and samples without, and the
         # foreign column can only be over the ones that carry them. Saying
         # nothing about that is a figure over a subset presented as the
         # bench's, which is the silent narrowing this directory refuses
         # everywhere else. Found 2026-08-22 by probing the mode's own
         # branches after it was written, not by anything failing.
         plant=lambda t: {'log': write(os.path.join(t, 'w.log'), WILD_MIXED)},
         argv=['{log}', '--wild'],
         ok=V(exit=0, has=['marked *', '1 of 2 sample(s)'])),

    case('wild-drops-an-unpaired-stamp', 'read-run.py', None,
         "CONTROL: a killed process's trailing `pre` is counted, not paired",
         # The instrument writes two lines a sample. A log a killed process
         # left ends in a `pre`, and pairing it with what follows would read
         # one bench's work as another's -- so it is dropped and COUNTED,
         # the count being the only thing that says the log is short.
         plant=lambda t: {'log': write(os.path.join(t, 'w.log'), WILD_MIXED)},
         argv=['{log}', '--wild'],
         ok=V(exit=0, has=['1 unpaired stamp(s) dropped'])),

    case('wild-refuses-a-json', 'read-run.py', None,
         'CONTROL: the stamps are on stderr, so --wild wants the .log',
         # Every other mode takes criterion's JSON and this one does not,
         # so the wrong file is the likely mistake; it dies in json.load
         # otherwise, which names nothing.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--wild'],
         ok=V(exit=2, has=['in the .log beside this file'])),

    case('replace-inside-a-list-item', 'read-run.py', None,
         'an anchor naming one task replaced the whole list with it',
         # --replace's unit is a blank-line paragraph, and a list with no
         # blank lines between its items is ONE. Measured 2026-08-22 in
         # this README's own open list: an anchor naming task 3 took tasks
         # 1, 2 and 3 and wrote back task 3 alone, at exit 0. The echo had
         # named task 1 as what was going, which is a warning where the
         # difference between losing two paragraphs and not is a refusal.
         plant=lambda t: {'readme': edited_readme(t),
                          'anchor': task_anchor(LAST),
                          'with': write(os.path.join(t, 'w.txt'), 'x\n')},
         argv=['--replace', '{anchor}',
               '--with', '{with}', '--readme', '{readme}'],
         # The count is not asserted: the list loses an item whenever a
         # task is spent, and `3-item list` was a stored number one
         # renumbering away from being wrong.  What the case is about is
         # the refusal and what it warns of.
         ok=V(exit=1, has=['--replace: this paragraph is a',
                           'discard the items above'])),

    case('replace-a-whole-list-from-its-first-item', 'read-run.py', None,
         'CONTROL: quoting the list from item 1 still replaces all of it',
         # The other side, and the one that says the refusal did not simply
         # ban lists: a caller replacing the whole list quotes it from the
         # start, which is what it would do anyway, and gets it.
         plant=lambda t: {'readme': edited_readme(t),
                          'anchor': task_anchor(1),
                          'with': write(os.path.join(t, 'w.txt'), 'x\n')},
         argv=['--replace', '{anchor}',
               '--with', '{with}', '--readme', '{readme}'],
         # `out, first: 1.` and not the item's words: what went out
         # STARTING AT ITEM 1 is the whole claim, and quoting the lead
         # here would store the anchor this case was just taught to
         # derive, one line down.
         ok=V(exit=0, has=['out, first: 1.'])),

    case('plateau-band-across-processes', 'read-all.sh', None,
         'two processes saturated to different depths and gated clean',
         # Run 18's registration 5. Every recorded process asserts the
         # in-process state it measured in, and a process outside the run's
         # own band measured somewhere else -- which every gate beside this
         # one is blind to, each being WITHIN one process. The spread here
         # is the 14% an unsaturated process reads below a saturated one on
         # the dose measurements, so the fixture is the failure the band is
         # sized for and not an invented number.
         plant=lambda t: synthetic_run(t, plateau=['16.4', '19.1']),
         argv=['{tag}'],
         ok=V(exit=1, has=['the plateau is not flat', '16.4', '19.1'],
              hasnt=['999.0'])),

    case('plateau-band-holds-together', 'read-all.sh', None,
         'CONTROL: two processes inside the band, and the excluded logs',
         # The other side of the case above, and the one that says its
         # verdict is the readings and not the mere presence of a line: two
         # processes 1.2% apart pass, at exit 0, while the rider and gate
         # logs beside them carry 999.0 and are excluded by name. Counting
         # either would put the spread past any band, so this control fails
         # the moment that exclusion goes.
         plant=lambda t: synthetic_run(t, plateau=['19.0', '19.23']),
         argv=['{tag}'],
         ok=V(exit=0, has=['plateau: 2 process(es)', 'every process gated'],
              hasnt=['not flat'])),

    case('plateau-reading-missing-from-a-process', 'read-all.sh', 'bd88db5',
         'one reading left over gated the plateau flat, over one process',
         # The readings were counted among themselves and never against the
         # processes: one survivor is lo == hi, a spread of 0.00, and `every
         # process asserted the same in-process state` said over a run in
         # which the other process asserted nothing -- a half launched
         # without the dose, or a binary without the preamble, which is the
         # state the gate exists to catch. run-major.sh's own count fires
         # only under SATURATE, so nothing upstream said so either.
         plant=lambda t: synthetic_run(t, plateau=['19.0', None]),
         argv=['{tag}'],
         ok=V(exit=1, has=['1 reading(s) parsed from the',
                           '2 recorded process log(s)'],
              hasnt=['every process gated clean']),
         bug=V(exit=0, has=['plateau: 1 process(es)',
                            'every process gated clean'])),

    case('plateau-reading-in-exponent-form', 'read-all.sh', 'bd88db5',
         'a victim under 0.1 ms/iter was dropped by the extractor in silence',
         # `show` on a Double writes `8.5e-2` below 0.1, and the digits-and-
         # dot pattern that pulled the reading out matched no such line, so
         # the process vanished from the count with nothing said -- and
         # until the case above, a vanished process narrowed the band rather
         # than failing it. Two such readings 1.2% apart are a flat plateau.
         plant=lambda t: synthetic_run(t, plateau=['8.5e-2', '8.6e-2']),
         argv=['{tag}'],
         ok=V(exit=0, has=['plateau: 2 process(es)',
                           'every process gated clean']),
         bug=V(exit=0, has=['every process gated clean'],
               hasnt=['plateau:'])),

    case('plateau-reading-that-is-no-number', 'read-all.sh', 'bd88db5',
         'a reading of NaN was dropped, and the rest gated flat',
         # The other way a token before `ms/iter` fails to be a reading: a
         # victim timed over zero iterations shows as `NaN`, which moves
         # neither lo nor hi when compared, so any band holds it. Counted
         # apart and refused, not compared.
         plant=lambda t: synthetic_run(t, plateau=['19.0', 'NaN']),
         argv=['{tag}'],
         ok=V(exit=1, has=['1 of the line(s) no number']),
         bug=V(exit=0, has=['plateau: 1 process(es)'])),

    case('plateau-counted-per-log', 'read-all.sh', '03db05d',
         'two readings in one log covered for none in another',
         # Readings against logs was a count against a count, and a log
         # carrying two lines beside one carrying none satisfied it -- the
         # proxy for "every recorded process asserted its state", not the
         # property. Each log is asked now and the ones without a line are
         # named, which is also where a hand probe log in the run's
         # namespace surfaces: README's rule that no probe takes the
         # prefix, read back at the gate. Found 2026-08-23 by review.
         plant=lambda t: synthetic_run(t, plateau=[['19.0', '19.1'], None]),
         argv=['{tag}'],
         ok=V(exit=1, has=['log(s) with no reading',
                           'runzz-lookrts-slice.log'],
              hasnt=['every process gated clean']),
         bug=V(exit=0, has=['plateau: 2 process(es)',
                            'every process gated clean'])),

    case('plateau-counted-per-process', 'run-major.sh', None,
         'a half without the preamble joined a saturated run in silence',
         # The count, and it is the bench count's own shape: SATURATE is
         # set on the launch line and the binary is one that does not carry
         # the preamble, so every process runs UNSATURATED and each of its
         # figures is in a state the run does not know it is in. Nothing
         # else here can see it -- the process exits 0, leaves a JSON and
         # runs the count asked of it -- which is why the check is a count
         # of the line and not a reading of it.
         shadow=dict(extra=halves('zzpl-lookrts', 'zzpl-a1g')
                     + [('zzpl-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts', 'SATURATE': '1'},
         argv=['zzpl'],
         ok=V(exit=1, has=['did not assert its state',
                           '0 @@saturate line(s), not 1'])),

    case('wild-stamps-counted-per-process', 'run-major.sh', '41ab734',
         'a binary without the instrument joined an instrumented run',
         # The plateau count's twin, on the other launch switch, and it
         # was missing while the plateau's was there -- one switch of two
         # asserted, which is not a distinction a reader could predict.
         # WILDLOG is set and the binary carries no instrument, so every
         # process runs UNINSTRUMENTED: it exits 0, leaves a JSON, runs
         # its benches and writes a log with no stamps in it, and the only
         # thing that would ever have said so is `--wild`, which post-run
         # step 1b reaches for on a suspicious cell and not on every
         # process. ANY count above zero passes, unlike the plateau's
         # exactly-one: the instrument writes two stamps per sample.
         shadow=dict(extra=halves('zzwl-lookrts', 'zzwl-a1g')
                     + [('zzwl-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts', 'WILDLOG': '1'},
         argv=['zzwl'],
         ok=V(exit=1, has=['carries no @@wild stamps',
                           'only --wild would ever have said so']),
         bug=V(exit=0, hasnt=['carries no @@wild stamps'])),

    case('launch-switches-recorded-whether-set-or-not', 'run-major.sh', '41ab734',
         'the run recorded every provenance but the one it was launched with',
         # THE FORGET-PATH, which neither count reaches: both assertions
         # are conditional on their own switch, so they fire for an
         # operator who remembered and are silent for one who did not --
         # and forgetting is the failure. This cannot stop the run; what
         # it does is put the switches in the run's own record beside the
         # commits, the dirty count and `uptime`, at its first minute.
         # The verdict is on the LOG and not the terminal, that record
         # being the thing a write-up reads back weeks later.
         shadow=dict(extra=halves('zzle-lookrts', 'zzle-a1g')
                     + [('zzle-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzle'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzle-wallclock.log')).read(),
         ok=V(exit=0, has=['launch env: WILDLOG=unset SATURATE=unset']),
         bug=V(exit=0, hasnt=['launch env:'])),

    case('gate-records-and-asserts-its-launch-switches', 'run-gate.sh', '41ab734',
         'the gate proved the pair and said nothing about the instrument',
         # The gate takes the same switches the run will take (README's
         # recipe, step 14 then step 17), so a gate run without them
         # proves the pair mechanically and proves nothing about the
         # instrument the evening is for -- and its verdict reads clean
         # either way. It is also the CHEAP place to catch it: forty
         # minutes against the several hours it stands before.
         #
         # One invocation, both halves of the change: WILDLOG set over a
         # stand-in that carries no instrument gives the assertion, and
         # SATURATE left off gives the recorded `unset` beside it, which
         # is the form neither assertion can see.
         shadow=dict(extra=[('zzgl-a1g', FAKE_HALF),
                            ('zzgl-lookrts', FAKE_HALF),
                            ('zzgl-pair.txt', 'a stand-in pair note.\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts', 'WILDLOG': '1'},
         argv=['zzgl'],
         ok=V(has=['launch env: WILDLOG=1 SATURATE=unset',
                   'carries no @@wild stamps',
                   'would be uninstrumented']),
         bug=V(has=['gate begins'], hasnt=['launch env:'])),

    case('clean-legs-are-not-the-saturated-ones', 'run-alonelegs.sh', None,
         'the clean sweep was refused over the saturated legs beside it',
         # `-sat` is a suffix on the HALF's name, so the clean sweep's
         # relaunch guard globbed `$R-al-$H-*` and took `$R-al-$H-sat-*`
         # with it. The same over-matching prefix glob install-tables.sh
         # names for a half whose name begins with the basis's plus a
         # hyphen, one script over. Run 18 runs clean first and saturated
         # second, so the documented order never meets it and a RERUN of
         # either half's clean legs does.
         shadow=dict(extra=[('zzal-g912', FAKE_HALF),
                            ('zzal-al-g912-sat-cnn-slice-c32-r1.json', '[]\n'),
                            ('zzal-pair.txt', 'a stand-in pair note.\n')]),
         argv=['zzal', 'g912'],
         # Past the guard everything goes to the driver log, which is why
         # the probe is that log: an empty stdout alone would also be what
         # a driver that died before the redirect leaves. `shapes:` is
         # echoed past the baked-line check, so this is also the control
         # that a baked half gets through it: `start:` alone would pass an
         # unbaked stand-in too. Found 2026-08-23 by review.
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzal-al-g912-driver.log')).read(),
         ok=V(has=['start:', 'shapes: 3'],
              hasnt=['already has alone-leg artifacts',
                     'baked RTS line unread'])),

    case('alonelegs-refuses-a-previous-attempt', 'run-alonelegs.sh', None,
         "CONTROL: the guard still fires on the sweep's OWN artifacts",
         # The other side of the case above. Its fix narrows a glob, and a
         # narrowed glob that matches nothing at all would pass that case
         # and lose the guard outright -- these legs would then be
         # overwritten in place with nothing said, which is what the guard
         # exists to prevent.
         shadow=dict(extra=[('zzal2-g912', FAKE_HALF),
                            ('zzal2-al-g912-cnn-slice-c32-r1.json', '[]\n'),
                            ('zzal2-pair.txt', 'a stand-in pair note.\n')]),
         argv=['zzal2', 'g912'],
         ok=V(exit=1, has=['already has alone-leg artifacts'])),

    case('alonelegs-refuses-an-unbaked-half', 'run-alonelegs.sh', '3ebdb76',
         'a half without the baked RTS line ran all its legs under a DONE line',
         # The header says the line is read back before anything runs, and
         # it was -- into an echo that set no status, the one check in the
         # file that did not. So a half built without `-A32m -I0 -T -M8G`
         # ran its 24 legs at the default nursery and closed with
         # `DONE-ALONELEGS` and no complaint, the `!!` sitting in the driver
         # log where nothing reads it. The refusal is on stdout now, before
         # that log exists, so a refused attempt leaves nothing for the
         # relaunch guard to read as a previous one; the old script said it
         # inside the log, which is why the probe reads the log when there
         # is one.
         shadow=dict(extra=[('zzub-g912', FAKE_HALF_UNBAKED),
                            ('zzub-pair.txt', 'a stand-in pair note.\n')]),
         argv=['zzub', 'g912'],
         probe=lambda subs: (open(os.path.join(
             subs['at'], 'zzub-al-g912-driver.log')).read()
             if os.path.exists(os.path.join(
                 subs['at'], 'zzub-al-g912-driver.log')) else ''),
         ok=V(exit=1, has=['baked RTS line unread'],
              hasnt=['DONE-ALONELEGS', 'start:']),
         bug=V(has=['baked RTS line unread', 'DONE-ALONELEGS'])),

    case('alonelegs-refuses-a-listless-half', 'run-alonelegs.sh', '16e7b55',
         'a half listing nothing was refused inside the driver log it left',
         # The same shape as the unbaked refusal, one check down: it fired
         # after the redirect, so the refusal sat in a driver log nobody
         # reads, and the relaunch guard then read that log as a previous
         # attempt. Before the redirect now, on stdout, leaving nothing --
         # which the probe asks directly. Found 2026-08-23 by review.
         shadow=dict(extra=[('zzll-g912', FAKE_HALF_LISTLESS),
                            ('zzll-pair.txt', 'a stand-in pair note.\n')]),
         argv=['zzll', 'g912'],
         probe=lambda subs: 'driver log left: %s' % os.path.exists(
             os.path.join(subs['at'], 'zzll-al-g912-driver.log')),
         ok=V(exit=1, has=['--list gave nothing', 'driver log left: False']),
         bug=V(exit=1, has=['driver log left: True'],
               hasnt=['--list gave nothing'])),

    # ---- probe-areacurve.sh --------------------------------------------
    case('areacurve-exit-carries-its-complaints', 'probe-areacurve.sh', None,
         'a wrong count or a nonzero exit was echoed into the log, at exit 0',
         # Its checks mirror run-gate.sh's line for line and, alone among
         # the five drivers with them, set no BAD: six processes could come
         # out short or dead and the script ended `AREA CURVE COMPLETE` at
         # exit 0, every `!!` behind the redirect. A stand-in that runs
         # nothing is the short count. No bug verdict, and NEVER one: the
         # script before the fix cd'd to an absolute path and named its half
         # outright, so a shadow could not hold it -- run from one on
         # 2026-08-23 it ran HERE, on the real binary, and overwrote Run
         # 16's recorded -A8m artifacts. `shadow_dir` refuses such a
         # program now, and the two seams are what let this case exist.
         shadow=dict(extra=[('zzac-half', FAKE_HALF)]),
         env={'HALF': 'zzac-half', 'OUT': 'zzac-curve'},
         argv=[],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzac-curve-driver.log')).read(),
         ok=V(exit=1, has=['expected 15, got 0', 'WITH 6 COMPLAINT(S)'],
              hasnt=['AREA CURVE COMPLETE'])),

    case('areacurve-runs-clean-on-a-full-count', 'probe-areacurve.sh', None,
         'CONTROL: six processes at the full count end the curve at exit 0',
         shadow=dict(extra=[('zzac2-half', FAKE_AREA)]),
         env={'HALF': 'zzac2-half', 'OUT': 'zzac2-curve'},
         argv=[],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzac2-curve-driver.log')).read(),
         ok=V(exit=0, has=['AREA CURVE COMPLETE'], hasnt=['!!'])),

    case('areacurve-refuses-a-previous-attempt', 'probe-areacurve.sh', None,
         'CONTROL: the curve refuses to overwrite its own artifacts',
         # The guard the run drivers have and this one did not, which is
         # the whole of why the 2026-08-23 overwrite above could happen.
         shadow=dict(extra=[('zzac3-half', FAKE_AREA),
                            ('zzac3-curve-16m.json', '[]\n')]),
         env={'HALF': 'zzac3-half', 'OUT': 'zzac3-curve'},
         argv=[],
         ok=V(exit=1, has=['already has artifacts', 'zzac3-curve-16m.json'])),

    case('counts-file-says-it-was-restricted', 'run-counts.sh', None,
         'a smoke run left a counts file that read as a recorded column',
         # ONLY and ARMS are for a smoke run of this script and never for a
         # recorded column, and the file recorded neither -- so the two
         # artifacts differed by a line count and nothing else, a silent
         # cap in the one form this directory's rules refuse. What reads
         # the file later cannot see the environment that wrote it.
         shadow=dict(extra=[('zzct-g912', FAKE_HALF)]),
         env={'ONLY': 'shape-a', 'ARMS': 'list', 'N': '1'},
         argv=['zzct', 'g912'],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzct-counts-g912.txt')).read(),
         ok=V(has=['ONLY=shape-a ARMS=list', 'RESTRICTED'])),

    case('counts-file-says-a-full-sweep-was-full', 'run-counts.sh', None,
         'CONTROL: an unrestricted sweep says so rather than saying nothing',
         # The absence of a word is not what a reader should have to
         # notice, so the full sweep stamps `full` and the check above
         # cannot pass by the file simply being quiet.
         shadow=dict(extra=[('zzct2-g912', FAKE_HALF)]),
         env={'N': '1'},
         argv=['zzct2', 'g912'],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzct2-counts-g912.txt')).read(),
         ok=V(has=['N=1'], hasnt=['RESTRICTED'])),

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
             'the same run gives 0.54% and 0.31%',
             'the same run gives 0.74% and 0.31%'))},
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
         bug=V(has=['major run begins'], hasnt=['carries a hyphen'])),

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

    case('relaunch-guard-skips-the-riders', 'run-major.sh', '3ebdb76',
         "a relaunch was refused over the riders' files, which it never writes",
         # The guard globs `$R-*.json` and `$R-*.log` and excepted the
         # gate's, the one other writer of that prefix it knew; the alone-leg
         # riders are the other, `$R-al-*`, written AFTER the run at README's
         # step 19 -- so a relaunch after the riders, with the major JSONs
         # moved aside, met `already has artifacts` over files it would not
         # overwrite. read-all.sh's roster skips both, one script over.
         shadow=dict(extra=halves('zzrl-lookrts', 'zzrl-a1g')
                     + [('zzrl-pair.txt', 'a stand-in pair note.\n'),
                        ('zzrl-al-lookrts-cnn-slice-c32-r1.json', '[]\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzrl'],
         ok=V(exit=0, has=['major run complete'],
              hasnt=['already has artifacts']),
         bug=V(exit=1, has=['already has artifacts',
                            'zzrl-al-lookrts-cnn-slice-c32-r1.json'])),

    case('major-run-refuses-a-previous-attempt', 'run-major.sh', None,
         "CONTROL: the guard still fires on the run's OWN artifacts",
         # The other side of the case above: a narrowed exclusion that took
         # a process's JSON with the riders' would lose the guard outright,
         # and hours would be overwritten in place with nothing said.
         shadow=dict(extra=halves('zzrp-lookrts', 'zzrp-a1g')
                     + [('zzrp-pair.txt', 'a stand-in pair note.\n'),
                        ('zzrp-lookrts-rev.json', '[]\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzrp'],
         ok=V(exit=1, has=['already has artifacts', 'zzrp-lookrts-rev.json'],
              hasnt=['major run begins'])),

    case('major-run-wants-its-pair-note', 'run-major.sh', '3ebdb76',
         'a run without its note logged `!!` and went on, for read-all.sh to count',
         # The note carries the pair's recipe and the gate's verdict, which
         # the run copies into its log; without one the run logged `!! no
         # <note>` through log() and went on at exit 0 -- and read-all.sh
         # counts every stamped `!!` as a process complaint, with no carve-
         # out, so every later reading of that run failed as "the run
         # complained about itself" over eighteen clean processes. Refused
         # before the hours instead, as a missing binary is.
         shadow=dict(extra=halves('zznn-lookrts', 'zznn-a1g')),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zznn'],
         ok=V(exit=1, has=['no zznn-pair.txt'], hasnt=['major run begins']),
         bug=V(exit=0, has=['!! no zznn-pair.txt', 'major run complete'])),

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
         bug=V(has=['zzhg-lookrts-pa-rev.json --block'],
               hasnt=['is not a class name'])),

    case('install-refuses-a-hyphenated-lead', 'install-tables.sh', '3ebdb76',
         'a hyphenated lead slipped both patterns, and the block above took it',
         # The two patterns that find a class block here both read
         # `[a-z0-9]`, so a lead carrying a hyphen was missed by BOTH, they
         # agreed, and the cross-check written against exactly that failure
         # could not fire -- which run-major.sh's own comment had recorded
         # and nothing had acted on. The missed block then ran inside the
         # one above it and took its figures. Refused by name now, as
         # run-major.sh refuses the class.
         plant=lambda t: {'doc': edited_readme(
             t, ('**`bcastmid` ---', '**`bcast-mid` ---'))},
         shadow=dict(extra=whole_run(['lookrts'], prefix='zzhl')),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzhl'],
         # The old script's signature and not merely the absence of the
         # new refusal: the renamed block's own table install REFUSED, and
         # the computed paragraphs went in across SEVEN blocks, the eighth
         # having been handed the one above it.
         ok=V(exit=1, has=['carries a hyphen'], hasnt=['table(s) installed']),
         bug=V(exit=1, has=['REFUSED', 'across 7 class block(s)'],
               hasnt=['carries a hyphen'])),

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

    A program that cds to an ABSOLUTE path is not held by a shadow at all:
    it runs here, on the real binaries, writing the real artifacts. The
    old probe-areacurve.sh did, on 2026-08-23, when its first case was run
    against it before its fix, and five minutes of a new run overwrote Run
    16's recorded -A8m JSON and log before the case timed out. Refused
    here, as a fixture that cannot be built -- which is what `--against`
    or `--audit` meets for any revision of a script from before it got
    its `cd "$(dirname "$0")"`.
    """
    # The path quoted too: `cd "/home/..."` is the same escape and slipped
    # the first form of this. Found 2026-08-23 by review. Cases:
    # `shadow-refuses-an-absolute-cd`, `shadow-refuses-a-quoted-absolute-cd`
    # and `shadow-holds-its-own-directory`, asked of this function directly.
    if re.search(r'^\s*cd\s+["\']?/', text, re.M):
        raise AssertionError('%s cds to an absolute path, so a shadow cannot'
                             ' hold it and running it would run for real'
                             % prog)
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
    """{lineno: the innermost function it is in}, and None for module
    scope.

    Innermost, which `ast.walk` visiting the outer def first and a plain
    assignment buy: `setdefault` kept the outer, so a nested def's parse
    was the outer's and flagged whenever the outer ran at import, called
    or not. Found 2026-08-23 by review; the handled control plants it.
    """
    at = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for n in ast.walk(fn):
                at[getattr(n, 'lineno', 0)] = fn
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
    The helper form of the import-time parse is a case since 2026-08-22,
    `env-parse-through-a-helper`, with the handled form its control.
    """
    src = open(os.path.join(HERE, path)).read()
    tree = ast.parse(src)
    at, bad, note = _scopes(tree), [], []

    # A helper CALLED at module scope parses at import as surely as a
    # module-scope line does, and the guard read only the line's own
    # scope -- so align-as.py's `number()`, the very form this family was
    # counted from, passed, and the family had no live site in the tree: a
    # silent search. A parse inside a `try` is under a handler and is not
    # the family. Found 2026-08-22 by review.
    handled = set()
    for t in ast.walk(tree):
        if isinstance(t, (ast.Try, getattr(ast, 'TryStar', ast.Try))):
            handled.update(range(t.body[0].lineno,
                                 t.body[-1].end_lineno + 1))
    defs = {fn.name: fn for fn in ast.walk(tree)
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef))}

    def calls(node):
        # The calls a node MAKES when it runs: not those inside a def or
        # a lambda it merely defines, which run when called, if ever.
        for c in ast.iter_child_nodes(node):
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef,
                              ast.Lambda)):
                continue
            if isinstance(c, ast.Call):
                yield c
            yield from calls(c)

    # What runs at import: the module's statements but its defs, and but
    # the `if __name__ == '__main__'` block, which runs as a script and
    # not on import -- seeded from that block too, the first cut of this
    # put 91 of read-run.py's 102 defs at import, measured 2026-08-23 by
    # review. A class body does run, so it seeds; its methods do not. A
    # call made under a `try` is handled where it is made, so what it
    # calls is not at import unhandled on that account.
    at_import = set()
    todo = [s for s in tree.body
            if not isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not (isinstance(s, ast.If) and ast.unparse(s.test)
                     == "__name__ == '__main__'")]
    while todo:
        for n in calls(todo.pop()):
            name = getattr(n.func, 'id', None)
            if name in defs and name not in at_import \
                    and n.lineno not in handled:
                at_import.add(name)
                todo.append(defs[name])

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
        where = at.get(n.lineno)
        if (getattr(n.func, 'id', None) == 'int' and n.args
                and 'environ' in ast.unparse(n.args[0])
                and (where is None or where.name in at_import)
                and n.lineno not in handled):
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
    """Every family, over every Python program here. Names the site, not
    a count.

    The shell drivers are outside its reach, the families being shapes of
    a Python AST, and the ok line says so. The one shell family a review
    wanted -- a `!!` complaint that sets no status, three instances in
    three scripts on 2026-08-22 -- was measured rather than adopted: a
    window of three lines around each `!!`, read for `BAD=`, `exit` or a
    status assignment, missed two of the three and flagged two sound
    sites, the word `exit` inside an echoed string counting and a refusal
    four lines down not. Deciding it wants a shell parser, and a list that
    never empties is one nobody reads.
    """
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
              ' environment parse, over the %d Python file(s) here; the'
              ' shell scripts are outside an AST family\'s reach'
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
                        ' the source of every Python program here')
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
        print('the defect families, over this directory\'s Python source:')
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
            print('and the families over this directory\'s Python source:')
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
