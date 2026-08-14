#!/usr/bin/env python3
"""Read one criterion --json run of this benchmark and print its tables.

Every per-strategy and per-shape figure quoted in README.md comes from here.
Extend this script rather than writing a new one: the definitions below took
a session to settle, and an ad-hoc reader gets them subtly wrong -- which
statistic the column winsorizes, that CI% is a half-width and not a
bound, that the
A/A and sum-only rows are controls, that `l` is not in the JSON at all.

Definitions, once:

  slope   the OLS per-call fit, `anRegress[time].regCoeffs.iters.estPoint`,
          preferred over `anMean` because millisecond-scale benches here ramp
          (README.md#r2-is-the-ramp-detector-not-the-noise-detector).
  CI%     (confIntLDX + confIntUDX) / 2 / slope * 100 -- the mean half-width
          as a percentage of the slope, "how many digits are real". Criterion
          reports the two deviations separately and they differ by up to 1.4x;
          the max is available as ci_hi.
  corr    the shared forcing pass every strategy is timed through, taken per
          shape as the mean of whatever `sum-only*` benches the run carries.
          Run 6 (-O1) is the run that licensed subtracting it, its two halves
          agreeing to 0.01% paired; README's sum-only section carries the
          decision and the caveat the halves do not settle.
  net     slope - corr: what the fill itself costs, and what every ratio
          this reader forms divides. A run with no `sum-only` bench has
          corr = 0 and net = slope, and says so on stderr rather than
          publishing an uncorrected column silently.
  time    winsorized geomean over EVERY shape of net / `list`'s net on the
          same shape: nothing dropped, outliers capped at 3 MADs. So all rows
          cover one population and two columns are comparable, and a wild
          cell is bounded rather than deleted. The CI%, noise, smp and alloc
          columns stay raw -- the correction shifts a point estimate, it does
          not make a cell better measured. `sum-only*` and `*-nosum` rows
          have no corrected time and read `--`.
  worst   the row's worst shape as a ratio to `list`, over every shape. A
          geomean answers "typical"; this answers "how bad does it get",
          which for a library fallback is the disqualifying question, no
          average can reach it, and no estimator choice can flatter it.
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
          allocated fit at R2 1.000 -- figures a rough pass found and Run 6
          (-O1) then reproduced to three digits at full budget, over a shape
          set of its own. The median over a PINNED shape set does
          reproduce, which is what keeps the column meaningful, so it is a
          statistic of a strategy and a shape set both (README.md's alloc
          bullet). `l` is not in the JSON, so it
          is computed from the shape lists in Main.hs; a shape the current
          Main.hs no longer defines reports alloc in bytes instead.

An A/A pair has two ratios and they now usually agree. With nothing dropped
both arms cover every shape, so the ratio of two published columns IS the
paired ratio whenever neither arm had a cell capped -- the geomeans divide
term by term. They part only where capping is asymmetric, a cell being capped
against its own row's median.
--aa prints both and --selftest asserts the identity for the uncapped pairs.
The floor is a consequence of the correction as much as the margins are:
subtracting a term common to both arms magnifies their disagreement too,
which on Run 12 took it from 0.23% to 0.35%. --aa therefore prints each
pair's RAW ratio and its `f` beside the net one: the net figure is the floor
between two published rows, the raw one is how much the arm disagrees with
itself, and quoting the first as the second overstates it by 1/(1-f) -- 2.6x
on Run 12's `scaled` cells, where the forcing pass is 61% of the bench.

Controls, not strategies: the `*-aa-*` rows (an existing strategy run twice
under a second name, true ratio exactly 1, so their spread is the noise
floor), `sum-only*` (the shared term every other row now has subtracted,
so its own net is zero and its time reads --), and `*-nosum` (a strategy run
again and forced with one element instead of the sum, so its BASE minus it is
that sum in situ -- what `sum-only` is a proxy for, and the one thing
`sum-only`'s own two halves cannot test about it, both of them re-reading a
fixed vector. --aa prints the comparison; neither a `-nosum` arm nor
`sum-only` has a corrected time to give, since subtracting the forcing pass
from a bench that never ran it would report a fill as cheaper than it is).
--no-controls drops them from
the aggregates but not from the correction, which is computed before it, so
the column means the same with the flag as without; they are always listed
by --aa, which is where they say what they are for. That a control
carries such a name is what --lint holds Main.hs's roster to, this test
being the only thing standing between a renamed control and its silently
entering the aggregates as a strategy.

One run, one population. Every aggregate here is over the shapes the file
holds, so it belongs to the main set or to one stride class and to nothing
in between: `population_of` names which, every mode says so in its first
line, --selftest fails a file spanning two, and --markdown declines to
publish a table for one. A major run is one process per population for
exactly this reason (README.md#making-a-major-benchmark-run), and the way
to get a mixed file is `classes` with no prefix.

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
  --shapes          per shape: CI% max / median / mean, and sample count
  --aa              the A/A and sum-only control pairs with their spans,
                    and the in-situ forcing term off the `-nosum` arms
  --pair A B        compare two arms shape by shape: paired geomean, a
                    bootstrap interval, win count and sign test
  --compare OTHER   compare one arm across two runs of the same population,
                    every arm at once -- what a paired run's two halves want
  --compare O --alloc   whether the two agree on what each arm allocates,
                    partitioned by size and never by column
  --compare O --chapter the run chapter's own arithmetic, so that writing
                    one need not begin by reading the last one
  --claims          every claim ordering and its registered verdict in one
                    call, in the claims section's order, from a manifest
                    --lint holds to the roster
  --steps           every cell read at sample level for a mid-bench change
                    of level, which the fitted slope averages away and no
                    other column here can show
  --cells           every cell as TSV, for anything not covered above
  --markdown        README's Results table, numbers recomputed and the
                    editorial column carried over from the one there --
                    six columns instead for a stride-class run, and none
                    at all for a run spanning two populations
  --fingerprint     the kept per-shape record (What Run N compares
                    against): dims, `list`'s net per call, and the
                    fingerprint arms' net ratios, as two README tables
  --block           a stride-class block's mechanical parts in the form's
                    order: table, controls, provenance/anchor skeleton,
                    a three-shape population's per-shape line, and the
                    three properties' verdicts derived rather than eyeballed
  --in-place        with --markdown, --fingerprint or --block, install the
                    tables into README instead of printing them: matched by
                    whole line, count asserted, a class table narrowed by
                    its block's lead, and refusing rather than guessing
  --exclude S       drop strategy S from every aggregate (repeatable)
  --exclude-shape H drop shape H likewise (repeatable)
  --selftest        check this reader's invariants against the run given
  --lint            check Main.hs's roster against README and against
                    itself -- no run file needed
  --brief           with --aa or --block, drop the standing explanation and
                    the table --in-place installs anyway; every computed
                    figure still prints
  --check-doc       anchors, the paths the document names, replace-list
                    coverage, widths, and a sweep of the superseded figures
                    still quoted, in README prose and Main.hs comments
                    alike -- no run needed
  --para PATTERN    print README paragraphs whose bolded lead matches, with
                    the line each starts at -- no run needed

A run artifact is made when a question needs it, and kept while questions
keep coming back to it. That is also when this script runs, so it is written
to be useful on a partial run -- a filtered handful of benches, or a single
shape:

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
which is what keeps it live. The correction added for Run 6 (-O1) was checked
the same way before its column was published: all 44 of that run's
uncorrected figures, and then all 44 corrected ones, were recomputed from
--cells by a throwaway script and agreed to the printed precision. Run 6
(-O1)'s JSON is not kept either -- that is
decided, not an oversight -- so do not restore a table-pinned EXPECTED
against it: the reader is guarded by invariants and by --lint, and by nothing
that would notice the published table drifting. Each invariant is
non-vacuous: breaking the dims regex, the winsorizing, the correction or the
A/A identity fails the matching check, and all four were broken to confirm
it.
It exits 2, not 0,
when the run file is missing: a refusal is information.
"""

import argparse
import collections
import contextlib
import difflib
import io
import json
import math
import os
import subprocess
import random
import re
import signal
import statistics as stats
import sys
import textwrap

TOL = 1e-9


