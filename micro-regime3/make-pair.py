#!/usr/bin/env python3
"""Build a paired run's two binaries: one with its loops aligned, one padded
to the same size and cache-line phase.

A paired run wants two builds differing in Main's loop alignment and in
nothing else an offset can see. `align-as.py` gives the aligned half but grows
`.text`, which moves every library linked after it, so a plain build is not
the counterpart it looks like: the libraries land at different offsets and
their own straddles are rerolled rather than held. `pad-as.py` fixes that
given the right PAD_BYTES, and the right PAD_BYTES is two measurements deep.
This does both, and then checks that it worked.

    ./make-pair.py                       # micro-aligned and micro-unaligned
    ./make-pair.py --prefix try          # try-aligned and try-unaligned
    ./make-pair.py --regime=''           # plain -O1 instead of -fspec-constr
    ./make-pair.py --regime=-fspec-constr        # the default, spelled out
    ./make-pair.py --verify-only         # re-gate what is here, build nothing

--regime takes the bare GHC flag, which this wraps in --ghc-options itself,
having a -pgma of its own to compose it with. The `=` is not optional when
the value is a real flag: argparse reads a dash-leading word as the next
option and exits 2 saying --regime expected one argument, so `--regime
-fspec-constr` never reaches a build. Only the empty form survives the
space, which is exactly the spelling that would not have caught this.

Four builds, about five minutes, and it refuses rather than guesses: a phase
match below the threshold, a moved fill, a failing `check`, halves that
disagree with each other or list different benches, or a fill not at offset 0
is reported and the binaries are left for inspection. It writes
`<prefix>-pair.txt` beside the binaries with everything it measured, the
verdict, and a line saying the gate has not been run; `run-gate.sh` appends
to that file, so what a later session needs to know about the pair travels
with the pair rather than with whoever built it.

`--verify-only` re-gates the binaries already here and builds nothing, which
is README's fork for a pair it would be wrong to rebuild -- the offsets a
run's predictions are registered against are that pair's. Two gates need the
plain build and so do not run: PAD_BYTES is not re-derived and the moved-fill
comparison has nothing to compare against. Both the note and the verdict say
which.

Whether the note is appended to or replaced is not a mode but a fact about
the binaries, decided in `note_mode` off the md5s the note records: the same
pair keeps its gate verdict, a different one does not, and a note too old to
carry md5s is appended to rather than destroyed on a guess. A rebuild is
therefore not automatically a fresh start -- this tool is deterministic, so
the usual rebuild reproduces the pair byte for byte and the verdict above it
still applies to it.

Non-vacuity. `--min-phase 99` against a pair that reaches 95 reports the
phase failure and exits 1, where the default 90 exits 0. The rest are refusals
about a mispadded binary, which cannot be conjured on demand -- so they live
in `gates`, out of `main`, and are exercised by calling it with crafted
values. Against the live pair's measurements it returns nothing; each of the
eight breaks below fires exactly the branch it should, checked 2026-08-10:
a phase of 80, a plain-build fill differing in one offset, a plain-build fill
differing only in ORDER, either half's `check` exiting 1, the aligned half
disagreeing while exiting 0, the two logs differing, the two listings
differing, and an aligned fill away from 0. The order case is the one worth
naming: it fires only because `fills` stopped sorting, and it did not fire
before. `fp=None` correctly fires nothing, that being the verify-only skip.

`note_mode` is out of `main` for the same reason and proven the same way,
each of its four answers costing a build otherwise: no note at all writes a
fresh one; a note whose md5s match appends, saying re-verified or rebuilt
according to which happened; a note whose md5s differ is replaced and says so,
naming the gate verdict it is dropping; and a note carrying no md5s is
appended to unjudged. That branch is not decoration: Run 10's note was
hand-written before md5s were recorded and would have hit it, until the two
hashes were added to it by hand, which is also the cheapest way to retire the
branch for any note that predates them.

The `check` refusals have a history behind them. The first version of
`align-as.py` padded 928 labels instead of 395, and the binary it produced
failed `check` on the first shape while its offsets still looked right, which
is why the branch is here and why offsets alone are not the gate. `check`
runs against BOTH halves, the aligned one being the only one that can be
mispadded; it ran against the unaligned half alone until 2026-08-10, which
pointed the gate at the binary that could not fail. It also runs through
`sh_rc` rather than `sh`, since `check` reports a disagreement by exiting
nonzero and `sh` would abort before any of this could be written down.

The tool is deterministic on this tree: three runs gave the same PAD_BYTES and
binaries md5-identical to the pair built by hand. The note records both md5s,
so that claim can be checked against something.
"""
import argparse
import collections
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = ('build/x86_64-linux/ghc-9.12.4/micro-0.1/x/micro/build/micro/micro')
_spec = importlib.util.spec_from_file_location(
    'lo', os.path.join(HERE, 'loop-offsets.py'))
