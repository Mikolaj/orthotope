#!/usr/bin/env bash
# The write-up's installs, all of them, in one call.
#
#     ./install-tables.sh run14           # writes runs/run14.md
#
# `--markdown`, `--fingerprint` and a `--block` per class,
# every one from the BASIS half, every one `--in-place`. That is a table
# per class and two more, a count a session loses track of: the failure is
# not a wrong table but a missing one, and a run file one table short looks
# exactly like one with them all.
#
# It installs and collects; it decides nothing. Each mode's stderr is the
# hand-work it leaves -- a row new to the roster installs as `?` and is
# filled by hand, a departed row is dropped with a warning -- so this
# gathers those and prints them at the end as the list they are.
#
# It also RANKS, once, and installs nothing from it: `--extremes` over the
# same class list, because a superlative about the classes -- widest, best,
# tightest floor -- is a claim about every population at once and this is
# the only program that holds them all. The cross-class summary is
# INSTALLED since 2026-09-22, its ten rows read off each class's own
# `--block` and its emphasis off that block's `summary bolds` line, which
# decides on the unrounded values where the table prints three decimals;
# what the rank owes the author is the sort under the sentence, not the
# sentence, and the prose around the table is still the author's but for
# the class section's lead tallies, installed off --cross-classes.
#
# The class list comes from the JSONs on disk rather than from a literal
# here: run-major.sh's own class literal went out of step with the binary
# once, and a write-up that installs one block too few is the same
# defect one stage later.
#
# Its defects, and the control that a full pass rewrites no table, are cases
# in defects.py; add one there before fixing anything here.
#
# WRITES THE RUN'S OWN FILE and nothing else -- every table a run
# publishes is in `runs/run<N>.md`, which is why one `DOC` can serve every
# install. Copy that file aside first and copy it back to undo:
# `git checkout --` discards every uncommitted edit with the install.
# Read the diff afterwards rather than the terminal: install prints what
# it replaced, not what the file now says.
#
# Measured over Run 13's artifacts, 2026-08-15, against a copy: ten calls
# write eleven tables; a full pass over a document that already carries them
# leaves the ELEVEN TABLES byte-identical, so a rerun after fixing one
# refusal costs nothing but a re-wrap: that measurement predates the
# computed-paragraph block below, which writes its three paragraphs per
# class as one line each where the document keeps them wrapped, so a full
# pass now comes back word for word identical and re-wrapped -- 24
# paragraphs on a document carrying them already, measured 2026-08-16. Nothing
# is wrapped by hand afterwards, the commit hook wrapping a tracked document
# back; and renaming a class block's bolded lead makes that one install
# refuse -- `0 line(s) start with '**`scaled`', need exactly one` -- which
# this reports and exits 1 on, the other ten having landed.
#

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./install-tables.sh RUN   # e.g. run14; writes runs/run14.md"
  exit 2
fi
R="$1"
# Both halves from the note's `HALVES:` line through pair-halves.sh: the
# basis every table comes from, and the other half for the cross-half line
# the class-block form calls item 5, which --block reads only when given
# the second JSON.
HALVES_SET=$(./pair-halves.sh "$R") || exit 1   # the note's HALVES
eval "$HALVES_SET"                                # line, and nothing else
# The run's own file, named after the run this driver was given -- not the
# newest in runs/, which is what read-run.py defaults to: installing run19's
# tables while run20.md exists is a mistake this can refuse and that one
# cannot see. Overridable so a dry run can aim at a copy, which is also
# this script's own control.
DOC=${DOC:-runs/$R.md}
[ -f "$DOC" ] || { echo "no $DOC -- a run publishes into its own file, so"
  echo "   make it before installing, or set DOC to name it"; exit 1; }

MAIN="$R-$BASIS-main.json"
[ -f "$MAIN" ] || { echo "no $MAIN -- wrong run or wrong BASIS?"; exit 1; }
# shellcheck disable=SC2010  # the names here are the drivers' own, alphanumeric
CLASSES=$(ls -1 "$R-$BASIS"-*.json 2>/dev/null \
            | grep -v -- '-main\.json$' | grep -v "^$R-gate-")
[ -n "$CLASSES" ] || { echo "no class JSONs for $R-$BASIS"; exit 1; }

