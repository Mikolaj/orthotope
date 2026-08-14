#!/usr/bin/env bash
# The write-up's installs, all of them, in one call.
#
#     ./install-tables.sh run14           # writes README.md
#
# `--markdown`, `--fingerprint` and a `--block` per class, every one from
# the BASIS half, every one `--in-place`. That is eleven writes into this
# file, and eleven is a number a session loses count of: the failure is not
# a wrong table but a missing one, and a page with ten of eleven installed
# looks exactly like a page with eleven.
#
# It installs and collects; it decides nothing. Each mode's stderr is the
# hand-work it leaves -- a row new to the roster installs as `?` and is
# filled by hand, a departed row is dropped with a warning -- so this
# gathers those and prints them at the end as the list they are.
#
# The class list comes from the JSONs on disk rather than from a literal
# here: run-major.sh's own class literal went out of step with the binary
# once, and a write-up that installs seven blocks of eight is the same
# defect one stage later.
#
# WRITES THE PAGE, so commit or park README.md first -- `git checkout --
# README.md` is the undo, and there is no other. Read the diff afterwards
# rather than the terminal: install prints what it replaced, not what the
# page now says.
#
# Measured over Run 13's artifacts, 2026-08-15, against a copy: ten calls
# write eleven tables; a full pass over a page that already carries them
# leaves it byte-identical, so a rerun after fixing one refusal costs
# nothing; and renaming a class block's bolded lead makes that one install
# refuse -- `0 line(s) start with '**`scaled`', need exactly one` -- which
# this reports and exits 1 on, the other ten having landed.

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./install-tables.sh RUN      # e.g. run14; writes README.md"
  exit 2
fi
R="$1"
BASIS=${BASIS:-lookrts}
DOC=${DOC:-README.md}        # overridable so a dry run can aim at a copy,
                             # which is also this script's own control

MAIN="$R-$BASIS-main.json"
[ -f "$MAIN" ] || { echo "no $MAIN -- wrong run or wrong BASIS?"; exit 1; }
CLASSES=$(ls -1 "$R-$BASIS"-*.json 2>/dev/null \
            | grep -v -- '-main\.json$' | grep -v "^$R-gate-")
[ -n "$CLASSES" ] || { echo "no class JSONs for $R-$BASIS"; exit 1; }

BAD=0
DONE=0                       # tables, not invocations: --fingerprint
                             # installs two, so ten calls write eleven
HAND=""
install () {   # $1 = json, $2.. = mode
  local f=$1; shift
  local err
  err=$(./read-run.py "$f" "$@" --in-place --readme "$DOC" 2>&1 >/dev/null)
  if [ $? != 0 ]; then
    echo "  !! $f $* REFUSED:"
    printf '%s\n' "$err" | sed 's/^/       /'
    BAD=$((BAD + 1))
    return
  fi
  echo "  $f $*"
  DONE=$((DONE + $(printf '%s\n' "$err" | grep -c '^installed at ')))
  [ -z "$err" ] || HAND="$HAND
    $f $*:
$(printf '%s\n' "$err" | sed 's/^/      /')"
}

echo "=== installing into $DOC, all from $BASIS"
install "$MAIN" --markdown
install "$MAIN" --fingerprint
for c in $CLASSES; do install "$c" --block; done

echo
if [ -n "$HAND" ]; then
  echo "What the installs left for you, and it is not optional:$HAND"
  echo
fi
if [ "$BAD" -eq 0 ]; then
  echo "$DONE table(s) installed, counted off install's own lines rather"
  echo "than off the call count -- --fingerprint writes two. The cross-class"
  echo "summary is NOT among them: it is assembled last, by hand, from the"
  echo "class tables above."
else
  echo "$BAD install(s) REFUSED -- a refusal is the design, never a silent"
  echo "write to the wrong place. Fix the header it could not find and rerun;"
  echo "the ones that landed are idempotent."
fi
[ "$BAD" -eq 0 ] || exit 1
