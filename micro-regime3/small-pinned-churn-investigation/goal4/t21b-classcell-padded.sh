#!/bin/bash
# The 2.4a follow-up the refuted lean demands (cheapest-refutation rule):
# t21's fixed-n matched-dose design at -A32m rerun on the PADDED binary,
# cnn-slice-c32 poison only. t21 (run15) read sub-threshold +12.2%,
# own-group -2.4%; the padded scan then read cnn-slice +12.7% with NO
# collapse anywhere. This cell discriminates the two accounts: padded
# mega-dose ~0% = the pad de-poisons the upfront route and the scan's
# residue is the criterion-machinery interleaved route (item 39,
# class-independent, out of padding's reach); padded mega-dose still
# ~+12% = the pad's own-group conversion failed mechanically and the
# object size is the next thing to check.
# Registered lean, judged not remembered: ~0%, by t21's own-group cell
# and the 3296 B > 3276 B arithmetic.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./newform-padded
D=small-pinned-churn-investigation/goal4
exec > $D/t21b-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B

run() {
  local name=$1 n=$2; shift 2
  /usr/bin/time -f %e -o $D/t21b-$name.time \
    $B -m glob "$@" -n "$n" +RTS -A32m > $D/t21b-$name.log 2>&1
  local first
  first=$(awk '/^benchmarking /{print $2; exit}' $D/t21b-$name.log)
  echo "$name: wall $(cat $D/t21b-$name.time) s, first=$first, benches=$(grep -c '^benchmarking ' $D/t21b-$name.log)"
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
w = lambda n: float(open(f"{d}/t21b-{n}.time").read())
alone = (w("alone-conv1d-400k") - w("alone-conv1d-200k")) / 200e3 * 1e6
print(f"victim alone (padded binary): {alone:.2f} us/iter")
v = ((w("pair-slice-400k") - w("pair-slice-200k"))
     - (w("alone-slice-400k") - w("alone-slice-200k"))) / 200e3 * 1e6
print(f"after padded cnn-slice-c32: {v:.2f} us/iter  ({(v/alone-1)*100:+.1f}%)")
EOF
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-T21B