# A HALF WHOSE NAME BEGINS WITH THE BASIS'S PLUS A HYPHEN is caught by the
# glob above: with BASIS=a1g and a control called `a1g-pa`, `$R-a1g-pa-rev.json`
# matches `$R-a1g-*.json`. Nothing downstream sees it -- MISSING is leads
# without JSONs and stays empty -- and `ls` sorts the control's file after
# the basis's own, so the CONTROL half's table is the one left in every
# class block, under a driver whose header says every table comes from the
# basis. Told apart by the tag: class names carry no hyphen (run-major.sh
# refuses one), so a tag that does is another half's name and not a class.
for f in $CLASSES; do
  t=${f#"$R-$BASIS-"}; t=${t%.json}
  case $t in *-*)
    echo "!! $f: the tag '$t' is not a class name -- class names carry no"
    echo "   hyphen, so this is another half caught by the basis glob and"
    echo "   its table would install as the basis's. Rename that half, or"
    echo "   move its JSONs aside before installing."
    exit 1 ;;
  esac
done

# The class list comes from the disk, so a class whose JSON is absent is
# simply never installed and the tables half of this driver says nothing --
# "a run file with ten of eleven installed looks exactly like one with
# eleven", which is what the header opens by warning about and what this
# loop was doing. The file's own block leads are the roster to check
# against: one bolded lead per class, and a lead with no JSON is a table
# that will not be written. Found 2026-08-16 by withholding one class JSON
# and watching ten tables install in silence.
# READ FROM THE CLASS SECTION ALONE, since 2026-09-02: a block's lead
# sits between `## The stride classes, run by run` and `## Provenance`,
# and a paragraph elsewhere that opens with a bolded backticked name is
# not one -- Run 23's head opened two with an ARM's name, `mut-odo` among
# them, and the hyphen check below refused the whole install over a lead
# that was never a block's. --check-doc refuses a stray CLASS name outside
# the section; an arm's name it cannot know, so the scope is what settles it.
CLASS_SECTION=$(awk '/^## The stride classes, run by run$/ {p=1; print; next}
                     p && /^## / {exit}  p' "$DOC")
[ -n "$CLASS_SECTION" ] || { echo "!! no '## The stride classes, run by run'"
  echo "   section in $DOC, so no class block can be found and nothing is"
  echo "   installed"; exit 1; }
LEADS=$(printf '%s\n' "$CLASS_SECTION" | grep -o '^\*\*`[a-z0-9]*`' \
          | tr -d '*`' | sort)
[ -n "$LEADS" ] || { echo "!! no class block leads in $DOC --"
  echo "   the check that a class is not silently skipped has"
  echo "   nothing to check against, so it did not run"; exit 1; }
# A lead carrying a hyphen is refused by name, as run-major.sh refuses the
# class: both patterns that find a block here read `[a-z0-9]`, so such a
# lead slipped both, they agreed, and the cross-check below could not fire
# -- the block then ran inside the one above it and took its figures.
# Found 2026-08-22 by review. Case: `install-refuses-a-hyphenated-lead`.
HYPHENATED=$(printf '%s\n' "$CLASS_SECTION" \
               | grep -o '^\*\*`[a-z0-9][a-z0-9-]*`' | tr -d '*`' | grep -- -)
if [ -n "$HYPHENATED" ]; then
  echo "!! a class block lead in $DOC carries a hyphen, which neither pattern"
  echo "   here can find and run-major.sh refuses in a class name:"
  printf '%s\n' "$HYPHENATED" | sed 's/^/     /'
  exit 1
fi
HAVE=$(printf '%s\n' $CLASSES | sed "s/^$R-$BASIS-//; s/\.json$//" | sort)
MISSING=$(comm -23 <(printf '%s\n' "$LEADS") <(printf '%s\n' "$HAVE"))
if [ -n "$MISSING" ]; then
  echo "!! $(printf '%s\n' "$MISSING" | wc -l) class block(s) in $DOC have no"
  echo "   $R-$BASIS-*.json, so their tables would go silently uninstalled:"
  printf '%s\n' "$MISSING" | sed 's/^/     /'
  # AND THE LINE EACH WAS FOUND ON, because the JSON is usually present and
  # the block is not. Run 20 wrote `**`reshape1` sits apart at 0.9995**`
  # into the chapter head and lost a long evening to the message above;
  # printing the lead ends it in one call. The class section is the only
  # part read for leads now, so what this names is a lead inside it.
  echo "   the lead each was found on -- a block's lead sits in the class"
  echo "   section, and anything else here is a paragraph that merely"
  echo "   begins with a bolded class name:"
  for m in $MISSING; do
    grep -n "^\*\*\`$m\`" "$DOC" | sed 's/^/     /'
  done
  exit 1
fi

# A class of fewer than three shapes has no per-shape line to install, and
# the reader is RIGHT not to emit one: `--block`'s per-shape paragraph is
# guarded by len(shapes) > 2. The computed-paragraph block below met that as
# `--block emitted no per-shape` and exited 1 -- AFTER the eleven tables had
# been written, so the file was left carrying fresh tables over stale
# computed paragraphs, at exit 1, and the message blamed the reader's output
# format for what the reader correctly does. Not hypothetical: five class
# blocks were two-shape when last written, which is the state the block
# below opens by recording. Asked HERE, where nothing has been written yet.
SHORT=$(python3 - "$CLASSES" <<'ENDPY'
import json, sys
for f in sys.argv[1].split():
    n = len({b['reportName'].split('/')[0] for b in json.load(open(f))[2]})
    if n < 3:
        print('%s: %d shape(s)' % (f, n))
ENDPY
)
if [ -n "$SHORT" ]; then
  echo "!! a class here has fewer than three shapes, so --block emits no"
  echo "   per-shape line for it and the computed-paragraph install would"
  echo "   refuse once the tables were already in:"
  printf '%s\n' "$SHORT" | sed 's/^/     /'
  echo "   NOTHING HAS BEEN WRITTEN. Either that class wants its third"
  echo "   shape, or this driver wants a two-shape form of that paragraph."
  exit 1
fi

BAD=0
DONE=0                       # tables, not invocations: --fingerprint
                             # installs two, so ten calls write eleven
HAND=""
install () {   # $1 = json, $2.. = mode
  local f=$1; shift
  local err
  err=$(./read-run.py "$f" "$@" --in-place --run-doc "$DOC" 2>&1 >/dev/null)
  if [ $? != 0 ]; then
    echo "  !! $f $* REFUSED:"
    printf '%s\n' "$err" | sed 's/^/       /'
    BAD=$((BAD + 1))
    return
  fi
  echo "  $f $*"
  DONE=$((DONE + $(printf '%s\n' "$err" | grep -c '^installed at ')))
  # The hand-work list is what a run must READ, so it holds only what is
  # owed BY THIS RUN. Collecting the whole of each mode's stderr put
  # `installed at ...`, every `ok:` line and the same standing reminder
  # once per class into a "not optional" block on a run with nothing
  # outstanding -- which is how a reader learns to skim the one list that
  # is not skimmable. Warnings about the data stay: they are this run's.
  local owed
  # A `summary row ... disagrees` line describes the row as it stood
  # BEFORE this call, the rows being installed after every block, so it is
  # set aside here and asked again below once they are in: Run 40's list
  # carried ten such lines for rows this same call had just replaced.
  owed=$(printf '%s\n' "$err" | grep -v '^installed at ' | grep -v '^ok: ' \
           | grep -v "^the block's prose is yours" \
           | grep -v '^summary row `[a-z0-9]*` disagrees')
  [ -z "$owed" ] || HAND="$HAND
    $f $*:
$(printf '%s\n' "$owed" | sed 's/^/      /')"
}

echo "=== installing into $DOC, all from $BASIS"
install "$MAIN" --markdown
install "$MAIN" --fingerprint --classes $CLASSES
# The two tables the write-up used to type, the Provenance anchors and the
# two-column geomeans: their rows off both halves' main JSONs, their
# headers and leads left to the prose (read-run.py --hand-tables).
if [ -n "${OTHER:-}" ] && [ -f "$R-$OTHER-main.json" ]; then
  install "$MAIN" --compare "$R-$OTHER-main.json" --hand-tables
else
  echo "  note: no other half's main JSON ($R-${OTHER:-}-main.json), so the"
  echo "  anchors and the two-column rows are NOT installed -- yours by hand"
fi
for c in $CLASSES; do install "$c" --block; done

# The block's THREE COMPUTED paragraphs, which --block emits and --in-place
# did not write: Controls, Provenance and the per-shape line. Leaving them to
# hand-copying cost 24 transcriptions a run and, on 2026-08-15, five class
# blocks that silently kept no per-shape line at all -- they were two-shape
# when last written and nothing said the line had become owed. The lead and
# the verdict paragraph stay the author's, as the form says; these three are
# the reader's own output and are installed like the table.
echo "=== installing each class block's computed paragraphs"
python3 - "$R" "$BASIS" "$DOC" "$LEADS" "$OTHER" <<'ENDPY' || BAD=$((BAD+1))
import os, re, subprocess, sys
R, BASIS, DOC, LEADS = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
OTHER = sys.argv[5]
doc = open(DOC).read(); paras = doc.split('\n\n')
# The class section alone, as the shell above reads it: its heading to the
# next `## `.
sec = next(i for i, p in enumerate(paras)
           if '\n## The stride classes, run by run' in '\n' + p)
sec_end = next(i for i in range(sec + 1, len(paras))
               if '\n## ' in '\n' + paras[i])
leads = {}
for i in range(sec, sec_end):
    m = re.match(r'\*\*`([a-z0-9]+)` ---', paras[i].lstrip())
    if m: leads[m.group(1)] = i
# The class blocks are picked out twice in this one file, by the grep above
# and by the pattern here, and this one asks for the dash the other does
# not. A lead missing from THIS list is not merely skipped: the block above
# it then runs to the next lead this pattern did find, and the loop rewrites
# every Controls/Provenance/per-shape paragraph in that range -- so the
# skipped block is handed the previous class's figures. Measured 2026-08-17
# against a copy with one lead's dash replaced by a single hyphen: the window
# block came out carrying `slice`'s provenance, anchor and shape count,
# reported as `24 computed paragraph(s) installed across 7 class block(s)`
# at exit 0. It is the failure the roster check above exists against, one
# stage later and worse. The two are held to each other instead.
# read-run.py's `install` carries no third pattern: it ends a block at any
# bolded backticked lead, which its own comment says is looser on purpose.
if sorted(leads) != sorted(LEADS.split()):
    grepped, here = set(LEADS.split()), set(leads)
    print('  REFUSED: the two ways this file finds a class block disagree.')
    print('    the grep above:  ' + ' '.join(sorted(grepped)))
    print('    the pattern here: ' + ' '.join(sorted(here)))
    # Name the difference rather than leaving it to be eyeballed: which
    # lead moved is the whole diagnosis, the lists are long enough that
    # spotting it by eye is a step, and it gives a case something to
    # assert that no OTHER disagreement can satisfy.
    for miss in sorted(grepped - here):
        print('    missing from the pattern: ' + miss)
    for extra in sorted(here - grepped):
        print('    matched by the pattern only: ' + extra)
    print('    a lead this one misses is given the block above it, whose'
          ' figures overwrite its own')
    sys.exit(1)
order = sorted(leads.items(), key=lambda kv: kv[1])
done = says_new = says_kept = 0
# WHAT THE CLASS SAYS IS PROSE ONCE WRITTEN, so its skeleton is installed
# only over the CARRIED copy -- the paragraph as the run file's first
# commit had it, which is the previous run's -- or over a skeleton still
# carrying `___`, and any other is the author's and kept. A file git has
# no commit of carries nothing to tell apart, so only a `___` is replaced.
carried = set()
added = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%H', '--',
                        DOC], capture_output=True, text=True)
