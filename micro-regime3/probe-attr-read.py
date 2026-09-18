#!/usr/bin/env python3
"""Bucket a probe-attr histogram by ROLE, and difference the two arms.

    ./probe-attr-read.py probe-attr-<shape>.txt [Main.hs]

perf gives instructions per source line; the question item 4 asks is
whether the excess sits in the element loop or in the loop nest around
it, which is a question about spans of lines and not about lines.  The
spans are derived from Main.hs by anchor phrase rather than written down,
so an edit that moves the file moves them with it and a phrase that stops
being unique fails loudly instead of silently mapping to the wrong span.

The arms are not symmetric in source -- the add-in-leaf arm carries its
run loop in `runs` where `fillStage2` reaches it through `runsWith` --
and an arm's samples do not always land in the function the dispatch
table names: `lib-stage1` is a dispatcher that hands `fillStage2` a view
whose innermost run is strided and nothing else, and `lib-stage2` and
`lib-stage2-lean` reach that fill too, so all three bucket by its spans.  `harness` is the shared forcing pass,
which is the control: it must come out equal, both arms being timed
through it.

Main.hs is the twin's: the histogram's `# Main.hs at HASH` line, which
probe-attr.sh reads off the run's pair note, names the build, and it is
read with `git show`; a second argument overrides it with a file, and a
histogram naming no build is read against the working tree with a
warning. The harness bucket is the check on that: it is the one span
every arm passes through, so an arm with none of its samples there was
read against the wrong file, and the reader refuses.

Exit 2 on usage, a lost anchor, a file with no arm sections or a Main.hs
the harness shows is not the twin's; 1 if a file names an arm this does not
know or the harness differs across arms; 0 clean.
"""
import os
import re
import subprocess
import sys


def die(msg):
    """Exit 2 -- did not run -- rather than `sys.exit(str)`'s 1, which is
    the code a finding gets."""
    sys.stderr.write(msg.rstrip('\n') + '\n')
    sys.exit(2)

# arm -> the function its samples land in, which is NOT always the one
# the dispatch table names: `lib-stage1` is `fbLibStage1`, a dispatcher
# that hands `fillStage2` a view whose innermost run is strided and
# nothing else, and the two stage-two arms reach that fill through
# `canonView`. Until 2026-09-18 `lib-stage1` was
# bound to the add-in-leaf function here, so every lib-stage1 span sat
# in the wrong body and the reader refused on the overlap. The name must
# be unique in the file; the sub-anchors searched from it need only be
# unique WITHIN the function: `let writeRun !outPos !baseOff =` recurs
# across the add-in-leaf family, which a first version asserted unique
# in the file and refused on.
LEAF = 'fbMutOdoVecdimsAddInLeafU2 sh (T (Strides ats) ao v)'
FILL = 'fillStage2 sh ats !ao !l !v = VS.create'
FUNCS = {
    'mut-odo-vecdims-add-in-leaf-u2': LEAF,
    'lib-stage1': FILL,
    'lib-stage2': FILL,
    'lib-stage2-lean': FILL,
}
# FOUR ROLES AND NOT TWO, because the short-run residue is not where the
# long-run one was: an inner run of three does ONE unrolled pair and then
# the epilogue, so the loop's ends are paid once a run where its body is
# paid once a pair, and lumping them hides exactly the term that matters
# on a conv-shaped view. `ends` is the per-run prologue and epilogue,
# `loop` the unrolled body, `run` the loop over runs with the broadcast
# leaf beside it, `odo` the odometer levels above it. The two bodies are
# not symmetric in source -- the leaf writes its run loop into `runs`
# where the fill reaches it through `runsWith` -- so `run` is each body's
# own way of doing that, which is the comparison the question wants.
LEAF_SPANS = {
    'ends': ('  let writeRun !outPos !baseOff =',
             '                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)'),
    'loop': ('              | otherwise = do',
             '        in  inner outPos baseOff'),
    'run': ('      writeRunSet !outPos !baseOff =',
            '        in  run n outPos baseOff'),
    'odo': ('      go !lev !outPos !baseOff',
            '  _ <- go 0 0 ao'),
}
FILL_SPANS = {
    'ends': ('  let {-# INLINE writeRunStep #-}',
             '                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)'),
    'loop': ('              | otherwise = do',
             '        in  inner outPos baseOff'),
    'run': ('      {-# INLINE writeRunSet #-}',
            '            in  run n outPos baseOff'),
    'odo': ('      go !lev !outPos !baseOff',
            '  _ <- go 0 0 ao'),
}
SPANS = {(arm, role): span for arm, fn in FUNCS.items()
         for role, span in (LEAF_SPANS if fn is LEAF else FILL_SPANS).items()}
