#!/bin/bash
# Op-cache fetches per iteration for every cell of a binary, over the
# main set and every stride class: run-counts.sh's sweep with the fetch
# counter in place of the instruction counter, raw event 0x28F on this
# Zen 3, which reads taken branches plus window crossings -- the window
# half of the entry model behind align-as.py's LOOP_ENTRIES (README, the
# placement section). A probe: an input to README, run by hand, and
# never a recorded column, which is why it takes binaries by path and
# writes probe-named files rather than RUN-counts-HALF.txt.
#
#     ./probe-fetches.sh probe-flag-exit-bin probe-flag-entries-bin
#     ./probe-fetches-read.py probe-fetches-probe-flag-exit-bin.txt \
#                             probe-fetches-probe-flag-entries-bin.txt
#
# Like instructions, fetches retire the same under load, so this runs
# whenever; the machine's business changes when they retire and not how
# many. A cell is two processes, -n 2N and -n N, differenced over N.
# Output per binary: probe-fetches-<name>.txt, one line a cell --
# population, shape, arm, N, fetches an iteration -- with `!!` for a
# cell perf could not count, which is also the exit status. ONLY=<shape>
# restricts it to one shape, for a smoke run and never for a reading.
set -u
cd "$(dirname "$0")" || exit 1
[ $# -ge 1 ] || { echo "usage: ./probe-fetches.sh BINARY [BINARY...]"; exit 2; }
N=${N:-50}
EV=${EVENT:-r20000078f:u}
if ! command -v perf > /dev/null 2>&1; then
  echo "!! no perf on PATH; nothing ran"; exit 2
fi
if ! perf stat -x, -e "$EV" /bin/true 2>&1 | grep -q '^[0-9]\+,'; then
  echo "!! perf will not count $EV here; nothing ran"; exit 2
fi
count() {  # count BINARY SEL SHAPE ARM ITERS -> the event over one process
  local f; f=$(mktemp)
  # shellcheck disable=SC2086
  perf stat -x, -e "$EV" -o "$f" "$1" $2 -m glob "$3/$4" -n "$5" > /dev/null 2>&1
  local c; c=$(grep "$EV" "$f" | cut -d, -f1); rm -f "$f"
  case $c in ''|*[!0-9]*) echo "NaN" ;; *) echo "$c" ;; esac
}
BAD=0
for B in "$@"; do
  case $B in */*) ;; *) B=./$B ;; esac      # a bare name is a file here, not a command
  [ -x "$B" ] || { echo "!! $B is not an executable here"; BAD=1; continue; }
  OUT=probe-fetches-$(basename "$B").txt
  BEGAN=$(date +%s)
  {
    echo "# $B $(md5sum "$B" | cut -d' ' -f1) N=$N event=$EV $(date -Is)"
    echo "# population shape arm N fetches/iter"
    [ -z "${ONLY-}" ] || echo "# RESTRICTED to ONLY=$ONLY: a smoke run"
  } > "$OUT"
  # --list ends with a roster line carrying no `/`, which is not a cell.
  MAIN=$("$B" --list 2>/dev/null | grep /)
  CLS=$("$B" classes --list 2>/dev/null | grep /)
  [ -n "$MAIN" ] && [ -n "$CLS" ] || { echo "!! $B: --list gave nothing"; BAD=1; continue; }
  POPS="main $(printf '%s\n' "$CLS" | cut -d/ -f1 | sed 's/-.*//' | awk '!seen[$0]++')"
  for P in $POPS; do
    if [ "$P" = main ]; then SEL=; LIST=$MAIN
    else SEL=classes; LIST=$(printf '%s\n' "$CLS" | grep "^$P-"); fi
    SHAPES=$(printf '%s\n' "$LIST" | cut -d/ -f1 | awk '!seen[$0]++')
    ARMS=$(printf '%s\n' "$LIST" | cut -d/ -f2 | awk '!seen[$0]++')
    for S in $SHAPES; do
      [ -z "${ONLY-}" ] || [ "$S" = "$ONLY" ] || continue
      for A in $ARMS; do
        printf '%s\n' "$LIST" | grep -qx "$S/$A" || continue
        c2=$(count "$B" "$SEL" "$S" "$A" $((2 * N))); c1=$(count "$B" "$SEL" "$S" "$A" "$N")
        if [ "$c2" = NaN ] || [ "$c1" = NaN ]; then
          echo "!! $P $S $A: perf could not count" >> "$OUT"; BAD=1
        else
          echo "$P $S $A $N $(( (c2 - c1) / N ))" >> "$OUT"
        fi
      done
    done
    echo "### $(date -Is) $B $P done" >&2
  done
  echo "# end $(date -Is) elapsed=$(( $(date +%s) - BEGAN ))s" >> "$OUT"
done
exit $BAD
