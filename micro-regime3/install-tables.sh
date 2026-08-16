#!/usr/bin/env bash
# The write-up's installs, all of them, in one call.
#
#     ./install-tables.sh run14           # writes README.md
#
# `--markdown`, `--fingerprint`, a `--block` per class and `--claims`,
# every one from the BASIS half, every one `--in-place`. That is eleven
# tables and one reading per claim, and those are numbers a session loses
# count of: the failure is not a wrong table but a missing one, and a page
# with ten of eleven installed looks exactly like a page with eleven.
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
#
# The claims install joined on 2026-08-16 and is counted apart from the
# tables, installing a paragraph per claim rather than rows; its own four
# proofs -- idempotence, a renamed lead, a deleted reading, a filtered run
# -- are in `install_readings`, where the code they check is.

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

# The claims section's per-claim readings, the last figure-bearing block a
# run was still hand-copying: a dozen orderings out of --claims, which is
# where a wrong verdict got invented, and on 2026-08-15 where a whole
# section of the previous run's figures got shipped. Not run through
# install() above: it writes a paragraph per claim rather than rows, so
# its own line is not a table to count, and what it prints when it inserts
# a missing reading is a notice rather than hand-work.
echo "=== installing the claims section's readings"
CERR=$(./read-run.py "$MAIN" --claims --in-place --readme "$DOC" 2>&1 >/dev/null)
if [ $? != 0 ]; then
  echo "  !! $MAIN --claims REFUSED:"
  printf '%s\n' "$CERR" | sed 's/^/       /'
  BAD=$((BAD + 1))
else
  printf '%s\n' "$CERR" | sed 's/^/  /'
fi

# The block's THREE COMPUTED paragraphs, which --block emits and --in-place
# did not write: Controls, Provenance and the per-shape line. Leaving them to
# hand-copying cost 24 transcriptions a run and, on 2026-08-15, five class
# blocks that silently kept no per-shape line at all -- they were two-shape
# when last written and nothing said the line had become owed. The lead and
# the verdict paragraph stay the author's, as the form says; these three are
# the reader's own output and are installed like the table.
echo "=== installing each class block's computed paragraphs"
python3 - "$R" "$BASIS" "$DOC" <<'ENDPY' || BAD=$((BAD+1))
import re, subprocess, sys
R, BASIS, DOC = sys.argv[1], sys.argv[2], sys.argv[3]
doc = open(DOC).read(); paras = doc.split('\n\n')
leads = {}
for i, p in enumerate(paras):
    m = re.match(r'\*\*`([a-z0-9]+)` \u2014', p.lstrip())
    if m: leads[m.group(1)] = i
order = sorted(leads.items(), key=lambda kv: kv[1])
done = 0
for n, (c, start) in enumerate(reversed(order)):
    k = [x for x, _ in order].index(c)
    end = order[k + 1][1] if k + 1 < len(order) else len(paras)
    blk = subprocess.run(['./read-run.py', f'{R}-{BASIS}-{c}.json', '--block',
                          '--brief'], capture_output=True, text=True).stdout
    log = open(f'{R}-{BASIS}-{c}.log').read()
    m = re.search(r'elapsed (\S+); peak (\d+) MiB in use, (\d+) MiB max', log)
    if not m:
        print(f'  REFUSED {c}: no provenance line in {R}-{BASIS}-{c}.log'); sys.exit(1)
    el, pk, mr = m.groups()
    def grab(tag):
        g = re.search(r'\n(' + tag + r'.*?)(?=\n\n|\Z)', blk, re.S)
        return ' '.join(g.group(1).split()) if g else None
    ctrl, prov, per = grab('Controls:'), grab('Provenance:'), grab('Per shape')
    if not (ctrl and prov and per):
        print(f'  REFUSED {c}: --block emitted no ' +
              ('Controls' if not ctrl else 'Provenance' if not prov else 'per-shape'))
        sys.exit(1)
    ctrl = ctrl.replace('Controls: ___ (the reading is yours). ', 'Controls: ')
    prov = (prov.replace('elapsed ___', 'elapsed ' + el)
                .replace('peak ___ MiB', f'peak {pk} MiB')
                .replace('___ MiB max residency', f'{mr} MiB max residency')
                .replace(" (copy from the process's stderr line)", ''))
    prov_at = None
    for j in range(start, end):
        s = paras[j].lstrip()
        if s.startswith('Controls:'): paras[j] = ctrl; done += 1
        elif s.startswith('Provenance:'): paras[j] = prov; prov_at = j; done += 1
        elif s.startswith('Per shape'): paras[j] = per; done += 1
    if prov_at is not None and not any(
            paras[j].lstrip().startswith('Per shape') for j in range(start, end)):
        paras.insert(prov_at + 1, per); done += 1   # every class is three-shape now
        print(f'  {c}: per-shape line ADDED, the block had none')
open(DOC, 'w').write('\n\n'.join(paras))
print(f'  {done} computed paragraph(s) installed across {len(order)} class block(s)')
ENDPY

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