ROLES = ['ends', 'loop', 'run', 'odo']

# The shared forcing pass, `VS.sum . f sh`, which both arms are timed
# through: it is the control, and it must come out equal.
HARNESS = re.compile(r'^\s*arm sh a \(n, (Fill|Term)')


def spans(src, main_hs):
    lines = src.splitlines()
    starts = {}
    for arm, name in FUNCS.items():
        if src.count(name) != 1:
            die('%s does not name one definition in %s (%d matches)'
                     % (arm, main_hs, src.count(name)))
        starts[arm] = src[:src.index(name)].count('\n')
    out = {}
    for (arm, role), (a, b) in SPANS.items():
        i = starts[arm]
        lo = hi = None
        for k in range(i, len(lines)):
            if lo is None and lines[k] == a:
                lo = k + 1
            elif lo is not None and lines[k] == b:
                hi = k + 1
                break
        if lo is None or hi is None:
            die('span %s/%s not found after line %d of %s'
                     % (arm, role, i + 1, main_hs))
        out[(arm, role)] = (lo, hi)
    # Spans are trimmed against each other in ROLE order, an opening
    # anchor being allowed to sit on the previous role's closing line --
    # which is how the source reads and would otherwise count those lines
    # twice. Overlap that survives the trim is a defect and refuses.
    for arm in FUNCS:
        prev = None
        for role in ROLES:
            k = (arm, role)
            if k not in out:
                continue
            lo, hi = out[k]
            if prev is not None and lo <= prev:
                # ONE LINE OF OVERLAP IS THE SOURCE READING AND MORE IS A
                # MIS-SPECIFIED SPAN. Trimming whatever it finds looks like
                # tolerance and is not: give two roles the same opening
                # anchor and an unbounded trim hands back a table that reads
                # exactly like a correct one, which is the failure shape this
                # directory refuses everywhere else. Proved 2026-08-30 by
                # giving `odo` the `run` anchor, which the unbounded form
                # passed silently.
                if prev - lo >= 1:
                    die('spans %s/%s and the role before it overlap by %d'
                             ' line(s), so one of the two anchors is wrong;'
                             ' only the shared boundary line is trimmed'
                             % (arm, role, prev - lo + 1))
                lo = prev + 1
                out[k] = (lo, hi)
            if lo > hi:
                die('span %s/%s is empty after trimming: %d..%d'
                         % (arm, role, lo, hi))
            prev = hi
    seen = {}
    for (arm, role), (lo, hi) in out.items():
        for k in range(lo, hi + 1):
            if (arm, k) in seen:
                die('line %d of %s is in both %s and %s'
                         % (k, arm, seen[(arm, k)], role))
            seen[(arm, k)] = role
    harness = [i + 1 for i, l in enumerate(lines) if HARNESS.match(l)]
    return out, set(harness)


