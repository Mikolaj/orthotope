#!/usr/bin/env bash
# The post-run list's step 1, over every process a run left: the gates
# behind the rule in one README section, its title whole on one line so
# a grep for it lands here too --
# Which population answers a question, and how to ask all of them
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
# That comparison is like with like, which neither the README nor `--aa`
# says outright: `aa_table` takes each A/A pair's cells on `net`, so the
# cell printed here is the same quantity as the published net floor. The
# `sum-only` pair `--aa` prints beside them is NOT in it: that one is
# compared raw, its raw ratio being the position test, and `aa_pairs`
# keeps it out of the floor for the same reason -- so a sum-only cell
# wider than every A/A cell used to be printed here as the A/A worst, and
# on Run 11's slice process it tied the widest A/A cell and the tie went
# to it. Case: `aa-worst-cell-is-not-the-sum-only-pair`.
#
# It also gates THE PLATEAU, where a run carries one: every process's own
# `@@saturate` reading inside a band of the run's own, which is Run 18's
# registration 5. That gate is over the LOGS and every other one here is
# over a JSON, which is the reason it stands apart at the top rather than
# joining the per-process table -- and a run without the preamble carries
# no such line and is not gated on it, in silence, an absent instrument
# being no kind of failure.
#
# Seconds, no benchmark run, safe on a busy machine -- it only reads JSONs
# and logs.
#
# Its defects are cases in defects.py, the first two an in-situ row
# read as the A/A worst cell and a killed run gating what landed and calling
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
  echo "usage: ./read-all.sh RUN [--brief-facts] [--for-brief]  # e.g. run14"
  echo "  --brief-facts  and derive, from the same readings, the facts the"
  echo "                 checker's brief states in prose for its two agents"
  echo "  --for-brief    and print those facts already written into the"
  echo "                 brief's items 5 and 6, to paste over them; implies"
  echo "                 --brief-facts. What it cannot derive it marks"
  echo "                 <yours>, as the pair note's --fill-in does"
  exit 2
fi
R=""
BRIEF=0
FORBRIEF=0
# Refused rather than absorbed: an unknown flag taken and ignored is this
# tree's silent-option family, and a `--brief-facts` swallowed as a second
# RUN would gate nothing and say `every process gated clean`.
for a in "$@"; do
  case "$a" in
    --brief-facts) BRIEF=1 ;;
    --for-brief) BRIEF=1; FORBRIEF=1 ;;
    -*) echo "read-all.sh: unknown option $a" >&2; exit 2 ;;
    *) if [ -z "$R" ]; then R="$a"
       else echo "read-all.sh: one run at a time, not $R and $a" >&2; exit 2
       fi ;;
  esac
done
if [ -z "$R" ]; then
  echo "read-all.sh: name the run, e.g. ./read-all.sh run14" >&2
  exit 2
fi

# Every JSON the run left, the gate's excluded: those are five arms over
# the shape set and not a population, so their A/A gate is not this one.
# `$R-al-*` joins the gate in the exclusion, and for the same reason: an
# alone-leg rider is one bench on one shape with no A/A pair and no
# sum-only, so gating it asserts nothing and buries the eighteen this
# driver exists to count -- Run 16 left 54 of them beside its 18.
# Case: `alone-leg-riders-are-not-populations`.
# shellcheck disable=SC2010  # the names here are the drivers' own, alphanumeric
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

