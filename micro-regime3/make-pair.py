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
    ./make-pair.py --regime ''           # plain -O1 instead of -fspec-constr

Four builds, about five minutes, and it refuses rather than guesses: a phase
match below the threshold, a moved fill, a failing `check` or a fill not at
offset 0 is reported and the binaries are left for inspection. What it prints
is the provenance a run should keep -- README's open list quotes these figures
for the pair Run 10 uses, and re-running this is how a later `Main.hs` gets
its own.

Non-vacuity. Run at `--min-phase 99` against a pair that reaches 95, it
reports the phase failure and exits 1, where the default 90 exits 0 -- so the
refusal is live and not decoration. The `check` branch has its own history:
the first version of `align-as.py` padded 928 labels instead of 395, and the
binary it produced failed `check` on the first shape while its offsets still
looked right, which is why that branch is here and why offsets alone are not
the gate. The tool is deterministic on this tree: three runs gave the same
PAD_BYTES and binaries md5-identical to the pair built by hand.
"""
import argparse
import collections
import importlib.util
import os
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
    groups = collections.Counter(f['bytes'] for f in lo.scan(b, 28))
    return sorted(tuple(sorted(f['mod'] for f in lo.scan(b, 28)
                               if f['bytes'] == body))
                  for body, n in groups.items() if n >= 4)


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--prefix', default='micro')
    p.add_argument('--regime', default='-fspec-constr')
    p.add_argument('--min-phase', type=float, default=90.0,
                   help='%% of library loops that must share an offset')
    a = p.parse_args()

    aligned = f'{a.prefix}-aligned'
    unaligned = f'{a.prefix}-unaligned'
    plain = f'{a.prefix}-plain-tmp'

    print('1/4  plain build, to measure what aligning costs in .text')
    build('db-plain-tmp', plain, a.regime)
    print('2/4  aligned build')
    build('db-aligned', aligned, a.regime, pgma='align-as.py')
    pad = text_size(aligned) - text_size(plain)
    print(f'     .text grows {pad} bytes')

    print(f'3/4  padded build at PAD_BYTES={pad}, to read the residual phase')
    build('db-pad', unaligned, a.regime, pgma='pad-as.py', pad=pad)
    A, X = lib(aligned), lib(unaligned)
    common = set(A) & set(X)
    delta = collections.Counter(A[s]['start'] - X[s]['start']
                                for s in common).most_common(1)[0][0]
    print(f'     commonest library delta {delta}, i.e. {delta % 64} mod 64')

    if delta % 64:
        pad += delta % 64
        print(f'4/4  rebuilding at PAD_BYTES={pad} to make it a whole number '
              f'of lines')
        build('db-pad', unaligned, a.regime, pgma='pad-as.py', pad=pad)
    else:
        print('4/4  already in phase, no rebuild needed')

    A, X = lib(aligned), lib(unaligned)
    common = set(A) & set(X)
    phase = 100.0 * sum(1 for s in common if A[s]['mod'] == X[s]['mod']) / len(common)
    strad = 100.0 * sum(1 for s in common
                        if A[s]['straddles'] == X[s]['straddles']) / len(common)
    fa, fx, fp = fills(aligned), fills(unaligned), fills(plain)
    agree = sh(f'./{unaligned} check')
    ok, bad = agree.count('agree=True'), agree.count('agree=False')

    print(f'\nPAD_BYTES={pad}')
    print(f'  .text            {text_size(unaligned)} vs {text_size(aligned)}')
    print(f'  library phase    {phase:.0f}% share an offset, {strad:.0f}% the '
          f'same straddle state')
    print(f'  fills aligned    {fa}')
    print(f'  fills unaligned  {fx}   (plain: {fp})')
    print(f'  check            {ok} agree, {bad} disagree')

    fail = []
    if phase < a.min_phase:
        fail.append(f'library phase {phase:.0f}% below --min-phase')
    if fx != fp:
        fail.append('padding moved a fill: the unaligned half is not the '
                    'plain build with padding after it')
    if bad or not ok:
        fail.append('the unaligned half does not agree on every shape')
    if any(m != 0 for grp in fa for m in grp):
        fail.append('a fill is not at offset 0 in the aligned half')
    sh(f'rm -f {plain}')
    for f in fail:
        print('FAIL: ' + f)
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
