#!/usr/bin/env python3
"""What one roster change did, read off the two binaries rather than prose.

    ./roster-delta.py run24-g912 run25-g912      # OLD then NEW

A run's roster delta is stated in three places -- the pair note's roster
block, README's Provenance chain, and the registration -- and until
2026-09-04 all three were written by hand from a `diff` of two `--list`
outputs that nothing here performed. Run 25's preparation did that diff by
hand and got one clause of it wrong in its own note, writing `twelve A/A
controls` where two of the twelve are the `-nosum` forcing controls; the
same session improvised the per-class view count, which no mode gives
either. Both are subtractions over two listings, so both belong here.

WHAT IT ANSWERS, and each is a sentence a roster block owes:
  the bench totals, main set and classes, on each side;
  which arms landed and which left, by name;
  whether the arms both rosters carry kept their ORDER, which is a
    delta of its own -- Provenance says so at *And a third: the ORDER
    they ran in*, order being able to move layout where membership
    does not;
  which main-set shapes landed and left;
  the class views per class, on each side, and which views moved.

It reads `--list` and `classes --list` and nothing else, so it says what
the binaries carry and never what a document claims about them. Exit 0
clean, 2 where a binary would not answer -- a listing that comes back empty
is that, and not an empty roster: `scan`'s own lesson in loop-offsets.py.

Non-vacuity: pointed at one binary twice it must report nothing moved, and
the corpus carries that as a control beside the real delta of Run 24 to Run
25, whose figures the case asserts.
"""

import collections
import subprocess
import sys


def listing(path, mode):
    """`shape/arm` lines from a half, or exit 2 saying which call failed."""
    cmd = ['./' + path] + ([mode] if mode else []) + ['--list']
    try:
        got = subprocess.run(cmd, capture_output=True, text=True)
    except OSError as exc:
        sys.exit('%s: %s' % (' '.join(cmd), exc))
    if got.returncode != 0:
        sys.exit('%s exited %d: %s' % (' '.join(cmd), got.returncode,
                                       got.stderr.strip() or '(no stderr)'))
    lines = [l for l in got.stdout.split('\n') if '/' in l]
    if not lines:
        # A binary that answers nothing reads exactly like a roster with no
        # benches, and every count below would then be a true statement
        # about a file that was never really opened.
        sys.exit('%s listed nothing -- wrong binary, or a mode it lacks'
                 % ' '.join(cmd))
    return lines


def ordered(seq):
    """Unique, in first-encountered order, which is the roster's own."""
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out


def split(lines):
    shapes = ordered(l.split('/', 1)[0] for l in lines)
    arms = ordered(l.split('/', 1)[1] for l in lines)
    return shapes, arms


def names(label, gone, came):
    for word, xs in (('out', gone), ('in', came)):
        if xs:
            print('     %-4s (%d): %s' % (word, len(xs), ', '.join(xs)))
    if not gone and not came:
        print('     unmoved')


def main():
    if len(sys.argv) != 3:
        sys.exit('usage: ./roster-delta.py OLD NEW   # two binaries,'
                 ' OLD first')
    old, new = sys.argv[1], sys.argv[2]
    print('== %s -> %s' % (old, new))

    for mode, what in ((None, 'main set'), ('classes', 'classes')):
        ol = listing(old, mode)
        nl = listing(new, mode)
        os_, oa = split(ol)
        ns, na = split(nl)
        unit = 'shape' if mode is None else 'view'
        print('  %s: %d -> %d benches, %d -> %d arms over %d -> %d %ss'
              % (what, len(ol), len(nl), len(oa), len(na),
                 len(os_), len(ns), unit))
        print('   arms')
        names('arms', [a for a in oa if a not in na],
              [a for a in na if a not in oa])
        # ORDER, of the arms both carry: a delta stated in membership alone
        # can read empty while the run is not repeatable.
        both_old = [a for a in oa if a in na]
        both_new = [a for a in na if a in oa]
        print('     %d survivor(s), %s' % (
            len(both_old),
            'in the same order' if both_old == both_new
            else 'REORDERED: %s -> %s' % (both_old, both_new)))
        print('   %ss' % unit)
        names(unit, [s for s in os_ if s not in ns],
              [s for s in ns if s not in os_])
        if mode == 'classes':
            # A view's class is its prefix up to the first hyphen, the
            # derivation every driver here uses (Main.hs `classOf`).
            oc = collections.Counter(s.split('-', 1)[0] for s in os_)
            nc = collections.Counter(s.split('-', 1)[0] for s in ns)
            print('   views per class (%d -> %d classes)'
                  % (len(oc), len(nc)))
            for c in sorted(set(oc) | set(nc)):
                mark = '' if oc.get(c) == nc.get(c) else '   <-- moved'
                print('     %-10s %3s -> %-3s%s'
                      % (c, oc.get(c, '-'), nc.get(c, '-'), mark))


if __name__ == '__main__':
    main()
