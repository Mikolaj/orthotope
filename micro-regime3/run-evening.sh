#!/usr/bin/env bash
# The run list's machine steps as one command: the gate, the busy-box
# alarm, the sequence, the alone-leg riders and the counted work, in the
# order the list gives them and under the environment the pair note
# names, each stage's verdict appended to `$R-evening.txt` as it lands.
#
#     ./run-evening.sh run24 &        # the harness wakes you when it exits
#
# Until 2026-09-02 those were five launch lines an executing session typed
# between waits, each wait a turn end, each line a place to mis-order, to
# drop the environment, or to write a waiter that greps its own command
# line. This runs them; the session starts it in the background and reads
# `$R-evening.txt` when the harness wakes it, and `run-status.sh` reads
# the same file. Nothing here decides anything a person decides: the
# gate's VERDICT is still written into the note by hand (README, step
# 14a), from the two `--compare` readings this puts in `$R-evening-out.txt`.
#
# WHAT IT READS FROM THE NOTE, three machine lines beside the prose that
# explains them (pair-note-template.txt):
#     HALVES: basis=g912 other=spot        via pair-halves.sh
#     LAUNCH: WILDLOG=1 SATURATE=1         or `LAUNCH: none`
#     RIDERS: clean sat                    or `RIDERS: clean`, or `none`
# A note without them is refused before anything runs, naming the line.
#
# WHAT STOPS IT AND WHAT DOES NOT. The gate refusing (exit 1) is the
# apparatus and stops the evening, as README's gate step says; a gate the
# note already records as mechanically clean is not re-run. A busy box at
# the alarm stops it, the sequence being hours. After that nothing stops
# it: run-major.sh's complaints, a rider refused, a counts sweep that
# could not count are each recorded as a complaint and the next stage
# runs, eight sound populations being worth more than a stop -- and the
# last line says COMPLETE or COMPLETE WITH COMPLAINTS, which is also the
# exit status. It refuses to start over a previous attempt's
# `$R-evening.txt`, as run-major.sh refuses over a previous attempt's
# JSONs: the stages' own guards then say what an earlier attempt left.
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

if [ $# -ne 1 ]; then
  echo "usage: ./run-evening.sh RUN &     # e.g. run24"
  exit 2
fi
R=$1
NOTE="$R-pair.txt"
STATUS="$R-evening.txt"
OUT="$R-evening-out.txt"

HALVES=$(./pair-halves.sh "$R") || exit 1
eval "$HALVES"

[ -f "$NOTE" ] || { echo "no $NOTE"; exit 1; }
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
if [ -e "$STATUS" ]; then
  echo "$R already has $STATUS, a previous attempt's record:"
  sed 's/^/  /' "$STATUS"
  echo "relaunching would run the stages over its artifacts, which each"
  echo "stage refuses on its own. Move it aside if that attempt is dead."
  exit 1
fi

COMPLAINTS=()
stamp () { echo "=== $(date -Is) $*" | tee -a "$STATUS"; }
# Every stage's own output goes to $OUT whole, and one line of it to the
# status file: the status file is what a session reads, and it must stay
# a screenful.
stage () {   # stage LABEL cmd...   -> the command's status, recorded.
  # PLAIN=1 in front of the call runs the command without the launch
  # environment: the counts want none, an instruction count being what
  # the preamble's dose is counted into and cancelled out of, so under
  # SATURATE every cell would spend two doses for nothing.
  local label=$1; shift
  stamp "$label: start"
  { echo; echo "##### $label"; } >> "$OUT"
  if [ -n "${PLAIN:-}" ]; then "$@" >> "$OUT" 2>&1
  else env "${ENV[@]}" "$@" >> "$OUT" 2>&1; fi
  local rc=$?
  if [ "$rc" = 0 ]; then
    stamp "$label: done, rc=0"
  else
    stamp "$label: done, rc=$rc -- COMPLAINT, read $OUT under '##### $label'"
    COMPLAINTS+=("$label rc=$rc")
  fi
  return "$rc"
}

stamp "evening begins for $R: basis $BASIS, control $OTHER, launch env\
 '${LAUNCH# }', riders '${RIDERS# }'"

# 14. THE GATE, unless the note records it mechanically clean already; a
# note recording a FAILED gate gets it run again, the apparatus having
# presumably been fixed since. Only the exit status stops the evening;
# the machine check inside it does not gate since 2026-08-23.
# The NEWEST GATE block decides, as README's step 13 reads the note: an
# older clean block under a later FAILED one, or from before a rebuild,
# must not inherit.
if grep '^GATE: run' "$NOTE" | tail -1 | grep -q 'Mechanically clean'; then
  stamp "gate: inherited, $NOTE's newest GATE block is mechanically clean"
else
  if ! stage gate ./run-gate.sh "$R"; then
    stamp "EVENING STOPPED AT THE GATE: it is the apparatus, and README's\
 gate step says what to read"
    exit 1
  fi
  # The reading the verdict is written from, both passes, put where the
  # session will find it and not judged here.
  { echo; echo "##### gate reading, -a pair then -b pair (write the verdict"
    echo "##### above the note's GATE block from these)"
    ./read-run.py "$R-gate-$BASIS-a.json" --compare "$R-gate-$OTHER-a.json"
    ./read-run.py "$R-gate-$BASIS-b.json" --compare "$R-gate-$OTHER-b.json"
  } >> "$OUT" 2>&1
  stamp "gate: the two --compare readings are in $OUT; the verdict is yours\
 to write into $NOTE (step 14a)"
fi

# 16. THE ALARM, the reading run-alonelegs.sh takes (machine-busy.sh says
# why /proc/stat and not a loadavg), refused above MAXBUSY percent
# non-idle, default 5.
BUSY=$(./machine-busy.sh) || BUSY=
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

# 17. THE SEQUENCE. Its complaints are not fatal (run-major.sh says why)
# and neither are they here; the exit status carries them out.
stage sequence ./run-major.sh "$R" || true

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

# 20. THE COUNTED WORK, over every population: the main set and then each
# class the basis binary lists, in its order, control then basis apiece.
CLASSES=$(./"$R-$BASIS" classes --list 2>/dev/null | cut -d- -f1 | awk '!seen[$0]++')
for c in '' $CLASSES; do
  for h in $OTHER $BASIS; do
    PLAIN=1 stage "counts $h ${c:-main}" ./run-counts.sh "$R" "$h" $c || true
  done
done

if [ "${#COMPLAINTS[@]}" -eq 0 ]; then
  stamp "EVENING COMPLETE: every stage exited 0. Read $R-wallclock.log's\
 '!!' lines anyway, then the post-run list, its step 0 first"
  exit 0
fi
stamp "EVENING COMPLETE WITH ${#COMPLAINTS[@]} COMPLAINT(S): $(IFS=,; echo "${COMPLAINTS[*]}")\
 -- read each in $OUT before any figure; the post-run list's step 0 is still first"
exit 1
