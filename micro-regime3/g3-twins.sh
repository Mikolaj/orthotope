#!/usr/bin/env bash
# Post-run step 0's two -g3 twins, built from the pair note's own recipes
# with -g3 added and nothing else moved. They NAME the fill groups and the
# straddlers for `loop-offsets.py --match`; they are not timed and never
# join a table, `-g3` being a different program (README, post-run step 0).
#
#     ./g3-twins.sh run40            # builds probe-g3-<half>-run40, both
#     ./g3-twins.sh run40 --dry-run  # prints the two parsed recipes only
#
# THE RECIPES ARE READ OFF THE NOTE, `$R-pair.txt`'s HOW EACH HALF IS BUILT
# block, and not copied from the last run's probe: probe-* is ignored by
# git, so Run 40 found no Run 39 script on disk and re-derived one from
# Run 38's by hand. Per half the block gives a `  $R-<half>` line and then
# the command up to `then`: its environment assignments, its
# --project-file, and its --ghc-options, of which the one carrying `-pgma`
# is the shim's and is rebuilt here with a builddir of this script's own.
# Printed before anything builds, so a recipe misread is seen first.
set -u
cd "$(dirname "$0")" || exit 1
if [ $# -lt 1 ] || [ $# -gt 2 ] || { [ $# -eq 2 ] && [ "$2" != --dry-run ]; }; then
  echo "usage: ./g3-twins.sh RUN [--dry-run]"
  exit 2
fi
R=$1; DRY=${2:-}
NOTE="$R-pair.txt"
[ -f "$NOTE" ] || { echo "no $NOTE, so there is no recipe to read"; exit 2; }
HALVES=$(./pair-halves.sh "$R") || exit 2
eval "$HALVES"

# THE TWINS ARE OF THE PAIR'S SOURCE OR NOT BUILT (2026-09-25, by review).
# They build from this tree's Main.hs and align-as.py, so each must sit at
# the commit the note's `Main.hs at` or `shim at` row names and be clean
# against it; otherwise their loop bodies are not the timed binaries' and
# `--match` names the wrong copies or none. --dry-run says a mismatch and
# refuses nothing, since it builds nothing; G3_TREE=1 builds over one, for
# a move known to leave the code alone, a write-up's comment edit being
# the usual one, and prints the mismatch above the build.
SRC_BAD=
for row in 'Main.hs at:Main.hs' 'shim at:align-as.py'; do
  lbl=${row%%:*}; path=${row#*:}
  want=$(sed -n "s/^ *$lbl  *\([0-9a-f]\{7,40\}\).*/\1/p" "$NOTE" | head -1)
  have=$(git log -1 --format=%H -- "$path" 2>/dev/null)
  if [ -z "$want" ]; then
    SRC_BAD="$SRC_BAD
    $NOTE has no '$lbl <commit>' row"
  elif [ -z "$have" ]; then
    SRC_BAD="$SRC_BAD
    git names no commit for $path here, so nothing holds it to $want"
  elif [ "$(git rev-parse -q --verify "$want^{commit}" 2>/dev/null)" \
         != "$have" ]; then
    SRC_BAD="$SRC_BAD
    $path is at $(git log -1 --format=%h -- "$path"), and the note's row\
 names $want"
  elif ! git diff --quiet HEAD -- "$path"; then
    SRC_BAD="$SRC_BAD
    $path differs from its commit in the working tree"
  fi
done
if [ -z "$SRC_BAD" ]; then
  echo "### source: Main.hs and align-as.py at the note's commits, clean"
elif [ -n "$DRY" ] || [ "${G3_TREE:-}" = 1 ]; then
  echo "### the twins would not be of the pair's source:$SRC_BAD"
  [ -n "$DRY" ] || echo "### G3_TREE=1: building from the tree as it stands"
else
  echo "### the twins would not be of the pair's source:$SRC_BAD"
  echo "### nothing built: put both files at the note's commits, clean, or"
  echo "### set G3_TREE=1 for a move that leaves the code alone"
  exit 2
fi

recipe () {  # recipe HALF -> three lines: env, project file, ghc options
  python3 - "$NOTE" "$R-$1" <<'PY'
import re, sys
note, tag = sys.argv[1], sys.argv[2]
lines = open(note).read().split('\n')
at = [i for i, l in enumerate(lines) if re.match(r'\s+%s\s' % re.escape(tag), l)]
if len(at) != 1:
    sys.exit('%d recipe header(s) for %s in %s, need 1' % (len(at), tag, note))
body = []
for l in lines[at[0] + 1:]:
    if l.strip() == 'then':
        break
    body.append(l.strip().rstrip('\\').strip())
cmd = ' '.join(body)
if 'cabal build micro' not in cmd:
    sys.exit('the recipe for %s carries no `cabal build micro`' % tag)
env = cmd[:cmd.index('cabal build micro')].split()
if not all(re.match(r'^[A-Z_][A-Z0-9_]*=\S*$', e) for e in env):
    sys.exit('the recipe for %s has something other than environment'
             ' assignments before cabal: %s' % (tag, ' '.join(env)))
pf = re.findall(r'--project-file=(\S+)', cmd)
opts = [o for o in re.findall(r'--ghc-options="([^"]*)"', cmd)
        if '-pgma' not in o]
if len(pf) > 1 or len(opts) != 1:
    sys.exit('the recipe for %s has %d project files and %d non-shim'
             ' --ghc-options, need at most 1 and exactly 1'
             % (tag, len(pf), len(opts)))
print(' '.join(env))
print(pf[0] if pf else '-')
print(' '.join(opts[0].split()))
PY
}

build () {  # build HALF
  local h=$1 bd="db-g3-$1" env pf opts out
  { read -r env; read -r pf; read -r opts; } < <(recipe "$h") || return 2
  [ -n "$opts" ] || return 2
  out="probe-g3-$h-$R"
  echo "### $h: env '$env', project file '$pf', ghc-options '$opts -g3'"
  [ -z "$DRY" ] || return 0
  local pfa=()
  [ "$pf" = - ] || pfa=(--project-file="$pf")
  rm -rf "$bd"
  # shellcheck disable=SC2086  # the environment is a word list on purpose
  env $env cabal build micro "${pfa[@]}" --builddir="$bd" \
    --ghc-options="$opts -g3" \
    --ghc-options="-pgma $PWD/align-as.py -fforce-recomp" || return 1
  cp "$(cabal list-bin micro "${pfa[@]}" --builddir="$bd")" "$out" || return 1
  rm -rf "$bd"
  echo "### $(date -Is) $out built, $(stat -c%s "$out") B"
}

for h in "$BASIS" "$OTHER"; do
  build "$h" || { echo "### the $h twin did not build"; exit 1; }
done
