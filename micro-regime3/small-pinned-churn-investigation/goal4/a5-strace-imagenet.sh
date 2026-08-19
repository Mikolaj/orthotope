#!/bin/bash
# padding-plan.txt A5: the strace kernel-time attribution of the imagenet
# -A32m pathology (old plan 2.9; weakened by items 31-32 -- the knobs it
# would explain measured null and -AL works the cost around -- but never
# run). The README floor section's temporary tooBig edit, rebuilt here
# FROM A COPY under goal4/a5-pkg so the live tree is never touched: all
# six tooBig shapes promoted into convShapes, sizeCap raised to imagenet,
# the lookrts recipe with -M20G in the baked RTS line. Then strace -c
# -e trace=memory over imagenet-224-c64-k3/bq-expand at -A32m, -A64m and
# -A4m -AL64m (item 32's mover), two n's each for per-call differencing,
# plus one /usr/bin/time wall+sys cell per area.
# Registered lean, judged not remembered (items 31-32's residue): the
# -A32m kernel premium sits in the memory syscalls (madvise/munmap churn)
# and the -A64m and -AL cells carry ~none of it -- attribution, not a new
# knob; a 32m cell whose kernel time is NOT in trace=memory syscalls
# would instead reopen old plan 2.9's account.
# NOTE the source is the padding-edit tree at padSmall=False; imagenet's
# l is far above 410, so the pad cannot touch these cells.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
D=goal4
exec > $D/a5-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

mkdir -p $D/a5-pkg
cp ../Main.hs ../Probe.hs ../micro.cabal ../align-as.py \
   ../cabal.project.freeze $D/a5-pkg/
chmod +x $D/a5-pkg/align-as.py
echo "packages: ." > $D/a5-pkg/cabal.project
python3 - $D/a5-pkg/Main.hs <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
def sub1(old, new):
    global s
    assert s.count(old) == 1, (old[:60], s.count(old))
    s = s.replace(old, new)
sub1("sizeCap = 1800000", "sizeCap = 28901376  -- A5 TEMPORARY: imagenet included")
entries = """  [ ("vgg-28-c256-k3",      [28, 28, 256, 3, 3])      -- 1806336  (~1.8M)
  , ("vgg-112-c64-k3",      [112, 112, 64, 3, 3])     -- 7225344  (~7M)
  , ("resnet-stem-112-c3-k7", [112, 112, 3, 7, 7])    -- 1843968  (~1.8M)
  , ("resnet-56-c128-k3",   [56, 56, 128, 3, 3])      -- 3612672  (~3.6M)
  , ("resnet-56-c256-k3",   [56, 56, 256, 3, 3])      -- 7225344  (~7.2M)
  , ("imagenet-224-c64-k3", [224, 224, 64, 3, 3])     -- 28901376 (~29M)
  ]"""
sub1("tooBig =\n" + entries, "tooBig = []")
tail = '  , ("conv1d-24",           [24, 3, 3, 24])           -- 5184\n  ]'
promoted = entries.replace("  [ ", "  , ", 1).rstrip()
sub1(tail, tail[:-3] + promoted)
open(p, "w").write(s)
print("a5 edit applied")
EOF

( cd $D/a5-pkg &&
  LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 cabal build micro --builddir=db \
    --ghc-options="-fspec-constr" \
    --ghc-options="-pgma $PWD/align-as.py -fforce-recomp" \
    --ghc-options='"-with-rtsopts=-I0 -T -M20G"' &&
  cp "$(cabal list-bin micro --builddir=db)" ../a5-micro-imagenet &&
  rm -rf db ) || { echo "A5 BUILD FAILED"; exit 1; }
B=$D/a5-micro-imagenet
md5sum $B
strings $B | grep -x -- '-I0 -T -M20G'
G='imagenet-224-c64-k3/bq-expand'

for area in "-A32m" "-A64m" "-A4m -AL64m"; do
  tag=$(echo "$area" | tr -d ' -')
  /usr/bin/time -f '%e wall  %S sys' -o $D/a5-$tag-time.txt \
    $B -m glob "$G" -n 200 +RTS $area > $D/a5-$tag-n200.log 2>&1
  echo "== $area: $(cat $D/a5-$tag-time.txt)"
  for n in 100 200; do
    strace -c -f -e trace=memory -o $D/a5-$tag-strace-n$n.txt \
      $B -m glob "$G" -n $n +RTS $area > $D/a5-$tag-strace-n$n.log 2>&1
  done
  tail -12 $D/a5-$tag-strace-n200.txt
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A5
