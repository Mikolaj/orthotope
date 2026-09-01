#!/bin/bash
# Read the fill pair WITHIN each half and never across it.
#
#     ./probe-fillpair-read.sh main
#
# The halves differ in one source change, but they are two builds, and
# task 5 measured what that costs: `-down`, which the change does not
# touch and whose counted work is identical between them, moved 15.13% in
# TIME. So an absolute of one half against the other prices the layout
# and not the fill, and the only sound reading is an arm against an arm
# inside one binary -- which is what `--pair` gives.
#
# The changed arms are `-u2` (the shipped fill) and `-u2-down`; the
# unchanged ones are `-down` and `-add-in-leaf`, the un-unrolled leaf.
# So a changed-over-unchanged ratio moving between the halves IS the
# change, and an unchanged-over-unchanged one moving is the layout term
# it has to be read against. Both are printed; the second is the control
# and reading the first without it is what this file exists to prevent.
set -u
cd "$(dirname "$0")" || exit 1
POP=${1:?usage: ./probe-fillpair-read.sh POPULATION}
U=mut-odo-vecdims-add-in-leaf-u2
PAIRS="$U:mut-odo-vecdims-add-in-leaf-down
$U:mut-odo-vecdims-add-in-leaf
lib-stage1:mut-odo-vecdims-add-in-leaf-down
$U-down:mut-odo-vecdims-add-in-leaf-down
mut-odo-vecdims-add-in-leaf-down:mut-odo-vecdims-add-in-leaf
lib-stage2:lib-stage1"
for h in A B; do
  f=probe-fill$h-$POP.json
  [ -e "$f" ] || { echo "!! $f absent -- that half has not run"; exit 1; }
done
printf '%-62s %10s %10s %10s\n' "arm / arm  (the last two are CONTROLS)" "A" "B" "B/A"
printf '%s\n' "$PAIRS" | while IFS=: read -r a b; do
  [ -n "$a" ] || continue
  va=$(./read-run.py "probe-fillA-$POP.json" --pair "$a" "$b" 2>/dev/null \
       | awk '/^'"$a"' \/ /{print $4}')
  vb=$(./read-run.py "probe-fillB-$POP.json" --pair "$a" "$b" 2>/dev/null \
       | awk '/^'"$a"' \/ /{print $4}')
  # Joined on `:` so that ONE empty side is caught: `"$va$vb"` read as
  # a number whenever the other side was one, and python then divided
  # by nothing. Found 2026-09-01 by review.
  case "$va:$vb" in
    *[!0-9.:]*|:*|*:) printf '%-62s %10s %10s %10s\n' "$a / $b" "${va:-?}" "${vb:-?}" "--" ;;
    *) printf '%-62s %10s %10s %10s\n' "$a / $b" "$va" "$vb" \
         "$(python3 -c "print('%.4f' % ($vb/$va))")" ;;
  esac
done
