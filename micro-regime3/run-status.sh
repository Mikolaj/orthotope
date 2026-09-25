#!/usr/bin/env bash
# Which steps of the run chapter's three lists are done, read off the
# artifacts and the repository and never off a session's memory.
#
#     ./run-status.sh run24
#
# One line per step it can see -- `done`, `NOT DONE` or `yours` for a step
# no artifact records -- and a last line, `STATUS: all done` or `STATUS: N
# step(s) not done, first: ...`, which is also the exit status: 0 when
# every checkable step is done, 1 otherwise, 2 when this could not run.
# A session is finished with a run when this says all done and the
# `yours` lines have been done by hand; before that it is not, whatever
# it has to report. The chapter's own steps are what judged doneness
# until 2026-09-02, from inside, which is where a session stops at a
# reporting boundary and calls the remainder out of scope.
#
# What each verdict rests on is said on its line, so a `done` can be
# checked and a `NOT DONE` says what is missing. Where the JSONs are gone
# the run stages read what landed in the documents instead, and say so.
# The two document gates are RUN here, seconds each, rather than inferred.
#
# Non-vacuity, re-aimed 2026-09-18: on run35, written up and committed
# with its artifacts on disk, every checkable step reads done and it
# exits 0; on a run name with no artifact at all every artifact-reading
# step reads NOT DONE and it exits 1, the two document gates alone
# reading done, being about the tree and not the run (the case
# `status-reads-an-unstarted-run`); and with the run file's `What this
# run was built to answer` heading edited out, step 5 reads NOT DONE
# naming the heading, and 7 with it, --check-doc finding the anchor
# dead. Re-aim the first whenever run35's artifacts are offered for
# deletion: a finished run whose note and twins are gone reads steps 0,
# 2 and 14 NOT DONE, and any step born after it, so it is no control --
# run23 read four such on 2026-09-18, which this comment had named as
# reading all done.
#
# Step 2c is proved in defects.py and mutants.py rather than here, which
# is where a proof outlives the code it is about: the two directions are
# `status-counts-the-slots-a-note-still-owes` and
# `status-clears-2c-when-the-slots-are-written`, and the break that says
# they bite is `run-status counts a marker inside a comment`.
set -u
cd "$(dirname "$0")" || exit 1
if [ $# -ne 1 ]; then
  echo "usage: ./run-status.sh RUN     # e.g. run24"
  exit 2
fi
R=$1
N=${R#run}
case $N in ''|*[!0-9]*) echo "RUN is run<N>, not '$R'"; exit 2 ;; esac
DOC="runs/$R.md"
NOTE="$R-pair.txt"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/run-status.XXXXXX") || exit 2
trap 'rm -rf "$TMP"' EXIT

MISSING=0; FIRST=; PHASE=pre; FIRSTPHASE=
say () {  # say STEP VERDICT WHAT-IT-RESTS-ON
  printf '  %-5s %-8s %s\n' "$1" "$2" "$3"
  if [ "$2" = "NOT DONE" ]; then
    MISSING=$((MISSING + 1)); : "${FIRST:=$1}"
    # AND WHICH LIST IT BELONGS TO, which the step label cannot say: the
    # pre-run list numbers 0 to 12c and the post-run list 0 to 11, so a
    # bare `7` is in both. The phase is what the caller already knows.
    : "${FIRSTPHASE:=$PHASE}"
  fi
}
parses () { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }

echo "run status for $R, off the artifacts and the repository:"
# THE ENTRY POINT, PRINTED WHERE A SESSION ALREADY IS. This is the first
# command a run's session runs, so it is the one place that can hand over
# the list before README is opened -- and opening README is the failure
# the chapter's own head block has now failed to stop four preparations
# it records: Runs 24, 26, 27 and 28, each arriving with a section
# anchor and reading the framing to find it. Not consecutive -- the
# chapter records nothing of Run 25's arrival either way. A line here costs nothing and
# reaches a session that never meant to read the chapter at all.
echo "  execute from \`./read-run.py --checklist pre\`, or run or post"
echo "  for the other halves; do not read README's run chapter to find it"
echo "  it prints each step through its why: line; --full adds the reasons"
echo "pre-run"
# STEP 1 FIRST, since it is the one step whose answer is a listing rather
# than a verdict: nothing named for this run may exist yet, and `ls $R-*`
# saying `No such file` is what a run about to be prepared looks like. The
# checklist made a session run that `ls` and read it by eye, one call and a
# rule to remember, where this line already had the directory open. What it
# must NOT do is judge: a leftover is a thing to clear and a spent
# preparation is a thing to enter, and which of the two it is comes from
# the steps below, not from the count.
FOUND=$(ls -d "$R"-* 2>/dev/null | wc -l)
if [ "$FOUND" -eq 0 ]; then
  say 1 "done" "nothing named $R-* here, which is a run about to be prepared"
else
  say 1 "see" "$FOUND file(s) named $R-* already: a preparation under way, or\
 leftovers to clear -- the steps below say which"
fi
# A reader has no authority over the halves: an inherited BASIS or OTHER
# that disagreed with the note would survive the helper's refusal and
# every later step would be judged against the wrong name.
unset BASIS OTHER
if [ -f "$NOTE" ]; then
  say 2 "done" "$NOTE exists"
  HALVES=$(./pair-halves.sh "$R" 2>"$TMP/h") && eval "$HALVES"
  if [ -n "${BASIS:-}" ]; then
    say 2b "done" "HALVES line: basis=$BASIS other=$OTHER"
  else
    say 2b "NOT DONE" "$(head -1 "$TMP/h")"
  fi
  for l in LAUNCH RIDERS; do
    grep -q "^$l:" "$NOTE" && say 2b "done" "$l line present" \
      || say 2b "NOT DONE" "no $l: line in $NOTE (run-evening.sh reads it)"
  done
  grep -q "^VARIABLE-CHECK:" "$NOTE" && say 2b "done" \
    "VARIABLE-CHECK line present" \
    || say 2b "NOT DONE" "no VARIABLE-CHECK: line in $NOTE (preflight's 9b \
runs it)"
  # 2c. THE FILL-IN BLOCK'S OWED ROWS, which nothing read until 2026-09-07:
  # every other step here judges an ARTIFACT, and that block is the one
  # product of this half no artifact records, so a row left unwritten was
  # invisible until somebody re-read the note. `preflight.sh --fill-in`
  # prints `<yours>` for each row it cannot derive and the template carries
  # the same marker, so the count of them is the count of rows the half
  # still owes -- a line of output rather than a reading.
  # NUMBERED 2c AND NOT 3: every line this script prints names a step of
  # the chapter's own lists, and the pre-run list's 3 is a retired number
  # -- the md5s and the two commits read BACK, rows preflight's fill-in
  # derives, the step being retired 2026-09-25 -- kept unused so no pointer
  # lands on something else. The block is written at step 2, beside 2a and 2b which
  # are the note's other lines.
  # COUNTED AS SLOTS AND NOT AS FILL-IN ROWS, which is what the marker
  # actually marks: --draft writes `<yours>` for every block it will not
  # decide as well as for every fill-in row, so a message naming only the
  # rows would undercount a note whose recipes were still empty -- and
  # those are the slots that matter most.
  # `#` LINES ARE NOT SLOTS. --draft's own header explains the marker and
  # so contains it twice, and a session redirects that header into the
  # note; counting those would have reported two owed slots on a note with
  # none. The same skip covers the template scaffolding a draft leaves
  # under each block, which quotes the marker for the same reason.
  SLOTS=$(grep -v '^[[:space:]]*#' "$NOTE" | grep -F '<yours>' || true)
  OWED=$(printf '%s' "$SLOTS" | grep -c . || true)
  if [ "$OWED" = 0 ]; then
    say 2c "done" "no <yours> slot left in $NOTE"
  else
    # BOTH SHAPES, since both are slots: a fill-in row is indented and
    # unlabelled past its name, a block is a title at column 0 carrying
    # its marker. A lister for the indented shape alone named a subset of
    # what the count counted.
    say 2c "NOT DONE" "$OWED slot(s) still <yours> in $NOTE, fill-in rows \
and undecided blocks alike: \
$(printf '%s\n' "$SLOTS" \
  | sed "s/<yours>.*//; s/\[PAIR'S\]:*//; s/^ *//; s/ *$//" \
  | grep -v '^$' | tr '\n' ';' | sed 's/;$//')"
  fi
