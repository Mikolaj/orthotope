#!/usr/bin/env python3
"""Post-run step 6e's worklist: each reader command a run file quotes, run,
and every figure in its sentence that no quoted command printed.

    ./check-commands.py runs/run46.md

A run file names the command a figure came from so that a reader can run
it again, and a figure credited to the wrong command, or retyped wrong,
reads as evidence all the same. This runs each quoted command once, while
the run's artifacts are on disk, and holds each decimal and percentage of
the sentence quoting it to the outputs of that sentence's commands: a
figure matches a number printed at its own precision, or a percentage or a
count of points off a printed ratio, 3.6% from 0.9639. What matches
nothing is listed with its sentence. A WORKLIST AND NOT A GATE, ruled
2026-10-05 by the owner and measured the same day on Run 45's file as it
stood before its floor sentence was fixed: eight sentences listed, the
misattributed floor among them, and seven whose figures the prose itself
credits elsewhere -- another reader, a probe file, a reading across runs
-- or derives. Post-run step 6e runs it.

It runs readers only -- read-run.py, roster-delta.py, loop-offsets.py and
registration-drift.py -- and names any other program a sentence quotes
rather than running it. A span holding `$` or `<` is a template and is
skipped. A bare `--mode ARGS` span is read-run.py's where it names a run or
a file, or where `on` or `over` and a backticked JSON follow it, as the run
files write a mode's input; a bare `--compare ...` with neither reads the
run's main-set pair, its halves off pair-halves.sh.

    --dir DIR    run the commands from DIR, this script's own by default

Exit 0 when every figure matched, 1 with the list, 2 when nothing was read.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
READERS = {'read-run.py', 'roster-delta.py', 'loop-offsets.py',
           'registration-drift.py'}
# A decimal or a percentage standing alone, as copy-run-file.py masks it.
FIGURE_RE = re.compile(r'(?:(?<![\w.\-])|(?<=[\s(][-+])|(?<=\d--))'
                       r'(\d+\.\d+%?|\d+%)(?!\.\d)')
NUMBER_RE = re.compile(r'\d+(?:\.\d+)?')
SPAN_RE = re.compile(r'`([^`]+)`')
SENTENCE_RE = re.compile(r'(?<=[.!?])\s+(?=[A-Z*`(\[])')
TIMEOUT = 900


def prose(text):
    """The prose paragraphs, each on one line: headings, tables and fenced
    blocks left out."""
    # answered boolean-pair-state: the run files this reads carry no fence
    # of any kind, so no marker sits inside a block of another kind.
    out, cur, fenced = [], [], False
    for line in text.split('\n'):
        if line.startswith('```'):
            # answered boolean-pair-state: as at the binding of `fenced` above.
            fenced = not fenced
            continue
        if fenced or line.startswith(('|', '#')):
            continue
        if not line.strip():
            if cur:
                out.append(' '.join(cur))
                cur = []
            continue
        cur.append(line.strip())
    if cur:
        out.append(' '.join(cur))
    return out


def command(span, run, where, after=''):
    """The argv SPAN stands for, a string saying why it is not run, or
    None where it is no command at all. AFTER is the sentence following the
    span, where a bare mode's JSON may be named."""
    if '$' in span or '<' in span:
        return None
    words = span.split()
    if not words:
        return None
    if words[0].startswith('../../horde-ad/tools/'):
        # horde-ad's tools, where loop-offsets.py went on 2026-10-06.
        return words if words[0][21:] in READERS else None
    if words[0].startswith('./'):
        prog = words[0][2:]
        if prog == 'loop-offsets.py':
            # The run files' spelling, from before it moved.
            return ['../../horde-ad/tools/loop-offsets.py'] + words[1:]
        if prog in READERS:
            return words
        if re.match(r'[\w.-]+\.(sh|py)$', prog):
            return '%s is not a reader' % prog
        return None
    if not re.match(r'--[a-z][a-z-]*$', words[0]):
        return None
    on = re.match(r'\s+(?:on|over)\s+`([^`\s]+\.json)`', after)
    if on and not any(w.endswith('.json') for w in words[1:]):
        return ['./read-run.py', on.group(1)] + words
    named = [w for w in words[1:] if re.search(r'run\d+|\.json$|\.txt$', w)]
    if named:
        return ['./read-run.py'] + words
    if words[0] == '--compare':
        halves = pair_of(run, where)
        if not halves:
            return 'a bare --compare with no pair to read for %s' % run
        basis, other = halves
        return (['./read-run.py', '%s-%s-main.json' % (run, basis),
                 '--compare', '%s-%s-main.json' % (run, other)] + words[1:])
    return None


