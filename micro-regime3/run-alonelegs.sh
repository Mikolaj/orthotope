#!/bin/bash
# The alone-leg riders a pair note owes with its pair (README, the Run 16
# chapter): the 24 main-set `list` alone-legs on one half's own binary, one
# bench per process, so the deflation columns can be read and the published
# tables get their clean-absolute companions.
#
#     ./run-alonelegs.sh run17 wildlog     # the control half, first
#     ./run-alonelegs.sh run17 det         # the basis half, second
#
# run16-alonelegs.sh's shape with the run and the half as arguments, since
# Run 17's halves no longer name an area. No +RTS line: every binary carries
# the one baked line since 2026-08-21, and this reads it back before anything
# runs. The environment passes through untouched, so a half that wants
# WILDLOG set gets it from the launch line, as its major processes did, and
# the driver log records whether it was. The three Provenance anchors get a
# second rep, the rest single runs read against the known multi-process draw
# band (~2%). About 15-20 min a half.
#
# Refuses to start over a previous attempt's artifacts, as run-major.sh does:
# the JSONs would be overwritten in place and nothing said. ONLY=<shape>
# restricts the sweep to one shape and skips the second reps; it is for a
# smoke run of this script and never for a recorded rider.
set -u
cd "$(dirname "$0")" || exit 1
R="${1:?usage: ./run-alonelegs.sh RUN HALF   # e.g. run17 det}"
H="${2:?usage: ./run-alonelegs.sh RUN HALF   # e.g. run17 det}"
B=./$R-$H
[ -x "$B" ] || { echo "no $B here -- $R-pair.txt has the recipe"; exit 1; }
EXISTING=$(ls -1 "$R-al-$H"-*.json "$R-al-$H"-*.log 2>/dev/null)
if [ -n "$EXISTING" ]; then
  echo "$R-$H already has alone-leg artifacts here:"
  printf '%s\n' "$EXISTING" | sed 's/^/  /'
  echo "relaunching would overwrite them in place. Move them aside first."
  exit 1
fi
exec > "$R-al-$H-driver.log" 2>&1
echo "start: $(date -Is), loadavg: $(cat /proc/loadavg)"
echo "WILDLOG=${WILDLOG-unset}"
md5sum "$B"
strings "$B" | grep -x -- '-A32m -I0 -T -M8G' \
  || echo "!! baked RTS line unread: not the one baked since 2026-08-21"
SHAPES=$("$B" --list 2>/dev/null | cut -d/ -f1 | awk '!seen[$0]++')
[ -n "$SHAPES" ] || { echo "!! --list gave nothing; wrong binary?"; exit 1;
                    }
ANCHORS="cnn-slice-c32 cifar-L2-16-c64-k3 stretch-wide-2xM"
if [ -n "${ONLY-}" ]; then
  SHAPES=$ONLY; ANCHORS=
  echo "ONLY=$ONLY: a smoke run of this script, not a rider"
fi
echo "shapes: $(echo $SHAPES | wc -w)"
BAD=0
leg() {  # leg SHAPE REP -- one process, one bench, and the count checked
  local out=$R-al-$H-$1-$2 rc nb
  "$B" -m glob "$1/list" --json "$out.json" > "$out.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "$out.log")
  [ "$rc" = 0 ] || { echo "    !! $1 $2: exit $rc"; BAD=1; }
  [ "$nb" = 1 ] || { echo "    !! $1 $2: expected 1 bench, got $nb"; BAD=1; }
  awk -v s="$1-$2:" '/^time /{print s, $2, $3; exit}' "$out.log"
}
for S in $SHAPES; do leg "$S" r1; done
for S in $ANCHORS; do leg "$S" r2; done
echo "end: $(date -Is), loadavg: $(cat /proc/loadavg)"
if [ "$BAD" = 0 ]; then echo "DONE-ALONELEGS-$R-$H"
else echo "DONE-ALONELEGS-$R-$H WITH COMPLAINTS"; fi
exit $BAD