lo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lo)


def sh(cmd, env=None):
    e = dict(os.environ, **(env or {}))
    r = subprocess.run(cmd, shell=True, cwd=HERE, env=e,
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'FAILED: {cmd}\n{r.stdout[-2000:]}{r.stderr[-2000:]}')
    return r.stdout


def sh_rc(cmd):
    """Like `sh`, but hands the failure back instead of dying on it.

    `check` reports a disagreement by `error`ing on the first one, so it exits
    nonzero and `sh` would abort the whole tool right there. Loud, but it
    aborts BEFORE the note is written and before the two refusals about
    disagreement can name which half failed -- which is to say those refusals
    were unreachable, and the aligned one had been added precisely to carry
    the sentence about a mispadded binary whose offsets still look right.

    Returns the two streams apart, which is not fastidiousness: the binary
    writes its provenance line to stderr precisely to leave `--list` and
    criterion's stdout machine-readable, so folding the two together counts
    that line as a bench and reports one more than the roster holds.
    """
    r = subprocess.run(cmd, shell=True, cwd=HERE, capture_output=True,
                       text=True)
    return r.returncode, r.stdout, r.stderr


def build(builddir, out, regime, pgma=None, pad=None):
    opts = f'--ghc-options="{regime}"' if regime else ''
    if pgma:
        opts += f' --ghc-options="-pgma {HERE}/{pgma} -fforce-recomp"'
    sh(f'rm -rf {builddir}')
    sh(f'cabal build micro --builddir={builddir} {opts}',
       env={'PAD_BYTES': str(pad)} if pad is not None else None)
    sh(f'cp {builddir}/{BIN} {out}')
    sh(f'rm -rf {builddir}')
    return out


def text_size(b):
    for line in sh(f'size -A {b}').split('\n'):
        if line.startswith('.text'):
            return int(line.split()[1])
    sys.exit(f'no .text in {b}')


def heads(b):
    h = {}
    for f in lo.scan(b, None):
        cur = h.get(f['start'])
        if cur is None or f['len'] < cur['len']:
            h[f['start']] = f
    return h


def lib(b):
    return {f['sym']: f for f in heads(b).values()
            if '_Main_' not in (f['sym'] or '')}


def fills(b):
    """The fill groups in ADDRESS order, which is the order the page reads.

    Position carries the arm here: `loop-offsets.py`'s own header reads the
    build/mut-odo group as [dead, mut-odo, dead, build], so the second and
    fourth entries are the two arms Run 10's fourth prediction is stated on,
    and README quotes the group as [3, 53, 59, 45] throughout. Sorting kept
    the multiset and lost that -- the note recorded (3, 45, 53, 59), the same
    four numbers saying something else -- so nothing here sorts, at either
    level. It also makes the `fx != fp` refusal below stricter, since a
    reordering now fails it where two sorted tuples compared equal.
    """
    found = lo.scan(b, 28)
    groups = collections.Counter(f['bytes'] for f in found)
    return [[f['mod'] for f in found if f['bytes'] == body]
            for body, n in groups.items() if n >= 4]


def note_mode(old, want_md5, verify_only):
    """Append to the pair note, or replace it? -> (appending, head, warning).

    One question decides it: is the pair the note describes the pair now on
    disk? The md5s the note records make that answerable rather than assumed,
    which matters because the gate verdict `run-gate.sh` appends is the only
    thing in the file that cost an hour. Same hashes -- a re-verification, or
    a rebuild this tool's determinism reproduced -- and the verdict still
    applies, so append and leave the standing text alone; re-emitting it would
    restate "GATE: not yet run" underneath a verdict saying it did. Different
    hashes and these are other binaries, so the note is replaced and whatever
    goes with it is named on the way out rather than vanishing. A note with no
    md5s at all cannot be judged -- it predates their being recorded, as Run
    10's hand-written one does -- and is appended to rather than destroyed on
    a guess.

    Out here rather than inline so the four answers can be had without four
    builds; the proofs are in the module docstring.
    """
    old_md5 = set(re.findall(r'^  md5 \w+\s+([0-9a-f]{32})$', old, re.M))
    if not old:
        return False, [], ''
    if not old_md5:
        return True, ['', 'APPENDED -- the note above records no md5s, so'
                      ' whether it', 'describes these binaries could not be'
                      ' checked:'], ''
    if old_md5 == want_md5:
        if verify_only:
            return True, ['', 'RE-VERIFIED, building nothing:'], ''
        return True, ['', 'REBUILT -- the md5s came out unchanged, so this is'
                      ' the same', 'pair and whatever is recorded above still'
                      ' applies to it:'], ''
    return False, [], ('described a different pair (md5s differ) and has been'
                       ' replaced' + ('; it recorded a GATE line, which does'
                                      ' not carry to these binaries'
                                      if 'GATE' in old else ''))


