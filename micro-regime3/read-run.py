#!/usr/bin/env python3
"""Read one criterion --json run of this benchmark and print its tables.

Every per-strategy and per-shape figure quoted in README.md comes from here.
Extend this script rather than writing a new one: the definitions below took
a session to settle, and an ad-hoc reader gets them subtly wrong -- which
statistic the trim drops, that CI% is a half-width and not a bound, that the
A/A and sum-only rows are controls, that `l` is not in the JSON at all.

Definitions, once:

  slope   the OLS per-call fit, `anRegress[time].regCoeffs.iters.estPoint`,
          preferred over `anMean` because millisecond-scale benches here ramp
          (README.md#r2-is-the-ramp-detector-not-the-noise-detector).
  CI%     (confIntLDX + confIntUDX) / 2 / slope * 100 -- the mean half-width
          as a percentage of the slope, "how many digits are real". Criterion
          reports the two deviations separately and they differ by up to 1.4x;
          the max is available as ci_hi.
  time    geomean over shapes of slope / `list`'s slope on the same shape,
          with each strategy's own highest-CI shape dropped first (README's
          aggregate: one wild cell moves a 35-shape geomean by 1/35 while
          ordinary noise divides by sqrt 35).
  noise   this row's CI% against the median CI% of the same shape, medianed
          over shapes: 1.00 is an ordinary bench. It is what identifies a
          bench whose own figures are least trustworthy, and so the one to
          suspect of disturbing whatever shares its process -- `concat-runs`
          read 2.45 here and is no longer timed.
  alloc   `anRegress[allocated].regCoeffs.iters.estPoint` / (8 * l), i.e. per
          call as a multiple of the result vector, median over shapes, which
          is what README's column is. The multiples were held shape-independent
          to within half a percent, so that the median smoothed nothing and
          merely avoided privileging one shape. That is wrong: over the whole
          shape set they vary by a median 3.93x and a worst 22x, every
          allocated fit at R2 1.000. The median over a PINNED shape set does
          reproduce, which is what keeps the column meaningful, so it is a
          statistic of a strategy and a shape set both (README.md's alloc
          bullet). `l` is not in the JSON, so it
          is computed from the shape lists in Main.hs; a shape the current
          Main.hs no longer defines reports alloc in bytes instead.

An A/A pair has two ratios and they answer different questions. The ratio of
the two published `time` columns is what a reader comparing two rows of the
table would compute, and it carries the trim's own asymmetry: each arm drops
its own worst-CI shape, so unless that is the same shape the two columns are
geomeans over different shape sets. The paired ratio -- geomean over shapes
of the two slopes on the same shape -- carries measurement noise alone. On
Failed Run 6 they part company exactly where the dropped shapes differ:
1.0200 published against 0.9991 paired, 0.9882 against 0.9999, while the one
pair that drops the same shape from both arms reads 1.0014 either way. So
README's ~2% floor is the right thing to compare two published rows against,
and most of it is the trim rather than the machine; a margin measured
per-shape should be compared against the paired figure instead. --aa prints
both, and says which shape each arm dropped.

Controls, not strategies: the `*-aa-*` rows (an existing strategy run twice
under a second name, true ratio exactly 1, so their spread is the noise
floor) and `sum-only*` (a shared term, and subtracting it from itself divides
by zero). --no-controls drops them from the aggregates; they are always
listed by --aa, which is where they say what they are for. That a control
carries such a name is what --lint holds Main.hs's roster to, this test
being the only thing standing between a renamed control and its silently
entering the aggregates as a strategy.

The one field this script does not read, written down because criterion
documents it nowhere near to hand: `reportMeasured` is the raw sample list,
each sample itself a list whose [0] is the time and [3] the iteration count.
That is the way in to anything the fitted slope hides -- a warm-up ramp, a
lone outlying sample -- where --cells reports only how many samples there
were.

Every mode also warns on stderr about the cells README says to distrust:
R2 under 0.99, fewer than ten samples, a fit too starved for a confidence
interval at all, and an ALLOCATED fit under 0.99 where there was allocation
to fit. Warnings, not a verdict.

Modes:
  (default)         roster summary and the README strategy table
  --shapes          per shape: CI% max / median / mean, trimmed and not
  --drops           which cells the trim removes, grouped by shape
  --aa              the A/A and sum-only control pairs, with their spans
  --cells           every cell as TSV, for anything not covered above
  --exclude S       drop strategy S from every aggregate (repeatable)
  --exclude-shape H drop shape H likewise (repeatable)
  --selftest        check this reader's invariants against the run given
  --lint            check Main.hs's roster against README and against
                    itself -- no run file needed

No run artifacts are kept in this directory: the normal state is none, and
one is made when a question needs it. That is also when this script runs, so
it is written to be useful on a partial run -- a filtered handful of benches,
or a single shape, where the trim has nothing to drop and says so:

    micro -m glob 'cnn-slice-c32/list' 'cnn-slice-c32/bq-expand' --json x.json

takes seconds rather than hours, and exercises everything here but the
aggregates that need a shape set.

Validation: while Failed Run 6's JSON was still in the tree this reader
reproduced README's CI% column to the printed precision (sum-only 0.11,
mut-odo-vecdims 0.15, bq-expand 0.19, bq-mut-runs-mulback 0.42, mut-offsets
0.79, offtab 1.15) and the three ratios of its noise-floor table -- the
evidence that the definitions above are the published ones, which outlives
the artifact. --selftest asserted exactly those figures while they could be
asserted; with the artifact gone, and no later run able to reproduce a
deleted roster, it checks invariants of whatever run it is handed instead,
which is what keeps it live. Run 6 (-O1)'s JSON is not kept either -- that is
decided, not an oversight -- so do not restore a table-pinned EXPECTED
against it: the reader is guarded by invariants and by --lint, and by nothing
that would notice the published table drifting. Each invariant is
non-vacuous: breaking the dims regex, the trim, or the A/A identity fails the
matching check, and all three were broken to confirm it. It exits 2, not 0,
when the run file is missing: a refusal is information.
"""