rel = subprocess.run(['git', 'ls-files', '--full-name', DOC],
                     capture_output=True, text=True).stdout.strip()
if added.returncode == 0 and added.stdout.split() and rel:
    first = subprocess.run(['git', 'show', '%s:%s' % (added.stdout.split()[-1],
                                                      rel)],
                           capture_output=True, text=True)
    if first.returncode == 0:
        carried = {' '.join(q.split()) for q in first.stdout.split('\n\n')}
# NOTHING IS WRITTEN UNTIL EVERY CLASS HAS PASSED, so a refusal on a late
# class leaves the file as it was -- and says so, since 2026-09-18, where
# an earlier class's ADDED line used to stand on the screen over a file
# that never changed. The ADDED lines are printed after the write.
added = []
def refuse(*lines):
    for line in lines:
        print(line)
    print(f'  nothing written: {DOC} stands as it was')
    sys.exit(1)
def summary_row(blk, c):
    """One cross-class row's cells, read off that class's own --block.

    Every field is the reader's: the shape count from the header, the
    plain arm and its `worst` from the plain-arm line, the two named arms
    from theirs, the floor from the margin line, and WHICH COLUMN BOLDS
    from `summary bolds` -- computed there on the unrounded values, which
    is the whole reason it is not decided here.
    """
    def one(pat, what):
        m = re.search(pat, blk, re.M)
        if not m:
            refuse(f'  REFUSED {c}: --block emitted no {what} line, so the'
                   f' cross-class summary cannot be installed from it')
        return m.groups()
    shapes, _ = one(r'over (\d+) shapes of the (\w+) class', 'shape count')
    plain, worst = one(r'^\s*mut-odo-vecdims\s+\(the plain arm\)\s+'
                       r'([\d.]+)\s+worst\s+([\d.]+)', 'plain arm')
    oarm, oval = one(r'^\s*best outside vecdims\s+(\S+)\s+([\d.]+)',
                     'best outside vecdims')
    carm, cval = one(r'^\s*ceiling \(vecdims\)\s+(\S+)\s+([\d.]+)',
                     'ceiling')
    floor, _fp = one(r"floor of ([\d.]+)% \(`([^`]+)`\)", 'floor')
    bold, = one(r'^\s*summary bolds\s+(best outside vecdims|ceiling)',
                'summary bolds')
    out = f'`{oarm}` {oval}'
    ceil = f'`{carm}` {cval}'
    if bold == 'ceiling':
        ceil = f'**`{carm}`** {cval}'
    else:
        out = f'**`{oarm}`** {oval}'
    return f'| `{c}` | {shapes} | {plain} | {worst} | {out} | {ceil} | {floor}% |'


