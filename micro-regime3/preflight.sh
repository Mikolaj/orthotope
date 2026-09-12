#!/usr/bin/env bash
# The pre-run list's steps 4 to 10, in one call.
#
#     ./preflight.sh run19            # the halves from the note's HALVES line
#     ./preflight.sh run19 --note     # 10c, 10d and 8 alone, seconds
#     ./preflight.sh run19 --figures  # step 12b: the note's fill-in
#                                     # figures against the artifacts
#
# 10c runs THIRD rather than last, ahead of every expensive step: it and 8
# are the two that read what the preparation WROTE, and a defect in a note
# is the likeliest thing a first pass finds. Read at minute eight it costs the
# whole pass again; read at second five it costs nothing. `--note` is the
# other half of that -- the same two steps alone, wanting no binary, for a
# note or a registration edited after a full pass. It is NOT a preflight
# and says so on every run.
#
# The halves come from the note's `HALVES:` line through pair-halves.sh
# since 2026-09-02, as in every script here; there is no default to move.
# The non-vacuity note below was taken on Run 17's pair and names its
# halves, and re-reading it wants that pair's note.
#
# Eight tool calls became one. That is not the point: the point is that
# step 8 is the one README says is skipped most often, and a script cannot
# skip it. Each step below prints PASS or FAIL with what it read, and the
# exit status is the whole verdict -- so this is a thing to run, not to
# pipe, `tail` having eaten a nonzero status here before (README, the
# session notes on not piping a verification command).
#
# WHAT IT DOES NOT DO, and each is deliberate:
#   9b, the pair's own variable -- what the halves differ in is checked by
#       the command the PAIR NOTE names, or by the note saying which
#       variable leaves no trace. There is no general form of it, and a
#       script that guessed one would report a pair sound on a reading
#       that was never about that pair.
#   10a/10b, the --survey legs -- the build's, and their answer is the
#       binary's rather than the reading session's, so they go in the note
#       at step 2 and not here. And 10's own `--library` figure is a registered
#       variable of the pair, read against the note and not against any
#       threshold here, so its PASS says the figure was read and no more.
#   11 and 12, the smoke sweep and the roster pass -- machine time, and
#       properties of the pair rather than of the session, so they are
#       recorded in the note and inherited. Running them here would pay for
#       them again. Each has a script of its own for when it IS owed:
#       ./smoke-sweep.sh RUN and ./smoke-l1.sh RUN [CLASS ...].
#   13 onward -- the run list, which wants a quiet machine and a go-ahead.
#
# Non-vacuity, 2026-08-22, and demonstrated rather than asserted: two stub
# halves outside the run's namespace -- `zzrun-good` and `zzrun-bad`, made
# and removed in one call, answering `check`, `--list` and `diag` -- were
# broken one detection at a time. Halves disagreeing on `check` FAILs step
# 4,5; halves listing 9 benches against 10 FAILs step 6; a diag row ten
# times apart FAILs step 9 with `plain -O1 is ~10`. The same stubs unbroken
# PASS all three, which is the control that says the three FAILs were the
# breaks and not the stubs. On the real run17 pair it reads ten PASS and
# exits 0, reproducing every figure the Run 17 preparation read by hand:
# 1128 benches, byte-identical `check`, scan/mut 1.000, --library 25.3%.
# `--note`'s own, 2026-09-01, on two stub notes made and removed in one
# call: one naming an absent `probe-` path reads 10c FAIL and exits 1, one
# naming a present path reads 10c PASS and exits 0, and step 8 PASSes under
# both -- which is the control saying the FAIL was the stub and not the
# mode.
# Step 10's zero-fill FAIL, 2026-08-23: no stub reaches it through this
# script, a stub answering `check` being no ELF, so its awk was fed
# `./loop-offsets.py /bin/true run14-lookrts` -- `0 self-loops` for the
# first -- and named /bin/true, where the run14 pair names nothing.
# RE-TAKEN 2026-08-23 against a binary that outlives run14, whose
# artifacts went the same day: `./loop-offsets.py /bin/true run18-g914`
# reads `0 self-loops` for the first and 32 for the second, so the arm
# of the check that fires on a zero fill is still reachable and still
# names the binary it fired on. Re-aim it again whenever the pair it
# names is offered for deletion.
#
# `--fill-in`'s own, 2026-09-07, and it is a CONTROL rather than a break,
# the mode making no verdict to break: every derived row was read against
# the same figure taken independently by hand on the run27 pair, and all
# agreed -- the two md5s, the two .text sizes, 665 benches with identical
# listings, five gate arms at 95 benches, scan/mut 1.000, --library 12.8%,
# the two surveys, both ghc-internal strings, both baked RTS lines and both
# instrument counts. The row that earned the mode is `.text`: by hand it had
# been read from `size -A`'s SECOND field, the load address, which is equal
# on every build here and so looks stable across a roster change. Re-take
# the control whenever a row is added.
#
# RE-TAKEN 2026-09-11 on the run29 pair, for the two rows that read the
# PREVIOUS run, and this time the control is how the defect was seen -- both
# had gone dark on a renamed basis tag. They reproduce the readings that
# preparation took by hand at pre-run steps 2 and 6c, figure for figure:
# offsets [0, 0, 0, 24, 0, 4] and [0, 0], 2 and 2 displacements, 39 -> 36
# arms with four out and one in. The defect and how it was watched are
# `fill-in-keys-the-previous-build-on-this-run-s-tag` in defects.py.
#
# It has no case in defects.py, deliberately: this script's own steps are
# that corpus and the reader's gates, so a case would run them twice to
# assert what they already assert. What is unique to it -- the three
# detections above -- is what the stub proof covers. The cost of that is on
# the record: the corpus retirement of 2026-09-02 left the three calls below
# naming ./check-scripts.py, which had gone, and nothing ran them until Run
# 24's preparation read three FAILs saying `No such file or directory`.
set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./preflight.sh RUN [--note|--no-corpus|--corpus] [--figures] [--fill-in]"
  echo "  --note        steps 10c, 10d and 8 alone -- the ones that read what"
  echo "                the preparation WROTE, in seconds and with no binary"
  echo "  --no-corpus   everything but 8c and 8d, the two that read every run"
  echo "                JSON on disk: run this, launch 11 and 12, and take"
  echo "                the two afterwards with --corpus"
  echo "  --corpus      8c and 8d alone"
  echo "  --figures     re-derive the note's fill-in figures FROM THE"
  echo "                ARTIFACTS and report every row that disagrees --"
  echo "                pre-run step 12b, in seconds and running no step"
  echo "  --fill-in     and print the note's fill-in block DERIVED from what"
  echo "                this pass read, to paste at pre-run step 2. A row it"
  echo "                cannot derive prints <yours>; beside --corpus it"
  echo "                prints the one row THAT call fills, 8c and 8d"
  exit 2
