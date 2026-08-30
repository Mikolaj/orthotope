#!/bin/bash
# The dispatch arm on the second compiler, which task 2 asks for outright:
# a compiler can move a crossover, so a threshold read on one compiler
# alone is a threshold nobody has checked. Run 21's OTHER half's recipe
# (run21-pair.txt) over today's source -- the project file selects the
# compiler and its freeze pins the plan, the store being filled for it.
set -eu
cd "$(dirname "$0")"
[ -e probe-disp-ghead ] && { echo "probe-disp-ghead exists already"; exit 1; }
LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 \
cabal build micro --project-file=cabal.project.ghead --builddir=db-dispghead \
  --ghc-options="-fspec-constr -fobject-determinism" \
  --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
cp "$(cabal list-bin micro --project-file=cabal.project.ghead \
        --builddir=db-dispghead)" probe-disp-ghead
rm -rf db-dispghead
echo "DISP GHEAD BUILT"