# THE PLATEAU, registration 5's gate: every recorded process asserts the
# in-process state it measured in, and this is where the run's own band is
# read over them. `run-major.sh` counts the line per process, which is a
# process that ran without the dose; this asks the other question, whether
# the processes that DID assert one asserted the same one -- a process
# outside the band having measured somewhere else, and its figures being
# read before they are quoted rather than after.
#
# A run without the preamble carries no such line and is not gated here,
# which is every run up to and including Run 17. Silent about the absence
# on purpose: an absent instrument is not a failed one, and this driver
# already refuses a run that is not all here.
#
# The band is over the VICTIM reading, the fixed-iteration `list` the
# preamble times after collecting, and 5% is loose against the 0.9% ten
# processes of one alone leg span and tight against the 14% an unsaturated
# process reads below a saturated one (the dose measurements, README's Run
# 18 entry). PLATEAU_BAND overrides it for a run whose own spread is known
# to be wider.
#
# Over the RECORDED processes' logs and no others, which is the same
# exclusion FILES makes above and for the same reasons: the gate's halves
# are five arms and not a population, and an alone leg is one bench in its
# own process. `run-major.sh` echoes each reading into the wallclock log
# too, indented behind its process's name, so that copy does not start the
# line and is not counted twice here.
PLATEAU_BAND=${PLATEAU_BAND:-5}
# shellcheck disable=SC2010  # as above
PLOGS=$(ls -1 "$R"-*.log 2>/dev/null \
          | grep -v -e "^$R-gate-" -e "^$R-al-" -e "^$R-wallclock\.log$")
NPLOGS=$(printf '%s\n' "$PLOGS" | grep -c .)
# The token before `ms/iter`, whatever its spelling: `show` on a Double
# writes `8.5e-2` below 0.1, and a digits-and-dot pattern dropped such a
# line in silence, the process then missing from the count below with
# nothing said. Case: `plateau-reading-in-exponent-form`.
SAT=$([ -z "$PLOGS" ] || grep -h '^@@saturate ' $PLOGS 2>/dev/null \
        | awk '{ for (i = 2; i <= NF; i++)
                   if ($i == "ms/iter") print $(i - 1) }')
# THE STATE EACH PROCESS ASSERTED, which is what the gate below reads:
# `inuse=` and `keep=` off the same line, per log, with the log's name so a
# process that differs can be named. Carried since Run 28; a run whose logs
# have neither falls back to the victim band, which the gate says.
STATEV=$([ -z "$PLOGS" ] || grep -H '^@@saturate ' $PLOGS 2>/dev/null \
  | awk -F: '{ line = $0; sub(/^[^:]*:/, "", line)
               iu = ""; kp = ""
               n = split(line, w, /[ \t]+/)
               for (i = 1; i <= n; i++) {
                 if (w[i] ~ /^inuse=/) iu = substr(w[i], 7)
                 if (w[i] ~ /^keep=/)  kp = substr(w[i], 6) }
               if (iu != "" && kp != "") print $1, iu, kp }')
# AND THE SPREAD WITHIN EACH HALF, a reading beside the run-wide one: a
# pair's two halves are its two groups here, taken off the log name, and a
# spread that is flat within each half and wide across them is the pair's
# variable and not drift. Silent where the names give no halves.
HALFSPREAD=$([ -z "$PLOGS" ] || grep -H '^@@saturate ' $PLOGS 2>/dev/null \
  | awk -F: -v r="$R" '{ nm = $1; sub("^" r "-", "", nm); sub(/-[^-]*\.log$/, "", nm)
                         line = $0; sub(/^[^:]*:/, "", line)
                         n = split(line, w, /[ \t]+/)
                         for (i = 2; i <= n; i++)
                           if (w[i] == "ms/iter" && w[i-1] + 0 > 0) {
                             v = w[i-1] + 0
                             if (!(nm in lo) || v < lo[nm]) lo[nm] = v
                             if (!(nm in hi) || v > hi[nm]) hi[nm] = v
                             c[nm]++ } }
     END { k = 0; for (h in lo) k++
           if (k < 2) exit
           for (h in lo)
             printf "  within %-8s %d process(es), %.4f to %.4f, spread %.2f%%\n",
                    h, c[h], lo[h], hi[h], 100 * (hi[h] - lo[h]) / lo[h] }')