summary, left_standing = {}, []
for n, (c, start) in enumerate(reversed(order)):
    k = [x for x, _ in order].index(c)
    # The LAST block ends at the next heading, not at the end of the file.
    # It used to run to len(paras), and `### Provenance` sat right after
    # the last class block -- so a paragraph opening `Provenance:` in the
    # section of that name would have been silently rewritten with the
    # last class's elapsed and heap line. The split of 2026-08-25 moved
    # that section into the run file too, one heading below the last
    # class block and promoted to `## Provenance`, so the guard's subject
    # is live again and is the same section it always was. Non-vacuous 2026-08-16, both
    # ways over a copy carrying such a sentence: the committed version
    # replaced it with `scaled`'s provenance and this one leaves it. The
    # first attempt at that control proved nothing -- the old script was
    # run from the scratchpad, and it cds to its own directory, so it
    # found no JSONs and exited having done nothing.
    nxt = next((j for j in range(start + 1, len(paras))
                if paras[j].lstrip().startswith('#')), len(paras))
    # The heading boundary is EVERY block's, not the last one's: applied
    # to the last alone, a `###` section standing between two class blocks
    # fell inside the range of the one above it, and any paragraph of it
    # opening `Provenance:`, `Controls:` or `Per shape` was rewritten with
    # that class's figures and counted as installed, at exit 0. The comment
    # above records fixing exactly this for the last block. 2026-08-17.
    end = min(order[k + 1][1], nxt) if k + 1 < len(order) else nxt
    # The cross-half line is item 5 of the form and needs the other
    # half; where that JSON is absent -- a run that recorded one half --
    # the call drops back to a single-file block and the line is simply
    # not owed, which is what `have_other` below then asserts.
    other_json = f'{R}-{OTHER}-{c}.json'
    have_other = os.path.exists(other_json)
    # Said, and then HELD: a wrong OTHER looks exactly like a run that
    # recorded one half, so the skip names both readings -- and where the
    # block still carries an `Across the halves:` paragraph the refusal
    # below decides, this note alone having left a previous run's line
    # standing at exit 0 (2026-09-01, by review).
    if not have_other:
        print(f'  note {c}: no {other_json}, so no cross-half line is'
              f' installed -- correct for a run that recorded one half,'
              f' and a wrong OTHER otherwise')
    sweeps = [f'{R}-counts-{BASIS}-{c}.txt', f'{R}-counts-{OTHER}-{c}.txt']
    got = subprocess.run(['./read-run.py', f'{R}-{BASIS}-{c}.json', '--block',
                          '--brief']
                         + (['--compare', other_json] if have_other else [])
                         + (['--counts'] + sweeps
                            if have_other and all(map(os.path.exists, sweeps))
                            else []),
                         capture_output=True, text=True)
    if got.returncode != 0:
        # The reader's own words, not a guess about the block's shape: an
        # absent JSON used to surface as `--block emitted no Controls`,
        # which names the form and hides the missing file.
        refuse(f'  REFUSED {c}: read-run.py exited {got.returncode}:',
               '    ' + (got.stderr.strip().replace('\n', '\n    ')
                         or '(no stderr)'))
    blk = got.stdout
    # THE CROSS-CLASS SUMMARY'S OWN ROW, off the same block. Assembled by
    # hand until 2026-09-22, which is a transcription of figures this
    # output already carries -- and its bolding was the part sessions got
    # wrong, Run 28 breaking a three-decimal tie with `--pair`, a
    # different statistic, and bolding the wrong cell of `rev`.
    summary[c] = summary_row(blk, c)
    log = open(f'{R}-{BASIS}-{c}.log').read()
    m = re.search(r'elapsed (\S+); peak (\d+) MiB in use, (\d+) MiB max', log)
    if not m:
        refuse(f'  REFUSED {c}: no provenance line in {R}-{BASIS}-{c}.log')
    el, pk, mr = m.groups()
    def grab(tag):
        g = re.search(r'\n(\*{0,2}' + tag + r'.*?)(?=\n\n|\Z)', blk, re.S)
        return ' '.join(g.group(1).split()) if g else None
    ctrl, prov, per = grab('Controls:'), grab('Provenance:'), grab('Per shape')
    across = grab('Across the halves:') if have_other else None
    says = grab('What the class says:') if have_other else None
    if have_other and not across:
        refuse(f'  REFUSED {c}: the other half is on disk and --block emitted'
              f' no cross-half line, so item 5 of the form would be left'
              f' standing from the previous run')
    if not (ctrl and prov and per):
        refuse(f'  REFUSED {c}: --block emitted no ' +
              ('Controls' if not ctrl else 'Provenance' if not prov else 'per-shape'))
    if not have_other and any(paras[j].lstrip().lstrip('*')
                                  .startswith('Across the halves:')
                              for j in range(start, end)):
        refuse(f'  REFUSED {c}: no {other_json}, and the block carries an'
              f' `Across the halves:` paragraph -- a cross-half line left'
              f' standing from a previous run, or the note\'s HALVES line'
              f' names the wrong other half ({OTHER}); delete the paragraph'
              f' or fix the note, then rerun')
    ctrl = ctrl.replace('Controls:** ___ (the reading is yours). ', 'Controls:** ')
    prov = (prov.replace('elapsed ___', 'elapsed ' + el)
                .replace('peak ___ MiB', f'peak {pk} MiB')
                .replace('___ MiB max residency', f'{mr} MiB max residency')
                .replace(" (copy from the process's stderr line)", ''))
    # The four fills above are unasserted replaces against wording
    # `read-run.py` owns, so a reworded emit would install the literal
    # `___` into the run file at exit 0, and nothing sweeps for it the way
    # `check_doc` sweeps a published `?`. 2026-08-17.
    if '___' in ctrl or '___' in prov:
        refuse(f'  REFUSED {c}: a `___` placeholder survived the fill, so the'
              f' wording read-run.py emits has moved and this script is'
              f' filling a form that no longer exists')
    prov_at = None
    for j in range(start, end):
        s = paras[j].lstrip().lstrip('*')
        if s.startswith('Controls:'): paras[j] = ctrl; done += 1
        elif s.startswith('Provenance:'): paras[j] = prov; prov_at = j; done += 1
        elif s.startswith('Per shape'): paras[j] = per; done += 1
        elif across and s.startswith('Across the halves:'):
            paras[j] = across; done += 1
        elif says and s.startswith('What the class says:'):
            if '___' in paras[j] or ' '.join(paras[j].split()) in carried:
                paras[j] = says; says_new += 1
            else:
                says_kept += 1
    # Item 5 owed -- the other half on disk, the line emitted -- and no
    # `Across the halves:` slot in the block to fill: the loop above
    # matched nothing and moved on, which dropped the line in silence.
    # A block pasted from the pre-item-5 form is how the state arises.
    if across and not any(paras[j].lstrip().lstrip('*')
                              .startswith('Across the halves:')
                          for j in range(start, end)):
        refuse(f'  REFUSED {c}: the other half is on disk, --block emitted'
              f' the cross-half line, and the block has no `Across the'
              f" halves:` paragraph to fill -- item 5 of the form would be"
              f' dropped in silence')
    if prov_at is not None and not any(
            paras[j].lstrip().lstrip('*').startswith('Per shape')
            for j in range(start, end)):
        paras.insert(prov_at + 1, per); done += 1   # every class is three-shape now
        added.append(f'  {c}: per-shape line ADDED, the block had none')
