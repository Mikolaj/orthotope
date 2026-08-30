#!/bin/bash
# The second half of the quiet evening, unattended: task 2's three
# processes and then `reshape1`, which is last because it is the one
# population neither task names and so the one to lose if the night runs
# short.
#
# RUN IT ONLY AFTER THE THRESHOLD RULE HAS BEEN APPLIED to the re-take
# probe-evening-a.sh took -- probe-times-note.txt has the rule, and it is
# the evening's only decision. A `lib-stage2-disp` cut to a crossover the
# class did not measure is an arm timed against nothing.
#
# The two dispatch processes are the same question on two compilers, which
# the task asks for outright: a compiler can move a crossover, so a
# threshold read on one compiler alone is a threshold nobody has checked.
# The spill-free process is `-u2` against `-down` and wants no second
# compiler, its figures being a diagnostic whatever they say.
#
# About an hour and fifty. Wait on the last line below.
set -u
cd "$(dirname "$0")" || exit 1
export WILDLOG=1 SATURATE=1
BIN=./probe-disp-g912  OUT=probe-runlen-disp    ./probe-times.sh runs || echo "!! disp g912 complained"
BIN=./probe-disp-ghead OUT=probe-runlen-ghead   ./probe-times.sh runs || echo "!! disp ghead complained"
BIN=./probe-nospill-g912 OUT=probe-runlen-nospill ./probe-times.sh runs || echo "!! nospill complained"
./probe-times.sh reshape1 || echo "!! reshape1 complained"
echo "=== $(date -Is) EVENING B COMPLETE" | tee -a probe-bangtime-wallclock.log