# WHAT THE PAIR NOTE DECLARES EXPECTED, on the gate-verdict pattern: a
# pair whose VARIABLE moves what the preamble leaves resident fires the
# state gate on every process, every time, and no reading afterwards can
# make it pass -- so `STATUS: all done`, which the run chapter calls the
# one state in which a session is finished with a run, became unreachable
# for the whole of such a run. Run 31 is the case: its `-O2` half left
# 74448896 bytes in use against the plain half's 95420416, one value per
# half and none within one, disclosed in its head, its Provenance and an
# open entry, and its post-run step 1 still read NOT DONE at the end.
#
# A DECLARATION IS NOT A SUPPRESSION. It is written into the note BY HAND
# with its reason, exactly as the gate's own verdict is at run list step
# 14a, so what it costs is a sentence somebody had to mean; the block is
# still printed in full, the states still listed per process, and the
# line says the note declared it. What changes is only that a declared
# firing is a READING and not a refusal.
#     EXPECT: state           the processes will not assert one state
#     EXPECT: band            the victim's spread will pass the band
#     EXPECT: state band      both
# Absent or empty, nothing is declared and every gate is as it was.
EXPECTED=$(sed -n 's/^EXPECT: *//p' "$R-pair.txt" 2>/dev/null | tr '\n' ' ')
expects () {
  case " $EXPECTED " in *" $1 "*) return 0 ;; esac
  return 1
}

WILD_PLATEAU=0
if [ -n "$SAT" ]; then
  # Counted against the logs and not only among themselves: one reading
  # left over is lo == hi, a spread of 0.00, and `every process asserted
  # the same state` said over one process. Per log, not count against
  # count: two lines in one log beside none in another is the same number
  # twice, so the logs without a line are listed by name -- which is also
  # where a hand probe log in the run's namespace surfaces. A token that
  # is no number is counted apart: compared, `NaN` moves neither lo nor hi
  # and any band holds it. Cases: `plateau-reading-missing-from-a-process`,
  # `plateau-counted-per-log`, `plateau-reading-that-is-no-number`.
  WITHOUT=$(grep -L '^@@saturate ' $PLOGS 2>/dev/null)
  NWITHOUT=$(printf '%s\n' "$WITHOUT" | grep -c .)
  read -r NSAT NBAD LO HI SPREAD <<EOF
