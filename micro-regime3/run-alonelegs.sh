#!/bin/bash
# The alone-leg riders a pair note owes with its pair (README, the Run 16
# chapter): the 24 main-set `list` alone-legs on one half's own binary, one
# bench per process, so the deflation columns can be read and the published
# tables get their clean-absolute companions.
#
#     ./run-alonelegs.sh run19 ghead       # the control half, first
#     ./run-alonelegs.sh run19 g912        # the basis half, second
#
# THE SECOND ARGUMENT IS A HALF'S NAME AND NOT ITS ROLE, so which of the two
# is the basis is the PAIR NOTE's to say and never this comment's. It used
# to name Run 17's halves here, and named them the wrong way round -- Run
# 17's basis is `wildlog` and its control `det`, where the lines above read
# them the other way -- which cost nothing only because the pair note is
# authoritative and was read first. Run 19's halves are above because they
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
# multi-process draw band (~2%). About two and a half minutes a half clean
# and five and a half saturated, measured over Run 21's four 27-leg sweeps
# on 2026-08-29. It read "15-20 min a half" until then, which is a
# duration a session PLANS the quiet window around: the figure was six
# times the truth and had the riders budgeted an hour.
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
[ $# -ge 2 ] || { echo "usage: ./run-alonelegs.sh RUN HALF   # e.g. run17 det"
                  exit 2; }   # 2, "did not run", as every usage path here
R="$1"
H="$2"
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
# The listing likewise, before the redirect: refused after it, this left
# a driver log for the relaunch guard to read as a previous attempt.
# Case: `alonelegs-refuses-a-listless-half`.
SHAPES=$("$B" --list 2>/dev/null | cut -d/ -f1 | awk '!seen[$0]++')
[ -n "$SHAPES" ] || { echo "!! --list gave nothing; wrong binary?"; exit 1; }
# AND THE MACHINE, which is what every guard above is blind to: these legs
# are TIMED, one bench a process, so a box doing something else times the
# something else. Run list step 16 is this alarm before the sequence and
# the riders at step 19 had none, which is how four legs came to be
# launched onto a box whose owner had taken it back and had to be thrown
# away (2026-08-26). NOT A LOADAVG: the one-minute figure still carries
# the sequence that has just ended, so it would refuse the launch the
# procedure asks for -- riders follow the sequence -- while passing a box
# that got busy a minute ago. The reading is machine-busy.sh's, shared
# with run-evening.sh. MAXBUSY overrides in percent, and an ONLY= smoke
# run skips it, being declared not a rider.
# Case: `alonelegs-refuses-a-busy-machine`.
#
# BROKEN ON PURPOSE 2026-08-26, on the busy box that occasioned it, and
# this is what it said rather than what it was meant to say. As a rider it
# printed `the machine is busy: 10.6% of its CPUs non-idle over two
# seconds, against a 5% bar`, exited 1 and wrote no artifact. With
# MAXBUSY=100 on the same box it went past and into the sweep, which is
# the pass branch. With ONLY=cnn-slice-c32 it printed `machine: 11.7% busy
# at launch, against a 5% bar` and ran, which is the measure-but-do-not-
# refuse branch. The driver log's own loadavg line read 2.36 beside that
# 11.7%, which is the history contamination the paragraph above claims.
BUSY=$(./machine-busy.sh)
# MEASURED ALWAYS AND REFUSED ONLY FOR A RIDER, so that an ONLY= smoke run
# exercises the reading itself -- the half of this that can go wrong
# silently -- and skips only the refusal.
if [ -z "${ONLY-}" ]; then
  if awk -v x="$BUSY" -v m="${MAXBUSY:-5}" 'BEGIN{exit !(x>m)}'; then
    echo "!! the machine is busy: ${BUSY}% of its CPUs non-idle over two"
    echo "   seconds, against a ${MAXBUSY:-5}% bar. These legs are timed one"
    echo "   bench to a process, so what ran here would be the intruder and"
    echo "   not the leg. Nothing ran and no artifact was written; rerun on a"
    echo "   quiet box, or set MAXBUSY to say what you are accepting."
    exit 1
  fi
fi
exec > "$R-al-$H$SUF-driver.log" 2>&1
echo "machine: ${BUSY-skipped}% busy at launch, against a ${MAXBUSY:-5}% bar"
echo "start: $(date -Is), loadavg: $(cat /proc/loadavg)"
echo "WILDLOG=${WILDLOG-unset} SAT=${SAT-unset}"
md5sum "$B"
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
