#!/usr/bin/env bash
# The post-run list's step 1, over every process a run left.
#
#     ./read-all.sh run14
#
# `--selftest` and `--aa` are one invocation per process, and a paired run
# leaves eighteen of them. Nine is what a session runs when it is counting
# by hand and thinking of populations rather than processes, and the nine
# it skips are the control half's -- which since 2026-08-14 is half the
# run. This gates all of them and prints one line each.
#
# It gates and reports; it does not read. The A/A WORST CELL is a figure
# for a person, so this prints it beside each verdict rather than deciding
# on it: a failed gate invalidates that population's whole time column and
# only that one, and a pair inside the floor whose worst cell is an order
# of magnitude outside it is a finding the aggregate is hiding.
#
# That comparison is like with like, which neither the page nor `--aa`
# says outright: `aa_table` takes each pair's cells on `net`, raw only for
# the `sum-only` pair whose raw ratio IS the position test, so the cell
# printed here is the same quantity as the published net floor.
#
# Seconds, no benchmark run, safe on a busy machine -- it only reads JSONs.
#
# Both defects this has had are cases in ./check-scripts.py -- an in-situ row
# read as the A/A worst cell, and a killed run gating what landed and calling
# it clean. A fix here wants a case there first; it is what keeps the proof
# alive past the commit.
#
# The worst-cell column is checked rather than trusted: over Run 13 it puts
# `scaled` at 11.59% on scaled-super-r3, which is the figure README records
# for that run's slot from a reading taken without this script, and `rev` at
# 0.85%, the largest of that process's seven A/A lines counted by hand. Both
# reproduce under the selection below, rewritten 2026-08-17; the failure
# that rewrite is for is an `--aa` whose every twin is filtered out, where
# the old selection reported an in-situ row's 6.52% as the A/A worst and
# this one leaves the fallback to fire.

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./read-all.sh RUN      # e.g. run14"
  exit 2
fi
R="$1"

# Every JSON the run left, the gate's excluded: those are five arms over
# the shape set and not a population, so their A/A gate is not this one.
# `$R-al-*` joins the gate in the exclusion, and for the same reason: an
# alone-leg rider is one bench on one shape with no A/A pair and no
# sum-only, so gating it asserts nothing and buries the eighteen this
# driver exists to count -- Run 16 left 54 of them beside its 18.
# Case: `alone-leg-riders-are-not-populations`.
FILES=$(ls -1 "$R"-*.json 2>/dev/null \
          | grep -v -e "^$R-gate-" -e "^$R-al-")
if [ -z "$FILES" ]; then
  echo "no $R-*.json here; the run has not landed, or the name is wrong"
  exit 1
fi

# What the run MEANT to leave, off its own wallclock log, because the glob
# above sees only what landed: a run killed after nine of its eighteen
# processes leaves nine JSONs and this gated the nine and printed `every
# process gated clean` over them -- the by-hand miscount the header says
# this script exists to prevent, one stage later. `run-major.sh` logs
# `start <name>` and `done <name> rc=` per process, so its log answers the
# two questions the glob cannot: did every process that started finish
# clean, and did every one leave a JSON. A run is killed DURING a process,
# so the one that was running leaves a `start` with no `done` and both
# tests below see it. No new artifact and nothing to keep in step -- the
# run writes this log already and every run on disk carries one.
#
# What is NOT reconstructed, having been tried and refuted the same day:
# the halves' cross product, for the processes a killed run never reached
# at all. Those leave no line to read, and inferring them from halves x
# tags refuses three of the five runs on disk -- Runs 11, 12 and 13 ran
# the eight class processes on the BASIS HALF ALONE, which each of their
# `halves:` lines says and Run 14's does not. The intent moved between
# runs and only the current spelling is in `run-major.sh`, so what the log
# records is read here and never what it implies. Found 2026-08-17 by
# review, the refutation by proving the fix.
LOG="$R-wallclock.log"
if [ ! -f "$LOG" ]; then
  echo "no $LOG, so how this run ended is unknown and the glob above is"
  echo "  the only roster -- which is what lets half a run gate clean."
  echo "  Name the right run, or read its processes by hand."
  exit 1
fi
STARTED=$(awk '$3 == "start" { print $4 }' "$LOG" | grep -v -- "-gate-" \
            | sort -u)