$(printf '%s\n' "$SAT" | awk '
    $1 !~ /^[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?$/ { nbad++; next }
    n == 0 { lo = hi = $1 + 0 }
    { n++; if ($1 + 0 < lo) lo = $1 + 0; if ($1 + 0 > hi) hi = $1 + 0 }
    END { s = (n > 0 && lo > 0) ? 100 * (hi - lo) / lo : 0
          printf "%d %d %s %s %.2f\n", n, nbad + 0, lo, hi, s }')
EOF
  if [ "$NBAD" != 0 ] || [ "$NSAT" != "$NPLOGS" ] || [ "$NWITHOUT" != 0 ]
  then
    echo "!! the plateau is not this run's: $NSAT reading(s) parsed from the"
    echo "   $NPLOGS recorded process log(s), $NBAD of the line(s) no number"
    echo "   -- a process without a reading measured in a state nobody"
    echo "   asserted, and a band over the rest is a band over a different"
    echo "   run. The lines, per process:"
    grep -H '^@@saturate ' $PLOGS 2>/dev/null | sed 's/^/   /'
    [ "$NWITHOUT" = 0 ] || echo "   log(s) with no reading:" \
                                "$(printf '%s' "$WITHOUT" | tr '\n' ' ')"
    echo
    WILD_PLATEAU=1
  else
    # THE GATE IS THE STATE AND THE VICTIM READING IS A READING, since Run
    # 29. The question this gate asks is whether every process asserted the
    # SAME in-process state; the victim's ms/iter was a proxy for it, and
    # the proxy is timed with `list`. So a pair whose variable moves `list`
    # moves the proxy and nothing else: Run 29 struck `-fspec-constr` off
    # one half, read an 11.82% spread against this 5% band, and was flat
    # WITHIN each half at 1.98% and 1.88% with `inuse` and `keep` identical
    # to the byte on all twenty-two processes. It failed a gate on its own
    # variable, and post-run step 1 could not go green for a sound run.
    # The `@@saturate` line has carried the state itself all along --
    # `inuse=` and `keep=` -- so that is what is gated now, and the victim
    # spread is printed beside it, per half where the log names give one.
    # A run whose logs predate those fields falls back to the band, which
    # is what every run up to Run 27 gets. Cases:
    # `plateau-gates-the-state-and-not-the-victim` and the control beside
    # it; the band's own cases above are unchanged.
    read -r NSTATED NSTATES <<EOF
$(printf '%s\n' "$STATEV" | awk 'NF >= 3 { n++; k[$2 " " $3] = 1 }
                                  END { m = 0; for (x in k) m++
                                        printf "%d %d\n", n + 0, m + 0 }')
EOF
    if [ "$NSTATED" != "$NSAT" ]; then
      echo "plateau: $NSAT process(es), victim $LO-$HI ms/iter, spread\
 $SPREAD%, and the state fields are not in these logs -- gated on the\
 victim against the $PLATEAU_BAND% band, as every run before Run 28 is"
      awk -v s="$SPREAD" -v b="$PLATEAU_BAND" 'BEGIN { exit !(s > b) }' \
        && { echo "!! and it is outside that band: a process outside it"
             echo "   measured in a state the others did not, so read it"
             echo "   before its figures. The readings, per process:"
             grep -H '^@@saturate ' $PLOGS 2>/dev/null | sed 's/^/   /'
             WILD_PLATEAU=1; }
      echo
    elif [ "$NSTATES" != 1 ]; then
      if expects state; then
        echo "plateau: $NSAT process(es) report $NSTATES distinct inuse/keep\
 pairs, which $R-pair.txt DECLARES expected -- a reading and not the gate"
        echo "  every A/A gate below is still WITHIN a process, which is\
 what the states parting means and what the declaration does not change"
      else
        echo "!! the processes did not assert ONE state: $NSAT process(es)"
        echo "   report $NSTATES distinct inuse/keep pairs, so they did not"
        echo "   all saturate alike and every A/A gate below is WITHIN a"
        echo "   process. The states, per process:"
      fi
      printf '%s\n' "$STATEV" | awk 'NF >= 3 { printf "   %s inuse=%s keep=%s\n", $1, $2, $3 }'
      # THE PER-HALF SPREAD IS PRINTED HERE TOO, and this is the branch
      # that wanted it most: a run whose states part by half is exactly
      # the run whose plateau has to be read per half, and until
      # 2026-09-14 this branch alone withheld it, so Run 31 hand-rolled
      # from the twenty-two `@@saturate` lines what was already computed
      # four hundred lines above.
      printf '%s\n' "$HALFSPREAD"
      echo
      expects state || WILD_PLATEAU=1
    else
      echo "plateau: $NSAT process(es) assert ONE state, inuse and keep\
 identical on every one -- the gate"
      echo "  victim $LO-$HI ms/iter, spread $SPREAD% -- a reading and not\
 the gate, the victim being timed with \`list\`"
      printf '%s\n' "$HALFSPREAD"
      awk -v s="$SPREAD" -v b="$PLATEAU_BAND" 'BEGIN { exit !(s > b) }' \
        && echo "  that spread is past the $PLATEAU_BAND% band and the state\
 is identical, which is what a pair whose variable moves \`list\` looks\
 like -- read the per-half spreads above before reading it as drift"
      echo
    fi
  fi
fi

BAD=0
FACTS=""
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
  # population, where an indent names a `printf` width. The `sum-only`
  # pair is skipped by its name: it prints above that header with the A/A
  # pairs and is not one (the header of this file). Ties go to the first
  # line and a 0.00% cell is still a cell, which is what `best` starting
  # below zero buys.
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
            | awk 'BEGIN { best = -1 }
                   /^in-situ forcing term/ { insitu = 1 }
                   /^[^ ]/ { sumonly = ($1 ~ /^sum-only/) }
                   /worst cell/ && !insitu && !sumonly {
                     split($0, w, "worst cell ")
                     split(w[2], v, "%")
                     if (v[1] + 0 > best) { best = v[1] + 0; s = w[2] } }
                   END { if (s) print "worst cell " s }')
  if [ "$aarc" != 0 ]; then
    worst='!! --aa REFUSED this file, so its A/A is unread'
    BAD=$((BAD + 1))
  else
    [ -n "$worst" ] || worst='(no A/A pair in this file)'
  fi
  printf '%-28s %-9s %s\n' "$tag" "$st" "$worst"
  # Kept for --brief-facts from the readings just taken rather than taken
  # again: the floor is the same `--aa --brief` output the worst cell came
  # from, and a second invocation could disagree with the line above it.
  FACTS="$FACTS$tag	$(printf '%s\n' "$aa" \
      | sed -n 's/.*spread of \([0-9.]*\)% (this population.*/\1/p')	$worst
"
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
if [ "$BAD" -eq 0 ] && [ "$SHORT" = 0 ] && [ "$NOISY" = 0 ] \
   && [ "$WILD_PLATEAU" = 0 ]; then
  echo "every process gated clean. The worst cells above are yours to read:"
  echo "  a pair inside the floor with a cell an order of magnitude outside"
  echo "  it is a finding, not noise, and the floor goes in the run file's head"
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
  [ "$WILD_PLATEAU" = 0 ] \
    || { echo "and its processes did not all assert one state, quoted at"
         echo "the top: every A/A gate below is WITHIN a process and so says"
         echo "nothing about a process that saturated somewhere else"; }
fi
# --brief-facts: THE BRIEF'S THIS RUN ONLY FACTS, DERIVED. Item 6 of
# checker-brief.txt states this run's figures in prose for two agents who
# arrive knowing none of them, and it is retyped every run. Run 27 retyped
# it twice, once before its intrusion was found and once after, and left
# four readings standing in the second's block: THREE of them the FIRST
# window's -- `ONE window`, `runs 0.9885` and a 2.65% plateau -- and one
# an intrusion range its own run file had already corrected. Every row below is a reading this
# driver has just taken or one line of arithmetic over the same JSONs, so
# a figure here cannot belong to a window that was thrown away.
# It is not the whole block: what the run MEANS, which registrations it
# carries and what to disbelieve are the write-up's, and the brief says so.
brief_facts () {
  BASIS=$(sed -n 's/.*; \([A-Za-z0-9]*\) is the basis.*/\1/p' "$LOG" \
            | head -1)
  echo
  echo "--- the brief's THIS RUN ONLY facts, derived; read items 5 AND 6 of"
  echo "    checker-brief.txt against these and change what disagrees ---"
  # ITEM 5's ROWS TOO, since 2026-09-13. Both items are hand-edited every
  # run and both restate the run file's head; the rows below are the ones
  # an artifact can settle, so what is left to a hand is prose rather than
  # re-derivation. Run 30 retyped the repetition fact and got it wrong in
  # four places -- it called the fourth repetition this chapter has read the
  # first -- which a row off the note's own md5s would not have done.
  NOTE="$R-pair.txt"
  if [ -f "$NOTE" ]; then
    printf '  %-14s %s\n' 'md5s' \
      "$(sed -n 's/^ *md5 \([a-z0-9]*\) *\([0-9a-f]\{32\}\)/\1=\2/p' \
           "$NOTE" | tr '\n' ' ')"
    # ANCHORED AT THE FACT BLOCK'S OWN INDENT. `^ *repetition ` matched
    # the note's PROSE first -- the sentence saying what a one-sided md5
    # row means, which opens with the word and is indented as prose --
    # and published that instead of the entry of that name, boilerplate
    # standing where a fact belongs. A note is gitignored and per-run, so
    # the indent is what names these and a line number would not.
    printf '  %-14s %s\n' 'repetition' \
      "$(sed -n '/^  repetition /,$p' "$NOTE" | head -6 \
           | sed 's/^ *repetition *//' | tr '\n' ' ' \
           | sed 's/  */ /g; s/\. .*/./')"
    # THE WHOLE SENTENCE AND NOT ITS FIRST LINE. The note WRAPS this
    # entry, and `head -1` cut it at `-- they do`, where the next line
    # reads `NOT agree`: --for-brief pastes this row into the brief as
    # prose, so the cut published the fact inverted. Joined to its
    # continuations and cut at the first full stop instead.
    printf '  %-14s %s\n' 'text' \
      "$(sed -n '/^ *\.text /,$p' "$NOTE" | head -6 | sed 's/^ *\.text *//' \
           | tr '\n' ' ' | sed 's/  */ /g; s/\. .*/./')"
  else
    printf '  %-14s %s\n' 'note' "no $NOTE, so item 5's binary rows are NOT\
 derived -- read them by hand"
  fi
  if [ -f "$R-evening-out.txt" ]; then
    MC=$(sed -n 's/^ *geomean \(.*\)/\1/p' "$R-evening-out.txt" | head -1)
    # A FIRED CHECK IS NOT A BOX MOVE until it is read against the previous
    # build of THIS recipe: Run 30's fired at +12.96% against a fingerprint
    # belonging to the other half's regime, and the box had not moved at all.
    if grep -q 'BOX MOVED' "$R-evening-out.txt"; then
      MC="$MC -- BOX MOVED, which is the check asking whether the FINGERPRINT's
                 half is this basis's recipe; read it against that recipe's
                 previous build before believing it"
    else
      MC="$MC -- did not fire"
    fi
    printf '  %-14s %s\n' 'machine check' "$MC"
  fi
  # THE VERDICT ABOVE GOVERNS THESE ROWS. A failed gate invalidates that
  # population's whole time column, a short run is a reading of what
  # landed, and a plateau that is not flat says the processes measured in
  # different states -- so the rows below are printed under any of those
  # and are not the run's facts until it is fixed. Printed and not
  # withheld: they are what shows WHAT went wrong.
  if [ "$BAD" -ne 0 ] || [ "$SHORT" != 0 ] || [ "$NOISY" != 0 ] \
     || [ "$WILD_PLATEAU" != 0 ]; then
    echo "  !! this run did NOT gate clean above, so what follows is"
    echo "     derived from processes this driver has just refused and is"
    echo "     not yet this run's facts"
  fi
  printf '  %-14s %s\n' 'processes' \
    "$(printf '%s\n' $FILES | grep -c .) gated above, from $LOG"
  # THE ABSENCE IS A ROW. Without the halves the floors cannot be labelled
  # and the bar rows cannot be built at all, and a first draft of this
  # block printed every floor as the control's and no bar row, in silence.
  # A log carrying no such clause is not hypothetical -- Runs 11 to 13
  # wrote that line another way, and a killed run may never reach it.
  [ -n "$BASIS" ] || printf '  %-14s %s\n' 'halves' \
    "no \`is the basis\` clause in $LOG, so the floors below are labelled by
                 half and the bar rows are NOT derived -- read them by hand"
  # The stamp is the SECOND field: every line here opens with `===`.
  # A SECOND WINDOW is a HOLE and not an ordering -- in any sequence every
  # process starts after the one before it finished, which is what a first
  # draft of this row counted and reported twenty times over on a run that
  # had one window. So the largest hole between one process finishing and
  # the next starting is what prints: a sequence reads in seconds and a
  # rerun taken hours later reads in hours. `date` does the arithmetic, the
  # stamps carrying an offset and a run being able to cross midnight.
  printf '  %-14s %s\n' 'windows' \
    "$(awk '$3 == "start" { print $2 }' "$LOG" | sort | head -1) to \
$(awk '$3 == "done" { print $2 }' "$LOG" | sort | tail -1), largest hole \
between one process finishing and the next starting $(awk \
  '$3 == "start" { s[$4] = $2 } $3 == "done" { d[$4] = $2 }
   END { for (p in s) if (p in d) print s[p], d[p] }' "$LOG" \
  | sort | while read -r st dn; do
      printf '%s %s\n' "$(date -d "$st" +%s)" "$(date -d "$dn" +%s)"
    done | awk 'NR > 1 { g = $1 - prev; if (g > max) max = g }
                { prev = $2 }
                END { printf "%dm", (max + 0) / 60 }') -- hours mean a \
second window"
  # The absence again: a run whose logs carry no `@@saturate` line has no
  # plateau to state, and a row that just vanished reads as a plateau
  # nobody owed. Every process since the preamble landed writes one.
  if [ -n "$SAT" ]; then
    printf '  %-14s %s\n' 'plateau' \
      "$NSAT process(es), victim $LO-$HI ms/iter, spread $SPREAD%"
  else
    printf '  %-14s %s\n' 'plateau' \
      "no \`@@saturate\` line in these logs, so there is none to state"
  fi
  # SORTED, because the row exists to be read against a paragraph: awk's
  # hash order put `rev other` before `main basis` and left the reader
  # hunting for each population in a line of twenty-two.
  printf '  %-14s %s\n' 'floors' \
    "$(printf '%s' "$FACTS" | awk -F'\t' -v b="$BASIS" \
        '{ split($1, t, "-"); half = t[1]; pop = substr($1, length(half) + 2)
           lab = (b == "") ? " " half : (half == b ? " basis" : " other")
           printf "%s%s %s%%\n", pop, lab, $2 }' \
       | LC_ALL=C sort | tr '\n' ';' | sed 's/;/; /g')"
  printf '  %-14s %s\n' 'A/A past 5%' \
    "$(printf '%s' "$FACTS" | awk -F'\t' \
        '$3 ~ /worst cell/ { split($3, w, "worst cell "); split(w[2], v, "%")
                            if (v[1] + 0 > 5) printf "%s %s%%; ", $1, v[1] }')"
  echo "  list vs the 0.7% bar, per population, basis over other:"
  for pop in $(printf '%s' "$FACTS" | awk -F'\t' \
                 '{ split($1, t, "-"); print substr($1, length(t[1]) + 2) }' \
               | sort -u); do
    a="$R-$BASIS-$pop.json"
    b=$(printf '%s\n' $FILES | grep -v -- "-$BASIS-" | grep -- "-$pop\.json")
    # ONE HALF IS A ROW. Runs 11 to 13 ran their classes on the basis
    # alone, and a population skipped for want of a second half left no
    # line at all -- a reader then reads the ten rows printed as the ten
    # populations, which is the silent narrowing this driver refuses
    # everywhere else.
    if [ ! -f "$a" ] || [ -z "$b" ]; then
      printf '    %-12s %s\n' "$pop" \
        "one half only, so there is no cross-half figure to derive"
      continue
    fi
    printf '    %-12s %s\n' "$pop" \
      "$(./read-run.py "$a" --compare "$b" 2>/dev/null \
           | awk '$1 == "list" {
                    d = $2 - 1; if (d < 0) d = -d
                    if (d > 0.007)
                      print $2, "PAST the bar -- an ordering, not a subtraction"
                    else
                      print $2, "inside the bar"
                    exit }')"
  done
  # AND THE SAME ELEVEN FIGURES AS THE DELTA CHAIN'S BULLET WANTS THEM,
  # which is a main-set number and a class RANGE with both ends named.
  # README's Provenance carries that bullet for every run and nothing
  # derived it: Run 31 read the eleven rows above and wrote `23.72 to
  # 38.35 points` by eye into two documents, and got the same figure
  # wrong on a third site the same evening. The rows are the reading and
  # this is the sentence they are quoted as; both are printed, because a
  # range with no rows under it cannot be checked and rows with no range
  # over them are what got summarised by hand.
  printf '  %-14s %s\n' 'list, as the delta bullet quotes it' ''
  for pop in $(printf '%s' "$FACTS" | awk -F'\t' \
                 '{ split($1, t, "-"); print substr($1, length(t[1]) + 2) }' \
               | sort -u); do
    a="$R-$BASIS-$pop.json"
    b=$(printf '%s\n' $FILES | grep -v -- "-$BASIS-" | grep -- "-$pop\.json")
    { [ -f "$a" ] && [ -n "$b" ]; } || continue
    ./read-run.py "$a" --compare "$b" 2>/dev/null \
      | awk -v p="$pop" '$1 == "list" { print p, $2; exit }'
  done | awk '
      { if ($1 == "main") main = $2
        else { if (lo == "" || $2 + 0 < lo + 0) { lo = $2; lop = $1 }
               if (hi == "" || $2 + 0 > hi + 0) { hi = $2; hip = $1 } } }
      END {
        if (main != "") printf "    main set   %.2f points\n", (main - 1) * 100
        if (lo != "")
          printf "    classes    %.2f points on %s to %.2f on %s\n",
                 (lo - 1) * 100, lop, (hi - 1) * 100, hip }'
  for h in $BASIS $(printf '%s\n' $FILES | sed 's/^'"$R"'-//; s/-.*//' \
                      | sort -u | grep -v "^$BASIS$"); do
    m="$R-$h-main.json"
    [ -f "$m" ] || continue
    printf '  %-14s %s\n' "sunk $h" \
      "$(./read-run.py "$m" --markdown 2>&1 >/dev/null \
           | sed -n 's/^warning: \([0-9]*\) cell(s) whose forcing term.*/\1/p'
        )$(./read-run.py "$m" --markdown 2>&1 >/dev/null \
             | sed -n 's/.*and \([0-9]*\) row(s) are geomeans.*/ cell(s) over \1 row(s)/p')"
  done
}