else
  say 2 "NOT DONE" "no $NOTE"
fi
BINS=0
for h in ${OTHER:-} ${BASIS:-}; do [ -x "./$R-$h" ] && BINS=$((BINS + 1)); done
if [ -n "${BASIS:-}" ]; then
  if [ "$BINS" = 2 ]; then say 2 "done" "both binaries here"
  elif [ -f "$DOC" ]; then say 2 "done" "binaries gone, but $DOC exists, so they were built"
  else say 2 "NOT DONE" "$BINS of 2 binaries here"; fi
fi
REG_LEAD="What Run $N \(is\|was\) built to answer"   # is: registered; was: moved
REG_HEAD="## What this run was built to answer, and what it answered"
# README is read UNWRAPPED, a lead spanning a line break matching nothing
# in the wrapped form the tree keeps -- and a wrap80 that cannot run is
# exit 2, the reading not having happened: with its status dropped, steps
# 10, 12a and 12c were judged off an empty file. Case:
# `status-blocks-without-wrap80`.
command -v wrap80 >/dev/null || { echo "BLOCKED: wrap80 is not on PATH, and README.md is read through it; nothing below was judged"; exit 2; }
if ! wrap80 --unwrap README.md > "$TMP/readme"; then
  echo "BLOCKED: wrap80 --unwrap README.md failed, so nothing below was judged"; exit 2
