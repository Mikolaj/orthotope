#!/bin/bash
# Goal-2 Stage B phase 2, 2026-08-18: follow-ups the phase-1 verdicts opened.
# (1) -xn tie-break rep at 64m (read -2.4% once, inside single-cell draw).
# (2) The -AL64m discovery: bq-expand alone at -A4m went 4.355 -> 2.766 ms.
#     Chart its reach: does it help list-like arms at -A4m (whose GC
#     pressure is small-object-driven, so predicted not); does bq-expand
#     stay poison-immune under it; does list's small -A4m tax grow under it
#     (more large-object accumulation between GCs, the 27601-style risk);
#     and a smaller point -AL16m to see the knee.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal2
exec > $D/stageB2-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

# (1) -xn rep, poisoned, 64m
o=$D/vpois-vgg-A64m-xn-r2
$B -m glob 'cnn-slice-c32/list' 'vgg-14-c512-k3/list' --json $o.json +RTS -A64m -xn > $o.log 2>&1
echo "vpois vgg -A64m [-xn] r2 victim=$(awk "/^benchmarking vgg-14-c512-k3\/list\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $o.log)"

# (2a) alone legs at -A4m -AL64m and -AL16m
cell_alone() { # bench tag flags
  local N=$1 T=$2; shift 2
  local o=$D/AL-alone-$T
  $B -m glob "$N" --json $o.json +RTS "$@" > $o.log 2>&1
  echo "alone $N [$*] $(awk "/^benchmarking ${N//\//\\/}\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $o.log)"
}
cell_alone 'vgg-14-c512-k3/bq-expand' bq-AL16m -A4m -AL16m
cell_alone 'vgg-14-c512-k3/list' list-AL64m -A4m -AL64m
cell_alone 'stretch-inner256/list' inner-AL64m -A4m -AL64m
cell_alone 'stretch-inner256/bq-expand' innerbq-plain -A4m
cell_alone 'stretch-inner256/bq-expand' innerbq-AL64m -A4m -AL64m

# (2b) poisoned cells at -A4m -AL64m: bq (stays immune?) and list (tax grows?)
cell_pois() { # victimbench tag flags
  local N=$1 T=$2; shift 2
  local o=$D/AL-pois-$T
  $B -m glob 'cnn-slice-c32/list' "$N" --json $o.json +RTS "$@" > $o.log 2>&1
  local first=$(awk '/^benchmarking /{print $2; exit}' $o.log)
  local ord=ok; [ "$first" = "cnn-slice-c32/list" ] || ord="INVALID(ran $first first)"
  echo "pois $N [$*] victim=$(awk "/^benchmarking ${N//\//\\/}\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $o.log) $ord"
}
cell_pois 'vgg-14-c512-k3/bq-expand' bq-AL64m -A4m -AL64m
cell_pois 'vgg-14-c512-k3/list' list-AL64m -A4m -AL64m

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-STAGEB2
