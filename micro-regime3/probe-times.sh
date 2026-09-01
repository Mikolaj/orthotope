#!/bin/bash
# One criterion process per population, on whichever binary BIN names, at
# criterion's default budget and under Run 21's launch environment. The
# three uses it was written for, and the three questions they answer:
#
#   ./probe-times.sh main rev revsome slice scaled window bcast bcastmid
#   ./probe-times.sh runs
#       -- probe-bang-g912, the default: the TIME half of the unboxing fix.
#          [the ceiling]'s ninth reading measured that fix in INSTRUCTIONS
#          and left time open, which is what task 1 in README's open list
#          has left: the 2.4 to 4.5 it holds the branch on is a time ratio,
#          and the second term -- time over instructions -- is untouched by
#          that reading. The binary is the ninth reading's own, Run 21's
#          basis recipe over the current source, so every arm sits at the
#          slot it sat at in Run 21 and each JSON is `--compare`-able with
#          run21-g912-<pop>.json, the pair being the fix and nothing else.
#
#   BIN=./probe-disp-g912 OUT=probe-runlen-disp ./probe-times.sh runs
#       -- the dispatch arm against the three it dispatches between, in one
#          process, which is task 2's first half. Its threshold is cut to
#          the crossover the re-take above measures, so this process runs
#          AFTER that one and not before.
#
#   BIN=./probe-nospill-g912 OUT=probe-runlen-nospill ./probe-times.sh runs
#       -- `-u2` against `-down` in a spill-free binary, task 2's second
#          half. Read that one with --corr=insitu: `sum-only` runs larger
#          than the bench under -fllvm, so the default correction sinks
#          every cell, and its column is comparable to no figure in README.
#
# WANTS A QUIET MACHINE. About 101 minutes for the main set and 13 to 30 a
# class, by Run 21's own wall-clock log, which is what says whether a
# process is running slow -- scaled by the bench count, criterion spending
# its budget per bench.
#
# The launch environment is Run 21's, WILDLOG=1 SATURATE=1, and it is not
# optional for the first use: the saturating preamble installs the
# block-pool state Run 21's processes measured in, so a process without it
# is not comparable with the half this run is read against. Both switches
# are asserted per process below, as run-major.sh asserts them, and echoed
# whether set or not -- an assertion conditional on a switch cannot see the
# failure that matters, which is an operator who forgot one.
#
# Non-vacuity, 2026-08-30, each guard broken deliberately and refusing:
# probe-times-selftest.log records the four.
#
# Artifacts $OUT-<pop>.{json,log} and $OUT-wallclock.log. NEVER a run's own
# prefix: read-all.sh and check-scripts.py --properties read a $R-*.json as
# one of that run's processes, and a probe parked there reads exactly like
# the run breaking.
set -u
cd "$(dirname "$0")" || exit 1
[ $# -ge 1 ] || { echo "usage: [BIN=... OUT=...] ./probe-times.sh POP [POP ...]   # main, or a class name"; exit 2; }

BIN=${BIN:-./probe-bang-g912}
OUT=${OUT:-probe-bangtime}
LOG=$OUT-wallclock.log
case $BIN in /*|./*) ;; *) BIN=./$BIN ;; esac
[ -x "$BIN" ] || { echo "no $BIN here"; exit 2; }
case $OUT in probe-*|smoke-*) ;;
  *) echo "OUT is '$OUT': a probe's artifacts are probe-* or smoke-*, never a"
     echo "run's own prefix -- read-all.sh would read them as that run's"
     echo "processes and gate the run on them."; exit 2 ;;
esac

# Refuse a relaunch over artifacts, as the run drivers do: they are
# overwritten in place with nothing said. Per population, this being
# launched a population at a time.
for p in "$@"; do
  E=$(ls -1 "$OUT-$p.json" "$OUT-$p.log" 2>/dev/null)
  [ -z "$E" ] || { echo "$OUT-$p already has artifacts:"; printf '%s\n' "$E" | sed 's/^/  /'
                   echo "relaunching would overwrite them. Move them aside first."; exit 2; }
done

MAIN_BENCHES=$("$BIN" --list 2>/dev/null | wc -l)
CLASS_LIST=$("$BIN" classes --list 2>/dev/null)
[ "$MAIN_BENCHES" -gt 0 ] || { echo "--list gave nothing; wrong binary?"; exit 2; }
[ -n "$CLASS_LIST" ] || { echo "classes --list gave nothing; wrong binary?"; exit 2; }

BAD=0
log () { echo "=== $(date -Is) $*" | tee -a "$LOG"; }

# Asked whether git answered, as run-major.sh asks: unasked, a refusal
# reads `tree at , Main.hs at` -- a commit nobody has. 2026-09-01.
HEAD_AT=$(git log -1 --format=%h 2>/dev/null)
MAIN_AT=$(git log -1 --format=%h -- Main.hs 2>/dev/null)
GITLINE="tree at $HEAD_AT, Main.hs at $MAIN_AT"
[ -n "$HEAD_AT" ] && [ -n "$MAIN_AT" ] \
  || GITLINE="GIT DID NOT ANSWER, so no commit is recorded here"
log "$OUT begins on $BIN, md5 $(md5sum "$BIN" | cut -d' ' -f1) -- THE MD5 IS\
 THE BINARY'S IDENTITY and the commits below are the TREE'S, which a probe\
 reusing an earlier binary can be several commits ahead of; $GITLINE;\
 populations: $*"
log "launch env: WILDLOG=${WILDLOG-unset} SATURATE=${SATURATE-unset} -- both\
 are Run 21's, and a process missing one is not comparable with it"
uptime | tee -a "$LOG"

for p in "$@"; do
  if [ "$p" = main ]; then
    want=$MAIN_BENCHES
    sel=()
  else
    want=$(printf '%s\n' "$CLASS_LIST" | grep -c "^$p-")
    sel=(classes "$p-")
  fi
  if [ "$want" -eq 0 ]; then
    log "  !! population $p matches no bench -- skipped, not run empty"
    BAD=$((BAD + 1)); continue
  fi
  out=$OUT-$p
  log "start $out ($want benches expected)"
  "$BIN" ${sel[@]+"${sel[@]}"} --json "$out.json" > "$out.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "$out.log")
  ns=$(grep -c '^@@saturate ' "$out.log")
  nw=$(grep -c '^@@wild ' "$out.log")
  log "done  $out rc=$rc benchmarking=$nb saturate=$ns wild=$nw"
  [ "$rc" = 0 ] || { log "  !! nonzero exit -- read $out.log before trusting anything after"; BAD=$((BAD + 1)); }
  [ "$nb" = "$want" ] || { log "  !! $out: expected $want benches, got $nb -- the selection is not what was asked for"; BAD=$((BAD + 1)); }
  if [ -n "${SATURATE:-}" ] && [ "${SATURATE}" != 0 ]; then
    [ "$ns" = 1 ] || { log "  !! $out: SATURATE=$SATURATE was set and this log carries $ns @@saturate line(s), not 1 -- the process did not assert its state, so its figures are not this probe's"; BAD=$((BAD + 1)); }
    grep -h '^@@saturate ' "$out.log" | sed "s|^|      $out |" | tee -a "$LOG"
  fi
  if [ -n "${WILDLOG:-}" ] && [ "${WILDLOG}" != 0 ]; then
    [ "$nw" -gt 0 ] || { log "  !! $out: WILDLOG=$WILDLOG was set and this log carries no @@wild stamps -- the instrument is not in this binary"; BAD=$((BAD + 1)); }
  fi
done

if [ "$BAD" -eq 0 ]; then log "$OUT complete; every process ran the count asked of it"
else log "$OUT complete, with $BAD complaint(s) above -- read them before any figure"; fi
[ "$BAD" -eq 0 ] || exit 1
