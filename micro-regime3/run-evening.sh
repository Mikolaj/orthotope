#!/usr/bin/env bash
# The run list's machine steps that want a QUIET BOX, as one command: the
# gate, the busy-box alarm, the sequence and the alone-leg riders, in the
# order the list gives them and with the machine check, which wants none, read
# off the sequence before the riders, under the environment the pair note
# names, each stage's verdict appended to `$R-evening.txt` as it lands.
#
#     ./run-evening.sh run24          # both in the background, and what
#     ./run-counts-all.sh run24       # that means for a SESSION rather
#                                     # than a person is README's run list
#                                     # step 14, which carries the
#                                     # measurement. Then step
#                                     # 20, on a box back in use
#
# THE COUNTED WORK IS NOT HERE, and this file's last line is what that
# buys: the machine is its owner's again the moment the riders land, and
# the session is woken there to say so (README, run list step 19a).
#
# The session starts it in the background and reads `$R-evening.txt` when
# the harness wakes it, and `run-status.sh` reads the same file. Nothing
# here decides anything a person decides, and the gate owes no verdict: its
# four readings go to `$R-evening-out.txt` for the write-up to quote, as the
# machine check's does.
#
# WHAT IT READS FROM THE NOTE, three machine lines beside the prose that
# explains them (pair-note-template.txt), and its COMPARE line for the
# machine check:
#     HALVES: basis=g912 other=spot        via pair-halves.sh
#     LAUNCH: WILDLOG=1 SATURATE=1         or `LAUNCH: none`
#     RIDERS: clean sat                    or `RIDERS: clean`, or `none`
# A note without them is refused before anything runs, naming the line.
# So is a launch under the harness without the reaper switch, exit 2, the
# check below saying why, and a COMPARE naming a run with no file.
#
# WHAT STOPS IT AND WHAT DOES NOT. The gate refusing (exit 1) is the apparatus
# and stops the evening; a gate the note already records as mechanically
# clean is not re-run. A busy box at the alarm stops it, the sequence being
# hours. After that nothing stops it: a half the instance gate could not test,
# run-major.sh's complaints, a machine check that could not compare and a
# refused rider are each recorded as a complaint and the next stage runs, a
# sound sequence being worth more than a stop -- and the last line hands the
# machine back, with the complaint count where there is one, which is also the
# exit status. It refuses to start over a previous attempt's `$R-evening.txt`,
# as run-major.sh refuses over a previous attempt's JSONs: the stages' own
# guards then say what an earlier attempt left.
#
# ARTIFACT NAMES: `$R-evening.txt` and `$R-evening-out.txt`, both `.txt`
# so that neither is a `$R-*.log` for run-major.sh's relaunch guard or
# read-all.sh's plateau glob to read as a process.
#
# Driven by the cases in defects.py against stand-ins, the whole evening in
# seconds (`evening-chains-the-stages`, and the refusals beside it). A
# fix here wants a case there first.
set -u
cd "$(dirname "$0")" || exit 1

# `--from STAGE` resumes a dead attempt at gate, alarm, instance, sequence,
# machine or riders: it wants that attempt's status file, appends to it under a
# `resumed` line, and runs the named stage and every one after it -- the
# sequence only where no process of it started, the stray check refusing
# any $R-*.json or $R-*.log. Cases:
# `evening-resumes-from-a-named-stage`, `evening-refuses-to-resume-nothing`.
FROM=gate
if [ $# -eq 3 ] && [ "$2" = --from ]; then
  FROM=$3
elif [ $# -ne 1 ]; then
  FROM=usage
fi
case $FROM in
  gate|alarm|instance|sequence|machine|riders) ;;
  *)
  echo "usage: ./run-evening.sh RUN [--from gate|alarm|instance|sequence|machine|riders]"
  echo "                                 # e.g. run24, in the background;"
  echo "                                 # README's run list step 14 says"
  echo "                                 # what that means for a session"
  exit 2 ;;