import argparse
import collections
import json
import math
import os
import re
import signal
import statistics as stats
import sys

TOL = 1e-9


def dims_by_shape(main_hs):
    """Map shape name -> its dims, from the shape lists in Main.hs.

    'mkStrided' views a shape with its two innermost dims transposed, so for
    the listed dims the view's innermost extent sInner is the second-to-last
    and its stride tInner is the last. Hence l = product, m = l / sInner is
    the run count -- the size of the base-offsets table every strategy here
    builds -- and sInner = l / m is how long each copied run is.
    """
    entry = re.compile(r'^\s*(?:[\[,] )?\("([^"]+)",\s*(\[[^\]]*\])\)'
                       r'(?:\s*--\s*(\d+))?')
    out, ann = {}, {}
    try:
        text = open(main_hs).read().split('\n')
    except OSError:
        return out, ann
    for start in ('convShapes', 'stretchShapes'):
        try:
            i = next(k for k, l in enumerate(text)
                     if l.startswith(start + ' ='))
        except StopIteration:
            continue
        for line in text[i + 1:]:
            m = entry.match(line)
            if m:
                out[m.group(1)] = [int(d) for d in re.findall(r'\d+',
                                                              m.group(2))]
                if m.group(3):
                    ann[m.group(1)] = int(m.group(3))
            elif line.strip() == ']':
                break
    return out, ann


