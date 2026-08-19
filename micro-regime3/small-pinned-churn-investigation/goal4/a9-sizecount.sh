#!/bin/bash
# Stretch goal 5: what "small" measures for the interleaved allocation
# term -- count or bytes (item 60's second OPEN). All cells at -A1G,
# where the controls are clean, on the movable spray (interunboxed, no
# pinned-class confound), ReproSmall's k:/intersize: arguments. Two
# axes: size at fixed count (k:1000 x 36/100/288 doubles = 288/800/2304
# B), and count at ~fixed bytes (k:1000 x 288 vs k:4000 x 72 vs k:8000
# x 36 -- every size sub-threshold, every count past saturation). One
# pinned spot cell (inter intersize:36) checks the pinned side matches.
# Registered lean, judged not remembered: size-independent within the
# sub-threshold class at saturation -- item 29's upfront result (800,
# 1800, 2304 B all full strength) carried to the interleaved route, so
# the size axis reads flat and the fixed-bytes axis reads flat too
# (count already saturated); a tax rising with bytes at fixed count
# would instead make bytes the dose and re-open item 41(c).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
R=goal4/ReproSmall
exec > goal4/a9-sizecount-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $R
run() { local name=$1; shift
  $R "$@" -RTS > goal4/a9-sc-$name.log 2>&1
  echo "== $name: $(grep -h 'victim:\|intersize' goal4/a9-sc-$name.log | tr '\n' ' ')"
}
run alone-1g                    victim +RTS -A1G -I0 -T
run unboxed-k1000-sz288-1g      interunboxed victim +RTS -A1G -I0 -T
run unboxed-k1000-sz100-1g      interunboxed intersize:100 victim +RTS -A1G -I0 -T
run unboxed-k1000-sz36-1g       interunboxed intersize:36 victim +RTS -A1G -I0 -T
run unboxed-k4000-sz72-1g       interunboxed k:4000 intersize:72 victim +RTS -A1G -I0 -T
run unboxed-k8000-sz36-1g       interunboxed k:8000 intersize:36 victim +RTS -A1G -I0 -T
run pinned-k1000-sz36-1g        inter intersize:36 victim +RTS -A1G -I0 -T
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A9-SIZECOUNT
