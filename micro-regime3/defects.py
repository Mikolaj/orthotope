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
    Results table, the run's own geomeans, the fingerprint,
    the class blocks and the run's own provenance all live in
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
        print('BLOCKED: no runs/run<N>.md in %s -- the Results table'
              ' and the class blocks are all in one, so'
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


def plant_begins_mid_sentence(tmp):
    """The run file with a paragraph's opening words gone, as Run 22's
    write-up left its anchors paragraph: the Provenance lead every run
    file carries, lower-cased mid-sentence."""
    return unwrapped_rundoc_edit(
        tmp, '**Each stride class carries an anchor of its own',
        'carries an anchor of its own')


def plant_cut_before_heading(tmp):
    """The run file with the paragraph before its class section cut
    mid-sentence, where a heading follows and the stop check excused it
    until 2026-09-26."""
    return unwrapped_rundoc_edit(
        tmp, "and the equal weighting of shapes are [README's *Reading a"
             " run file*](../README.md#reading-a-run-file).",
        'and the equal weighting of shapes are')


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

    Both halves planted: a Main.hs copy retiring timed shapes, and a README
    declaring them retired after the run -- so the newest run file's `over
    N shapes` are held to a main set that keeps them. Drop the
    declaration's effect and every one of them matches no population.
    HOW MANY it retires is derived, not one: the check also accepts a count
    equal to today's timed set, so the fixture retires enough shapes to put
    today's set below the run's population, else a main set one shape
    larger than the run's lands on the run's count once one is retired and
    the dropped exemption goes unseen -- which is how the mutant survived
    on 2026-09-05, the day a shape was timed again. Planted under the
    Provenance heading, as the class fixture is. Added 2026-09-04.
    """
    main = open(MAIN).read()
    old = 'retiredShapes =\n  [ '
    if main.count(old) != 1:
        raise AssertionError('retiredShapes list occurs %d times, need 1'
                             % main.count(old))
    names = []
    for lst in ('convShapes', 'stretchShapes'):
        body = main.split('\n%s =\n' % lst, 1)[1].split('\n  ]', 1)[0]
        names += re.findall(r'\("([\w-]+)",\s*\[', body)
    readme = subprocess.run(['wrap80', '--unwrap'], input=open(README).read(),
                            capture_output=True, text=True, check=True).stdout
    declared = set()
    for m in DECLARED_AFTER_RE.finditer(readme):
        declared |= set(re.findall(r'`([\w.-]+)`', m.group(1)))
    declared_retired = set()
    for m in DECLARED_RETIRED_RE.finditer(readme):
        declared_retired |= set(re.findall(r'`([\w.-]+)`', m.group(1)))
    retired = _reader().retired_shapes(MAIN)
    timed = [n for n in names if n not in retired]
    # The run's population as the reader derives it, and one more retired
    # than the gap between today's set and it.
    was = len(timed) - len(declared & set(timed)) + len(declared_retired & retired)
    # The run's own count is what the dropped exemption must leave matching
    # no population, and a fixture cannot choose it; say so loudly rather
    # than let the mutant survive as it did once a class reached a count.
    assert was not in class_population_sizes(), (
        'the run file\'s main-set count %d is also a class population\'s'
        ' size, so no retirement here can make the mutant see anything' % was)
    n = max(1, len(timed) - was + 1)
    picks = []
    for sh in ['vgg-14-c512-k3'] + list(reversed(timed)):
        if sh in timed and sh not in declared and sh not in picks:
            picks.append(sh)
    picks = picks[:n]
    assert len(picks) == n, 'not enough undeclared timed shapes to retire'
    entries = ''.join('"%s"\n  , ' % sh for sh in picks)
    out = {'main': write(os.path.join(tmp, 'Main.hs'),
                         main.replace(old, old + entries, 1))}
    ticked = ['`%s`' % sh for sh in picks]
    decl = (ticked[0] if n == 1
            else ', '.join(ticked[:-1]) + ' and ' + ticked[-1])
    out['readme'] = unwrapped_readme_edit(
        tmp, '\n## Provenance\n',
        '\n## Provenance\n\n%s %s retired 2026-09-04, after the run.\n'
        % (decl, 'was' if n == 1 else 'were'))
    return out


def class_population_sizes():
    """The size of every timed class population Main.hs defines.

    A fixture that plants a main-set count checks it against these: the
    population check accepts a quoted count equal to ANY population's size,
    so a planted count landing on a class's size makes a check that drops
    an exemption pass anyway -- which is how the added-after mutant
    survived Run 34's check-all, `runs` having grown to seventeen views.
    """
    classes = {}
    for s, d in _reader().dims_by_shape(MAIN)[0].items():
        if d['cls'] != 'main' and not d['retired']:
            classes.setdefault(d['cls'], set()).add(s)
    return {len(v) for v in classes.values()}


def plant_main_shapes_exempt(tmp):
    """The fixture of `main-shapes-added-after-the-run-are-exempt`.

    Both halves planted, and the figure derived rather than written: a
    declaration in README of one or two main-set shapes never added
    after any run, and a run file whose every `over N shapes` at the run's
    TRUE main-set size -- Main.hs's timed set less whatever the live
    README already declares added, plus what it declares retired -- is
    moved down by the ones planted, to a count no class carries. So the
    fixture builds
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
    # The moved count must be NO population's size, or the mutant that
    # drops the exemption finds it matching a class and survives: two
    # planted took 19 to 17 on the day `runs` grew to seventeen views
    # (971ffb6), and the mutant survived Run 34's check-all. So plant one
    # shape where two would land on a class size.
    sizes = class_population_sizes()
    fake = next(fake[:k] for k in (2, 1) if was - k not in sizes)
    now = was - len(fake)
    doc = subprocess.run(['wrap80', '--unwrap'], input=rundoc_text(),
                         capture_output=True, text=True, check=True).stdout
    # README quotes the run's population too, so both documents move.
    pat = re.compile(r'\bover (all )?%d shapes' % was, re.I)
    assert pat.search(doc), (
        'the run file quotes no `over %d shapes`, so this fixture cannot'
        ' build and the case and its mutant go with it. A write-up that'
        ' spells the figure in words removes the only digit form the file'
        ' carried -- Run 36 wrote `nineteen main-set shapes` -- so keep'
        ' the digits where a sentence names the main set' % was)
    down = lambda m: 'over %s%d shapes' % (m.group(1) or '', now)  # noqa: E731
    doc = pat.sub(down, doc)
    readme = pat.sub(down, readme)
    anchor = '## Provenance\n'
    assert readme.count(anchor) == 1
    readme = readme.replace(anchor, anchor + '\n%s %s added'
                            ' 2026-09-02, after the run.\n'
                            % (' and '.join('`%s`' % n for n in fake),
                               'were' if len(fake) > 1 else 'was'), 1)
    return {'readme': write(os.path.join(tmp, 'R.md'), readme),
            'rundoc': write_rundoc(tmp, doc)}


def plant_fills_entry_region(tmp):
    """A Cmm dump of two arms' workers and the LLVM assembly of both, with
    the second worker's loop where LLVM's rotation leaves it: in the
    function's entry region, before its first `_blk_` label, right after
    the first worker's last block and a tab-indented `.size`."""
    dump = write(os.path.join(tmp, 'fixture.dump-cmm'), (
        '$wfbA_QaA_entry() { //  [R1]\n'
        '     QA0: // global\n'
        '         call $wgo_QA_info(R1) args: 8, res: 8, upd: 8;\n'
        '}\n'
        '$wgo_QA_entry() { //  [R1]\n'
        '     QA1: // global\n'
        '         call (P64[Sp])() args: 8, res: 0, upd: 8;\n'
        '}\n'
        '$wfbB_QbB_entry() { //  [R1]\n'
        '     QB0: // global\n'
        '         call $wgo_QB_info(R1) args: 8, res: 8, upd: 8;\n'
        '}\n'
        '$wgo_QB_entry() { //  [R1]\n'
        '     QB1: // global\n'
        '         call (P64[Sp])() args: 8, res: 0, upd: 8;\n'
        '}\n'))
    asm = write(os.path.join(tmp, 'fixture.s'), (
        'QA_info$def:\n'
        '\tmovq\t%rdi, %rax\n'
        '_blk_QA1$def:\n'
        '\tret\n'
        '\t.size\tQA_info$def, .Lfunc_end1-QA_info$def\n'
        'QB_info$def:\n'
        '\tmovq\t%rdi, %rax\n'
        '.LBB2_1:\n'
        '\tmovsd\t(%rdi), %xmm0\n'
        '\tmovsd\t%xmm0, (%rsi)\n'
        '\taddq\t$8, %rsi\n'
        '\tdecq\t%rcx\n'
        '\tjne\t.LBB2_1\n'
        '_blk_QB1$def:\n'
        '\tret\n'
        '\t.size\tQB_info$def, .Lfunc_end2-QB_info$def\n'))
    return {'dump': dump, 'asm': asm}


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


def rundoc_with_a_results_table(tmp, time='0.025'):
    """A run file carrying a Results table with one row worth reading.

    Post-run 5a compares the published column the install is about to
    overwrite against the one going in, so the fixture is a table with a
    figure in it and nothing else: `--movement` reads the row by name and
    the rest of the file is what a run file must look like for the table
    to be found at all.
    """
    m = _reader()
    return write_rundoc(
        tmp,
        '# Run 96\n\n## Results\n\nA paragraph above the table.\n\n'
        + m.RESULTS_HDR + '\n'
        + '|---|---:|---:|---:|---:|---:|---|\n'
        + '| lib-stage2-lean | %s | 0.113 | 0.53 | 69 | 1.00x | a tier |\n'
          % time
        + '| list (baseline) | 1.000 | 1.000 | 0.74 | 21 | 25.20x | -- |\n'
        + '\nA paragraph below it.\n')


def pair_with_a_compare_run(tmp):
    """Run 98's basis JSON and note, the note naming `COMPARE: run97`, and
    what each cross-run default then reads: Run 97's note, its main JSON
    on both halves, and `runs/run97.md` with a Results table.

    Run 97's halves are named apart from Run 98's, so a default that paired
    halves by NAME rather than by role finds no file.
    """
    write(os.path.join(tmp, 'run98-pair.txt'), NOTE_STUB + 'COMPARE: run97\n')
    write(os.path.join(tmp, 'run97-pair.txt'),
          'a stand-in pair note.\nHALVES: basis=nospec other=ghead\n')
    os.mkdir(os.path.join(tmp, 'runs'))
    os.rename(rundoc_with_a_results_table(tmp),
              os.path.join(tmp, 'runs', 'run97.md'))
    for name in ('run98-a1g', 'run97-nospec', 'run97-ghead'):
        synth_json(tmp, 'main', name='%s-main.json' % name)
    return {'j': synth_json(tmp, 'main', name='run98-lookrts-main.json'),
            'run': os.path.join(tmp, 'run98')}


def plant_half_mover(tmp):
    """`pair_with_a_compare_run` with one arm slowed on ONE half: Run 98's
    basis runs `lib-stage1` three times slower on the first main-set
    shape, which moves its geomean past the 3% bar on that half alone.
    `lib-stage1` carries no A/A copy, so the half's floor stays tight."""
    got = pair_with_a_compare_run(tmp)
    synth_json(tmp, 'main', name='run98-lookrts-main.json',
               skew=[(main_shapes()[0], 'lib-stage1', 3)])
    return got


def plant_gate_with_registration(tmp):
    """Run 96's gate on four synthetic legs and a README carrying its OPEN
    registration, whose one span predicts `list`'s cross figure at 2.0
    within 1% -- where two synthetic halves read about 1."""
    write(os.path.join(tmp, 'run96-pair.txt'),
          'a stand-in pair note.\nHALVES: basis=nb other=ob\n')
    for h in ('nb', 'ob'):
        for leg in 'ab':
            synth_json(tmp, 'main', name='run96-gate-%s-%s.json' % (h, leg))
    readme = write(os.path.join(tmp, 'R.md'),
                   '# R\n\n- `OPEN` **What Run 96 is built to answer,'
                   ' registered before it runs.** (1) *The regime holds.*'
                   ' `predict: cross list 2.0 within 1% on main basis`.\n')
    return {'run': os.path.join(tmp, 'run96'), 'readme': readme}


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


def rundoc_with_a_defaced_summary(tmp):
    """The run file with every cross-class summary CELL made wrong.

    The class names and the row ORDER are left alone, which is what the
    installer keys on and preserves: a table inherited from run to run is
    no place for a reordering, so the fixture proves the cells are
    refilled in place rather than the table rebuilt in some order of the
    script's own. `9.99%` is the marker -- no floor reads that -- so the
    case can assert it is gone rather than only that a count was printed.
    """
    text = rundoc_text()
    head = '| class | shapes | mut-odo-vecdims |'
    i = text.index(head)
    end = text.index('\n\n', i)
    rows = text[i:end].split('\n')
    out = []
    for line in rows:
        m = re.match(r'\| `(\w+)` \|', line)
        out.append(f'| `{m.group(1)}` | 0 | 9.99 | 9.99 |'
                   f' **`zznoarm`** 9.99 | `zznoarm` 9.99 | 9.99% |'
                   if m else line)
    return {'doc': write_rundoc(tmp, text[:i] + '\n'.join(out) + text[end:])}


def rundoc_without_class_table(tmp, cls='rev'):
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


def stub_half(tmp, name, body=None):
    """A stand-in half written into `tmp` and made executable, named by
    its path.

    The shell drivers `cd` to their own directory, so a shadow's `extra`
    reaches them; a Python reader here takes the paths it is handed, so
    its cases plant the stand-ins and name them. Two ways of shipping one
    fixture, and which a case wants is decided by the program.
    """
    path = os.path.join(tmp, name)
    write(path, FAKE_HALF if body is None else body)
    os.chmod(path, 0o755)
    return path


# A site of a run's binary, kept as objdump's own listing of it: the binary
# dies at the deletion offer, and a listing is the one form of a site that
# can be tracked. This one is `run25-g912` from 0x4275c0 to 0x427640, read
# 2026-09-04: the tail of a continuation, the info table in front of
# `$wrun` -- `fbConcatRuns`'s `run` -- and the entry code after it. The
# table's SRT word, `78 d8 3d 01` at 0x42761c, opens with `js -40`, and
# the bytes from 0x4275f6 sum to 40, so the survey read a straddling
# self-loop there that no `-g3` twin held and that control leaves at its
# second instruction. The window starts mid-instruction, as any window
# into tables-next-to-code does, and objdump has re-synchronised by the
# `mov 0x8(%rbp),%r14` that precedes the phantom's head.
PHANTOM_LISTING = """\

run25-g912:     file format elf64-x86-64


Disassembly of section .text:

00000000004275c0 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x1bc40>:
  4275c0:\t10 48 8b             \tadc    %cl,-0x75(%rax)
  4275c3:\t5b                   \tpop    %rbx
  4275c4:\t18 48 89             \tsbb    %cl,-0x77(%rax)
  4275c7:\t45 e8 48 83 c5 e0    \trex.RB call ffffffffe107f915 <_end+0xffffffffdf705cad>
  4275cd:\tf6 c3 07             \ttest   $0x7,%bl
  4275d0:\t75 16                \tjne    4275e8 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x1bc68>
  4275d2:\t48 8b 03             \tmov    (%rbx),%rax
  4275d5:\tff e0                \tjmp    *%rax
  4275d7:\t90                   \tnop
  4275d8:\t01 00                \tadd    %eax,(%rax)
  4275da:\t00 00                \tadd    %al,(%rax)
  4275dc:\t00 00                \tadd    %al,(%rax)
  4275de:\t00 00                \tadd    %al,(%rax)
  4275e0:\t1e                   \t(bad)
  4275e1:\t00 00                \tadd    %al,(%rax)
  4275e3:\t00 58 4e             \tadd    %bl,0x4e(%rax)
  4275e6:\t3e 01 48 8d          \tds add %ecx,-0x73(%rax)
  4275ea:\t3d 51 4e 3e 01       \tcmp    $0x13e4e51,%eax
  4275ef:\t48 89 de             \tmov    %rbx,%rsi
  4275f2:\t4c 8b 75 08          \tmov    0x8(%rbp),%r14
  4275f6:\t48 83 c5 10          \tadd    $0x10,%rbp
  4275fa:\te9 61 ff ff ff       \tjmp    427560 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x1bbe0>
  4275ff:\t41 ff 65 f0          \tjmp    *-0x10(%r13)
  427603:\t0f 1f 44 00 00       \tnopl   0x0(%rax,%rax,1)
  427608:\t04 00                \tadd    $0x0,%al
  42760a:\t00 00                \tadd    %al,(%rax)
  42760c:\t01 00                \tadd    %eax,(%rax)
  42760e:\t00 00                \tadd    %al,(%rax)
  427610:\t02 00                \tadd    (%rax),%al
  427612:\t00 00                \tadd    %al,(%rax)
  427614:\t02 00                \tadd    (%rax),%al
  427616:\t00 00                \tadd    %al,(%rax)
  427618:\t08 00                \tor     %al,(%rax)
  42761a:\t00 00                \tadd    %al,(%rax)
  42761c:\t78 d8                \tjs     4275f6 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x1bc76>
  42761e:\t3d 01 48 8d 45       \tcmp    $0x458d4801,%eax
  427623:\td0 4c 39 f8          \trorb   $1,-0x8(%rcx,%rdi,1)
  427627:\t0f 82 d2 00 00 00    \tjb     4276ff <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x1bd7f>
  42762d:\t48 c7 45 d8 90 76 42 \tmovq   $0x427690,-0x28(%rbp)
  427634:\t00 
  427635:\t48 8b 43 07          \tmov    0x7(%rbx),%rax
  427639:\t48 8b 4b 17          \tmov    0x17(%rbx),%rcx
  42763d:\t48                   \trex.W
  42763e:\t8b                   \t.byte 0x8b
  42763f:\t53                   \tpush   %rbx
"""


def phantom_listing(tmp):
    """The saved site above, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run25-g912-0x4275c0.dis')
    write(path, PHANTOM_LISTING)
    return {'dis': path}


# A second site, `run26-g912` from 0x42c640 to 0x42c6c0, read 2026-09-06:
# the tail of a continuation, the return-frame table in front of a
# continuation of `$wfbCanonVecdims`, and that continuation, which
# tail-jumps to a list equality. The table's SRT word, `00 73 3e 01` at
# 0x42c66c, throws the sweep out of step for the whole continuation, so
# the jump's opcode at 0x42c68a is swallowed into a `(bad)` and the low
# two bytes of its displacement, `71 d3`, read as `jno -45` back to the
# table's first byte -- a body straight-line flow reaches, the one
# transfer in it being the swallowed jump, which is why the flow test
# that refuses the site above passes this one and the `(bad)` inside it
# is the tell. The window opens on the `lea` of a return sequence, so
# objdump is in step from its first byte and out of it from the table.
PHANTOM2_LISTING = """\

run26-g912:     file format elf64-x86-64


Disassembly of section .text:

000000000042c640 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x20d00>:
  42c640:\t49 8d 5c 24 e9       \tlea    -0x17(%r12),%rbx
  42c645:\t48 83 c5 20          \tadd    $0x20,%rbp
  42c649:\tff 65 00             \tjmp    *0x0(%rbp)
  42c64c:\t49 c7 85 88 03 00 00 \tmovq   $0x20,0x388(%r13)
  42c653:\t20 00 00 00 
  42c657:\te9 54 54 35 01       \tjmp    1781ab0 <stg_gc_unbx_r1>
  42c65c:\t0f 1f 40 00          \tnopl   0x0(%rax)
  42c660:\t09 3e                \tor     %edi,(%rsi)
  42c662:\t00 00                \tadd    %al,(%rax)
  42c664:\t00 00                \tadd    %al,(%rax)
  42c666:\t00 00                \tadd    %al,(%rax)
  42c668:\t1e                   \t(bad)
  42c669:\t00 00                \tadd    %al,(%rax)
  42c66b:\t00 00                \tadd    %al,(%rax)
  42c66d:\t73 3e                \tjae    42c6ad <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x20d6d>
  42c66f:\t01 48 c7             \tadd    %ecx,-0x39(%rax)
  42c672:\t45 f8                \trex.RB clc
  42c674:\t80 b9 42 00 48 8d 35 \tcmpb   $0x35,-0x72b7ffbe(%rcx)
  42c67b:\t43 19 3e             \trex.XB sbb %edi,(%r14)
  42c67e:\t01 49 89             \tadd    %ecx,-0x77(%rcx)
  42c681:\tde 48 89             \tfimuls -0x77(%rax)
  42c684:\t5d                   \tpop    %rbp
  42c685:\t00 48 83             \tadd    %cl,-0x7d(%rax)
  42c688:\tc5 f8 e9             \t(bad)
  42c68b:\t71 d3                \tjno    42c660 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x20d20>
  42c68d:\t32 01                \txor    (%rcx),%al
  42c68f:\t90                   \tnop
  42c690:\t0f 00 00             \tsldt   (%rax)
  42c693:\t00 02                \tadd    %al,(%rdx)
\t...
  42c69d:\t00 00                \tadd    %al,(%rax)
  42c69f:\t00 0e                \tadd    %cl,(%rsi)
  42c6a1:\t00 00                \tadd    %al,(%rax)
  42c6a3:\t00 48 73             \tadd    %cl,0x73(%rax)
  42c6a6:\t3e 01 48 8d          \tds add %ecx,-0x73(%rax)
  42c6aa:\t45 d0 4c 39 f8       \trex.RB rorb $1,-0x8(%r9,%rdi,1)
  42c6af:\t0f 82 b7 00 00 00    \tjb     42c76c <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x20e2c>
  42c6b5:\t48 c7 45 f0 e8 c6 42 \tmovq   $0x42c6e8,-0x10(%rbp)
  42c6bc:\t00 
  42c6bd:\t48 89 f3             \tmov    %rsi,%rbx
"""


def phantom2_listing(tmp):
    """The second saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run26-g912-0x42c640.dis')
    write(path, PHANTOM2_LISTING)
    return {'dis': path}


def listing_with_eleven_straddlers(tmp):
    """A listing whose straddler and exit-span lists both overflow.

    ELEVEN sites, because both listings stop at ten and a fixture of ten
    says nothing about a listing that truncates. Synthetic where the two
    above are captured: each captured site carries one loop, and a binary
    with eleven of them dies at the deletion offer. Each site is the
    smallest shape `scan` accepts -- a conditional back edge, so the head
    has an exit span at all, and a fall-through jump landing past the line
    so that span straddles too.
    """
    out = ['', 'zzsurvey:     file format elf64-x86-64', '', '',
           'Disassembly of section .text:', '']
    for i in range(11):
        sym = 'micro_Main_zdwfbSite%d_info' % i
        base = 0x410000 + 0x100 * i
        a = base + 0x3e
        out.append('%016x <%s>:' % (base, sym))
        out.append('  %x:\t31 c0                \txor    %%eax,%%eax' % a)
        out.append('  %x:\t75 fc                \tjne    %x <%s+0x3e>'
                   % (a + 2, a, sym))
        out.append('  %x:\t48 83 c0 01          \tadd    $0x1,%%rax' % (a + 4))
        out.append('  %x:\teb 10                \tjmp    %x <%s+0x5a>'
                   % (a + 8, a + 0x1c, sym))
        out.append('')
    path = os.path.join(tmp, 'zzsurvey-eleven.dis')
    write(path, '\n'.join(out) + '\n')
    return {'dis': path}


# A third site, `run28-g912` from 0x41c9dc to 0x41ca10, read 2026-09-11:
# the tail of a block, a `jmp *-0x10(%r13)`, a two-byte pad, and then the
# info table, whose OWN words are the body. The layout word and the type
# word read as three `add %al,(%rax)` and an `adc`, and the low two bytes
# of the word after them, `78 f6`, close them as `js -10` -- ten bytes,
# five instructions, no transfer inside for the flow test to leave at and
# no `(bad)` for the filter, so both of the guards above admit it. It
# straddles at mod 60, which is how it reached a pair note as a refusal.
# The tell is the run of zero bytes: `00 00` is a legal instruction, so
# both guards above read this body as code, and no real loop of the twenty
# binaries read carries four zero bytes in a row. Nothing branches to the
# head but the `js` itself, and the last real instruction before it is the
# indirect jump, so the body is unreachable as well as data.
PHANTOM3_LISTING = """\

run28-g912:     file format elf64-x86-64


Disassembly of section .text:

000000000041c9dc <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x10e1c>:
  41c9dc:\tf0 98                \tlock cwtl
  41c9de:\t0c 7b                \tor     $0x7b,%al
  41c9e0:\t01 48 89             \tadd    %ecx,-0x77(%rax)
  41c9e3:\t5d                   \tpop    %rbp
  41c9e4:\tf8                   \tclc
  41c9e5:\t4c 8b 73 10          \tmov    0x10(%rbx),%r14
  41c9e9:\t48 83 c5 f0          \tadd    $0xfffffffffffffff0,%rbp
  41c9ed:\te9 9e fe ff ff       \tjmp    41c890 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x10cd0>
  41c9f2:\t41 ff 65 f0          \tjmp    *-0x10(%r13)
  41c9f6:\t66 90                \txchg   %ax,%ax
  41c9f8:\t02 00                \tadd    (%rax),%al
  41c9fa:\t00 00                \tadd    %al,(%rax)
  41c9fc:\t00 00                \tadd    %al,(%rax)
  41c9fe:\t00 00                \tadd    %al,(%rax)
  41ca00:\t12 00                \tadc    (%rax),%al
  41ca02:\t00 00                \tadd    %al,(%rax)
  41ca04:\t78 f6                \tjs     41c9fc <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x10e3c>
  41ca06:\t41 01 48 8d          \tadd    %ecx,-0x73(%r8)
  41ca0a:\t45                   \trex.RB
  41ca0b:\tf0 4c 39 f8          \tlock cmp %r15,%rax
  41ca0f:\t72 23                \tjb     41ca34 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x10e74>
"""


def phantom3_listing(tmp):
    """The third saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run28-g912-0x41c9dc.dis')
    write(path, PHANTOM3_LISTING)
    return {'dis': path}


# A fourth site, `run32-ghead` from 0x430b40 to 0x430c60, read 2026-09-16:
# `fillStage2`'s 51-byte stepping loop at 0x430b89, residue 9, its body in
# the line and its exit `cmp; jge` ending at byte 65 -- the placement that
# Run 32's HEAD half timed and that `LOOP_EXITSPAN=1` was written to
# remove -- followed at 0x430c00 by a rotated pair whose outer loop's back
# edge is a `jmp`, which has no fall-through and so no exit span. Planted
# for the survey's exit-span count: ONE exit span astride, and the pair's
# `jmp` read as no exit rather than as a span through the next block.
EXITSPAN_LISTING = """\

run32-ghead:     file format elf64-x86-64


Disassembly of section .text:

0000000000430b40 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22bb8>:
  430b40:\tf0 48 01 d0          \tlock add %rdx,%rax
  430b44:\t48 89 f3             \tmov    %rsi,%rbx
  430b47:\teb 12                \tjmp    430b5b <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22bd3>
  430b49:\tf2 0f 11 04 d9       \tmovsd  %xmm0,(%rcx,%rbx,8)
  430b4e:\t48 8d 7b 01          \tlea    0x1(%rbx),%rdi
  430b52:\tf2 0f 11 04 f9       \tmovsd  %xmm0,(%rcx,%rdi,8)
  430b57:\t48 83 c3 02          \tadd    $0x2,%rbx
  430b5b:\t48 8d 7b 01          \tlea    0x1(%rbx),%rdi
  430b5f:\t48 39 c7             \tcmp    %rax,%rdi
  430b62:\t7c e5                \tjl     430b49 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22bc1>
  430b64:\t48 39 c3             \tcmp    %rax,%rbx
  430b67:\t7d 05                \tjge    430b6e <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22be6>
  430b69:\tf2 0f 11 04 d9       \tmovsd  %xmm0,(%rcx,%rbx,8)
  430b6e:\t49 83 fa 01          \tcmp    $0x1,%r10
  430b72:\t7e 0f                \tjle    430b83 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22bfb>
  430b74:\t4c 0f af d2          \timul   %rdx,%r10
  430b78:\t48 89 f0             \tmov    %rsi,%rax
  430b7b:\t4c 01 d0             \tadd    %r10,%rax
  430b7e:\te9 cf 01 00 00       \tjmp    430d52 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22dca>
  430b83:\t48 89 c3             \tmov    %rax,%rbx
  430b86:\tff 65 00             \tjmp    *0x0(%rbp)
  430b89:\t4c 8b 5c 24 40       \tmov    0x40(%rsp),%r11
  430b8e:\tf2 41 0f 10 04 db    \tmovsd  (%r11,%rbx,8),%xmm0
  430b94:\tf2 0f 11 04 f1       \tmovsd  %xmm0,(%rcx,%rsi,8)
  430b99:\t4c 01 cb             \tadd    %r9,%rbx
  430b9c:\tf2 41 0f 10 04 db    \tmovsd  (%r11,%rbx,8),%xmm0
  430ba2:\t4c 8d 76 01          \tlea    0x1(%rsi),%r14
  430ba6:\tf2 42 0f 11 04 f1    \tmovsd  %xmm0,(%rcx,%r14,8)
  430bac:\t4c 01 cb             \tadd    %r9,%rbx
  430baf:\t48 83 c6 02          \tadd    $0x2,%rsi
  430bb3:\t4c 8d 5e 01          \tlea    0x1(%rsi),%r11
  430bb7:\t49 39 c3             \tcmp    %rax,%r11
  430bba:\t7c cd                \tjl     430b89 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22c01>
  430bbc:\t48 39 c6             \tcmp    %rax,%rsi
  430bbf:\t7d 10                \tjge    430bd1 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22c49>
  430bc1:\t4c 8b 5c 24 40       \tmov    0x40(%rsp),%r11
  430bc6:\tf2 41 0f 10 04 db    \tmovsd  (%r11,%rbx,8),%xmm0
  430bcc:\tf2 0f 11 04 f1       \tmovsd  %xmm0,(%rcx,%rsi,8)
  430bd1:\t4c 01 c7             \tadd    %r8,%rdi
  430bd4:\t49 ff ca             \tdec    %r10
  430bd7:\t48 89 c6             \tmov    %rax,%rsi
  430bda:\t4d 85 d2             \ttest   %r10,%r10
  430bdd:\t7e 0b                \tjle    430bea <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22c62>
  430bdf:\t48 89 f0             \tmov    %rsi,%rax
  430be2:\t48 01 d0             \tadd    %rdx,%rax
  430be5:\t48 89 fb             \tmov    %rdi,%rbx
  430be8:\teb c9                \tjmp    430bb3 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22c2b>
  430bea:\t48 89 f3             \tmov    %rsi,%rbx
  430bed:\tff 65 00             \tjmp    *0x0(%rbp)
  430bf0:\t66 66 2e 0f 1f 84 00 \tdata16 cs nopw 0x0(%rax,%rax,1)
  430bf7:\t00 00 00 00 
  430bfb:\t0f 1f 44 00 00       \tnopl   0x0(%rax,%rax,1)
  430c00:\tf2 0f 11 04 f1       \tmovsd  %xmm0,(%rcx,%rsi,8)
  430c05:\t4c 8d 4e 01          \tlea    0x1(%rsi),%r9
  430c09:\tf2 42 0f 11 04 c9    \tmovsd  %xmm0,(%rcx,%r9,8)
  430c0f:\t48 83 c6 02          \tadd    $0x2,%rsi
  430c13:\t4c 8d 4e 01          \tlea    0x1(%rsi),%r9
  430c17:\t49 39 d9             \tcmp    %rbx,%r9
  430c1a:\t7c e4                \tjl     430c00 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22c78>
  430c1c:\t48 39 de             \tcmp    %rbx,%rsi
  430c1f:\t7d 05                \tjge    430c26 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22c9e>
  430c21:\tf2 0f 11 04 f1       \tmovsd  %xmm0,(%rcx,%rsi,8)
  430c26:\t4c 01 c7             \tadd    %r8,%rdi
  430c29:\t49 ff ca             \tdec    %r10
  430c2c:\t48 89 de             \tmov    %rbx,%rsi
  430c2f:\t4d 85 d2             \ttest   %r10,%r10
  430c32:\t7e 12                \tjle    430c46 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22cbe>
  430c34:\t48 8b 44 24 40       \tmov    0x40(%rsp),%rax
  430c39:\tf2 0f 10 04 f8       \tmovsd  (%rax,%rdi,8),%xmm0
  430c3e:\t48 89 f3             \tmov    %rsi,%rbx
  430c41:\t48 01 d3             \tadd    %rdx,%rbx
  430c44:\teb cd                \tjmp    430c13 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x22c8b>
  430c46:\t48 89 f3             \tmov    %rsi,%rbx
  430c49:\tff 65 00             \tjmp    *0x0(%rbp)
  430c4c:\t48 89 c7             \tmov    %rax,%rdi
  430c4f:\t48 01 d7             \tadd    %rdx,%rdi
  430c52:\t48 c1 e7 03          \tshl    $0x3,%rdi
  430c56:\t49 89 c8             \tmov    %rcx,%r8
  430c59:\t49 01 f8             \tadd    %rdi,%r8
  430c5c:\t48 89 c7             \tmov    %rax,%rdi
  430c5f:\t48                   \trex.W
"""


def exitspan_listing(tmp):
    """The fourth saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run32-ghead-0x430b40.dis')
    write(path, EXITSPAN_LISTING)
    return {'dis': path}


# A fifth site, `run33-gheadexit` from 0x496880 to 0x4968e0, read
# 2026-09-16: a `jmp stg_gc_unpt_r1`, the `nopl` that pads to the next
# info table, and the table's first word, `78 fa`, decoding as `js -6`
# back to the pad. The pad is reached by no path, holds no `(bad)` and
# no zero run, and six bytes cannot straddle, so the three tells and the
# straddle count all passed it; what met it was the exit-span count,
# which read two astride on that half where the shim's own line read
# none. No emitted loop begins with a `nop`, which is the tell.
PHANTOM4_LISTING = """\

run33-gheadexit:     file format elf64-x86-64


Disassembly of section .text:

0000000000496880 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x888f8>:
  496880:\t48 8b 45 10          \tmov    0x10(%rbp),%rax
  496884:\t49 89 04 24          \tmov    %rax,(%r12)
  496888:\t49 8d 5c 24 e9       \tlea    -0x17(%r12),%rbx
  49688d:\t48 83 c5 20          \tadd    $0x20,%rbp
  496891:\tff 65 00             \tjmp    *0x0(%rbp)
  496894:\t49 c7 85 88 03 00 00 \tmovq   $0x20,0x388(%r13)
  49689b:\t20 00 00 00 
  49689f:\te9 dc 49 34 01       \tjmp    17db280 <stg_gc_unpt_r1>
  4968a4:\t0f 1f 40 00          \tnopl   0x0(%rax)
  4968a8:\t78 fa                \tjs     4968a4 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x8891c>
  4968aa:\tff                   \t(bad)
  4968ab:\tff                   \t(bad)
  4968ac:\tff                   \t(bad)
  4968ad:\tff                   \t(bad)
  4968ae:\tff                   \t(bad)
  4968af:\tff 05 03 00 00 00    \tincl   0x3(%rip)        # 4968b8 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x88930>
  4968b5:\t00 00                \tadd    %al,(%rax)
  4968b7:\t00 00                \tadd    %al,(%rax)
  4968b9:\t00 00                \tadd    %al,(%rax)
  4968bb:\t00 05 00 00 00 02    \tadd    %al,0x2000000(%rip)        # 24968c1 <_end+0xac4b49>
  4968c1:\t00 00                \tadd    %al,(%rax)
  4968c3:\t00 00                \tadd    %al,(%rax)
  4968c5:\t00 00                \tadd    %al,(%rax)
  4968c7:\t00 0e                \tadd    %cl,(%rsi)
  4968c9:\t00 00                \tadd    %al,(%rax)
  4968cb:\t00 00                \tadd    %al,(%rax)
  4968cd:\t00 00                \tadd    %al,(%rax)
  4968cf:\t00 48 8d             \tadd    %cl,-0x73(%rax)
  4968d2:\t45 80 4c 39 f8 72    \trex.RB orb $0x72,-0x8(%r9,%rdi,1)
  4968d8:\t7d 49                \tjge    496923 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x8899b>
  4968da:\t83 c4 10             \tadd    $0x10,%esp
  4968dd:\t4d                   \trex.WRB
  4968de:\t3b                   \t.byte 0x3b
  4968df:\ta5                   \tmovsl  %ds:(%rsi),%es:(%rdi)
"""


def phantom4_listing(tmp):
    """The fifth saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run33-gheadexit-0x496880.dis')
    write(path, PHANTOM4_LISTING)
    return {'dis': path}


# A sixth site, `run35-exit` from 0x41f8f0 to 0x41f962, read 2026-09-18:
# an info table's last zero byte and the `movq $0x41f978,-0x8(%rbp)` after
# it, the continuation push, read one byte out of step, the immediate's
# low bytes `78 f9` decoding as `js -7` back to that zero byte. Seven
# bytes at offset 63, so it straddles and its exit span is astride, and
# the four tells pass it: the flow is straight, no `(bad)`, no zero run,
# no nop. The tell is the `45` the sweep landed on, the movq's ModRM
# byte, which objdump prints as the prefix `rex.RB` since the `clc` it
# read next takes none of it: a stray REX names a sweep that entered an
# instruction mid-way. Over the twenty-four run binaries on disk the tell
# marks three bodies and no real loop, and moves no `--library` figure;
# the totals it moves are run35-exit's, nine straddling and one astride
# to eight and none, run35-gheadexit's nine straddling to eight, and
# run30-libcase's 63 astride to 62. It refuses the second site too,
# whose body carries a `rex.RB clc` of its own, which is why the mutant
# for that site drops three tells.
PHANTOM5_LISTING = """\

run35-exit:     file format elf64-x86-64


Disassembly of section .text:

000000000041f8f0 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x13d00>:
\t...
  41f8f8:\t0e                   \t(bad)
  41f8f9:\t00 00                \tadd    %al,(%rax)
  41f8fb:\t00 00                \tadd    %al,(%rax)
  41f8fd:\t00 00                \tadd    %al,(%rax)
  41f8ff:\t00 48 8d             \tadd    %cl,-0x73(%rax)
  41f902:\t45 e0 4c             \trex.RB loopne 41f951 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x13d61>
  41f905:\t39 f8                \tcmp    %edi,%eax
  41f907:\t0f 82 ec 00 00 00    \tjb     41f9f9 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x13e09>
  41f90d:\t48 c7 45 f0 40 f9 41 \tmovq   $0x41f940,-0x10(%rbp)
  41f914:\t00 
  41f915:\t4c 89 f3             \tmov    %r14,%rbx
  41f918:\t48 89 75 f8          \tmov    %rsi,-0x8(%rbp)
  41f91c:\t48 83 c5 f0          \tadd    $0xfffffffffffffff0,%rbp
  41f920:\tf6 c3 07             \ttest   $0x7,%bl
  41f923:\t75 1b                \tjne    41f940 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x13d50>
  41f925:\t48 8b 03             \tmov    (%rbx),%rax
  41f928:\tff e0                \tjmp    *%rax
  41f92a:\t66 0f 1f 44 00 00    \tnopw   0x0(%rax,%rax,1)
  41f930:\t01 00                \tadd    %eax,(%rax)
  41f932:\t00 00                \tadd    %al,(%rax)
  41f934:\t00 00                \tadd    %al,(%rax)
  41f936:\t00 00                \tadd    %al,(%rax)
  41f938:\t1e                   \t(bad)
  41f939:\t00 00                \tadd    %al,(%rax)
  41f93b:\t00 00                \tadd    %al,(%rax)
  41f93d:\t00 00                \tadd    %al,(%rax)
  41f93f:\t00 48 c7             \tadd    %cl,-0x39(%rax)
  41f942:\t45 f8                \trex.RB clc
  41f944:\t78 f9                \tjs     41f93f <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x13d4f>
  41f946:\t41 00 48 8b          \tadd    %cl,-0x75(%r8)
  41f94a:\t43 0f 48 8b 5b 07 48 \trex.XB cmovs -0x76b7f8a5(%r11),%ecx
  41f951:\t89 
  41f952:\t45 00 48 83          \tadd    %r9b,-0x7d(%r8)
  41f956:\tc5 f8 f6             \t(bad)
  41f959:\tc3                   \tret
  41f95a:\t07                   \t(bad)
  41f95b:\t75 1b                \tjne    41f978 <microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info+0x13d88>
  41f95d:\t48 8b 03             \tmov    (%rbx),%rax
  41f960:\tff e0                \tjmp    *%rax
"""


def phantom5_listing(tmp):
    """The sixth saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run35-exit-0x41f8f0.dis')
    write(path, PHANTOM5_LISTING)
    return {'dis': path}


# A seventh site, `run36-gheadnospec` from 0x4a4819 to 0x4a4841, read
# 2026-09-18 against the shim's verified line, which read no exit span
# astride where the survey read one: a `jmp stg_gc_unbx_r1`, a two-byte
# pad, and the info table before the function's prologue at 0x4a4838,
# whose words decode as `add %al,(%rax)` and `adc`. The body is two of
# its zero bytes and the low bytes of the word after them, `78 fc`, a
# `js -4` back to the head: the third site's shape, with two zero bytes
# where `zero_run` asks four. Every tell passed it, and four bytes at
# offset 50 cannot straddle, so only the exit-span count met it. The
# tell is an instruction of two zero bytes, which no compiler emits.
PHANTOM6_LISTING = """\

run36-gheadnospec:     file format elf64-x86-64


Disassembly of section .text:

00000000004a4819 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x96811>:
  4a4819:\t48 c7 45 00 e8 47 4a \tmovq   $0x4a47e8,0x0(%rbp)
  4a4820:\t00 
  4a4821:\te9 42 d4 2a 01       \tjmp    1751c68 <stg_gc_unbx_r1>
  4a4826:\t66 90                \txchg   %ax,%ax
  4a4828:\t01 00                \tadd    %eax,(%rax)
  4a482a:\t00 00                \tadd    %al,(%rax)
  4a482c:\t00 00                \tadd    %al,(%rax)
  4a482e:\t00 00                \tadd    %al,(%rax)
  4a4830:\t10 00                \tadc    %al,(%rax)
  4a4832:\t00 00                \tadd    %al,(%rax)
  4a4834:\t78 fc                \tjs     4a4832 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x9682a>
  4a4836:\t34 01                \txor    $0x1,%al
  4a4838:\t48 8d 45 f0          \tlea    -0x10(%rbp),%rax
  4a483c:\t4c 39 f8             \tcmp    %r15,%rax
  4a483f:\t72 3d                \tjb     4a487e <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x96876>
  4a4841:\t48 c7 45 f0 d0 74 75 \tmovq   $0x17574d0,-0x10(%rbp)
"""


def phantom6_listing(tmp):
    """The seventh saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run36-gheadnospec-0x4a4819.dis')
    write(path, PHANTOM6_LISTING)
    return {'dis': path}


# An eighth site, `run36-gheadtwopass` from 0x43f237 to 0x43f28c, read
# the same day against the same line: a `jmp *0x0(%rbp)`, the two-byte
# pad to the next info table, `66 90`, and that table's first word,
# `70 fc`, decoding as `jo -4` back to the pad -- the fifth site's shape
# with a pad objdump spells `xchg %ax,%ax` and not `nop`, so the pad
# tell, reading for `nop`, passed it. The tell reads that spelling too
# since 2026-09-18.
PHANTOM7_LISTING = """\

run36-gheadtwopass:     file format elf64-x86-64


Disassembly of section .text:

000000000043f237 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x30f57>:
  43f237:\t48 8b 7d 30          \tmov    0x30(%rbp),%rdi
  43f23b:\t48 89 de             \tmov    %rbx,%rsi
  43f23e:\t4c 8b 75 08          \tmov    0x8(%rbp),%r14
  43f242:\t48 8b 5d 28          \tmov    0x28(%rbp),%rbx
  43f246:\t48 83 c5 10          \tadd    $0x10,%rbp
  43f24a:\te9 01 fd ff ff       \tjmp    43ef50 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x30c70>
  43f24f:\t48 83 c5 40          \tadd    $0x40,%rbp
  43f253:\tff 65 00             \tjmp    *0x0(%rbp)
  43f256:\t66 90                \txchg   %ax,%ax
  43f258:\t70 fc                \tjo     43f256 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x30f76>
  43f25a:\tff                   \t(bad)
  43f25b:\tff                   \t(bad)
  43f25c:\tff                   \t(bad)
  43f25d:\tff                   \t(bad)
  43f25e:\tff                   \t(bad)
  43f25f:\tff 05 03 00 00 00    \tincl   0x3(%rip)        # 43f268 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x30f88>
  43f265:\t00 00                \tadd    %al,(%rax)
  43f267:\t00 00                \tadd    %al,(%rax)
  43f269:\t00 00                \tadd    %al,(%rax)
  43f26b:\t00 05 00 00 00 02    \tadd    %al,0x2000000(%rip)        # 243f271 <_end+0xaf7cf9>
  43f271:\t00 00                \tadd    %al,(%rax)
  43f273:\t00 00                \tadd    %al,(%rax)
  43f275:\t00 00                \tadd    %al,(%rax)
  43f277:\t00 0e                \tadd    %cl,(%rsi)
  43f279:\t00 00                \tadd    %al,(%rax)
  43f27b:\t00 00                \tadd    %al,(%rax)
  43f27d:\t00 00                \tadd    %al,(%rax)
  43f27f:\t00 48 8d             \tadd    %cl,-0x73(%rax)
  43f282:\t45 b0 4c             \trex.RB mov $0x4c,%r8b
  43f285:\t39 f8                \tcmp    %edi,%eax
  43f287:\t72 0c                \tjb     43f295 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x30fb5>
  43f289:\t48 89 f0             \tmov    %rsi,%rax
  43f28c:\t48 8d 1d ad 16 3a 01 \tlea    0x13a16ad(%rip),%rbx        # 17e0940 <microzm0zi1zminplacezmmicro_Main_main67_closure+0x23e0>
"""


def phantom7_listing(tmp):
    """The eighth saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run36-gheadtwopass-0x43f237.dis')
    write(path, PHANTOM7_LISTING)
    return {'dis': path}


# A ninth site, `run33-gheadexit` from 0x4a52b6 to 0x4a52ff, saved
# 2026-09-18 for the flow test's mutant and for no case: a `jmp
# stg_gc_noregs`, the `nopl` pad after it and the table word `78 f4`, a
# `js -12` back to the jmp itself. The flow test alone refuses it, the
# head being the jmp; the first site, which that mutant judged over until
# this day, carries `add %al,(%rax)` words the zero tell's instruction
# form now refuses too, so dropping the flow test there counted nothing.
# The same shape sits in run34-gheadexit and run35-gheadexit.
PHANTOM8_LISTING = """\

run33-gheadexit:     file format elf64-x86-64


Disassembly of section .text:

00000000004a52b6 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x9732e>:
  4a52b6:\t48 c7 45 e8 40 52 4a \tmovq   $0x4a5240,-0x18(%rbp)
  4a52bd:\t00 
  4a52be:\t4c 89 75 f0          \tmov    %r14,-0x10(%rbp)
  4a52c2:\t48 89 5d f8          \tmov    %rbx,-0x8(%rbp)
  4a52c6:\t48 89 75 00          \tmov    %rsi,0x0(%rbp)
  4a52ca:\t48 83 c5 e8          \tadd    $0xffffffffffffffe8,%rbp
  4a52ce:\te9 8d 5b 33 01       \tjmp    17dae60 <stg_gc_noregs>
  4a52d3:\t0f 1f 44 00 00       \tnopl   0x0(%rax,%rax,1)
  4a52d8:\t78 f4                \tjs     4a52ce <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x97346>
  4a52da:\tff                   \t(bad)
  4a52db:\tff                   \t(bad)
  4a52dc:\tff                   \t(bad)
  4a52dd:\tff                   \t(bad)
  4a52de:\tff                   \t(bad)
  4a52df:\tff 06                \tincl   (%rsi)
  4a52e1:\t07                   \t(bad)
  4a52ea:\t00 00                \tadd    %al,(%rax)
  4a52ec:\t06                   \t(bad)
  4a52ed:\t00 00                \tadd    %al,(%rax)
  4a52ef:\t00 02                \tadd    %al,(%rdx)
  4a52f1:\t00 00                \tadd    %al,(%rax)
  4a52f3:\t00 00                \tadd    %al,(%rax)
  4a52f5:\t00 00                \tadd    %al,(%rax)
  4a52f7:\t00 0e                \tadd    %cl,(%rsi)
  4a52f9:\t00 00                \tadd    %al,(%rax)
  4a52fb:\t00 00                \tadd    %al,(%rax)
  4a52fd:\t00 00                \tadd    %al,(%rax)
  4a52ff:\t00 48 8d             \tadd    %cl,-0x73(%rax)
"""


def phantom8_listing(tmp):
    """The ninth saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run33-gheadexit-0x4a52b6.dis')
    write(path, PHANTOM8_LISTING)
    return {'dis': path}


# A tenth site, `run36-gheadnospec` from 0x42ea22 to 0x42ea7c, saved
# 2026-09-18, and a real loop rather than a phantom: 44 bytes at 0x42ea40
# walking a list, `mov 0xe(%rbx),%rbx` and `jne` back, with the
# return-frame push `movq $0x42ea40,0x0(%rbp)` inside it, eight bytes
# that objdump prints as seven and a second line of one. `parse` read the
# first line alone until that day, so the body's byte sum fell one short
# of its span and `scan` dropped it as a jump into an instruction. The
# window carries the pad and table words before the head, and a second
# such push after the loop.
LONGINSN_LISTING = """\

run36-gheadnospec:     file format elf64-x86-64


Disassembly of section .text:

000000000042ea22 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x20a1a>:
  42ea22:\t48 8d 05 2f 6c 3a 01 \tlea    0x13a6c2f(%rip),%rax        # 17d5658 <microzm0zi1zminplacezmmicro_Main_main61_closure+0x710>
  42ea29:\t48 8b 5d 18          \tmov    0x18(%rbp),%rbx
  42ea2d:\teb 15                \tjmp    42ea44 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x20a3c>
  42ea2f:\t90                   \tnop
  42ea30:\t88 1c 00             \tmov    %bl,(%rax,%rax,1)
  42ea33:\t00 00                \tadd    %al,(%rax)
  42ea35:\t00 00                \tadd    %al,(%rax)
  42ea37:\t00 1e                \tadd    %bl,(%rsi)
  42ea39:\t00 00                \tadd    %al,(%rax)
  42ea3b:\t00 70 f8             \tadd    %dh,-0x8(%rax)
  42ea3e:\t3a 01                \tcmp    (%rcx),%al
  42ea40:\t48 8b 45 08          \tmov    0x8(%rbp),%rax
  42ea44:\t48 89 d9             \tmov    %rbx,%rcx
  42ea47:\t83 e1 07             \tand    $0x7,%ecx
  42ea4a:\t48 83 f9 01          \tcmp    $0x1,%rcx
  42ea4e:\t74 21                \tje     42ea71 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x20a69>
  42ea50:\t48 c7 45 00 40 ea 42 \tmovq   $0x42ea40,0x0(%rbp)
  42ea57:\t00 
  42ea58:\t48 89 d8             \tmov    %rbx,%rax
  42ea5b:\t48 8b 5b 0e          \tmov    0xe(%rbx),%rbx
  42ea5f:\t48 8b 40 06          \tmov    0x6(%rax),%rax
  42ea63:\t48 89 45 08          \tmov    %rax,0x8(%rbp)
  42ea67:\tf6 c3 07             \ttest   $0x7,%bl
  42ea6a:\t75 d4                \tjne    42ea40 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x20a38>
  42ea6c:\t48 8b 03             \tmov    (%rbx),%rax
  42ea6f:\tff e0                \tjmp    *%rax
  42ea71:\t48 c7 45 08 a0 ea 42 \tmovq   $0x42eaa0,0x8(%rbp)
  42ea78:\t00 
  42ea79:\t48 89 c3             \tmov    %rax,%rbx
  42ea7c:\t48 83 c5 08          \tadd    $0x8,%rbp
"""


def longinsn_listing(tmp):
    """The tenth saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run36-gheadnospec-0x42ea22.dis')
    write(path, LONGINSN_LISTING)
    return {'dis': path}


# An eleventh site, `run36-gheadtwopass` from 0x482cf4 to 0x482d8b, read
# 2026-09-19: the ninth straddler the parser fix of 2cbaeb6 made the
# survey read where the shim's verified line has eight. At 0x482d4d a
# block loads an error closure, pops the stack and tail-calls
# `stg_ap_0_fast`; the check after it, entered by a forward branch,
# turns an element count into bytes and branches back to that block on
# a negative result, `jl -54`. No path from the head reaches the back
# edge, so it is a branch into an exit block and no loop, the shape of
# every heap-check failure block; the flow test admitted it for the
# forward branch targeting the check, the `je` at 0x482cf4 that opens
# this window, and follows the body's own edges since 2026-09-19.
# Straddles: 54 bytes at offset 13.
EXITBLOCK_LISTING = """\

run36-gheadtwopass:     file format elf64-x86-64


Disassembly of section .text:

0000000000482cf4 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74a14>:
  482cf4:\t74 67                \tje     482d5d <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74a7d>
  482cf6:\t48 8b 5b 07          \tmov    0x7(%rbx),%rbx
  482cfa:\t48 85 c0             \ttest   %rax,%rax
  482cfd:\t0f 8e 9a 00 00 00    \tjle    482d9d <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74abd>
  482d03:\t48 85 c0             \ttest   %rax,%rax
  482d06:\t0f 8c 98 00 00 00    \tjl     482da4 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74ac4>
  482d0c:\t48 ba ff ff ff ff ff \tmovabs $0xfffffffffffffff,%rdx
  482d13:\tff ff 0f 
  482d16:\t48 39 d0             \tcmp    %rdx,%rax
  482d19:\t0f 8f a1 00 00 00    \tjg     482dc0 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74ae0>
  482d1f:\t48 c1 e0 03          \tshl    $0x3,%rax
  482d23:\t48 85 c0             \ttest   %rax,%rax
  482d26:\t7c 25                \tjl     482d4d <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74a6d>
  482d28:\t48 c7 45 f8 40 30 48 \tmovq   $0x483040,-0x8(%rbp)
  482d2f:\t00 
  482d30:\t41 be 08 00 00 00    \tmov    $0x8,%r14d
  482d36:\t48 89 da             \tmov    %rbx,%rdx
  482d39:\t48 89 c3             \tmov    %rax,%rbx
  482d3c:\t48 89 4d 00          \tmov    %rcx,0x0(%rbp)
  482d40:\t48 89 55 20          \tmov    %rdx,0x20(%rbp)
  482d44:\t48 83 c5 f8          \tadd    $0xfffffffffffffff8,%rbp
  482d48:\te9 c3 13 2d 01       \tjmp    1754110 <stg_newAlignedPinnedByteArrayzh>
  482d4d:\t48 8d 1d 5c 4c 4a 01 \tlea    0x14a4c5c(%rip),%rbx        # 19279b0 <ghczminternal_GHCziInternalziForeignPtr_mallocPlainForeignPtrAlignedBytes2_closure>
  482d54:\t48 83 c5 38          \tadd    $0x38,%rbp
  482d58:\te9 93 f3 2c 01       \tjmp    17520f0 <stg_ap_0_fast>
  482d5d:\t48 85 c0             \ttest   %rax,%rax
  482d60:\t7e 4e                \tjle    482db0 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74ad0>
  482d62:\t48 85 c0             \ttest   %rax,%rax
  482d65:\t7c 4d                \tjl     482db4 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74ad4>
  482d67:\t48 bb ff ff ff ff ff \tmovabs $0xfffffffffffffff,%rbx
  482d6e:\tff ff 0f 
  482d71:\t48 39 d8             \tcmp    %rbx,%rax
  482d74:\t0f 8f 86 00 00 00    \tjg     482e00 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74b20>
  482d7a:\t48 c1 e0 03          \tshl    $0x3,%rax
  482d7e:\t48 85 c0             \ttest   %rax,%rax
  482d81:\t7c ca                \tjl     482d4d <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x74a6d>
  482d83:\t48 c7 45 08 40 31 48 \tmovq   $0x483140,0x8(%rbp)
  482d8a:\t00 
  482d8b:\t41 be 08 00 00 00    \tmov    $0x8,%r14d
"""


def exitblock_listing(tmp):
    """The eleventh saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run36-gheadtwopass-0x482cf4.dis')
    write(path, EXITBLOCK_LISTING)
    return {'dis': path}


# A twelfth site, `run36-gheadnospec` from 0x432411 to 0x432434, and a
# control: a real 24-byte copy loop at 0x43241c, entered by a `jmp` into
# its compare and closed by a `jmp` back to its head after the `jge`
# that exits it. The blanket flow test of 2026-09-04, refusing any
# unconditional transfer inside a body, lost this shape; the one that
# follows the body's own edges keeps it, the closing `jmp` being reached
# by fall-through from the `jge`.
ROTATED_LISTING = """\

run36-gheadnospec:     file format elf64-x86-64


Disassembly of section .text:

0000000000432411 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x24409>:
  432411:\t48 89 f0             \tmov    %rsi,%rax
  432414:\t48 89 f3             \tmov    %rsi,%rbx
  432417:\t48 01 d3             \tadd    %rdx,%rbx
  43241a:\teb 11                \tjmp    43242d <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x24425>
  43241c:\tf2 41 0f 10 04 f8    \tmovsd  (%r8,%rdi,8),%xmm0
  432422:\tf2 0f 11 04 f1       \tmovsd  %xmm0,(%rcx,%rsi,8)
  432427:\t4c 01 cf             \tadd    %r9,%rdi
  43242a:\t48 ff c6             \tinc    %rsi
  43242d:\t48 39 de             \tcmp    %rbx,%rsi
  432430:\t7d 27                \tjge    432459 <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x24451>
  432432:\teb e8                \tjmp    43241c <microzm0zi1zminplacezmmicro_Main_zdfNFDataTzuzdcrnf_info+0x24414>
  432434:\t41 ff 65 f8          \tjmp    *-0x8(%r13)
"""


def rotated_listing(tmp):
    """The twelfth saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run36-gheadnospec-0x432411.dis')
    write(path, ROTATED_LISTING)
    return {'dis': path}


# A thirteenth site, `run41-gheadnospec` from 0x497d90 to 0x497e1e, read
# 2026-09-26: an info table ending at 0x497dd7 and the continuation after
# it, `movq $0x497df8,0x0(%rbp)`, `mov %rbx,%r14` and a `jmp` rel32 back,
# read one byte out of step, so that the mov's last byte and the jmp's
# opcode, `de e9`, decode as `fsubrp` and the displacement's low bytes,
# `70 fc`, as `jo -4` back to it. Four bytes at offset 34, so only the
# exit-span count met it, and the five tells before this one pass it: the
# flow is straight, the body holds no `(bad)`, no zero run, no stray REX
# and no pad. The tell is the x87 instruction, which GHC's x86-64 code
# generator does not emit.
PHANTOM9_LISTING = """\

run41-gheadnospec:     file format elf64-x86-64


Disassembly of section .text:

0000000000497d90 <microzm0zi1zminplacezmmicro_Main_zdfEqAxiszuzdczeze_info+0x81960>:
  497d90:\tf0 4c 89 45 f8       \tlock mov %r8,-0x8(%rbp)
  497d95:\t48 83 c5 e0          \tadd    $0xffffffffffffffe0,%rbp
  497d99:\t41 ff 65 f8          \tjmp    *-0x8(%r13)
  497d9d:\t0f 1f 00             \tnopl   (%rax)
  497da0:\t87 05 00 00 00 00    \txchg   %eax,0x0(%rip)        # 497da6 <microzm0zi1zminplacezmmicro_Main_zdfEqAxiszuzdczeze_info+0x81976>
  497da6:\t00 00                \tadd    %al,(%rax)
  497da8:\t1e                   \t(bad)
  497da9:\t00 00                \tadd    %al,(%rax)
  497dab:\t00 58 63             \tadd    %bl,0x63(%rax)
  497dae:\t32 01                \txor    (%rcx),%al
  497db0:\t48 c7 45 00 d8 7d 49 \tmovq   $0x497dd8,0x0(%rbp)
  497db7:\t00 
  497db8:\t48 89 de             \tmov    %rbx,%rsi
  497dbb:\t4c 8d 35 e8 0f 31 01 \tlea    0x1310fe8(%rip),%r14        # 17a8daa <microzm0zi1zminplacezmmicro_Main_zdfOrdAxis_closure+0x12a>
  497dc2:\te9 e1 7f 13 01       \tjmp    15cfda8 <ghczminternal_GHCziInternalziDataziOldList_actualSort_info>
  497dc7:\t90                   \tnop
  497dc8:\t87 05 00 00 00 00    \txchg   %eax,0x0(%rip)        # 497dce <microzm0zi1zminplacezmmicro_Main_zdfEqAxiszuzdczeze_info+0x8199e>
  497dce:\t00 00                \tadd    %al,(%rax)
  497dd0:\t1e                   \t(bad)
  497dd1:\t00 00                \tadd    %al,(%rax)
  497dd3:\t00 10                \tadd    %dl,(%rax)
  497dd5:\t63 32                \tmovsxd (%rdx),%esi
  497dd7:\t01 48 c7             \tadd    %ecx,-0x39(%rax)
  497dda:\t45 00 f8             \tadd    %r15b,%r8b
  497ddd:\t7d 49                \tjge    497e28 <microzm0zi1zminplacezmmicro_Main_zdfEqAxiszuzdczeze_info+0x819f8>
  497ddf:\t00 49 89             \tadd    %cl,-0x77(%rcx)
  497de2:\tde e9                \tfsubrp %st,%st(1)
  497de4:\t70 fc                \tjo     497de2 <microzm0zi1zminplacezmmicro_Main_zdfEqAxiszuzdczeze_info+0x819b2>
  497de6:\tff                   \t(bad)
  497de7:\tff 87 05 00 00 00    \tincl   0x5(%rdi)
  497ded:\t00 00                \tadd    %al,(%rax)
  497def:\t00 1e                \tadd    %bl,(%rsi)
  497df1:\t00 00                \tadd    %al,(%rax)
  497df3:\t00 f0                \tadd    %dh,%al
  497df5:\t62 32 01 48 c7       \t(bad)
  497dfa:\t45 f8                \trex.RB clc
  497dfc:\t30 7e 49             \txor    %bh,0x49(%rsi)
  497dff:\t00 4c 89 f7          \tadd    %cl,-0x9(%rcx,%rcx,4)
  497e03:\t48 8d 35 a7 6b 47 01 \tlea    0x1476ba7(%rip),%rsi        # 190e9b1 <stg_INTLIKE_closure+0x111>
  497e0a:\t4c 8d 35 a1 75 46 01 \tlea    0x14675a1(%rip),%r14        # 18ff3b2 <ghczminternal_GHCziInternalziNum_zdfNumIntzuzdczt_closure+0x2>
  497e11:\t48 89 5d 00          \tmov    %rbx,0x0(%rbp)
  497e15:\t48 83 c5 f8          \tadd    $0xfffffffffffffff8,%rbp
  497e19:\te9 52 c3 1d 01       \tjmp    1674170 <ghczminternal_GHCziInternalziList_scanr_info>
"""


def phantom9_listing(tmp):
    """The thirteenth saved site, planted for `--survey`: {'dis': path}."""
    path = os.path.join(tmp, 'run41-gheadnospec-0x497d90.dis')
    write(path, PHANTOM9_LISTING)
    return {'dis': path}


# The run-fill loop this README prices, 28 bytes and eight instructions, as
# `run25-g912` carries it at 0x434558; a second body differs in one
# register so the two group apart. Listings built from them are what the
# `--delta` cases subtract, a fixture needing two builds a line apart being
# nothing a system binary can stand in for.
LOOP_BODY = [('f2 0f 10 04 fa', 'movsd  (%rdx,%rdi,8),%xmm0'),
             ('49 89 f1', 'mov    %rsi,%r9'),
             ('4d 01 c1', 'add    %r8,%r9'),
             ('f2 42 0f 11 04 c9', 'movsd  %xmm0,(%rcx,%r9,8)'),
             ('48 01 c7', 'add    %rax,%rdi'),
             ('49 ff c0', 'inc    %r8'),
             ('49 39 d8', 'cmp    %rbx,%r8'),
             ('7c e4', 'jl')]
LOOP_BODY_B = [(b, t) if i != 1 else ('49 89 f9', 'mov    %rdi,%r9')
               for i, (b, t) in enumerate(LOOP_BODY)]
MAIN_SYM = 'microzm0zi1zminplacezmmicro_Main_zdfNFDataT_info'
LIB_SYM = ('statisticszm0zi16zi5zi0zm536b490adb2e81edec0faef6e3a878a0b1ba1a1e'
           '08e9471ff97c2975863bedae_StatisticsziQuantile_zdfOrdContParamzuzdc'
           'max_info')


def loop_listing(tmp, name, groups):
    """A listing holding `groups`, each (symbol, body, heads): the body at
    every head, under the symbol, in objdump's own form."""
    out = ['', '%s:     file format elf64-x86-64' % name, '', '',
           'Disassembly of section .text:', '']
    for sym, body, heads in groups:
        for head in sorted(heads):
            out.append('%016x <%s>:' % (head, sym))
            a = head
            for raw, text in body:
                if text == 'jl':
                    text = 'jl     %x <%s+0x0>' % (head, sym)
                out.append('  %x:\t%-21s\t%s' % (a, raw + ' ', text))
                a += len(raw.split())
            out.append('')
    path = os.path.join(tmp, name)
    write(path, '\n'.join(out) + '\n')
    return path


def delta_listings(tmp, kind):
    """OLD and NEW listings for `--delta`: {'old': path, 'new': path}.

    `grows`:   one copy of a group becomes two, the reading the default
               threshold dropped until b39ff49;
    `moves`:   two groups, one whose offsets move and no address survives,
               one that keeps an address and moves the other a line;
    `library`: a Main group beside a library one on both sides.
    """
    main = lambda heads, body=LOOP_BODY: (MAIN_SYM, body, heads)
    if kind == 'grows':
        old = [main([0x401000])]
        new = [main([0x401000, 0x402000])]
    elif kind == 'moves':
        old = [main([0x401000, 0x402000]),
               main([0x403000, 0x404000], LOOP_BODY_B)]
        new = [main([0x401040, 0x402108]),
               main([0x403000, 0x404040], LOOP_BODY_B)]
    elif kind == 'library':
        old = [main([0x401000, 0x402000]),
               (LIB_SYM, LOOP_BODY_B, [0x501027, 0x50102f])]
        new = [main([0x401000, 0x402000]),
               (LIB_SYM, LOOP_BODY_B, [0x501027, 0x50102f])]
    else:
        raise ValueError(kind)
    return {'old': loop_listing(tmp, 'zzdl-old', old),
            'new': loop_listing(tmp, 'zzdl-new', new)}

def parked_arm():
    """One arm the roster carries as `Only`, from Main.hs and not written
    out here: which arms are parked moves every run that prunes, and a
    fixture naming one by hand is a fixture that rots at the next prune.
    """
    roster = _reader().roster_of(open(os.path.join(HERE, 'Main.hs')).read())
    parked = [n for n, r, _ in roster if r == 'Only']
    assert parked, 'no parked arm in the roster, so this fixture has no case'
    return parked[0]


def readme_with_a_registration(tmp, arm=None, task=None, task_arm=None,
                               lead_extra=None, unscoped=False, bare=False,
                               script='read-run.py', views_only=False,
                               cross_both_target=None, no_items=False):
    """The README plus a synthetic OPEN registration, at the end.

    SYNTHETIC and not an edit of the live one, which is the whole point:
    a registration lives in the open list only until post-run step 5 moves
    it into the run's own file, so a fixture that edits the live entry
    stops building the moment the run it belongs to is written up. This
    one appends its own, so the case answers for the CHECK rather than for
    whichever run happens to be in hand. Run 99 is a number no run reaches.

    `arm` names an arm to put in backticks -- pass `parked_arm()` for the
    defect direction -- and `task` a task number to defer to.

    Every item is adjudicable, as `--lint` has held since 2026-09-17: a
    scoped `predict:` span, a committed `script:`, or a task deferral.
    `unscoped` drops the span's scope, `bare` adds an item with neither
    span nor script, and `script` names the script item (2) carries.
    `cross_both_target` moves item (1)'s target off 1, which is the
    defect direction for the `both` check: a cross-half span reads the
    two halves as reciprocals, so only a unity target holds on both.

    `task_arm` is the other half of the deferral: it PLANTS a task 99
    under the live tasks heading naming that arm, and defers to it. A
    registration's own arms and the arms of the task it points at are
    two populations, and until 2026-09-05 only the first was read --
    which is how Run 25 lost three predictions of four in one deferred
    item, every one of them stated against an arm parked the day after
    it was written.
    """
    text = subprocess.run(['wrap80', '--unwrap'], input=open(README).read(),
                          capture_output=True, text=True, check=True).stdout
    # `lead_extra` puts a clause INSIDE the bold lead, which is the shape
    # Run 33 declared and which `--move-registration` refuses after the
    # hours are spent: the mover matches the lead whole, ending at
    # `runs.**`, so one clause more is a refusal at post-run step 5 that
    # nothing catches at pre-run 7.
    tail = (' --- %s.**' % lead_extra) if lead_extra else '.**'
    if no_items:
        # A registration as the OWNER leaves it and before the preparation
        # predicts: the entry is committed with the pair and the numbered
        # items come later, at pre-run step 12a. Every other shape this
        # helper builds carries at least item (1), so no case could reach
        # the readers' empty-selection paths until this one.
        entry = ("- `OPEN` **What Run 99 is built to answer, registered"
                 " before it runs%s Registered for this fixture and for"
                 " nothing else. What the run predicts, item by item, is"
                 " the preparation's to add here before it runs, and none"
                 " is registered yet." % tail)
        return write(os.path.join(tmp, 'R.md'), text + '\n' + entry + '\n')
    entry = ("- `OPEN` **What Run 99 is built to answer, registered before"
             " it runs%s Registered for this fixture and for nothing else."
             " (1) *The box.* `list` moves under 3%%, `predict: cross list"
             " %s within 3%%%s`; killed by more."
             % (tail, cross_both_target or '1.0',
                '' if unscoped else ' on main both'))
    if arm:
        entry += (" (2) *The arm.* `%s` leads its family; killed by a loss,"
                  " `script: %s`." % (arm, script))
    if bare:
        entry += " (5) *The unread.* Something moves; killed by nothing."
    if views_only:
        entry += (" (6) *The views.* `predict: countdiff mut-odo-vecdims"
                  " bq-expand under 100 on views stretch-primes both`.")
    if task:
        entry += " (3) *The additions.* Task %s's, read there." % task
    if task_arm:
        entry += " (4) *The deferral.* Task 99's, read there."
        # After the HEADING LINE, not by paragraph: unwrapped, the heading
        # carries no blank line before it, so a `\n\n` split leaves it
        # glued to the paragraph above and finds nothing. The reader's own
        # `unwrapped_paragraphs` does isolate it, which is why the check
        # sees the tasks that this fixture could not.
        anchor = '\n### Standing rulings from past runs'
        assert text.count(anchor) == 1, ('tasks heading: %d site(s)'
                                         % text.count(anchor))
        eol = text.index('\n', text.index(anchor) + 1)
        text = (text[:eol + 1]
                + "\n99. `OPEN` **A planted task, for the deferral fixture"
                  " alone.** It predicts that `%s` leads its family; killed"
                  " by a loss.\n" % task_arm
                + text[eol + 1:])
    return write(os.path.join(tmp, 'R.md'), text + '\n' + entry + '\n')


def prev_rundoc_for_a_registration(tmp, pointer):
    """`runs/run98.md` beside a fixture README registering Run 99.

    Its compares-against section declares the next run's pair, which is
    what a run file's does, and `pointer` is whether it also names the
    registration. Those are the two committed declarations Run 35 had of
    itself -- the open list's and the previous run file's -- and they
    named different pairs with every check here green, the registration
    check reading arms and not pairs.
    """
    d = os.path.join(tmp, 'runs')
    os.makedirs(d, exist_ok=True)
    ref = ' [registered 2026-09-18][open]' if pointer else ''
    return write(os.path.join(d, 'run98.md'),
                 '# Run 98\n\n## What the next run compares against\n\n'
                 '**Run 99 is the pair below%s.** One variable and nothing'
                 ' else.\n\n## Another section\n\nProse.\n' % ref)


def readme_with_an_uncovered_figure(tmp, kind):
    """The README plus a section no replace-list bullet links, carrying a
    figure the coverage check could not see until 2026-09-04: `wrapped`,
    a list item whose decimal wraps past its first line, where wrap80
    indents the continuation six and the check took four as code; `hex`,
    a paragraph whose only figures are an address and a mod-64 offset,
    which is the pinning claim's whole vocabulary.
    """
    text = open(README).read()
    if kind == 'wrapped':
        sec = ('\n### Zz coverage probe\n\n'
               '   1. **A step whose one figure sits past the first line of'
               ' its item**, the largest deviation the anchor check allows'
               ' being 4.1% on the middle anchor.\n')
    else:
        sec = ('\n### Zz coverage probe\n\n'
               'The first head of each group moved by 0x3d00 and the rest by'
               ' 0x4cc0, every mod-64 offset preserved.\n')
    return write(os.path.join(tmp, 'R.md'), text + sec)

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


def rundoc_summary_row_short(tmp, cls='rev'):
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


def readme_with_a_run_step_and_its_reasons(tmp):
    """A run list of two steps, the first carrying reasons under `why:`."""
    return write(os.path.join(tmp, 'R.md'),
                 '# A run list\n\n'
                 '    grep -i gate $R-pair.txt     # 13. has the gate passed?\n'
                 '    #      ACTION-BEFORE-WHY: read the verdict\n'
                 "    #      why: --para 'A paired Run has one gate more'\n"
                 '    #      REASON-AFTER-WHY, skipped by default\n'
                 '    ./run-evening.sh $R          # 14. the evening\n'
                 '    #      ACTION-OF-14\n')


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


def readme_answered_stub_unfilled(tmp):
    """A copy of README whose newest ANSWERED run entry still carries the
    `___` placeholder `--move-registration` leaves for the verdict clause.

    Self-aiming, by the stub's own shape rather than by a run number: the
    entry is found by its family lead and the clause after `in a clause
    each:` is replaced whole, so the fixture follows a requote instead of
    failing to build after one. Run 28 shipped this state as far as the
    SECOND checker pass -- every mechanical gate passed over a bare
    underscore where sixteen verdicts belong -- which is the defect the
    check beside this case was written for.
    """
    text = open(README).read()
    flat = subprocess.run(['wrap80', '--unwrap'], input=text,
                          capture_output=True, text=True, check=True).stdout
    m = re.search(r'(- `ANSWERED` \*\*What Run \d+ was built to answer[^\n]*?'
                  r'in a clause each: )(.*?)(?=\n)', flat)
    assert m, 'no ANSWERED run entry with a verdict clause to empty'
    return write(os.path.join(tmp, 'R.md'),
                 flat[:m.start(2)] + '___.' + flat[m.end(2):])


def readme_six_pair_perturbed(tmp):
    """A copy of README whose carry-back sentence quotes a first figure no
    other site does, found by the sentence's shape rather than by the
    run's figure -- `X% and Y% read on the six pairs` -- so that the
    fixture follows the requote instead of failing to build after it.

    RE-SHAPED 2026-09-05: the anchor was `the same run gives **X% and
    Y%**`, which Run 24's floor sentence carried inside one of the
    check's own AGREEING sites. Run 25's prune left SIX A/A pairs in all
    and only FOUR carrying back to Run 10, so that sentence could not say
    `the six pairs that carry back to Run 10` truthfully any more and was
    rewritten -- and an anchor that lands OUTSIDE an AGREEING site
    perturbs text the check does not read, which is a fixture that builds
    and a case that cannot fire. The shape here is one of the sites.

    RE-SHAPED AGAIN 2026-09-11, for the same reason one roster later, and
    the anchor is now population-independent so a third landing does not
    move it. Run 28 landed the shipped fill's own A/A pair, so the set is
    EIGHT and the sentence cannot say `the six pairs` either; what it can
    say at any size is `pairs that carry back to Run 10`, and the check's
    own pattern was generalised to that on the same day. The figures are
    bolded in the live sentence, which the earlier anchor did not allow
    for.
    """
    text = open(README).read()
    flat_text = subprocess.run(['wrap80', '--unwrap'], input=text,
                               capture_output=True, text=True,
                               check=True).stdout
    shape = (r'(pairs that carry back to Run 10[^.]*?\*{0,2})'
             r'([\d.]+)(%\*{0,2} and \*{0,2}[\d.]+%)')
    ms = list(re.finditer(shape, flat_text))
    assert len(ms) == 1, ('the carry-back sentence occurs %d times in README,'
                          ' need 1' % len(ms))
    m = ms[0]
    old = m.group(0)
    new = '%s%.2f%s' % (m.group(1), float(m.group(2)) + 0.30, m.group(3))
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


def rundoc_results_names_a_run_shape(tmp):
    """The run file with a sentence in Results naming a `block` shape,
    `block-run64-gap1`, whose `run64-` the stale-name check read as a half
    of Run 64."""
    text = rundoc_text()
    old = '## Results'
    assert text.count(old) == 1
    new = ('## Results\n\nThe widest cell is `block-run64-gap1`, at 0.968.\n')
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


def rundoc_with_a_long_head(tmp):
    """The run file with its head padded to one paragraph past the form,
    the reader's HEAD_PARAGRAPHS, past the preamble. Padded by however
    many the live head lacks, so the fixture outlives the run and the
    limit.
    """
    text = rundoc_text()
    head, sep, rest = text.partition('\n## ')
    assert sep, 'the run file has no `## ` section to end its head at'
    paras = [q for q in head.split('\n\n') if q.strip()
             and not q.lstrip().startswith('#')]
    extra = ''.join('**zz-head-paragraph %d, one more than the form.** Its'
                    ' figure is 1.2345.\n\n' % k
                    for k in range(max(1, _reader().HEAD_PARAGRAPHS + 2
                                       - len(paras))))
    return write_rundoc(tmp, head.rstrip('\n') + '\n\n' + extra.rstrip('\n')
                        + '\n\n' + sep + rest)


def rundoc_pair_with_carried_body_claim(tmp):
    """`rundoc_pair` held, plus a BODY paragraph both files share verbatim
    that calls itself this run's.

    The head is gated by position and the body was only counted, so Run 29
    cleared its head, saw `--check-doc` go green, and left thirty carried
    paragraphs in the body -- thirteen of which its checker returned, one
    asserting the opposite of the run's central finding and one whose
    `this run` had meant a run four earlier since it was written. This
    plants that shape: identical text, below the first `## `, saying `this
    run`. Added 2026-09-12.
    """
    made = rundoc_pair(tmp, held=True)
    para = ('**zz-carried-claim, a body paragraph carried whole.** What'
            ' this run reads here is 1.234, and it says so in both files.')
    at = os.path.dirname(made['rundoc'])
    for name in sorted(n for n in os.listdir(at)
                       if re.match(r'run\d+\.md$', n)):
        path = os.path.join(at, name)
        text = open(path).read()
        head, sep, rest = text.partition('\n## ')
        assert sep, '%s has no `## ` section to end its head at' % name
        first, nl, tail = rest.partition('\n')
        write(path, head + sep + first + nl + '\n' + para + '\n' + tail)
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


def rundoc_carried_figures(tmp):
    """A registration quoting one figure its span derives and one it cannot.

    Item (1) names two real arms and quotes 0.4242, which that pair does
    not produce on the run given: the shape of the defect this mode exists
    for, an item whose prose figure belongs to some other comparison than
    its own span's. Item (2) names a pair and quotes nothing, so it is
    counted and never warned -- the control that keeps the warning from
    being "every item with a span". Added 2026-09-12.
    """
    doc = ('# Run 99 (fixture)\n\n'
           'A head paragraph.\n\n'
           '## What this run was built to answer, and what it answered\n\n'
           '(1) *The carried one.* On the main set:'
           ' `predict: pair mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims'
           ' 0.64 within 5%` --- Run 98 reading 0.4242. (2) *The bare one.*'
           ' `predict: pair bq-expand list 0.11 within 5%` and no figure'
           ' quoted at all.\n')
    return {'rundoc': write_rundoc(tmp, doc, name='run99.md')}


def scoped_spans_run(tmp):
    """Run 99's two main-set halves, their note and counts sweeps, and a
    run file whose registration scopes every span: one read on the main
    set on both halves, one on a class, one on the basis alone, a `cell`
    span, a `countdiff` span that holds and one on a named view that
    does not, and an item adjudicated by a committed script.

    The cell's figure and the countdiff bounds are derived here through
    the reader, so the spans hold or fail by construction and the case
    reads which cells and counts each kind took.
    """
    m = _reader()
    write(os.path.join(tmp, 'run99-pair.txt'), NOTE_STUB)
    a = synth_json(tmp, 'main', name='run99-lookrts-main.json')
    b = synth_json(tmp, 'main', name='run99-a1g-main.json')
    ca = synth_counts(tmp, 'ca.txt', cheap_sum_only=True)
    cb = synth_counts(tmp, 'cb.txt', cheap_sum_only=True)
    cells, shapes, strategies, _ = m.load(a, MAIN)
    m.apply_correction(cells, shapes, strategies)
    sh = shapes[0]
    x = cells[sh]['mut-odo-vecdims']['net'] / cells[sh]['bq-expand']['net']
    counts = m.parse_counts(ca)[0]
    d = max(counts[s]['mut-odo-vecdims'] - counts[s]['bq-expand']
            for s in shapes)
    doc = ('# Run 99 (fixture)\n\nA head paragraph.\n\n'
           '## What this run was built to answer, and what it answered\n\n'
           '(1) *Main.* `predict: cross list 1.0 within 99%% on main both`.'
           ' (2) *A class.* `predict: cross list 1.0 within 99%% on bcast'
           ' both`. (3) *The basis.* `predict: cross list 1.0 within 99%% on'
           ' main basis`. (4) *A cell.* `predict: cell %s/mut-odo-vecdims'
           ' over %s/bq-expand %.4f within 0.1%% on main both`. (5) *Counted.*'
           ' `predict: countdiff mut-odo-vecdims bq-expand under %d on main'
           ' both`. (6) *Counted on a view.* `predict: countdiff'
           ' mut-odo-vecdims bq-expand under %d on views %s on main both`.'
           ' (7) *By hand.* Read by `script: read-run.py`.\n'
           % (sh, sh, x, d + 1, d, sh))
    return {'a': a, 'b': b, 'ca': ca, 'cb': cb,
            'rundoc': write_rundoc(tmp, doc, name='run99.md')}


def scoped_spans_in_place(tmp, stale=False):
    """`scoped_spans_run` laid out as a run is, for --predictions
    --in-place to find by name: the sweeps as `run99-counts-HALF.txt`,
    and, where `stale`, a verdict paragraph for item (1) already written
    by an earlier call, which a rerun replaces rather than repeats.
    """
    r = scoped_spans_run(tmp)
    shutil.copy(r['ca'], os.path.join(tmp, 'run99-counts-lookrts.txt'))
    shutil.copy(r['cb'], os.path.join(tmp, 'run99-counts-a1g.txt'))
    if stale:
        # Appended as a first call leaves it, after the file's own final
        # newline: stripped first, the paragraph read back clean and hid a
        # rerun writing item (1) twice.
        text = open(r['rundoc']).read()
        write(r['rundoc'], text + '\n\n**Read by --predictions, item (1):**'
              ' STALE, from an earlier call.')
    return r


def scoped_spans_two_blanks(tmp):
    """`scoped_spans_in_place` with every heading after two blank lines,
    as a run file keeps them, for the heading-spacing case."""
    r = scoped_spans_in_place(tmp)
    text = open(r['rundoc']).read()
    write(r['rundoc'], re.sub(r'(?<=[^\n])\n\n(## )', r'\n\n\n\1', text))
    return r


def heading_spacing_word(path):
    """HEADING LOST ITS BLANK where any `## ` heading has one blank line
    above it and not two, else HEADINGS KEEP TWO BLANKS."""
    lines = open(path).read().split('\n')
    lost = [l for i, l in enumerate(lines) if l.startswith('## ') and i > 1
            and not (lines[i - 1] == '' and lines[i - 2] == '')]
    return 'HEADING LOST ITS BLANK' if lost else 'HEADINGS KEEP TWO BLANKS'


def drift_repo(tmp, moved=True):
    """A throwaway checkout for registration-drift.py: a README carrying
    Run 97's registration, a Main.hs, and, where `moved`, one commit to
    `fooFill` after the registration; the note names the tip as built."""
    d = os.path.join(tmp, 'repo')
    os.makedirs(d)
    g = lambda *a: subprocess.run(['git', '-C', d, '-c', 'user.email=t@t',
                                   '-c', 'user.name=t'] + list(a),
                                  check=True, capture_output=True, text=True)
    g('init', '-q')
    write(os.path.join(d, 'README.md'), 'What Run 97 is built to answer.\n')
    write(os.path.join(d, 'Main.hs'), 'fooFill :: Int\nfooFill = 1\n')
    g('add', '.')
    g('commit', '-q', '-m', 'register')
    if moved:
        write(os.path.join(d, 'Main.hs'), 'fooFill :: Int\nfooFill = 2\n')
        g('commit', '-q', '-am', 'rebuild the fill')
    tip = g('rev-parse', '--short', 'HEAD').stdout.strip()
    write(os.path.join(d, 'run97-pair.txt'), '  Main.hs at        %s\n' % tip)
    return {'dir': d}


def drift_since_repo(tmp, code=True, pragma=False):
    """A throwaway checkout for `registration-drift.py --since`: a roster
    of two arms, `lib-a` reaching `fooFill` through `fbA` and `lib-b`
    reaching nothing, built once as Run 96, then one commit that changes
    `fooFill`'s code where `code`, only a comment above it otherwise, and
    only an INLINE pragma for it at column 0 where `pragma`;
    Run 97's note names the tip, and no binary is here."""
    d = os.path.join(tmp, 'repo')
    os.makedirs(d)
    g = lambda *a: subprocess.run(['git', '-C', d, '-c', 'user.email=t@t',
                                   '-c', 'user.name=t'] + list(a),
                                  check=True, capture_output=True, text=True)
    g('init', '-q')
    head = ('roster :: [(String, Arm)]\nroster =\n'
            '  [ ("lib-a",  Fill fbA)\n  , ("lib-b",  Fill fbB)\n  ]\n'
            'fbA :: Int\nfbA = fooFill 1\nfbB :: Int\nfbB = 2\n')
    write(os.path.join(d, 'Main.hs'),
          head + 'fooFill :: Int -> Int\nfooFill x = x\n')
    g('add', '.')
    g('commit', '-q', '-m', 'build 96')
    base = g('rev-parse', '--short', 'HEAD').stdout.strip()
    write(os.path.join(d, 'Main.hs'), head + (
        '{-# INLINE fooFill #-}\nfooFill :: Int -> Int\nfooFill x = x\n'
        if pragma else
        'fooFill :: Int -> Int\nfooFill x = x + 1\n' if code else
        '-- a note on the fill\nfooFill :: Int -> Int\nfooFill x = x\n'))
    g('commit', '-q', '-am', 'inline the fill' if pragma else
      'rebuild the fill' if code else 'note the fill')
    tip = g('rev-parse', '--short', 'HEAD').stdout.strip()
    write(os.path.join(d, 'run96-pair.txt'), '  Main.hs at        %s\n' % base)
    write(os.path.join(d, 'run97-pair.txt'), '  Main.hs at        %s\n' % tip)
    return {'dir': d}


def prior_with_mode_args(tmp):
    """A README whose one registration item names its prior's mode WITH
    the mode's arguments, `--pair A B`, and no file: the form --lint read
    as no mode until 2026-09-24. Shared by the case and by the mutant's
    judge, whose shell string cannot carry the backticks."""
    lead = a_registration_lead()
    return edited_readme(tmp, (
        lead,
        '- `OPEN` **What Run 99 is built to answer, registered before it'
        ' runs.** (1) *A prior named with its mode and arguments.* Run 98'
        ' read it at 1.12, `--pair lib-stage2-lean-u1 lib-stage3-lean` on'
        ' its main set. `predict: pair lib-stage2-lean-u1 lib-stage3-lean'
        ' 1.05 within 4% on main both`.\n\n' + lead))


def a_previous_note(tmp):
    """Run 97's note beside a copy of the live template, for --draft: a
    [PAIR'S] block, a `[SAME, ...]` block rewritten for its pair in ONE
    paragraph, and no RERUN line, which the template gained later."""
    shutil.copy(os.path.join(HERE, 'pair-note-template.txt'), tmp)
    return write(os.path.join(tmp, 'run97-pair.txt'),
                 "The pair run97-a and run97-b, Run 97's, written by hand"
                 ' 2026-01-01.\n\n'
                 "WHAT THIS PAIR MEASURES [PAIR'S]: the regime, the fourth"
                 ' time.\n\n'
                 'HALVES: basis=a other=b\n\n'
                 'THE MACHINE [SAME, ITS TERMS REWRITTEN]: the fingerprint'
                 ' read against is\nRun 96\'s own, and the check carries a'
                 ' source term.\n\n'
                 'Verified when built, 2026-01-01:\n'
                 '  Main.hs at        deadbee, tree clean\n'
                 '  shim at           deadbee, tree clean\n')


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


def registration_to_move(tmp, n=97):
    """A README with one OPEN registration, and the run file to move it to.

    The registration carries a link to a README section by BARE anchor,
    which is what a registration written in the open list naturally has
    and what stops resolving the moment the text lands in `runs/`. Built
    rather than borrowed: the live README's registration is this run's
    and moves with every write-up.
    """
    m = _reader()
    d = os.path.join(tmp, m.RUNS_DIR)
    os.makedirs(d, exist_ok=True)
    readme = write(os.path.join(tmp, 'README.md'),
                   '# T\n\n## What is open\n\n'
                   '- `OPEN` **What Run %d is built to answer, registered'
                   ' before it runs.** Registered before the run. (1) *a*'
                   ' `predict: cross list 1.0 within 1%%`, read against'
                   ' [the shapes](#the-shape-set) and no other.\n'
                   '- `ANSWERED` **Something else.** Its body.\n\n'
                   '## The shape set\n\nA paragraph.\n' % n)
    doc = write(os.path.join(d, 'run%d.md' % n),
                '# Run %d\n\nA head paragraph.\n\n%s\n\n'
                'The previous run\'s registration, to be replaced.\n'
                % (n, m.REG_HEAD))
    return {'readme': readme, 'doc': doc}


def registration_to_move_with_pointer(tmp, n=97):
    """`registration_to_move`, the run file also carrying the pointer
    pre-run step 12a adds to the previous run's file and step 5's copy
    brings across: `**Run N's pair ... [registered <date>][open]**`."""
    got = registration_to_move(tmp, n)
    text = open(got['doc']).read()
    old = 'A head paragraph.\n\n'
    assert text.count(old) == 1
    write(got['doc'], text.replace(old, old + (
        "**Run %d's pair is this run's, both recipes to the character,"
        ' [registered 2026-09-24][open]**, on the owner\'s word.\n\n'
        % n), 1))
    return got


def lone_rundoc(tmp):
    """A run file with no earlier run beside it, which is a fixture's shape.

    `previous_run_doc` looks in the directory the file sits in, so a
    fixture built alone has nothing before it -- the state a first run is
    in, and the one a copy handed to a mode is in more often than that.
    """
    m = _reader()
    d = os.path.join(tmp, m.RUNS_DIR)
    os.makedirs(d, exist_ok=True)
    return write(os.path.join(d, 'run1.md'), '# Run 1\n\nA head.\n')


def brief_facts_without_halves(tmp):
    """A synthetic run whose log never says which half is the basis.

    Runs 11 to 13 wrote that line differently and a killed run may not
    reach it at all, so the driver has to meet a log without it. Built by
    taking the clause out of the fixture's own log rather than by a second
    fixture, which would drift from it.
    """
    out = synthetic_run(tmp, plateau=[['19.0'], ['19.1']])
    log = here_file('%s-wallclock.log' % out['tag'])
    text = open(log).read()
    assert ' is the basis' in text, 'the fixture stopped naming the basis'
    write(log, text.replace(' is the basis', ''))
    return out


def brief_facts_underscored_basis(tmp):
    """The same run with its basis named `look_rts`, in the log's clause
    and on a note's md5 row, a half's tag being [A-Za-z0-9_]."""
    out = synthetic_run(tmp, plateau=[['19.0'], ['19.1']])
    log = here_file('%s-wallclock.log' % out['tag'])
    text = open(log).read()
    assert text.count('lookrts is the basis') == 1, 'the clause moved'
    write(log, text.replace('lookrts is the basis', 'look_rts is the basis'))
    write(here_file('%s-pair.txt' % out['tag']),
          'A pair note, its md5 rows alone.\n\n'
          '  md5 look_rts      0123456789abcdef0123456789abcdef\n')
    return out


def plateau_two_halves(tmp):
    """A paired run's plateau logs: two halves, two processes each.

    `synthetic_run`'s own plateau logs are one half's, and the by-half
    block prints nothing under two halves, so the second half is written
    on top of the fixture rather than into it -- the shape
    `brief_facts_without_halves` uses, and for the same reason: a second
    fixture would drift from the first.

    The halves are deliberately unalike. `lookrts` is flat, 19.0 against
    19.1, and `o2half` is not, 30.0 against 33.0 -- so the run-wide spread
    and one half's are both wide while the other half is tight, which is
    the state a pair whose variable moves `list` produces and the one a
    reader has to tell from drift.
    """
    out = synthetic_run(tmp, plateau=[['19.0'], ['19.1']])
    sat = ('@@saturate dose=1x by=list sprayed=1000000 in 6.0 s; victim'
           ' vgg-14-c512-k3/list %s ms/iter over 20; inuse=1 keep=1\n')
    for pop, ms in (('rev', '30.0'), ('slice', '33.0')):
        write(here_file('%s-o2half-%s.log' % (out['tag'], pop)),
              'benchmarking x/y\n' + sat % ms)
    return out


def inherited_pair(tmp, n=97, share=True, half=False):
    """Two consecutive runs' files, the later copied from the earlier.

    Step 5 copies the previous run's file whole and the write-up edits it,
    so a paragraph nobody touched is BOTH inherited and outside the
    checker's diff, whose base is that copy. The fixture carries one of
    each kind: a paragraph making a claim about the run in front of it,
    which must be reported, and one of the standing apparatus every run
    re-carries, which must not. `share=False` is the control, the write-up
    having rewritten both, so the report has nothing to name.

    `half=True` is the third shape and the one a diff shows: the claim's
    LEAD is rewritten for this run and its body still quotes the run
    before. It is in the diff, so a checker pass reading that diff sees a
    paragraph being worked on rather than a claim left standing -- which
    is how Run 33's floor paragraph and its class-property entry passed
    one pass each and were caught by the next reading the whole document.
    """
    m = _reader()
    d = os.path.join(tmp, m.RUNS_DIR)
    os.makedirs(d, exist_ok=True)
    claim = ('**On Run %d the floor is 0.31%% on the basis half.** This run'
             ' reads it over the six A/A pairs.\n' % (n - 1))
    standing = ('The table below is installed by the reader and never'
                ' edited by hand.\n')
    write(os.path.join(d, 'run%d.md' % (n - 1)),
          '# Run %d\n\nA head paragraph.\n\n%s\n%s' % (n - 1, claim, standing))
    if half:
        body = ('**On Run %d the floor is 0.44%% on the basis half.** Run %d'
                ' read it over the six A/A pairs and named the pair that'
                ' carried it.\n\n%s' % (n, n - 1, standing))
    elif share:
        body = claim + '\n' + standing
    else:
        body = ('**On Run %d the floor is 0.44%% on the basis half.** This'
                ' run reads it over the six A/A pairs.\n\nThe table below'
                ' is installed by the reader, never by hand.\n' % n)
    doc = write(os.path.join(d, 'run%d.md' % n),
                '# Run %d\n\nA head paragraph of its own.\n\n%s' % (n, body))
    return {'doc': doc}


def lost_pair(tmp, n=97, deleted=True):
    """A run file whose step-5 copy is a commit, and which lost a paragraph.

    Same shape as `stale_pair` and for the same reason: `--lost` reads the
    run file against the commit that ADDED it, so the fixture is a git
    checkout and not two loose files.

    THE CONTROL IS BUILT IN. The copy carries THREE paragraphs: a head, one
    the write-up REWRITES around the same body, and one the write-up
    REMOVES. A mode that reported the rewritten one would be reporting
    every edited paragraph, which is `--stale`'s job and not this one, so
    the case asserts one gone and the other not named. `deleted=False`
    keeps all three and is the control on which the mode must find nothing.
    """
    doc = os.path.join(tmp, 'run%d.md' % n)
    kept_para = ('**The straddling loops stand at TEN on each half.** The'
                 ' survey reads them off the timed binary and the count'
                 ' moved on both halves alike, so it is the source.')
    goes = ('**The regime was confirmed in this run own binaries before the'
            ' hours were spent.** Diag on one shape puts the two figures'
            ' ten times apart, which is the level this basis asks for.')
    write(doc, '# Run %d\n\nA head paragraph.\n\n%s\n\n%s\n'
               % (n - 1, kept_para, goes))
    env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
               GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')
    for cmd in (['init', '-q'], ['add', '--', os.path.relpath(doc, tmp)],
                ['-c', 'commit.gpgsign=false', 'commit', '-q', '-m',
                 'copy run%d to run%d' % (n - 1, n)]):
        subprocess.run(['git', '-C', tmp] + cmd, check=True, env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rewritten = ('**The straddling loops stand at TWELVE on each half.** The'
                 ' survey reads them off the timed binary and the count'
                 ' moved on both halves alike, so it is the source.')
    body = '# Run %d\n\nA head paragraph.\n\n%s\n' % (n, rewritten)
    if not deleted:
        body += '\n%s\n' % goes
    write(doc, body)
    return {'doc': doc}


def stale_pair(tmp, n=97, kept=True, word=False):
    """A run file whose step-5 copy is a commit, and which edited a figure
    -- or did not.

    `--stale` reads the run file against the commit that ADDED it, which
    is step 5's copy of the previous run's file, so the fixture has to be
    a git checkout and not two loose files: the copy is the commit and the
    working file is the write-up. `kept=True` plants the defect the mode
    exists for, a paragraph whose lead was rewritten for this run around a
    figure that was not; `kept=False` is the control, the same edit with
    the figure moved too, on which the mode must find nothing.

    The figure is a percentage, which is the shape of a measured one --
    the mode leads with decimals, percentages and two-digit counts, a
    first draft having printed every `one` and `two` in the document.
    """
    m = _reader()
    d = os.path.join(tmp, m.RUNS_DIR)
    os.makedirs(d, exist_ok=True)
    doc = os.path.join(d, 'run%d.md' % n)
    # `word=True` plants the shape two of Run 35's four stale figures had,
    # a WORD numeral: the mode's first tiers admitted digits alone, so those
    # two sat in the bucket only --all prints while its docstring claimed
    # the default view printed them.
    planted = 'thirty-four' if word else '0.31%'
    copy = ('# Run %d\n\nA head paragraph.\n\n**On Run %d the floor is'
            ' %s on the basis half.** It is read over the six A/A pairs'
            ' this roster carries, and the pair that carries it is named'
            ' beside the figure in the table above.\n'
            % (n - 1, n - 1, planted))
    write(doc, copy)
    env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
               GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')
    for cmd in (['init', '-q'], ['add', '--', os.path.relpath(doc, tmp)],
                ['-c', 'commit.gpgsign=false', 'commit', '-q', '-m',
                 'copy run%d to run%d' % (n - 1, n)]):
        subprocess.run(['git', '-C', tmp] + cmd, check=True, env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    figure = planted if kept else ('forty-one' if word else '0.44%')
    write(doc, '# Run %d\n\nA head paragraph of its own, rewritten for this'
               ' run.\n\n**On Run %d the floor is %s on the basis half, the'
               ' widest of the eight A/A pairs.** It is read over the eight'
               ' pairs this roster carries, and this run names the pair that'
               ' carries it beside the figure in the table above.\n'
               % (n, n, figure))
    return {'doc': doc, 'figure': figure}


def brief_pair(tmp, run='run97', whole=True, stale_block=False, bodied=False):
    """A facts file and a checker brief, the brief missing an item or not.

    `--brief-update` writes the brief's two THIS RUN ONLY items from the
    facts file `post-run-readings.sh` leaves, which is the one step of the
    verification half nothing checked -- a stale brief looks exactly like a
    used one, and both checker passes read it as given.

    `whole=False` is the shape the case is about: a brief carrying item 5
    and not item 6, which is what a half-finished edit or a renumbering
    leaves. A mode that wrote what it could would leave one item this run's
    and one the run before's, which is worse than either, so the refusal is
    the behaviour and the brief must come back byte for byte.
    """
    d = os.path.join(tmp, 'log-read-%s' % run)
    os.makedirs(d, exist_ok=True)
    write(os.path.join(d, 'for-brief.txt'),
          'some facts above the marker\n\n'
          '--- paste over checker-brief.txt items 5 and 6; <yours> is prose ---\n'
          ' 5. THIS RUN ONLY -- THE BOX AND THE PAIR. The basis is %s-exit.\n'
          ' 6. THIS RUN ONLY -- THE WINDOW AND THE INSTRUMENTS. One window.\n'
          % run)
    body = ' 5. THIS RUN ONLY -- THE BOX AND THE PAIR. Last run\'s.\n'
    # `bodied` gives each old item an indented body, the shape every real
    # brief has: the header line alone being replaced left those bodies
    # under the new items, run after run.
    if bodied:
        body += '    last run\'s body of item five\n'
    if whole:
        body += ' 6. THIS RUN ONLY -- THE WINDOW AND THE INSTRUMENTS. Last run\'s.\n'
        if bodied:
            body += '    last run\'s body of item six\n\nTHE NEXT SECTION stays.\n'
    # A SUBSTITUTION BLOCK NAMING ANOTHER RUN, for the case that the mode
    # rewrites it: it wrote the two items alone while its docstring said it
    # wrote this too. The halves come from pair-halves.sh, so the fixture
    # ships that script and a note for it to read.
    head = 'The brief.\n\n'
    if stale_block:
        head = ('The brief.\n\nSubstitute per run: RUN=run11 BASIS=wrong'
                ' OTHER=alsowrong PREV=run9\n\n')
        here = os.path.dirname(os.path.abspath(__file__))
        shutil.copy(os.path.join(here, 'pair-halves.sh'), tmp)
        write(os.path.join(tmp, '%s-pair.txt' % run),
              'a stand-in pair note.\nHALVES: basis=exit other=ghead\n'
              'COMPARE: run96\n')
        write(os.path.join(tmp, 'run96-pair.txt'),
              'the previous run.\nHALVES: basis=nospec other=ghead\n')
    brief = write(os.path.join(tmp, 'checker-brief.txt'), head + body)
    return {'brief': brief, 'run': run, 'dir': tmp}


def rundoc_heading_spacing(tmp, blanks=1):
    """A run file whose second heading is preceded by `blanks` blank lines.

    Two is this project's spacing and one is the shape that bites: with
    NONE the heading joins the paragraph above it and `--replace`, whose
    unit is a blank-line paragraph, takes the heading out with it -- the
    defect the open list records for 2026-09-03 and which Run 27 put back
    into README by an off-by-one insert. Built rather than borrowed: the
    live files are the thing the check is meant to keep clean.
    """
    sep = '\n' * blanks
    return write_rundoc(tmp,
                        '# Run 97\n\nA head paragraph.\n' + sep
                        + '## Results\n\nA paragraph under it.\n')



def doc_with_a_table(tmp, n=1):
    """A document of three sections, the middle one carrying `n` tables.

    One table is what every earlier case wants and is left byte for byte
    as it was; several is what `--with-tables N` selects among, and those
    are labelled so a case can say WHICH one came back.
    """
    if n == 1:
        tables = '| a | b |\n|---|---|\n| 1 | 2 |\n\n'
    else:
        tables = ''.join('| a%d | b%d |\n|---|---|\n| %d | %d |\n\n'
                         % (k, k, k, k) for k in range(1, n + 1))
    return write(os.path.join(tmp, 'S.md'),
                 '# T\n\n## Header one\n\nProse one.\n\n## Middle\n\n'
                 'Prose before.\n\n' + tables +
                 'Prose after the table.\n\n## Tail\n\nProse three.\n')


def doc_with_a_glued_table(tmp):
    """A section whose table follows its lead with NO blank line between.

    Which is how every two-column table in this chapter is written, and
    markdown renders it the same -- so a splitter keyed on the paragraph
    STARTING with a bar cannot see it, and the table is unselectable
    while the fingerprints below it, which do start one, are the only
    things `--with-tables N` can name. The second table here is glued and
    the first is not, so a case can say which one came back.
    """
    return write(os.path.join(tmp, 'G.md'),
                 '# T\n\n## Middle\n\n'
                 '| a1 | b1 |\n|---|---|\n| 1 | 1 |\n\n'
                 'The lead sentence of the glued table.\n'
                 '| a2 | b2 |\n|---|---|\n| 2 | 2 |\n\n'
                 'Prose after.\n\n## Tail\n\nProse three.\n')


def note_with_gate_below_the_fill(tmp, name='run97-pair.txt'):
    """A previous note whose gate verdict continues BELOW the fill-in block.

    That is the ORDINARY shape and not a contrived one: run-gate.sh
    appends its block at the end of the note and the hand verdict is
    written beside it, so a gate's continuations sit under the fill-in
    block rather than over it. The blocks run GATE, `Verified when
    built`, then two paragraphs that continue the gate and nothing else.
    """
    return write(os.path.join(tmp, name),
                 'The pair run97-a and run97-b, Run 97s, written by hand'
                 ' 2026-01-01\nBEFORE either of the PAIRS binaries'
                 ' exists.\n\n'
                 'HALVES: basis=a other=b\n\n'
                 "WHAT THIS PAIR MEASURES [PAIRS]: the thing.\n\n"
                 'THE MACHINE [SAME]: the box.\n\n'
                 'GATE: RUN AND SOUND, 2026-01-01. Five benches a half.\n\n'
                 'Verified when built, 2026-01-01:\n'
                 '  md5 a           deadbeef\n\n'
                 'AND THE PALINDROME SPREAD WAS RUN 96s, arm for arm, and'
                 ' this paragraph is the gates and spent with it.\n\n'
                 'AND THE MACHINE CHECK DID NOT FIRE for run97 either.\n')


def note_for_the_check(tmp, broken=True, vc='regime other'):
    """This run's note, with or without the three stale statements.

    Run 99's, so the synthetic registration `readme_with_a_registration`
    appends is the one read, and a `runs/run98.md` beside it so the
    previous run resolves to 98. Broken, the note carries one of each
    kind: a continuity claim reaching only Run 96, an item (5) where that
    registration carries one, and a half that is on no roll; and it lacks
    the VARIABLE-CHECK line the unbroken one carries.

    THE HALVES ARE REAL TAGS since 2026-09-18, when the roll moved out of
    the notes into README's *Which two halves a pair has*: the check reads
    the CHAPTER's roll now, so a fixture naming `c` and `d` failed its own
    control for the tags rather than for what it was built to test. The
    broken half is a tag no roll carries, which is the finding.
    """
    write(os.path.join(_mkruns(tmp), 'run98.md'), '# Run 98\n')
    other = 'zzhalf' if broken else 'ghead'
    # The ENTRY POINT the executing session reads, tagged as run list step
    # 13 wants it and as pre-run 12c now requires: without it that step
    # falls back to reading the note whole, which both runs that met the
    # branch did, at eight hundred and 745 lines.
    entry = ('' if broken else
             'ENTRY POINT FOR THE SESSION THAT RUNS THIS [EXEC]: pre-run'
             ' is spent; the gate at 14 is owed.\n\n')
    return write(os.path.join(tmp, 'run99-pair.txt'),
                 'The pair run99-exit and run99-%s, Run 99s, written by'
                 ' hand 2026-01-01\n\n'
                 % other
                 + entry +
                 'HALVES: basis=exit other=%s\n%s\n'
                 'NAMING THE HALVES [SAME]: the roll is the chapter\'s.\n\n'
                 'THE COUNTS [SAME]: run-status.sh holds this run to 22'
                 ' counts files,\nas it held Runs 20 to %d.\n\n'
                 'WHAT THE PAIR PRICES [PAIRS]: what item (%d) asks.\n'
                 % (other, '' if broken else 'VARIABLE-CHECK: %s\n' % vc,
                    96 if broken else 98, 5 if broken else 1))


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
    # THE CHECKER'S OWN EXEMPTION, and this fixture has to share it or the
    # two disagree about which names count: a repetition names its
    # predecessor's half ON PURPOSE, and check_run_doc lets a token pass
    # when `byte for byte` follows within eighty characters. Run 30's
    # Results names run29-nospec that way, which built this plant a second
    # run and failed it at `names 2 run(s)`.
    runs = {m.group(1) for m in re.finditer(r'(?<![\w-])run(\d+)-[a-z0-9]+', seg)
            if 'byte for byte' not in seg[m.end():m.end() + 80]}
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
    the floor pair and the carry-back figure are cross-site agreement and can
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
    at = [i for i, x in enumerate(paras) if x.startswith('**`bcast` ')]
    assert len(at) == 1, 'bcast lead: %d paragraph(s)' % len(at)
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
    That is the DELETION decay, answered by re-aiming. The half named
    `spot` inside `dead-spot`, `spot-check`,
    `hotspot` and `spotless` is the point of the block: a rename bounded
    by `\\b` renames the FORM the pair varies, `-` being a word boundary.
    """
    return {'note': write(os.path.join(tmp, 'run23-pair.txt'), STUB_NOTE)}


STUB_NOTE_MACHINE_CHECK = """\
hdr

A [SAME]: g912 leads, spot follows; run23-g912 and run23-spot.
HALVES: basis=g912 other=spot

Verified when built, 2026-09-01:
  md5 g912         deadbeef, a BUILD line and owed

THE MACHINE CHECK IS A SEPARATE ANSWER AND IT FIRED: `list`'s net against
the fingerprint run22.md keeps reads a geomean of -3.66% over 19 of 19
shapes.
"""


def stub_pair_note_machine_check(tmp):
    """A note whose machine check sits where a real one does, under the fills.

    THE ORDER IS THE CASE. `run-gate.sh --machine`'s answer is written
    below the fill-in block, and a block classification is sticky, so an
    unnamed lead there inherits `fill` and reaches `_fill_skeleton`, which
    passes a paragraph carrying no rows through unchanged. Put the same
    block after a `GATE:` one and it inherits `gate` and is dropped whether
    or not its lead is named -- which is why this is a note of its own and
    not STUB_NOTE with a block appended.
    """
    return {'note': write(os.path.join(tmp, 'run23-pair.txt'),
                          STUB_NOTE_MACHINE_CHECK)}


STUB_NOTE_NAMED_FILLS = """\
hdr

A [SAME]: g912 leads, spot follows; run23-g912 and run23-spot.
HALVES: basis=g912 other=spot

Verified when built, 2026-09-01:
  md5 g912         deadbeef, a BUILD line and owed

NAMED FILLS, post-run step 0, 2026-09-02, off the binaries that were timed,
by `./loop-offsets.py run23-HALF --match` with both twins:
  g912   326 self-loops of at most 64 B in _Main_ code, 24 straddling.
"""


def stub_pair_note_named_fills(tmp):
    """A note whose post-run named fills sit where Run 40's did, under the
    fills -- the machine check's place, and dropped for its reason."""
    return {'note': write(os.path.join(tmp, 'run23-pair.txt'),
                          STUB_NOTE_NAMED_FILLS)}



def counts_leg(tmp, run, half, pop=None, elapsed=80, ended=True):
    """One `run-counts.sh` leg as a file: its header, one row, its stamp.

    Three lines rather than a captured sweep, because what the totals mode
    reads is the header and the `# end` line and nothing between them --
    a fixture carrying a real sweep's thousand rows would assert the same
    thing and hide which two lines the claim rests on.
    """
    name = '%s-counts-%s%s.txt' % (run, half, '-%s' % pop if pop else '')
    path = os.path.join(tmp, name)
    with open(path, 'w') as fh:
        fh.write('# %s-%s deadbeef N=50 2026-01-01T00:00:00+00:00 full%s\n'
                 % (run, half, ' class=%s' % pop if pop else ''))
        fh.write('# shape arm N instructions/iter\n')
        fh.write('a-shape an-arm 50 1000\n')
        if ended:
            fh.write('# end 2026-01-01T00:01:20+00:00 elapsed=%ds\n' % elapsed)
    return path


def synth_json(tmp, pop='main', name=None, **kw):
    """One population as a file: `main`, or a class by name."""
    shapes = main_shapes() if pop == 'main' else class_shapes(pop)
    return synth_run(os.path.join(tmp, name or '%s.json' % pop), shapes, **kw)


def plant_alloc_skewed_pair(tmp):
    """Two halves alike but for what ONE arm allocates.

    Named rather than inlined because the mutant of the per-arm allocation
    reading plants it too, and a mutant's judge cannot go through
    defect-run.py: that would run the tree's reader where the point is to
    run the mutated copy. One builder, two readers of it.
    """
    return {'run': synth_json(tmp, 'main', name='a.json'),
            'other': synth_json(tmp, 'main', name='b.json',
                                alloc_skew=[(sh, 'bq-expand', 0.8)
                                            for sh in main_shapes()])}


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


def consumer_arms():
    """The timed arms with no corrected time that are not controls.

    Which is the reducing consumers, read through the reader's own two
    predicates rather than by suffix here: the point of the pair is that
    `no_net` and `is_control` stopped being the same set on 2026-09-10,
    and a fixture spelling either out by hand is the drift that split
    them in the first place. AN EMPTY LIST WOULD MAKE THE FINGERPRINT
    CONTROL VACUOUS, its `hasnt` being built from this and evaluated at
    import. What answers for that is the other case, whose `[0]` sits in
    a plant lambda and so raises when the FIXTURE IS BUILT, reported as
    `FIXTURE DID NOT BUILD ... nothing was tried, so this is no verdict`
    -- loud, but not the import-time guard this claimed until 2026-09-10.
    A roster with no reducing consumer wants both cases retired rather
    than caught.
    """
    m = _reader()
    roster = m.roster_of(open(os.path.join(HERE, 'Main.hs')).read())
    return [n for n, role, _fn in roster
            if role != 'Only' and m.no_net(n) and not m.is_control(n)]


def timed_arm_count():
    """How many arms `synth_run` puts in a synthetic run: the roster's timed
    ones, controls included, which is what a population line counts. Why a
    case derives it rather than writing it out is `compared_arm_count`'s
    docstring; the two `pin-*` cases below pinned 24 and went red the day
    `libunord-stage3` landed.
    """
    m = _reader()
    roster = m.roster_of(open(os.path.join(HERE, 'Main.hs')).read())
    return sum(1 for _n, role, _fn in roster if role != 'Only')


def doc_expr(blocks):
    """A source expression for a document of `blocks`, newline-free.

    A `\\n` written into a case's argv passes through this file's own
    parse and arrives as a real newline inside the string literal the
    expression is built from, which is a syntax error rather than a
    failing case. Joining with chr(10) keeps every escape out of it.
    """
    sep = "+chr(10)+chr(10)+"
    return '(' + sep.join(repr(b) for b in blocks) + ')'


def synth_counts(tmp, name, ratio=1.0, refuse=(), extra_arms=(), n=50,
                 cheap_sum_only=False, shapes=None):
    """One half's `run-counts.sh` artifact, derived as `synth_run` is.

    The arms come from Main.hs's roster through the reader's own parser and
    the shapes from `main_shapes`, so a roster change moves this fixture
    with the run beside it rather than leaving a literal to rot. `ratio`
    scales every count, which is what a compiler emitting different code
    looks like to `perf`; `refuse` names `(shape, arm)` cells it could not
    count, written as the `!!` line the real artifact writes; `extra_arms`
    names arms the counts hold and no run times, which is the narrowing
    this file exists over.

    `cheap_sum_only` gives the two `sum-only` arms a count BELOW every
    other, which is what the real artifact holds -- the forcing pass is
    the cheapest bench there is. The default leaves them where sorting
    puts them, near the end and so among the dearest, which no cross-half
    case can tell apart because it subtracts nothing; a WITHIN-half
    reading corrects against them and sinks every cell on the default
    fixture. Added 2026-09-05 with `--counts --pair`, whose first case
    exited 2 on it and whose sibling below now plants that on purpose.
    """
    m = _reader()
    main_hs = os.path.join(HERE, 'Main.hs')
    roster = m.roster_of(open(main_hs).read())
    arms = [a for a, role, _ in roster if role != 'Only'] + list(extra_arms)
    shapes = main_shapes() if shapes is None else shapes
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
                if cheap_sum_only and arm.startswith('sum-only'):
                    base = 1000 + 7 * len(sh)
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


def rundoc_without_a_per_shape_line(tmp):
    """The run's own file with its first class block's per-shape
    paragraph removed, which is what the ADDED branch repairs."""
    paras = rundoc_text().split('\n\n')
    gone = next(p for p in paras
                if p.lstrip().lstrip('*').startswith('Per shape'))
    return edited_rundoc(tmp, ('\n\n' + gone, ''))


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


def rundoc_with_unwritten_class_says(tmp):
    """The run file with every class block's `What the class says:`
    paragraph a skeleton still carrying its `___`, as install-tables.sh
    writes one: the state in which the install owes it afresh."""
    paras = rundoc_text().split('\n\n')
    n = 0
    for i, p in enumerate(paras):
        if p.lstrip().lstrip('*').startswith('What the class says:'):
            paras[i] = '**What the class says:** ___ a skeleton left unfilled.'
            n += 1
    if not n:
        raise AssertionError('no `What the class says:` paragraph in the run'
                             ' file')
    return write_rundoc(tmp, '\n\n'.join(paras))


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


def corpus_with_a_class_run(tmp):
    """Two built main runs behind a class run that sorts first, for a
    limit that must count runs opened and not main tables read back."""
    d = corpus_of_two(tmp)['corpus']
    synth_json(d, 'flip', name='0-flip.json')
    return {'corpus': d}


def floor_legs(tmp):
    """A paired class leg beside an alone leg, as view-floor.py globs
    them: `zzvf-<half>-flip.json` twice and one `zzvf-al-<half>-<shape>-r1`
    holding a single arm, which is no class and carries no A/A group."""
    d = os.path.join(tmp, 'legs')
    os.mkdir(d)
    for half in ('ghead', 'g912'):
        synth_json(d, 'flip', name='zzvf-%s-flip.json' % half)
    write(os.path.join(d, 'zzvf-al-ghead-cnn-r1.json'), json.dumps(
        [['criterion'], [], [{'reportName': 'cnn/list', 'reportAnalysis': {
            'anRegress': [{'regCoeffs': {'iters': {'estPoint': 1.0}}}]}}]]))
    return d


def reroll_legs(tmp, ratio):
    """One leg of one view, as probe-flip-reroll writes them: an arm and
    its A/A copy `ratio` apart, over a sum-only floor of nothing."""
    d = os.path.join(tmp, 'legs')
    os.mkdir(d)
    reps = [{'reportName': 'v/%s' % arm, 'reportAnalysis': {
        'anRegress': [{'regCoeffs': {'iters': {'estPoint': x}}}]}}
        for arm, x in (('x', 1.0), ('x-aa', ratio),
                       ('sum-only-early', 0.0), ('sum-only-late', 0.0))]
    write(os.path.join(d, 'leg1.json'), json.dumps([['criterion'], [], reps]))
    return d


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

G3_RECIPES = """
HOW EACH HALF IS BUILT, in the note's own form:

  zzg3-lookrts   cd here, then
                        LOOP_A=1 LOOP_B=1 \\
                        cabal build micro \\
                          --project-file=cabal.project.x \\
                          --builddir=db-a \\
                          --ghc-options="-fobject-determinism" \\
                          --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
                      then
                        cp it

  zzg3-a1g       the same source, then
                        LOOP_A=1 LOOP_B=1 \\
                        cabal build micro \\
                          --project-file=cabal.project.x \\
                          --builddir=db-b \\
                          --ghc-options="-fspec-constr \\
                                         -fobject-determinism" \\
                          --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
                      then
                        cp it
"""

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
def counts_attempt(run, clean=()):
    """An earlier call of run-counts-all.sh as its status lines read: every
    population of the stand-ins swept, the labels in `clean` at rc=0 and
    the rest refused, and its closing tally."""
    at = '=== 2026-09-03T13:20:00+02:00 '
    lines = [at + 'counted work begins for %s: basis lookrts, control a1g'
             % run]
    n = 0
    for pop in ('main', 'rev', 'other'):
        for h in ('a1g', 'lookrts'):
            lab = 'counts %s %s' % (h, pop)
            lines.append(at + lab + ': start')
            if lab in clean:
                lines.append(at + lab + ': done, rc=0')
            else:
                lines.append(at + "%s: done, rc=2 -- COMPLAINT, read"
                             " %s-evening-out.txt under '##### %s'"
                             % (lab, run, lab))
                n += 1
    lines.append(at + 'EVENING COMPLETE WITH %d COMPLAINT(S) OVER BOTH CALLS'
                 ' -- read each in %s-evening-out.txt before any figure'
                 % (n, run))
    return '\n'.join(lines) + '\n'


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


# A perf whose cycles bend at the third process, as a mode drawn per
# process bends them: every event in `-e` answered, instructions
# proportional to `-n`, cycles proportional to it up to `-n 2` and 150000
# over at `-n 3`, so a cell read at N=1 differences to 200000 on
# `(2N - N)` and 350000 on `(3N - 2N)`.
PERF_MODES = """\
#!/bin/sh
out=""; n=2; want_o=0; want_n=0; want_e=0; ev=instructions:u
for a in "$@"; do
  if [ "$want_o" = 1 ]; then out=$a; want_o=0; continue; fi
  if [ "$want_n" = 1 ]; then n=$a; want_n=0; continue; fi
  if [ "$want_e" = 1 ]; then ev=$a; want_e=0; continue; fi
  case $a in -o) want_o=1 ;; -n) want_n=1 ;; -e) want_e=1 ;; esac
done
lines=""
for e in $(echo "$ev" | tr ',' ' '); do
  case $e in
    cycles:u) v=$((200000 * n)); [ "$n" = 3 ] && v=$((v + 150000)) ;;
    *) v=$((100000 * n)) ;;
  esac
  lines="$lines$v,,$e,257660,100.00,,
"
done
if [ -n "$out" ]; then printf '%s' "$lines" > "$out"
else printf '%s' "$lines" >&2; fi
exit 0
"""


# The same stand-in with the third process refused: `-n 3` reads
# `<not counted>`, as a perf hiccup on that one process would.
PERF_THIRD_REFUSED = PERF_MODES.replace(
    '  lines="$lines$v,,$e,257660,100.00,,',
    '  [ "$n" = 3 ] && v="<not counted>"\n'
    '  lines="$lines$v,,$e,257660,100.00,,')
assert PERF_THIRD_REFUSED.count('not counted') == 1, 'the refusal went astray'

# Linear to within 0.02 percent on cycles, and on the integer slopes 49 then
# 50, which part by 2 percent: at N=100 the three processes read 1000000,
# 1004999 and 1009999 cycles, raw slopes of 4999 and 5000.
PERF_TRUNCATED = """\
#!/bin/sh
out=""; n=200; want_o=0; want_n=0; want_e=0; ev=instructions:u
for a in "$@"; do
  if [ "$want_o" = 1 ]; then out=$a; want_o=0; continue; fi
  if [ "$want_n" = 1 ]; then n=$a; want_n=0; continue; fi
  if [ "$want_e" = 1 ]; then ev=$a; want_e=0; continue; fi
  case $a in -o) want_o=1 ;; -n) want_n=1 ;; -e) want_e=1 ;; esac
done
lines=""
for e in $(echo "$ev" | tr ',' ' '); do
  case $e in
    cycles:u) case $n in 100) v=1000000 ;; 200) v=1004999 ;; *) v=1009999 ;;
              esac ;;
    *) v=$((1000 * n)) ;;
  esac
  lines="$lines$v,,$e,257660,100.00,,
"
done
if [ -n "$out" ]; then printf '%s' "$lines" > "$out"
else printf '%s' "$lines" >&2; fi
exit 0
"""

# A stall sweep of two shapes whose first carries a `# NONLINEAR` mark on
# one of the two arms, as probe-stalls.sh writes one.
STALLS_MARKED = """\
# ./zz 0 N=1 2026-09-25T00:00:00+02:00 ARMS=A B
# shape arm N instructions:u cycles:u stalled-cycles-frontend:u \
branch-misses:u cache-misses:u
s1 A 1 2000 3000 300 20 10
# NONLINEAR s1 A: cycles:u 3000 then 4500
s1 B 1 2000 2500 250 20 10
s1 sum-only-early 1 1000 1000 100 10 5
s2 A 1 2000 3000 300 20 10
s2 B 1 2000 2500 250 20 10
s2 sum-only-early 1 1000 1000 100 10 5
"""


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


WILD_LOUD_LOG = """\
@@wild shp/arm pre iters=1 alloc=1 mut=1000000000 gc=0 gcs=1/0 inuse=1 load=0.1 run=100 cpu=1000
@@wild shp/arm post iters=1 alloc=2 mut=2000000000 gc=0 gcs=1/0 inuse=1 load=0.1 run=101 cpu=1200
@@wild other/arm pre iters=1 alloc=1 mut=1000000000 gc=0 gcs=1/0 inuse=1 load=0.1 run=200 cpu=2000
@@wild other/arm post iters=1 alloc=2 mut=2000000000 gc=0 gcs=1/0 inuse=1 load=0.1 run=201 cpu=2100
"""
"""One bench with a second of foreign CPU beside it and one without.

The first trips the 0.25-of-a-core bar the reader calls an INTRUSION and
the second does not, so the remedy printed under the verdict names one
shape and not both -- which is the whole of what a session has to type
where post-run step 3's rerun is not taken.
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

# A head whose every spot a conditional jump crosses: two `jmp *(%rbp)`
# spots between `.Lfar` and `.Lin`, each followed by a `jl .Lfar` that a
# pad at the spot lengthens from rel8 to rel32, the far label being just
# over a hundred bytes up. `.Lprev` keeps the text's start out of the
# group's spots. What the settled plan does here is what Run 38's
# control half needed at `.LQeN1`.
ASM_CROSSED_SPOTS = """\
\t.text
.Lprev:
\tmovq %rax, %rcx
\tcmpq %rax, %rsi
\tjl .Lprev
.Lfar:
""" + '\tmovq %rax, %rcx\n' * 34 + """\
\tjmp *(%rbp)
\tmovq %rax, %rcx
\tjl .Lfar
\tjmp *(%rbp)
\tmovq %rax, %rdx
\tjl .Lfar
.Lin:
""" + '\tmovq %rax, %rcx\n' * 19 + """\
\tcmpq %rax, %rsi
\tjl .Lin
\tret
"""


def asm_fallthrough(tmp):
    return asm(tmp, ASM_HEAD_AFTER_FALLTHROUGH)


def asm_table(tmp):
    return asm(tmp, ASM_HEAD_BEHIND_TABLE)


def asm_pair(tmp):
    return asm(tmp, ASM_ROTATED_PAIR)


def asm_crossed(tmp):
    return asm(tmp, ASM_CROSSED_SPOTS)


# The two costs of 2026-09-15, each with its answer worked by hand. The
# fill's shape, as Run 32's HEAD half laid it: a 9 B preamble (3, 3, 3)
# ending in the dead spot, a body of 51 B (42 + 4 + 3 + 2) whose exit
# `cmp; jge` (3 + 2) makes a 56 B span, and the outer loop 42 B on with a
# 55 B cycle. The body fits a line for the pad point at 0..13 and the
# exit span at 0..8, so the plain cost pads for 14..63, a budget of 50,
# and leaves the head at 9 with the exit astride; the exit-span cost pads
# for 9..63, a budget of 55, which fires at 9. A cut the entry count
# keeps: a 20 B preamble (17 + 3), a body of 8 movs, a cmp and a jl (29 B,
# 10 instructions, two entries) and an exit of 8 movs and a jmp (26 B, 9
# instructions, two entries). The exit span is 55 B and crosses for
# 10..63, a budget of 54, fired at 20; the entry count charges nothing
# until the body itself is cut, at 36..61, a budget of 28, not fired at
# 20, so the head stays where the sweep's smaller-piece rule would price
# it -- a control of the arithmetic and not of the machine. Under the
# block rules the same cut is free too, and the budget is worked from
# the rules' costly residues: the exit's jmp alone in its block at 10 to
# 13, the cmp+jl pair astride the boundary at 36 to 39 and a short last
# block at 40 to 45, the head in the line's last eight bytes at 56 to
# 63, none at 20. The jmp spot's budget would be 54, the text spot's,
# 20 bytes earlier, 48, and the planner takes the smaller: a directive
# after `.text` that fires as no bytes at residue 0, nothing after the
# jmp, and the head left at 20 where the exit span moves it to 0.
ASM_EXIT_ASTRIDE = """\
\t.text
.Lstart:
\tmovq\t%rdi, %rax
\tmovq\t%rsi, %rbx
\tjmp\t*(%rbp)
.Lin:
\t.skip\t42, 0x90
.Lout:
\tleaq\t1(%rsi), %r11
\tcmpq\t%rax, %r11
\tjl\t.Lin
\tcmpq\t%rax, %rsi
\tjge\t.Ldone
\t.skip\t17, 0x90
.Ldone:
\t.skip\t22, 0x90
\tjmp\t.Lout
"""

ASM_ENTRIES_CUT = """\
\t.text
.Lstart:
\t.skip\t17, 0x90
\tjmp\t*(%rbp)
.Lin:
""" + '\tmovq\t%rax, %rcx\n' * 8 + """\
\tcmpq\t%rax, %rsi
\tjl\t.Lin
""" + '\tmovq\t%rax, %rdx\n' * 8 + """\
\tjmp\t.Ldone
\t.skip\t9, 0x90
.Ldone:
\tret
"""


def asm_exit(tmp):
    return asm(tmp, ASM_EXIT_ASTRIDE)


# A loop whose back edge is an unconditional jmp, followed by a dead block
# of 9 bytes (3 + 3 + 3 -- movq, movq, `jmp *(%rbp)`) up to that block's
# own jump: the 8 B preamble (5 + 3) ends in the dead spot, the body is
# 26 B (8 movq of 3 and a 2-byte jmp). Read past the jmp, the exit span
# is 35 B and costly from residue 30, a budget of 34, which the shim as
# committed before the fix emits; with no exit after an unconditional
# back edge the body alone counts, costly from 39, a budget of 25.
# Worked by hand, the old budget first guessed at 35 for a 4-byte jmp
# and corrected by running the old shim, 2026-09-15.
ASM_JMP_BACK_EDGE = """\
\t.text
.Lstart:
\tmovq\t$1, %rax
\tjmp\t*(%rbp)
.Lin:
""" + '\tmovq\t%rax, %rcx\n' * 8 + """\
\tjmp\t.Lin
.Ldead:
\tmovq\t%rax, %rdx
\tmovq\t%rax, %rsi
\tjmp\t*(%rbp)
"""


def asm_jmp_back(tmp):
    return asm(tmp, ASM_JMP_BACK_EDGE)


def asm_entries(tmp):
    return asm(tmp, ASM_ENTRIES_CUT)


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
    # ALL of it by default: a table is written over the whole population,
    # so a fixture short of it installs a table no checker reads as the
    # run's, for a reason the case is not about. `n` is for the cases that
    # only need a couple of shapes and would rather build less.
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


def a_reducing_consumer():
    """One arm the correction leaves with no corrected time, off the roster.

    `no_net` is the predicate and the `-sum` suffix is how Main.hs spells
    it, so the first such arm is TAKEN rather than named: an arm named here
    is an arm a parking can retire, and the case below wants only that its
    cells have no net to divide.
    """
    roster = _reader().roster_of(open(os.path.join(HERE, 'Main.hs')).read())
    return next(n for n, _role, _fn in roster if n.endswith('-sum'))


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


def class_counts(prefix, cls):
    """One class's count sweeps on both halves, as `extra` entries, the
    halves' counts parting by a tenth so a counts-against-clock clause has
    a rate to compute (the counts clause's case, 2026-09-23)."""
    tmp = tempfile.mkdtemp(prefix='zz-synth-')
    try:
        return [('%s-counts-%s-%s.txt' % (prefix, half, cls),
                 open(synth_counts(tmp, half, ratio=r, cheap_sum_only=True,
                                   shapes=class_shapes(cls))).read())
                for half, r in (('lookrts', 1.1), ('a1g', 1.0))]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def readings_run(prefix, complete, compare=None):
    """A paired run's main set and one class on both halves, with its
    note, as `extra` for a shadow -- and, where `complete`, its counts
    sweeps and an evening file ending EVENING COMPLETE, which is what
    post-run-readings.sh waits for before a count-dependent reading.
    `compare` names a COMPARE run on the note, and gives that run a note
    and a main set on both halves, its halves named apart from these.
    """
    def extra():
        out = list(whole_run(['lookrts', 'a1g'], prefix=prefix,
                             classes=class_names()[:1]))
        out.append(('%s-pair.txt' % prefix, NOTE_STUB + (
            'COMPARE: %s\n' % compare if compare else '')))
        if compare:
            out.append(('%s-pair.txt' % compare,
                        'a stand-in pair note.\n'
                        'HALVES: basis=nospec other=ghead\n'))
            out += [('%s-%s-main.json' % (compare, h),
                     synth_text(main_shapes(), samples=2))
                    for h in ('nospec', 'ghead')]
        if complete:
            tmp = tempfile.mkdtemp(prefix='zz-synth-')
            try:
                for half in ('lookrts', 'a1g'):
                    p = synth_counts(tmp, half, cheap_sum_only=True)
                    out.append(('%s-counts-%s.txt' % (prefix, half),
                                open(p).read()))
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            out.append(('%s-evening.txt' % prefix,
                        '=== 2026-01-01T00:00:00+00:00 EVENING COMPLETE:'
                        ' every stage of both calls exited 0\n'))
        return out
    return extra


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
              slow=1.0, drop_arms=(), fingerprint=None, alloc_skew=()):
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
            # ALLOCATION IS THE ONLY AXIS A PAIR CAN MOVE WITHOUT MOVING
            # TIME, and until 2026-09-19 no fixture could: `skew` scales a
            # slope and every synthetic pair allocated identically, so the
            # per-arm reading `--alloc --per-shape` gives had nothing to
            # bite on. Two of `-O2`'s passes do exactly this on a live
            # pair, which is what the mode was written for.
            for sh_w, arm_w, f_w in alloc_skew:
                if sh_w == sh and arm_w == name:
                    alloc *= f_w
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
                  into=None, plateau=None, skew=(), states=None,
                  expect=None):
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

    `states` is the in-process state each of those processes asserts, one
    `inuse` value per process, and it is what the plateau gate reads since
    Run 29 -- the victim reading beside it being a reading and not the
    gate, since the victim is timed with `list` and a pair whose variable
    moves `list` moves it. Default: every process asserts the same state,
    which is what a sound run looks like however far its victims spread.

    `skew` is `synth_run`'s, applied to both class runs.

    `expect` writes a pair note carrying an `EXPECT:` line, which is how a
    run DECLARES that its own variable fires one of the plateau gates --
    the gate-verdict pattern, written by hand after the run and with its
    reason, so that a pair which can never assert one state does not leave
    post-run step 1 red for the whole of its life. It is a note and not a
    flag for that reason: a declaration somebody had to mean.
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
               ' vgg-14-c512-k3/list %s ms/iter over 20; inuse=%s keep=1')
        if states == 'omit':
            # A run whose logs predate the state fields, which is every
            # run up to Run 27: the gate falls back to the victim band.
            sat = ('@@saturate dose=1x by=list sprayed=1000000 in 6.0 s;'
                   ' victim vgg-14-c512-k3/list %s ms/iter over 20')
            st = [None] * len(plateau)
        else:
            st = list(states) if states is not None else [1] * len(plateau)
        for cls, ms, iu in zip(('rev', 'slice'), plateau, st):
            # A list is several lines in one log, which no process writes
            # and a count of lines against logs cannot tell from one each.
            lines = ([] if ms is None else ms if isinstance(ms, list)
                     else [ms])
            write(place('%s-lookrts-%s.log' % (tag, cls)),
                  'benchmarking x/y\n'
                  + ''.join((sat % m if iu is None else sat % (m, iu))
                            + '\n' for m in lines))
        # A rider's and a gate half's, at readings no band could hold: both
        # are excluded by name, so a gate that counted either would fail
        # loudly here instead of passing over a wider set.
        for other in ('al-lookrts-cnn-slice-c32-r1', 'gate-lookrts-a'):
            write(place('%s-%s.log' % (tag, other)),
                  (sat % '999.0' if states == 'omit'
                   else sat % ('999.0', 1)) + '\n')
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
    if expect:
        write(place('%s-pair.txt' % tag),
              'A pair note, enough of one for the declaration to be read.\n'
              '\nHALVES: basis=lookrts other=lookrts\n'
              'EXPECT: %s\n' % expect)
    write(place('%s-wallclock.log' % tag), '\n'.join(log) + '\n')
    return {'tag': tag}


def for_brief_note(tmp):
    """A run whose pair note WRAPS the rows --for-brief pastes.

    The real notes wrap, and two of the rows were read a line at a time:
    `.text` ended at `-- they do` with `NOT agree` on the next line, and
    `repetition` matched a prose sentence that opens with the word, above
    the entry of that name. Both are here, indented as the notes indent
    them -- the entries at two spaces, the prose deeper.
    """
    r = synthetic_run(tmp, expect='nothing')
    with open(here_file('%s-pair.txt' % r['tag']), 'a') as f:
        f.write('\n'
                '                repetition and the md5 row below is'
                ' one-sided: nothing may\n'
                '                be expected to reproduce.\n'
                '\n'
                '  md5           basis 0123456789abcdef0123456789abcdef\n'
                '  repetition       NOT OWED: the inputs moved under both'
                ' halves.\n'
                '  .text            111 bytes on basis, 222 on other --'
                ' they do\n'
                '                   NOT agree, the other half larger by'
                ' 111 bytes.\n')
    return r


def for_brief_readings(tmp):
    """A run in the shadow with the files post-run-readings.sh writes for
    --for-brief to fill its slots from: a cross-run comparison and its
    bridge, two --wild readings, four classes' A/A headers, three counts
    comparisons and two predictions sweeps, each in the reader's own words.
    """
    into = os.path.join(tmp, 'shadow')
    r = synthetic_run(tmp, into=into)
    d = os.path.join(into, 'log-read-%s' % r['tag'])
    os.mkdir(d)
    head = 'x.json: criterion 1.6.5.0, 10 reports = 5 benchmarks over %d shapes of the %s class\n'
    counts = ('counts geomean over the 16 arm(s) above, which are the arms'
              ' with a\ncorrected time: %s\n')
    files = {
        'main-lookrts-vs-compare.txt':
            'x.json: criterion 1.6.5.0\n\n\nthis run / zzprev-nospec-main.json,'
            ' per arm, over 3 shared shape(s)\n\narm   ratio    recip   faster'
            '      range\nlib-stage2-lean  0.9952   1.0048    2/3  0.9..1.0\n'
            'list  1.0002   0.9998    1/3  0.9..1.0\n'
            'bq-expand  1.0128   0.9874    1/3  0.9..1.0\n\n'
            # The reducing consumers' own table follows, raw, under a
            # header of the same shape: Run 34's span read both as one.
            'reducing consumers, 1 arm(s), on RAW `slope`\n'
            'arm   ratio    recip   faster      range\n'
            'liblist-stage2-sum  0.9000   1.1111    3/3  0.9..1.0\n',
        'main-lookrts-bridge.txt':
            'geomean over the 2 arm(s) 1.0030; 0 outside the 3.3% drift band\n',
        'wild-runzz-lookrts-rev.txt':
            'NO bench reaches 0.25 foreign: nothing else was running on this'
            ' machine\n',
        'wild-runzz-wallclock.txt':
            'runzz-wallclock.log: no paired `@@wild` samples here.\n',
        # A warning ahead of the header, as stderr lands before a buffered
        # stdout: Run 34's `runs` read that way and was left out.
        'runs-lookrts-aa.txt':
            'warning: 1 cell(s) with R2 < 0.99\n' + head % (17, 'runs'),
        'window-lookrts-aa.txt': head % (8, 'window'),
        'bcast-lookrts-aa.txt': head % (6, 'bcast'),
        'flip-lookrts-aa.txt': head % (6, 'flip'),
        'main-counts-cmp.txt': counts % '1.0053',
        'window-counts-cmp.txt': counts % '0.9989',
        'runs-counts-cmp.txt': counts % '1.0098',
        'main-lookrts-pred.txt':
            '5 span(s): 1 HELD, 3 KILLED, 0 not read, 1 out of scope;'
            ' item(s) with no span, yours to adjudicate: (4)\n',
        'main-a1g-pred.txt':
            '5 span(s): 4 HELD, 0 KILLED, 0 not read, 1 out of scope;'
            ' every item carries a span or a script\n',
    }
    for name, text in files.items():
        write(os.path.join(d, name), text)
    return r


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
# derived two ways at two sites (`ragged-gate-after-exclude`,
# `alloc-ceiling-over-the-named-cells`,
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
    'evening-14a-stamp-does-not-say-when': dict(
        family='false-comment', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='every run whose gate is not inherited, which is every pair'
                ' built anew',
        ok='the stamp handing 14a to a session names 19a as the moment,'
           ' which is where 14a and the run list both put it',
        bug='it said the verdict was yours with no when, two seconds before'
            ' the sequence line, and a session wrote it there',
        # No case: the stamp is reachable only where the gate RUNS AND
        # PASSES, and no stand-in here makes it pass -- which is why the one
        # control case, evening-chains-the-stages, inherits the gate
        # instead. A case was written and withdrawn rather than left to
        # assert the driver's source text, which expires the moment the code
        # under it moves.
        proved='ran',
        notes='Watched 2026-09-13 at Run 30, which read the gate verdict at'
              ' the stamp and ran run-status.sh 58 seconds into an'
              ' eight-hour sequence: run30-libcase-main carries two benches'
              ' of cnn-L1-6x6-c1 at 0.77 and 0.61 of a core, benches 11 and'
              ' 12 of 684. run30-evening.txt stamps the line at 02:05:16 and'
              ' the sequence at 02:05:18. The rule is in run list step 17'
              ' and the deferral in 14a and 19a; what the session read at'
              ' the moment it acted was this line, which carried neither.'),
    'predictions-name-the-main-set-an-item-reads-on': dict(
        family='two-spellings', discovery='audit', harm='latent',
        trigger='--predictions with --classes over a registration whose'
                ' item says `on the main set`, which every item of Run 30'
                ' and Run 31 does',
        ok='names the main set for that item, the run file being the'
           ' population the spans were read on whether or not its JSON'
           ' is among the class paths',
        bug='built the available names from the class paths alone, so'
            ' `main` was never among them and the item came back as'
            ' naming nothing, to be read by hand',
        proved='ran',
        notes='Found 2026-09-13 by running the block\'s first case against'
              ' the reader as committed, the block having landed the same'
              ' day with no case: `(2) main` was absent where `(1) runs`'
              ' was present.'),
    'agreeing-sweep-one-capture-row-with-alone-patterns': dict(
        family='scan-for-parse', discovery='review', harm='latent',
        trigger='an AGREEING row whose patterns capture one figure and'
                ' which carries alone-patterns; no row does today',
        ok='both the alone-disagreement message and the ok line take the'
           ' figure as a tuple of one, as the else branch already did',
        bug='`sites[0][0]` took the first CHARACTER of a one-capture'
            ' figure in the message, and the ok line\'s two-slot format'
            ' raised TypeError on a one-element tuple',
        # No case: the rows are a table in the checker's own source, and
        # a case would have to plant one there. The two branches were made
        # arity-aware beside the else branch, and the two-capture row that
        # does carry alone-patterns, the carry-back figure, prints the
        # same line before and after.
        proved='asserted',
        notes='Found 2026-09-13 by a blind reader of the range that added'
              ' the isinstance shim to two of the four sibling branches.'),
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
    'major-run-takes-the-populations-to-rerun': dict(
        family='guard-on-the-wrong-side', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='post-run step 3, which reruns the populations an intrusion'
                ' touched and says to drive it through this script',
        ok='runs the populations named, both halves, and refuses only over'
           ' what they would overwrite',
        bug='no way to name one, and a guard refusing over every artifact of'
            ' the run, so the step could not be carried out at all'),
    'move-registration-repoints-the-anchors-it-carries': dict(
        family='domain-unchecked', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='a registration whose text links a README section by bare'
                ' anchor, which is what writing it in the open list gives',
        ok='rewrites `](#` to `](../README.md#` as it moves the text',
        bug='moved the text a directory down with the anchors untouched, so'
            ' every such link arrived dead'),
    'predictions-skip-a-degenerate-pair': dict(
        family='guard-on-the-wrong-side', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='a registration span whose pair has a cell the forcing term'
                ' did not leave positive on the population read, as Run 27'
                ' item (6) has on the main set',
        ok='records that span NOT READ, with the sunk count and the first'
           ' cell, and adjudicates the rest',
        bug='exit 2 out of the middle of the walk, the eight later items'
            ' unadjudicated and stdout silent about which'),
    'cross-span-on-an-arm-with-no-corrected-time': dict(
        family='two-spellings', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='a registration writing a `cross` span over a reducing'
                ' consumer, as Run 29 item (3) does over'
                ' `libunord-stage7-sum`',
        ok='reads it on `pair`\'s key, slope for a `no_net` arm, over the'
           ' whole population, and refuses a cell with no positive value'
           ' there',
        bug='divided net and dropped every shape whose net was not'
            ' positive, reading 0.5854 over 3 shapes of 14 on Run 29 `runs`'
            ' where the raw ratio over all 14 is 0.9779, and NOT READ on'
            ' `block`, which reverses the item\'s verdict'),
    'replace-takes-an-abutting-table': dict(
        family='guard-on-the-wrong-side', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='an anchor naming a class block\'s bolded lead, which every'
                ' run file writes with its installed table on the next line'
                ' and no blank between them',
        ok='refuses, naming the table\'s line count, and writes nothing',
        bug='replaced lead and table together at exit 0, taking the flip'
            ' class\'s 38 rows out of Run 29\'s file, with --check-doc'
            ' passing straight afterwards'),
    'status-reads-a-bare-item-header': dict(
        family='scan-for-parse', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='a carrier return whose headers are the bare `ITEM N` the'
                ' chapter asks for, as Run 27\'s was',
        ok='reads the four blocks present',
        bug='read all four absent, so post-run 4, 5 and 6a stood NOT DONE'
            ' with the file written and complete'),
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
    'properties-refuse-a-limit-that-is-not-a-count': dict(
        family='domain-unchecked', discovery='lint', harm='latent',
        trigger='CORPUS_LIMIT set to something that is not a whole number',
        ok='refused under main() at exit 2, naming the variable',
        bug='a traceback out of the import line'),
    'properties-refuse-a-negative-limit': dict(
        family='domain-unchecked', discovery='lint', harm='latent',
        trigger='CORPUS_LIMIT=-1',
        ok='refused under main() at exit 2, naming the variable',
        bug='every property swept nothing and blamed an empty corpus'),
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
    'draft-carries-the-gates-machine-check': dict(
        family='other:unnamed-block-inherits-its-neighbour',
        discovery='in-use', harm='fired', harm_count=1,
        trigger="a note whose machine-check block sits under the fill-in"
                ' block, which is where run-gate.sh leaves it',
        ok='dropped with the pair whose gate read it, the drafted note'
           ' carrying GATE: NOT RUN and no reading',
        bug="the previous run's box move carried into the next note, under"
            ' a lead beginning AND IT FIRED and above a gate reset to NOT'
            ' RUN',
        notes='Watched 2026-09-09 at Run 28\'s preparation, which drafted'
              " run28-pair.txt from run27-pair.txt and found Run 27's"
              ' -3.66% machine check in it. Nothing checks a pair note, so'
              " what caught it was the draft's own instruction to read"
              ' every carried line.'),
    'no-mode-read-a-carried-over-registration': dict(
        family=None, discovery='in-use', harm='fired', harm_count=1,
        trigger='a registration carried over from the previous run, which'
                ' is the ordinary case here',
        ok='--carry-over reads the previous OPEN entry out of git and'
           ' names the words that moved, item by item',
        bug='the comparison hand-rolled against the run file, whose copy'
            ' carries a verdict per item, so every item reads as changed',
        # No case: the fixture would want a git HISTORY with a registration
        # moved out of README, which no plant here builds. The splitter the
        # mode shares with registration_items IS covered, by
        # `predictions-enumerates-items-twice`; what is not is the history
        # walk, whose three wrong drafts are in the fix's commit message.
        proved='ran',
        notes='Watched 2026-09-13 at Run 30\'s preparation, which wrote a'
              ' difflib script against runs/run29.md and read all eleven'
              ' items as changed, the verdicts step 5 appends being the'
              ' whole of the difference. What it then did is worth the'
              ' record: it abandoned the diff and checked the carry-over a'
              ' THIRD way, off the phrases the previous run\'s VERDICT text'
              ' quotes -- *against a registered 0.5* and its like -- which'
              ' happens to be right and reads nothing of the registration'
              ' it claims to be checking. The chapter\'s own instruction'
              ' names this'
              ' shape: a computation a write-up hand-rolls is a defect'
              ' report against the reader.'),
    'carried-prints-every-derivation-not-a-shortlist': dict(
        family='false-comment', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='--carried over more than six populations, which is every'
                ' registration read on the classes',
        ok='the derivations nearest a quoted figure, the rest counted,'
           ' and --verbose for all of them',
        bug='the span derived on every population on one line, burying the'
            ' item it flags',
        notes='Watched 2026-09-13 at Run 30\'s preparation: four flagged'
              ' items, a derivation per population PER SPAN -- so twenty-two'
              ' on a one-span item and twice that on (6), which names two'
              ' arm pairs -- and 8922 bytes to say what 2878 says now. The README line the mode runs under'
              ' calls its output a shortlist to read, so this is the mode'
              ' disagreeing with its own documentation rather than with a'
              ' preference. Ordering by nearness was the other half: the'
              ' 0.7433 that sits beside a quoted 0.7425 now leads its'
              ' line instead of sitting eleventh in it.'),
    'draft-emits-a-handover-slot-per-block': dict(
        family='other:unnamed-block-inherits-its-neighbour',
        discovery='in-use', harm='fired', harm_count=1,
        trigger='a previous note whose handover runs to more than one'
                ' announced block, which every note here has',
        ok='one handover slot, as the gate gets one gate line',
        bug='the same slot and the same scaffolding emitted once per'
            ' block, and listed as many times under YOURS TO WRITE',
        notes='Watched 2026-09-12 at Run 30\'s preparation, whose draft'
              ' opened with three identical ENTRY POINT slots off a'
              ' run29-pair.txt carrying ONE such heading. `NOTE_HANDOVER`'
              ' has four leads, so a handover spanning an ENTRY POINT'
              ' paragraph and a WHAT THE PREPARATION LEARNED one announces'
              ' twice; the gate branch beside it had the dedup and this one'
              ' did not.'),
    'draft-s-yours-list-renames-only-the-run-number': dict(
        family='two-spellings', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='--draft where a block title names a half, on a run that'
                ' does not reuse the previous basis tag',
        ok='the YOURS list carries the same rename the body does',
        bug='a title naming a half this pair does not have, two lines'
            ' above the body heading that names the right one',
        notes='Watched 2026-09-12 at Run 30\'s preparation: the list said'
              ' `THE BASIS IS run30-spec` where the block below it said'
              ' `THE BASIS IS run30-nospec`, the list applying'
              ' `p.replace(prev, draft)` and the body the full map. It'
              ' reads as a well-formed title, which is why the body had to'
              ' be beside it for anyone to notice.'),
    # ---- preflight.sh ----
    'note-paths-read-a-name-that-merely-contains-the-run': dict(
        family='scan-for-parse', discovery='in-use', harm='fired',
        harm_count=1,
        trigger="a note naming a file whose name contains `$R-`, which the"
                ' roster pass writes',
        ok='the path is read whole, a leading boundary consumed and stripped',
        bug='its tail harvested as a path of its own and reported gone,'
            ' with the file present',
        proved='ran',
        notes='Watched 2026-09-10 on Run 28\'s note, which names'
              ' smoke-l1-run28-bcast.json and -flip.json: 10c FAILed on'
              ' run28-bcast.json and run28-flip.json, neither of which is a'
              ' file. The third boundary defect in that one regex; the two'
              ' before it are in the step\'s own comment.'),
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
    'fill-in-keys-the-previous-build-on-this-run-s-tag': dict(
        family='quiet-failure', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='a run whose basis TAG differs from the previous run\'s,'
                ' the recipe unchanged',
        ok='the fill-in block reads the previous run\'s basis half, asking'
           ' that run\'s own note where this run\'s tag does not name it',
        bug='the --delta row reports a binary that never existed as not'
            ' here, and the roster-delta membership lines print nothing',
        # No case, so no audit watches this; what watched it is the
        # preparation the two dark rows landed in. The clause below says so.
        proved='ran',
        notes='Watched 2026-09-11 at Run 29\'s preparation, which renamed'
              ' the basis g912 -> spec on an unchanged recipe:'
              ' log-preflight-r29.txt carries `run28-spec is not here` and'
              ' no `main set:` line at all, with run28-g912 in the'
              ' directory. One occurrence, that preparation, this being the'
              ' first rename since --fill-in was born 2026-09-07. Both'
              ' readings had been taken by hand at steps 2 and 6c, and the'
              ' fix reproduces them figure for figure.'),
    'step-8d-replays-the-whole-corpus': dict(
        family='two-spellings', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='every --corpus run since the step was written',
        ok='the cases of what changed since the last run, dated from the'
           ' previous run file being born',
        bug='the whole corpus replayed, minutes where the list budgets'
            ' seconds, with the step announcing that it did',
        # No case, for the reason checks.py's UNCOVERED gives preflight's
        # STEPS. The bug direction was WATCHED rather than replayed.
        proved='ran',
        notes='Watched 2026-09-13 at Run 30\'s preparation, which reported'
              ' the step still running three times before asking why: the'
              ' call was `defect-run.py .` where the list says'
              ' `--changed <last run\'s commit>`, as the list then spelled'
              ' it. Slower and not weaker, so'
              ' what it cost is a step nobody runs twice. MEASURED WITH THE'
              ' FIX: the changed set is 277 of 376 cases here, read-run.py'
              ' alone owning 222, so the saving appears only on a run that'
              ' leaves the reader alone -- kept anyway, the list being the'
              ' governing document.'),
    'step-9-asserts-specconstr-of-every-basis': dict(
        family='domain-unchecked', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='a pair whose BASIS half is built without `-fspec-constr`',
        ok='the regime expected is read off the basis half\'s own recipe'
           ' block in the note, and the binary held to that',
        bug='a FAIL saying the regime is NOT SpecConstr, on a binary built'
            ' exactly as its own recipe asks',
        # No case, for the reason checks.py's UNCOVERED gives preflight's
        # STEPS -- a case would run them twice -- and the bug direction was
        # WATCHED rather than replayed, as the two records above were.
        proved='ran',
        notes='Watched 2026-09-12 at Run 30\'s preparation, the first pair'
              ' here whose basis is unflagged: log-preflight-r30.txt carries'
              ' `9 FAIL regime is NOT SpecConstr: scan/mut 9.992 -- plain'
              ' -O1 is ~10`, which is the reading README gives for plain'
              ' -O1 and the one the pair was built for. The step asserted'
              ' half of a sentence its own comment states whole; harmless'
              ' from Run 8 to Run 29, every basis having carried the flag.'
              ' The derivation was proved non-vacuous by hand over the three'
              ' branches: run30-pair.txt gives o1, run29-pair.txt gives spec'
              ' and a note with no such block gives unknown.'),
    'step-9-derives-the-regime-from-a-flag-name-in-prose': dict(
        family='domain-unchecked', discovery='review', harm='latent',
        trigger='a pair whose recipe raises the LEVEL rather than naming'
                ' `-fspec-constr`, or whose recipe block says a flag name'
                ' in its prose',
        ok='the expected regime is read off the `--ghc-options` lines of'
           ' the basis half\'s recipe block, `-O2` asking for SpecConstr'
           ' as `-fspec-constr` does',
        bug='a recipe built at -O2 classed as plain -O1 and FAILed for'
            ' reading as SpecConstr; and a block whose PROSE names the'
            ' flag classed as flagged whatever its command passes',
        # No case, for the reason checks.py's UNCOVERED gives preflight's
        # STEPS -- a case would run them twice -- and the derivation was
        # proved by hand over five inputs instead.
        proved='ran',
        notes='Found 2026-09-13 at Run 31\'s preparation, reading the step'
              ' before its pair -- the first whose control half is built at'
              ' -O2, which turns SpecConstr on. The Run 30 repair above'
              ' read a FLAG NAME where the step\'s own comment names a'
              ' PASS, so the level reaches the same pass by another road'
              ' and was not recognised. The prose half is what the first'
              ' fix walked into: matching `-O2` over the whole block made'
              ' run30-pair.txt\'s control derive spec, its recipe block'
              ' saying `GHC enabling that pass at -O2 and not at -O1` of a'
              ' half built at plain -O1. Narrowed to the `--ghc-options`'
              ' lines and proved non-vacuous by hand over five inputs:'
              ' run31-pair.txt gives o1 for nospec and spec for o2,'
              ' run30-pair.txt gives o1 for BOTH halves, and a name with no'
              ' block gives unknown. The o2 reading is measured and not'
              ' argued -- `diag` on vgg-14-c512 reads scan/mut 9.992 on'
              ' run31-nospec and 1.000 on run31-o2.'),
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
                      bug='died with math domain error where other modes refuse'),
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
    'planned-straddles-are-heads-in-every-cost': dict(family='two-spellings', discovery='in-use', harm='fired',
                      harm_count=1,
                      trigger='ALIGN_AS_VERBOSE=1 with LOOP_BLOCKRULES=1 over a rotated pair',
                      ok='(1 planned) beside the 1 verified, a head count under every cost',
                      bug='(0 planned), the chosen cost truncated: cycles under the block rules, exit lines under the exit span'),
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
                      trigger='the carry-back figure, the six-pair figure until 2026-09-11, quoted differently at two sites',
                      ok='fails, carry-back figure is quoted differently',
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
    'half-name-carries-no-hyphen': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a HALVES line naming a half with a hyphen',
                      ok='refuses, naming the grammar',
                      bug='cut at the first hyphen and handed the truncation to every driver'),
    'note-blocks-resume-after-the-fill': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a gate verdict continuing BELOW the fill-in block',
                      ok='withheld with the rest of the gate',
                      bug="--draft carried the previous pair's gate into the next note"),
    'compare-reads-no-reducing-consumer': dict(family='other:silent-drop', discovery='review', harm='latent',
                      trigger='a `-sum` arm whose cross a registration quotes',
                      ok='a block of its own under the table, on raw slope',
                      bug='dropped, so the prior was re-derived by a hand-written geomean'),
    'section-splits-a-table-from-its-lead': dict(family='scan-for-parse', discovery='review', harm='latent',
                      trigger='a table sharing a paragraph with its introducing sentence',
                      ok='its own paragraph, so --with-tables N can name it',
                      bug='unselectable: the section offered one table where it carried two'),
    'note-check-reads-the-carried-blocks': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger="a note whose carried blocks still describe the previous pair",
                      ok='three kinds of stale statement named with their lines',
                      bug='nothing read the note as prose, 10c and 10d being structural'),
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
    # ---- what nothing read, and what nothing subtracted ----
    'registration-arm-is-not-timed': dict(family='vacuous-check', discovery='in-use', harm='fired', harm_count=1,
                      trigger='an OPEN registration naming an arm the roster parks',
                      ok='fails, names the arm and the registration',
                      bug='no check read a registration at all; Run 24 lost a clause of one to it'),
    'registration-defers-to-a-missing-task': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger="a registration deferring to a task number that is not there",
                      ok='fails, names the task number',
                      bug='the deferral resolved to nothing and every gate passed'),
    'gate-show-absorbs-a-third-argument': dict(family='silent-option', discovery='review', harm='latent',
                      trigger='a third word after --show',
                      ok='refuses, naming the count it got',
                      bug='absorbed without effect and without error, printing the selection at exit 0'),
    'gate-show-derives-the-selection': dict(family='two-spellings', discovery='in-use', harm='fired', harm_count=1,
                      trigger="the note's gate-arms line written beside a SEL that moved",
                      ok='the globs and the count come from the script that will run',
                      bug='SEL was read out of run-gate.sh by eye, or out of the previous note'),
    'coverage-check-sees-a-figure-on-a-wrapped-continuation': dict(family='scan-for-parse', discovery='review', harm='fired', harm_count=1,
                      trigger='a list item whose figure wrap80 puts on a continuation line',
                      ok='an indented line is code only inside a block a blank line opened',
                      bug="four spaces read as code, so the run chapter's two decimals went unseen and the chapter owed no bullet"),
    'coverage-check-sees-an-address-as-a-figure': dict(family='vacuous-check', discovery='review', harm='fired', harm_count=1,
                      trigger='a section whose only figures are hex addresses and mod-64 offsets',
                      ok='an address of three hex digits or more is a figure',
                      bug="the pinning claim's readings, a cross-run series in the run chapter, passed a check that exists to find them"),
    'survey-reads-a-saved-listing': dict(family=None, discovery='review', harm='latent',
                      trigger='a site of a binary that has since been deleted',
                      ok='a saved objdump listing is read as the binary it came from',
                      bug='objdump alone, so no case could hold a site of a run binary, which dies at the deletion offer as three JSON fixtures did once'),
    'survey-counts-a-data-word-as-a-loop': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=1, proved='ran',
                      notes='watched by hand on run25-g912 against its -g3 twin, 2026-09-04, before the fixture was cut from it',
                      trigger='an info-table word decoding as a backward branch whose span the bytes before it fill',
                      ok='a closing branch no straight-line flow from the head reaches is not a loop',
                      bug="run25-g912's survey read five straddlers where its twin and every other binary read four"),
    'survey-counts-a-swallowed-jump-as-a-loop': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=1, proved='ran',
                      notes='read on run26-g912 against its -g3 twin, 2026-09-06, after the write-up had counted it as a sixth straddler; the twin refused it by byte identity',
                      trigger='an info-table word throwing the sweep out of step through a continuation whose own jump displacement then decodes as a backward branch',
                      ok='a body with an undecodable instruction in it is not a loop, no code GHC emits decoding as (bad)',
                      bug="run26-g912's survey read six straddlers where its twin read five, the sixth a return-frame table and a continuation of $wfbCanonVecdims"),
    'survey-counts-no-exit-span': dict(family=None, discovery='in-use', harm='latent',
                      notes='the shim counts its own exit spans only under ALIGN_AS_VERBOSE, which no recipe sets, so Run 33 paid two throwaway rebuilds to read a line the binary carries',
                      trigger="a half built under LOOP_EXITSPAN=1, whose exit spans the shim says all fit, and a half built without it, whose 65 and 72 astride nothing had counted",
                      ok='the survey counts the exit spans astride beside the straddlers, as align-as.py defines the span',
                      bug='the survey counted bodies alone, so a switch that moves exits and not bodies left no reading in the binary'),
    'survey-counts-a-nop-pad-table-word-as-a-loop': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=1, proved='ran',
                      notes='read on run33-gheadexit against the shim\'s verified line, 2026-09-16: two exit spans astride against none, both this shape, and run32-ghead carries one',
                      trigger='a nopl pad after an unconditional jump, followed by an info-table word decoding as a short backward jcc to the pad',
                      ok='a body whose head is a nop is a pad and not a loop',
                      bug='the pad passed the flow test, the (bad) tell and the zero-run tell, and its six bytes cannot straddle, so only the exit-span count ever saw it'),
    'survey-counts-a-return-address-word-as-a-loop': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=1, proved='ran',
                      notes="read on run35-exit against the shim's verified line, 2026-09-18: nine straddling and one exit span astride against eight and none; run35-gheadexit carries a straddler of the shape and run30-libcase an exit span astride",
                      trigger="an info table's last zero byte read as the start of the continuation push after it, whose immediate's low bytes decode as a short backward jcc to that byte",
                      ok='a body carrying a stray REX prefix, rex.* in the mnemonic column, is the sweep out of step over code and not a loop',
                      bug='the body passed the flow test, the (bad) tell, the zero-run tell and the nop tell, and its seven bytes at offset 63 both straddle and put its exit span astride'),
    'survey-counts-a-table-word-pair-as-a-loop': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=1, proved='ran',
                      notes="read on run36-gheadnospec against the shim's verified line, 2026-09-18: one exit span astride against none, on a body of four bytes",
                      trigger='two zero bytes of an info table followed by a word whose low bytes decode as a short backward jcc to them',
                      ok='a body carrying an instruction of two zero bytes, add %al,(%rax), is a table and not a loop, no compiler emitting one',
                      bug='the zero-run tell asked four zero bytes and the body had two, so it passed every tell, and four bytes at offset 50 put its exit span astride'),
    'survey-counts-a-two-byte-pad-and-its-table-word-as-a-loop': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=1, proved='ran',
                      notes="read on run36-gheadtwopass against the shim's verified line, 2026-09-18: one exit span astride against none, the pad sitting after a jmp *0x0(%rbp) that nothing falls through",
                      trigger='a two-byte pad after an unconditional jump, followed by an info-table word decoding as a short backward jcc to the pad',
                      ok="a body whose head objdump spells nop, nopl, nopw or xchg %ax,%ax, behind any prefix, is a pad and not a loop",
                      bug="the pad tell read the mnemonic's spelling, nop, and objdump spells the two-byte pad xchg %ax,%ax, so the fifth site's shape passed it at two bytes"),
    'survey-drops-a-body-with-an-eight-byte-instruction': dict(family='scan-for-parse', discovery='review', harm='fired', harm_count=12, proved='ran',
                      notes="found by a census of the twelve run binaries on disk taken for the Run 36 phantoms, 2026-09-18: 27 to 113 Main loops a binary dropped, every one holding an instruction of eight bytes or more, the return-frame push among them",
                      trigger='a self-loop of at most a line holding an instruction of eight bytes or more, which objdump prints over two lines',
                      ok="the second line's bytes belong to the instruction, so the body's byte sum meets its span and the loop is counted",
                      bug='the second line was read as an instruction of its own when it held two bytes or more and not at all when it held one, so the body fell short of its span and scan dropped it as a jump into an instruction'),
    'survey-counts-a-branch-into-an-exit-block-as-a-loop': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=1, proved='ran',
                      notes="read on run36-gheadtwopass against the shim's verified line, 2026-09-19, after 2cbaeb6 let the survey see it: nine straddling against eight; the heap-check failure block is the same shape and every binary carries them",
                      trigger='a backward branch into a block that leaves the body by an unconditional transfer, the code after that block entered by a forward branch from outside',
                      ok="a body whose head does not reach its closing branch through the body's own edges, fall-through and the branches inside it, is no loop",
                      bug='the flow test resumed at any instruction some branch anywhere targets, so the forward branch into the check carried the flow to the back edge'),
    'delta-sees-a-group-that-grows-past-the-threshold': dict(family='quiet-failure', discovery='review', harm='fired', harm_count=1, proved='ran',
                      notes='watched on run24-g912 against run25-g912 at --len 0, 2026-09-04, at both thresholds',
                      trigger='a group under --min-copies in OLD and over it in NEW',
                      ok='either side meeting the threshold selects the group',
                      bug='the OLD side alone was tested and `k not in og` excluded the rest'),
    'delta-leaves-the-library-groups-to-library': dict(family='two-spellings', discovery='review', harm='fired', harm_count=2, proved='ran',
                      notes="watched on both halves of Run 25, 2026-09-04, the Quantile pair standing as a third group in --delta's report",
                      trigger="a linked library's loop group on both sides",
                      ok='the population is Main-compiled code, as --match and --survey take it',
                      bug='every group was read, so the statistics Quantile pair sat in the summary on both halves'),
    'delta-subtracts-two-builds': dict(family=None, discovery='in-use', harm='fired', harm_count=2,
                      trigger="two builds' tracked groups, on the pinning claim's own reading",
                      ok='offsets, surviving addresses and the displacement set, derived',
                      bug='two preparations subtracted the address lists by hand'),
    'roster-delta-reads-two-listings': dict(family=None, discovery='in-use', harm='fired', harm_count=1,
                      trigger='a roster change stated in three documents',
                      ok='arms, shapes, views and the survivors\' order, off the binaries',
                      bug="written from a diff nothing performed; Run 25's note miscounted the controls"),
    'fills-entry-region-goes-to-the-previous-proc': dict(family='scan-for-parse', discovery='in-use', harm='fired', harm_count=1,
                      trigger='an -fllvm function whose loop sits before its first `_blk_` label',
                      ok='the loop is listed under the worker whose function holds it',
                      bug='it was listed under the previous function\'s last block, so under the neighbouring arm, and under nothing for its own'),
    'smoke-warnings-kept-only-in-a-temp-dir': dict(family='quiet-failure', discovery='in-use', harm='fired', harm_count=1,
                      trigger='a sweep whose reader modes warn',
                      ok='the warnings are printed, deduped, beside the verdict',
                      bug='only the mode NAMES were printed, the findings left in a dir wiped with /tmp'),
    'net-correction-netted-a-reducing-consumer': dict(
        family='other:new-family-outside-a-name-keyed-predicate',
        discovery='in-use', harm='fired', harm_count=1,
        trigger='a `-sum` arm on a population where it beats the sum-only'
                ' control',
        ok='no correction, its spans read raw, and it stays a candidate',
        bug='the term subtracted anyway, so the cell went non-positive and'
            ' the row had no geomean at all'),
    'fingerprint-names-an-arm-with-no-corrected-time': dict(
        family='two-spellings', discovery='review', harm='latent',
        trigger='an arm `no_net` covers and `is_control` does not',
        ok='the kept per-shape table names only arms the time column reads'),
    'draft-carries-a-block-naming-another-run-unmarked': dict(
        family='two-spellings', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='a [SAME] block quoting a run older than the one renamed',
        ok='the draft heads the note with the blocks to check, and names'
           ' which run each points at'),
    'note-figures-reads-a-row-only-as-present': dict(
        family='vacuous-check', discovery='review', harm='latent',
        trigger='a figure that has slid onto a neighbouring fill-in row',
        ok='held to the row of its own label, and named with both readings'),
    'roster-pass-prints-a-failing-mode-as-rc-0': dict(
        family='other:status-read-after-its-own-negation',
        discovery='in-use', harm='fired', harm_count=1,
        trigger='any required reader mode exiting non-zero on a leg',
        ok='the status is taken before the `if`, so the line names it',
        bug='`(rc=0)` beside every failing mode, `$?` in the body of `if !`'
            ' being the negation\'s status',
        proved='ran',
        notes='Watched 2026-09-10 on Run 28\'s roster pass, which printed'
              ' `--selftest(rc=0)` for the bcast and flip legs where the'
              ' mode had exited 1. The verdict was never wrong -- `failed`'
              ' is set on the same condition and the pass counted both'
              ' findings -- but a reader who trusts the printed status'
              ' reads a pass. The shell semantics were confirmed'
              ' directly: `bash -c \'if ! (exit 7); then echo $?; fi\''
              ' prints 0.'),
    'readings-rewrite-their-directory-whole': dict(
        family='unverified-state', discovery='review', harm='latent',
        trigger='log-read-RUN/ holding a vs-compare reading from an earlier'
                ' call, the note\'s COMPARE line since removed',
        ok='the directory is rewritten whole, the stale reading gone',
        bug='the stale reading stayed beside the fresh ones',
        notes='Found 2026-09-17 reading the script after its first call on'
              ' a real run, Run 34.'),
    # The review pass of 2026-09-18 over every script here.
    'status-counts-the-short-named-twins': dict(family='two-spellings', discovery='review', harm='fired',
                      trigger='run23, run24 or run25, whose twins are named -r<N>',
                      ok='step 0 reads done off the -r<N> twins',
                      bug='step 0 read NOT DONE for ever on three finished runs',
                      notes='Runs 24 and 25 read step 0 NOT DONE on 2026-09-18 with their twins on disk; run23, its twins gone, reads it by the absence branch either way.'),
    'view-floor-skips-the-legs-that-are-not-classes': dict(family='vacuous-check', discovery='review', harm='fired',
                      trigger='a run with alone legs or gate processes on disk',
                      ok='the alone, gate and main legs are passed over',
                      bug='each read as a class with no A/A group, raising the exit to 2',
                      notes='Run 32: 92 such lines before the per-class tables.'),
    'two-modes-at-once-off-the-roll-call': dict(family='silent-option', discovery='review', harm='latent',
                      trigger='--stale --lint, or any of the six beside a listed mode',
                      ok='refuses at exit 2, one mode at a time',
                      bug='ran the first and dropped the second without a word'),
    'properties-limit-counts-a-class-run-it-opened': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='CORPUS_LIMIT over a corpus holding a class run',
                      ok='the limit counts every run opened',
                      bug='a class run was opened uncounted, the limit bounding main tables'),
    'properties-help-before-the-corpus': dict(family='other:exit-at-import', discovery='review', harm='latent',
                      trigger='--help in a tree with no runs/run<N>.md',
                      ok='the help text, at exit 0',
                      bug='BLOCKED at exit 2 before main() read the flag'),
    'install-says-the-file-stands-on-a-refusal': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a refusal on any class after the first',
                      ok='says nothing was written; ADDED lines print after the write',
                      bug='an ADDED line stood on the screen over an unchanged file'),
    'counts-did-not-run-is-exit-2': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='no perf, a blocked counter, no temp path, no binary, an output already there, no roster',
                      ok='exit 2, as the usage guard and the sibling probes say did-not-run',
                      bug='exit 1, the code of a sweep that ran and came out wrong'),
    'attr-reader-binds-lib-stage1-to-the-leaf': dict(family='other:binding-outlived-the-dispatch', discovery='review', harm='fired',
                      trigger='any probe-attr histogram naming lib-stage1',
                      ok='lib-stage1 buckets by the fillStage2 spans its samples land in',
                      bug='refused: lib-stage1/odo overlapping the role before it by 73 lines',
                      proved='ran', notes='Both Run 32 samples naming lib-stage1 refused; watched 2026-09-18.'),
    'attr-reader-reads-the-working-tree-in-silence': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a histogram read after Main.hs moved, with no file given',
                      ok='refuses, naming the arm and the file; the header names the build',
                      bug='harness 0, everything in elsewhere, no word said',
                      proved='ran', notes="Run 32's histograms against the tree of 2026-09-18, and a header naming 0eda736."),
    'figures-drops-a-refused-gate-row': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a pair whose run-gate.sh --show refuses before printing',
                      ok='gate arms: the artifact gave nothing to check',
                      bug='the row left the check at a PASS', proved='asserted'),
    'attr-probe-divides-by-a-zero-count': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='perf stat reporting 0 instructions:u for an arm',
                      ok='no count, BAD=1, the loop goes on',
                      bug='division by 0 ended the probe at exit 1, the later arms unrun and $OUT short of them',
                      proved='asserted'),
    'readings-wait-took-the-pred-file-at-any-rc': dict(family='vacuous-check', discovery='review', harm='latent',
                      trigger='--predictions exiting 2 or raising in the readings stub',
                      ok='the case refuses rc=2 and !! crashed',
                      bug='the bare name matched either line', proved='asserted'),
    'reroll-sweep-ends-on-a-dead-leg': dict(family='unverified-state', discovery='review', harm='latent',
                      trigger='a run27 binary killed mid-group',
                      ok='the leg is set aside as *.failed.json, the sweep goes on, exit 1',
                      bug='the sweep ended silently and the next run skipped the leg as done',
                      proved='ran', notes='Watched on stub halves, one exiting 137 after opening --json.'),
    'reroll-reader-averages-a-nan-floor': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='a leg with no A/A copies, or a net at or below zero',
                      ok='the leg is named and left out of the median, rc 1',
                      bug='statistics.median over a nan: a finite wrong floor, or nan and nothing flagged',
                      proved='asserted'),
    'read-all-drops-a-refused-compare-from-the-range': dict(family='quiet-failure', discovery='review', harm='latent',
                      trigger='a class whose other-half JSON --compare refuses',
                      ok='!! <pop>: --compare gave no list line, so the range omits it',
                      bug='the population left the range with no mark', proved='asserted'),
    'checks-pyflakes-guard-accepts-what-the-step-does-not-run': dict(family='two-spellings', discovery='review', harm='latent',
                      trigger='a pyflakes script on PATH and no importable module',
                      ok='the step runs whichever it found',
                      bug='the guard passed and python3 -m pyflakes failed on a traceback',
                      proved='asserted'),
    'property-judges-read-only-greps-status': dict(family='error-as-value', discovery='review', harm='latent',
                      trigger='a reader that prints HOLDS and then exits non-zero',
                      ok='pipefail: the judge is red',
                      bug='the judge was green on grep alone', proved='asserted'),
    'busy-compare-fails-behind-a-bash-error': dict(family='domain-unchecked', discovery='review', harm='latent',
                      trigger='machine-busy.sh printing nothing or a non-number',
                      ok='refuses naming the reading, exit 2',
                      bug='[ "" -lt 5 ] refused at exit 2 behind a bash error and a message naming an empty percentage',
                      proved='ran', notes='The old line replayed in bash with an empty reading, 2026-09-18.'),

    # ---- the seams Run 40's write-up met, 2026-09-25 ----
    'fill-in-straddle-row-reads-the-listed-word': dict(
        family='scan-for-parse', discovery='in-use', harm='fired',
        harm_count=1,
        trigger='a binary with more than ten straddling self-loops, whose'
                ' survey line gains `, 10 longest listed`',
        ok='the row carries the count, `24 straddling`',
        bug='the row read `listed straddling`, so the note carried no'
            ' straddle count at all',
        proved='ran',
        notes='Watched 2026-09-25 on Run 40\'s note, whose fill-in had'
              ' carried it from the preparation unnoticed.'),
    'brief-facts-text-row-runs-on-past-its-row': dict(
        family='scan-for-parse', discovery='in-use', harm='fired',
        harm_count=1,
        trigger="a note whose `.text` row ends with no full stop",
        ok='the row and its own continuation lines, cut at a full stop',
        bug="the md5, launch and repetition rows joined into the brief's"
            ' item 5 as one sentence',
        proved='ran',
        notes='Watched 2026-09-25 on run40-pair.txt, and trimmed by hand'
              ' in that run\'s brief.'),

    # ---- the seams Run 37's write-up met, 2026-09-20 ----
    'checklist-prints-no-execution-order': dict(
        family='two-spellings', discovery='in-use', harm='fired',
        proved='ran',
        trigger='the post list executed in the order it prints in',
        ok='prints the execution order beside the list and names the'
           ' steps that run out of printed turn',
        bug='printed the steps in numeric order with nothing saying which'
            ' run out of it, so Run 37 took 9 and 10 after 6d and had to'
            ' record the deviation in its own post-mortem'),
    'brief-update-reopens-filled-slots': dict(
        family='quiet-failure', discovery='in-use', harm='fired',
        proved='ran',
        trigger='a second --brief-update over a brief whose `<yours>`'
                ' slots had been filled',
        ok='says how many filled slots the paste re-opened and that git'
           ' holds what it overwrote',
        bug='pasted the facts file\'s empty slots back over the prose and'
            ' said nothing but a higher slot count, which reads as the'
            ' ordinary reminder'),
    'class-block-second-slot-unnamed': dict(
        family='false-comment', discovery='in-use', harm='fired',
        proved='ran',
        trigger='a class block, which carries two `___` where only the'
                ' first said what it wanted',
        ok='both slots name what goes in them',
        bug='the second stood bare, so a session that filled the first'
            ' met a check reporting ten still open and had to find out'
            ' why'),
    'stalls-marks-a-cell-no-one-process-read': dict(
        family='unverified-state', discovery='in-use', harm='fired',
        harm_count=1, proved='ran',
        trigger='a cell whose processes draw different modes, as Run 40'
                "'s runs-3 consumers did under cycles:u",
        ok='the cell is followed by a # NONLINEAR line naming the event'
           ' and both slopes',
        bug='the (2N - N) figure printed as a measured cell and nothing'
            ' else, 12.3 and 5.1 cycles a run where the modes ran 6.8'
            ' to 10.2'),
    # The review of 2026-09-25 over every script whole. `harm` is unknown
    # throughout: nothing was looked into beyond the defect itself.
    'settled-rounds-see-only-the-short-loops': dict(
        family='vacuous-check', discovery='review', harm='unknown',
        trigger='LOOP_SETTLED=1, a group whose tier-0 cost lands on its plan'
                ' while an outer head or a long loop lands off it',
        ok='the group is off the plan and is planned again',
        bug='the group read as on the plan and was never planned again'),
    'major-run-names-a-population-it-lacks': dict(
        family='silent-option', discovery='review', harm='unknown',
        trigger='a population argument naming neither main nor a class,'
                ' `rnus` for `runs`',
        ok='refused at exit 2, naming the populations there are',
        bug='nothing ran, and the run logged itself complete at exit 0'),
    'stalls-reader-reads-past-a-nonlinear-mark': dict(
        family='scan-for-parse', discovery='review', harm='unknown',
        trigger='a stall sweep carrying a # NONLINEAR line for one of the'
                ' three cells of a shape',
        ok='the shape is dropped and named, exit 1',
        bug='the shape joined the table and the geomean, exit 0'),
    'stalls-keeps-a-cell-whose-check-process-failed': dict(
        family='other:check-voids-what-it-checks', discovery='review',
        harm='unknown',
        trigger='perf counting the -n N and -n 2N processes and not the'
                ' -n 3N one',
        ok='the cell is printed, followed by a # UNCHECKED line',
        bug='the cell was a `perf could not count` line, exit 1'),
    'stalls-linearity-reads-the-untruncated-slopes': dict(
        family='other:truncated-before-compared', discovery='review',
        harm='unknown',
        trigger='a small cell whose two slopes, linear to within the'
                ' tolerance, truncate to integers two percent apart',
        ok='no # NONLINEAR line',
        bug='# NONLINEAR, 49 then 50 cycles'),
    'counts-all-retake-tallies-its-own-call': dict(
        family='unverified-state', discovery='review', harm='unknown',
        trigger='a re-take after an attempt whose every sweep complained',
        ok='a clean re-take closes EVENING COMPLETE at exit 0',
        bug='it closed WITH 6 COMPLAINT(S) at exit 1, the first'
            " attempt's"),
    'counts-all-retake-keeps-what-an-earlier-call-wrote': dict(
        family='unverified-state', discovery='review', harm='unknown',
        trigger='a re-take where an earlier call wrote one population\'s'
                ' counts file',
        ok='that population is kept and said so',
        bug='it was asked again, which run-counts.sh refuses, a new'
            ' complaint'),
    'g3-twins-refuses-a-note-naming-no-source': dict(
        family='unverified-state', discovery='review', harm='unknown',
        trigger='Main.hs or align-as.py moved between the run and post-run'
                ' step 0, or a note naming neither',
        ok='nothing built, the mismatch named, exit 2',
        bug='the twins were built from the tree as it stood'),
    'properties-page-is-each-process-own': dict(
        family='environment-decides', discovery='review', harm='unknown',
        trigger='two properties.py processes at once, as the suite runs'
                ' them, or anything else at the fixed temp name',
        ok='each process reads back its own table',
        bug='one could read another\'s table, or a directory there'
            ' crashed it'),
    'r39-rules-exits-2-on-a-run-not-here': dict(
        family='error-as-value', discovery='review', harm='unknown',
        trigger='a run whose main JSON is absent',
        ok='exit 2, did not run', bug='exit 1, candidates found'),
    'fetch-model-exits-2-on-a-table-it-cannot-read': dict(
        family='error-as-value', discovery='review', harm='unknown',
        trigger='rescore of a table with no layout or no rows',
        ok='exit 2, did not run', bug='exit 1, a build failed'),
    'entries-sweep-exits-2-without-its-tools': dict(
        family='error-as-value', discovery='review', harm='unknown',
        trigger='gcc, perf or objdump missing, or perf not counting',
        ok='exit 2, did not run', bug='exit 1, a build failed'),
    'r38-sweep-exits-2-without-its-tools': dict(
        family='error-as-value', discovery='review', harm='unknown',
        trigger='gcc, perf, objdump or nm missing, or perf not counting',
        ok='exit 2, did not run', bug='exit 1, a build failed'),
    'interleave-refuses-a-cell-off-the-roster': dict(
        family='quiet-failure', discovery='review', harm='unknown',
        trigger='a cell whose shape or arm a binary lacks, a typo',
        ok='refused at exit 2, naming the cell and the binary',
        bug='empty processes differenced to ratios, printed as measured'),
    'brief-facts-reads-a-basis-with-an-underscore': dict(
        family='two-spellings', discovery='review', harm='unknown',
        trigger='a basis tag carrying `_`, which pair-halves.sh allows',
        ok='the basis is read, and its md5 row printed',
        bug='no basis read, the rows needing one dropped, and the md5'
            ' row empty'),
    'instance-gate-keeps-an-earlier-slow-draw': dict(
        family='unverified-state', discovery='review', harm='unknown',
        trigger='a gate re-run after a swap that parked a .slow',
        ok='the second slow draw is parked as .slow2 beside the first',
        bug='it was moved over the first, freeing its frames'),
    'view-floor-legs-refuses-a-factor-it-ignores': dict(
        family='silent-option', discovery='review', harm='unknown',
        trigger='--legs given with --factor',
        ok='refused at exit 2, --bar naming the legs\' threshold',
        bug='--factor was ignored and the exit set at a literal 2.0'
            ' percent'),
    'fill-in-survey-row-reads-the-listed-word-and-a-silent-survey': dict(
        family='scan-for-parse', discovery='review', harm='unknown',
        proved='ran',
        trigger='more than ten exit spans astride, a survey objdump'
                ' refused, or 10, 20 or 30 astride',
        ok='the count read whole, a silent survey named as such, and'
           ' only 0 a PASS',
        bug='`listed exit spans astride`, a refused survey read as the'
            ' straddle stop, and 10 astride a PASS',
        notes='Watched 2026-09-25 on srv and srv_say lifted out of the'
              ' script over stand-in surveys: before, 57 astride read'
              ' `listed`, a refused survey `,  at offset 0, ...` under'
              " 10a's stop, and 10 astride PASSed; after, 57, 20 and 10"
              ' FAIL with their counts, the refused survey reads'
              " `--survey read nothing`, and Run 40's halves PASS at 0."),
    'fill-in-roster-rows-drop-their-headings': dict(
        family='scan-for-parse', discovery='review', harm='unknown',
        proved='ran',
        trigger='a roster delta that moved class views and no arm',
        ok='the out line under `views`, below `classes:`',
        bug='the out line under no heading, reading as arms leaving',
        notes='Watched 2026-09-25 on the filter as the script runs it,'
              ' over a stand-in delta that moved two class views, and'
              ' on Run 39 against Run 40, every section unmoved.'),
    'note-paths-strip-a-name-s-own-first-character': dict(
        family='scan-for-parse', discovery='review', harm='unknown',
        proved='ran',
        trigger='a note line opening with a path that starts `./`, `/` or'
                ' `_`',
        ok='the path checked whole',
        bug='`./run40-x.json` checked as `/run40-x.json` and reported'
            ' gone',
        notes='Watched 2026-09-25 on the harvest over planted note lines:'
              ' before, `./run40-g912-main.json` at a line\'s head came'
              ' out `/run40-g912-main.json` and `_run40-x.txt`'
              ' `run40-x.txt`; after, both whole. Run 40\'s note passes'
              ' 10c under either.'),
    'parallel-steps-leave-the-readings-fan-out-uncapped': dict(
        family='other:nested-fan-out', discovery='in-use', harm='fired',
        proved='ran',
        trigger='check-all running the cases that call'
                ' post-run-readings.sh under -j 7',
        ok='READ_JOBS=1 on every -j step, a reader per case',
        bug='six readers per case, up to 42 against 16 CPUs',
        notes='The owner saw every CPU busy during the case steps on'
              ' 2026-09-26; the attribution is by mechanism, no'
              ' per-second record covering the spike. After the fix a'
              ' whole check-all, sampled each second, peaked at six'
              ' readers at once.'),
}


RECORDS = [
    # ---- read-run.py, the first review's ------------------------------
    # ---- --counts-totals, the scale a pair note asks for leg by leg ----
    # TWO PREPARATIONS DERIVED THESE BY HAND and each recorded it as an
    # improvisation, the note's COUNTS block wanting the previous run's
    # twenty-two figures to set the scale its own evening is read against.
    # The mode reads each leg's own header rather than its filename, so a
    # copied or renamed file answers for the run that wrote it.
    case('counts-totals-does-not-sum-the-legs', 'read-run.py', None,
         'the pair note\'s per-leg scale was hand-derived, twice running',
         plant=lambda t: {
             'a': counts_leg(t, 'zz', 'nospec', elapsed=300),
             'b': counts_leg(t, 'zz', 'o2', elapsed=200),
             'c': counts_leg(t, 'zz', 'nospec', 'runs', elapsed=400),
             'd': counts_leg(t, 'zz', 'o2', 'runs', elapsed=100)},
         argv=['--counts-totals', '{tmp}/zz'],
         ok=V(exit=0,
              has=['4 counted leg(s) over 2 population(s) and 2 halves,'
                   ' 1000s in all', 'runs', 'main', '700s', '300s'])),

    # A KILLED SWEEP LEAVES A FILE THAT PARSES, which is the failure the
    # unfinished branch exists for: summed silently it enters the scale as
    # a fast leg, and the next preparation reads a budget that was never
    # spent. The leg is named, kept out of every total, and the mode exits
    # 1 -- a partial answer said to be partial, as the run chapter asks of
    # every reading whose silence would otherwise pass for a verdict.
    case('counts-totals-sums-a-leg-that-never-ended', 'read-run.py', None,
         'a killed sweep would have entered the scale as a fast leg',
         plant=lambda t: {
             'a': counts_leg(t, 'zz', 'nospec', elapsed=300),
             'b': counts_leg(t, 'zz', 'o2', ended=False)},
         argv=['--counts-totals', '{tmp}/zz'],
         ok=V(exit=1,
              has=['300s in all', 'NOT summed', 'no `# end` stamp',
                   'zz-counts-o2.txt'])),

    case('counts-totals-refuses-a-prefix-that-names-nothing',
         'read-run.py', None,
         'a mistyped run name would have printed an empty scale',
         plant=lambda t: {},
         argv=['--counts-totals', '{tmp}/no-such-run'],
         ok=V(exit=2, has=['no counts file here'])),

    # ---- run-heartbeat.sh -----------------------------------------
    # THE SCRIPT EXISTS BECAUSE THE LOOP WAS IN THE CHAPTER, eleven lines
    # of `while true` with two redirects and a `cut`, retyped every run.
    # checks.py's own rule is that every tracked shebang file here is a
    # program a step or a case must name, so a script added without one
    # is a gap the day it lands -- which is how this one arrived, and
    # what the shape pass caught.
    #
    # THE PREFIX IS TAKEN WHERE IT POINTS, as `--over-list`'s is, so these
    # plant in a temp directory and need no shadow: the script cds to its
    # own directory for a bare name and a path-qualified one resolves
    # from there.
    case('heartbeat-does-not-tick-what-a-run-has-produced', 'run-heartbeat.sh',
         None, 'the run list carried the heartbeat as a shell loop to retype',
         plant=lambda t: {
             'a': synth_json(t, 'main', name='zz-a-main.json'),
             'b': write(os.path.join(t, 'zz-evening.txt'),
                             '=== 2026-01-01 sequence: done, rc=0\n'),
             'c': write(os.path.join(t, 'zz-wallclock.log'),
                             '=== 2026-01-01 major run complete\n')},
         env={'HEARTBEAT_ONCE': '1'},
         argv=['{tmp}/zz'],
         ok=V(exit=0, has=['heartbeat: 1 JSONs', 'sequence: done, rc=0',
                           'major run complete'])),

    # THE TICK A RUN THAT HAS PRODUCED NOTHING STILL OWES. For the first
    # half-hour neither file exists -- run-major.sh writes the wall-clock
    # log when the SEQUENCE starts, not when the evening does -- and a run
    # that died in the gate is the one a heartbeat is most use for, so a
    # missing file is an empty field and never an error.
    case('heartbeat-errors-before-the-run-has-written-anything',
         'run-heartbeat.sh', None,
         'a tick before the first file exists would have read as a failure',
         plant=lambda t: {},
         env={'HEARTBEAT_ONCE': '1'},
         argv=['{tmp}/zz'],
         ok=V(exit=0, has=['heartbeat: 0 JSONs'])),

    case('heartbeat-takes-no-argument-as-a-run', 'run-heartbeat.sh', None,
         'a missing run name would have ticked over the whole directory',
         plant=lambda t: {},
         argv=[],
         ok=V(exit=2, has=['usage: ./run-heartbeat.sh RUN'])),

    # ---- --hand-tables, the two tables the write-up used to type ----
    case('hand-tables-reads-a-stale-row', 'read-run.py', None,
         "CONTROL: the anchors and the two-column rows are read against the"
         ' JSONs, and a row the JSONs do not give is named',
         # README's open list carried `A hand-edited table goes stale
         # unchecked` from Run 20 to Run 40: Run 22's anchors held the
         # previous run's figures in seven of nine cells past every gate.
         # The live run file's rows against two synthetic halves disagree
         # on both tables, so both have to be named.
         plant=lambda t: {'doc': write_rundoc(t, rundoc_text()),
                          'a': synth_json(t, 'main', name='a.json'),
                          'b': synth_json(t, 'main', name='b.json')},
         argv=['{a}', '--compare', '{b}', '--hand-tables',
               '--run-doc', '{doc}'],
         ok=V(exit=1, has=['anchors: `cnn-slice-c32`',
                           'two-column: `mut-odo-vecdims`'])),

    case('hand-tables-drops-a-departed-row', 'read-run.py', '0b38fd0',
         'a two-column row for an arm the run no longer times refused the'
         ' whole install',
         # Run 41's install stopped at 5b on `lib-stage3-lean-onelevel`,
         # retired from timing between the runs, until the row was deleted
         # by hand -- where --markdown drops such a row with a warning.
         # The planted row names an arm neither JSON times.
         plant=lambda t: {'doc': unwrapped_rundoc_edit(
                              t, '| `mut-odo-vecdims` | **',
                              '| `retired-arm` | **0.045** | 0.058 |\n'
                              '| `mut-odo-vecdims` | **'),
                          'a': synth_json(t, 'main', name='a.json'),
                          'b': synth_json(t, 'main', name='b.json')},
         argv=['{a}', '--compare', '{b}', '--hand-tables', '--in-place',
               '--run-doc', '{doc}'],
         ok=V(exit=0, has=['`retired-arm`', 'dropped']),
         bug=V(exit=2, has=['no such arm in both JSONs'])),

    # ---- --gate-draft, run list step 14a's four readings as one table ----
    case('gate-draft-reads-the-registration-spans', 'read-run.py',
         '715e7c0',
         "a registration's cross span already outside its band at the gate"
         ' went unread for six hours, until post-run step 5c',
         # Run 41's gate read `bq-expand` at 1.36 in both passes against a
         # registered 1.303 within 1%, and nothing said so before 5c.
         plant=plant_gate_with_registration,
         argv=['--gate-draft', '{run}', '--readme', '{readme}'],
         ok=V(exit=0, has=['item (1)', 'OUTSIDE']),
         bug=V(exit=0, hasnt=['item (1)'])),


    case('gate-draft-names-the-half-that-drifted', 'read-run.py', None,
         'CONTROL: the draft puts the four readings side by side and names'
         " each half's widest move between its own two legs",
         # Runs 39 and 40 wrote the table by hand from four --compare
         # outputs and quoted a `prediction` of the second pass that is an
         # identity. One cell of the basis's -b leg is slowed, so the basis
         # must be the half named as moving, on that arm.
         plant=lambda t: {
             'note': write(os.path.join(t, 'zz-pair.txt'),
                           'HALVES: basis=nb other=ob\n'),
             'ba': synth_json(t, 'main', name='zz-gate-nb-a.json'),
             'bb': synth_json(t, 'main', name='zz-gate-nb-b.json',
                              skew=[(main_shapes()[0], 'list', 3)]),
             'oa': synth_json(t, 'main', name='zz-gate-ob-a.json'),
             'ob': synth_json(t, 'main', name='zz-gate-ob-b.json')},
         argv=['--gate-draft', '{tmp}/zz'],
         ok=V(exit=0, has=['gate draft for zz', 'nb moved between its own'
                           ' two legs by at most', 'on list',
                           'by construction'])),

    # ---- --over-list, the sweep behind the properties' only-claim ----
    # THE CLAIM IS A NEGATIVE OVER A THOUSAND CELLS and the mode's whole
    # job is to make its silence readable: Run 31 hand-rolled it from
    # `--cells` and its independent checker hand-rolled it again, agreeing
    # on three cells of 1078 with neither able to show the other what it
    # had read. So this plants ONE cell above the baseline and requires
    # both halves of the answer -- the cell named, and the denominator
    # line that makes a clean run different from an empty one.
    case('over-list-misses-a-planted-cell', 'read-run.py', None,
         'the only-claim behind property 1 had no mode and was hand-rolled',
         plant=lambda t: {
             'a': synth_json(t, 'main', name='zz-nospec-main.json',
                             skew=[(main_shapes()[0], _reader().PLAIN, 100)]),
             'b': synth_json(t, 'main', name='zz-o2-main.json')},
         argv=['--over-list', '{tmp}/zz'],
         ok=V(exit=0,
              has=['population(s) read', 'cell(s) above 1',
                   main_shapes()[0], _reader().PLAIN],
              hasnt=['NO cell above 1'])),

    # THE OTHER DIRECTION, and it is the one the claim is usually read in:
    # a run with nothing above the baseline must SAY how much it read, or
    # a sweep that found no populations at all reads the same as a clean
    # one. That is this README's own rule for a grep, applied to a mode
    # whose ordinary answer is silence.
    case('over-list-clean-run-says-what-it-read', 'read-run.py', None,
         'a clean sweep and an empty one read alike without the count',
         # THE CLEAN RUN IS BUILT AND NOT ASSUMED: the synthetic model
         # gives `lib-stage1` above the baseline on every shape, so a
         # default pair is not clean and a case that took it for clean
         # would have asserted the wrong branch. `list` is skewed slowest
         # instead, which is a run with nothing above it by construction.
         plant=lambda t: {
             'a': synth_json(t, 'main', name='zz-nospec-main.json',
                             skew=[(sh, 'list', 100)
                                   for sh in main_shapes()]),
             'b': synth_json(t, 'main', name='zz-o2-main.json',
                             skew=[(sh, 'list', 100)
                                   for sh in main_shapes()])},
         argv=['--over-list', '{tmp}/zz'],
         ok=V(exit=0,
              has=['2 population(s) read', 'NO cell above 1'],
              hasnt=['cell(s) above 1,'])),

    # A PREFIX THAT NAMES NOTHING IS A 2 AND NOT A CLEAN RUN, which is the
    # exit every script here owes for a run that did not happen -- and the
    # failure this mode would otherwise have is the quietest one it could:
    # a mistyped run name printing a clean sweep over no populations.
    # A POPULATION WITH NO `list` COMPARED NOTHING, and counted as read it
    # turned a sweep over nothing into a clean verdict -- the mode's own
    # failure mode wearing the answer it exists to prevent. A filtered
    # probe is a run without `list`, which is the shape that made
    # `--bridge` raise rather than refuse. Found 2026-09-14 by the shape
    # pass, asking the mode a question other than the one it was written
    # for, and not by any check.
    case('over-list-calls-a-baseless-population-clean', 'read-run.py', None,
         'a population with no `list` read as a clean sweep',
         plant=lambda t: {
             'a': synth_json(t, 'main', name='zz-a-main.json',
                             drop_arms=('list',))},
         argv=['--over-list', '{tmp}/zz'],
         ok=V(exit=2,
              has=['NO readable `list` to compare against',
                   'compared nothing'],
              hasnt=['NO cell above 1'])),

    case('over-list-refuses-a-prefix-that-names-nothing', 'read-run.py', None,
         'a mistyped run name would have read as a clean sweep',
         plant=lambda t: {},
         argv=['--over-list', '{tmp}/no-such-run'],
         ok=V(exit=2, has=['no population JSON here'])),

    case('install-lands-in-next-block', 'read-run.py', '045ca63',
         'a class whose own table is absent took the next class\'s',
         plant=lambda t: {'rundoc': rundoc_without_class_table(t),
                          'run': synth_json(t, 'rev')},
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
                          'run': synth_json(t, 'rev')},
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
                                                      ('lib-stage2-lean', 1.08),
                                                      ('liblist-stage1', 1.01))])},
         # The third mover was lib-stage2-disp until 2026-09-07, when it
         # was parked Only and left the synthetic run: a skewed arm has
         # to be a timed one, and the docstring's own lesson about the
         # denominator holds for the names.
         argv=['{run}', '--compare', '{other}', '--movers', '3'],
         ok=V(exit=0,
              has=['3 of %d arm(s) move past 3%%' % compared_arm_count(),
                   'in 3 group(s)', 'bq-expand', 'lib-stage1',
                   'lib-stage2-lean'],
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

    case('block-compare-prose-comes-out-wrapped', 'read-run.py', None,
         'the two paragraphs install-tables.sh does NOT write, in the'
         ' form the run file keeps',
         # THE ARM THAT MATTERS, and the one Run 36's defect landed in.
         # install-tables.sh writes Controls, Provenance and the per-shape
         # line; `Across the halves` and `What the class says` exist only
         # with the second JSON and are placed by hand, so they are the two
         # a session joins -- and `lib- stage2-lean-u1` reached the page in
         # a `What the class says` paragraph. The assertion is a span of
         # the cross-half boilerplate too long to survive an eighty-column
         # wrap. This arm honours no --in-place and never did.
         plant=lambda t: {'run': synth_json(t, 'rev', name='a.json'),
                          'other': synth_json(t, 'rev', name='b.json')},
         argv=['{run}', '--block', '--compare', '{other}', '--brief'],
         ok=V(exit=0,
              has=['**Across the halves:** 0 of the %d arms are faster on'
                   ' this half and %d slower, at a geomean of'
                   % (compared_arm_count(), compared_arm_count())])),

    case('block-prose-comes-out-wrapped-for-a-caller-to-join', 'read-run.py',
         None,
         'the class block a run file pastes, emitted in the form it keeps',
         # BORN 2026-09-19 OUT OF AN ARM NAME BROKEN IN HALF. `--in-place`
         # installs a block's TABLE and leaves its prose to the author, by a
         # ruling this mode's docstring carries -- and it printed that prose
         # WRAPPED, where the run file keeps one line a paragraph. Run 36
         # joined the wrapped lines in a script of its own, a break fell
         # inside `lib-stage2-lean-u1`, and `lib- stage2-lean-u1` reached the
         # page: an arm name that renders wrong, matches no row of the table
         # above it, and answers no search for the arm. The seam was the
         # joining, so the prose is emitted already joined. The assertion is
         # a ninety-four-character span of the Provenance boilerplate, which
         # cannot be contiguous in anything wrapped at eighty.
         plant=lambda t: {'run': synth_json(t, 'rev', name='a.json'),
                          'doc': write_rundoc(t, open(RUNDOC).read())},
         argv=['{run}', '--block', '--brief', '--in-place',
               '--run-doc', '{doc}'],
         ok=V(exit=0,
              has=['**Provenance:** elapsed ___, peak ___ MiB in use, ___'
                   ' MiB max residency (copy from the process'])),

    case('alloc-per-shape-gives-no-per-arm-reading', 'read-run.py', None,
         'CONTROL: the per-arm allocation ratio a pair whose variable moves it needs',
         # BORN 2026-09-19, OUT OF A FIGURE COMPUTED BY HAND AND GOT WRONG.
         # `--compare --alloc` counts cells inside 1e-4 and names the worst,
         # which answers whether a pair AGREES and not by how much it parts.
         # Run 36's pair parts on two families, and the write-up needed the
         # size per arm: the only other route is the `alloc` column, a MEDIAN
         # over shapes that must not be divided across halves, so the figure
         # went into a script instead -- whose print took an absolute
         # deviation and put `2 - ratio` on the page, reversing one arm's
         # direction in three places. The mode prints both columns for that
         # reason. This case is the moving direction; the one below is the
         # level one, and a mode that answered only one of them would pass
         # nothing worth having.
         plant=plant_alloc_skewed_pair,
         argv=['{run}', '--compare', '{other}', '--alloc', '--per-shape'],
         ok=V(exit=0,
              has=['per arm, over the cells above', 'other/this', 'this/other',
                   'bq-expand', '0.8000', '1.2500'])),

    case('alloc-per-shape-invents-a-movement', 'read-run.py', None,
         'CONTROL: two halves built alike read 1.0000 on every arm',
         # The other direction, and the one that would hide a sign error:
         # a pair that moves no allocation must read 1.0000 both ways, so
         # that a run quoting a figure from this table is quoting a
         # movement and not an artefact of the fit.
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json'),
             'other': synth_json(t, 'main', name='b.json')},
         argv=['{run}', '--compare', '{other}', '--alloc', '--per-shape'],
         ok=V(exit=0, has=['per arm, over the cells above', '1.0000'],
              hasnt=['0.8000'])),

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

    case('results-reads-a-shape-name-as-a-run', 'read-run.py', 'd4a6a00',
         "the stale-name check read `block-run64-gap1` in Results as Run"
         " 64's half",
         # A word boundary falls after a hyphen, so `\\brun(\\d+)-` matched
         # inside the `block` class's shape names. Met 2026-09-25 when Run
         # 40's copy test named two of them in Results; the token now has to
         # stand clear of a word character or a hyphen on its left.
         plant=lambda t: {'rundoc': rundoc_results_names_a_run_shape(t)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(hasnt=['names run']),
         bug=V(has=['names run 64'])),

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

    case('counts-pair-reads-two-arms-on-one-half', 'read-run.py', None,
         'a registration comparing two arms on ONE binary had no counted-work'
         ' mode, so the write-up hand-rolled the arithmetic',
         # `--counts` read a PAIR of sweep files beside `--compare` and
         # answered only *did this arm move between the halves*. Run 25's
         # registration 7 turned on the other question and there was no
         # mode: the write-up differenced each arm against the sweep's
         # `sum-only` mean per shape and geomeaned over the eighteen, which
         # is the standing instruction's own definition of a defect report
         # against this reader. The corrected column is the one comparable
         # with a `--pair` time ratio; the raw one is what the file holds.
         plant=lambda t: {'run': synth_json(t, 'main'),
                          'counts': synth_counts(t, 'c.txt',
                                                 cheap_sum_only=True)},
         argv=['{run}', '--counts', '{counts}',
               '--pair', 'mut-odo-vecdims', 'bq-expand'],
         ok=V(exit=0, has=['counted work within one half',
                           'corrected', 'raw',
                           'mut-odo-vecdims / bq-expand'],
              hasnt=['no shape carries both'])),

    case('counts-pair-per-shape-differences-beside-the-resolution',
         'read-run.py', None,
         'CONTROL: --per-shape with a within-half --counts pair prints each'
         ' shape\'s instruction difference and the sum-only-early/late'
         ' spread it is read against',
         # Run 34 hand-rolled both: a stage-twelve-over-eleven difference
         # per shape, whose corrected ratio dropped seventeen of nineteen
         # shapes, and the spread between the two copies of the forcing
         # pass, which no mode priced.
         plant=lambda t: {'run': synth_json(t, 'main'),
                          'counts': synth_counts(t, 'c.txt',
                                                 cheap_sum_only=True)},
         argv=['{run}', '--counts', '{counts}',
               '--pair', 'mut-odo-vecdims', 'bq-expand', '--per-shape'],
         ok=V(exit=0, has=['per shape, mut-odo-vecdims - bq-expand',
                           '|early - late|', 'the resolution'])),

    case('counts-pair-sinks-loudly', 'read-run.py', None,
         'a within-half reading whose correction leaves no work said so'
         ' rather than printing a ratio of two negatives',
         # THE NON-VACUITY OF THE CASE ABOVE: on the default fixture the
         # `sum-only` arms sort among the dearest, so the correction sinks
         # every cell -- which is how the case above was found to need a
         # faithful one. Here that is the planting, and the mode must name
         # it and exit 2 rather than divide.
         plant=lambda t: {'run': synth_json(t, 'main'),
                          'counts': synth_counts(t, 'c.txt')},
         argv=['{run}', '--counts', '{counts}',
               '--pair', 'mut-odo-vecdims', 'bq-expand'],
         ok=V(exit=2, has=['no shape carries both'])),

    case('counts-pair-refuses-two-files', 'read-run.py', None,
         'the two arities of --counts read as each other',
         # ONE sweep file with `--pair` is the within-half reading and TWO
         # with `--compare` is the cross-half one. Given two files and a
         # `--pair`, the older arity is what the caller means and the
         # newer one is what the flag now also spells, so it is refused by
         # name rather than read as either.
         plant=lambda t: {'run': synth_json(t, 'main'),
                          'a': synth_counts(t, 'a.txt'),
                          'b': synth_counts(t, 'b.txt', ratio=1.05)},
         argv=['{run}', '--counts', '{a}', '{b}',
               '--pair', 'mut-odo-vecdims', 'bq-expand'],
         ok=V(exit=2, has=['takes ONE sweep file'])),

    case('counts-alone-is-refused', 'read-run.py', None,
         'CONTROL: --counts with neither owner is the unread-flag family,'
         ' and it is refused rather than dropped',
         # It left the modifier table when it gained a second arity, one
         # `needs` no longer naming both owners -- so this is what says the
         # refusal survived the move.
         plant=lambda t: {'run': synth_json(t, 'main'),
                          'counts': synth_counts(t, 'c.txt')},
         argv=['{run}', '--counts', '{counts}'],
         ok=V(exit=2, has=['does nothing alone'])),

    case('counts-compare-still-takes-two', 'read-run.py', None,
         'CONTROL: the cross-half arity is unmoved, which is what says the'
         ' new one was added beside it and not over it',
         plant=lambda t: {'run': synth_json(t, 'main', name='this.json'),
                          'other': synth_json(t, 'main', name='that.json'),
                          'a': synth_counts(t, 'a.txt'),
                          'b': synth_counts(t, 'b.txt', ratio=1.05)},
         argv=['{run}', '--compare', '{other}',
               '--counts', '{a}', '{b}'],
         ok=V(exit=0, has=['counted work, this run against'])),

    case('pin-restricts-to-the-shared-shapes', 'read-run.py', None,
         'a cross-run figure was pinned by one --exclude-shape per retired'
         ' shape, typed out',
         # `match bases before reading any ratio` asks every cross-run
         # figure to be read over the shapes the two runs share, and until
         # 2026-09-05 that was a hand-typed flag apiece. Run 24's write-up
         # improvised it with two and filed the improvisation as a task;
         # Run 25 improvised it with eight and needed them for every
         # cross-run figure it published. A typed list is a place to drop a
         # shape in silence, which is the failure this mode removes.
         plant=lambda t: {
             'run': synth_run(os.path.join(t, 'big.json'), main_shapes()),
             'other': synth_run(os.path.join(t, 'small.json'),
                                main_shapes()[:6])},
         argv=['{run}', '--pin', '{other}'],
         # The population line is shared with `pin-is-the-flags-it-replaces`
         # below, which reaches it by the flags: two cases, two routes, one
         # expected line, and that pair is the equivalence a write-up
         # substituting one for the other relies on. Byte-for-byte on the
         # real artifacts too, 2026-09-05: `--pin run25-g912-main.json` and
         # the eight `--exclude-shape` flags it stands for gave identical
         # output on run24-g912-main.json.
         ok=V(exit=0, has=['pinned to the 6 shape(s)', 'dropping',
                           'reading %d of them over 6 shapes'
                           % timed_arm_count()])),

    case('pin-says-when-it-drops-nothing', 'read-run.py', None,
         'CONTROL: a pin against a run holding every shape drops none and'
         ' says so, which is what says the case above pinned on its'
         ' populations and not on the flag',
         plant=lambda t: {
             'run': synth_run(os.path.join(t, 'a.json'), main_shapes()),
             'other': synth_run(os.path.join(t, 'b.json'), main_shapes())},
         argv=['{run}', '--pin', '{other}'],
         ok=V(exit=0, has=['it drops none'], hasnt=['dropping'])),

    case('pin-refuses-a-disjoint-population', 'read-run.py', None,
         'a pin against a run sharing no shape read as an empty table'
         ' rather than as a refusal',
         # EXIT 2 and not 1: the run did not happen, which is this
         # directory's convention for a check that could not be made.
         plant=lambda t: {
             'run': synth_run(os.path.join(t, 'm.json'), main_shapes()),
             'other': synth_json(t, 'rev')},
         argv=['{run}', '--pin', '{other}'],
         ok=V(exit=2, has=['share no shape'])),

    case('pin-is-the-flags-it-replaces', 'read-run.py', None,
         'CONTROL: --pin and the --exclude-shape flags it stands for read'
         ' the same population, which is the whole of what it claims',
         # The pair above says the mode restricts; this says it restricts
         # to the SAME set the hand-typed form did, which is what a
         # write-up substituting one for the other is relying on. Same
         # planted shapes, the two routes, one expected line -- the twin is
         # `pin-restricts-to-the-shared-shapes` above.
         plant=lambda t: {
             'run': synth_run(os.path.join(t, 'big2.json'), main_shapes())},
         argv=['{run}'] + [f for sh in main_shapes()[6:]
                           for f in ('--exclude-shape', sh)],
         ok=V(exit=0, has=['reading %d of them over 6 shapes'
                           % timed_arm_count()])),

    case('checklist-prints-the-readings-list', 'read-run.py', None,
         'CONTROL: --checklist readings prints the chapter\'s list of what a'
         ' session reads, items 1 to 10, and nothing else',
         # The readings list sat inside the reasons at the chapter's foot,
         # reachable by --para alone, while each checklist step names its
         # items by number (2026-09-23).
         argv=['--checklist', 'readings'],
         ok=V(exit=0, has=["1. this chapter's three checklists",
                           "10. the PREVIOUS run's pair note"],
              hasnt=['grep -i gate $R-pair.txt'])),

    case('check-doc-refuses-a-cheaper-block', 'read-run.py', None,
         'the recommended-tasks heading keeps no run\'s block since'
         ' 2026-09-25, and seven once stood under it',
         plant=lambda t: {'readme': write(
             os.path.join(t, 'P.md'), open(README).read()
             + '\n**What Run 1 made cheaper for nobody.**\n')},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['made cheaper` block(s) (Runs', 'where the'
                                                            ' heading keeps'
                                                            ' none'])),

    case('checklist-default-stops-at-why', 'read-run.py', None,
         'CONTROL: a step prints through its `why:` line by default, the'
         ' reasons under it are skipped, and the next step resumes',
         # Plan item 21.1, 2026-09-23: the short form became the default
         # and the chapter's steps put their action above `why:`.
         plant=lambda t: {'readme': readme_with_a_run_step_and_its_reasons(t)},
         argv=['--checklist', 'run', '--readme', '{readme}'],
         ok=V(exit=0, has=['ACTION-BEFORE-WHY',
                           "why: --para 'A paired Run has one gate more'",
                           './run-evening.sh $R', 'ACTION-OF-14'],
              hasnt=['REASON-AFTER-WHY'])),

    case('checklist-full-prints-the-reasons', 'read-run.py', None,
         'CONTROL: --full prints the reasons the default form skips',
         plant=lambda t: {'readme': readme_with_a_run_step_and_its_reasons(t)},
         argv=['--checklist', 'run', '--full', '--readme', '{readme}'],
         ok=V(exit=0, has=['ACTION-BEFORE-WHY', 'REASON-AFTER-WHY'])),

    case('record-prints-a-series-aligned', 'read-run.py', None,
         'CONTROL: --record NAME prints series/NAME.tsv, its notes and'
         ' its rows; an unknown name is refused with the names it has',
         argv=['--record', 'floor'],
         ok=V(exit=0, has=['# The A/A floor', 'carry-basis'])),

    case('record-refuses-an-unknown-series', 'read-run.py', None,
         'CONTROL: --record with a name series/ lacks exits 2, naming'
         ' the series it has',
         argv=['--record', 'no-such-series'],
         ok=V(exit=2, has=['one of floor'])),

    case('checklist-post-a-stops-at-the-seam', 'read-run.py', None,
         'CONTROL: --checklist post-a is the post list down to step 6 and'
         ' no further',
         # The post list is longer than the other two together and has a
         # seam: nothing from step 6 on is actionable until 5b's tables are
         # in. Run 25 read all 412 lines at once, hours before it could act
         # on half of them, and then re-read most of them at their steps.
         plant=lambda t: {'readme': edited_readme(t)},
         argv=['--checklist', 'post-a', '--readme', '{readme}'],
         ok=V(exit=0, has=['steps 0 to 5', '0. NAME THE FILL GROUPS',
                           'install-tables.sh'],
              hasnt=['walk the replace list', 'offer the artifacts'])),

    case('checklist-post-b-starts-at-the-seam', 'read-run.py', None,
         'CONTROL: --checklist post-b is the post list from step 6 on, and'
         ' with post-a it is the whole list',
         plant=lambda t: {'readme': edited_readme(t)},
         argv=['--checklist', 'post-b', '--readme', '{readme}'],
         ok=V(exit=0, has=['steps 6 to 11', 'walk the replace list',
                           'offer the artifacts'],
              hasnt=['0. NAME THE FILL GROUPS'])),

    case('checklist-post-half-refuses-a-missing-seam', 'read-run.py', None,
         'a half of the post list cut at a line number rather than at its'
         ' own text',
         # THE NON-VACUITY OF THE TWO ABOVE: they would pass just as well
         # on a mode that sliced the block at a fixed offset, and a fixed
         # offset is what goes wrong silently the next time a step is
         # added. Remove the seam and the mode must refuse by name rather
         # than cut somewhere.
         plant=lambda t: {'readme': edited_readme(t, (
             '    #   6. walk the replace list under Provenance',
             '    #   6. WALK the replace list under Provenance'))},
         argv=['--checklist', 'post-a', '--readme', '{readme}'],
         ok=V(exit=1, has=['seam', 'occurs 0 times'])),

    case('checklist-post-is-still-whole', 'read-run.py', None,
         'CONTROL: --checklist post is unsplit and carries both ends,'
         ' which is what says the halves are cut out of it',
         plant=lambda t: {'readme': edited_readme(t)},
         argv=['--checklist', 'post', '--readme', '{readme}'],
         ok=V(exit=0, has=['0. NAME THE FILL GROUPS', 'walk the replace list',
                           'offer the artifacts'],
              hasnt=['steps 0 to 5', 'steps 6 to 11'])),

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

    case('sunk-warning-names-the-rows-not-every-cell', 'read-run.py',
         '2ab20a4',
         'the sunk-cell warning enumerated every cell on every call, where'
         ' the per-row coverage beside it is the finding',
         # The line already carries the count, the worst cell and how many
         # shapes each short row covers. The enumeration between them is
         # the same information cell by cell, and it is the bulk: on Run
         # 27's main set it is seventy `shape/arm` pairs on every reader
         # call. The rows are what a reader acts on; the cells are in the
         # JSON. --verbose restores them, as it restores the standing
         # explanation --brief drops.
         plant=lambda t: {'run': sunk_json(t, main_shapes(), 'lib-stage1')},
         argv=['{run}', '--markdown'],
         ok=V(has=['cell(s) whose forcing term', 'row(s) are geomeans',
                   'over 18 of 19', '--cells'],
              hasnt=['all of them alexnet-L1-55-c3-k11/lib-stage1']),
         # The bug direction is what makes the `hasnt` above worth
         # anything: a string that appears in neither direction passes it
         # for free, and only the audit at `2ab20a4^` shows this one on
         # the screen.
         bug=V(has=['cell(s) whose forcing term', 'row(s) are geomeans',
                    'all of them alexnet-L1-55-c3-k11/lib-stage1'],
               hasnt=['--cells'])),

    case('sunk-warning-fires-under-every-mode', 'read-run.py', None,
         'CONTROL: shortening the line did not silence it, and it is the'
         ' same line whichever mode asked -- the silent-option risk',
         plant=lambda t: {'run': sunk_json(t, class_shapes('scaled'),
                                           'lib-stage1')},
         argv=['{run}', '--block', '--brief'],
         ok=V(has=['cell(s) whose forcing term', 'row(s) are geomeans'],
              hasnt=['all of them scaled-'])),

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
         'CONTROL: the two-column table is the one a reading wants, so'
         ' one caller asks for tables',
         plant=lambda t: {'doc': doc_with_a_table(t)},
         argv=['--section', 'Middle', '--with-tables', '--readme', '{doc}'],
         ok=V(exit=0, has=['| a | b |'])),

    case('section-with-tables-selects-one-table', 'read-run.py', None,
         'the reading list names ONE table and --with-tables was'
         ' all-or-nothing, so item 4 pulled the whole fingerprint with it',
         # Reading-list item 4 is "the two-column table under it, the ONE
         # table read". Run 25 took it with bare --with-tables and got Run
         # 24's per-shape fingerprint besides: 118 lines where the prose
         # alone is 36. A number picks one and withholds the rest, so the
         # enumeration can be obeyed rather than approximated.
         plant=lambda t: {'doc': doc_with_a_table(t, 3)},
         argv=['--section', 'Middle', '--with-tables', '2',
               '--readme', '{doc}'],
         ok=V(exit=0, has=['| a2 | b2 |', 'table paragraph(s) withheld'],
              hasnt=['| a1 | b1 |', '| a3 | b3 |'])),

    case('section-splits-a-table-from-its-lead', 'read-run.py', '7249a35',
         'a table sharing a paragraph with its lead could not be selected,'
         ' so --with-tables 1 released another table instead',
         # Reading-list item 4 asks for the compares-against section's
         # two-column table by `--with-tables 1`, and that table follows
         # its lead with no blank line, as every one here does. Only the
         # per-shape fingerprints started a paragraph with a bar, so the
         # ONE table the list names was the one the mode could not reach.
         # Found by Run 32's carrier, which reported it from inside the
         # digest rather than as a refusal anybody saw.
         plant=lambda t: {'doc': doc_with_a_glued_table(t)},
         argv=['--section', 'Middle', '--with-tables', '2',
               '--readme', '{doc}'],
         ok=V(exit=0, has=['| a2 | b2 |', 'The lead sentence'],
              hasnt=['| a1 | b1 |']),
         bug=V(exit=1, has=['this section carries 1 table'])),

    case('note-blocks-resume-after-the-fill', 'read-run.py', '7249a35',
         "a gate verdict written BELOW the fill-in block escaped the"
         ' withholding and --draft carried it into the next note',
         # The state was sticky and RESET to plain after the fill-in
         # block, which is one paragraph -- so everything under it read as
         # ordinary content. Run 33's draft opened with Run 32's
         # palindrome spread and its machine check, tag substitution
         # applied, naming a gate process no run will write.
         plant=lambda t: {'note': note_with_gate_below_the_fill(t)},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'c,d'],
         ok=V(exit=0, has=['GATE: NOT RUN', 'HALVES: basis=c other=d'],
              hasnt=['PALINDROME', 'MACHINE CHECK DID NOT FIRE']),
         bug=V(exit=0, has=['PALINDROME', 'MACHINE CHECK DID NOT FIRE'])),

    case('draft-compares-with-the-run-it-drafts-from', 'read-run.py', None,
         'CONTROL: a carried COMPARE line is reset to the drafted-from run,'
         ' a ruling that picked another being the last pair\'s',
         plant=lambda t: {'note': write(os.path.join(t, 'run97-pair.txt'),
                                        NOTE_STUB + 'COMPARE: run95\n')},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'c,d'],
         ok=V(exit=0, has=['COMPARE: run97'], hasnt=['COMPARE: run95'])),

    case('draft-adds-a-compare-line', 'read-run.py', None,
         'CONTROL: a note from before the COMPARE line drafts one under'
         ' HALVES',
         plant=lambda t: {'note': write(os.path.join(t, 'run97-pair.txt'),
                                        NOTE_STUB)},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'c,d'],
         ok=V(exit=0, has=['HALVES: basis=c other=d\nCOMPARE: run97'])),

    case('compare-reads-no-reducing-consumer', 'read-run.py', '7249a35',
         'a `cross` prior on a `-sum` arm was re-derivable only by a'
         ' hand-written geomean over two JSONs',
         # `--compare` skips them because their net is the forcing term
         # subtracted from itself; `--predictions` has read them on raw
         # `slope` since Run 29 but only for an arm some span names. Run
         # 32's preparation wrote the geomean by hand and Run 33's could
         # not quote two of the three figures its note wanted.
         plant=lambda t: {'a': synth_json(t, name='a.json'),
                          'b': synth_json(t, name='b.json', slow=1.1)},
         argv=['{a}', '--compare', '{b}'],
         ok=V(exit=0, has=['reducing consumers', 'sum-only-late',
                           'RAW `slope`']),
         bug=V(exit=0, hasnt=['reducing consumers'])),

    case('note-check-reads-the-carried-blocks', 'read-run.py', '7249a35',
         'nothing read the note as PROSE: 10c and 10d are predicates over'
         ' structure, so a carried block describing the previous pair'
         ' passed them both',
         plant=lambda t: {'note': note_for_the_check(t),
                          'readme': readme_with_a_registration(t)},
         argv=['--note-check', '{note}', '--readme', '{readme}'],
         ok=V(exit=1, has=['continuity claim reaching only Run 96',
                           'item (5)', 'not on the roll', 'no [EXEC] block',
                           'no VARIABLE-CHECK line']),
         bug=V(exit=2, hasnt=['continuity claim'])),

    case('note-check-passes-a-note-with-none-of-them', 'read-run.py', None,
         'CONTROL: the same note with its three statements current',
         plant=lambda t: {'note': note_for_the_check(t, broken=False),
                          'readme': readme_with_a_registration(t)},
         argv=['--note-check', '{note}', '--readme', '{readme}'],
         ok=V(exit=0, has=['clean'],
              hasnt=['continuity claim', 'not on the roll'])),

    case('note-check-refuses-a-variable-check-in-no-form', 'read-run.py',
         None,
         'CONTROL: a VARIABLE-CHECK line in none of its three forms is'
         ' refused with the line it sits on, not run as a command',
         plant=lambda t: {'note': note_for_the_check(
                              t, broken=False, vc='./run99-ghead diag'),
                          'readme': readme_with_a_registration(t)},
         argv=['--note-check', '{note}', '--readme', '{readme}'],
         ok=V(exit=1, has=['VARIABLE-CHECK reads `./run99-ghead diag`'],
              hasnt=['no VARIABLE-CHECK line'])),

    case('section-with-tables-refuses-a-number-past-the-end', 'read-run.py',
         None,
         'a table number past the section printed no table and exited 0,'
         ' which reads exactly like a section carrying none',
         plant=lambda t: {'doc': doc_with_a_table(t, 3)},
         argv=['--section', 'Middle', '--with-tables', '9',
               '--readme', '{doc}'],
         ok=V(exit=1, has=['9', '3 table'])),

    case('section-with-tables-bare-still-prints-every-table', 'read-run.py',
         None,
         'CONTROL: the number is optional and bare --with-tables is what it'
         ' was',
         plant=lambda t: {'doc': doc_with_a_table(t, 3)},
         argv=['--section', 'Middle', '--with-tables', '--readme', '{doc}'],
         ok=V(exit=0, has=['| a1 | b1 |', '| a2 | b2 |', '| a3 | b3 |'])),

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

    case('para-at-hands-back-a-usable-handle', 'read-run.py', None,
         'a grep gave a line number and `--para` wanted a lead, so sessions'
         ' paired `grep -n` with `sed -n` instead of either',
         # `--para` matches leads because a line number into prose does not
         # survive a rewrap or an `--in-place` install. What it could not
         # take was what a caller actually holds after grepping, which is
         # the number -- so the mode recommended and the thing in hand did
         # not meet, and the habit the mode exists to replace survived it.
         # This asks for line 3 on purpose: its lead is THREE words, below
         # the handle's old six-word floor, which left `short` unset and
         # printed `--para ''` -- a handle matching every paragraph in both
         # documents; and its first word is shared with two other leads, so
         # the handle has to lengthen until it names one. Both ends of the
         # same loop, in one case.
         plant=lambda t: {'readme': readme_of_leads(t)},
         argv=['--para-at', '{readme}:3', '--readme', '{readme}'],
         ok=V(exit=0,
              has=["handle: --para 'Alpha the first'", 'Body one'],
              hasnt=["--para ''", 'Body three'])),

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
                          'run': synth_json(t, 'rev')},
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

    case('two-modes-at-once-off-the-roll-call', 'read-run.py', '18021d0',
         'six modes late in the dispatch chain -- --stale, --brief-update,'
         ' --series, --cell-movers, --movement, --winsor -- were off the'
         ' one-mode roll call, so one beside another mode was dropped',
         # Six `if args.X: sys.exit(...)` branches of the same chain were
         # outside the roll call, so `--stale --lint` printed the stale
         # report at exit 0 and ran no lint -- the silent drop the comment
         # beside the list says it prevents.
         plant=lambda t: {'doc': edited_rundoc(t)},
         argv=['--stale', '--lint', '--run-doc', '{doc}'],
         ok=V(exit=2, has=['one mode at a time', '--stale', '--lint']),
         # The bug is the missing refusal and not an exit: --stale on a
         # fixture outside a git checkout exits 2 on its own account.
         bug=V(hasnt=['one mode at a time'])),

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

    case('superlative-worklist-names-its-settling-mode', 'read-run.py', None,
         'CONTROL: each superlative the sweep lists names the mode whose'
         ' sorted output settles it',
         # Run 34's checker and probe found a quantifier written without
         # the population sorted, again and again, each settled in the end
         # by one mode's output that the sweep had not named.
         plant=untracked_doc,
         argv=['--check-doc', '--worklists', '--readme', '{doc}'],
         ok=V(has=['settle by --cross-classes'])),

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
         '--aa died where other modes refuse, on the same file',
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
         # Over the newest run alone since 2026-09-18, as checks.py runs the
         # properties: over every run on disk this one case was 212 s of
         # the suite's 706, and the withheld line it asserts prints for
         # one run as for all.
         env={'CORPUS_RUN': 'newest'},
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
             'rundoc': relead(t, 'rev', lambda s: s.replace(
                 ', `rev-primes` (`l` 250357, `sInner` 89)', '')),
             'run': synth_run(os.path.join(t, 'rev.json'),
                              run_order_shapes('rev'))},
         argv=['{run}', '--block', '--run-doc', '{rundoc}'],
         ok=V(exit=0, has=['does not name `rev-primes`']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('lead-order-mislabels-the-per-shape-line', 'read-run.py', '3596ba2',
         'a lead listed its shapes in an order the installed line is not in',
         # The per-shape paragraph is installed IN RUN ORDER. It was
         # LABELLED *in the lead's order* until 2026-09-11, so a lead
         # listing them differently did not go stale, it mislabelled live
         # ratios. The label now names the run's order, which retires the
         # mislabelling; the notice below stays, a lead disagreeing with
         # the run still being worth saying. It fires at exit 0, which is
         # how Run 28 shipped `flip` disagreeing: printed, not read.
         plant=lambda t: {
             'rundoc': relead(t, 'rev', lambda s: s.replace(
                 '`rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3),'
                 ' `rev-gather48-src-50` (`l` 22500, `sInner` 3)',
                 '`rev-gather48-src-50` (`l` 22500, `sInner` 3),'
                 ' `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3)')),
             'run': synth_run(os.path.join(t, 'rev.json'),
                              run_order_shapes('rev'))},
         argv=['{run}', '--block', '--run-doc', '{rundoc}'],
         ok=V(exit=0, has=['it lists them `rev-gather48-src-50`,'
                           ' `rev-cnn-L1-24x24-c1`']),
         # No --audit: `--run-doc` postdates every commit this case could
         # replay against, so the older reader rejects the argv rather
         # than reproducing anything. The run-file split, 2026-08-25.
         ),

    case('lead-figures-disagree-with-main-hs', 'read-run.py', '3596ba2',
         'a lead\'s hand-copied `l` had no source but the lead',
         plant=lambda t: {
             'rundoc': relead(t, 'rev', lambda s: s.replace(
                 '`rev-primes` (`l` 250357', '`rev-primes` (`l` 250358')),
             'run': synth_run(os.path.join(t, 'rev.json'),
                              run_order_shapes('rev'))},
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
         plant=lambda t: {'run': synth_run(os.path.join(t, 'rev.json'),
                                           run_order_shapes('rev'))},
         argv=['{run}', '--block'],
         ok=V(exit=0, hasnt=['lead `rev`'])),

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

    case('carried-figures-misses-a-two-place-figure', 'read-run.py', None,
         'CONTROL: an item quoting a figure its own pair span cannot'
         ' produce is named, and one quoting none is not',
         # The figures a registration carries in are prose beside the
         # span, and nothing read them: --lint holds the ARMS to the
         # roster, --check-doc the anchors and widths, and a wrong number
         # beside a right arm passes both. This derives each `pair A B`
         # span on the runs given and asks whether any figure the item
         # quotes matches any derivation.
         # THE PATTERN'S PLACES ARE THE CASE. Written `\d.\d{3,4}` it
         # missed `1.16 to 1.36`, which is the two-place form the real
         # error was written in and the one figure this was built to
         # catch; `0.4242` here is four and `0.64` in the span is the
         # target, excluded as a prediction rather than a carried figure.
         plant=lambda t: dict(rundoc_carried_figures(t),
                              run=synth_json(t, 'main', name='a.json'),
                              other=synth_json(t, 'main', name='b.json')),
         argv=['{run}', '--carried', '--others', '{other}',
               '--run-doc', '{rundoc}'],
         ok=V(exit=0,
              has=['(1) quotes 0.4242',
                   '2 item(s) with a pair span, 1 quoting nothing it'
                   ' derives'],
              hasnt=['(2) quotes'])),

    case('no-mode-read-a-carried-over-registration', 'read-run.py',
         '84d82b5',
         'the carry-over comparison was hand-rolled, against the wrong copy',
         # NO CASE, and not for preflight's reason: this one would want a
         # git HISTORY with a registration moved out of README, which no
         # plant here builds. What IS covered is the splitter the mode
         # shares with registration_items, by
         # `predictions-enumerates-items-twice`; what is not is the history
         # walk, and its three wrong drafts are worth naming here because a
         # rewrite meets all three again. `git log -S` finds nothing, the
         # README being wrapped and the lead straddling a break in every
         # blob. The pathspec for `log` is CWD-relative where `REV:path` is
         # repo-relative, and mixing them returns no commits, silently. And
         # the walk is NEWEST first: bounding it by the run file's birth
         # looks right and is not, step 5 writing that file, so every state
         # carrying the lead is at or before it -- that draft walked past
         # Run 29 to Run 22 and reported its items as Run 22's, which is a
         # wrong answer where a refusal was owed.
         argv=None, ok=None),

    case('carried-prints-every-derivation-not-a-shortlist', 'read-run.py',
         'e5c08d1',
         'a flagged item listed its span on every population handed in',
         # The README line this mode runs under promises `a shortlist to
         # read`, and it printed the span derived on every JSON given:
         # eleven populations on two halves is twenty-two derivations on
         # ONE line, so the mode's output buried the item it was flagging.
         # Run 30's preparation read four such lines and the near-matches
         # that mattered -- 0.7433 against a quoted 0.7425 -- sat somewhere
         # in the middle of them. The nearest few come first now.
         # The judge hands it eight controls so the flagged item derives
         # past the six the shortlist keeps, and asks for the count the cap
         # prints. The control above keeps the warning itself honest; this
         # one keeps its SIZE honest, which no other case reads.
         plant=lambda t: dict(rundoc_carried_figures(t),
                              run=synth_json(t, 'main', name='a.json'),
                              o1=synth_json(t, 'main', name='b.json'),
                              o2=synth_json(t, 'main', name='c.json'),
                              o3=synth_json(t, 'main', name='d.json'),
                              o4=synth_json(t, 'main', name='e.json'),
                              o5=synth_json(t, 'main', name='f.json'),
                              o6=synth_json(t, 'main', name='g.json'),
                              o7=synth_json(t, 'main', name='h.json'),
                              o8=synth_json(t, 'main', name='i.json')),
         argv=['{run}', '--carried', '--others', '{o1}', '{o2}', '{o3}',
               '{o4}', '{o5}', '{o6}', '{o7}', '{o8}',
               '--run-doc', '{rundoc}'],
         ok=V(exit=0, has=['(1) quotes 0.4242',
                           'more (--verbose for all)']),
         bug=V(exit=0, has=['(1) quotes 0.4242'],
               hasnt=['more (--verbose for all)'])),

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

    case('predictions-calls-every-floor-the-main-set-one', 'read-run.py',
         None,
         'the tolerance line naming the population its floor came from',
         # The VALUE was always right -- floor_pct is derived from the
         # JSON handed in, so 0.52% on `small` and 2.89% on `runs` -- and
         # the label said main-set for all of them. A span read on a class
         # then looks like a main-set verdict, which is how Run 26's
         # registration (1) read as HELD by the mode and KILLED by the
         # write-up, both correct, and cost a session an hour deciding
         # they contradicted each other (2026-09-06).
         plant=lambda t: dict(rundoc_registration_with_verdicts(t),
                              run=synth_json(t, 'small', name='a.json'),
                              other=synth_json(t, 'small', name='b.json')),
         argv=['{run}', '--compare', '{other}', '--predictions',
               '--run-doc', '{rundoc}'],
         ok=V(has=['A/A floor of the population read'],
              hasnt=['main-set A/A floor'])),

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

    # THE BAR A CROSS-FILE FIGURE IS READ AGAINST, and the mode printed
    # none until 2026-09-15. `--aa` gives the floor WITHIN one half; a
    # figure ACROSS two files had no counterpart, so a pair's headline was
    # written against nothing. Run 32 called the compiler worth nothing
    # this roster can measure and three of eight strategies clear the bar
    # its own A/A copies set. Two synthetic runs read A/A at exactly 1, so
    # the bar is 0.00% and NOTHING clears it -- which is the clean-run
    # direction, and the clause it prints is the one a reader needs when a
    # comparison has nothing to claim.
    case('compare-prints-no-aa-bar', 'read-run.py', None,
         'a cross-file figure had no bar of its own to be read against',
         plant=lambda t: {'run': synth_json(t, 'main', name='a.json'),
                          'other': synth_json(t, 'main', name='b.json')},
         argv=['{run}', '--compare', '{other}'],
         ok=V(exit=0,
              has=['A/A bar for this comparison',
                   "nothing here is this comparison's to claim"])),

    # AND THE OTHER DIRECTION, which is the one a real pair has: an arm
    # skewed on one shape in one file alone moves further than the bar and
    # is NAMED, where the twins still agree. Without the naming the line
    # would be a number a reader has to apply by hand, which is what a
    # session did to get Run 32's head wrong.
    case('compare-names-no-arm-past-the-bar', 'read-run.py', None,
         'the bar was a figure with no arms measured against it',
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json'),
             'other': synth_json(t, 'main', name='b.json',
                                 skew=[(main_shapes()[0], 'lib-stage1', 4)])},
         argv=['{run}', '--compare', '{other}'],
         ok=V(exit=0,
              has=['A/A bar for this comparison',
                   'move further than the bar', 'lib-stage1'],
              hasnt=["nothing here is this comparison's to claim"])),

    # THE PUBLISHED COLUMN AGAINST ITSELF ACROSS TWO RUNS. `time` is a
    # winsorized geomean whose cap is that row's own and that run's own, so
    # one row's two published figures divide to the arm's movement only
    # where the cap did not move under them. Run 31 published
    # `lib-stage2-lean-u1` at 0.029 and Run 32 at 0.025 -- fourteen points
    # on an arm that moved 1.6 -- and the chapter forbade dividing two ROWS
    # of one table while saying nothing about one row down two runs. The
    # fixture skews ONE cell of one arm far out in one file: that widens
    # the row's MAD there and caps nothing, where the unskewed file caps
    # the same cells to a tighter ceiling, so the two published figures
    # part while the paired ratio does not.
    case('compare-does-not-flag-column-drift', 'read-run.py', None,
         "one row's two published figures divided to what no arm did",
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json'),
             'other': synth_json(t, 'main', name='b.json',
                                 skew=[(main_shapes()[0], 'lib-stage1', 40),
                                       (main_shapes()[1], 'lib-stage1', 30)])},
         argv=['{run}', '--compare', '{other}'],
         ok=V(exit=0,
              has=['published-column drift', 'column', 'against paired',
                   'lib-stage1'])),

    # WHAT THE COLUMN OWES ITS OWN ESTIMATOR, per row. The gap was
    # reimplemented by hand on 2026-09-15 to establish it, which is the
    # day this mode was asked for; a row whose cells are capped reads a
    # published figure its cells do not average to, and only this says so.
    case('winsor-does-not-say-what-the-cap-moved', 'read-run.py', None,
         'the published column hid how much of itself was the estimator',
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json',
                               skew=[(main_shapes()[0], 'lib-stage1', 40),
                                     (main_shapes()[1], 'lib-stage1', 30)])},
         argv=['{run}', '--winsor'],
         ok=V(exit=0,
              has=['winsorizing, per timed row', 'plain', 'published',
                   'capped', 'lib-stage1'])),

    case('block-compare-writes-what-the-class-says', 'read-run.py', None,
         'CONTROL: --block --compare with both sweeps prints the class'
         ' paragraph\'s figures with `___` where the finding goes',
         # Run 34 wrote ten such paragraphs, each restating the verdict
         # lines, the cross-half line and the counts comparison by hand.
         plant=lambda t: {
             'a': synth_json(t, 'bcast', name='a.json'),
             'b': synth_json(t, 'bcast', name='b.json'),
             'ca': synth_counts(t, 'ca.txt', cheap_sum_only=True,
                                shapes=class_shapes('bcast')),
             'cb': synth_counts(t, 'cb.txt', cheap_sum_only=True,
                                shapes=class_shapes('bcast'))},
         argv=['{a}', '--block', '--brief', '--compare', '{b}', '--counts',
               '{ca}', '{cb}'],
         ok=V(exit=0, has=['**What the class says:** property 1',
                           'A/A bar of', 'counts geomean of 1.0000', '___'])),

    case('winsor-censuses-the-pairs-that-part-in-sign', 'read-run.py', None,
         'CONTROL: --winsor counts the pairs of timed rows whose column'
         ' ratio and paired geomean part in sign, and names the widest'
         ' disagreement',
         # Run 34 wrote `DO NOT DIVIDE` over a census it took by hand, and
         # a sentence about which pairs part in sign is a superlative over
         # every pair, which no mode sorted.
         plant=lambda t: {
             'run': synth_json(t, 'main', name='a.json',
                               skew=[(main_shapes()[0], 'lib-stage1', 40),
                                     (main_shapes()[1], 'lib-stage1', 30)])},
         argv=['{run}', '--winsor'],
         ok=V(exit=0, has=['pair(s) of timed rows', 'part in sign',
                           'the widest disagreement'])),

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

    case('replace-takes-an-abutting-table', 'read-run.py', '931d558',
         'a paragraph that abuts its installed table took the table with it',
         # The heading case above is the same shape and this is its third
         # instance. Every class block in a run file is a bolded lead with
         # its table on the next line and no blank between them, which
         # `--block --in-place` writes that way, so an anchor naming the
         # lead carries the table into the replacement. Run 29's write-up
         # lost the `flip` class's 38 rows that way at exit 0 --- and
         # `--check-doc` PASSED immediately after, which the heading case
         # cannot say: a gate holds a table it finds to the JSONs and
         # cannot miss one that is gone. Recovered from the previous
         # commit and re-installed. The `out, last` line named a table row
         # where prose belonged, which is how it was caught, and saying so
         # was not enough --- the difference this guard is the third of.
         plant=lambda t: {
             'doc': write(os.path.join(t, 'doc.md'),
                          '# T\n\nkeep me\n\nthe planted lead\n'
                          '| strategy | time |\n|---|---:|\n'
                          '| list | 1.000 |\n\nafter\n'),
             'readme': write(os.path.join(t, 'other.md'), '# other\n'),
             'new': write(os.path.join(t, 'new.txt'), 'replacement\n')},
         argv=['--replace', 'the planted lead', '--with', '{new}',
               '--run-doc', '{doc}', '--readme', '{readme}'],
         ok=V(exit=1, has=['table'], hasnt=['chars ->']),
         bug=V(exit=0, has=['chars ->'])),

    case('para-traceback-on-a-bracketed-lead', 'read-run.py', None,
         'a lead pasted verbatim is retried as a literal instead of'
         ' raising or matching nothing',
         # --para compiles its argument as a regex and the chapter tells a
         # session to locate a paragraph by its bolded lead. Every
         # registration item's lead carries brackets: pasted whole it
         # COMPILES and matches nothing at exit 0, and truncated to an
         # unbalanced bracket it raises re.error with a Python stack. Run
         # 30 met the traceback and recorded the silent half only after
         # testing its own reproducer, which did not reproduce.
         plant=lambda t: {
             'doc': write(os.path.join(t, 'doc.md'),
                          '# T\n\n**(9) *The floor for a second run.* '
                          'the planted body\n'),
             'readme': write(os.path.join(t, 'other.md'), '# other\n')},
         argv=['--para', '(9) *The floor for a second run.*',
               '--run-doc', '{doc}', '--readme', '{readme}'],
         ok=V(exit=0, has=['the planted body'])),

    case('para-refuses-an-uncompilable-pattern', 'read-run.py', None,
         'an unbalanced bracket falls back to the literal instead of'
         ' raising a Python stack',
         # `--para '(11'` is what truncating a registration lead gives, and
         # it raised `re.error: missing ), unterminated subpattern` out of
         # the compile. It now matches literally; where that finds nothing,
         # the ordinary `no paragraph` is the answer and the stack is gone.
         plant=lambda t: {
             'doc': write(os.path.join(t, 'doc.md'), '# T\n\n**a lead\n'),
             'readme': write(os.path.join(t, 'other.md'), '# other\n')},
         argv=['--para', '(11', '--run-doc', '{doc}', '--readme', '{readme}'],
         ok=V(exit=1, has=['no paragraph'], hasnt=['Traceback'])),

    case('carried-note-does-not-name-inherited', 'read-run.py', None,
         'the carried-paragraph note names --inherited, the mode that'
         ' lists what it is counting',
         # The note counts the paragraphs a run carried whole and names no
         # way to see them; --inherited is that way and is named only in
         # the post list, mid-paragraph. Run 30 read the paragraph, missed
         # the command, wrote its head without it, and had a checker pass
         # return twelve stale carried paragraphs -- every one of which
         # that one command lists. A count with no route to its own
         # members is the shape this record is about.
         plant=rundoc_pair_with_carried_body_claim,
         argv=['--check-doc', '--worklists', '--run-doc', '{rundoc}'],
         ok=V(has=['--inherited'])),

    case('stale-names-a-word-numeral-in-its-default-view', 'read-run.py',
         None,
         'a figure kept as a WORD reaches the default view, two of the four'
         ' this mode was written for being words',
         # The mode's first tiers led with digits alone, so `thirty-four
         # rows` and `ten consumers` -- two of the four figures Run 35
         # shipped stale, and half its own justification -- sat in the
         # bucket only --all prints while the docstring said it printed
         # them. Found by re-opening that claim rather than by any gate:
         # nothing here could have caught a mode whose output matched its
         # code and not its purpose. `one` to `nine` stay out, being prose.
         plant=lambda t: stale_pair(t, word=True),
         argv=['--stale', '--run-doc', '{doc}'],
         ok=V(exit=0, has=['thirty', '1 edited paragraph(s)'],
              hasnt=['1 more keep only'])),

    # THE ONLY READING THAT SEES A DELETION. Every gate here is a
    # predicate over what is PRESENT, so a paragraph a scripted edit
    # removed leaves its neighbours joining seamlessly and passes all of
    # them -- the failure the user-scope CLAUDE.md records from orthotope,
    # where a removed paragraph left --lint, --check-doc and a purpose-built
    # truncation check all exiting 0. Post-run step 6e asks for this
    # comparison and supplied no tool until 2026-09-22, so every run
    # hand-rolled it; Run 38 wrote the script twice in one session.
    case('lost-paragraph-is-reported-and-a-rewritten-one-is-not',
         'read-run.py', 'a40f7b8',
         'a paragraph a scripted edit removed passed every gate here',
         plant=lost_pair,
         argv=['--lost', '--run-doc', '{doc}'],
         ok=V(exit=0, has=['1 WENT BY COUNT', 'The regime was confirmed'],
              hasnt=['straddling loops',
                     'no paragraph went by count in either document']),
         # Before the mode there was nothing to run: argparse refuses the
         # flag, which is what `every gate here` amounted to.
         bug=V(exit=2, hasnt=['WENT BY COUNT'])),

    # The control: the same edit with nothing removed, on which the mode
    # must find nothing -- a rewritten lead over the same body is
    # `--stale`'s subject and not this one's.
    case('lost-names-no-paragraph-when-none-went', 'read-run.py', None,
         'a mode that reported every edited paragraph would report nothing',
         plant=lambda t: lost_pair(t, deleted=False),
         argv=['--lost', '--run-doc', '{doc}'],
         ok=V(exit=0, has=['none went by count',
                           'no paragraph went by count in either document'])),

    case('brief-update-refuses-a-brief-it-cannot-place', 'read-run.py',
         None,
         'the brief is left byte for byte when one of its two THIS RUN'
         ' ONLY items is not there to replace',
         # The brief's two run-specific items are the half that goes stale,
         # and a stale brief looks exactly like a used one: both checker
         # passes read it as given and neither can tell its figures are the
         # run before's. Writing what it can would leave one item this
         # run's and one the last run's, which no reader of the brief can
         # see and which is worse than leaving both stale -- so a brief
         # missing item 6 is refused whole, with the brief untouched. The
         # control below is the same call on a brief carrying both.
         plant=lambda tmp: brief_pair(tmp, whole=False),
         argv=['--brief-update', '{run}', '--brief-dir', '{dir}'],
         ok=V(exit=2, has=['no ` 5. THIS RUN ONLY`', 'untouched']),
         probe=lambda subs: open(subs['brief']).read()),

    case('brief-update-writes-the-substitution-block', 'read-run.py', None,
         'RUN, BASIS, OTHER and PREV are written from pair-halves.sh, which'
         ' the docstring promised and the code did not do',
         # The mode wrote the two items and nothing else while its
         # docstring, the chapter line naming it and its commit message all
         # said it wrote the block too. No gate could see it: the output
         # matched the code. Found by re-opening the claim. The fixture
         # plants a block naming another run, and every driver reads the
         # halves through pair-halves.sh, so this does too.
         plant=lambda t: brief_pair(t, stale_block=True),
         argv=['--brief-update', '{run}', '--brief-dir', '{dir}'],
         ok=V(exit=0, has=['substitution block', 'RUN=run97'],
              hasnt=['RUN=run11'])),

    case('brief-update-writes-both-items', 'read-run.py', None,
         'both THIS RUN ONLY items come from the facts file, and the'
         ' `<yours>` slots left in them are named',
         # The control for the refusal above, and the mode's own purpose:
         # the chapter has said since 2026-09-05 that these items are
         # pasted and not retyped, and the pasting was the step nothing
         # checked.
         plant=brief_pair,
         argv=['--brief-update', '{run}', '--brief-dir', '{dir}'],
         ok=V(exit=0, has=['items 5 and 6 written'])),

    case('brief-update-replaces-each-item-whole', 'read-run.py', '14dc173',
         'the paste replaced each item\'s header line alone, so the old'
         ' item\'s indented body stood under the new one, one layer a run',
         # Found by Run 39's first checker pass, 2026-09-23: items 5 and 6
         # carried Runs 36 to 39's blocks one under another, the brief
         # having been pasted into four times.
         plant=lambda t: brief_pair(t, bodied=True),
         argv=['--brief-update', '{run}', '--brief-dir', '{dir}'],
         probe=lambda subs: open(subs['brief']).read(),
         ok=V(has=['One window', 'THE NEXT SECTION stays'],
              hasnt=["last run's body"]),
         bug=V(has=["last run's body"])),

    case('replace-refusal-does-not-name-delete', 'read-run.py', None,
         'the table refusal names --delete, the mode that removes the'
         ' table it is refusing to take',
         # The refusal told a caller to `replace the prose above it by
         # quoting only that`, which is exactly what leaves the old table
         # standing BELOW the new one: Run 30 did it twice, to the
         # two-column table and to the Provenance anchors, and read both
         # duplicates back out of --inherited hours later. A message that
         # names the next step is the cheapest guard there is, and this one
         # named the step that produces the defect.
         plant=lambda t: {
             'doc': write(os.path.join(t, 'doc.md'),
                          '# T\n\nkeep me\n\nthe planted lead\n'
                          '| strategy | time |\n|---|---:|\n'
                          '| list | 1.000 |\n\nafter\n'),
             'readme': write(os.path.join(t, 'other.md'), '# other\n'),
             'new': write(os.path.join(t, 'new.txt'), 'replacement\n')},
         argv=['--replace', 'the planted lead', '--with', '{new}',
               '--run-doc', '{doc}', '--readme', '{readme}'],
         ok=V(exit=1, has=['--delete'])),

    case('carried-body-paragraph-calls-itself-this-runs', 'read-run.py',
         '1da8c56',
         'a run file went green with thirty carried paragraphs in its body',
         # The head's refusal is by POSITION. Run 29 cleared the head, this
         # gate went green, and thirteen of its checker's twenty-six
         # findings were carried paragraphs in the body -- among them a
         # cross-run paragraph every figure of which was the run before's,
         # and one asserting that the two columns MAY be differenced where
         # the run's whole finding is that they may not. What parts a stale
         # paragraph from the apparatus is what it says about itself, not
         # where it sits: `this run` is a claim about the run in front of
         # it and `Run 8 re-ran every class` is the standing apparatus, so
         # the body is gated on the narrow predicate and `--inherited`
         # keeps the wide one as a reading.
         plant=rundoc_pair_with_carried_body_claim,
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['call themselves this run', 'zz-carried-claim']),
         bug=V(hasnt=['call themselves this run'])),

    case('cells-stdout-is-tsv-alone', 'read-run.py', '1da8c56',
         'the TSV mode printed a banner and a blank line above its header',
         # The post-run list sends a caller to `--cells` precisely so a
         # figure is not read by counting fields off a human table -- and
         # then this mode put two lines above its own header, so the naive
         # read the rule invites finds the banner. Run 29's write-up parsed
         # it twice at the wrong offset, once taking line 1 for the header
         # and once line 2. Every mode still says its population in its
         # first line; under `--cells` alone that line goes to stderr, so
         # stdout is a header and its rows.
         plant=lambda t: {'run': synth_json(t, 'main')},
         argv=['{run}', '--cells'],
         probe=lambda subs: 'FIRSTLINE: ' + subprocess.run(
             [str(subs['prog']), str(subs['run']), '--cells'],
             capture_output=True, text=True).stdout.split('\n')[0][:22],
         ok=V(has=['FIRSTLINE: shape\tstrategy']),
         bug=V(hasnt=['FIRSTLINE: shape'])),

    case('block-names-the-summary-s-bold-column', 'read-run.py', '1da8c56',
         'which column the cross-class summary bolds was picked by eye',
         # The summary emphasises the faster of its two named arms and the
         # rule is that the emphasis follows the COLUMN -- which prints
         # three decimals, where the two tie often: four of Run 29's ten
         # rows did. Run 28 broke such a tie with `--pair`, a different
         # statistic, and got `rev` the wrong way round. `--block` reads
         # the column at full precision now and says so, and says when the
         # print cannot show why. The ceiling ARM got this same line on
         # 2026-09-01 for the same reason, one column across.
         plant=lambda t: {'run': synth_json(t, 'rev')},
         argv=['{run}', '--block', '--brief'],
         ok=V(has=['summary bolds']),
         bug=V(hasnt=['summary bolds'])),

    case('head-is-three-paragraphs', 'read-run.py', None,
         'CONTROL: a run file whose head runs past three paragraphs is'
         ' refused, the gate, window and the rest being Provenance\'s',
         # Run 34's head was twenty-one paragraphs, most restating
         # Provenance or a class block, and every restatement a site two
         # figures could disagree across.
         plant=lambda t: {'rundoc': rundoc_with_a_long_head(t)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['head carries %d paragraphs'
                           % (_reader().HEAD_PARAGRAPHS + 1)])),

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

    case('paragraph-that-begins-mid-sentence-fails', 'read-run.py',
         '4a1793a',
         'a paragraph that lost its opening words passed every gate',
         # Run 22's write-up left the anchors paragraph beginning `anchors
         # read`, and --check-doc, which read how a paragraph ENDS and never
         # how one begins, passed it; Run 23 found it by reading. Planted
         # the same way on the Provenance lead every run file carries.
         plant=lambda t: {'rundoc': plant_begins_mid_sentence(t)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['begin mid-sentence']),
         bug=V(exit=0, hasnt=['begin mid-sentence'])),

    case('paragraph-cut-before-a-heading-fails', 'read-run.py',
         '4a1793a',
         'a paragraph cut mid-sentence passed when a heading followed it',
         # The stop check excused a paragraph whose next block was not
         # prose, meaning a sentence running into an indented code sample
         # or a table -- and counted a heading and a link reference as not
         # prose too, so the closing paragraph of every section went
         # unchecked. Found 2026-09-26 by planting a cut on Run 41's last
         # Provenance paragraph. Planted on the apparatus paragraph every
         # run file carries before its class section.
         plant=lambda t: {'rundoc': plant_cut_before_heading(t)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['stop mid-sentence']),
         bug=V(exit=0, hasnt=['stop mid-sentence'])),

    case('vecdims-arms-name-the-summary-column', 'read-run.py',
         '26816e6',
         "`family` named both an arm with its A/A copies and the"
         " `mut-odo-vecdims` group whose best outside arm the cross-class"
         " summary reads",
         # Run 38's comprehension probe found the two senses in one run
         # file, and the ruling of 2026-09-26 kept `family` for an arm with
         # its copies: the group is `the vecdims arms`, and the column,
         # the ceiling line and the class verdicts say so.
         argv=['--unit', 'SUMMARY_COLS[3]'],
         ok=V(has=['best outside vecdims']),
         bug=V(has=['best outside family'])),

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
         ok=V(has=['ceiling (vecdims)    mut-odo-vecdims'],
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

    # The exit span and the entry count, worked by hand above the two
    # fixtures. The first is the plain form's own reading of the fill's
    # shape and is what Run 32's HEAD half paid for: a control kept so the
    # flag's case proves a difference and not a coincidence.
    case('deadspot-leaves-the-exit-astride', 'align-as.py', None,
         'the body fits, the exit does not, and the plain cost is content',
         plant=asm_exit, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after jmp\t*(%rbp): .p2align\t6, 0x90, 50'],
              hasnt=['exit span(s) astride'])),

    case('exitspan-moves-the-exit-off-the-boundary', 'align-as.py', None,
         'the exit span raises the budget and the head goes to 0',
         plant=asm_exit, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_EXITSPAN': '1', 'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after jmp\t*(%rbp): .p2align\t6, 0x90, 55',
                           '0 exit span(s) astride',
                           '2 head(s) the exit cost places at a residue the'
                           ' plain cost would not: .Lin, .Lout'])),

    case('exitspan-pads-the-cut-the-entries-keep', 'align-as.py', None,
         'a cut leaving whole entries on both sides, priced by lines',
         plant=asm_entries, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_EXITSPAN': '1', 'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after jmp\t*(%rbp): .p2align\t6, 0x90, 54',
                           '0 exit span(s) astride'])),

    case('entries-keep-the-cut-the-exitspan-pads', 'align-as.py', None,
         'the same cut priced by entries, and the head stays',
         plant=asm_entries, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_ENTRIES': '1', 'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after jmp\t*(%rbp): .p2align\t6, 0x90, 28',
                           '1 exit span(s) astride',
                           '1 head(s) the entries cost places at a residue the'
                           ' exit cost would not: .Lin'])),

    case('blockrules-keep-what-the-exit-span-pads', 'align-as.py', None,
         'the same cut priced by the block rules, and the head stays',
         plant=asm_entries, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_BLOCKRULES': '1', 'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after .text: .p2align\t6, 0x90, 48',
                           'before .Lin: jmp\t*(%rbp)',
                           '1 head(s) the blocks cost places at a residue'
                           ' the exit cost would not: .Lin'])),

    case('exitspan-reads-no-exit-after-a-jmp-back-edge', 'align-as.py', None,
         'a dead block after an unconditional back edge was the exit span',
         plant=asm_jmp_back, probe=emitted,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_EXITSPAN': '1', 'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['after jmp\t*(%rbp): .p2align\t6, 0x90, 25'],
              hasnt=['.p2align\t6, 0x90, 34'])),

    case('cost-flags-want-the-dead-spot-form', 'align-as.py', None,
         'a cost of the planner asked for without the planner',
         plant=asm,
         env={'REAL_AS': '{as}', 'LOOP_EXITSPAN': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         # Refused in one line at import, as a non-number is, and not
         # implied: a switch that switched another on would be a default,
         # and a pair's note records no default.
         ok=V(exit=1, has=['want LOOP_DEADSPOT=1 beside them'],
              hasnt=['Traceback'])),

    # ---- the settled plan, LOOP_SETTLED=1 (2026-09-22) -------------------
    # Four controls guarding the switch forward, each against the block
    # rules it builds on: the back edge's three rules, the spot no jump
    # crosses, and the rounds that plan again what the pad moved.
    case('settled-charges-the-back-edge', 'align-as.py', None,
         "the back edge on a 16-byte boundary, in a line's first eight bytes"
         ' or its last four, charged where the block rules charge nothing',
         plant=asm_pair,
         # The pair's inner back edge sits 45 bytes from its head: residues
         # 2 and 3 put it across or on the boundary at 48, 15 to 18 in the
         # line's last four bytes, 19 on the line's end, 20 to 26 in the
         # next line's first eight, 34 and 35 and 50 and 51 on 80 and 96.
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_SETTLED': '1', 'ALIGN_AS_VERBOSE': '1',
              'LOOP_TRACE': '.Lin'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['block-rule costly residues [18, 19, 20, 21, 56,'
                           ' 57, 58, 59, 60, 61, 62, 63]',
                           'settled costly residues [2, 3, 15, 16, 17, 18,'
                           ' 19, 20, 21, 22, 23, 24, 25, 26, 34, 35, 50, 51,'
                           ' 56, 57, 58, 59, 60, 61, 62, 63]',
                           'settled in 1 round(s), 0 group(s) planned again'])),

    case('blockrules-take-the-spot-the-budget-prefers', 'align-as.py', None,
         'the far spot, crossed by two jumps, wins on budget alone',
         plant=asm_crossed,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_BLOCKRULES': '1', 'ALIGN_AS_VERBOSE': '1',
              'LOOP_TRACE': '.Lin'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['spots at lines [40, 43], chosen spot line 40'])),

    case('settled-takes-the-spot-fewer-jumps-cross', 'align-as.py', None,
         'the same group under the settled plan: the nearer spot, one'
         ' jump across it against two',
         plant=asm_crossed,
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_SETTLED': '1', 'ALIGN_AS_VERBOSE': '1',
              'LOOP_TRACE': '.Lin'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['spots at lines [40, 43], chosen spot line 43',
                           'settled in 1 round(s), 0 group(s) planned again'])),

    case('settled-plans-again-what-the-pad-moved', 'align-as.py', None,
         'a pad that grows the jump across it is read off the assembler'
         ' and the group planned again with the shift',
         plant=asm_crossed,
         # Pinned at 15 so that the grown jump lands the head on a costly
         # residue, 19, which the free plan above happens to dodge.
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_SETTLED': '1', 'ALIGN_AS_VERBOSE': '1',
              'LOOP_PIN': '.Lin:15'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['settled in 2 round(s), 1 group(s) planned again'],
              hasnt=['still off the plan', 'Traceback'])),

    case('planned-straddles-are-heads-in-every-cost', 'align-as.py', '6798792',
         'the planned count was the chosen cost truncated, cycles under the'
         ' block rules',
         plant=asm_pair,
         # The rotated pair's outer head yields and straddles under every
         # cost; the verified count said so and the planned one agreed
         # only under the plain cost, where the cost IS the count.
         env={'REAL_AS': '/usr/bin/gcc', 'LOOP_DEADSPOT': '1',
              'LOOP_BLOCKRULES': '1', 'ALIGN_AS_VERBOSE': '1'},
         argv=['-c', '-o', '{obj}', '{asm}'],
         ok=V(exit=0, has=['1 short loop(s) straddling (1 planned)']),
         bug=V(has=['1 short loop(s) straddling (0 planned)'])),

    # ---- probe-nospill-fills.py ---------------------------------------
    case('fills-entry-region-goes-to-the-previous-proc',
         'probe-nospill-fills.py', 'ef3085d',
         'a loop in an LLVM function\'s entry region credited to the previous proc',
         # A `.LBB` block inherits the last `_blk_` owner seen, and the
         # reset on `.size` never fired, the directive being
         # tab-indented; a function's entry label was no owner at all.
         # LLVM rotates each worker's loop into exactly that region,
         # so on 2026-09-05 `-u2`'s loop was read under `-u1` and the
         # six-instruction loops under nothing.
         plant=plant_fills_entry_region,
         argv=['{dump}', '{asm}', 'fbA', 'fbB'],
         ok=V(exit=0, has=['QB/.LBB2_1:'], hasnt=['QA1/.LBB2_1:']),
         bug=V(has=['QA1/.LBB2_1:'], hasnt=['QB/.LBB2_1:'])),

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

    case('offsets-refuses-a-match-only-flag', 'loop-offsets.py', None,
         '--loose or --source without --match, read by nobody',
         # The family the --len-under-survey case guards, for the two knobs
         # --match brought: both are consulted inside that report alone, so
         # anywhere else they would be accepted and honoured by nobody. The
         # refusal fires in the dispatch, before any binary is opened.
         argv=['--loose', 'x'],
         ok=V(exit=2, has=['read by --match alone'])),

    # SEVERAL PAIRS IN ONE CALL, and an ODD count refused rather than the
    # last binary paired with nothing. `--library` took exactly two until
    # 2026-09-15, so re-deriving the whole surviving series -- which its
    # own open entry asks for, the recorded per-run figures and today's
    # reading disagreeing -- was a shell loop, and the one a session wrote
    # timed out. The refusal fires in the dispatch, before any binary is
    # opened, so the names need not exist.
    case('offsets-library-takes-an-odd-count', 'loop-offsets.py', None,
         '--library paired the last binary with nothing',
         argv=['--library', 'x', 'y', 'z'],
         ok=V(exit=2, has=['two at a time', 'even number'])),

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

    case('survey-truncates-its-straddler-listing-without-saying-so',
         'loop-offsets.py', '55216ae',
         'ten sites under a count of eleven read as the whole of them, on'
         ' both listings',
         plant=listing_with_eleven_straddlers,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['still straddling   : 11, 10 longest listed',
                           'exit spans astride : 11, 10 longest listed']),
         bug=V(exit=0, has=['still straddling   : 11'],
               hasnt=['longest listed'])),

    case('survey-reads-a-saved-listing', 'loop-offsets.py', '8b4f51d',
         'a site of a dead binary could not be held: objdump was the only'
         ' way in, and a listing of the site was refused as no ELF',
         plant=phantom_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['self-loops of at most 64 B']),
         bug=V(exit=1, has=['file format not recognized'])),

    case('survey-counts-a-data-word-as-a-loop', 'loop-offsets.py', '8b4f51d',
         'an info-table word decoding as a backward branch, over bytes that'
         ' happened to sum, was counted as a straddling self-loop',
         # NOT AUDITED: the reader before the fix takes ELF alone, and the
         # binary this was read on dies at the deletion offer. Watched by
         # hand on 2026-09-04, on run25-g912 against its -g3 twin: five
         # straddling against four, the fifth refused by byte identity, and
         # the same word reading `js -123` in run24-g912, past the cap.
         plant=phantom_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['still straddling   : 0'], hasnt=['0x4275f6']),
         no_audit='fixture-from-a-document-the-era-lacks'),

    case('survey-counts-a-table-body-as-a-loop', 'loop-offsets.py', '6040630',
         'an info table whose own words are the body -- zero bytes and a'
         ' type word, closed by the word after them read as `js` -- counted'
         ' as a straddling self-loop, both existing guards admitting it',
         # It reached Run 28's pair note as one of the basis half's three
         # refusals, recorded as a loop nobody could name. Nothing branches
         # to the head but that `js`, and the code before it ends in an
         # indirect jump and a pad.
         plant=phantom3_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['still straddling   : 0'], hasnt=['0x41c9fc']),
         bug=V(exit=0, has=['still straddling   : 1', '0x41c9fc'])),

    case('survey-counts-a-swallowed-jump-as-a-loop', 'loop-offsets.py', '71fac05',
         'a continuation the sweep decoded out of step, its own jump'
         ' displacement reading as a backward branch, was counted as a'
         ' straddling self-loop that straight-line flow reaches',
         plant=phantom2_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['still straddling   : 0'], hasnt=['0x42c660']),
         bug=V(exit=0, has=['still straddling   : 1', '0x42c660'])),

    case('survey-counts-no-exit-span', 'loop-offsets.py', '0b170a9',
         'the survey counted bodies astride a line and not exit spans, so'
         ' the one placement LOOP_EXITSPAN moves had no reading off the'
         ' binary, only off a rebuild under ALIGN_AS_VERBOSE',
         plant=exitspan_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['exit spans astride : 1', '0x430b89'],
              hasnt=['exit span 57 B']),
         bug=V(exit=0, hasnt=['exit spans astride'])),

    case('survey-counts-a-nop-pad-table-word-as-a-loop', 'loop-offsets.py',
         '0b170a9',
         'a nopl pad and the table word after it, read as a six-byte'
         ' self-loop, counted as an exit span astride where the shim'
         ' counted none',
         plant=phantom4_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['0 self-loops of at most 64 B'],
              hasnt=['0x4968a4']),
         bug=V(exit=0, has=['1 self-loops of at most 64 B'])),

    case('survey-counts-a-return-address-word-as-a-loop', 'loop-offsets.py',
         'e4f0624',
         "an info table's last byte and the continuation push after it,"
         ' read as a seven-byte self-loop at offset 63, counted straddling'
         ' and astride where the shim counted neither',
         plant=phantom5_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['0 self-loops of at most 64 B'],
              hasnt=['0x41f93f']),
         bug=V(exit=0, has=['1 self-loops of at most 64 B'])),

    case('survey-counts-a-table-word-pair-as-a-loop', 'loop-offsets.py',
         'b1a488d',
         'two zero bytes of an info table and the low bytes of the word'
         ' after them, read as a four-byte self-loop and counted astride'
         ' where the shim counted none',
         plant=phantom6_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['0 self-loops of at most 64 B'],
              hasnt=['0x4a4832']),
         bug=V(exit=0, has=['1 self-loops of at most 64 B'])),

    case('survey-counts-a-two-byte-pad-and-its-table-word-as-a-loop',
         'loop-offsets.py', 'b1a488d',
         'a two-byte pad after an unconditional jump, xchg %ax,%ax, and'
         ' the table word after it, read as a four-byte self-loop and'
         ' counted astride where the shim counted none',
         plant=phantom7_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['0 self-loops of at most 64 B'],
              hasnt=['0x43f256']),
         bug=V(exit=0, has=['1 self-loops of at most 64 B'])),

    case('survey-counts-an-x87-decode-of-a-jump-as-a-loop',
         'loop-offsets.py', 'b173873',
         "a continuation's mov and jmp read one byte out of step after an"
         ' info table, fsubrp and jo -4, read as a four-byte self-loop and'
         ' counted astride on a LOOP_EXITSPAN=1 build, which owes none',
         plant=phantom9_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['0 self-loops of at most 64 B'],
              hasnt=['0x497de2']),
         bug=V(exit=0, has=['1 self-loops of at most 64 B'])),

    case('survey-drops-a-body-with-an-eight-byte-instruction',
         'loop-offsets.py', '2cbaeb6',
         "an instruction objdump prints over two lines read from the first"
         ' alone, so a loop holding one failed the byte sum and was dropped'
         ' unsaid',
         plant=longinsn_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['1 self-loops of at most 64 B']),
         bug=V(exit=0, has=['0 self-loops of at most 64 B'])),

    case('survey-counts-a-branch-into-an-exit-block-as-a-loop',
         'loop-offsets.py', '886bbf5',
         'a backward branch into a block that leaves the body'
         ' unconditionally, the check after it entered by a forward branch,'
         ' read as a straddling loop where the shim counted none',
         plant=exitblock_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['0 self-loops of at most 64 B'],
              hasnt=['0x482d4d']),
         bug=V(exit=0, has=['1 self-loops of at most 64 B',
                            'still straddling   : 1'])),

    case('survey-keeps-a-loop-closed-by-a-jmp', 'loop-offsets.py', None,
         'CONTROL: a loop entered by a jmp into its compare and closed by'
         ' a jmp back to its head is a loop, which the blanket flow test'
         ' of 2026-09-04 denied',
         plant=rotated_listing,
         argv=['--survey', '{dis}'],
         ok=V(exit=0, has=['1 self-loops of at most 64 B'])),

    # ---- read-all.sh ---------------------------------------------------
    # A HALF'S SPREAD NAMED NO PROCESS, so a half that drifted and a half
    # that is flat but for ONE outlier printed the same figure. Run 38's
    # control half read 9.41% where ten of its eleven processes sat inside
    # 2.42% and the eleventh, the main set's, carried the rest -- and the
    # session learned that by hand-rolling a loop over twenty-two logs,
    # because the block prints a spread and no names.
    case('plateau-spread-names-no-process', 'read-all.sh', 'a40f7b8',
         "a half's one outlier was indistinguishable from a half that drifted",
         plant=plateau_two_halves,
         argv=['{tag}'],
         ok=V(has=['within o2half', 'lowest o2half-rev, highest o2half-slice',
                   'within lookrts', 'lowest lookrts-rev, highest lookrts-slice']),
         bug=V(has=['within o2half'],
               hasnt=['lowest o2half-rev, highest o2half-slice'])),

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

    case('for-brief-pastes-a-wrapped-note-row', 'read-all.sh', '71eee9c',
         'a wrapped note row was pasted cut at its first line, inverted',
         # --for-brief writes the derived rows into the brief's items 5
         # and 6 so a write-up pastes rather than transcribes, which is
         # the whole of why it exists. But the note WRAPS its entries, so
         # a row taken as `head -1` ends mid-clause: `.text ... -- they
         # do`, where the note's next line reads `NOT agree`. The paste
         # published the fact INVERTED, which is worse than the
         # transcription it was built to retire. The fixture also carries
         # a prose line beginning with the word `repetition`, ahead of
         # the entry of that name and indented as prose: `^ *repetition `
         # matched it and published boilerplate where a fact belongs.
         plant=lambda t: for_brief_note(t),
         argv=['{tag}', '--for-brief'],
         ok=V(has=['they do NOT agree', 'NOT OWED'],
              hasnt=['one-sided']),
         bug=V(has=['one-sided'], hasnt=['they do NOT agree'])),

    case('for-brief-fills-its-slots-from-the-readings', 'read-all.sh', None,
         'CONTROL: every <yours> an artifact settles is filled off'
         ' post-run-readings.sh\'s files, and only the largest finding and'
         ' the pair\'s variable are left typed',
         shadow=dict(),
         plant=for_brief_readings,
         argv=['{tag}', '--for-brief'],
         ok=V(has=['the 3 shared timed arms span 0.9952 on `lib-stage2-lean`'
                   ' to 1.0128 on `bq-expand`',
                   'geomean over the 2 arm(s) 1.0030',
                   'THE PUBLISHED BASIS IS runzz-lookrts.',
                   'THE INTRUSION VERDICT IS CLEAN',
                   'runs 17, window 8, bcast and flip 6',
                   '0.9989 on window to 1.0098 on runs',
                   '5 HELD, 3 KILLED, 0 not read, 2 out of scope',
                   "<yours: the pair's variable>",
                   "<yours: what this run's largest finding is>"],
              hasnt=['<yours: the intrusion verdict from --wild over every'
                     ' log, the'])),

    case('for-brief-names-the-readings-it-wants', 'read-all.sh', None,
         'CONTROL: with no readings directory each slot says which command'
         ' writes what it is filled from',
         shadow=dict(),
         plant=lambda t: synthetic_run(t, into=os.path.join(t, 'shadow')),
         argv=['{tag}', '--for-brief'],
         ok=V(has=['./post-run-readings.sh runzz'],
              hasnt=['THE INTRUSION VERDICT IS CLEAN'])),

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

    case('machine-check-refuses-its-own-fingerprint', 'read-run.py', None,
         'from post-run 5b the box check compared a run against the'
         ' fingerprint it had just installed in its own file, and said the'
         ' box still measures as it did',
         # Step 5b installs --fingerprint into the run's own file and
         # --machine reads the kept fingerprint out of that same file, so
         # from 5b on the reading is the run against itself -- and it
         # still prints `inside 3%, so the box still measures as it did`,
         # which is what makes it worth a refusal rather than a sentence.
         # Run 24 read -0.03% that way, off zero only by the installed
         # table's rounding. Run 25's basis read +0.00% here on 2026-09-05
         # and gave up its honest +0.32% only when handed --run-doc
         # runs/run24.md, which is the workaround this replaces.
         plant=lambda t: {'run': synth_json(t, 'main',
                                            name='run98-g-main.json',
                                            fingerprint=os.path.join(
                                                t, 'run98.md')),
                          'fp': os.path.join(t, 'run98.md')},
         argv=['{run}', '--machine', '--run-doc', '{fp}'],
         ok=V(exit=2, has=['run98', 'its own'], hasnt=['inside 3%'])),

    case('machine-check-takes-another-runs-fingerprint', 'read-run.py', None,
         'CONTROL: the refusal is on the run NAME matching, so a previous'
         ' run\'s file still reads',
         plant=lambda t: {'run': synth_json(t, 'main',
                                            name='run98-g-main.json',
                                            fingerprint=os.path.join(
                                                t, 'run97.md')),
                          'fp': os.path.join(t, 'run97.md')},
         argv=['{run}', '--machine', '--run-doc', '{fp}'],
         ok=V(exit=0, has=['inside 3%'], hasnt=['its own'])),

    case('wild-names-the-shapes-to-exclude', 'read-run.py', None,
         'the intrusion verdict named the benches and left the session to'
         ' assemble the reading that stands in for a rerun, which Run 33'
         ' did by hand under a rerun it had stopped',
         # Post-run step 3 reruns the populations an intrusion touched;
         # where the rerun is not taken, what stands in for it drops those
         # SHAPES from both halves and re-reads. The shapes are on the
         # screen already, so the mode that names the benches can name the
         # call -- and it is shapes and not benches, a cell being an arm
         # on a shape and the comparison being per shape.
         plant=lambda t: {'log': write(os.path.join(t, 'w.log'),
                                       WILD_LOUD_LOG)},
         argv=['{log}', '--wild'],
         ok=V(exit=0, has=['IN ONE LINE: 1 of 2 bench(es)',
                           '--exclude-shape shp'],
              hasnt=['--exclude-shape other'])),

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
         plant=lambda t: {'readme': doc_of_a_list(t),
                          'anchor': '- `OPEN` **Item 4.**',
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
         plant=lambda t: {'readme': doc_of_a_list(t),
                          'anchor': '- `OPEN` **Item 1.**',
                          'with': write(os.path.join(t, 'w.txt'), 'x\n')},
         argv=['--replace', '{anchor}',
               '--with', '{with}', '--readme', '{readme}'],
         # `out, first: 1.` and not the item's words: what went out
         # STARTING AT ITEM 1 is the whole claim, and quoting the lead
         # here would store the anchor this case was just taught to
         # derive, one line down.
         ok=V(exit=0, has=['out, first: - `OPEN` **Item 1.**'])),

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
         # in-process state it measured in, and a process that asserted a
         # different one measured somewhere else -- which every gate beside
         # this one is blind to, each being WITHIN one process. **The
         # fixture asserts the DEPTHS since Run 29**: the case's own gist
         # has always said `different depths`, and until `states` existed it
         # could only spread the victim reading, which is a proxy and, on a
         # pair whose variable moves `list`, a proxy that moves for the
         # variable. The 14% spread stays beside them, being the dose
         # measurements' own figure for an unsaturated process against a
         # saturated one, so the fixture is that failure and not an
         # invented number.
         plant=lambda t: synthetic_run(t, plateau=['16.4', '19.1'],
                                       states=[1, 2]),
         argv=['{tag}'],
         ok=V(exit=1, has=['did not assert ONE state', 'inuse=1', 'inuse=2'],
              hasnt=['999.0'])),

    case('brief-facts-leaves-the-delta-range-to-the-eye', 'read-all.sh',
         None,
         "the delta chain's `list` range was summarised by eye from the"
         ' eleven rows above it',
         # README's Provenance carries a bullet per run quoting this run's
         # `list` move as a main-set figure and a class RANGE with both
         # ends named, and nothing derived it: the eleven per-population
         # rows were already printed and the sentence over them was read
         # off by eye. Run 31 wrote `23.72 to 38.35 points` by hand into
         # two documents and got the same figure wrong at a third site the
         # same evening. Both are printed now -- a range with no rows
         # under it cannot be checked, and rows with no range over them
         # are what got summarised by hand.
         #
         # WHAT THIS CASE PROVES AND WHAT IT DOES NOT. `synthetic_run`
         # builds ONE half -- every log is `<tag>-lookrts-*` -- so the
         # cross-half loop finds no second file and the two arithmetic
         # lines cannot fire here. What is proved is that the block is
         # reached and printed at all, which is the wiring; the
         # arithmetic over it is exercised on a real pair and by nothing
         # in this suite. A two-half fixture would close that and is not
         # built: the knob would reach every read-all case, and a fixture
         # grown for one assertion is how the captured `run14-*` JSONs
         # this file replaced came to tie thirty-four cases to artifacts
         # the procedure offers for deletion.
         plant=lambda t: synthetic_run(t),
         argv=['{tag}', '--brief-facts'],
         ok=V(has=['list, as the delta bullet quotes it'])),

    case('declared-state-split-still-refuses-the-run', 'read-all.sh', None,
         'a pair whose variable moves the resident state could never pass',
         # THE GATE IS RIGHT AND UNPASSABLE, which is a different thing
         # from wrong. A pair whose variable changes what the preamble's
         # spray leaves resident asserts two states on every process, so
         # post-run step 1 refuses for the whole life of the run and
         # `STATUS: all done` -- the one state the chapter calls finished
         # -- is out of reach. Run 31 is the case, its `-O2` half leaving
         # 74448896 bytes in use against the plain half's 95420416,
         # disclosed in its head, its Provenance and an open entry, and its
         # step 1 still red at the end. The note declares it AFTER the run
         # and with its reason, as the gate's own verdict is written, and
         # the block is still printed whole: what changes is that a
         # declared firing reads as a finding and not as a refusal.
         plant=lambda t: synthetic_run(t, plateau=['16.4', '19.1'],
                                       states=[1, 2], expect='state'),
         argv=['{tag}'],
         ok=V(exit=0,
              has=['DECLARES expected', 'a reading and not the gate',
                   'inuse=1', 'inuse=2'],
              hasnt=['did not assert ONE state',
                     'did NOT gate clean'])),

    case('plateau-gates-the-state-and-not-the-victim', 'read-all.sh',
         '17384a7',
         'a pair whose variable moves the victim failed a gate on its own'
         ' variable',
         # Run 29 struck `-fspec-constr` off one half. The preamble's victim
         # is timed with `list`, the one arm that flag moves, so the run read
         # an 11.82% spread against a 5% band while every one of its
         # twenty-two processes asserted `inuse` and `keep` identical TO THE
         # BYTE and each half was flat within itself at 1.98% and 1.88%. The
         # gate failed a sound run on its own variable, and `run-status.sh`
         # re-runs this driver without honouring PLATEAU_BAND, so post-run
         # step 1 could not go green. The gate is the STATE now and the
         # victim spread is printed beside it, per half where the log names
         # give halves. This fixture is that run in miniature: two processes
         # 16.4% apart in victim and identical in state.
         plant=lambda t: synthetic_run(t, plateau=['16.4', '19.1'],
                                       states=[1, 1]),
         argv=['{tag}'],
         ok=V(exit=0, has=['assert ONE state', 'a reading and not the gate',
                           'every process gated clean'],
              hasnt=['did not assert ONE state']),
         bug=V(exit=1, has=['the plateau is not flat'])),

    case('plateau-falls-back-where-the-state-is-not-logged', 'read-all.sh',
         None,
         'CONTROL: a run whose logs predate the state fields is still gated'
         ' on the victim band',
         # The branch the case above would otherwise leave unexercised, and
         # this tree's rule is that a checker branch with no live control is
         # a silent search. Every run up to Run 27 wrote the `@@saturate`
         # line without `inuse=` or `keep=`; those runs keep the band they
         # were gated under, and the driver says which of the two it used.
         plant=lambda t: synthetic_run(t, plateau=['16.4', '19.1'],
                                       states='omit'),
         argv=['{tag}'],
         ok=V(exit=1, has=['the state fields are not in these logs',
                           'outside that band'])),

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

    case('brief-facts-derives-what-the-brief-retypes', 'read-all.sh', None,
         "the checker's brief carries a run's figures in prose typed by"
         ' hand, and a rerun stranded four of them mid-block',
         # Item 6 of checker-brief.txt is the run's own facts written out
         # for two agents who cannot derive them. Run 27 rewrote that block
         # twice -- once before its intrusion was found and once after --
         # and left `ONE window`, the first window's `runs` baseline, the
         # first window's plateau spread and an intrusion range the run
         # file had already corrected. Every one of those is a reading this
         # driver already takes or can take beside the ones it takes.
         plant=lambda t: synthetic_run(t, plateau=[['19.0'], ['19.1']]),
         argv=['{tag}', '--brief-facts'],
         ok=V(exit=0, has=['THIS RUN ONLY facts', 'plateau', 'floors',
                           'the 0.7% bar'])),

    case('brief-facts-says-the-run-did-not-gate-clean', 'read-all.sh', None,
         'the derived block printed a failed run\'s floors as facts, where'
         ' a failed gate invalidates that population\'s whole column',
         # The block is a reading and the gate is the verdict; printed
         # under a FAIL with nothing said, its rows are figures from a
         # population this driver has just refused. It prints them still
         # -- they are what a session needs to see what went wrong -- and
         # says at the head that they are not the run's facts yet.
         plant=lambda t: synthetic_run(t, killed=True,
                                       plateau=[['19.0'], ['19.1']]),
         argv=['{tag}', '--brief-facts'],
         ok=V(exit=1, has=['THIS RUN ONLY facts', 'did NOT gate clean'])),

    case('brief-facts-names-a-population-with-one-half', 'read-all.sh',
         None,
         'a population timed on one half was skipped, so the rows printed'
         ' read as the populations there are',
         # Runs 11 to 13 ran their classes on the basis alone. A row that
         # is not there is not an absent figure, it is an absent
         # population -- the silent narrowing this driver refuses in the
         # paragraph about its own roster.
         # The fixture is already that shape: it writes the basis half of
         # each class and no control, which is why this needed no second
         # one -- a first attempt removed a file that was never written.
         plant=lambda t: synthetic_run(t, plateau=[['19.0'], ['19.1']]),
         argv=['{tag}', '--brief-facts'],
         ok=V(has=['one half only'])),

    case('brief-facts-says-when-there-is-no-plateau', 'read-all.sh', None,
         'CONTROL: with no `@@saturate` line in any log the plateau row'
         ' vanished, where every other absence here is a row',
         plant=lambda t: synthetic_run(t),
         argv=['{tag}', '--brief-facts'],
         ok=V(has=['no `@@saturate` line in these logs'])),

    case('brief-facts-says-when-the-halves-are-unreadable',
         'read-all.sh', None,
         'with no `is the basis` clause in the log the derived block'
         ' labelled every floor `other` and printed no bar row at all',
         # The halves come from the run's own log, which is the authority
         # this driver already trusts and which outlives the pair note.
         # A log without that clause -- Runs 11 to 13's shape -- left
         # BASIS empty, and the rows that need it vanished in silence
         # rather than saying the reading did not happen, which is what
         # `--fill-in`'s `<yours>` and this driver's own BLOCKED do.
         plant=lambda t: brief_facts_without_halves(t),
         argv=['{tag}', '--brief-facts'],
         ok=V(exit=0, has=['no `is the basis` clause',
                           'THIS RUN ONLY facts'],
              hasnt=['basis 0.'])),

    case('brief-facts-is-off-by-default', 'read-all.sh', None,
         'CONTROL: the block is asked for, so a gate run prints what it'
         ' always printed and no session reads a derivation it did not ask'
         ' for',
         plant=lambda t: synthetic_run(t, plateau=[['19.0'], ['19.1']]),
         argv=['{tag}'],
         ok=V(exit=0, has=['every process gated clean'],
              hasnt=['THIS RUN ONLY facts'])),

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
         # Exit 2 since 2026-09-18, the did-not-run code the usage guard
         # and the sibling probes use; 1 read as a sweep that ran wrong.
         ok=V(exit=2, has=['perf will not count instructions here',
                           'Nothing ran'])),

    case('counts-did-not-run-is-exit-2', 'run-counts.sh', '18021d0',
         'a sweep that did not run exited 1, the code of one that ran and'
         ' came out wrong',
         # The usage guard and the sibling probes say did-not-run at 2;
         # the perf, paranoid, mktemp, binary, output and roster guards
         # here said 1. The one caller reads no code apart, which is why
         # this is a record and not a fired defect.
         shadow=dict(extra=[('zzct6-g912', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_BLOCKED)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzct6', 'g912'],
         ok=V(exit=2, has=['Nothing ran']),
         bug=V(exit=1, has=['Nothing ran'])),

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
         # Exit 2 since 2026-09-18, as every guard here that says Nothing ran.
         ok=V(exit=2, has=['mktemp gives no writable file', 'Nothing ran'])),

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

    case('stalls-marks-a-cell-no-one-process-read', 'probe-stalls.sh',
         'd8ab388',
         'a difference of two processes in different modes read as a'
         ' measured cell',
         # Run 40's `runs-3` consumers drew one of three op-cache modes per
         # process, and `(2N - N) / N` over two processes in different
         # modes printed figures outside every mode, with nothing to say
         # so (2026-09-25). The third process at `-n 3N` is the check: a
         # cell whose two slopes part is followed by a `# NONLINEAR` line.
         # The stand-in perf bends cycles and not instructions, so the
         # line names the one event and not the other. The script before
         # the check printed the cell and no such line.
         shadow=dict(extra=[('zzps1-fake', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_MODES)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'BIN': './zzps1-fake',
              'OUT': 'probe-zzps1', 'ONLY': 'shape-a', 'ARMS': 'list',
              'N': '1', 'EVENTS': 'instructions:u,cycles:u'},
         argv=[],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'probe-zzps1.txt')).read(),
         ok=V(exit=0, has=['shape-a list 1 100000 200000',
                           '# NONLINEAR shape-a list: cycles:u 200000 then'
                           ' 350000'],
              hasnt=['instructions:u 100000 then']),
         bug=V(exit=0, has=['shape-a list 1 100000 200000'],
               hasnt=['NONLINEAR'])),

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
    case('answered-stub-keeps-its-slot', 'read-run.py', None,
         'the ANSWERED stub shipped with --move-registration\'s bare `___`',
         # The one defect of Run 28's write-up that no mechanical gate saw.
         # `--move-registration` writes the stub and leaves `___` for the
         # clause of verdicts; the step that fills it is a person's, so the
         # two are a handover with nothing on the far side. Run 28's entry
         # reached the second checker pass with the placeholder standing and
         # was found by an agent reading README beside the run file, not by
         # anything here. The gate is one line and the case is its control.
         # NO `fix`: this is a check that did not exist rather than a repair
         # of one that did, so there is no revision before a fix to replay,
         # and the ok direction is the whole of what there is to prove.
         plant=lambda t: {'readme': readme_answered_stub_unfilled(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['still carry `___`']),
         ),

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
         # with nothing behind it. RE-SHAPED 2026-09-05, the shape itself
         # having gone with the prune: a self-aiming anchor still has to
         # land INSIDE one of the check's own sites, and the fixture's
         # docstring says what it cost when it did not.
         plant=lambda t: {'readme': readme_six_pair_perturbed(t)},
         argv=['--check-doc', '--readme', '{readme}'],
         ok=V(exit=1, has=['carry-back figure is quoted differently']),
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
             'as an order of magnitude: it rests on eight pairs',
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
             t, 'as an order of magnitude: it rests on eight pairs',
             'as an order of magnitude: it rests on eighteen pairs',
             'The same eight controls ride every process',
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
             # The declaration is appended rather than edited in, the
             # delta bullet it once edited having moved to its run's file.
             'readme': write(os.path.join(t, 'P.md'), open(README).read()
                             + '\n- `runs-4`, `runs-5`, `runs-256` and'
                             ' `runs-512` were added 2026-08-30, after the'
                             ' run.\n'),
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

    case('class-view-retired-by-name-leaves-its-class', 'read-run.py',
         '110b014',
         "a class view retired by name in `retiredShapes` still counted in"
         " its class's size, so the first run file tabling the class"
         " without it failed `--check-doc`",
         # `runs-3` left timing on 2026-09-25 through `retiredShapes`, the
         # first class view there, while `dims_by_shape` read that list for
         # main-set shapes alone and retired a class shape only by its
         # class. Run 41's file, the first to table `runs` at sixteen,
         # then failed the class-count and population checks against a
         # Main.hs `runs` of seventeen. The expression reads the live
         # Main.hs, so it holds while `runs-3` stays retired there.
         argv=['--unit', "dims_by_shape(os.path.join(os.path.dirname("
               "__file__), 'Main.hs'))[0]['runs-3']['retired']"],
         ok=V(has=['True']), bug=V(has=['False'])),

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

    case('half-name-carries-no-hyphen', 'pair-halves.sh', '7249a35',
         'a hyphenated tag was CUT at the hyphen and handed on truncated,'
         ' so every driver would have run a binary nobody built',
         # Run 33's pair was declared `run33-ghead-exit`; `other=ghead-exit`
         # read back as `ghead`. The sibling case above it is run-major.sh's
         # class names, cut the same way and refused since 8cb5eb7.
         shadow=dict(extra=[('zzph5-pair.txt',
                             'a stand-in pair note.\n'
                             'HALVES: basis=lookrts other=a1g-pa\n')]),
         argv=['zzph5'],
         ok=V(exit=1, has=["a half's tag is [A-Za-z0-9_]"],
              hasnt=['BASIS=']),
         bug=V(exit=0, has=['BASIS=lookrts; OTHER=a1g'],
               hasnt=["a half's tag"])),

    case('halves-skip-a-prose-line-before-the-machine-line',
         'pair-halves.sh', '1aaea4d',
         'a sentence of the note that wrapped the word `HALVES:` onto a'
         ' line start was read as the machine line, so every driver refused'
         ' a pair whose real line sat right below it',
         # Run 35's preparation, 2026-09-18: THE BASIS block says that every
         # script reads the HALVES: line through this script, and the wrap
         # put those two words first on a line. preflight aborted at exit 2
         # before a step ran, and the note read right to a human. The first
         # line that PARSES is the machine line; a `^HALVES:` that does not
         # is prose.
         shadow=dict(extra=[('zzph6-pair.txt',
                             'a stand-in pair note. Every script that takes'
                             ' a run reads the\n'
                             'HALVES: line below through pair-halves.sh.\n'
                             'HALVES: basis=lookrts other=a1g\n')]),
         argv=['zzph6'],
         ok=V(exit=0, has=['BASIS=lookrts; OTHER=a1g']),
         bug=V(exit=1, has=['does not parse'], hasnt=['BASIS='])),

    case('halves-fall-back-to-the-environment-without-a-note',
         'pair-halves.sh', None,
         'CONTROL: no note at all takes the environment, and says so',
         env={'BASIS': 'x', 'OTHER': 'y'},
         argv=['zzph4'],
         ok=V(exit=0, has=['halves from the environment', 'BASIS=x; OTHER=y'])),

    case('halves-read-the-compare-line', 'pair-halves.sh', None,
         'CONTROL: the COMPARE line is printed as a third assignment',
         shadow=dict(extra=[('zzph6-pair.txt',
                             NOTE_STUB + 'COMPARE: run97\n')]),
         argv=['zzph6'],
         ok=V(exit=0, has=['BASIS=lookrts; OTHER=a1g; COMPARE=run97'])),

    case('halves-refuse-a-compare-line-naming-no-run', 'pair-halves.sh', None,
         'CONTROL: a COMPARE line naming a path and not a run is refused',
         shadow=dict(extra=[('zzph7-pair.txt',
                             NOTE_STUB + 'COMPARE: runs/run97.md\n')]),
         argv=['zzph7'],
         ok=V(exit=1, has=["COMPARE: run<N>"], hasnt=['BASIS='])),

    # ---- post-run-readings.sh, post-run step 4's readings in one command
    case('readings-wait-for-the-evening-to-complete', 'post-run-readings.sh',
         None,
         'CONTROL: before EVENING COMPLETE the timed readings are taken and'
         ' the count-dependent ones are not',
         shadow=dict(extra=readings_run('zzpr', complete=False)),
         argv=['zzpr'],
         # THE PRED JOB IS ASKED FOR BY NAME AT rc 0 OR 1, since
         # 2026-09-18: its exit code belongs to the REGISTRATION and not to
         # this script. `--predictions` returns `1 if unread else 0`, and a
         # `counts` or `countdiff` span cannot be read before the sweeps
         # exist -- which is precisely the state this control is in. Run
         # 35's registration was the first to carry such spans and turned
         # this case red with nothing in post-run-readings.sh having moved.
         # The bare name alone let rc=2 and a traceback through, so the
         # hasnt list refuses both. The other two rc=0 assertions stay:
         # those readings owe nothing to a registration. What this case is
         # about is WHICH readings are taken before EVENING COMPLETE, which
         # the hasnt list below and this name together settle.
         ok=V(has=['rc=0 main-lookrts-aa.txt', 'main-a1g-pred.txt',
                   'rc=0 %s-a1g-block.txt' % class_names()[0],
                   'not before EVENING COMPLETE'],
              hasnt=['rc=2 main-a1g-pred.txt', '!! crashed',
                     'main-counts-cmp.txt', 'half-movers.txt',
                     'cell-movers.txt'])),

    case('readings-take-the-counts-once-complete', 'post-run-readings.sh',
         None,
         'CONTROL: after EVENING COMPLETE the counts comparison and step 4b\'s'
         ' cell ranking are taken, and --half-movers is skipped naming the'
         ' missing COMPARE line',
         shadow=dict(extra=readings_run('zzpr2', complete=True)),
         argv=['zzpr2'],
         ok=V(has=['rc=0 main-counts-cmp.txt', 'rc=0 cell-movers.txt',
                   'no COMPARE line'],
              hasnt=['not before EVENING COMPLETE'])),

    case('repoint-moves-the-links-and-keeps-the-old-runs-own', 'read-run.py',
         None,
         'CONTROL: --repoint moves every link into the previous run\'s file'
         ' to the newest, renames the Contents entry, and keeps and names'
         ' the links whose own text names the previous run',
         # Run 39's step 5 did this by hand over 26 links, three of them to
         # keep, and a reference definition the first pass missed.
         plant=lambda t: {
             'readme': write(os.path.join(t, 'README.md'),
                             '# R\n\n- [Run 96](runs/run96.md)\n'
                             '  - [Results](runs/run96.md#results)\n\n'
                             'See [the run file\'s property 1](runs/run96.md#p)'
                             ' and [in Run 96\'s own\nfile](runs/run96.md#x).\n\n'
                             '[results]: runs/run96.md#results\n'),
             'doc': write(os.path.join(t, 'run97.md'), '# Run 97\n')},
         argv=['--repoint', 'run96', '--readme', '{readme}',
               '--run-doc', '{doc}'],
         probe=lambda subs: open(subs['readme']).read(),
         ok=V(exit=0, has=['- [Run 97](runs/run97.md)',
                           '[Results](runs/run97.md#results)',
                           "[the run file's property 1](runs/run97.md#p)",
                           "file](runs/run96.md)", 'anchor dropped',
                           '[results]: runs/run97.md#results'],
              hasnt=['- [Run 96]'])),

    case('counts-cost-sums-the-stages-per-half', 'read-run.py', None,
         'CONTROL: --counts-cost pairs each counts stage\'s start and done'
         ' stamps and sums them per half, naming a stage still open',
         shadow=dict(extra=[('zzcc-evening.txt',
                             '=== 2026-01-01T10:00:00+00:00 counts a1g main:'
                             ' start\n=== 2026-01-01T10:05:00+00:00 counts'
                             ' a1g main: done, rc=0\n=== 2026-01-01T10:05:00'
                             '+00:00 counts lookrts main: start\n'
                             '=== 2026-01-01T10:06:40+00:00 counts lookrts'
                             ' main: done, rc=0\n=== 2026-01-01T10:06:40'
                             '+00:00 counts a1g rev: start\n')]),
         argv=['--counts-cost', 'zzcc'],
         ok=V(exit=0, has=['total a1g', ' 300 s', 'total lookrts', ' 100 s',
                           'started and not done, so not counted: a1g rev'])),

    case('compare-cell-reads-one-cell-on-both-halves', 'read-run.py', None,
         'CONTROL: --compare --cell prints the cell\'s raw and net slope on'
         ' both halves with their ratio, and says where no log carries the'
         ' mutator clock',
         shadow=dict(extra=readings_run('zzprc', complete=False)),
         argv=['{at}/zzprc-a1g-main.json', '--compare',
               '{at}/zzprc-lookrts-main.json', '--cell',
               '%s/list' % main_shapes()[0]],
         ok=V(exit=0, has=['raw slope, s', 'net, s', 'this/other',
                           'mutator clock is not read'])),

    case('compare-cell-refuses-a-cell-it-cannot-find', 'read-run.py', None,
         'CONTROL: a cell absent from either file is refused, exit 2',
         shadow=dict(extra=readings_run('zzprd', complete=False)),
         argv=['{at}/zzprd-a1g-main.json', '--compare',
               '{at}/zzprd-lookrts-main.json', '--cell', 'no-shape/list'],
         ok=V(exit=2, has=['is not a cell of both files'])),

    case('block-writes-the-counts-clause-it-can-compute',
         'read-run.py', None,
         'CONTROL: with both count sweeps given, a class block\'s paragraph'
         ' carries the counts-against-clock clause itself and no `___` for it',
         # Run 39's session wrote the ten clauses by hand, two geomeans the
         # same paragraph prints divided (2026-09-23).
         shadow=dict(extra=lambda: readings_run('zzpra', complete=True)()
                     + class_counts('zzpra', class_names()[0])),
         argv=['{at}/zzpra-a1g-%s.json' % class_names()[0], '--block',
               '--compare', '{at}/zzpra-lookrts-%s.json' % class_names()[0],
               '--brief', '--counts',
               '{at}/zzpra-counts-a1g-%s.txt' % class_names()[0],
               '{at}/zzpra-counts-lookrts-%s.txt' % class_names()[0]],
         ok=V(has=['Its counted work parts by'],
              hasnt=["___ (how this class's counted work"])),

    case('readings-keep-a-file-they-did-not-write', 'post-run-readings.sh',
         'c1c1144',
         'a file in log-read-RUN/ that no call of the script wrote was'
         ' moved to log-read-RUN-kept/, and a note pointing at it went stale',
         # Run 39's session kept its own readings in that directory, and
         # the script's second call deleted them with the rest (2026-09-23);
         # the repair moved them aside instead, and Run 41's note, pointing
         # into log-read-run41/, went stale at the counts' landing. Since
         # 2026-09-26 the call deletes only what a call of it wrote.
         shadow=dict(extra=readings_run('zzpr9', complete=False)),
         plant=lambda tmp: (os.makedirs(os.path.join(
             tmp, 'shadow', 'log-read-zzpr9'), exist_ok=True), write(
                 os.path.join(tmp, 'shadow', 'log-read-zzpr9', 'mine.txt'),
                 'a session\'s own reading\n'), None)[-1],
         argv=['zzpr9'],
         probe=lambda subs: 'PROBE: mine.txt %s' % (
             'stayed' if 'mine.txt' in os.listdir(os.path.join(
                 str(subs['at']), 'log-read-zzpr9')) else 'went'),
         ok=V(has=['PROBE: mine.txt stayed']),
         bug=V(has=['PROBE: mine.txt went'])),

    case('readings-take-the-counts-after-a-complained-evening',
         'post-run-readings.sh', 'f241d66',
         'an evening that ended EVENING COMPLETE WITH N COMPLAINT(S) never'
         ' got its count readings, the script matching the clean form alone',
         # Run 39, 2026-09-23: its first sequence attempt refused and was
         # relaunched, so the counts driver closed on the complained form,
         # and the count-dependent readings said `not before EVENING
         # COMPLETE` over a file whose last line read EVENING COMPLETE.
         shadow=dict(extra=lambda: [
             (n, '=== 2026-01-01T00:00:00+00:00 EVENING COMPLETE WITH 1'
                 ' COMPLAINT(S) OVER BOTH CALLS -- read each\n')
             if n.endswith('-evening.txt') else (n, t)
             for n, t in readings_run('zzpr8', complete=True)()]),
         argv=['zzpr8'],
         ok=V(has=['rc=0 main-counts-cmp.txt'],
              hasnt=['not before EVENING COMPLETE']),
         bug=V(has=['not before EVENING COMPLETE'])),

    case('readings-read-the-compare-run-and-every-log', 'post-run-readings.sh',
         None,
         'CONTROL: the note\'s COMPARE run is read on the main set, each half'
         ' against its own, and --wild over every log, --for-brief last',
         shadow=dict(extra=readings_run('zzpr4', complete=True,
                                        compare='run97')),
         argv=['zzpr4'],
         # --wild exits 2 on every stand-in log, none carrying samples, and
         # is not counted with the readings that did not happen: Run 34's
         # wallclock log and its riders' four driver logs carry none
         # either. --deflation's two, with no riders here, are counted.
         ok=V(has=['2 did not happen, exiting 2 or worse, and 4 --wild'
                   ' reading(s) exited 2 on a log carrying no samples',
                   'rc=0 main-lookrts-vs-compare.txt',
                   'rc=0 main-a1g-bridge.txt', 'rc=0 half-movers.txt',
                   'wild-zzpr4-a1g-main.txt', 'for-brief.txt'])),

    case('readings-predictions-take-the-counts-once-complete',
         'post-run-readings.sh', None,
         'CONTROL: after EVENING COMPLETE each half\'s --predictions gets'
         ' its own sweep first and the other half\'s second, so a counts or'
         ' countdiff span is read and not NOT READ',
         shadow=dict(extra=readings_run('zzpr5', complete=True)),
         argv=['zzpr5', '--list'],
         ok=V(exit=0, has=['main-a1g-pred.txt ./read-run.py'
                           ' zzpr5-a1g-main.json --compare'
                           ' zzpr5-lookrts-main.json --predictions --counts'
                           ' zzpr5-counts-a1g.txt zzpr5-counts-lookrts.txt',
                           # and the class block, whose item 6 quotes the
                           # counts geomean
                           '{0}-a1g-blockcmp.txt ./read-run.py'
                           ' zzpr5-a1g-{0}.json --block --compare'
                           ' zzpr5-lookrts-{0}.json --brief --counts'
                           ' zzpr5-counts-a1g-{0}.txt'
                           ' zzpr5-counts-lookrts-{0}.txt'.format(
                               class_names()[0])],
              hasnt=['rc='])),

    case('readings-count-a-crashed-reading', 'post-run-readings.sh', None,
         'CONTROL: a reading that dies in a traceback exits 1, which is a'
         ' reading\'s own verdict code, and is counted as not having happened',
         # Found by review, 2026-09-17: the exit rule read the status alone.
         shadow=dict(extra=readings_run('zzpr6', complete=False),
                     mutate=[('read-run.py', 'def winsor_table(cells, shapes,'
                              ' strategies):', 'def winsor_table(cells, shapes,'
                              ' strategies):\n    raise RuntimeError("planted")')]),
         argv=['zzpr6'],
         ok=V(exit=1, has=['crashed: main-a1g-winsor.txt main-lookrts-winsor.txt'])),

    case('readings-cells-dump-is-stdout-alone', 'post-run-readings.sh', None,
         'CONTROL: a -cells.tsv carries the TSV alone, the reader\'s'
         ' header and warnings on stderr being in the other files',
         shadow=dict(extra=readings_run('zzpr3', complete=False)),
         argv=['zzpr3'],
         probe=lambda subs: open(os.path.join(
             str(subs['at']), 'log-read-zzpr3',
             'main-lookrts-cells.tsv')).read().split('\n')[0],
         ok=V(hasnt=['criterion 1.6'])),

    case('readings-rewrite-their-directory-whole', 'post-run-readings.sh',
         '6581d06',
         'a reading an earlier call left, against a COMPARE run the note no'
         ' longer names, stayed in the directory, where --for-brief reads it'
         ' as this call\'s',
         shadow=dict(extra=readings_run('zzpr7', complete=False)),
         plant=lambda tmp: (os.makedirs(os.path.join(
             tmp, 'shadow', 'log-read-zzpr7'), exist_ok=True), write(
                 os.path.join(tmp, 'shadow', 'log-read-zzpr7',
                              'main-lookrts-vs-compare.txt'),
                 'this run / run96-nospec-main.json, per arm\n'), None)[-1],
         argv=['zzpr7'],
         # A presence word and not the listing: since 2026-09-23 the script
         # names what it moves aside, so the file's name is in its output
         # whichever way the directory went.
         probe=lambda subs: 'STALE PRESENT' if os.path.exists(os.path.join(
             str(subs['at']), 'log-read-zzpr7', 'main-lookrts-vs-compare.txt'))
             else 'stale absent',
         ok=V(has=['stale absent'], hasnt=['STALE PRESENT']),
         bug=V(has=['STALE PRESENT'])),

    # ---- g3-twins.sh, post-run step 0's twins off the note's recipes ----
    case('g3-twins-reads-the-note-recipes', 'g3-twins.sh', None,
         "CONTROL: each half's environment, project file and flags come off"
         " the note's own recipe block, -g3 added",
         # Run 40 re-derived its twin script from Run 38's by hand, probe-*
         # being ignored by git. Built on Run 40's own recipes the script's
         # twins came out md5-identical to the hand script's, 2026-09-25;
         # this holds the parse, --dry-run building nothing.
         shadow=dict(extra=[('zzg3-pair.txt', NOTE_STUB + G3_RECIPES)]),
         argv=['zzg3', '--dry-run'],
         ok=V(exit=0, has=["### lookrts: env 'LOOP_A=1 LOOP_B=1', project"
                           " file 'cabal.project.x', ghc-options"
                           " '-fobject-determinism -g3'",
                           "### a1g: env 'LOOP_A=1 LOOP_B=1', project file"
                           " 'cabal.project.x', ghc-options '-fspec-constr"
                           " -fobject-determinism -g3'"])),

    case('g3-twins-refuses-a-recipe-it-cannot-read', 'g3-twins.sh', None,
         'CONTROL: a word before `cabal` that is no assignment refuses,'
         ' rather than being passed to env as a command',
         shadow=dict(extra=[('zzg3-pair.txt', NOTE_STUB + G3_RECIPES.replace(
             'LOOP_A=1 LOOP_B=1', 'LOOP_A=1 nice LOOP_B=1', 1))]),
         argv=['zzg3', '--dry-run'],
         ok=V(exit=1, has=['something other than environment assignments',
                           'did not build'])),

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
         ok=V(exit=0, has=['gate: inherited', 'alarm:',
                           'instance gate: done, rc=0', 'sequence: done, rc=0',
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

    case('evening-refuses-the-harness-without-the-reaper-switch',
         'run-evening.sh', '1be8870',
         'under the harness with its memory-pressure reaper live, the'
         ' evening is refused before the note is read; before the fix it'
         ' went on to read the note, and would have run the hours',
         # Run 35's driver, 2026-09-18 03:52: killed two and a half hours
         # in on a kernel memory-stall trigger fed by swap-ins, with 43 GB
         # free. The switch lives in the user settings; a session started
         # before it lacks it, and this is where that session is stopped.
         env={'CLAUDE_CODE_SESSION_ID': 'zz',
              'CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP': ''},
         argv=['zzem'],
         ok=V(exit=2, has=['CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1',
                           'Nothing ran'],
              hasnt=['evening begins']),
         bug=V(exit=1, has=['no zzem-pair.txt'],
               hasnt=['CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP'])),

    case('evening-status-is-one-line', 'evening-status.sh', None,
         'CONTROL: the mid-evening status is one line naming the evening\'s'
         ' last stamp and the sequence\'s last process, off two tails',
         # README's run list asks a session questioned mid-evening to answer
         # from a tail and nothing heavier; Run 39's session answered with
         # a grep over the wallclock log and a read of the previous run's
         # beside it, one of them inside an intruded bench's window.
         shadow=dict(extra=[
             ('zzst-evening.txt', '=== 2026-01-01T02:00:00+00:00 evening'
              ' begins for zzst\n=== 2026-01-01T02:30:00+00:00 sequence:'
              ' start\n'),
             ('zzst-wallclock.log', '=== 2026-01-01T02:30:00+00:00 start'
              ' zzst-a1g-main from ./zzst-a1g\n=== 2026-01-01T03:00:00+00:00'
              ' done  zzst-a1g-main rc=0 benchmarking=5\n'
              '=== 2026-01-01T03:00:00+00:00 start zzst-lookrts-main from'
              ' ./zzst-lookrts\n')]),
         argv=['zzst'],
         ok=V(exit=0, has=['sequence: start', '1 done',
                           'zzst-lookrts-main'])),

    case('evening-status-refuses-usage', 'evening-status.sh', None,
         'CONTROL: no run named is usage, exit 2',
         argv=[], ok=V(exit=2, has=['usage:'])),

    case('evening-resumes-from-a-named-stage', 'run-evening.sh', None,
         'CONTROL: --from sequence over a dead attempt\'s status file runs'
         ' the sequence and the riders and not the gate, appending to that'
         ' file under a resumed line',
         # Run 39's sequence refused after its gate had run, and the
         # session relaunched it by hand, stamping the status file itself.
         shadow=dict(extra=lambda: evening_fixture('zzer') + [
             ('zzer-evening.txt', '=== 2026-01-01T00:00:00+00:00 evening'
              ' begins for zzer\n=== 2026-01-01T00:30:00+00:00 gate: done,'
              ' rc=0\n')]),
         env={'MAXBUSY': '100', 'FAKE_SATURATE': '1',
              'ONLY': main_shapes()[0]},
         argv=['zzer', '--from', 'sequence'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzer-evening.txt')).read(),
         ok=V(exit=0, has=['evening begins for zzer', 'evening resumed for'
                           ' zzer from sequence', 'sequence: done, rc=0',
                           'riders a1g clean: done, rc=0'],
              hasnt=['gate: inherited', 'instance gate: start'])),

    case('evening-refuses-to-resume-nothing', 'run-evening.sh', None,
         'CONTROL: --from with no status file is refused, there being no'
         ' attempt to resume',
         shadow=dict(extra=lambda: evening_fixture('zzen')),
         env={'MAXBUSY': '100'},
         argv=['zzen', '--from', 'sequence'],
         ok=V(exit=2, has=['nothing to resume'],
              hasnt=['evening begins', 'evening resumed'])),

    case('evening-refuses-a-stray-run-artifact-before-the-gate',
         'run-evening.sh', 'a35f698',
         'a file named for the run that run-major.sh\'s relaunch guard'
         ' refuses over let the evening spend its gate and then refuse the'
         ' sequence, the riders running in its place on the quiet box',
         # Run 39, 2026-09-23: the executing session sent the driver's own
         # output to run39-evening-launch.log, which is a $R-*.log; the
         # gate took its half hour, the sequence refused at once over that
         # one file, and the riders ran before the hours instead of after.
         shadow=dict(extra=lambda: evening_fixture('zzes')
                     + [('zzes-launch.log', 'the driver\'s own output\n')]),
         env={'MAXBUSY': '100', 'ONLY': main_shapes()[0]},
         argv=['zzes'],
         ok=V(exit=1, has=['zzes-launch.log', 'Nothing ran'],
              hasnt=['evening begins']),
         bug=V(has=['sequence: done, rc=1'])),

    # ---- instance-gate.sh, run list step 16a ----------------------------
    # A half's launch instance against a fresh copy, since 2026-09-18: Run
    # 34's mounted instance read 1.075 of a copy the day after its evening
    # and 1.10 a day later still, untouched, so a draw is gated once per launch
    # (README, the placement section). The verdict logic runs on faked
    # cycles with the shadow itself standing in for the mount; the no-mount
    # exit and usage are the other two paths.
    case('instance-gate-refuses-usage', 'instance-gate.sh', None,
         'CONTROL: no run named is usage, exit 2',
         argv=[], ok=V(exit=2, has=['usage:'])),

    case('instance-gate-has-nothing-to-gate-for-a-stub-half',
         'instance-gate.sh', None,
         'CONTROL: a half that is no ELF binary launches from disk, so there'
         ' is no instance to gate, said so at exit 0',
         # THIS CASE USED TO READ THE BOX. The shadow symlinks the real
         # hugebin/, and an early `exit 0` on a missing mount fired before
         # the per-half loop, saying the same thing in other words -- so the
         # branch below was reachable only while that mount happened to be
         # up, and the case went red the day hugebin/ was suspended
         # (2026-09-19). Its own prose admitted the dependency and no check
         # could act on prose. INSTANCE_DIR does not lift it either: setting
         # it takes the other branch, which derives B from $DIR and never
         # calls half-bin.sh. What lifted it, 2026-09-20, was dropping the
         # early exit so the loop speaks per half in every case; the case is
         # unchanged and now passes mounted or not, which is what a control
         # over a script should do. What the evening's stand-ins meet is
         # this path: half-bin.sh finds no mount, or keeps a non-ELF half
         # off one, and hands back the disk path either way.
         shadow=dict(extra=[('zzig-pair.txt', NOTE_STUB)]
                     + halves('zzig-lookrts', 'zzig-a1g')),
         argv=['zzig'],
         ok=V(exit=0, has=['launches from disk', 'nothing to gate'],
              hasnt=['REDRAWN', 'UNTESTED'])),

    case('instance-gate-swaps-in-the-copy-when-the-launch-draw-is-slow',
         'instance-gate.sh', None,
         'CONTROL: a launch instance 10% slower than its fresh copy is'
         ' parked as .slow and the copy takes its name',
         shadow=dict(extra=[('zzig-pair.txt', NOTE_STUB)]
                     + halves('zzig-lookrts', 'zzig-a1g')),
         env={'INSTANCE_DIR': '.', 'INSTANCE_FAKE': '1100,1000'},
         argv=['zzig'],
         probe=lambda subs: ' '.join(sorted(
             f for f in os.listdir(subs['at']) if f.startswith('zzig-'))),
         ok=V(exit=0, has=['launch/copy 1.1000', 'REDRAWN',
                           'zzig-a1g.slow', 'zzig-lookrts.slow'],
              hasnt=['UNTESTED', '.gate'])),

    case('instance-gate-lets-a-level-launch-instance-stand',
         'instance-gate.sh', None,
         'CONTROL: within the bar the copy is discarded and nothing is'
         ' renamed',
         shadow=dict(extra=[('zzig-pair.txt', NOTE_STUB)]
                     + halves('zzig-lookrts', 'zzig-a1g')),
         env={'INSTANCE_DIR': '.', 'INSTANCE_FAKE': '1020,1000'},
         argv=['zzig'],
         probe=lambda subs: ' '.join(sorted(
             f for f in os.listdir(subs['at']) if f.startswith('zzig-'))),
         ok=V(exit=0, has=['level within 5%'],
              hasnt=['REDRAWN', '.slow', '.gate'])),

    case('instance-gate-discards-a-slow-copy', 'instance-gate.sh', None,
         'CONTROL: a copy slower than the launch instance is the one'
         ' discarded, and the launch instance stands under its name',
         shadow=dict(extra=[('zzig-pair.txt', NOTE_STUB)]
                     + halves('zzig-lookrts', 'zzig-a1g')),
         env={'INSTANCE_DIR': '.', 'INSTANCE_FAKE': '1000,1200'},
         argv=['zzig'],
         probe=lambda subs: ' '.join(sorted(
             f for f in os.listdir(subs['at']) if f.startswith('zzig-'))),
         ok=V(exit=0, has=['copy was the slow draw'],
              hasnt=['REDRAWN', '.slow', '.gate'])),

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
         #
         # ASSERTED ON THE TEXT AND NOT THE LABEL since 2026-09-04, when
         # pre-run step 1 -- nothing named for this run may exist yet --
         # moved into this script: two sections each have a step 1, so
         # `  1     done` stopped naming the post-run one, and for an
         # UNSTARTED run the pre-run one legitimately reads done. A label
         # was never the claim; the sentence beside it is.
         ok=V(exit=1, has=['NOT DONE', 'STATUS: ',
                           'nothing named run98-* here'],
              hasnt=['all done',
                     'read-all.sh gates every process clean',
                     "says complete",
                     'counts file(s) complete',
                     'runs/run98.md exists'])),

    # ---- read-run.py --check-doc, the coverage check ------------------
    case('coverage-check-sees-a-figure-on-a-wrapped-continuation',
         'read-run.py', '320ece0',
         'a list item whose figure wrapped past its first line was skipped'
         ' as an indented block, so a section carrying only such figures'
         ' read as figure-free and owed no replace-list bullet',
         plant=lambda t: {
             'readme': readme_with_an_uncovered_figure(t, 'wrapped')},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1, has=['no replace-list bullet links',
                           'Zz coverage probe']),
         bug=V(hasnt=['Zz coverage probe'])),

    case('coverage-check-sees-an-address-as-a-figure', 'read-run.py',
         '320ece0',
         "a section whose figures are addresses and offsets -- the pinning"
         " claim's -- was invisible to the coverage check, which wanted a"
         ' decimal',
         plant=lambda t: {
             'readme': readme_with_an_uncovered_figure(t, 'hex')},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1, has=['no replace-list bullet links',
                           'Zz coverage probe']),
         bug=V(hasnt=['Zz coverage probe'])),

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

    case('move-registration-splits-the-items-it-moves', 'read-run.py', None,
         'the registration landed as one paragraph, so `registration (N)`'
         ' could not be jumped to',
         # Run 28's arrived as a single 35,160-character line while every
         # class block and every verdict cited an item by number, so
         # looking one up was a scan of the whole. Its comprehension probe
         # raised it as that probe's one structural finding, and the
         # write-up raised it independently -- two readers on one defect.
         # Fixed at the MOVE and not by hand afterwards, the hand copy
         # being what this mode exists to abolish. NO `fix`: the split is
         # a capability the mode did not have rather than a repair of one
         # it had wrong, so there is nothing before it to replay.
         plant=lambda t: registration_to_move(t),
         argv=['--move-registration', '--readme', '{readme}',
               '--run-doc', '{doc}'],
         probe=lambda subs: open(subs['doc']).read(),
         ok=V(exit=0, has=['Registered before the run.\n\n(1) *a*']),
         ),

    case('move-registration-leaves-the-pointer-to-itself', 'read-run.py',
         '6206be5',
         "the preparation's pointer to the registration, copied into the"
         ' new run file at step 5, stayed there naming this run as the'
         " next run's pair",
         # Run 40's write-up found it by reading and deleted it by hand;
         # no step said to. The move takes it with the registration.
         plant=lambda t: registration_to_move_with_pointer(t),
         argv=['--move-registration', '--readme', '{readme}',
               '--run-doc', '{doc}'],
         probe=lambda subs: open(subs['doc']).read(),
         ok=V(exit=0, has=['A head paragraph.', 'Registered before the run.',
                           'pointer to this registration, deleted'],
              hasnt=["on the owner's word"]),
         bug=V(has=["on the owner's word"])),

    case('move-registration-repoints-the-anchors-it-carries',
         'read-run.py', 'ca928dc',
         'a registration written in the open list links README sections by'
         ' bare anchor, and the move landed those links in runs/ dead',
         # The text is authored where `](#section)` resolves and read where
         # it does not. --check-doc catches it, so it costs a minute rather
         # than a run -- but it costs that minute every run, and the mode
         # is the only thing that knows the text crossed a directory.
         plant=lambda t: registration_to_move(t),
         argv=['--move-registration', '--readme', '{readme}',
               '--run-doc', '{doc}'],
         probe=lambda subs: open(subs['doc']).read(),
         ok=V(exit=0, has=['](../README.md#the-shape-set)'],
              hasnt=['](#the-shape-set)']),
         bug=V(exit=0, has=['](#the-shape-set)'],
               hasnt=['](../README.md#the-shape-set)'])),

    case('checklist-steps-prints-the-imperative-half', 'read-run.py', None,
         'the post list runs to hundreds of lines of which a session'
         ' executes the step lines, and it is read whole at every run',
         # The rationale is not duplicated anywhere -- measured, zero of
         # 318 sentences over sixty characters appears in README prose --
         # so there is nothing to delete and moving it would be a
         # rewrite. What a session wants at the moment of doing the work
         # is the imperative half, which is derivable: the step leads and
         # the commands, without the continuations under them.
         argv=['--checklist', 'post', '--imperative'],
         ok=V(exit=0, has=['./run-status.sh $R', '10b.'])),

    case('check-doc-refuses-a-piped-gate-in-the-chapter',
         'read-run.py', None,
         "the chapter's own recipes can pipe a gate, and a pipe reports the"
         " LAST command's status, so the recipe reads as passing",
         # Run 27 read `check-all | tail`'s exit 0 and had to run it again,
         # then chained `--predictions` behind `&&` while writing the rule
         # that forbids it. A rule a document states and its own examples
         # break is worth less than the check that holds the examples to
         # it, and this is the only place the examples live.
         plant=lambda t: {'readme': edited_readme(
             t, ('    ./read-run.py --check-doc --quiet',
                 '    ./read-run.py --check-doc --quiet | tail -3'))},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1, has=['pipes or chains a gate'])),

    case('status-finds-a-10c-commit-without-a-document', 'run-status.sh',
         'f8dc57d',
         '10c read NOT DONE when the tail\'s commit touched neither document,'
         ' the subjects being read off a path-filtered log',
         # Run 39's 10c commit had nothing left to fix and was empty; the
         # step read NOT DONE until a sentence was added to README to give
         # the commit a path (2026-09-23). No shadow: a shadow is no git
         # checkout, and git's answer is what this reads.
         argv=['run39'],
         ok=V(has=['10c   done']),
         # No audit: the case reads the real repository's history, and
         # Run 39's 10c commit carries a README edit, so no revision holds
         # the empty 10c commit the defect needs.
         no_audit='other:history-holds-no-empty-commit'),

    case('status-names-the-subject-it-looked-for', 'run-status.sh', None,
         'a NOT DONE on a step said no subject names it, without saying'
         ' that the run name is half of what it matched on',
         # The filter is `run N` or `runN` FIRST and the step second, so a
         # subject reading `step 6d: ...` is invisible however plainly it
         # names the step. Run 27 wrote two of those and read NOT DONE
         # over work that was done; the message now prints the form it
         # wanted, which is the one thing that turns the line into a fix.
         shadow=dict(),
         argv=['run27'],
         ok=V(has=['write `Run 27 step 6d: ...`'])),

    case('wild-header-carries-the-foreign-unit', 'read-run.py', None,
         'the `foreign` column is a ratio of ONE CORE and its neighbour is'
         ' a percentage, so a reading of 0.96 was taken for 0.96%',
         # The legend says it -- and sits under the last of 490 rows,
         # where a session that reads the head of the table never meets
         # it. Run 27's step 2 cleared an intrusion of 0.96 of a core on
         # that reading, and the checker found it at 6d, after the whole
         # write-up had been written against the intruded window. The unit
         # belongs in the header, next to the number it governs.
         plant=lambda t: {'log': write(os.path.join(t, 'w.log'),
                                       WILD_MIXED)},
         argv=['{log}', '--wild'],
         ok=V(exit=0, has=['fgn/core'], hasnt=[' foreign   load'])),

    case('prose-facts-joins-the-one-mode-guard', 'read-run.py', None,
         'the mode added 2026-09-18 was outside the guard that refuses two'
         ' at once, so --prose-facts --lint ran the first and dropped the'
         ' lint',
         # THE THIRD RECURRENCE of one defect: two modes in 2026-09-08, six
         # in the review of 2026-09-18, and this one the same day, added
         # beside two that DID join the roll call in that review's own fix.
         # A structural test was considered and refused: `--modes` prints
         # every `args.X` the dispatch branches on, but a dozen of them are
         # not single modes at all -- --replace, --section, --note,
         # --checklist, --carried and the rest -- so the check would want a
         # curated exemption list, which is the same list going stale one
         # level up. An instance case apiece is cheaper and cannot rot.
         argv=['--prose-facts', 'run97', '--lint'],
         ok=V(exit=2, has=['one mode at a time', '--prose-facts',
                           '--lint'])),

    case('new-modes-join-the-one-mode-guard', 'read-run.py', None,
         'two modes added 2026-09-08 were outside the guard that refuses'
         ' two at once, so the dispatch ran one and dropped the other',
         # The guard names the modes it knows, and a mode added without
         # joining it is the silent drop the guard exists to stop:
         # `--inherited --lint` printed the inherited report and said
         # nothing about the lint it did not run. Found by a shape pass
         # over the commit that added them, an hour after it landed.
         argv=['--inherited', '--lint'],
         ok=V(exit=2, has=['one mode at a time', '--inherited', '--lint'])),

    case('imperative-is-refused-without-the-checklist',
         'read-run.py', None,
         '`--imperative` means nothing on its own and was taken and'
         ' ignored, which is this file\'s silent-option family',
         # `--draft` and `--halves` are refused without `--note` for the
         # same reason and by the same paragraph; this flag arrived the
         # same day as the guard it needed and missed it.
         plant=lambda t: {'run': synth_run(os.path.join(t, 'r.json'),
                                           main_shapes()[:2])},
         argv=['{run}', '--imperative'],
         ok=V(exit=2, has=['--imperative is --checklist'])),

    case('modes-names-both-arities-of-a-flag', 'read-run.py', None,
         "a flag's one-line help named one of its two arities, and two"
         ' runs hand-rolled the computation the other one prints',
         # `--counts`'s help read *with --compare*, which is the cross-half
         # arity; the within-half one, `--counts SWEEP.txt --pair A B`, was
         # taken 2026-09-05 and hand-rolled again by Run 26's write-up and
         # Run 27's. A table written by hand would drift the same way, so
         # this one is read off the dispatch's own `if` tests.
         argv=['--modes'],
         ok=V(exit=0, has=['dispatches on', 'args.pair and args.counts',
                           'args.compare and args.counts'])),

    case('inherited-names-a-paragraph-carried-whole', 'read-run.py', None,
         'a paragraph left verbatim by the write-up is outside the'
         " checker's diff, whose base is the copy step 5 made",
         # Both passes read PRETIP..HEAD over the run file, and PRETIP is
         # the commit that copies the previous run's file: an EDITED
         # paragraph shows there, an untouched one produces no diff line
         # at all. Run 27 shipped nine such paragraphs past both passes
         # (its probe found them by reading the document whole) and two
         # more past the probe. This mode is that reading, mechanised.
         plant=lambda t: inherited_pair(t),
         argv=['--inherited', '--run-doc', '{doc}'],
         ok=V(exit=0, has=['carried whole', 'On Run 96 the floor'],
              hasnt=['The table below is installed'])),

    case('inherited-refuses-a-run-with-nothing-before-it',
         'read-run.py', None,
         'CONTROL: with no earlier run file beside it the comparison is'
         ' impossible, and a reading that cannot happen says so',
         # The branch a fixture meets first: a run file in a directory of
         # its own has no predecessor, and a mode that printed `0` there
         # would report `nothing was carried` where the truth is that
         # nothing was compared. Exit 2, which this tree reads as the run
         # not happening.
         plant=lambda t: {'doc': lone_rundoc(t)},
         argv=['--inherited', '--run-doc', '{doc}'],
         ok=V(exit=2, has=['no earlier run file', 'did not happen'])),

    case('inherited-passes-a-file-that-inherited-nothing',
         'read-run.py', None,
         'CONTROL: a run file sharing no paragraph with the previous run'
         ' reports none, so the report cannot be read as always firing',
         plant=lambda t: inherited_pair(t, share=False),
         argv=['--inherited', '--all', '--run-doc', '{doc}'],
         ok=V(exit=0, has=['0 paragraph(s)',
                           '0 paragraph(s) this run CHANGED that still'
                           ' name Run 96'])),

    case('inherited-names-a-half-updated-paragraph', 'read-run.py', None,
         'a paragraph whose LEAD was rewritten for this run and whose body'
         ' still quotes the run before read as work being done, by every'
         ' pass whose object is the diff',
         # The complement of the carried half above, added 2026-09-16.
         # That half catches what a diff cannot see; this catches what a
         # diff SHOWS and a reader skims, the changed line looking like
         # the work. Run 33's floor paragraph carried Run 32's carriers,
         # closed thresholds, wild cells, registration number and
         # fifteen-run series under a lead rewritten for Run 33, and its
         # class-property entry an updated head over a tail that
         # contradicted it; one checker pass read that diff and passed
         # both, and the next found them by reading the finished file.
         plant=lambda t: inherited_pair(t, half=True),
         argv=['--inherited', '--all', '--run-doc', '{doc}'],
         ok=V(exit=0, has=['1 paragraph(s) this run CHANGED that still'
                           ' name Run 96', 'On Run 97 the floor'])),

    case('check-doc-holds-a-heading-to-two-blank-lines',
         'read-run.py', None,
         'a heading run into the paragraph above it passed every gate,'
         ' and `--replace` then takes the heading with the paragraph',
         # Run 27 reintroduced by an off-by-one insert the defect the open
         # list records fixed on 2026-09-03, and no gate saw it: the wrap
         # pass asks about line length INSIDE a paragraph, never about
         # what separates two. Found by eye, from a heading looking wrong.
         plant=lambda t: {'rundoc': rundoc_heading_spacing(t, blanks=1)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(exit=1, has=['blank line', '## Results'])),

    case('check-doc-passes-two-blank-lines', 'read-run.py', None,
         'CONTROL: the spacing this project uses is not reported',
         plant=lambda t: {'rundoc': rundoc_heading_spacing(t, blanks=2)},
         argv=['--check-doc', '--quiet', '--run-doc', '{rundoc}'],
         ok=V(hasnt=['is preceded by'])),

    case('predictions-skip-a-degenerate-pair', 'read-run.py', 'e55f8d3',
         'a span whose pair carries a sunk cell exited 2 out of the middle'
         ' of the walk, so every span after it went unadjudicated',
         # `pair_stats` refuses such a cell and exits, which is right for
         # `--pair`, whose whole output is that pair, and wrong here: a
         # registration reads many spans over one population, and Run 27's
         # item (6) names a `libunord` pair whose main-set cells ARE the
         # forcing pass by the item's own words. `break_margin` already
         # takes the other route for the same reason.
         plant=lambda t: {
             'run': sunk_json(t, main_shapes(), 'lib-stage1'),
             'other': sunk_json(t, main_shapes(), 'lib-stage1',
                                name='other.json'),
             'doc': write(os.path.join(t, 'r.md'),
                          '# Run 99\n\n## What this run was built to answer,'
                          ' and what it answered\n\n(1) *a* `predict: pair'
                          ' lib-stage1 mut-odo-vecdims 1.0 within 1%`. (2)'
                          ' *b* `predict: cross list 1.0 within 1%`.\n')},
         argv=['{run}', '--compare', '{other}', '--predictions',
               '--run-doc', '{doc}'],
         ok=V(exit=1, has=['no positive net', 'NOT READ',
                           'cross list 1.0 within 1%',
                           'within 1.00%: HELD']),
         bug=V(exit=2, hasnt=['cross list 1.0 within 1%',
                              'within 1.00%: HELD'])),

    case('predictions-name-the-main-set-an-item-reads-on', 'read-run.py',
         '4e121a2',
         'an item saying `on the main set` named no population, the block'
         ' having built its names from the class paths alone; one naming'
         ' a class names it, and one naming neither is handed to the hand',
         # The block reads each item for the populations it names and
         # prints the mapping, so that a span registered on `runs` is not
         # read on the main set and reported KILLED for the wrong question.
         # `main` is the file the spans were read on, so it is available
         # whether or not its JSON is among --classes; until 2026-09-13 it
         # was not, and `on the main set` came back as naming nothing.
         plant=lambda t: {
             'run': synth_json(t),
             'other': synth_json(t, name='other.json'),
             'runs': synth_json(t, pop='runs', name='x-runs.json'),
             'doc': write(os.path.join(t, 'r.md'),
                          '# Run 99\n\n## What this run was built to answer,'
                          ' and what it answered\n\n(1) *a* On `runs`:'
                          ' `predict: cross list 1.0 within 1%`. (2) *b* On'
                          ' the main set: `predict: cross list 1.0 within'
                          ' 1%`. (3) *c* `predict: cross list 1.0 within'
                          ' 1%`.\n')},
         argv=['{run}', '--compare', '{other}', '--predictions',
               '--run-doc', '{doc}', '--classes', '{runs}'],
         ok=V(has=['the populations each item names', '(1) runs',
                   '(2) main', '(3) no population named; read by hand']),
         bug=V(has=['(1) runs'], hasnt=['(2) main'])),

    case('cross-span-on-an-arm-with-no-corrected-time', 'read-run.py',
         'dc2bf44',
         'a cross span over a reducing consumer netted whatever shapes kept'
         ' a positive net, and said only how many there were',
         # `pair` takes its key from `pair_sunk` -- slope for a `no_net`
         # arm, net otherwise -- and refuses a sunk cell; `cross` divided
         # `net` outright and dropped the shape. `no_net`'s own docstring
         # closes by saying every span a registration writes over such an
         # arm is a `pair`, which held until Run 29's item (3) wrote a
         # `cross` over `libunord-stage7-sum`. On that run's `runs` the old
         # branch read 0.5854 over the 3 shapes of 14 whose net stayed
         # positive, against 0.9779 raw over all 14, and on `block` it read
         # none at all: the item is KILLED read the first way and HELD the
         # second. The fixture sinks EVERY cell of the arm, which is
         # `block`'s state and the one no subsample can hide.
         plant=lambda t: {
             'run': synth_run(os.path.join(t, 'nonet.json'), main_shapes(),
                              sunk=[(sh, a_reducing_consumer())
                                    for sh in main_shapes()]),
             'other': synth_run(os.path.join(t, 'nonet-other.json'),
                                main_shapes(),
                                sunk=[(sh, a_reducing_consumer())
                                      for sh in main_shapes()]),
             'doc': write(os.path.join(t, 'nonet.md'),
                          '# Run 99\n\n## What this run was built to'
                          ' answer, and what it answered\n\n(1) *a*'
                          ' `predict: cross %s 1.0 within 5%%`. (2) *b*'
                          ' `predict: cross list 1.0 within 5%%`.\n'
                          % a_reducing_consumer())},
         argv=['{run}', '--compare', '{other}', '--predictions',
               '--run-doc', '{doc}'],
         ok=V(exit=0, has=['read 1.0000', 'within 5.00%: HELD'],
              hasnt=['NOT READ']),
         bug=V(exit=1, has=['NOT READ: no shape readable for it'])),

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

    case('major-run-takes-the-populations-to-rerun', 'run-major.sh',
         'a08f92b',
         'post-run step 3 says to drive a rerun through this script, and'
         ' the script could run only all eleven populations or none',
         # An intrusion touches one population, and step 3 reruns THAT one
         # on both halves. The driver had no way to be told which, and its
         # relaunch guard refused over every artifact of the run rather
         # than over the ones the invocation would write -- so the step's
         # own instruction could not be carried out. Run 27 met it.
         shadow=dict(extra=lambda text: halves('zzpr-lookrts', 'zzpr-a1g', classes=classes_in(text))
                     + [('zzpr-pair.txt', NOTE_STUB),
                        ('zzpr-lookrts-rev.json', '[]\n'),
                        ('zzpr-a1g-rev.json', '[]\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzpr', 'runs'],
         ok=V(exit=0, has=['major run begins', 'start zzpr-a1g-runs',
                           'start zzpr-lookrts-runs'],
              hasnt=['already has artifacts', 'start zzpr-lookrts-main',
                     'start zzpr-a1g-main', 'start zzpr-a1g-bcast']),
         bug=V(exit=1, has=['already has artifacts'],
               hasnt=['major run begins'])),

    case('major-run-still-refuses-what-it-would-overwrite', 'run-major.sh',
         None,
         'CONTROL: named a population whose artifacts are here, it refuses'
         ' as it always did -- the guard is narrowed, not dropped',
         shadow=dict(extra=lambda text: halves('zzpq-lookrts', 'zzpq-a1g', classes=classes_in(text))
                     + [('zzpq-pair.txt', NOTE_STUB),
                        ('zzpq-lookrts-runs.json', '[]\n')]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzpq', 'runs'],
         ok=V(exit=1, has=['already has artifacts', 'zzpq-lookrts-runs.json'],
              hasnt=['major run begins'])),

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

    case('tree-line-lists-tracked-changes-only', 'run-major.sh',
         '8a833d3',
         'the provenance tree line listed every untracked path, burying the'
         ' process lines post-run step 1 reads',
         # Run 41's wall-clock log carried 527 untracked scratch paths
         # between its launch line and its first process. The count is
         # what the line is for; of the paths, only tracked changes can
         # say the source differs from its commit. The shadow is made a
         # git repository, so git answers and every file in it is
         # untracked, the planted scratch file among them.
         shadow=dict(extra=lambda text: halves('zztl-lookrts', 'zztl-a1g', classes=classes_in(text))
                     + [('zztl-pair.txt', NOTE_STUB),
                        ('zztl-scratch.txt', 'untracked\n')]),
         plant=lambda t: (subprocess.run(
             ['git', 'init', '-q', os.path.join(t, 'shadow')], check=True),
             {})[1],
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zztl'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zztl-wallclock.log')).read(),
         ok=V(has=['path(s) untracked or modified'],
              hasnt=['zztl-scratch.txt']),
         bug=V(has=['zztl-scratch.txt'])),

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
    case('install-owes-a-summary-row-it-then-replaced', 'install-tables.sh',
         '38556eb',
         "the hand-work list carried `summary row ... disagrees` for rows"
         ' the same call then installed',
         # --block checks each class's summary row as it installs the
         # block, and the rows are installed after the blocks, so every
         # class reported its old row under `not optional` (Run 40's
         # install listed all ten). The lines are set aside and each class
         # is checked again once the rows are in.
         plant=lambda t: {'doc': write_rundoc(t, rundoc_text())},
         shadow=dict(extra=lambda: whole_run(['lookrts', 'ovhalf'],
                                             prefix='zzit',
                                             classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzit'],
         ok=V(has=['cross-class summary row(s) installed'],
              hasnt=["disagrees with this class's cells"]),
         bug=V(has=["disagrees with this class's cells"])),

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
                           'across 10 class block(s)'])),

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

    # THE CROSS-CLASS SUMMARY WAS TRANSCRIBED BY HAND until 2026-09-22,
    # ten rows of figures every one of which the class blocks already
    # carry -- and its BOLDING was the half sessions got wrong, Run 28
    # breaking a three-decimal tie with `--pair`, a different statistic,
    # and bolding the wrong cell of `rev`. Installed off each class's own
    # `--block`, with `summary bolds` deciding the emphasis on the
    # unrounded values.
    case('install-leaves-the-cross-class-summary-untouched',
         'install-tables.sh', 'a40f7b8',
         'ten rows of figures the class blocks already carried were'
         ' transcribed by hand, and the bolding with them',
         plant=rundoc_with_a_defaced_summary,
         # TWO HALVES, because the summary is a paired run's table: the
         # one-half state has a case of its own above and the driver is
         # right to install less there.
         shadow=dict(extra=lambda: whole_run(['lookrts', 'o2half'],
                                             prefix='zzsum',
                                             classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'o2half'},
         argv=['zzsum'],
         # `hasnt` reads the driver's OUTPUT and not the document, and
         # the per-class check reports the defaced cells there by design
         # -- `summary row `bcast` disagrees ... says 9.99` -- so what the
         # output can say is the count and the order, and `LEFT STANDING`
         # is the one marker that would mean a row went unfilled.
         ok=V(has=['10 cross-class summary row(s) installed',
                   'in the order the table already had'],
              hasnt=['LEFT STANDING']),
         bug=V(hasnt=['cross-class summary row(s) installed'])),

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
         # AND SAYS THE FILE STANDS: the write is one, after every class,
         # so a refusal on a late class left an earlier class's ADDED line
         # on the screen over a file that never changed (2026-09-18).
         ok=V(exit=1, has=['REFUSED', 'no `Across the halves:`',
                           'nothing written'])),

    case('install-says-the-file-stands-on-a-refusal', 'install-tables.sh',
         '18021d0',
         'a refusal on a late class left an earlier ADDED line on the'
         ' screen over a file that was never written',
         # The write is one, after every class, so every in-loop exit
         # leaves the file as it was; the refusal now says so, and the
         # ADDED lines print after the write. The header named
         # `git checkout --` as the undo besides, which discards every
         # uncommitted edit with the install; it names a copy aside now.
         plant=lambda t: {'doc': edited_rundoc(t, (
             '\n\n' + an_across_paragraph(), ''))},
         shadow=dict(extra=lambda: whole_run(['lookrts', 'ovhalf'],
                                     prefix='zzx5', classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzx5'],
         ok=V(exit=1, has=['nothing written']),
         bug=V(exit=1, has=['REFUSED'], hasnt=['nothing written'])),

    case('install-adds-a-missing-per-shape-line-after-the-write',
         'install-tables.sh', None,
         'CONTROL: a block with no per-shape paragraph gets one, and the'
         ' ADDED line is printed once the file is written',
         # The other side of the record above: the one path that prints
         # a success line per class, now deferred to after the write.
         # Watched 2026-09-18 on this fixture, the paragraph back in the
         # file and the line under the write.
         plant=lambda t: {'doc': rundoc_without_a_per_shape_line(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts', 'ovhalf'],
                                     prefix='zzad', classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzad'],
         ok=V(exit=0, has=['per-shape line ADDED, the block had none',
                           'computed paragraph(s) installed'],
              hasnt=['REFUSED', 'nothing written'])),

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

    case('install-writes-what-the-class-says', 'install-tables.sh', None,
         'CONTROL: a block whose `What the class says:` paragraph still'
         ' carries `___` gets this run\'s skeleton, figures in place',
         plant=lambda t: {'doc': rundoc_with_unwritten_class_says(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts', 'ovhalf'],
                                             prefix='zzws',
                                             classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzws'],
         probe=lambda subs: open(subs['doc']).read(),
         ok=V(exit=0, has=['`What the class says:` skeleton(s) installed',
                           '**What the class says:** property 1'],
              hasnt=['a skeleton left unfilled'])),

    case('install-keeps-a-written-class-says', 'install-tables.sh', None,
         'CONTROL: a `What the class says:` paragraph with no `___` is the'
         ' author\'s, and a rerun of the install leaves it',
         plant=lambda t: {'doc': edited_rundoc(t)},
         shadow=dict(extra=lambda: whole_run(['lookrts', 'ovhalf'],
                                             prefix='zzwk',
                                             classes=recorded_classes())),
         env={'DOC': '{doc}', 'BASIS': 'lookrts', 'OTHER': 'ovhalf'},
         argv=['zzwk'],
         ok=V(exit=0, has=['`What the class says:` paragraph(s) kept'],
              hasnt=['skeleton(s) installed'])),

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
         # Fourteen since 2026-09-25: --hand-tables' line joins the count.
         ok=V(exit=0, has=['14 table(s) installed'])),

    # ---- read-run.py --note, the previous pair note for the next pair ---
    case('note-read-withholds-the-handover', 'read-run.py', None,
         "CONTROL: --note drops what a preparation does not decide and"
         ' keeps its build lines',
         # Reading-list item 10 made executable. Both directions asserted:
         # a filter that dropped everything would satisfy the `hasnt` half
         # alone, and one that dropped nothing the `has` half alone.
         # WIDENED 2026-09-07 with the mode: a `[SAME]` block is --draft's
         # to carry over, so reading one here is reading a block you will
         # not type, and its CONTENT now goes with the handover and the
         # gate. Its NAME stays, --draft bringing it back. The old `has`
         # asserted the content and would have passed on the name alone,
         # which is the vacuity the widening removes.
         plant=stub_pair_note,
         argv=['--note', '{note}'],
         ok=V(exit=0,
              has=['A CARRIED BLOCK', 'md5 g912', '--list', 'handover'],
              hasnt=['ENTRY POINT FOR THE SESSION', 'GATE VERDICT',
                     'sequence         RUN in one window',
                     'the dead-spot form'])),

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

    case('draft-rewrites-a-backticked-historical-roll', 'read-run.py',
         '214e717',
         'the bare-tag rename reached a roll of every half on record and'
         ' replaced two of its members',
         # A `[SAME]` block may name a half because the PAIR has it, and it
         # may name one because the chapter once did. The bare-tag rename
         # cannot tell those apart by position, and the roll under NAMING
         # THE HALVES is the second kind: carried through a draft it comes
         # back with this run's tags standing where two historical ones
         # were, still a well-formed list, read by no checker, and carried
         # again by the next draft. Backticks are the tell -- the note
         # spells a live half bare and a rolled one in backticks -- so the
         # rename now refuses a match with a backtick on either side.
         plant=lambda t: {'note': write(
             os.path.join(t, 'run29-pair.txt'),
             "hdr\n\nA [SAME]: g912 leads, ghead follows. Every half on"
             " record is hyphen-free (`aligned`, `g912`, `ghead`,"
             " `spot`).\nHALVES: basis=g912 other=ghead\n")},
         argv=['--note', '{note}', '--draft', 'run30',
               '--halves', 'spec,nospec'],
         ok=V(exit=0,
              has=['spec leads, nospec follows',
                   '(`aligned`, `g912`, `ghead`, `spot`)'],
              hasnt=['(`aligned`, `spec`, `nospec`, `spot`)']),
         bug=V(exit=0, has=['(`aligned`, `spec`, `nospec`, `spot`)'])),

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

    case('draft-carries-the-gates-machine-check', 'read-run.py', 'c7364e1',
         "a spent machine-check reading rode into the next pair's note",
         # THE ORDER IS THE CASE, which is what the fixture's docstring
         # says: the block sits UNDER the fill-in block, so an unnamed
         # lead inherits `fill` and `_fill_skeleton` passes a paragraph
         # with no rows through unchanged. Put it after a `GATE:` block
         # and it inherits `gate` and is dropped either way, which is why
         # this is a note of its own. Found 2026-09-09 by Run 28's
         # preparation, reading every carried line as the draft's own
         # header asks -- nothing checks a pair note's prose.
         plant=stub_pair_note_machine_check,
         argv=['--note', '{note}', '--draft', 'run24',
               '--halves', 'g912,ghead'],
         ok=V(exit=0, has=['GATE: NOT RUN'], hasnt=['-3.66%']),
         bug=V(exit=0, has=['-3.66%'])),

    case('draft-carries-the-named-fills', 'read-run.py', '94a3cfd',
         "a spent post-run named-fills block rode into the next pair's"
         ' note, renamed to the new run and naming twins no build made',
         # Under the fill-in block, as the machine check's case is and for
         # its reason: there an unnamed lead inherits `fill` and passes.
         # Found 2026-09-26 by Run 41's preparation, as preflight's 10c
         # reading two twin paths gone.
         plant=stub_pair_note_named_fills,
         argv=['--note', '{note}', '--draft', 'run24',
               '--halves', 'g912,ghead'],
         ok=V(exit=0, has=['GATE: NOT RUN'], hasnt=['326 self-loops']),
         bug=V(exit=0, has=['326 self-loops'])),

    case('draft-emits-a-handover-slot-per-block', 'read-run.py', '89bdb3c',
         'the handover slot came out once per announced block, not once',
         # `NOTE_HANDOVER` carries FOUR leads, so one handover spanning an
         # ENTRY POINT paragraph and a WHAT THE PREPARATION LEARNED one
         # announces twice and the loop emitted a slot for each -- with the
         # slot NAME fixed rather than the title's, so the duplicates were
         # identical and read as a template wanting to be filled in several
         # places. The gate branch three lines above had carried the same
         # dedup since Run 26's note accumulated three gate blocks.
         # The judge reads the YOURS list rather than the body, because
         # that list joins the titles with `; ` and so turns a count into a
         # substring, which is what V can assert.
         plant=lambda t: {'note': write(
             os.path.join(t, 'run29-pair.txt'),
             "hdr\n\nENTRY POINT FOR THE SESSION THAT RUNS THIS [PAIR'S]."
             " Spent.\n\nWHAT THE PREPARATION LEARNED: nothing to carry."
             "\n\nA [SAME]: spec leads, nospec follows."
             "\nHALVES: basis=spec other=nospec\n")},
         argv=['--note', '{note}', '--draft', 'run30',
               '--halves', 'nospec,libcase'],
         ok=V(exit=0,
              has=['ENTRY POINT FOR THE SESSION THAT RUNS THIS'],
              hasnt=['ENTRY POINT FOR THE SESSION THAT RUNS THIS;'
                     ' ENTRY POINT FOR THE SESSION THAT RUNS THIS']),
         bug=V(exit=0,
               has=['ENTRY POINT FOR THE SESSION THAT RUNS THIS;'
                    ' ENTRY POINT FOR THE SESSION THAT RUNS THIS'])),

    case('draft-s-yours-list-renames-only-the-run-number', 'read-run.py',
         '89bdb3c',
         'the YOURS list named a half the drafted pair does not have',
         # The titles in that list are the PREVIOUS note's, and it renamed
         # them with `p.replace(prev, draft)` -- the run number alone --
         # where the body got the full half map. So a block led `THE BASIS
         # IS run29-spec` was listed as `THE BASIS IS run30-spec`, a half
         # this pair does not carry, two lines above the body's own heading
         # reading `run30-nospec`. It bites only where the new basis does
         # not reuse the old basis TAG, which is exactly the run that
         # renames -- and the list reads well-formed either way.
         plant=lambda t: {'note': write(
             os.path.join(t, 'run29-pair.txt'),
             "hdr\n\nTHE BASIS IS run29-spec [PAIR'S]: it publishes the"
             " table.\n\nA [SAME]: spec leads, nospec follows."
             "\nHALVES: basis=spec other=nospec\n")},
         argv=['--note', '{note}', '--draft', 'run30',
               '--halves', 'nospec,libcase'],
         ok=V(exit=0, has=['THE BASIS IS run30-nospec'],
              hasnt=['THE BASIS IS run30-spec']),
         bug=V(exit=0, has=['THE BASIS IS run30-spec'])),

    case('draft-carries-a-pairs-block-as-a-model', 'read-run.py', None,
         "CONTROL: a [PAIR'S] block crosses under a <yours> line, its"
         ' continuation with it, and the handover still does not',
         # Since 2026-09-23 the draft carries each decided block as a
         # model to rewrite, which retired the separate `--note` read a
         # preparation took only to see how the blocks had been written.
         # The `<yours>` line is the guard: run-status.sh's 2c counts it
         # until it is deleted, which the next case holds.
         plant=lambda t: {'note': write(
             os.path.join(t, 'run29-pair.txt'),
             "hdr\n\nENTRY POINT FOR THE SESSION THAT RUNS THIS [PAIR'S]."
             " Spent on run29-spec.\n\nTHE ROSTER [PAIR'S]: 5 benches on"
             " run29-spec.\n\n  and a continuation line.\n\nA [SAME]:"
             " spec leads.\nHALVES: basis=spec other=nospec\n")},
         argv=['--note', '{note}', '--draft', 'run30',
               '--halves', 'nospec,libcase'],
         ok=V(exit=0,
              has=["THE ROSTER [PAIR'S]: <yours> -- the previous pair's",
                   "THE ROSTER [PAIR'S]: 5 benches on run30-nospec",
                   'and a continuation line',
                   "ENTRY POINT FOR THE SESSION THAT RUNS THIS [PAIR'S]:"
                   ' <yours>'],
              hasnt=['Spent on'])),

    case('draft-takes-same-blocks-from-the-template', 'read-run.py', None,
         'CONTROL: a [SAME] block the template has comes from the template,'
         ' carrying the LAUNCH and RIDERS values, the HALVES line and a'
         ' named list of what ran on under it',
         # Since 2026-09-23. The note's own copy of each block had grown at
         # every carry; the template's is current by construction. The
         # fixture puts the HALVES line inside a replaced block, which is
         # the line every driver reads, and a run-on paragraph under it,
         # which is the one thing the replacement drops.
         plant=lambda t: (write(os.path.join(t, 'pair-note-template.txt'),
             'LAUNCH [SAME]: the lean launch text.\n'
             '    <env> ./run-gate.sh $R\nLAUNCH: <NAME=value ...>\n\n'
             'THE ALONE-LEG RIDERS [SAME]: the lean riders.\n'
             '    <env> SAT=1 ./run-alonelegs.sh $R <basis>\n'
             'RIDERS: clean sat\n'),
             {'note': write(os.path.join(t, 'run29-pair.txt'),
             'hdr\n\nLAUNCH [SAME]: the long old launch text of run29.\n'
             'HALVES: basis=spec other=nospec\n'
             'LAUNCH: WILDLOG=1 SATURATE=1\n\n'
             'A RUN-ON paragraph under the launch block.\n\n'
             'THE ALONE-LEG RIDERS [SAME]: old riders.\nRIDERS: clean\n\n'
             'Half names [SAME]: carried as before, run29-spec.\n')})[1],
         argv=['--note', '{note}', '--draft', 'run30',
               '--halves', 'nospec,libcase'],
         ok=V(exit=0,
              has=['the lean launch text',
                   'WILDLOG=1 SATURATE=1 ./run-gate.sh run30',
                   'LAUNCH: WILDLOG=1 SATURATE=1', 'RIDERS: clean\n',
                   'WILDLOG=1 SAT=1 ./run-alonelegs.sh run30 nospec',
                   'HALVES: basis=nospec other=libcase',
                   'DROPPED WITH THEIR BLOCK', 'A RUN-ON paragraph',
                   'carried as before, run30-nospec'],
              hasnt=['the long old launch text',
                     'SATURATE=1 SAT=1', 'RIDERS: clean sat'])),

    case('status-counts-a-carried-model-as-a-slot', 'run-status.sh', None,
         "CONTROL: a [PAIR'S] model still under its <yours> line reads NOT"
         ' DONE at 2c, named by its title',
         shadow=dict(extra=[('run97-pair.txt', NOTE_STUB
                             + "\nTHE ROSTER [PAIR'S]: <yours> -- the"
                               " previous pair's block follows as a model:"
                               ' rewrite it for this pair and delete this'
                               " line\nTHE ROSTER [PAIR'S]: 5 benches.\n")]),
         argv=['run97'],
         ok=V(exit=1, has=['1 slot(s) still <yours>', 'THE ROSTER'])),

    case('net-correction-netted-a-reducing-consumer', 'read-run.py',
         '5ccc5d9',
         'a `-sum` arm was netted against a forcing pass it never ran',
         # The arm the fixture sinks is DERIVED, not named: the first the
         # live reader calls `no_net` and not `is_control`, which is the
         # class under test and survives a rename. Every cell of it goes
         # non-positive, which is the state Run 28's bcast and flip legs
         # were in on five rows at once -- the consumer reading faster
         # than the `sum-only` control whose cost was being subtracted.
         plant=lambda t: {'run': synth_json(
             t, pop='flip', name='zz-consumer.json',
             sunk=[(sh, consumer_arms()[0])
                   for sh in class_shapes('flip')])},
         argv=['{run}', '--selftest'],
         ok=V(exit=0, hasnt=['no geomean to bracket']),
         bug=V(exit=1, has=['a cell the forcing term did not leave positive,'
                            ' so this row has no geomean to bracket'])),

    case('fingerprint-names-an-arm-with-no-corrected-time', 'read-run.py',
         None,
         'CONTROL: the kept per-shape table names no arm the `time` column'
         ' reads as `--`',
         # The two columns agreed by construction while `is_control` WAS
         # `no_net` plus the twins; once the reducing consumers joined
         # `no_net` alone, this column went on dividing their nets. Held
         # here rather than left to agree again by accident: the assertion
         # is over the arm names the column prints, so it bites whenever
         # the filter and `time_of` part.
         plant=lambda t: {'run': synth_json(t, pop='main',
                                            name='zz-fp.json')},
         argv=['{run}', '--fingerprint'],
         # The `has` is not decoration: a `hasnt` alone passes on output
         # that says nothing at all, and this mode printing an empty table
         # would satisfy it. The column head is what the assertion is
         # about, so it is what anchors it.
         ok=V(exit=0, has=['best outside vecdims'],
              hasnt=['`%s`' % a for a in consumer_arms()])),

    case('draft-carries-a-block-naming-another-run-unmarked', 'read-run.py',
         None,
         'CONTROL: a carried [SAME] block naming a run the rename does not'
         ' touch is flagged, and one naming only the previous run is not',
         # The renames map the PREVIOUS run onto this one and touch no
         # other number, so a `[SAME]` block quoting an older run's figure
         # comes through pointing one run too far back and reads as
         # correctly carried, every name in it having been substituted.
         # Both directions in one fixture: the first block names run21,
         # which no rename reaches, and the second names run23, which is
         # the previous run and becomes run24 -- so the notice must name
         # the first and not the second.
         plant=lambda t: {'note': write(
             os.path.join(t, 'run23-pair.txt'),
             "hdr\n\nOLD [SAME]: against run21-g912, the previous build of"
             " this recipe.\n\nMINE [SAME]: run23-g912 leads.\n"
             "HALVES: basis=g912 other=spot\n")},
         argv=['--note', '{note}', '--draft', 'run24',
               '--halves', 'g912,ghead'],
         ok=V(exit=0, has=['CHECK THESE CARRIED BLOCKS', 'OLD',
                           'names Run 21'],
              hasnt=['MINE                ', 'names Run 23'])),

    case('draft-notice-names-the-line-and-not-only-the-block',
         'read-run.py', None,
         'CONTROL: a flagged [SAME] block carries the LINES that name the'
         ' old run under it, and an innocent line of the same block does'
         ' not come with them',
         # The block-level notice says which block is stale and leaves a
         # dozen lines to re-read for the clause that is; Run 35's five
         # rewrites were each one sentence inside a flagged block. Both
         # directions in one fixture: the second line names run21 and must
         # appear under the row, the first names nothing and must not.
         plant=lambda t: {'note': write(
             os.path.join(t, 'run23-pair.txt'),
             "hdr\n\nOLD [SAME]: a line that names nothing.\n"
             "against run21-g912, the previous build of this recipe.\n"
             "\nHALVES: basis=g912 other=spot\n")},
         argv=['--note', '{note}', '--draft', 'run24',
               '--halves', 'g912,ghead'],
         ok=V(exit=0, has=['names Run 21',
                           '| against run21-g912, the previous build'],
              hasnt=['| a line that names nothing'])),

    case('draft-flags-a-carried-block-asserting-a-compile-option',
         'read-run.py', None,
         'CONTROL: a carried [SAME] block naming a compile option is'
         ' flagged for it, and an RTS option is not one',
         # An old run number in a carried block points one run too far back
         # and may be right; a COMPILE OPTION in one is a claim about this
         # pair's regime and goes false the moment the variable changes.
         # Both directions in one fixture: the first block asserts
         # `-fspec-constr` and names no run at all, so the run-number test
         # cannot reach it, and the second names an RTS option and a cabal
         # flag, neither of which reaches the optimiser. Non-vacuous by
         # `--at`: at the parent revision this fixture draws NO notice at
         # all, neither block naming a run, which is the gap it closes.
         plant=lambda t: {'note': write(
             os.path.join(t, 'run30-pair.txt'),
             "hdr\n\nOPT [SAME]: NEITHER half carries `-fspec-constr`.\n\n"
             "RTS [SAME]: -A32m on both, passed through --ghc-options.\n"
             "HALVES: basis=nospec other=libcase\n")},
         argv=['--note', '{note}', '--draft', 'run31',
               '--halves', 'nospec,o2'],
         ok=V(exit=0, has=['CHECK THESE CARRIED BLOCKS',
                           'asserts -fspec-constr'],
              hasnt=['RTS      ', 'asserts -A32m',
                     'asserts --ghc-options'])),

    case('doc-prints-one-part-of-the-docstring', 'read-run.py', None,
         'CONTROL: --doc modes prints the Modes list with the two gates in'
         ' it and not its neighbours',
         # The pre-run list's step 7 asks for the Modes list, --para,
         # --section and the two gates, and the only way to any of them was
         # the whole docstring, which a preparation then carries for the
         # rest of its session. It needs no run file and no README, which
         # is why this case runs from an empty directory.
         argv=['--doc', 'modes'],
         ok=V(exit=0, has=['Modes:', '--lint', '--check-doc', '--para',
                           '--section'],
              hasnt=['Definitions, once:', 'Validation:'])),

    case('doc-prints-the-span-grammar', 'read-run.py', None,
         'CONTROL: --doc spans prints the `predict:` grammar, which lives in'
         ' a function\'s docstring and in no part of the module\'s',
         # A preparation writing Run 40's registration reached the grammar
         # only by reading source, `grep -n` and `sed` over this script.
         argv=['--doc', 'spans'],
         ok=V(exit=0, has=['`predict: cross ARM X',
                           '`predict: countdiff A B under N',
                           'A CROSS-HALF KIND SCOPED `both` IS READ TWICE'],
              hasnt=['Modes:'])),

    case('doc-refuses-a-part-that-is-not-one', 'read-run.py', None,
         'CONTROL: --doc with a name that is no part refuses at 2 rather'
         ' than printing the lot',
         argv=['--doc', 'nosuch'],
         ok=V(exit=2, has=['no part `nosuch`'], hasnt=['Modes:'])),

    case('note-figures-reads-a-row-only-as-present', 'preflight.sh', None,
         'CONTROL: --figures holds each derived figure to the note ROW of'
         ' its own label, not to the note anywhere',
         # NO CASE, and for a reason of its own rather than the one the
         # record below gives preflight: --figures reads the two BINARIES,
         # which are not tracked, and the mutants copy holds tracked files
         # alone -- a stub half cannot answer `size -A`, having no ELF in
         # it. Watched instead, 2026-09-10, on Run 28's own pair and note:
         # three figures planted wrong -- one md5 digit, `.text` off by
         # one on the control half, and `deadbee` for the shim commit --
         # and each was named with its row and both readings, the note
         # restored from a copy taken first. Clean before and after.
         argv=None, ok=None, no_audit='too-dangerous-to-run'),

    # ---- smoke-l1.sh, the roster pass ------------------------------------
    case('roster-pass-prints-a-failing-mode-as-rc-0', 'smoke-l1.sh',
         '11767f9',
         'a required mode that exited non-zero was reported as rc=0',
         # NO CASE: reaching the branch wants a real -L1 leg whose reader
         # mode fails, and the driver refuses a previous attempt's
         # artifacts, so a fixture would have to write such a leg's JSON
         # into this directory -- where `properties.py` reads every run on
         # disk and would then fail on it, which is the state Run 28's own
         # pass left. Watched instead, on that pass; the shell semantics
         # were confirmed directly.
         argv=None, ok=None, no_audit='too-dangerous-to-run'),

    # ---- preflight.sh, the pre-run list's steps 4 to 10 in one call -----
    # ---- what nothing read, and what nothing subtracted ---------------
    # THE REGISTRATION, both arms. The fixture is SYNTHETIC and appended
    # rather than an edit of the live entry: a registration lives in the
    # open list only until post-run step 5 moves it into the run's own
    # file, so a fixture editing the live one stops building the day its
    # run is written up.
    case('movement-reads-the-column-it-overwrites', 'read-run.py', None,
         "post-run 5a's movement reading had no mode, so two runs took it"
         ' by hand and one published sixteen points for a row that moved'
         ' fourteen, having divided the table\'s three decimals',
         # It reads the same two sources the install does -- `readme_rows`
         # for the table in the run file, `strategy_rows` for this run --
         # so the movement cannot disagree with what `--markdown` is about
         # to write over it. And it says what the hand reading did not:
         # `there` is three decimals, so a move under a point is inside
         # the rounding and no reading at all.
         plant=lambda t: {'j': synth_json(t, 'main'),
                          'doc': rundoc_with_a_results_table(t)},
         argv=['{j}', '--movement', '--run-doc', '{doc}'],
         ok=V(exit=0, has=['against the table in', 'points',
                           "`there` is the table's own THREE decimals"])),

    # ---- the note's COMPARE line, the earlier run of every cross-run reading
    case('movement-defaults-to-the-compare-run', 'read-run.py', None,
         'CONTROL: --movement with no --run-doc reads the COMPARE run\'s'
         ' file beside the JSON, not the newest in runs/',
         plant=pair_with_a_compare_run,
         argv=['{j}', '--movement'],
         ok=V(exit=0, has=['against the table in', 'run97.md'])),

    case('bridge-defaults-to-the-compare-run', 'read-run.py', None,
         'CONTROL: --bridge with no --compare takes the same half of the'
         ' COMPARE run, by role and not by name',
         plant=pair_with_a_compare_run,
         argv=['{j}', '--bridge'],
         ok=V(exit=0, has=['run97-nospec-main.json'])),

    case('half-movers-default-to-the-compare-run', 'read-run.py', None,
         'CONTROL: --half-movers RUN alone takes PREV off the COMPARE line',
         plant=pair_with_a_compare_run,
         argv=['--half-movers', '{run}'],
         ok=V(exit=0, has=['run97'], hasnt=['no COMPARE line'])),

    case('half-movers-name-the-widest-cell', 'read-run.py', 'c1feef3',
         'a flagged half-local mover gave no cell to time, so each copy test'
         ' began by hand-parsing --compare --per-shape',
         # Run 41's copy test needed the widest cell of each of eight
         # movers and a one-off script found them. The mover here is
         # slowed on one shape alone, so that shape is the widest cell.
         plant=plant_half_mover,
         argv=['--half-movers', '{run}'],
         ok=V(exit=0, has=['lib-stage1', main_shapes()[0]]),
         bug=V(exit=0, hasnt=[main_shapes()[0]])),

    case('half-movers-refuse-without-prev-or-compare', 'read-run.py', None,
         'CONTROL: --half-movers RUN alone, with no COMPARE line, is refused'
         ' naming both ways out',
         plant=lambda t: {'run': (write(os.path.join(t, 'run98-pair.txt'),
                                        NOTE_STUB), os.path.join(t, 'run98'))[1]},
         argv=['--half-movers', '{run}'],
         ok=V(exit=2, has=['no COMPARE line'])),

    case('compare-line-naming-no-run-is-refused', 'read-run.py', None,
         'CONTROL: a COMPARE line naming a path is refused, not taken for'
         ' a run nobody has',
         plant=lambda t: {'run': (write(os.path.join(t, 'run98-pair.txt'),
                                        NOTE_STUB + 'COMPARE: runs/run97.md\n'),
                                  os.path.join(t, 'run98'))[1]},
         argv=['--half-movers', '{run}'],
         ok=V(exit=2, has=['COMPARE: run<N>'])),

    case('series-reads-one-cell-over-every-run', 'read-run.py', None,
         'CONTROL: --series prints one cell\'s ratio run by run and half by'
         ' half, each beside that half\'s floor, off the notes and JSONs in'
         ' a directory',
         # Run 34's write-up requoted `mut-odo-vecdims` over `bq-expand` on
         # `stretch-pow2stride` for every run since Run 30 in four places.
         plant=lambda t: {'dir': (
             write(os.path.join(t, 'run98-pair.txt'), NOTE_STUB),
             write(os.path.join(t, 'run99-pair.txt'), 'a stand-in pair note.\n'
                   'HALVES: basis=nospec other=ghead\n'),
             [synth_json(t, 'main', name='%s-main.json' % n)
              for n in ('run98-lookrts', 'run98-a1g', 'run99-nospec',
                        'run99-ghead')], t)[-1]},
         argv=['--series', 'mut-odo-vecdims', 'bq-expand',
               'stretch-pow2stride', '{dir}'],
         ok=V(exit=0, has=['| run98 | lookrts | ', '| run99 | nospec | ',
                           '| run | basis | ratio | floor | control | ratio'
                           ' | floor |'])),

    case('floor-pairs-reads-every-population', 'read-run.py', None,
         'the standing floor-pair registration -- the A/A copies against'
         ' their originals -- had no mode, so Run 32 read it as sixteen'
         ' spans and Run 33 by a script written for the evening and thrown'
         ' away',
         # It is the reader's own `aa_pairs` and `aa_floor`, the helpers
         # the class block and the chapter already share, so this mode
         # and `--aa` cannot disagree without disagreeing with
         # themselves. It prints and never judges: the floor IS the
         # widest of the pairs it lists, so `inside its own floor` is
         # true by construction and a verdict column would be a silent
         # search -- what the registration asks is how wide it is and
         # which pair carries it.
         plant=lambda t: {'j': synth_json(t, 'main',
                                          name='run95-x-main.json')},
         argv=['--floor-pairs', '{tmp}/run95'],
         ok=V(exit=0, has=['run95-x-main.json -- floor',
                           'carried by', 'carries it in 1 of 1',
                           '1 population(s)'])),

    case('check-doc-abstention-names-its-patterns', 'read-run.py', None,
         'the abstention named the patterns it wanted and not the site it'
         ' had already matched, so an author who reworded one of two sites'
         ' grepped the documents for the other',
         # The comment beside the abstention has named this case since
         # 2026-09-15 and no case carried the name. Run 33 reworded four
         # of these paragraphs in one stretch, met four abstentions, and
         # went looking for the surviving site each time; the figure is
         # enough to find it, these being quoted twice and no more.
         # The anchor is the sentence's run-independent prefix, the
         # figures after it being the run's: Run 34's write-up requoted
         # Run 33's `0.47% and 0.62%` and the fixture stopped building.
         plant=lambda t: {'readme': unwrapped_readme_edit(
             t,
             'Over the four pairs that carry back to Run 10 this run reads',
             'Over those same four pairs this run reads')},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1, has=['could not locate at least two sites quoting the'
                           " run's carry-back figure", 'It found 1:',
                           'It looked for:'])),

    case('registration-lead-is-the-movers-key', 'read-run.py', None,
         'a registration whose bold lead carried one clause more passed'
         ' pre-run 7 and was refused by --move-registration after the run,'
         ' when the entry had been committed for a day and the hours were'
         ' spent',
         # `--move-registration` matches the lead WHOLE and refuses
         # anything else; nothing held the lead where it is written. Run
         # 33 declared its pair with the recipes named inside the bold
         # span, `--lint` and `--check-doc` both passed it, and the move
         # refused at post-run step 5. The clause belongs in the body,
         # where it travels into the run file with the rest.
         plant=lambda t: {'readme': readme_with_a_registration(
             t, lead_extra='declared by request, the recipes in Run 98')},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['not the form --move-registration matches'])),

    case('registration-lead-in-the-movers-form-passes',
         'read-run.py', None,
         'CONTROL: the canonical lead is not reported, so the check cannot'
         ' be read as firing on every registration',
         plant=lambda t: {'readme': readme_with_a_registration(t)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(hasnt=['not the form --move-registration matches'])),

    case('lint-names-a-section-that-points-at-no-registration',
         'read-run.py', None,
         'a compares-against section declaring the next run\'s pair while'
         ' the open list registers one, with no pointer between them, went'
         ' unnamed -- and on Run 35 the two declared DIFFERENT pairs, this'
         ' check reading a registration\'s arms and not its pair',
         plant=lambda t: {'readme': readme_with_a_registration(t),
                          'prev': prev_rundoc_for_a_registration(t, False)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['names no registration'])),

    case('lint-passes-a-section-that-names-the-registration',
         'read-run.py', None,
         'CONTROL: the same section carrying its `[registered ...][open]`'
         ' pointer is not named',
         plant=lambda t: {'readme': readme_with_a_registration(t),
                          'prev': prev_rundoc_for_a_registration(t, True)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(hasnt=['names no registration'])),

    case('lint-notes-a-count-prior-with-no-sweep', 'read-run.py', None,
         'a registration quoting an instruction count whose sweep is on no'
         ' disk here is a figure pre-run 12b cannot read back: Run 35\'s'
         ' items (2) and (3) quoted a plain build\'s counts and 12b could'
         ' re-derive their times and not their instructions',
         plant=lambda t: {'readme': readme_with_a_registration(
             t, views_only=True)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(has=['quotes a count prior for'])),

    case('lint-passes-a-count-prior-whose-sweep-is-here', 'read-run.py', None,
         'CONTROL: the same span with a counts file naming both arms is'
         ' not noted',
         plant=lambda t: {'readme': readme_with_a_registration(
             t, views_only=True),
                          'sweep': write(
                              os.path.join(t, 'run98-counts-exit.txt'),
                              'shape mut-odo-vecdims 10 100\n'
                              'shape bq-expand 10 200\n')},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(hasnt=['quotes a count prior'])),

    case('registration-arm-is-not-timed', 'read-run.py', 'f40fad2',
         'nothing here read a registration, and Run 24 lost a clause of one',
         plant=lambda t: {'readme': readme_with_a_registration(
             t, arm=parked_arm())},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['registration names arms the roster does not'
                           ' time']),
         # Before the fix `--lint` read no registration at all, so the
         # planted one passed with the rest.
         bug=V(exit=0, hasnt=['registration'])),

    case('registration-defers-to-a-missing-task', 'read-run.py', 'f40fad2',
         'a registration deferred to a task number that was not there',
         plant=lambda t: {'readme': readme_with_a_registration(t, task='999')},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['defers to task(s) that are not under the tasks'
                           ' heading: 999']),
         bug=V(exit=0, hasnt=['registration'])),

    case('registration-deferral-target-arm-is-not-timed', 'read-run.py',
         None,
         "a registration's deferral target named a parked arm and only the"
         ' registration itself was read',
         # `--lint` has held an OPEN registration's own backticked arms to
         # the timed roster since f40fad2, and checked that each `task N`
         # it defers to RESOLVES -- and nothing about what that task then
         # names. Run 25's item (4) deferred to task 10, three of whose
         # four class predictions are stated against `lib-stage2` and
         # `canon-vecdims`, parked the day after they were written: three
         # predictions of four unreadable before the machine was started,
         # past a check that reported the pointer good.
         plant=lambda t: {'readme': readme_with_a_registration(
             t, task_arm=parked_arm())},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['defers to task 99, which names arms the roster'
                           ' does not time'])),

    case('predictions-read-each-span-on-its-scope', 'read-run.py', None,
         'CONTROL: a span is read only on the population and half it names,'
         ' and the cell and countdiff kinds read what they name',
         plant=scoped_spans_run,
         argv=['{a}', '--compare', '{b}', '--predictions', '--run-doc',
               '{rundoc}', '--counts', '{ca}', '{cb}'],
         ok=V(has=['out of scope, this file being main on the basis half',
                   '6 span(s): 4 HELD, 1 KILLED, 0 not read, 1 out of scope',
                   'item(s) adjudicated by a committed script: (7)'
                   ' read-run.py'])),

    case('predictions-scope-a-half', 'read-run.py', None,
         'CONTROL: on the control half a basis span is out of scope too',
         plant=scoped_spans_run,
         argv=['{b}', '--compare', '{a}', '--predictions', '--run-doc',
               '{rundoc}', '--counts', '{cb}', '{ca}'],
         ok=V(has=['out of scope, this file being main on the control half',
                   '6 span(s): 3 HELD, 1 KILLED, 0 not read, 2 out of'
                   ' scope'])),

    case('registration-drift-names-the-commits-after-it',
         'registration-drift.py', None,
         'CONTROL: a commit to Main.hs after the registration and before the'
         ' build is listed with the definition it touched, exit 1',
         plant=lambda t: drift_repo(t, moved=True),
         argv=['run97', '--dir', '{dir}'],
         ok=V(exit=1, has=['rebuild the fill', 'in: fooFill',
                           '1 commit(s) the registration did not see'])),

    case('registration-drift-is-quiet-over-an-unmoved-source',
         'registration-drift.py', None,
         'CONTROL: a build from the registration\'s own source lists nothing,'
         ' exit 0',
         plant=lambda t: drift_repo(t, moved=False),
         argv=['run97', '--dir', '{dir}'],
         ok=V(exit=0, has=['no commit to Main.hs between them'])),

    case('drift-since-names-the-arms-a-commit-reaches',
         'registration-drift.py', None,
         'CONTROL: --since names the definition a commit changed and the'
         ' roster arm reaching it through a caller, and the arm it does not',
         plant=lambda t: drift_since_repo(t, code=True),
         argv=['run97', '--since', 'run96', '--dir', '{dir}'],
         ok=V(exit=1, has=['rebuild the fill', 'code: fooFill',
                           'arms: lib-a', 'by none: lib-b'])),

    # ---- registration-drift.py --since, and a pragma read as a comment --
    # `defs_of` ended a definition at every unindented line and kept only
    # those naming one, so a column-0 `{-# INLINE f #-}` -- 164 of them in
    # Main.hs -- and every `data`, `newtype` and `instance` line belonged to
    # nothing, and a commit changing only those printed `code: none --
    # comments only` and reached no arm. Found 2026-09-25 by a blind read
    # of the session that wrote it.
    case('drift-since-reads-a-pragma-as-a-comment',
         'registration-drift.py', 'e9c02a6',
         'a commit changing only an INLINE pragma was reported as comments'
         ' only, reaching no arm',
         plant=lambda t: drift_since_repo(t, pragma=True),
         argv=['run97', '--since', 'run96', '--dir', '{dir}'],
         ok=V(exit=1, has=['inline the fill', 'code: fooFill',
                           'arms: lib-a'],
              hasnt=['comments only']),
         bug=V(exit=1, has=['comments only'])),

    case('drift-since-reads-a-comment-only-commit-as-one',
         'registration-drift.py', None,
         'CONTROL: a commit moving only a comment changes no definition and'
         ' reaches no arm',
         plant=lambda t: drift_since_repo(t, code=False),
         argv=['run97', '--since', 'run96', '--dir', '{dir}'],
         ok=V(exit=1, has=['note the fill', 'code: none -- comments only',
                           'by none: lib-a, lib-b'],
              hasnt=['arms: lib-a'])),

    case('predictions-in-place-keeps-the-headings-two-blanks', 'read-run.py',
         'd941cc6',
         'the in-place writer stripped every paragraph\'s leading newline,'
         ' so each heading kept after two blank lines came back after one',
         # Run 39's write-up met it as five headings of its run file at
         # one blank, found by --check-doc on one of them and by hand on
         # the rest; replayed tool by tool on a copy, 2026-09-23.
         plant=scoped_spans_two_blanks,
         argv=['{a}', '--compare', '{b}', '--predictions', '--in-place',
               '--run-doc', '{rundoc}'],
         probe=lambda subs: heading_spacing_word(subs['rundoc']),
         ok=V(has=['HEADINGS KEEP TWO BLANKS']),
         bug=V(has=['HEADING LOST ITS BLANK'])),

    case('predictions-write-the-span-readings-in-place', 'read-run.py', None,
         'CONTROL: --predictions --in-place reads every population on both'
         ' halves and writes the readings under each item carrying spans'
         ' and no script, leaving the verdict and the tally to write',
         plant=lambda t: scoped_spans_in_place(t),
         argv=['{a}', '--compare', '{b}', '--predictions', '--in-place',
               '--run-doc', '{rundoc}'],
         probe=lambda subs: open(subs['rundoc']).read(),
         ok=V(exit=0, has=['**Read by --predictions, item (1):** `cross list'
                           ' 1.0 within 99% on main both`: HELD on main'
                           ' basis', 'HELD on main control',
                           '**Read by --predictions, item (6):**',
                           'KILLED on main basis',
                           'read on no population and half here'],
              hasnt=['item (7):'])),

    case('predictions-in-place-replaces-its-own-paragraph', 'read-run.py',
         None,
         'CONTROL: a rerun replaces the paragraph an earlier call wrote and'
         ' does not add a second',
         plant=lambda t: scoped_spans_in_place(t, stale=True),
         argv=['{a}', '--compare', '{b}', '--predictions', '--in-place',
               '--run-doc', '{rundoc}'],
         probe=lambda subs: (lambda t: 'item-1-paragraphs=%d stale=%s' % (
             t.count('item (1):**'), 'STALE' in t))(
                 open(subs['rundoc']).read()),
         ok=V(exit=0, has=['item-1-paragraphs=1 stale=False'])),

    case('registration-span-carries-its-scope', 'read-run.py', None,
         'CONTROL: an OPEN registration\'s span with no `on POP` and no half'
         ' is refused, a span read on every file it is handed being how'
         ' thirteen of Run 30\'s main-set spans were KILLED for the wrong'
         ' question',
         plant=lambda t: {'readme': readme_with_a_registration(
             t, unscoped=True)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['carries no scope'])),

    case('registration-views-are-no-population-scope', 'read-run.py', None,
         'CONTROL: `on views S` names shapes and not a population, so a'
         ' countdiff span carrying it and no `on POP` is refused as unscoped',
         # The scope test once looked for an `on` token anywhere, and the
         # `on` of `on views` satisfied it, so the span passed lint and was
         # read on every file it was handed. Found by review, 2026-09-17.
         plant=lambda t: {'readme': readme_with_a_registration(
             t, views_only=True)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['item (6) span `predict: countdiff',
                           'carries no scope'])),

    case('section-falls-back-to-a-bolded-lead', 'read-run.py', None,
         'CONTROL: `--section` on a name that is a BOLDED LEAD and not a'
         ' heading prints that paragraph and says which it was',
         # Half the chapter's named subjects are leads rather than
         # headings, and note-check's own roll message sends a reader to
         # one by name. Refusing outright sent Run 36's preparation to
         # `grep` for a tag and `sed` for a window -- the path into the
         # chapter this mode exists to avoid. Added 2026-09-19.
         plant=lambda t: {'readme': README},
         argv=['--section', 'Which two halves a pair has',
               '--readme', '{readme}'],
         ok=V(exit=0, has=['this is a BOLDED LEAD',
                           'Which two halves a pair has is a property'])),

    case('section-lead-is-narrowed', 'read-run.py', None,
         'CONTROL: `--section` on a name several bolded leads carry lists'
         ' them and refuses, as the heading branch does, rather than'
         ' printing the first',
         # The first draft of the fallback printed match one and returned
         # 0, so `--section 'the note'` handed back one of seven leads and
         # read as an answer. Found by the transcript pass the day the
         # fallback landed, 2026-09-19.
         plant=lambda t: {'readme': README},
         argv=['--section', 'the note', '--readme', '{readme}'],
         ok=V(exit=1, has=['bolded lead(s) do; narrow it to one'])),

    case('section-names-para-when-nothing-matches', 'read-run.py', None,
         'CONTROL: `--section` on a name that is neither heading nor lead'
         ' still refuses, and names `--para` -- which is what says the'
         ' case above did not pass for matching everything',
         plant=lambda t: {'readme': README},
         argv=['--section', 'No such subject anywhere', '--readme',
               '{readme}'],
         ok=V(exit=1, has=['no heading and no bolded lead matches',
                           '`--para PATTERN` searches every paragraph'])),

    case('registration-both-on-a-non-unity-cross', 'read-run.py', None,
         'CONTROL: `both` on a cross-half span whose target is away from 1'
         ' is refused, the two halves reading it as reciprocals',
         # `cross` and `counts` read THIS half over the other, so `both`
         # reads one span twice, once each way. Run 36's registration
         # wanted `cross list 1.2974`; had it written `both`, half its
         # spans would have been unholdable the day they were written.
         # A SECOND WAY for a span's vocabulary to ask what its prose did
         # not, and not Run 35's item (3), whose target was 1.0 and which
         # this refusal allows: that one died of its band. The grammar
         # admits
         # it and the arms-and-scope checks cannot see it. Found
         # preparing Run 36, refused since 2026-09-19.
         plant=lambda t: {'readme': readme_with_a_registration(
             t, cross_both_target='1.2974')},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['item (1) span `predict: cross list 1.2974',
                           'scoped `both` on a cross-half kind',
                           '0.7708 on the control'])),

    case('registration-item-is-adjudicable', 'read-run.py', None,
         'CONTROL: an item with neither a span nor a committed script is'
         ' refused, Run 34 having read four items\' clauses by hand',
         plant=lambda t: {'readme': readme_with_a_registration(t, bare=True)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['item (5) carries neither a `predict:` span nor'
                           ' a committed `script:`'])),

    case('registration-script-is-committed', 'read-run.py', None,
         'CONTROL: a `script:` naming no committed file is refused',
         plant=lambda t: {'readme': readme_with_a_registration(
             t, arm='list', script='zz-no-such-script.py')},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1, has=['zz-no-such-script.py, which is not committed'])),

    case('registration-clean-reads-ok', 'read-run.py', None,
         'CONTROL: a registration naming a timed arm and no task passes,'
         ' which is what says the two above failed for their planting',
         plant=lambda t: {'readme': readme_with_a_registration(t)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=0, has=['every arm the OPEN registration(s) name is'
                           ' timed'])),

    case('registration-span-reads-are-printed', 'read-run.py', 'b104ba1',
         'under an OPEN registration --lint prints each span as'
         ' --predictions will compare it -- the mode, the operands and their'
         ' orientation -- for the author to read against the sentence',
         # Run 35's item (3) spanned a claim about the PREVIOUS run as
         # `counts`, which compares the two HALVES, and --lint held the
         # span's arms and scope only; registered and answered 2026-09-18.
         plant=lambda t: {'readme': readme_with_a_registration(t)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=0, has=['`predict: cross list 1.0 within 3% on main'
                           ' both`', 'on THIS half over the same arm on'
                           ' the OTHER']),
         bug=V(exit=0, hasnt=['on THIS half over the same arm'])),

    case('gate-show-derives-the-selection', 'run-gate.sh', None,
         'CONTROL: --show prints SEL and the count it derives, and spends'
         ' no machine',
         shadow=dict(extra=[('zzshow-a1g', FAKE_HALF),
                            ('zzshow-lookrts', FAKE_HALF),
                            ('zzshow-pair.txt', NOTE_STUB)]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzshow', '--show'],
         # Three shapes and five globs in the stand-in, so 15.
         ok=V(exit=0, has=['glob   */list', 'arms   5', 'shapes 3',
                           'expect 15 benches a process'],
              hasnt=['expecting'])),

    case('gate-show-absorbs-a-third-argument', 'run-gate.sh', None,
         'a third word after --show was taken without effect or error',
         # No fix_rev: the defect and its repair are the same day and the
         # same body of work as `--show` itself, so there is no commit at
         # which the flag exists and the refusal does not. A control, then,
         # guarding forward -- which is what the corpus's third kind is for.
         shadow=dict(extra=[('zzshow2-a1g', FAKE_HALF),
                            ('zzshow2-lookrts', FAKE_HALF),
                            ('zzshow2-pair.txt', NOTE_STUB)]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzshow2', '--show', 'nonsense'],
         ok=V(exit=2, has=['too many arguments'],
              hasnt=['expect 15 benches a process'])),

    case('gate-show-names-the-compare-run', 'run-gate.sh', None,
         'CONTROL: --show names the run file the machine check reads, off'
         ' the note\'s COMPARE line',
         # run32.md is a record and stays, so the shadow's symlinked runs/
         # carries it.
         shadow=dict(extra=[('zzshow3-a1g', FAKE_HALF),
                            ('zzshow3-lookrts', FAKE_HALF),
                            ('zzshow3-pair.txt',
                             NOTE_STUB + 'COMPARE: run32\n')]),
         argv=['zzshow3', '--show'],
         ok=V(exit=0, has=['compare runs/run32.md'])),

    case('gate-refuses-a-compare-run-with-no-file', 'run-gate.sh', None,
         'CONTROL: a COMPARE run with no run file is refused before the'
         ' machine, whose check would read nothing after forty minutes',
         shadow=dict(extra=[('zzshow4-a1g', FAKE_HALF),
                            ('zzshow4-lookrts', FAKE_HALF),
                            ('zzshow4-pair.txt',
                             NOTE_STUB + 'COMPARE: run1\n')]),
         argv=['zzshow4', '--show'],
         ok=V(exit=1, has=['runs/run1.md'], hasnt=['expect 15 benches'])),

    case('delta-of-a-build-against-itself-moves-nothing', 'loop-offsets.py',
         None,
         'CONTROL: --delta of one binary against itself keeps every offset'
         ' and moves no address',
         # A system binary rather than a run's: a case pinned to `run<N>-`
         # artifacts rots at the deletion offer, which three fixtures here
         # already did once.
         # `--code ''`: a system binary has no Main-compiled code, and the
         # population --delta reads by default is Main's (2026-09-04).
         argv=['--delta', '/bin/sh', '/bin/sh', '--len', '0', '--code', ''],
         ok=V(exit=0, has=['nothing moved', 'every mod-64 offset preserved',
                           'survive to the byte'],
              hasnt=['offsets MOVED', 'NOT a whole line'])),

    case('delta-names-a-group-one-side-lacks', 'loop-offsets.py', None,
         'CONTROL: a group in one binary and not the other is named as'
         ' such rather than dropped, which is what a compiler change does',
         argv=['--delta', '/bin/sh', '/bin/cat', '--len', '0', '--code', ''],
         # AND THE SUMMARY SAYS SO. It used to count only the groups it
         # had compared, so a pair sharing no group at all read `0 group(s)
         # kept every offset; 0 group(s) moved at all` -- which is what
         # `nothing moved` looks like and means `nothing was compared`.
         # The count itself is /bin/sh's and not this case's: it read 3
         # until the survey parsed long instructions whole and 4 after, so
         # the claim is that it is not 0.
         ok=V(exit=0, has=['IN /bin/sh ONLY',
                           'matched nothing on the other side'],
              hasnt=[' 0 matched nothing', 'group(s) moved at all'])),

    case('delta-sees-a-group-that-grows-past-the-threshold',
         'loop-offsets.py', 'b39ff49',
         'a group under --min-copies in OLD and over it in NEW was in'
         ' neither selection, so the one group whose copy count is the'
         ' finding was dropped in silence',
         # NOT AUDITED: the fixture is a listing, which the reader before
         # 8b4f51d could not open. Watched 2026-09-04 on run24-g912 against
         # run25-g912 at --len 0: a 34-byte group read `1 -> 2 copies` at
         # --min-copies 1 and vanished at the default.
         plant=lambda t: delta_listings(t, 'grows'),
         argv=['--delta', '{old}', '{new}'],
         ok=V(exit=0, has=['1 -> 2 copies', 'copy COUNT moved']),
         no_audit='fixture-from-a-document-the-era-lacks'),

    case('delta-reads-moved-offsets-and-displacements', 'loop-offsets.py',
         None,
         'CONTROL: heads moving off their offsets, an address surviving and'
         ' the displacements are read as such -- the direction the identity'
         ' control cannot see, so a reader reporting preservation'
         ' unconditionally passed it',
         plant=lambda t: delta_listings(t, 'moves'),
         argv=['--delta', '{old}', '{new}'],
         ok=V(exit=0, has=['offsets MOVED: [0, 0] -> [0, 8]',
                           'NO address survives to the byte',
                           '2 displacement(s): 0x40, 0x108 (NOT a whole'
                           ' line)',
                           'every mod-64 offset preserved: [0, 0]',
                           '1 address(es) survive to the byte: 0x403000',
                           '1 displacement(s): 0x40',
                           'of the 2 compared: 1 kept every offset, 2 moved'
                           ' at all'])),

    case('delta-leaves-the-library-groups-to-library', 'loop-offsets.py',
         '8b4f51d',
         "a linked library's loops stood among the tracked groups and in the"
         ' summary a note copies, where --match and --survey read Main alone',
         # NOT AUDITED: a listing, which the reader before the fix could not
         # open. Watched 2026-09-04 on both halves of Run 25: the statistics
         # Quantile pair, [39, 47] on the basis, counted as a third group.
         plant=lambda t: delta_listings(t, 'library'),
         argv=['--delta', '{old}', '{new}'],
         ok=V(exit=0, has=['1 group(s) read',
                           '4 library loop(s) left to --library']),
         no_audit='fixture-from-a-document-the-era-lacks'),

    case('roster-delta-reads-two-listings', 'roster-delta.py', None,
         'CONTROL: two identical listings move nothing, and the survivors'
         ' keep their order',
         plant=lambda t: {'old': stub_half(t, 'zzrd-old'),
                          'new': stub_half(t, 'zzrd-new')},
         argv=['{old}', '{new}'],
         ok=V(exit=0, has=['main set: 15 -> 15 benches, 5 -> 5 arms over'
                           ' 3 -> 3 shapes',
                           'in the same order', 'unmoved',
                           'views per class (2 -> 2 classes)'])),

    case('roster-delta-refuses-a-listless-half', 'roster-delta.py', None,
         'CONTROL: a binary that answers nothing exits 2 rather than'
         ' reporting an empty roster, which reads like a true statement',
         plant=lambda t: {
             'a': stub_half(t, 'zzrd-mute', '#!/bin/sh\nexit 0\n'),
             'b': stub_half(t, 'zzrd-also', '#!/bin/sh\nexit 0\n')},
         argv=['{a}', '{b}'],
         ok=V(exit=2, has=['listed nothing'])),

    case('smoke-warnings-kept-only-in-a-temp-dir', 'smoke-l1.sh', 'f40fad2',
         'the pass named the modes that warned and not what they warned',
         # NO CASE: the reader warns only over a real -L1 process, and this
         # suite's stand-ins answer --list and run no benchmark, so nothing
         # a fixture can build reaches the branch. Verified by hand instead,
         # 2026-09-04, on a fabricated LOGDIR: three .err files for one leg
         # print three distinct warnings once each, and another leg's line
         # does not appear. The sweep's own half was verified on a real
         # sweep the same day.
         argv=None, ok=None, no_audit='too-dangerous-to-run'),

    # ---- the review of 2026-09-04 ----------------------------------------
    # Fifteen findings over the shell and Python here, by a reviewer reading
    # the files whole; a case for each program that can be driven, and a
    # record alone for the four that cannot: a judge, two docstrings and a
    # probe.
    case('gate-refuses-an-arm-its-list-lacks', 'run-gate.sh', '5ef414d',
         'SEL named two arms the prune had parked, and the count that would'
         ' say so was checked per process, after its forty minutes',
         # `build` and `mut-odo` went to `Only` in 41d3bad and the gate's
         # selection kept naming them, so every process would have come
         # back two arms short of EXPECT and the gate failed after its
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


    case('evening-reads-the-pair-and-not-each-half-against-itself',
         'run-evening.sh', None,
         'CONTROL: the gate emits the two cross-half passes AND each half'
         ' over its own two legs',
         # BORN 2026-09-19. The palindrome gives four processes and the
         # driver read two PAIRS of them, which answers whether the passes
         # agree and not what a disagreement IS. Run 36's `list` parted 1.60
         # points across the passes and the gate was sound: the control
         # half's own `a` over its `b` read 1.0128 where the basis's read
         # 1.0004, and those two account for 1.28 of the 1.60. That session
         # ran them by hand, inside the one window where nothing else may
         # run. They are the same two commands the driver already makes,
         # against different JSONs, so the window pays nothing extra.
         shadow=dict(extra=lambda: evening_fixture('zzel', md5=False)),
         env={'MAXBUSY': '100', 'FAKE_SATURATE': '1',
              'ONLY': main_shapes()[0]},
         argv=['zzel'],
         probe=lambda subs: open(os.path.join(subs['at'],
                                              'zzel-evening-out.txt')).read(),
         # FOUR readings, not two headings: the heading survives a
         # dropped reading, so the count is what the assertion is on.
         ok=V(has=['##### gate reading, -a pair then -b pair',
                   '##### each half against ITSELF, -a over -b',
                   'per arm, over'])),


    case('status-counts-the-slots-a-note-still-owes', 'run-status.sh', None,
         'CONTROL: a note carrying <yours> reads NOT DONE at 2c, naming'
         ' both slot shapes and ignoring the comment lines',
         # Step 2c, added 2026-09-07 with `preflight.sh --fill-in`. Every
         # other step here judges an artifact; the fill-in block is the one
         # product of the pre-run half no artifact records, so a row left
         # unwritten was invisible until somebody re-read the note.
         #
         # THREE THINGS AT ONCE, because each was wrong at some point in
         # the hour it was written. A `[PAIR'S]` slot sits at column 0 and
         # a fill-in row is indented, and a lister for the indented shape
         # alone named a subset of what the count counted. And `--draft`'s
         # own header explains the marker and so contains it twice, and a
         # session makes its note by redirecting that header, so a count
         # that read comment lines reported owed slots on a finished note.
         shadow=dict(extra=[('run97-pair.txt', NOTE_STUB
                             + '\n# a header explaining <yours>\n'
                               '\nWHAT THIS PAIR MEASURES [PAIR\'S]: <yours>'
                               '\n\nVerified when built, YYYY-MM-DD:\n'
                               '  repetition       <yours>\n')]),
         argv=['run97'],
         ok=V(exit=1,
              has=['2 slot(s) still <yours>',
                   'WHAT THIS PAIR MEASURES', 'repetition'])),

    case('status-clears-2c-when-the-slots-are-written', 'run-status.sh', None,
         'CONTROL: the same note with the slots written reads done at 2c,'
         ' the comment line notwithstanding',
         # The other direction, and the one that says the NOT DONE above
         # was the slots and not the stub: a note whose only remaining
         # `<yours>` is inside a comment is a note that owes nothing.
         shadow=dict(extra=[('run97-pair.txt', NOTE_STUB
                             + '\n# a header explaining <yours>\n'
                               '\nWHAT THIS PAIR MEASURES [PAIR\'S]: the'
                               ' compiler.\n\nVerified when built,'
                               ' 2026-09-07:\n  repetition       not owed\n')]),
         argv=['run97'],
         ok=V(has=['no <yours> slot left'],
              hasnt=['slot(s) still <yours>'])),

    case('status-counts-the-short-named-twins', 'run-status.sh', '18021d0',
         'step 0 missed the twins of Runs 23 to 25, which their own'
         ' scripts name `probe-g3-<half>-r<N>`',
         # The three twin scripts before Run 27 build `probe-g3-<half>-r23`
         # and the glob read `-run23` alone, so those three finished runs
         # read step 0 NOT DONE for ever -- run23 being the run this
         # script's own non-vacuity note says reads all done.
         shadow=dict(extra=[('probe-g3-a-r97', '#!/bin/sh\n'),
                            ('probe-g3-b-r97', '#!/bin/sh\n')]),
         argv=['run97'],
         ok=V(has=['2 -g3 twin(s) here']),
         bug=V(hasnt=['2 -g3 twin(s) here'])),

    # ---- view-floor.py, the per-view floor -----------------------------
    case('view-floor-skips-the-legs-that-are-not-classes', 'view-floor.py',
         '18021d0',
         'the skip of the main set, the alone legs and the gate processes'
         ' skipped nothing, each read as a class with no A/A group',
         # `if cls in (...): pass` skipped nothing, and tested the class
         # where the alone and gate legs carry their marker in the half's
         # place, so every such leg of a finished run raised the exit to 2
         # with a `carries no A/A group` line apiece -- 92 on Run 32.
         plant=lambda t: {'dir': floor_legs(t)},
         argv=['zzvf', '-d', '{dir}'],
         ok=V(exit=0, hasnt=['carries no A/A group']),
         bug=V(exit=2, has=['carries no A/A group'])),

    # ---- the review of 2026-09-18: records whose fix has no case ------
    # The probes carry none by policy (checks.py); preflight.sh's and
    # read-all.sh's proofs are that day's two mutants in mutants.py, the
    # fixtures a case would want being unbuildable here; the rest are this
    # suite's own instruments, which no case runs. Each says what was
    # watched.
    case('attr-reader-binds-lib-stage1-to-the-leaf', 'probe-attr-read.py',
         '18021d0',
         'lib-stage1 was anchored inside the add-in-leaf function, where'
         ' its samples land in fillStage2',
         # Main.hs dispatches lib-stage1 to fbLibStage1, a dispatcher that
         # hands fillStage2 a view whose innermost run is strided and
         # nothing else; the reader's table said
         # fbMutOdoVecdimsAddInLeafU2, so every lib-stage1 span sat in
         # the wrong body and the reader refused on the overlap, on every
         # sample of Run 32. Each arm now names the function its samples
         # land in, and the Main.hs the twin was built from is an
         # argument, the histogram's line numbers being that build's.
         argv=None, ok=None),

    case('attr-reader-reads-the-working-tree-in-silence',
         'probe-attr-read.py', '7b80fa9',
         "a histogram read against a Main.hs that was not its twin's"
         ' bucketed the harness as elsewhere and said nothing',
         # The build now rides in the histogram's header, off the pair
         # note through the twin's name, and the harness bucket is the
         # check: the control every arm passes through, empty for an arm
         # only when the file is not the build's, refused at exit 2.
         # Watched 2026-09-18 on Run 32's histograms against a tree past
         # their twins, and on a header naming a later build.
         argv=None, ok=None),

    case('figures-drops-a-refused-gate-row', 'preflight.sh', '18021d0',
         '--figures dropped the gate row at a PASS when run-gate.sh --show'
         ' refused before printing',
         # Mutant `--figures drops a refused gate row instead of leaving
         # it unchecked`; watched in a shadow with a note and no binaries.
         argv=None, ok=None),

    case('attr-probe-divides-by-a-zero-count', 'probe-attr.sh', '18021d0',
         'a perf count of 0 passed the digits guard and divided by zero,'
         ' which ends the probe at exit 1 with the arms after it unrun',
         argv=None, ok=None),

    case('readings-wait-took-the-pred-file-at-any-rc', 'defects.py', '18021d0',
         "the readings-wait control's bare file name let rc=2 and a"
         ' traceback through',
         # The hasnt list refuses `rc=2 main-a1g-pred.txt` and `!! crashed`
         # now, both as post-run-readings.sh prints them.
         argv=None, ok=None),

    case('reroll-sweep-ends-on-a-dead-leg', 'probe-flip-reroll.sh', '18021d0',
         'under set -e a dead leg ended the sweep before its exit line,'
         ' and its half-written JSON read as a finished leg next time',
         # criterion opens --json before its first bench. The leg is set
         # aside as `*.failed.json`, the sweep goes on and exits 1; the
         # alone leg of probe-flip-counters.sh had the same shape beside a
         # perf leg that carried `|| true`, and is set aside the same way.
         # Watched on stub halves, one exiting 137 mid-write.
         argv=None, ok=None),

    case('reroll-reader-averages-a-nan-floor', 'probe-flip-reroll-read.py',
         '18021d0',
         'a leg with no A/A floor put a nan into statistics.median, which'
         ' hands back whichever value sorts to the middle',
         # Under a nan median every `>` is False and every arm reads
         # fixed; under a finite wrong one the verdict is wrong and says
         # nothing. The floorless leg is named and left out, at rc 1, and
         # a JSON the reader cannot parse is named rather than a
         # traceback. Watched on synthesized legs.
         argv=None, ok=None),

    case('read-all-drops-a-refused-compare-from-the-range',
         'read-all.sh', '18021d0',
         "a population whose --compare refused left the delta bullet's"
         ' range with no mark on it',
         # Mutant `a refused --compare drops its population from the delta
         # range in silence`; watched in a shadow of Run 35 with both rev
         # JSONs cut off mid-file.
         argv=None, ok=None),

    case('checks-pyflakes-guard-accepts-what-the-step-does-not-run',
         'checks.py', '18021d0',
         'the guard passed on a pyflakes script while the lint ran the'
         ' module, so a box with the script alone failed on a traceback',
         argv=None, ok=None),

    case('property-judges-read-only-greps-status', 'mutants.py', '18021d0',
         "the two per-shape property judges' status was grep's alone, the"
         " reader's exit lost in the pipe",
         argv=None, ok=None),

    case('busy-compare-fails-behind-a-bash-error', 'probe-cache-run.sh',
         '18021d0',
         'an empty machine-busy.sh reading refused behind `integer'
         ' expression expected` and a message naming an empty percentage',
         # probe-order-reversal.sh and probe-within-evening.sh carried the
         # same line and take the same form: an unreadable reading refuses
         # by name, and awk compares the percentage.
         argv=None, ok=None),

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

    case('status-reads-a-complained-evening-as-complete', 'run-status.sh',
         'f241d66',
         'an evening file ending EVENING COMPLETE WITH N COMPLAINT(S) read'
         ' as NOT DONE, the check matching the clean form alone',
         # Run 39, 2026-09-23, the same line post-run-readings.sh missed.
         shadow=dict(extra=[('run96-evening.txt',
                             '=== 2026-09-04T00:00:00+02:00 EVENING COMPLETE'
                             ' WITH 1 COMPLAINT(S) OVER BOTH CALLS -- read'
                             ' each\n')]),
         argv=['run96'],
         ok=V(has=['run96-evening.txt ends COMPLETE']),
         bug=V(has=["run96-evening.txt's last line"])),

    # THE DRIVER'S TWO CLOSING LINES AS IT WRITES THEM, one case each: the
    # fixtures above spell `major run complete` bare, which run-major.sh
    # never writes, so a reader keyed on either literal form would pass
    # them and fail a real run -- the shape of the complained-evening
    # defect, whose form nothing held a reader to (2026-09-23).
    case('status-reads-major-run-complete-as-written', 'run-status.sh', None,
         'CONTROL: run-major.sh\'s clean closing line, verbatim, reads done',
         shadow=dict(extra=[('run95-wallclock.log',
                             '=== 2026-09-04T00:00:00+02:00 major run complete;'
                             ' every process ran the count asked of it\n')]),
         argv=['run95'],
         ok=V(has=['run95-wallclock.log says complete, no complaint'])),

    case('status-reads-a-complained-major-run-as-written', 'run-status.sh',
         None,
         'CONTROL: run-major.sh\'s complained closing line, verbatim, with'
         ' the stamped complaint above it, reads NOT DONE naming the count',
         shadow=dict(extra=[('run94-wallclock.log',
                             '=== 2026-09-04T00:00:00+02:00   !! run94-a1g-main:'
                             ' expected 5 benches, got 4 -- the selection is'
                             ' not what was asked for\n'
                             '=== 2026-09-04T01:00:00+02:00 major run complete,'
                             ' with 1 complaint(s) above -- read them before'
                             ' any figure\n')]),
         argv=['run94'],
         ok=V(has=["with 1 '!!' line(s)"])),

    case('lint-refuses-a-mutant-judge-naming-a-parked-arm', 'read-run.py',
         None,
         'CONTROL: a mutant whose judge names an arm the roster no longer'
         ' times fails --lint, naming the mutant and the arm',
         # The rate column's judge paired the shipped leaf with the -u1
         # leaf, which c870e1e parked; on Run 39's files it read red
         # unmutated and the mutant counted as not applied, found only by
         # a check-all over the write-up (2026-09-23).
         shadow=dict(mutate=[('mutants.py',
                              "A = [\\'mut-odo-vecdims-add-in-leaf-u2\\',"
                              " \\'mut-odo-vecdims\\']",
                              "A = [\\'mut-odo-vecdims-add-in-leaf-u2\\',"
                              " \\'mut-odo-vecdims-add-in-leaf-u1\\']")]),
         argv=['--lint'],
         ok=V(exit=1, has=['mutant judge', 'mut-odo-vecdims-add-in-leaf-u1'])),

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
         bug=V(exit=0, has=['sweep clean'], hasnt=['did NOT refuse']),
         no_audit='other:pre-fix-script-invokes-a-retired-mode'),

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

    case('carry-over-is-silent-on-a-registration-with-no-item',
         'read-run.py', '3a9ba3f',
         '--carry-over exited 1 saying nothing where the registration'
         ' carried no numbered item yet',
         # The window is every registration between the commit that
         # declares the pair and the preparation that predicts, which is
         # where a preparation actually runs the mode. `if not items:
         # return 1` printed nothing, and 1 is this tree's code for
         # findings, so an empty selection read as a finding with no line
         # to read. Met in use on 2026-09-19, at Run 37's preparation,
         # which had to open the source to find out why.
         plant=lambda t: {
             'readme': readme_with_a_registration(t, no_items=True)},
         argv=['run99', '--carry-over', '--readme', '{readme}'],
         ok=V(exit=2, has=['carries no numbered item',
                           'empty selection']),
         bug=V(exit=1, hasnt=['numbered item'])),

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

    case('properties-limit-counts-a-class-run-it-opened', 'properties.py',
         '18021d0',
         'CORPUS_LIMIT bounded the main tables the round-trip read back,'
         ' opening every run on disk, a class run uncounted',
         # The break sat after the population filter, so a class run was
         # opened and passed over uncounted and every run on disk was
         # loaded whatever the limit -- the shape the record above holds
         # one loop in, in the loop beside it.
         plant=corpus_with_a_class_run,
         env={'CORPUS': '{corpus}', 'CORPUS_LIMIT': '2'},
         argv=[],
         ok=V(has=['over 1 population(s) on disk'],
              hasnt=['over 2 population(s) on disk']),
         bug=V(has=['over 2 population(s) on disk'])),

    case('properties-help-before-the-corpus', 'properties.py', '18021d0',
         '--help exited 2 from a tree with no runs/run<N>.md, the newest'
         ' run doc being resolved at import before main() saw the flag',
         # A second exit-2 route the docstring did not name, and it hid
         # the help text exactly where a reader wants it.
         shadow=dict(extra=[('runs', '')]),
         argv=['--help'],
         ok=V(exit=0, has=['properties.py'], hasnt=['BLOCKED']),
         bug=V(exit=2, has=['BLOCKED'])),

    case('properties-refuse-a-limit-that-is-not-a-count', 'properties.py',
         '4ea1464',
         'CORPUS_LIMIT was parsed at import, so a value that is not a count'
         ' was a traceback and a negative one an empty sweep blamed on the'
         ' corpus',
         # The source lint's one standing question (`env-parse-at-import`),
         # answered: the value is read under main() and refused, at exit 2
         # naming the variable, where it is not a whole number.
         plant=corpus_of_one,
         env={'CORPUS': '{corpus}', 'CORPUS_LIMIT': 'x'},
         argv=[],
         ok=V(exit=2, has=['CORPUS_LIMIT'], hasnt=['Traceback']),
         bug=V(exit=1, has=['Traceback'])),

    case('properties-refuse-a-negative-limit', 'properties.py', '4ea1464',
         'a negative CORPUS_LIMIT swept nothing and said the corpus was empty',
         plant=corpus_of_one,
         env={'CORPUS': '{corpus}', 'CORPUS_LIMIT': '-1'},
         argv=[],
         ok=V(exit=2, has=['CORPUS_LIMIT'], hasnt=['empty corpus']),
         bug=V(exit=1, has=['empty corpus'], hasnt=['CORPUS_LIMIT'])),

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

    # Three records without a case: two docstrings and a probe.
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

    case('note-paths-read-a-name-that-merely-contains-the-run', 'preflight.sh',
         None,
         "10c took the tail of `smoke-l1-run28-bcast.json` for a path of its"
         ' own and reported it gone',
         # NO CASE, for the reason checks.py's UNCOVERED gives preflight,
         # and the same reason as the record below. Its own harvest regex
         # had a right boundary and a class boundary from two earlier
         # findings and none on the LEFT, so any name CONTAINING the run's
         # own left its tail behind. Written into a note by the roster
         # pass's own artifacts, which is when it fires -- the file was
         # present and the step FAILed. The bug direction was WATCHED, on
         # Run 28's live note, and the fix was shown to keep biting: a
         # planted `run28-nosuchthing.json` still FAILs naming that path
         # and no other, the note restored from a copy taken first.
         argv=None, ok=None, no_audit='too-dangerous-to-run'),

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

    case('fill-in-keys-the-previous-build-on-this-run-s-tag', 'preflight.sh',
         '907c218',
         'a renamed basis tag lost both of the fill-in block\'s cross-run'
         ' reads',
         # NO CASE, and NOT for the reason the two records above give.
         # checks.py's UNCOVERED entry says outright that *a case would run
         # them twice* covers preflight's STEPS and not its REPORTERS, and
         # --fill-in is a reporter: what stands behind it is the control in
         # preflight.sh's header, every derived row read against the same
         # figure taken independently by hand, and that control is re-taken
         # there for this defect. A case would want a second run's binaries
         # and note planted beside this one's, which every preparation has
         # for free and no fixture here has yet. The previous build of this recipe
         # was `run$PN-$BASIS` with THIS run's tag in it, which holds only
         # while the tag does. Run 29 renamed the basis `g912` -> `spec`,
         # the recipe unchanged, and both reads went dark at once: the
         # --delta one reported `run28-spec` -- a name Run 28 never wrote --
         # as not here, and the roster-delta one printed NOTHING, against
         # the comment beside PB promising a named absence. Both matter on
         # exactly the run that renames: the fills delta is the pinning
         # claim's only reading and a rebuild retires it.
         # The bug direction was WATCHED on the live run
         # (log-preflight-r29.txt of 2026-09-11, the `not available` line
         # and no `main set:` line at all), and the fix was proved by
         # running its own derivation beside the old one: PB empty before,
         # `run28-g912` after, and the two reads then printing what the
         # preparation had taken by hand at steps 2 and 6c, figure for
         # figure. The fallback asks the PREVIOUS run's note for its basis,
         # through pair-halves.sh, which is where every other script reads a
         # half's name -- with BASIS and OTHER unset for the call, that
         # script refusing an environment that disagrees with the note it is
         # handed, and this pass carrying this run's names.
         argv=None, ok=None),

    case('fill-in-compilers-row-reads-ghc-internal', 'preflight.sh',
         'a063b2d',
         'the compilers row derived a string both HEADs here carry alike',
         # `ghc-internal-10.100.0` is in the binaries of both HEADs this
         # series has built, 20260803 and 20260918, so the row could not
         # tell the compiler Run 35 used from Run 39's,
         # and every note from Run 36 on wrote the `ghc-10.1.YYYYMMDD`
         # string by hand over it, --figures checking the useless one. NO
         # CASE: --fill-in is a reporter and wants a second run's binaries
         # planted. WATCHED
         # 2026-09-23 on Run 39's halves: the old pattern printed
         # ghc-internal-10.100.0 for both, the new one ghc-10.1.20260918
         # for both, and `--figures run39` passed on the new one against
         # the note's hand-written row.
         argv=None, ok=None),

    case('fill-in-fills-row-drops-offsets-moved', 'preflight.sh', 'a063b2d',
         "the fills row printed 2d's displacements and not what moved",
         # The filter over `--delta` kept the lines of a group that kept
         # its offsets and dropped `offsets MOVED: [...] -> [...]`, the
         # line of one that did not -- which is the reading 2d exists for.
         # Run 39's derived block printed six displacements under no
         # statement of the move, and the preparation pasted the line in by
         # hand. NO CASE, as above. WATCHED 2026-09-23 on run38-gheadnospec
         # against run39-gheadnospec: the old filter passed 6 lines, the
         # new one 7, the seventh being `offsets MOVED: [18, 15, 0, 0, 9,
         # 2] -> [0, 0, 0, 0, 0, 0]`.
         argv=None, ok=None),

    case('step-8d-replays-the-whole-corpus', 'preflight.sh', '7fc3dc6',
         'the changed-since-the-last-run step replayed every case there is',
         # NO CASE, for the reason checks.py's UNCOVERED gives preflight's
         # STEPS: a case would run this suite twice, and this step IS the
         # suite. The bug direction was watched in this session's own logs.
         # THE BASELINE IS THE INTERESTING PART and the place a rewrite
         # would go wrong: `--changed` defaults to HEAD, which selects only
         # uncommitted edits, and the obvious commit -- the NEWEST touching
         # runs/run<PN>.md -- is whatever session last amended that file,
         # which on this very run was the preparation itself, hours old.
         # Either would have passed vacuously. The FIRST commit touching it
         # is the run file being born at post-run step 5, which is the last
         # run finishing and is immune to later amendment.
         argv=None, ok=None),

    case('step-9-asserts-specconstr-of-every-basis', 'preflight.sh',
         'c916885',
         'the regime step FAILed a basis built exactly as its recipe asks',
         # NO CASE, for the reason the first two preflight records above
         # give and checks.py's UNCOVERED repeats: step 9 is a STEP, so a
         # case would run this suite twice. The bug direction was WATCHED,
         # on the live run.
         # The step read ONE of the two regimes its own comment names.
         # README gives both -- baseOffsetsScan against baseOffsetsMut equal
         # to three figures under SpecConstr and ten times apart at plain
         # -O1 -- and the code asserted the first, which was every basis
         # from Run 8 to Run 29 and is not Run 30's: the request of
         # 2026-09-12 made both halves plain -O1, so the step FAILed the
         # pair it was given for being the pair it was given. WHICH REGIME
         # TO EXPECT IS NOT THIS SCRIPT'S TO KNOW, so it now reads the flag
         # off the BASIS half's recipe block in the note -- the same file
         # 10d already holds to the HALVES line -- and holds the binary to
         # that, naming the disagreement in either direction.
         # Proved non-vacuous by hand over all three branches, the copy
         # having no binary to run `diag` on: run30-pair.txt derives o1,
         # run29-pair.txt derives spec, and a note carrying no such block
         # derives unknown, which FAILs saying the regime is UNCONFIRMED
         # rather than passing on a guess.
         argv=None, ok=None),

    case('checklist-prints-no-execution-order', 'read-run.py',
         'e4894dc',
         'the post list printed its steps in numeric order and nothing'
         ' said which of them run out of that order, so a session'
         ' executing it in the order given took 9 and 10 after 6d',
         # The numbers are stable because pointers resolve to them, so
         # the fix is a second, derived statement of the order rather
         # than a renumbering. Read off the live README: the constant
         # is checked against the list's own numbers, so this case also
         # fails if a step is added without POST_EXEC.
         argv=['--checklist', 'post', '--imperative'],
         ok=V(exit=0, has=['EXECUTION ORDER',
                           'run out of printed turn']),
         bug=V(exit=0, hasnt=['EXECUTION ORDER'])),

    case('brief-update-reopens-filled-slots', 'read-run.py', 'e4894dc',
         'a second paste brought the facts file\'s empty `<yours>` back'
         ' over prose a session had written, and said nothing',
         # TIER 1 ONLY. The fixture is a brief and a facts file whose
         # shapes this runner would have to be told; written from the
         # live loss rather than guessed at, and the mutant `the brief
         # re-opens filled slots without saying so` carries the
         # non-vacuity in mutants.py.
         None, None),

    case('class-block-second-slot-unnamed', 'read-run.py', 'e4894dc',
         'a class block carried two `___` and only the first said what'
         ' it wanted, so the second read as already done',
         # TIER 1 ONLY: the invocation wants a class JSON and its twin,
         # which post-run 11 offers for deletion, so a case built on one
         # goes LOST with the run rather than proving anything later.
         None, None),

    case('step-9-derives-the-regime-from-a-flag-name-in-prose',
         'preflight.sh', 'dace8e7',
         'the regime step read a flag NAME anywhere in the recipe block',
         # NO CASE, for the reason the three preflight records above give
         # and checks.py's UNCOVERED repeats: step 9 is a STEP, so a case
         # would run this suite twice.
         # Two faults, one fix. The step's own comment names a PASS --
         # SpecConstr -- and the code keyed on ONE flag that turns it on,
         # so a half built at -O2, which turns it on too, classed as plain
         # -O1 and would have FAILed for reading as SpecConstr. That is the
         # record above one level up, the flag name standing in for the
         # pass. And the search ran over the WHOLE block, prose included,
         # which the first fix walked into: run30-pair.txt's control block
         # says `GHC enabling that pass at -O2 and not at -O1` of a half
         # built at plain -O1, so matching `-O2` there derived spec for a
         # binary that has none. The fix reads the `--ghc-options` lines
         # alone -- what cabal is handed -- and treats a block naming none
         # of them as UNCONFIRMED rather than as plain -O1 by default.
         # Proved non-vacuous by hand over five inputs, the two notes on
         # disk being the controls: run31-pair.txt derives o1 for nospec
         # and spec for o2, run30-pair.txt derives o1 for BOTH of its
         # halves, and a name with no block derives unknown.
         argv=None, ok=None),
    # ---- --draft's fill-in skeleton, and the column it writes a row at --
    # A ROW WHOSE LABEL IS SIXTEEN CHARACTERS WIDE WENT OUT WITH ONE SPACE
    # AFTER IT, where `FILL_LABEL` wants two -- so the row `--draft` wrote
    # could be read back by nothing: not by the next `--draft`, not by
    # `_fill_trimmed`, not by preflight's `--figures`. `md5 gheadtwopass`
    # is sixteen. Run 38's preparation was handed a draft carrying no such
    # row and `--figures` answered `md5 gheadtwopass NO SUCH ROW in the
    # note` against a note that carried it plainly at its own column;
    # Run 37's note has the same unreadable row, so it had bitten twice
    # and a hand had supplied the row both times.
    # THE COLUMN IS NOW 20, written as a 16-wide field and TWO literal
    # spaces rather than as a wider field: a half tag long enough to push
    # a label past sixteen still gets its two spaces, where `%-18s` would
    # only have moved the failure to eighteen.
    # WHAT THE `has` BELOW STANDS FOR is the round trip -- a draft's own
    # block read back as the next note's -- which one invocation cannot
    # run. Taken by hand on 2026-09-21 before this case was written: fed a
    # note at column 20, `--draft` wrote `md5 gheadtwopass` back at 19,
    # and feeding THAT draft in again produced a block holding `Main.hs
    # at` and `md5 gheadnospec` and no md5 of the other half at all.
    case('draft-writes-a-fill-row-no-reader-can-read',
         'read-run.py', '5d645f1',
         'a provenance row vanished from the draft a preparation was handed',
         plant=lambda t: {
             'a': write(os.path.join(t, 'zz-pair.txt'),
                        'The pair zz-gheadnospec and zz-gheadtwopass,'
                        ' written by hand 2026-01-01.\n'
                        '\n'
                        'Half names [SAME]: gheadnospec is the basis,'
                        ' gheadtwopass the other.\n'
                        'HALVES: basis=gheadnospec other=gheadtwopass\n'
                        'COMPARE: run98\n'
                        '\n'
                        'Verified when built, 2026-01-01:\n'
                        '  Main.hs at        abc1234, tree clean\n'
                        '  md5 gheadnospec   0123456789abcdef'
                        '0123456789abcdef\n'
                        '  md5 gheadtwopass  fedcba9876543210'
                        'fedcba9876543210\n')},
         argv=['--note', '{tmp}/zz-pair.txt', '--draft', 'run99',
               '--halves', 'gheadnospec,gheadtwopass'],
         ok=V(exit=0,
              has=['  md5 gheadtwopass  <yours>',
                   '  md5 gheadnospec   <yours>',
                   '  Main.hs at        <yours>']),
         bug=V(exit=0,
               has=['  md5 gheadtwopass <yours>'],
               hasnt=['  md5 gheadtwopass  <yours>'])),

    # ---- --draft, and a header line wrapped between hand and date ------
    # The draft puts the template's `Run NN's, written by hand YYYY-MM-DD`
    # back over the previous note's header, so the run number and the
    # build date read as slots. The pattern wanted single spaces, and Run
    # 39's note breaks that line after `hand`, so Run 40's draft opened
    # with `Run 39's, written by hand` and `2026-09-23` -- the one place a
    # draft states something false about the pair it drafts. Fixed by hand
    # in that note, 2026-09-24.
    case('draft-keeps-a-wrapped-header-date', 'read-run.py', 'fdc3a18',
         'a header line broken before its date carried the previous run'
         ' and its build date into the draft',
         plant=lambda t: {'note': write(
             os.path.join(t, 'run97-pair.txt'),
             'The pair run97-a and run97-b, Run 97\'s, written by hand\n'
             '2026-01-01 BEFORE either binary exists.\n\n'
             'HALVES: basis=a other=b\n')},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'a,b'],
         ok=V(exit=0, has=["Run NN's, written by hand YYYY-MM-DD"],
              hasnt=['2026-01-01']),
         bug=V(exit=0, has=['2026-01-01'])),

    # ---- --draft, and what it dropped or never offered --------------------
    # A `[SAME, ...]` block is one a note rewrote for its own pair, and the
    # template's block of that title replaced it; written as ONE paragraph
    # it went with nothing in the DROPPED list, which is how Run 39's
    # machine block -- the fingerprint read against, the terms the check
    # carried -- never reached Run 40's draft. And a [PAIR'S] block the
    # template gained after the previous note was written reached no draft
    # at all, the draft carrying that kind only from the note: Run 40's
    # note went without the RERUN line. Both found 2026-09-24 by Run 40's
    # preparation.
    case('draft-drops-a-rewritten-same-block', 'read-run.py', 'fdc3a18',
         "a note's rewrite of a [SAME] block left the draft unseen",
         plant=lambda t: {'note': a_previous_note(t)},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'a,b'],
         ok=V(exit=0, has=["THE MACHINE [PAIR'S]: <yours> -- what"
                           ' run97-pair.txt added',
                           'the fingerprint read against is']),
         bug=V(exit=0, hasnt=['the fingerprint read against is'])),

    case('draft-never-offers-a-template-block', 'read-run.py', 'fdc3a18',
         'a [PAIR\'S] block the template gained reached no draft',
         plant=lambda t: {'note': a_previous_note(t)},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'a,b'],
         ok=V(exit=0, has=["A RERUN, SAID BEFORE THE HOURS [PAIR'S]:"
                           " <yours> -- the template's block, which"
                           ' run97-pair.txt does not carry',
                           'RERUN: ask']),
         bug=V(exit=0, hasnt=['RERUN: ask'])),

    case('draft-drops-the-quiet-after-block', 'read-run.py', '0a573c4',
         "the template's QUIET-AFTER block, added 2026-09-25, reached no"
         ' draft, its key missing from MACHINE_KEYS',
         # Found by the transcript pass over the change that added it: the
         # commit said a template block with a new machine line is carried
         # into the next draft, and a draft of Run 41 showed it was not.
         plant=lambda t: {'note': a_previous_note(t)},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'a,b'],
         ok=V(exit=0, has=['QUIET-AFTER: ask']),
         bug=V(exit=0, hasnt=['QUIET-AFTER: ask'])),

    case('draft-repeat-carries-the-pairs-blocks-whole', 'read-run.py', None,
         'CONTROL: --repeat carries a [PAIR\'S] block with no <yours> line'
         ' and makes an input it cannot read a NOT READ slot at the head,'
         ' never a MOVED one',
         plant=lambda t: {'note': a_previous_note(t)},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'a,b',
               '--repeat'],
         ok=V(exit=0, has=["WHAT THIS PAIR MEASURES [PAIR'S]: the regime",
                           "NOT READ SINCE run97's BUILD, THE SOURCE"
                           " [PAIR'S]: <yours>"],
              hasnt=["WHAT THIS PAIR MEASURES [PAIR'S]: <yours>",
                     "MOVED SINCE run97's BUILD, THE SOURCE"])),

    case('draft-repeat-refuses-other-halves', 'read-run.py', None,
         'CONTROL: --repeat refuses halves that are not the previous'
         ' note\'s, carrying its blocks whole being right only for them',
         plant=lambda t: {'note': a_previous_note(t)},
         argv=['--note', '{note}', '--draft', 'run98', '--halves', 'c,d',
               '--repeat'],
         ok=V(exit=1, has=['--repeat carries run97\'s'])),

    case('preflight-9b-echoed-a-prose-fragment', 'preflight.sh', 'fdc3a18',
         "step 9b printed a sentence of the note's prose as the reading",
         # 9b was the note's to name in prose, and the step found it by
         # grepping `step 9b` and echoed the next lines: on Run 40's note
         # that was WHAT THIS PAIR MEASURES saying the two steps were one
         # reading, printed under `9b yours` as though it were one. NO
         # CASE, for the reason the preflight records above give: 9b is a
         # STEP. WATCHED 2026-09-24 both ways: before, `9b yours step 9b
         # are ONE reading on this pair, as on Runs 36's to 39's...`
         # (Run 40's first preflight); after, on the real binaries, `9b
         # PASS run40-gheadtwopass is SpecConstr, which its recipe asks
         # for: scan/mut 1.000`, and every other branch by the block run
         # out of the file in a scratch directory: `regime basis` PASS at
         # 9.992, a recipe disagreeing with its binary FAIL naming both,
         # `run` matching and not, `none` echoed, a malformed line and a
         # missing one each FAIL.
         argv=None, ok=None),

    # ---- --lint, and a prior with nothing beside it that derives it ----
    # THE ERROR NO PASS HERE COULD SEE was a figure quoted against the
    # wrong mode IN AN ITEM'S PROSE. `--carried` derives what a `pair`
    # span quotes and names an item matching nothing, so a span's own
    # figures are read; the sentence beside a span is read by nothing,
    # and that is where this one sat. Run 38's registration called 0.51 an A/A floor where
    # `--aa` gives 0.59% for that and the 0.51 is `--compare`'s widest
    # arm-to-duplicate gap; both numbers are real, and only the pairing
    # was wrong, which every arms-and-scope check passes over. What let
    # it in is that the registration stated its provenance ONCE, at the
    # head, for every prior at once: a collective claim is checked
    # against no item.
    # A 1.0 SPAN IS EXEMPT BY DESIGN and item (2) below is the control for
    # it -- a null quotes no earlier figure, so it has no provenance to
    # name, and flagging the null families would have made this refuse
    # ten times over on a registration that was right.
    # THE FIXTURE IS SYNTHETIC and not the live registration: post-run
    # step 5 MOVES a registration out of README into the run's own file,
    # so a case keyed on the open list's current text goes LOST the day
    # the run ends.
    case('registration-prior-names-no-mode', 'read-run.py', '2bc393e',
         'a prior read off the wrong mode sat in prose no pass reads',
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(),
             '- `OPEN` **What Run 99 is built to answer, registered before'
             ' it runs.** (1) *A prior quoted with nothing beside it that'
             ' derives it.* `predict: cross list 1.2950 within 1% on main'
             ' basis`. A band drawn off the run before, and no mode named.'
             ' (2) *And a null, which quotes nothing and is exempt.*'
             ' `predict: cross bq-expand 1.0 within 3% on main basis`.'
             '\n\n' + a_registration_lead()))},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1,
              has=["Run 99's item (1) quotes a prior and names neither"
                   ' the mode nor the file that derives it'],
              hasnt=["Run 99's item (2) quotes a prior"]),
         bug=V(hasnt=['quotes a prior and names neither'])),

    # ---- --lint, and a prior whose mode is named with its arguments ----
    # THE CHECK ABOVE REFUSED A PRIOR THAT NAMED ITS MODE. Run 40's item
    # (2) said its prior came off "`--pair lib-stage2-lean-u1
    # lib-stage3-lean` on the two main JSONs", and the check wanted a bare
    # `` `--mode` `` or a file name, so a mode given with its arguments --
    # the more useful form, the one a reader can rerun -- read as no mode
    # at all. The session added file names to get past it. Found
    # 2026-09-24 by Run 40's preparation.
    case('registration-prior-mode-with-arguments-refused', 'read-run.py',
         '9f7b276',
         'a prior naming its mode with the arguments was read as naming none',
         plant=lambda t: {'readme': prior_with_mode_args(t)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(hasnt=['quotes a prior and names neither']),
         bug=V(has=["Run 99's item (1) quotes a prior and names neither"])),

    # ---- --lint, and a registration's script that `./` cannot run ------
    # Run 39's registration adjudicates its item (2) by `script:
    # probe-r39-rules.py`, "run as `./probe-r39-rules.py run39 run38`",
    # and the file was committed at mode 100644, as was probe-r38-sweep.py
    # beside it: the command the registration gives answered `Permission
    # denied`. --lint asked only that the script be COMMITTED. Found
    # 2026-09-23 by Run 39's 12b re-derivation, a carrier agent running
    # the stated command against Run 38. The fixture names defects.py,
    # a module committed at 100644 by design, so the case needs no file
    # of its own at the wrong mode.
    case('registration-script-not-executable', 'read-run.py', '56736bc',
         'a registration named a committed script its `./` could not run',
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(),
             '- `OPEN` **What Run 99 is built to answer, registered before'
             ' it runs.** (1) *A clause no span states.* `script:'
             ' defects.py`, run as `./defects.py run99 run98`.'
             '\n\n' + a_registration_lead()))},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=1,
              has=["Run 99's item (1) names script defects.py, which is"
                   ' committed without its executable bit']),
         bug=V(exit=0, hasnt=['executable bit'])),

    # ---- preflight.sh, 8d's baseline and 10f ---------------------------
    # NO CASE for either, for the reason the preflight records above give
    # and checks.py's UNCOVERED repeats: these are STEPS, so a case would
    # run this suite twice. Both directions were WATCHED, on the live run.
    case('8d-baseline-never-reached-the-tool', 'preflight.sh', '2bc393e',
         'the step dated from HEAD while saying it dated from the last run',
         # `defect-run.py --changed "$PREV_COMMIT" .` -- with a SPACE. The
         # flag is `--changed[=REV]`, so the hash went in as a second ROOT,
         # that root answered BLOCKED for holding no defects.py, and the
         # real root took the flag's default, which is HEAD. `tail -1`
         # then showed the HEAD line alone and the BLOCKED one never
         # reached the verdict. So the step selected what differs from
         # HEAD -- nothing, whenever the preparation itself had changed no
         # script -- and reported an empty selection as though that were a
         # reading of the tree. The pre-run list spelled the same flag the
         # same wrong way, at three sites.
         # WATCHED 2026-09-22 both ways on run38: before, `8d FAIL
         # defect-run: no program ... differs from HEAD ... an empty
         # selection`; after, `8d PASS every defect of what changed since
         # run37's file refused again`, which selects and replays.
         argv=None, ok=None),

    case('launch-path-reported-and-never-judged', 'preflight.sh', '2bc393e',
         'a mount raised between runs would have taken the placement term',
         # The fill-in block's `launch` row names the path and says
         # outright that it does not judge, and no other step of the
         # preparation judged it --
         # so `hugebin/` standing mounted puts a 2 MiB-frame placement
         # term, 15 percent on one arm of Run 33's basis, into every
         # cross-run absolute a run publishes, and the only sign is a row
         # a session reads as the expected `./`. It stood mounted, empty
         # and writable, when Run 38's preparation began on 2026-09-21,
         # and a hand caught it before either sweep ran.
         # KEYED ON THE PATH half-bin.sh RETURNS and not on `mountpoint`,
         # so what is judged is where a half will run from; PLACEMENT=1 is
         # the acknowledgement for a run whose question IS that term.
         # IT IS NOT IN THE `--note` PATH. That flag's own gloss promises
         # steps that run with no binary, and this one returns without a
         # verdict where the basis half is not there, so it would have been
         # a step that silently did not happen in the case the flag
         # advertises.
         # WATCHED 2026-09-22 over all five branches, half-bin.sh stubbed
         # and restored at an identical md5, by running the function's own
         # text out of the file: no path under hugebin/ PASSes; the mount
         # with PLACEMENT unset FAILs; with PLACEMENT=1 PASSes; with
         # PLACEMENT=0 FAILs, the flag being tested for its documented
         # value and not for emptiness; and a half-bin.sh that refuses
         # FAILs rather than reading as a half launching from disk.
         argv=None, ok=None),

    # ---- --check-doc's hand-wrap verdict, which named no line ----------
    # `wrapped by hand` is the usual cause and not the only one: a
    # paragraph is flagged when a line of it is in NEITHER fixed point,
    # and a LONG line can be in neither -- two literal spaces inside
    # backticks survive in the file and are collapsed by `--unwrap`, so
    # the line the file has is one no form produces. The verdict named
    # the paragraph's first line number and nothing else, which sent a
    # session hunting a hand-wrapped paragraph that did not exist.
    # THE FIRST DRAFT OF THE FIX NAMED THE WRONG LINE, caught by watching
    # it: `ok` is the comparison loop's and by the time the message is
    # built it holds the LAST block's, so the set was rebuilt for the
    # block being reported.
    case('hand-wrap-verdict-names-no-line', 'read-run.py', '2bc393e',
         'the verdict named a paragraph and not what was wrong with it',
         plant=lambda t: {'readme': edited_readme(t, (
             a_registration_lead(),
             '- `OPEN` **A planted line no fixed point produces.** It quotes'
             ' `a  b`, two literal spaces inside backticks, which --unwrap'
             ' collapses.\n' + a_registration_lead()))},
         argv=['--check-doc', '--quiet', '--readme', '{readme}'],
         ok=V(exit=1,
              has=['whose first line in neither form is',
                   'A planted line no fixed point produces']),
         bug=V(hasnt=['whose first line in neither form'])),

    # ---- the seams Run 40's write-up met, 2026-09-25 ----
    case('fill-in-straddle-row-reads-the-listed-word', 'preflight.sh',
         'c653c15',
         "--fill-in's straddle row printed `listed straddling` where the"
         ' count belongs, once more than ten loops straddle',
         # The survey prints `still straddling : 24, 10 longest listed`
         # past ten and `: 7` at or under, and the row took the line's
         # last field. NO CASE, for the reason the preflight records above
         # give: the fill-in is a STEP. WATCHED 2026-09-25 both ways on
         # Run 40's two binaries: before, `231 at offset 0, listed
         # straddling`; after, `24 straddling` on each half.
         argv=None, ok=None),

    case('brief-facts-text-row-runs-on-past-its-row', 'read-all.sh',
         'c653c15',
         "--brief-facts' .text row ran on through the note's next rows when"
         ' the row ended with no full stop',
         # It joined six lines and cut at the first `. `, so Run 40's
         # row, ending `the load address` bare, carried the md5, launch
         # and repetition rows into the brief's item 5. WATCHED 2026-09-25
         # both ways on run40-pair.txt, and the new join read identically
         # to the old on run39-pair.txt, whose row wraps across three
         # lines and ends in a full stop.
         argv=None, ok=None),

    # ---- the review of 2026-09-25, over the scripts whole ----
    case('settled-rounds-see-only-the-short-loops', 'align-as.py', '1a359bd',
         'a group whose outer or long heads landed off the plan read as on'
         ' it whenever its short loops cost what the plan bought',
         # The test added 1e-9 to every tier and compared the tuples, so an
         # equal tier 0 fell below its padded self and decided the whole
         # comparison: (0, 5, 3) against a plan of (0, 2, 1) was not more.
         # Asked of the function, the three answers being a group moved on
         # tier 1, one better on tier 0 and worse after it, and one within
         # the tolerance.
         argv=['--unit', '(costs_more((0, 5, 3), (0, 2, 1)),'
                         ' costs_more((0, 5, 3), (1, 0, 0)),'
                         ' costs_more((0, 2, 1 + 5e-10), (0, 2, 1)))'],
         ok=V(has=['(True, False, False)']),
         bug=V(has=['(False, False, False)'])),

    case('major-run-names-a-population-it-lacks', 'run-major.sh', '2054bef',
         'a mistyped population ran nothing and logged a complete run',
         # `wanted` matched the name against nothing, so the relaunch
         # guard, the main run and every class run were all skipped, and
         # the run logged `major run complete` at exit 0 -- post-run step
         # 3's rerun of `runs` asked for as `rnus` reading as done.
         shadow=dict(extra=lambda text: halves('zzpn-lookrts', 'zzpn-a1g',
                                               classes=classes_in(text))
                     + [('zzpn-pair.txt', NOTE_STUB)]),
         env={'OTHER': 'a1g', 'BASIS': 'lookrts'},
         argv=['zzpn', 'rnus'],
         ok=V(exit=2, has=["'rnus' is no population"],
              hasnt=['major run begins', 'major run complete']),
         bug=V(exit=0, has=['major run complete'],
               hasnt=['start zzpn-'])),

    case('stalls-reader-reads-past-a-nonlinear-mark', 'probe-stalls-read.py',
         '7a8e621',
         'a cell probe-stalls.sh marked no one process\'s joined the table'
         ' and the geomean',
         # The reader skipped every `#` line, the marks with the header's
         # comments, so the shape the mark named was read as measured.
         plant=lambda t: {'txt': write(os.path.join(t, 'probe-zz.txt'),
                                       STALLS_MARKED)},
         argv=['A', 'B', '{txt}'],
         ok=V(exit=1, has=['(geomean over 1,', 'no one process read: s1']),
         bug=V(exit=0, has=['(geomean over 2,'])),

    case('stalls-keeps-a-cell-whose-check-process-failed', 'probe-stalls.sh',
         '7a8e621',
         'a perf hiccup on the -n 3N process alone discarded a cell whose'
         ' two published processes counted',
         # The third process is a check on the figure and not part of it,
         # and it had joined the NaN test with the two that are.
         shadow=dict(extra=[('zzps2-fake', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_THIRD_REFUSED)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'BIN': './zzps2-fake',
              'OUT': 'probe-zzps2', 'ONLY': 'shape-a', 'ARMS': 'list',
              'N': '1', 'EVENTS': 'instructions:u,cycles:u'},
         argv=[],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'probe-zzps2.txt')).read(),
         ok=V(exit=0, has=['shape-a list 1 100000 200000',
                           '# UNCHECKED shape-a list'],
              hasnt=['perf could not count', 'NONLINEAR']),
         bug=V(exit=1, has=['!! shape-a list: perf could not count'],
               hasnt=['shape-a list 1 100000 200000'])),

    case('stalls-linearity-reads-the-untruncated-slopes', 'probe-stalls.sh',
         '7a8e621',
         'the linearity test compared slopes truncated to integers, so a'
         ' small cell tripped it on the truncation alone',
         # 4999 and 5000 cycles over N=100 truncate to 49 and 50, which
         # part by 2.04 percent against a LINEAR_TOL of 0.02.
         shadow=dict(extra=[('zzps3-fake', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_TRUNCATED)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'BIN': './zzps3-fake',
              'OUT': 'probe-zzps3', 'ONLY': 'shape-a', 'ARMS': 'list',
              'N': '100', 'EVENTS': 'instructions:u,cycles:u'},
         argv=[],
         probe=lambda subs: open(os.path.join(
             subs['at'], 'probe-zzps3.txt')).read(),
         ok=V(exit=0, has=['shape-a list 100 1000 49'],
              hasnt=['NONLINEAR']),
         bug=V(exit=0, has=['# NONLINEAR shape-a list: cycles:u 49 then'
                            ' 50'])),

    case('counts-all-retake-tallies-its-own-call', 'run-counts-all.sh',
         '7a5e3e9',
         'a re-take after a blocked perf could never close clean, the tally'
         ' counting the first attempt\'s complaints',
         # The header calls a re-take safe, and the tally read every
         # `-- COMPLAINT,` in the status file, the refused attempt's six
         # among them, so the clean re-take ended WITH 6 at exit 1.
         shadow=dict(extra=[('zzcf-lookrts', FAKE_HALF),
                            ('zzcf-a1g', FAKE_HALF),
                            ('zzcf-pair.txt', NOTE_STUB),
                            ('zzcf-evening.txt',
                             EVENING_DONE + counts_attempt('zzcf'))]),
         plant=lambda t: {'stub': stub_dir(t, PERF_ANSWERS)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzcf'],
         ok=V(exit=0, has=['counts lookrts other: done, rc=0',
                           'EVENING COMPLETE: every stage of both calls'],
              hasnt=['COMPLAINT(S)']),
         bug=V(exit=1, has=['counts lookrts other: done, rc=0',
                            'EVENING COMPLETE WITH 6 COMPLAINT(S)'])),

    case('counts-all-retake-keeps-what-an-earlier-call-wrote',
         'run-counts-all.sh', '7a5e3e9',
         'a re-take refused every population whose counts an earlier call'
         ' had written, each a new complaint',
         # run-counts.sh refuses over its own artifact, rightly, and the
         # re-take asked it anyway for the populations that had counted.
         shadow=dict(extra=[('zzcg-lookrts', FAKE_HALF),
                            ('zzcg-a1g', FAKE_HALF),
                            ('zzcg-pair.txt', NOTE_STUB),
                            ('zzcg-counts-a1g.txt', 'counted earlier\n'),
                            ('zzcg-evening.txt',
                             EVENING_DONE + counts_attempt(
                                 'zzcg', clean=('counts a1g main',)))]),
         plant=lambda t: {'stub': stub_dir(t, PERF_ANSWERS)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzcg'],
         ok=V(exit=0, has=['counts a1g main: zzcg-counts-a1g.txt kept from'
                           ' an earlier call',
                           'EVENING COMPLETE: every stage of both calls'],
              hasnt=['COMPLAINT(S)']),
         bug=V(exit=1, has=['counts a1g main: done, rc=2 -- COMPLAINT'])),

    case('counts-all-retake-keeps-an-earlier-complaint', 'run-counts-all.sh',
         None,
         'CONTROL: a file kept from a sweep that complained is still a'
         ' complaint, the re-take not reading it again',
         shadow=dict(extra=[('zzch-lookrts', FAKE_HALF),
                            ('zzch-a1g', FAKE_HALF),
                            ('zzch-pair.txt', NOTE_STUB),
                            ('zzch-counts-a1g.txt', 'counted earlier\n'),
                            ('zzch-evening.txt',
                             EVENING_DONE + counts_attempt('zzch'))]),
         plant=lambda t: {'stub': stub_dir(t, PERF_ANSWERS)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'ONLY': 'shape-a',
              'ARMS': 'list', 'N': '1'},
         argv=['zzch'],
         ok=V(exit=1, has=['counts a1g main: zzch-counts-a1g.txt kept from'
                           ' an earlier call, which complained -- COMPLAINT',
                           'EVENING COMPLETE WITH 1 COMPLAINT(S)'])),

    case('g3-twins-refuses-a-note-naming-no-source', 'g3-twins.sh', '78f5ca2',
         'the twins were built from whatever Main.hs and shim the tree held,'
         ' against a note that names none',
         # The twins are of the pair's source only if the tree is at the
         # note's `Main.hs at` and `shim at` commits, and nothing asked.
         # A stand-in cabal says whether a build was started.
         shadow=dict(extra=[('zzg3-pair.txt', NOTE_STUB + G3_RECIPES)]),
         plant=lambda t: {'stub': stub_dir(
             t, '#!/bin/sh\necho stub cabal ran\nexit 1\n', name='cabal')},
         env={'PATH': '{stub}:/usr/bin:/bin'},
         argv=['zzg3'],
         ok=V(exit=2, has=["has no 'Main.hs at <commit>' row",
                           'nothing built'],
              hasnt=['stub cabal ran']),
         bug=V(exit=1, has=['stub cabal ran', 'twin did not build'])),

    case('g3-twins-refuses-a-source-git-cannot-name', 'g3-twins.sh', None,
         'CONTROL: with the rows there and no git to hold the tree to them,'
         ' nothing is built',
         # The shadow is outside any repository, so git answers nothing
         # here, as a dubious-ownership refusal would.
         shadow=dict(extra=[('zzg3-pair.txt', NOTE_STUB + G3_RECIPES
                             + '  Main.hs at        0123abc, tree clean\n'
                               '  shim at           4567def, tree clean\n')]),
         plant=lambda t: {'stub': stub_dir(
             t, '#!/bin/sh\necho stub cabal ran\nexit 1\n', name='cabal')},
         env={'PATH': '{stub}:/usr/bin:/bin'},
         argv=['zzg3'],
         ok=V(exit=2, has=['git names no commit for Main.hs',
                           'git names no commit for align-as.py'],
              hasnt=['stub cabal ran'])),

    case('g3-twins-builds-over-the-source-when-told', 'g3-twins.sh', None,
         'CONTROL: G3_TREE=1 builds from the tree over a mismatch, saying'
         ' the mismatch first',
         shadow=dict(extra=[('zzg3-pair.txt', NOTE_STUB + G3_RECIPES)]),
         plant=lambda t: {'stub': stub_dir(
             t, '#!/bin/sh\necho stub cabal ran\nexit 1\n', name='cabal')},
         env={'PATH': '{stub}:/usr/bin:/bin', 'G3_TREE': '1'},
         argv=['zzg3'],
         ok=V(exit=1, has=["has no 'Main.hs at <commit>' row",
                           'building from the tree as it stands',
                           'stub cabal ran'])),

    case('properties-page-is-each-process-own', 'properties.py', '8feaab9',
         'the round-trip wrote every table to one fixed temp path, which'
         ' concurrent runs share',
         # The suite runs properties.py up to seven at a time, so one
         # process could read back another's table or a file just
         # truncated. The race is not replayed; something else already at
         # the fixed name stands for the other process, a directory being
         # the occupant that fails every time rather than some.
         plant=lambda t: dict(corpus_of_one(t), tmpd=os.path.dirname(
             os.makedirs(os.path.join(t, 'tmpd', 'zz-prop-README.md'))
             or os.path.join(t, 'tmpd', 'x'))),
         env={'CORPUS': '{corpus}', 'TMPDIR': '{tmpd}'},
         argv=[],
         ok=V(exit=0, has=['every property holds'],
              hasnt=['IsADirectoryError']),
         bug=V(exit=1, has=['IsADirectoryError', 'zz-prop-README.md'])),

    # Four probes whose `sys.exit(str)` exited 1, their docstrings' code for
    # a finding or a failed build, where the run had not happened: exit 2
    # is this directory's did-not-run, as probe-second-term.py states it.
    # A PATH holding a python3 and no gcc stands for a box without the
    # tools.
    case('r39-rules-exits-2-on-a-run-not-here', 'probe-r39-rules.py',
         '82c6a1c',
         'a run whose JSON was absent exited 1, the code for candidates',
         argv=['zznorun', 'run38'],
         ok=V(exit=2, has=['is not here; nothing ran']),
         bug=V(exit=1, has=['is not here; nothing ran'])),

    case('fetch-model-exits-2-on-a-table-it-cannot-read',
         'probe-fetch-model.py', '82c6a1c',
         'a table with no layout exited 1, the code for a failed build',
         plant=lambda t: {'txt': write(os.path.join(t, 'empty.txt'), '')},
         argv=['rescore', '{txt}'],
         ok=V(exit=2, has=['carries no layout or no rows']),
         bug=V(exit=1, has=['carries no layout or no rows'])),

    case('entries-sweep-exits-2-without-its-tools', 'probe-entries-sweep.py',
         '82c6a1c',
         'a box without gcc exited 1, the code for a failed build',
         plant=lambda t: {'stub': stub_dir(
             t, '#!/bin/sh\nexec /usr/bin/python3 "$@"\n', name='python3')},
         env={'PATH': '{stub}'},
         argv=['fill'],
         ok=V(exit=2, has=['gcc is not on PATH; nothing ran']),
         bug=V(exit=1, has=['gcc is not on PATH; nothing ran'])),

    case('r38-sweep-exits-2-without-its-tools', 'probe-r38-sweep.py',
         '82c6a1c',
         'a box without gcc exited 1, which its siblings give a failed build',
         plant=lambda t: {'stub': stub_dir(
             t, '#!/bin/sh\nexec /usr/bin/python3 "$@"\n', name='python3')},
         env={'PATH': '{stub}'},
         argv=[],
         ok=V(exit=2, has=['gcc is not on PATH; nothing ran']),
         bug=V(exit=1, has=['gcc is not on PATH; nothing ran'])),

    case('interleave-refuses-a-cell-off-the-roster', 'probe-interleave.sh',
         'b741161',
         'a cell the binaries lack selected no bench and printed process'
         ' noise as measured ratios',
         # The sibling probe-stalls.sh refuses exactly this; here a typo
         # ran empty processes and the 2N-N difference came out a ratio
         # with a median and a range.
         shadow=dict(extra=[('zzil-a', FAKE_HALF), ('zzil-b', FAKE_HALF)]),
         plant=lambda t: {'stub': stub_dir(t, PERF_MODES)},
         env={'PATH': '{stub}:/usr/bin:/bin', 'PAIRS': '1'},
         argv=['zzil-a', 'zzil-b', 'main/shape-a/lits'],
         ok=V(exit=2, has=['main/shape-a/lits is not in ./zzil-a --list'],
              hasnt=['1.0000']),
         bug=V(exit=0, has=['main/shape-a/lits  1.0000'])),

    case('brief-facts-reads-a-basis-with-an-underscore', 'read-all.sh',
         'c8ffd5d',
         'a basis named with `_` read as no basis at all, and its md5 row'
         ' dropped',
         # pair-halves.sh allows [A-Za-z0-9_] in a half's name; the three
         # patterns here took [A-Za-z0-9] or [a-z0-9], so `look_rts`
         # matched nothing and the block said the log names no basis.
         plant=brief_facts_underscored_basis,
         argv=['{tag}', '--brief-facts'],
         ok=V(exit=0, has=['look_rts=0123456789abcdef0123456789abcdef',
                           'THIS RUN ONLY facts'],
              hasnt=['no `is the basis` clause']),
         bug=V(has=['no `is the basis` clause'],
               hasnt=['look_rts=0123456789abcdef0123456789abcdef'])),

    case('instance-gate-keeps-an-earlier-slow-draw', 'instance-gate.sh',
         'df1a269',
         'a second swap parked its slow draw over the first, freeing the'
         ' frames the header says a .slow holds',
         # `run-evening.sh RUN --from instance` re-runs the gate after a
         # swap, and `mv B B.slow` overwrote the first parked draw, whose
         # frames the next fresh copy then likely drew.
         shadow=dict(extra=[('zzig-pair.txt', NOTE_STUB),
                            ('zzig-a1g.slow', 'the first slow draw\n')]
                     + halves('zzig-lookrts', 'zzig-a1g')),
         env={'INSTANCE_DIR': '.', 'INSTANCE_FAKE': '1100,1000'},
         argv=['zzig'],
         probe=lambda subs: ' '.join(sorted(
             f for f in os.listdir(subs['at']) if f.startswith('zzig-')))
         + '\n' + open(os.path.join(subs['at'], 'zzig-a1g.slow')).read(),
         ok=V(exit=0, has=['zzig-a1g.slow2', 'the first slow draw',
                           'parked as ./zzig-a1g.slow2']),
         bug=V(exit=0, has=['parked as ./zzig-a1g.slow,'],
               hasnt=['the first slow draw', 'slow2'])),

    case('view-floor-legs-refuses-a-factor-it-ignores', 'view-floor.py',
         'ea3aa93',
         '--legs ignored --factor and failed at a hard-coded 2.0 percent,'
         ' the docstring naming the factor',
         # Legs of one view have no class floor to take a factor of, so
         # the exit was a literal nobody could set.
         plant=lambda t: {'legs': reroll_legs(t, 1.021)},
         argv=['zzvl', '--legs', '{legs}', '--factor', '5'],
         ok=V(exit=2, has=['--legs reads its bar from --bar']),
         bug=V(exit=1, has=['the A/A floor over 1 legs', '2.10%'])),

    case('view-floor-legs-takes-its-bar', 'view-floor.py', None,
         'CONTROL: --bar sets the spread --legs fails at, 2.0 by default',
         plant=lambda t: {'legs': reroll_legs(t, 1.021)},
         argv=['zzvl', '--legs', '{legs}', '--bar', '5'],
         ok=V(exit=0, has=['2.10%'])),

    # Three fixes to preflight.sh, whose steps and reporters have no case
    # (checks.py's UNCOVERED); how each bug direction was watched is its
    # record's `notes`.
    case('fill-in-survey-row-reads-the-listed-word-and-a-silent-survey',
         'preflight.sh', 'e164ea1',
         'the astride count read the word `listed` past ten spans, a refused'
         ' survey read as the straddle stop, and 10, 20 or 30 astride PASSed',
         # The sibling of `fill-in-straddle-row-reads-the-listed-word` on
         # the astride row, and the same function's two neighbours.
         argv=None, ok=None),

    case('fill-in-roster-rows-drop-their-headings', 'preflight.sh',
         '427f450',
         "--fill-in's roster rows kept `out` and `in` lines and dropped the"
         ' arms, shapes and views headings over them',
         argv=None, ok=None),

    case('note-paths-strip-a-name-s-own-first-character', 'preflight.sh',
         'a68dbd0',
         '10c stripped a line-initial `.`, `/` or `_` from the name itself,'
         ' so `./run40-x.json` was checked as `/run40-x.json`',
         argv=None, ok=None),

    # ---- check-all's own steps ----
    case('parallel-steps-leave-the-readings-fan-out-uncapped', 'checks.py',
         '8acfeaf',
         'a -j step ran post-run-readings.sh cases with its six readers'
         ' apiece, filling the box the seven was chosen to leave free',
         argv=['--unit', "[s[0] for s in STEPS if '-j' in s[1]"
                         " and 'READ_JOBS=1' not in s[1]]"],
         ok=V(has=['[]']),
         bug=V(has=["'cases, ok direction'", "'selftest mutants'"])),

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
    # would dose or restrict a driver the case did not ask to. Nor the
    # harness's own marker, which would make every evening case refuse in a
    # session that predates the reaper switch; the one case that wants it
    # sets it itself.
    'strip_env': ['BASIS', 'OTHER', 'SATURATE', 'SATURATE_BY', 'WILDLOG',
                  'SAT', 'ONLY', 'ARMS', 'N', 'MAXBUSY', 'FAKE_SATURATE',
                  'CLAUDE_CODE_SESSION_ID', 'INSTANCE_DIR', 'INSTANCE_FAKE',
                  'INSTANCE_BAR', 'INSTANCE_CELL', 'INSTANCE_N'],
    'cleanup': sweep,
    # THE CASES THAT BUILD IN THIS DIRECTORY, run alone under -j after the
    # rest: every read-all.sh case, `synthetic_run` being a run this
    # directory has to hold; the four --deflation cases, whose legs sit
    # beside the run; the staged and untracked documents, beside which a
    # case of each direction died in a traceback in the first parallel run
    # and passed alone; and preflight's step-9 case. Every other case
    # builds in its temp directory or a shadow. Derived 2026-09-18 from the
    # users of `here_file`, transitively, by name and not by call -- a
    # plant is passed as `plant=staged_doc` -- and the two undeclared ones
    # showed as a traceback in each direction of the first parallel run.
    'serial': ['read-all.sh',
               'deflation-ignores-the-saturated-legs',
               'deflation-legs-beside-the-run-not-the-cwd',
               'deflation-names-which-leg-set-is-missing',
               'deflation-skips-a-leg-with-no-positive-slope',
               'added-lines-over-head', 'added-lines-untracked',
               'superlative-worklist-names-its-settling-mode',
               'step-9-asserts-specconstr-of-every-basis'],
}
