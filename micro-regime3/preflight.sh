#!/usr/bin/env bash
# The pre-run list's steps 4 to 10, in one call.
#
#     ./preflight.sh run19            # the halves from the note's HALVES line
#     ./preflight.sh run19 --note     # 10c, 10d and 8 alone, seconds
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
  echo "usage: ./preflight.sh RUN [--note|--no-corpus|--corpus]  # e.g. run17"
  echo "  --note        steps 10c, 10d and 8 alone -- the ones that read what"
  echo "                the preparation WROTE, in seconds and with no binary"
  echo "  --no-corpus   everything but 8c and 8d, the two that read every run"
  echo "                JSON on disk: run this, launch 11 and 12, and take"
  echo "                the two afterwards with --corpus"
  echo "  --corpus      8c and 8d alone"
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
shift
for a in "$@"; do
  case $a in
    --note) NOTE_ONLY=1 ;;
    --no-corpus) CORPUS=0 ;;
    --corpus) REST=0 ;;
    *) echo "unknown argument '$a' --" \
            "./preflight.sh RUN [--note|--no-corpus|--corpus]"; exit 2 ;;
  esac
done
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
        echo "  every step\047s raw output kept in $TMP -- wiped with /tmp,"
        echo "  and readable only where this ran; copy out what you hand on"
      else
        rm -rf "$TMP"
      fi' EXIT

BAD=0
say () {  # say STEP VERDICT DETAIL
  printf '  %-4s %-4s %s\n' "$1" "$2" "$3"
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
  if [ -f "$R-pair.txt" ]; then
    MISSING=$(grep -oE '(probe-[A-Za-z0-9._{},-]*[A-Za-z0-9_}]/?|'"$R"'-[A-Za-z0-9._-]+\.(json|log|txt))' \
                "$R-pair.txt" | sort -u \
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
"./$R-$BASIS" check > "$TMP/a.log" 2>&1; ra=$?
"./$R-$OTHER" check > "$TMP/b.log" 2>&1; rb=$?
if [ "$ra" != 0 ] || [ "$rb" != 0 ]; then
  say '4,5' FAIL "a check exited $ra/$rb -- read $TMP before it goes"
elif cmp -s "$TMP/a.log" "$TMP/b.log"; then
  say '4,5' PASS "both halves agree on every shape, byte-identical"
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
SCAN=$("./$R-$BASIS" diag 2>/dev/null \
       | awk '/^vgg-14-c512 /{f=1} f && /baseOffsetsScan /{print $(NF-3); exit}')
MUT=$("./$R-$BASIS" diag 2>/dev/null \
      | awk '/^vgg-14-c512 /{f=1} f && /baseOffsetsMut /{print $(NF-3); exit}')
if [ -z "$SCAN" ] || [ -z "$MUT" ]; then
  say 9 FAIL "could not read the diag row; regime UNCONFIRMED"
else
  RATIO=$(python3 -c "print('%.3f' % ($SCAN/$MUT))")
  if python3 -c "import sys; sys.exit(0 if 0.98 < $SCAN/$MUT < 1.02 else 1)"
  then say 9 PASS "SpecConstr: scan/mut $RATIO on vgg-14-c512 ($SCAN vs $MUT)"
  else say 9 FAIL "regime is NOT SpecConstr: scan/mut $RATIO -- plain -O1 is ~10"
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

# 8c and 8d LAST, and not merely last in the printing: they are the two
# that read every run JSON on disk, so putting them at the end is what
# lets --no-corpus stop short of them, the sweeps run, and --corpus take
# them afterwards. Whichever way, they never share the directory with a
# sweep that is still writing.
if [ "$CORPUS" = 1 ]; then
./properties.py > "$TMP/prop" 2>&1 \
  && say 8c PASS "properties over every run JSON here" \
  || say 8c FAIL "properties: $(grep -m1 FAIL "$TMP/prop")"

defect-run.py . > "$TMP/cs" 2>&1 \
  && say 8d PASS "every planted defect refused again" \
  || say 8d FAIL "defect-run: $(tail -1 "$TMP/cs")"
fi

echo
if [ "$BAD" -eq 0 ]; then
  echo "all clear. NOT done here and still owed: 9b, the pair's own variable,"
  echo "which only $R-pair.txt can name; and 11 and 12, which the note records"
  echo "and a spent preparation inherits. Then the run list, from step 13."
  [ "$CORPUS" = 1 ] || echo "  8c and 8d did NOT run: --corpus takes them" \
                            "once 11 and 12 have landed."
  [ "$REST" = 1 ] || echo "  ONLY 8c and 8d ran; this is no preflight."
else
  echo "$BAD step(s) FAILED -- read them before anything that costs an evening."
fi
exit $((BAD > 0))