FINE=$(awk '$3 == "done" && $5 == "rc=0" { print $4 }' "$LOG" \
         | grep -v -- "-gate-" | sort -u)
# An empty search proves nothing, and `printf '%s\n' ""` puts ONE EMPTY
# LINE into each `comm` below -- so a log this awk matches nothing in left
# UNFINISHED and LOST as whitespace, SHORT at 0, and the roster check
# passed in silence over a single JSON. That is the failure this check was
# written against, inside the check itself, and the same shape as the
# empty-LEADS guard in install-tables.sh. Measured 2026-08-17 by review:
# one log with no `start` line, one JSON, `every process gated clean`.
if [ -z "$STARTED" ]; then
  echo "no \`start\` line in $LOG, so what this run launched is unknown and"
  echo "  the glob above is the only roster -- which is what lets half a run"
  echo "  gate clean. Is this a major run's log, and is it complete?"
  exit 1
fi
LANDED=$(printf '%s\n' $FILES | sed 's/\.json$//' | sort -u)
UNFINISHED=$(comm -23 <(printf '%s\n' "$STARTED") <(printf '%s\n' "$FINE"))
LOST=$(comm -23 <(printf '%s\n' "$STARTED") <(printf '%s\n' "$LANDED"))
SHORT=0
[ -z "$(printf '%s' "$UNFINISHED$LOST" | tr -d '[:space:]')" ] || SHORT=1
if [ "$SHORT" = 1 ]; then
  echo "!! $LOG says this run is not all here, so what follows gates a part"
  echo "   of it and is not this run's reading:"
  [ -z "$(printf '%s' "$UNFINISHED" | tr -d '[:space:]')" ] \
    || echo "   started and did not finish clean:" \
       "$(printf '%s' "$UNFINISHED" | tr '\n' ' ')"
  [ -z "$(printf '%s' "$LOST" | tr -d '[:space:]')" ] \
    || echo "   started and left no JSON:" \
       "$(printf '%s' "$LOST" | tr '\n' ' ')"
  echo
fi

# run-major.sh's own complaints, which this script used to step over. It
# logs `!!` for a process whose selection came out the wrong size, and for a
# class prefix matching no bench; the first leaves `rc=0` AND a JSON, so it
# moves neither STARTED, FINE nor LANDED and every test above reads it
# clean. `run-major.sh` carries that verdict out in its exit status alone,
# which a run launched with `&` loses, so the log is the only place it
# survives -- and this script already reads the log, one field over. Found
# 2026-08-17 by review; a wrong-count process is caught by nothing else.
# Anchored on run-major.sh's own stamp. Every complaint it makes goes
# through `log ()`, so it reads `=== <date>   !! ...`; the pair note it
# quotes beside them is indented and carries no stamp, and run-gate.sh
# writes `!!` INTO that note whenever the machine check fires. Counting
# bare `!!` therefore made every run whose gate tripped that check report
# a complaint no process made, at exit 1, for ever after -- Run 16, whose
# gate fired for a deliberate change of basis area. Case:
# `quoted-note-block-is-not-a-run-complaint`.
NOISY=$(grep -c '^=== .*!!' "$LOG")
if [ "$NOISY" != 0 ]; then
  echo "!! $LOG carries $NOISY complaint(s) from the run itself:"
  grep '^=== .*!!' "$LOG" | sed 's/^/   /'
  echo
fi