fi
R=$1
NOTE_ONLY=0
# 8c reads every run JSON on disk and 8d plants fixtures beside them, so
# neither may run while a sweep is WRITING one: a smoke JSON caught
# half-written fails prop_selftest_over_the_corpus with a traceback, on a
# file no run produced. The list keeps them before step 11 for that
# reason, which costs the roster pass -- the pre-run half's longest step
# -- the minutes they take. These two flags are the way out: everything
# else first, the sweeps launched, and the corpus read when they land.
# Split 2026-09-03, after Run 24's preparation ran 8d beside a roster
# pass still writing its last leg and read the traceback as a defect.
CORPUS=1
REST=1
FILLIN=0
FIGURES=0
shift
for a in "$@"; do
  case $a in
    --note) NOTE_ONLY=1 ;;
    --no-corpus) CORPUS=0 ;;
    --corpus) REST=0 ;;
    --fill-in) FILLIN=1 ;;
    --figures) FIGURES=1 ;;
    *) echo "unknown argument '$a' --" \
            "./preflight.sh RUN [--note|--no-corpus|--corpus] [--figures] [--fill-in]"
       exit 2 ;;
  esac
done
# --fill-in reports what a pass READ, so it means nothing beside --note,
# which runs none of what it reports. Refused rather than absorbed, which
# is the defect family this tree counts.
# WITH --corpus IT IS ALLOWED, and prints the script-checks row alone: the
# pre-run list runs `--no-corpus --fill-in`, whose block marks 8c and 8d
# `<yours>` because they have not run yet, and refusing the flag on the
# call that DOES run them left those two rows to be written by hand --
# which is the transcription this mode exists to remove (2026-09-08).
# --figures RUNS NO STEP, so every other flag here selects steps it will
# not take. REFUSED rather than absorbed, which is the family this tree
# counts and which its own first form was an instance of: it exited early
# and left a `--fill-in` beside it doing nothing, silently (2026-09-10).
if [ "$FIGURES" = 1 ] \
   && { [ "$FILLIN" = 1 ] || [ "$NOTE_ONLY" = 1 ] \
        || [ "$CORPUS" = 0 ] || [ "$REST" = 0 ]; }; then
  echo "--figures runs no step, and every other flag here selects which"
  echo "steps run; take it alone."; exit 2
fi
if [ "$FILLIN" = 1 ] && [ "$NOTE_ONLY" = 1 ]; then
  echo "--fill-in reports what a pass read, and --note runs none of it;"
  echo "drop one of them."; exit 2
fi
if [ "$CORPUS" = 0 ] && [ "$REST" = 0 ]; then
  echo "--no-corpus and --corpus together ask for nothing to run"; exit 2
fi
# --note runs neither half, so a corpus flag beside it was taken and
# ignored: absorbed without effect is the defect family this tree counts.
if [ "$NOTE_ONLY" = 1 ] && { [ "$CORPUS" = 0 ] || [ "$REST" = 0 ]; }; then
  echo "--note runs 10c, 10d and 8 alone, so a corpus flag beside it means"
  echo "nothing; drop one of them."; exit 2
fi
HALVES_SET=$(./pair-halves.sh "$R") || exit 2   # the note's HALVES line,
eval "$HALVES_SET"                                # refused loudly without

# --figures: PRE-RUN STEP 12b, MADE MECHANICAL. The note's fill-in rows are
# re-derived FROM THE ARTIFACTS -- the two binaries and git -- and every
# figure the derivation produces must appear in the note's row of the same
# label. Not a diff of the whole block: the rows are prose a preparation
# writes, and what must survive that writing is the FIGURES.
#
# It runs no step, which is what makes it a seconds-long check owed after
# the note is filled in rather than a second preflight. Every row it reads
# is derivable without one: md5, .text, the two compilers out of the
# binaries, the baked RTS, the instrument counts, the two commits, the
# bench count and the gate's selection.
#
# IN ITS ROLE AND NOT MERELY PRESENT, which is the whole point: 12b's own
# text says a citation that has slid onto another row passes a presence
# test, and Run 28's preparation wrote this check by hand as a one-off
# script because nothing here did it. That script found two errors and its
# author threw it away, which is the shape this mode retires (2026-09-10).
figures () {
  python3 - "$R" "$BASIS" "$OTHER" <<'PY'
import os, re, subprocess, sys
R, basis, other = sys.argv[1], sys.argv[2], sys.argv[3]
def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True).stdout
try:
    note = open('%s-pair.txt' % R).read()
except OSError as e:
    print('BLOCKED: %s' % e); sys.exit(2)
if 'Verified when built' not in note:
    print('BLOCKED: %s-pair.txt has no fill-in block to read' % R)
    sys.exit(2)
# The block's rows: `  LABEL   VALUE`, continuations indented past it.
rows, label = {}, None
for line in note.split('Verified when built', 1)[1].splitlines():
    m = re.match(r'  (\S(?:.*?\S)?)\s{2,}(\S.*)$', line)
    if m and not line.startswith('    '):
        label, rows[m.group(1)] = m.group(1), m.group(2)
    elif label and line.startswith('    '):
        rows[label] += ' ' + line.strip()