# THE CROSS-CLASS SUMMARY, INSTALLED AND NOT TRANSCRIBED. The row ORDER
# is the document's own and not this script's: the table is inherited from
# run to run and reordering it would be a change nobody asked for, so the
# existing rows are read for their class names and refilled in place.
head = '| class | shapes | mut-odo-vecdims | worst | best outside vecdims'
sumj = next((j for j, t in enumerate(paras) if t.startswith(head)), None)
if sumj is None:
    print('  note: no cross-class summary table here to install; the ten'
          ' rows are printed above and are yours to place')
elif summary:
    rows = paras[sumj].split('\n')
    out, filled, kept = [], 0, []
    for line in rows:
        m = re.match(r'\| `(\w+)` \|', line)
        if m and m.group(1) in summary:
            out.append(summary[m.group(1)]); filled += 1
        else:
            if m:
                kept.append(m.group(1))
            out.append(line)
    paras[sumj] = '\n'.join(out)
    print(f'  {filled} cross-class summary row(s) installed, in the order the'
          f' table already had')
    if kept:
        # NOT a refusal: refusing writes nothing at all, and one stale row
        # would cost the whole install mid-write-up. The document is
        # written, the row is left as it stood, and the exit status says
        # so -- which is the `|| BAD=$((BAD+1))` this heredoc already
        # runs under, so the driver counts it with its other complaints.
        print('  !! and %d row(s) LEFT STANDING, this run having no block'
              ' for them: %s' % (len(kept), ' '.join(kept)))
        left_standing.append(len(kept))
