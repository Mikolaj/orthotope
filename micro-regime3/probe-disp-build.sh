#!/bin/bash
# NOT A CURRENT RECIPE: built on Run 21's basis, -fspec-constr among its
# flags, which no basis has carried since Run 29; the current basis is in
# the last run's pair note.
#
# The dispatch arm's binary: Run 21's basis recipe (run21-pair.txt) over
# the current source, which is probe-bang-g912's recipe too -- so the two
# differ in the roster alone and the dispatch arm's three neighbours are
# read in one process with it.
#
# Wants no quiet machine; `check` is owed on it, and so is the allocation
# reading that shows the dispatch firing, which is the one thing `check`
# cannot see (every threshold is correct).
set -eu
cd "$(dirname "$0")"
[ -e probe-disp-g912 ] && { echo "probe-disp-g912 exists already"; exit 1; }
LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 \
cabal build micro --builddir=db-disp \
  --ghc-options="-fspec-constr -fobject-determinism" \
  --ghc-options="-pgma $PWD/../../horde-ad/tools/align-as.py -fforce-recomp"
cp "$(cabal list-bin micro --builddir=db-disp)" probe-disp-g912
rm -rf db-disp
echo "DISP BUILT"