fi
git show HEAD:micro-regime3/README.md > "$TMP/readme.head.wrapped" 2>/dev/null
if ! wrap80 --unwrap "$TMP/readme.head.wrapped" > "$TMP/readme.head"; then
  echo "BLOCKED: wrap80 --unwrap failed on HEAD's README.md, so nothing below was judged"; exit 2
fi
if grep -q "$REG_LEAD" "$TMP/readme" || { [ -f "$DOC" ] && grep -q "^$REG_HEAD" "$DOC"; }; then
  say 12a "done" "a registration for Run $N is in README's open list or in $DOC"
else
  say 12a "NOT DONE" "no '$REG_LEAD' in README.md and no registration section in $DOC"
fi
if grep -q "$REG_LEAD" "$TMP/readme.head" \
   || { [ -f "$DOC" ] && git show "HEAD:micro-regime3/$DOC" 2>/dev/null | grep -q "^$REG_HEAD"; }; then
  say 12c "done" "the registration is committed"
else
  say 12c "NOT DONE" "the registration is not in HEAD"
fi

PHASE=run
echo "run"
if [ -f "$NOTE" ] && grep '^GATE: run' "$NOTE" | tail -1 | grep -q 'Mechanically clean'; then
  say 14 "done" "$NOTE's newest GATE block is mechanically clean"
elif [ -n "${BASIS:-}" ] && parses "$R-gate-$BASIS-a.json" && parses "$R-gate-$BASIS-b.json" \
     && parses "$R-gate-$OTHER-a.json" && parses "$R-gate-$OTHER-b.json"; then
  say 14 "done" "four gate JSONs parse (the note does not record it clean; read run-gate.sh's block)"
else
  say 14 "NOT DONE" "no clean GATE block in $NOTE and no complete set of gate JSONs"