def gates(*, min_phase, phase, fa, fx, fp, uncheck, alcheck, same,
          listed_same):
    """Every refusal, as a function of what was measured and nothing else.

    Out here rather than inline in `main` so that each can be exercised
    without a build: import this module, call this with crafted values, and
    the branch either fires or does not. That is the only way most of them
    can be proven at all -- a mispadded binary is what the `check` refusals
    are about, and producing one on purpose costs an assembler shim and five
    minutes per attempt. The proofs are recorded in the module docstring.

    `uncheck` and `alcheck` are each (exit code, agree count, disagree count);
    `fp` is None when there was no plain build to compare against.
    """
    rc_u, ok, bad = uncheck
    rc_a, ok_a, bad_a = alcheck
    fail = []
    if phase < min_phase:
        fail.append(f'library phase {phase:.0f}% below --min-phase')
    if fp is not None and fx != fp:
        fail.append('padding moved a fill: the unaligned half is not the '
                    'plain build with padding after it')
    if rc_u or bad or not ok:
        fail.append('the unaligned half does not agree on every shape')
    if rc_a or bad_a or not ok_a:
        fail.append('the aligned half does not agree on every shape -- the'
                    ' padding is wrong, and its offsets will look right')
    if not same:
        fail.append('the two halves disagree with each other about some'
                    ' shape, where padding alone cannot change an answer')
    if not listed_same:
        fail.append('the two halves list different benches, so no run over'
                    ' them can be pinned to one selection')
    if any(m != 0 for grp in fa for m in grp):
        fail.append('a fill is not at offset 0 in the aligned half')
    return fail


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--run', required=True,
                   help='the run this pair is for, e.g. run13. It goes in'
                        ' every name this directory holds -- both binaries and'
                        ' the note -- so two runs cannot write one filename'
                        ' however alike their half names are. Required rather'
                        ' than defaulted: run-gate.sh once named its output'
                        ' without a run and silently overwrote the previous'
                        " gate's.")
    p.add_argument('--basis', default='aligned',
                   help='the half this builds with the shim (default aligned)')
    p.add_argument('--other', default='unaligned',
                   help='its counterpart, which --verify-only must be told'
                        ' when the pair is not an unaligned/aligned one')
    p.add_argument('--regime', default='-fspec-constr')
    p.add_argument('--min-phase', type=float, default=90.0,
                   help='%% of library loops that must share an offset')
    p.add_argument('--verify-only', action='store_true',
                   help='re-gate the pair already here, building nothing')
    a = p.parse_args()
    a.prefix = f'micro-{a.run}'

    aligned = f'{a.prefix}-{a.basis}'
    unaligned = f'{a.prefix}-{a.other}'
    if not a.verify_only and (a.basis, a.other) != ('aligned', 'unaligned'):
        sys.exit('this builds an unaligned/aligned pair and models no other:'
                 ' --basis/--other are for pointing --verify-only at a pair'
                 ' built by hand, not for building one')
    plain = f'{a.prefix}-plain-tmp'
    pad = fp = None

    if a.verify_only:
        # README's procedure forks here: a pair already in the directory is
        # confirmed rather than rebuilt, since rebuilding it can retire the
        # offsets a run's predictions are registered against. Two gates need
        # the plain build and so cannot run: PAD_BYTES is not re-derived, and
        # the moved-fill comparison has nothing to compare against. The note
        # says which, rather than reading as a full pass.
        for b in (aligned, unaligned):
            if not os.path.exists(os.path.join(HERE, b)):
                sys.exit(f'--verify-only wants {b} beside this script')
        print('verify-only: building nothing; PAD_BYTES and the moved-fill'
              ' gate are not re-derived')
    else:
        print('1/4  plain build, to measure what aligning costs in .text')
        build('db-plain-tmp', plain, a.regime)
        print('2/4  aligned build')
        build('db-aligned', aligned, a.regime, pgma='align-as.py')
        pad = text_size(aligned) - text_size(plain)
        print(f'     .text grows {pad} bytes')

        print(f'3/4  padded build at PAD_BYTES={pad}, to read the residual '
              f'phase')
        build('db-pad', unaligned, a.regime, pgma='pad-as.py', pad=pad)
        A, X = lib(aligned), lib(unaligned)
        common = set(A) & set(X)
        delta = collections.Counter(A[s]['start'] - X[s]['start']
                                    for s in common).most_common(1)[0][0]
        print(f'     commonest library delta {delta}, i.e. {delta % 64} mod 64')

        if delta % 64:
            pad += delta % 64
            print(f'4/4  rebuilding at PAD_BYTES={pad} to make it a whole '
                  f'number of lines')
            build('db-pad', unaligned, a.regime, pgma='pad-as.py', pad=pad)
        else:
            print('4/4  already in phase, no rebuild needed')
        fp = fills(plain)

    A, X = lib(aligned), lib(unaligned)
    common = set(A) & set(X)
    phase = 100.0 * sum(1 for s in common if A[s]['mod'] == X[s]['mod']) / len(common)
    strad = 100.0 * sum(1 for s in common
                        if A[s]['straddles'] == X[s]['straddles']) / len(common)
    fa, fx = fills(aligned), fills(unaligned)
    # Both halves, and the aligned one is the half that matters: it is the
    # one the shim rewrote and so the only one that can be mispadded. This
    # checked the unaligned half alone until 2026-08-10, which is to say it
    # pointed its gate at the binary that could not fail. Tolerantly, via
    # sh_rc: `check` errors out on the first disagreement, so `sh` would take
    # the tool down with it and write no note at all.
    rc_u, agree_u, err_u = sh_rc(f'./{unaligned} check')
    rc_a, agree_a, err_a = sh_rc(f'./{aligned} check')
    ok, bad = agree_u.count('agree=True'), agree_u.count('agree=False')
    ok_a, bad_a = agree_a.count('agree=True'), agree_a.count('agree=False')
    same = agree_u == agree_a
    # The roster the two halves would time. Identical listings are what lets a
    # run pin its selection across the pair; differing ones mean these are not
    # two builds of one program, whatever the offsets say.
    _, list_u, _ = sh_rc(f'./{unaligned} --list')
    _, list_a, _ = sh_rc(f'./{aligned} --list')
    benches, listed_same = len(list_u.strip().split('\n')), list_u == list_a

    fail = gates(min_phase=a.min_phase, phase=phase, fa=fa, fx=fx, fp=fp,
                 uncheck=(rc_u, ok, bad), alcheck=(rc_a, ok_a, bad_a),
                 same=same, listed_same=listed_same)

    # Provenance the note used to leave to a hand-written file: without the
    # commit a deleted artifact cannot be repeated even in principle
    # (README's step 9), and without the md5s the determinism claim two
    # paragraphs down cannot be checked against anything.
    md5 = dict(reversed(l.split()) for l in
               sh(f'md5sum {unaligned} {aligned}').strip().split('\n'))
    src = sh_rc('git log -1 --format=%h -- Main.hs')[1].strip() or 'unknown'
    dirty = 'modified since' if sh_rc(
        'git status --porcelain -- Main.hs')[1].strip() else 'clean at'
    notderived = 'not re-derived (--verify-only)'
    # Three fields would be assertions about a build that did not happen if
    # --verify-only wrote them plainly: the clock now is not when the pair was
    # made, the tree's commit now is not the one it was made from, and
    # --regime is then an unused default rather than a flag any build saw.
    # Step 9 transcribes the commit and the regime out of this file, so a
    # confident wrong answer here is worse than an absent one.
    stamp = 'verified' if a.verify_only else 'built'
    source = (f'tree is {dirty} {src}, and the pair predates this line'
              if a.verify_only else f'{dirty} {src}')
    regime = notderived if a.verify_only else (a.regime or '-O1 (empty)')
    verdict = ('PASSED every gate' if not fail
               else f'FAILED {len(fail)} gate(s), listed below')
    if a.verify_only:
        verdict += '; two of them not run, this being --verify-only'
    measured = [
        f'  {stamp:15s}  {sh("date -Is").strip()}',
        f'  Main.hs          {source}',
        f'  GHC              {BIN.split("/ghc-")[1].split("/")[0]}',
        f'  regime           {regime}',
        f'  PAD_BYTES        {pad if pad is not None else notderived}',
        f'  .text            {text_size(unaligned)} vs {text_size(aligned)}',
        f'  md5 {a.other:12s} {md5[unaligned]}',
        f'  md5 {a.basis:12s} {md5[aligned]}',
        f'  library phase    {phase:.0f}% share an offset, {strad:.0f}% the '
        f'same straddle state',
        f'  fills {a.basis:10s} {" and ".join(map(str, fa))}',
        f'  fills {a.other:10s} {" and ".join(map(str, fx))}',
        f'  fills plain      {" and ".join(map(str, fp)) if fp else notderived}',
        f'  --list           {benches} benches, '
        f'{"identical" if listed_same else "DIFFERING"} between the halves',
        f'  check {a.other:10s} {ok} agree, {bad} disagree, exit {rc_u}',
        f'  check {a.basis:10s} {ok_a} agree, {bad_a} disagree, exit {rc_a}'
        f'{"" if same else "  -- AND IT DIFFERS FROM THE OTHER HALF"}',
        f'  make-pair.py     {verdict}',
    ] + [f'  FAIL: {f}' for f in fail]
    standing = [
        'Do not rebuild either between the halves of a run: that is what the',
        'pairing measures. make-pair.py is deterministic, so a rebuild whose',
        'md5s match the two above is the same pair and inherits whatever is',
        'recorded below.',
        '',
        'GATE: not yet run against this pair. run-gate.sh appends its verdict',
        'here, and README\'s procedure says the gate belongs to the pair rather',
        'than to the session -- if the lines below say it passed, the next',
        'action is the run itself and not another gate.',
    ]
    # Whether to append to the note or start a new one turns on ONE question:
    # is the pair described in it the pair now on disk? The md5s above make
    # that answerable rather than assumed, which matters because the gate
    # verdict run-gate.sh appends is the only thing in the file that cost an
    # hour. Same hashes -- a re-verification, or a rebuild the tool's
    # determinism reproduced -- and the verdict still applies, so append and
    # leave the standing text where it is; re-emitting it would restate
    # "GATE: not yet run" under a verdict saying it did. Different hashes and
    # these are other binaries, so the note is replaced and what goes with it
    # is named on the way out. A note with no md5s at all cannot be judged --
    # it predates their being recorded -- and is appended to rather than
    # destroyed on a guess.
    path = os.path.join(HERE, f'{a.prefix}-pair.txt')
    old = open(path).read() if os.path.exists(path) else ''
    appending, head, warn = note_mode(old, {md5[unaligned], md5[aligned]},
                                      a.verify_only)
    # A note it would REPLACE, carrying a gate verdict, is an hour of someone
    # else's quiet machine and possibly the only copy of a hand-built half's
    # recipe. Replacing it is right after a rebuild -- the binaries really are
    # other ones -- and wrong when this tool has simply been pointed at the
    # wrong pair, which is what happens by default beside a hand-built one:
    # both default names still exist, so nothing above refuses. Refuse here
    # instead, and name the flags that say which pair is meant.
    if not appending and 'GATE' in old:
        sys.exit(f'{a.prefix}-pair.txt describes a different pair'
                 f' ({a.basis}/{a.other} are what this looked at) and records'
                 f' a GATE verdict, so replacing it would drop an hour of'
                 f' machine time and whatever else is written by hand there.'
                 f' Pass --basis/--other for the pair you mean, or move the'
                 f' note aside if you really are starting again.')
    if warn:
        print(f'NOTE: {a.prefix}-pair.txt {warn}')
    if appending:
        note = head + measured + ['']
    else:
        note = [f'The pair {unaligned} and {aligned}, built by make-pair.py.',
                ''] + measured + [''] + standing + ['']
    with open(path, 'a' if appending else 'w') as f:
        f.write('\n'.join(note))
    print('\n'.join(measured))
    print(f'  {"appended to" if appending else "written to":16} '
          f'{a.prefix}-pair.txt')

    if not a.verify_only:
        sh(f'rm -f {plain}')
    for f in fail:
        print('FAIL: ' + f)
    # `check` names the shape and the disagreeing arms in the message it dies
    # with, and that message is the whole diagnostic; without this the tool
    # would report that a half disagreed and not say about what.
    for half, rc, err in ((unaligned, rc_u, err_u), (aligned, rc_a, err_a)):
        if rc:
            print(f'--- ./{half} check exited {rc}, saying:\n'
                  f'{err.strip()[-800:]}')
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
