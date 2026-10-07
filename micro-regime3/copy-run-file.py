#!/usr/bin/env python3
"""Post-run step 5's copy: the last run's file as this run's, with every
decimal, percentage and run number in its prose masked.

    ./copy-run-file.py runs/run45.md runs/run46.md

The write-up starts from the last run's file, and a figure the copy carries
unedited is last run's number under this run's name. Each is written as
`{{was 1.2929}}`, the old figure kept as a model, and `--check-doc` refuses
a run file still carrying one, so keeping a figure is retyping it. Counts
and number words are left to `--stale`. Why that scope:
why: --para 'COMMIT THE COPY'

Left alone: headings, whose anchors README links into, though the title's
run number is renamed; table rows, which the installs overwrite; code spans
and fenced blocks; link targets; and a number inside a word, `ghc-9.12.4`
or `10.1.20260918`.

Exit 0 with the copy written, 2 when nothing was: a name that is not
`runN.md`, a source that is not there, or a destination that is.
"""
import os
import re
import sys

# A decimal or a percentage standing alone, signed or opening a `--` range,
# and not part of a dotted version.
FIGURE_RE = re.compile(r'(?:(?<![\w.\-])|(?<=[\s(][-+])|(?<=\d--))'
                       r'(\d+\.\d+%?|\d+%)(?!\.\d)')
# A run number and the list it heads: `Run 44`, `Runs 40 and 42 to 45`.
RUNS_RE = re.compile(r'\bRuns? \d+(?:(?:,\s*|\s+and\s+|\s+or\s+|\s+to\s+|--)'
                     r'\d+)*')
# What a line keeps whole inside its prose: code spans, link targets and
# autolinks.
KEEP_RE = re.compile(r'`[^`]*`|\]\([^)]*\)|<https?://[^>]*>')
NAME_RE = re.compile(r'^run(\d+)\.md$')


def mask_prose(text):
    """TEXT with its figures masked, and how many."""
    n = [0]

    def figure(m):
        n[0] += 1
        return '{{was %s}}' % m.group(1)

    def runs(m):
        def one(d):
            n[0] += 1
            return '{{was %s}}' % d.group(0)
        # answered spaced-split: the match is RUNS_RE's, whose first space
        # is the one after `Run` or `Runs`.
        head, _, rest = m.group(0).partition(' ')
        return head + ' ' + re.sub(r'\d+', one, rest)

    out, last = [], 0
    for k in KEEP_RE.finditer(text):
        out.append(RUNS_RE.sub(runs, FIGURE_RE.sub(figure,
                                                   text[last:k.start()])))
        out.append(k.group(0))
        last = k.end()
    out.append(RUNS_RE.sub(runs, FIGURE_RE.sub(figure, text[last:])))
    return ''.join(out), n[0]


def mask(doc, old, new):
    """DOC with its prose masked and its title's run renamed, and the count
    of masks."""
    # answered boolean-pair-state: the run files this reads carry no fence
    # of any kind, so no marker sits inside a block of another kind.
    lines, fenced, total = [], False, 0
    for i, line in enumerate(doc.split('\n')):
        if line.startswith('```'):
            # answered boolean-pair-state: as at the binding of `fenced` above.
            fenced = not fenced
        if fenced or line.startswith('```') or line.startswith('|') \
                or re.match(r'\s*\[[^\]]+\]:\s', line):
            lines.append(line)
        elif line.startswith('#'):
            if i == 0:
                line = re.sub(r'^# Run %s\b' % old, '# Run %s' % new, line)
            lines.append(line)
        else:
            line, n = mask_prose(line)
            total += n
            lines.append(line)
    return '\n'.join(lines), total


def main(argv):
    if len(argv) != 2:
        sys.stderr.write('usage: ./copy-run-file.py runs/runM.md'
                         ' runs/runN.md\n')
        return 2
    src, dst = argv
    names = [NAME_RE.match(os.path.basename(p)) for p in (src, dst)]
    if not all(names):
        sys.stderr.write('copy-run-file.py: %s and %s must both be named'
                         ' runN.md, the numbers being what the title is'
                         ' renamed by; nothing was written\n' % (src, dst))
        return 2
    if not os.path.isfile(src):
        sys.stderr.write('copy-run-file.py: %s is not there; nothing was'
                         ' written\n' % src)
        return 2
    if os.path.lexists(dst):
        sys.stderr.write('copy-run-file.py: %s already exists, and step 5'
                         ' copies over no write-up; nothing was written\n'
                         % dst)
        return 2
    text, n = mask(open(src).read(), names[0].group(1), names[1].group(1))
    with open(dst, 'w') as f:
        f.write(text)
    print('%s: copied from %s, %d figure(s) masked as {{was ...}}. Commit'
          ' it before editing it; --check-doc refuses it while one is left'
          % (dst, os.path.basename(src), n))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