BAD=0
printf '%-28s %-9s %s\n' process selftest 'A/A worst cell'
for f in $FILES; do
  tag=${f#"$R"-}; tag=${tag%.json}
  # Held in a variable and not in a scratch file, which is not a style
  # choice: this wrote to /tmp, the sandbox permits /tmp/claude and the
  # session's own directory and not that, and the redirect's failure made
  # the `if` false for every file -- so a clean run printed ten FAILs with
  # the real worst cells beside them and exited 1, the two shell errors
  # per process being the only tell and the first thing a `| tail` hides.
  # A step README calls read-only has no business needing a writable path.
  if selftest=$(./read-run.py "$f" --selftest 2>&1); then
    st=ok
  else
    st=FAIL; BAD=$((BAD + 1))
  fi
  # --aa prints a `worst cell` line under each A/A pair AND under each
  # in-situ `sum-only` row. Those are gate 3's reading and not this one, so
  # take the lines ABOVE the in-situ table's header and the largest figure
  # among them. Taking the last line instead read a `-nosum` row and called
  # it the A/A worst -- 23.50% where the A/A pairs of that process reach
  # 2.14%. Taking the least-indented lines instead, which was the repair,
  # read one whenever the A/A loop emitted nothing at all -- every twin
  # filtered out leaves the in-situ rows the least indented there are, and
  # the `(no A/A pair in this file)` fallback below never fires. The
  # section header cannot go the same way: it is the one line naming the
  # population, where an indent names a `printf` width.
  # The STATUS is read, and the stderr kept, for the reason the selftest
  # call below keeps its own: with `2>/dev/null` and no `$?`, a reader that
  # REFUSED this file produced no `worst cell` line, fell through to the
  # fallback, and printed `(no A/A pair in this file)` -- an assertion
  # ABOUT THE FILE where the truth was that the question went unanswered.
  # Every process then read as gated clean, at exit 0. Measured 2026-08-17
  # against a shadow whose `--aa` was broken outright: two processes, both
  # reported as having no A/A pair, `every process gated clean`.
  aa=$(./read-run.py "$f" --aa --brief 2>&1); aarc=$?
  worst=$(printf '%s\n' "$aa" \
            | awk '/^in-situ forcing term/ { insitu = 1 }
                   /worst cell/ && !insitu {
                     split($0, w, "worst cell ")
                     split(w[2], v, "%")
                     if (v[1] + 0 >= best + 0) { best = v[1]; s = w[2] } }
                   END { if (s) print "worst cell " s }')
  if [ "$aarc" != 0 ]; then
    worst='!! --aa REFUSED this file, so its A/A is unread'
    BAD=$((BAD + 1))
  else
    [ -n "$worst" ] || worst='(no A/A pair in this file)'
  fi
  printf '%-28s %-9s %s\n' "$tag" "$st" "$worst"
  # A failing selftest prints FAIL: lines, and this shows them -- unless it
  # never got that far, where showing only FAILs leaves a bare FAIL beside
  # `(no A/A pair in this file)` and no reason anywhere. A run file the
  # reader REFUSES says so on stderr and prints no FAIL at all, which is
  # how a ragged JSON read here as an ordinary gate failure.
  if [ "$st" != ok ]; then
    if printf '%s\n' "$selftest" | grep -q '^FAIL'; then
      printf '%s\n' "$selftest" | grep '^FAIL' | sed 's/^/    /'
    else
      printf '%s\n' "$selftest" | tail -3 | sed 's/^/    /'
    fi
  fi
  # And the refusal's own words, for the same reason: a complaint naming
  # no cause sends its reader to a clean log to look for one.
  [ "$aarc" = 0 ] || printf '%s\n' "$aa" | tail -3 | sed 's/^/    /'
done

echo
if [ "$BAD" -eq 0 ] && [ "$SHORT" = 0 ] && [ "$NOISY" = 0 ]; then
  echo "every process gated clean. The worst cells above are yours to read:"
  echo "  a pair inside the floor with a cell an order of magnitude outside"
  echo "  it is a finding, not noise, and the floor goes in the chapter head"
else
  # The processes that landed are still gated and their verdicts still
  # printed -- whether the nine that ran are sound is what says to resume
  # or to rerun -- but a partial run never reads as a clean one, which is
  # what the verdict above used to say and the exit code used to be.
  [ "$BAD" -eq 0 ] \
    || { echo "$BAD process(es) FAILED their gate -- each invalidates that"
         echo "population's whole time column and only that one"; }
  [ "$SHORT" = 0 ] \
    || { echo "and the run is not all here: the processes named at the top"
         echo "are missing, so this is a reading of what landed and not of"
         echo "$R -- finish or rerun it before any figure of it is quoted"; }
  [ "$NOISY" = 0 ] \
    || { echo "and the run complained about itself, quoted at the top: a"
         echo "process can exit 0 and leave a JSON having run the wrong"
         echo "selection, which every gate below reads as sound"; }
fi
{ [ "$BAD" -eq 0 ] && [ "$SHORT" = 0 ] && [ "$NOISY" = 0 ]; } || exit 1