want, extra, unchecked = [], [], []
for half in (basis, other):
    if not os.access('%s-%s' % (R, half), os.X_OK):
        extra.append('%-16s ./%s-%s is not here, so its rows went unread'
                     % ('(binary)', R, half))
        continue
    b = '%s-%s' % (R, half)
    want.append(('md5 %s' % half, sh('md5sum %s' % b).split()[:1]))
    want.append(('.text', sh("size -A %s | grep '^\\.text'" % b).split()[1:2],
                 True))
    want.append(('compilers', [sh("strings %s | grep -oE"
                                  " 'ghc-internal-[0-9.]+' | sort -u"
                                  % b).strip()], True))
    # THE INSTRUMENTS ROW IS A VERDICT AND NOT A FIGURE -- the note writes
    # `one @@wild and one @@saturate`, which no digit matches, and there is
    # no figure here to slide onto a neighbouring row. So the COUNT is
    # asserted of the binary and the ROW is held to naming both marks,
    # which is what it is for. Found by this mode's first run against a
    # hand-written note (2026-09-10).
    for t in ('@@wild', '@@saturate'):
        got = sh("strings %s | grep -c '%s'" % (b, t)).strip()
        if got != '1':
            extra.append('instruments      %s carries %s %s, want 1'
                         % (b, got, t))
    want.append(('instruments', ['@@wild', '@@saturate']))
    rts = re.search(r'"(-A\S[^"]*)"',
                    sh('./%s +RTS --info 2>/dev/null | grep with-rtsopts' % b))
    want.append(('baked RTS', [rts.group(1)] if rts else ['UNREADABLE']))
for lbl, path in (('Main.hs at', 'Main.hs'), ('shim at', 'align-as.py')):
    want.append((lbl, [sh('git log -1 --format=%%h -- :/micro-regime3/%s'
                          % path).strip()]))
n = len(sh('./%s-%s --list 2>/dev/null' % (R, basis)).split())
want.append(('--list', ['%d benches' % n]))
# BOTH QUANTITIES THE ROW'S LABEL IMPLIES: the bench count alone left
# `gate arms` checking a figure the label does not name (2026-09-10).
gate = sh('./run-gate.sh %s --show 2>/dev/null' % R)
gf = [m.group(1) for m in
      (re.search(r'arms\s+(\d+)', gate), re.search(r'expect (\d+) benches', gate))
      if m]
if gf:
    want.append(('gate arms', gf))
bad, checked, seen = list(extra), 0, {}
# THE ORDER RULE IS FOR THE TWO ROWS THAT CARRY BOTH HALVES UNDER ONE
# LABEL AND DIFFERENT FIGURES IN THEM -- `.text` and `compilers`. Applied
# to every row it fired on `instruments`, whose halves carry the same two
# marker names by design, which is an assertion about nothing.
for entry in want:
    lbl, figs = entry[0], entry[1]
    ordered = len(entry) > 2 and entry[2]
    if lbl not in rows:
        bad.append('%-16s NO SUCH ROW in the note' % lbl); continue
    for f in figs:
        # AN EMPTY DERIVATION IS NOT A CHECK. `if f and ...` skipped it
        # and the summary counted it anyway, so a git that answered
        # nothing, or a binary that would not read, moved no number on a
        # PASS line -- the only evidence the check bit (2026-09-10).
        if not f:
            unchecked.append('%-16s the artifact gave nothing to check'
                             % lbl)
            continue
        at = rows[lbl].find(f)
        if at < 0:
            bad.append('%-16s the artifact says %s; the row reads: %s'
                       % (lbl, f, rows[lbl][:60]))
            continue
        checked += 1
        # AND IN THE RIGHT HALF'S PLACE. Four rows carry both halves under
        # one label, and a presence test passes them swapped -- which is
        # the very failure this mode exists against, one level down. The
        # basis is written first in every such row, so its figure must
        # come first (2026-09-10).
        if ordered and lbl in seen and seen[lbl] > at:
            bad.append('%-16s %s is the control\'s and stands before the'
                       ' basis\'s in the row' % (lbl, f))
        if ordered:
            seen[lbl] = at
if unchecked:
    bad += unchecked
if bad:
    print('12b FAIL: %d finding(s):' % len(bad))
    for b in bad:
        print('  ' + b)
    sys.exit(1)
print('12b PASS: %d figure(s) over %d row(s), each re-derived from the'
      ' artifacts and found in its own row and its own half\'s place'
      % (checked, len({e[0] for e in want})))
PY
}
if [ "$FIGURES" = 1 ]; then
  figures; exit $?
fi
if [ "$NOTE_ONLY" = 0 ]; then
  for h in $OTHER $BASIS; do
    [ -x "./$R-$h" ] || { echo "missing ./$R-$h -- $R-pair.txt has the recipe"
                          exit 2; }
  done
fi

# Scratch OUTSIDE the run's own namespace: a $R-*.json or $R-*.log here is
# read by run-major.sh as a previous attempt and by read-all.sh as one of
# the run's own processes, which is how a half-written probe once turned
# eighteen clean gates into two failures (README, the Run 17 tasks).
TMP=$(mktemp -d "${TMPDIR:-/tmp}/preflight.XXXXXX") || exit 1
# A FAILED step's raw output is KEPT rather than deleted. Every step
# redirects into $TMP and every verdict quotes a `tail -1` or a `grep -m1`
# of it, so deleting it at exit destroyed the evidence and kept a summary
# of the destroyed thing: 8d failed under this script and passed standing
# alone, and what would have said why was gone (2026-09-03). It stays in
# the TEMP directory, which the machine wipes -- a run's scratch does not
# belong in the checkout, and this is scratch. BUT THE PATH IS NOT ONE TO
# HAND ON: the outer wrapper puts a tmpfs over /tmp, so a directory a
# session keeps there is invisible from Mikolaj's own shell and from any
# other session. Whoever ran preflight can read it; anyone else needs the
# part that matters copied out.
# Written as if/else and not `A && B || C`: that shape runs C when A
# fails, which is how a fallback comes to speak for a command that never
# ran, and this file is read as an example.
trap 'if [ "${BAD:-0}" -gt 0 ] && [ -d "$TMP" ]; then
        echo "  the raw output of every step kept in $TMP -- wiped with /tmp,"
        echo "  and readable only where this ran; copy out what you hand on"
      else
        rm -rf "$TMP"
      fi' EXIT

BAD=0
say () {  # say STEP VERDICT DETAIL
  printf '  %-4s %-4s %s\n' "$1" "$2" "$3"
  # Every verdict is also recorded tab-separated, so --fill-in can quote a
  # step's own reading rather than taking it again: the fill-in block is
  # then provably the data the verdicts were given on, and not a second
  # measurement that could disagree with them.
  printf '%s\t%s\t%s\n' "$1" "$2" "$3" >> "$TMP/verdicts"
  [ "$2" = PASS ] || BAD=$((BAD + 1))
}

