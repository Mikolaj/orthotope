#!/usr/bin/env bash
# A major run, paired: both halves take the main set and both take every
# class (README, the run's plan). 18 processes, unattended, several hours.
#
#     ./run-major.sh run10          # the argument names every artifact
#
# Nothing here builds. The pair comes from the recipe in its own note and
# must not be rebuilt between the halves, which is what the pairing
# measures; this refuses to start without both binaries.
#
# What it adds over pasting the sequence is the counting: every process's
# bench count is checked against what the roster actually holds, so a
# selection that silently caught the wrong set is loud at once rather than at
# the write-up. The expected count is READ FROM THE BINARY rather than
# written down -- a literal would be wrong for the next roster, and this one
# moved twice on 2026-08-14, which would have made a correct run trip the
# alarm on every process. A class process gets the same treatment as a main one: its
# count is its prefix's share of `classes --list`, and a prefix matching
# nothing is reported rather than passing as a run of zero benches. The
# reverse -- a class the BINARY has that CLASSES does not name -- is
# refused before the run, and the complaints ride out in the exit status.

# Driven by ./check-scripts.py without binaries or hours: all eighteen
# processes against stand-ins that hand back a previous run's real cells.
# A fix here wants a case there first.

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./run-major.sh RUN      # e.g. run10, and it names every artifact"
  echo "the prefix is the run's identity, so there is no default to fall back on:"
  echo "artifacts called run-* would not say which run made them, and the next"
  echo "run would overwrite them."
  exit 2
fi
R=$1
PREFIX="$R"                  # the binaries and their note carry the run, as
                             # every artifact here does, so that two runs
                             # cannot write one filename however alike their
                             # half names are -- see run-gate.sh, whose output
                             # did not and quietly overwrote Run 10's. One
                             # scheme throughout: `<run>-<rest>`, binaries,
                             # note and JSONs alike

# WHICH TWO HALVES, since the pair is no longer always unaligned/aligned.
# BASIS is the half the expected bench counts are read from and every
# --in-place table comes from; the other contributes the --compare and a
# yardstick column, and THE BASIS runs SECOND, which is where it ran in Run
# 10, so a run repeating that one inherits its process position. It does
# not inherit the binary: reusing a previous basis binary was refused on
# 2026-08-16 and every pair is built here, both halves back to back. Both halves run every class, which they did not before
# 2026-08-14 -- the loop below says what changed and why. Change these two names per pair -- and
# nothing else here, the counting below being what makes a wrong selection
# loud in the log rather than at the write-up.
OTHER=${OTHER:-a32m}
BASIS=${BASIS:-lookrts}
HALVES="$OTHER $BASIS"
# A pair is two halves, and nothing downstream can tell that it is not. With
# the two names equal, every second process writes the JSON the one before it
# just wrote: nine files take eighteen processes' worth of the evening, the
# bench counting passes because each process really did run its count,
# read-all.sh matches nine started names against nine JSONs and gates clean,
# and the reader is then handed a file to --compare with itself. Two adjacent
# hand-edited lines carrying similar-looking values is the slip this is for.
if [ "$OTHER" = "$BASIS" ]; then
  echo "!! OTHER and BASIS are both '$BASIS' -- a pair is two halves"
  exit 1
fi

# The run's name identifies it against the NEXT run; this guards it against
# itself. Relaunching with a name already used overwrites every JSON and log
# of the first attempt in place, which is hours gone and nothing said.
# `ls a b c` exits nonzero when ANY operand is missing, so testing its status
# would let a half-finished run through -- which is the very state you would
# relaunch from. Test the listing instead.
#
# The gate's own artifacts are excluded, and that exclusion is load-bearing
# rather than tidy: run-gate.sh writes `$R-gate-<half>-<pass>.json` into the
# same `$R-` space this globs, so without it the gate the procedure requires
# before the evening would read as a previous attempt and refuse the very run
# it was meant to clear.
#
# The wall-clock log wants no operand of its own: `$R-*.log` already covers
# it, and naming it besides listed it twice in the refusal.
EXISTING=$(ls -1 "$R"-*.json "$R"-*.log 2>/dev/null \
             | grep -v "^$R-gate-")
if [ -n "$EXISTING" ]; then
  echo "$R already has artifacts here:"
  printf '%s\n' "$EXISTING" | sed 's/^/  /'
  echo "relaunching would overwrite them. Move them aside, or pick another"
  echo "name -- and if the first attempt died mid-sequence, read its"
  echo "wall-clock log for how far it got before deciding which."
  exit 1