# --for-brief: THE SAME FACTS, ALREADY IN THE BRIEF'S SENTENCES. The rows
# above are what an artifact can settle; this writes them into items 5 and
# 6 so the write-up pastes rather than re-derives. It is `--fill-in` for
# the checker's brief, and it exists for the same reason: Run 32's brief
# carried `thirteen of the sixteen inside 1%` where the reader says
# fourteen, the write-up copied that figure into the run file, and the
# checker found it there. A figure that is transcribed is a figure that
# can be transcribed wrong. What it cannot derive it marks <yours>.
for_brief () {
  facts="$1"
  # THE DELIMITER IS NOT `/`: one of the labels is `A/A past 5%`, and a
  # slash-delimited `s` command died on it with `unknown option to s`,
  # printing an empty row rather than failing -- which is this tree's
  # silent-shortfall family in one character.
  row () { printf '%s\n' "$facts" | sed -n 's|^  '"$1"' *||p' | head -1; }
  echo
  echo "--- paste over checker-brief.txt items 5 and 6; <yours> is prose ---"
  echo " 5. THIS RUN ONLY -- THE BOX AND THE PAIR. The gate machine check"
  echo "    read $(row 'machine check'). Against PREVBASIS: <yours: the"
  echo "    shared-arm span, from --compare>. The binaries are"
  echo "    $(row 'md5s')with .text $(row 'text')"
  echo "    Repetition: $(row 'repetition')"
  echo "    THE TWO HALVES DIFFER IN <yours: the pair's variable> AND IN"
  echo "    NOTHING ELSE. THE PUBLISHED BASIS IS <yours>. The two columns"
  echo "    may be differenced where \`list\` sits inside the 0.7% bar:"
  printf '%s\n' "$facts" | sed -n '/list vs the 0.7% bar/,/^  list, as the/p' \
    | sed -n 's/^    /      /p'
  echo " 6. THIS RUN ONLY -- THE WINDOW AND THE INSTRUMENTS. Window"
  echo "    $(row 'windows')"
  echo "    Processes: $(row 'processes'). Plateau: $(row 'plateau')."
  echo "    Floors over eight A/A pairs: $(row 'floors')"
  echo "    A/A worst cells past 5%: $(row 'A/A past 5%')"
  # A HALF WITH NO SUNK CELL SAYS SO. The row is empty when nothing sank,
  # which is the good answer; pasted as a bare label it reads as a figure
  # nobody derived, which is this tree's silent-shortfall family again.
  echo "    Sunk cells: $(printf '%s\n' "$facts" | sed -n 's/^  sunk /sunk /p' \
                            | sed 's/[[:space:]]*$//; s/^\(sunk [a-z]*\)$/\1 none/' \
                            | tr '\n' ';' | sed 's/;$//')"
  echo "    <yours: the intrusion verdict from --wild over every log, the"
  echo "    class shape counts, the counted work's range, the registration"
  echo "    tally, and what this run's largest finding is>"
}

if [ "$BRIEF" = 0 ]; then
  :
else
  FACTS_OUT=$(brief_facts)
  printf '%s\n' "$FACTS_OUT"
  [ "$FORBRIEF" = 0 ] || for_brief "$FACTS_OUT"
fi

{ [ "$BAD" -eq 0 ] && [ "$SHORT" = 0 ] && [ "$NOISY" = 0 ] \
    && [ "$WILD_PLATEAU" = 0 ]; } || exit 1
