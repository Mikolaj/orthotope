#!/usr/bin/env python3
"""The source commits a registration did not see: what landed between it and
the build, and which top-level definitions each touched.

    ./registration-drift.py run39          # exit 0 none, 1 some, 2 no reading
    ./registration-drift.py run39 --dir D  # a checkout elsewhere (the cases)

A registration prices spans on the source as it stood when it was written,
and the pair is built from the tip on the day. Run 39's registration was
committed before `c0a8aaa` rebuilt the inward fill behind one arm of its
item (1) pair, so the span priced one variable where the build carried two,
and died on it; the preparation's note then named the wrong fill. This lists
every commit to `Main.hs` after the one that first carried the registration
and up to the commit the note's `Main.hs at` row names, each with the
definitions its hunk headers name, the nearest above each hunk and so now
and then a neighbour, for the preparation to read against the arms
the registration names. It reads git and the note, and writes nothing.
Cases: `registration-drift-names-the-commits-after-it` and its empty twin.
"""
import os
import re
import subprocess
import sys

# A hunk header names the nearest unindented line above the hunk, which
# is the definition a change sits in or, where the change opens a new one,
# its neighbour; and on a declaration line it names the keyword.
KEYWORDS = {'data', 'type', 'newtype', 'import', 'instance', 'class',
            'module', 'where', 'deriving', 'infixl', 'infixr', 'infix'}


def git(d, *args):
    r = subprocess.run(['git', '-C', d] + list(args), capture_output=True,
                       text=True)
    return r.stdout if r.returncode == 0 else None


def main(argv):
    d = os.path.dirname(os.path.abspath(__file__))
    if '--dir' in argv:
        i = argv.index('--dir')
        d = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if len(argv) != 1 or not re.match(r'run\d+$', argv[0]):
        print('usage: ./registration-drift.py runN [--dir CHECKOUT]')
        return 2
    run = argv[0]
    n = run[3:]
    note = os.path.join(d, '%s-pair.txt' % run)
    if not os.path.exists(note):
        print('no %s, whose `Main.hs at` row names the build; nothing read'
              % os.path.basename(note))
        return 2
    m = re.search(r'^\s*Main\.hs at\s+([0-9a-f]{7,40})\b', open(note).read(),
                  re.M)
    if not m:
        print('%s has no `Main.hs at <hash>` row; nothing read'
              % os.path.basename(note))
        return 2
    build = m.group(1)
    lead = 'What Run %s is built to answer' % n
    added = git(d, 'log', '--reverse', '--format=%h', '-S', lead, '--',
                'README.md')
    if not added or not added.split():
        print('no commit of README.md carries `%s`; nothing read' % lead)
        return 2
    reg = added.split()[0]
    log = git(d, 'log', '--reverse', '--format=%h %s',
              '%s..%s' % (reg, build), '--', 'Main.hs')
    if log is None:
        print('git cannot read %s..%s; nothing read' % (reg, build))
        return 2
    commits = [l.split(' ', 1) for l in log.splitlines() if l]
    print('%s: the registration first committed at %s, the build at %s'
          % (run, reg, build))
    if not commits:
        print('no commit to Main.hs between them: the registration saw the'
              ' source the pair was built from')
        return 0
    for h, subj in commits:
        diff = git(d, 'show', '-U0', '--format=', h, '--', 'Main.hs') or ''
        defs = []
        for hunk in re.findall(r'^@@[^@]*@@ ?(.*)$', diff, re.M):
            w = re.match(r"([a-z][A-Za-z0-9_']*)", hunk.strip())
            if w and w.group(1) not in defs and w.group(1) not in KEYWORDS:
                defs.append(w.group(1))
        print('  %s %s' % (h, subj))
        print('      in: %s' % (', '.join(defs) or 'no top-level definition'
                                ' named by its hunks'))
    print('%d commit(s) the registration did not see: read each against the'
          ' arms its spans name before the evening' % len(commits))
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