def dims_by_shape(main_hs):
    """Map shape name -> dict(dims, l, m, s_inner), from Main.hs's lists.

    One (l, sInner) rule per list, mirroring the generator that builds
    that list's views. 'mkStrided' (and 'mkRev'/'mkRevSome'/'mkSliced',
    which keep its view shape) transposes the two innermost dims, so the
    view's innermost extent sInner is the second-to-last listed dim;
    'mkBroadcast' and 'mkScaled' keep the listed shape, so sInner is the
    last; 'mkBroadcastMid' inserts a stretch factor b, so l = b * product;
    'mkReshape1' appends a size-1 dim; 'mkWindow' lists image and kernel,
    the view being neither. In every case m = l / sInner is the run count
    -- the size of the base-offsets table every strategy here builds.

    These readings are this script's one unverifiable assumption -- no
    JSON carries the strided shape -- and `m` and every `alloc` multiple
    rest on them, so getting one wrong would scale a whole column for
    every strategy at once. `micro -- check` asserts the mkStrided reading
    per main-set shape against the view itself, and each entry's leading
    trailing-comment number annotates its true l, which --selftest holds
    the parse to for whatever population its run carries.

    Each entry also records the list it came from, as `lst`, which is what
    `population_of` reads: the lists are the populations.
    """
    def strided(ds, _):
        return math.prod(ds), (ds[-2] if len(ds) > 1 else 1)

    # the listed shape IS the view shape, so sInner is its last dim --
    # true of the broadcast and scaled lists both
    def listed(ds, _):
        return math.prod(ds), (ds[-1] if ds else 1)

    def bcastmid(ds, b):
        return b * math.prod(ds), (ds[-2] if len(ds) > 1 else 1)

    def reshape1(ds, _):
        return math.prod(ds), 1

    def window(ds, _):
        h, w, kh, kw = ds
        return (h - kh + 1) * (w - kw + 1) * kh * kw, kh

    sh_re = r'(?P<dims>\[[^\]]*\])'
    blocks = [
        ('convShapes', sh_re, strided),
        ('stretchShapes', sh_re, strided),
        ('revShapes', sh_re, strided),
        ('revSomeShapes', r'\[[^\]]*\],\s*' + sh_re, strided),
        ('broadcastShapes', sh_re, listed),
        ('broadcastMidShapes', r'(?P<b>\d+),\s*' + sh_re, bcastmid),
        ('reshape1Shapes', sh_re, reshape1),
        ('slicedShapes', sh_re, strided),
        ('windowShapes', sh_re, window),
        ('scaledViews', sh_re + r',\s*Strides\s*\[[^\]]*\]', listed),
    ]
    out, ann = {}, {}
    try:
        text = open(main_hs).read().split('\n')
    except OSError:
        return out, ann
    for start, mid, rule in blocks:
        entry = re.compile(r'^\s*(?:[\[,] )?\("([^"]+)",\s*' + mid
                           + r'\)(?:\s*--\s*(?P<ann>\d+))?')
        try:
            i = next(k for k, l in enumerate(text)
                     if l.startswith(start + ' ='))
        except StopIteration:
            continue
        for line in text[i + 1:]:
            m = entry.match(line)
            if m:
                ds = [int(d) for d in re.findall(r'\d+', m.group('dims'))]
                b = (int(m.group('b'))
                     if 'b' in m.groupdict() and m.group('b') else None)
                l, s_inner = rule(ds, b)
                out[m.group(1)] = dict(
                    dims=ds, l=l, s_inner=s_inner, lst=start,
                    m=(l // s_inner if s_inner else 0))
                if m.group('ann'):
                    ann[m.group(1)] = int(m.group('ann'))
            elif line.strip() == ']':
                break
    return out, ann


# The two lists that make up the main set. Every other list dims_by_shape
# reads is one stride-class population, timed one process per class
# (README.md#making-a-major-benchmark-run).
MAIN_LISTS = ('convShapes', 'stretchShapes')


def class_label(members):
    """A class population's name: the prefix its shapes share, which is
    also what selects it for a run (`classes rev-`)."""
    return 'the %s class' % '/'.join(sorted({sh.split('-')[0]
                                             for sh in members}))


def population_of(shapes, dims):
    """(kind, label): which population a run's shapes come from.

    `main` when they are all conv/stretch shapes, `class` when they all
    come from one stride-class list, `mixed` when they span more than one
    -- which `classes` without a prefix produces, and which README's
    one-JSON-at-a-time rule forbids, a geomean over two populations being
    a statistic of neither. `unknown` when Main.hs defines none of them,
    the case of a run whose shapes were renamed since. Shapes Main.hs does
    not define cast no vote; the rest still decide.
    """
    groups = {}
    for sh in shapes:
        d = dims.get(sh)
        if d:
            groups.setdefault('main' if d['lst'] in MAIN_LISTS else d['lst'],
                              []).append(sh)
    if not groups:
        return 'unknown', 'a population Main.hs does not define'
    named = sorted('the main set' if k == 'main' else class_label(v)
                   for k, v in groups.items())
    if len(groups) > 1:
        return 'mixed', ' + '.join(named)
    return ('main' if 'main' in groups else 'class'), named[0]


def load(path, main_hs):
    """(cells, shapes, strategies, meta); orders follow the run, not
    the file."""
    if not os.path.exists(path):
        sys.stderr.write('%s: no such run file; the analysis did not happen\n'
                         % path)
        sys.exit(2)
    raw = json.load(open(path))
    dims, ann = dims_by_shape(main_hs)
    ell = {s: d['l'] for s, d in dims.items()}
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
    # The roster's own size, which is what says whether this run is the
    # whole thing; `benches` counts only what the JSON holds, so on a
    # filtered run the two differ and several figures change meaning.
    try:
        rostered = len([n for n, r, _ in roster_of(open(main_hs).read())
                        if r != 'Only'])
    except OSError:
        rostered = 0
    meta = dict(version=raw[1], reports=len(raw[2]), path=path,
                rostered=rostered,
                benches=len(strategies), shapes=len(shapes), dims=dims,
                ann=ann,
                ragged=len(raw[2]) != len(shapes) * len(strategies),
                known_l=sum(1 for s in shapes if s in ell))
    return cells, shapes, strategies, meta


def apply_correction(cells, shapes, strategies):
    """Set each cell's `net` = slope - the shape's shared forcing term.

    Every strategy is timed as `VS.sum . fb`, so every slope carries one
    forcing pass; `sum-only*` times that pass alone, and subtracting it is
    what leaves the fill. The term is taken per shape, as the mean of
    whichever halves the run carries, because it is a property of the shape's
    vector and not of the strategy reading it.

    It is computed from the strategies present before --no-controls, so
    dropping the controls from the aggregates cannot silently change the
    published column; an explicit --exclude of a `sum-only` arm does change
    it, that being what asking for it means.

    A run carrying no such bench gets a zero term and an uncorrected column,
    which `health` reports rather than leaving to be inferred -- the case of
    the two-bench filtered runs this reader is meant to stay useful on.
    """
    terms = {}
    for sh in shapes:
        halves = [cells[sh][st]['slope'] for st in strategies
                  if st.startswith('sum-only') and st in cells[sh]]
        terms[sh] = stats.fmean(halves) if halves else 0.0
    for sh in shapes:
        for st in cells[sh]:
            cells[sh][st]['net'] = cells[sh][st]['slope'] - terms[sh]
    return terms


def health(cells, shapes, strategies, terms):
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

    The correction is reported here too, in both directions it can go wrong:
    absent, so the column is uncorrected, and larger than a cell it is
    subtracted from, which would make a net non-positive and a ratio
    meaningless.

    Non-vacuity, both halves: setting a strategy's allocated R2 to 0.5 warns,
    and lifting a `sum-only` cell's allocation past the exemption warns on the
    bad R2 it already had -- so the exemption is what silences those and not
    something else. The two correction warnings likewise: `--exclude
    sum-only-early --exclude sum-only-late` reports the uncorrected column and
    reproduces the raw figures, and inflating the term 50x reports 1353 sunk
    cells of 1452 -- neither of which a real run here has produced, which is
    why both were provoked.
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
    if not any(terms.values()):
        out.append('no `sum-only` bench in this run, so the time column is'
                   ' UNCORRECTED and not comparable to a full run\'s')
    else:
        # A `-nosum` arm is exempt with `sum-only`, and for the mirror-image
        # reason: it is the one kind of arm that never ran the forcing pass,
        # so on a fast fill its whole cost can legitimately fall below the
        # term, and subtracting one from the other was never meaningful.
        sunk = [(cells[sh][st]['net'], sh, st) for sh in shapes
                for st in strategies
                if not st.startswith('sum-only')
                and not st.endswith('-nosum')
                and cells[sh][st]['net'] <= 0]
        if sunk:
            n, sh, st = min(sunk)
            out.append('%d cell(s) whose forcing term is not smaller than the'
                       ' cell itself, worst %s/%s -- their ratios are not'
                       ' readable' % (len(sunk), sh, st))
    for line in out:
        sys.stderr.write('warning: ' + line + '\n')


def is_control(name):
    return ('-aa' in name or name.startswith('sum-only')
            or name.endswith('-nosum'))


def twin_of(name):
    """The row an A/A control duplicates: strip from '-aa' onward."""
    return name[:name.index('-aa')] if '-aa' in name else None


def base_of(name):
    """The row a `-nosum` control is subtracted from."""
    return name[:-len('-nosum')] if name.endswith('-nosum') else None


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




WINSOR_K = 3.0


def winsorize(logs, k=WINSOR_K):
    """Cap, do not drop: pull outliers to median +- k MADs and keep them.

    This is what replaced the trim, and it differs in what it is afraid of.
    Trimming deleted each strategy's worst-MEASURED cell, which on a time
    budget is usually its slowest, so a strategy catastrophic on one shape
    had that shape removed -- and since the cell removed differed by
    strategy, two columns ended up geomeans over different shape sets.
    Capping bounds a cell's influence without removing its evidence: the
    catastrophe still counts, at a weight it cannot dominate, and every row
    still covers every shape.

    MAD scaled by 1.4826 so k is in standard deviations for a normal; k = 3
    touches only what is genuinely far out. A zero MAD (half the cells
    identical) caps nothing rather than collapsing the row. Returns the
    capped logs and how many were capped, the count being what `--selftest`
    needs to know which identities it may still assert.
    """
    med = stats.median(logs)
    mad = stats.median([abs(x - med) for x in logs]) * 1.4826
    if mad <= 0:
        return logs, 0
    lo, hi = med - k * mad, med + k * mad
    out = [min(max(x, lo), hi) for x in logs]
    return out, sum(1 for a, b in zip(logs, out) if a != b)


def worst_of(cells, shapes, strategy):
    """The strategy's worst shape, as a ratio to `list`.

    A geomean answers "typical" and no robust version of it can answer "how
    bad does this get" -- the two questions want different statistics. For a
    library fallback the second is the disqualifying one: a strategy three
    times its own average on some shape is not shippable whatever its mean
    says. Being a maximum it is also the one figure no estimator choice can
    flatter.
    """
    if any('list' not in cells[s] for s in shapes):
        return float('nan')
    if strategy.startswith('sum-only') or strategy.endswith('-nosum'):
        return float('nan')
    return max(cells[s][strategy]['net'] / cells[s]['list']['net']
               for s in shapes)


def time_of(cells, shapes, strategy):
    """README's `time` column: winsorized geomean of net / `list`'s net.

    Over EVERY shape. Nothing is dropped, so all rows cover one population
    and two columns are comparable; a cell far enough out to distort the mean
    is capped instead, which bounds its influence without deleting its
    evidence; 'winsorize' records why that beats dropping a cell.

    A filtered run need not contain the baseline; then there is no ratio to
    give and the column reads nan rather than the reader stopping. So does a
    `sum-only` or `-nosum` arm, which never ran the forcing pass, and any
    cell the term did not leave positive -- `health` reports that one.
    """
    if strategy.startswith('sum-only') or strategy.endswith('-nosum'):
        return float('nan')
    if any('list' not in cells[s] for s in shapes):
        return float('nan')
    if any(cells[s][strategy]['net'] <= 0 or cells[s]['list']['net'] <= 0
           for s in shapes):
        return float('nan')
    logs = [math.log(cells[s][strategy]['net'] / cells[s]['list']['net'])
            for s in shapes]
    return math.exp(stats.fmean(winsorize(logs)[0]))


def strategy_rows(cells, shapes, strategies):
    """The table's rows, sorted: (time, name, CI%, noise, smp, alloc).

    The plain table and --markdown both render this and neither computes it,
    so the published markdown cannot drift from what the terminal shows --
    which is the same reason README says to extend this script rather than
    write a second reader, applied inside the script.
    """
    have_list = all('list' in cells[sh] for sh in shapes)
    typical = {sh: med_or_nan(cis(cells, sh, strategies)) for sh in shapes}
    rows = []
    for st in strategies:
        ci = [cells[s][st]['ci'] for s in shapes
              if cells[s][st]['ci'] is not None]
        alloc = [cells[s][st]['alloc'] for s in shapes
                 if cells[s][st]['alloc'] is not None]
        noise = med_or_nan([cells[sh][st]['ci'] / typical[sh]
                            for sh in shapes
                            if typical[sh] and typical[sh] == typical[sh]
                            and cells[sh][st]['ci'] is not None])
        rows.append((time_of(cells, shapes, st) if have_list else float('nan'),
                     st, med_or_nan(ci), noise,
                     stats.median(cells[s][st]['n'] for s in shapes),
                     stats.median(alloc) if alloc else None,
                     worst_of(cells, shapes, st) if have_list
                     else float('nan')))
    # A `sum-only` row has no time by construction rather than by mishap, so
    # it sorts to the head, where it reads as the term the column subtracts.
    rows.sort(key=lambda r: (-1.0 if r[0] != r[0] else r[0], r[1]))
    return rows, have_list


def strategy_table(cells, shapes, strategies, meta, args, terms):
    rows, have_list = strategy_rows(cells, shapes, strategies)
    print('%-28s %7s %6s %6s %6s %5s %8s'
          % ('strategy', 'time', 'worst', 'CI%', 'noise', 'smp', 'alloc'))
    for time, st, ci, noise, smp, alloc, worst in rows:
        mark = ' *' if is_control(st) else ''
        a = '%7.2fx' % alloc if alloc is not None else '      --'
        t = '     --' if time != time else '%7.3f' % time
        w = '     --' if worst != worst else '%6.3f' % worst
        print('%-28s %s %s %6.2f %6.2f %5.0f %s%s'
              % (st, t, w, ci, noise, smp, a, mark))
    if not have_list:
        print('\ntime is --: this run has no `list` bench to divide by')
    print('\n* control, not a strategy (--aa explains; --no-controls omits)')
    if any(terms.values()) and have_list:
        share = {st: med_or_nan([terms[sh] / cells[sh][st]['slope']
                                 for sh in shapes if st in cells[sh]])
                 for st in ('list', 'bq-expand')}
        known = ' and '.join('%.1f%% of %s' % (100 * v, k)
                             for k, v in share.items() if v == v)
        print('time has the shared forcing pass subtracted from every row;')
        if known:
            print('that term is a median ' + known + ' over shapes.')
        print('The `sum-only` rows are that term, so they read -- rather than')
        print('a figure of a different kind in the same column.')
    print('worst is the row\'s worst shape: how bad it gets, which no average')
    print('answers. time is a winsorized geomean over every shape -- nothing')
    print('dropped, outliers capped at %.0f MADs -- so all rows compare.'
          % WINSOR_K)
    print('noise is this row\'s CI% against the median CI% of the same shape,')
    print('medianed over shapes: 1.00 is an ordinary bench, and the')
    print('outlier is the bench to suspect of disturbing whatever shares')
    print('its process.')
    if meta['known_l'] < len(shapes):
        print('alloc missing for %d shape(s) Main.hs no longer defines'
              % (len(shapes) - meta['known_l']))


def readme_rows(readme, strategies, recognise=None):
    """README's Results table, keyed by strategy: (label, style, needs).

    Only the rightmost column and the emphasis are read. Those are editorial
    -- which tier a strategy needs, which rows the prose calls out -- and no
    run can produce them, so --markdown carries them forward instead of asking
    for them again. Everything numeric is recomputed.

    A `precondition` column sat beside `needs` until the precondition ruling
    (README.md#what-the-benchmark-does) stopped timing every strategy that had
    one, leaving every surviving row's cell empty; what it recorded is now at
    those strategies' roster entries in Main.hs.

    Rows are matched by stripping emphasis and the `(baseline)` suffix, and
    only names in `recognise` are taken, so the other markdown tables on the
    page cannot be mistaken for this one however their column count lands --
    which the name filter now does alone, the cross-class summary being seven
    columns wide too since the eighth went.

    `recognise` defaults to the run's own arms, which is what a caller
    carrying figures forward wants. --markdown widens it to the whole roster,
    because a row this run does NOT carry is exactly what its departed-row
    warning is about, and reading only the carried ones made that warning
    unreachable: `gone` was computed as the keys of this dict not in
    `strategies`, and every key was in `strategies` by construction. It had
    never fired. Widening keeps the set closed -- a name has to be rostered --
    so the cross-class summary, whose first cell is a class name, still cannot
    match.

    What the closed set costs, since it is the price of that disambiguation: a
    row whose NAME has left the roster is neither carried nor rostered, so it
    is neither fresh nor gone and its disappearance is reported by nothing.
    The `bq-scan-mulback-aa-*` pair is in that state today, re-pointed and
    renamed after Run 8 published it.

    Non-vacuity, confirmed rather than argued: against the 49-row Run 8 table
    and a one-shape run of today's 34-arm roster, --markdown reports 23 gone,
    naming every arm the two rulings stopped timing and no other, alongside
    the 10 fresh it already reported. Before this change the same call
    reported none.
    """
    out = {}
    try:
        text = open(readme).read().split('\n')
    except OSError:
        return out
    for line in text:
        if not line.lstrip().startswith('|'):
            continue
        cell = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cell) != 7:
            continue
        bare = re.sub(r'[*`]', '', cell[0]).replace('(baseline)', '').strip()
        if bare not in (strategies if recognise is None else recognise):
            continue
        style = ('bold' if cell[0].startswith('**')
                 else 'italic' if cell[0].startswith('*') else 'plain')
        out[bare] = (cell[0], style, cell[-1])
    return out


def capture(fn, *a):
    """What an emitter prints, so it can be installed instead of pasted."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a)
    return buf.getvalue()


def tables_in(text):
    """The pipe-tables in an emitter's output, each as a list of lines."""
    out, cur = [], []
    for line in text.split('\n'):
        if line.startswith('|'):
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def install(readme, table, src, after=None):
    """Replace README's copy of `table` with it, or refuse.

    `src` is the run file the rows came from, and it is named on the way
    out because nothing here can check it: the published table is the
    basis half's by convention alone, and a table installed from the other
    half satisfies every gate this script has, the header being the same
    line either way. Run 10 installed one and the page carried it. So the
    half is printed at the moment it is installed, where the transcript
    and the terminal both keep it, rather than left to the provenance
    section written hours later.

    Pasting by hand is what this exists to stop: the cross-class summary's
    header is written out twice, once indented as the spec that fixes the
    columns and once as the table's own, and a session that located the
    table by searching for that text hit the spec first -- putting a run's
    rows under the wrong paragraph and leaving the previous run's table
    standing, with every mechanical check still green because the check
    looked the table up the same wrong way.

    So the match is by whole line, which an indented copy cannot satisfy,
    and the count is asserted rather than assumed: a header occurring more
    than once must be narrowed by `after`, the first line of the block the
    right table belongs to. Refusal is the failure mode, never a silent
    write to the wrong place.

    Born checked, four ways deliberately (2026-08-08). Pointed at a header
    no line equals, it exits 1 saying so. Pointed at the six-column class
    header with no `after`, it exits 1 naming eight matches rather than
    taking the first. Given an `after` no line starts with, it exits 1
    rather than falling back. And installed over a table it already agrees
    with -- the main Results table, both fingerprint tables and a class
    block's -- it leaves README byte-identical, which is the check that the
    right table was found and not merely a table. That last one was run
    again on 2026-08-14, when `src` was added: the install prints the run
    file the rows came from and README is byte-identical after it.
    """
    with open(readme) as f:
        lines = f.read().split('\n')
    hdr = table[0]
    hits = [i for i, line in enumerate(lines) if line == hdr]
    if after is not None:
        start = [i for i, line in enumerate(lines) if line.startswith(after)]
        if len(start) != 1:
            sys.exit('--in-place: %d line(s) start with %r, need exactly one'
                     % (len(start), after))
        hits = [i for i in hits if i > start[0]][:1]
    if len(hits) != 1:
        sys.exit('--in-place: %d line(s) equal the header, need exactly one;'
                 ' refusing to guess\n  %s' % (len(hits), hdr[:68]))
    i = hits[0]
    j = i
    while j < len(lines) and lines[j].startswith('|'):
        j += 1
    was = j - i
    lines[i:j] = table
    with open(readme, 'w') as f:
        f.write('\n'.join(lines))
    sys.stderr.write('installed at %s:%d from %s, %d row(s) replacing %d\n'
                     % (os.path.basename(readme), i + 1,
                        os.path.basename(src), len(table), was))


def emit_or_install(text, args, shapes, meta, block=False):
    """Print an emitter's output, or install its tables into README.

    A class table's header is one of eight identical lines, so it is
    narrowed by the bolded lead of its own block -- which is also the thing
    a reader would use, and which fails loudly if the class has no block
    yet. A block's prose is not installed: the controls sentence and the
    paragraph are the author's, and only the table it carries is mechanical.
    """
    if not args.in_place:
        sys.stdout.write(text)
        return
    kind, label = population_of(shapes, meta['dims'])
    after = None
    if kind == 'class':
        after = '**`%s`' % label.replace('the ', '').replace(' class', '')
    tables = tables_in(text)
    if not tables:
        sys.exit('--in-place: this mode emitted no table')
    install(args.readme, tables[0], args.run, after)
    for extra in tables[1:]:
        install(args.readme, extra, args.run, after)
    if block:
        sys.stderr.write('the block\'s prose is yours: controls, provenance'
                         ' and the paragraph are not installed\n')
        for line in text.split('\n'):
            if not line.startswith('|'):
                sys.stdout.write(line + '\n')


def markdown_table(cells, shapes, strategies, meta, args, terms):
    """Emit README's Results table, ready to paste over the one there.

    The numbers come from `strategy_rows`, the same call the terminal table
    renders, so the two cannot disagree; what a run cannot know is carried
    over from the table already in README. Anything it could not carry is
    named on stderr rather than silently emitted blank -- a new strategy needs
    its `needs` written by hand, and a strategy that has left the roster needs
    deleting from the prose around the table, which no generator can do.

    A stride-class run gets the same table SIX columns wide instead: `needs`
    is a property of a strategy, not of a population, so it is stated once in
    the main table and a class table points at it. That also keeps the
    carry-forward anchored -- `readme_rows` matches a table by its width and
    its strategy names, and a class table repeating that column would match it
    too, leaving every population's table competing to be the one a later run
    copies from. A mixed run gets no table at all.
    """
    rows, have_list = strategy_rows(cells, shapes, strategies)
    kind, label = population_of(shapes, meta['dims'])
    if kind == 'mixed':
        sys.stderr.write('refusing to emit a table for %s: one JSON at a'
                         ' time, never merged, so that a geomean is some'
                         ' population\'s -- see\n'
                         '  README.md#making-a-major-benchmark-run\n' % label)
        sys.exit(1)
    # A class table drops the editorial column but keeps the emphasis:
    # which row shipped and which leads is what a reader looks for first,
    # and it is the same row in every population's table.
    editorial = kind != 'class'
    # Read the table by the ROSTER, not by this run's arms, so that a row the
    # run has dropped is still seen and can be reported. See `readme_rows`.
    try:
        rostered = {n for n, _, _ in roster_of(open(args.main).read())}
    except OSError:
        rostered = set(strategies)
    prev = readme_rows(args.readme, set(strategies),
                       rostered or set(strategies))
    fresh, gone = [], [n for n in prev if n not in strategies]
    print('| strategy | time | worst | CI% | smp | alloc'
          + (' | needs |' if editorial else ' |'))
    print('|---|---:|---:|---:|---:|---:' + ('|---|' if editorial else '|'))
    for time, st, ci, noise, smp, alloc, worst in rows:
        if st in prev:
            label_, style, needs = prev[st]
        else:
            if editorial:
                fresh.append(st)
            label_ = st
            style = 'italic' if is_control(st) else 'plain'
            needs = '?'
        num = ['--' if time != time else '%.3f' % time,
               '--' if worst != worst else '%.3f' % worst, '%.2f' % ci,
               '%.0f' % smp, '--' if alloc is None else '%.2fx' % alloc]
        if style == 'italic':
            label_ = label_ if label_.startswith('*') else '*%s*' % label_
            num = ['*%s*' % v for v in num]
        elif style == 'bold':
            label_ = label_ if label_.startswith('**') else '**%s**' % label_
            num[0] = '**%s**' % num[0]
        tail = needs + ' |' if editorial else ''
        print('| %s | %s |%s' % (label_, ' | '.join(num),
                                 ' ' + tail if tail else ''))
    if not editorial:
        sys.stderr.write('ok: six columns, for %s: needs is the main'
                         " table's, being a property of a strategy and not"
                         ' of a population\n' % label)
    if not have_list:
        sys.stderr.write('warning: no `list` bench, so every time reads --\n')
    if fresh:
        sys.stderr.write('warning: %d row(s) new since the table in %s, with'
                         ' needs left as `?` for you to write:'
                         ' %s\n' % (len(fresh), os.path.basename(args.readme),
                                    ', '.join(fresh)))
    if gone and editorial:
        sys.stderr.write('warning: %d row(s) in that table are absent from'
                         ' this run and have been dropped; check the prose'
                         ' still holds: %s\n' % (len(gone), ', '.join(gone)))
    if editorial and not fresh and not gone:
        sys.stderr.write('ok: needs carried forward for all %d rows, none'
                         ' added, none dropped\n' % len(rows))


def shape_table(cells, shapes, strategies, meta):
    print('%-22s %9s %8s %7s %7s %7s %5s  %s'
          % ('shape', 'l', 'm', 'CImax', 'CImed', 'CImean', 'smp',
             'worst cell'))
    rows = []
    for sh in shapes:
        ci = {st: cells[sh][st]['ci'] for st in strategies
              if cells[sh][st]['ci'] is not None}
        if not ci:
            continue
        mx = max(ci, key=ci.get)
        d = meta['dims'].get(sh)
        l, m = (d['l'], d['m']) if d else (0, 0)
        rows.append((ci[mx], sh, l, m,
                     stats.median(ci.values()), stats.fmean(ci.values()),
                     stats.median(cells[sh][st]['n'] for st in strategies),
                     mx))
    for mx, sh, l, m, med, mean, smp, who in sorted(rows, reverse=True):
        print('%-22s %9s %8s %7.2f %7.3f %7.3f %5.0f  %s'
              % (sh, l or '?', m or '?', mx, med, mean, smp, who))
    print('\nl and m come from Main.hs (m = run count = base-offsets table')
    print('size; sInner = l / m); ? means Main.hs no longer defines it.')
    print('The worst-cell column names the strategy whose CI% is widest')
    print('here; nothing is dropped, so it is also what the winsorizing')
    print('geomean is most likely to have capped.')




# Fixed so that re-running the reader on one JSON gives one answer; a
# published interval that moved between readings would be worse than none.
BOOT_SEED, BOOT_REPS = 20260804, 10000


def paired_ci(ratios, lo=2.5, hi=97.5):
    """Percentile bootstrap of the geomean of per-shape ratios.

    Resamples SHAPES, not samples within a bench -- criterion already
    bootstraps the latter, and what is unknown here is how much of a pair's
    disagreement is the shape set it was measured over. Paired by shape on
    purpose: `list` cancels out of A_s/B_s, so the interval owes nothing to
    the baseline, and shape-to-shape spread, which is six-fold across this
    set, cancels with it.
    """
    if len(ratios) < 2:
        return None
    rng = random.Random(BOOT_SEED)
    logs = [math.log(r) for r in ratios]
    n = len(logs)
    out = sorted(math.exp(sum(rng.choices(logs, k=n)) / n)
                 for _ in range(BOOT_REPS))
    return out[int(BOOT_REPS * lo / 100)], out[int(BOOT_REPS * hi / 100)]


def sign_p(k, n):
    """Two-sided sign test: how lopsided k wins of n is under a fair coin.

    The assumption-free backstop to the geomean. It never forms a mean, so a
    cell measured to +-70% casts one vote like every other shape and cannot
    distort it. What it gives up is magnitude: it says A beats B, never by
    how much.
    """
    k = max(k, n - k)
    tail = sum(math.comb(n, i) for i in range(k, n + 1))
    return min(1.0, 2.0 * tail / 2 ** n)


def pair_stats(cells, shapes, a, b):
    """One pair's per-shape ratios, and whether they had to be taken raw.

    The one computation `--pair` and `--claims` share, held in one place so
    the verdict a claim prints cannot disagree with the figures beside it.
    Netting an arm that never ran the forcing pass is meaningless, so a
    pair with a `sum-only` or `-nosum` half is compared raw and says so.
    """
    raw = any(x.startswith('sum-only') or x.endswith('-nosum')
              for x in (a, b))
    key = 'slope' if raw else 'net'
    return raw, [cells[s][a][key] / cells[s][b][key] for s in shapes]


def pair_table(cells, shapes, strategies, pairs, quiet=False):
    """Compare two arms shape by shape, which is the sharp way to compare them.

    A strategy's ratio to `list` spans six-fold across this shape set, so an
    unpaired comparison of two columns fights that spread; the ratio A_s/B_s
    does not, both arms moving together with the shape. `list` cancels out of
    it too, so nothing here depends on the baseline -- the one figure the
    absolute anchor exists to police.

    This exists because the alternative was a throwaway script per session:
    the paired geomeans and win counts quoted in README (0.926 against
    `bq-expand`, "faster on 32 of 33") were each recomputed by hand and
    deleted, which is how one of them came to be quoted beside a figure from
    a different run. The published ratio is printed beside the paired one
    because they answer different questions -- this script's docstring says
    which -- and the interval wants multiplying by the factor `--aa`
    calibrates before it is believed.
    """
    print('%-46s %8s %19s %8s %9s'
          % ('A / B', 'paired', '95% CI', 'A wins', 'sign p'))
    for a, b in pairs:
        missing = [x for x in (a, b) if x not in strategies]
        if missing:
            print('%-46s not in this run: %s' % (a + ' / ' + b,
                                                 ', '.join(missing)))
            continue
        raw, r = pair_stats(cells, shapes, a, b)
        g, n = geomean(r), len(r)
        k = sum(1 for x in r if x < 1)
        ci = paired_ci(r)
        pub = (time_of(cells, shapes, a) / time_of(cells, shapes, b)
               if not raw else float('nan'))
        print('%-46s %8.4f %19s %8s %9.2g'
              % (a + ' / ' + b, g,
                 '--' if not ci else '%.4f..%.4f' % ci,
                 '%d/%d' % (k, n), sign_p(k, n)))
        lo, hi = min(zip(r, shapes)), max(zip(r, shapes))
        print('%46s range %.3f (%s) .. %.3f (%s)'
              % ('', lo[0], lo[1], hi[0], hi[1]))
        print('%46s published-column ratio %s%s'
              % ('', '--' if pub != pub else '%.4f' % pub,
                 '; compared RAW, one arm has no corrected time' if raw
                 else ''))
    # `--claims` prints a dozen of these in one call and the standing
    # explanation once would be twelve times; it is the same reasoning
    # `--brief` applies to `--aa` and `--block`, and drops no figure.
    if quiet:
        return
    print('\npaired is the geomean of the per-shape ratio, which is what a')
    print('margin measured per shape should be compared against; the')
    print('published-column ratio is what a reader of the table computes,')
    print('capping asymmetry aside. `A wins` counts shapes where A < B, and')
    print('sign p is that count under a fair coin -- no distributional')
    print('assumption, immune to a wild cell, and blind to magnitude.')


def controls_skeleton(cells, shapes, strategies, terms):
    """The Controls paragraph's facts, in the form's own order.

    `--block` already hands over the provenance line as a fill-in-the-blank
    rather than making a session read it off a log. The controls sentence
    wanted the same and did not have it, so every write-up re-extracted the
    same four things from `--aa`'s table by eye or by a script of its own:
    which A/A pair is largest and where its worst cell falls, how many of
    the intervals cover 1, what the `sum-only` halves agree to, and the
    in-situ medians. Eight class blocks a run, so eight extractions, and
    the one that matters -- which pair is largest -- is a sort a reader
    does wrong by looking at the first row.

    The reading stays the author's, as it does for the provenance line: this
    prints the figures and no verdict. `--aa` above it is unchanged and
    remains where the intervals, spans and raw/`f` readings are read.

    Born checked against the eight blocks Run 13 wrote by hand, which were
    extracted from `--aa` by a script before this existed: every figure it
    emits is in the paragraph that run installed, on all eight classes. Two
    of them appear there as a deviation (`2.74%`) where this prints a ratio
    (`1.0274`), which is the same figure and is why the check allows both
    forms. The check itself needed a guard before it was worth anything: its
    first form found no paragraphs at all -- the blocks put two blank lines
    before `Controls:`, so splitting on one left a leading newline -- and
    reported eight of eight passing over an empty loop.
    """
    pos = {st: i for i, st in enumerate(strategies)}
    aa, so = [], None
    for a in strategies:
        b = twin_of(a)
        if not b or b not in pos:
            continue
        r = [cells[s][a]['net'] / cells[s][b]['net'] for s in shapes]
        dev = [abs(x - 1) * 100 for x in r]
        ci = paired_ci(r)
        aa.append((geomean(r), a, max(zip(dev, shapes)),
                   None if not ci else (ci[0] <= 1.0 <= ci[1])))
    if 'sum-only-early' in pos and 'sum-only-late' in pos:
        r = [cells[s]['sum-only-late']['slope']
             / cells[s]['sum-only-early']['slope'] for s in shapes]
        dev = [abs(x - 1) * 100 for x in r]
        ci = paired_ci(r)
        so = (geomean(r), max(zip(dev, shapes)),
              None if not ci else (ci[0] <= 1.0 <= ci[1]))
    if not aa:
        return
    big = max(aa, key=lambda t: abs(t[0] - 1))
    cover = sum(1 for g, _, _, c in aa if c)
    print()
    print('Controls: ___ (the reading is yours). The largest A/A pair is')
    print('`%s` at %.4f, worst cell %.2f%% on `%s`,'
          % (big[1], big[0], big[2][0], big[2][1]))
    print('and %d of %d intervals cover 1.' % (cover, len(aa)), end=' ')
    if so:
        print('The `sum-only` halves agree at %.4f' % so[0])
        print('on a worst cell of %.2f%% on `%s`, its interval %s 1.'
              % (so[1][0], so[1][1], 'covering' if so[2] else 'missing'))
    else:
        print()
    ins = [(base_of(b), b) for b in strategies if base_of(b) in strategies]
    meds = []
    for base, arm in ins:
        r = []
        for s in shapes:
            gap = cells[s][base]['slope'] - cells[s][arm]['slope']
            term = cells[s][base]['slope'] - cells[s][base]['net']
            if gap > 0 and term > 0:
                r.append(gap / term)
        if r:
            meds.append((base, stats.median(r)))
    if meds:
        print('The in-situ term reads %s of `sum-only` as medians,'
              % ', '.join('%.4f' % m for _, m in meds))
        print('on %s.' % ', '.join('`%s`' % b for b, _ in meds))
    # The largest pair RAW, and what the correction multiplies it by. The
    # net figure is the floor between two published rows and the raw one is
    # how much an arm disagrees with itself; quoting the first as the second
    # overstates it by 1/(1-f), which over Runs 10 to 13 is 1.30x in
    # `reshape1` and 1.81x in `scaled` -- so a class block that published
    # the net alone made the same wobble look half again worse in one class
    # than in another (README.md#what-is-open). `--aa` has printed both all
    # along; the block did not, and eight blocks a run are where the figure
    # is actually read.
    b = twin_of(big[1])
    raw = geomean([cells[s][big[1]]['slope'] / cells[s][b]['slope']
                   for s in shapes])
    fs = []
    for s in shapes:
        term = cells[s][big[1]]['slope'] - cells[s][big[1]]['net']
        mean = (cells[s][big[1]]['slope'] + cells[s][b]['slope']) / 2
        if mean > 0:
            fs.append(term / mean)
    if fs and stats.fmean(fs) < 1:
        amp = 1 / (1 - stats.fmean(fs))
        print('Raw, that pair reads %.4f, which the correction amplifies'
              % raw)
        print('by %.2fx -- quote both wherever that is past 1.5.' % amp)


def chapter_skeleton(cells, shapes, strategies, meta, other, main_hs):
    """The run chapter's mechanical parts, as `--block` does for a class.

    A chapter's paragraphs are the same paragraphs every run -- the pair's
    identity, the regime confirmation, the headline arm-by-arm reading, the
    floor, the wild-cell draw, the allocation check -- differing in figures
    and in which findings are live. A session that has to READ the previous
    run's chapter to learn what to assert pays for the whole of it before
    writing a word, which is the largest single cost of a write-up. This
    hands over the figures so the reading is optional.

    What it does NOT emit is anything outside the two JSONs: the elapsed
    times, the heap peaks, the wall-clock window, the md5s and the commit
    come from the logs and the pair note, and are left as blanks in the
    same spirit as `--block`'s provenance line -- copied, not guessed. The
    prose stays the author's throughout; this writes no sentence.

    Born checked against Run 13's own chapter: every figure it emits is one
    that chapter published, the floors, the worst cells, the arm counts,
    the geomean over the arms and the spread ranking alike.
    """
    b_cells, b_shapes, b_strategies, b_meta = load(other, main_hs)
    apply_correction(b_cells, b_shapes, b_strategies)
    both_sh = [s for s in shapes if s in b_shapes]
    both_st = [t for t in strategies if t in b_strategies]
    print('\nchapter skeleton, this run against %s'
          % os.path.basename(other))
    print('  regime, md5s, commit, elapsed, heap peaks, wall-clock window:'
          ' ___ (from the')
    print('  pair note and the logs -- this mode reads neither)')
    rows = []
    for st in both_st:
        if st.startswith('sum-only') or st.endswith('-nosum'):
            continue
        r = [cells[sh][st]['net'] / b_cells[sh][st]['net'] for sh in both_sh
             if cells[sh][st]['net'] > 0 and b_cells[sh][st]['net'] > 0]
        if len(r) < 2:
            continue
        lg = [math.log(x) for x in r]
        rows.append((geomean(r), stats.pstdev(lg), st))
    if not rows:
        return
    out = [t for t in rows if abs(t[0] - 1) > 0.01]
    print('\n  arm by arm, over %d arm(s): %d within 1%% of 1, %d outside'
          % (len(rows), len(rows) - len(out), len(out)))
    for g, _, st in sorted(out, key=lambda t: -abs(t[0] - 1)):
        print('    %-30s %.4f  (%+.2f%%)' % (st, g, (g - 1) * 100))
    print('    below 1: %d   above 1: %d   geomean over the arms: %.4f'
          % (sum(1 for g, _, _ in rows if g < 1),
             sum(1 for g, _, _ in rows if g > 1),
             geomean([g for g, _, _ in rows])))
    sp = sorted(rows, key=lambda t: -t[1])
    print('\n  widest per-shape spread (log sd), which ranks how loosely an')
    print('  arm measures rather than what it computes:')
    for i, (g, sd, st) in enumerate(sp[:6], 1):
        print('    %d. %-28s %.4f%s' % (i, st, sd,
              '   <- moved past 1%' if abs(g - 1) > 0.01 else ''))
    for tag, cs, shs, sts in (('basis', cells, shapes, strategies),
                              ('other', b_cells, b_shapes, b_strategies)):
        aa = []
        for a in sts:
            b = twin_of(a)
            if not b or b not in sts:
                continue
            r = [cs[x][a]['net'] / cs[x][b]['net'] for x in shs]
            dev = [abs(v - 1) * 100 for v in r]
            aa.append((geomean(r), a, max(zip(dev, shs))))
        if not aa:
            continue
        big = max(aa, key=lambda t: abs(t[0] - 1))
        worst = max(aa, key=lambda t: t[2][0])
        print('\n  %s half: floor %.2f%% (%s), worst A/A cell %.2f%% on %s'
              % (tag, abs(big[0] - 1) * 100, big[1],
                 worst[2][0], worst[2][1]))
    print('\n  allocation between the halves: run --compare --alloc; the'
          ' figure belongs')
    print('  in the chapter and the trap it carries is documented there.')
    print('\nThe reading, the findings and every sentence are yours. This is'
          '\nthe arithmetic a chapter opens with, so that writing one need'
          '\nnot begin by reading the last.')


def compare_alloc(cells, shapes, strategies, meta, other, main_hs):
    """Whether two halves of a pair agree on what each arm allocates.

    Allocation is deterministic per call, so a pair whose halves differ only
    in placement must agree on every cell, and a level that DOES move is a
    code change rather than a slot. That makes this the claim to check first
    when anything else moves -- which is why it wants a mode of its own
    rather than a script per run. Two things a script per run got wrong here
    on 2026-08-14, both of which this mode exists to make unrepeatable.

    The `alloc` column and the raw fitted bytes are ONE quantity, not two:
    the multiple is the bytes divided by a constant per shape, so between two
    runs their relative differences are identical and no choice between the
    columns is available. A write-up chose between them anyway -- read the
    bytes, found the `sum-only` controls disagreeing, then "corrected" itself
    by recomputing on the multiple as `--cells` PRINTS it, at four decimals,
    where the rounding hides the disagreement and every cell agrees. That is
    arithmetic on rounding, which this page forbids everywhere else.

    So the partition here is by SIZE and never by column. An arm allocating a
    few tens of bytes a call has a fit that resolves nothing, and its cells
    disagree between any two processes; every arm that allocates in earnest
    agrees exactly. The same write-up explained its 34 cells by an RTS-line
    difference between the halves, a mechanism the previous pair refutes --
    it shared an RTS line and disagreed on 37. Both partitions print, so
    neither half of that has to be rediscovered.

    Non-vacuous 2026-08-14, both branches exercised live rather than planted:
    on Run 13's pair the small-allocator line reports 34 cells disagreeing
    and names the largest of them, while the earnest-allocator line reports
    792 of 792 -- so the agreeing and disagreeing paths both run on one
    invocation, on the pair the mode was written for.
    """
    FLOOR = 100.0                # bytes a call, below which the fit is noise
    b_cells, b_shapes, b_strategies, b_meta = load(other, main_hs)
    mine = population_of(shapes, meta['dims'])[1]
    theirs = population_of(b_shapes, b_meta['dims'])[1]
    if mine != theirs:
        sys.exit('this run is %s and %s is %s: different populations, and no'
                 ' figure crosses between them'
                 % (mine, os.path.basename(other), theirs))
    both_sh = [s for s in shapes if s in b_shapes]
    both_st = [t for t in strategies if t in b_strategies]
    print('\nallocation, this run against %s, over %d shared cell(s)'
          % (os.path.basename(other), len(both_sh) * len(both_st)))
    missing = sorted(set(strategies) ^ set(b_strategies))
    if missing:
        print('  arms in one run only, skipped: %s' % ', '.join(missing))

    big, small = [], []
    for sh in both_sh:
        for st in both_st:
            a, b = cells[sh][st]['alloc_bytes'], b_cells[sh][st]['alloc_bytes']
            if a is None or b is None:
                continue
            d = 0.0 if a == b else abs(a - b) / max(abs(a), abs(b))
            top = max(a, b)
            (big if top >= FLOOR else small).append((d, sh, st, top))

    def line(label, rows):
        if not rows:
            print('  %-22s none' % label)
            return
        ok = sum(1 for d, _, _, _ in rows if d <= 1e-4)
        worst = max(rows)
        print('  %-22s %d of %d agree to 1e-4; worst %.2e on %s/%s'
              % (label, ok, len(rows), worst[0], worst[1], worst[2]))
    line('arms that allocate:', big)
    line('under %d bytes/call:' % FLOOR, small)
    if small and any(d > 1e-4 for d, _, _, _ in small):
        n = sum(1 for d, _, _, _ in small if d > 1e-4)
        print('    those %d allocate at most %.0f byte(s) a call, so the fit'
              ' resolves nothing' % (n, max(r[3] for r in small)))
        print('    there; it is a property of fitting a near-zero'
              ' allocation and not of this pair')
    print('\nThe multiple the alloc column publishes is these bytes divided'
          '\nby a constant per shape, so it agrees exactly where these do and'
          '\nthere is no second column to prefer. Allocation is deterministic'
          '\nper call: a level that moves is a code change, never a slot.')


def compare_table(cells, shapes, strategies, meta, other, main_hs):
    """One arm's figure in this run against the same arm in another.

    `--pair` compares two arms inside one run; this compares one arm across
    two runs of the same population, which is what a paired run asks for --
    Run 10's aligned half against its unaligned one, arm by arm, is its
    fourth prediction. Both sides are corrected before dividing, since the
    forcing term is not identical between two builds (README's open list
    measures it moving 0.6% across an alignment change), so subtracting each
    run's own is the only reading that means anything.

    Shapes and arms present in both are what it reports; anything else is
    named and skipped, a silently narrowed comparison being the failure this
    whole file is written against.
    """
    b_cells, b_shapes, b_strategies, b_meta = load(other, main_hs)
    apply_correction(b_cells, b_shapes, b_strategies)
    mine = population_of(shapes, meta['dims'])[1]
    theirs = population_of(b_shapes, b_meta['dims'])[1]
    if mine != theirs:
        sys.exit('this run is %s and %s is %s: different populations, and no'
                 ' figure crosses between them'
                 % (mine, os.path.basename(other), theirs))

    both_sh = [s for s in shapes if s in b_shapes]
    both_st = [t for t in strategies if t in b_strategies]
    missing = ([s for s in shapes if s not in b_shapes]
               + [s for s in b_shapes if s not in shapes])
    print('\nthis run / %s, per arm, over %d shared shape(s)'
          % (os.path.basename(other), len(both_sh)))
    if missing:
        print('  shapes in one run only, skipped: %s'
              % ', '.join(sorted(set(missing))))
    if len(both_st) != len(strategies) or len(both_st) != len(b_strategies):
        print('  arms in one run only, skipped: %s'
              % ', '.join(sorted(set(strategies) ^ set(b_strategies))))

    rows = []
    for st in both_st:
        # The arms with no corrected time: their net is the forcing term
        # subtracted from itself, so a ratio of two of them is a ratio of two
        # near-zeros. `--aa` is where those two are compared.
        if st.startswith('sum-only') or st.endswith('-nosum'):
            continue
        rs = []
        for sh in both_sh:
            a, b = cells[sh][st]['net'], b_cells[sh][st]['net']
            if a > 0 and b > 0:
                rs.append(a / b)
        if rs:
            rows.append((geomean(rs), sum(1 for r in rs if r < 1),
                         len(rs), st))
    print('\n%-34s %8s %8s %10s' % ('arm', 'ratio', 'faster', 'range'))
    for g, wins, n, st in sorted(rows):
        rs = sorted(cells[sh][st]['net'] / b_cells[sh][st]['net']
                    for sh in both_sh
                    if cells[sh][st]['net'] > 0 and b_cells[sh][st]['net'] > 0)
        print('%-34s %8.4f %5d/%-3d %5.3f..%.3f'
              % (st, g, wins, n, rs[0], rs[-1]))
    print('\nsum-only and -nosum arms are left out, having no corrected time'
          '\nto divide; --aa is where those are read.'
          '\nBelow 1 means this run is faster. The ratio is the geomean of the'
          '\nper-shape ratio, both sides corrected by their own forcing term;'
          '\n`faster` counts shapes where this run wins. A run-to-run figure'
          '\ncarries whatever the two builds differ in, which for anything but'
          '\na pinned pair includes code placement (README, the floor'
          '\nsection).')


def aa_table(cells, shapes, strategies, terms, meta, brief=False):
    pos = {st: i for i, st in enumerate(strategies)}
    pairs = [(st, twin_of(st)) for st in strategies if twin_of(st)]
    if 'sum-only-early' in pos and 'sum-only-late' in pos:
        pairs.append(('sum-only-late', 'sum-only-early'))
    if not pairs:
        print('no control pairs in this run')
        return
    calib = []
    # A filtered run removes the benches a distant pair was placed to span,
    # so its `span` is not the roster's and the crossed design it is half of
    # collapses. Measured: a 12-arm selection put spans of 28 and 0 at 5 and
    # 0, which is not a position contrast at all. Say so rather than let a
    # cheap probe look like an answer to the position question.
    if meta['rostered'] and len(strategies) < meta['rostered']:
        print('NOTE: %d of the roster\'s %d arms are in this run, so every'
              ' span below is\n      shorter than the roster places it and'
              ' no distant pair is distant.\n      Position needs a full run.'
              % (len(strategies), meta['rostered']))
    print('%-28s %-24s %5s %9s %8s %7s'
          % ('control', 'twin', 'span', 'published', 'paired', 'mean|d|'))
    for a, b in pairs:
        if b not in pos:
            continue
        # The `sum-only` pair is the correction, so netting it would divide
        # zero by zero; its raw ratio IS the position test the correction
        # rests on, and is the one figure here that must stay uncorrected.
        key = 'slope' if a.startswith('sum-only') else 'net'
        r = [cells[s][a][key] / cells[s][b][key] for s in shapes]
        dev = [abs(x - 1) * 100 for x in r]
        worst = max(zip(dev, shapes))
        pub = time_of(cells, shapes, a) / time_of(cells, shapes, b)
        print('%-28s %-24s %5d %9s %8.4f %6.2f%%'
              % (a, b, abs(pos[a] - pos[b]) - 1,
                 '       --' if pub != pub else '%9.4f' % pub,
                 geomean(r), stats.fmean(dev)))
        ci = paired_ci(r)
        if ci:
            half = (ci[1] - ci[0]) / 2 * 100
            covers = ci[0] <= 1.0 <= ci[1]
            calib.append((a, b, geomean(r), half, covers))
            print('%56s 95%% CI %.4f..%.4f (+-%.2f%%), %s 1'
                  % ('', ci[0], ci[1], half,
                     'covers' if covers else 'MISSES'))
        print('%56s worst cell %.2f%% on %s' % ('', worst[0], worst[1]))
        # The paired figure above is NET, so it carries the correction's
        # 1/(1-f) amplification and is not how much the arm disagrees with
        # itself. Print the raw ratio and f beside it, because reading the
        # net one as the arm's own disagreement is a mistake this made easy:
        # Run 10's `scaled` pair reads 5.36% net off 2.13% raw at f = 0.598,
        # and the write-up quoted the 11% of one cell as the arm being slow
        # by a ninth. Net is the floor between two published rows; raw is the
        # arm against itself. The sum-only pair has no correction to remove.
        if not a.startswith('sum-only'):
            raw = [cells[s][a]['slope'] / cells[s][b]['slope'] for s in shapes]
            f = stats.fmean([1 - cells[s][b]['net'] / cells[s][b]['slope']
                             for s in shapes if cells[s][b]['slope']])
            print('%56s raw %.4f at f %.3f, so 1 + raw/(1-f) ~= %.4f'
                  % ('', geomean(raw), f, 1 + (geomean(raw) - 1) / (1 - f)))
    insitu = [(b, base_of(b)) for b in strategies
              if base_of(b) in strategies]
    if insitu and any(terms.values()):
        print('\n%-28s %-24s %9s %8s %7s'
              % ('in-situ forcing term', 'against sum-only', 'ratio',
                 'median', 'mean|d|'))
        for arm, base in insitu:
            r = []
            for s in shapes:
                gap = cells[s][base]['slope'] - cells[s][arm]['slope']
                term = cells[s][base]['slope'] - cells[s][base]['net']
                if gap > 0 and term > 0:
                    r.append(gap / term)
            if not r:
                continue
            dev = [abs(x - 1) * 100 for x in r]
            worst = max(zip(dev, shapes))
            print('%-28s %-24s %9.4f %8.4f %6.2f%%'
                  % (base + ' - ' + arm, 'sum-only', geomean(r),
                     stats.median(r), stats.fmean(dev)))
            print('%64s worst cell %.2f%% on %s' % ('', worst[0], worst[1]))
        if not brief:
            print('\nA `-nosum` arm is its base run again and forced with one')
            print('element rather than the sum, so base minus it is that sum'
                  ' over')
            print('a vector the fill has just written. `sum-only` re-reads a')
            print('FIXED vector instead, which is the one thing its own two')
            print('halves cannot test about it: a ratio of 1 here says the'
                  ' two')
            print('reads cost the same and the subtracted term is unbiased.')

    # The pairs whose true ratio is exactly 1 are the only place the
    # computed interval can be held to an answer, so they are what says
    # whether it may be believed.
    known = [c for c in calib if not c[0].startswith('sum-only')]
    if len(known) >= 2:
        miss = [c for c in known if not c[4]]
        halves = sorted(c[3] for c in known)
        typical = stats.median(halves)
        spread = max(abs(c[2] - 1) for c in known) * 100
        print('\ncalibration: %d pair(s) with a true ratio of exactly 1, so'
              ' the interval\ncan be held to an answer here and nowhere else.'
              % len(known))
        print('  %d of %d intervals cover 1%s' % (len(known) - len(miss),
              len(known),
              '' if not miss else '; missing: '
              + ', '.join(c[0] for c in miss)))
        print('  median half-width %.2f%% against an observed spread of'
              ' %.2f%%,' % (typical, spread))
        if typical > 0:
            print('  so a computed interval understates real variability by'
                  ' about %.0fx.' % (spread / typical))
        print('  Multiply by that before believing any interval this reader'
              ' prints,\n  and read the factor as an order of magnitude: it'
              ' rests on %d pairs.' % len(known))
    elif calib:
        print('\ncalibration: fewer than two pairs of known ratio, so nothing'
              ' here says\nwhat the intervals above are worth.')

    if brief:
        return
    print('\nspan is how many benches run between the pair: a pair spanning a')
    print('bench measures whatever that bench leaves behind it. published is')
    print('the ratio of the two `time` columns, what a reader comparing two')
    print('rows gets. paired is the')
    print('per-shape geomean, measurement noise alone; compare a per-shape')
    print('margin against that one. Both have the forcing pass subtracted,')
    print('as the table does -- except the `sum-only` pair, which is that')
    print('pass, reads raw, and has no published ratio to give. See this')
    print('script\'s docstring.')


def step_scan(path, min_iters=50, min_samples=20):
    """Every cell's best change of level mid-bench, and how strong it is.

    Criterion fits ONE slope per cell, so a bench that runs at two speeds
    publishes their average and reports nothing about either -- the fit
    stays tight, the interval narrow and R2 at 1.000 while the number is
    of a state the arm was only half in. That is measured, not feared:
    `scaled`'s A/A slot is a 4.46% step two thirds of the way through one
    arm's samples, and the wild cell is the same thing entered before the
    bench began (README.md#what-is-open). Both are invisible to every
    other column here, which is why this mode exists.

    The statistic is the best two-segment split of per-iteration times,
    taken past the warm-up ramp, scored against the pooled scatter inside
    the two segments. **The threshold is the whole test.** Some split is
    always the best one, so taking it at face value flags a quarter of all
    cells and means nothing; `t` above 40 with a step past 2% flags about
    3% of them and puts the arms this page already suspects -- `build`,
    `mut-odo`, `offtab` -- at the top. Never quote the first without the
    second.

    Read a hit as a question, not a verdict: what confirms one is the
    shape the two known instances have -- both segments flat within
    themselves, the earlier one level with a twin or with the same arm in
    another process, and allocation per iteration identical across the
    split, which `--cells` and the pair's own twin supply.
    """
    raw = json.load(open(path))
    out = []
    for r in raw[2]:
        m = [s for s in r['reportMeasured'] if s[3] >= min_iters]
        if len(m) < min_samples:
            continue
        m.sort(key=lambda s: s[3])
        per = [s[0] / s[3] for s in m]
        n = len(per)
        # Prefix sums make the sweep linear rather than quadratic: the run
        # files here carry ~4000 cells of ~100 samples, and a quadratic
        # sweep over all of them is minutes where this is seconds.
        pre, pre2 = [0.0], [0.0]
        for v in per:
            pre.append(pre[-1] + v)
            pre2.append(pre2[-1] + v * v)

        def ss(i, j):
            k = j - i
            s1, s2 = pre[j] - pre[i], pre2[j] - pre2[i]
            return max(s2 - s1 * s1 / k, 0.0)

        tot, k = min(((ss(0, i) + ss(i, n), i) for i in range(6, n - 6)),
                     key=lambda z: z[0])
        var = tot / (n - 2)
        if var <= 0:
            continue
        a, b = pre[k] / k, (pre[n] - pre[k]) / (n - k)
        t = abs(b - a) / math.sqrt(var * (1 / k + 1 / (n - k)))
        out.append((r['reportName'], (b / a - 1) * 100, t, k, n, m[k][3]))
    return out


def step_table(path, cells, shapes, strategies, meta):
    hits = step_scan(path)
    strong = [h for h in hits if h[2] > 40 and abs(h[1]) > 2]
    weak = [h for h in hits if h[2] > 10 and abs(h[1]) > 2]
    print('%s: %d cell(s) read at sample level' % (meta['path'], len(hits)))
    print('  step past 2%%: %d at t>10, %d at t>40 -- and %d cells have SOME'
          ' best split, which is why the threshold is the test'
          % (len(weak), len(strong), len(hits)))
    if not strong:
        print('  nothing above the threshold in this population')
        return
    print()
    print('  %-46s %8s %7s %10s' % ('cell', 'step', 't', 'at sample'))
    for name, d, t, k, n, iters in sorted(strong, key=lambda h: -abs(h[1])):
        print('  %-46s %+7.2f%% %7.0f %6d/%-4d' % (name, d, t, k, n))
    print()
    print('  A hit is a question: confirm it with both segments flat, the'
          ' earlier one level')
    print('  with a twin or the same arm elsewhere, and allocation per'
          ' iteration equal across it.')


def cell_dump(cells, shapes, strategies):
    # `slope_net_s` is here so that a ratio taken from this dump is the one
    # the tables publish: raw slopes alone would silently give uncorrected
    # figures to anything recomputing from the TSV.
    print('shape\tstrategy\tslope_s\tslope_net_s\tci_pct\tci_hi_pct\tr2'
          '\tsamples\talloc_bytes\talloc_mult')
    for sh in shapes:
        for st in strategies:
            c = cells[sh][st]
            print('%s\t%s\t%.9g\t%.9g\t%s\t%s\t%.6f\t%d\t%s\t%s'
                  % (sh, st, c['slope'], c['net'],
                     'NA' if c['ci'] is None else '%.4f' % c['ci'],
                     'NA' if c['ci_hi'] is None else '%.4f' % c['ci_hi'],
                     c['r2'], c['n'],
                     'NA' if c['alloc_bytes'] is None
                     else '%.6g' % c['alloc_bytes'],
                     'NA' if c['alloc'] is None else '%.4f' % c['alloc']))


# The per-shape record README keeps between runs, in the two-table form
# What Run N compares against pastes whole. Membership mirrors that
# section's rule -- the shipped arm, the rows the Results table bolds,
# and any arm an open question names; an arm leaves when its question
# closes -- and the grouping keeps every emitted row inside README's
# width. The short column heads are the stretch table's convention; the
# README intro above the tables maps them back to full arm names.
# `bq-scan-packed-mulback` and `bq-mut-runs-mulback` left on 2026-08-09, by
# the membership rule's own clause: an arm leaves when its question closes,
# and the precondition ruling closed both by stopping their benches. Their
# columns went from README's tables in the same edit -- `install` matches a
# table by its whole header line, so a narrowed emitter and a wide table on
# the page would refuse rather than install.
FINGERPRINT_TABLES = [
    ('| shape | `sInner` | `l` | `list`, net | bq-expand |',
     True, ['bq-expand']),
    ('| shape | scan-rem-gm | vecdims | mut-odo | build |',
     False, ['bq-scan-rem-gm-mulback', 'mut-odo-vecdims', 'mut-odo',
             'build']),
]


def fmt_abs(seconds):
    """A per-call time at reading precision, in README's units."""
    for unit, scale in (('s', 1), ('ms', 1e-3), ('µs', 1e-6),
                        ('ns', 1e-9)):
        if seconds >= scale:
            return '%.3g %s' % (seconds / scale, unit)
    return '%.3g s' % seconds


def fingerprint_table(cells, shapes, strategies, meta):
    """The kept per-shape record: dims, `list`'s net per call (absolute,
    so every ratio beside it converts back and the baseline is guarded at
    every shape), and the fingerprint arms' net ratios. Shapes sorted by
    l then name; an arm the run does not carry prints `--`.

    Born checked: pointed at a run without `list` (--exclude list) it
    refuses with exit 1, and its first emitted paste caught two Run 6
    cells still standing in README's hand-carried table --
    `alexnet-L1-55-c3-k11`'s scan-packed column and `stretch-bigstride`'s
    shipped one -- which is why the intro above the tables says to
    transcribe nothing by hand."""
    if 'list' not in strategies:
        sys.exit('--fingerprint needs the `list` baseline in the run')
    dims = meta['dims']
    ordered = sorted(shapes, key=lambda sh: (
        dims[sh]['l'] if sh in dims else float('inf'), sh))
    for i, (header, with_dims, arms) in enumerate(FINGERPRINT_TABLES):
        if i:
            print()
        print(header)
        print('|---' + '|---:' * (header.count('|') - 2) + '|')
        for sh in ordered:
            d = dims.get(sh)
            base = cells[sh]['list']['net']
            row = ['`%s`' % sh]
            if with_dims:
                row += [str(d['s_inner']), str(d['l'])] if d else ['?', '?']
                row.append(fmt_abs(base))
            for arm in arms:
                c = cells[sh].get(arm)
                row.append('%.3f' % (c['net'] / base) if c else '--')
            print('| ' + ' | '.join(row) + ' |')


# The three arms the second class property names
# (README.md#the-claims-run-14-should-test). Constants rather than literals
# because the property has been re-aimed twice, and a re-aim that misses one
# use of a name is how a verdict starts disagreeing with the claim it checks.
# The orderings each numbered claim rests on, as pairs, in the claims
# section's own order (README.md#the-claims-run-14-should-test). A manifest
# rather than a parser over the prose: the claims are not uniformly
# machine-readable -- claim 2's second half is `offtab` BEHIND the shipped
# arm rather than an `A < B` ordering, and claim 4 states two readings of
# one arm -- so anything scraping them would be wrong on exactly the two
# that need care. Claims 7 and 8 name no pair: 7 is the allocation column,
# read by `--compare --alloc`, and 8 is structural, read off the table.
# `--lint` holds every arm here to the roster, which is what stops a
# re-aimed claim from leaving a verdict checking an arm no run times.
# Each pair carries its registered expectation, so `--claims` prints a
# verdict rather than leaving every reading to be judged by eye against the
# claims section. The predicate follows the section's own rules: a direction
# claim is judged on which side of 1 the paired geomean falls ("the margin
# is the finding and the p is not"), a tie on the sign test alone (which is
# how claims 4 and 6 are stated), and claim 9's stable half on the two best
# shapes of the sort, its geomean being explicitly not the claim.
CLAIMS = [
    (1, 'the ceiling ordering, on unconditional arms',
     [('mut-odo-vecdims', 'mut-flat-gm', 'faster'),
      ('mut-flat-gm', 'bq-mut-runs-gm-mulback', 'faster'),
      ('bq-mut-runs-gm-mulback', 'bq-odo-gm-mulback', 'faster')]),
    (2, 'the m-length table beats the scratch that builds it and the '
        'l-length table that replaces it',
     [('bq-expand', 'bq-mut', 'faster'),
      ('offtab', 'bq-expand', 'slower')]),
    (3, 'a mul-back output pays on the shipped build',
     [('bq-expand-gm-mulback', 'bq-expand', 'faster')]),
    (4, 'the scan ties its own build control, and ties the shipped arm',
     [('bq-scan-rem-gm-mulback', 'bq-expand-gm-mulback', 'tie'),
      ('bq-scan-rem-gm-mulback', 'bq-expand', 'tie')]),
    (5, 'the build ordering, trimmed to its timed arms',
     [('bq-expand', 'bq-gen', 'faster'),
      ('bq-mut-runs', 'bq-expand', 'faster')]),
    (6, 'the first attempt ties the baseline',
     [('gen-quotrem', 'list', 'tie')]),
    (9, 'read per shape, not on its geomean',
     [('bq-expand-b', 'bq-expand',
       ('best2', 'stretch-inner1', 'stretch-wide-2xM')),
      ('bq-expand-zf', 'bq-expand', 'slower')]),
]


def claims_table(cells, shapes, strategies, args):
    """Every claim's reading and its registered verdict, in one call.

    Each ordering is one `--pair`, and a write-up used to run a dozen of
    them by hand and then judge each against the claims section by eye --
    which is where a wrong verdict gets invented, so the expectations now
    ride in the manifest above and the verdict is printed beside the
    figures. What stays the author's is everything a predicate cannot
    hold: whether a HELD margin moved against the run before, and whether
    a movement clears the floor -- a margin inside it is requoted without
    comment.

    Claims 7 and 8 print as reminders with no figures, having no pair:
    7 is `--compare --alloc` between the halves and 8 is read off the
    table. Naming them here rather than omitting them is the point -- a
    list of seven where the page has nine is how a claim goes unchecked.

    Born checked: run against Run 13's basis, every ordering it prints
    reproduces the figure that run published -- geomean, win count and
    sign p alike -- on all thirteen of them. The verdicts' own
    non-vacuity, 2026-08-14 against that same run: every pair prints HELD,
    and flipping claim 3's expectation to `slower` printed BROKE on the
    same figures, as did swapping claim 9's two registered shapes for
    `stretch-primes` -- so both predicate kinds can fail, and the reverted
    manifest returned thirteen HELDs.
    """
    missing = [a for _, _, ps in CLAIMS for p in ps for a in p[:2]
               if a not in strategies]
    if missing:
        print('NOTE: %d arm(s) of the claims list are not in this run: %s'
              % (len(missing), ', '.join(sorted(set(missing)))))
        print('      a filtered run cannot check the claims; use a full one.')
    held = broke = 0
    for n, label, pairs in CLAIMS:
        print('\nclaim %d -- %s' % (n, label))
        live = [[a, b] for a, b, _ in pairs
                if a in strategies and b in strategies]
        for a, b, _ in pairs:
            if [a, b] not in live:
                print('  %s / %s: not in this run' % (a, b))
        if live:
            pair_table(cells, shapes, strategies, live, quiet=True)
        for a, b, expect in pairs:
            if [a, b] not in live:
                continue
            _, r = pair_stats(cells, shapes, a, b)
            g = geomean(r)
            p = sign_p(sum(1 for x in r if x < 1), len(r))
            if isinstance(expect, tuple):
                best = sorted(s for _, s in sorted(zip(r, shapes))[:2])
                ok = best == sorted(expect[1:])
                want = 'best two shapes are %s' % ' and '.join(
                    sorted(expect[1:]))
                got = 'they are %s' % ' and '.join(best)
            elif expect == 'tie':
                ok = p >= 0.05
                want, got = 'a tie by sign test', 'sign p %.2g' % p
            else:
                ok = (g < 1) if expect == 'faster' else (g > 1)
                want = 'A %s (geomean %s 1)' % (expect,
                                                '<' if expect == 'faster'
                                                else '>')
                got = 'geomean %.4f' % g
            held += ok
            broke += not ok
            print('  %s  %s / %s: registered %s; %s'
                  % ('HELD ' if ok else 'BROKE', a, b, want, got))
    print('\n%d of %d registered orderings held.' % (held, held + broke))
    print('\nclaim 7 -- allocation: no pair; read it with'
          '\n  ./read-run.py BASIS.json --compare OTHER.json --alloc')
    print('claim 8 -- structural: no pair; read the fast tier off the table'
          '\n  and check the gap to bq-gen is populated.')
    print('\nA verdict answers the registered predicate and nothing more.'
          '\nWhether a HELD margin moved against the run before, and whether'
          '\na movement clears the floor, are still the reading\'s to say.')


PROP2_FASTEST = 'mut-odo-vecdims'
PROP2_PURE = 'bq-scan-rem-gm-mulback'
SHIPPED = 'bq-expand'


def is_pure(needs):
    """Does this `needs` cell say the arm requires nothing of the API?

    The shipped arm's cell reads `**nothing -- SHIPPED**` and the others
    `nothing (pure)`, so the test is the shared word once emphasis is gone.
    A cell left as `?` -- a row newer than the table it is carried from --
    is not pure and not impure, and the caller is told rather than guessed
    at, since a silent wrong answer here is exactly what this function is
    here to stop.
    """
    return needs.strip().strip('*').lower().startswith('nothing')


def block_verdicts(cells, shapes, strategies, meta, args):
    """The claims a class paragraph makes, derived instead of eyeballed.

    Everything here is readable off the table printed two inches above, and
    that is the problem: reading it off by eye is what the procedure's
    derive-from---cells rule forbids and what a session does anyway, the
    table being right there while the paragraph is being written. Three of
    Run 9's class sentences were wrong that way -- a `build`/`offtab`
    ordering, an `offtab`-trails-`bq-expand` count given as one class when
    it was four, and a pair quoted backwards -- each caught only by
    recomputing afterwards. So the recomputation moves to where the prose is
    written.

    It states the three properties' verdicts and nothing else: no adjectives,
    no mechanism, no comparison to another run. Those are the author's, and a
    skeleton that guessed at them would be trusted for more than it knows.

    Property 2 is read on the arms the claim NAMES, which is the reading the
    claim makes; where a class's actual leaders differ, the first two lines
    say so and the author decides. Both readings are wanted -- Run 9's
    `reshape1` breaks the named one and holds the leaders one.

    Non-vacuous: on Run 9 it says HOLDS for property 2 on `window` and names
    a different, correct break on each of `rev`, `bcast`, `reshape1`,
    `bcastmid` and `slice`, so it is not a constant; and `is_pure` separates
    `nothing (pure)` and `**nothing -- SHIPPED**` from `mutable \\`Int\\`
    scratch` and from an unwritten `?`.
    """
    rows, have_list = strategy_rows(cells, shapes, strategies)
    if not have_list:
        return
    needs = {st: n for st, (_, _, n)
             in readme_rows(args.readme, strategies).items()}
    timed = [r for r in rows if not is_control(r[1]) and r[0] == r[0]]
    if not timed:
        return
    unknown = [r[1] for r in timed if r[1] not in needs
               or needs[r[1]].strip() in ('?', '')]
    pure = [r for r in timed if is_pure(needs.get(r[1], '?'))]
    print()
    print('Verdicts, derived from the cells above; the paragraph is yours:')
    print('  fastest timed arm   %-30s %.3f' % (timed[0][1], timed[0][0]))
    if pure:
        print('  fastest pure arm    %-30s %.3f' % (pure[0][1], pure[0][0]))
    shipped = next((r for r in timed if r[1] == SHIPPED), None)
    if shipped:
        print('  %-19s %-30s %.3f   worst %.3f'
              % (SHIPPED, '(shipped)', shipped[0], shipped[6]))
        print('  property 1, `worst` under 1: %s'
              % ('HOLDS' if shipped[6] < 1 else '**BREAKS**'))
    clauses = []
    if timed[0][1] != PROP2_FASTEST:
        clauses.append('fastest is `%s`, not `%s`' % (timed[0][1],
                                                      PROP2_FASTEST))
    if pure and pure[0][1] != PROP2_PURE:
        clauses.append('fastest pure is `%s`, not `%s`' % (pure[0][1],
                                                           PROP2_PURE))
    if shipped:
        # Against the arms the claim NAMES, not against whichever arms lead:
        # `reshape1` breaks this clause only on the named reading, the flat
        # fills having taken its top, and the named reading is the claim's.
        by = dict((r[1], r[0]) for r in timed)
        ahead = [n for n in (PROP2_FASTEST, PROP2_PURE)
                 if n in by and shipped[0] < by[n]]
        if ahead:
            clauses.append('`%s` is AHEAD of %s'
                           % (SHIPPED, ', '.join('`%s`' % a for a in ahead)))
    verdict2 = ('HOLDS' if not clauses
                else '**BREAKS** -- ' + '; '.join(clauses))
    print('  property 2, top of the table: %s' % verdict2)
    # This verdict is mechanical and PRE-RULING, and one standing ruling
    # overrides it: the first clause is the vecdims FAMILY's, not one arm's,
    # so a sibling leading by a thousandth is not a break. Say so here rather
    # than let a write-up copy six breaks out of a run that has one -- Run 10
    # would have read as breaking property 2 in six of eight classes, where
    # the family reading makes it one, `reshape1`.
    if timed[0][1] != PROP2_FASTEST and timed[0][1].startswith(PROP2_FASTEST):
        print('     (the leader is a `%s` sibling, so the first clause does'
              ' NOT break:\n      it is read as the family\'s until a run'
              ' separates them -- README, the claims)' % PROP2_FASTEST)
    tiers = [(st, dict((r[1], r[5]) for r in rows).get(st))
             for st in (PROP2_FASTEST, SHIPPED, 'list')]
    print('  property 3, allocation: %s'
          % ', '.join('%s %s' % (st, '--' if a is None else '%.2fx' % a)
                      for st, a in tiers))
    if unknown:
        print('  NOT classified pure or impure, `needs` unwritten: %s'
              % ', '.join(unknown))


def block_skeleton(cells, shapes, strategies, meta, args, terms):
    """A stride-class block's mechanical parts in one place, in the form's
    order (README.md#the-stride-classes-run-by-run): the six-column table,
    the controls off the same computation `--aa` prints, the provenance
    and anchor skeleton -- elapsed time and heap peaks left blank, to be
    copied from the process's stderr line rather than guessed -- and, for
    a three-shape population, the bolded rows' per-shape ratios in run
    order, which is the order the block's lead lists its shapes in. The
    judgement stays with the author: the lead and the class's paragraph
    are deliberately not scaffolded, a skeleton writing no findings.

    Born checked: pointed at the main set it refuses with exit 1 naming
    the population, and its rev output matched the hand-written rev block
    to the digit, the per-shape line and the anchor both."""
    kind, label = population_of(shapes, meta['dims'])
    if kind != 'class':
        sys.exit('--block is for a stride-class run, and this run is %s'
                 % label)
    if 'list' not in strategies:
        sys.exit('--block needs the `list` baseline in the run')
    # --brief drops the table: --in-place installs it from this same
    # computation, so a session that is installing has no use for the copy
    # on its terminal, and it is the bulk of what this mode prints.
    if not args.brief:
        markdown_table(cells, shapes, strategies, meta, args, terms)
        print()
    aa_table(cells, shapes, strategies, terms, meta, args.brief)
    controls_skeleton(cells, shapes, strategies, terms)
    dims = meta['dims']
    anchor = max(shapes, key=lambda sh: dims.get(sh, {}).get('l', 0))
    print()
    print('Provenance: elapsed ___, peak ___ MiB in use, ___ MiB max'
          ' residency (copy')
    print("from the process's stderr line); the reader reads %d benchmarks"
          ' over %d' % (meta['benches'], meta['shapes']))
    print('shapes of %s. Anchor: `%s`, `list` at' % (label, anchor))
    print('%s per call raw, %s net.'
          % (fmt_abs(cells[anchor]['list']['slope']),
             fmt_abs(cells[anchor]['list']['net'])))
    if len(shapes) > 2:
        rows = readme_rows(args.readme, strategies)
        bold = [st for st in strategies
                if rows.get(st, ('', '', ''))[1] == 'bold']
        print()
        print("Per shape, in the lead's order (%s):" % ', '.join(shapes))
        for st in bold:
            print('  `%s` %s' % (st, '/'.join(
                '%.3f' % (cells[sh][st]['net'] / cells[sh]['list']['net'])
                for sh in shapes)))
    # What the fitted slopes cannot show, and a class block never looked
    # for: a cell that changed level mid-bench. `rev` and `slice` carry
    # the most of them over Runs 10 to 13, and the threshold is the test
    # rather than a detail -- see --steps, whose reading this repeats.
    hits = [h for h in step_scan(meta['path'])
            if h[2] > 40 and abs(h[1]) > 2]
    print()
    if hits:
        print('Steps: %d cell(s) changed level mid-bench, %s.'
              % (len(hits), ', '.join('`%s` %+.2f%%' % (h[0], h[1])
                                      for h in hits[:4])))
        print('Read each as a question -- both segments flat, the earlier'
              ' one level with a twin -- not as a verdict.')
    else:
        print('Steps: none past 2% at t over 40.')
    block_verdicts(cells, shapes, strategies, meta, args)


ARM_RE = re.compile(r'^\s*[\[,]\s*\("([^"]+)",\s*'
                    r'(Base|Fill|Twin|Term|Force|Only)(?:\s+(fb\w+))?\)')


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


FIGURE_RE = re.compile(r'\b0\.\d{3}\b|\d+\.\d+\s*[×x]\b'
                       r'|\b\d{1,2}\.\d%|\b\d+\.\d{2,}\b')

# A sentence quoting a figure this page no longer publishes. Each has to earn
# its place -- README's own rule is that a superseded NUMBER is cut while a
# superseded DECISION is kept, and the test is whether someone would redo the
# work without it. That is a judgement, so these are listed for adjudication
# rather than failed: the check exists because the rule fires while writing
# and needs something that fires while reviewing. Main.hs comments are swept
# too, since Run 7's write-up put its hard cases exactly there -- the one
# file the sweep did not then read.
COMPARATIVE_RE = [re.compile(p, re.I) for p in (
    r'where (?:Failed )?Run \d', r'where it (?:read|had|was)',
    r'\bwas \d+[\d.]*[%x×]?\b', r'had (?:read|been|put)',
    r'against its (?:published|own) \d', r'\(was \d',
    r'used to (?:say|call|read|be)', r'once said', r'earlier version')]

# A superlative is a claim about the WHOLE table and is derived by sorting
# it, never by looking at the arms the sentence is about. The reading is
# what adjudicates -- most hits here are sound -- but the reading has to
# happen, and the failure mode is not noticing you wrote one. Run 10 shipped
# two false ones past every check: "uniquely among the nine populations",
# which sorting puts at six of nine, and "the widest of any population",
# which `--pair` puts second to `reshape1`. Neither word is among the four
# the rule names, which is why the cousins are here too. `worst` is left out
# on purpose: it is a column name in every table this file prints.
#
# Bare `the only` and `never` are NOT in the list and were tried: this file
# argues about method constantly, so they matched 84 lines of prose that
# claims nothing about a table ("the only home for an open question", "never
# migrated"), and a report that long is one nobody reads. They are back in a
# form that has to name a table thing. Tuned against the two real errors and
# the three commonest false ones, all four counts recorded above.
SUPERLATIVE_RE = [re.compile(p, re.I) for p in (
    r'\bno other\b', r'\bnowhere else\b', r'\buniquely?\b',
    r'\bthe (?:largest|smallest|widest|narrowest)\b',
    r'\bthe (?:fastest|slowest|best|highest|lowest)\b',
    r'\bof any (?:population|class|run|arm|shape)\b',
    r'\bin every (?:population|class|run|regime)\b',
    r'\bthe only (?:population|class|run|regime|arm|shape|cell|row'
    r'|one|two|three)\b',
    r'\bnever (?:slower|faster|above|below|past|worse|better)\b')]

# An absolute millisecond figure is foreign here -- a run's own figures are
# ratios -- so it was measured in another repo and no run here replaces it.
# Like the sweep above, listed for judging: check it against its source.
MS_RE = re.compile(r'\b\d+(?:\.\d+)?\s*ms\b')


def unwrapped_paragraphs(lines):
    """[(first line, paragraph, spans)] with each paragraph on one line.

    From `wrap80 --unwrap`, the formatter that writes this file, so that what
    counts as a paragraph is what counts as one everywhere else rather than a
    second opinion kept here. `spans` is [(line number, words on it)] for the
    lines the paragraph came from, which is what places a match: counted in
    words and not characters, because unwrapping may set a sentence gap to two
    spaces where the break had been and a character offset would then point a
    column out.

    Table rows are dropped, as every caller wants prose. Without wrap80
    nothing is returned and the caller is told so: a read that silently
    narrows is the failure this exists to undo.
    """
    try:
        flat = subprocess.run(['wrap80', '--unwrap'], input='\n'.join(lines),
                              text=True, capture_output=True,
                              check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        raise SystemExit('BLOCKED: wrap80 --unwrap failed (%s), so no prose'
                         ' was read at all' % e)
    src = [(n, l.strip()) for n, l in enumerate(lines, 1)
           if l.strip() and not l.lstrip().startswith('|')]
    out, k = [], 0
    for para in (l for l in flat.split('\n') if l.strip()):
        if para.lstrip().startswith('|'):
            continue
        words, first, spans = para.split(), None, []
        while k < len(src) and sum(c for _, c in spans) < len(words):
            n, l = src[k]
            if first is None:
                first = n
            spans.append((n, len(l.split())))
            k += 1
        out.append((first, para, spans))
    return out


def prose_hits(lines, pats):
    """[(line number, line)] for each line whose PARAGRAPH matches a pattern.

    Matching line by line makes the answer depend on where the prose happens
    to be wrapped, because a phrase the pattern needs whole -- "where Run 9",
    "the fastest" -- stops matching as soon as a break lands inside it. That
    is invisible: the sweep just gets quieter, and nothing says a claim went
    unadjudicated. Reflowing this file to its 80-column limit moved one
    comparative out of sight and brought six superlatives back into it, none
    of the seven having changed a word, which is what put this here. A match
    is reported against the line it starts on, so the line numbers still
    point where a reader should look, and a line matching twice is listed
    once, as it was when the test was `any`.

    What a paragraph is comes from `wrap80 --unwrap`, the formatter that
    writes this file, rather than from a second opinion kept here: one
    definition, in the tool that enforces it. The rule it applies is the one
    this function used to carry -- indentation alone cannot mark a block,
    since a list item's continuation is indented exactly as deeply as code,
    and what separates them is that code opens a run of lines after a blank
    while continuation prose sits inside one.

    A match is placed by counting words rather than characters, because
    unwrapping may set a sentence gap to two spaces where the line break had
    been, and a character offset would then point one column out.

    Without wrap80 nothing is swept and the caller is told so: a sweep that
    silently narrows is the failure this function exists to undo.
    """
    out = []
    for first, para, spans in unwrapped_paragraphs(lines):
        for p in pats:
            for m in p.finditer(para):
                at, seen = len(para[:m.start()].split()), 0
                line = first
                for n, c in spans:
                    if seen > at:
                        break
                    line, seen = n, seen + c
                out.append((line, para))
    return sorted(set(out))


def headings_of(text):
    """Every heading and the anchor GitHub gives it."""
    out = {}
    for h in re.findall(r'^#+\s+(.*)$', text, re.M):
        s = re.sub(r'[`*_]', '', h.lower())
        out[re.sub(r'[^a-z0-9 -]', '', s).strip().replace(' ', '-')] = h
    return out




# Where a named path may live. This directory first, then the orthotope
# checkout it sits in, then the sibling this page cites for horde-ad's
# benchmark, its docs and its CLAUDE.md.
PATH_ROOTS = [('.', 'here'), ('..', 'orthotope'),
              ('../../horde-ad', 'horde-ad')]
# Names that exist only while a run or a pair does, so their absence is the
# directory's normal state rather than a broken reference. The templates
# (`$R-...`, `<prefix>-...`) are caught by the `$`/`<` test instead.
#
# Each alternative spells the convention exactly rather than as a prefix,
# because an exemption is a hole and a loose one swallows the very mistake it
# should catch: a `<something>-pair.*\.txt` spelling once exempted a note
# whose name was in the wrong order, so it named no file and stood misspelt
# in README while this check reported every path resolving. Anchored on
# `run\d+-`, it exempts a note or an artifact that is merely deleted -- the
# directory's normal state -- and fails one that is misnamed.
TRANSIENT_RE = re.compile(r'^(?:run\d+-pair\.txt|smoke.*\.(?:json|md)|'
                          r'README\.smoke\.md|run\d+-[\w.-]*\.'
                          r'(?:json|log))$')
# A template names no file: `$R-<half>-main.json`, `<run>-pair.txt`. The
# exclusion is of `$` and `<` ANYWHERE in the token and not just at its head,
# which is the form this first had -- a spelling that let a mid-token `<run>`
# through and failed the run on it.
PATH_EXT_RE = re.compile(r'^[^$<]*[^/$<]\.'
                         r'(?:hs|py|cabal|sh|md|txt|yaml|yml)$')


def check_paths(doc):
    """Resolve every path-shaped name the document backticks.

    Pass 2 of the `doc-verification` discipline, in the one form that is
    worth mechanizing here. It is anchored on the EXTENSION and not on a
    slash, which is the whole design: this page backticks criterion bench
    names, and a bench name is `shape/arm` -- `lenet-L1-28-c1-k5/bq-expand`,
    `*/list`, `stretch-inner1/bq-expand-b` -- so a slash-based rule reports
    thirty benches and some arithmetic (`1/(1-f)`, `transpose_2/4/5/6`) as
    missing files and stops being read, which is the failure the skill's own
    case study records. Ending in a known source or config extension picks
    out the eighteen real ones and nothing else.

    A name that does not resolve FAILS: this is the check that catches a
    renamed script. Names outside any checkout (`~/r/horde-ad`) and
    templates are not path-shaped by the test above. Transient artifacts are
    listed separately rather than failed, a run's artifacts being kept
    while questions keep coming back to them.

    The sibling policy differs from the skill's deliberately, and the
    difference is recorded here rather than left to be rediscovered. That
    checker STOPS when a configured sibling is absent, because resolving
    names is the whole of what it does and a partial run proves almost
    nothing. Here it is one check among several about the page's internal
    consistency, all of which are worth running without horde-ad mounted --
    a fresh clone of this branch has no sibling at all. So an absent sibling
    downgrades to a NOTE that names the count, the root and every path it
    could not check, which is loud enough not to be a silent degrade.

    Non-vacuous, each confirmed by breaking it and reverting (2026-08-12,
    against a copy, the README verified byte-identical afterwards):
    appending a line naming `read-runn.py` failed and named it; naming
    `docs/ghc-issue-no-such-file.md` failed and named it, which is the
    sibling half; and appending a bench name and an arithmetic fragment --
    `stretch-nosuch-shape/bq-nosuch-arm` and `1/(2-g)` -- did NOT fail,
    the unclassified count going 408 to 410 instead, which is the false
    positive this check is shaped to avoid and the reason it is anchored on
    the extension. Re-confirmed 2026-08-12 after the template exclusion was
    widened to the whole token: the two bad names still fail and are named,
    while a bench name, an arithmetic fragment and `$R-<h>.json` together
    raise nothing. The absent-sibling branch has a live control too, run by
    pointing PATH_ROOTS at a directory that does not exist: 14 paths
    resolved, the other 4 were listed by name under NOT CHECKED with the
    root, and the run still exited 0.

    The transient exemption then earned a control nobody had to plant, which
    is the better kind: tightening it to spell the convention exactly made
    the run FAIL on a misspelt pair note already standing in README, which
    the looser pattern had been exempting silently. A check whose first
    failure is a defect nobody planted has proved more than a planted break
    can, and it is why each exemption spells a name rather than a prefix.
    Re-confirmed on the tightened form by planting `run12-pair-wrong.txt`,
    which fails, beside `run99-main.json`, which is exempt as it should be.
    """
    out = {'ok': [], 'transient': [], 'unresolved': [], 'unmounted': [],
           'unmounted_root': '', 'in_sibling': 0, 'unclassified': 0}
    here = os.path.dirname(os.path.abspath(__file__))
    for tok in sorted(set(re.findall(r'`([^`\s]+)`', doc))):
        if not PATH_EXT_RE.match(tok):
            out['unclassified'] += 1
            continue
        rel = tok.lstrip('./')
        if TRANSIENT_RE.match(rel):
            out['transient'].append(tok)
            continue
        for root, label in PATH_ROOTS:
            base = os.path.join(here, root)
            if not os.path.isdir(base):
                if not out['unmounted_root']:
                    out['unmounted_root'] = root
                continue
            if os.path.exists(os.path.join(base, rel)):
                out['ok'].append(tok)
                out['in_sibling'] += label == 'horde-ad'
                break
        else:
            if out['unmounted_root']:
                out['unmounted'].append(tok)
            else:
                out['unresolved'].append(tok)
    return out


# A sentinel for "no diff to compare against", distinct from "the diff adds
# nothing": with it every hit prints in the flat old form rather than being
# reported as not-new, which would be a lie about an unknown.
EVERYTHING = frozenset()


def added_lines(*paths):
    """The stripped text of every line this working tree ADDS over HEAD.

    Matched by content, not by line number, because a sweep hit carries the
    line it sits on and an edit above it moves every number below. A line
    the diff adds and that also existed elsewhere before is a false
    positive here, which costs one entry printed under NEW and is the safe
    direction to err in.

    Returns EVERYTHING when there is no diff to be had -- not a git
    checkout, git absent, or the file untracked -- so the caller falls back
    to the flat listing rather than announcing that nothing is new.

    Non-vacuous, all three branches exercised 2026-08-12: with README.md
    edited it returned 103 added lines; against `Main.hs`, which that tree
    did not touch, it returned the empty set; and against a path outside
    the repo, where `git diff` exits non-zero, it returned EVERYTHING and
    the flat form came back. The last is the branch worth naming: `cwd` is
    pinned to this script's directory, so the "not a checkout" case cannot
    be reached by running from elsewhere and needs git itself to fail.

    **That proof used to close over `sweep` as well, and saying so is the
    point.** It read `sweep` printing the new superlative under NEW, which
    made it a proof of two functions at once -- and when the other one
    changed, the half of it that had died went on being asserted here. What
    this function returns is checked above; whether a caller can match a hit
    against it is `is_fresh`'s to prove, and is proven there. A control that
    spans two functions is a control neither of them owns.
    """
    try:
        out = subprocess.run(['git', 'diff', '-U0', '--'] + list(paths),
                             cwd=os.path.dirname(os.path.abspath(__file__)),
                             capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return EVERYTHING
    if out.returncode != 0:
        return EVERYTHING
    return frozenset(l[1:].strip() for l in out.stdout.split('\n')
                     if l.startswith('+') and not l.startswith('+++')
                     and l[1:].strip())


LEAD_RE = re.compile(r'\*\*(.+?)\*\*', re.S)

# How many body-matched paragraphs `--para` prints when no lead matches. The
# lead search is exact enough to print every hit; the body search is not, so
# it is capped and says how many it dropped -- a silent cap would read as
# "that is all there is", which is the failure the no-silent-caps rule names.
PARA_BODY_CAP = 6


def paragraphs(readme, pattern):
    r"""Print the paragraphs whose BOLDED LEAD matches, and their line numbers.

    Retrieval, so that reading a paragraph does not mean finding it first.
    A session working through this page otherwise pairs a `grep -n` with a
    `sed -n` for every passage it wants, and both go stale the moment an
    edit above moves the lines -- which every `--in-place` install and every
    prose fix does. Matching the lead rather than the body is what keeps the
    output one paragraph instead of every line that mentions a word.

    **The page does NOT guarantee the precondition this used to claim.**
    It said every paragraph opens with a bolded lead; of the 868 paragraphs
    this function's own splitter returns, 457 carry a bolded span and 411
    carry none, and 37 of those 411 carry a figure. So a third of a percent
    of the page was not the gap -- a run's own material was. The unbolded
    ones are the opening section's continuous argument and the continuation
    paragraphs inside list entries, where the entry's lead already names the
    thing; `grep -n '^\*\*'` between two headings therefore gives a
    section's CLAIMS and not its contents, which is what the Provenance walk
    should be read as asking for.

    Hence the body fallback below, which fires only when no lead matches.
    Searching bodies first would print every paragraph mentioning a common
    word, which is why the lead is tried alone first; searching them never
    left those 37 reachable only by the `grep -n`/`sed -n` pair this mode
    exists to replace, which is the habit it was watching for and did not
    catch. Paragraph granularity is what bounds the fallback's output where
    a line-granular body search would not.

    A paragraph is what `wrap80 --unwrap` says it is, which is what the
    sweeps read too. Splitting on blank lines instead made a bulleted run one
    paragraph, so a lead inside one printed the whole run: 16 lines where the
    paragraph asked for is 3, over the 16 blocks here that hold more than one
    bullet, the largest 73 lines.

    Non-vacuous (2026-08-13): `--para 'wild cell'` returned the two
    paragraphs whose leads name it and not the dozens of lines that mention
    it; `--para 'no such lead anywhere'` printed the no-match line and
    exited 1; and a lead broken over two lines is still matched, the
    paragraph being one line by the time the pattern sees it.

    All four branches exercised when the fallback was added, on the same
    day: a lead match still returns alone and exits 0; `'The floor grows
    with the margins'`, the unbolded paragraph that sent this session to a
    hand-rolled slice in the first place, now returns by body and exits 0;
    `'therefore'` matches 15 bodies, prints 6 and says 9 were dropped; and a
    pattern in neither lead nor body prints the no-match line and exits 1.
    """
    try:
        lines = open(readme).read().split('\n')
    except OSError as e:
        sys.stderr.write('--para: %s\n' % e)
        return 2
    rx = re.compile(pattern, re.I)
    paras = list(unwrapped_paragraphs(lines))
    hits = 0
    for first, para, _ in paras:
        lead = LEAD_RE.search(para)
        if lead and rx.search(' '.join(lead.group(1).split())):
            print('%s:%d' % (os.path.basename(readme), first))
            print(para)
            print()
            hits += 1
    if hits:
        return 0

    body = [(first, para) for first, para, _ in paras if rx.search(para)]
    if not body:
        print('no paragraph whose bolded lead or body matches %r' % pattern)
        return 1
    print('no bolded lead matches %r; falling back to the body, where %d'
          ' paragraph(s) match:' % (pattern, len(body)))
    for first, para in body[:PARA_BODY_CAP]:
        print('%s:%d (body)' % (os.path.basename(readme), first))
        print(para)
        print()
    if len(body) > PARA_BODY_CAP:
        print('... and %d more, not printed; narrow the pattern rather than'
              ' reading past the cap' % (len(body) - PARA_BODY_CAP))
    return 0


def check_doc(readme, main_hs):
    """The mechanical half of verifying the write-up, as one command.

    Checks that used to be as many throwaway scripts, rewritten from memory
    each run and deleted after -- which is how a heading rename came to be
    verified by something that no longer existed. Anchors and coverage FAIL;
    the sweeps only list, because what they find needs judging.

    The superlative sweep's non-vacuity: appending one planted sentence --
    "the fastest of any population, which nobody sorted" -- took the count
    from 72 to 73 on a copy, and it was tuned to catch the two false
    superlatives Run 10's write-up actually shipped past every other check
    while missing the three commonest innocent phrasings. It only lists;
    sorting the table is the reader's, as with the figure sweep.

    Non-vacuity, each confirmed by breaking it: renaming a heading fails the
    anchor check and names the dead link; deleting a bullet from the replace
    list fails coverage and names all three sections that bullet covered;
    lengthening a line fails the width check; and renaming the marker the
    replace list is found by fails loudly rather than silently checking
    nothing. The second of those took two attempts -- the first edited a
    string the list no longer contained, so the break itself did nothing and
    the check was credited with a pass it had not earned. Verify that a
    deliberate break landed before believing what it proves. The figure
    sweep's Main.hs half: a planted `where Run 6 read 0.500` comment was
    listed as Main.hs with its line, beside the README entries, and was
    gone on revert. The ms sweep's
    break: `9.9 ms` appended to a prose, a table and an indented code line
    was listed for the prose line alone, the other two exempt as meant. The
    script's own anchor scan: appending a bogus README anchor
    (`no-such-anchor`) here failed the run and named this file -- and so did
    this sentence's first draft, which spelled the anchor out in the very
    form the scan reads. The yardstick check: deleting the older regime's
    column from that table failed with the regime it still named, and
    deleting the table's header failed with the other message.
    """
    try:
        doc = open(readme).read()
        main = open(main_hs).read()
    except OSError as e:
        sys.stderr.write('check-doc: %s\n' % e)
        return 2
    lines = doc.split('\n')
    anchors = headings_of(doc)
    bad, note = [], []

    refs = dict(re.findall(r'^\[([a-z0-9-]+)\]:\s*#([a-z0-9-]+)\s*$', doc,
                           re.M))
    dead = [a for a in re.findall(r'\]\(#([a-z0-9-]+)\)', doc)
            if a not in anchors]
    dead += ['[%s]:' % k for k, v in refs.items() if v not in anchors]
    dead += ['%s (used, undefined)' % u
             for u in set(re.findall(r'\]\[([a-z0-9-]+)\]', doc))
             if u not in refs and not re.search(r'^\[%s\]:' % u, doc, re.M)]
    dead += ['Main.hs -> ' + m for m in re.findall(r'README\.md#([a-z0-9-]+)',
                                                   main) if m not in anchors]
    me = open(os.path.abspath(__file__)).read()
    dead += ['read-run.py -> ' + m
             for m in re.findall(r'README\.md#([a-z0-9-]+)', me)
             if m not in anchors]
    if dead:
        bad.append('%d dead anchor(s): %s' % (len(dead), ', '.join(dead)))
    else:
        note.append('every anchor resolves, in %s, in %s and in this script'
                    % (os.path.basename(readme), os.path.basename(main_hs)))

    p = check_paths(doc)
    if p['unresolved']:
        bad.append('%d named path(s) do not resolve: %s'
                   % (len(p['unresolved']),
                      ', '.join(sorted(p['unresolved']))))
    else:
        note.append('%d named path(s) resolve, %d of them in a sibling '
                    'checkout; %d transient and %d not path-shaped, neither '
                    'checked'
                    % (len(p['ok']), p['in_sibling'], len(p['transient']),
                       p['unclassified']))
    if p['unmounted']:
        note.append('%d path(s) NOT CHECKED, %s is not mounted: %s'
                    % (len(p['unmounted']), p['unmounted_root'],
                       ', '.join(sorted(p['unmounted']))))

    # ASKED OF THE CANONICAL WRAPPED FORM, not of the working copy, so the
    # answer does not depend on how this file happens to be wrapped right
    # now. The coverage check below skips a line indented four spaces as
    # code -- and a nested list item's CONTINUATION lines are indented that
    # deeply too, so unwrapping the file turns each item into one line
    # indented three and hands the check figures it had never seen. That is
    # the same indentation heuristic `prose_hits` was rewritten to abandon,
    # and it made a fully unwrapped README fail a check about replace-list
    # coverage, which is the form the standing rule says to edit in. Wrapping
    # first costs one more formatter pass and makes the verdict invariant;
    # today's committed file already IS this form, so it changes nothing
    # about what the check says of it.
    #
    # Non-vacuous 2026-08-13, four states: the committed file, one paragraph
    # unwrapped, and the WHOLE file unwrapped all exit 0 -- the last having
    # failed here before this, which is what the change is for -- while
    # deleting one replace-list bullet still names its section and exits 1.
    # The last is the control: a check made invariant must not have been
    # made blind.
    canon = lines
    try:
        canon = subprocess.run(['wrap80'], input=doc, capture_output=True,
                               text=True, check=True).stdout.split('\n')
    except (OSError, subprocess.CalledProcessError):
        note.append('wrap80 unavailable, so coverage was asked of the working'
                    ' copy, whose answer depends on how it is wrapped')

    # Which section each line sits in, for both the coverage check and the
    # figure sweep.
    sec, cur = [], '(preamble)'
    for line in canon:
        m = re.match(r'^#+\s+(.*)$', line)
        if m:
            cur = m.group(1)
        sec.append(cur)
    head = [i for i, l in enumerate(canon)
            if l.startswith('**What the next run replaces.**')]
    tail = [i for i, l in enumerate(canon)
            if l.startswith('How a run is made')]
    if not head or not tail or tail[0] < head[0]:
        # A search that cannot find its subject has checked nothing.
        bad.append('could not locate the replace-list between its markers, so'
                   ' the coverage check did not run')
    else:
        block = '\n'.join(canon[head[0]:tail[0]])
        covered = set(re.findall(r'\]\(#([a-z0-9-]+)\)', block))
        covered |= {refs[k] for k in re.findall(r'\]\[([a-z0-9-]+)\]', block)
                    if k in refs}
        slug = {v: k for k, v in anchors.items()}
        gaps = []
        for i, line in enumerate(canon):
            if (line.lstrip().startswith('|') or line.startswith('    ')
                    or sec[i] == 'Provenance'):
                continue
            s = slug.get(sec[i])
            if FIGURE_RE.search(line) and s and s not in covered \
                    and sec[i] not in gaps:
                gaps.append(sec[i])
        if gaps:
            bad.append('%d figure-bearing section(s) no replace-list bullet'
                       ' links: %s' % (len(gaps), '; '.join(gaps)))
        else:
            note.append('every figure-bearing section is linked from the'
                        ' replace list')

    # The README is not checked against a width. It is checked against the
    # formatter, which is a stronger thing to ask and a cheaper one to fix:
    # `wrap80 -i README.md` and there is nothing left to adjudicate. Asking
    # for a width instead is what taught readers of this check to wrap their
    # own edits line by line, which costs a great deal and does not converge,
    # since shortening one line pushes words onto the next.
    #
    # Nothing is lost by dropping the width test with unwrappable() under it.
    # A line the formatter leaves past 80 is one it cannot break -- a table,
    # a code block, a contents entry -- which is exactly what that function
    # computed: over this README and three rewrappings of it, all 67 such
    # lines were ones it exempted, every time. And the formatter catches two
    # things the width never could, a document left under-wrapped and a line
    # ending on a dangling article.
    # WHAT IS FORBIDDEN IS HAND-WRAPPING, and that is a property of a
    # PARAGRAPH, not of the file. Demanding the whole file be exactly as
    # wrap80 leaves it fails a document with one paragraph edited and left
    # long -- which is the state the standing rule asks for, an edit being
    # made at whatever length falls out of it -- so the check went red on an
    # ordinary edit and the way to green was to wrap. Wrap between edits and
    # the next exact-match edit has to quote breaks the last one moved, so
    # unwrap, and the cycle repeats per edit: a session ran it that way for
    # a whole write-up, having read the rule against it. The pressure was
    # this check, so this check is where it is removed -- in what it asks,
    # and in what it says when it passes: a verdict phrased as a state of
    # the file ("is as wrap80 leaves it") names the command that makes it
    # true, and a session ran that command to green a gate it was already
    # green for.
    #
    # A paragraph mid-edit is one of two innocent things: untouched, so
    # exactly as wrap80 left it, or just edited, so entirely on one line.
    # Hand-wrapping is neither, and that is what fails. The published form is
    # a separate question, asked at commit rather than here.
    #
    # Non-vacuous, every branch exercised 2026-08-14 on this README.
    # Untouched it says no paragraph is wrapped by hand and exits 0. With
    # one paragraph unwrapped -- what one edit leaves -- it says the same
    # and 1 still on one line, and exits 0, where the whole-file test called
    # that same file 4 lines wrong and failed. With one paragraph rewritten
    # a word per line it names it, gives its line, and exits 1. And with the
    # first item of a bulleted block joined into one line -- the same edit,
    # inside a list -- it is mid-edit and exits 0, where the block unit
    # called it hand-wrapped and failed: block 49, whose first item runs to
    # 16 lines, is the live control for that, and it is the case a whole
    # file unwrapped does not reach, every block being flat there.
    try:
        want = subprocess.run(['wrap80', readme], capture_output=True,
                              text=True, check=True).stdout
        flat = subprocess.run(['wrap80', '--unwrap', readme],
                              capture_output=True, text=True,
                              check=True).stdout
    except OSError:
        # A check that did not run must not read as one that passed.
        bad.append('BLOCKED: wrap80 is not on PATH, so the README wrapping'
                   ' was not checked at all')
    except subprocess.CalledProcessError as e:
        bad.append('BLOCKED: wrap80 failed (%d), so the README wrapping was'
                   ' not checked at all' % e.returncode)
    else:
        cur = open(readme).read()
        if want == cur:
            note.append('no paragraph of the README is wrapped by hand')
        else:
            # Aligned by index: wrapping never adds or removes a blank line,
            # so the three agree on how many blocks there are. Where they do
            # not, something outside this check's subject moved one, and the
            # whole-file comparison is the honest thing left to report.
            #
            # NO LIVE CONTROL, and named rather than left to look exercised:
            # over the eleven documents of these two repos the three counts
            # never differ, and by construction cannot, wrap80 touching no
            # blank line. The branch earns its place anyway because `zip`
            # truncates to the shortest -- so without it a mismatch would
            # under-check in silence, which is the one outcome worse than
            # reporting the whole file.
            # Judged LINE by line inside a block, because a block is not a
            # paragraph: a bulleted run is one block holding several, and an
            # edit to one item leaves that block matching neither form --
            # wrap80 would re-wrap the item, the unwrapped form would put
            # every sibling on its own line -- so a whole-block comparison
            # called a list mid-edit hand-wrapped and failed. A line an edit
            # left long is one the unwrapped form has, a line the formatter
            # would produce is in its own output, and hand-wrapping is what
            # is in neither.
            cp, wp, fp = (t.split('\n\n') for t in (cur, want, flat))
            if len(cp) == len(wp) == len(fp):
                hand, loose = [], []
                for i, (c, w, f) in enumerate(zip(cp, wp, fp)):
                    if c == w:
                        continue
                    ok = set(w.split('\n')) | set(f.split('\n'))
                    (loose if all(l in ok for l in c.split('\n'))
                     else hand).append(i)
                if hand:
                    # Summed rather than searched for: a short block can occur
                    # as a substring of an earlier one, and `index` would then
                    # send the reader to a paragraph that is fine.
                    at = cur.count('\n', 0,
                                   sum(len(b) + 2 for b in cp[:hand[0]])) + 1
                    bad.append('%d paragraph(s) of %s are wrapped by hand --'
                               ' first at line %d; run `wrap80 -i %s`, never'
                               ' re-wrap a line by hand'
                               % (len(hand), os.path.basename(readme), at,
                                  os.path.basename(readme)))
                else:
                    note.append('no paragraph of the README is wrapped by'
                                ' hand; %d still on one line, so it is'
                                ' mid-edit' % len(loose))
            else:
                # Diffed rather than compared by position: one inserted line
                # shifts every line under it, and reporting the whole file as
                # changed hides the one line worth looking at.
                d = list(difflib.unified_diff(lines, want.split('\n'),
                                              lineterm='', n=0))
                n = sum(1 for l in d
                        if l[:1] in '+-' and not l.startswith(('---', '+++')))
                at = next((m.group(1) for l in d
                           for m in [re.match(r'@@ -(\d+)', l)] if m), '?')
                bad.append('%s is not as wrap80 leaves it and its blocks do'
                           ' not line up with the formatter\'s (%d line(s),'
                           ' from line %s) -- run `wrap80 -i %s`'
                           % (os.path.basename(readme), n, at,
                              os.path.basename(readme)))

    # A paragraph that stops mid-sentence is what a scripted rewrite leaves
    # when it replaces more text than its author read. The shape is specific:
    # an edit anchored on a PREFIX and replacing a whole line -- which, on a
    # file in its unwrapped form, is a whole paragraph -- silently discards
    # whatever followed the part the author had in front of them. Nothing
    # else here sees it. The wrap check above compares against the
    # formatter's own output, so a truncated paragraph is wrapped exactly as
    # wrap80 would wrap it and passes; the figure sweeps read the numerals
    # that remain; `--lint` reads names. That is how one went out past two
    # green gates on 2026-08-14, and this check is the repair.
    #
    # What it asks, per paragraph rather than per line: does the last line of
    # a prose block end the way a sentence ends. Four things are not prose
    # and are skipped -- an indented line, a table row (indented or not), a
    # heading or blockquote, and a link reference definition. Two more end
    # legitimately without terminal punctuation and are the reason this is
    # not a one-line rule. A block ending in a FIGURE is a data line, not a
    # sentence: the per-shape line each three-shape class block carries ends
    # in a ratio, and the block form is this page's rather than a run's to
    # change. And a sentence may run INTO an indented block -- a code sample
    # or an indented table -- leaving the prose before it ending on `of` or a
    # dash with the rest after; three paragraphs of this page do that, so
    # the following block's indentation is consulted before failing anything.
    #
    # Non-vacuous, 2026-08-14, every branch exercised on this README. Whole
    # and untouched it reports 0 and exits 0. With a paragraph's TAIL dropped
    # -- the 2026-08-14 failure replayed, and re-wrapped first so that the
    # hand-wrapping check above cannot fire in its place -- it names the
    # paragraph, gives its line and exits 1. Its two exemptions have LIVE
    # CONTROLS here rather than planted ones, which is what keeps them from
    # being holes nobody tests: removing the figure ending fails this README
    # on 3 paragraphs, the `Per shape, in the lead's order` lines, and
    # removing the indented-continuation one fails it on 3 others, the
    # paragraphs that run into a code sample. Both were measured by removal
    # rather than assumed.
    #
    # WHAT IT DOES NOT CATCH, said here so nobody reads it as more: a deletion
    # from the MIDDLE of a paragraph, which leaves the paragraph still ending
    # in a sentence. The first attempt at the test above cut there, and this
    # check was right not to fire; only a dropped tail has a signature here.
    # A non-vacuity test has to reproduce the failure's shape, not merely
    # damage the file.
    def _tail(b):
        ls = [l for l in b.split('\n') if l.strip()]
        return ls[-1] if ls else None

    def _head(b):
        ls = [l for l in b.split('\n') if l.strip()]
        return ls[0] if ls else None

    def _not_prose(l):
        t = l.strip()
        return (l[:1] in ' \t' or t.startswith(('|', '#', '>', '<'))
                or bool(re.match(r'^\[[^\]]+\]:', t)))

    whole_md = '\n'.join(lines)
    blocks = whole_md.split('\n\n')
    cut = []
    for i, b in enumerate(blocks):
        tail = _tail(b)
        if tail is None or _not_prose(tail):
            continue
        t = tail.rstrip()
        ends_sentence = re.search(r'[.:;!?)\]*`"\u2019\u201d]$', t)
        if ends_sentence or re.search(r'[\d%]$', t):
            continue
        nxt = _head(blocks[i + 1]) if i + 1 < len(blocks) else None
        if nxt is not None and _not_prose(nxt):
            continue
        at = whole_md.count('\n', 0,
                            sum(len(x) + 2 for x in blocks[:i])) + 1
        cut.append((at, t))
    if cut:
        bad.append('%d paragraph(s) of %s stop mid-sentence -- first at line'
                   ' %d, ending "%s". A scripted rewrite that anchors on a'
                   ' prefix replaces the whole paragraph, including the part'
                   ' you did not read; quote the full old text instead'
                   % (len(cut), os.path.basename(readme), cut[0][0],
                      cut[0][1][-48:]))
    else:
        note.append('every prose paragraph of the README ends a sentence')

    # This page says of itself that it cites no line and no permalink,
    # deliberately -- naming arm, strategy and shape names instead, which
    # `--lint` can check and a line number could not, a citation surviving
    # the refactor that moves it. That was a claim in prose with nothing
    # holding it, and prose line numbers are the worse half: the formatter
    # rewraps this file on every edit, and where a hook restores its
    # committed form it can move between one session turn and the next, so
    # a `.md:12` would rot with nothing in any history to show it. Its
    # counterpart in horde-ad is `check-plan-citations.py`'s PROSE-LINE,
    # which refuses the same citation from the other side.
    #
    # Non-vacuous 2026-08-13: planting `micro-regime3/README.md:12` and a
    # permalink pinned at `5f0647baa` in the Provenance section reported
    # both, named them, and exited 1; removing them returned the ok line
    # and exit 0. The claim it enforces was true when written -- the page
    # carried zero of either -- which is what makes this a guard rather
    # than a repair.
    # Read off the raw lines rather than the unwrapped form: a citation
    # carries no space, so no break can fall inside one.
    whole = '\n'.join(lines)
    cited = sorted(set(re.findall(r'\b[\w./-]+\.(?:md|hs|py|txt|cabal|yaml'
                                  r'|yml|sh|json):\d+', whole)))
    pinned = sorted(set(re.findall(r'blob/[0-9a-f]{7,40}/', whole)))
    if cited or pinned:
        bad.append('%s cites %d line(s) and %d pinned permalink(s) where it'
                   ' says it cites neither: %s -- name a phrase, a heading or'
                   ' an arm, which a reflow cannot move'
                   % (os.path.basename(readme), len(cited), len(pinned),
                      ', '.join((cited + pinned)[:4])))
    else:
        note.append('the README cites no line and no pinned permalink, as it'
                    ' says of itself')

    # Main.hs and this script are code: no formatter here sets their width,
    # so they are measured against one and shortened by hand.
    wide = []
    for path, limit, comment_only in ((main_hs, 79, True),
                                      (os.path.abspath(__file__), 79, False)):
        for i, line in enumerate(open(path).read().split('\n'), 1):
            if len(line) <= limit:
                continue
            if comment_only and not line.strip().startswith('--'):
                continue
            wide.append('%s:%d (%d)' % (os.path.basename(path), i, len(line)))
    if wide:
        bad.append('%d code line(s) past the width: %s'
                   % (len(wide), ', '.join(wide[:6])))
    else:
        note.append('comments and this script are inside their widths')

    comparatives = [('%s:%d' % (os.path.basename(readme), i), l)
                    for i, l in prose_hits(lines, COMPARATIVE_RE)]
    comparatives += [('%s:%d' % (os.path.basename(main_hs), i),
                      l.split('--', 1)[1].strip())
                     for i, l in enumerate(main.split('\n'), 1)
                     if '--' in l
                     and any(p.search(l.split('--', 1)[1])
                             for p in COMPARATIVE_RE)]
    foreign = [(i, l) for i, l in prose_hits(lines, [MS_RE])
               if not lines[i - 1].startswith('    ')]
    superlatives = [('%s:%d' % (os.path.basename(readme), i), l)
                    for i, l in prose_hits(lines, SUPERLATIVE_RE)]

    added = added_lines(readme, main_hs)

    def is_fresh(text, added):
        """Does this hit's text carry a line the working tree added?

        CONTAINMENT, not equality, and that is the whole of this function.
        A hit's text is its entire PARAGRAPH for README and a comment's
        body for Main.hs, while `added` holds physical lines off `git diff`,
        so no hit can ever equal one and equality called every hit old --
        which is what it did, silently, from the commit that taught
        `prose_hits` to work in paragraphs until this was written. The two
        halves were each right and were changed a commit apart; nothing
        failed, the sweeps just said `none added by this diff` over a diff
        that had added plenty, and the freshness signal the whole listing
        exists for was gone.

        A Main.hs hit has already lost its `--`, so the added line is
        stripped of one before the test or it could never match. Lines of
        under three words are skipped: after stripping, a very short one
        matches almost any paragraph, and marking every hit new is as
        useless as marking none. What that costs is a paragraph whose only
        added line is a two-word one, which an edit hardly ever leaves.
        Erring toward NEW is otherwise right, and a line the diff adds that
        also stood elsewhere before is a false positive the caller accepts.

        Non-vacuous, and all three outcomes came out of one run, 2026-08-13.
        A paragraph carrying both a superlative and a superseded figure was
        pasted into the run chapter: the comparative sweep went to 62 hits
        and the superlative sweep to 81, each printing that paragraph and no
        other under NEW, while the absolute-time sweep stayed at 22 and said
        "none added by this diff", which is the right answer for a paragraph
        quoting no time. Reverting it put all three back to none. The same
        paste through the reader as it stood before this function moved the
        two counts identically and left all three sweeps saying none, 0 NEW
        -- which is the failure this replaces, and its shape: the counts
        were the only thing that ever moved, and nobody reads a count of 81
        for what is new in it.
        """
        for a in added:
            if a.startswith('--'):
                a = a.lstrip('-').strip()
            if len(a.split()) >= 3 and a in text:
                return True
        return False

    def sweep(hits, headline):
        """Print a sweep, NEW FIRST and counted apart.

        The whole value of these lists is which entries a write-up just
        wrote, and that is the one thing the flat form cannot show: Run 11
        shipped four false superlatives that were sitting in a list of 71,
        indistinguishable from 67 correct ones, and a wall of 71 gets
        adjudicated as a wall. `added` is the set of lines this working tree
        adds over HEAD, matched by content rather than by line number, so a
        hit is new when a line inside it is new -- see `is_fresh` for why
        that is containment and not equality.
        """
        fresh = [h for h in hits if is_fresh(h[1], added)]
        old_ = [h for h in hits if not is_fresh(h[1], added)]
        if added is EVERYTHING:
            print('note: %d %s' % (len(hits), headline))
        elif fresh:
            print('note: %d %s -- %d ADDED BY THIS DIFF, listed first and'
                  ' the only ones this write-up owes:' % (len(hits), headline,
                                                          len(fresh)))
        else:
            print('note: %d %s -- none added by this diff:'
                  % (len(hits), headline))
        for i, l in fresh:
            print('    NEW %s: %s' % (i, l[:60]))
        for i, l in old_:
            print('        %s: %s' % (i, l[:60]))

    for line in note:
        print('ok:   ' + line)
    if comparatives:
        sweep(comparatives, 'superseded figure(s) quoted; each has to earn'
              ' its place by the redo test, so adjudicate rather than assume')
    if superlatives:
        sweep(superlatives, 'superlative(s) in prose; each is a claim about'
              ' the whole table, so derive it by sorting rather than from'
              ' the arms the sentence is about')
    if foreign:
        sweep([('%s:%d' % (os.path.basename(readme), i), l)
               for i, l in foreign],
              'absolute time figure(s) quoted in prose; a class'
              " block's anchor is its run's, replaced with its block --"
              ' check any other against the repo it came from')

    # The yardstick table keeps a column for the regime this run is NOT in,
    # which reads like a leftover and is the opposite: it is the only place
    # the previous run's basis survives once this chapter has replaced
    # everything else of it, and a return to that regime would have nothing
    # to read against. Prose asks for it to be kept; this makes the asking
    # stick.
    yard = [l for l in lines if l.startswith('| strategy |') and '(' in l]
    if not yard:
        bad.append('the yardstick table is gone: no `| strategy |` header'
                   ' naming its runs, so no run has a basis to be read'
                   ' against')
    else:
        regimes = set(re.findall(r'\(([^)]*)\)', yard[0]))
        if len(regimes) < 2:
            bad.append('the yardstick table names one regime (%s); the'
                       " other regime's column is the only surviving record"
                       ' of that run and is not to be pruned'
                       % (', '.join(sorted(regimes)) or 'none'))
        else:
            print('ok:   the yardstick keeps a column per regime (%s)'
                  % ' / '.join(sorted(regimes)))

        # A paired run puts two columns here, one per half, and neither may
        # be dropped or folded into the other: an aligned build is a regime
        # and not a second reading of the one beside it. Keyed off the run
        # number so this holds for any later pairing and not just Run 10.
        # It HAS a live control now that Run 10 has landed: the yardstick
        # carries its two columns, so the pass above is a real pass, and
        # deleting the unaligned one from a copy fails with the message below
        # (re-proved 2026-08-11). Before that it could not fire at all and was
        # exercised by hand only. The run that would have published an aligned
        # column and no unaligned one was Run 11, aligned against a max-skip
        # half; SETTLED BY RENAMING THE COLUMNS, not by widening this, so the
        # rule below is unchanged and reads as "a paired run publishes a
        # column per half". Widening was refused because it would need a list
        # of which half names count as a counterpart, which grows with every
        # pair and is wrong the first time one is invented (README's open
        # list, under what the roster owes the next run). RE-PROVED against
        # that rename, 2026-08-11: a copy whose yardstick header carries only
        # `Run 11 (SpecConstr, aligned)` exits 1 on the message below, and one
        # carrying `Run 11 (SpecConstr, max-skip)` beside it exits 0. So the
        # rename is what passes it and the rule still bites.
        halves = collections.defaultdict(set)
        for run, regime in re.findall(r'Run (\d+) \(([^)]*)\)', yard[0]):
            # (?<!un) because `'aligned' in 'unaligned'` is True, which made
            # this reject the one pairing the message below calls correct: a
            # run naming its columns `unaligned` and `aligned` read as two
            # aligned halves and failed. Run 10 passed only because its other
            # column is named for no half at all, and Run 11 passes because
            # `max-skip` contains no `aligned` -- so the bug was invisible to
            # every run on the page. Found by a blind walk of the procedure,
            # 2026-08-11.
            halves[run].add(bool(re.search(r'(?<!un)aligned', regime)))
        for run, kinds in sorted(halves.items()):
            if kinds == {True}:
                bad.append('the yardstick names Run %s aligned and nothing'
                           ' else: a paired run publishes a column per half,'
                           ' the other one being named for the build it is'
                           ' -- unaligned, max-skip -- and never folded in'
                           % run)

    # Run-current facts stated in prose, held to the roster and to each
    # other. Three sentences quote what the current roster or the current
    # run's floor is, and each went stale exactly once before this existed:
    # `mut-flat-gm-nosum` landed and the controls sentence went on saying
    # ten controls and 34 benches, and the opening paragraph quoted Run 12's
    # noise floors as Run 13's for a whole run while the floor section
    # carried the right pair. Counts come from the roster, which is the
    # authority; the floor pair has no source on disk once the JSONs go, so
    # it is held to AGREEMENT across its sites -- a check that catches the
    # stale-opening failure without pretending to know which site is right.
    # A site the regexes cannot find FAILS rather than passing empty, the
    # phrasing being part of what is checked.
    #
    # Non-vacuous 2026-08-14, each on an unwrapped copy (the phrases split
    # across wrapped lines, which is why this reads the unwrapped form):
    # lowering the controls sentence's count to ten named the sentence and
    # the roster's own count; planting Run 12's 0.35% back into the opening
    # named the two disagreeing pairs; and rewording `A/A arms` out of the
    # controls sentence failed as `could not locate` rather than passing.
    # Re-proven 2026-08-14 after the roster took eight more A/A arms and the
    # controls sentence crossed twenty: each of the four counts was walked
    # one off in turn and each named itself and the roster's own figure. The
    # crossing is also what the hyphen in that first pattern is for -- the
    # prose writes `twenty-three`, which the old pattern could not match and
    # which failed, correctly, as `could not locate` rather than as a pass.
    roster = roster_of(main)
    if roster:
        W2N = {w: i for i, w in enumerate(
            'zero one two three four five six seven eight nine ten eleven'
            ' twelve thirteen fourteen fifteen sixteen seventeen eighteen'
            ' nineteen twenty'.split())}
        W2N.update(thirty=30, forty=40, fifty=50, sixty=60, seventy=70,
                   eighty=80, ninety=90)

        def num(tok):
            """A digit string, a number word, or a hyphenated compound.

            The compound arm exists because a count that crosses twenty is
            written `twenty-three` in this page's prose, which the word map
            alone cannot read and the pattern above must therefore admit
            a hyphen into.
            """
            tok = tok.lower()
            if tok.isdigit():
                return int(tok)
            if '-' in tok:
                parts = [W2N.get(p) for p in tok.split('-')]
                if any(p is None for p in parts):
                    return None
                return sum(parts)
            return W2N.get(tok)

        paras = unwrapped_paragraphs(lines)
        uw = '\n'.join(p for _, p, _ in paras)
        aa = [n for n, r, _ in roster if r == 'Twin']
        controls = [n for n, r, _ in roster if r in ('Twin', 'Term', 'Force')]
        timed = [n for n, r, _ in roster if r != 'Only']
        twinned = {twin_of(n) for n in aa}
        facts = [
            (r'are ([a-z\d-]+) controls: ([a-z\d-]+) A/A arms',
             (len(controls), len(aa)), "the controls sentence"),
            (r'with the controls the run is ([a-z\d]+) benches',
             (len(timed),), 'the bench count'),
            (r'([A-Za-z\d]+) A/A controls run an existing strategy twice',
             (len(aa),), "the floor section's design sentence"),
            (r'([a-z\d]+) strategies, each duplicated once beside its base',
             (len(twinned),), 'the crossed-design count'),
        ]
        lost, off = [], []
        for pat, want, whose in facts:
            ms = re.findall(pat, uw)
            if len(ms) != 1:
                lost.append('%s (%d matches for its phrasing)'
                            % (whose, len(ms)))
                continue
            got = ms[0] if isinstance(ms[0], tuple) else (ms[0],)
            got = tuple(num(g) for g in got)
            if got != want:
                off.append('%s says %s where the roster holds %s'
                           % (whose, '/'.join(map(str, got)),
                              '/'.join(map(str, want))))
        if lost:
            bad.append('could not locate %s, so the run-current count check'
                       ' did not run there -- if the sentence was reworded,'
                       ' this check\'s pattern moves with it'
                       % '; '.join(lost))
        if off:
            bad.append('run-current count(s) out of date: %s'
                       % '; '.join(off))
        if not lost and not off:
            print('ok:   the prose counts of controls, A/A arms, benches and'
                  ' twinned strategies all match the roster')

        floors = [m for p in (
            r'a noise floor this run measures at ([\d.]+)%[^.]*?'
            r' and ([\d.]+)%',
            r'floor is ([\d.]+)% on the basis half and ([\d.]+)%'
            r' on the control',
            r'no A/A pair further than ([\d.]+)% from 1 on the basis half'
            r' or ([\d.]+)% on the control') for m in re.findall(p, uw)]
        if len(floors) < 2:
            bad.append('could not locate at least two sites quoting the'
                       ' run\'s floor pair, so the floor-agreement check did'
                       ' not run -- if the sentences were reworded, this'
                       ' check\'s patterns move with them')
        elif len(set(floors)) > 1:
            bad.append('the run\'s floor pair is quoted differently across'
                       ' its %d sites: %s -- the head of the run chapter'
                       ' carries the measurement, so requote the others'
                       % (len(floors),
                          '; '.join('%s%%/%s%%' % f for f in set(floors))))
        else:
            print('ok:   the run\'s floor pair reads %s%%/%s%% at all %d'
                  ' sites that quote it' % (floors[0] + (len(floors),)))

        # Prospective tense about a run that has already happened. An open
        # list entry written before a run says what that run WILL do, and
        # the verdict pass rewrites it -- except when it does not: "Run 13
        # takes it at full budget, and its Results row will come out with
        # `?`" stood for a day after the row was in the table, filled with
        # a different phrase. Only `will` and `is to be` count as
        # prospective: this page narrates finished runs in the historic
        # present ("Run 10 takes it"), so verbs alone cannot tell a stale
        # promise from an idiom, and a sweep that listed every historic
        # present would be one nobody reads. Listed for adjudication, not
        # failed. Non-vacuous 2026-08-14: planting that very sentence in
        # the open list on a copy listed it with its line; the shipped page
        # lists nothing.
        m = re.search(r'^## About the last run \(Run (\d+)\)$', doc, re.M)
        lo = [i for i, l in enumerate(lines, 1)
              if l.startswith('## What is open')]
        hi = [i for i, l in enumerate(lines, 1)
              if l.startswith('## The goal')]
        if m and lo and hi:
            run_now = int(m.group(1))
            pro = re.compile(r'\bRun (\d+)\b[^.;]*?\b(?:will|is to be)\b'
                             r'|\b(?:will|is to be)\b[^.;]*?\bRun (\d+)\b')
            stale = []
            for first, para, _ in paras:
                if not lo[0] <= first < hi[0]:
                    continue
                olds = [int(a or b) for a, b in pro.findall(para)
                        if int(a or b) <= run_now]
                if olds:
                    stale.append((first, para))
            if stale:
                print('note: %d open-list paragraph(s) speak prospectively'
                      ' of a run that has already happened -- rewrite to'
                      ' what it did, or say why the promise stands:'
                      % len(stale))
                for first, para in stale:
                    print('        %s:%d: %s'
                          % (os.path.basename(readme), first, para[:60]))

    # Links into the run chapter from standing prose. The chapter is
    # replaced by the next run, so such a link keeps resolving -- the
    # rename step re-points it -- while the content it promised leaves:
    # five links reading "the head of the run chapter" decayed exactly that
    # way, their targets' substance having moved to the floor section when
    # Run 11's chapter was replaced. Listed for adjudication at every
    # check, not only at the rename, because the decay happens at the
    # replacement and nothing else looks then. Links from inside the
    # chapter's own sections are the run's and die with it, so only lines
    # above the chapter heading are swept; a bare link bullet -- the
    # Contents map's entry -- promises no content beyond the heading and is
    # exempt, or the map would head this list at every check and teach
    # readers to skim it. Non-vacuous 2026-08-14: planting
    # `([see the run](#about-the-last-run-run-13))` in the opening
    # paragraph of a copy listed it with its line; the shipped page lists
    # none, its one such link being the Contents entry the exemption is
    # for.
    m = re.search(r'^## About the last run', doc, re.M)
    if m:
        chap_at = doc[:m.start()].count('\n') + 1
        into = [(i, l.strip()) for i, l in enumerate(lines[:chap_at - 1], 1)
                if re.search(r'\]\(#about-the-last-run-run-\d+\)', l)
                and not (l.strip().startswith('- [')
                         and l.strip().endswith(')'))]
        if into:
            print('note: %d link(s) into the run chapter from standing'
                  ' prose; each is re-verified at the rename, its content'
                  ' being replaced with the chapter:' % len(into))
            for i, l in into:
                print('        %s:%d: %s'
                      % (os.path.basename(readme), i, l[:60]))

    for line in bad:
        print('FAIL: ' + line)
    return 1 if bad else 0


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
    named so that this reader counts it as a strategy. A fifth check is
    about the shape lists rather than the roster, the roster being not the
    only thing in Main.hs that goes stale silently.

    Non-vacuity, each confirmed by breaking it: renaming a bench in the
    roster fails the README check, commenting an entry out fails the
    rostered check, pointing a `-aa` arm at another function fails the twin
    check, pointing a `-nosum` arm at another function fails the Force check
    with the arm and both function names -- the one check here that had gone
    unproven, settled 2026-08-09 -- renaming a `Twin` arm to drop its `-aa`
    fails both the twin and
    the control-naming ones, a second `Base` entry fails the reference
    check, and misannotating window-28x28-k5's l by one fails the
    annotation check with both numbers -- as does mistyping a dimension,
    confirmed on one entry of each list rule that computes l differently
    (window, bcastmid, reshape1 and the strided rule the main set shares).
    Each names the arm or entry at fault rather than only the count. The
    README check reads names as delimited tokens: against a scratch README
    saying only `mut-odo-vecdims`, a rostered `mut-odo` fails, where
    substring containment had passed it.
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
    forces = [(n, f) for n, r, f in roster if r == 'Force']

    bad = []
    # As a delimited token, not a substring: `mut-odo` inside
    # `mut-odo-vecdims` documents only the longer name.
    undocumented = [n for n in names
                    if not re.search(r'(?<![\w-])%s(?![\w-])' % re.escape(n),
                                     doc)]
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

    # The claims manifest names arms `--claims` will ask the reader for, and
    # a re-aimed claim that misses one leaves a verdict checking an arm no
    # run times -- which fails only when somebody runs it, months later.
    # Held to the roster here, where every other name in this file is.
    # Non-vacuous 2026-08-14: renaming one arm of claim 4 in the manifest
    # named it and exited 1; restoring it returned the ok line.
    claimed = sorted({a for _, _, ps in CLAIMS for pr in ps for a in pr[:2]})
    stray = [a for a in claimed if a not in names]
    if stray:
        bad.append('%d arm(s) the claims manifest names are not rostered,'
                   ' so `--claims` would ask for what no run times: %s'
                   % (len(stray), ', '.join(stray)))
    else:
        print('ok:   every arm the claims manifest names is rostered'
              ' (%d across %d claims)' % (len(claimed), len(CLAIMS)))

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

    # Same question for the `-nosum` arms, and it matters more: a Force arm
    # pointed at the wrong function would not be a noisy control, it would
    # make `base - arm` a difference of two unrelated fills and report it as
    # a forcing term.
    off = []
    for n, f in forces:
        base = base_of(n)
        if base is None:
            off.append('%s is a Force arm whose name has no -nosum' % n)
        elif base not in fun:
            off.append('%s names %s, which is not in the roster' % (n, base))
        elif fun[base] != f:
            off.append('%s runs %s where %s runs %s'
                       % (n, f, base, fun[base]))
    if off:
        bad.append('Force control(s) not duplicating what the name says: %s'
                   % '; '.join(off))
    elif forces:
        print('ok:   each of the %d -nosum controls runs the same function as'
              ' the arm its name subtracts from' % len(forces))

    mislabelled = [n for n, r, _ in roster
                   if is_control(n) != (r in ('Twin', 'Term', 'Force'))]
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

    # The fingerprint's membership has two sources -- FINGERPRINT_TABLES
    # here, and README's rule that the Results table's bolded rows are in
    # it -- so this holds them together: every bolded Results row is a
    # fingerprint arm, and every fingerprint arm is rostered. The rule's
    # open-question half (`mut-odo`, `build` today) cannot be read
    # mechanically, so an extra fingerprint arm is fine; a bolded row left
    # out is not.
    #
    # Non-vacuity: against a scratch README with `offtab`'s row bolded it
    # fails naming offtab; against a scratch Main.hs whose roster drops
    # ("build", ...) it fails naming build, beside the rostered check
    # losing fbBuild.
    fp_arms = {a for _, _, arms in FINGERPRINT_TABLES for a in arms}
    bolded = [st for st, (_, style, _) in
              readme_rows(readme, names).items() if style == 'bold']
    off = ([b for b in bolded if b not in fp_arms]
           + ['%s (not rostered)' % a for a in sorted(fp_arms)
              if a not in names])
    if off:
        bad.append('fingerprint membership drifted: %s' % ', '.join(off))
    else:
        print('ok:   every bolded Results row is among the %d fingerprint'
              ' arms (%d bolded), and every fingerprint arm is rostered'
              % (len(fp_arms), len(bolded)))

    # The l annotations, statically: each entry's leading trailing-comment
    # number must equal what its list's rule computes, so a mistyped shape
    # or annotation is caught at edit time -- the oracle used to be
    # run-gated, firing in --selftest only for the shapes a JSON happened
    # to hold, which for a class list meant after its process had run.
    # An entry without an annotation is counted rather than failed: the
    # annotation is the oracle, not a requirement, and the count is what
    # keeps an absence visible.
    dims, ann = dims_by_shape(main_hs)
    wrong = [(sh, ann[sh], dims[sh]['l']) for sh in ann
             if dims[sh]['l'] != ann[sh]]
    if wrong:
        bad.append('l annotation(s) disagreeing with their list\'s rule: %s'
                   % '; '.join('%s annotated %d where the rule gives %d'
                               % w for w in wrong))
    else:
        print('ok:   every l annotation matches its list\'s rule (%d of %d'
              ' entries annotated)' % (len(ann), len(dims)))

    # Probe.hs is a separate program with copies of six of Main.hs's shapes,
    # so that all four of its element types run transcribed code rather than
    # three copies against one original. The copy is what this checks: a dim
    # that stopped matching would leave the probe measuring a shape it still
    # names after. Its base-offsets build is deliberately NOT checked -- see
    # that file's header on why its figures are its own.
    #
    # Non-vacuity: it was written from a wrong copy and caught it. Three of
    # the six were transposed or re-ranked on first writing
    # (cnn-slice-c32, stretch-inner1, stretch-tall-Mx2) and this named all
    # three; restoring one wrong dim fails it again with both shapes printed.
    probe = os.path.join(os.path.dirname(os.path.abspath(main_hs)), 'Probe.hs')
    try:
        ptext = open(probe).read()
    except OSError:
        # Printed directly, as lint's notes are. This branch appended to a
        # list no code defined -- a NameError from its birth -- until a
        # scratch --main run first reached it during Run 7's write-up: the
        # one lint branch the real directory can never fire, and the
        # silent-search rule caught up with it.
        print('note: no Probe.hs beside Main.hs, so its shape copies are'
              ' unchecked')
    else:
        entry = re.compile(r'^\s*[\[,] \("([^"]+)",\s*(\[[^\]]*\])\)', re.M)
        block = ptext[ptext.index('probeShapes ='):] if 'probeShapes =' \
            in ptext else ''
        pshapes = {n: [int(d) for d in re.findall(r'\d+', ds)]
                   for n, ds in entry.findall(block.split('\n  ]')[0])}
        mine = dims_by_shape(main_hs)[0]
        if not pshapes:
            bad.append('Probe.hs defines no probeShapes, so the shape-copy'
                       ' check read nothing')
        else:
            off = ['%s %s in Probe.hs against %s in Main.hs'
                   % (n, ds, mine[n]['dims']) for n, ds in pshapes.items()
                   if n not in mine or mine[n]['dims'] != ds]
            if off:
                bad.append('%d probe shape(s) disagreeing with Main.hs: %s'
                           % (len(off), '; '.join(off)))
            else:
                print('ok:   all %d Probe.hs shapes match Main.hs\'s own dims'
                      % len(pshapes))

    # This named `concat-runs` alone until the two rulings
    # (README.md#what-the-benchmark-does) made the not-timed set the larger
    # half of the strategies. So it reports the split rather than only the
    # names, and wraps them: a note that runs off the line is one nobody
    # reads, and which arms are checked-but-untimed is the one thing about
    # the roster no run's output shows.
    only = [n for n, r, _ in roster if r == 'Only']
    if only:
        print('note: %d of the %d roster arms are rostered and checked but'
              ' deliberately not' % (len(only), len(names)))
        print('      timed, each with the reason at its entry:')
        # Not at hyphens: every one of these names carries them, and a name
        # split across two lines is one no grep of this output can find.
        for line in textwrap.wrap(', '.join(only), 66,
                                  break_on_hyphens=False,
                                  break_long_words=False):
            print('        ' + line)
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

    Non-vacuity of the two correction checks, confirmed by breaking them:
    inflating the forcing term 50x fails the positivity one on 1353 cells and
    takes the winsorizing check down with it; tightening the scaling
    tolerance to
    1.01 fails the scaling one and names the two shapes it compared; and
    excluding both `sum-only` arms turns the first into a named skip rather
    than a silent pass, as a one-shape run does to the second.

    The population check likewise: concatenating a one-shape main run's
    reports with a one-shape window-class run's failed it, naming both
    populations, while every other invariant on that file passed -- which
    is what the check is for, a merged run looking healthy from every
    other angle. --markdown refused the same file. A cheaper provocation
    than concatenating anything, since a recipe nobody will run is worth
    little: `classes rev-primes bcast-inner8` selects across two class lists
    in one process and the reader names both.

    The baseline identity likewise, the last check here to have gone unproven
    (2026-08-09): dividing the corrected numerator by the UNcorrected
    baseline -- `list`'s slope where its net belongs, which is the mistake the
    identity exists to catch -- makes `list` against itself read 0.9688 and
    fails, where the intact reader on the same file says exactly 1. It needs
    two shapes to run at all: on one, this whole block is skipped along with
    winsorizing and the A/A identity, so a one-shape smoke exercises none of
    the three.
    """
    ok, bad, skip = [], [], []

    known = [sh for sh in shapes if sh in meta['dims']]
    if not known:
        skip.append('no shape of this run is defined in Main.hs, so the'
                    ' shape parse is unexercised (renamed since the run?)')
    else:
        checked = 0
        for sh in known:
            d = meta['dims'][sh]
            want = meta['ann'].get(sh)
            if want is None:
                continue
            checked += 1
            if d['l'] != want:
                bad.append('%s %s: parsed l=%d against Main.hs\'s own'
                           ' annotation %d'
                           % (sh, d['dims'], d['l'], want))
        if checked and not bad:
            # `bad` holds only this check's mismatches here: it is the
            # first check run, so an "each matching" claim beside a FAIL
            # naming a mismatch cannot both print, as they once did.
            ok.append('shape parse: %d of %d shapes found in Main.hs, %d with'
                      ' an l annotation, each matching the dims parsed'
                      % (len(known), len(shapes), checked))
        else:
            skip.append('no shape in Main.hs carries an l annotation, so the'
                        ' dims parse has no oracle here')
        skip.append('sInner comes from a per-list reading of the generator'
                    ' (see dims_by_shape), which no JSON carries and so'
                    ' nothing here can confirm: m and alloc inherit it.'
                    ' `micro -- check` asserts each class\'s structure'
                    ' against the actual view, which is where it CAN be'
                    ' confirmed')

    # One population per file. Every aggregate below is a geomean over
    # whatever shapes the file holds, so a merged run publishes figures
    # belonging to no population at all.
    kind, label = population_of(shapes, meta['dims'])
    if kind == 'mixed':
        bad.append('this run spans %s, and one JSON holds one population:'
                   ' a geomean over two of them is a statistic of neither'
                   ' (README.md#making-a-major-benchmark-run)' % label)
    elif kind == 'unknown':
        skip.append('Main.hs defines none of this run\'s shapes, so which'
                    ' population it measured cannot be checked here')
    else:
        ok.append('population: every shape of this run is %s' % label)

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

    halves = [st for st in strategies if st.startswith('sum-only')]
    if not halves:
        skip.append('no `sum-only` bench in this run, so the correction is'
                    ' zero and the time column uncorrected -- untested here')
    else:
        term_bad = [sh for sh in shapes
                    if not 0 < cells[sh][halves[0]]['slope']]
        sunk = [(sh, st) for sh in shapes for st in strategies
                if st not in halves and not st.endswith('-nosum')
                and cells[sh][st]['net'] <= 0]
        if term_bad or sunk:
            bad.append('correction: %d shape(s) with a non-positive forcing'
                       ' term and %d cell(s) it did not leave positive'
                       % (len(term_bad), len(sunk)))
        else:
            ok.append('correction: the forcing term is positive on all %d'
                      ' shape(s) and leaves every cell\'s net positive, from'
                      ' %d half/halves' % (len(shapes), len(halves)))

        # The term is subtracted per shape, so it must be the SAME pass on
        # every shape -- one sum over l elements. If it were not, both halves
        # would be wrong together and their agreement would not notice: that
        # test fixes the term's dependence on position, this one its
        # dependence on size, and the correction needs both.
        known = [sh for sh in shapes if sh in meta['dims']]
        per = [(stats.fmean([cells[sh][h]['slope'] for h in halves])
                / meta['dims'][sh]['l'], sh) for sh in known
               if meta['dims'][sh]['l']]
        if len(per) < 2:
            skip.append('fewer than two shapes with known dims, so the'
                        ' forcing term\'s scaling with l is unexercised')
        else:
            lo, hi_ = min(per), max(per)
            spread = hi_[0] / lo[0]
            # 1.5x is loose enough for cache effects across a 6000x range of
            # l (Run 6 (-O1) spans 1.04x) and tight enough that a term
            # measuring a different quantity on some shape cannot pass.
            if spread > 1.5:
                bad.append('correction: the forcing term is %.2fx as costly'
                           ' per element on %s as on %s, so it is not one'
                           ' pass over l elements and subtracting it per'
                           ' shape is unsound'
                           % (spread, hi_[1], lo[1]))
            else:
                ok.append('correction: the forcing term is %.3f-%.3f ns per'
                          ' element over %d shape(s), a %.2fx spread, so it'
                          ' scales with l as one pass must'
                          % (lo[0] * 1e9, hi_[0] * 1e9, len(per), spread))

    if len(shapes) < 2:
        skip.append('one shape only, so the winsorizing and the A/A identity'
                    ' below are unexercised')
    elif any('list' not in cells[sh] for sh in shapes):
        # A filtered run that leaves the baseline out has no ratios to check.
        # Saying so beats the KeyError this used to raise: the docstring
        # promises this reader is useful on a partial run, and a four-bench
        # gate is exactly that.
        ok.append('winsorizing: not checked, the run carries no `list` to'
                  ' divide by -- add `*/list` to the selection to exercise it')
    else:
        capped = 0
        for st in strategies:
            # The arms `time_of` declines to give a figure for: correcting
            # them is meaningless, so there is no geomean to bracket.
            if st.startswith('sum-only') or st.endswith('-nosum'):
                continue
            ratios = [cells[sh][st]['net'] / cells[sh]['list']['net']
                      for sh in shapes]
            capped += winsorize([math.log(r) for r in ratios])[1]
            got = time_of(cells, shapes, st)
            if not min(ratios) - TOL <= got <= max(ratios) + TOL:
                bad.append('%s: winsorized geomean %.6g outside the per-shape'
                           ' range %.6g..%.6g' % (st, got, min(ratios),
                                                  max(ratios)))
        ok.append('winsorizing: every row covers all %d shapes and its geomean'
                  ' lands inside its own per-shape range (%d cell(s) capped'
                  ' in all)' % (len(shapes), capped))

        if 'list' in strategies:
            one = time_of(cells, shapes, 'list')
            if abs(one - 1.0) > TOL:
                bad.append('list against itself is %.12g, want 1' % one)
            else:
                ok.append('baseline: list against itself is exactly 1')

        # With nothing dropped, a published ratio is the paired one WHENEVER
        # neither arm had a cell capped -- the geomeans then divide term by
        # term. A capped cell is capped against its own row's median, so a
        # pair where one arm was capped may legitimately differ.
        pairs = [(a, twin_of(a)) for a in strategies
                 if twin_of(a) in strategies]
        clean = []
        for a, b in pairs:
            na = winsorize([math.log(cells[sh][a]['net']
                                     / cells[sh]['list']['net'])
                            for sh in shapes])[1]
            nb = winsorize([math.log(cells[sh][b]['net']
                                     / cells[sh]['list']['net'])
                            for sh in shapes])[1]
            (clean if na == nb == 0 else None) is None or clean.append((a, b))
        if not clean:
            skip.append('every control pair had a cell capped, so the'
                        ' published-equals-paired identity is unexercised'
                        ' (%d pair(s) present)' % len(pairs))
        for a, b in clean:
            published = time_of(cells, shapes, a) / time_of(cells, shapes, b)
            paired = geomean([cells[sh][a]['net'] / cells[sh][b]['net']
                              for sh in shapes])
            if abs(published - paired) > 1e-6 * paired:
                bad.append('%s/%s uncapped yet published %.6f != paired %.6f'
                           % (a, b, published, paired))
            else:
                ok.append('A/A identity: %s/%s uncapped, so published =='
                          ' paired (%.4f)' % (a, b, published))

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
                   ' (not needed by --lint or --check-doc)')
    p.add_argument('--main', default=os.path.join(here, 'Main.hs'),
                   help='Main.hs to read shape sizes from'
                        ' (default: alongside)')
    p.add_argument('--shapes', action='store_true')
    p.add_argument('--aa', action='store_true')
    p.add_argument('--cells', action='store_true')
    p.add_argument('--steps', action='store_true')
    p.add_argument('--pair', nargs=2, action='append', default=[],
                   metavar=('A', 'B'))
    p.add_argument('--compare', metavar='OTHER.json',
                   help='this run against another of the same population,'
                        ' one arm at a time')
    p.add_argument('--chapter', action='store_true',
                   help='with --compare: the run chapter\'s mechanical'
                        ' figures, as --block does for a class')
    p.add_argument('--claims', action='store_true',
                   help='every claim ordering and its registered verdict'
                        " in one call, in the claims section's order")
    p.add_argument('--alloc', action='store_true',
                   help='with --compare: allocation agreement instead of'
                        ' times, on the multiple the alloc column publishes')
    p.add_argument('--markdown', action='store_true')
    p.add_argument('--fingerprint', action='store_true')
    p.add_argument('--block', action='store_true')
    # The standing explanations and the installed table are read once and
    # then reprinted on every later call: ten populations of --aa is ~250
    # lines of prose a session has already read, and --block's table is
    # thrown away because --in-place installs it. --brief drops both. It
    # drops nothing computed -- every figure still prints.
    p.add_argument('--brief', action='store_true')
    p.add_argument('--in-place', action='store_true',
                   help='install --markdown/--fingerprint/--block tables into'
                        ' README instead of printing them')
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--lint', action='store_true')
    p.add_argument('--check-doc', action='store_true')
    p.add_argument('--para', metavar='PATTERN',
                   help="print README paragraphs whose bolded lead matches,"
                        " with the line each starts at; needs no run file")
    p.add_argument('--readme', default=os.path.join(here, 'README.md'),
                   help='README.md to check bench names against'
                        ' (default: alongside)')
    p.add_argument('--no-controls', action='store_true')
    p.add_argument('--exclude', action='append', default=[],
                   metavar='STRATEGY')
    p.add_argument('--exclude-shape', action='append', default=[],
                   metavar='SHAPE')
    args = p.parse_args()

    if args.para:
        sys.exit(paragraphs(args.readme, args.para))
    if args.check_doc:
        sys.exit(check_doc(args.readme, args.main))
    if args.lint:
        sys.exit(lint(args.main, args.readme))
    if args.run is None:
        p.error('a run file is required for everything but --lint and'
                ' --check-doc')
    if not os.path.exists(args.run):
        sys.stderr.write('%s: no such run file; the analysis did not happen\n'
                         % args.run)
        sys.exit(2)
    cells, shapes, strategies, meta = load(args.run, args.main)
    shapes = [s for s in shapes if s not in args.exclude_shape]
    strategies = [s for s in strategies if s not in args.exclude]
    # Before --no-controls, so that omitting the controls from the aggregates
    # cannot change what the published column means.
    terms = apply_correction(cells, shapes, strategies)
    if args.no_controls:
        strategies = [s for s in strategies if not is_control(s)]
    if not shapes or not strategies:
        sys.exit('nothing left after --exclude')

    if args.selftest:
        sys.exit(selftest(cells, shapes, strategies, meta))
    if args.compare and not os.path.exists(args.compare):
        sys.stderr.write('%s: no such run file; the comparison did not'
                         ' happen\n' % args.compare)
        sys.exit(2)
    roster = ('%d benchmarks over %d shape%s of %s'
              % (meta['benches'], meta['shapes'],
                 '' if meta['shapes'] == 1 else 's',
                 population_of(shapes, meta['dims'])[1]))
    if (len(strategies), len(shapes)) != (meta['benches'], meta['shapes']):
        roster += ('; reading %d of them over %d shape%s'
                   % (len(strategies), len(shapes),
                      '' if len(shapes) == 1 else 's'))
    print('%s: criterion %s, %d reports = %s%s%s'
          % (os.path.basename(args.run), meta['version'], meta['reports'],
             roster,
             '  (RAGGED: some cells missing)' if meta['ragged'] else '',
             '' if len(shapes) > 1 else '  (one shape: nothing to spread)'))
    print()
    health(cells, shapes, strategies, terms)
    if args.shapes:
        shape_table(cells, shapes, strategies, meta)
    elif args.aa:
        aa_table(cells, shapes, strategies, terms, meta, args.brief)
    elif args.pair:
        pair_table(cells, shapes, strategies, args.pair)
    elif args.claims:
        claims_table(cells, shapes, strategies, args)
    elif args.compare and args.chapter:
        chapter_skeleton(cells, shapes, strategies, meta,
                         args.compare, args.main)
    elif args.compare and args.alloc:
        compare_alloc(cells, shapes, strategies, meta, args.compare,
                      args.main)
    elif args.compare:
        compare_table(cells, shapes, strategies, meta, args.compare,
                      args.main)
    elif args.steps:
        step_table(args.run, cells, shapes, strategies, meta)
    elif args.cells:
        cell_dump(cells, shapes, strategies)
    elif args.markdown:
        text = capture(markdown_table, cells, shapes, strategies, meta,
                       args, terms)
        emit_or_install(text, args, shapes, meta)
    elif args.fingerprint:
        text = capture(fingerprint_table, cells, shapes, strategies, meta)
        emit_or_install(text, args, shapes, meta)
    elif args.block:
        text = capture(block_skeleton, cells, shapes, strategies, meta,
                       args, terms)
        emit_or_install(text, args, shapes, meta, block=True)
    else:
        strategy_table(cells, shapes, strategies, meta, args, terms)


if __name__ == '__main__':
    main()