fi
# The verdict is a person's to write and this cannot judge it, but it
# can see that one was written: `GATE VERDICT` opens the hand-written block
# Runs 39 and 40 put above the GATE block, which `yours` read past.
if [ -f "$NOTE" ] && grep -q '^GATE VERDICT' "$NOTE"; then
  say 14a "done" "$NOTE carries a GATE VERDICT line above its GATE block"
else
  say 14a yours "the gate's verdict above the note's GATE block is written by hand, opening \`GATE VERDICT\`; read $NOTE"
fi
if [ -f "$R-wallclock.log" ] && grep -q 'major run complete' "$R-wallclock.log"; then
  # The driver's own stamp, as read-all.sh counts it: the note it quotes
  # is indented, and a FAILED GATE block carries `!!`. Case:
  # `status-counts-only-stamped-complaints`.
  C=$(grep -c '^=== .*!!' "$R-wallclock.log")
  if [ "$C" = 0 ]; then say 17 "done" "$R-wallclock.log says complete, no complaint"
  else say 17 "NOT DONE" "$R-wallclock.log says complete with $C '!!' line(s); read them before any figure"; fi
  if [ -n "${BASIS:-}" ]; then
    GOT=0; WANT=0
    for f in "$R-$BASIS"-*.json "$R-$OTHER"-*.json; do
      case $f in *-gate-*|*-al-*|*'*'*) continue ;; esac
      WANT=$((WANT + 1)); parses "$f" && GOT=$((GOT + 1))
    done
    [ "$GOT" = "$WANT" ] && [ "$GOT" -gt 0 ] \
      && say 17 "done" "$GOT process JSON(s) parse" \
      || say 17 "NOT DONE" "$GOT of $WANT process JSONs parse"
  fi
elif [ -f "$DOC" ] && grep -q '^## Results' "$DOC"; then
  say 17 "done" "no wallclock log here, but $DOC has a Results section, so the sequence landed"
else
  say 17 "NOT DONE" "no 'major run complete' in $R-wallclock.log"
fi
if [ -n "${BASIS:-}" ] && [ -f "$NOTE" ]; then
  RIDERS=$(grep -m1 '^RIDERS:' "$NOTE" | cut -d: -f2)
  case " $RIDERS " in *" none "*) say 19 "done" "RIDERS: none" ;; *)
    for h in $OTHER $BASIS; do
      for s in '' sat; do
        case $s in sat) case " $RIDERS " in *" sat "*) ;; *) continue ;; esac ;; esac
        L="$R-al-$h${s:+-sat}-driver.log"
        if [ -f "$L" ] && grep -q "^DONE-ALONELEGS-$R-$h\$" "$L"; then
          say 19 "done" "$L ends DONE without complaints"
        elif [ -f "$L" ] && grep -q '^DONE-ALONELEGS' "$L"; then
          say 19 "NOT DONE" "$L ends DONE WITH COMPLAINTS"
        elif [ -f "$DOC" ] && ! [ -x "./$R-$BASIS" ]; then
          say 19 "done" "binaries gone; $L not here to read, $DOC stands for it"
        else
          say 19 "NOT DONE" "no $L with a DONE line"
        fi
      done
    done ;;
  esac
fi
if [ -n "${BASIS:-}" ]; then
  if [ -x "./$R-$BASIS" ]; then
    POPS=$(./"$R-$BASIS" classes --list 2>/dev/null | cut -d- -f1 | awk '!seen[$0]++')
    GOT=0; WANT=0; BAD=
    for c in '' $POPS; do for h in $OTHER $BASIS; do
      WANT=$((WANT + 1)); F="$R-counts-$h${c:+-$c}.txt"
      if [ -f "$F" ] && grep -q '^# end' "$F" && ! grep -q '^!!' "$F"; then GOT=$((GOT + 1))
      else BAD="$BAD $F"; fi
    done; done
    [ "$GOT" = "$WANT" ] && say 20 "done" "$GOT counts file(s), each ended and none refused" \
      || say 20 "NOT DONE" "$GOT of $WANT counts files complete; missing or refused:$BAD"
  elif [ -f "$DOC" ]; then
    say 20 "done" "binaries gone, so the populations cannot be listed; $DOC stands for the counts"
  else
    say 20 "NOT DONE" "no ./$R-$BASIS to list the populations from, and no $DOC"
  fi
