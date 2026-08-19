#!/bin/bash
# padding-plan.txt A4: the -A4m added-miss attribution, mutator vs
# collector symbols (nursery-position-plan 2.6's pending half; item 18
# took counters only, and at -A1G). perf record over the conv1d-24
# fixed-n design at -A4m: victim alone, poison alone, pair -- the added
# misses' symbol split (evacuate/scavenge vs mutator code) settles old
# plan 1.5(d)'s conceptual objection: collector-side weakens it and
# re-scores the rival accounts, mutator-side stands measured.
# No direction was registered; the cell decides. Wall is taken beside
# each record so the -A4m tax itself is on file with the samples.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal4
exec > $D/a4-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B
cell() { # name selection...
  local name=$1; shift
  /usr/bin/time -f %e -o $D/a4-$name.time \
    perf record -e cache-misses -o $D/a4-$name.data -- \
    $B -m glob "$@" -n 400000 +RTS -A4m > $D/a4-$name.log 2>&1
  perf report --stdio -i $D/a4-$name.data > $D/a4-$name-report.txt 2>&1
  echo "$name: wall $(cat $D/a4-$name.time) s, first=$(awk '/^benchmarking /{print $2; exit}' $D/a4-$name.log)"
  echo "  top symbols:"
  grep -m 6 '%' $D/a4-$name-report.txt | tail -5
}
cell alone  'conv1d-24/list'
cell poison 'cnn-slice-c32/list'
cell pair   'cnn-slice-c32/list' 'conv1d-24/list'
echo "evacuate/scavenge shares per cell:"
for c in alone poison pair; do
  echo "== $c"
  grep -E 'evacuate|scavenge' $D/a4-$c-report.txt | head -6
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A4
