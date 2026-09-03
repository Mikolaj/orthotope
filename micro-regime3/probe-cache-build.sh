#!/bin/bash
# The built half of the past-cache probe (README's tasks after Run 24):
# two regime-2 views of 8 million elements -- 64 MB of source and as much
# of output against this box's 32 MB of L3, where every rostered view fits
# -- built into a scratch copy of the package with the size cap raised
# for that copy alone, on Run 24's basis recipe. Not a roster change: the
# cap keeps a mistyped dimension from taking an evening, and a cell this
# size buys criterion few samples, so the views live here and nowhere in
# Main.hs.
#
# Wants no quiet machine; probe-cache-run.sh does. Artifacts:
# probe-cache-spot and probe-cache-build.log; the scratch copy is removed.
set -eu
cd "$(dirname "$0")"
[ -e probe-cache-spot ] && { echo "probe-cache-spot exists already"; exit 1; }
D=scratch-cache
rm -rf "$D" && mkdir "$D"
cp Main.hs Probe.hs micro.cabal cabal.project cabal.project.freeze align-as.py "$D"/
python3 - "$D/Main.hs" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new, 1)
rep('sizeCap = 1800000', 'sizeCap = 9000000')
rep('           && all ((> sizeCap) . product . snd) tooBig\n', '')
rep('  , ("runs-r3-48x30", [1250, 48, 30])   -- 1800000, merges to runs of 1440\n  ]',
    '  , ("runs-r3-48x30", [1250, 48, 30])   -- 1800000, merges to runs of 1440\n'
    '  , ("runs-cache-96",   [87381, 96])    -- 8388576, past the cache\n'
    '  , ("runs-cache-4096", [2048, 4096])   -- 8388608, past the cache\n  ]')
open(p, 'w').write(s)
EOF
( cd "$D" && LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 \
  cabal build micro --builddir=db-cache \
    --ghc-options="-fspec-constr -fobject-determinism" \
    --ghc-options="-pgma $PWD/align-as.py -fforce-recomp" ) > probe-cache-build.log 2>&1
cp "$(cd "$D" && cabal list-bin micro --builddir=db-cache)" probe-cache-spot
rm -rf "$D"
echo "CACHE PROBE BUILT: probe-cache-spot, md5 $(md5sum probe-cache-spot | cut -d' ' -f1)"
