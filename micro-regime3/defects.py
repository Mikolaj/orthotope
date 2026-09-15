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


def readme_with_a_registration(tmp, arm=None, task=None, task_arm=None):
    """The README plus a synthetic OPEN registration, at the end.

    SYNTHETIC and not an edit of the live one, which is the whole point:
    a registration lives in the open list only until post-run step 5 moves
    it into the run's own file, so a fixture that edits the live entry
    stops building the moment the run it belongs to is written up. This
    one appends its own, so the case answers for the CHECK rather than for
    whichever run happens to be in hand. Run 99 is a number no run reaches.

    `arm` names an arm to put in backticks -- pass `parked_arm()` for the
    defect direction -- and `task` a task number to defer to.

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
    entry = ("- `OPEN` **What Run 99 is built to answer, registered before"
             " it runs.** Registered for this fixture and for nothing else."
             " (1) *The box.* `list` moves under 3%; killed by more.")
    if arm:
        entry += " (2) *The arm.* `%s` leads its family; killed by a loss." % arm
    if task:
        entry += " (3) *The additions.* Task %s's, read there." % task
    if task_arm:
        entry += " (4) *The deferral.* Task 99's, read there."
        # After the HEADING LINE, not by paragraph: unwrapped, the heading
        # carries no blank line before it, so a `\n\n` split leaves it
        # glued to the paragraph above and finds nothing. The reader's own
        # `unwrapped_paragraphs` does isolate it, which is why the check
        # sees the tasks that this fixture could not.
        anchor = '\n### Recommended tasks after Run'
        assert text.count(anchor) == 1, ('tasks heading: %d site(s)'
                                         % text.count(anchor))
        eol = text.index('\n', text.index(anchor) + 1)
        text = (text[:eol + 1]
                + "\n99. `OPEN` **A planted task, for the deferral fixture"
                  " alone.** It predicts that `%s` leads its family; killed"
                  " by a loss.\n" % task_arm
                + text[eol + 1:])
    return write(os.path.join(tmp, 'R.md'), text + '\n' + entry + '\n')


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


def inherited_pair(tmp, n=97, share=True):
    """Two consecutive runs' files, the later copied from the earlier.

    Step 5 copies the previous run's file whole and the write-up edits it,
    so a paragraph nobody touched is BOTH inherited and outside the
    checker's diff, whose base is that copy. The fixture carries one of
    each kind: a paragraph making a claim about the run in front of it,
    which must be reported, and one of the standing apparatus every run
    re-carries, which must not. `share=False` is the control, the write-up
    having rewritten both, so the report has nothing to name.
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
    if share:
        body = claim + '\n' + standing
    else:
        body = ('**On Run %d the floor is 0.44%% on the basis half.** This'
                ' run reads it over the six A/A pairs.\n\nThe table below'
                ' is installed by the reader, never by hand.\n' % n)
    doc = write(os.path.join(d, 'run%d.md' % n),
                '# Run %d\n\nA head paragraph of its own.\n\n%s' % (n, body))
    return {'doc': doc}


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