def main():
    if len(sys.argv) not in (2, 3):
        die(__doc__)
    arms, cur, built = {}, None, None
    for ln in open(sys.argv[1]):
        m = re.match(r'^# Main\.hs at ([0-9a-f]{7,})\s*$', ln)
        if m:
            built = m.group(1)
        m = re.match(r'^=== (\S+) ', ln)
        if m:
            cur = m.group(1)
            arms[cur] = {}
            continue
        m = re.match(r'^\s+[0-9.]+%\s+(\d+)\s+(\S+)', ln)
        if m and cur:
            arms[cur][m.group(2)] = arms[cur].get(m.group(2), 0) + int(m.group(1))
    if not arms:
        die('no arm sections in that file')
    here = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) == 3:
        main_hs, src = sys.argv[2], open(sys.argv[2]).read()
    elif built:
        main_hs = 'Main.hs at %s' % built
        got = subprocess.run(['git', 'show', '%s:./Main.hs' % built],
                             capture_output=True, text=True, cwd=here)
        if got.returncode != 0:
            die('%s: git show refused -- %s' % (main_hs, got.stderr.strip()))
        src = got.stdout
    else:
        main_hs = os.path.join(here, 'Main.hs')
        src = open(main_hs).read()
        print('!! the histogram names no Main.hs build, so this reads the'
              ' working tree, whose line numbers may not be the twin\'s')
    sp, harness = spans(src, main_hs)

    def bucket(arm, counts):
        out = dict.fromkeys(ROLES, 0)
        out['harness'] = out['elsewhere'] = 0
        for site, n in counts.items():
            m = re.match(r'^Main\.hs:(\d+)$', site)
            if not m:
                out['elsewhere'] += n
                continue
            k = int(m.group(1))
            if k in harness:
                out['harness'] += n
                continue
            for role in ROLES:
                sp_k = (arm, role)
                if sp_k in sp and sp[sp_k][0] <= k <= sp[sp_k][1]:
                    out[role] += n
                    break
            else:
                out['elsewhere'] += n
        return out

    # THE HARNESS IS THE CHECK ON THE FILE: every arm is timed through it,
    # so an arm with no sample there was read against a Main.hs whose
    # line numbers are not the twin's, and the table was wrong in every
    # column and said nothing (2026-09-18). Refused before it is printed.
    for arm, counts in arms.items():
        if (arm, ROLES[0]) in sp and not any(
                int(m.group(1)) in harness for m in
                (re.match(r'^Main\.hs:(\d+)$', s) for s in counts) if m):
            die('%s: no sample of %s falls in the harness, so %s is not the'
                ' file the twin was built from; give that build\'s Main.hs'
                ' as the second argument' % (sys.argv[1], arm, main_hs))
    hdr = ROLES + ['harness', 'elsewhere', 'total']
    print(('%-16s' + '%11s' * len(hdr)) % tuple(['arm'] + hdr))
    got, unknown = {}, 0
    for arm, counts in arms.items():
        if (arm, ROLES[0]) not in sp:
            print('%-16s   -- no spans known for this arm, counted whole: %d'
                  % (arm, sum(counts.values())))
            unknown = 1
            continue
        b = bucket(arm, counts)
        got[arm] = b
        print(('%-16s' + '%11d' * len(hdr))
              % tuple([arm] + [b[c] for c in hdr[:-1]] + [sum(b.values())]))
    # The difference row is the file's two bucketed arms, second minus
    # first, where it carries exactly two, and not a pair of names: the
    # histograms here carry the add-in-leaf arm beside `lib-stage2-lean`,
    # and no `lib-stage2` at all.
    if len(got) == 2:
        (na, a), (nb, b) = got.items()
        hdr = ROLES + ['harness', 'elsewhere']
        print(('%-16s' + '%11d' * (len(hdr) + 1) + '   <-- %s minus %s')
              % tuple(['difference'] + [b[c] - a[c] for c in hdr]
                      + [sum(b.values()) - sum(a.values()), nb, na]))
    # AND EQUAL ACROSS THE ARMS, which is what makes it the control: a
    # harness a hundredth apart is the sampling; wider is a finding.
    hs = [b['harness'] for b in got.values()]
    if len(hs) > 1 and max(hs) - min(hs) > 0.01 * max(hs):
        print('!! the harness bucket differs across the arms by more than'
              ' 1%%: %s' % ', '.join('%s %d' % (a, b['harness'])
                                      for a, b in got.items()))
        unknown = 1
    return unknown


sys.exit(main())