step_8 () {
  ./read-run.py --check-doc --quiet > "$TMP/doc" 2>&1 \
    && say 8 PASS "anchors, paths, widths, sweeps" \
    || say 8 FAIL "--check-doc: $(grep -m1 FAIL "$TMP/doc")"
}

# THE TWO STEPS THAT READ WHAT THE PREPARATION WROTE are functions rather
# than lines in the flow, because they are the two it re-runs. 8 reads the
# documents and 10c the note, both in seconds, and neither wants a binary
# -- so `--note` is them alone, and a note or a registration edited after a
# full pass is re-checked without paying again for 8c and 8d, which read
# this directory's Python source and its run JSONs and cannot have moved.
# Run 23's preparation paid two whole passes to re-test 10c, 2026-09-01.
  step_10c () {  # 10c. AND WHAT THE NOTE POINTS AT, which nothing else reads. The run
  # file must OUTLIVE its artifacts and --check-doc now refuses one that
  # names them; the pair note is the opposite -- it is MEANT to go with the
  # pair -- so the rule it needs is the weaker one, that anything it cites
  # outlives IT. That matters because the note is the entry point a later
  # session re-enters a prepared run through, and a preparation may be days
  # old, this chapter says so outright. A note pointing at a directory somebody
  # tidied is a stale entry point, and the session that follows it finds out
  # at the moment it is trusting the note most.
  #
  # Paths are taken from backticked and bare mentions of this directory's own
  # artifact names. Anything outside the run's and probe's namespaces is not
  # a path this can check and is left alone.
  #
  # A probe name may not END the captured token on `.` or `-`, which is what
  # the last character class is for: `.` is in the body class, so a name at
  # the end of a SENTENCE used to be captured with the full stop attached and
  # reported gone. A `probe-ds-{off,on}-g912` brace form is captured WHOLE,
  # the braces being in the body class, and expanded by hand below, however
  # many groups and an empty alternative among them: a body
  # class that stopped at the brace captured `probe-ds-`, and a last class
  # admitting `-` let that truncation through, so a note naming the form
  # FAILed with every path present -- Run 23's preparation met both forms
  # in one call, 2026-09-01, and the brace half was still open by review
  # the same day. Non-vacuity, that day, on stub notes made and removed in
  # one call beside two stub directories: `reproduces probe-zzst-a.` and
  # `probe-zzst-{a,b}` each PASS, `probe-nosuchthing-g912` FAILs naming
  # that path, and the brace form FAILs naming `probe-zzst-b` once that
  # directory is removed -- so the arm that fires on an absent path is
  # reachable through the plain form and the expanded one alike. The same
  # day on `probe-zzst-{a,b}-{c,d}` over four stub directories: PASS with
  # all four present, FAIL naming `probe-zzst-b-d` with that one removed.
  # AND A THIRD BOUNDARY, on the LEFT, 2026-09-10: with none, a name that
  # merely CONTAINS the run's own leaves its tail behind as a path of its
  # own, so a note saying `smoke-l1-run28-bcast.json` -- which the roster
  # pass writes and which was present -- reported `run28-bcast.json` gone.
  # The leading character is consumed by the match and stripped after it,
  # `grep -oE` having no lookbehind; at the head of a line nothing is
  # consumed and the first character is alphanumeric, so the strip is a
  # no-op there. AND THE NAME IS TAKEN WHOLE, prefix and all: a boundary
  # alone made the step blind to every `smoke-l1-$R-*.json` the roster
  # pass writes and the note names, since `smoke-l1-` fails the class and
  # the tail no longer matched on its own -- a loud false report traded
  # for a silent gap, which is the worse of the two. Non-vacuity
  # 2026-09-10, on one line carrying both forms: a planted
  # `run28-nosuchthing.json` and a planted `smoke-l1-run28-nosuch.json`
  # are each named, and a present name of either form is not. `/` is in
  # neither class for the same reason `-` is: a path under a directory is
  # one path, and a boundary that stopped at the slash read
  # `smoke-legs-1/smoke-l1-$R-bcast.json` as a bare file in this one.
  if [ -f "$R-pair.txt" ]; then
    MISSING=$(grep -oE '(^|[^A-Za-z0-9._/-])(probe-[A-Za-z0-9._{},-]*[A-Za-z0-9_}]/?|[A-Za-z0-9._/-]*'"$R"'-[A-Za-z0-9._-]+\.(json|log|txt))' \
                "$R-pair.txt" | sed -E 's/^[^A-Za-z0-9]//' | sort -u \
              | while read -r q; do
                  # Brace groups expand without eval, one group a pass
                  # until none is left, split by hand because `read -a`
                  # DROPS a trailing empty alternative (`{-x,}`) while
                  # keeping a leading one; and a bare comma joins two
                  # names, so a comma-carrying leaf splits into paths.
                  todo=("${q%/}")
                  while [ "${#todo[@]}" -gt 0 ]; do
                    q=${todo[0]}; todo=("${todo[@]:1}")
                    case $q in
                      *\{*\}*)
                        pre=${q%%\{*}; rest=${q#*\{}; post=${rest#*\}}
                        body=${rest%%\}*}
                        while :; do
                          case $body in
                            *,*) todo+=("$pre${body%%,*}$post")
                                 body=${body#*,} ;;
                            *)   todo+=("$pre$body$post"); break ;;
                          esac
                        done ;;
                      *,*)
                        left=${q%%,*}; rest=${q#*,}
                        [ -z "$left" ] || todo+=("$left")
                        [ -z "$rest" ] || todo+=("$rest") ;;
                      *) [ -e "$q" ] || echo "$q" ;;
                    esac
                  done
                done)
    if [ -z "$MISSING" ]; then
      say 10c PASS "every path $R-pair.txt names is still here"
    else
      say 10c FAIL "$R-pair.txt points at $(printf '%s\n' "$MISSING" | wc -l) \
  path(s) that are gone: $(printf '%s ' $MISSING)"
    fi
  else
    # Unreachable since pair-halves.sh refuses a missing note at the head
    # of this script, and kept as the loud form for the day that changes.
    say 10c FAIL "no $R-pair.txt -- the note is written at pre-run step 2"
  fi
}
step_10d () {  # 10d. AND THAT THE RECIPES BUILD THE HALVES THE LINE NAMES:
  # pair-halves.sh read the HALVES line above and refused an environment
  # disagreeing with it, but the line can name halves the recipe blocks do
  # not build, and that is a note describing another pair. Non-vacuity
  # 2026-09-01 on stub notes: a note naming both halves PASSes, one
  # naming only the basis FAILs naming the other's binary.
  [ -f "$R-pair.txt" ] || return 0
  MISS=$(for h in $BASIS $OTHER; do
           grep -q "$R-$h" "$R-pair.txt" || echo "$R-$h"; done)
  if [ -z "$MISS" ]; then
    say 10d PASS "HALVES line basis=$BASIS other=$OTHER, and the note names both binaries"
  else
    say 10d FAIL "$R-pair.txt never names: $(echo $MISS) -- its HALVES line and its recipes disagree"
  fi
}
if [ "$NOTE_ONLY" = 1 ]; then
  echo "preflight for $R: the note and the documents alone"
  echo
  step_10c
  step_10d
  step_8
  echo
  if [ "$BAD" -eq 0 ]; then
    echo "the steps that read what this half WROTE are clean. THIS IS NOT"
    echo "A PREFLIGHT: 4 to 7, 8b to 8d, 9 and 10 did not run, so a pair is"
    echo "not sound on this. Run ./preflight.sh $R whole before the gate."
  else
    echo "$BAD step(s) FAILED -- fix, then rerun this before the whole pass."
  fi
  exit $((BAD > 0))
