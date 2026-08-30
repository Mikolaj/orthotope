#!/bin/bash
# The -g3 twin item 4's attribution wants: the g912 recipe with -g3, so
# the binary carries a line table and perf can say which SOURCE LINE the
# instructions of a fill go to. A -g3 build is a twin to READ and never
# one to time (README.md#what-is-open) -- on the native backend it is a
# different program and what differs is register allocation -- so what
# transfers from it is which line runs and in what proportion, never a
# count. The timed binary's own counts are in the counted-work sweeps.
set -eu
cd "$(dirname "$0")"
[ -e probe-attr-g912 ] && { echo "probe-attr-g912 exists already"; exit 1; }
LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 \
cabal build micro --builddir=db-attr \
  --ghc-options="-fspec-constr -fobject-determinism -g3" \
  --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
cp "$(cabal list-bin micro --builddir=db-attr)" probe-attr-g912
rm -rf db-attr
echo "ATTR TWIN BUILT"
