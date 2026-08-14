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
# The worst-cell column is checked rather than trusted: over Run 13 it puts
# `scaled` at 11.59% on scaled-super-r3, which is the figure README records
# for that run's slot from a reading taken without this script, and `rev` at
# 0.85%, the largest of that process's seven A/A lines counted by hand.

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./read-all.sh RUN      # e.g. run14"
  exit 2
fi
R="$1"

# Every JSON the run left, the gate's excluded: those are five arms over
# the shape set and not a population, so their A/A gate is not this one.
FILES=$(ls -1 "$R"-*.json 2>/dev/null | grep -v "^$R-gate-")
if [ -z "$FILES" ]; then
  echo "no $R-*.json here; the run has not landed, or the name is wrong"
  exit 1
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
  # in-situ `sum-only` row, the second lot indented deeper. Those are gate
  # 3's reading and not this one, so take the LEAST-indented lines, which
  # are the A/A pairs, and the largest figure among them. Taking the last
  # line instead read a `-nosum` row and called it the A/A worst -- 23.50%
  # where the A/A pairs of that process reach 2.14%.
  worst=$(./read-run.py "$f" --aa --brief 2>/dev/null \
            | awk '/worst cell/ { i = match($0, /[^ ]/)
                                  if (!m || i < m) { m = i }
                                  n++; ind[n] = i; ln[n] = $0 }
                   END { for (k = 1; k <= n; k++)
                           if (ind[k] == m) {
                             split(ln[k], w, "worst cell ")
                             split(w[2], v, "%")
                             if (v[1] + 0 >= best + 0) { best = v[1]; s = w[2] }
                           }
                         if (s) print "worst cell " s }')
  [ -n "$worst" ] || worst='(no A/A pair in this file)'
  printf '%-28s %-9s %s\n' "$tag" "$st" "$worst"
  [ "$st" = ok ] || printf '%s\n' "$selftest" | grep '^FAIL' | sed 's/^/    /'
done

echo
if [ "$BAD" -eq 0 ]; then
  echo "every process gated clean. The worst cells above are yours to read:"
  echo "  a pair inside the floor with a cell an order of magnitude outside"
  echo "  it is a finding, not noise, and the floor goes in the chapter head"
else
  echo "$BAD process(es) FAILED their gate -- each invalidates that"
  echo "population's whole time column and only that one"
fi
[ "$BAD" -eq 0 ] || exit 1
