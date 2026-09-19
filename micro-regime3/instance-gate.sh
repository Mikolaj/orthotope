#!/usr/bin/env bash
# The instance gate, run list step 16a since 2026-09-18: does a half LAUNCH
# from a slow instance? A binary's code frames are drawn when its file
# instance is first read and held while the file stays cached, and a draw
# reads 7 to 15 percent slower than a byte-identical copy on the same cell
# in one run of every few -- README's placement section, Run 33's basis and
# Run 34's, whose mounted instance still read 1.10 of a fresh copy a day and
# a half later, untouched. So the draw is a property of the instance, and
# one reading per launch gates it. Each half's launch instance is timed
# against a fresh copy beside it on ONE cell, cycles an iteration as `-n 2N`
# less `-n N` over N under perf, alternated a b b a a b b a; when the launch
# instance reads slower than the copy by more than INSTANCE_BAR percent
# (default 5) the copy is swapped in under the launch name and the slow one
# parked as `.slow`, which HOLDS its frames: page shuffling is off on this
# box, so a freed block is the likeliest thing the next copy gets, and the
# slow one is kept until the deletion offer, post-run step 11, never freed
# before the swap. A copy slower than the launch instance is discarded and the
# launch instance stands. Two slow draws are indistinguishable here and
# pass; the bar is coarse by the instrument, repeats of one instance under
# this form parting by up to eight percent on a quiet box (README, the open
# list), so a three percent term passes and what is caught is the draw
# that has moved a run's figures.
#
#     ./instance-gate.sh RUN            # both halves, from the note's HALVES line
#
# Exit 0 when every half is level or has been swapped, or when there is no
# instance to gate: no mount -- WHICH IS THE ORDINARY CASE since the owner
# suspended hugebin/ on 2026-09-19, so this gate normally skips itself and
# the run list's step 16a is suspended with it -- or a half that is no ELF
# binary, which is the corpus's stub. Exit 1 when a half could not be tested -- hugebin/ mounted
# read-only, perf missing, a copy refused -- which run-evening.sh records
# as a complaint and goes on from, the launch instance then UNTESTED and
# said so. Exit 2 on usage.
#
# INSTANCE_CELL and INSTANCE_N pick the cell, by default
# scaled-rank1-m1/mut-odo-vecdims-add-in-leaf-u1 at 4000, the cell the Run
# 34 instance was proved on; a half whose roster lacks the cell is a perf
# failure here and a complaint there. Its processes are not the run's, so
# run-evening.sh strips WILDLOG before calling. Two hooks for the cases:
# INSTANCE_DIR names the directory the instances live in and wants no
# mount, and INSTANCE_FAKE=A,B hands back A and B cycles an iteration for
# the launch instance and the copy instead of running either.
set -u
cd "$(dirname "$0")" || exit 2
[ $# -eq 1 ] || { echo "usage: ./instance-gate.sh RUN    # both halves, one cell each"; exit 2; }
R=$1
HALVES=$(./pair-halves.sh "$R") || exit 1
eval "$HALVES"
DIR=${INSTANCE_DIR:-hugebin}
CELL=${INSTANCE_CELL:-scaled-rank1-m1/mut-odo-vecdims-add-in-leaf-u1}
N=${INSTANCE_N:-4000}
BAR=${INSTANCE_BAR:-5}
if [ -z "${INSTANCE_DIR:-}" ] && ! mountpoint -q hugebin 2>/dev/null; then
  echo "instance gate: hugebin/ is not mounted, so the halves launch from" \
       "disk and there is no instance to gate (README, the placement section)"
  exit 0
fi

TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT
FAKE=
count () {  # count BIN ITERS -> "cycles instructions", user space, or fails
  if [ -n "${INSTANCE_FAKE:-}" ]; then
    echo "$(( FAKE * $2 )) $(( 1000 * $2 ))"; return 0
  fi
  perf stat -x, -e cycles:u,instructions:u -o "$TMP" \
    "$1" classes -m glob "$CELL" -n "$2" > /dev/null 2>&1 || return 1
  echo "$(grep ',cycles:u' "$TMP" | cut -d, -f1) $(grep ',instructions:u' "$TMP" | cut -d, -f1)"
}
per_iter () {  # per_iter BIN -> "cycles/iter instructions/iter", differenced
  local one two
  one=$(count "$1" "$N") || return 1
  two=$(count "$1" $((2 * N))) || return 1
  set -- $one $two
  [ -n "$1" ] && [ -n "$3" ] || return 1
  echo "$(( ($3 - $1) / N )) $(( ($4 - $2) / N ))"
}
median4 () { printf '%s\n' "$@" | sort -n | awk '{a[NR]=$1} END{printf "%d", (a[2]+a[3])/2}'; }

RC=0
for h in $OTHER $BASIS; do
  if [ -n "${INSTANCE_DIR:-}" ]; then
    B=$DIR/$R-$h
    [ -x "$B" ] || { echo "instance gate $h: no $B to gate"; RC=1; continue; }
  else
    B=$(./half-bin.sh "$R" "$h" 2>/dev/null) \
      || { echo "instance gate $h: half-bin.sh refuses ./$R-$h"; RC=1; continue; }
    case $B in
      hugebin/*) ;;
      *) echo "instance gate $h: $B launches from disk, no ELF binary being" \
              "on the mount for it; nothing to gate"; continue ;;
    esac
  fi
  G=$B.gate
  rm -f "$G"
  if ! cp "$B" "$G" 2>/dev/null; then
    echo "instance gate $h: cannot draw a second copy beside $B -- $DIR" \
         "read-only? (sudo mount -o remount,rw hugebin) -- so the launch" \
         "instance is UNTESTED"
    RC=1; continue
  fi
  A=(); C=(); AI=; CI=; ok=1
  for v in a b b a a b b a; do
    FAKE=${INSTANCE_FAKE:-}
    case $v in
      a) bin=$B; FAKE=${FAKE%%,*} ;;
      b) bin=$G; FAKE=${FAKE##*,} ;;
    esac
    if ! out=$(per_iter "$bin"); then
      echo "instance gate $h: perf stat gave no reading on $bin for" \
           "$CELL -n $N (perf on PATH? the cell in this half's roster?);" \
           "the launch instance is UNTESTED"
      ok=0; break
    fi
    set -- $out
    case $v in a) A+=("$1"); AI=$2 ;; b) C+=("$1"); CI=$2 ;; esac
  done
  if [ "$ok" = 0 ]; then rm -f "$G"; RC=1; continue; fi
  MA=$(median4 "${A[@]}"); MC=$(median4 "${C[@]}")
  RATIO=$(awk -v a="$MA" -v c="$MC" 'BEGIN{printf "%.4f", a/c}')
  echo "instance gate $h: $CELL -n $N, cycles an iteration --" \
       "launch $B $(IFS=,; echo "${A[*]}") median $MA;" \
       "copy $(IFS=,; echo "${C[*]}") median $MC; launch/copy $RATIO;" \
       "instructions $AI against $CI"
  if [ "$AI" != "$CI" ] && awk -v a="$AI" -v c="$CI" 'BEGIN{d=a-c; if (d<0) d=-d; exit !(d/c > 0.001)}'; then
    echo "instance gate $h: the two ran DIFFERENT work, $AI against $CI" \
         "instructions an iteration, which two copies of one file cannot;" \
         "read $CELL's log before believing the ratio"
    RC=1
  fi
  if awk -v r="$RATIO" -v bar="$BAR" 'BEGIN{exit !(r > 1 + bar / 100)}'; then
    if mv "$B" "$B.slow" && { mv "$G" "$B" || { mv "$B.slow" "$B"; false; }; }; then
      echo "instance gate $h: REDRAWN -- the launch instance read slower" \
           "than a fresh copy by more than $BAR%; the copy now launches as" \
           "$B and the slow draw is parked as $B.slow, holding its frames" \
           "until the deletion offer, post-run step 11"
    else
      echo "instance gate $h: the swap failed; read $DIR by hand"
      RC=1
    fi
  elif awk -v r="$RATIO" -v bar="$BAR" 'BEGIN{exit !(r < 1 - bar / 100)}'; then
    rm -f "$G"
    echo "instance gate $h: level -- the fresh copy was the slow draw, by" \
         "more than $BAR%, and is discarded; the launch instance stands"
  else
    rm -f "$G"
    echo "instance gate $h: level within $BAR%; the launch instance stands"
  fi
done
exit "$RC"