fi
CLASSES="rev revsome bcast bcastmid reshape1 slice window scaled"
# A CLASS NAME CARRIES NO HYPHEN, and this is the one place that says so.
# The population of a bench is derived below by cutting its name at the
# first hyphen, while a SHAPE name carries hyphens of its own
# (`bcast-inner8`), so the two are told apart by that asymmetry alone. A
# class called `bcast-mid` would cut to `bcast` and merge with the class of
# that name: one process for two populations, its count agreeing with what
# the prefix selects, and the second population never getting a process, a
# JSON or a word said about it. The existing names read as though this were
# known -- `bcastmid` and `revsome`, not `bcast-mid` and `rev-some` -- but
# nothing enforced it, and install-tables.sh's two lead patterns BOTH miss a
# hyphenated lead, so they agree and the cross-check written against exactly
# that failure cannot fire. Loud here, before the hours.
for c in $CLASSES; do
  case $c in *-*)
    echo "class name '$c' carries a hyphen, which the population derivation"
    echo "below cannot survive: it cuts each bench name at its first hyphen,"
    echo "so this class would merge with whatever stands before that hyphen."
    echo "Rename it without one, in classViews and here, before the run."
    exit 1 ;;
  esac
done

NOTE="$PREFIX-pair.txt"

for h in $HALVES; do
  [ -x "./$PREFIX-$h" ] || { echo "missing ./$PREFIX-$h -- $NOTE has the recipe"; exit 1; }
done

MAIN_BENCHES=$(./"$PREFIX-$BASIS" --list 2>/dev/null | wc -l)
[ "$MAIN_BENCHES" -gt 0 ] || { echo "--list gave nothing; wrong binary?"; exit 1; }
CLASS_LIST=$(./"$PREFIX-$BASIS" classes --list 2>/dev/null)
[ -n "$CLASS_LIST" ] || { echo "classes --list gave nothing; wrong binary?"; exit 1; }

# CLASSES is a literal where every count here is read from the binary, so the
# two can drift apart in both directions -- and only one of them was loud. A
# prefix naming nothing is reported per class below; a class the BINARY has
# that no prefix names ran nowhere, printed nothing and left no artifact,
# under an exit 0. So it is caught HERE, before the hours, where the fix is
# one word in the line above. Non-vacuous, and cheaply: drop a name from
# CLASSES and the run refuses naming it, put it back and the run starts.
UNNAMED=
for c in $(printf '%s\n' "$CLASS_LIST" | cut -d/ -f1 | cut -d- -f1 | sort -u)
do
  case " $CLASSES " in *" $c "*) ;; *) UNNAMED="$UNNAMED $c" ;; esac
done
if [ -n "$UNNAMED" ]; then
  echo "./$PREFIX-$BASIS has class population(s) CLASSES does not name:$UNNAMED"
  echo "each would run nowhere, print nothing and leave no artifact. Add them"
  echo "to CLASSES above, in classViews' order, before starting the run."
  exit 1
fi

BAD=0                        # mechanical complaints; the sequence carries on
                             # past every one of them, and the exit status is
                             # what says any were raised

log () { echo "=== $(date -Is) $*" | tee -a "$R-wallclock.log"; }

run () {   # $1 = half, $2 = artifact tag, $3 = benches expected, $4.. = args
  local h=$1 tag=$2 want=$3; shift 3
  local out="$R-$tag" rc nb
  log "start $out"
  ./"$PREFIX-$h" "$@" --json "$out.json" > "$out.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "$out.log")
  log "done  $out rc=$rc benchmarking=$nb"
  [ "$rc" = 0 ] || { log "  !! nonzero exit -- read $out.log before trusting anything after"; BAD=$((BAD + 1)); }
  # Named, because nine of these in one log looked identical and the only
  # thing saying which process each belonged to was the line above it.
  [ "$nb" = "$want" ] || { log "  !! $out: expected $want benches, got $nb -- the selection is not what was asked for"; BAD=$((BAD + 1)); }
}

# TWO commits, because HEAD is not what the binaries were built from and
# saying so once cost a wrong provenance line: HEAD dates the tree the run was
# launched from, and the Main.hs commit dates the source under it. NEITHER is
# necessarily the pair's own -- a write-up edits Main.hs's comments without
# rebuilding, so both can be ahead of the binaries -- which is why README's
# recording step transcribes the commit out of the pair note instead. A dirty
# tree is what makes either a lie, so the count goes in too.
# ASKED WHETHER GIT ANSWERED, because the reassuring reading is the one
# it gives when it did not: `tree at , Main.hs at ` for the commits and
# `0 path(s) untracked or modified` for the count, which is exactly what a
# clean tree looks like -- and the count is the safeguard the paragraph
# above leans on. Reachable without leaving this directory: a dubious-
# ownership refusal, a stale index lock, a `.git` the sandbox mounted
# read-only. It does not stop the run, six hours being worth more than a
# provenance line, but the line cannot read as a commit nobody has.
# Found 2026-08-17 by a toy run of this procedure.
HEAD_AT=$(git log -1 --format=%h 2>/dev/null)
MAIN_AT=$(git log -1 --format=%h -- Main.hs 2>/dev/null)
DIRTY=$(git status --porcelain 2>/dev/null); GIT_SAID=$?
# Either field empty, not just the first: run from a directory where
# Main.hs is not the tracked path, `git log -- Main.hs` answers nothing
# while `git log` answers fine, and the line came out `Main.hs at ` with
# every other field right -- the same empty field, one over, produced by
# the toy run that found the first.
if [ "$GIT_SAID" != 0 ] || [ -z "$HEAD_AT" ] || [ -z "$MAIN_AT" ]; then
  log "major run begins; GIT DID NOT ANSWER, so this run records no commit\
 and no tree state -- the write-up's provenance line cannot be taken from\
 here; roster is $MAIN_BENCHES benches"
