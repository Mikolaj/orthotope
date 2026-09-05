#!/usr/bin/env python3
"""Gate 3's sign, adjudicated at fixed iteration counts.

The gate fails when the in-situ forcing term's medians leave 1 on the same
side by more than a few percent. From Run 16 they read ABOVE 1 where Runs 8
to 10 read below. README's entry names the measurement: the `-nosum` arms
read against `sum-only` at FIXED ITERATION COUNTS rather than through
criterion, which separates a biased READ from two biased ARMS. Taken
2026-09-05, and the reading is in that entry: the arms.

(t(2N) - t(N)) / N is the per-call cost and owes nothing to criterion's
sampling or its analysis; every per-process constant, the preamble
included, cancels in the subtraction.

TWO VERSIONS OF THIS WERE WRONG. N is per bench: the first used one N for
every bench and produced ratios of 8 to 27 with a negative among them,
because `sum-only` is microseconds per call: at N=1000 its timed work is
milliseconds against tens of milliseconds of process-to-process wall
noise, so the denominator was noise. N is now calibrated per bench off the
run's own slopes so every run takes about two seconds, and each is
repeated with the MINIMUM taken, timing noise being one-sided. The second
passed bare bench names, which criterion's -n mode matches as PREFIXES:
`SHAPE/list` ran three benches and `SHAPE/mut-odo-vecdims` eight, read as
3.06x and 6.98x inflation against criterion, while `-nosum` and
`sum-only-early` are prefixes of nothing and read exact. `-m glob` selects
one, and `wall` counts the `benchmarking` lines and refuses any count but
one, which is README's rule for every filtered probe made by hand.

Run by hand on a quiet box, one process at a time; a shape on one half is
about four minutes, the saturating preamble running once per process. Not
covered by the corpus: it is a probe, and its output is an input to README.
"""
import os, subprocess, sys, time, statistics as stats

HALVES = ['run25-g912', 'run25-ghead']
SHAPES = ['cnn-L1-24x24-c1', 'lenet-L1-28-c1-k5', 'gather48-src-50',
          'stretch-coprime-r7']
PAIRS = [('mut-odo-vecdims', 'mut-odo-vecdims-nosum'),
         ('bq-expand', 'bq-expand-nosum')]
CTRL = ['sum-only-early', 'sum-only-late']
TARGET_S = 2.0
REPS = 3
ENV = dict(os.environ, SATURATE='1')


def slopes(binary):
    """Per-call seconds per shape/arm, from that half's own main-set JSON."""
    j = binary + '-main.json'
    out = subprocess.run(['./read-run.py', j, '--cells'], check=True,
                         capture_output=True, text=True).stdout
    d = {}
    for ln in out.splitlines():
        f = ln.split('\t')
        if len(f) >= 3 and f[0] != 'shape':
            try:
                d[(f[0], f[1])] = float(f[2])
            except ValueError:
                pass
    return d


def wall(binary, bench, n):
    best = None
    for _ in range(REPS):
        t0 = time.perf_counter()
        r = subprocess.run(['./' + binary, '-m', 'glob', '-n', str(n), bench],
                           capture_output=True, text=True, env=ENV)
        dt = time.perf_counter() - t0
        nb = (r.stdout + r.stderr).count('benchmarking ')
        if nb != 1:
            sys.exit('%s -n %d %r selected %d benches'
                     % (binary, n, bench, nb))
        if r.returncode != 0:
            sys.exit('%s -n %d %r rc=%d' % (binary, n, bench, r.returncode))
        best = dt if best is None else min(best, dt)
    return best


def percall(binary, sl, shape, arm):
    est = sl.get((shape, arm))
    if not est or est <= 0:
        return None
    n = max(1000, int(TARGET_S / est))
    return (wall(binary, '%s/%s' % (shape, arm), 2 * n)
            - wall(binary, '%s/%s' % (shape, arm), n)) / n


def main():
    print('# gate 3 at fixed iters: (t(2N)-t(N))/N, N per bench for ~%.0fs,'
          ' min of %d, SATURATE=1, -m glob' % (TARGET_S, REPS))
    for binary in HALVES:
        sl = slopes(binary)
        print('\n== %s' % binary)
        rows = {}
        for shape in SHAPES:
            cs = [percall(binary, sl, shape, c) for c in CTRL]
            if any(c is None or c <= 0 for c in cs):
                print('   %-20s control not positive, skipped' % shape)
                continue
            ctrl = stats.fmean(cs)
            for base, nosum in PAIRS:
                a, b = (percall(binary, sl, shape, base),
                        percall(binary, sl, shape, nosum))
                if a is None or b is None:
                    continue
                r = (a - b) / ctrl
                rows.setdefault(base, []).append(r)
                print('   %-20s %-16s in-situ %8.3f us  sum-only %8.3f us'
                      '  ratio %7.4f'
                      % (shape, base, (a - b) * 1e6, ctrl * 1e6, r))
        for base, rs in rows.items():
            print('   MEDIAN %-16s %.4f over %d shape(s)'
                  % (base, stats.median(rs), len(rs)))


main()