fi
if [ -f "$R-evening.txt" ]; then
  # Either of run-counts-all.sh's two closing forms; the complained one is
  # the steps' to read, not undone. Case:
  # `status-reads-a-complained-evening-as-complete`.
  tail -1 "$R-evening.txt" | grep -qE 'EVENING COMPLETE(:| WITH)' && say 14-20 "done" "$R-evening.txt ends COMPLETE" \
    || say 14-20 "NOT DONE" "$R-evening.txt's last line: $(tail -1 "$R-evening.txt" | cut -c1-80)"
fi

PHASE=post
echo "post-run"
# 0 IS THE ONE STEP WHOSE WINDOW CLOSES, and until 2026-09-13 it was the one
# step this file could not prompt: it spends the binaries, so a run that
# reaches step 11 without it cannot go back. The twins are what it leaves,
# one per half, named for the run -- `probe-g3-<half>-run<N>` since Run 27
# and `-r<N>` by the three twin scripts before it, which the first form
# of this glob missed, reading those finished runs NOT DONE for ever.
TWINS=$(ls probe-g3-*-"$R" probe-g3-*-"${R/run/r}" 2>/dev/null | wc -l)
if [ "$TWINS" -ge 2 ]; then
  say 0 "done" "$TWINS -g3 twin(s) here; the fill groups are named off them"
elif [ -f "$DOC" ] || ls "$R"-*.json >/dev/null 2>&1; then
  say 0 "NOT DONE" "no probe-g3-*-$R twins: step 0 names the fill groups off\
 them and SPENDS the binaries, so it cannot be taken after step 11"
fi
if ls "$R"-*.json >/dev/null 2>&1; then
  ./read-all.sh "$R" > "$TMP/ra" 2>&1 && say 1 "done" "read-all.sh gates every process clean" \
    || say 1 "NOT DONE" "read-all.sh: $(tail -1 "$TMP/ra" | cut -c1-90)"
elif [ -f "$DOC" ]; then
  say 1 "done" "no JSONs here to gate; the write-up's floor table stands for it"
else
  say 1 "NOT DONE" "no JSONs here to gate and no $DOC"
fi