def pair_of(run, where):
    """(basis, other) off pair-halves.sh, or None."""
    try:
        # answered dropped-status: pair-halves.sh prints nothing on stdout
        # when it refuses, and a pair lacking either half is None below.
        out = subprocess.run(['./pair-halves.sh', run], cwd=where,
                             capture_output=True, text=True,
                             timeout=60).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    got = dict(re.findall(r'(BASIS|OTHER)=([\w.-]+)', out))
    return (got['BASIS'], got['OTHER']) if len(got) == 2 else None


def matches(figure, numbers):
    """Whether FIGURE is printed among NUMBERS at its own precision, or as
    a percentage or points off a printed ratio."""
    bare = figure.rstrip('%')
    k = len(bare.split('.')[1]) if '.' in bare else 0
    v = float(bare)
    for x in numbers:
        if abs(round(x, k) - v) < 1e-9:
            return True
        if x < 10 and abs(round(100 * abs(1 - x), k) - v) < 1e-9:
            return True
    return False


def main(argv):
    where = HERE
    if argv[:1] == ['--dir']:
        if len(argv) < 2:
            sys.stderr.write('check-commands.py: --dir wants a directory\n')
            return 2
        where, argv = argv[1], argv[2:]
    if len(argv) != 1:
        sys.stderr.write('usage: ./check-commands.py [--dir DIR]'
                         ' runs/runN.md\n')
        return 2
    try:
        text = open(argv[0]).read()
    except OSError as e:
        sys.stderr.write('check-commands.py: %s; nothing was read\n' % e)
        return 2
    run = os.path.basename(argv[0])[:-3]
    outputs, refused, listed = {}, [], []
    for para in prose(text):
        for sentence in SENTENCE_RE.split(para):
            argvs = []
            for m in SPAN_RE.finditer(sentence):
                span = m.group(1)
                got = command(span, run, where, sentence[m.end():])
                if isinstance(got, str):
                    refused.append((span, got))
                elif got:
                    argvs.append(tuple(got))
            if not argvs:
                continue
            numbers = []
            for a in argvs:
                if a not in outputs:
                    try:
                        r = subprocess.run(list(a), cwd=where,
                                           capture_output=True, text=True,
                                           timeout=TIMEOUT)
                        outputs[a] = r.stdout + r.stderr
                    except (OSError, subprocess.SubprocessError) as e:
                        outputs[a] = ''
                        refused.append((' '.join(a), 'did not run: %s' % e))
                numbers += [float(n) for n in NUMBER_RE.findall(outputs[a])]
            claimed = FIGURE_RE.findall(SPAN_RE.sub(' ', sentence))
            unmatched = [f for f in claimed if not matches(f, numbers)]
            if unmatched:
                listed.append((sentence, unmatched))
    print('%s: %d command(s) run, %d not run, %d sentence(s) with a figure'
          ' no command printed' % (os.path.basename(argv[0]), len(outputs),
                                   len(refused), len(listed)))
    for sentence, unmatched in listed:
        print('  %s' % sentence)
        print('      unmatched: %s' % ', '.join(unmatched))
    for span, why in refused:
        print('  not run: `%s` -- %s' % (span, why))
    return 1 if listed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
