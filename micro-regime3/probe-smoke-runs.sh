#!/bin/bash
# -L1 previews of the three `runs` processes the quiet evening will take at
# criterion's default budget. Rough by construction and quoted nowhere:
# what they are for is the threshold. `lib-stage2-disp` has to be cut to
# the crossover the class MEASURES, and the class is a 30-minute process,
# so without a preview the evening carries a serial dependency -- re-take,
# read, rebuild, run -- with a rebuild in the middle of it. The adjacent
# shapes of this class differ by factors of two to six across the
# crossover, which is far above what -L1 blurs, so a preview settles the
# BRACKET even though it settles no figure. The full-budget re-take stays
# the authority and the arm is rebuilt if it disagrees.
set -u
cd "$(dirname "$0")" || exit 1
for spec in "probe-bang-g912:probe-smoke-runs-bang" \
            "probe-disp-g912:probe-smoke-runs-disp" \
            "probe-nospill-g912:probe-smoke-runs-nospill"; do
  B=${spec%%:*}; O=${spec#*:}
  echo "=== $(date -Is) start $O on $B"
  WILDLOG=1 SATURATE=1 ./"$B" classes runs- -L1 --json "$O.json" > "$O.log" 2>&1
  echo "=== $(date -Is) done  $O rc=$? benchmarking=$(grep -c '^benchmarking ' "$O.log")"
done
echo "=== $(date -Is) SMOKE RUNS COMPLETE"
