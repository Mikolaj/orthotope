"""Every defect these scripts have had, planted again and refused again.

The records of this directory's defects, on the form `defect-cases.py`
describes and in the Python form `defect-load.py` allows -- a module, so the
fixtures stay callables that derive from the live documents and the story
of each case stays beside it as a comment. The shared tools run it:

    defect-cases.py .               # validate and report the records
    defect-run.py .                 # every case against the working tree
    defect-run.py --audit .         # every case against the code before its
                                    #   own fix, where it MUST fail
    defect-run.py -k install .      # the cases whose id or name matches
    defect-run.py --changed .       # only the cases whose own script differs
                                    #   from HEAD: what an edit owes, where
                                    #   the whole suite is four and a half
                                    #   minutes and one shell driver is
                                    #   fourteen cases
    defect-run.py --list .          # what is covered, and by which fix
    defect-run.py --at REV .        # diagnose some other revision
    ./properties.py                 # the properties, over every run on disk
    defect-lint.py .                # the defect families, over the source
    check-all .                     # all of it, in checks.py's order

The programs run HERE (`run_dir: here` in CONFIG below): both readers resolve
Main.hs and README.md from `__file__` and both shell drivers cd to their own
directory, so a copy run from anywhere else answers a different question --
which is how one proof was made worthless before this file existed. The
pre-fix program is materialised as ONE FILE beside today's neighbours
(`materialise: file`): a driver under test still calls today's
`./read-run.py`, exactly as the proofs did. So the suite plants files in
this directory and MUST RUN UNSANDBOXED from a session rooted elsewhere:
a session's sandbox permits writes under the repo it started in and nowhere
else, and every fixture that writes here dies on `Read-only file system`,
reported as a fixture that did not build.

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
`loop-offsets.py` guard `main()` behind `__name__`, so they
import clean and a record's `unit` evaluates against them (through `importlib`, the
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

WHAT THE RUN-FILE SPLIT COST IT, since a coverage loss nobody counted is
the kind this file exists against. Moving a run's write-up into
`runs/run<N>.md` on 2026-08-25 took 23 of these out of --audit at once,
each marked at its own site with which of four things its history cannot
take: a `--run-doc` no older reader accepts (13), a mode given no document
and defaulting to a README that no longer carries what it reads (3), a
fixture built from a document the era's copy is not (5), and a driver that
reads the split itself (2). The three-valued outcome is what made that
countable rather than quiet. Replaying the README of the day was tried
first and does not reach them: an era README carries era FIGURES, so a
fixture anchored on a figure this run published will not build against it,
which is the half the docstring below already calls loosely paired.

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
over DATA, quantified across every run on disk. `defect-lint.py` is discovery
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

import atexit
import hashlib
import importlib.util
import inspect
import json
import os
import re
import shutil
import subprocess
import tempfile
import zlib

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


# ---------------------------------------------------------------- fixtures

def readme_lines(rev=None):
    """This README, as of `rev` when a revision is being replayed.

    `--check-doc` resolves the `README.md#` anchors it finds in the
    READER'S OWN source, so a replayed revision carries the anchors of its
    day -- and the write-up steps rename headings, four in the
    pre-split chapters and two today. Run
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


def rundoc_lines(rev=None):
    """The run's own file, as of `rev` when a revision is being replayed.

    A head paragraph opening with a bolded backticked ARM name -- Run 23's
    file has two -- is neutralised, a space put after the two asterisks: an installer
    from before 34dadda read every such paragraph as a class block's lead
    and refused before reaching the defect a case planted (2026-09-02).
    The installer of today reads the class section alone and is untouched.
    """
    return rundoc_text(rev).split('\n')


def rundoc_text(rev=None):
    """The run file's text, every fixture's one source; see rundoc_lines."""
    rel = os.path.relpath(RUNDOC, HERE)
    text = open(RUNDOC).read() if rev is None else at_rev(rel, rev)
    head, sep, rest = text.partition('\n## The stride classes, run by run')
    head = re.sub(r'(?m)^\*\*`', '** `', head)
    return head + sep + rest


def write_rundoc(tmp, text, name=None):
    """A copy of the run file, KEEPING ITS NAME.

    `run<N>.md` is where the run number is written now -- no heading
    carries it -- so a copy called `R.md` reads as no run at all, and the
    checks that ask which run this is skip themselves over it.
    """
    return write(os.path.join(tmp, name or os.path.basename(RUNDOC)), text)


def edited_rundoc(tmp, *edits, **kw):
    """`edited_readme`, against the run's own file."""
    text = rundoc_text()
    for old, new in edits:
        k = text.count(old)
        if k != 1:
            raise AssertionError('anchor occurs %d times, need 1: %r'
                                 % (k, old[:60]))
        text = text.replace(old, new, 1)
    return write_rundoc(tmp, text, kw.get('name'))


def unwrapped_rundoc_edit(tmp, old, new):
    """`unwrapped_readme_edit`, against the run's own file."""
    text = subprocess.run(['wrap80', '--unwrap'], input=rundoc_text(),
                          capture_output=True, text=True, check=True).stdout
    k = text.count(old)
    if k != 1:
        raise AssertionError('anchor occurs %d times, need 1: %r'
                             % (k, old[:60]))
    return write_rundoc(tmp, text.replace(old, new, 1))


def runs_summary_row(tmp, shapes=None, short_by=None):
    """The cross-class summary's `runs` row, re-cut to SHAPES shapes.

    The count is DERIVED from the run file rather than written here: the
    `runs` class has grown three times (seven views, then eleven, then
    fourteen), and each time a fixture anchored on the old figure stopped
    building -- which is a silent search dressed as a case, the failure
    this file's own class-shape fixture was rebuilt in 2026-09-01 to
    escape. Anchoring on the row's SHAPE rather than on its value is what
    makes it survive the next growth. Added 2026-09-03, after Run 24 took
    the class to fourteen and broke both anchors at once.
    """
    if (shapes is None) == (short_by is None):
        raise AssertionError('give runs_summary_row exactly one of shapes'
                             ' and short_by')
    text = subprocess.run(['wrap80', '--unwrap'], input=rundoc_text(),
                          capture_output=True, text=True, check=True).stdout
    m = re.search(r'^\| `runs` \| (\d+) \|', text, re.M)
    if not m:
        raise AssertionError("no cross-class summary `runs` row in the run"
                             " file, so this fixture has no subject")
    want = shapes if shapes is not None else int(m.group(1)) - short_by
    return unwrapped_rundoc_edit(tmp, m.group(0),
                                 '| `runs` | %d |' % want)


DECLARED_AFTER_RE = re.compile(
    r'((?:`[\w.-]+`(?:,\s+(?:and\s+)?|\s+and\s+))*`[\w.-]+`)\s+(?:was|were)'
    r' added \d{4}-\d{2}-\d{2}, after the run')

DECLARED_RETIRED_RE = re.compile(
    r'((?:`[\w.-]+`(?:,\s+(?:and\s+)?|\s+and\s+))*`[\w.-]+`)\s+(?:was|were)'
    r' retired \d{4}-\d{2}-\d{2}, after the run')


def plant_retired_class_exempt(tmp):
    """The fixture of `retired-classes-timed-by-the-run-are-exempt`.

    Both halves planted, on a class every run file carries: a Main.hs copy
    retiring `rev` from timing, and a README declaring `rev` retired after
    the run -- so the newest run file, which timed it, is held to a class
    count that keeps it. Drop the declaration's effect and that file reads
    one block over. The declaration goes under the Provenance heading,
    which every README revision carries, so the anchor outlives the bullet
    a write-up rewrites. Added 2026-09-04.
    """
    main = open(MAIN).read()
    old = 'retiredClasses = ['
    if main.count(old) != 1:
        raise AssertionError('retiredClasses list occurs %d times, need 1'
                             % main.count(old))
    out = {'main': write(os.path.join(tmp, 'Main.hs'),
                         main.replace(old, old + '"rev", ', 1))}
    out['readme'] = unwrapped_readme_edit(
        tmp, '\n## Provenance\n',
        '\n## Provenance\n\n`rev` was retired 2026-09-04, after the run.\n')
    return out


def plant_retired_shape_exempt(tmp):
    """The fixture of `retired-shapes-timed-by-the-run-are-exempt`.

    Both halves planted, on a shape every run file times: a Main.hs copy
    retiring `vgg-14-c512-k3`, and a README declaring it retired after the
    run -- so the newest run file's `over N shapes` are held to a main set
    that keeps it. Drop the declaration's effect and every one of them
    matches no population. Planted under the Provenance heading, as the
    class fixture is. Added 2026-09-04.
    """
    main = open(MAIN).read()
    old = 'retiredShapes =\n  [ '
    if main.count(old) != 1:
        raise AssertionError('retiredShapes list occurs %d times, need 1'
                             % main.count(old))
    out = {'main': write(os.path.join(tmp, 'Main.hs'),
                         main.replace(old, old + '"vgg-14-c512-k3"\n  , ', 1))}
    out['readme'] = unwrapped_readme_edit(
        tmp, '\n## Provenance\n',
        '\n## Provenance\n\n`vgg-14-c512-k3` was retired 2026-09-04, after'
        ' the run.\n')
    return out


def plant_main_shapes_exempt(tmp):
    """The fixture of `main-shapes-added-after-the-run-are-exempt`.

    Both halves planted, and the figure derived rather than written: a
    declaration in README of two main-set shapes never added after any
    run, and a run file whose every `over N shapes` at the run's TRUE
    main-set size -- Main.hs's timed set less whatever the live README
    already declares added, plus what it declares retired -- is moved
    down by the two planted. So the fixture builds
    the same subject whether or not a real declaration stands, and a
    figure in it cannot go stale under a later main-set change, which the
    class sibling's hand-written 7 can.
    """
    main = open(MAIN).read()
    names = []
    for lst in ('convShapes', 'stretchShapes'):
        body = main.split('\n%s =\n' % lst, 1)[1].split('\n  ]', 1)[0]
        names += re.findall(r'\("([\w-]+)",\s*\[', body)
    readme = subprocess.run(['wrap80', '--unwrap'], input=open(README).read(),
                            capture_output=True, text=True, check=True).stdout
    declared = set()
    for m in DECLARED_AFTER_RE.finditer(readme):
        declared |= set(re.findall(r'`([\w.-]+)`', m.group(1)))
    # The run's TRUE population as the reader derives it: the timed main
    # set, less what README declares added after the run, plus what it
    # declares retired after it (2026-09-04, when eight shapes were).
    retired = _reader().retired_shapes(MAIN)
    declared_retired = set()
    for m in DECLARED_RETIRED_RE.finditer(readme):
        declared_retired |= set(re.findall(r'`([\w.-]+)`', m.group(1)))
    timed = [n for n in names if n not in retired]
    real = declared & set(timed)
    fake = [n for n in ('stretch-primes', 'stretch-inner256')
            if n in timed and n not in real]
    assert len(fake) == 2, 'the two planted shapes must be timed and undeclared'
    was = len(timed) - len(real) + len(declared_retired & retired)
    now = was - len(fake)
    doc = subprocess.run(['wrap80', '--unwrap'], input=rundoc_text(),
                         capture_output=True, text=True, check=True).stdout
    # README quotes the run's population too, so both documents move.
    pat = re.compile(r'\bover (all )?%d shapes' % was, re.I)
    assert pat.search(doc), 'the run file quotes no `over %d shapes`' % was
    down = lambda m: 'over %s%d shapes' % (m.group(1) or '', now)  # noqa: E731
    doc = pat.sub(down, doc)
    readme = pat.sub(down, readme)
    anchor = '## Provenance\n'
    assert readme.count(anchor) == 1
    readme = readme.replace(anchor, anchor + '\n`%s` and `%s` were added'
                            ' 2026-09-02, after the run.\n' % tuple(fake), 1)
    return {'readme': write(os.path.join(tmp, 'R.md'), readme),
            'rundoc': write_rundoc(tmp, doc)}


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


def rundoc_with_ragged_row(tmp):
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

    The table it plants in is now the run's OWN two halves and no earlier
    run's, the yardstick having been removed on 2026-08-29 once every run
    from 7 on had a file of its own. So this drops ONE cell where it used
    to drop two: a row a single cell short is as ragged as one five short
    and is what a hand-edited two-column table can actually suffer. The
    defect the docstring above describes is the wide table's and is kept
    because it is why the width pass exists.
    """
    lines = rundoc_lines()
    h = next(i for i, l in enumerate(lines) if l.startswith('| strategy |')
             and '(' in l)
    for i in range(h + 2, len(lines)):
        if not lines[i].startswith('|'):
            raise AssertionError('no data row found under the'
                                 " run's two-column table")
        cells = lines[i].split('|')[1:-1]
        if len(cells) > 2:
            lines[i] = '|' + '|'.join(cells[:1] + cells[2:]) + '|'
            break
    return write_rundoc(tmp, '\n'.join(lines))


def rundoc_without_class_table(tmp, cls='slice'):
    lines = rundoc_lines()
    i, j = class_table_span(lines, cls)
    del lines[i:j]
    return write_rundoc(tmp, '\n'.join(lines))


def rundoc_paired_run_aligned_only(tmp):
    """A copy naming one half aligned and no counterpart.

    The check this provokes had a control in the document until
    2026-08-29: the yardstick carried Run 10's aligned column beside its
    unaligned one, so the passing branch was a real pass and deleting one
    of them failed (re-proved 2026-08-11). Removing the yardstick took
    that control with it -- the run file now carries only this run's two
    halves, and no live run names a half aligned -- which left the branch
    a silent search. This is its control now, planted rather than found,
    and it is the whole reason the fixture exists.
    """
    lines = rundoc_lines()
    yard = [i for i, l in enumerate(lines)
            if l.startswith('| strategy |') and '(' in l]
    assert len(yard) == 1, 'two-column header: %d line(s)' % len(yard)
    h = lines[yard[0]]
    cells = h.split('|')
    hit = [k for k, c in enumerate(cells) if 'Run ' in c and '(' in c]
    assert len(hit) >= 2, 'header names %d halves, need a pair' % len(hit)
    cells[hit[0]] = re.sub(r'\(([^)]*)\)', '(SpecConstr, aligned)',
                           cells[hit[0]])
    cells[hit[1]] = re.sub(r'\(([^)]*)\)', '(SpecConstr, aligned)',
                           cells[hit[1]])
    lines[yard[0]] = '|'.join(cells)
    return write_rundoc(tmp, '\n'.join(lines))

def rundoc_yardstick_renamed_with_qmark(tmp):
    """The yardstick header renamed, and a `?` left in a published cell.

    The header is found by `check_doc`'s own rule, so this fixture cannot
    drift from the check it provokes.
    """
    lines = rundoc_lines()
    yard = [i for i, l in enumerate(lines)
            if l.startswith('| strategy |') and '(' in l]
    assert len(yard) == 1, 'yardstick header: %d line(s)' % len(yard)
    lines[yard[0]] = lines[yard[0]].replace('| strategy |', '| stratXgy |', 1)
    cell = re.compile(r'\| `[a-z0-9-]+` \| \d+ \| \d+ \| [\d.]+ [num]?s \|')
    fp = [i for i, l in enumerate(lines) if cell.match(l)]
    assert fp, 'no fingerprint row to plant a `?` in'
    lines[fp[0]] = re.sub(r'\| [\d.]+ [num]?s \|', '| ? |', lines[fp[0]], 1)
    return write_rundoc(tmp, '\n'.join(lines))


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


def rundoc_summary_row_short(tmp, cls='slice'):
    lines = rundoc_lines()
    at = [i for i, l in enumerate(lines) if l.startswith('| `%s` |' % cls)]
    assert len(at) == 1, 'summary row `%s`: %d line(s)' % (cls, len(at))
    cells = lines[at[0]].rstrip().rstrip('|').split('|')
    lines[at[0]] = '|'.join(cells[:-1]) + '|'
    return write_rundoc(tmp, '\n'.join(lines))


def readme_with_trailing_buried_action(tmp):
    return write(os.path.join(tmp, 'R.md'), open(README).read()
                 + '\n## A trailing checklist\n\n'
                   '    # then run ./read-run.py --survey to see it\n'
                   '    echo hello\n')


def readme_with_a_pointer_and_a_buried_action(tmp):
    """A trailing block holding one `why:` pointer and one real burial.

    The pointer must be passed over and the action beside it reported, so
    the exemption is shown to be a hole of exactly one shape rather than
    an off switch for the sweep.
    """
    return write(os.path.join(tmp, 'P.md'), open(README).read()
                 + '\n## A trailing checklist\n\n'
                   "    #      why: --para 'Then confirm the regime'\n"
                   '    # then run ./read-run.py --survey to see it\n'
                   '    echo hello\n')


def unwrapped_readme_edit(tmp, old, new, *more):
    """`edited_readme`, but against the README's UNWRAPPED form.

    `more` takes further (old, new) pairs flat, for a defect that only
    exists when SEVERAL sites move together -- the A/A population agreeing
    with itself and disagreeing with the roster is the case that wanted it,
    and one edit cannot express it.

    An anchor of more than a few words cannot survive in the wrapped file:
    a line break lands inside it and the literal match silently finds
    nothing. That is not hypothetical here -- this helper exists because
    `the same run gives 0.49% and 0.29%` matched while README.md sat
    unwrapped mid-write-up and stopped matching the moment the commit hook
    wrapped it back, turning a passing case into FIXTURE DID NOT BUILD on a
    document nobody had touched. Unwrapping first makes the anchor's
    fortunes independent of how the file happens to be wrapped, which is
    what every other search here is already told to do; the copy is written
    unwrapped, which the wrap gate reads as mid-edit and passes.
    """
    text = subprocess.run(['wrap80', '--unwrap'], input=open(README).read(),
                          capture_output=True, text=True, check=True).stdout
    pairs = [(old, new)] + list(zip(more[::2], more[1::2]))
    for o, w in pairs:
        n = text.count(o)
        if n != 1:
            raise AssertionError('anchor occurs %d times, need 1: %r'
                                 % (n, o[:60]))
        text = text.replace(o, w, 1)
    return write(os.path.join(tmp, 'R.md'), text)


def _mkruns(tmp):
    """A `runs/` under `tmp`, which is where a run file has to sit.

    The reader finds the run before this one beside it, so a fixture that
    wrote one run file into `tmp` itself would be asking a question about
    a directory the case does not control.
    """
    at = os.path.join(tmp, 'runs')
    os.makedirs(at, exist_ok=True)
    return at


def readme_link_to_an_older_run(tmp):
    """A copy whose links into the run file name the run BEFORE this one.

    Built by renumbering, not by spelling a path out, so it keeps working
    at every run. `runs/` accumulates, so the older file is really there
    and the link really resolves -- which is the whole difficulty: the
    dead-anchor check cannot see it and the browser renders it.
    """
    was = os.path.basename(RUNDOC)
    now = int(re.match(r'run(\d+)\.md$', was).group(1))
    text = open(README).read()
    k = text.count('runs/' + was)
    assert k, 'no link into %s to renumber, so this fixture plants nothing' % was
    return write(os.path.join(tmp, 'R.md'),
                 text.replace('runs/' + was, 'runs/run%d.md' % (now - 1)))


def readme_deliberate_link_wrapped(tmp):
    """A copy carrying a DELIBERATE link into the run before, whose text
    names that run across a line break -- `[Run\n  22's file](runs/run22.md)`
    -- which is the form the wrapped document actually holds.

    The exemption for such links reads the run's name out of the text, and
    read on the wrapped file it saw `Run` at one line's end and `22` at the
    next's start, so a link the write-up placed on purpose failed the check
    the moment the Stop hook rewrapped the file (Run 23, 2026-09-02).
    """
    was = os.path.basename(RUNDOC)
    now = int(re.match(r'run(\d+)\.md$', was).group(1))
    text = open(README).read()
    para = ("\nThe account is in [Run\n  %d's own file](runs/run%d.md), kept"
            " for good.\n" % (now - 1, now - 1))
    return write(os.path.join(tmp, 'R.md'), text + para)


def readme_six_pair_perturbed(tmp):
    """A copy of README whose six-pair sentence quotes a first figure no
    other site does, found by the sentence's shape rather than by the
    run's figure -- `the same run gives **X% and Y%**` -- so that the
    fixture follows the requote instead of failing to build after it."""
    text = open(README).read()
    flat_text = subprocess.run(['wrap80', '--unwrap'], input=text,
                               capture_output=True, text=True,
                               check=True).stdout
    ms = re.findall(r'the same run gives \*\*([\d.]+)% and ([\d.]+)%\*\*',
                    flat_text)
    assert len(ms) == 1, ('the six-pair sentence occurs %d times, need 1'
                          % len(ms))
    x, y = ms[0]
    old = 'the same run gives **%s%% and %s%%**' % (x, y)
    new = 'the same run gives **%.2f%% and %s%%**' % (float(x) + 0.30, y)
    return write(os.path.join(tmp, 'R.md'), flat_text.replace(old, new, 1))


def rundoc_results_names_identical_predecessor(tmp):
    """The run file with a sentence in Results naming the predecessor's
    basis half as identical, `is run<N-1>-g912 byte for byte` -- the form
    a repetition run writes on purpose and the check used to read as a
    stale name."""
    was = os.path.basename(RUNDOC)
    now = int(re.match(r'run(\d+)\.md$', was).group(1))
    text = rundoc_text()
    old = '## Results'
    assert text.count(old) == 1
    new = ('## Results\n\nThis basis is run%d-g912 byte for byte, the md5'
           ' says.\n' % (now - 1))
    return write_rundoc(tmp, text.replace(old, new, 1))


def rundoc_with_todo_marker(tmp):
    """The run file with one deferred paragraph left as `[[TODO]]`."""
    text = rundoc_text()
    old = '## Results'
    assert text.count(old) == 1
    return write_rundoc(tmp, text.replace(old, '## Results\n\n[[TODO]]\n', 1))


def rundoc_pair(tmp, held=True):
    """Two run files in one directory: this run's, and a predecessor.

    The previous-run check is a DIFF BETWEEN TWO FILES, so its fixture is
    two of them. `held` makes the predecessor this run's file verbatim,
    which is the state a write-up that made the file and stopped is in --
    every figure-bearing paragraph of the head the run before's. Without
    it the predecessor's leads are marked, so no key matches and nothing
    is held; the newer file is byte-identical in both, so the two cases
    differ in the predecessor alone and every other check reads the same
    document either way.

    What this replaces is a copy of the COMMITTED README with its chapter
    heading renumbered -- the only way to build the state while both runs
    shared one file, and one that stopped being buildable the hour a
    chapter was rewritten.
    """
    at = os.path.join(tmp, 'runs')
    os.makedirs(at, exist_ok=True)
    text = rundoc_text()
    m = re.match(r'run(\d+)\.md$', os.path.basename(RUNDOC))
    assert m, 'the run file is not named run<N>.md, so it names no run'
    now = int(m.group(1))
    was = text
    if not held:
        head, sep, rest = text.partition('\n## ')
        assert sep, 'the run file has no `## ` section to end its head at'
        marked, k = re.subn(r'(?m)^\*\*', '**zz-previous-run: ', head)
        assert k, 'no bolded lead in the head to mark, so the control'\
                  ' would be the held case over again'
        was = marked + sep + rest
    write(os.path.join(at, 'run%d.md' % (now - 1)), was)
    return {'rundoc': write(os.path.join(at, 'run%d.md' % now), text)}


def rundoc_pair_with_address_paragraph(tmp):
    """`rundoc_pair` held, plus a head paragraph carrying no decimal.

    The staleness check reads the head through `FIGURE_RE`, which matches
    a decimal and nothing else -- not a hex address, not a byte count, not
    a count spelled in words. Run 24 met that: it replaced every one of
    the twenty paragraphs the check named and three MORE were still the
    run before's, carrying `0x4205aa`, `2408930 bytes` and `23 of 24`
    between them, and only the end-to-end read found them. The head is
    replaced WHOLE every run, so nothing about it should be filtered by
    what kind of figure a paragraph happens to carry. Added 2026-09-03.
    """
    made = rundoc_pair(tmp, held=True)
    para = ('**zz-address-only, a head paragraph whose figures are an'
            ' address and a count.** The tracked loop sits at 0x425540'
            ' and its group at 2408930 bytes, on 23 of 24 shapes.\n\n')
    at = os.path.dirname(made['rundoc'])
    for name in sorted(n for n in os.listdir(at)
                       if re.match(r'run\d+\.md$', n)):
        path = os.path.join(at, name)
        text = open(path).read()
        head, sep, rest = text.partition('\n## ')
        assert sep, '%s has no `## ` section to end its head at' % name
        write(path, head + '\n\n' + para.rstrip('\n') + '\n' + sep + rest)
    return made


def rundoc_registration_with_verdicts(tmp):
    """A registration section shaped as a written-up run leaves it.

    The mode reads from the registration HEADING to the next `## `, which
    after post-run step 5's third act holds the registration paragraph AND
    a verdict paragraph per item -- so every item is found twice, its span
    counted twice, and an item whose span sits in the registration is
    listed as having none because the verdict paragraph repeating its
    number has none. Run 24 read eleven entries for six items. The mode
    runs before the verdicts are written, so the procedure never met it;
    what it costs is that the mode cannot be re-run as a cross-check
    afterwards, which is the one thing a second pass would want it for.
    Added 2026-09-03.
    """
    doc = ('# Run 99 (fixture)\n\n'
           'A head paragraph.\n\n'
           '## What this run was built to answer, and what it answered\n\n'
           '(1) *The first.* `predict: cross list 1.0 within 99%` and a'
           ' kill condition. (2) *The second.* No span here.\n\n'
           '(1) *The first.* **HELD**, the verdict paragraph.\n\n'
           '(2) *The second.* **HELD**, the verdict paragraph.\n')
    return {'rundoc': write_rundoc(tmp, doc, name='run99.md')}


def rundoc_current_run_sentence(tmp):
    """A verdict sentence attributing a figure to the run in hand.

    Its own PARAGRAPH, under the claim's lead, because the sweep reads a
    paragraph at a time and splits it into sentences: appended to the lead
    LINE, which is where this fixture started, the sentence lands inside
    another one and the figure is never reached.
    """
    ANCHOR = '**Claim 10 '   # RE-AIMED 2026-09-04, from claim 1, retired
    # that day by the prune with every rung below its top parked;
    # 2026-08-28 from claim 2, retired with its arm parked; and 2026-08-25
    # from claim 3, which retired at Run 19's write-up along with 4, 5 and
    # 9. The anchor has to be a claim the MANIFEST still carries, not
    # merely a heading the section still shows: with the claim gone from
    # `CLAIMS` the reader computes no reading for it, so the planted
    # sentence is never adjudicated and the figure never appears -- which
    # is how this case failed the hour the manifest shrank, and again on
    # 2026-08-28 and 2026-09-04 when a claim retired with its arms: the
    # sentence names the live claim's arm, so it reads as one about the
    # claim that is left.
    doc = rundoc_text()
    run = re.match(r'run(\d+)\.md$', os.path.basename(RUNDOC))
    assert run, 'the run file is not named run<N>.md, so it names no run'
    paras = doc.split('\n\n')
    at = [i for i, p in enumerate(paras) if p.startswith(ANCHOR)]
    assert len(at) == 1, '%s lead: %d paragraph(s)' % (ANCHOR, len(at))
    paras.insert(at[0] + 1, 'In Run %s, `mut-odo-vecdims-add-in-leaf-u2`'
                            ' reads 0.9312 against it.' % run.group(1))
    return write_rundoc(tmp, '\n\n'.join(paras))


def doc_of_a_list(tmp, items=4):
    """A document whose one list has no blank line between its items.

    Which makes it ONE paragraph, and `--replace` replaces paragraphs.
    Built rather than borrowed so the case does not move with the README's
    own lists.
    """
    body = '\n'.join('- `OPEN` **Item %d.** Its body, which is unique to it.'
                     % k for k in range(1, items + 1))
    return write(os.path.join(tmp, 'R.md'),
                 '# T\n\nA paragraph before it.\n\n%s\n\nA paragraph after'
                 ' it.\n' % body)


def doc_with_a_table(tmp):
    """A document of three sections, the middle one carrying a table."""
    return write(os.path.join(tmp, 'S.md'),
                 '# T\n\n## Header one\n\nProse one.\n\n## Middle\n\n'
                 'Prose before.\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n'
                 'Prose after the table.\n\n## Tail\n\nProse three.\n')


def doc_of_a_big_paragraph(tmp, n=1800):
    """A document whose middle paragraph is past `--delete`'s size bar."""
    return write(os.path.join(tmp, 'B.md'),
                 '# T\n\nBefore.\n\nA long one, %s end.\n\nAfter.\n'
                 % ('x' * n))


