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
# Non-vacuity, 2026-09-02: on run23, written up and committed, every
# checkable step reads done and it exits 0; on a run name with no artifact
# at all every artifact-reading step reads NOT DONE and it exits 1, the
# two document gates alone reading done, being about the tree and not the
# run; and on run23 with the run file's `What this run was built to
# answer` heading edited out, step 5 reads NOT DONE naming the heading,
# and 7 with it, --check-doc finding the anchor dead. Re-aim the first
# two whenever run23's artifacts are offered for deletion.
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

MISSING=0; FIRST=
say () {  # say STEP VERDICT WHAT-IT-RESTS-ON
  printf '  %-5s %-8s %s\n' "$1" "$2" "$3"
  if [ "$2" = "NOT DONE" ]; then
    MISSING=$((MISSING + 1)); : "${FIRST:=$1}"
  fi
}
parses () { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }

echo "run status for $R, off the artifacts and the repository:"
echo "pre-run"
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
command -v wrap80 >/dev/null || { echo "BLOCKED: wrap80 is not on PATH, and README.md is read through it; nothing was judged"; exit 2; }
if ! wrap80 --unwrap README.md > "$TMP/readme"; then
  echo "BLOCKED: wrap80 --unwrap README.md failed, so nothing was judged"; exit 2
fi
git show HEAD:micro-regime3/README.md > "$TMP/readme.head.wrapped" 2>/dev/null
if ! wrap80 --unwrap "$TMP/readme.head.wrapped" > "$TMP/readme.head"; then
  echo "BLOCKED: wrap80 --unwrap failed on HEAD's README.md, so nothing was judged"; exit 2
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

echo "run"
if [ -f "$NOTE" ] && grep '^GATE: run' "$NOTE" | tail -1 | grep -q 'Mechanically clean'; then
  say 14 "done" "$NOTE's newest GATE block is mechanically clean"
elif [ -n "${BASIS:-}" ] && parses "$R-gate-$BASIS-a.json" && parses "$R-gate-$BASIS-b.json" \
     && parses "$R-gate-$OTHER-a.json" && parses "$R-gate-$OTHER-b.json"; then
  say 14 "done" "four gate JSONs parse (the note does not record it clean; read run-gate.sh's block)"
else
  say 14 "NOT DONE" "no clean GATE block in $NOTE and no complete set of gate JSONs"
fi
say 14a yours "the gate's verdict above the note's GATE block is written by hand; read $NOTE"
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
  tail -1 "$R-evening.txt" | grep -q 'EVENING COMPLETE:' && say 14-20 "done" "$R-evening.txt ends COMPLETE" \
    || say 14-20 "NOT DONE" "$R-evening.txt's last line: $(tail -1 "$R-evening.txt" | cut -c1-80)"
fi

echo "post-run"
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
  # 6d's commit carries 6b's and 6c's work, so a subject naming both of
  # those names it too, which is how Run 23 wrote it.
  for s in 6b 6d 7a; do
    if printf '%s\n' "$SUBJ" | grep -qi "\b$s\b" \
       || { [ "$s" = 6d ] && printf '%s\n' "$SUBJ" | grep -qi '\b6b\b.*\b6c\b'; }; then
      say "$s" "done" "a commit subject names step $s"
    else
      say "$s" "NOT DONE" "no commit subject naming Run $N's step $s"
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
exit 1
