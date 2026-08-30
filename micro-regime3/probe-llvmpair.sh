#!/bin/bash
# The same change under the LLVM backend, because the mechanism is
# register allocation and the two backends do not allocate alike: [the
# ceiling]'s sixth reading has GHC's NCG picking a spill victim with no
# next-use information at all (GHC #27742) where LLVM got these loops
# spill-free. A win that is the NCG's alone is still worth having -- the
# NCG is what a default build uses -- but it must be scoped, and this is
# what scopes it.
set -eu
cd "$(dirname "$0")"
for tag in before after; do
  [ -e "probe-llvm-$tag-g912" ] && { echo "probe-llvm-$tag-g912 exists"; exit 1; }
done
for tag in before after; do
  cp "/tmp/claude/Main.hs.$tag" Main.hs
  cabal build micro --builddir=db-lp \
    --ghc-options="-fspec-constr -fobject-determinism" \
    --ghc-options="-fllvm -optlc-align-loops=64 -fforce-recomp"
  cp "$(cabal list-bin micro --builddir=db-lp)" "probe-llvm-$tag-g912"
  rm -rf db-lp
  echo "built probe-llvm-$tag-g912"
done
cp /tmp/claude/Main.hs.after Main.hs
echo "LLVM PAIR BUILT"