def doc_wrapped(tmp):
    """A document whose paragraphs are WRAPPED, as every committed one here is.

    The anchor modes are handed a phrase a caller read in the rendered
    prose; where the formatter's break falls inside it, matching the bytes
    finds nothing. Built rather than borrowed so the case does not move
    when the README is re-wrapped.
    """
    return write(os.path.join(tmp, 'W.md'),
                 '# T\n\nA paragraph whose sentence runs\nover a line break'
                 ' here.\n\nAnother paragraph.\n')


def doc_wrapped_list(tmp):
    """A wrapped list whose FIRST item runs over two lines."""
    return write(os.path.join(tmp, 'WL.md'),
                 '# T\n\n- `OPEN` **Item 1.** Its body, which is long\n'
                 '  enough to be wrapped.\n'
                 '- `OPEN` **Item 2.** Its body.\n\nAfter it.\n')


def one_item(tmp):
    """A replacement carrying ONE list item, as an edit to one would."""
    return write(os.path.join(tmp, 'new.txt'),
                 '- `OPEN` **Item 1.** Its body, rewritten.\n')


def whole_list(tmp, items=4):
    """A replacement carrying the whole list, as a caller replacing it would."""
    return write(os.path.join(tmp, 'new.txt'),
                 '\n'.join('- `OPEN` **Item %d.** Its body, rewritten.' % k
                           for k in range(1, items + 1)) + '\n')


def readme_of_leads(tmp):
    """A small document: three leads sharing a word, and one alone."""
    return write(os.path.join(tmp, 'R.md'), '\n\n'.join([
        '# T',
        '**Alpha the first.** Body one, which is unique to it.',
        '**Alpha the second.** Body two, which is unique to it.',
        '**Alpha the third.** Body three, which is unique to it.',
        '**Beta alone.** Body four, which is unique to it.',
    ]) + '\n')


def rundoc_retirement_sentence(tmp, retiring=True):
    """A claims paragraph quoting a figure the manifest cannot account for.

    Planted under the live claim's lead, the same anchor
    `rundoc_current_run_sentence` uses and for the same reason: it is a
    claim the manifest still carries, so the paragraph is adjudicated at
    all. The figure is the fixture's and is not read from the run.

    With `retiring`, the sentence is about a retirement, which is the
    state Run 19's write-up left eleven figures in -- a retired claim
    takes its pair out of the manifest, so the reading recorded as its
    epitaph is by construction unaccountable, and listing it reads a
    correct write-up as a defective one. Without, it is the same figure
    in an ordinary sentence, which must still be listed.
    """
    doc = subprocess.run(['wrap80', '--unwrap'], input=rundoc_text(),
                         capture_output=True, text=True, check=True).stdout
    paras = doc.split('\n\n')
    at = [i for i, x in enumerate(paras) if x.startswith('**Claim 10 ')]
    assert len(at) == 1, 'claim 10 lead: %d paragraph(s)' % len(at)
    sent = ('Claim 10 retires here, having last read 0.8271 against it.'
            if retiring else 'Claim 10 reads 0.8271 against it.')
    paras.insert(at[0] + 1, sent)
    return write_rundoc(tmp, '\n\n'.join(paras))


def readme_citing_dotfile(tmp):
    return edited_readme(tmp, ('\n## What is open',
                               '\nhorde-ad keeps its hlint exceptions in'
                               ' `.hlint.yaml`.\n\n## What is open'))


def rundoc_stale_basis_in_results(tmp):
    """The Results section naming a half of the run BEFORE this chapter's.

    Run 14's write-up shipped exactly this -- `run13-maxskip` standing in
    that lead while run14-lookrts's tables were installed under it -- past
    --lint, --check-doc, --selftest and --aa, none of which read the name.
    The plant is derived from the run file rather than spelled out, so it
    keeps working when the run number moves, and it asserts what it
    swept: a Results section naming no run, or naming two, would leave the
    check passing for its own reasons.
    """
    lines = rundoc_lines()
    start = next(i for i, l in enumerate(lines)
                 if re.match(r'#{1,6} Results\s*$', l))
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
    return write_rundoc(tmp, '\n'.join(lines))


def rundoc_naming_its_own_artifact(tmp):
    """The run file citing a path step 11 offers for deletion.

    Run 20 wrote "the superseded artifacts are parked as
    `probe-run20-exposed/`" into its own file and then KEPT the directory
    because the prose cited it, which is the dependency running backwards:
    the run file exists to outlive the artifacts. Derived from the live run
    file so the run number moves with it.
    """
    lines = rundoc_lines()
    cur = re.search(r'run(\d+)\.md$', RUNDOC).group(1)
    start = next(i for i, l in enumerate(lines)
                 if re.match(r'#{1,6} Results\s*$', l))
    lines.insert(start, 'The copies are in `probe-run%s-exposed/`.\n' % cur)
    return write_rundoc(tmp, '\n'.join(lines))


def rundoc_class_blocks(lines):
    """The run file's class block names, off its own leads.

    Derived and not listed, as `install-tables.sh` and `read-run.py` both
    derive them: a class added or renamed moves every fixture resting on
    this with it, where a literal rots at the next roster change and takes
    a case down during a write-up. One helper rather than a copy per
    planter, for the reason `read-run.py` gives about the third way of
    finding a class block being a third thing to keep in step.
    """
    cstart = next(i for i, l in enumerate(lines)
                  if re.match(r'#{1,6} The stride classes', l))
    return [m.group(1) for l in lines[cstart:]
            for m in [re.match(r'\*\*`([a-z0-9]+)` ---', l)] if m]


def rundoc_with_a_stray_class_lead(tmp):
    """A bolded class name at a line start, outside the class section.

    Which is how `install-tables.sh` locates a block, so one anywhere else
    is read as a further block with no table under it and the installer
    refuses naming a JSON that is present. Run 20's chapter head carried
    `**`reshape1` sits apart at 0.9995**`; unwrapped it sat mid-line and was
    harmless, and the wrap made it a line start.
    """
    lines = rundoc_lines()
    name = rundoc_class_blocks(lines)[0]
    start = next(i for i, l in enumerate(lines)
                 if re.match(r'#{1,6} Results\s*$', l))
    lines.insert(start, '**`%s` sits apart, a stray lead.**\n' % name)
    return write_rundoc(tmp, '\n'.join(lines))


def rundoc_with_a_stray_class_lead_in_provenance(tmp):
    """The same stray, planted AFTER the class section instead of before it.

    The sibling above plants one in the run file's opening, which the check
    read from the start. It stopped at the class section, so Provenance --
    the 153 lines after it, rewritten every run and naming the classes
    throughout -- went unread, while the check's own message said `outside
    the class section` and `install-tables.sh` grepped the whole file. This
    case is the half that was missing: planted both ways against the narrow
    form, the sibling was caught and this one was not.
    """
    lines = rundoc_lines()
    name = rundoc_class_blocks(lines)[0]
    start = next(i for i, l in enumerate(lines)
                 if re.match(r'#{1,6} Provenance\s*$', l))
    lines.insert(start + 2, '**`%s` sits apart, a stray lead.**\n' % name)
    return write_rundoc(tmp, '\n'.join(lines))


def rundoc_repeating_a_class_lead(tmp):
    """The same class leading twice INSIDE the class section.

    The stray sweep excludes that region on purpose, a bolded class-name
    lead being how a block legitimately starts there, so the predicate
    inside it is duplicate rather than stray. Both reach
    `install-tables.sh` the same way: its loose grep counts the repeat,
    `comm` leaves the name over, and it refuses with the `no
    run<N>-<basis>-*.json` message naming a file that is present. This is
    that defect reached from inside the section, where a stray planted
    outside it is what the sibling cases plant.
    """
    lines = rundoc_lines()
    name = rundoc_class_blocks(lines)[0]
    at = next(i for i, l in enumerate(lines)
              if re.match(r'\*\*`%s` ---' % re.escape(name), l))
    lines.insert(at + 2, '**`%s` sits apart, a repeated lead.**\n' % name)
    return write_rundoc(tmp, '\n'.join(lines))


def rundoc_miscounting_its_class_processes(tmp):
    """The class process count bent off one-per-class-per-half.

    A run spends one process per class per half, so the figure is the block
    count or twice it and nothing else. That is a structural truth, where
    the floor pair and the six-pair figure are cross-site agreement and can
    be uniformly stale -- which is why this is the one of Run 14's four
    wrong subjects that turned out checkable. The phrasing is what makes it
    so: `N class processes` reads `sixteen` in run19.md and run20.md alike,
    where bare `N processes` carries `eighteen`, `nine`, `four` and
    `fourteen` in run20.md alone, every one of them correct.
    """
    lines = rundoc_lines()
    n = len(rundoc_class_blocks(lines))
    # EVERY mention is bent, and to a digit, so this needs no word map and
    # no guess at which spelling the run used: what the check asks is that
    # the structural figure be quoted SOMEWHERE, so leaving one correct
    # mention standing would rightly pass. 2n+1 is outside {n, 2n} for
    # every n >= 1.
    # WHITESPACE-TOLERANT THROUGHOUT, because the document is WRAPPED and
    # the formatter puts its breaks where the width falls: a literal space
    # between `class` and `processes` bent one of run22.md's two mentions
    # and left the other, so the checker saw a correct figure, rightly
    # passed, and the case failed for a reason that was the fixture's.
    # Assert the count rather than `>= 1` for the same reason -- an
    # under-bent fixture must be loud where it was silent.
    want = len(re.findall(r'\b[\w-]+\s+class\s+processes\b',
                          '\n'.join(lines)))
    bent, k = re.subn(r'\b[\w-]+(\s+class\s+processes)\b',
                      r'%d\1' % (2 * n + 1), '\n'.join(lines))
    assert want and k == want, ('bent %d of %d class process count(s)'
                                % (k, want))
    return write_rundoc(tmp, bent)


def rundoc_naming_a_subset_of_its_class_processes(tmp):
    """A run that names a SUBSET of its class processes, which is legal.

    The count check asks that the structural figure be quoted somewhere,
    not that every quoted figure be it -- because a run has subsets to
    name. Run 20 reran four of its class processes; writing that as `those
    four class processes were rerun`, one word from what it does say, made
    an every-figure check fail on right prose. This plants such a sentence
    and the run must stay clean, which is the half a check like this gets
    wrong silently: a false positive on a correct document reads as the
    check working.

    The subset is INSERTED rather than found, and its size derived, so that
    the fixture outlives the run it was written against: the sentence it
    first bent, `Those four were rerun`, is in run20.md and in no other run
    file, and `RUNDOC` follows the newest.
    """
    lines = rundoc_lines()
    n = len(rundoc_class_blocks(lines))
    assert n >= 3, 'a subset smaller than the population needs n >= 3'
    at = next(i for i, l in enumerate(lines)
              if re.match(r'#{1,6} Provenance\s*$', l))
    lines.insert(at + 2, 'Those %d class processes were rerun on a quiet'
                         ' box.\n' % (n - 1))
    return write_rundoc(tmp, '\n'.join(lines))


def rundoc_without_class_leads(tmp):
    """Every class block lead unbackticked, so the grep finds none.

    `install-tables.sh` checks that no class is silently skipped by holding
    the JSONs on disk to the README's leads, and the check was itself silent
    when its own search came back empty.
    """
    src = rundoc_text()
    doc, n = re.subn(r'(?m)^\*\*`([a-z0-9]+)`', r'**\1', src)
    # A sweep, so it says what it swept: a plant that quietly matches
    # nothing -- or matches something else -- leaves the old script failing
    # for its own reasons and the audit certifying a non-vacuity nobody
    # demonstrated. The property is that leads existed and that none is
    # left, not how many there were.
    if not n or re.search(r'(?m)^\*\*`[a-z0-9]+`', doc):
        raise AssertionError('unbackticked %d lead(s) and %s remain' %
                             (n, 'some' if n else 'all'))
    return write_rundoc(tmp, doc)


def rundoc_heading_between_blocks(tmp):
    """A section, with a `Provenance:` paragraph, between two class blocks.

    `install-tables.sh` gives each block the range up to the next LEAD and
    stops at a heading for the last block only, so anything of that shape
    standing between two blocks is inside the range of the one above it.
    """
    paras = rundoc_text().split('\n\n')
    at = [i for i, x in enumerate(paras) if x.startswith('**`revsome`')]
    assert len(at) == 1, 'revsome lead: %d paragraph(s)' % len(at)
    paras[at[0]:at[0]] = ['### A section standing between two class blocks',
                          'Provenance: ZZMARKER, and this paragraph is'
                          ' nobody\'s to rewrite.']
    return write_rundoc(tmp, '\n\n'.join(paras))


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


def era_main(rev):
    """Main.hs as of `rev`, or today's when `rev` is None.

    The counterpart of `era_readme`, and it exists for the same reason:
    a fixture derived from this directory is only right for the code of
    its own era, and Main.hs cites README headings by anchor. Pairing
    today's source with an older document reads every anchor renamed
    since as dead -- `the-mutable-ceiling-taken` against that era's
    `the-mutable-ceiling-not-taken`, the rename that came with the
    decision to take the ceiling -- and a case replayed that way fails
    on the mismatch rather than on the defect it was written for.
    """
    return open(MAIN).read() if rev is None else at_rev('Main.hs', rev)


def era_main_file(tmp, rev):
    """`era_main` as a file a case can point `--main` at."""
    return write(os.path.join(tmp, 'era-Main.hs'), era_main(rev))


def mangled_main(tmp, rev=None):
    """A Main.hs whose roster the parser cannot find, of `rev`'s era."""
    return write(os.path.join(tmp, 'Main.hs'),
                 era_main(rev).replace('roster', 'r0ster'))


