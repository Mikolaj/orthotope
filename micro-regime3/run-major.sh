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
#
# THE LAUNCH SWITCHES ARE COUNTED THE SAME WAY, and recorded besides. An
# instrument switched on by an environment variable is off unless the launch
# line sets it, and nothing else here can see that: the bench counts come out
# right, the gate passes and the reader is happy over logs with no stamps in
# them. So each switch that IS set is asserted per process -- one `@@saturate`
# line, at least one `@@wild` stamp -- and both are echoed into the wallclock
# log at the start whether set or not, because an assertion conditional on the
# switch cannot see the failure that matters, which is an operator who forgot
# one. The echo cannot stop that run; it puts the fact in the run's own record
# at minute one rather than leaving it to be inferred hours later from an
# absence, and only then if `--wild` is reached for at all.

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
# second column of the run's own file, and THE BASIS runs SECOND, which is
# where it ran in Run
# 10, so a run repeating that one inherits its process position. It does
# not inherit the binary: reusing a previous basis binary was refused on
# 2026-08-16 and every pair is built here, both halves back to back. Both halves run every class, which they did not before
# 2026-08-14 -- the loop below says what changed and why. Change these two names per pair -- and
# nothing else here, the counting below being what makes a wrong selection
# loud in the log rather than at the write-up.
OTHER=${OTHER:-spot}
BASIS=${BASIS:-g912}
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
# The alone-leg riders' `$R-al-*` are the other writer of this prefix, and
# excluded for the same reason: run-alonelegs.sh writes them AFTER the run
# (README's step 19) and nothing here ever writes that name, so a relaunch
# after the riders was refused over files it would not have touched --
# read-all.sh's roster skips both, one script over. Found 2026-08-22 by
# review. Case: `relaunch-guard-skips-the-riders`, with
# `major-run-refuses-a-previous-attempt` the control that the run's own
# artifacts still refuse it.
#
# The wall-clock log wants no operand of its own: `$R-*.log` already covers
# it, and naming it besides listed it twice in the refusal.
EXISTING=$(ls -1 "$R"-*.json "$R"-*.log 2>/dev/null \
             | grep -v -e "^$R-gate-" -e "^$R-al-")
if [ -n "$EXISTING" ]; then
  echo "$R already has artifacts here:"
  printf '%s\n' "$EXISTING" | sed 's/^/  /'
  echo "relaunching would overwrite them. Move them aside, or pick another"
  echo "name -- and if the first attempt died mid-sequence, read its"
  echo "wall-clock log for how far it got before deciding which."
  exit 1
