#!/usr/bin/env bash
# A major run, paired: both halves take the main set, the classes go to the
# aligned half alone (README, the run's plan). Ten processes, unattended,
# several hours.
#
#     ./run-major.sh run10          # the argument names every artifact
#
# Nothing here builds. The pair comes from make-pair.py and must not be
# rebuilt between the halves, which is what the pairing measures; this
# refuses to start without both binaries.
#
# What it adds over pasting the sequence is the counting: each main process's
# bench count is checked against what the roster actually holds, so a
# selection that silently caught the wrong set is loud at once rather than at
# the write-up. The expected count is READ FROM THE BINARY rather than
# written down -- a literal would be wrong for the next roster, and Run 11
# already plans an arm, which would make a correct run trip the alarm on
# every process.

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
CLASSES="rev revsome bcast bcastmid reshape1 slice window scaled"

for h in unaligned aligned; do
  [ -x "./micro-$h" ] || { echo "missing ./micro-$h -- run ./make-pair.py"; exit 1; }
done

MAIN_BENCHES=$(./micro-aligned --list 2>/dev/null | wc -l)
[ "$MAIN_BENCHES" -gt 0 ] || { echo "--list gave nothing; wrong binary?"; exit 1; }

log () { echo "=== $(date -Is) $*" | tee -a "$R-wallclock.log"; }

run () {   # $1 = binary half, $2 = artifact tag, $3.. = extra args
  local h=$1 tag=$2; shift 2
  local out="$R-$tag" rc nb
  log "start $out"
  ./micro-"$h" "$@" --json "$out.json" > "$out.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "$out.log")
  log "done  $out rc=$rc benchmarking=$nb"
  [ "$rc" = 0 ] || log "  !! nonzero exit -- read $out.log before trusting anything after"
  if [ "$tag" != "${tag%main}" ] && [ "$nb" != "$MAIN_BENCHES" ]; then
    log "  !! expected $MAIN_BENCHES benches, got $nb -- the selection is not the roster"
  fi
}

log "major run begins; $(git log -1 --format=%h); roster is $MAIN_BENCHES benches"
uptime | tee -a "$R-wallclock.log"

for h in unaligned aligned; do run "$h" "$h-main"; done
for c in $CLASSES; do run aligned "aligned-$c" classes "$c-"; done

log "major run complete"
echo
echo "Read it with the halves kept apart:"
echo "  ./read-run.py $R-unaligned-main.json            # succeeds the last run's basis"
echo "  ./read-run.py $R-aligned-main.json              # the new regime"
echo "  ./read-run.py $R-aligned-main.json --compare $R-unaligned-main.json"
echo "                                                  # the per-arm layout term"
echo "Install from the UNALIGNED half only (README, the run's plan)."