def readings_digest(run='run97', bare=False):
    """A carrier's return for reading-list items 2, 4, 5 and 6.

    One `ITEM N` block apiece, each block the artifact the list already
    says that item owes, and each figure beside the invocation that
    re-emits it -- a claim with no named invocation being a gap, here as
    in the run file.

    `bare` heads each block `ITEM N` and nothing else, which is what the
    chapter asks for and what Run 27's carrier wrote; the titled form is
    Run 26's, so a check reading the header has to take both.
    """
    text = ('# %s-readings.txt -- the carrier\'s return for reading-list'
            ' items 2, 4, 5 and 6.\n\n'
            'ITEM 2 (the last run\'s head and Results prose)\n'
            '    what this run\'s head must answer: the last one rests on'
            ' a repetition this one cannot take.\n'
            '    from: ./read-run.py --section Results --run-doc'
            ' runs/run96.md\n\n'
            'ITEM 4 (the two-column table, the ONE table read)\n'
            '    does it carry the last run\'s columns? yes, both.\n'
            '    from: ./read-run.py --section \'What the next run compares'
            ' against\' --with-tables 1\n\n'
            'ITEM 5 (the properties and the prose after them)\n'
            '    live: three.\n'
            '    from: ./read-run.py --lint\n\n'
            'ITEM 6 (the class blocks)\n'
            '    the form: six numbered items, verdicts first, the'
            ' paragraph the author\'s.\n'
            '    from: ./read-run.py run96-rev.json --block\n' % run)
    if bare:
        text = re.sub(r'^(ITEM \d+) .*$', r'\1', text, flags=re.M)
    return text


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
    runs = {m.group(1) for m in re.finditer(r'\brun(\d+)-[a-z0-9]+', seg)
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
                 cheap_sum_only=False):
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
              ' `--changed <last run\'s commit>`. Slower and not weaker, so'
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
         'CONTROL: the geomean table is hand-edited, so one caller wants'
         ' them',
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
         ok=V(exit=0, has=['./run-status.sh $R', '10b.'],
              hasnt=['why: --para'])),

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
         argv=['--inherited', '--run-doc', '{doc}'],
         ok=V(exit=0, has=['0 paragraph(s)'])),

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
         ok=V(exit=0, has=['13 table(s) installed'])),

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
         ok=V(exit=0, has=['best outside family'],
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

    case('registration-clean-reads-ok', 'read-run.py', None,
         'CONTROL: a registration naming a timed arm and no task passes,'
         ' which is what says the two above failed for their planting',
         plant=lambda t: {'readme': readme_with_a_registration(t)},
         argv=['--lint', '--readme', '{readme}'],
         ok=V(exit=0, has=['every arm the OPEN registration(s) name is'
                           ' timed'])),

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
         ok=V(exit=0, has=['IN /bin/sh ONLY',
                           '3 matched nothing on the other side'],
              hasnt=['group(s) moved at all'])),

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

    case('status-wants-the-carriers-digest', 'run-status.sh', None,
         'the three steps that read the previous run through a carrier were'
         ' judged on nothing, so a delegated reading not taken read the same'
         ' as one taken',
         # Reading-list items 2, 4, 5 and 6 are one carrier's batch and its
         # return is $R-readings.txt. The chapter's own sentence is that a
         # reading which owes nothing cannot be told from a reading not
         # done; post-run 4 owes items 5 and 6, step 5 item 2 and step 6a
         # item 4, and each is judged on its block from Run 26 on.
         shadow=dict(),
         argv=['run98'],
         ok=V(exit=1, has=['no ITEM 5 block', 'no ITEM 6 block',
                           'no ITEM 2 block', 'no ITEM 4 block'])),

    case('status-reads-the-carriers-digest', 'run-status.sh', None,
         'CONTROL: with the blocks present those three steps read done',
         shadow=dict(extra=[('run97-readings.txt', readings_digest())]),
         argv=['run97'],
         ok=V(has=['carries the ITEM 2 block', 'carries the ITEM 4 block',
                   'carries the ITEM 5 block', 'carries the ITEM 6 block'],
              hasnt=['no ITEM 2 block'])),

    case('status-reads-a-bare-item-header', 'run-status.sh', 'e8f1c31',
         'a block headed `ITEM N` and nothing else read as absent, so the'
         ' carrier\'s return was owed four times over with the file there',
         # The chapter asks for `one ITEM N block apiece` and names no
         # title; Run 26's carrier wrote one anyway and Run 27's did not,
         # so the header that matched was the decorated one. `[^0-9]` was
         # there to keep ITEM 2 off ITEM 25 and took the end of the line
         # with it.
         shadow=dict(extra=[('run97-readings.txt',
                             readings_digest(bare=True))]),
         argv=['run97'],
         ok=V(has=['carries the ITEM 2 block', 'carries the ITEM 4 block',
                   'carries the ITEM 5 block', 'carries the ITEM 6 block'],
              hasnt=['no ITEM 2 block']),
         bug=V(has=['no ITEM 2 block', 'no ITEM 4 block', 'no ITEM 5 block',
                    'no ITEM 6 block'],
               hasnt=['carries the ITEM 2 block'])),

    case('status-wants-no-digest-before-run-26', 'run-status.sh', None,
         'CONTROL: the carrier batch is an instruction of 2026-09-05, and'
         ' every run up to 25 read the previous run\'s file directly',
         shadow=dict(),
         argv=['run20'],
         ok=V(exit=1, hasnt=['ITEM 2', 'ITEM 4', 'ITEM 5', 'ITEM 6'])),

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