fi
CLASSES="rev revsome bcast bcastmid reshape1 slice window scaled runs"
# A CLASS NAME CARRIES NO HYPHEN, and this is the one place that says so.
# The population of a bench is derived below by cutting its name at the
# first hyphen, while a SHAPE name carries hyphens of its own
# (`bcast-inner8`), so the two are told apart by that asymmetry alone. A
# class called `bcast-mid` would cut to `bcast` and merge with the class of
# that name: one process for two populations, its count agreeing with what
# the prefix selects, and the second population never getting a process, a
# JSON or a word said about it. The existing names read as though this were
# known -- `bcastmid` and `revsome`, not `bcast-mid` and `rev-some` -- but
# nothing enforced it, and install-tables.sh's two lead patterns both read
# `[a-z0-9]`, so a hyphenated lead slipped both and the cross-check between
# them could not fire; that script refuses such a lead by name now, and
# this is loud here, before the hours.
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
# Refused without it, before the hours, as a missing binary is: the note
# carries the pair's recipe and the gate's verdict, which the run copies
# into its log below. A run without one used to log `!! no <note>` and go
# on at exit 0 -- and read-all.sh counts every stamped `!!` as a process
# complaint, with no carve-out, so every later reading of that run failed
# as "the run complained about itself" over eighteen clean processes.
# Found 2026-08-22 by review. Case: `major-run-wants-its-pair-note`.
[ -f "$NOTE" ] || { echo "no $NOTE -- a pair's note is written at pre-run step 2,"
                    echo "and the gate writes its verdict into it; nothing runs"
                    echo "without one"; exit 1; }

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
  # THE PLATEAU, counted exactly as the bench count above is, and for the
  # same reason: a process that did not assert its state is not in the
  # state the others measured in, and nothing else here would say so.
  # Run 18's preamble prints one `@@saturate` line per process before
  # criterion sees the roster; the reading it carries is registration 5's,
  # and the band over the whole run is `read-all.sh`'s to gate. Zero is
  # the right count for a run without the preamble, so the count is only
  # asked for when a dose was set -- a binary WITHOUT the preamble under
  # `SATURATE=1` then reads 0 against 1 and complains, which is the case
  # that matters, an unsaturated half silently joining a saturated run.
  if [ -n "${SATURATE:-}" ] && [ "${SATURATE}" != 0 ]; then
    local nsat
    nsat=$(grep -c '^@@saturate ' "$out.log")
    [ "$nsat" = 1 ] || { log "  !! $out: SATURATE=$SATURATE was set and this log carries $nsat @@saturate line(s), not 1 -- the process did not assert its state, so its figures are not in the run's"; BAD=$((BAD + 1)); }
    grep -h '^@@saturate ' "$out.log" | sed "s|^|      $out |" \
      | tee -a "$R-wallclock.log"
  fi
  # THE OTHER SWITCH, counted the same way and for the same reason. The
  # per-sample instrument writes a `@@wild` line per criterion sample,
  # two per sample in fact, so ANY count above zero is the assertion --
  # unlike the preamble's, which is exactly one a process. Zero under
  # `WILDLOG` set is a binary built without the instrument, joining an
  # instrumented run with nothing else able to see it: the JSONs, the
  # bench counts, the gate and the reader all come out right, and the
  # log simply has no stamps in it.
  if [ -n "${WILDLOG:-}" ] && [ "${WILDLOG}" != 0 ]; then
    local nwild
    nwild=$(grep -c '^@@wild ' "$out.log")
    [ "$nwild" -gt 0 ] || { log "  !! $out: WILDLOG=$WILDLOG was set and this log carries no @@wild stamps -- the instrument is not in this binary, so the run is uninstrumented and only --wild would ever have said so"; BAD=$((BAD + 1)); }
  fi
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
# THE LAUNCH ENVIRONMENT, recorded whether or not it carries anything. The
# two assertions in `run()` fire only when their switch IS set, so neither
# can see the failure that matters -- an operator who forgot one. Nothing
# downstream notices either: the bench counts come out right, the gate
# passes, the reader is happy, and the registration the pair was built to
# answer comes back empty, discovered at the write-up if `--wild` is
# reached for at all, which post-run step 2 says is not every process.
# This cannot stop that run, but it puts the fact in the run's own record
# at its first minute instead of leaving it to be inferred from an absence
# hours later. `run-alonelegs.sh` has echoed its own switches since Run 17
# and this is that line, in the driver that spends the evening.
log "launch env: WILDLOG=${WILDLOG-unset} SATURATE=${SATURATE-unset} --\
 the note's LAUNCH block says what this pair wants, and a switch reading\
 unset where it wants a value is an uninstrumented run that will otherwise\
 look perfect"
if [ "$GIT_SAID" = 0 ]; then
  log "tree: $(printf '%s' "$DIRTY" | grep -c .) path(s) untracked or modified"
  [ -z "$DIRTY" ] || printf '%s\n' "$DIRTY" | tee -a "$R-wallclock.log"
fi
uptime | tee -a "$R-wallclock.log"

# Which gate this run stands on, COPIED and not judged: the note's wording is
# a person's, and a predicate over it would be guessing at the one fact worth
# a quiet hour. If the lines below say the gate has not run, or that it
# failed, stop and read README's gate step -- nothing here will.
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