fi

echo "preflight for $R: basis $BASIS, control $OTHER"
echo

if [ "$REST" = 1 ]; then
# THE TWO HALVES CHECK CONCURRENTLY, which is the whole of this step's
# cost -- `check` runs over every shape and class view, the two runs take
# minutes apiece and nearly all of a preflight between them, and they are
# independent: each reads its own binary and writes its own log, and the
# assertion below is that the two logs AGREE, which no scheduling can
# move. `check` is a correctness pass and times nothing, so contention
# reaches no figure. Halved 2026-09-10; before it they ran one after the
# other for no reason but the order the list writes them in.
"./$R-$BASIS" check > "$TMP/a.log" 2>&1 & pa=$!
"./$R-$OTHER" check > "$TMP/b.log" 2>&1 & pb=$!
wait "$pa"; ra=$?
wait "$pb"; rb=$?
if [ "$ra" != 0 ] || [ "$rb" != 0 ]; then
  say '4,5' FAIL "a check exited $ra/$rb -- read $TMP before it goes"
elif cmp -s "$TMP/a.log" "$TMP/b.log"; then
  # The two exit statuses are on the PASS line and not the FAIL line alone,
  # since 2026-09-07: a preparation that wants them re-ran `check` by hand
  # to read them, which the pre-run list forbids by name and which costs
  # minutes over the whole shape set. They are 0 and 0 here by construction
  # -- a nonzero one takes the branch above -- and printing them is what
  # says so without a second run.
  say '4,5' PASS "both halves agree on every shape, byte-identical; \
check exited $ra and $rb"
else
  say '4,5' FAIL "the halves' check output DIFFERS -- the pair is not sound"
fi

"./$R-$BASIS" --list 2>/dev/null > "$TMP/la"
"./$R-$OTHER" --list 2>/dev/null > "$TMP/lb"
N=$(wc -l < "$TMP/la")
if [ "$N" -eq 0 ]; then
  say 6 FAIL "--list gave nothing; wrong binary?"
elif cmp -s "$TMP/la" "$TMP/lb"; then
  say 6 PASS "$N benches, the two listings identical"
else
  say 6 FAIL "the halves ROSTER DIFFERENTLY -- one source built twice does not"
fi

# 6b. THE GATE'S OWN SELECTION, derived by the script that will run it rather
# than read out of it by eye. `--show` pays for the check run-gate.sh makes
# before its forty minutes -- every glob in SEL listed once per shape by BOTH
# halves -- and prints the count the note's `gate arms` line owes. Both halves
# of that earn the step: the refusal is a check, catching a gate arm the roster
# has parked, and the printed count is what stops a note carrying the previous
# run's globs. Run 25's preparation wrote exactly that, on 2026-09-04, the day
# the prune parked two of the five and re-cut SEL in the same commit.
if ./run-gate.sh "$R" --show > "$TMP/gate" 2>&1; then
  say 6b PASS "$(grep -c '^  glob' "$TMP/gate") gate arm(s), \
$(grep -m1 'expect ' "$TMP/gate" | sed 's/^ *expect *//')"
else
  say 6b FAIL "the gate refuses its own selection: $(tail -1 "$TMP/gate")"
fi

step_10c
step_10d

./read-run.py --lint > "$TMP/lint" 2>&1 \
  && say 7 PASS "roster and shape annotations" \
  || say 7 FAIL "--lint: $(grep -m1 FAIL "$TMP/lint")"

step_8

