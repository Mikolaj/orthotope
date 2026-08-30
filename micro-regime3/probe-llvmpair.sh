#!/bin/bash
# The same change under the LLVM backend, because the mechanism is
# register allocation and the two backends do not allocate alike: [the
# ceiling]'s sixth reading has GHC's NCG picking a spill victim with no
# next-use information at all (GHC #27742) where LLVM got these loops
# spill-free. A win that is the NCG's alone is still worth having -- the
# NCG is what a default build uses -- but it must be scoped, and this is
# what scopes it.
#
# BOTH SOURCES COME FROM GIT, and the first version of this took them
# from /tmp instead: a tracked script whose recipe reads a scratch path
# cannot be re-run by anyone, the wrapper hiding that path from the
# machine's owner and a restart wiping it. BEFORE names the tree without
# the fill change; the `after` half is the working tree, which is what a
# session pricing its own edit has in hand.
set -eu
cd "$(dirname "$0")"
BEFORE=${BEFORE:-dc8fe46}          # the tree before any fill change
for tag in before after; do
  [ -e "probe-llvm-$tag-g912" ] && { echo "probe-llvm-$tag-g912 exists"; exit 1; }
done
cp Main.hs Main.hs.workingtree
restore () { cp Main.hs.workingtree Main.hs; rm -f Main.hs.workingtree; }
trap restore EXIT
for tag in before after; do
  if [ "$tag" = before ]; then
    git show "$BEFORE:micro-regime3/Main.hs" > Main.hs
  else
    cp Main.hs.workingtree Main.hs
  fi
  cabal build micro --builddir=db-lp \
    --ghc-options="-fspec-constr -fobject-determinism" \
    --ghc-options="-fllvm -optlc-align-loops=64 -fforce-recomp"
  cp "$(cabal list-bin micro --builddir=db-lp)" "probe-llvm-$tag-g912"
  rm -rf db-lp
  echo "built probe-llvm-$tag-g912"
done
echo "LLVM PAIR BUILT"