def shape_facts(dims):
    """(l, m, sInner) for listed dims; see 'dims_by_shape'."""
    l = math.prod(dims)
    s_inner = dims[-2] if len(dims) > 1 else 1
    return l, (l // s_inner if s_inner else 0), s_inner


def load(path, main_hs):
    """(cells, shapes, strategies, meta); orders follow the run, not
    the file."""
    if not os.path.exists(path):
        sys.stderr.write('%s: no such run file; the analysis did not happen\n'
                         % path)
        sys.exit(2)
    raw = json.load(open(path))
    dims, ann = dims_by_shape(main_hs)
    ell = {s: shape_facts(d)[0] for s, d in dims.items()}
    cells = collections.defaultdict(dict)
    shapes, strategies = [], []
    for r in raw[2]:
        shape, _, strategy = r['reportName'].rpartition('/')
        an = r['reportAnalysis']
        fits = {g['regResponder']: g for g in an['anRegress']}
        t = fits['time']['regCoeffs']['iters']
        # Criterion writes the two bounds independently, and on a starved fit
        # it can write ONE of them null -- 4 samples on
        # stretch-wide-2xM/cm-gather did it. A half-interval is no interval,
        # so both must be present for a CI at all; guarding on `lo` alone
        # crashed the reader on the run that first produced such a cell.
        lo, hi = t['estError']['confIntLDX'], t['estError']['confIntUDX']
        if lo is None or hi is None:
            lo = hi = None
        slope = t['estPoint']
        alloc = fits.get('allocated')
        alloc_b = alloc['regCoeffs']['iters']['estPoint'] if alloc else None
        l = ell.get(shape)
        cells[shape][strategy] = dict(
            slope=slope, r2=fits['time']['regRSquare']['estPoint'],
            n=len(r['reportMeasured']), mean=an['anMean']['estPoint'],
            ci=None if lo is None else (lo + hi) / 2 / slope * 100,
            ci_hi=None if lo is None else max(lo, hi) / slope * 100,
            alloc_bytes=alloc_b,
            alloc_r2=(alloc['regRSquare']['estPoint'] if alloc else None),
            alloc=None if (alloc_b is None or not l) else alloc_b / (8 * l))
        if shape not in shapes:
            shapes.append(shape)
        if strategy not in strategies:
            strategies.append(strategy)
    meta = dict(version=raw[1], reports=len(raw[2]), path=path,
                benches=len(strategies), shapes=len(shapes), dims=dims,
                ann=ann,
                ragged=len(raw[2]) != len(shapes) * len(strategies),
                known_l=sum(1 for s in shapes if s in ell))
    return cells, shapes, strategies, meta


def health(cells, shapes, strategies):
    """What README says to distrust, counted: bad fits and starved cells.

    Warnings, not a verdict -- a ramped bench is normal here and shows up as
    a high mean rather than a low R2
    (README.md#r2-is-the-ramp-detector-not-the-noise-detector).

    The ALLOCATED fit is checked too, and used not to be, so a bad one
    reached the alloc column with nothing saying so. Allocation is
    near-deterministic per call, so its fit is normally exact -- R2 1.000000
    is the median over a run -- and anything short of 0.99 means the column's
    figure for that cell is not to be read. Cells allocating under a tenth of
    their result are exempt: there is no slope to fit there and the R2 is
    noise about zero, which is `sum-only` by construction and nothing else so
    far.

    Non-vacuity, both halves: setting a strategy's allocated R2 to 0.5 warns,
    and lifting a `sum-only` cell's allocation past the exemption warns on the
    bad R2 it already had -- so the exemption is what silences those and not
    something else.
    """
    bad_fit, starved, no_ci, bad_alloc = [], [], [], []
    for sh in shapes:
        for st in strategies:
            c = cells[sh][st]
            if c['r2'] < 0.99:
                bad_fit.append((c['r2'], sh, st))
            if c['n'] < 10:
                starved.append((c['n'], sh, st))
            if c['ci'] is None:
                no_ci.append((sh, st))
            if (c.get('alloc_r2') is not None and c['alloc_r2'] < 0.99
                    and (c['alloc'] or 0) >= 0.1):
                bad_alloc.append((c['alloc_r2'], sh, st))
    out = []
    if bad_fit:
        r2, sh, st = min(bad_fit)
        out.append('%d cell(s) with R2 < 0.99, worst %.4f on %s/%s'
                   % (len(bad_fit), r2, sh, st))
    if starved:
        n, sh, st = min(starved)
        out.append('%d cell(s) under 10 samples, fewest %d on %s/%s'
                   % (len(starved), n, sh, st))
    if no_ci:
        out.append('%d cell(s) with no confidence interval (starved fit): %s'
                   % (len(no_ci), ', '.join('%s/%s' % p for p in no_ci[:3])))
    if bad_alloc:
        r2, sh, st = min(bad_alloc)
        out.append('%d cell(s) with an allocated R2 < 0.99, worst %.4f on'
                   ' %s/%s -- their alloc column figures are not readable'
                   % (len(bad_alloc), r2, sh, st))
    for line in out:
        sys.stderr.write('warning: ' + line + '\n')


def is_control(name):
    return '-aa' in name or name.startswith('sum-only')


def twin_of(name):
    """The row an A/A control duplicates: strip from '-aa' onward."""
    return name[:name.index('-aa')] if '-aa' in name else None


def geomean(xs):
    return math.exp(sum(map(math.log, xs)) / len(xs))


def cis(cells, shape, strategies):
    """The CI% of a shape's cells, minus the fits too starved to have one.

    Criterion writes null bounds when a fit is that thin, which the health
    warnings report; every summary here drops those cells rather than
    refusing to run, since one starved cell should not blind the other 43.
    """
    return [cells[shape][st]['ci'] for st in strategies
            if cells[shape][st]['ci'] is not None]


def med_or_nan(xs):
    return stats.median(xs) if xs else float('nan')


def worst_shape(cells, shapes, strategy):
    """The cell the trim drops: this strategy's highest-CI shape."""
    return max(shapes, key=lambda s: cells[s][strategy]['ci'] or 1e9)


def trimmed_cells(cells, shapes, strategy):
    """Shapes for `strategy` minus its own highest-CI one (README's trim).

    A run of one shape (a filtered run, say) has nothing to trim, and
    dropping its only cell would leave an empty geomean, so it is left whole.
    """
    if len(shapes) < 2:
        return list(shapes)
    worst = worst_shape(cells, shapes, strategy)
    return [s for s in shapes if s != worst]


def time_of(cells, shapes, strategy):
    """README's `time` column: trimmed geomean of slope / `list`'s slope.

    A filtered run need not contain the baseline; then there is no ratio to
    give and the column reads nan rather than the reader stopping.
    """
    kept = trimmed_cells(cells, shapes, strategy)
    if any('list' not in cells[s] for s in kept):
        return float('nan')
    return geomean([cells[s][strategy]['slope'] / cells[s]['list']['slope']
                    for s in kept])


def strategy_table(cells, shapes, strategies, meta, args):
    have_list = all('list' in cells[sh] for sh in shapes)
    typical = {sh: med_or_nan(cis(cells, sh, strategies)) for sh in shapes}
    rows = []
    for st in strategies:
        kept = trimmed_cells(cells, shapes, st)
        ratios = ([cells[s][st]['slope'] / cells[s]['list']['slope']
                   for s in kept] if have_list else [])
        ci = [cells[s][st]['ci'] for s in shapes
              if cells[s][st]['ci'] is not None]
        alloc = [cells[s][st]['alloc'] for s in shapes
                 if cells[s][st]['alloc'] is not None]
        noise = med_or_nan([cells[sh][st]['ci'] / typical[sh]
                            for sh in shapes
                            if typical[sh] and typical[sh] == typical[sh]
                            and cells[sh][st]['ci'] is not None])
        rows.append((geomean(ratios) if ratios else float('nan'),
                     st, med_or_nan(ci), noise,
                     stats.median(cells[s][st]['n'] for s in shapes),
                     stats.median(alloc) if alloc else None))
    rows.sort()
    print('%-28s %7s %6s %6s %5s %8s'
          % ('strategy', 'time', 'CI%', 'noise', 'smp', 'alloc'))
    for time, st, ci, noise, smp, alloc in rows:
        mark = ' *' if is_control(st) else ''
        a = '%7.2fx' % alloc if alloc is not None else '      --'
        print('%-28s %7.3f %6.2f %6.2f %5.0f %s%s'
              % (st, time, ci, noise, smp, a, mark))
    if not have_list:
        print('\ntime is nan: this run has no `list` bench to divide by')
    print('\n* control, not a strategy (--aa explains; --no-controls omits)')
    print('noise is this row\'s CI% against the median CI% of the same shape,')
    print('medianed over shapes: 1.00 is an ordinary bench, and the')
    print('outlier is the bench to suspect of disturbing whatever shares')
    print('its process.')
    if meta['known_l'] < len(shapes):
        print('alloc missing for %d shape(s) Main.hs no longer defines'
              % (len(shapes) - meta['known_l']))


def shape_table(cells, shapes, strategies, meta):
    dropped = {(worst_shape(cells, shapes, st), st) for st in strategies}
    print('%-22s %9s %8s %7s %7s %7s %7s %5s %4s  %s'
          % ('shape', 'l', 'm', 'CImax', 'CImaxT', 'CImed', 'CImean',
             'smp', 'drop', 'worst cell'))
    rows = []
    for sh in shapes:
        ci = {st: cells[sh][st]['ci'] for st in strategies
              if cells[sh][st]['ci'] is not None}
        kept = {st: c for st, c in ci.items() if (sh, st) not in dropped}
        if not ci:
            continue
        mx = max(ci, key=ci.get)
        mxt = max(kept, key=kept.get) if kept else None
        l, m, _ = (shape_facts(meta['dims'][sh]) if sh in meta['dims']
                   else (0, 0, 0))
        rows.append((ci[mx], sh, l, m, kept[mxt] if mxt else float('nan'),
                     stats.median(ci.values()), stats.fmean(ci.values()),
                     stats.median(cells[sh][st]['n'] for st in strategies),
                     sum(1 for s, _ in dropped if s == sh),
                     mx + ('' if mxt in (None, mx) else ' -> ' + mxt)))
    for mx, sh, l, m, mxt, med, mean, smp, nd, who in sorted(rows,
                                                             reverse=True):
        print('%-22s %9s %8s %7.2f %7.2f %7.3f %7.3f %5.0f %4d  %s'
              % (sh, l or '?', m or '?', mx, mxt, med, mean, smp, nd, who))
    print('\nl and m come from Main.hs (m = run count = base-offsets table')
    print('size; sInner = l / m); ? means Main.hs no longer defines it.')
    print('CImaxT is the max after the trim, and drop counts the cells the')
    print('trim removes from that shape. The worst-cell column names the')
    print('strategy, and "a -> b" means the trim took a and left b worst.')


def drop_table(cells, shapes, strategies):
    by_shape = collections.defaultdict(list)
    for st in strategies:
        sh = max(shapes, key=lambda s: cells[s][st]['ci'] or 1e9)
        by_shape[sh].append((cells[sh][st]['ci'], st))
    total = sum(ci for v in by_shape.values() for ci, _ in v
                if ci is not None)
    print('the trim drops one cell per strategy; they land on %d of %d shapes'
          % (len(by_shape), len(shapes)))
    for sh in sorted(by_shape, key=lambda s: -sum(c for c, _ in by_shape[s])):
        v = by_shape[sh]
        s = sum(c for c, _ in v if c is not None)
        print('\n%-24s %d cell(s), CI%% sum %.2f (%.1f%% of %.2f), mean %.2f'
              % (sh, len(v), s, s / total * 100, total, s / len(v)))
        for ci, st in sorted(v, key=lambda x: -(x[0] or 0)):
            print('    %6s  %s'
                  % ('starved' if ci is None else '%6.2f' % ci, st))


def aa_table(cells, shapes, strategies):
    pos = {st: i for i, st in enumerate(strategies)}
    pairs = [(st, twin_of(st)) for st in strategies if twin_of(st)]
    if 'sum-only-early' in pos and 'sum-only-late' in pos:
        pairs.append(('sum-only-late', 'sum-only-early'))
    if not pairs:
        print('no control pairs in this run')
        return
    print('%-28s %-24s %5s %9s %8s %7s'
          % ('control', 'twin', 'span', 'published', 'paired', 'mean|d|'))
    for a, b in pairs:
        if b not in pos:
            continue
        r = [cells[s][a]['slope'] / cells[s][b]['slope'] for s in shapes]
        dev = [abs(x - 1) * 100 for x in r]
        worst = max(zip(dev, shapes))
        wa, wb = worst_shape(cells, shapes, a), worst_shape(cells, shapes, b)
        print('%-28s %-24s %5d %9.4f %8.4f %6.2f%%'
              % (a, b, abs(pos[a] - pos[b]) - 1,
                 time_of(cells, shapes, a) / time_of(cells, shapes, b),
                 geomean(r), stats.fmean(dev)))
        print('%56s worst cell %.2f%% on %s' % ('', worst[0], worst[1]))
        print('%56s trim drops %s / %s%s'
              % ('', wa, wb, '' if wa == wb else '   <-- DIFFERENT shapes, so'
                 ' the published ratio compares different shape sets'))
    print('\nspan is how many benches run between the pair: a pair spanning a')
    print('bench measures whatever that bench leaves behind it. published is')
    print('the ratio of the two `time` columns, what a reader comparing two')
    print('rows gets, trim asymmetry included -- the ~2% floor. paired is the')
    print('per-shape geomean, measurement noise alone; compare a per-shape')
    print('margin against that one. See this script\'s docstring.')


def cell_dump(cells, shapes, strategies):
    print('shape\tstrategy\tslope_s\tci_pct\tci_hi_pct\tr2\tsamples'
          '\talloc_bytes\talloc_mult')
    for sh in shapes:
        for st in strategies:
            c = cells[sh][st]
            print('%s\t%s\t%.9g\t%s\t%s\t%.6f\t%d\t%s\t%s'
                  % (sh, st, c['slope'],
                     'NA' if c['ci'] is None else '%.4f' % c['ci'],
                     'NA' if c['ci_hi'] is None else '%.4f' % c['ci_hi'],
                     c['r2'], c['n'],
                     'NA' if c['alloc_bytes'] is None
                     else '%.6g' % c['alloc_bytes'],
                     'NA' if c['alloc'] is None else '%.4f' % c['alloc']))


ARM_RE = re.compile(r'^\s*[\[,]\s*\("([^"]+)",\s*'
                    r'(Base|Fill|Twin|Term|Only)(?:\s+(fb\w+))?\)')


def roster_of(main):
    """Main.hs's `roster` as (name, role, function) triples, in run order.

    That list is the single source both the benchmark and `check` are built
    from, so what this parses is what actually runs and what is actually
    checked -- there is no second list left to compare it against.
    """
    out = []
    lines = main.split('\n')
    try:
        i = next(k for k, l in enumerate(lines) if l.startswith('roster ='))
    except StopIteration:
        return out
    for line in lines[i + 1:]:
        m = ARM_RE.match(line)
        if m:
            out.append((m.group(1), m.group(2), m.group(3)))
        elif line.strip() == ']':
            break
    return out


def lint(main_hs, readme):
    """Static checks over Main.hs and README.md, needing no run at all.

    The question this used to ask second -- is every benchmarked strategy
    also held to the reference by `check`? -- is gone, and deliberately: the
    roster and the agreement chain were two hand-written lists of the same
    strategies, one list now builds both, and the drift cannot happen rather
    than being merely detectable. A check that cannot fail is a silent
    search, so what replaced it are the ways that one list can still be
    wrong: an arm nobody documented, a strategy defined and rostered
    nowhere, an A/A control not duplicating what its name claims, a control
    named so that this reader counts it as a strategy.

    Non-vacuity, each confirmed by breaking it: renaming a bench in the
    roster fails the README check, commenting an entry out fails the
    rostered check, pointing a `-aa` arm at another function fails the twin
    check, renaming a `Twin` arm to drop its `-aa` fails both the twin and
    the control-naming ones, and a second `Base` entry fails the reference
    check. Each names the arm at fault rather than only the count.
    """
    try:
        main = open(main_hs).read()
        doc = open(readme).read()
    except OSError as e:
        sys.stderr.write('lint: %s\n' % e)
        return 2
    roster = roster_of(main)
    if not roster:
        print('FAIL: no roster parsed out of %s, so none of the checks below'
              ' happened' % main_hs)
        return 1
    names = [n for n, _, _ in roster]
    timed = [n for n, r, _ in roster if r != 'Only']
    fun = {n: f for n, _, f in roster}
    defined = set(re.findall(r'^(fb\w+)\s*::', main, re.M))
    rostered = {f for _, _, f in roster if f}
    twins = [(n, f) for n, r, f in roster if r == 'Twin']

    bad = []
    undocumented = [n for n in names if n not in doc]
    if undocumented:
        bad.append('%d roster arm(s) named nowhere in README: %s'
                   % (len(undocumented), ', '.join(undocumented)))
    else:
        print('ok:   all %d roster arms are named somewhere in README, %d of'
              ' them timed' % (len(names), len(timed)))

    unrostered = sorted(defined - rostered)
    if unrostered:
        bad.append('%d strategy function(s) defined but absent from the'
                   ' roster, so neither timed nor checked: %s'
                   % (len(unrostered), ', '.join(unrostered)))
    else:
        print('ok:   every fb function defined in Main.hs is in the roster'
              ' (%d of them, one of which is the reference)' % len(rostered))

    off = []
    for n, f in twins:
        base = twin_of(n)
        if base is None:
            off.append('%s is an A/A control whose name has no -aa' % n)
        elif base not in fun:
            off.append('%s names %s, which is not in the roster' % (n, base))
        elif fun[base] != f:
            off.append('%s runs %s where %s runs %s'
                       % (n, f, base, fun[base]))
    if off:
        bad.append('A/A control(s) not duplicating what the name says: %s'
                   % '; '.join(off))
    elif twins:
        print('ok:   each of the %d A/A controls runs the same function as'
              ' the arm its name duplicates' % len(twins))

    mislabelled = [n for n, r, _ in roster
                   if is_control(n) != (r in ('Twin', 'Term'))]
    bases = [n for n, r, _ in roster if r == 'Base']
    if mislabelled:
        bad.append('%d arm(s) whose name and role disagree, so this reader'
                   ' would file them in the wrong column: %s'
                   % (len(mislabelled), ', '.join(mislabelled)))
    if len(bases) != 1:
        bad.append('%d Base arm(s), want exactly one -- the reference every'
                   ' other arm is held to: %s'
                   % (len(bases), ', '.join(bases) or 'none'))
    if not mislabelled and len(bases) == 1:
        print('ok:   every control is named as this reader\'s own control'
              ' test reads it, and %s alone is the reference' % bases[0])

    only = [n for n, r, _ in roster if r == 'Only']
    if only:
        print('note: rostered and checked but deliberately not timed, with'
              ' the reason at the entry: %s' % ', '.join(only))
    for line in bad:
        print('FAIL: ' + line)
    return 1 if bad else 0


def selftest(cells, shapes, strategies, meta):
    """Check the reader against invariants, not against a stored run.

    It used to assert Failed Run 6's published columns, which was the right
    check while that JSON sat here; it does not survive the artifact being
    deleted, and no later run can reproduce those numbers -- Run 6 (-O1) has
    a different roster and shape set by construction. So what is checked now is
    what holds of any run this reader is handed, which keeps the check live
    in the normal case: no artifacts in the tree, one made when wanted.
    """
    ok, bad, skip = [], [], []

    known = [sh for sh in shapes if sh in meta['dims']]
    if not known:
        skip.append('no shape of this run is defined in Main.hs, so the'
                    ' shape parse is unexercised (renamed since the run?)')
    else:
        checked = 0
        for sh in known:
            dims = meta['dims'][sh]
            want = meta['ann'].get(sh)
            if want is None:
                continue
            checked += 1
            if math.prod(dims) != want:
                bad.append('%s %s: parsed l=%d against Main.hs\'s own'
                           ' annotation %d'
                           % (sh, dims, math.prod(dims), want))
        if checked:
            ok.append('shape parse: %d of %d shapes found in Main.hs, %d with'
                      ' an l annotation, each matching the dims parsed'
                      % (len(known), len(shapes), checked))
        else:
            skip.append('no shape in Main.hs carries an l annotation, so the'
                        ' dims parse has no oracle here')
        skip.append('sInner = the second-to-last listed dim is a reading of'
                    ' mkStrided, not something a run can confirm: m and'
                    ' alloc inherit it unchecked')

    malformed = [(sh, st) for sh in shapes for st in strategies
                 if not (cells[sh][st]['slope'] > 0
                         and 0.0 <= cells[sh][st]['r2'] <= 1.0
                         and cells[sh][st]['n'] >= 1)]
    if malformed:
        bad.append('%d cell(s) with a non-positive slope, an R2 outside'
                   ' [0,1] or no samples, e.g. %s/%s'
                   % (len(malformed), malformed[0][0], malformed[0][1]))
    else:
        ok.append('cells: %d parsed, all with a positive slope, R2 in [0,1]'
                  ' and at least one sample' % (len(shapes) * len(strategies)))

    if len(shapes) < 2:
        skip.append('one shape only, so the trim and the A/A identity below'
                    ' are unexercised')
    else:
        for st in strategies:
            kept = trimmed_cells(cells, shapes, st)
            ratios = [cells[sh][st]['slope'] / cells[sh]['list']['slope']
                      for sh in shapes]
            got = time_of(cells, shapes, st)
            if len(kept) != len(shapes) - 1:
                bad.append('%s: trim kept %d of %d shapes, want one fewer'
                           % (st, len(kept), len(shapes)))
            elif not min(ratios) - TOL <= got <= max(ratios) + TOL:
                bad.append('%s: trimmed geomean %.6g outside the per-shape'
                           ' range %.6g..%.6g' % (st, got, min(ratios),
                                                  max(ratios)))
        ok.append('trim: one cell dropped per strategy, each trimmed geomean'
                  ' inside its own per-shape range')

        if 'list' in strategies:
            one = time_of(cells, shapes, 'list')
            if abs(one - 1.0) > TOL:
                bad.append('list against itself is %.12g, want 1' % one)
            else:
                ok.append('baseline: list against itself is exactly 1')

        pairs = [(a, twin_of(a)) for a in strategies
                 if twin_of(a) in strategies]
        matched = [(a, b) for a, b in pairs
                   if worst_shape(cells, shapes, a)
                   == worst_shape(cells, shapes, b)]
        if not matched:
            skip.append('no control pair drops the same shape from both arms,'
                        ' so the published-equals-paired identity is'
                        ' unexercised (%d pair(s) present)' % len(pairs))
        for a, b in matched:
            dropped = worst_shape(cells, shapes, a)
            common = [sh for sh in shapes if sh != dropped]
            published = time_of(cells, shapes, a) / time_of(cells, shapes, b)
            paired = geomean([cells[sh][a]['slope'] / cells[sh][b]['slope']
                              for sh in common])
            if abs(published - paired) > 1e-6 * paired:
                bad.append('%s/%s drop the same shape yet published %.6f !='
                           ' paired %.6f' % (a, b, published, paired))
            else:
                ok.append('A/A identity: %s/%s drop %s from both arms and'
                          ' published == paired (%.4f)'
                          % (a, b, dropped, published))

    for line in ok:
        print('ok:   ' + line)
    for line in skip:
        print('skip: ' + line)
    for line in bad:
        print('FAIL: ' + line)
    return 1 if bad else 0


def main():
    # --cells exists to be piped, and the default Python SIGPIPE handler
    # turns `| head` into a traceback rather than a clean stop.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    here = os.path.dirname(os.path.abspath(__file__))
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('run', nargs='?', help='criterion --json output'
                   ' (not needed by --lint)')
    p.add_argument('--main', default=os.path.join(here, 'Main.hs'),
                   help='Main.hs to read shape sizes from'
                        ' (default: alongside)')
    p.add_argument('--shapes', action='store_true')
    p.add_argument('--drops', action='store_true')
    p.add_argument('--aa', action='store_true')
    p.add_argument('--cells', action='store_true')
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--lint', action='store_true')
    p.add_argument('--readme', default=os.path.join(here, 'README.md'),
                   help='README.md to check bench names against'
                        ' (default: alongside)')
    p.add_argument('--no-controls', action='store_true')
    p.add_argument('--exclude', action='append', default=[],
                   metavar='STRATEGY')
    p.add_argument('--exclude-shape', action='append', default=[],
                   metavar='SHAPE')
    args = p.parse_args()

    if args.lint:
        sys.exit(lint(args.main, args.readme))
    if args.run is None:
        p.error('a run file is required for everything but --lint')
    if not os.path.exists(args.run):
        sys.stderr.write('%s: no such run file; the analysis did not happen\n'
                         % args.run)
        sys.exit(2)
    cells, shapes, strategies, meta = load(args.run, args.main)
    shapes = [s for s in shapes if s not in args.exclude_shape]
    strategies = [s for s in strategies if s not in args.exclude]
    if args.no_controls:
        strategies = [s for s in strategies if not is_control(s)]
    if not shapes or not strategies:
        sys.exit('nothing left after --exclude')

    if args.selftest:
        sys.exit(selftest(cells, shapes, strategies, meta))
    roster = ('%d benchmarks over %d shape%s'
              % (meta['benches'], meta['shapes'],
                 '' if meta['shapes'] == 1 else 's'))
    if (len(strategies), len(shapes)) != (meta['benches'], meta['shapes']):
        roster += ('; reading %d of them over %d shape%s'
                   % (len(strategies), len(shapes),
                      '' if len(shapes) == 1 else 's'))
    print('%s: criterion %s, %d reports = %s%s%s'
          % (os.path.basename(args.run), meta['version'], meta['reports'],
             roster,
             '  (RAGGED: some cells missing)' if meta['ragged'] else '',
             '' if len(shapes) > 1 else '  (one shape: nothing to trim)'))
    print()
    health(cells, shapes, strategies)
    if args.shapes:
        shape_table(cells, shapes, strategies, meta)
    elif args.drops:
        drop_table(cells, shapes, strategies)
    elif args.aa:
        aa_table(cells, shapes, strategies)
    elif args.cells:
        cell_dump(cells, shapes, strategies)
    else:
        strategy_table(cells, shapes, strategies, meta, args)


if __name__ == '__main__':
    main()
