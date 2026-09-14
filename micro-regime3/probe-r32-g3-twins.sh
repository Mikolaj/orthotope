#!/usr/bin/env bash
# Post-run step 0's two -g3 twins for Run 32, built from run32-pair.txt's
# own two recipes with -g3 added and nothing else moved -- as Runs 25 to
# 31's were. They NAME the fill groups and the straddlers; they are not
# timed and never join a table, `-g3` being a different program (README).
# probe- prefix, because no probe of any kind takes the run's prefix.
#
# THE TWO RECIPES DIFFER IN THE PROJECT FILE, which is this pair's own
# variable, as it was Run 28's: the ghead half is built through
# cabal.project.ghead, which selects the in-tree stage1 and pins its plan,
# so the twin is built through it too. THE OTHER COMPILER'S TWIN IS NOT
# USELESS -- the match is by byte identity of the loop body and the two
# compilers emit many of these bodies alike, which is what named four of
# the six straddlers Run 28's own HEAD twin refused. Build both, pass both
# to `--match`, and start with the half's own.
#
# NO REGIME FLAG: this pair is plain -O1 on both halves, `-O1` being
# micro.cabal's own, so neither recipe spells one and neither twin does.
# That is where this differs from Runs 25 to 28's twins, which all carried
# `-fspec-constr`.
set -u
cd "$(dirname "$0")" || exit 1

build () {   # $1 = half, $2 = project file or `-`, then the recipe's env
  local h=$1 pf=$2; shift 2
  local bd="db-g3-$h"
  local pfa=()
  [ "$pf" = - ] || pfa=(--project-file="$pf")
  echo "### $(date -Is) building probe-g3-$h-run32"
  rm -rf "$bd"
  env "$@" \
  cabal build micro "${pfa[@]}" --builddir="$bd" \
    --ghc-options="-fobject-determinism -g3" \
    --ghc-options="-pgma $PWD/align-as.py -fforce-recomp" || return 1
  cp "$(cabal list-bin micro "${pfa[@]}" --builddir="$bd")" \
     "probe-g3-$h-run32" || return 1
  rm -rf "$bd"
  echo "### $(date -Is) probe-g3-$h-run32 done, $(stat -c%s "probe-g3-$h-run32") B"
}

build nospec - \
  LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 \
  || { echo "### nospec twin FAILED"; exit 1; }
build ghead cabal.project.ghead \
  LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 \
  || { echo "### ghead twin FAILED"; exit 1; }
echo "### $(date -Is) both twins built"
