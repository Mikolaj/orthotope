#!/bin/bash
# The alone-leg riders a pair note owes with its pair (README, the Run 16
# chapter): the 24 main-set `list` alone-legs on one half's own binary, one
# bench per process, so the deflation columns can be read and the published
# tables get their clean-absolute companions.
#
#     ./run-alonelegs.sh run18 g914        # the control half, first
#     ./run-alonelegs.sh run18 g912        # the basis half, second
#
# THE SECOND ARGUMENT IS A HALF'S NAME AND NOT ITS ROLE, so which of the two
# is the basis is the PAIR NOTE's to say and never this comment's. It used
# to name Run 17's halves here, and named them the wrong way round -- Run
# 17's basis is `wildlog` and its control `det`, where the lines above read
# them the other way -- which cost nothing only because the pair note is
# authoritative and was read first. Run 18's halves are above because they
# are this file's next caller; a reader of a later run substitutes.
#
# Run 16's own one-off rider script generalised, the run and the half as
# arguments, since Run 17's halves no longer name an area. That one-off is
# deleted: it was gitignored by `run[0-9]*` and so never tracked, which is
# how a near-twin sat here unversioned. No +RTS line: every binary carries
# the one baked line since 2026-08-21, and this reads it back before anything
# runs, refusing a half without it. The environment passes through untouched,
# so a half that wants WILDLOG set gets it from the launch line, as its major
# processes did, and the driver log records whether it was. The three Provenance
# anchors get a second rep, the rest single runs read against the known
# multi-process draw band (~2%). About 15-20 min a half.
#
# Refuses to start over a previous attempt's artifacts, as run-major.sh does:
# the JSONs would be overwritten in place and nothing said. ONLY=<shape>
# restricts the sweep to one shape and skips the second reps; it is for a
# smoke run of this script and never for a recorded rider. SAT=<dose> takes
# the legs through the saturating preamble (SATURATE=<dose> for every leg,
# on a binary carrying it) and suffixes the artifacts -sat, so a half's
# clean legs and its saturated legs sit side by side -- the two columns of
# the deflation decomposition Run 18 registers. SATURATE_BY passes through
# with it: unset is the roster's own sprayer, `spray` the pure pinned burst.
set -u
cd "$(dirname "$0")" || exit 1
R="${1:?usage: ./run-alonelegs.sh RUN HALF   # e.g. run17 det}"
H="${2:?usage: ./run-alonelegs.sh RUN HALF   # e.g. run17 det}"
B=./$R-$H
SUF=${SAT:+-sat}               # artifacts of saturated legs carry it
[ -x "$B" ] || { echo "no $B here -- $R-pair.txt has the recipe"; exit 1; }
EXISTING=$(ls -1 "$R-al-$H$SUF"-*.json "$R-al-$H$SUF"-*.log 2>/dev/null)
# THE CLEAN SWEEP'S GLOB WOULD OTHERWISE TAKE THE SATURATED LEGS. `-sat`
# is a suffix on the half's name, so with SUF empty `$R-al-$H-*` matches
# `$R-al-$H-sat-*` too, and a clean sweep run after a saturated one was
# refused over artifacts that are not its own -- the same over-matching
# prefix glob install-tables.sh names for a half whose name begins with
# the basis's plus a hyphen. Run 18 runs clean first and saturated second,
# so the documented order never met it; a rerun of either half's clean
# legs would have. Found 2026-08-22 by review. Case:
# `clean-legs-are-not-the-saturated-ones`.
#
# Guarded on EXISTING being non-empty because `printf '%s\n' ""` writes ONE
# EMPTY LINE, which `grep -v` passes through and `[ -n ]` then reads as an
# artifact -- the same empty-search trap read-all.sh records.
if [ -z "$SUF" ] && [ -n "$EXISTING" ]; then
  EXISTING=$(printf '%s\n' "$EXISTING" | grep -v "^$R-al-$H-sat-")
fi
if [ -n "$EXISTING" ]; then
  echo "$R-$H already has alone-leg artifacts here:"
  printf '%s\n' "$EXISTING" | sed 's/^/  /'
  echo "relaunching would overwrite them in place. Move them aside first."
  exit 1
fi
# Refused and not merely said: this echoed and went on, the one check here
# that set no status, so a half without the line ran its legs at the
# default nursery under a DONE line with no complaint. Found 2026-08-22 by
# review. And refused BEFORE the redirect below, so a refused attempt
# leaves no driver log for the relaunch guard above to read as a previous
# one. Case: `alonelegs-refuses-an-unbaked-half`.
"$B" +RTS --info 2>/dev/null | grep -q 'with-rtsopts.*-A32m -I0 -T -M8G' \
  || { echo "!! baked RTS line unread: not the one baked since 2026-08-21,"
       echo "   so every leg would run at the default nursery; wrong binary?"
       exit 1; }
exec > "$R-al-$H$SUF-driver.log" 2>&1
echo "start: $(date -Is), loadavg: $(cat /proc/loadavg)"
echo "WILDLOG=${WILDLOG-unset} SAT=${SAT-unset}"
md5sum "$B"
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
  local out=$R-al-$H$SUF-$1-$2 rc nb
  env ${SAT:+SATURATE=$SAT} "$B" -m glob "$1/list" --json "$out.json" \
    > "$out.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "$out.log")
  [ "$rc" = 0 ] || { echo "    !! $1 $2: exit $rc"; BAD=1; }
  [ "$nb" = 1 ] || { echo "    !! $1 $2: expected 1 bench, got $nb"; BAD=1; }
  [ -z "$SUF" ] || grep -q '^@@saturate ' "$out.log" \
    || { echo "    !! $1 $2: no @@saturate line -- binary without it?"; BAD=1; }
  awk -v s="$1-$2:" '/^time /{print s, $2, $3; exit}' "$out.log"
}
for S in $SHAPES; do leg "$S" r1; done
for S in $ANCHORS; do leg "$S" r2; done
echo "end: $(date -Is), loadavg: $(cat /proc/loadavg)"
if [ "$BAD" = 0 ]; then echo "DONE-ALONELEGS-$R-$H"
else echo "DONE-ALONELEGS-$R-$H WITH COMPLAINTS"; fi
exit $BAD
