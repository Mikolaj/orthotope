#!/bin/bash
# padding-plan.txt task 2.2: FORM-CHANGE NULL -- newform-unpadded against
# run15-lookrts, interleaved pairs (A B A B per cell, one bench per
# process), default area, on vgg-14-c512-k3's six measured arms (the
# remeasure.sh arm-specificity set) plus list on both sub-410 shapes;
# vgg/sum-only-early rides as the per-pair layout control, its timed
# expression calling no rewritten builder.
# Registered lean, judged not remembered (plan 2.2): within the drift
# band, most arms under 1.5% (the relink-noise scale of item 38-adjacent
# history); an arm outside the band means the constructor rewrite changed
# compiled code and the affected builder is re-examined before anything
# else runs. Caution (item 24): offtab and build alone-legs spread
# 21%/10% across processes at -A32m; read their cells with that in mind.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
A=./run15-lookrts        # anchor
B=./newform-unpadded
D=small-pinned-churn-investigation/goal4
exec > $D/t22-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $A $B

CELLS="vgg-list:vgg-14-c512-k3/list
vgg-bq-expand:vgg-14-c512-k3/bq-expand
vgg-mut-odo-vecdims:vgg-14-c512-k3/mut-odo-vecdims
vgg-bq-scan-rem-gm:vgg-14-c512-k3/bq-scan-rem-gm-mulback
vgg-offtab:vgg-14-c512-k3/offtab
vgg-build:vgg-14-c512-k3/build
vgg-sum-only:vgg-14-c512-k3/sum-only-early
slice-list:cnn-slice-c32/list
L1c6-list:cnn-L1-6x6-c1/list"

one() { # binary tag cellname glob
  local bin=$1 tag=$2 name=$3 glob=$4
  $bin -m glob "$glob" --json $D/t22-$name-$tag.json \
    > $D/t22-$name-$tag.log 2>&1
  awk -v pfx="$name-$tag:" '/^time /{print pfx, $2, $3; exit}' \
    $D/t22-$name-$tag.log
}

for cell in $CELLS; do
  name=${cell%%:*}; glob=${cell#*:}
  one $A a-r1 "$name" "$glob"
  one $B b-r1 "$name" "$glob"
  one $A a-r2 "$name" "$glob"
  one $B b-r2 "$name" "$glob"
done

python3 small-pinned-churn-investigation/goal4/t2x-reduce.py $D t22
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-T22