open(DOC, 'w').write('\n\n'.join(paras))
for line in added:
    print(line)
print(f'  {done} computed paragraph(s) installed across {len(order)} class block(s)')
if left_standing:
    sys.exit(1)
if says_new:
    print(f'  {says_new} `What the class says:` skeleton(s) installed, each'
          f' `___` the finding the block owes')
if says_kept:
    print(f'  {says_kept} `What the class says:` paragraph(s) kept, written'
          f' since the run file was first committed')
ENDPY

# THE CLASS SECTION'S LEAD TALLIES, off --cross-classes's `lead:` line:
# the comparison count and split, the geomean range and both extremes,
# which the write-up transcribed by hand until 2026-09-26. The clause is
# replaced where the lead carries it, and a tail after it is the author's.
echo "=== installing the class section's lead tallies"
OTHERS=""
for c in $CLASSES; do
  o="$R-${OTHER:-}-${c#"$R-$BASIS-"}"
  [ -n "${OTHER:-}" ] && [ -f "$o" ] || { OTHERS=""; break; }
  OTHERS="$OTHERS $o"
done
if [ -z "$OTHERS" ]; then
  echo "  note: not every class has its other half's JSON, so the lead's"
  echo "  cross-half tallies are NOT installed -- yours by hand"
else
  # shellcheck disable=SC2086  # the names are the drivers' own, one word each
  CROSS=$(./read-run.py --cross-classes --classes $CLASSES --others $OTHERS 2>&1)
  if [ $? != 0 ]; then
    echo "  !! --cross-classes REFUSED:"
    printf '%s\n' "$CROSS" | sed 's/^/       /'
    BAD=$((BAD + 1))
  else
    python3 - "$DOC" "$CROSS" <<'ENDPY' || BAD=$((BAD+1))
