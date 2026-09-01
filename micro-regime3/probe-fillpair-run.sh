#!/bin/bash
# The pair's evening: each population on both halves, adjacent, control
# (A, the fill unchanged) first. runs leads because it settles task 5 as
# well as pricing the change; main is the headline; slice is where the
# residue this all came from was visible.
set -u
cd "$(dirname "$0")" || exit 1
export WILDLOG=1 SATURATE=1
# The populations are the argument when there is one, so a stopped
# evening resumes at the population it stopped in rather than
# refusing over the artifacts of the ones that finished.
# `${*:-...}` and not `"${@:-...}"`: quoted, the default is ONE word,
# `runs main slice`, which names no population, so the wrapper ran
# nothing and still printed COMPLETE. Found 2026-09-01 by review.
BAD=0
for pop in ${*:-runs main slice}; do
  for h in A B; do
    BIN=./probe-fill$h-g912 OUT=probe-fill$h ./probe-times.sh "$pop" \
      || { echo "!! probe-fill$h $pop complained"; BAD=$((BAD + 1)); }
  done
done
# Complaints ride the COMPLETE line, as probe-evening-c's do: the line a
# session waits on is the log's last, and a complaint on stdout alone
# never reaches it.
echo "=== $(date -Is) FILL PAIR COMPLETE, complaints=$BAD" \
  | tee -a probe-fillA-wallclock.log
exit $((BAD > 0))