esac
R=$1
ORDER="gate alarm instance sequence machine riders"
rank () { local i=0 s; for s in $ORDER; do i=$((i + 1)); [ "$s" = "$1" ] && echo $i; done; }
at () { [ "$(rank "$1")" -ge "$(rank "$FROM")" ]; }
NOTE="$R-pair.txt"
STATUS="$R-evening.txt"
OUT="$R-evening-out.txt"

# Under the harness a tracked task can be killed on a kernel memory-pressure
# event, which took Run 35's driver two and a half hours in (README, the
# recommended tasks after Run 35); the user settings disable that reaper
# with the variable below, and a session started before the setting lacks
# it. Refused here, before the hours; a plain terminal has no reaper and is
# not asked.
if [ -n "${CLAUDE_CODE_SESSION_ID:-}" ] &&
   [ "${CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP:-}" != 1 ]; then
  echo "under the harness without CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1:"
  echo "   its memory-pressure reaper can kill this evening hours in, as it"
  echo "   did Run 35's. The user settings set it; a session started before"
  echo "   they did lacks it. Start a new session. Nothing ran."
  exit 2
fi

HALVES=$(./pair-halves.sh "$R") || exit 1
eval "$HALVES"

[ -f "$NOTE" ] || { echo "no $NOTE"; exit 1; }
# The machine check after the sequence reads the fingerprint of the run the
# note's COMPARE line names, where it names one, and the newest run file's
# otherwise. A named run with no file would make that check the one thing
# the hours could not answer, so it is refused here, before them. Case:
# `evening-refuses-a-compare-run-with-no-file`.
MDOC=()
if [ -n "${COMPARE:-}" ]; then
  [ -f "runs/$COMPARE.md" ] || { echo "!! $NOTE names COMPARE: $COMPARE, and runs/$COMPARE.md is not there -- the machine check after the sequence would have no fingerprint to read. Nothing ran."; exit 1; }
  MDOC=(--run-doc "runs/$COMPARE.md")
fi
# The two machine lines this file owns, read as pair-halves.sh reads its
# own: present, and of the words allowed. A LAUNCH line is a list of
# NAME=value words or the word `none`; a RIDERS line is `clean`, `clean
# sat` or `none`. Anything else is refused by name, before the hours.
LAUNCH_LINE=$(grep -m1 '^LAUNCH:' "$NOTE")
RIDERS_LINE=$(grep -m1 '^RIDERS:' "$NOTE")
if [ -z "$LAUNCH_LINE" ] || [ -z "$RIDERS_LINE" ]; then
  echo "!! $NOTE lacks a machine line this driver reads:"
  [ -n "$LAUNCH_LINE" ] || echo "   LAUNCH: <NAME=value ...>   or   LAUNCH: none"
  [ -n "$RIDERS_LINE" ] || echo "   RIDERS: clean [sat]        or   RIDERS: none"
  echo "   pair-note-template.txt shows where each goes. Nothing ran."
  exit 1
fi
LAUNCH=${LAUNCH_LINE#LAUNCH:}
RIDERS=${RIDERS_LINE#RIDERS:}
ENV=()
for w in $LAUNCH; do
  case $w in
    none) ;;
    [A-Za-z_]*=*) ENV+=("$w") ;;
    *) echo "!! $NOTE's LAUNCH line carries '$w', which is not NAME=value"
       echo "   and not 'none'. Nothing ran."; exit 1 ;;
  esac
done
SAT=0; CLEAN=0
for w in $RIDERS; do
  case $w in
    clean) CLEAN=1 ;;
    sat) SAT=1 ;;
    none) ;;
    *) echo "!! $NOTE's RIDERS line carries '$w'; the words are clean, sat"
       echo "   and none. Nothing ran."; exit 1 ;;
  esac
done
if [ "$SAT" = 1 ] && [ "$CLEAN" = 0 ]; then
  echo "!! $NOTE's RIDERS line asks for saturated legs and no clean ones;"
  echo "   the decomposition wants both. Nothing ran."; exit 1
fi

for h in $OTHER $BASIS; do
  [ -x "./$R-$h" ] || { echo "missing ./$R-$h -- $NOTE has the recipe"; exit 1; }