import re, sys
DOC, cross = sys.argv[1], sys.argv[2]
lead = [l.split('lead: ', 1)[1] for l in cross.split('\n')
        if l.startswith('  lead: ')]
if len(lead) != 1:
    print('  !! --cross-classes printed %d lead line(s), need one' % len(lead))
    sys.exit(1)
lead = lead[0]
paras = open(DOC).read().split('\n\n')
sec = next(i for i, p in enumerate(paras)
           if '\n## The stride classes, run by run' in '\n' + p)
sec_end = next((i for i in range(sec + 1, len(paras))
                if '\n## ' in '\n' + paras[i]), len(paras))
pat = re.compile(r'Over the \S+ classes the reader counts \*\*.*? and'
                 r' `[^`]+` at \*\*[\d.]+\*\* on `[a-z0-9]+`')
hits = [(j, m) for j in range(sec, sec_end)
        for m in [pat.search(' '.join(paras[j].split()))]
        if m and '. ' not in m.group(0)]
if not hits:
    print('  note: no lead clause in the class section to replace; place'
          ' it by hand:\n    ' + lead)
    sys.exit(0)
if len(hits) > 1:
    print('  !! %d paragraphs of the class section carry the lead clause,'
          ' need one; nothing written' % len(hits))
    sys.exit(1)
