#!/usr/bin/env bash
# The pair's two halves, read from its note and from nowhere else.
#
#     HALVES=$(./pair-halves.sh run24) || exit 1    # the refusal's status
#     eval "$HALVES"                         # sets BASIS, OTHER and COMPARE
#
# Two lines and not `eval "$(...)" || exit`: eval's status is the evaluated
# text's, and an empty text evaluates to 0, so the one-line form went on
# past every refusal here with both names unset.
#
# The note is the authority on which half is the basis (README, *Which two
# halves a pair has*), and until 2026-09-02 every script that needed the
# names carried its own `${BASIS:-...}` default, five of them set together
# at a pre-run step of their own and checked against the note by a sixth.
# A five-site edit is the shape of edit that gets four fifths done, and a
# wrong OTHER in one of them sweeps the wrong half and looks clean. So the
# names are written ONCE, on the note's `HALVES:` line --
#
#     HALVES: basis=g912 other=spot
#
# -- and every script reads them through this file. It prints the shell
# assignments on stdout for the caller to eval, and on any refusal prints
# the reason on stderr, prints nothing to eval, and exits 1: no note, no
# HALVES line, a line naming one half twice, or an environment that
# already carries BASIS or OTHER and disagrees with the note. Agreeing is
# allowed, so a launch line may still spell the names out for a reader.
# With NO note at all the environment's BASIS (and OTHER, if set) stand
# in, said on stderr: that is the install of a pair whose note has gone,
# and the corpus's stand-ins; every driver that spends the machine wants
# the note itself and refuses without it.
#
# COMPARE is the note's `COMPARE: run<N>`, the earlier run every cross-run
# reading of the pair goes against, and empty where the note has none. A
# line naming anything but a run is refused, since `runs/$COMPARE.md` is
# what the readers open.
#
# The defects.py cases for this file are its controls: a note read,
# and each refusal.
set -u
cd "$(dirname "$0")" || exit 1
if [ $# -ne 1 ]; then
  echo "usage: HALVES=\$(./pair-halves.sh RUN) || exit 1; eval \"\$HALVES\"" >&2
  exit 1
fi
R=$1
NOTE="$R-pair.txt"
# No note, and the environment names the basis: a pair whose note has
# gone -- an install re-run after the artifacts were offered -- or a
# stand-in in defects.py. Said on stderr, so a launch that meant to
# read a note and found none is not silent about it. OTHER may be unset
# here, a one-half run having none; the scripts that need two check.
if [ ! -f "$NOTE" ]; then
  if [ -n "${BASIS:-}" ]; then
    echo "no $NOTE: halves from the environment, BASIS=$BASIS OTHER=${OTHER:-}" >&2
    echo "BASIS=$BASIS; OTHER=${OTHER:-}; COMPARE="
    exit 0
  fi
  echo "no $NOTE -- a pair's note is written at pre-run step 2, and its" >&2
  echo "HALVES: line is where the two halves' names live" >&2
  exit 1
fi
# THE FIRST LINE THAT PARSES, and not the first that begins with the word:
# a sentence of the note's own prose can wrap `HALVES:` onto a line start,
# and reading that one refused a whole pair before a step ran (defects.py,
# halves-skip-a-prose-line-before-the-machine-line, Run 35's preparation).
# A `^HALVES:` line that does NOT parse is still picked up below, so a
# malformed machine line keeps its own refusal instead of reading as absent.
LINE=$(awk '/^HALVES:/ && /basis=[^ ]/ && /other=[^ ]/ { print; exit }' "$NOTE")
[ -n "$LINE" ] || LINE=$(grep -m1 '^HALVES:' "$NOTE")
if [ -z "$LINE" ]; then
  echo "!! $NOTE has no 'HALVES: basis=<b> other=<o>' line, which is the" >&2
  echo "   one place the halves are named since 2026-09-02. Add it under" >&2
  echo "   THE BASIS IS; pair-note-template.txt shows where." >&2
  exit 1
fi
# UP TO THE NEXT SPACE, and not up to the first character outside the
# grammar: a name carrying one was CUT there and handed on truncated, so
# `other=ghead-exit` reached every driver as `ghead` and named a binary
# nobody built. Read whole here, refused below, since a wrong name that
# parses is the one failure no step downstream can see. Run 33's pair was
# declared `run33-ghead-exit` and renamed for exactly this.
B=$(printf '%s\n' "$LINE" | sed -n 's/.*basis=\([^ ]*\).*/\1/p')
O=$(printf '%s\n' "$LINE" | sed -n 's/.*other=\([^ ]*\).*/\1/p')
if [ -z "$B" ] || [ -z "$O" ]; then
  echo "!! $NOTE's HALVES line does not parse: '$LINE'" >&2
  echo "   wanted 'HALVES: basis=<b> other=<o>', names of [A-Za-z0-9_]" >&2
  exit 1
fi
for N in "$B" "$O"; do
  case $N in
    *[!A-Za-z0-9_]*)
      echo "!! $NOTE names a half '$N': a half's tag is [A-Za-z0-9_], and" >&2
      echo "   a hyphen in one is read wrong here and by install-tables.sh's" >&2
      echo "   \$R-<basis>-*.json glob alike. Name the half in one token." >&2
      exit 1 ;;
  esac
done
# A pair is two halves; run-major.sh says what one name in both costs.
if [ "$B" = "$O" ]; then
  echo "!! $NOTE names '$B' as both halves -- a pair is two halves" >&2
  exit 1
fi
# The environment may repeat the note and may not contradict it: a launch
# line carrying an older pair's names would otherwise silently win.
if [ -n "${BASIS:-}" ] && [ "$BASIS" != "$B" ]; then
  echo "!! BASIS=$BASIS in the environment, but $NOTE says basis=$B --" >&2
  echo "   the note is the authority; unset BASIS or fix the note" >&2
  exit 1
fi
if [ -n "${OTHER:-}" ] && [ "$OTHER" != "$O" ]; then
  echo "!! OTHER=$OTHER in the environment, but $NOTE says other=$O --" >&2
  echo "   the note is the authority; unset OTHER or fix the note" >&2
  exit 1
fi
C=$(grep -m1 '^COMPARE:' "$NOTE")
if [ -n "$C" ]; then
  C=$(printf '%s\n' "$C" | sed 's/^COMPARE:[[:space:]]*//; s/[[:space:]]*$//')
  if ! printf '%s\n' "$C" | grep -qx 'run[0-9][0-9]*'; then
    echo "!! $NOTE's COMPARE line names '$C', where it names a run," >&2
    echo "   'COMPARE: run<N>', whose file is runs/run<N>.md" >&2
    exit 1
  fi
fi
echo "BASIS=$B; OTHER=$O; COMPARE=$C"
