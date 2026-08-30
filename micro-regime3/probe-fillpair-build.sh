#!/bin/bash
# The pair that prices a fill change in TIME, which counted work cannot
# do: instructions are load-insensitive and so cheap, but what this
# README publishes is time, and the second term between them is largest
# on the runs class.
#
# Two binaries, ONE recipe (Run 21's basis: -fspec-constr,
# -fobject-determinism, the max-skip shim), differing only in the source:
# BEFORE names the tree without the change and the `after` half is the
# working tree. Both come from git rather than from a scratch path, so
# this is re-runnable by anyone; the first version read /tmp and was not.
#
# The rosters must be identical between the halves, or slots move and the
# pair varies two things; the caller checks that with --list, as
# probe-times.sh's own counting does at run time.
set -eu
cd "$(dirname "$0")"
BEFORE=${BEFORE:-1c33cff}          # fillStage2 changed, the two unrolled fills not
for t in A B; do
  [ -e "probe-fill$t-g912" ] && { echo "probe-fill$t-g912 exists"; exit 1; }
done
cp Main.hs Main.hs.workingtree
restore () { cp Main.hs.workingtree Main.hs; rm -f Main.hs.workingtree; }
trap restore EXIT
build () {                      # $1 = tag
  LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 \
  cabal build micro --builddir=db-fp \
    --ghc-options="-fspec-constr -fobject-determinism" \
    --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
  cp "$(cabal list-bin micro --builddir=db-fp)" "probe-fill$1-g912"
  rm -rf db-fp
}
git show "$BEFORE:micro-regime3/Main.hs" > Main.hs
build A
cp Main.hs.workingtree Main.hs
build B
echo "FILL PAIR BUILT"