done
if [ "$FROM" != gate ] && ! [ -e "$STATUS" ]; then
  echo "--from $FROM: no $STATUS, so there is nothing to resume; run the"
  echo "evening without --from. Nothing ran."
  exit 2
fi
if [ "$FROM" = gate ] && [ -e "$STATUS" ]; then
  echo "$R already has $STATUS, a previous attempt's record:"
  sed 's/^/  /' "$STATUS"
  echo "relaunching would run the stages over its artifacts, which each"
  echo "stage refuses on its own. Move it aside if that attempt is dead, or"
  echo "resume it with --from STAGE."
  exit 1
fi
# AND WHAT THE SEQUENCE'S OWN GUARD WOULD REFUSE OVER, refused here, before
# the gate spends its minutes: run-major.sh refuses any $R-*.json or $R-*.log
# but the gate's and the riders', and it runs third, so a stray file under
# that name would let the gate run, the sequence refuse at once and the riders
# take the quiet box in its place -- a session's own redirect of this driver's
# output among them. The two filters are one rule and are kept alike by hand.
# Case:
# `evening-refuses-a-stray-run-artifact-before-the-gate`.
# shellcheck disable=SC2010  # the names here are the drivers' own
STRAY=$(ls -1 "$R"-*.json "$R"-*.log 2>/dev/null \
          | grep -v -e "^$R-gate-" -e "^$R-al-")
if at sequence && [ -n "$STRAY" ]; then
  echo "!! $R already has files run-major.sh's relaunch guard refuses over,"
  echo "   so the sequence would refuse after the gate had run:"
  printf '%s\n' "$STRAY" | sed 's/^/     /'
  echo "   Move them aside, and send this driver's own output, if anywhere,"
  echo "   to a name not beginning $R-. Nothing ran."
  exit 1
fi

COMPLAINTS=()
stamp () { echo "=== $(date -Is) $*" | tee -a "$STATUS"; }
# Every stage's own output goes to $OUT whole, and one line of it to the
# status file: the status file is what a session reads, and it must stay
# a screenful.
stage () {   # stage LABEL cmd...   -> the command's status, recorded.
  local label=$1; shift
  stamp "$label: start"
  { echo; echo "##### $label"; } >> "$OUT"
  env "${ENV[@]}" "$@" >> "$OUT" 2>&1
  local rc=$?
  if [ "$rc" = 0 ]; then
    stamp "$label: done, rc=0"
  else
    stamp "$label: done, rc=$rc -- COMPLAINT, read $OUT under '##### $label'"
    COMPLAINTS+=("$label rc=$rc")
  fi
  return "$rc"
}

if [ "$FROM" = gate ]; then
  stamp "evening begins for $R: basis $BASIS, control $OTHER, launch env\
 '${LAUNCH# }', riders '${RIDERS# }'"
else
  stamp "evening resumed for $R from $FROM: basis $BASIS, control $OTHER,\
 launch env '${LAUNCH# }', riders '${RIDERS# }'"
fi

