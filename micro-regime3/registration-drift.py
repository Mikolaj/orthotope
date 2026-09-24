#!/usr/bin/env python3
"""The source commits a registration did not see: what landed between it and
the build, and which top-level definitions each touched.

    ./registration-drift.py run39          # exit 0 none, 1 some, 2 no reading
    ./registration-drift.py run39 --dir D  # a checkout elsewhere (the cases)
    ./registration-drift.py run40 --since run39   # the source since a build

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

`--since PREV` asks the preparation's question rather than the check's:
every commit to `Main.hs` since the build PREV's note names, up to this
run's note's build or HEAD where no note is written yet, each with the
definitions whose CODE changed -- both sides parsed, whole-line comments
dropped, so a comment-only commit says so -- and the arms that reach them,
by a textual call graph of the build's `Main.hs` walked back from each
changed definition to the roster's functions. Textual means a name a
definition mentions counts as a call, which over-approximates. And the walk
is value-level: a changed `data`, `newtype`, `type`, `class` or `instance`
declaration is named under `code:`, and reaches an arm only through a
definition whose own code changed with it. Where
the basis binary is here its `--list` says which arms are timed, and only
those are named; without one every roster arm reached is. This is the
arm-by-arm reading the pre-run list's reading 7 is scoped by. Cases:
`drift-since-names-the-arms-a-commit-reaches` and
`drift-since-reads-a-comment-only-commit-as-one`.
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


ARM_RE = re.compile(r'^\s*[\[,]\s*\("([^"]+)",\s*'
                    r'(Base|Fill|Twin|Term|Force|Only)(?:\s+(fb\w+))?\)')
DEF_RE = re.compile(r"^([a-z_][A-Za-z0-9_']*)\b")
NAME_RE = re.compile(r"[a-z_][A-Za-z0-9_']*")


def defs_of(text):
    """Top-level definitions as name -> code, comments dropped.

    A definition runs from an unindented line naming it -- its signature or
    an equation -- to the next unindented line; whole-line `--` comments and
    `{- -}` blocks are dropped and trailing comments kept, so a commit that
    moves only comments changes no definition here. A column-0 pragma
    belongs to the definition it names, `{-# INLINE f #-}` to `f`, and one
    naming none to `{-# pragmas`; a type-level declaration is keyed by its
    keyword and first name, `data OdoLevel`. Until 2026-09-25 both went to
    no definition, so a commit changing only them printed `comments only`.
    Case: `drift-since-reads-a-pragma-as-a-comment`.
    """
    out, name, block = {}, None, False
    for line in text.split('\n'):
        if block:
            block = '-}' not in line
            continue
        if line.lstrip().startswith('{-') and not line.lstrip().startswith(
                '{-#'):
            block = '-}' not in line
            continue
        if not line.strip() or line.lstrip().startswith('--'):
            continue
        if line[0] not in ' \t':
            m = DEF_RE.match(line)
            p = re.match(r"\{-#\s*\w+\s+([a-z_][A-Za-z0-9_']*)", line)
            k = re.match(r'(data|newtype|type|class|instance)\s+(\S+)', line)
            if line.startswith('{-#'):
                name = p.group(1) if p else '{-# pragmas'
            elif k:
                name = '%s %s' % k.groups()
            elif m and m.group(1) not in KEYWORDS:
                name = m.group(1)
            else:
                name = None
        if name:
            out[name] = out.get(name, '') + line.rstrip() + '\n'
    return out


def roster_of(text):
    """(arm, function) pairs off `roster =`, as read-run.py's roster_of;
    the function is None for an entry naming none, the forcing pair."""
    out, on = [], False
    for line in text.split('\n'):
        if line.startswith('roster ='):
            on = True
        elif on:
            m = ARM_RE.match(line)
            if m:
                out.append((m.group(1), m.group(3)))
            elif line.strip() == ']':
                break
    return out


def since(d, run, prev):
    """The --since reading; see the docstring."""
    rows = {}
    for r in (prev, run):
        f = os.path.join(d, '%s-pair.txt' % r)
        m = os.path.exists(f) and re.search(
            r'^\s*Main\.hs at\s+([0-9a-f]{7,40})\b', open(f).read(), re.M)
        rows[r] = m.group(1) if m else None
    if not rows[prev]:
        print('no `Main.hs at` row in %s-pair.txt, which names the build to'
              ' read from; nothing read' % prev)
        return 2
    tip = rows[run] or 'HEAD'
    log = git(d, 'log', '--reverse', '--format=%h %s',
              '%s..%s' % (rows[prev], tip), '--', 'Main.hs')
    main = git(d, 'show', '%s:./Main.hs' % tip)
    if log is None or main is None:
        print('git cannot read %s..%s; nothing read' % (rows[prev], tip))
        return 2
    commits = [l.split(' ', 1) for l in log.splitlines() if l]
    defs = defs_of(main)
    callers = {}
    for n, code in defs.items():
        for used in set(NAME_RE.findall(code)) & set(defs):
            if used != n:
                callers.setdefault(used, set()).add(n)
    arms = roster_of(main)
    note = os.path.join(d, '%s-pair.txt' % run)
    h = os.path.exists(note) and re.search(r'^HALVES: basis=(\w+)',
                                           open(note).read(), re.M)
    binary = h and os.path.join(d, '%s-%s' % (run, h.group(1)))
    timed = None
    if binary and os.access(binary, os.X_OK):
        r = subprocess.run([binary, '--list'], capture_output=True, text=True)
        timed = {l.split('/', 1)[1] for l in r.stdout.split() if '/' in l}
        arms = [a for a in arms if a[0] in timed]
    print('%s since %s: Main.hs %s..%s, %d commit(s); arms named are %s'
          % (run, prev, rows[prev], tip, len(commits),
             'the timed ones, off %s --list' % os.path.basename(binary)
             if timed is not None else 'every roster arm, no basis binary'
             ' being here to say which are timed'))
    reached_any = set()
    for c, subj in commits:
        old = defs_of(git(d, 'show', '%s^:./Main.hs' % c) or '')
        new = defs_of(git(d, 'show', '%s:./Main.hs' % c) or '')
        touched = sorted(n for n in set(old) | set(new)
                         if old.get(n) != new.get(n))
        seen, todo = set(touched), list(touched)
        while todo:
            for up in callers.get(todo.pop(), ()):
                if up not in seen:
                    seen.add(up)
                    todo.append(up)
        hit = [a for a, f in arms if f in seen]
        reached_any.update(hit)
        print('  %s %s' % (c, subj))
        print('      code: %s' % (', '.join(touched) or 'none -- comments'
                                  ' only'))
        if touched:
            print('      arms: %s' % (', '.join(hit) or 'none'))
    rest = [a for a, _ in arms if a not in reached_any]
    print('reached by some commit: %d arm(s); by none: %s'
          % (len(reached_any), ', '.join(rest) or 'none'))
    return 1 if commits else 0


def main(argv):
    d = os.path.dirname(os.path.abspath(__file__))
    if '--dir' in argv:
        i = argv.index('--dir')
        d = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    prev = None
    if '--since' in argv:
        i = argv.index('--since')
        prev = argv[i + 1] if i + 1 < len(argv) else ''
        argv = argv[:i] + argv[i + 2:]
    if len(argv) != 1 or not re.match(r'run\d+$', argv[0]) or (
            prev is not None and not re.match(r'run\d+$', prev)):
        print('usage: ./registration-drift.py runN [--since runM]'
              ' [--dir CHECKOUT]')
        return 2
    run = argv[0]
    if prev is not None:
        return since(d, run, prev)
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