else
  log "major run begins; tree at $HEAD_AT, Main.hs at $MAIN_AT; roster is\
 $MAIN_BENCHES benches"
fi
log "halves: $HALVES, in that order; $BASIS is the basis, and every class runs\
 on both halves"
if [ "$GIT_SAID" = 0 ]; then
  log "tree: $(printf '%s' "$DIRTY" | grep -c .) path(s) untracked or modified"
  [ -z "$DIRTY" ] || printf '%s\n' "$DIRTY" | tee -a "$R-wallclock.log"
fi
uptime | tee -a "$R-wallclock.log"

# Which gate this run stands on, COPIED and not judged: the note's wording is
# a person's, and a predicate over it would be guessing at the one fact worth
# a quiet hour. If the lines below say the gate has not run, or that it
# failed, stop and read README's gate step -- nothing here will.
if [ -f "$NOTE" ]; then
  log "$NOTE says, about the gate:"
  # Every line saying `gate`, and -- for one that STARTS with the token,
  # the shape run-gate.sh writes -- the indented block under it. The token
  # alone dropped exactly the lines worth having: neither the machine
  # verdict nor `!! the machine check FAILED` carries the word, so a gate
  # that failed on the machine alone reached this log as a FAILED headline
  # over four clean processes with the reason nowhere. Only a line STARTING
  # a block may end one, the four artifact lines inside it being named
  # `$R-gate-*` and so saying the word themselves.
  awk '/^GATE:/             { blk = 1; print; next }
       tolower($0) ~ /gate/ { print; next }
       blk && /^[ \t]/      { print; next }
                            { blk = 0 }' "$NOTE" \
    | sed 's/^/      /' | tee -a "$R-wallclock.log"
else
  log "!! no $NOTE -- this run's provenance is the commit and nothing else"
fi

for h in $HALVES; do run "$h" "$h-main" "$MAIN_BENCHES"; done
# EVERY class on BOTH halves since 2026-08-14, where they used to be the
# basis's alone. What forced it is that a pair's variable can act on a class
# and not on the main set -- Run 14 varies the allocation area, and the
# classes are where the shapes whose excess allocation crosses the nursery
# live (README.md#what-moves-a-figure-when-no-strategy-changed) -- so a
# class read on one half only cannot say whether the variable touched it.
# The cost is one more process per class, paid every run so that no run
# has to notice in advance that its own question needs them; the
# basis's artifacts keep their names, so nothing that reads a class block
# has to change. Each class's two halves run adjacent, control then basis,
# mirroring the main sets above -- and each bench process being its own OS
# process, that order carries no heap state between them.
for c in $CLASSES; do
  want=$(printf '%s\n' "$CLASS_LIST" | grep -c "^$c-")
  if [ "$want" -eq 0 ]; then
    log "  !! class prefix $c- matches no bench -- skipped, not run empty"
    BAD=$((BAD + 1))
    continue
  fi
  for h in $HALVES; do run "$h" "$h-$c" "$want" classes "$c-"; done
done

if [ "$BAD" -eq 0 ]; then
  log "major run complete; every process ran the count asked of it"
else
  log "major run complete, with $BAD complaint(s) above -- read them before\
 any figure"
fi
echo
echo "Read it with the halves kept apart:"
echo "  ./read-run.py $R-$BASIS-main.json               # the basis, and the table"
echo "  ./read-run.py $R-$OTHER-main.json               # the control"
echo "  ./read-run.py $R-$BASIS-main.json --compare $R-$OTHER-main.json"
echo "                                                  # the per-arm difference"
echo "Every --in-place table comes from the basis half (README, the run's plan):"
echo "  --markdown, --fingerprint and --block from $R-$BASIS-*.json"
# The complaints above are not fatal -- there is no reading in which eight
# sound populations are worth discarding for one that is not -- but they have
# to leave the script by some door, and a run launched with `&` is read by
# whatever collected it. This is that door; the wall-clock log is still where
# the complaint itself is.
[ "$BAD" -eq 0 ] || exit 1