# 14. THE GATE, unless the note records it mechanically clean already FOR
# THESE BINARIES; a note recording a FAILED gate gets it run again, the
# apparatus having presumably been fixed since. Only the exit status stops
# the evening; the machine check left the gate on 2026-10-05 and is stage
# 17a below.
# The NEWEST GATE block decides, as README's step 13 reads the note, and it
# names the pair it gated by md5 (run-gate.sh's `halves md5:` line, since
# 2026-09-04): an older clean block under a later FAILED one does not
# inherit, and neither does a clean one naming other binaries, which is
# what a block from before a rebuild is -- by its text alone it inherited,
# and the evening would have run hours on a pair nobody gated. A block
# without the line cannot be tied to anything and runs the gate too. Cases:
# `evening-does-not-inherit-a-gate-of-other-binaries` and its untied sibling.
BLOCK=$(awk '/^GATE: run/ { out = $0; blk = 1; next }
             blk && /^[ \t]/ { out = out "\n" $0; next }
             { blk = 0 }
             END { print out }' "$NOTE")
HALVES_MD5="$BASIS=$(md5sum "./$R-$BASIS" | cut -d' ' -f1) $OTHER=$(md5sum "./$R-$OTHER" | cut -d' ' -f1)"
INHERIT=0
at gate || INHERIT=2
if [ "$INHERIT" = 0 ] && printf '%s\n' "$BLOCK" | head -1 | grep -q 'Mechanically clean'; then
  if printf '%s\n' "$BLOCK" | grep -qF "halves md5: $HALVES_MD5"; then
    INHERIT=1
  elif printf '%s\n' "$BLOCK" | grep -q 'halves md5:'; then
    stamp "gate: NOT inherited: $NOTE's newest clean GATE block names other\
 binaries by md5, so it is from before a rebuild; the gate runs again"
  else
    stamp "gate: NOT inherited: $NOTE's newest clean GATE block has no\
 'halves md5:' line (run-gate.sh writes one since 2026-09-04), so it cannot\
 be tied to these binaries; the gate runs again"
  fi
fi
if [ "$INHERIT" = 2 ]; then
  :
elif [ "$INHERIT" = 1 ]; then
  stamp "gate: inherited, $NOTE's newest GATE block is mechanically clean\
 and names these two binaries"
else
  if ! stage gate ./run-gate.sh "$R"; then
    stamp "EVENING STOPPED AT THE GATE: it is the apparatus, and README's\
 gate step says what to read"
    exit 1
  fi
  # The gate's reading, both passes, put where the write-up will find it
  # and not judged here.
  { echo; echo "##### gate reading, -a pair then -b pair"
    ./read-run.py "$R-gate-$BASIS-a.json" --compare "$R-gate-$OTHER-a.json"
    ./read-run.py "$R-gate-$BASIS-b.json" --compare "$R-gate-$OTHER-b.json"
    # AND EACH HALF AGAINST ITSELF, which is what says whether a spread
    # between the two passes above is the PAIR disagreeing or one half
    # moving between its own two legs, the passes' ratio being those two
    # divided. They cost what the two above cost and run in the same
    # window, after the gate's last process has exited.
    # why: --para 'If that line says the gate has not run'
    echo; echo "##### each half against ITSELF, -a over -b: what a spread"
    echo "##### between the two passes above is, before it is the pair's"
    ./read-run.py "$R-gate-$BASIS-a.json" --compare "$R-gate-$BASIS-b.json"
    ./read-run.py "$R-gate-$OTHER-a.json" --compare "$R-gate-$OTHER-b.json"
    # THE FOUR AS ONE TABLE, which the write-up's Provenance quotes: per
    # arm both passes and both halves' own legs, and each half's widest own
    # drift, saving the transcription.
    echo; echo "##### the four readings per arm as one table (read-run.py"
    echo "##### --gate-draft), for the write-up"
    ./read-run.py --gate-draft "$R"
  } >> "$OUT" 2>&1
  stamp "gate: the four --compare readings and their table are in $OUT,\
 for the write-up and NOT for now: the sequence starts two seconds after this\
 line and README's run list step 17 wants nothing else on the machine until\
 it ends"
fi

# 16. THE ALARM, the reading run-alonelegs.sh takes (machine-busy.sh says
# why /proc/stat and not a loadavg), refused above MAXBUSY percent
# non-idle, default 5.
# Before the sequence and not before the riders alone, which take the same
# reading themselves.
if at sequence; then
BUSY=$(../../horde-ad/tools/machine-busy.sh) || BUSY=
# An unreadable figure refuses: awk compares an empty string to the bar
# and lets it through, which is the one direction this alarm must not fail.
case $BUSY in ''|*[!0-9.]*) BUSY=100.0 ;; esac
if awk -v x="$BUSY" -v m="${MAXBUSY:-5}" 'BEGIN{exit !(x>m)}'; then
  stamp "EVENING STOPPED AT THE ALARM: ${BUSY}% of the CPUs non-idle over\
 two seconds, against a ${MAXBUSY:-5}% bar. The sequence is hours and it\
 would time the intruder; set MAXBUSY to say what you accept, or wait"
  exit 1
