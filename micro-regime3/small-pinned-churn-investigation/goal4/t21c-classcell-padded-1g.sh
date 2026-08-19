#!/bin/bash
# The decision table's -A1G row, measured rather than inferred: item 13's
# mega-dose design (conv1d-24/list victim, cnn-slice-c32/list poison,
# fixed-n differencing) on the PADDED binary at -A1G, where the unpadded
# run15 reading is +44% -- the worst upfront-route tax on record.
# Registered lean, judged not remembered: ~0%, t21b's verdict carried to
# the big area (the pad converts the spray to own-group, and item 16 has
# own-group at zero at -A1G).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./newform-padded
D=small-pinned-churn-investigation/goal4
exec > $D/t21c-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B

run() {
  local name=$1 n=$2; shift 2
  /usr/bin/time -f %e -o $D/t21c-$name.time \
    $B -m glob "$@" -n "$n" +RTS -A1G > $D/t21c-$name.log 2>&1
  local first
  first=$(awk '/^benchmarking /{print $2; exit}' $D/t21c-$name.log)
  echo "$name: wall $(cat $D/t21c-$name.time) s, first=$first, benches=$(grep -c '^benchmarking ' $D/t21c-$name.log)"
}

run alone-conv1d-200k 200000 'conv1d-24/list'
run alone-conv1d-400k 400000 'conv1d-24/list'
run alone-slice-200k  200000 'cnn-slice-c32/list'
run alone-slice-400k  400000 'cnn-slice-c32/list'
run pair-slice-200k   200000 'cnn-slice-c32/list' 'conv1d-24/list'
run pair-slice-400k   400000 'cnn-slice-c32/list' 'conv1d-24/list'

python3 - "$D" <<'EOF'
import sys
d = sys.argv[1]
w = lambda n: float(open(f"{d}/t21c-{n}.time").read())
alone = (w("alone-conv1d-400k") - w("alone-conv1d-200k")) / 200e3 * 1e6
print(f"victim alone at -A1G (padded binary): {alone:.2f} us/iter")
v = ((w("pair-slice-400k") - w("pair-slice-200k"))
     - (w("alone-slice-400k") - w("alone-slice-200k"))) / 200e3 * 1e6
print(f"after padded cnn-slice-c32: {v:.2f} us/iter  ({(v/alone-1)*100:+.1f}%)")
EOF
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-T21C
