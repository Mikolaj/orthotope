#!/bin/bash
# The corrected poison scan. Criterion runs benches in ROSTER order, so the
# victim must sit LAST in the roster for every candidate to precede it.
# stretch-inner256 is position 24 of 24. Every process ASSERTS the order it got.
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts; V=stretch-inner256; A=${1:-32m}
# Candidate ENUMERATION only; order is irrelevant here (each pair process
# asserts its own execution order below).  --list prints alphabetical order,
# NOT execution order -- never read a roster position off it.
[ -f /tmp/shapes.txt ] ||
  $B --list 2>/dev/null | cut -d/ -f1 | awk '!seen[$0]++' > /tmp/shapes.txt
echo "victim=$V (roster position 24), -A$A"
$B -m glob "$V/list" --json /tmp/p2-alone.json +RTS -A$A > /tmp/p2-alone.log 2>&1
base=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$2; exit}" /tmp/p2-alone.log)
bu=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$3; exit}" /tmp/p2-alone.log)
echo "alone baseline: $base $bu   (benchmarking=$(grep -c '^benchmarking ' /tmp/p2-alone.log))"
echo
printf '%-24s %10s %10s %s\n' candidate victim delta order
for C in $(cat /tmp/shapes.txt); do
  [ "$C" = "$V" ] && continue
  o=/tmp/p2-$C
  $B -m glob "$C/list" "$V/list" --json $o.json +RTS -A$A > $o.log 2>&1
  first=$(awk '/^benchmarking /{print $2; exit}' $o.log | cut -d/ -f1)
  t=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$2; exit}" $o.log)
  u=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$3; exit}" $o.log)
  nb=$(grep -c '^benchmarking ' $o.log)
  if [ "$first" != "$C" ]; then ord="INVALID(ran $first first)"; else ord=ok; fi
  [ "$u" = "$bu" ] || ord="$ord UNITS($u vs $bu)"
  d=$(python3 -c "print('%+.1f%%' % ((float('$t')/float('$base')-1)*100))" 2>/dev/null || echo '?')
  printf '%-24s %10s %10s %s nb=%s\n' "$C" "$t" "$d" "$ord" "$nb"
done
echo DONE-POISON2
