#!/bin/bash
# Every reading this probe's write-up needs, in one pass, so that the
# reader is run once at the end rather than a call at a time beside a
# process it would disturb. Output: probe-read.txt.
#
# A reader call is a second or two of CPU and the evening's figures are
# what a second or two of CPU on a neighbouring core is capable of moving,
# which is why this exists as a script instead of as a habit.
set -u
cd "$(dirname "$0")" || exit 1
POPS="main rev revsome slice scaled window bcast bcastmid reshape1 runs"
exec > probe-read.txt 2>&1
echo "===================== probe-read, $(date -Is)"
echo
echo "===================== 0. the reader's own invariants, per JSON"
for p in $POPS; do
  [ -e "probe-bangtime-$p.json" ] || { echo "-- probe-bangtime-$p.json absent"; continue; }
  echo "--- probe-bangtime-$p"; ./read-run.py "probe-bangtime-$p.json" --selftest 2>&1 | tail -3
done
for f in probe-runlen-disp-runs probe-runlen-ghead-runs probe-runlen-nospill-runs; do
  [ -e "$f.json" ] || { echo "-- $f.json absent"; continue; }
  echo "--- $f"; ./read-run.py "$f.json" --selftest 2>&1 | tail -3
done
echo
echo "===================== 1. did the BOX move? the machine check"
./read-run.py probe-bangtime-main.json --machine 2>&1
echo "   (exit $?)"
echo
echo "===================== 2. task 1: lib-stage2 against lib-stage1, per population"
for p in $POPS; do
  [ -e "probe-bangtime-$p.json" ] || continue
  echo "--- $p"
  ./read-run.py "probe-bangtime-$p.json" --pair lib-stage2 lib-stage1 2>/dev/null | sed -n '3,6p'
done
echo
echo "===================== 3. task 1: the same, and every other arm, against Run 21"
for p in $POPS; do
  [ -e "probe-bangtime-$p.json" ] || continue
  echo "--- $p, this probe / run21-g912-$p"
  ./read-run.py "probe-bangtime-$p.json" --compare "run21-g912-$p.json" 2>/dev/null | sed -n '3,60p'
done
echo
echo "===================== 4. task 1: each population's own floor"
for p in $POPS; do
  [ -e "probe-bangtime-$p.json" ] || continue
  echo "--- $p"
  ./read-run.py "probe-bangtime-$p.json" --aa --brief 2>/dev/null | grep -E '^[a-z].*aa|^ +9|worst cell' | head -12
done
echo
echo "===================== 5. task 2: the crossover, and the two others on the same class"
for a in "lib-stage2 lib-stage1" "lib-stage2-concat lib-stage1" \
         "canon-memcpy-r2 canon-vecdims" \
         "mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims-add-in-leaf-down" \
         "mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims-add-in-leaf-u2-down"; do
  echo "--- $a on probe-bangtime-runs"
  ./read-run.py probe-bangtime-runs.json --pair $a --per-shape 2>/dev/null | sed -n '3,13p'
done
echo
echo "===================== 6. task 2: the dispatch arm, on each compiler"
for f in probe-runlen-disp-runs probe-runlen-ghead-runs; do
  [ -e "$f.json" ] || { echo "-- $f.json absent"; continue; }
  for a in "lib-stage2-disp lib-stage1" "lib-stage2-disp lib-stage2" \
           "lib-stage2-disp lib-stage2-concat" "lib-stage2 lib-stage1"; do
    echo "--- $a on $f"
    ./read-run.py "$f.json" --pair $a --per-shape 2>/dev/null | sed -n '3,13p'
  done
  echo "--- $f floor"
  ./read-run.py "$f.json" --aa --brief 2>/dev/null | grep -E 'aa-|worst cell' | head -8
done
echo
echo "===================== 7. task 2: -u2 against -down in the spill-free binary"
if [ -e probe-runlen-nospill-runs.json ]; then
  for a in "mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims-add-in-leaf-down" \
           "mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims-add-in-leaf-u2-down" \
           "mut-odo-vecdims-add-in-leaf-down mut-odo-vecdims-add-in-leaf"; do
    echo "--- $a, --corr=insitu"
    ./read-run.py probe-runlen-nospill-runs.json --corr=insitu --pair $a --per-shape 2>/dev/null | sed -n '3,13p'
  done
  echo "--- its floor, --corr=insitu"
  ./read-run.py probe-runlen-nospill-runs.json --corr=insitu --aa --brief 2>/dev/null | grep -E 'aa-|worst cell' | head -8
else
  echo "-- probe-runlen-nospill-runs.json absent"
fi
echo
echo "===================== 7b. the list consumer under each stage, which calls the same fill"
for p in main rev runs; do
  [ -e "probe-bangtime-$p.json" ] || continue
  echo "--- liblist-stage2 / liblist-stage1 on $p"
  ./read-run.py "probe-bangtime-$p.json" --pair liblist-stage2 liblist-stage1 --per-shape 2>/dev/null | sed -n '3,13p'
done
echo
echo "===================== 7c. what moved at all: every arm past 5% against Run 21"
for p in main rev bcast runs; do
  [ -e "probe-bangtime-$p.json" ] || continue
  echo "--- $p"
  ./read-run.py "probe-bangtime-$p.json" --compare "run21-g912-$p.json" --movers 5 2>/dev/null | sed -n '3,40p'
done
echo
echo "===================== 8. the per-shape ratios behind population 2"
for p in main rev bcast bcastmid; do
  [ -e "probe-bangtime-$p.json" ] || continue
  echo "--- $p"
  ./read-run.py "probe-bangtime-$p.json" --pair lib-stage2 lib-stage1 --per-shape 2>/dev/null | sed -n '3,32p'
done
echo
echo "===================== done $(date -Is)"
