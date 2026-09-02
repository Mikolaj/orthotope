#!/usr/bin/env bash
# Post-run step 0's two -g3 twins for Run 23, built from run23-pair.txt's
# own two recipes with -g3 added and nothing else moved -- as Run 22's were
# taken on 2026-08-31. They NAME the fill groups; they are not timed and
# never join a table, `-g3` being a different program (README).
# probe- prefix, because no probe of any kind takes the run's prefix.
set -u
cd "$(dirname "$0")" || exit 1

build () {   # $1 = half, then the env the recipe puts in front of cabal
  local h=$1; shift
  local bd="db-g3-$h"
  echo "### $(date -Is) building probe-g3-$h-r23"
  rm -rf "$bd"
  env "$@" \
  cabal build micro --builddir="$bd" \
    --ghc-options="-fspec-constr -fobject-determinism -g3" \
    --ghc-options="-pgma $PWD/align-as.py -fforce-recomp" || return 1
  cp "$(cabal list-bin micro --builddir="$bd")" "probe-g3-$h-r23" || return 1
  rm -rf "$bd"
  echo "### $(date -Is) probe-g3-$h-r23 done, $(stat -c%s "probe-g3-$h-r23") B"
}

build g912 LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1                 || { echo "### g912 twin FAILED"; exit 1; }
build spot LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 || { echo "### spot twin FAILED"; exit 1; }
echo "### $(date -Is) both twins built"
