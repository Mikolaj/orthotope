#!/bin/bash
# The follow-up comment's reproducer matrix: goal4/ReproV2.hs (the issue
# description's Repro.hs plus the interleave modes, the bytes the
# comment embeds), all interleave modes and the alone legs at -A32m and
# -A1G, 1G twice (the residue split's area). The comment's table is
# this driver log; the verbatim outputs are the a8-*.log cells.
# Registered leans, judged not remembered (items 44, 54, 55 carried to
# this program; the control leans REVISED after the first matrix and
# probe cells of 2026-08-19): inter ~+25% at 32m / ~+12% at 1G;
# interunboxed ~+23% / ~+9%; interbig ~+15% / +1-2%; internoalloc and
# internoallocr ~+13-19% at 32m (the punctuation term this victim pays
# there for any interleaved activity) and ~0-2% at 1G, where the
# allocation-vs-not discrimination is clean. Added 2026-08-19 with the
# interunboxedbig mode (3600 B movable = large object, own block group,
# never in the nursery): lean, at the controls' level at both areas --
# the route's ingredient is allocation that passes through the nursery;
# it poisoning like interunboxed would instead say smallness per se.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
R=goal4/ReproV2
exec > goal4/a8-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $R goal4/ReproV2.hs
run() { local name=$1; shift
  $R "$@" -RTS > goal4/a8-$name.log 2>&1
  echo "== $name: $(grep victim: goal4/a8-$name.log)"
}
for r in r1 r2; do
  for m in "" inter interbig interunboxed interunboxedbig internoalloc internoallocr; do
    tag=${m:-alone}
    run $tag-32m-$r $m victim +RTS -A32m -I0 -T
  done
done
for r in r1 r2; do
  for m in "" inter interbig interunboxed interunboxedbig internoalloc internoallocr; do
    tag=${m:-alone}
    run $tag-1g-$r $m victim +RTS -A1G -I0 -T
  done
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A8