def run_json(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        raise AssertionError('no %s to build a fixture from' % name)
    return p


STUB_NOTE = """\
The pair run23-g912 and run23-spot, Run 23's, written by hand 2026-09-01

Half names [SAME]: g912 is the basis, spot the other.
HALVES: basis=g912 other=spot

ENTRY POINT FOR THE SESSION THAT RUNS THIS [PAIR'S]. Handover, not owed.

A CARRIED BLOCK [SAME]: the dead-spot form, run23-spot, spot alone, a
spot-check, hotspot and spotless.

GATE VERDICT, written by hand: SOUND. Handover, not owed.

Verified when built, 2026-09-01:
  md5 g912         deadbeef, a BUILD line and owed
  sequence         RUN in one window, which is that run's progress
                   and its continuation line
  --list           1320 on both, a BUILD line and owed
"""


def stub_pair_note(tmp):
    """A pair note carrying one of everything --note has to tell apart.

    Written rather than taken from a real note because the real ones are
    gitignored and go with their pair: a case built on run23-pair.txt
    would be a case that stops running the day the artifacts are offered.
    That is the DELETION decay, answered by re-aiming; era_main_hs below
    answers the other one, the main set growing under a captured run. The half named `spot` inside `dead-spot`, `spot-check`,
    `hotspot` and `spotless` is the point of the block: a rename bounded
    by `\\b` renames the FORM the pair varies, `-` being a word boundary.
    """
    return {'note': write(os.path.join(tmp, 'run23-pair.txt'), STUB_NOTE)}


def era_main_hs(tmp, run):
    """Main.hs with the main lists trimmed to the shapes a captured run has.

    The three cases below read a CAPTURED run through `--claims`, whose
    population gate holds the run to TODAY's main set and, when the run
    falls short, prints a note and reads nothing back. Two main-set shapes
    landed on 2026-09-02 for Run 24, which put every captured run on disk
    at 24 of 26 and turned that gate on: the two `has` cases went red and
    the `hasnt` case went VACUOUS, passing because every figure was
    suppressed rather than because the sentence exempted one. Re-aiming
    them at a newer run does not help -- no captured run can carry a shape
    added after it -- so what they pass is the era's main set as far as
    the run itself shows it, and no later addition can reach them.

    Trimming only REMOVES entries, so every shape the run does carry keeps
    its dims and its `l`. The assertion is the point: a trim that loses or
    keeps the wrong names would leave the gate firing for a new reason and
    the cases red for a reason nobody would look for.

    AND THE LIVE GATE STAYS AS IT IS, ruled 2026-09-03: it looked as
    though `--claims` should honour the declaration that the population
    sizes honour since d08d6a5, and it should not. The gap cannot arise
    where the procedure uses the mode -- post-run step 4a and
    install-tables.sh both point it at `$R-<basis>-main.json`, this run's
    own, built from today's Main.hs and carrying every shape by
    construction -- so the only thing that ever tripped it was a fixture
    aiming it at an older run, which is what this function is for. And
    the note-and-exit-0 path is load-bearing besides: smoke-sweep.sh runs
    `--claims` over the one-shape smoke run and wants exit 0, calling it
    the read-back's only pre-run exercise, so making the shape gap
    nonzero would fail the sweep. Do not re-propose it.
    """
    want = {r['reportName'].split('/')[0]
            for r in json.load(open(run))[2]}
    src = open(MAIN).read()
    got = set()
    for lst in MAIN_LIST_NAMES:
        head = '\n%s =\n' % lst
        i = src.index(head) + len(head)
        j = src.index('\n  ]', i)
        entries = re.split(r'\n(?=  [,\[] )', src[i:j])
        kept = [e for e in entries
                if (re.search(r'\("([\w-]+)",', e) or _NO).group(1) in want]
        assert kept, '%s: the run shares no shape with %s' % (run, lst)
        got |= {re.search(r'\("([\w-]+)",', e).group(1) for e in kept}
        kept[0] = re.sub(r'^  , ', '  [ ', kept[0])
        src = src[:i] + '\n'.join(kept) + src[j:]
    assert got == want, ('trimmed main set %s the run\'s: only here %s, only'
                         ' in the run %s' % ('is not', sorted(got - want),
                                             sorted(want - got)))
    return write(os.path.join(tmp, 'Main.hs'), src)


class _NoMatch:
    """A stand-in whose `group` is a name no shape list carries."""

    @staticmethod
    def group(_n):
        return ''


_NO = _NoMatch()

MAIN_LIST_NAMES = ('convShapes', 'stretchShapes')


def synth_json(tmp, pop='main', name=None, **kw):
    """One population as a file: `main`, or a class by name."""
    shapes = main_shapes() if pop == 'main' else class_shapes(pop)
    return synth_run(os.path.join(tmp, name or '%s.json' % pop), shapes, **kw)


def compared_arm_count():
    """How many arms a `--compare` of two synthetic runs puts in its table.

    The synthetic runs take their arms from Main.hs's roster, so a case
    asserting a count over them has to as well. Pinning the number is what
    `movers-count-disagrees-with-its-rows` did -- `3 of 42` -- and it went
    red the day Run 20's arms landed and the roster reached 45, on a mode
    that was answering correctly. A fixture derived from Main.hs and an
    expectation written out by hand are the same defect this file exists
    over, one on each side of the assertion.

    The count is the roster's timed arms less those with no corrected time
    to divide -- `sum-only` and the `-nosum` twins -- which is what
    `compare_table` drops, read through the reader's own `no_net` rather
    than restated here.
    """
    m = _reader()
    roster = m.roster_of(open(os.path.join(HERE, 'Main.hs')).read())
    return sum(1 for n, role, _fn in roster
               if role != 'Only' and not m.no_net(n))


def doc_expr(blocks):
    """A source expression for a document of `blocks`, newline-free.

    A `\\n` written into a case's argv passes through this file's own
    parse and arrives as a real newline inside the string literal the
    expression is built from, which is a syntax error rather than a
    failing case. Joining with chr(10) keeps every escape out of it.
    """
    sep = "+chr(10)+chr(10)+"
    return '(' + sep.join(repr(b) for b in blocks) + ')'


def synth_counts(tmp, name, ratio=1.0, refuse=(), extra_arms=(), n=50):
    """One half's `run-counts.sh` artifact, derived as `synth_run` is.

    The arms come from Main.hs's roster through the reader's own parser and
    the shapes from `main_shapes`, so a roster change moves this fixture
    with the run beside it rather than leaving a literal to rot. `ratio`
    scales every count, which is what a compiler emitting different code
    looks like to `perf`; `refuse` names `(shape, arm)` cells it could not
    count, written as the `!!` line the real artifact writes; `extra_arms`
    names arms the counts hold and no run times, which is the narrowing
    this file exists over.
    """
    m = _reader()
    main_hs = os.path.join(HERE, 'Main.hs')
    roster = m.roster_of(open(main_hs).read())
    arms = [a for a, role, _ in roster if role != 'Only'] + list(extra_arms)
    shapes = main_shapes()
    path = os.path.join(tmp, name)
    refused = {(s, a) for s, a in refuse}
    with open(path, 'w') as f:
        f.write('# %s %s N=%d 2026-01-01T00:00:00+00:00 full\n'
                % (name, '0' * 32, n))
        f.write('# shape arm N instructions/iter\n')
        for sh in sorted(shapes):
            for i, arm in enumerate(sorted(arms)):
                if (sh, arm) in refused:
                    f.write('!! %s %s perf refused this cell\n' % (sh, arm))
                    continue
                # A count per (shape, arm) that differs by arm, so that a
                # mode folding two arms together cannot read as correct.
                base = 1000000 + 1000 * i + 7 * len(sh)
                f.write('%s %s %d %d\n'
                        % (sh, arm, n, int(round(base * ratio))))
    return path


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


def rundoc_without_across(tmp):
    """The run file with every `Across the halves:` paragraph deleted: a
    run that recorded one half, as install-tables.sh must meet it."""
    paras = rundoc_text().split('\n\n')
    kept = [p for p in paras
            if not p.lstrip().lstrip('*').startswith('Across the halves:')]
    if len(kept) == len(paras):
        raise AssertionError('no `Across the halves:` paragraph in the run'
                             ' file to delete')
    return write_rundoc(tmp, '\n\n'.join(kept))


def an_across_paragraph():
    """One class block's `Across the halves:` paragraph, wrapped form.

    Named dynamically like a_registration_lead above: its figures are
    reinstalled with every run, so a pinned copy dies at the next
    install.
    """
    for p in rundoc_text().split('\n\n'):
        if p.lstrip().lstrip('*').startswith('Across the halves:'):
            return p
    raise AssertionError('no `Across the halves:` paragraph in the run file'
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


def deflation_legs(tag='runzzd', half='h', n=3, clean=True, sat=True,
                   at=None):
    """A run with BOTH rider sets beside it, clean and saturated.

    In HERE and swept with the rest, or under `at`, a directory that is
    not the cwd the cases run in, for the case that wants the legs found
    beside the run rather than beside the caller. Run 18 takes each shape's `list` alone twice -- `SAT=` off and on --
    because its registration 3 is a decomposition and not one ratio: the
    state is the saturated leg over the clean one and the rest is the
    roster cell over the saturated one. Two legs a shape is what makes
    that readable, and one is what makes it a hand-rolled subtraction in
    a write-up.
    """
    shapes = main_shapes()[:n]
    place = (lambda name: os.path.join(at, name)) if at else here_file
    run = place('%s-%s-main.json' % (tag, half))
    synth_run(run, shapes)
    for sh in shapes:
        if clean:
            synth_run(place('%s-al-%s-%s-r1.json' % (tag, half, sh)), [sh])
        if sat:
            synth_run(place('%s-al-%s-sat-%s-r1.json'
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


def corpus_of_two(tmp):
    """Two built main runs, for a limit that must count runs."""
    d = empty_corpus(tmp)['corpus']
    synth_json(d, 'main', name='a-main.json')
    synth_json(d, 'main', name='b-main.json')
    return {'corpus': d}


def corpus_with_an_unreadable_run(tmp):
    """One built run beside a JSON cut off mid-file, as a killed process
    leaves one."""
    d = corpus_of_one(tmp)['corpus']
    whole = open(os.path.join(d, 'main.json')).read()
    write(os.path.join(d, 'truncated-main.json'), whole[:len(whole) // 2])
    return {'corpus': d}


# The stand-in pair note, carrying the one machine line every driver reads
# since 2026-09-02: the halves, as pair-halves.sh reads them. The names are
# the ones every `halves()` call below uses.
NOTE_STUB = 'a stand-in pair note.\nHALVES: basis=lookrts other=a1g\n'

FAKE_HALF = """\
#!/bin/sh
# A stand-in for `$PREFIX-$half`, answering the two questions a driver asks
# before it commits the machine: what benches are there, and what RTS line
# is baked in. It runs none.
if [ "$1" = --list ]; then
  for s in shape-a shape-b shape-c; do
    for a in list bq-expand mut-odo-vecdims sum-only-early sum-only-late; do
      echo "$s/$a"
    done
  done
fi
# The class roster, which `classes --list` answers and `--list` does not:
# two classes so that a sweep restricted to one can be seen to have
# EXCLUDED the other rather than merely to have run.
if [ "$1" = classes ] && [ "$2" = --list ]; then
  for s in rev-shape-a rev-shape-b other-shape-a; do
    for a in list bq-expand mut-odo-vecdims sum-only-early sum-only-late; do
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

# And one listing nothing, which is the other wrong binary. BOTH listing
# branches go: a binary that lists nothing lists nothing, and stripping
# only the main-set one left the class roster answering, which is a
# half-listless stand-in nothing here wants. The assertion below is what
# caught that when the class branch was added.
FAKE_HALF_LISTLESS = FAKE_HALF.replace(
    'if [ "$1" = --list ]; then\n'
    '  for s in shape-a shape-b shape-c; do\n'
    '    for a in list bq-expand mut-odo-vecdims sum-only-early sum-only-late; do\n'
    '      echo "$s/$a"\n    done\n  done\nfi\n', '')
FAKE_HALF_LISTLESS = re.sub(
    r'# The class roster.*?^fi\n', '', FAKE_HALF_LISTLESS,
    flags=re.S | re.M)
assert 'shape-a' not in FAKE_HALF_LISTLESS, 'the listless stand-in kept it'

# The stand-in listing one arm more than the gate's SEL names, for the
# case that adds that arm to SEL: since 2026-09-04 the gate reads its list
# before the first process, so an arm the list lacks stops it there.
FAKE_HALF_WITH_OFFTAB = FAKE_HALF.replace('sum-only-late; do',
                                          'sum-only-late offtab; do')
assert FAKE_HALF_WITH_OFFTAB.count('offtab') == 2, 'the wider stand-in lost it'

# A gate recorded clean, as run-gate.sh writes its block's first two lines.
CLEAN_GATE = ('GATE: run 2026-09-02. Mechanically clean: four processes, each\n'
              '  exit 0 with the 15 benches asked for.\n')


def gate_md5_line(extra, run, basis='lookrts', other='a1g'):
    """The `halves md5:` line run-gate.sh writes into its block, computed
    over the stand-ins a case ships, so a note can carry a gate of exactly
    those binaries -- the one kind run-evening.sh inherits."""
    body = dict(extra)
    return '    halves md5: %s=%s %s=%s\n' % (
        basis, hashlib.md5(body['%s-%s' % (run, basis)].encode()).hexdigest(),
        other, hashlib.md5(body['%s-%s' % (run, other)].encode()).hexdigest())


def evening_fixture(run, md5=True, stale=False):
    """An evening's stand-ins and note, the note recording a clean gate.

    With `md5` the block names the stand-ins themselves, which is the
    block run-evening.sh inherits; with `stale` it names other binaries,
    the state a rebuild leaves; with neither it has no md5 line, as a
    block from before 2026-09-04.
    """
    hs = halves('%s-lookrts' % run, '%s-a1g' % run)
    line = ''
    if md5:
        line = gate_md5_line(hs, run)
        if stale:
            line = re.sub(r'=[0-9a-f]{32}', '=' + '0' * 32, line)
    return hs + [('%s-pair.txt' % run, NOTE_STUB + 'LAUNCH: SATURATE=1\n'
                  'RIDERS: clean\n' + CLEAN_GATE + line)]

# The status file run-evening.sh leaves behind, in the four states
# run-counts-all.sh reads it in: the riders landed and the machine handed
# back, the same with a complaint from the sequence, a stage still in
# flight, and an evening stopped before the sequence ever ran.
_EVENING_BEGINS = ('=== 2026-09-03T02:09:17+02:00 evening begins for the'
                   ' stand-in run\n')
_EVENING_HEAD = _EVENING_BEGINS + ('=== 2026-09-03T12:58:25+02:00 sequence:'
                                   ' done, rc=0\n')
_EVENING_FREE = ('=== 2026-09-03T13:15:02+02:00 RIDERS DONE AND THE MACHINE'
                 ' IS FREE: every stage exited 0\n')
EVENING_DONE = _EVENING_HEAD + _EVENING_FREE
EVENING_DONE_SORE = _EVENING_HEAD.replace(
    'sequence: done, rc=0',
    "sequence: done, rc=1 -- COMPLAINT, read zz-evening-out.txt under"
    " '##### sequence'") + _EVENING_FREE
assert 'COMPLAINT' in EVENING_DONE_SORE, 'the sore stand-in lost its complaint'
EVENING_MID_STAGE = _EVENING_HEAD + ('=== 2026-09-03T12:58:25+02:00 riders'
                                     ' a1g clean: start\n')
EVENING_STOPPED = _EVENING_BEGINS + (
    '=== 2026-09-03T02:54:41+02:00 EVENING STOPPED AT THE ALARM: 42.0% of'
    ' the CPUs non-idle over two seconds\n')

# A stand-in that RUNS: one `benchmarking` line per bench of the gate's own
# five-arm selection, for a driver that counts them against `--list`.
FAKE_AREA = """\
#!/bin/sh
for s in shape-a shape-b shape-c; do
  for a in list bq-expand mut-odo-vecdims sum-only-early sum-only-late; do
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
if [ "$1" = +RTS ] && [ "$2" = --info ]; then
  echo ' ,("Flag -with-rtsopts", "-A32m -I0 -T -M8G")'; exit 0
fi
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
# The preamble's line, for a case standing in a binary that carries it:
# printed when SATURATE reaches the process, as the real one prints it.
if [ -n "${FAKE_SATURATE:-}" ] && [ -n "${SATURATE:-}" ]; then
  echo "@@saturate dose=$SATURATE by=list sprayed=1000000 in 6.0 s"
fi
OUT=""; SHAPE=""; PATS=""; want=0
for a in "$@"; do
  [ "$want" = 1 ] && { OUT="$a"; want=0; continue; }
  case "$a" in --json) want=1 ;; -*|classes|glob) ;;
    *) SHAPE="$a"; PATS="$PATS $a" ;; esac
done
python3 - "$SRC" "$OUT" "$SHAPE" "$PATS" <<'ENDPY'
import fnmatch, json, sys
src, out, shape, pats = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split()
d = json.load(open(src))
if any('*' in p or '/' in p for p in pats):   # -m glob patterns, as the gate
    d[2] = [b for b in d[2]                    # and the riders select
            if any(fnmatch.fnmatch(b['reportName'], p) for p in pats)]
elif shape.endswith('-'):      # a prefix over a class's shapes, not a shape
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
# machine's own perf is deliberately NOT used by either case: a case
# leaning on it would pass or fail on the very state the guard exists to
# catch, so it would answer for the box and not for the guard.
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


def classes_in(text):
    """The classes a driver's own `CLASSES="..."` literal names, hyphenated
    ones dropped (they are the defect one case plants), or None where the
    text has no such literal, which lets `whole_run` take today's."""
    m = re.search(r'^CLASSES="([^"]*)"', text, re.M)
    if not m:
        return None
    return [c for c in m.group(1).split() if '-' not in c] or None


def halves(*names, classes=None):
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
            for n in names] + whole_run([n.split('-', 1)[1] for n in names],
                                        classes=classes)

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


# The dead-spot form's three shapes, each with a known answer worked by
# hand from the instruction sizes -- a case is a control only when its
# expected directive was derived without the code under test. A head
# reached by fall-through with a `jmp` before it: the loop is 10 B (4, 4,
# 2) at 4 B (1, 3) past the jump, so it straddles for the pad point at
# 51..59 and the pad those need is 5..13. A head behind an info table: the
# loop is 9 B (4, 3, 2) at 16 B past an `.align 8`, so it straddles when
# the align lands at 40, the pad point at 33..40, needing 24..31. A rotated
# pair, both loops 47 B (42 + 3 + 2; 3 + 2 + 40 + 2) and 42 B apart: the
# inner is resident for the pad point at 0..17 and the outer, which
# `overlapped` names, at 22..39, so the inner wins at residue 0 and the
# directive fires for 18..63, a pad of 1..46.
ASM_HEAD_AFTER_FALLTHROUGH = """\
\t.text
\t.globl\tgo
go:
\tmovq\t%rdi, %rax
\tjmp\t.Lgo
\tnop
.Lgo:
\ttestq\t%rax, %rax
.Lloop:
\taddq\t$1, %rax
\tcmpq\t$10, %rax
\tjne\t.Lloop
\tret
"""

ASM_HEAD_BEHIND_TABLE = """\
\t.text
\t.align 8
\t.quad\t1
\t.long\t30
\t.long\t0
.Lr_info:
.Lr:
\tmovq\t8(%rbp), %r14
\ttestb\t$7, %bl
\tjne\t.Lr
\tret
"""

ASM_ROTATED_PAIR = """\
\t.text
.Lstart:
\tjmp\t*(%rbp)
.Lin:
\t.skip\t42, 0x90
.Lout:
\tcmpq\t%r8, %rsi
\tjl\t.Lin
\t.skip\t40, 0x90
\tjmp\t.Lout
"""


def asm_fallthrough(tmp):
    return asm(tmp, ASM_HEAD_AFTER_FALLTHROUGH)


def asm_table(tmp):
    return asm(tmp, ASM_HEAD_BEHIND_TABLE)


def asm_pair(tmp):
    return asm(tmp, ASM_ROTATED_PAIR)


def emitted(subs):
    """Where the shim's directives landed, as one line per place worth
    asking about: after each unconditional jump, after `.text`, before
    each `.L` label. The verdict then names a place and what is there."""
    lines = open(subs['asm']).read().split('\n')
    out = []
    for k, l in enumerate(lines[:-1]):
        s, nxt = l.strip(), lines[k + 1].strip()
        if s.startswith('jmp') or s == '.text':
            out.append('after %s: %s' % (s, nxt))
        if nxt.startswith('.L') and nxt.endswith(':'):
            out.append('before %s %s' % (nxt, s))
    return '\n'.join(out)


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
    conv = sorted(sh for sh, d in dims.items()
                  if d['lst'] == 'convShapes' and not d.get('retired'))
    stretch = sorted(sh for sh, d in dims.items()
                     if d['lst'] == 'stretchShapes' and not d.get('retired'))
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
    hit = [p for p in rundoc_text().split('\n\n')
           if p.lstrip().startswith('**`%s` ---' % cls)]
    assert len(hit) == 1, 'lead `%s`: %d paragraph(s)' % (cls, len(hit))
    return hit[0]


def relead(tmp, cls, rewrite, name=None):
    """A copy of the run file with one class lead rewritten by `rewrite`.

    The lead is handed over UNWRAPPED, one line, because `lead_shapes`
    normalises whitespace before it reads and a plant that had to
    reproduce the wrap would be testing the wrapper. What comes back is
    written as the paragraph, and `edited_readme` asserts it replaced
    exactly one.
    """
    old = lead_of(cls)
    new = rewrite(' '.join(old.split()))
    assert new != ' '.join(old.split()), 'the rewrite changed nothing'
    return edited_rundoc(tmp, (old, new), name=name)


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


CLASS_SECTION = '## The stride classes, run by run'


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
                      rundoc_text(), re.M)
    assert len(rows) >= 4, 'class table floor column: %d row(s)' % len(rows)
    said = []
    for i, (cls, now) in enumerate(rows):
        if bend is not None and i == bend:
            now = now + '9'
        said.append('`%s` 1.11%%%s%s%%' % (cls, joiner, now))
    return ('**The floor column can be read against its predecessor\'s.**'
            ' All of them moved: ' + ', '.join(said) + '.')


def rundoc_with_floor_movement(tmp, **kw):
    """A copy carrying that paragraph, under the class section's heading.

    Placed right under the heading so it is inside the section the check
    reads and outside every class block, which is where the real one
    stood.
    """
    return edited_rundoc(tmp, (CLASS_SECTION + '\n',
                               CLASS_SECTION + '\n\n'
                               + floor_movement_para(**kw) + '\n'))


def rundoc_floor_movement_off_column(tmp):
    """One movement landing off the column, the rest right."""
    return rundoc_with_floor_movement(tmp, bend=0)


def rundoc_floor_movement_reshaped(tmp):
    """Every figure right and the shape the check matches on rewritten.

    What must not happen is a silent pass: keying the vacuity guard on
    the sentence's opening phrase was the first attempt, and rewording
    that phrase turned the whole check off.
    """
    return rundoc_with_floor_movement(tmp, joiner=' -> ')


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


def all_class_names():
    """Every stride class Main.hs defines, timed or retired, from its shape
    lists rather than from a literal.

    A class is a shape list that is not the main set, and its name is the
    shape prefix before the first hyphen -- the same derivation
    run-major.sh makes, and the one whose hyphen assumption it now refuses
    to let a class name break.
    """
    dims, _ = _reader().dims_by_shape(os.path.join(HERE, 'Main.hs'))
    return sorted({sh.split('-')[0] for sh, d in dims.items()
                   if d['lst'] not in ('convShapes', 'stretchShapes')})


def class_names():
    """The classes the binary TIMES: every class less Main.hs's
    `retiredClasses`, which `check` keeps and `classes --list` drops --
    so a stand-in answering that listing, and a driver's CLASSES held to
    it, model the binary. Since 2026-09-04."""
    retired = _reader().retired_classes(os.path.join(HERE, 'Main.hs'))
    return [c for c in all_class_names() if c not in retired]


def recorded_classes():
    """The classes the newest run file carries a block for, of Main.hs's.

    A class added to Main.hs ahead of its first run has no block in any
    run file yet, and install-tables.sh is right to refuse a JSON with no
    block -- so a fixture installed into the live run file models the run
    that file records and passes these, where a fixture a driver lists
    and launches models the next run and keeps `class_names()`, the
    default. Otherwise every install case fails from the day a class is
    added to the day it is first run. The leads are read as the installer
    reads them. Found 2026-08-28, when the `runs` class landed a run
    ahead of its file.
    """
    leads = set(re.findall(r'^\*\*`([a-z0-9]*)`', rundoc_text(),
                           re.M))
    return [c for c in all_class_names() if c in leads]


_WHOLE = {}


SRC = 'srcrun'      # the stand-ins' data, named OUTSIDE any run's own glob


def whole_run(halves_of, samples=2, prefix=SRC, short_class=None,
              classes=None):
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
    if classes is None:
        classes = class_names()
    key = (tuple(halves_of), samples, prefix, short_class, tuple(classes))
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
                     for c in classes]
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
        # EXCEPT WHERE THE BASE IS A `Force` BASE TOO: an in-situ row is
        # base minus `-nosum`, so dropping such a base takes the row with
        # it, and since the prune of 2026-09-04 every `Force` base is a
        # twin base -- the fixture then carried no in-situ row at all and
        # the old code had nothing to misread, the vacuous pass above by
        # another route. There the twin goes and the base stays: no pair
        # forms and the row survives.
        bases = {fn for _, role, fn in timed if role == 'Twin'}
        forced = {fn for _, role, fn in timed if role == 'Force'}
        kept, first_term = [], True
        for n, role, fn in timed:
            if role not in ('Twin', 'Force') and fn in bases - forced:
                continue
            if role == 'Twin' and fn in forced:
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
        # `list` is the ONLY arm a fingerprint holds, so a fixture that
        # dropped it has nothing to write. Two knobs here do: `no_twins`
        # takes it, `list` being a twin's base, and `drop_arms` can name it.
        # It used to fail as a KeyError carrying the first shape's name,
        # which names the shape and not the cause. 2026-08-23.
        missing = [sh for sh in shapes if sh not in fp_net]
        if missing:
            raise ValueError(
                'synth_run: fingerprint= needs a `list` net per shape and %d '
                'of %d have none, first %s -- `list` is dropped by '
                'no_twins=True, being a twin base, and by drop_arms naming it'
                % (len(missing), len(shapes), missing[0]))
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
    # THE RUN FILE GOES INTO THIS INDEX TOO. `added_lines` asks one
    # `ls-files --error-unmatch` of every document it reads and falls back
    # to its EVERYTHING sentinel if any is unknown -- so a run file this
    # throwaway index has never heard of turns the freshness sweep off,
    # and the case then reads a document with nothing marked NEW as a
    # defect. Measured 2026-08-25, before the first run file was
    # committed.
    for cmd in (('git', 'read-tree', 'HEAD'),
                ('git', 'add', os.path.basename(doc),
                 os.path.relpath(RUNDOC, HERE))):
        r = subprocess.run(cmd, cwd=HERE, env=env, capture_output=True,
                           text=True)
        assert r.returncode == 0, '%s: %s' % (cmd, r.stderr.strip())
    return {'doc': os.path.basename(doc), 'index': idx}


# ------------------------------------------------------------------- cases


def _takes_text(fn):
    """Whether a shadow's `extra` wants the script's text: one required
    positional, where a plant taking the revision has two."""
    return len([q for q in inspect.signature(fn).parameters.values()
                if q.default is q.empty]) == 1


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


def case(name, prog, fix, gist, argv, ok, bug=None, plant=None, env=None,
         probe=None, shadow=None, no_audit=None):
    """One defect, both ways round, as a record on the shared form.

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

    A plant taking a second parameter is handed the REVISION under test --
    None for the live tree -- because a fixture derived from this README is
    only right for the code of its own era. `readme_lines` says what goes
    wrong otherwise. A shadow takes the revision under test INTO the shadow,
    and the mutations are applied on top of it, so --audit reads the same
    latent defect the case was written for; the shadow's program is what
    the runner then invokes.

    The tier-1 fields come from TIER1 above, by name, and are null where
    it says nothing; `proved` is `ran` only where a bug verdict exists, the
    audit having watched it. `argv=None` is a record
    with no case, memory alone -- a defect whose program has since left this
    tree -- and `no_audit` names why the bug direction is not replayed, from
    the validator's vocabulary.
    """
    assert bug is None or fix, (
        '%s: a bug verdict wants the commit that fixed it, or --audit has'
        ' nothing to replay -- drop the bug to make it a control' % name)

    def plant_py(ctx):
        subs = {}
        if shadow is not None:
            subs['prog'] = os.path.join(
                shadow_dir(str(ctx.tmp), prog, ctx.text, **shadow), prog)
        if plant is not None:
            got = (plant(str(ctx.tmp), ctx.rev) if _takes_rev(plant)
                   else plant(str(ctx.tmp)))
            subs.update(got or {})
        return subs

    rec = {'id': name, 'program': prog, 'name': gist,
           'kind': 'defect' if fix else 'control'}
    if fix:
        rec.update(fix_rev=fix, family=None, trigger=None, ok=None, bug=None,
                   proved='ran' if bug else None, harm=None, discovery=None)
        rec.update(TIER1.get(name, {}))
    if no_audit:
        rec['no_audit'] = no_audit
    if argv is None:
        return rec
    if plant is not None or shadow is not None:
        rec['plant_py'] = plant_py
    if argv[:1] == ['--unit']:
        rec['unit'] = argv[1]
    else:
        rec['invoke'] = list(argv)
    if env:
        rec['env'] = dict(env)
    if probe is not None:
        rec['probe_py'] = probe
    for key, want in (('expect', ok), ('bug', bug)):
        if want is None:
            continue
        if want['exit'] is not None:
            rec[key + '_exit'] = want['exit']
        if want['has']:
            rec[key + '_text'] = list(want['has'])
        if want['hasnt']:
            rec[key + '_absent'] = list(want['hasnt'])
    return rec


def V(exit=None, has=(), hasnt=()):
    """A verdict: the exit code, what must be said, what must not."""
    return {'exit': exit, 'has': list(has), 'hasnt': list(hasnt)}


# ---------------------------------------------------------------- tier 1

