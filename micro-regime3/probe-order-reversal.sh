#!/bin/bash
# The open item at README's "The basis half carries the wider class floor":
# a SECOND class reversed, which is what the entry says would retire the
# position candidate -- "A second class reversed is what would, and it is
# the same measurement the level half wants -- one run of two processes
# answering both."
#
# The precedent is the measurement of 2026-08-23 on `slice`: the pair run
# again with the halves' order reversed, on the same binaries, the same
# switches and the same evening. Both halves of that reading followed the
# HALF and not the position -- g912 faster in both orders, 0.9937 running
# second and 0.9878 running first, and g912 carrying the wider floor in
# both, 6.01% against 3.30% second and 3.41% against 1.79% first. That is
# one class of eight on one run of four, which weakens the position
# candidate without retiring it. This takes four more classes.
#
# WHY BOTH ORDERS HERE AND NOT JUST THE REVERSED ONE: Run 26 ran ghead
# first throughout, this morning. Comparing tonight's reversed order
# against this morning's processes would confound the order with the
# evening, which is the one thing the 2026-08-23 precedent was careful to
# avoid by running both orders in one sitting. So each class gets four
# processes, both orders, back to back.
#
# AND WHY THE ORDERS ALTERNATE ACROSS CLASSES: run back to back, the
# second order of a class always sits later in the evening than the
# first, so an evening drift would land on one order throughout. The
# classes below alternate which order goes first, so the drift is
# balanced against the order rather than aliased with it.
#
# WANTS A QUIET MACHINE. By Run 26's own wallclock log the four classes
# cost about 7m52s, 7m52s, 7m52s and 10m29s a process, so four processes
# apiece is some two and a quarter hours.
#
# No build: run26-g912 and run26-ghead are Run 26's own halves, on disk.
#
# Artifacts $PREFIX-<class>-<slot>-<class>.{json,log}, where <slot> is
# b1/c2 for the basis-first order and c1/b2 for the control-first one, so
# the name says which half ran and where it sat. Every stage's verdict is
# appended to $LOG (probe-order-reversal.txt by default) as it lands; the last line is the
# one to wait on.
set -u
cd "$(dirname "$0")" || exit 1

BASIS=${BASIS:-./run26-g912}
CONTROL=${CONTROL:-./run26-ghead}
MAXBUSY=${MAXBUSY:-5}
# One binary pair to a PREFIX, so a second pair's blocks neither overwrite
# the first's artifacts nor interleave in its log. probe-times.sh refuses
# an OUT outside probe-*/smoke-*, so a PREFIX stays inside it.
PREFIX=${PREFIX:-probe-ord}
LOG=${LOG:-probe-order-reversal.txt}

# Class, then which order runs first. The four cheapest classes by Run
# 26's wallclock, which is what buys four of them rather than one.
CLASSES=${CLASSES:-"rev:basis bcast:control scaled:basis bcastmid:control"}

log () { echo "=== $(date -Is) $*" | tee -a "$LOG"; }

for b in "$BASIS" "$CONTROL"; do
  [ -x "$b" ] || { echo "no $b here"; exit 2; }
done

# AN UNREADABLE READING REFUSES BY NAME: `[ "" -lt 5 ]` refused too, at
# exit 2, behind `integer expression expected` and a message naming an
# empty percentage (2026-09-18, by review).
BUSY=$(./machine-busy.sh) || BUSY=
case $BUSY in ''|*[!0-9.]*) echo "machine-busy.sh gave no reading (${BUSY:-empty})"; exit 2 ;; esac
awk -v x="$BUSY" -v m="$MAXBUSY" 'BEGIN { exit !(x < m) }' \
  || { echo "machine $BUSY% busy: not a quiet window"; exit 2; }

export WILDLOG=1 SATURATE=1
log "order reversal begins: basis $BASIS md5 $(md5sum "$BASIS" | cut -d' ' -f1),\
 control $CONTROL md5 $(md5sum "$CONTROL" | cut -d' ' -f1); classes and the\
 order each starts with: $CLASSES; alarm $BUSY% busy, under the $MAXBUSY% bar"

BAD=0
stage () {  # class, binary, slot name
  local cls=$1 bin=$2 slot=$3
  log "  class $cls, slot $slot: start"
  BIN=$bin OUT=$PREFIX-$cls-$slot ./probe-times.sh "$cls"
  local rc=$?
  log "  class $cls, slot $slot: done, rc=$rc"
  [ "$rc" = 0 ] || BAD=$((BAD + 1))
}

for spec in $CLASSES; do
  cls=${spec%%:*}
  first=${spec##*:}
  log "class $cls: both orders, $first first"
  if [ "$first" = basis ]; then
    stage "$cls" "$BASIS"   b1   # basis first
    stage "$cls" "$CONTROL" c2
    stage "$cls" "$CONTROL" c1   # control first
    stage "$cls" "$BASIS"   b2
  else
    stage "$cls" "$CONTROL" c1   # control first
    stage "$cls" "$BASIS"   b2
    stage "$cls" "$BASIS"   b1   # basis first
    stage "$cls" "$CONTROL" c2
  fi
done

log "ORDER REVERSAL COMPLETE: complaints=$BAD -- read the '!!' lines of each\
 $PREFIX-*-wallclock.log anyway, then each class's floor and level in both\
 orders with ./read-run.py $PREFIX-<class>-<slot>-<class>.json --aa and\
 --pair, the question being whether the wider floor and the faster level\
 follow the HALF or the POSITION"
exit $((BAD > 0))
