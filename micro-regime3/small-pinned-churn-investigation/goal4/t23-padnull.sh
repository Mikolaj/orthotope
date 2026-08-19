#!/bin/bash
# padding-plan.txt task 2.3: PADDING NULL ON BIG SHAPES -- newform-padded
# against newform-unpadded, interleaved pairs (A B A B per cell, one
# bench per process), default area, on vgg-14-c512-k3's six measured arms
# and stretch-inner256's three MixedLoad arms; vgg/sum-only-early rides
# as the per-pair layout control.
# Registered lean, judged not remembered (plan 2.3): flat to the floor --
# padTo is identity above 410 and the branch is one compare per result
# allocation (folded away entirely in the unpadded binary, so what this
# pair carries is that compare plus the constant flip's relink).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
A=./newform-unpadded     # control
B=./newform-padded
D=small-pinned-churn-investigation/goal4
exec > $D/t23-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $A $B

CELLS="vgg-list:vgg-14-c512-k3/list
vgg-bq-expand:vgg-14-c512-k3/bq-expand
vgg-mut-odo-vecdims:vgg-14-c512-k3/mut-odo-vecdims
vgg-bq-scan-rem-gm:vgg-14-c512-k3/bq-scan-rem-gm-mulback
vgg-offtab:vgg-14-c512-k3/offtab
vgg-build:vgg-14-c512-k3/build
vgg-sum-only:vgg-14-c512-k3/sum-only-early
inner256-list:stretch-inner256/list
inner256-bq-expand:stretch-inner256/bq-expand
inner256-mut-odo-vecdims:stretch-inner256/mut-odo-vecdims"

one() { # binary tag cellname glob
  local bin=$1 tag=$2 name=$3 glob=$4
  $bin -m glob "$glob" --json $D/t23-$name-$tag.json \
    > $D/t23-$name-$tag.log 2>&1
  awk -v pfx="$name-$tag:" '/^time /{print pfx, $2, $3; exit}' \
    $D/t23-$name-$tag.log
}

for cell in $CELLS; do
  name=${cell%%:*}; glob=${cell#*:}
  one $A a-r1 "$name" "$glob"
  one $B b-r1 "$name" "$glob"
  one $A a-r2 "$name" "$glob"
  one $B b-r2 "$name" "$glob"
done

python3 small-pinned-churn-investigation/goal4/t2x-reduce.py $D t23
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-T23