fi
stamp "alarm: ${BUSY}% busy, under the ${MAXBUSY:-5}% bar"
fi

# 16a. THE INSTANCE GATE, since 2026-09-18: each half's launch instance
# against a fresh copy on one cell, the copy swapped in when the launch
# instance is the slow draw -- instance-gate.sh says how, and README's
# placement section why. After the alarm because it times, before the
# sequence because the sequence is what it protects. Its processes are not
# the run's, so WILDLOG is stripped as the clean riders strip SATURATE. A
# half it cannot test is a complaint and not a stop.
at instance && { stage "instance gate" env -u WILDLOG ./instance-gate.sh "$R" || true; }

# 17. THE SEQUENCE. Its complaints are not fatal (run-major.sh says why)
# and neither are they here; the exit status carries them out.
at sequence && { stage sequence ./run-major.sh "$R" || true; }

# 17a. THE MACHINE CHECK: `list`'s net against the fingerprint the COMPARE
# run's file, or the newest run file, keeps, read on the basis half's
# main-set JSON, which carries `*/list` and both `sum-only` halves on every
# shape. After the sequence because that JSON is the first that can answer
# it, and it stops nothing. Its reading goes to $OUT, where read-all.sh's
# brief takes it, and one line of it to the status file. Case:
# `evening-takes-the-machine-check-off-the-main-set`.
# why: --para 'If that line says the gate has not run'
if at machine; then
  stage machine ./read-run.py "$R-$BASIS-main.json" --machine "${MDOC[@]}" \
    || true
  # The newest machine section's figures, a resumed evening carrying more
  # than one.
  MC=$(awk '/^##### / { sec = $0 } sec == "##### machine" && /^ *geomean / {
              sub(/^ */, ""); line = $0 } END { print line }' "$OUT")
  if awk '/^##### / { sec = $0 } sec == "##### machine" && /BOX MOVED/ {
            hit = 1 } END { exit !hit }' "$OUT"; then
    stamp "machine: $MC -- BOX MOVED: read it against the fingerprint half's\
 previous build before believing it; the run goes on, and the write-up names it"
  elif [ -n "$MC" ]; then
    stamp "machine: $MC, inside the bar"
  fi
fi

# 19. THE RIDERS, control first, clean before saturated, as the note's own
# block spells them; `SAT=` is the rider's spelling of SATURATE=. A CLEAN
# leg runs with SATURATE and SATURATE_BY unset whatever the LAUNCH line
# carries: the pair's launch switches include SATURATE on a pair with the
# preamble, and passed through they would dose the clean legs too, named
# clean and complained about by nothing (found by review, 2026-09-02).
if [ "$CLEAN" = 1 ]; then
  for h in $OTHER $BASIS; do
    stage "riders $h clean" env -u SATURATE -u SATURATE_BY \
      ./run-alonelegs.sh "$R" "$h" || true
    if [ "$SAT" = 1 ]; then
      stage "riders $h sat" env SAT=1 ./run-alonelegs.sh "$R" "$h" || true
    fi
  done
else
  stamp "riders: none, as $NOTE says"
fi

# 19a. AND THE MACHINE IS FREE, which is the last thing this says because
# it is the first thing the woken session owes: the counted work is
# insensitive to load, so it is a call of its own and the box goes back to
# its owner here rather than an hour later.
if [ "${#COMPLAINTS[@]}" -eq 0 ]; then
  stamp "RIDERS DONE AND THE MACHINE IS FREE: every stage exited 0. Read\
 $R-wallclock.log's '!!' lines anyway, say the box need not be quiet any\
 more -- a probe that wants it quiet again is asked for from here, README\
 19a -- and launch the counted work in the same turn, backgrounded as this\
 was: ./run-counts-all.sh $R"
  exit 0
fi
stamp "RIDERS DONE AND THE MACHINE IS FREE, WITH ${#COMPLAINTS[@]}\
 COMPLAINT(S): $(IFS=,; echo "${COMPLAINTS[*]}") -- read each in $OUT before\
 any figure; the counted work is still next: ./run-counts-all.sh $R"
exit 1