if [ -f "$DOC" ]; then
  say 5 "done" "$DOC exists"
  [ -n "$(git log -1 --format=%h -- "$DOC")" ] && say 5 "done" "$DOC is committed" \
    || say 5 "NOT DONE" "$DOC has no commit"
  grep -q "runs/$R.md" README.md && say 5 "done" "README links $DOC" \
    || say 5 "NOT DONE" "README.md never names runs/$R.md"
  grep -q "^$REG_HEAD" "$DOC" && say 5 "done" "the registration is in $DOC's last section" \
    || say 5 "NOT DONE" "no '$REG_HEAD' in $DOC (--move-registration)"
  grep -q '___' "$DOC" && say 5 "NOT DONE" "$DOC still carries a '___' verdict slot" \
    || say 5 "done" "no '___' slot left in $DOC"
  grep -q '\[\[TODO\]\]' "$DOC" && say 6a "NOT DONE" "$DOC carries [[TODO]]" \
    || say 6a "done" "no [[TODO]] in $DOC"
  SUBJ=$(git log --format=%s -- "$DOC" README.md | grep -i "run $N\b\|$R\b")
  # 10c by SUBJECT ALONE, whatever the commit touched: the tail's commit
  # may carry no document edit at all, and a path-filtered log hid Run 39's
  # until a sentence was invented to give it one. The other steps' commits
  # do carry the documents and keep the filter. Case:
  # `status-finds-a-10c-commit-without-a-document`.
  SUBJ10C=$(git log --format=%s | grep -i "run $N\b\|$R\b")
  # 6d's commit carries 6b's and 6c's work, so a subject naming both of
  # those names it too, which is how Run 23 wrote it.
  # The tail after the checker joined them 2026-09-08 as 7b and is 10c
  # since 2026-09-11, having been renumbered to the position its own text
  # always described; it is a step like the others and reads NOT DONE
  # until a subject names it.
  # 10c ACCEPTS ITS OLD NAME, and that is not laziness: the tail was 7b
  # until 2026-09-11, so a run written between those two dates carries a
  # commit saying `step 7b` -- Runs 27 and 28 do -- and would read NOT
  # DONE for ever after --
  # which is this file's own documented hazard, met by its own change.
  # A renumber may not un-do a finished run.
  for s in 6b 6d 7a 10c; do
    S=$SUBJ; [ "$s" = 10c ] && S=$SUBJ10C
    if printf '%s\n' "$S" | grep -qi "\b$s\b" \
       || { [ "$s" = 10c ] && printf '%s\n' "$S" | grep -qi '\b7b\b'; } \
       || { [ "$s" = 6d ] && printf '%s\n' "$SUBJ" | grep -qi '\b6b\b.*\b6c\b'; }; then
      say "$s" "done" "a commit subject names step $s"
    else
      # NAMES THE FORM IT WANTED, because the filter is the RUN first and
      # the step second: a subject reading `step 6d: ...` is invisible
      # here however plainly it names the step, and Run 27 wrote two of
      # those and read NOT DONE over work that was done. A line that says
      # what to write turns the verdict into a fix.
      say "$s" "NOT DONE" \
          "no commit subject carries both the run and step $s -- write \`Run $N step $s: ...\`"
    fi
  done
  grep "$REG_LEAD" "$TMP/readme" | grep -q 'ANSWERED' \
    && say 10 "done" "README's entry for Run $N reads ANSWERED" \
    || say 10 "NOT DONE" "README's open-list entry for Run $N does not read ANSWERED"
else
  say 5 "NOT DONE" "no $DOC"
fi
./read-run.py --lint > "$TMP/lint" 2>&1 && say 8 "done" "--lint passes" \
  || say 8 "NOT DONE" "--lint: $(grep -m1 'FAIL\|BLOCKED' "$TMP/lint" | cut -c1-90)"
./read-run.py --check-doc --quiet > "$TMP/cd" 2>&1 && say 7 "done" "--check-doc --quiet passes" \
  || say 7 "NOT DONE" "--check-doc: $(grep -m1 'FAIL\|BLOCKED' "$TMP/cd" | cut -c1-90)"
say 11 yours "offer the artifacts for deletion, once, after 7 is presented"

echo
if [ "$MISSING" -eq 0 ]; then
  echo "STATUS: all done (the 'yours' lines are done by hand and not read here)"
  exit 0
fi
echo "STATUS: $MISSING step(s) not done, first: $FIRST"
# THE ONE LIST THIS SESSION OWES, and not the three the head offers: the
# head prints before any step has been read and so cannot know which, while
# here the phase of the first NOT DONE step says it outright. Run 38's
# executing session read the 49 KB pre-run list it did not owe, having been
# handed all three names at the top.
case "$FIRSTPHASE" in
  pre)  echo "  you owe \`./read-run.py --checklist pre\` ALONE, and none of the other two" ;;
  run)  echo "  you owe \`./read-run.py --checklist run\`, with \`post-a\` read at step 13a;" 
        echo "  the pre-run list is the preparation's and is spent" ;;
  post) echo "  you owe \`./read-run.py --checklist post-a\`, and \`post-b\` at step 5c;"
        echo "  the pre-run and run lists are spent" ;;
esac
exit 1