j, m = hits[0]
flat = ' '.join(paras[j].split())
new = flat[:m.start()] + lead + flat[m.end():]
if new == flat:
    print('  the lead tallies already read as --cross-classes prints them')
else:
    paras[j] = new
    open(DOC, 'w').write('\n\n'.join(paras))
    print('  the lead tallies installed, the clause the class section'
          ' opens by quoting')
ENDPY
  fi
fi

# The one rank, and the one thing here that writes nothing. Assigned and
# then tested rather than piped: a pipeline exits with its LAST command's
# status, so `| sed` would report sed's success whatever the reader did,
# and this driver's whole contract is that a refusal is loud.
echo "=== the cross-class extremes, which the summary's superlatives want"
EXTR=$(./read-run.py --extremes --classes $CLASSES 2>&1)
if [ $? != 0 ]; then
  echo "  !! --extremes REFUSED:"
  printf '%s\n' "$EXTR" | sed 's/^/       /'
  BAD=$((BAD + 1))
else
  printf '%s\n' "$EXTR" | sed 's/^/  /'
fi

# The summary rows asked again, now that they are installed: --block
# without --in-place writes nothing and checks the row in DOC as it now
# stands, so what survives here is a row the install did not fix.
for c in $CLASSES; do
  still=$(./read-run.py "$c" --block --run-doc "$DOC" 2>&1 >/dev/null \
            | grep '^summary row `[a-z0-9]*` disagrees')
  [ -z "$still" ] || HAND="$HAND
    $c, after the summary install:
      $still"
done

echo
if [ -n "$HAND" ]; then
  echo "What the installs left for you, and it is not optional:$HAND"
  echo
fi
if [ "$BAD" -eq 0 ]; then
  echo "$DONE table(s) installed, counted off install's own lines rather"
  echo "than off the call count -- --fingerprint writes two, and so does"
  echo "--hand-tables, the anchors and the two-column rows, on one line. The"
  echo "cross-class"
  echo "summary is installed too since 2026-09-22, outside that count and"
  echo "reported on its own line above: its ten rows come off each"
  echo "class's own block and its emphasis off that block's \`summary bolds\`"
  echo "line, which decides on the UNROUNDED values where the table prints"
  echo "three decimals -- four of Run 29's ten rows tie at those decimals,"
  echo "and Run 28 broke such a tie with --pair, a different statistic, and"
  echo "got \`rev\` backwards. The rank above it is for the PROSE's"
  echo "superlatives, which are still yours, as is every word around the"
  echo "table but the lead's tallies installed above."
else
  echo "$BAD install(s) REFUSED -- a refusal is the design, never a silent"
  echo "write to the wrong place. Fix what it names -- a header it could not"
  echo "find, a run file that is not there -- and rerun;"
  echo "the ones that landed are idempotent."
fi
[ "$BAD" -eq 0 ] || exit 1