# The tier-1 fields of every record with a fix, filled on 2026-09-02 by a
# reading of each case's gist, comment and verdicts against the closed
# vocabularies of `defect-cases.py`, and merged into the record by `case()`
# below. Kept apart from the case list so the list stays as it was written.
# `proved` is not here, with one exception: it is `ran` wherever a bug
# verdict exists, the audit having watched it, and a record with NO CASE
# has no audit to watch anything -- so where such a record's bug direction
# was seen in real use, this table carries the `proved` and says why. The families that were judgement calls were read
# a second time against their cases: two-spellings covers one quantity
# derived two ways at two sites (`claims-arm-counted-per-registration`,
# `ragged-gate-after-exclude`, `alloc-ceiling-over-the-named-cells`,
# `lead-order-mislabels-the-per-shape-line`, `gate-arms-track-the-selection`),
# false-comment a message naming a wrong remedy
# (`withheld-line-names-a-flag-that-is-not-one`), and
# guard-on-the-wrong-side a verdict living where nobody reads
# (`run-that-complained-does-not-gate-clean`,
# `launch-switches-recorded-whether-set-or-not`); a check that had not
# existed (`open-list-entry-without-a-status`) fits no family and is null.
# `harm` leans on the comment and the fix commit alone, so a defect that
# fired without either saying so reads as latent, and `harm_count` is given
# only where a number is written.
TIER1 = {
    # ---- the review of 2026-09-04 ----
    'gate-refuses-an-arm-its-list-lacks': dict(
        family='guard-on-the-wrong-side', discovery='review', harm='latent',
        trigger='SEL naming an arm --list does not carry, as build and'
                ' mut-odo were after 41d3bad',
        ok='refuses before the first process, naming the arm and its count',
        bug='ran the four processes and failed each on its count, after the'
            ' forty minutes'),
    'evening-does-not-inherit-a-gate-of-other-binaries': dict(
        family='unverified-state', discovery='review', harm='latent',
        trigger='a clean GATE block, then either half rebuilt',
        ok='runs the gate again, saying the block names other binaries',
        bug='inherited the block by its text alone'),
    'evening-does-not-inherit-an-untied-gate': dict(
        family='unverified-state', discovery='review', harm='latent',
        trigger='a clean GATE block without a halves md5 line',
        ok='runs the gate again, saying the block is untied',
        bug='inherited the block by its text alone'),
    'status-blocks-without-wrap80': dict(
        family='quiet-failure', discovery='review', harm='latent',
        trigger='wrap80 off PATH',
        ok='exits 2 saying BLOCKED and naming wrap80',
        bug='judged steps 10, 12a and 12c off an empty file and printed an'
            ' empty reason for step 7'),
    'status-counts-only-stamped-complaints': dict(
        family='scan-for-parse', discovery='review', harm='latent',
        trigger='a wallclock log quoting a FAILED GATE block',
        ok='counts the stamped `=== ... !!` lines alone',
        bug='counted the quoted line and read step 17 NOT DONE for ever'),
    'smoke-exercises-the-arm-filter': dict(
        family='vacuous-check', discovery='review', harm='fired',
        trigger='--exclude named an Only arm, bq-expand-b since c10e8cf',
        ok='excludes an arm the run lists, then every arm, whose refusal is'
           ' the check',
        bug='the filter removed nothing and the mode passed unexercised'),
    'predictions-block-without-wrap80': dict(
        family='quiet-failure', discovery='review', harm='latent',
        trigger='wrap80 off PATH, on a run named run<N>',
        ok='BLOCKED at exit 2, nothing adjudicated',
        bug='read the wrapped README, missed the lead and adjudicated the'
            ' run file\'s section at exit 0'),
    'predictions-alone-is-refused': dict(
        family='silent-option', discovery='review', harm='latent',
        trigger='--predictions without --compare',
        ok='refused as a modifier of --compare',
        bug='absorbed; the default table printed at exit 0'),
    'predictions-and-alloc-are-two-readings': dict(
        family='silent-option', discovery='review', harm='latent',
        trigger='--compare X --predictions --alloc',
        ok='refused as two readings of --compare',
        bug='--alloc dropped without a word'),
    'properties-limit-bounds-runs-not-figures': dict(
        family='vacuous-check', discovery='review', harm='fired',
        trigger='CORPUS_LIMIT=2, as the property mutants set it',
        ok='stops after that many runs and reports that many',
        bug='checked one figure, opened every run and reported them all'
            ' covered, so the fmt_abs mutant rested on a single figure'),
    'properties-name-an-unreadable-run': dict(
        family='quiet-failure', discovery='review', harm='latent',
        trigger='a JSON cut off mid-file in the corpus',
        ok='FAIL naming it unreadable, and not counted among the runs',
        bug='skipped silently and counted as a run covered'),
    'shadow-refuses-a-double-dash-cd': dict(
        family='scan-for-parse', discovery='review', harm='latent',
        trigger='`cd -- /path` in a driver', ok='refused as absolute',
        bug='held in a shadow, so the driver would have run for real'),
    'shadow-refuses-a-tilde-cd': dict(
        family='scan-for-parse', discovery='review', harm='latent',
        trigger='`cd ~/path` in a driver', ok='refused as absolute',
        bug='held in a shadow, so the driver would have run for real'),
    'shadow-refuses-a-home-cd': dict(
        family='scan-for-parse', discovery='review', harm='latent',
        trigger='`cd "$HOME/path"` in a driver', ok='refused as absolute',
        bug='held in a shadow, so the driver would have run for real'),
    'shadow-refuses-a-pushd': dict(
        family='scan-for-parse', discovery='review', harm='latent',
        trigger='`pushd /path` in a driver', ok='refused as absolute',
        bug='held in a shadow, so the driver would have run for real'),
    'era-judge-writes-the-shared-copy': dict(
        family='unverified-state', discovery='review', harm='latent',
        trigger='selftest-mutants.py running the era_main_hs judge before'
                ' the property judges',
        ok='plants the probe shape into a Main.hs of its own',
        bug='wrote the copy\'s Main.hs and restored nothing, so the later'
            ' judges read two zz-era-probe entries',
        # No case: a judge is driven by selftest-mutants.py alone.
        proved='ran',
        notes='Watched 2026-09-04: the old and the new judge each run once'
              ' in a fresh copy of the tracked files, with CORPUS at this'
              ' directory and CORPUS_LIMIT=2, and the copy\'s Main.hs'
              ' counted for zz-era-probe afterwards: one entry left by the'
              ' old, none by the new'),
    'mutants-name-a-property-without-one': dict(
        family='false-comment', discovery='review', harm='latent',
        trigger='reading mutants.py against properties.py',
        ok='a mutant per property, and properties.py points here',
        bug='"the three properties" over mutants for two, the third proved'
            ' by a dated sentence alone',
        proved='asserted'),
    'match-docstring-claims-any-length': dict(
        family='false-comment', discovery='review', harm='latent',
        trigger='reading --match\'s docstring against its body',
        ok='the docstring says the twin\'s loops are the survey\'s'
           ' population, capped at a line, which loses nothing',
        bug='claimed loops of any length were searched',
        proved='asserted'),
    'probe-cache-count-is-a-literal': dict(
        family='two-spellings', discovery='review', harm='latent',
        trigger='lib-stage2 parked to Only on 2026-09-04 with the probe'
                ' still naming it',
        ok='reads the class list before launching and refuses an arm it'
           ' lacks; WANT is what the list carries',
        bug='WANT=14 against a 12-bench run, failed after it ran',
        proved='asserted'),
    'draft-renames-a-half-onto-the-other': dict(
        family='other:rewrite-feeds-the-next-rewrite',
        discovery='review', harm='latent',
        trigger='--draft where the new basis reuses the old other name',
        ok='every rename in one pass, so nothing written is renamed again',
        bug='both halves of the carried-over note under one name, silently'),
    # ---- preflight.sh ----
    'preflight-names-a-retired-callee': dict(
        family='other:caller-left-behind', discovery='in-use', harm='fired',
        trigger='pre-run steps 8b to 8d, run at any time after 27580a5',
        ok='the three steps call defect-lint.py with the two linters,'
           ' properties.py and defect-run.py',
        bug='three FAILs reading `./check-scripts.py: No such file or'
            ' directory`, so the three steps had not run since 2026-09-02',
        # The one record that carries its own `proved`: it has no case, so
        # no audit watches its bug direction, and what did watch it is the
        # preparation that met the three FAILs. See the clause below.
        proved='ran', harm_count=1,
        notes='Watched 2026-09-02 at Run 24\'s preparation: the first'
              ' ./preflight.sh run24 printed 8b, 8c and 8d FAILing, two of'
              ' them quoting `./check-scripts.py: No such file or'
              ' directory` and 8c with an empty message, its grep for FAIL'
              ' finding none. One occurrence, that preparation, the steps'
              ' having been dark from 27580a5 until the repair the same'
              ' day. The three PASSed on the re-run.'),
    # ---- read-run.py, the first review's ----
    'install-lands-in-next-block': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a run doc whose class block carries no table of its own',
                      ok='refuses to write, the search bounded by the block',
                      bug='installed the rows over the next class table at exit 0'),
    'block-brief-cannot-install': dict(family=None, discovery='review', harm='latent',
                      trigger='--block --in-place --brief, the recommended combination',
                      ok='installs the table, --brief dropping it from the terminal only',
                      bug='exited 1 with "this mode emitted no table"'),
    'sunk-cell-costs-a-shape-not-a-row': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='a shape whose cell the forcing term does not leave positive',
                      ok='both columns carry a figure and the shortfall is said',
                      bug='worst_of skipped the non-positive test time_of has, a plausible worst beside time --'),
    'withheld-line-names-a-flag-that-is-not-one': dict(family='false-comment', discovery='in-use', harm='fired',
                      trigger='--check-doc --quiet with lines withheld',
                      ok='says rerun with --worklists',
                      bug='said rerun without --quiet, which withholds the same lines'),
    'deflation-with-no-legs-answers-anyway': dict(family='quiet-failure', discovery='generalisation', harm='latent',
                      trigger='--deflation on a run with no alone legs, a class JSON among them',
                      ok='refuses at exit 2 saying the riders were not taken',
                      bug='a header and a geomean over nothing at exit 0'),
    'deflation-ignores-the-saturated-legs': dict(family='quiet-failure', discovery='in-use', harm='fired',
                      trigger='both clean and sat- rider sets on disk',
                      ok='prints sat/clean and roster/sat beside the total',
                      bug='sat- legs keyed sat-<shape>, matched no shape and were dropped silently'),
    'deflation-legs-beside-the-run-not-the-cwd': dict(family='environment-decides', discovery='in-use', harm='fired',
                      trigger='a run named through a directory, from another cwd',
                      ok='finds the legs beside the run',
                      bug='globbed the cwd and said the riders were not taken with every leg on disk'),
    'claims-arm-counted-per-registration': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='--claims --exclude on an arm in several registrations',
                      ok='reports one arm',
                      bug='counted the arm once per registration while naming it once, eight for one'),
    'population-main-hs-does-not-define': dict(family=None, discovery='review', harm='latent',
                      trigger='a run whose shapes Main.hs no longer defines',
                      ok='refuses naming the undefined population',
                      bug='the unknown branch returned two fields of three and died unpacking'),
    'ragged-gate-after-exclude': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='--exclude of the one arm whose cells are missing',
                      ok='gates on the holes found after --exclude and reads the run',
                      bug='ragged flag computed before --exclude, refused at exit 2 printing 0 cells missing'),
    'in-place-alone': dict(family='silent-option', discovery='review', harm='latent',
                      trigger='--in-place with no installing mode',
                      ok='refuses at exit 2, --in-place is a modifier',
                      bug='printed a table, wrote nothing, exited 0'),
    # ---- a comparison narrowed in silence ----
    'chapter-names-the-shapes-it-dropped': dict(family='quiet-failure', discovery='generalisation', harm='latent',
                      trigger='--compare --chapter with the other half a shape short',
                      ok='names the shapes in one run only, skipped',
                      bug='computed the intersection and said nothing'),
    'alloc-names-the-shapes-it-dropped': dict(family='quiet-failure', discovery='generalisation', harm='latent',
                      trigger='--compare --alloc with the other half a shape short',
                      ok='names the shapes in one run only, skipped',
                      bug='named dropped arms and not shapes'),
    # ---- the sunk cell ----
    'selftest-survives-a-sunk-baseline': dict(family='domain-unchecked', discovery='audit', harm='latent',
                      trigger='a shape whose every arm is sunk, baseline net exactly 0',
                      ok='reports rows with no geomean to bracket, exit 1',
                      bug='divided by the baseline before the r <= 0 gate could look, ZeroDivisionError'),
    'selftest-names-a-zero-slope-cell': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='a cell with time slope exactly 0',
                      ok='the cell has no CI and --selftest names it',
                      bug='load() divided CI bounds by the slope, ZeroDivisionError in every mode'),
    'table-survives-a-zero-list-slope': dict(family='domain-unchecked', discovery='generalisation', harm='latent',
                      trigger='a list cell with slope 0 in the default mode',
                      ok='no share for the cell and the health warning names it',
                      bug='the share line divided by the slope, ZeroDivisionError'),
    'fingerprint-refuses-a-sunk-cell': dict(family='domain-unchecked', discovery='generalisation', harm='latent',
                      trigger='--fingerprint over a sunk cell',
                      ok='writes -- for the cell',
                      bug='divided and installed the figure, outliving the run'),
    'block-per-shape-refuses-a-sunk-cell': dict(family='domain-unchecked', discovery='generalisation', harm='latent',
                      trigger='--block per-shape line over a sunk cell',
                      ok='writes --/ for the cell',
                      bug='divided the sunk cell into the installed line'),
    'machine-check-drops-a-sunk-baseline': dict(family='domain-unchecked', discovery='generalisation', harm='latent',
                      trigger='--machine over a shape whose list net is not positive',
                      ok='drops the shape by name and says so',
                      bug='ValueError out of geomean, filed verbatim into the pair note by run-gate.sh'),
    # ---- read-run.py, the second review's ----
    'checkdoc-without-a-roster': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='--check-doc with a Main.hs it cannot parse',
                      ok='BLOCKED: no roster parsed, exit 1',
                      bug='if roster: with no else skipped five checks, ok lines, exit 0'),
    'checkdoc-open-list-out-of-order': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='the goal section placed above the open list',
                      ok='BLOCKED: the open list, exit 1',
                      bug='the sweep silently did not run, exit 0'),
    'checkdoc-paired-run-aligned-with-no-counterpart': dict(family=None, discovery='review', harm='latent',
                      trigger='a paired run whose yardstick columns are all named aligned',
                      ok='fails: a paired run publishes a column per half',
                      bug='the other half folded into one column passed'),
    'checkdoc-qmark-under-renamed-yardstick': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a renamed yardstick header over a published ? cell',
                      ok='still carry the ? is reported',
                      bug='the ? gate sat inside the yardstick block and was silently disabled'),
    'claims-current-run-not-exempt': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='a stale figure in a sentence naming the run in hand',
                      ok='the figure is read and listed',
                      bug='CLAIMS_PAST exempted any sentence naming a run, this one included'),
    # ---- read-run.py, later reviews' cases ----
    'insitu-worst-cell-label': dict(family='scan-for-parse', discovery='review', harm='fired',
                      trigger='--aa with one shape dropped from the in-situ ratios',
                      ok='says how many shapes are covered and which dropped',
                      bug='zipped ratios against the full list, every later ratio renamed'),
    'pair-refuses-a-sunk-cell': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='--pair over a sunk cell',
                      ok='refuses at exit 2, not readable',
                      bug='pair_stats divided nets unguarded, math domain error'),
    'compare-refuses-a-partial-other': dict(family='unverified-state', discovery='review', harm='latent',
                      trigger='--compare with the other half missing a cell',
                      ok='refuses at exit 2 naming the missing cells',
                      bug='indexed the other run without a hole gate, KeyError'),
    'summary-row-width': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='a summary row a column short of its header',
                      ok='says the row is not checked and why',
                      bug='zip stopped at the shortest, the tail compared against nothing'),
    'two-modes-at-once': dict(family='silent-option', discovery='review', harm='latent',
                      trigger='--markdown --fingerprint together',
                      ok='refuses at exit 2, one mode at a time',
                      bug='if/elif ran the first and dropped the second silently'),
    'fmt-abs-above-its-top-unit': dict(family='two-spellings', discovery='property', harm='latent',
                      trigger='a per-call time past 1000 s',
                      ok='writes 1500 s',
                      bug='%.3g wrote 1.5e+03 s, which FINGERPRINT_ABS_RE cannot read back'),
    'fmt-abs-at-the-unit-boundary': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='a time from 999.5 us up',
                      ok='writes 1 ms',
                      bug='wrote 1e+03 us, which --machine dropped in silence'),
    'alloc-fit-on-an-unknown-shape': dict(family='error-as-value', discovery='review', harm='latent',
                      trigger='a shape with no alloc fit in the run',
                      ok='the allocated R2 warning still fires',
                      bug='a missing alloc read as allocated nothing, silencing the warning'),
    'markdown-installs-into-the-main-table': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='--markdown --in-place on a run whose population Main.hs does not define',
                      ok='refuses at exit 1 naming the undefined population',
                      bug='kind != class chose the main header, kind == class narrowed nothing, rows installed over Results'),
    'selftest-survives-a-sunk-cell': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='--selftest over a sunk arm cell',
                      ok='names the work the arm removed, exit 0',
                      bug='math domain error inside winsorize and no verdict at all'),
    'aa-survives-a-sunk-cell': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='--aa over a sunk cell',
                      ok='prints the calibration',
                      bug='died with math domain error where --claims refuses'),
    'aa-lists-controls-under-no-controls': dict(family=None, discovery='review', harm='latent',
                      trigger='--aa --no-controls',
                      ok='refuses at exit 2, --no-controls drops the controls',
                      bug='reported a file of controls as having no control pairs'),
    'blocked-message-names-the-file': dict(family=None, discovery='review', harm='latent',
                      trigger='--check-doc with an unparsable Main.hs',
                      ok='names Main.hs by path',
                      bug='printed the contents of Main.hs where its path belonged'),
    'pair-refusal-names-shape-first': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='--pair refusing a sunk cell',
                      ok='names shape/arm like every other line',
                      bug='named arm/shape'),
    'alloc-ceiling-over-the-named-cells': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='--compare --alloc with agreeing and disagreeing cells',
                      ok='ceiling is the max over the cells the sentence names',
                      bug='ceiling was a max including cells the sentence excludes'),
    'dropped-control-pairs-are-named': dict(family='quiet-failure', discovery='audit', harm='latent',
                      trigger='--block over a run with a sunk control pair',
                      ok='says which control pairs are not readable',
                      bug='the intervals count narrowed with nothing in the installed text saying so'),
    'controls-survive-a-negative-term': dict(family='domain-unchecked', discovery='generalisation', harm='latent',
                      trigger='--block over a sum-only cell with a negative term',
                      ok='says the halves agreement cannot be carried',
                      bug='the second sum-only site was unguarded, math domain error in paired_ci'),
    'properties-buries-its-verdict-in-the-readers-stderr': dict(family=None, discovery='review', harm='latent',
                      trigger='--properties over a corpus of runs with dropped rows',
                      ok='withholds reader warnings and counts them by kind',
                      bug='258 warning lines buried six lines of verdict'),
    # ---- this file's own instruments ----
    'tree-check-that-could-not-run': dict(family='vacuous-check', discovery='generalisation', harm='latent',
                      trigger='a git that fails during the tree check',
                      ok='fails saying the check did not happen',
                      bug='empty status before and after matched, guarantee passed unchecked'),
    'tree-change-in-both-directions': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a case that removes a file from the tree',
                      ok='names what left and what arrived, each marked',
                      bug='printed the alarm with nothing beneath it, additions only being listed'),
    'shadow-refuses-an-absolute-cd': dict(family='unverified-state', discovery='in-use', harm='fired', harm_count=1,
                      trigger='a program with cd /absolute run from a shadow',
                      ok='shadow_dir refuses, cds to an absolute path',
                      bug='built the shadow and the program ran here on the real artifacts'),
    'shadow-refuses-a-quoted-absolute-cd': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='cd "/absolute" in quotes',
                      ok='refused like the bare form',
                      bug='the pattern read cd / alone and the quoted form slipped it'),
    'fixture-ci-bounds-are-criterion-shaped': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='any synthetic run cell',
                      ok='both CI deviations positive, CI% 1.0000',
                      bug='negative lower bound gave CI% 0 everywhere, the column untested by every fixture'),
    'env-parse-through-a-helper': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='int(environ) inside a helper called at module scope',
                      ok='the lint follows calls made at import',
                      bug='only module-scope lines were read, the family had no live site'),
    # ---- the write-up's derived sources ----
    'lead-drops-a-shape': dict(family=None, discovery='in-use', harm='fired', harm_count=5,
                      trigger='a class lead naming fewer shapes than the run carries',
                      ok='--block says the lead does not name the shape',
                      bug='nothing compared the lead to the run beneath it'),
    'lead-order-mislabels-the-per-shape-line': dict(family='two-spellings', discovery='generalisation', harm='latent',
                      trigger='a lead listing its shapes out of run order',
                      ok='--block says the lead lists them in another order',
                      bug='the per-shape line was labelled by the lead order and installed in run order'),
    'lead-figures-disagree-with-main-hs': dict(family=None, discovery='generalisation', harm='latent',
                      trigger='a lead whose l or sInner differs from Main.hs',
                      ok='--block quotes both figures',
                      bug='the hand-copied figure had no source but the lead'),
    'break-priced-against-its-population-floor': dict(family=None, discovery='in-use', harm='fired', harm_count=5,
                      trigger='a class property break inside or outside its A/A floor',
                      ok='prices the break, INSIDE or OUTSIDE the floor',
                      bug='reported a sort with no width'),
    'a-wide-floor-swallows-the-same-break': dict(family=None, discovery='generalisation', harm='latent',
                      trigger='the same break against a floor twice as wide',
                      ok='reads INSIDE the floor',
                      bug='nothing said whether the break was wider than the run could see'),
    'open-list-entry-without-a-status': dict(family=None, discovery='review', harm='fired', harm_count=7,
                      trigger='an open-list entry opening with no status token',
                      ok='fails naming the entry',
                      bug='the preamble promised a token per entry and sublists carried none'),
    'open-list-status-check-does-not-pass-empty': dict(family='vacuous-check', discovery='generalisation', harm='latent',
                      trigger='every entry indented into a sub-bullet',
                      ok='fails, the status check did not run',
                      bug='a list of no entries was trivially all statused'),
    'answered-account-fails-the-document': dict(family=None, discovery='review', harm='latent',
                      trigger='an ANSWERED entry past 500 words with no only-copy ruling',
                      ok='fails naming the entry and the three ways out',
                      bug='the account grew in the open list unnoticed'),
    'floor-movement-reads-the-previous-column': dict(family=None, discovery='lint', harm='fired', harm_count=8,
                      trigger='a movement paragraph whose figures are not the column above it',
                      ok='fails, reading the PREVIOUS run column',
                      bug='every gate green over the previous run paragraph'),
    'floor-movement-reworded-does-not-pass-empty': dict(family='vacuous-check', discovery='generalisation', harm='latent',
                      trigger='the movement sentence reworded past its opening phrase',
                      ok='fails saying the sentence may have been reworded',
                      bug='keyed on the phrase, rewording turned the check off'),
    'extremes-ranks-and-says-where-the-two-readings-differ': dict(family=None, discovery='in-use', harm='fired', harm_count=3,
                      trigger='--extremes --classes over the class runs',
                      ok='ranks the populations and names each extreme holder',
                      bug='no mode, the sort left to the eye'),
    'extremes-counts-one-class-twice': dict(family=None, discovery='review', harm='latent',
                      trigger='--classes naming one class twice',
                      ok='refuses, a class is named twice',
                      bug='would have ranked one population as two'),
    'extremes-is-not-for-the-main-set': dict(family=None, discovery='review', harm='latent',
                      trigger='--extremes --classes over a main-set JSON',
                      ok='refuses, ranks the stride classes',
                      bug='would have ranked the main set as a class'),
    'extremes-with-no-classes': dict(family='silent-option', discovery='review', harm='latent',
                      trigger='--extremes with no --classes',
                      ok='refuses saying none were given',
                      bug='exit 2 with no such message'),
    'classes-without-a-mode-that-reads-it': dict(family='silent-option', discovery='generalisation', harm='latent',
                      trigger='--classes beside a mode that does not read it',
                      ok='refuses at exit 2, does nothing alone',
                      bug='the files were read by nobody at exit 0'),
    # ---- align-as.py ----
    'maxskip-zero-is-off': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='LOOP_MAXSKIP=0',
                      ok='off, like unset and empty',
                      bug='bool(environ.get) was true for any value, the max-skip form built'),
    'head-after-a-zero-operand-instruction': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a loop head following ret or another bare mnemonic',
                      ok='aligned and counted',
                      bug='INSTR required whitespace after the mnemonic, the head dropped silently'),
    'pad-is-announced': dict(family=None, discovery='review', harm='latent',
                      trigger='PAD_BYTES over a target of two modules',
                      ok='one line per module says where the pad went',
                      bug='the pad was per invocation and nothing said so'),
    'empty-pad-bytes': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='PAD_BYTES= empty',
                      ok='read as unset, the compile proceeds',
                      bug='int("") at import killed the compile with ValueError'),
    'non-number-refused-in-one-line': dict(family=None, discovery='review', harm='latent',
                      trigger='PAD_BYTES=abc',
                      ok='one line naming the variable and value, exit 1',
                      bug='a ValueError traceback out of the shim, outside any handler'),
    'probe-that-did-not-assemble': dict(family='error-as-value', discovery='generalisation', harm='latent',
                      trigger='LOOP_MAXSKIP with a probe copy that fails to assemble',
                      ok='says the output is not the max-skip form',
                      bug='no lengths returned, the max-skip half built as the unconditional one'),
    # ---- loop-offsets.py ----
    'objdump-status': dict(family='error-as-value', discovery='review', harm='latent',
                      trigger='--survey of a binary objdump cannot open',
                      ok='refuses naming objdump and its message',
                      bug='stdout read alone, 0 self-loops at exit 0'),
    'addr2line-status': dict(family='error-as-value', discovery='generalisation', harm='latent',
                      trigger='arms() with an unreadable -e file',
                      ok='says addr2line failed and falls back to the mangled symbol',
                      bug='read as a build without DWARF, an empty dict'),
    'suppressed-groups-are-counted': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='--len with a group below --min-copies',
                      ok='says how many groups were suppressed',
                      bug='the group vanished in silence, the docstring example among them'),
    # ---- read-all.sh ----
    'aa-worst-cell-is-not-an-insitu-row': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a file with every A/A twin filtered out',
                      ok='(no A/A pair in this file)',
                      bug='least-indented line was an in-situ row, read as the A/A worst'),
    'aa-worst-cell-is-not-the-sum-only-pair': dict(family='scan-for-parse', discovery='review', harm='fired',
                      trigger='a sum-only raw cell wider than every A/A cell',
                      ok='the pair is skipped by name',
                      bug='its raw worst cell printed as the A/A worst'),
    'killed-run-does-not-gate-clean': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='a run killed after some of its processes',
                      ok='names the unfinished process and exits 1, not all here',
                      bug='gated the JSONs that landed and said every process gated clean'),
    'log-with-no-start-lines': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='a wall-clock log with no start lines',
                      ok='fails, no start line in the log',
                      bug='an empty awk match put one empty line into comm, gated clean over one JSON'),
    'aa-refusal-is-not-no-A-A-pair': dict(family='error-as-value', discovery='review', harm='latent',
                      trigger='a reader whose --aa refuses the file',
                      ok='--aa REFUSED, exit 1',
                      bug='stderr discarded and $? unread, (no A/A pair in this file), gated clean'),
    'run-that-complained-does-not-gate-clean': dict(family='guard-on-the-wrong-side', discovery='review', harm='latent',
                      trigger='a run log carrying its own stamped !! with rc=0',
                      ok='counts and quotes the complaints, exit 1',
                      bug='only exit codes were read and the complaint hid behind rc=0'),
    'quoted-note-block-is-not-a-run-complaint': dict(family='scan-for-parse', discovery='in-use', harm='fired',
                      trigger='a pair note quoted into the log carrying !!',
                      ok='counts only stamped === lines, gates clean',
                      bug='bare !! counted, every gate-tripped run complained for ever after'),
    # ---- read-run.py, beside the drivers ----
    'table-row-narrower-than-its-header': dict(family=None, discovery='in-use', harm='fired', harm_count=4,
                      trigger='a table row with fewer cells than its header',
                      ok='fails, narrower than its header',
                      bug='the row rendered from the left, values under the wrong runs'),
    'machine-check-names-the-control-it-leaves': dict(family=None, discovery='in-use', harm='fired',
                      trigger='--machine firing on a moved list net',
                      ok='names the two controls that tell box from area',
                      bug='could only say ASK'),
    'machine-check-does-not-stop-a-moved-box': dict(family=None, discovery='in-use', harm='fired',
                      trigger='a run whose list net moved past the band',
                      ok='BOX MOVED, exit 0, the evening goes ahead',
                      bug='exit 1 stopped the evening for a question with one answer'),
    'machine-check-tells-a-level-shift-from-a-skewed-shape': dict(family=None, discovery='generalisation', harm='latent',
                      trigger='a moved box with one shape skewed past 7%',
                      ok='says the shapes did NOT move together, ordering in question',
                      bug='one verdict for both, exit 1'),
    # ---- read-all.sh, the plateau gate ----
    'alone-leg-riders-are-not-populations': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=54,
                      trigger='a run directory holding $R-al-* rider files',
                      ok='riders excluded from the population glob',
                      bug='each rider gated as a population, burying the eighteen'),
    'plateau-reading-missing-from-a-process': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='one recorded process with no plateau reading',
                      ok='fails, fewer readings than process logs',
                      bug='one reading was lo == hi, a flat plateau over one process'),
    'plateau-reading-in-exponent-form': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a reading show writes as 8.5e-2',
                      ok='the token before ms/iter is the reading, both processes counted',
                      bug='digits-and-dot pattern missed it, the process vanished'),
    'plateau-reading-that-is-no-number': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='a reading of NaN',
                      ok='counted apart and refused',
                      bug='NaN moved neither bound and the rest gated flat'),
    'plateau-counted-per-log': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='one log with two readings and another with none',
                      ok='each log asked, the ones without a line named',
                      bug='count against count was satisfied'),
    # ---- run-major.sh, run-gate.sh and run-alonelegs.sh ----
    'wild-stamps-counted-per-process': dict(family='unverified-state', discovery='generalisation', harm='latent',
                      trigger='WILDLOG=1 with a binary carrying no instrument',
                      ok='fails, carries no @@wild stamps',
                      bug='the uninstrumented process exited 0 and nothing said so'),
    'launch-switches-recorded-whether-set-or-not': dict(family='guard-on-the-wrong-side', discovery='generalisation', harm='latent',
                      trigger='a run launched without a switch',
                      ok='launch env: WILDLOG=unset SATURATE=unset in the log',
                      bug='each assertion conditional on its own switch, the forgotten one unrecorded'),
    'gate-records-and-asserts-its-launch-switches': dict(family='unverified-state', discovery='generalisation', harm='latent',
                      trigger='run-gate.sh with WILDLOG=1 over a stand-in with no instrument',
                      ok='records the switches and says the run would be uninstrumented',
                      bug='proved the pair and said nothing about the instrument'),
    'alonelegs-refuses-an-unbaked-half': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a half whose +RTS --info lacks the baked line',
                      ok='refuses on stdout before any leg, exit 1',
                      bug='an echo set no status, 24 legs ran under DONE-ALONELEGS'),
    'alonelegs-refuses-a-listless-half': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a half whose --list gives nothing',
                      ok='refuses on stdout leaving no driver log',
                      bug='refused inside the driver log, which the relaunch guard read as a previous attempt'),
    # ---- read-run.py, figures across sites ----
    'six-pair-floor-disagrees-across-sites': dict(family='two-spellings', discovery='in-use', harm='fired', harm_count=6,
                      trigger='the six-pair figure quoted differently at two sites',
                      ok='fails, six-pair figure is quoted differently',
                      bug='nothing held the sites to each other'),
    'calibration-base-disagrees-across-sites': dict(family='two-spellings', discovery='in-use', harm='fired', harm_count=2,
                      trigger='the A/A population quoted as six here and eighteen there',
                      ok='fails, A/A population is quoted as',
                      bug='two sites said six for three runs beside blocks printing N of 18'),
    # ---- the run and smoke drivers ----
    'gate-arms-track-the-selection': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='an arm added to the selection globs',
                      ok='expected count derived from the selection',
                      bug='a literal count that had to equal the globs above it'),
    'pair-halves-must-differ': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='OTHER and BASIS carrying one name',
                      ok='refuses, a pair is two halves',
                      bug='nine JSONs written twice, gated clean, compared with itself'),
    'class-name-carries-no-hyphen': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a class named with a hyphen',
                      ok='refuses before the hours, carries a hyphen',
                      bug='cut at the first hyphen merged it with the class before the hyphen'),
    'smoke-exercises-the-shape-filter': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='a reader whose shape filter does not refuse an emptied run',
                      ok='fails, did NOT refuse',
                      bug='the sweep named a shape not in the run, the filter matched nothing and passed'),
    'relaunch-guard-skips-the-riders': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a relaunch with only $R-al-* rider files on disk',
                      ok='runs, the riders excluded from the guard',
                      bug='already has artifacts over files the run never writes'),
    'major-run-wants-its-pair-note': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a run launched without its pair note',
                      ok='refused before the hours, exit 1',
                      bug='logged a stamped !! and ran to completion, read-all.sh then failing every reading'),
    'provenance-git-could-not-read': dict(family='error-as-value', discovery='audit', harm='latent',
                      trigger='a run whose git cannot answer',
                      ok='GIT DID NOT ANSWER, neither field recorded',
                      bug='empty commits and 0 paths modified, a clean-looking tree'),
    'bench-count-complaint-names-its-process': dict(family=None, discovery='audit', harm='latent',
                      trigger='a process printing one bench short',
                      ok='the complaint names its process',
                      bug='nine identical complaints naming none'),
    # ---- install-tables.sh ----
    'no-class-block-leads': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='a run doc with no class block leads',
                      ok='fails, no class block leads',
                      bug='the guard was silent when its own search came back empty'),
    'basis-glob-catches-no-other-half': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a control half named <basis>-pa',
                      ok='refuses, is not a class name',
                      bug='$R-<basis>-*.json took the control and installed its table as the basis'),
    'install-refuses-a-hyphenated-lead': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='a class lead carrying a hyphen',
                      ok='refuses by name, carries a hyphen',
                      bug='both patterns missed it, agreed, and the block above took it'),
}