# 8b is three lint steps and not one: the defect families over the Python
# here and the two linters over the Python and the shell. An absent linter
# FAILS the step by name rather than being skipped, which is checks.py's
# rule, and absent means the invocation this step actually makes does not
# run -- so pyflakes is tested as the module it is invoked as, while
# `command -v` decides the shell linter, which is a command.
(
  command -v defect-lint.py >/dev/null \
    || { echo "defect-lint.py is not on PATH: the families went unchecked"
         exit 1; }
  defect-lint.py . || exit 1
  python3 -m pyflakes --version >/dev/null 2>&1 \
    || { echo "pyflakes is not on PATH: the Python here went unlinted"
         exit 1; }
  python3 -m pyflakes ./*.py || exit 1
  command -v shellcheck >/dev/null \
    || { echo "shellcheck is not on PATH: the shell here went unlinted"
         exit 1; }
  shellcheck -S warning -f gcc ./*.sh || exit 1
) > "$TMP/fam" 2>&1 \
  && say 8b PASS "the families and the two linters over this directory" \
  || say 8b FAIL "lint: $(tail -2 "$TMP/fam" | head -1)"

# The regime, in the binary, which nothing later can confirm. Read as
# README reads it: baseOffsetsScan against baseOffsetsMut on vgg-14-c512,
# equal to three figures under SpecConstr and ten times apart at plain -O1.
# WHICH OF THE TWO TO EXPECT IS THE NOTE'S TO SAY AND NOT THIS SCRIPT'S.
# Both readings are the list's, and this step asserted the first alone --
# harmless while the basis carried `-fspec-constr`, which it did on every
# run from Run 8 to Run 29, and a FAIL on the first pair whose basis does
# not. Run 30's halves are both plain -O1 by the request of 2026-09-12, so
# the binary was right and the expectation was wrong. Read the flag off the
# BASIS half's own recipe block, which 10d already holds to the HALVES
# line, and hold the binary to what its recipe asks for.
RECIPE=$(awk -v b="$R-$BASIS" -v o="$R-$OTHER" '
  $1 == o { f = 0 }
  $1 == b { f = 1 }
  f && /^[^ ]/ && $1 != b { f = 0 }
  f { print }' "$R-pair.txt" 2>/dev/null)
case "$RECIPE" in
  '')              WANT=unknown ;;
  *-fspec-constr*) WANT=spec ;;
  *)               WANT=o1 ;;
esac
SCAN=$("./$R-$BASIS" diag 2>/dev/null \
       | awk '/^vgg-14-c512 /{f=1} f && /baseOffsetsScan /{print $(NF-3); exit}')
MUT=$("./$R-$BASIS" diag 2>/dev/null \
      | awk '/^vgg-14-c512 /{f=1} f && /baseOffsetsMut /{print $(NF-3); exit}')
if [ -z "$SCAN" ] || [ -z "$MUT" ]; then
  say 9 FAIL "could not read the diag row; regime UNCONFIRMED"
elif [ "$WANT" = unknown ]; then
  say 9 FAIL "no recipe block for $R-$BASIS in $R-pair.txt; regime UNCONFIRMED"
else
  RATIO=$(python3 -c "print('%.3f' % ($SCAN/$MUT))")
  IS_SPEC=0
  python3 -c "import sys; sys.exit(0 if 0.98 < $SCAN/$MUT < 1.02 else 1)" \
    && IS_SPEC=1
  if [ "$WANT" = spec ] && [ "$IS_SPEC" = 1 ]; then
    say 9 PASS "SpecConstr, which the basis recipe asks for: scan/mut $RATIO on vgg-14-c512 ($SCAN vs $MUT)"
  elif [ "$WANT" = spec ]; then
    say 9 FAIL "the basis recipe sets -fspec-constr and the binary does not read as SpecConstr: scan/mut $RATIO -- SpecConstr is ~1"
  elif [ "$IS_SPEC" = 1 ]; then
    say 9 FAIL "the basis recipe sets no -fspec-constr and the binary reads as SpecConstr: scan/mut $RATIO -- plain -O1 is ~10"
  else
    say 9 PASS "plain -O1, which the basis recipe asks for: scan/mut $RATIO on vgg-14-c512 ($SCAN vs $MUT)"
  fi
fi

# Held to what it read and not to its exit alone: the plain form exits 0
# whatever it finds, so `0 self-loops` in a half PASSed here against the
# header's "exit status is the whole verdict". Two `==` headers, one per
# half, each with a count above zero, is what a half of this benchmark
# reads -- the run-fill loop is in every build this README has timed.
if ./loop-offsets.py "$R-$OTHER" "$R-$BASIS" > "$TMP/fills" 2>&1; then
  HEADS=$(grep -c '^== ' "$TMP/fills")
  EMPTY=$(awk '/^== / && $3 == 0 { print $2 }' "$TMP/fills" | tr -d :)
  if [ "$HEADS" != 2 ]; then
    say 10 FAIL "loop-offsets reported on $HEADS half/halves, not 2"
  elif [ -n "$EMPTY" ]; then
    say 10 FAIL "no 28-byte fill at all in $(echo $EMPTY) -- a half of this?"
  else
    say 10 PASS "fills read for both halves (the comparison is yours)"
  fi
else
  say 10 FAIL "loop-offsets refused: $(tail -1 "$TMP/fills")"
fi
./loop-offsets.py --library "$R-$BASIS" "$R-$OTHER" > "$TMP/lib" 2>&1 \
  && say 10 PASS "$(grep -m1 'same offset' "$TMP/lib" | sed 's/^ *//')" \
  || say 10 FAIL "--library refused: $(tail -1 "$TMP/lib")"
fi

# THE RUN BEHIND THIS ONE, as a number: the highest runs/run<N>.md below
# this run's N. Two places want it -- 8d, for the commit to date a script
# change from, and the fill-in block's two cross-run reads -- and it was
# inline in the second until 8d needed it too, so it is one function rather
# than the same three lines twice.
prev_run_n () {
  ls runs/run*.md 2>/dev/null | sed 's|.*/run||; s|\.md$||' \
    | awk -v n="${R#run}" '$0 ~ /^[0-9]+$/ && $0+0 < n+0' | sort -n | tail -1
}

# 8c and 8d LAST, and not merely last in the printing: they are the two
# that read every run JSON on disk, so putting them at the end is what
# lets --no-corpus stop short of them, the sweeps run, and --corpus take
# them afterwards. Whichever way, they never share the directory with a
# sweep that is still writing.
if [ "$CORPUS" = 1 ]; then
./properties.py > "$TMP/prop" 2>&1 \
  && say 8c PASS "properties over every run JSON here" \
  || say 8c FAIL "properties: $(grep -m1 FAIL "$TMP/prop")"

# 8d IS WHAT THE EDITS SINCE THE LAST RUN OWE, which is what the pre-run
# list asks for -- `defect-run.py --changed <last run's commit> .`, glossed
# there as *if any script here has changed since the last run* -- and not
# what this ran until 2026-09-13. The bare form replays the WHOLE corpus,
# minutes where the list's is seconds, and the two disagreed in plain sight:
# the PASS line said `every planted defect` beside a list saying `if any
# script here has changed`. Nothing was missed by it, a superset being
# slower rather than weaker; what it cost was a step nobody would run twice.
# THE COMMIT IS THE PREVIOUS RUN'S FILE BEING BORN. `runs/run<N>.md` is
# written at post-run step 5, so the FIRST commit touching it dates the last
# run finishing. NOT the newest such commit: a later session amending that
# file is ordinary -- Run 30's preparation amended run29.md's
# compares-against section the same day -- and dating from it would select
# nothing and pass vacuously, which is worse than slow.
PRN=$(prev_run_n)
PREV_COMMIT=""
[ -n "$PRN" ] && PREV_COMMIT=$(git log --reverse --format=%H \
                                 -- "runs/run$PRN.md" 2>/dev/null | head -1)
if [ -n "$PREV_COMMIT" ]; then
  defect-run.py --changed "$PREV_COMMIT" . > "$TMP/cs" 2>&1 \
    && say 8d PASS "every defect of what changed since run$PRN's file refused again" \
    || say 8d FAIL "defect-run: $(tail -1 "$TMP/cs")"
else
  # NEVER SILENTLY LESS: with no previous run file to date from, the whole
  # corpus runs, which is what this step did unconditionally before. The
  # fallback is the old behaviour kept as the floor, not discarded.
  defect-run.py . > "$TMP/cs" 2>&1 \
    && say 8d PASS "every planted defect refused again (no previous run file to date from)" \
    || say 8d FAIL "defect-run: $(tail -1 "$TMP/cs")"
fi
fi

# --fill-in: THE NOTE'S FILL-IN BLOCK, DERIVED. Every row below is either a
# step this pass has just run, quoted from its own verdict, or a cheap read
# beside it -- so what a preparation pastes into its note is the data the
# verdicts were given on. It exists because that block was transcribed by
# hand until 2026-09-07, and a hand can read the wrong column: Run 27's
# preparation recorded `size -A`'s SECOND field, the load address, as
# `.text`, and then reasoned at length about why it had not moved across a
# roster change. Nothing here can make that mistake twice.
# A row this cannot derive prints `<yours>`; run-status.sh counts those, so
# a row left unwritten is a line of output rather than a reading.
# It is NOT the whole note: the recipes, what the pair measures and the
# handover are a person's, and pair-note-template.txt says so.
fill_in () {
  vd () {  # the DETAIL of a step's verdict, and the verdict word before it
    awk -F'\t' -v s="$1" '$1 == s { v = $2; d = $3 } END {
      if (v == "") print "<yours>"; else print v ": " d }' "$TMP/verdicts"
  }
  # UNDER --corpus ONLY THE SCRIPT-CHECKS ROW EXISTS, 8c and 8d being all
  # that ran, so that row alone is printed rather than a block of thirty
  # `<yours>` around it. It is a REPLACEMENT for the row the earlier pass
  # left owed, which is why it names itself.
  if [ "$REST" = 0 ]; then
    echo
    echo "--- the fill-in row --corpus fills, for $R-pair.txt ---"
    printf '  %-16s %s\n' 'script checks' \
      "8b, and now 8c $(vd 8c); 8d $(vd 8d)"
    echo "--- replaces the 8c/8d line the earlier pass left <yours> ---"
    return 0
  fi
  txt () { size -A "$1" | awk '$1 == ".text" { print $2 }'; }   # FIRST field
  ver () { strings "$1" | grep -oE 'ghc-internal-[0-9.]+' | sort -u \
             | tr '\n' ' ' | sed 's/ *$//'; }
  ins () { printf '%s @@wild, %s @@saturate' \
             "$(strings "$1" | grep -c '@@wild')" \
             "$(strings "$1" | grep -c '@@saturate')"; }
  # The count line is taken WHOLE past its colon rather than by fields: a
  # field slice of it read "184 self-loops of at most" and dropped the "64
  # B" that says what a self-loop is here.
  srv () { ./loop-offsets.py --survey "$1" 2>/dev/null \
             | awk '/self-loops/ && !a { sub(/^[^:]*: */, ""); a = $0 }
                    /at offset 0/{b=$NF} /still straddling/{c=$NF}
                    END{print a", "b" at offset 0, "c" straddling"}'; }
  # The run behind this one, for the two cross-run reads: the highest
  # runs/run<N>.md below this N, and its basis binary if it is still here.
  # Both degrade to a named absence rather than to silence -- an artifact
  # offered for deletion is the normal reason, and a row that just vanished
  # would read as a row nobody owed.
  PN=$(prev_run_n)
  # AND ITS BASIS TAG IS NOT ALWAYS THIS RUN'S. A tag names what a half IS,
  # so a run that changes the variable renames the basis while the recipe
  # stands: Run 29's `spec` is Run 28's `g912` built again, and `run29-spec`
  # is a name Run 28 never wrote. Keyed on this run's tag alone, both reads
  # below went dark on that rename -- the --delta one saying a binary that
  # never existed was not here, the roster-delta one saying nothing at all
  # (2026-09-11). So fall back to the previous run's own note, which is
  # where every other script reads a half's name. BASIS and OTHER are unset
  # for the call: pair-halves.sh refuses an environment disagreeing with the
  # note it is asked about, and this one carries THIS run's names.
  PB=""
  if [ -n "$PN" ]; then
    if [ -x "./run$PN-$BASIS" ]; then
      PB="run$PN-$BASIS"
    else
      PPB=$( (unset BASIS OTHER; ./pair-halves.sh "run$PN" 2>/dev/null) \
             | sed -n 's/^BASIS=\([A-Za-z0-9_]*\).*/\1/p')
      [ -n "$PPB" ] && [ -x "./run$PN-$PPB" ] && PB="run$PN-$PPB"
    fi
  fi
  D=$(date +%F)
  echo
  echo "--- the note's fill-in block, derived; paste into $R-pair.txt ---"
  printf 'Verified when built, %s:\n' "$D"
  printf '  %-16s %s\n' 'Main.hs at' \
    "$(git log -1 --format=%h -- :/micro-regime3/Main.hs), tree $(git status \
       --porcelain -- :/micro-regime3/Main.hs | grep -q . && echo DIRTY \
       || echo clean) against it"
  printf '  %-16s %s\n' 'shim at' \
    "$(git log -1 --format=%h -- :/micro-regime3/align-as.py), tree $(git status \
       --porcelain -- :/micro-regime3/align-as.py | grep -q . && echo DIRTY \
       || echo clean) against it"
  printf '  %-16s %s\n' 'compilers' \
    "on PATH $(ghc --numeric-version 2>/dev/null); in the binaries, \
$BASIS $(ver "./$R-$BASIS") and $OTHER $(ver "./$R-$OTHER")"
  printf '  %-16s %s\n' 'baked RTS' \
    "$("./$R-$BASIS" +RTS --info 2>/dev/null | sed -n 's/.*"Flag -with-rtsopts", "\(.*\)").*/\1/p'), \
and $OTHER $("./$R-$OTHER" +RTS --info 2>/dev/null \
             | sed -n 's/.*"Flag -with-rtsopts", "\(.*\)").*/\1/p')"
  printf '  %-16s %s\n' 'instruments' \
    "$BASIS $(ins "./$R-$BASIS"); $OTHER $(ins "./$R-$OTHER")"
  printf '  %-16s %s\n' '.text' \
    "$(txt "./$R-$BASIS") bytes on $BASIS, $(txt "./$R-$OTHER") on $OTHER \
-- the FIRST column of size -A, the second being the load address"
  printf '  %-16s %s\n' "md5 $BASIS" "$(md5sum "./$R-$BASIS" | cut -d' ' -f1)"
  printf '  %-16s %s\n' "md5 $OTHER" "$(md5sum "./$R-$OTHER" | cut -d' ' -f1)"
  printf '  %-16s %s\n' 'repetition' '<yours> -- available only where the'
  printf '  %-16s %s\n' '' 'source did not move; say which and why'
  printf '  %-16s %s\n' 'fills' "$(vd 10)"
  if [ -n "$PB" ]; then
    printf '  %-16s %s\n' '' "against $PB, the previous build of this recipe:"
    ./loop-offsets.py --delta "$PB" "./$R-$BASIS" 2>/dev/null \
      | grep -E '^ +(every mod-64|NO address|[0-9]+ displacement|of the)' \
      | sed 's/^ */                   /'
  elif [ -n "$PN" ]; then
    printf '  %-16s %s\n' '' "no basis half of run$PN is here -- neither \
run$PN-$BASIS nor the half run$PN-pair.txt names -- so the --delta reading \
against the previous build of this recipe is not available"
  else
    # Named apart from the missing-binary case: with no earlier run file
    # at all there is no name to miss, and the branch above would have
    # spelled one out of an empty number as `run-$BASIS`.
    printf '  %-16s %s\n' '' "no run file below $R in runs/, so there is no \
previous build of this recipe to read --delta against"
  fi
  printf '  %-16s %s\n' 'straddle' "$BASIS $(srv "./$R-$BASIS")"
  printf '  %-16s %s\n' '' "$OTHER $(srv "./$R-$OTHER")"
  printf '  %-16s %s\n' 'regime' "$(vd 9)"
  printf '  %-16s %s\n' 'check' "$(vd '4,5')"
  printf '  %-16s %s\n' '--list' "$(vd 6)"
  if [ -n "$PB" ]; then
    # The membership lines by what they SAY, not by line number: a slice of
    # the first three printed the arms that left and not the ones that
    # landed, which is the half a roster block is written from.
    ./roster-delta.py "$PB" "./$R-$BASIS" 2>/dev/null \
      | grep -E '^ +(main set:|out |in |[0-9]+ survivor)' \
      | sed 's/^ */                   /'
  else
    # A named absence, as the comment at PB promises and as the --delta
    # branch above has always given: silence here read as a roster nobody
    # owed a delta for, on the one run where the delta was the point.
    printf '  %-16s %s\n' '' "no previous basis half here, so the membership \
delta is step 6c's to take by hand"
  fi
  printf '  %-16s %s\n' 'smoke sweep' '<yours> -- step 11, and it is the pair'\''s'
  printf '  %-16s %s\n' 'L1 ROSTER PASS:' '<yours> -- step 12: taken or not owed,'
  printf '  %-16s %s\n' '' 'on which roster, and WHAT IT FOUND'
  printf '  %-16s %s\n' 'document checks' "7 $(vd 7); 8 $(vd 8)"
  printf '  %-16s %s\n' 'script checks' "8b $(vd 8b)"
  if [ "$CORPUS" = 1 ]; then
    printf '  %-16s %s\n' '' "8c $(vd 8c); 8d $(vd 8d)"
  else
    printf '  %-16s %s\n' '' '8c and 8d <yours> -- --corpus takes them'
  fi
  printf '  %-16s %s\n' 'scripts set' \
    'NOTHING TO SET: the halves come from the HALVES line'
  printf '  %-16s %s\n' 'gate arms' "$(vd 6b)"
  echo "--- end of the derived block ---"
}

echo
if [ "$BAD" -eq 0 ]; then
  echo "all clear. NOT done here: 9b, the pair's own variable, which only"
  echo "$R-pair.txt can name; and 11 and 12, the smoke sweep and the roster"
  # `inherits` was asserted of 11 and 12 unconditionally, which is right for
  # a session RE-ENTERING a spent preparation and wrong for the first pass,
  # where neither has run and both are owed. The note is what says which,
  # and this script does not read it for that -- so it names the note
  # rather than guessing. Reworded 2026-09-04 after a first pass read
  # `a spent preparation inherits` over two steps that had not happened.
  echo "pass, which are the note's: OWED where its fill-in block does not"
  echo "record them, INHERITED where it does. Then the run list, from 13."
  [ "$CORPUS" = 1 ] || echo "  8c and 8d did NOT run: --corpus takes them" \
                            "once 11 and 12 have landed."
  [ "$REST" = 1 ] || echo "  ONLY 8c and 8d ran; this is no preflight."
else
  echo "$BAD step(s) FAILED -- read them before anything that costs an evening."
fi
# The block prints on a FAILING pass too, and deliberately: a pass that
# fails 4,5 still read nine other steps, and the rows they gave are what a
# preparation is about to re-derive by hand while it fixes the tenth. The
# rows quote their own verdicts, so a FAIL is carried into the block rather
# than hidden by it.
[ "$FILLIN" = 1 ] && fill_in
exit $((BAD > 0))