RECORDS = [
    # ---- read-run.py, the first review's ------------------------------
    case('install-lands-in-next-block', 'read-run.py', '045ca63',
         'a class whose own table is absent took the next class\'s',
         plant=lambda t: {'rundoc': rundoc_without_class_table(t),
                          'run': synth_json(t, 'slice')},
         argv=['{run}', '--block', '--in-place', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['refusing to write there'],
              hasnt=['installed at']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('block-brief-cannot-install', 'read-run.py', '045ca63',
         '--brief dropped the table --in-place had to install',
         plant=lambda t: {'rundoc': edited_rundoc(t),
                          'run': synth_json(t, 'slice')},
         argv=['{run}', '--block', '--in-place', '--brief',
               '--run-doc', '{rundoc}'],
         ok=V(exit=0, has=['installed at']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('why-pointer-is-not-a-buried-action', 'read-run.py', None,
         'twenty of this sweep\'s twenty-four hits were pointer lines',
         # A `why:` pointer names the paragraph behind its step, to be
         # fetched when the step surprises you. It is deliberately a
         # comment and deliberately not a line of the sequence, which is
         # the one thing this sweep asks a hit to become -- so every one
         # of them was an un-actionable hit, and twenty-eight of them
         # would have taught a reader to skip the worklist. Measured
         # 2026-09-01, the day the pointers landed: 24 hits before the
         # exemption and 4 after. The action beside the pointer in this
         # fixture is what keeps the exemption from being an off switch.
         plant=lambda t: {
             'readme': readme_with_a_pointer_and_a_buried_action(t)},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(has=['./read-run.py --survey'],
              hasnt=["why: --para 'Then confirm the regime'"])),

    case('buried-action-at-eof', 'read-run.py', None,
         'the last indented block of a document was never swept',
         plant=lambda t: {'readme': readme_with_trailing_buried_action(t)},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         # No --audit: `--worklists` is younger than the fix, so the code
         # before it rejects the argv as an unknown flag, which is no
         # reproduction of anything. Removal is the handling.
         ok=V(has=['--survey to see it'])),

    case('sunk-cell-costs-a-shape-not-a-row', 'read-run.py', '045ca63',
         'a plausible `worst` published beside `time --`',
         plant=_sunk_slice,
         argv=['{run}'],
         # The defect this was born for is `worst` printed beside a `time`
         # reading `--`, over a shape set one of whose cells means nothing --
         # and the repair of 2026-08-17 was to blank BOTH, which is the
         # `--      --` this case used to demand.
         #
         # RE-AIMED 2026-08-26, when that repair met the arms it was not
         # written for. A cell the forcing term does not leave positive is a
         # fill whose work an arm REMOVED, not a broken measurement, and
         # blanking the row over one of them left `canon-full` with no `time`
         # at all on the main set (`live_shapes` in read-run.py has the
         # ruling). So the cell costs the row a SHAPE and the row keeps its
         # figure, and what this case now holds is the pair of properties
         # that replaces the blanking: both columns carry a figure, and the
         # shortfall is SAID rather than left to be inferred from a count
         # nobody prints.
         #
         # Non-vacuous against the code before the change, which is where
         # the proof had to be taken -- the rule is younger than any commit
         # `--audit` could replay it against, as `--counts` was at Run 19.
         # `git show HEAD:...read-run.py` on this fixture prints
         # `mut-odo-vecdims                   --      --` and no `over 2 of
         # 3` line at all, so every `has` below fails there and the `hasnt`
         # holds only here.
         ok=V(exit=0, has=['mut-odo-vecdims over 2 of 3',
                           'the arm removed the work there'],
              hasnt=['mut-odo-vecdims                   --      --']),
         bug=V(has=['mut-odo-vecdims                   --  '],
               hasnt=['mut-odo-vecdims                   --      --'])),

    case('withheld-line-names-a-flag-that-is-not-one', 'read-run.py',
         'eeb5d24',
         'the withheld count sent a run to `--quiet`, which withholds too',
         # --check-doc --quiet ends by saying how many lines it kept back
         # and how to get them. It said "rerun without --quiet", and plain
         # --check-doc withholds as well -- `--worklists` is what promotes
         # them -- so following the message returns the same line. Met on
         # Run 17 at the worklists step (then 7, now 6e), whose content is
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

    # ---- the wider identity check, and its scoping ------------------
    # Both are --unit cases over synthetic documents, because the live
    # document cannot exercise this: the check fires only where the
    # working tree's chapter is renumbered against the committed copy,
    # which a committed tree never is. Each document is one section
    # holding one identical block; what differs is how much of the rest
    # the run replaced. Newlines are built with chr(10) rather than
    # written, an escape in a case's source passing through two layers
    # and arriving as a real newline inside a string literal, which is a
    # syntax error in the expression and not a failing test.
    # NON-VACUOUS IN BOTH DIRECTIONS, 2026-08-25, and the pair pins the
    # threshold from both sides rather than one: raising it to 1.1, so no
    # section ever qualifies, fails the first and leaves the control
    # green; dropping it to 0.0, so every section does, fails the control
    # and leaves the first green. Restoring 0.5 makes both pass. So
    # neither is passing on the function merely returning something.
    case('held-block-in-a-reworked-section', 'read-run.py', None,
         'a paragraph left standing where the run rewrote the section',
         argv=['--unit', 'held_in_reworked_sections('
               + doc_expr(['## H', 'new 0.111 prose', 'new 0.222 prose',
                           'kept 0.999 prose'])
               + ', ' + doc_expr(['## H', 'old 0.333 prose',
                                  'old 0.444 prose', 'kept 0.999 prose'])
               + ", {'h'})"],
         ok=V(has=['kept 0.999 prose'])),

    case('held-block-in-an-untouched-section', 'read-run.py', None,
         'CONTROL: a reference section is mostly unchanged every run by'
         ' design, so what it holds there is not a finding',
         argv=['--unit', 'held_in_reworked_sections('
               + doc_expr(['## H', 'kept 0.111 prose', 'kept 0.222 prose',
                           'new 0.999 prose'])
               + ', ' + doc_expr(['## H', 'kept 0.111 prose',
                                  'kept 0.222 prose', 'old 0.888 prose'])
               + ", {'h'})"],
         ok=V(has=['[]'])),

    # ---- --counts, registration 4's reading ---------------------------
    # No `fix` on either, so no `bug` and no --audit leg: the mode is
    # younger than every revision here, so there is nothing to replay it
    # against and a `bug` verdict would only assert that code predating a
    # flag rejects the flag. Both were written before the mode existed and
    # BOTH FAILED against the tree that lacked it -- argparse refusing
    # `--counts` at exit 2 -- which is the same proof --audit gives, taken
    # in the working tree because that is where it was available.
    case('counts-refused-cell-read-as-a-zero', 'read-run.py', None,
         'a cell perf refused read as a count of zero',
         # run-counts.sh writes `!!` where perf could not count a cell, and
         # a reader taking that line for data has a zero in a geomean --
         # which is not a wrong figure but a destroyed one, the arm reading
         # 0.0000 or dividing by nothing. Both halves are built at one
         # ratio here, so every arm must read exactly 1.0000: the refused
         # cell is dropped from its arm and NAMED, and the arm answers over
         # the shapes that were counted.
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json'),
             'other': synth_json(t, 'main', name='b.json'),
             'ca': synth_counts(t, 'counts-a.txt',
                                refuse=[(sorted(main_shapes())[0],
                                         'bq-expand')]),
             'cb': synth_counts(t, 'counts-b.txt')},
         argv=['{run}', '--compare', '{other}', '--counts', '{ca}', '{cb}'],
         ok=V(exit=0, has=['perf refused'], hasnt=['0.0000'])),

    case('counts-alone-does-nothing', 'read-run.py', None,
         'the counts files were read and the mode never ran',
         # FOUND BY PROBE at Run 19's verification, on the mode that run
         # had just added, and written after the fix rather than before
         # it -- which is the wrong order this file asks for and is
         # recorded rather than hidden. `--counts` names two files and is
         # a reading OF `--compare`; given without one it fell past every
         # arm of the dispatch to the default table, printed it, and
         # exited 0. That is the unread-flag family exactly, and the
         # sibling readings of --compare (--alloc, --chapter, --ci,
         # --bridge) were all already guarded, so the mode was added
         # beside four guards and joined none of them. It now joins both:
         # the modifier roll call, and the one refusing two readings of
         # --compare at once.
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json'),
             'ca': synth_counts(t, 'counts-a.txt'),
             'cb': synth_counts(t, 'counts-b.txt')},
         argv=['{run}', '--counts', '{ca}', '{cb}'],
         ok=V(exit=2, has=['does nothing alone'])),

    case('counts-arm-the-run-does-not-time', 'read-run.py', None,
         'an arm in the counts and not in the run, silently folded in',
         # The narrowing this whole file is written against, in the one
         # place a second artifact meets a run: the counts are taken over
         # whatever roster the binary held that day, so an arm that has
         # since left the run is exactly what a stale pair of counts
         # carries. Named and skipped, never quietly counted.
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json'),
             'other': synth_json(t, 'main', name='b.json'),
             'ca': synth_counts(t, 'counts-a.txt',
                                extra_arms=('zz-departed-arm',)),
             'cb': synth_counts(t, 'counts-b.txt',
                                extra_arms=('zz-departed-arm',))},
         argv=['{run}', '--compare', '{other}', '--counts', '{ca}', '{cb}'],
         ok=V(exit=0, has=['zz-departed-arm'])),

    # ---- --movers, the count a write-up takes by eye --------------------
    # No `fix`, so no `bug` and no --audit leg: the mode is younger than
    # every revision here. Both were written before it existed and BOTH
    # FAILED against the tree that lacked it, which is the same proof
    # --audit gives, taken where it was available.
    case('movers-count-disagrees-with-its-rows', 'read-run.py', None,
         'a movers count that did not match the arms it listed',
         # THE DEFECT THIS EXISTS FOR HAPPENED TO A READER RATHER THAN TO
         # THIS CODE, which is why it is a case and not a regression. Run
         # 19's independent checker reported twelve arms past 3% where
         # eleven move; the eleventh sits at 3.99% and the twelfth at
         # 2.51%, so no threshold convention explains it. What does is
         # that the count had to be taken BY EYE off `--chapter`, whose
         # per-arm block is a list of arms outside ONE percent -- a
         # 2.51% arm sits in the middle of it looking like a mover. Both
         # the checker and the session hand-rolled the count in awk,
         # because no mode answered it.
         #
         # So the property is that the headline count and the listed rows
         # come from one predicate: a mode counting with one test and
         # listing with another reproduces the very slip it replaces. One
         # arm is skewed clear past the threshold and one clear under it,
         # so no float sits near the boundary and the case tests the
         # predicate rather than the rounding.
         # THE COUNT IS ASSERTED WHOLE, `3 of N arm(s) move past 3%`,
         # and not as the substring `3 of` -- which `13 of N` satisfies,
         # so the loose form pinned nothing and would have passed an
         # implementation off by ten. Three arms are skewed clear past
         # the threshold and one clear under it, so the headline count,
         # the row set and the group count are each checked against a
         # known answer rather than against each other.
         #
         # N IS DERIVED AND WAS ONCE WRITTEN OUT. This case asserted `3 of
         # 42` and went red the day Run 20's arms landed and the roster
         # reached 45 -- on a mode that was answering correctly, which is
         # the worst kind of red: it says the code is wrong where the
         # fixture is. The arms come from Main.hs's roster, so the
         # denominator does too, through `compared_arm_count`. Only the
         # numerator is the fixture's, and it is the fixture's because
         # the skew list above puts it there.
         #
         # NON-VACUITY RE-PROVED after the derivation, 2026-08-25, since a
         # computed expectation can agree with a broken implementation by
         # construction and this one must not. Counting the headline with
         # a looser predicate than the rows are listed with -- the exact
         # defect this case is named for -- fails it, and so does a
         # denominator off by one. Restoring both makes it pass.
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json'),
             'other': synth_json(t, 'main', name='b.json',
                                 skew=[(sh, arm, f)
                                       for sh in main_shapes()
                                       for arm, f in (('bq-expand', 1.10),
                                                      ('lib-stage1', 1.12),
                                                      ('lib-stage2-disp', 1.08),
                                                      ('liblist-stage1', 1.01))])},
         argv=['{run}', '--compare', '{other}', '--movers', '3'],
         ok=V(exit=0,
              has=['3 of %d arm(s) move past 3%%' % compared_arm_count(),
                   'in 3 group(s)', 'bq-expand', 'lib-stage1',
                   'lib-stage2-disp'],
              hasnt=['liblist-stage1'])),

    case('movers-alone-does-nothing', 'read-run.py', None,
         'a numeric modifier whose zero slipped a truthiness guard',
         # FOUND BY AN INDEPENDENT CHECKER READING THE CODE, 2026-08-25,
         # and it is the counts case's defect surviving one value. The
         # modifier roll call tested `getattr(args, flag)` for truth,
         # which is right for a store_true flag and wrong for one taking
         # a NUMBER: `--movers 0` is falsy, so neither the guard nor the
         # dispatcher fired and the run printed its default table at exit
         # 0 -- the silence that loop exists to refuse. The guard now
         # asks whether a flag was GIVEN rather than whether its value is
         # truthy, which is a different question and the one it meant.
         plant=lambda t: {'run': synth_json(t, 'main', name='a.json')},
         argv=['{run}', '--movers', '0'],
         ok=V(exit=2, has=['does nothing alone'])),

    case('movers-with-none-says-so', 'read-run.py', None,
         'CONTROL: no arm past the threshold is an answer, not a silence',
         # The empty aggregate this file refuses everywhere: a header, no
         # rows and exit 0 reads as a reading. Two runs built alike move
         # no arm at all, so the mode has to SAY none rather than print a
         # table with nothing under it.
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json'),
             'other': synth_json(t, 'main', name='b.json')},
         argv=['{run}', '--compare', '{other}', '--movers', '3'],
         ok=V(exit=0, has=['no arm moves past'])),

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

    case('deflation-legs-beside-the-run-not-the-cwd', 'read-run.py', 'e9a8bb3',
         'the legs were globbed out of the cwd, not beside the run',
         # The run and both rider sets sit in the case's temp directory
         # and the reader runs from HERE, which is how a run named through
         # a directory was answered "the riders were not taken" with every
         # leg on disk -- from ~/r/orthotope, over run17-det-main.json,
         # 2026-08-28. Shown non-vacuous by hand before the fix was
         # committed: with the glob back on the bare pattern it FAILS on
         # both strings; --audit replays that by itself now.
         plant=lambda t: {'run': deflation_legs(at=t)},
         argv=['{run}', '--deflation'],
         ok=V(exit=0, has=['sat/clean'],
              hasnt=['the riders were not taken']),
         bug=V(exit=2, has=['the riders were not taken'])),

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
         # THE BREAK IS PLANTED since 2026-09-04: the manifest is one
         # registration, and whether the synthetic work order breaks it is
         # `_spread`'s accident, so the shipped fill is skewed clear past
         # its root on every shape.
         plant=lambda t: {'run': synth_json(t, 'main', skew=[
             (sh, 'mut-odo-vecdims-add-in-leaf-u2', 4.0)
             for sh in main_shapes()])},
         argv=['{run}', '--claims'],
         ok=V(has=['`CLAIMS` in this script is where that lands'])),

    case('claims-arm-counted-per-registration', 'read-run.py', '045ca63',
         'one filtered arm reported as eight',
         # THE EXCLUDED ARM MUST BE ONE `CLAIMS` NAMES IN EXACTLY ONE
         # REGISTRATION, which is the whole of what this case needs: filter
         # one arm, and the reader must report one arm rather than the
         # registrations it appears in. It was `bq-expand` until 2026-08-26,
         # when claim 2's second link retired and took that arm out of the
         # manifest -- the case then filtered nothing and said `0 arm(s)`;
         # `mut-flat-gm` until the prune of 2026-09-04 parked it with claim
         # 1. Claim 10's shipped fill is in one registration; `list` would
         # not serve, being the baseline every ratio divides by.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--claims', '--exclude',
               'mut-odo-vecdims-add-in-leaf-u2'],
         ok=V(has=['1 arm(s) of the claims list']),
         bug=V(has=['arm(s) of the claims list'],
               hasnt=['1 arm(s) of the claims list'])),

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
         #
         # THE BODIES LEFT README ON 2026-08-29, each registration moving
         # into the file of the run that made it and leaving a verdict and
         # a pointer. A stub carries no numbered items, so flipping its
         # marker trips nothing and this case stopped firing -- found by
         # the suite the same hour, which is what it is for. So the entry
         # is planted WHOLE now: the lead, the bad marker, and two items
         # carrying verdicts, one shouting and one not, which is the
         # distinction the pattern was keyed on.
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(),
             a_registration_lead().replace('`ANSWERED`', '`OPEN`', 1)
             # The verdict must sit INSIDE the bolded span, which is
             # where `adjudicated` looks and where every real item
             # puts it; outside it the item reads unadjudicated and
             # neither branch fires, which is silence and not a pass.
             + '\n  1. **A registered question. ANSWERED: it held.**'
               ' With its reading.'
             + '\n  2. **A second one, and the debt is PAID.**'
               ' With its reading too.'
             + '\n'))},
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
                              b, 'lib-stage1'), 'a.json'),
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
         # The fixture puts this run's file beside a predecessor that is
         # it VERBATIM, which is the state a write-up that made the file
         # and stopped is in: every figure-bearing paragraph of the head
         # is the run before's.
         #
         # A CONTROL sits beside it: the same newer file over a
         # predecessor whose leads are marked, so nothing matches. The two
         # differ in the predecessor alone, so a check that reported
         # regardless would fail the control.
         plant=rundoc_pair,
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=["head are unchanged from Run"])),

    case('run-file-head-new-says-nothing', 'read-run.py', None,
         'CONTROL: a head rewritten since the run before is not held',
         plant=lambda t: rundoc_pair(t, held=False),
         argv=['--check-doc', '--worklists', '--run-doc', '{rundoc}'],
         ok=V(hasnt=['head are unchanged from Run'])),

    case('run-file-alone-is-held-to-nothing', 'read-run.py', None,
         'CONTROL: one run file in runs/, and the diff says so',
         # The check needs two files, and a directory holding one is the
         # normal state of the first run under this layout. It must say
         # that in so many words: a silence there reads exactly like a
         # head with nothing held.
         plant=lambda t: {'rundoc': write(
             os.path.join(_mkruns(t), os.path.basename(RUNDOC)),
             rundoc_text())},
         argv=['--check-doc', '--worklists', '--run-doc', '{rundoc}'],
         ok=V(has=['is held to no predecessor'])),

    case('link-into-a-run-file-that-is-not-this-run', 'read-run.py', None,
         'a link the rename missed resolved, rendered, and promised the'
         ' run before',
         # WHAT THE FOUR-HEADING RENAME BECAME. A run's write-up used to
         # rename four headings and repoint every link to them, and
         # `--check-doc` caught what it missed as dead anchors; now the
         # run number is in a file name, runs/ keeps every run, so a link
         # left at the run before resolves on disk and renders in the
         # browser and is wrong. Nothing else here can see it.
         plant=lambda t: {'readme': readme_link_to_an_older_run(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['point at a run file that is not this'])),

    case('deliberate-link-into-an-older-run-survives-a-wrap', 'read-run.py',
         None,
         'CONTROL: a link whose text names the older run across a line'
         ' break is the exemption and not the miss',
         # The case above is the miss; this is the deliberate link the
         # exemption exists for, in the shape the wrapped document gives
         # it. The rule read `Run 22` as one token and the hook had put a
         # newline in it.
         plant=lambda t: {'readme': readme_deliberate_link_wrapped(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(hasnt=['point at a run file that is not this'])),

    case('results-names-an-identical-predecessor-half', 'read-run.py',
         None,
         "CONTROL: a repetition's Results may say `is run<N-1>-g912 byte"
         ' for byte`',
         # The stale-name check read every `run<N>-half` token in Results
         # as a name the rename missed. A repetition names its
         # predecessor's binary there on purpose, and Run 23 reworded to
         # lose the artifact name; `byte for byte` within eighty
         # characters after the token is now the exemption, and the case
         # `results-names-an-older-basis-half` stays the control that a
         # bare stale name still fails.
         plant=lambda t: {'rundoc': rundoc_results_names_identical_predecessor(t)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(hasnt=['names run'])),

    case('todo-marker-fails-the-document', 'read-run.py', None,
         'a paragraph deferred as `[[TODO]]` is refused until written',
         # A paragraph deferred until a measurement landed carried no
         # marker and was forgotten until an end-to-end read (Run 23).
         # The token is `[[TODO]]` and not TODO, which README's own TODO
         # list names in its heading.
         plant=lambda t: {'rundoc': rundoc_with_todo_marker(t)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['[[TODO]]'])),

    case('checklist-prints-one-list-alone', 'read-run.py', None,
         'CONTROL: --checklist run prints the run list and none of the'
         ' chapter around it',
         # The lists are what a session executes and used to be reachable
         # only inside 2600 lines of chapter (Run 23). The run list starts
         # at step 13 and ends at step 20's last comment; a header or a
         # paragraph of the chapter in the output would be the mode
         # reading past the block.
         plant=lambda t: {'readme': edited_readme(t)},
         argv=['--checklist', 'run', '--readme', '{readme}'],
         ok=V(exit=0, has=['13. has the gate run and passed', 'run-counts.sh'],
              hasnt=['## ', 'why the chapter'])),

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
             b, main_shapes()[0] + '/lib-stage1', 0.0))},
         argv=['{run}', '--selftest'],
         ok=V(exit=1, has=['non-positive slope'],
              hasnt=['ZeroDivisionError', 'Traceback']),
         bug=V(has=['ZeroDivisionError'])),

    case('table-survives-a-zero-list-slope', 'read-run.py', 'ba56d23',
         "a zero `list` slope divided in the table's share line, the default",
         # The family's last site, found by sweeping for it the day after
         # the selftest's: the share of the forcing term in `list` and
         # `mut-odo-vecdims` divides by their slopes, and a cell with none took
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
         # The bug is the sunk row's NEGATIVE figure and not the absence of
         # `--`: the pre-fix reader's fingerprint had fixed columns, three
         # of which the prune of 2026-09-04 parked, so it writes `--` for
         # those on today's roster and `hasnt` passed for the wrong reason.
         plant=lambda t: {'run': sunk_json(t, main_shapes(),
                                           'mut-odo-vecdims')},
         argv=['{run}', '--fingerprint'],
         ok=V(has=['| -- |'], hasnt=['| -0.']),
         bug=V(has=['| shape |', '| -0.'])),

    case('block-per-shape-refuses-a-sunk-cell', 'read-run.py', 'e2d6604',
         "a sunk cell was divided into the block's installed per-shape line",
         plant=lambda t: {'run': sunk_json(t, class_shapes('scaled'),
                                           'mut-odo-vecdims')},
         argv=['{run}', '--block', '--brief'],
         ok=V(has=['--/']),
         # No --audit: this mode is given no document and takes its own
         # default, which before the run-file split was a README that
         # now carries none of what it reads. 2026-08-25.
         ),

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
         # No --audit: this mode is given no document and takes its own
         # default, which before the run-file split was a README that
         # now carries none of what it reads. 2026-08-25.
         ),

    # ---- read-run.py, the second review's ------------------------------
    # BOTH PLANT AN ERA Main.hs, because Main.hs cites README headings by
    # anchor and a fixture pairing today's source with an older document
    # reads every anchor renamed since as dead --
    # `the-mutable-ceiling-taken` against that era's
    # `the-mutable-ceiling-not-taken`, the rename that came with the
    # decision to take the ceiling. `era_main` is `era_readme`'s
    # counterpart and the pair must move together.
    #
    # THE RULING, so the cheap wrong repair is not reached for: when these
    # fail under --audit it is NOT the `beyond its own history` case the
    # top of this file prescribes dropping the `bug` verdict for. Dropping
    # it costs the replay permanently; respelling the anchors restores it,
    # the old reader then exiting 0 with no failure at all. Check which of
    # the two it is by running the revision under test where `materialise`
    # puts it -- HERE, so its `__file__`-relative path roots resolve --
    # since a replay run from anywhere else adds a BLOCKED of its own and
    # reads like the unrecoverable case.
    case('checkdoc-without-a-roster', 'read-run.py', 'a6c32e8',
         'a roster it could not parse skipped five checks at exit 0',
         plant=lambda t, rev: {'main': mangled_main(t, rev),
                               'readme': era_readme(t, rev)},
         argv=['--check-doc', '--main', '{main}', '--readme', '{readme}'],
         ok=V(exit=1, has=['BLOCKED: no roster parsed']),
         bug=V(exit=0)),

    case('checkdoc-open-list-out-of-order', 'read-run.py', 'a6c32e8',
         'the goal section above the open list killed the sweep in silence',
         plant=lambda t, rev: {'main': era_main_file(t, rev),
                               'readme': readme_goal_above_open(t, rev)},
         argv=['--check-doc', '--main', '{main}', '--readme', '{readme}'],
         ok=V(exit=1, has=['BLOCKED: the open list']),
         bug=V(exit=0)),

    case('checkdoc-paired-run-aligned-with-no-counterpart',
         'read-run.py', 'a6c32e8',
         'a half named aligned with no counterpart folds a pair into one',
         plant=lambda t: {'rundoc': rundoc_paired_run_aligned_only(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(has=['aligned and nothing']),
         # No --audit, for the reason the case below gives: `--run-doc`
         # postdates every commit this could replay against.
         ),

    case('checkdoc-qmark-under-renamed-yardstick', 'read-run.py', 'a6c32e8',
         'a renamed yardstick header disabled the published-`?` gate',
         plant=lambda t: {'rundoc': rundoc_yardstick_renamed_with_qmark(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(has=['still carry the `?`']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

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
         # the artifacts up to Run 16 having been deleted that day, and
         # again 2026-09-02 to run23-g912 at Run 24's preparation, Run 18's
         # and Run 19's having gone the same way. The
         # figure is the FIXTURE's, planted into the README copy rather
         # than read from the run, so it does not move with the run; what
         # the run has to be is CAPTURED rather than built.
         plant=lambda t: {'rundoc': rundoc_current_run_sentence(t),
                          'run': run_json('run23-g912-main.json'),
                          'main': era_main_hs(t, run_json('run23-g912-main.json'))},
         argv=['{run}', '--claims', '--run-doc', '{rundoc}',
               '--main', '{main}'],
         ok=V(has=['0.9312']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    # ---- --para's retrieval shape, which had no case at all ---------
    # Added with the change they describe, 2026-08-25. `--para` is the
    # mode a session reaches for most and it was unguarded: on Run 19
    # `--para 'What Run'` returned four registration entries WHOLE,
    # thousands of characters each, read for one lead. Printing an index
    # when several match and the paragraph itself when one does is the
    # whole change; these three pin each branch, since a mode that
    # indexed always would cost a round trip on every unique match and
    # one that never indexed would not have changed anything.
    case('class-split-across-two-shape-lists', 'read-run.py', None,
         'a class declared in two Main.hs lists read as two populations',
         # A CLASS IS ITS SHAPES' NAME PREFIX, which is what the binary
         # selects one by (`classes reshape1-`) and what every block lead
         # is written with. `dims_by_shape` also records the LIST a shape
         # is declared in, and four sites took that for the class -- which
         # held only while the two agreed. `reshape1-strided-r3` needed a
         # different constructor and so a second list, and the reshape1
         # class then read as `the reshape1 class + the reshape1 class`:
         # `--block`, `--extremes` and `--markdown` refused it outright,
         # and `summary_row` and `lead_shapes` returned in SILENCE, which
         # is the half no exit code would have shown.
         #
         # No --audit: the fix has no earlier revision to replay against,
         # the defect and its repair landing in one commit. The failure
         # was taken in the working tree on 2026-08-25 instead -- with
         # `cls` reverted to `lst`, this exact call exits 1 saying `the
         # reshape1 class + the reshape1 class`, and four install-tables
         # cases fail with it -- which is the same proof at the only
         # moment it was available.
         plant=lambda t: {'run': synth_run(
             os.path.join(t, 'reshape1.json'),
             [s for s in class_shapes('reshape1')])},
         argv=['{run}', '--block', '--brief'],
         ok=V(exit=0, has=['of the reshape1 class'],
              hasnt=['reshape1 class + the reshape1 class'])),

    case('link-path-resolves-nowhere', 'read-run.py', None,
         'a link written for one file, moved into the other, pointed at'
         ' nothing',
         # THE SPLIT'S OWN SHAPE OF DEFECT, and the one the anchor check
         # cannot see: a link's FRAGMENT is held to the document it names,
         # and its PATH was held to nothing. A paragraph carrying
         # `[...](runs/run19.md)` moved out of README into
         # `runs/run19.md`, where that path means `runs/runs/run19.md`;
         # the fragment check passed it because there is no fragment, and
         # the every-link-names-this-run check passed it because it ends
         # in the current basename. Found by a reader, 2026-08-25.
         # `check_paths` was no help either: it resolves BACKTICKED names
         # and a link target is not one.
         plant=lambda t: {'rundoc': edited_rundoc(
             t, ('## Results', '## Results\n\nA planted paragraph naming'
                 ' [a file](no-such-dir/no-such.md) that is not there.'))},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['no-such-dir/no-such.md',
                           'resolve to no file'])),

    case('link-path-to-a-real-file-passes', 'read-run.py', None,
         'CONTROL: the same check over a path that is there',
         plant=lambda t: {'rundoc': edited_rundoc(
             t, ('## Results', '## Results\n\nA planted paragraph naming'
                 ' [a file](../Main.hs) that is.'))},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=0, hasnt=['resolve to no file'])),

    case('replace-shrinks-a-list-to-one-item', 'read-run.py', None,
         'an anchor in a list\'s FIRST item took all four and wrote back one',
         # THE GUARD BESIDE THIS ONE HAS THE WRONG PREMISE, and using it
         # is what showed that. A list with no blank line between its
         # items is one paragraph, so `--replace` replaces all of it; the
         # existing refusal exempts an anchor in the FIRST item, on the
         # theory that quoting a list from its start is what a caller
         # replacing the whole list would do. It is also exactly what a
         # caller EDITING THE FIRST ITEM does. Measured 2026-08-25 on this
         # README's non-urgent TODO list: an anchor naming its first
         # entry replaced all nine with one, 8859 characters for 656, at
         # exit 0, and the echo said so and was read past.
         #
         # The rule that separates them is the REPLACEMENT: a caller who
         # means the list passes a list back.
         plant=lambda t: {'doc': doc_of_a_list(t), 'new': one_item(t)},
         argv=['--replace', '**Item 1.**', '--with', '{new}',
               '--readme', '{doc}'],
         ok=V(exit=1, has=['4-item list', 'the replacement carries 1 item']),
         probe=lambda subs: open(subs['doc']).read()),

    case('replace-takes-a-whole-list-for-a-whole-list', 'read-run.py', None,
         'CONTROL: a list handed back as a list is the caller meaning it',
         plant=lambda t: {'doc': doc_of_a_list(t), 'new': whole_list(t)},
         argv=['--replace', '**Item 1.**', '--with', '{new}',
               '--readme', '{doc}'],
         ok=V(exit=0, has=['--replace: ']),
         probe=lambda subs: open(subs['doc']).read()),

    case('para-pointer-names-no-paragraph', 'read-run.py', None,
         'a step pointed at a paragraph lead a later edit had renamed',
         # THE POINTERS ARE WHAT MAKES SKIPPING THE PROSE SAFE. The list
         # says reading it front to back is the largest waste available
         # here, and what replaces that is fetching the one paragraph a
         # step hangs on -- which needs the step to name it. A named lead
         # is exactly what a later edit renames in silence, every other
         # check here staying green while the pointer aims at nothing,
         # which is the decay `--check-doc` already refuses for anchors.
         plant=lambda t: {'readme': edited_readme(
             t, ("why: --para 'Then confirm the regime'",
                 "why: --para 'Then confirm the regime it once had'"))},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['--para pointer', 'Then confirm the regime it'])),

    case('para-pointer-that-resolves-passes', 'read-run.py', None,
         'CONTROL: the pointers as they stand name one paragraph each',
         plant=lambda t: {'readme': edited_readme(t, ('# regime-3 micro',
                                                      '# regime-3 micro'))},
         argv=['--check-doc', '--worklists', '--readme', '{readme}'],
         ok=V(exit=0, has=['every --para pointer in the checklists'])),

    case('replace-matches-across-a-line-break', 'read-run.py', None,
         'an anchor the formatter broke in two counted 0 and was refused',
         # THE WRAPPING WAS THE CALLER'S PROBLEM AND SHOULD NOT HAVE BEEN.
         # A paragraph's line breaks are `wrap80`'s, put where the width
         # falls and moved by the next edit above, so an anchor quoted
         # from the rendered prose matched on one form of the document
         # and not the other. The chapter carried a whole precondition
         # about it -- unwrap before editing, and again after every
         # commit, because `wrap-restore` re-wraps -- for a distinction
         # no caller ever meant. Matching the flattened form retires it.
         plant=lambda t: {'doc': doc_wrapped(t), 'new': one_item(t)},
         argv=['--replace', 'sentence runs over a line', '--with', '{new}',
               '--readme', '{doc}'],
         ok=V(exit=0, has=['--replace: ']),
         probe=lambda subs: open(subs['doc']).read()),

    case('replace-still-refuses-an-anchor-found-twice', 'read-run.py', None,
         'CONTROL: flattening must not make a second occurrence invisible',
         plant=lambda t: {'doc': doc_wrapped(t), 'new': one_item(t)},
         argv=['--replace', 'paragraph', '--with', '{new}',
               '--readme', '{doc}'],
         ok=V(exit=1, has=['the anchor occurs'])),

    case('replace-takes-a-wrapped-lists-first-item', 'read-run.py', None,
         "an anchor quoted from a wrapped item's start landed on line two",
         # The first-item exemption tested the first LINE, so on a wrapped
         # list it exempted only what fitted there and refused the rest as
         # an anchor from the middle. It tests the first ITEM now.
         plant=lambda t: {'doc': doc_wrapped_list(t), 'new': one_item(t)},
         argv=['--replace', 'long enough to be wrapped', '--with', '{new}',
               '--readme', '{doc}'],
         ok=V(exit=1, has=['2-item list', 'the replacement carries 1 item'])),

    case('section-withholds-the-tables', 'read-run.py', None,
         'the reading a run owes was enumerated and could not be taken',
         # "not its figures", "not the previous run's readings", "not the
         # other seven" -- and no way to obey any of it: a session opens a
         # document with a line range, the tables sit between the
         # paragraphs it is told to read, and Run 20 ingested 38 KB of the
         # previous run's tables, 24% of that file, every byte named as
         # skippable one sentence later. The withheld size is printed so
         # the skip is visible rather than silent.
         plant=lambda t: {'doc': doc_with_a_table(t)},
         argv=['--section', 'Middle', '--readme', '{doc}'],
         ok=V(exit=0, has=['table paragraph(s) withheld', 'Prose after'],
              hasnt=['| a | b |'])),

    case('section-prints-tables-when-asked', 'read-run.py', None,
         'CONTROL: the geomean table is hand-edited, so one caller wants'
         ' them',
         plant=lambda t: {'doc': doc_with_a_table(t)},
         argv=['--section', 'Middle', '--with-tables', '--readme', '{doc}'],
         ok=V(exit=0, has=['| a | b |'])),

    case('section-indexes-an-ambiguous-name', 'read-run.py', None,
         'a name matching several headings printed all of them',
         # A wrong section is a wrong READ, not a wrong line, so this
         # indexes rather than guessing, as --para does.
         plant=lambda t: {'doc': doc_with_a_table(t)},
         argv=['--section', 'e', '--readme', '{doc}'],
         ok=V(exit=1, has=['heading(s) match'])),

    case('delete-refuses-a-section-sized-paragraph', 'read-run.py', None,
         'a range splice between two markers took 148936 characters',
         # `--replace` exists so a paragraph is NAMED rather than sliced,
         # and deletion had no mode -- so removing one fell back to
         # `s.find(lead)` for the start and `s.find(chr(10)*2)` for the
         # end. Measured 2026-08-26 in this reader's own run file: the end
         # anchor matched a later paragraph and took 148936 characters,
         # leaving 41 lines of 908, and the script printed the extent and
         # the last line it was about to cut -- text from a different
         # paragraph -- and was read past. An echo is not a refusal, which
         # is the same lesson the list guard above records.
         plant=lambda t: {'doc': doc_of_a_big_paragraph(t)},
         argv=['--delete', 'A long one', '--readme', '{doc}'],
         ok=V(exit=1, has=['REFUSED', 'the bar is 1500']),
         probe=lambda subs: open(subs['doc']).read()),

    case('delete-refuses-a-list', 'read-run.py', None,
         'dropping one item of a list is an edit, not a deletion',
         plant=lambda t: {'doc': doc_of_a_list(t)},
         argv=['--delete', '**Item 2.**', '--readme', '{doc}'],
         ok=V(exit=1, has=['4-item list']),
         probe=lambda subs: open(subs['doc']).read()),

    case('delete-takes-one-paragraph', 'read-run.py', None,
         'CONTROL: a plain paragraph under the bar is removed, and only it',
         plant=lambda t: {'doc': doc_of_a_big_paragraph(t, n=10)},
         argv=['--delete', 'A long one', '--readme', '{doc}'],
         ok=V(exit=0, has=['--delete: ']),
         probe=lambda subs: open(subs['doc']).read()),

    case('para-indexes-when-several-leads-match', 'read-run.py', None,
         'several matching leads printed whole where an index was wanted',
         plant=lambda t: {'readme': readme_of_leads(t)},
         argv=['--para', 'Alpha', '--readme', '{readme}'],
         ok=V(exit=0, has=['3 paragraph(s) whose lead matches'],
              hasnt=['Body one', 'Body three'])),

    case('para-prints-a-unique-match-whole', 'read-run.py', None,
         'CONTROL: one match is retrieved, not indexed for a second call',
         plant=lambda t: {'readme': readme_of_leads(t)},
         argv=['--para', 'Beta alone', '--readme', '{readme}'],
         ok=V(exit=0, has=['Body four'],
              hasnt=['paragraph(s) whose lead matches'])),

    case('para-all-restores-the-set', 'read-run.py', None,
         'CONTROL: --all is the escape for the reading that wants them all',
         plant=lambda t: {'readme': readme_of_leads(t)},
         argv=['--para', 'Alpha', '--all', '--readme', '{readme}'],
         ok=V(exit=0, has=['Body one', 'Body two', 'Body three'],
              hasnt=['paragraph(s) whose lead matches'])),

    # ---- the run file, read back -------------------------------------------
    case('retirement-epitaph-listed-as-unaccounted', 'read-run.py', None,
         'a retired claim\'s last reading listed as an unattributed figure',
         # CONTROL FIRST, below: the same figure in an ordinary sentence
         # is still listed, so this pair says the exemption is the word
         # `retires` and not the mode having stopped listing anything.
         # The captured run is re-aimed as the case above is, and for the
         # same reason: RE-AIMED 2026-09-02 from run19-g912, whose
         # artifacts went with Run 19's.
         plant=lambda t: {'rundoc': rundoc_retirement_sentence(t),
                          'run': run_json('run23-g912-main.json'),
                          'main': era_main_hs(t, run_json('run23-g912-main.json'))},
         argv=['{run}', '--claims', '--run-doc', '{rundoc}',
               '--main', '{main}'],
         ok=V(hasnt=['0.8271'])),

    case('ordinary-sentence-still-listed', 'read-run.py', None,
         'CONTROL: an unattributed figure outside a retirement is listed',
         plant=lambda t: {'rundoc': rundoc_retirement_sentence(t, False),
                          'run': run_json('run23-g912-main.json'),
                          'main': era_main_hs(t, run_json('run23-g912-main.json'))},
         argv=['{run}', '--claims', '--run-doc', '{rundoc}',
               '--main', '{main}'],
         ok=V(has=['0.8271'])),

    case('results-names-an-older-basis-half', 'read-run.py', None,
         "the Results lead named the PREVIOUS run's half under this run's"
         ' tables',
         # A control and not a defect replay: the check was written the day
         # this case was, so there is no `fix^` to replay it against. What
         # it holds is the property, which is what the next reader needs --
         # the fixture is the Run 14 defect built out of the current README.
         plant=lambda t: {'rundoc': rundoc_stale_basis_in_results(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['while the file is Run'])),

    case('rundoc-names-an-artifact-it-outlives', 'read-run.py', None,
         'the run file cited a directory step 11 offers for deletion',
         # And the citation then decided what was KEPT, which is the
         # dependency backwards: Run 20 kept probe-run20-exposed/ because
         # its own prose named it. A past run's artifacts are history and
         # do not die with this offer, so only `run<cur>-*` and
         # `probe-run<cur>-` are refused.
         plant=lambda t: {'rundoc': rundoc_naming_its_own_artifact(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['artifact path(s) named'])),

    case('rundoc-has-a-stray-class-lead', 'read-run.py', None,
         'a bolded class name in the head read as a ninth class block',
         # install-tables.sh finds a block by that shape, so it found nine,
         # one with no table, and refused naming a JSON that was present
         # all along -- an error message pointing away from the defect.
         # The wrap completes the trap: unwrapped the phrase sits mid-line.
         plant=lambda t: {'rundoc': rundoc_with_a_stray_class_lead(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['bolded class name'])),

    case('rundoc-has-a-stray-class-lead-in-provenance', 'read-run.py', None,
         'the same stray after the class section, where the sweep stopped',
         # The sibling above is planted before Results and was always
         # caught; this one is planted in Provenance and was not, the sweep
         # having read only up to the class section while its own message
         # said `outside the class section`. Both placements are kept so a
         # later narrowing of either bound fails here rather than silently.
         plant=lambda t: {
             'rundoc': rundoc_with_a_stray_class_lead_in_provenance(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['bolded class name'])),

    case('rundoc-repeats-a-class-lead', 'read-run.py', None,
         'the same class leading twice inside the class section',
         # The region the stray sweep excludes, where the predicate is
         # duplicate rather than stray. Left uncovered, the loose grep
         # counts nine leads for eight classes and the installer refuses
         # naming a JSON that is present -- the defect both sweeps exist
         # against, reached from the one place neither was looking.
         plant=lambda t: {'rundoc': rundoc_repeating_a_class_lead(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['lead more than one paragraph'])),

    case('rundoc-miscounts-its-class-processes', 'read-run.py', None,
         'a class process count that is not one per class per half',
         # One of Run 14's four wrong subjects, and the one with both a
         # truth and a stable phrasing. The bare total is NOT checked and
         # the planter's docstring says why: run20.md quotes four different
         # correct values for `N processes`, so a sweep over that would
         # flag right prose or admit anything.
         plant=lambda t: {
             'rundoc': rundoc_miscounting_its_class_processes(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['one per class per half'])),

    case('rundoc-names-a-subset-of-its-class-processes', 'read-run.py', None,
         'a legal subset mention failed the count check',
         # The other half of the case above, and the half that fails
         # silently: a check that flags right prose reads as a working
         # check. The count must be quoted somewhere, not everywhere.
         plant=lambda t: {
             'rundoc': rundoc_naming_a_subset_of_its_class_processes(t)},
         # BOTH refusal wordings are named, the containment form's and the
         # intersection form's: `hasnt` with only the current wording is a
         # search that cannot find the defect it guards, and this case
         # passed against HEAD until both were listed. The `ok:` line says
         # `class process count reads`, so neither string can match it.
         argv=['--check-doc', '--worklists', '--run-doc', '{rundoc}'],
         ok=V(hasnt=['class process count(s) quoted',
                     'no class process count quoted'])),

    # ---- read-run.py, later reviews' cases ---------------------------------
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
         plant=lambda t: {'rundoc': rundoc_summary_row_short(t),
                          'run': synth_json(t, 'slice')},
         argv=['{run}', '--block', '--run-doc', '{rundoc}'],
         ok=V(has=['not checked: it has 5 column(s)']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

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
             lambda bs: bad_alloc_fit(bs, 'slice-primes/bq-expand'))},
         argv=['{run}', '--main', '/dev/null'],
         ok=V(has=['allocated R2 < 0.99']),
         bug=V(has=['alloc missing for'], hasnt=['allocated R2 < 0.99'])),

    case('markdown-installs-into-the-main-table', 'read-run.py', 'febc2bd',
         "a class run whose shapes Main.hs lost installed into Results",
         plant=lambda t: {'rundoc': edited_rundoc(t),
                          'run': synth_json(t, 'rev')},
         argv=['{run}', '--markdown', '--in-place', '--main', '/dev/null',
               '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['a population Main.hs does not define'],
              hasnt=['installed at']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('selftest-survives-a-sunk-cell', 'read-run.py', 'febc2bd',
         'a sunk cell gave the gate a traceback and no verdict at all',
         plant=_sunk_slice,
         argv=['{run}', '--selftest'],
         # The defect is the traceback, and it stays refused. What moved on
         # 2026-08-26 is the VERDICT the gate then reaches: a sunk cell of an
         # arm is work removed and is named, where a sunk cell of the
         # BASELINE takes every row of its shape with it and still fails the
         # file -- which is the case two above, unchanged, and is what keeps
         # this pair from being one loosened check. Read them together.
         # Non-vacuous against the code before the change, taken in the
         # working tree for want of a commit to replay: it exits 1 there with
         # `FAIL: correction:` and says nothing about work removed.
         ok=V(exit=0, hasnt=['math domain error', 'Traceback', 'FAIL'],
              has=['work the arm removed']),
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
         'properties.py', '7a68237',
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
         argv=[],
         ok=V(exit=0, has=['line(s) of reader warning withheld',
                           'kind(s)']),
         # No --audit: the driver itself reads the split, so an older copy
         # of it cannot be run against this tree at all. 2026-08-25.
         no_audit='driver-reads-the-split'),

    # ---- this file's own instruments ------------------------------------
    # The runner and its tree guard live in `~/.claude/bin/defect-run.py`
    # since 2026-09-02, so these two are memory: the defects were this
    # suite's, and the live checks are the shared runner's selftest and
    # the control `defect-run-tree-delta` in the shared corpus.
    case('tree-check-that-could-not-run', 'check-scripts.py', 'ea4ab06',
         'this suite\'s one guarantee about itself passed unchecked',
         argv=None, ok=None, no_audit='program-retired'),

    case('tree-change-in-both-directions', 'check-scripts.py', 'ea1a3e6',
         'a file REMOVED tripped the alarm and printed nothing beneath it',
         argv=None, ok=None, no_audit='program-retired'),

    case('shadow-refuses-an-absolute-cd', 'defects.py', '77fd51b',
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

    case('shadow-refuses-a-quoted-absolute-cd', 'defects.py', '9a51f3a',
         'the same cd in quotes slipped the guard',
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'cd \"/nowhere-zz\"\\n')"],
         ok=V(has=['cds to an absolute path']),
         bug=V(has=['/shadow'], hasnt=['cds to an absolute path'])),

    case('shadow-holds-its-own-directory', 'defects.py', None,
         'CONTROL: `cd "$(dirname "$0")"` is what a shadow can hold',
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'cd \"$(dirname \"$0\")\"\\n')"],
         ok=V(has=['/shadow'], hasnt=['cds to an absolute path'])),


    case('fixture-ci-bounds-are-criterion-shaped', 'defects.py', '40f7a37',
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
             b, main_shapes()[0] + '/lib-stage1'))},
         argv=['{run}'],
         ok=V(exit=0, has=['1 cell(s) with no confidence interval'])),

    # The families lint moved to `~/.claude/bin/defect-lint.py` on
    # 2026-09-02, so this is memory; the control that went with it,
    # `env-parse-under-a-handler-is-not-flagged`, and the planted files
    # both read live in the shared corpus as `defect-lint-env-parse-*`.
    case('env-parse-through-a-helper', 'check-scripts.py', '40f7a37',
         'an import-time parse in a helper called at import went unflagged',
         # The family's guard read the line's own scope -- `at.get(n.lineno)
         # is None` is a module-scope line and nothing else -- so a helper
         # called at module scope, align-as.py's `number()` and the form
         # the family was counted from, passed, and the family had no live
         # site in the tree: a silent search. A helper called at import
         # parses at import.
         argv=None, ok=None, no_audit='program-retired'),

    case('properties-refuse-an-empty-corpus', 'properties.py', None,
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
         argv=[],
         ok=V(exit=1, has=['empty corpus proves nothing'],
              hasnt=['every property holds'])),

    case('properties-over-one-built-run', 'properties.py', None,
         'CONTROL: a corpus of one built run holds every property',
         plant=corpus_of_one,
         env={'CORPUS': '{corpus}'},
         argv=[],
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
             'rundoc': relead(t, 'slice', lambda s: s.replace(
                 ', `slice-coprime-r7` (`l` 60060, `sInner` 13)', '')),
             'run': synth_run(os.path.join(t, 'slice.json'),
                              run_order_shapes('slice'))},
         argv=['{run}', '--block', '--run-doc', '{rundoc}'],
         ok=V(exit=0, has=['does not name `slice-coprime-r7`']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('lead-order-mislabels-the-per-shape-line', 'read-run.py', '3596ba2',
         'a lead listed its shapes in an order the installed line is not in',
         # The per-shape paragraph is installed IN RUN ORDER and labelled
         # *in the lead's order*, so a lead that lists them differently
         # does not go stale -- it mislabels three live ratios, which is
         # the one of the three readings no reading of the block catches.
         plant=lambda t: {
             'rundoc': relead(t, 'slice', lambda s: s.replace(
                 '`slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3),'
                 ' `slice-primes` (`l` 250357, `sInner` 89)',
                 '`slice-primes` (`l` 250357, `sInner` 89),'
                 ' `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3)')),
             'run': synth_run(os.path.join(t, 'slice.json'),
                              run_order_shapes('slice'))},
         argv=['{run}', '--block', '--run-doc', '{rundoc}'],
         ok=V(exit=0, has=['it lists them `slice-primes`,'
                           ' `slice-cnn-L2-24x24-c32`']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('lead-figures-disagree-with-main-hs', 'read-run.py', '3596ba2',
         'a lead\'s hand-copied `l` had no source but the lead',
         plant=lambda t: {
             'rundoc': relead(t, 'slice', lambda s: s.replace(
                 '`slice-primes` (`l` 250357', '`slice-primes` (`l` 250358')),
             'run': synth_run(os.path.join(t, 'slice.json'),
                              run_order_shapes('slice'))},
         argv=['{run}', '--block', '--run-doc', '{rundoc}'],
         ok=V(exit=0, has=['is written (`l` 250358, `sInner` 89) where'
                           ' Main.hs gives (`l` 250357, `sInner` 89)']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

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
             lambda bs: _scale_arm(bs, 'bq-expand-aa-distant', 2.5),
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
         # No --audit: the fixture is built from today's document and
         # plants against an anchor the era's copy does not carry, so
         # the replay is a fixture that will not build. 2026-08-25.
         ),

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
         # No --audit: the fixture is built from today's document and
         # plants against an anchor the era's copy does not carry, so
         # the replay is a fixture that will not build. 2026-08-25.
         ),

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
         # No --audit: the fixture is built from today's document and
         # plants against an anchor the era's copy does not carry, so
         # the replay is a fixture that will not build. 2026-08-25.
         ),

    case('predictions-enumerates-items-twice', 'read-run.py', None,
         'each registration item counted once per paragraph naming it',
         plant=lambda t: dict(rundoc_registration_with_verdicts(t),
                              run=synth_json(t, 'main', name='a.json'),
                              other=synth_json(t, 'main', name='b.json')),
         argv=['{run}', '--compare', '{other}', '--predictions',
               '--run-doc', '{rundoc}'],
         # One span and one item without: the doubled form says `2 span(s)`
         # and lists `(2), (1), (2)`.
         ok=V(has=['1 span(s)'], hasnt=['(2), (1)'])),

    case('compare-does-not-name-its-direction', 'read-run.py', None,
         'a ratio whose direction the reader knows and does not say',
         # `--compare` puts the BASIS first, so below 1 is the basis
         # faster -- which the run chapter states and which a session
         # writing prose still gets backwards, four paragraphs of Run 24's
         # head having been written the wrong way round and caught by the
         # PUBLISHED COLUMNS rather than by anything the mode said. The
         # mode knows both file names and the convention; saying it costs
         # one line and removes the whole class of error.
         plant=lambda t: {'run': synth_json(t, 'main', name='a.json'),
                          'other': synth_json(t, 'main', name='b.json')},
         argv=['{run}', '--compare', '{other}'],
         ok=V(exit=0, has=['below 1 ='])),

    case('replace-takes-an-abutting-heading', 'read-run.py', None,
         'a paragraph that abuts a heading took the heading with it',
         # --replace's unit is blank-line separated, so a paragraph the
         # document does not separate from the heading below it carries
         # that heading into the replacement and the heading is gone. Run
         # 24 lost `## Results` from its own file that way, met two gates
         # later as `no Results heading`, and recoverable only because the
         # mode had printed the heading on its `out, last` line. A run
         # file's headings are what every install and every link resolve
         # against, so this refuses instead.
         plant=lambda t: {
             'doc': write(os.path.join(t, 'doc.md'),
                          '# T\n\nkeep me\n\nthe planted paragraph\n'
                          '## zz-Heading\n\nafter\n'),
             'readme': write(os.path.join(t, 'other.md'), '# other\n'),
             'new': write(os.path.join(t, 'new.txt'), 'replacement\n')},
         argv=['--replace', 'the planted paragraph', '--with', '{new}',
               '--run-doc', '{doc}', '--readme', '{readme}'],
         ok=V(exit=1, has=['heading'], hasnt=['chars ->'])),

    case('stale-head-check-sees-only-decimals', 'read-run.py', None,
         'three stale head paragraphs the check could not see',
         plant=rundoc_pair_with_address_paragraph,
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(has=['zz-address-only'])),

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
         # COUNTED, not counted TO ONE: the count is over the whole
         # list, so the first live ruling in README makes it 2 and a
         # literal `1` fails on a document nobody broke. Run 24 is
         # that run -- task 9's probe account is the only copy there
         # is -- so this asserts the exemption line and the planted
         # entry's absence from the bloated list, which is what its
         # registration sibling above asserts and is what the case is
         # about. Re-aimed 2026-09-03.
         ok=V(exit=0, has=['only-copy ruling(s)'],
              hasnt=['zz-planted-account'])),

    case('answered-registration-is-exempt', 'read-run.py', None,
         'the registrations were adjudicated by hand every run',
         # Six entries a reader cleared by hand each time the list was
         # printed, all of them long for the same recorded reason: a
         # registration is the only copy, the run chapter being replaced
         # every run and the run file keeping one geomean per strategy
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
         plant=lambda t: {'rundoc': rundoc_floor_movement_off_column(t)},
         argv=['--check-doc', '--worklists', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=["reading the PREVIOUS run's column"]),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('floor-movement-built-clean-passes', 'read-run.py', None,
         'CONTROL: the same built paragraph with every figure right',
         # The two cases beside this one both plant into a paragraph this
         # fixture constructs, so this is what says they fire on the
         # plant and not on the construction.
         plant=lambda t: {'rundoc': rundoc_with_floor_movement(t)},
         argv=['--check-doc', '--worklists', '--run-doc', '{rundoc}'],
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
         plant=lambda t: {'rundoc': rundoc_floor_movement_reshaped(t)},
         argv=['--check-doc', '--worklists', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['if that sentence was reworded']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

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

    case('cross-classes-aggregates-the-blocks-own-rows', 'read-run.py', None,
         "the class section's intro figures were assembled by hand",
         # And got wrong twice on Run 20: a population built here read 398
         # comparisons at 272/126 where the reader's own is 376 at
         # 259/117, and the high end was quoted from the wrong class
         # because the first attempt excluded a class's degenerate arms
         # wholesale instead of naming them. The intro and the eight
         # blocks it aggregates now come from one `cross_half_rows`,
         # which was proved output-identical on all eight blocks before
         # this mode was written.
         plant=lambda t: {
             'a': synth_run(os.path.join(t, 'rev.json'),
                            run_order_shapes('rev')),
             'b': synth_run(os.path.join(t, 'rev2.json'),
                            run_order_shapes('rev'))},
         argv=['--cross-classes', '--classes', '{a}', '--others', '{b}'],
         ok=V(exit=0, has=['class population(s)', 'arm-comparison(s)',
                           'geomeans'])),

    case('cross-classes-refuses-unpaired-lists', 'read-run.py', None,
         'a basis list and a control list that do not pair up',
         # Two files against one is not eight against eight with one
         # missing: which class lost its other half is unknowable from
         # here, so it refuses rather than zipping to the shorter.
         plant=lambda t: {
             'a': synth_run(os.path.join(t, 'rev.json'),
                            run_order_shapes('rev')),
             'b': synth_run(os.path.join(t, 'slice.json'),
                            run_order_shapes('slice')),
             'c': synth_run(os.path.join(t, 'rev2.json'),
                            run_order_shapes('rev'))},
         argv=['--cross-classes', '--classes', '{a}', '{b}',
               '--others', '{c}'],
         ok=V(exit=2, has=['they pair up or nothing does'])),

    case('ceiling-is-the-family-leader', 'read-run.py', None,
         'the ceiling read as the fastest arm once outside arms led',
         # The run file defines *ceiling* as the leading arm OF the family;
         # the code read `timed[0]`, and the two agreed until the library
         # arms overtook the family in Run 22, when every written row
         # disagreed at once and --extremes crowned an outside arm. The
         # synthetic model has an outside arm ahead of the family on its
         # own -- the library arms' per-function work is the smaller --
         # so nothing is skewed, and no arm is named: the fastest line
         # must not read a family arm and the ceiling line must.
         plant=lambda t: {'rundoc': edited_rundoc(t),
                          'run': synth_json(t, 'slice')},
         argv=['{run}', '--block', '--run-doc', '{rundoc}'],
         ok=V(has=['ceiling (family)    mut-odo-vecdims'],
              hasnt=['fastest timed arm   mut-odo-vecdims'])),

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

    # The dead-spot form plans from a probe, so these four hand the shim
    # the real assembler rather than the stand-in; a machine without
    # /usr/bin/gcc fails them loudly, which is the right verdict. The
    # expected directives are worked by hand above the fixtures.
    case('deadspot-pads-after-the-jump', 'align-as.py', None,
         'the pad went in front of the head, on the fall-through path',
         plant=asm_fallthrough, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after jmp\t.Lgo: .p2align\t6, 0x90, 13',
                           'before .Lloop: testq\t%rax, %rax',
                           '0 short loop(s) straddling (0 planned)'])),

    case('deadspot-keeps-the-table-with-its-label', 'align-as.py', None,
         'a head behind an info table was left where it fell',
         plant=asm_table, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after .text: .p2align\t6, 0x90, 31',
                           'before .Lr_info: .long\t0',
                           'before .Lr: .Lr_info:',
                           '1 head(s) in 1 group(s)'])),

    case('deadspot-outer-of-a-rotated-pair-yields', 'align-as.py', None,
         'the outer loop took the line and the inner one straddled',
         plant=asm_pair, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         # The line before `.Lin` is the directive itself: a `.skip rho`
         # would stand there had the outer loop won the residue.
         ok=V(exit=0, has=['after jmp\t*(%rbp): .p2align\t6, 0x90, 46',
                           'before .Lin: .p2align\t6, 0x90, 46',
                           '1 short loop(s) straddling (1 planned)'])),

    case('deadspot-off-is-the-at-head-form', 'align-as.py', None,
         'the switch off changed what the max-skip form emits',
         plant=asm_fallthrough, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_MAXSKIP': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after jmp\t.Lgo: nop',
                           'before .Lloop: .p2align\t6, 0x90, 9'],
              hasnt=['dead-spot'])),

    # ---- loop-offsets.py -----------------------------------------------
    case('objdump-status', 'loop-offsets.py', '0a1bc60',
         'a binary that was never opened read as one with no loops',
         argv=['--survey', 'no-such-binary'],
         ok=V(exit=1, has=['objdump'], hasnt=['0 self-loops']),
         bug=V(exit=0, has=['0 self-loops'])),

    case('offsets-refuses-two-reports', 'loop-offsets.py', None,
         '--survey beside --library, and --survey dropped without a word',
         # The dispatch is an if/return chain, so the pair printed the
         # library report alone -- the silent drop read-run.py's
         # one-mode guard refuses, found by hunting that family here.
         # A control until the fix has a hash; the refusal fires in
         # argparse, so the binaries are never opened and need not
         # exist.
         argv=['--survey', '--library', 'x', 'y'],
         ok=V(exit=2, has=['two reports, not one'])),

    case('offsets-refuses-an-unread-flag', 'loop-offsets.py', None,
         'a --len under --survey, accepted and honoured by nobody',
         # --survey scans every length up to the line by design and
         # --library keys on the loop bytes, so the grouped report's two
         # knobs are read by nobody under either: `--survey --len 24`
         # answered with the at-most-64 report, measured before the fix.
         argv=['--survey', '--len', '24', 'x'],
         ok=V(exit=2, has=['read only by the grouped report'])),

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

    case('len-zero-lifts-the-size-filter-not-the-cap', 'loop-offsets.py',
         None,
         'CONTROL: the header names the cap, not the lifted size filter',
         argv=['--unit', 'span_label(None)'],
         ok=V(has=["'at most 64 B'"], hasnt=['any length'])),

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

    # ---- read-run.py, beside the drivers -----------------------------------
    case('table-row-narrower-than-its-header', 'read-run.py', '0e2934c',
         'a row two cells short put its values under the wrong runs',
         plant=lambda t: {'rundoc': rundoc_with_ragged_row(t)},
         argv=['--check-doc', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['narrower than its header']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

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
         # No --audit: this mode is given no document and takes its own
         # default, which before the run-file split was a README that
         # now carries none of what it reads. 2026-08-25.
         ),

    case('machine-check-does-not-stop-a-moved-box', 'read-run.py', '8132e79',
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
                          'fp': os.path.join(t, 'fp-moved.md')},
         argv=['{run}', '--machine', '--run-doc', '{fp}'],
         ok=V(exit=0, has=['BOX MOVED', 'moved TOGETHER',
                           'GOES AHEAD EITHER WAY'], hasnt=['STOP']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('machine-check-tells-a-level-shift-from-a-skewed-shape',
         'read-run.py', '8132e79',
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
                          'fp': os.path.join(t, 'fp-same.md')},
         argv=['{run}', '--machine', '--run-doc', '{fp}'],
         ok=V(exit=0, has=['inside 3%'], hasnt=['BOX MOVED'])),

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

    # ---- read-all.sh, the plateau gate -------------------------------------
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

    # ---- run-major.sh, run-gate.sh and run-alonelegs.sh --------------------
    case('plateau-counted-per-process', 'run-major.sh', None,
         'a half without the preamble joined a saturated run in silence',
         # The count, and it is the bench count's own shape: SATURATE is
         # set on the launch line and the binary is one that does not carry
         # the preamble, so every process runs UNSATURATED and each of its
         # figures is in a state the run does not know it is in. Nothing
         # else here can see it -- the process exits 0, leaves a JSON and
         # runs the count asked of it -- which is why the check is a count
         # of the line and not a reading of it.
         shadow=dict(extra=lambda text: halves('zzpl-lookrts', 'zzpl-a1g', classes=classes_in(text))
                     + [('zzpl-pair.txt', NOTE_STUB)]),
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
         # step 2 reaches for on a suspicious cell and not on every
         # process. ANY count above zero passes, unlike the plateau's
         # exactly-one: the instrument writes two stamps per sample.
         shadow=dict(extra=lambda text: halves('zzwl-lookrts', 'zzwl-a1g', classes=classes_in(text))
                     + [('zzwl-pair.txt', NOTE_STUB)]),
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
         shadow=dict(extra=lambda text: halves('zzle-lookrts', 'zzle-a1g', classes=classes_in(text))
                     + [('zzle-pair.txt', NOTE_STUB)]),
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
                            ('zzgl-pair.txt', NOTE_STUB)]),
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
                            ('zzal-pair.txt', NOTE_STUB)]),
         argv=['zzal', 'g912'],
         # MAXBUSY=100 because the load guard below the artifact one reads
         # the REAL machine, and a corpus that reads the box answers for
         # the box: the bar is put where no reading can reach it, exactly
         # as the perf cases use a stub and not the machine's counter.
         # It doubles as this case's control that a quiet-enough box gets
         # through that guard, the refusal having its own case beside it.
         env={'MAXBUSY': '100'},
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

    case('alonelegs-refuses-a-busy-machine', 'run-alonelegs.sh', None,
         'timed legs were launched onto a box that had got busy',
         # The riders run AFTER the sequence, hours past where run list
         # step 16 last looked at the machine, and they are timed one
         # bench to a process -- so a box handed back to its owner in the
         # meantime gets timed instead of the leg. Four were launched that
         # way on 2026-08-26 and thrown away.
         #
         # MAXBUSY=-1 rather than a load: every reading of a real machine
         # is at or above 0 and so above -1, which fires the guard whatever
         # the box is doing. That is what makes this case deterministic on
         # a busy runner AND on an idle one -- a bar of 0 would pass an
         # idle box reading 0.0 and the case would then prove nothing
         # there, which is the silent-search failure this corpus exists to
         # refuse.
         shadow=dict(extra=[('zzal4-g912', FAKE_HALF),
                            ('zzal4-pair.txt', NOTE_STUB)]),
         argv=['zzal4', 'g912'],
         env={'MAXBUSY': '-1'},
         # Refused BEFORE the redirect, as its siblings are, so a refusal
         # leaves no driver log for the relaunch guard above to read as a
         # previous attempt -- which is asserted here and not assumed.
         ok=V(exit=1, has=['the machine is busy'],
              hasnt=['start:', 'shapes:'])),

    case('alonelegs-refuses-a-previous-attempt', 'run-alonelegs.sh', None,
         "CONTROL: the guard still fires on the sweep's OWN artifacts",
         # The other side of the case above. Its fix narrows a glob, and a
         # narrowed glob that matches nothing at all would pass that case
         # and lose the guard outright -- these legs would then be
         # overwritten in place with nothing said, which is what the guard
         # exists to prevent.
         shadow=dict(extra=[('zzal2-g912', FAKE_HALF),
                            ('zzal2-al-g912-cnn-slice-c32-r1.json', '[]\n'),
                            ('zzal2-pair.txt', NOTE_STUB)]),
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
                            ('zzub-pair.txt', NOTE_STUB)]),
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
                            ('zzll-pair.txt', NOTE_STUB)]),
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

    # ---- run-counts.sh, the counted-work column ----------------------------
    case('counts-refuses-a-blocked-perf', 'run-counts.sh', None,
         'a blocked perf spent the whole sweep writing NaN',
         # Every cell is two `perf stat` processes, so a machine that
         # refuses the counter does not fail the sweep -- it writes a `!!`
         # line per cell and takes a full sweep to do it. What the guard
         # asserts is a capability at the moment of use, a counter being
         # refusable by a container or a missing perf as much as by a
         # setting.
         #
         # Both sides use a STUB perf and not the machine's, or the case
         # would pass or fail on the box's own state -- which is the very
         # thing the guard is there to read.
         shadow=dict(extra=[('zzct3-g912', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_BLOCKED)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzct3', 'g912'],
         ok=V(exit=1, has=['perf will not count instructions here',
                           'Nothing ran'])),

    case('counts-refuses-an-unwritable-tmp', 'run-counts.sh', None,
         'a broken temp path bought the same sweep-long run of NaN',
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

    case('counts-sweeps-only-the-class-it-was-given', 'run-counts.sh', None,
         'a class sweep took the main set, or took every class at once',
         # `run-counts.sh` enumerated its shapes from `--list`, which is the
         # MAIN SET, so the counted-work reading covered the main set and
         # nothing else -- the artifact's own header said so and the gap was
         # invisible to anyone asking a class question of it, which is how
         # it was found. A third argument now names a class, and the two
         # things that can go wrong with it are both here: the sweep must
         # take that class's shapes from `classes --list` rather than the
         # main roster's, and it must take ONLY that class, `other-shape-a`
         # being in the stand-in's class roster for the second half of
         # that. The file is named for the class besides, so a class sweep
         # cannot overwrite the main-set column.
         shadow=dict(extra=[('zzctc-g912', FAKE_HALF)]),
         env={'N': '1'},
         argv=['zzctc', 'g912', 'rev'],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzctc-counts-g912-rev.txt')).read(),
         # And NOT stamped RESTRICTED: a class column is a recorded one,
         # and the stamp's `= full` test fired on `full class=rev`.
         ok=V(has=['rev-shape-a list', 'rev-shape-b list', 'class=rev'],
              hasnt=['other-shape-a', 'shape-c', 'RESTRICTED'])),

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

    case('counts-file-says-arms-alone-was-restricted', 'run-counts.sh',
         None,
         'an ARMS-only smoke run read as a recorded column',
         # The scope string still opens `full` when only ARMS restricts
         # (`full ARMS=list`), so a prefix test on the string cannot see
         # this form; the stamp reads the variables. 2026-09-01.
         shadow=dict(extra=[('zzct6-g912', FAKE_HALF)]),
         env={'ARMS': 'list', 'N': '1'},
         argv=['zzct6', 'g912'],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzct6-counts-g912.txt')).read(),
         ok=V(has=['ARMS=list', 'RESTRICTED'])),

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

    # ---- read-run.py, figures across sites ---------------------------------
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
         # RE-AIMED 2026-08-25 off Run 19's floor section, from
         # 0.54%/0.31%, which its write-up replaced. RE-AIMED AGAIN
         # 2026-08-26 off Run 20's, from 0.49%/0.29%, and the emphasis
         # markers are part of the anchor now because that write-up
         # bolded the pair. SELF-AIMING since 2026-09-02: the anchor is
         # read off README by the sentence's own shape, so a run's requote
         # no longer leaves a fixture that will not build -- three re-aims
         # in a week, the last by Run 23's write-up, each a loud failure
         # with nothing behind it.
         plant=lambda t: {'readme': readme_six_pair_perturbed(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['six-pair figure is quoted differently']),
         # No --audit: the fixture is built from today's document and
         # plants against an anchor the era's copy does not carry, so
         # the replay is a fixture that will not build. 2026-08-25.
         ),

    case('calibration-base-disagrees-across-sites', 'read-run.py', '054f3f1',
         'the A/A population read six pairs in one section and eighteen in another',
         # The twelve twins took the A/A population from six pairs to
         # eighteen on 2026-08-14, and two sites kept saying six for three
         # runs -- the reader's own section and the floor section's
         # per-population rule -- while every class block printed
         # "N of 18". Nothing compared them.
         plant=lambda t: {'readme': edited_readme(t, (
             'as an order of magnitude: it rests on six pairs',
             'as an order of magnitude: it rests on sixteen pairs'))},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['A/A population is quoted as']),
         # No --audit: the fixture is built from today's document and
         # plants against an anchor the era's copy does not carry, so
         # the replay is a fixture that will not build. 2026-08-25.
         ),

    # The three below hold the DOCUMENTS to Main.hs rather than to each
    # other, added 2026-08-29 after Run 21 shipped a set of counts that
    # agreed everywhere and were wrong everywhere. No `fix` on any of them:
    # the checks postdate every commit here, so there is nothing for
    # --audit to replay against, and each was instead proved able to fail
    # by hand on the live documents the day it was written.
    case('aa-population-agrees-with-itself-and-not-the-roster', 'read-run.py',
         None,
         'every site said eighteen pairs while the roster had sixteen',
         # THE CASE THE OLD CHECK COULD NOT SEE. It compared the sites to
         # each other, so a population that moved under all of them at once
         # passed: `offtab`'s parking took the A/A pairs from eighteen to
         # sixteen on 2026-08-28 and every site still read eighteen, in
         # agreement and wrong, through a whole write-up.
         plant=lambda t: {'readme': unwrapped_readme_edit(
             t, 'as an order of magnitude: it rests on six pairs',
             'as an order of magnitude: it rests on eighteen pairs',
             'The same six controls ride every process',
             'The same eighteen controls ride every process')},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['where the roster has'])),

    case('class-blocks-disagree-with-main-hs', 'read-run.py', None,
         'the run file carried one class block fewer than Main.hs defines',
         # Run 21 added a ninth class and shipped five stale `eight`s. A
         # count of the blocks against the shape lists needs no artifact,
         # so it survives the JSONs going.
         plant=lambda t: {'rundoc': unwrapped_rundoc_edit(
             t, '**`runs` --- run length swept',
             '**runs --- run length swept')},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['class block(s) where Main.hs defines'])),

    case('class-table-shapes-disagree-with-main-hs', 'read-run.py', None,
         'the cross-class table gave a class a shape count Main.hs refutes',
         # The table is hand-assembled and its `shapes` column was held to
         # nothing: `reshape1` and `bcastmid` went to four shapes on
         # 2026-08-25 and `runs` arrived at seven on 2026-08-28.
         plant=lambda t: {'rundoc': runs_summary_row(t, short_by=1)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['shape counts disagree with Main.hs'])),

    case('class-shapes-added-after-the-run-are-exempt', 'read-run.py', None,
         "a class shape added between runs failed the run file's true count",
         # Two runs shapes landed 2026-08-30 with Run 21's file the newest,
         # and both class-shape checks held that file's 7 to Main.hs's 9;
         # README's provenance bullet declares such an addition and the
         # reader takes the declared names out of what the file is held to.
         #
         # THE FIXTURE BUILDS ITS OWN SUBJECT, since 2026-09-01. It used to
         # take today's declaration away and watch the check fire, which
         # worked only while some class had grown SINCE the newest run --
         # and Run 22 ran with all four `runs` shapes in it, so the branch
         # had no live subject and the fixture stopped building, which is a
         # silent search dressed as a case. Now it plants both halves: a
         # declaration in README and a run file short by exactly the
         # declared four, where the exemption must hold.
         plant=lambda t: {
             'readme': unwrapped_readme_edit(
                 t, '`runs-4`, `runs-5`, `runs-256` and `runs-512` on'
                    ' 2026-08-30, before the run',
                 '`runs-4`, `runs-5`, `runs-256` and `runs-512` were added'
                 ' 2026-08-30, after the run'),
             'rundoc': runs_summary_row(t, short_by=4)},
         argv=['--check-doc', '--quiet', '--readme', '{readme}',
               '--run-doc', '{rundoc}'],
         ok=V(hasnt=['shape counts disagree with Main.hs'])),

    case('retired-classes-timed-by-the-run-are-exempt', 'read-run.py', None,
         "a class retired from timing after a run failed that run file's"
         " class count",
         # Main.hs retires a class from timing and keeps it in `check`, so
         # the class counts take it out -- and the newest run file, which
         # timed it, would then read one block over. README's provenance
         # bullet declares the retirement as after the run, as it declares
         # shapes added after one, and the reader keeps a declared class in
         # what that file is held to. Both halves planted, on `rev`.
         plant=plant_retired_class_exempt,
         argv=['--check-doc', '--quiet', '--readme', '{readme}',
               '--main', '{main}'],
         ok=V(hasnt=['class block(s) where Main.hs defines'])),

    case('retired-shapes-timed-by-the-run-are-exempt', 'read-run.py', None,
         "a main shape retired from timing after a run failed that run"
         " file's `over N shapes`",
         # The mirror of the class case above for the main set: Main.hs
         # retires a shape from timing and keeps it in `check`, the
         # population sizes take it out, and the newest run file, which
         # timed it, would then match no population. The provenance
         # bullet's `were retired DATE, after the run` puts it back for
         # that file. Both halves planted, on `vgg-14-c512-k3`.
         plant=plant_retired_shape_exempt,
         argv=['--check-doc', '--quiet', '--readme', '{readme}',
               '--main', '{main}'],
         ok=V(hasnt=['match no population'])),

    case('main-shapes-added-after-the-run-are-exempt', 'read-run.py', None,
         "a main-set shape added between runs failed every `over N shapes`"
         " the run file quotes",
         # Two main-set shapes landed 2026-09-02 for Run 24 with Run 23's
         # file the newest, and the population check held that file's
         # `over 24 shapes` to Main.hs's 26, where the class-shape checks
         # beside it already read the provenance bullet's declaration and
         # exempted the class shapes named there. The same declaration now
         # exempts main-set shapes from the population sizes, and the
         # roster-size sites alone stay held to today's Main.hs, being
         # sentences about the roster as it stands and not about a run.
         #
         # The fixture builds its own subject, as its sibling above does,
         # and derives its figure: `plant_main_shapes_exempt` declares two
         # main-set shapes never added after any run and moves every
         # `over N shapes` the run file quotes at its true size down by
         # two, so nothing here is a number a later main-set change can
         # leave stale.
         plant=plant_main_shapes_exempt,
         argv=['--check-doc', '--quiet', '--readme', '{readme}',
               '--run-doc', '{rundoc}'],
         ok=V(hasnt=['match no population Main.hs defines'])),

    # ---- the run and smoke drivers -----------------------------------------
    case('gate-arms-track-the-selection', 'run-gate.sh', 'febc2bd',
         'the expected bench count was a literal that had to equal SEL',
         shadow=dict(
             mutate=[('run-gate.sh',
                      "'*/sum-only-early' '*/sum-only-late')",
                      "'*/sum-only-early' '*/sum-only-late' '*/offtab')")],
             # The stand-in lists the added arm too: the gate reads its
             # list before launching since 2026-09-04, and this case is
             # about the count, not the refusal.
             extra=[('zzgate-a1g', FAKE_HALF_WITH_OFFTAB),
                    ('zzgate-lookrts', FAKE_HALF_WITH_OFFTAB),
                    ('zzgate-pair.txt', NOTE_STUB)]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzgate'],
         ok=V(has=['expecting 18 benches a process']),
         bug=V(has=['expecting 15 benches a process'])),

    case('smoke-sweep-runs-clean', 'smoke-sweep.sh', None,
         'CONTROL: every reader mode, both installers and its own refusals',
         shadow=dict(extra=lambda: halves('zzsw-lookrts', 'zzsw-a1g')
                     + [('zzsw-pair.txt', NOTE_STUB)]),
         # Both taken from the fixture rather than named: the sweep's own
         # defaults are chosen for how long a real -L1 process takes, which
         # a stand-in does not, and a shape the fixture does not carry
         # stops it at `--list has no <shape>` before any mode is swept.
         env={'SHAPE': main_shapes()[0], 'CLASS': class_shapes('window')[0],
              'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzsw'],
         ok=V(exit=0, has=['sweep clean'], hasnt=['!!'])),

    # ---- pair-halves.sh, the one place the halves are named ------------
    case('halves-read-from-the-note', 'pair-halves.sh', None,
         'CONTROL: the HALVES line is read and printed as two assignments',
         shadow=dict(extra=[('zzph-pair.txt', NOTE_STUB)]),
         argv=['zzph'],
         ok=V(exit=0, has=['BASIS=lookrts; OTHER=a1g'])),

    case('halves-refuse-a-disagreeing-environment', 'pair-halves.sh', None,
         'CONTROL: an environment naming another half than the note is refused',
         shadow=dict(extra=[('zzph2-pair.txt', NOTE_STUB)]),
         env={'OTHER': 'ghead'},
         argv=['zzph2'],
         ok=V(exit=1, has=['the note is the authority'],
              hasnt=['BASIS=lookrts;'])),

    case('halves-refuse-a-note-without-the-line', 'pair-halves.sh', None,
         'CONTROL: a note from before the line is refused naming it',
         shadow=dict(extra=[('zzph3-pair.txt', 'a stand-in pair note.\n')]),
         argv=['zzph3'],
         ok=V(exit=1, has=["has no 'HALVES: basis=<b> other=<o>' line"])),

    case('halves-fall-back-to-the-environment-without-a-note',
         'pair-halves.sh', None,
         'CONTROL: no note at all takes the environment, and says so',
         env={'BASIS': 'x', 'OTHER': 'y'},
         argv=['zzph4'],
         ok=V(exit=0, has=['halves from the environment', 'BASIS=x; OTHER=y'])),

    # ---- run-evening.sh, the run list's quiet machine steps as one command
    case('evening-chains-the-stages', 'run-evening.sh', None,
         'CONTROL: gate inherited, alarm, sequence and riders land in one'
         ' command, and the status file ends with the machine handed back',
         # The whole evening in seconds on the stand-ins: the note records
         # a clean gate, so that stage is inherited; the sequence runs
         # eighteen processes off the shipped run; the riders take one leg
         # a half (ONLY, a smoke run's restriction, keeps them to it). The
         # counted work left this driver on 2026-09-03 and has its own
         # cases below, which is what `counts a1g` must not appear for.
         shadow=dict(extra=lambda: evening_fixture('zzev')),
         # SATURATE on the launch line and a stand-in that prints the
         # preamble's line under it: the sequence's processes must carry
         # it and the CLEAN riders must not, the driver stripping it.
         env={'MAXBUSY': '100', 'FAKE_SATURATE': '1',
              'ONLY': main_shapes()[0]},
         argv=['zzev'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzev-evening.txt')).read(),
         ok=V(exit=0, has=['gate: inherited', 'alarm:', 'sequence: done, rc=0',
                           'riders a1g clean: done, rc=0',
                           'riders lookrts clean: done, rc=0',
                           'RIDERS DONE AND THE MACHINE IS FREE'],
              hasnt=['COMPLAINT', 'STOPPED', 'counts a1g'])),

    case('alonelegs-refuses-a-saturated-clean-leg', 'run-alonelegs.sh', None,
         'CONTROL: a clean leg whose log carries the preamble line complains',
         # The mirror of the SAT check: SATURATE reaching a clean leg from
         # the launch environment dosed it, and nothing said so until
         # 2026-09-02 (found by review of run-evening.sh).
         shadow=dict(extra=lambda: halves('zzsc-lookrts')),
         env={'ONLY': main_shapes()[0], 'MAXBUSY': '100',
              'SATURATE': '1', 'FAKE_SATURATE': '1'},
         argv=['zzsc', 'lookrts'],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'zzsc-al-lookrts-driver.log')).read(),
         ok=V(exit=1, has=['@@saturate line on a CLEAN leg',
                           'DONE-ALONELEGS-zzsc-lookrts WITH COMPLAINTS'])),

    case('evening-stops-at-a-refused-gate', 'run-evening.sh', None,
         'CONTROL: a gate that fails mechanically stops the evening before'
         ' the sequence',
         shadow=dict(extra=[('zzeg-lookrts', FAKE_HALF), ('zzeg-a1g', FAKE_HALF),
                            ('zzeg-pair.txt', NOTE_STUB + 'LAUNCH: none\n'
                             'RIDERS: none\n')]),
         argv=['zzeg'],
         ok=V(exit=1, has=['EVENING STOPPED AT THE GATE'],
              hasnt=['sequence: start'])),

    case('evening-refuses-a-note-without-machine-lines', 'run-evening.sh',
         None,
         'CONTROL: a note lacking LAUNCH: or RIDERS: is refused naming them',
         shadow=dict(extra=[('zzem-pair.txt', NOTE_STUB)]),
         argv=['zzem'],
         ok=V(exit=1, has=['lacks a machine line', 'LAUNCH:', 'RIDERS:'],
              hasnt=['evening begins'])),

    # ---- run-counts-all.sh, the evening's second call -------------------
    # The counted work left run-evening.sh on 2026-09-03 so that the box
    # could be handed back at the riders (README, run list step 19a), and
    # these are what the split owes: every population still swept, the
    # complaints of both calls still tallied in one place, and the one
    # ordering error the split makes possible refused.
    case('counts-all-sweeps-every-population', 'run-counts-all.sh', None,
         'CONTROL: the main set and every class, control then basis apiece,'
         ' and the status file ends COMPLETE',
         shadow=dict(extra=[('zzca-lookrts', FAKE_HALF),
                            ('zzca-a1g', FAKE_HALF),
                            ('zzca-pair.txt', NOTE_STUB),
                            ('zzca-evening.txt', EVENING_DONE)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_ANSWERS)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzca'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzca-evening.txt')).read(),
         ok=V(exit=0, has=['counts a1g main: done, rc=0',
                           'counts lookrts main: done, rc=0',
                           'counts a1g rev: done, rc=0',
                           'counts lookrts other: done, rc=0',
                           'EVENING COMPLETE: every stage of both calls'],
              hasnt=['COMPLAINT'])),

    case('counts-all-tallies-the-first-call-too', 'run-counts-all.sh', None,
         'CONTROL: a complaint from the quiet stages survives a clean sweep'
         ' here',
         # The tally is read back off the status file rather than counted
         # in this process, which is what the split costs if it is not:
         # the two calls are one evening, and a sequence that complained
         # would otherwise be reported COMPLETE by the call after it.
         shadow=dict(extra=[('zzcb-lookrts', FAKE_HALF),
                            ('zzcb-a1g', FAKE_HALF),
                            ('zzcb-pair.txt', NOTE_STUB),
                            ('zzcb-evening.txt', EVENING_DONE_SORE)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_ANSWERS)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzcb'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzcb-evening.txt')).read(),
         ok=V(exit=1, has=['counts a1g main: done, rc=0',
                           'EVENING COMPLETE WITH 1 COMPLAINT(S) OVER BOTH'])),

    # The two patterns of one refusal, a case each: they are matched
    # separately, so a typo in either is invisible from the other.
    case('counts-all-refuses-a-stage-still-running', 'run-counts-all.sh',
         None,
         'CONTROL: counting beside a timed process is refused, the status'
         " file's last line saying a stage is still in flight",
         shadow=dict(extra=[('zzcc-lookrts', FAKE_HALF),
                            ('zzcc-a1g', FAKE_HALF),
                            ('zzcc-pair.txt', NOTE_STUB),
                            ('zzcc-evening.txt', EVENING_MID_STAGE)]),
         argv=['zzcc'],
         ok=V(exit=1, has=['does not end where the counted work begins',
                           'Nothing ran'],
              hasnt=['counted work begins for'])),

    case('counts-all-refuses-a-stopped-evening', 'run-counts-all.sh', None,
         'CONTROL: an evening stopped at the alarm has no run to count',
         shadow=dict(extra=[('zzcd-lookrts', FAKE_HALF),
                            ('zzcd-a1g', FAKE_HALF),
                            ('zzcd-pair.txt', NOTE_STUB),
                            ('zzcd-evening.txt', EVENING_STOPPED)]),
         argv=['zzcd'],
         ok=V(exit=1, has=['does not end where the counted work begins',
                           'Nothing ran'],
              hasnt=['counted work begins for'])),

    case('counts-all-refuses-before-the-quiet-stages', 'run-counts-all.sh',
         None,
         'CONTROL: with no status file at all the counted work is not what'
         ' the run owes next',
         shadow=dict(extra=[('zzce-lookrts', FAKE_HALF),
                            ('zzce-a1g', FAKE_HALF),
                            ('zzce-pair.txt', NOTE_STUB)]),
         argv=['zzce'],
         ok=V(exit=1, has=['the quiet stages have not run', 'Nothing ran'],
              hasnt=['counted work begins for'])),

    # ---- run-status.sh, doneness off the artifacts ---------------------
    case('status-reads-an-unstarted-run', 'run-status.sh', None,
         'CONTROL: with no artifact every checkable step reads NOT DONE and'
         ' the exit is 1',
         shadow=dict(),
         argv=['run98'],
         # The two document gates read done, being about the tree; every
         # artifact-reading step must not.
         ok=V(exit=1, has=['NOT DONE', 'STATUS: '],
              hasnt=['all done', '  1     done', '  17    done', '  20    done',
                     '  5     done'])),

    # ---- read-run.py --predictions --------------------------------------
    case('predictions-hold-and-kill', 'read-run.py', None,
         'CONTROL: a span inside its tolerance reads HELD, one outside KILLED,'
         ' and an item with no span is named as yours',
         plant=lambda t: {
             'run': synth_json(t, 'main'),
             'other': synth_json(t, 'main', name='other.json', slow=1.25),
             'doc': write(os.path.join(t, 'r.md'),
                          '# Run 99\n\n## What this run was built to answer,'
                          ' and what it answered\n\n(1) *a* `predict: cross'
                          ' list 0.8 within 1%`. (2) *b* `predict: cross list'
                          ' 1.0 within 1%`. (3) *c* nothing here.\n')},
         argv=['{run}', '--compare', '{other}', '--predictions',
               '--run-doc', '{doc}'],
         ok=V(exit=0, has=['cross list 0.8 within 1%',
                           '0.00 point(s) off, within 1.00%: HELD',
                           '20.00 point(s) off, within 1.00%: KILLED',
                           'yours to adjudicate: (3)'])),

    case('pair-halves-must-differ', 'run-major.sh', '0431efe',
         'one name in both halves wrote nine JSONs twice and gated clean',
         shadow=dict(extra=lambda text: halves('zzhh-lookrts', classes=classes_in(text))
                     + [('zzhh-pair.txt', 'a stand-in pair note.\n'
                         'HALVES: basis=lookrts other=lookrts\n')]),
         env={'OTHER': 'lookrts', 'BASIS': 'lookrts'},
         argv=['zzhh'],
         ok=V(exit=1, has=['a pair is two halves']),
         bug=V(exit=0)),

    case('class-name-carries-no-hyphen', 'run-major.sh', '8cb5eb7',
         'a hyphenated class merged with the one before its hyphen',
         shadow=dict(mutate=[('run-major.sh', 'window scaled',
                              'window scaled bcast-mid')],
                     extra=lambda text: halves('zzhy-lookrts', 'zzhy-a1g', classes=classes_in(text))
                     + [('zzhy-pair.txt', NOTE_STUB)]),
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
                     extra=lambda: halves('zzxf-lookrts', 'zzxf-a1g')
                     + [('zzxf-pair.txt', NOTE_STUB)]),
         env={'SHAPE': main_shapes(1)[0], 'CLASS': class_shapes('window')[0],
              'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzxf'],
         ok=V(exit=1, has=['did NOT refuse']),
         # No --audit: the driver itself reads the split, so an older copy
         # of it cannot be run against this tree at all. 2026-08-25.
         ),

    case('major-run-runs-clean', 'run-major.sh', None,
         'CONTROL: the whole sequence, eighteen processes, on stand-ins',
         shadow=dict(extra=lambda text: halves('zzmj-lookrts', 'zzmj-a1g', classes=classes_in(text))
                     + [('zzmj-pair.txt', NOTE_STUB)]),
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
         shadow=dict(extra=lambda text: halves('zzrl-lookrts', 'zzrl-a1g', classes=classes_in(text))
                     + [('zzrl-pair.txt', NOTE_STUB),
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
         shadow=dict(extra=lambda text: halves('zzrp-lookrts', 'zzrp-a1g', classes=classes_in(text))
                     + [('zzrp-pair.txt', NOTE_STUB),
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
         shadow=dict(extra=lambda text: halves('zznn-lookrts', 'zznn-a1g', classes=classes_in(text))),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zznn'],
         ok=V(exit=1, has=['no zznn-pair.txt'], hasnt=['major run begins']),
         bug=V(exit=0, has=['!! no zznn-pair.txt', 'major run complete'])),

    case('provenance-git-could-not-read', 'run-major.sh', '845c8d0',
         'a run whose git failed recorded a commitless, CLEAN-looking tree',
         shadow=dict(extra=lambda text: halves('zzmj-lookrts', 'zzmj-a1g', classes=classes_in(text))
                     + [('zzmj-pair.txt', NOTE_STUB)]),
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
         shadow=dict(extra=lambda text: [('zzmj-lookrts',
                                     UNDERPRINT.replace('@HALF@', 'lookrts')
                                               .replace('@RUN@', SRC))]
                     + halves('zzmj-a1g', classes=classes_in(text))
                     + whole_run(['lookrts'], classes=classes_in(text))
                     + [('zzmj-pair.txt', NOTE_STUB)]),
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
         plant=lambda t: {'doc': edited_rundoc(
             t, ('**`window` --- overlapping', '**`window` - overlapping'))},
         shadow=dict(extra=lambda: whole_run(['lookrts'], prefix='zzit',
                                      classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzit'],
         # No --audit: this fixture is built from the live README, which
         # the Basic Latin pass reworded under it. Removal is the handling.
         ok=V(exit=1, has=['the two ways this file finds a class block',
                           'missing from the pattern: window'],
              hasnt=['matched by the pattern only'])),

    case('no-class-block-leads', 'install-tables.sh', '4086ab8',
         'the guard against a silently skipped class was itself silent',
         plant=lambda t: {'doc': rundoc_without_class_leads(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts'], prefix='zzit',
                                      classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzit'],
         ok=V(exit=1, has=['no class block leads'], hasnt=['REFUSED']),
         bug=V(has=['REFUSED'], hasnt=['no class block leads'])),

    case('heading-between-two-class-blocks', 'install-tables.sh', None,
         "a paragraph between blocks took the block above it's figures",
         plant=lambda t: {'doc': rundoc_heading_between_blocks(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts', 'ovhalf'],
                                             prefix='zzit',
                                             classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzit'],
         probe=lambda subs: open(subs['doc']).read(),
         # No --audit: this fixture is built from the live README, which
         # the Basic Latin pass reworded under it. Removal is the handling.
         ok=V(exit=0, has=['ZZMARKER',
                           'across 9 class block(s)'])),

    case('placeholder-that-outlived-its-wording', 'install-tables.sh',
         None,
         'a reworded emit installed a literal `___` into the run file',
         plant=lambda t: {'doc': edited_rundoc(t)},
         shadow=dict(mutate=[
             ('read-run.py',
              "print('**Provenance:** elapsed ___, peak ___ MiB in use, ___ MiB"
              " max'",
              "print('**Provenance:** elapsed ___, peak of ___ MiB in use, ___"
              " MiB max'")],
             extra=lambda: whole_run(['lookrts', 'ovhalf'], prefix='zzit', classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzit'],
         probe=lambda subs: open(subs['doc']).read(),
         # No --audit: this fixture is built from the live README, which
         # the Basic Latin pass reworded under it. Removal is the handling.
         ok=V(has=['placeholder survived'], hasnt=['peak of ___ MiB'])),

    case('two-shape-class-refused-before-writing', 'install-tables.sh',
         None,
         'a two-shape class aborted AFTER eleven tables were already in',
         plant=lambda t: {'doc': edited_rundoc(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts'], prefix='zzts',
                                     short_class='scaled', classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzts'],
         # No --audit: this fixture is built from the live README, which
         # the Basic Latin pass reworded under it. Removal is the handling.
         ok=V(exit=1, has=['fewer than three shapes',
                           'NOTHING HAS BEEN WRITTEN'],
              hasnt=['table(s) installed'])),

    case('install-refuses-a-standing-cross-half-line',
         'install-tables.sh', None,
         'a cross-half line left standing under this run, at exit 0',
         # An absent other-half JSON is correct for a run that recorded
         # one half and is a WRONG `OTHER` otherwise, and the two look
         # identical. A note naming both readings was the first answer,
         # and it left the previous run's `Across the halves:` paragraph
         # standing under this run's tables at exit 0 -- so where the
         # block still carries one, the install refuses. 2026-09-01.
         plant=lambda t: {'doc': edited_rundoc(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts'], prefix='zzxh',
                                             classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'nosuchhalf'},
         argv=['zzxh'],
         ok=V(exit=1, has=['REFUSED', 'left standing', 'OTHER=nosuchhalf'])),

    case('install-notes-a-one-half-run', 'install-tables.sh', None,
         'CONTROL: no other half and no paragraph to leave standing is a'
         ' one-half run, noted and not refused',
         plant=lambda t: {'doc': rundoc_without_across(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts'], prefix='zzxh',
                                             classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'nosuchhalf'},
         argv=['zzxh'],
         ok=V(exit=0, has=['no cross-half line is installed'],
              hasnt=['REFUSED'])),

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
         plant=lambda t: {'doc': edited_rundoc(t, (
             '\n\n' + an_across_paragraph(), ''))},
         shadow=dict(extra=lambda: whole_run(['lookrts', 'ovhalf'],
                                     prefix='zzx5', classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzx5'],
         ok=V(exit=1, has=['REFUSED', 'no `Across the halves:`'])),

    case('basis-glob-catches-no-other-half', 'install-tables.sh', '440b22d',
         'a control half named <basis>-pa was installed as the basis',
         plant=lambda t: {'doc': edited_rundoc(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts'], prefix='zzhg', classes=recorded_classes())
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
         plant=lambda t: {'doc': edited_rundoc(
             t, ('**`bcastmid` ---', '**`bcast-mid` ---'))},
         shadow=dict(extra=lambda: whole_run(['lookrts'], prefix='zzhl', classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts'},
         argv=['zzhl'],
         # The old script's signature and not merely the absence of the
         # new refusal: the renamed block's own table install REFUSED, and
         # the computed paragraphs went in across SEVEN blocks, the eighth
         # having been handed the one above it.
         ok=V(exit=1, has=['carries a hyphen'], hasnt=['table(s) installed']),
         bug=V(exit=1, has=['REFUSED', 'across %d class block(s)' % (len(recorded_classes()) - 1)],
               hasnt=['carries a hyphen'])),

    case('install-is-idempotent', 'install-tables.sh', None,
         'CONTROL: a full pass over an untouched run file rewrites no table',
         # Both halves, as the live procedure has them: the run file
         # carries every class's cross-half paragraph, and a one-half
         # install against it is the standing-line state refused above.
         plant=lambda t: {'doc': edited_rundoc(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts', 'ovhalf'],
                                             prefix='zzit',
                                             classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzit'],
         ok=V(exit=0, has=['12 table(s) installed'])),

    # ---- read-run.py --note, the previous pair note for the next pair ---
    case('note-read-withholds-the-handover', 'read-run.py', None,
         "CONTROL: --note drops the previous run's handover and keeps its"
         ' build lines',
         # Reading-list item 10 made executable. Both directions asserted:
         # a filter that dropped everything would satisfy the `hasnt` half
         # alone, and one that dropped nothing the `has` half alone.
         plant=stub_pair_note,
         argv=['--note', '{note}'],
         ok=V(exit=0,
              has=['A CARRIED BLOCK', 'md5 g912', '--list', 'handover'],
              hasnt=['ENTRY POINT FOR THE SESSION', 'GATE VERDICT',
                     'sequence         RUN in one window'])),

    case('note-draft-spares-a-hyphenated-name', 'read-run.py', None,
         'CONTROL: --draft renames the half and not the form it is spelled'
         ' inside',
         # `-` is a word boundary, so a `\\b`-bounded rename of the half
         # `spot` also renames `dead-spot`, which is the form the pair
         # varies rather than a half at all. mutants.py carries the proof.
         plant=stub_pair_note,
         argv=['--note', '{note}', '--draft', 'run24',
               '--halves', 'g912,ghead'],
         # `run23-spot` is NOT in the `hasnt`: the header LOGS every
         # substitution by name, so the old name is owed there and a
         # blanket absence check would fail on the log it wants.
         ok=V(exit=0,
              has=['the dead-spot form, run24-ghead, ghead alone, a',
                   'spot-check, hotspot and spotless',
                   'HALVES: basis=g912 other=ghead',
                   'bare spot -> ghead'],
              hasnt=['dead-ghead', 'ghead-check', 'hotghead', 'gheadless'])),

    case('draft-renames-a-half-onto-the-other', 'read-run.py', 'abd8ed8',
         'renaming one half at a time fed each result to the next rename',
         # The new BASIS reuses the old OTHER's name, which is ordinary --
         # Run 24's own pair moved `other` from spot back to ghead. Renamed
         # in turn, `g912` became `spot` and the second rename took that to
         # `ghead`, so both halves of the carried-over note read `ghead`
         # and the substitution log looked right. One pass now.
         plant=lambda t: {'note': write(
             os.path.join(t, 'run23-pair.txt'),
             "hdr\n\nA [SAME]: g912 leads, spot follows; run23-g912 and"
             " run23-spot.\nHALVES: basis=g912 other=spot\n")},
         argv=['--note', '{note}', '--draft', 'run24', '--halves',
               'spot,ghead'],
         ok=V(exit=0, has=['spot leads, ghead follows'],
              hasnt=['ghead leads, ghead follows']),
         bug=V(exit=0, has=['ghead leads, ghead follows'])),

    # ---- preflight.sh, the pre-run list's steps 4 to 10 in one call -----
    # ---- the review of 2026-09-04 ----------------------------------------
    # Fifteen findings over the shell and Python here, by a reviewer reading
    # the files whole; a case for each program that can be driven, and a
    # record alone for the four that cannot (a judge, a docstring, a probe).
    case('gate-refuses-an-arm-its-list-lacks', 'run-gate.sh', '5ef414d',
         'SEL named two arms the prune had parked, and the count that would'
         ' say so was checked per process, after its forty minutes',
         # `build` and `mut-odo` went to `Only` in 41d3bad and the gate's
         # selection kept naming them, so every process would have come
         # back three arms short of EXPECT and the gate failed after its
         # full run. The list is read before the first process now, and a
         # name it lacks refuses there; the selection names timed arms.
         shadow=dict(mutate=[('run-gate.sh',
                              "'*/sum-only-early' '*/sum-only-late')",
                              "'*/sum-only-early' '*/sum-only-late' '*/offtab')")],
                     extra=[('zzgl-a1g', FAKE_HALF), ('zzgl-lookrts', FAKE_HALF),
                            ('zzgl-pair.txt', NOTE_STUB)]),
         argv=['zzgl'],
         ok=V(exit=1, has=['!! SEL names */offtab'], hasnt=['gate begins']),
         # `SEL names` alone is in the old per-process complaint too.
         bug=V(has=['gate begins'], hasnt=['!! SEL names'])),

    case('evening-does-not-inherit-a-gate-of-other-binaries',
         'run-evening.sh', '465501c',
         'a clean GATE block was inherited by its text, after a rebuild too',
         # The block is tied to the binaries it gated by the md5 line
         # run-gate.sh writes; a rebuilt half has another md5, so the
         # newest clean block is of other binaries and the gate runs again.
         # Before, the evening ran hours on a pair that was never gated.
         shadow=dict(extra=lambda: evening_fixture('zzes', stale=True)),
         env={'MAXBUSY': '100', 'FAKE_SATURATE': '1',
              'ONLY': main_shapes()[0]},
         argv=['zzes'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzes-evening.txt')).read(),
         ok=V(has=['gate: NOT inherited', 'other binaries', 'gate: start'],
              hasnt=['gate: inherited']),
         bug=V(has=['gate: inherited'], hasnt=['gate: start'])),

    case('evening-does-not-inherit-an-untied-gate', 'run-evening.sh', '465501c',
         'a clean GATE block with no halves line inherited the same way',
         # A block from before the md5 line cannot be tied to any binary,
         # so it is not inherited either, and the stamp says which.
         shadow=dict(extra=lambda: evening_fixture('zzeu', md5=False)),
         env={'MAXBUSY': '100', 'FAKE_SATURATE': '1',
              'ONLY': main_shapes()[0]},
         argv=['zzeu'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzeu-evening.txt')).read(),
         ok=V(has=['gate: NOT inherited', "no 'halves md5:' line",
                   'gate: start'],
              hasnt=['gate: inherited']),
         bug=V(has=['gate: inherited'], hasnt=['gate: start'])),

    case('status-blocks-without-wrap80', 'run-status.sh', '87c77f0',
         'with wrap80 off PATH the README verdicts were read off an empty file',
         # `wrap80 --unwrap README.md > $TMP/readme 2>/dev/null` dropped
         # the status, so steps 10, 12a and 12c judged an empty file and
         # step 7 printed an empty reason, --check-doc's BLOCKED line
         # being grepped for FAIL alone. A tool the reading needs and
         # cannot find is exit 2 here, as everywhere in this directory.
         shadow=dict(),
         env={'PATH': '/usr/bin:/bin'},
         argv=['run98'],
         ok=V(exit=2, has=['BLOCKED', 'wrap80'], hasnt=['STATUS: ']),
         bug=V(exit=1, has=['NOT DONE', 'STATUS: '], hasnt=['wrap80'])),

    case('status-counts-only-stamped-complaints', 'run-status.sh', '87c77f0',
         'a GATE block quoted into the wallclock log counted as a complaint',
         # run-major.sh copies the note's GATE blocks into the log, and a
         # FAILED one carries `!!`; read-all.sh anchors its count on the
         # driver's own stamp for exactly this reason (its case
         # `quoted-note-block-is-not-a-run-complaint`) and step 17 did
         # not, so a note that had once recorded a failed gate read the
         # run NOT DONE for ever.
         shadow=dict(extra=[('run97-wallclock.log',
                             '=== 2026-09-04T00:00:00+02:00 major run begins\n'
                             '      GATE: run 2026-09-03. Mechanically FAILED,'
                             ' 1 complaint(s):\n'
                             '          !! the machine check FAILED -- read it'
                             ' before the evening\n'
                             '=== 2026-09-04T01:00:00+02:00 major run complete'
                             '\n')]),
         argv=['run97'],
         ok=V(has=['run97-wallclock.log says complete, no complaint'],
              hasnt=["'!!' line(s)"]),
         bug=V(has=["with 1 '!!' line(s)"], hasnt=['no complaint'])),

    case('smoke-exercises-the-arm-filter', 'smoke-sweep.sh', '5ef414d',
         '--exclude was exercised on an Only arm, so it removed nothing',
         # `bq-expand-b` has been `Only` since c10e8cf, in no --list and
         # no run JSON, and the line's own comment records the same
         # vacuity once fixed for `concat-runs`. The arms come from the
         # run's list now: one is excluded for the mode's ordinary path,
         # and all of them for the refusal that is the check -- the shape
         # filter's form, which a reader ignoring --exclude cannot pass.
         shadow=dict(mutate=[('read-run.py',
                              'strategies = [s for s in strategies if s not'
                              ' in args.exclude]',
                              'strategies = list(strategies)')],
                     extra=lambda: halves('zzxa-lookrts', 'zzxa-a1g')
                     + [('zzxa-pair.txt', NOTE_STUB)]),
         env={'SHAPE': main_shapes(1)[0], 'CLASS': class_shapes('window')[0],
              'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzxa'],
         ok=V(exit=1, has=['every arm', 'did NOT refuse']),
         bug=V(exit=0, has=['sweep clean'], hasnt=['did NOT refuse'])),

    case('predictions-block-without-wrap80', 'read-run.py', '690a3b5',
         'with wrap80 off PATH --predictions read the wrapped README and'
         " adjudicated the run file's section instead",
         # The README is read unwrapped because a lead spanning a line
         # break matches nothing; the fallback read the wrapped file,
         # missed the lead, and went on to the run doc's section -- the
         # previous run's, before post-run step 5 -- at a normal exit.
         # The file's other two wrap80 sites say BLOCKED; so does this.
         plant=lambda t: {
             'run': synth_json(t, 'main', name='run99-x-main.json'),
             'other': synth_json(t, 'main', name='other.json', slow=1.25),
             'doc': write(os.path.join(t, 'r.md'),
                          '# Run 99\n\n## What this run was built to answer,'
                          ' and what it answered\n\n(1) *a* `predict: cross'
                          ' list 0.8 within 1%`.\n')},
         env={'PATH': '/usr/bin:/bin'},
         argv=['{run}', '--compare', '{other}', '--predictions',
               '--run-doc', '{doc}'],
         ok=V(exit=2, has=['BLOCKED', 'wrap80'], hasnt=['HELD', 'KILLED']),
         bug=V(exit=0, has=['HELD'], hasnt=['BLOCKED'])),

    case('predictions-alone-is-refused', 'read-run.py', '690a3b5',
         '--predictions without --compare was absorbed without a word',
         # Missing from all three roll calls: the modifier loop, `modes`
         # and `subs`. Alone it printed the default table at exit 0.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--predictions'],
         ok=V(exit=2, has=['--predictions is a modifier of --compare']),
         bug=V(exit=0, hasnt=['is a modifier'])),

    case('predictions-and-alloc-are-two-readings', 'read-run.py', '690a3b5',
         '--compare X --predictions --alloc dropped --alloc without a word',
         # The predictions arm of the dispatch precedes the alloc one, and
         # `subs` did not list predictions, so the second reading was
         # never run and nothing said so. `--counts` is the one sub-flag
         # --predictions reads rather than clashes with.
         plant=lambda t: {
             'run': synth_json(t, 'main'),
             'other': synth_json(t, 'main', name='other.json', slow=1.25)},
         argv=['{run}', '--compare', '{other}', '--predictions', '--alloc'],
         ok=V(exit=2, has=['are 2 readings of --compare']),
         bug=V(hasnt=['readings of --compare'])),

    case('properties-limit-bounds-runs-not-figures', 'properties.py', 'ae6cbce',
         'CORPUS_LIMIT broke the innermost loop of the round-trip, bounding'
         ' neither the sweep nor the count it reported',
         # The break sat after `n += 1` in the per-figure loop, so every
         # run was still opened, one figure was checked, and the report
         # said the whole corpus; the mutant `fmt_abs labels every unit ns`
         # rested on that one figure. The limit counts runs, as the two
         # siblings and the docstring have it.
         plant=corpus_of_two,
         env={'CORPUS': '{corpus}', 'CORPUS_LIMIT': '1'},
         argv=[],
         ok=V(exit=0, has=['prop_abs_round_trip', 'in 1 run(s)'],
              hasnt=['in 2 run(s)']),
         bug=V(has=['in 2 run(s)'], hasnt=['in 1 run(s)'])),

    case('properties-name-an-unreadable-run', 'properties.py', 'ae6cbce',
         'a JSON that would not load was skipped and counted as covered',
         # `except Exception: continue`, and the report then counted every
         # file in the directory. A file cut off mid-write is what a
         # killed process leaves, and the property names it now.
         plant=corpus_with_an_unreadable_run,
         env={'CORPUS': '{corpus}'},
         argv=[],
         ok=V(exit=1, has=['truncated-main.json', 'unreadable', 'in 1 run(s)'],
              hasnt=['in 2 run(s)']),
         bug=V(exit=1, has=['in 2 run(s)'], hasnt=['unreadable'])),

    # The shadow guard, four forms it read as relative: `--` before the
    # path, a tilde, `$HOME`, and `pushd`. No tracked script uses them.
    case('shadow-refuses-a-double-dash-cd', 'defects.py', '462fb1b',
         '`cd -- /path` slipped the guard',
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'cd -- /nowhere-zz\\n')"],
         ok=V(has=['cds to an absolute path']),
         bug=V(has=['/shadow'], hasnt=['cds to an absolute path'])),

    case('shadow-refuses-a-tilde-cd', 'defects.py', '462fb1b',
         '`cd ~/path` slipped the guard',
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'cd ~/nowhere-zz\\n')"],
         ok=V(has=['cds to an absolute path']),
         bug=V(has=['/shadow'], hasnt=['cds to an absolute path'])),

    case('shadow-refuses-a-home-cd', 'defects.py', '462fb1b',
         '`cd "$HOME/path"` slipped the guard',
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'cd \"$HOME/nowhere-zz\"\\n')"],
         ok=V(has=['cds to an absolute path']),
         bug=V(has=['/shadow'], hasnt=['cds to an absolute path'])),

    case('shadow-refuses-a-pushd', 'defects.py', '462fb1b',
         '`pushd /path` slipped the guard',
         plant=lambda t: {'tmp': t},
         argv=['--unit', "shadow_dir('{tmp}', 'probe-areacurve.sh',"
                         " 'pushd /nowhere-zz\\n')"],
         ok=V(has=['cds to an absolute path']),
         bug=V(has=['/shadow'], hasnt=['cds to an absolute path'])),

    # Four records without a case: a judge, two docstrings and a probe.
    case('era-judge-writes-the-shared-copy', 'mutants.py', '462fb1b',
         "the era_main_hs judge planted its probe shape into the copy's"
         ' Main.hs, which nothing restored',
         # selftest-mutants.py restores the MUTATED file and no other, so
         # the two runs of that judge left two `zz-era-probe` entries for
         # every later judge to read. The judge points era_main_hs at a
         # planted copy of its own now. No verdict moved.
         argv=None, ok=None),

    case('mutants-name-a-property-without-one', 'mutants.py', '462fb1b',
         '"the three properties" stood over mutants for two',
         # `prop_table_reads_back` had none, and properties.py still
         # carried the dated 2026-08-17 sentence the docstring says was
         # retired into this file. The mutant widens `readme_rows`'
         # column test by one, as that proof did.
         argv=None, ok=None),

    case('match-docstring-claims-any-length', 'loop-offsets.py', 'd2ffa65',
         "--match said it looked among the twin's loops of any length",
         # It looks among `innermost(twin)`, capped at the line as the
         # survey is, and loses nothing by it: a byte-identical copy has
         # the same length, and no NOT NAMED on today's binaries is
         # rescued by lifting the cap. The prose now says what runs.
         argv=None, ok=None),

    case('probe-cache-count-is-a-literal', 'probe-cache-run.sh', '5ef414d',
         'WANT was a literal over an arm list that included an Only arm',
         # `lib-stage2` went to `Only` on 2026-09-04, so the probe would
         # have run and failed on 12 against 14. The list is read before
         # launch now, an arm it lacks refusing there, and WANT is what
         # the list carries. The probe's question is spent (README).
         argv=None, ok=None),

    case('preflight-names-a-retired-callee', 'preflight.sh', '81876de',
         'a retirement left preflight calling a script that had gone',
         # NO CASE, and the reason is the one checks.py's UNCOVERED gives
         # for the program: preflight's steps ARE this corpus and the
         # reader's gates, so a case would run them twice. What that costs
         # is this record. The retirement of check-scripts.py taught the
         # README, checks.py and the reader chapter the new commands and
         # left preflight's three calls behind, and nothing in the tree
         # runs those calls, so the three steps were dark from 2026-09-02
         # until Run 24's preparation ran them by hand. The bug direction
         # was WATCHED rather than remembered -- the first
         # `./preflight.sh run24` printed all three FAILs -- which is what
         # `proved` says here without a case to replay it.
         argv=None, ok=None),
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
    # And `cd -- /`, `cd ~/`, `cd "$HOME/` and `pushd /` since 2026-09-04,
    # four more escapes, each with a case; no tracked script uses them.
    if re.search(r'^\s*(cd|pushd)\s+(--\s+)?["\']?(/|~|\$HOME)', text, re.M):
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
    # A thunk where building it is slow: `whole_run` writes nine
    # populations a half, and evaluated in the `CASES` literal it ran for
    # every case naming one before argparse, which took `--list` from 0.1 s
    # to 2.1 s. 2026-09-01.
    if callable(extra):
        # An `extra` taking one argument is handed the SCRIPT'S TEXT, at the
        # revision under test, so a stand-in can ship what that era's
        # driver expects -- the classes its literal names, and no others.
        # The audit replays a 2026-08-22 driver against a stand-in carrying
        # the `runs` class added later, and the driver refused at its class
        # check before reaching the defect (found 2026-09-02).
        extra = extra(text) if _takes_text(extra) else extra()
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


# What the shared runner needs to know about this directory; the docstring
# above says why each is as it is.
CONFIG = {
    'run_dir': 'here',
    'materialise': 'file',
    'timeout': 600,
    # A session's own launch habit must not reach a case: BASIS or OTHER
    # exported in the shell makes every stub note refuse, and the switches
    # would dose or restrict a driver the case did not ask to.
    'strip_env': ['BASIS', 'OTHER', 'SATURATE', 'SATURATE_BY', 'WILDLOG',
                  'SAT', 'ONLY', 'ARMS', 'N', 'MAXBUSY', 'FAKE_SATURATE'],
    'cleanup': sweep,
}
