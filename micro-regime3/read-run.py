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
          decision and the caveat the halves do not settle. `--corr=insitu`
          takes the term from the `-nosum` pairs instead, which is a second
          convention and not a refinement of this one: it is for a build
          where this term cannot be subtracted at all, and its column is
          comparable to no figure in README.
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

The field criterion documents nowhere near to hand: `reportMeasured` is the
raw sample list, each sample itself a LIST whose [0] is the time and [3] the
iteration count. It is the way in to anything the fitted slope hides -- a
warm-up ramp, a lone outlying sample -- where --cells reports only how many
samples there were. **This script does read it**, in `step_scan` and so
under --steps and --block, which is what makes the array shape load-bearing
rather than a note: the paragraph here said the field was unread until
2026-08-16, and a stub written to that description -- samples with a length
and no contents -- got a `KeyError: 3` out of --block instead of an answer.

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
  --compare O --bridge  each arm as a ratio to `list` IN ITS OWN RUN, per
                    shape, which cancels a box change exactly where the
                    plain --compare reads absolutes and cannot
  --compare O --ci  each arm's CI% median against the other run's -- the
                    statistic the column publishes, and not the mean a
                    script over --cells reaches for
  --compare O --chapter the run chapter's own arithmetic, so that writing
                    one need not begin by reading the last one
  --claims          every claim ordering and its registered verdict in one
                    call, in the claims section's order, from a manifest
                    --lint holds to the roster
  --steps           every cell read at sample level for a mid-bench change
                    of level, which the fitted slope averages away and no
                    other column here can show
  --deflation       this run's `list` over its own alone legs, per shape:
                    the in-process deflation the riders exist to measure,
                    RAW over RAW because a leg carries no `sum-only` to
                    correct with. Legs found from this run's own name,
                    and where a SATURATED set is beside the clean one the
                    total is split as well -- the state a preamble puts
                    on a clean process, and the rest the roster adds
  --wild            the per-sample instrument's own LOG rather than a JSON:
                    each bench's `pre`/`post` pair differenced, and, where
                    the stamp carries the load fields, the CPU SOMETHING
                    ELSE consumed during each sample -- which is what tells
                    a wild cell from an external intrusion
  --machine         this run's `list` absolutes against the fingerprint
                    README keeps, which is the one check that asks whether
                    the BOX changed rather than the code; exits nonzero
                    when the whole baseline moved
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
  --corr=insitu     subtract the `-nosum` pairs' in-situ term in place of
                    `sum-only`, for a build where `sum-only` cannot be
                    subtracted at all -- an LLVM one, where it runs larger
                    than the bench. Says so on stderr every time, that
                    column being comparable to no figure in README
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

**--selftest is the numeric half of that and `./check-scripts.py` is the
other, which is where a defect of THIS FILE now goes.** Every invariant
above is about a run's figures, and two reviews on 2026-08-17 found thirty
defects that were not: a class table installed over the next class's, four
checks whose silence read as a pass, a mode dropped by the dispatch without
a word, a subprocess status ignored. --selftest calls no checker, no
installer and no flag guard, so it caught none of them and cannot. The
corpus drives this script from outside instead -- exit code and stderr
included -- and replays each case against the commit before its own fix,
which is what keeps it non-vacuous and what makes a fix's proof outlive the
commit that made it. **Add the case before the fix**; a defect fixed
without one has come back here twice already. Extending this script rather
than writing a new one still holds for anything that READS a run: the
corpus reads none, and is the exception the rule needed.
"""

import argparse
import collections
import contextlib
import difflib
import functools
import glob
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
    return 'the %s class' % class_prefix(members)


def class_prefix(members):
    """The prefix a class's shapes share.

    What `classes rev-` selects on and what a block's bolded lead is
    written with, so `emit_or_install` wanted it and got it by undoing
    the label above -- `label.replace('the ', '').replace(' class', '')`,
    a rule known in one place as itself and in another as its inverse.
    """
    return '/'.join(sorted({sh.split('-')[0] for sh in members}))


POP = collections.namedtuple('POP', 'kind label prefix')


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
        return POP('unknown', 'a population Main.hs does not define', '')
    named = sorted('the main set' if k == 'main' else class_label(v)
                   for k, v in groups.items())
    if len(groups) > 1:
        return POP('mixed', ' + '.join(named), '')
    one = next(iter(groups.values()))
    return POP('main' if 'main' in groups else 'class', named[0],
               '' if 'main' in groups else class_prefix(one))


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
        # A slope of exactly 0 divided here, in every mode, before the
        # malformed-cell check in `selftest` that exists to name that cell
        # could run -- the sunk-baseline defect one stage earlier, on the
        # slope rather than on the net. A cell with no slope has no CI
        # either. Found 2026-08-22 by review.
        if not slope:
            lo = hi = None
        alloc = fits.get('allocated')
        alloc_b = alloc['regCoeffs']['iters']['estPoint'] if alloc else None
        l = ell.get(shape)
        cells[shape][strategy] = dict(
            slope=slope, r2=fits['time']['regRSquare']['estPoint'],
            n=len(r['reportMeasured']),
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
    # Parsed once and carried, two callers having read Main.hs for it with
    # a fallback apiece and a local of the same name meaning different
    # things -- a count of the timed arms here, the set of every arm in
    # `markdown_table`.
    try:
        roster = roster_of(open(main_hs).read())
    except OSError:
        roster = []
    meta = dict(version=raw[1], reports=len(raw[2]), path=path,
                roster=roster,
                rostered=len([n for n, r, _ in roster if r != 'Only']),
                benches=len(strategies), shapes=len(shapes), dims=dims,
                ann=ann,
                ragged=len(raw[2]) != len(shapes) * len(strategies),
                known_l=sum(1 for s in shapes if s in ell))
    return cells, shapes, strategies, meta


def apply_correction(cells, shapes, strategies, mode='sumonly'):
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

    `mode='insitu'` subtracts the term the `-nosum` arms measure instead --
    an arm minus its twin, the sum as it runs over the vector the fill has
    just written, meaned over whichever pairs the run carries. That is gate
    3's own quantity (README.md#sum-only-and-the-correction-now-applied),
    promoted from auditing the correction to being it, and it is NOT the
    published convention: a figure read this way is comparable to no figure
    on that README, which is why it is a flag and not a fallback. What it is
    for is a build where `sum-only` cannot be subtracted at all -- under
    GHC HEAD's LLVM backend that bench runs up to 2.3x the bench it would be
    subtracted from, leaving a usable net on 3 of the 24 main-set shapes.
    Its own cost is that the term stops being
    one quantity: Run 16's three `-nosum` pairs disagree per shape by a
    median 1.06x and by 1.76x on `stretch-inner256`, where the two
    `sum-only` halves agree at 1.0001.

    Non-vacuity, both ways, on `run16-a32m-main.json`: the two modes differ
    on every row, by a median -0.74% and a worst -2.48% on `build`, with no
    ordering changed anywhere in the table; and one LLVM shape's leg reports
    7 sunk cells under the default and none under this. Emptying the
    `base_of` branch leaves the term zero and the column uncorrected, which
    `health` then reports, so it cannot pass by doing nothing.
    """
    terms = {}
    for sh in shapes:
        if mode == 'insitu':
            pairs = [cells[sh][base_of(st)]['slope'] - cells[sh][st]['slope']
                     for st in strategies
                     if base_of(st) and st in cells[sh]
                     and base_of(st) in cells[sh]]
        else:
            pairs = [cells[sh][st]['slope'] for st in strategies
                     if st.startswith('sum-only') and st in cells[sh]]
        terms[sh] = stats.fmean(pairs) if pairs else 0.0
    for sh in shapes:
        for st in cells[sh]:
            cells[sh][st]['net'] = cells[sh][st]['slope'] - terms[sh]
    return terms


def health(cells, shapes, strategies, terms, corr='sumonly'):
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
    meaningless. And under `--corr=insitu` the convention itself is
    reported, every time and not only when something is wrong, because that
    column looks exactly like the published one and is comparable to nothing
    in it.

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
            # `alloc` is None for a shape Main.hs no longer defines, `l`
            # being what turns bytes into the multiple -- and `or 0` then
            # read that as "allocated nothing" and skipped the warning
            # entirely, so an older JSON went quiet here while `--cells`
            # still printed its `alloc_bytes`. Unknown is not small: warn
            # and let the reader look. Found 2026-08-17 by review.
            if (c.get('alloc_r2') is not None and c['alloc_r2'] < 0.99
                    and (c['alloc'] is None or c['alloc'] >= 0.1)):
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
        out.append('no %s bench in this run, so the time column is'
                   ' UNCORRECTED and not comparable to a full run\'s'
                   % ('`-nosum` pair' if corr == 'insitu' else '`sum-only`'))
    elif corr == 'insitu':
        out.append('the correction is the in-situ term from the `-nosum`'
                   ' pairs, NOT the published `sum-only` one, so this'
                   ' column is comparable to no figure in README.md')
    else:
        # A `-nosum` arm is exempt with `sum-only`, and for the mirror-image
        # reason: it is the one kind of arm that never ran the forcing pass,
        # so on a fast fill its whole cost can legitimately fall below the
        # term, and subtracting one from the other was never meaningful.
        sunk = [(cells[sh][st]['net'], sh, st) for sh in shapes
                for st in strategies
                if not no_net(st)
                and cells[sh][st]['net'] <= 0]
        if sunk:
            n, sh, st = min(sunk)
            out.append('%d cell(s) whose forcing term is not smaller than the'
                       ' cell itself, worst %s/%s -- their ratios are not'
                       ' readable' % (len(sunk), sh, st))
    for line in out:
        sys.stderr.write('warning: ' + line + '\n')


AA = collections.namedtuple('AA', 'a b r g worst ci')


def aa_pairs(cells, shapes, strategies):
    """[(arm, twin, ratios, geomean, worst cell, interval)] for the A/A set.

    Three callers share it -- the controls paragraph, the chapter (once
    per half) and the summary row's floor -- each having written the same
    three lines and two of them the floor besides, which `aa_floor` below
    is, once. `--aa` keeps its own loop deliberately: it compares the
    `sum-only` pair too, on `slope` rather than `net`, and it needs the
    roster index for its span column, so folding it in would mean a
    parameter for each and a helper serving nobody plainly.

    `worst` is (deviation in %, shape), the largest cell, and the pairs
    come back in `strategies` order, which is what the printed tables
    walk. The `sum-only` pair is not here: it is compared on `slope`
    rather than `net`, being the correction itself, and each caller that
    wants it keeps its own branch.
    """
    out = []
    dropped = []
    for a in strategies:
        b = twin_of(a)
        if not b or b not in strategies:
            continue
        # Not readable rather than divided: on a file `--claims` refuses
        # outright, `--aa` used to die inside `geomean` with `math domain
        # error`, and `--block`, `--compare --chapter` and `summary_row` all
        # come through here. The guard `pair_stats` grew was never carried
        # to its siblings. Found 2026-08-17 by review.
        #
        # And SAID, on the same day, because dropping it quietly traded a
        # crash for the worse thing: `controls_skeleton` publishes "N of M
        # intervals cover 1" into the README off this list, and over a run
        # with eighteen pairs and two of them sunk it read 16 with nothing
        # anywhere saying which two had gone. The warning is here rather
        # than at each caller so that every one of them inherits it, and
        # `install-tables.sh` gathers it into the hand-work a run owes.
        if any(cells[s][x]['net'] <= 0 for s in shapes for x in (a, b)):
            dropped.append('%s/%s' % (a, b))
            continue
        r = [cells[s][a]['net'] / cells[s][b]['net'] for s in shapes]
        dev = [abs(x - 1) * 100 for x in r]
        out.append(AA(a, b, r, geomean(r), max(zip(dev, shapes)),
                      paired_ci(r)))
    if dropped:
        sys.stderr.write('warning: %d control pair(s) not readable, a cell'
                         ' having no positive net: %s -- every A/A figure'
                         ' below is over the rest\n'
                         % (len(dropped), ', '.join(dropped)))
    return out


CARRY_BACK = ('mut-odo-vecdims', 'bq-expand', 'bq-scan-rem-gm-mulback')
"""The three arms whose A/A twins predate the twelve added after Run 13.

Six pairs, both positions of each, and they are the only ones a floor can
be compared across runs on: everything else in the eighteen arrived later,
so a run-to-run reading of the eighteen-pair figure is over two different
populations. README calls this the six-pair figure and holds it to two
sites; before Run 17 it was derived by hand at the write-up, which is
where it was first quoted three ways.
"""

ANCHORS = ('cnn-slice-c32', 'cifar-L2-16-c64-k3', 'stretch-wide-2xM')
"""The three shapes README keeps `list`'s absolute per call for.

They guard the baseline the way the fingerprint guards it per shape, and
they are what says the box has not moved under a run. Kept here so the
chapter skeleton emits them rather than leaving a session to look them up
and quote them from the wrong half.
"""


def aa_floor(pairs):
    """The pair furthest from 1, which is what this README calls the floor."""
    return max(pairs, key=lambda p: abs(p.g - 1)) if pairs else None


def insitu_ratios(cells, shapes, strategies):
    """[(base, arm, ratios)]: the forcing term read in situ, per Force arm.

    `gap / term` per shape, where the gap is what the arm's own base
    loses by forcing and the term is what `sum-only` says forcing costs.
    Two callers computed it identically -- and built the pair list in
    opposite orders, `(base, arm)` in one and `(arm, base)` in the other,
    which is a trap rather than a style: swap the two names and the ratio
    inverts, silently and plausibly.
    """
    out = []
    for arm in strategies:
        base = base_of(arm)
        if base not in strategies:
            continue
        # The shapes come back WITH the ratios, because a shape whose gap
        # or term is not positive is dropped here and the caller labelled
        # its worst cell by zipping the ratios against `shapes` -- so one
        # dropped shape renamed every later ratio with its predecessor's
        # shape, and `--aa` printed a worst cell on a shape that did not
        # produce it. Found 2026-08-17 by review.
        r, at = [], []
        for s in shapes:
            gap = cells[s][base]['slope'] - cells[s][arm]['slope']
            term = cells[s][base]['slope'] - cells[s][base]['net']
            if gap > 0 and term > 0:
                r.append(gap / term)
                at.append(s)
        if r:
            out.append((base, arm, r, at))
    return out


def no_net(name):
    """Has this arm no corrected time? It never ran the forcing pass.

    Named because it was spelled out at eight sites and two of them did
    not spell it alike -- `health` wrote the two halves as separate `not`
    clauses and `selftest` tested membership of its own `sum-only` list --
    so a third control class, or a renamed suffix, had to be found in
    eight places by a grep that missed two of them. Not `is_control`,
    which is the WIDER set: it counts the `-aa` twins, which do have a
    corrected time and are only excluded from the published column.
    """
    return name.startswith('sum-only') or name.endswith('-nosum')


def is_control(name):
    return '-aa' in name or no_net(name)


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

    Reads `--` on exactly what `time_of` reads `--` on, the sunk cell
    included: without that last test a shape whose forcing term was not
    smaller than the cell published a plausible `worst` beside a `time --`
    in the same README row, computed over a shape set one of whose cells
    means nothing. Found 2026-08-17 by review; no run here carries such a
    cell, so no published figure moves -- which is also why the proof had
    to be made: with one cell's slope cut to a hundredth in a copy of Run
    14's slice JSON, `mut-odo-vecdims` reads `-- --` here and `-- 0.063`
    through the version before this.
    """
    if any('list' not in cells[s] for s in shapes):
        return float('nan')
    if no_net(strategy):
        return float('nan')
    if any(cells[s][strategy]['net'] <= 0 or cells[s]['list']['net'] <= 0
           for s in shapes):
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
    if no_net(strategy):
        return float('nan')
    if any('list' not in cells[s] for s in shapes):
        return float('nan')
    if any(cells[s][strategy]['net'] <= 0 or cells[s]['list']['net'] <= 0
           for s in shapes):
        return float('nan')
    logs = [math.log(cells[s][strategy]['net'] / cells[s]['list']['net'])
            for s in shapes]
    return math.exp(stats.fmean(winsorize(logs)[0]))


ROW = collections.namedtuple('ROW', 'time st ci noise smp alloc worst')


def strategy_rows(cells, shapes, strategies):
    """The table's rows, sorted: (time, name, CI%, noise, smp, alloc, worst).

    A namedtuple because the printed order is not the tuple order --
    `worst` is the second column on screen and the last field here -- so
    the four sites that read a row positionally were reading `r[6]` for
    it. Unpacking and indexing both still work, which is why no caller
    that iterates the row had to change.

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
        # `time_of` and `worst_of` return nan on a run with no `list`
        # themselves, by the same test `have_list` is, so neither wants a
        # ternary here.
        rows.append(ROW(time_of(cells, shapes, st), st, med_or_nan(ci), noise,
                        stats.median(cells[s][st]['n'] for s in shapes),
                        stats.median(alloc) if alloc else None,
                        worst_of(cells, shapes, st)))
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
        # A cell with no positive slope has no share to read, and divided
        # here in the default mode -- the zero-slope family's last site,
        # the selftest's having been named the day before. Found
        # 2026-08-23 by a sweep for the family.
        share = {st: med_or_nan([terms[sh] / cells[sh][st]['slope']
                                 for sh in shapes if st in cells[sh]
                                 and cells[sh][st]['slope'] > 0])
                 for st in ('list', FIX)}
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


# The two headers `--markdown` emits, and the one `readme_rows` finds the
# Results table by. One literal, so that the emitter and the reader of the
# same table cannot drift apart -- which is a way for the carry-forward to
# stop finding anything and report every row as new.
CLASS_HDR = '| strategy | time | worst | CI% | smp | alloc |'
RESULTS_HDR = '| strategy | time | worst | CI% | smp | alloc | needs |'


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
    read from the Results table alone -- located by its own header line, as
    `install` locates it, and ended at the first line that is not a row.
    The name filter stays as the second guard, against the separator row and
    against a name the roster does not hold.

    **The name filter does not do that job alone, and it used to be asked
    to.** A toy run on 2026-08-16 refuted the claim that stood here: the
    loop-offsets table is seven columns wide too and its first column is
    rostered arm names, so its rows were read as Results rows. Two things
    followed, and the second is why this is anchored rather than filtered
    harder. The departed-row warning named six arms that were not in the
    Results table at all, on a run carrying part of the roster. And `needs`
    was last-writer-wins over the whole README: a seven-column row planted
    for `bq-expand` BELOW the Results table put that table's last cell into
    the installed `needs`, and its emphasis with it, silently and at exit
    0. Nothing was wrong in the README only because the offsets table sits
    above the Results one.

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

    The anchoring was checked the same day, three ways: over the real README
    and Run 14's basis all 47 rows carry forward with none added or dropped
    and the copy is byte-identical; with the planted table restored below
    the Results one, `bq-expand` keeps its `needs` and its emphasis and the
    departed-row warning names the one row that really left; and a Results
    header renamed out of recognition warns that nothing was carried and
    the install refuses, where before it would have called every row new.

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
    at = [i for i, line in enumerate(text) if line == RESULTS_HDR]
    if len(at) != 1:
        sys.stderr.write('warning: %d line(s) in %s are the Results table'
                         ' header, so no `needs` cell was carried forward'
                         ' and every row will install as new\n'
                         % (len(at), os.path.basename(readme)))
        return out
    for line in text[at[0] + 1:]:
        if not line.startswith('|'):
            break
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
    line either way. Run 10 installed one and the README carried it. So the
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

    A fifth on 2026-08-17, when the block bound went in, both ways over a
    copy with `slice`'s table deleted: this refuses, naming the lead and
    its line, where the version before it installed slice's 49 rows over
    the `window` block's table and exited 0. The control against it is
    `install-tables.sh` over an untouched copy, whose eleven tables come
    back byte-identical -- a bound tight enough to refuse a real install
    would have shown up there.
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
        # Inside that block, and not merely below its lead. The eight class
        # tables share one header line, so the first hit below the lead is
        # the NEXT class's table whenever this block has none -- newly
        # written, or its table deleted mid-edit. Verified on a copy with
        # `slice`'s table removed: `--block --in-place` wrote slice's 49
        # rows over the `window` block's table and exited 0, which is the
        # silent write to the wrong place this function exists to refuse.
        # A block ends where the next lead, or the next heading, begins --
        # ANY bolded backticked lead, which is looser than either pattern
        # `install-tables.sh` picks the class blocks out with, deliberately
        # and rather than carrying a third spelling of them. What this
        # needs to know is where the block stops, so a lead it takes too
        # eagerly can only end the search early and refuse, never carry it
        # into the next block; the eleven such leads on today's README are
        # the eight class ones and three no class table sits behind.
        end = next((j for j in range(start[0] + 1, len(lines))
                    if lines[j].startswith('**`') or lines[j].startswith('#')),
                   len(lines))
        hits = [i for i in hits if start[0] < i < end]
        if not hits:
            sys.exit('--in-place: the block led by %r (%s:%d) carries no line'
                     ' equal to the header, and the next one below it belongs'
                     ' to another block; refusing to write there\n  %s'
                     % (after, os.path.basename(readme), start[0] + 1,
                        hdr[:68]))
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
    kind, label, prefix = population_of(shapes, meta['dims'])
    after = None
    if kind == 'class':
        after = '**`%s`' % prefix
    tables = tables_in(text)
    if not tables:
        sys.exit('--in-place: this mode emitted no table')
    for table in tables:
        install(args.readme, table, args.run, after)
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
    kind, label, prefix = population_of(shapes, meta['dims'])
    if kind == 'mixed':
        sys.stderr.write('refusing to emit a table for %s: one JSON at a'
                         ' time, never merged, so that a geomean is some'
                         ' population\'s -- see\n'
                         '  README.md#making-a-major-benchmark-run\n' % label)
        sys.exit(1)
    if kind == 'unknown':
        sys.stderr.write('refusing to emit a table for %s: which of README\'s'
                         ' tables these rows belong in is exactly what cannot'
                         ' be told, and --in-place has no block lead to narrow'
                         ' by, so it would install them over the main Results'
                         ' table -- a class run did, 49 rows at exit 0.\n'
                         '  Point --main at the Main.hs this run was built'
                         ' from.\n' % label)
        sys.exit(1)
    # A class table drops the editorial column but keeps the emphasis:
    # which row is the fix and which leads is what a reader looks for first,
    # and it is the same row in every population's table.
    editorial = kind != 'class'
    # Read the table by the ROSTER, not by this run's arms, so that a row the
    # run has dropped is still seen and can be reported. See `readme_rows`.
    rostered = {n for n, _, _ in meta['roster']} or set(strategies)
    prev = readme_rows(args.readme, set(strategies),
                       rostered or set(strategies))
    fresh, gone = [], [n for n in prev if n not in strategies]
    print(RESULTS_HDR if editorial else CLASS_HDR)
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

    A cell the forcing term did not leave positive is refused rather than
    divided: `time_of` and `worst_of` answer `--` for one and `--selftest`
    fails the file over it, while this divided regardless and handed
    `--pair` and `--claims` a ZeroDivisionError, or a negative ratio and
    then `math domain error` out of `geomean` -- a traceback where this
    file's convention is a refusal that says what did not happen. Found
    2026-08-17 by review.
    """
    raw = any(no_net(x) for x in (a, b))
    key = 'slope' if raw else 'net'
    sunk = [(s, x) for s in shapes for x in (a, b)
            if not cells[s][x][key] > 0]
    if sunk:
        sys.stderr.write('%s / %s: %d cell(s) with no positive %s, so this'
                         ' pair is not readable and nothing here is. The'
                         ' first: %s/%s\n'
                         % (a, b, len(sunk), key, sunk[0][0], sunk[0][1]))
        sys.exit(2)
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
    aa, so = aa_pairs(cells, shapes, strategies), None
    # The `sum-only` pair is computed HERE and again in `aa_table`, and the
    # guard against a cell with no positive figure was carried to that one
    # alone -- so a run whose forcing term came out non-positive, which
    # `health` reports and nothing stops, took `--block` down inside
    # `paired_ci` with `math domain error`. The sibling site is the way
    # every one of these has gone. Found 2026-08-17 by review of the day's
    # own fixes; said rather than skipped, since the halves' agreement is
    # a control the block publishes.
    if ('sum-only-early' in strategies and 'sum-only-late' in strategies
            and all(cells[s][h]['slope'] > 0 for s in shapes
                    for h in ('sum-only-early', 'sum-only-late'))):
        r = [cells[s]['sum-only-late']['slope']
             / cells[s]['sum-only-early']['slope'] for s in shapes]
        dev = [abs(x - 1) * 100 for x in r]
        ci = paired_ci(r)
        so = (geomean(r), max(zip(dev, shapes)),
              None if not ci else (ci[0] <= 1.0 <= ci[1]))
    if not aa:
        return
    if so is None and 'sum-only-early' in strategies:
        sys.stderr.write('warning: the `sum-only` halves are not comparable,'
                         ' a cell having no positive slope, so the Controls'
                         ' sentence below carries no reading of them\n')
    big = aa_floor(aa)
    cover = sum(1 for p in aa if p.ci and p.ci[0] <= 1.0 <= p.ci[1])
    print()
    print('**Controls:** ___ (the reading is yours). The largest A/A pair is')
    print('`%s` at %.4f, worst cell %.2f%% on `%s`,'
          % (big.a, big.g, big.worst[0], big.worst[1]))
    print('and %d of %d intervals cover 1.' % (cover, len(aa)), end=' ')
    if so:
        print('The `sum-only` halves agree at %.4f' % so[0])
        print('on a worst cell of %.2f%% on `%s`, its interval %s 1.'
              % (so[1][0], so[1][1], 'covering' if so[2] else 'missing'))
    else:
        print()
    meds = [(base, stats.median(r))
            for base, _, r, _ in insitu_ratios(cells, shapes, strategies)]
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
    b = big.b
    raw = geomean([cells[s][big.a]['slope'] / cells[s][b]['slope']
                   for s in shapes])
    fs = []
    for s in shapes:
        term = cells[s][big.a]['slope'] - cells[s][big.a]['net']
        mean = (cells[s][big.a]['slope'] + cells[s][b]['slope']) / 2
        if mean > 0:
            fs.append(term / mean)
    if fs and stats.fmean(fs) < 1:
        amp = 1 / (1 - stats.fmean(fs))
        print('Raw, that pair reads %.4f, which the correction amplifies'
              % raw)
        print('by %.2fx --- quote both wherever that is past 1.5.' % amp)


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
    b_cells, b_shapes, b_strategies = load_other(other, main_hs,
                                                 shapes, meta)
    both_sh = [s for s in shapes if s in b_shapes]
    both_st = [t for t in strategies if t in b_strategies]
    print('\nchapter skeleton, this run against %s'
          % os.path.basename(other))
    # Named and skipped, the way --compare does it: the geomeans below are
    # the chapter's headline figures, and a comparison narrowed in silence
    # is the failure this whole file is written against. This mode and
    # --alloc both computed `both_sh` and said nothing about the residue,
    # so a control half short of a shape read as a full comparison.
    missing_sh = ([s for s in shapes if s not in b_shapes]
                  + [s for s in b_shapes if s not in shapes])
    if missing_sh:
        print('  shapes in one run only, skipped: %s'
              % ', '.join(sorted(set(missing_sh))))
    if len(both_st) != len(strategies) or len(both_st) != len(b_strategies):
        print('  arms in one run only, skipped: %s'
              % ', '.join(sorted(set(strategies) ^ set(b_strategies))))
    # THE LOGS ARE READABLE AND THIS USED TO SAY THEY WERE NOT. Elapsed
    # time, the two heap peaks and the run's window are stamped by the
    # processes and by run-major.sh, so a chapter had no business asking
    # for them to be copied by hand -- Run 18 transcribed eighteen such
    # triples. What stays on the pair note is what only the note has: the
    # regime, the md5s and the commit.
    for tag, path in (('this half', meta.get('path')),
                      ('other half', other)):
        prov = provenance_line(path)
        if prov:
            print('  %s: %s' % (tag, prov))
    win = wallclock_window(meta.get('path'))
    if win:
        print('  wall-clock window: %s to %s, %d process(es)' % win)
    print('  regime, md5s and commit: ___ (from the pair note, which is the'
          ' only')
    print('  thing that has them)')
    rows = []
    for st in both_st:
        if no_net(st):
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
        aa = aa_pairs(cs, shs, sts)
        if not aa:
            continue
        big = aa_floor(aa)
        worst = max(aa, key=lambda p: p.worst[0])
        print('\n  %s half: floor %.2f%% (%s), worst A/A cell %.2f%% on %s'
              % (tag, abs(big.g - 1) * 100, big.a,
                 worst.worst[0], worst.worst[1]))
        six = [p for p in aa
               if any(p.a.startswith(b + '-aa') for b in CARRY_BACK)]
        if six:
            b6 = aa_floor(six)
            print('  %s half: six-pair figure %.2f%% (%s), over the %d pair(s)'
                  ' that carry back to Run 10'
                  % (tag, abs(b6.g - 1) * 100, b6.a, len(six)))
        anch = [(sh, cs[sh]['list']['net']) for sh in ANCHORS
                if sh in cs and 'list' in cs[sh]]
        if anch:
            print('  %s half: anchors %s'
                  % (tag, ', '.join('%s %s' % (sh, fmt_abs(t))
                                    for sh, t in anch)))
    print('\n  allocation between the halves: run --compare --alloc; the'
          ' figure belongs')
    print('  in the chapter and the trap it carries is documented there.')
    print('\nThe reading, the findings and every sentence are yours. This is'
          '\nthe arithmetic a chapter opens with, so that writing one need'
          '\nnot begin by reading the last.')


def small_ceiling(small):
    """The largest allocation among the cells that DISAGREE.

    The sentence it feeds counts the disagreeing cells and then quoted a
    maximum over all of them, agreeing ones included, so one agreeing cell
    just under the floor overstated by an order of magnitude the allocation
    whose fit it was calling unresolvable. Found 2026-08-17 by review.
    """
    return max(r[3] for r in small if r[0] > 1e-4)


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
    arithmetic on rounding, which this README forbids everywhere else.

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

    ONE MEASURED EXCEPTION to the closing rule, and Run 14's pair is it: the
    RTS nursery moves this fit on code that did not change. The same binary
    at `+RTS -A1G` reads every earnest allocator 2.3e-4 to 9.4e-4 from its
    default-nursery self, the allocated fit exact in both, where two default
    processes back to back agree to 4.9e-8 and one cell exactly -- six
    benches on run13-lookrts, 2026-08-14. So a pair varying the nursery
    reports 0 of N here and means nothing by it, and what would be a finding
    is a cell moving further than that. Why the counter reads differently
    under a large nursery is unmeasured. The closing text says this, rather
    than leaving a mode to print a rule its own pair breaks.
    """
    FLOOR = 100.0                # bytes a call, below which the fit is noise
    b_cells, b_shapes, b_strategies = load_other(other, main_hs,
                                                 shapes, meta)
    both_sh = [s for s in shapes if s in b_shapes]
    both_st = [t for t in strategies if t in b_strategies]
    print('\nallocation, this run against %s, over %d shared cell(s)'
          % (os.path.basename(other), len(both_sh) * len(both_st)))
    missing_sh = ([s for s in shapes if s not in b_shapes]
                  + [s for s in b_shapes if s not in shapes])
    if missing_sh:
        print('  shapes in one run only, skipped: %s'
              % ', '.join(sorted(set(missing_sh))))
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
              ' resolves nothing'
              % (n, small_ceiling(small)))
        print('    there; it is a property of fitting a near-zero'
              ' allocation and not of this pair')
    print('\nThe multiple the alloc column publishes is these bytes divided'
          '\nby a constant per shape, so it agrees exactly where these do and'
          '\nthere is no second column to prefer. Allocation is deterministic'
          '\nper call, so a level that moves is a code change and never a'
          '\nslot -- with one measured exception: a pair varying the RTS'
          '\nnursery moves this fit by up to 9.4e-4 on identical code, where'
          '\ntwo processes of one configuration agree to 4.9e-8. Ask what the'
          '\nhalves differ in before reading a disagreement as a code change.')


def bridge_table(cells, shapes, strategies, meta, other, main_hs,
                 band=3.3):
    """One arm across two runs, as a RATIO TO `list` rather than absolute.

    `--compare` divides one arm's net by the same arm's net in the other
    run, which is the right reading while the machine holds still and the
    wrong one the moment it does not. Run 18 met that: a BIOS idle setting
    moved between it and Run 17 and took every absolute about 4.9% with
    it, so `--compare` put `list` at +5.52% and every arm with it and said
    nothing about any arm. The bridge that run's registration 1 was
    written on had to be computed by hand, which is the shape README calls
    a defect report against this script.

    Dividing each arm by `list` IN ITS OWN RUN and only then across runs
    cancels a box term exactly, per shape, because the term multiplies
    both. What it cannot cancel is anything that moved `list` differently
    from the arms, which is the point: that residue is what a bridge is
    for.

    Both sides are corrected before the ratio is taken, as `--compare`
    does and for the same reason. `list` itself is dropped, being 1 by
    construction here, and so are the arms with no corrected time.
    """
    b_cells, b_shapes, b_strategies = load_other(other, main_hs,
                                                 shapes, meta)
    both_sh = [s for s in shapes if s in b_shapes]
    both_st = [t for t in strategies if t in b_strategies]
    # THE WHOLE MODE IS A RATIO TO `list`, so a run without it has no
    # bridge to read and gets a refusal rather than a KeyError three
    # frames down. A filtered probe is the ordinary way to have one.
    # UNREACHABLE HERE AND KEPT ANYWAY, named because a branch no control
    # exercises is a silent search: two runs of one population share
    # their shapes by construction, and two of different populations are
    # refused by `load_other` before this. It stands for a caller that
    # does not go through that check. Case:
    # `bridge-refuses-two-populations` pins the check that does fire.
    if not both_sh:
        sys.stderr.write('the two runs share no shape, so there is no'
                         ' per-shape ratio to take\n')
        return 2
    missing_list = [(w, sum('list' not in c[sh] for sh in both_sh))
                    for w, c in (('this run', cells), ('the other', b_cells))]
    missing_list = [(w, n) for w, n in missing_list if n]
    if missing_list:
        # The count, because the guard fires on ANY shared shape without
        # a `list` -- the loop below indexes every one -- while its
        # first wording claimed `every`, which a partially filtered run
        # falsifies.
        sys.stderr.write('--bridge divides every arm by `list` in its own'
                         ' run, and %s, so there is nothing to divide by\n'
                         % ' and '.join('%s carries no `list` on %d of the'
                                        ' %d shared shape(s)'
                                        % (w, n, len(both_sh))
                                        for w, n in missing_list))
        return 2
    print('\nbridge: this run / %s, each arm as a ratio to `list` in its own'
          ' run,\n  per shape, over %d shared shape(s) -- which cancels a box'
          ' term and a\n  denominator change exactly, where --compare does'
          ' not' % (os.path.basename(other), len(both_sh)))
    miss_sh = set(shapes) ^ set(b_shapes)
    if miss_sh:
        print('  shapes in one run only, skipped: %s'
              % ', '.join(sorted(miss_sh)))
    if set(strategies) ^ set(b_strategies):
        print('  arms in one run only, skipped: %s'
              % ', '.join(sorted(set(strategies) ^ set(b_strategies))))
    rows = []
    for st in both_st:
        if no_net(st) or st == 'list':
            continue
        rs = []
        for sh in both_sh:
            a, b = cells[sh][st]['net'], b_cells[sh][st]['net']
            la, lb = cells[sh]['list']['net'], b_cells[sh]['list']['net']
            if a > 0 and b > 0 and la > 0 and lb > 0:
                rs.append((a / la) / (b / lb))
        if rs:
            rows.append((geomean(rs), min(rs), max(rs), len(rs), st))
    if not rows:
        print('\n  no arm is comparable across these two runs.')
        return 2
    print('\n%-34s %8s %10s' % ('arm', 'ratio', 'range'))
    for g, lo, hi, n, st in sorted(rows):
        print('%-34s %8.4f %5.3f..%.3f' % (st, g, lo, hi))
    out = [r for r in rows if abs(r[0] - 1) > band / 100.0]
    g = geomean([r[0] for r in rows])
    print('\ngeomean over the %d arm(s) %.4f; %d outside the %.1f%% drift'
          ' band' % (len(rows), g, len(out), band))
    for gg, _, _, _, st in sorted(out, key=lambda r: -abs(r[0] - 1)):
        print('  %-34s %.4f (%+.2f%%)' % (st, gg, (gg - 1) * 100))
    print('\nWhat this does NOT do is exempt anything: a run whose'
          ' registration'
          '\nexempts the placement-exposed arms has to drop them itself,'
          ' this'
          '\nmode having no way to know which arms a given run put outside'
          ' its condition.')
    print('The band above is %.1f%%%s.'
          % (band, '' if abs(band - 3.3) < 1e-9 else
             ", NOT this README's standing 3.3%: --band was given"))
    return 0


def compare_ci(cells, shapes, strategies, meta, other, main_hs):
    """Each arm's CI% in this run against the same arm in another.

    `CI%` is the MEDIAN half-width across shapes, which is what the
    published column is, and that is the whole reason this mode exists:
    Run 18 asked what a saturating preamble does to the column, computed
    the MEAN over `--cells` instead, and got the opposite sign on two arms
    of three -- `build` reading 1.58 to 1.84 where the medians go 1.55 to
    1.42. The statistic the column publishes is the statistic a question
    about the column has to be asked in, and hand arithmetic over the dump
    is where that goes wrong.

    Unlike the time columns this needs no correction and no `list`: a
    half-width as a percentage of its own slope is already dimensionless,
    so the two runs are comparable however far apart their absolutes are.
    """
    b_cells, b_shapes, b_strategies = load_other(other, main_hs,
                                                 shapes, meta)
    both_sh = [s for s in shapes if s in b_shapes]
    both_st = [t for t in strategies if t in b_strategies]
    print('\nCI%%: this run against %s, per arm, as the MEDIAN half-width'
          '\n  across %d shared shape(s) -- the statistic the published'
          ' column is'
          % (os.path.basename(other), len(both_sh)))
    rows = []
    for st in both_st:
        a = [cells[sh][st]['ci'] for sh in both_sh
             if st in cells[sh] and cells[sh][st]['ci'] is not None]
        b = [b_cells[sh][st]['ci'] for sh in both_sh
             if st in b_cells[sh] and b_cells[sh][st]['ci'] is not None]
        if a and b:
            rows.append((stats.median(a), stats.median(b), st))
    if not rows:
        print('\n  no arm is comparable across these two runs.')
        return 2
    print('\n%-34s %8s %8s %8s' % ('arm', 'this', 'other', 'ratio'))
    for x, y, st in sorted(rows, key=lambda r: -(r[0] / r[1]) if r[1] else 0):
        print('%-34s %8.2f %8.2f %8.2f'
              % (st, x, y, (x / y) if y else float('nan')))
    # A zero CI% on EITHER side is out of the geomean: a zero in the
    # other run has no ratio, and a zero in THIS run has ratio 0, whose
    # log took the whole mode down with a ValueError -- the mirror of
    # the all-zero other run guarded since a6067af, found 2026-08-23 by
    # flipping that state's two files.
    zero = [st for x, y, st in rows if not (x > 0 and y > 0)]
    rs = [x / y for x, y, st in rows if x > 0 and y > 0]
    if zero:
        print('\n%d arm(s) with a zero CI%% on a side are out of the'
              ' geomean: %s' % (len(zero), ', '.join(zero)))
    if not rs:
        # A single `%`: no format operation runs on this print, so a
        # doubled one reaches the reader doubled -- as it did from
        # a6067af until the case caught it here.
        print('\nno arm has a non-zero CI% on both sides, so there is no'
              ' ratio to take.')
        return 0
    print('\ngeomean over the %d arm(s) %.2f, %d wider here and %d narrower.'
          % (len(rs), geomean(rs), sum(1 for r in rs if r > 1),
             sum(1 for r in rs if r < 1)))
    print('A cell resolving worse is not a cell measuring something'
          ' different:'
          '\nthis column is sampling error INSIDE one bench, where the A/A'
          ' floor'
          '\nis agreement BETWEEN two placements of one strategy. Run 18'
          ' moved'
          '\nthe two in opposite directions, so do not read either off the'
          ' other.')
    return 0


def provenance_line(json_path):
    """The `=== roster ...` line a process prints to its own stderr.

    Beside every recorded JSON is the `.log` its process wrote, and the
    last line of it carries the elapsed time and the two heap peaks that
    a run chapter and every class block quote. Reading it here is what
    stops eighteen of them being copied by hand.
    """
    if not json_path:
        return None
    log = re.sub(r'\.json$', '.log', json_path)
    try:
        with open(log, errors='replace') as f:
            hits = [l.strip() for l in f
                    if l.startswith('=== roster ') and 'elapsed' in l]
    except OSError:
        return None
    return hits[-1][len('=== '):] if hits else None


def wallclock_window(json_path):
    """(first stamp, last stamp, processes) from the run's wall-clock log.

    Found from the run's own name, as the alone legs are: the driver
    writes one `$R-wallclock.log` beside the JSONs and stamps every
    process into it, so the window a chapter opens with is a read and not
    a transcription.
    """
    if not json_path:
        return None
    base = os.path.basename(json_path)
    m = re.match(r'^(.+?)-.+\.json$', base)
    if not m:
        return None
    log = os.path.join(os.path.dirname(os.path.abspath(json_path)),
                       m.group(1) + '-wallclock.log')
    try:
        with open(log, errors='replace') as f:
            text = f.read()
    except OSError:
        return None
    stamps = re.findall(r'^=== (\S+) ', text, re.M)
    if not stamps:
        return None
    done = len(re.findall(r'^=== \S+ done ', text, re.M))
    return (stamps[0], stamps[-1], done)


def compare_table(cells, shapes, strategies, meta, other, main_hs,
                  brief=True):
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
    b_cells, b_shapes, b_strategies = load_other(other, main_hs,
                                                 shapes, meta)

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
        if no_net(st):
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
    if brief:
        return
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
    if 'sum-only-early' in strategies and 'sum-only-late' in strategies:
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
        if any(cells[s][x][key] <= 0 for s in shapes for x in (a, b)):
            print('%-28s %-24s  not readable: a cell with no positive %s'
                  % (a, b, key))
            continue
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
    insitu = insitu_ratios(cells, shapes, strategies)
    if insitu and any(terms.values()):
        print('\n%-28s %-24s %9s %8s %7s'
              % ('in-situ forcing term', 'against sum-only', 'ratio',
                 'median', 'mean|d|'))
        for base, arm, r, at in insitu:
            dev = [abs(x - 1) * 100 for x in r]
            worst = max(zip(dev, at))
            print('%-28s %-24s %9.4f %8.4f %6.2f%%'
                  % (base + ' - ' + arm, 'sum-only', geomean(r),
                     stats.median(r), stats.fmean(dev)))
            print('%64s worst cell %.2f%% on %s' % ('', worst[0], worst[1]))
            if len(at) < len(shapes):
                # A row over fewer shapes than the run has is a different
                # population from the one above it, and nothing else here
                # would say so.
                print('%64s over %d of %d shape(s): %s'
                      % ('', len(at), len(shapes),
                         ', '.join(s for s in shapes if s not in at)
                         + ' dropped, the gap or the term not positive'))
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
        # The spread is named as the FLOOR here because it is one, and
        # because the two names cost two wrong answers on 2026-08-23: a
        # session counting the floor asymmetry read `read-all.sh`'s A/A
        # WORST CELL column instead, which is a max over cells where the
        # floor is a max over pairs, and got a different number for the
        # same process -- 13.22% against 6.01% on run18-g912-slice. Both
        # figures are real and neither is the other; only this one is
        # what `--block` prints as `this class's floor` and what the
        # class table's floor column carries.
        print('  median half-width %.2f%% against an observed spread of'
              ' %.2f%% (this population\'s FLOOR),' % (typical, spread))
        if typical > 0:
            print('  so a computed interval understates real variability by'
                  ' about %.0fx.' % (spread / typical))
        print('  Multiply by that before believing any interval this reader'
              ' prints,\n  and read the factor as an order of magnitude: it'
              ' rests on %d pairs.' % len(known))
        # Hyphenated deliberately. read-all.sh scrapes this same output for
        # its column with an awk matching the unhyphenated phrase, and a
        # line here carrying it can be taken for a reading: it survives
        # today only because that awk stops at the in-situ section above,
        # which is ordering and not design. 2026-08-23.
        print('  THE FLOOR IS THIS FIGURE and not read-all.sh\'s A/A'
              ' worst-cell column:\n  a max over pairs against a max over'
              ' cells, twofold apart and more on\n  one process. Take a'
              ' floor from here or from --block, never by eye\n  off the'
              ' pair listing above, whose last rows are `sum-only`.')
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


def best_step(per):
    """(percent, t, split, n) for the best two-segment split of a series.

    Separate from `step_scan` so that `--selftest` can hand it a series it
    built: a constant one, where the answer must be that there is no step,
    and one with a step planted at a known sample, where the answer must be
    that step at that sample. Neither can be got from a run file, which is
    why the check would otherwise be unwritable.

    Prefix sums make the sweep linear rather than quadratic: the run files
    here carry ~4000 cells of ~100 samples, and a quadratic sweep over all
    of them is minutes where this is seconds.
    """
    n = len(per)
    if n < 20:
        return None
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
        return None
    a, b = pre[k] / k, (pre[n] - pre[k]) / (n - k)
    t = abs(b - a) / math.sqrt(var * (1 / k + 1 / (n - k)))
    return (b / a - 1) * 100, t, k, n


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
    3% of them and puts the arms this README already suspects -- `build`,
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
    # The only place this script indexes INTO a sample, so the only place a
    # run file whose samples are not criterion Measured arrays can be met.
    # A stub built to what `load` reads -- which is the list's length and
    # nothing else -- crashed here with `KeyError: 3` rather than saying
    # what was wrong with the file (2026-08-16, a toy run).
    unread = [r['reportName'] for r in raw[2]
              if not all(isinstance(s, (list, tuple)) and len(s) > 3
                         for s in r['reportMeasured'])]
    if unread:
        sys.stderr.write('warning: %d report(s) in %s carry samples that are'
                         ' not Measured arrays, so the step scan skipped'
                         ' them: %s\n'
                         % (len(unread), os.path.basename(path),
                            ', '.join(unread[:3])
                            + (', ...' if len(unread) > 3 else '')))
    for r in raw[2]:
        if r['reportName'] in unread:
            continue
        m = [s for s in r['reportMeasured'] if s[3] >= min_iters]
        if len(m) < min_samples:
            continue
        m.sort(key=lambda s: s[3])
        got = best_step([s[0] / s[3] for s in m])
        if got:
            d, t, k, n = got
            out.append((r['reportName'], d, t, k, n, m[k][3]))
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


def machine_check(cells, shapes, readme, thresh=3.0, spread=7.0):
    """Does the machine still measure what it measured last run?

    `list` is the arm to ask. It is the denominator of every published
    ratio, it is the one arm measured insusceptible to placement, and the
    fingerprint table keeps its net per call PER SHAPE -- so the previous
    run's absolutes survive in README long after its JSONs are offered for
    deletion, and no artifact has to be kept for this.

    The gate is the moment to ask it. Its selection carries `*/list` and
    both `sum-only` halves on every shape, so the comparison is net
    against net, and it runs before the evening rather than after it: a
    machine that has changed under the README invalidates a run that has
    not started yet, which is the only time that news is cheap.

    The threshold is the geomean over shapes, not a cell. Across the
    eleven kept processes of Runs 10 to 13 -- three regimes, two shims,
    main sets and gates alike -- `list`'s geomean against the eight-run
    median stays inside 0.82%, while single shapes wander to 7%. So 3% is
    over three times the worst excursion the record has, and a cell moving
    is normal where the whole baseline moving is not. The fingerprint
    prints three significant figures, which is about half a percent a
    cell and averages away over the shape set.

    `spread` is the second reading, and the one that says whether the move
    is a single number: the per-shape residual about the geomean, banded
    at the same 7% the paragraph above calls an ordinary single-shape
    wander. Inside it the shapes moved together, so one figure describes
    the box and every cross-run ORDERING survives; outside it they did
    not, and orderings are in question along with the level.

    NEITHER OUTCOME STOPS A RUN, and the mode returns 0 for both. It used
    to return 1 on the geomean, which failed the gate and left a quiet
    machine idle until a person woke to be asked -- the worst trade
    available, since the evening cannot be recovered and the reading can.
    Every claim this README publishes is a within-run comparison, so a box
    that moved between runs cannot reach one; the cross-run absolute
    column is what it reaches, and that re-baselines with each write-up.
    Only a comparison the mode cannot make AT ALL still returns 1: no
    shape of this run in the fingerprint, or every shape's `list` net
    non-positive. Some shapes sunk is not that -- those are dropped by
    name and the rest are compared, at 0.

    What it cannot do is say WHAT changed; that is a person's, and the
    first question is not the code but the box -- a kernel, a microcode
    update, a BIOS setting, a different machine, a thermal state -- asked
    when the machine is free rather than while it stands waiting.
    """
    want = {}
    for line in open(readme):
        m = FINGERPRINT_ABS_RE.match(line)
        if m:
            want[m.group(1)] = float(m.group(2)) * UNIT[m.group(3)]
    have = [(sh, cells[sh]['list']['net'], want[sh])
            for sh in shapes if sh in want and 'list' in cells[sh]]
    if not have:
        print('machine: no shape of this run is in README\'s fingerprint, so'
              ' there is nothing to compare -- which is itself worth reading')
        return 1
    # A non-positive net has no ratio and no log, and this is the fifth site
    # of the family the other four were guarded against on 2026-08-17. It is
    # the one where an unguarded traceback does lasting damage rather than
    # printing: run-gate.sh captures this output with 2>&1 and appends it
    # VERBATIM to the pair note, under a heading calling it an answer about
    # the box -- so a ValueError out of geomean would be filed there as the
    # gate's own finding, on the pair, permanently. `list` is the baseline
    # and the largest net in every run, so reaching this wants a disturbed
    # or inflated forcing term, which is a state `health` provokes and
    # reports rather than one no run can be in.
    sunk = [sh for sh, n, w in have if n <= 0 or w <= 0]
    if sunk:
        print('machine: %d shape(s) dropped, `list` net not positive: %s'
              % (len(sunk), ', '.join(sunk)))
        have = [t for t in have if t[1] > 0 and t[2] > 0]
    if not have:
        print('machine: every fingerprinted shape of this run has a'
              ' non-positive `list` net, so there is nothing to compare --'
              ' read the forcing term before the box')
        return 1
    ratios = [n / w for _, n, w in have]
    g = geomean(ratios)
    worst = max(have, key=lambda t: abs(math.log(t[1] / t[2])))
    print('machine: `list` net against the kept fingerprint, %d of %d shapes'
          % (len(have), len(shapes)))
    print('  geomean %+.2f%%, worst `%s` %+.2f%%, %d shape(s) past 5%%'
          % ((g - 1) * 100, worst[0], (worst[1] / worst[2] - 1) * 100,
             sum(1 for r in ratios if abs(r - 1) > 0.05)))
    if abs(g - 1) * 100 <= thresh:
        print('  inside %.0f%%, so the box still measures as it did.' % thresh)
        return 0
    # PAST the geomean threshold. This used to print STOP and return 1,
    # which failed the gate and left the evening waiting on a person --
    # and the person is asleep, which is why the gate runs at that hour.
    # Changed 2026-08-23: the box question NEVER stops a run. Every claim
    # this README publishes is a within-run comparison, arm against arm
    # inside one process, so a box that moved BETWEEN runs cannot reach
    # one; what it reaches is the cross-run absolute column, and the
    # fingerprint re-baselines with each write-up anyway. Run 18 met this
    # at +4.81% and the standing answer was `run anyway, re-baseline`,
    # taken by hand after hours of idle machine; that answer is now the
    # default. What the reading is still worth is the CLASSIFICATION
    # below, which the old text never made: whether the shapes moved
    # together.
    resid = [(sh, r / g - 1) for (sh, _, _), r in zip(have, ratios)]
    loud = [t for t in resid if abs(t[1]) * 100 > spread]
    far = max(resid, key=lambda t: abs(t[1]))
    print('  BOX MOVED: past %.0f%%, and the whole baseline with it --'
          ' not a strategy' % thresh)
    print('  and not drift.')
    if not loud:
        # A LEVEL SHIFT. The docstring's own calibration is what makes this
        # readable rather than a second arbitrary number: the geomean holds
        # inside 0.82% over eleven kept processes while single shapes wander
        # to 7%, so a residual inside 7% is shapes moving together and the
        # move is one number. Run 18's was this: +4.81% geomean, +9.50%
        # worst, a +4.47% residual.
        print('  Every shape moved TOGETHER --- worst residual about the'
              ' geomean %+.2f%%' % (far[1] * 100))
        print('  on `%s`, inside the %.0f%% a single shape ordinarily'
              ' wanders. So one' % (far[0], spread))
        print('  number describes it, and every cross-run ORDERING survives'
              ' it.')
    else:
        print('  The shapes did NOT move together: %d of them past %.0f%%'
              ' from the geomean,' % (len(loud), spread))
        print('  worst `%s` %+.2f%%. So a cross-run ORDERING is in question'
              % (far[0], far[1] * 100))
        print('  too, and not only the level --- which is the half of this'
              ' reading worth')
        print('  carrying into the write-up.')
    print('  THE RUN GOES AHEAD EITHER WAY, and this is not a failure. Ask'
          ' the box')
    print('  question of a PERSON afterwards --- a kernel, a microcode'
          ' update, a BIOS')
    print('  setting, a thermal state, a different machine, none of them'
          ' visible from')
    print('  inside a run --- and ask it while the machine is free, not'
          ' while it stands')
    print('  idle waiting to be asked. What the run owes is a paragraph'
          ' naming the')
    print('  move; what it does not owe is the evening.')
    # What it still leaves possible, named here because this is where a
    # session stands when it fires. The fingerprint is one half's, taken at
    # ONE allocation area, so a run whose basis moved to another area fails
    # this for that reason alone and not for the box -- which is Run 16,
    # where the basis moved to `-A32m` against a default-area fingerprint
    # and the check fired on every gate. The discriminating control costs
    # no build and no pair: `-rtsopts` is live, so run the gate's own
    # five-bench selection on a binary AT WHATEVER CONDITION THE
    # FINGERPRINT WAS TAKEN UNDER and read `--machine` on that. Inside the
    # threshold there, the box is unchanged and what fired is the thing
    # this run changed. Case:
    # `machine-check-names-the-control-it-leaves`.
    #
    # GENERALISED 2026-08-23 out of Run 18, which met this with the area
    # UNCHANGED: its fingerprint predated a saturating preamble, a source
    # patch and a compiler, and the message named only the area, so the
    # session had to invent the analogue -- the same binary with the
    # instrument off, then the previous run's own binary. The text now
    # names both, the second being what settles it, that binary being
    # what produced the fingerprint.
    print('  What separates the two costs no build and no pair: run the'
          ' gate\'s own')
    print('  five-bench selection on a binary at WHATEVER CONDITION THE'
          ' FINGERPRINT')
    print('  was taken under -- the allocation area, an instrument switched'
          ' on by an')
    print('  environment variable, a source patch, a compiler -- and read'
          ' --machine on')
    print('  that. Inside the threshold there, the box is unchanged and what'
          ' fired is')
    print('  the thing this run changed. The previous run\'s own binary, if'
          ' it is still')
    print('  on disk, answers it most directly of all: it produced the'
          ' fingerprint.')
    return 0


def deflation_table(run_path, cells, shapes, main_hs):
    """The roster cell over the same shape's ALONE LEG, per shape.

    The riders a paired run leaves -- `$R-al-<half>-<shape>-r1.json`, one
    bench in its own process -- exist so the in-process deflation can be
    read per shape instead of estimated, and this is the mode that reads
    it. Run 16 measured +11.43% at `-A32m` and Run 17 +11.51% and +11.62%
    on its two halves; before this mode existed both were computed by hand
    in the write-up, which by this README's own rule is a defect report
    against this script rather than a script to keep.

    RAW slope against RAW slope, and that is the one decision a session
    gets wrong. An alone leg is one bench in its own process, so it
    carries no `sum-only` bench and has no correction to subtract, while
    the roster's `list` has one; dividing the roster's NET by the leg's
    raw would fold the whole forcing term into the deflation and read
    about a point low on the microsecond shapes and far worse on the
    slowest. Both sides here are `slope`, so no correction convention
    enters the ratio at all and the figure owes nothing to which term the
    run subtracted.

    The legs are found from the run's own name -- `run17-wildlog-main.json`
    looks for `run17-al-wildlog-*-r1.json` -- so the mode takes no second
    path and cannot be pointed at another half's legs by accident. A shape
    the run has and the legs do not is reported rather than dropped: a
    partial rider set is what an interrupted evening leaves, and it is the
    case this mode must not average over in silence.

    That glob takes BOTH rider sets, `-sat` being a suffix on the half's
    name, and the saturated legs used to key as `sat-<shape>`, match no
    shape and vanish. They are the other half of a decomposition, not
    noise: with a saturating preamble the total splits into the STATE it
    puts on a clean process, `sat/clean`, and the REST the roster adds on
    top of it, `roster/sat`, whose product is the total. Run 18 registered
    those as separate quantities and subtracted them by hand in its
    write-up until this mode read them, which is the shape README calls a
    defect report against this script. Case:
    `deflation-ignores-the-saturated-legs`.
    """
    base = os.path.basename(run_path)
    m = re.match(r'^(.+?)-(.+?)-(?:main|[a-z0-9]+)\.json$', base)
    if not m:
        sys.stderr.write('%s: cannot read a run and a half out of this name,'
                         ' so the alone legs cannot be found\n' % base)
        return 2
    prefix, half = m.group(1), m.group(2)
    pat = '%s-al-%s-' % (prefix, half)
    legs, sat = {}, {}
    for path in sorted(glob.glob('%s*-r1.json' % pat)):
        shape = os.path.basename(path)[len(pat):-len('-r1.json')]
        # THE GLOB TAKES BOTH RIDER SETS. `-sat` is a suffix on the half's
        # name, so `$R-al-<half>-*` matches the saturated legs too; they
        # used to come back keyed `sat-<shape>`, match no shape of the run
        # and be dropped in silence. They are the other half of the
        # decomposition, so they are separated here rather than discarded.
        into = legs
        if shape.startswith('sat-'):
            into, shape = sat, shape[len('sat-'):]
        l_cells, l_shapes, _, _ = load(path, main_hs)
        if len(l_shapes) != 1 or 'list' not in l_cells[l_shapes[0]]:
            sys.stderr.write('%s: not one shape\'s `list`, so it is not an'
                             ' alone leg; skipped\n' % os.path.basename(path))
            continue
        # A ratio to this slope is logged below, so one that is not
        # positive would take the whole mode down -- the family every
        # net site was guarded against on 2026-08-17, on the raw side.
        # The slope is criterion's own, so no roster state reaches
        # this; a doctored or truncated leg does.
        if l_cells[l_shapes[0]]['list']['slope'] <= 0:
            sys.stderr.write('%s: its `list` slope is not positive, so no'
                             ' ratio to it has a log; skipped\n'
                             % os.path.basename(path))
            continue
        into[shape] = l_cells[l_shapes[0]]['list']['slope']
    if not legs:
        # SAY WHICH of the two is missing. With the saturated set on disk
        # and the clean one absent -- an interrupted rider evening, the
        # `SAT=` invocations having run and the plain ones not -- the old
        # wording said the riders were never taken, which is the one
        # thing the directory disproves.
        if sat:
            sys.stderr.write('%d saturated leg(s) are here and no CLEAN one:'
                             ' the total is roster over CLEAN, so the'
                             ' decomposition cannot be read from these'
                             ' alone\n' % len(sat))
        else:
            sys.stderr.write('no %s*-r1.json beside this run: the riders were'
                             ' not taken, or the run and half are not this'
                             ' file\'s\n' % pat)
        return 2
    rows, missing = [], []
    for sh in shapes:
        if 'list' not in cells[sh]:
            continue
        if sh not in legs:
            missing.append(sh)
            continue
        if cells[sh]['list']['slope'] <= 0:
            sys.stderr.write('%s: this run\'s `list` slope is not positive,'
                             ' so its deflation has no log; dropped\n' % sh)
            continue
        rows.append((sh, cells[sh]['list']['slope'] / legs[sh]))
    print('in-process deflation: this run\'s `list` over its own alone leg,'
          ' raw over raw')
    print('%-26s %10s %12s %12s'
          % ('shape', 'roster/alone', 'roster', 'alone'))
    for sh, r in rows:
        print('%-26s %10.4f %12s %12s'
              % (sh, r, fmt_abs(cells[sh]['list']['slope']),
                 fmt_abs(legs[sh])))
    if not rows:
        print('\nNO shape of this run has an alone leg beside it, so there is'
              ' no deflation to read here.')
        print('  the legs are the MAIN SET\'s; a class run has none of its'
              ' own, and this mode is not for one.')
        return 2
    g = math.exp(sum(math.log(r) for _, r in rows) / len(rows))
    up = sum(1 for _, r in rows if r > 1)
    lo = min(rows, key=lambda x: x[1])
    hi = max(rows, key=lambda x: x[1])
    print('\ngeomean %.4f (%+.2f%%) over %d shape(s); %d above 1'
          % (g, 100 * (g - 1), len(rows), up))
    print('  least %.4f on %s, most %.4f on %s'
          % (lo[1], lo[0], hi[1], hi[0]))
    split = [(sh, sat[sh] / legs[sh], cells[sh]['list']['slope'] / sat[sh])
             for sh, _ in rows if sh in sat]
    if split:
        # THE DECOMPOSITION, which is why a run takes each leg twice: the
        # STATE is what a saturating preamble puts on a clean process and
        # the REST is what the roster adds on top of that state. Their
        # product is the total above, so the three columns are one figure
        # split at the point a registration asks about rather than three
        # measurements.
        print('\nand with the saturated legs beside them, the same total'
              ' split in two')
        print('%-26s %10s %10s' % ('shape', 'sat/clean', 'roster/sat'))
        for sh, st, rest in split:
            print('%-26s %10.4f %10.4f' % (sh, st, rest))
        gs = math.exp(sum(math.log(s) for _, s, _ in split) / len(split))
        gr = math.exp(sum(math.log(r) for _, _, r in split) / len(split))
        print('\nstate  sat/clean  geomean %.4f (%+.2f%%) over %d shape(s)'
              % (gs, 100 * (gs - 1), len(split)))
        print('rest   roster/sat geomean %.4f (%+.2f%%), %d above 1'
              % (gr, 100 * (gr - 1), sum(1 for _, _, r in split if r > 1)))
        rlo = min(split, key=lambda x: x[2])
        rhi = max(split, key=lambda x: x[2])
        print('  the rest runs %.4f on %s to %.4f on %s'
              % (rlo[2], rlo[0], rhi[2], rhi[0]))
    elif sat:
        print('\n%d saturated leg(s) here match no shape of this run, so the'
              ' split is not read: %s' % (len(sat), ', '.join(sorted(sat))))
    if missing:
        print('\n%d shape(s) of this run have NO alone leg and are not in the'
              ' figure above: %s' % (len(missing), ', '.join(missing)))
        print('  a partial rider set is what an interrupted evening leaves;'
              ' the geomean above is over the legs that exist and says so')
    return 0


# /proc/stat is in USER_HZ, and the kernel fixes THAT at 100 for userspace
# whatever CONFIG_HZ it ticks at, so a jiffy is 10 ms here and the constant
# is not the machine's to vary. It is also the quantum of every foreign
# figure below, which is why they are aggregated per bench before being
# read: one jiffy across a two-millisecond sample is 5x its own work, and
# says nothing.
JIFFY_NS = 10 ** 7

# A bench whose foreign CPU reaches this multiple of its own, summed over
# all its samples, is named individually. Not a threshold on a sample.
WILD_LOUD = 0.25


def fmt_ratio(r):
    """A foreign ratio in a fixed seven columns, however large it gets.

    It is unbounded -- the denominator is a bench's own CPU, so a bench
    that ran for a few jiffies divides by nearly nothing -- and `%7.2f`
    on such a value runs into the column to its left and takes the table
    apart. Seen at 499999999.00 while the mode was being exercised on a
    two-sample toy log, which is what a real one looks like when the
    process barely ran. Anything past the machine's core count is already
    impossible as a reading, so the display saturates and says so.
    """
    if r != r or r > 999:
        return '   >999'
    return '%7.2f' % r


def parse_wild(line):
    """One `@@wild` line as a dict, or None.

    The stamp is `@@wild NAME PHASE key=value ...`, and the keys are read
    by name rather than by position precisely because Run 18's stamp adds
    three that Run 17's has not got: a log written by either instrument
    parses here, and which fields it turned out to carry is what the
    caller reports rather than something to fail on.
    """
    parts = line.split()
    if len(parts) < 3 or parts[0] != '@@wild':
        return None
    rec = {'name': parts[1], 'phase': parts[2]}
    for tok in parts[3:]:
        if '=' in tok:
            k, v = tok.split('=', 1)
            rec[k] = v
    return rec


def read_wild(path):
    """Every sample in one instrument log, as (bench, deltas).

    A SAMPLE IS A `pre`/`post` PAIR, those being criterion's `allocEnv`
    and `cleanEnv` hooks, which bracket the timed block from outside; and
    every quantity the stamp carries is a cumulative total, so everything
    read here is a difference between the two lines. A `pre` with no
    `post` is dropped and COUNTED rather than paired with what follows: a
    log a killed process left ends in one, and pairing it across would
    read the next bench's work as this one's.
    """
    samples, unpaired, pending = [], 0, {}
    with open(path, errors='replace') as f:
        for line in f:
            if not line.startswith('@@wild '):
                continue
            rec = parse_wild(line)
            if rec is None:
                continue
            nm = rec['name']
            if rec['phase'] == 'pre':
                if nm in pending:
                    unpaired += 1
                pending[nm] = rec
            elif rec['phase'] == 'post':
                pre = pending.pop(nm, None)
                if pre is None:
                    unpaired += 1
                    continue
                try:
                    samples.append((nm, wild_deltas(pre, rec)))
                except (KeyError, ValueError):
                    unpaired += 1
    return samples, unpaired + len(pending)


def wild_deltas(pre, post):
    """The differences one sample's two stamps bracket.

    `foreign` is the whole point of the load fields and is the one figure
    here that is not the process's own: the machine's busy jiffies over
    the sample, less what this process spent mutating and collecting in
    it. What is left ran somewhere else, which is the updater class the
    wild-cell entry needs told apart from a genuine wild cell -- flat RTS
    totals and a moved mutator clock being the signature of BOTH.

    The subtrahend is an ELAPSED clock and the minuend a CPU one, which is
    the approximation in it and is named here rather than corrected: the
    stamp carries `mutator_elapsed_ns`, these processes run single
    threaded and CPU-bound inside a sample, so the two agree except where
    the process was itself descheduled -- and a descheduled process is the
    intrusion this figure is looking for, so the error is towards
    UNDER-reporting one and never towards inventing one.
    """
    d = {'iters': int(post['iters'])}
    for k in ('alloc', 'mut', 'gc'):
        d[k] = int(post[k]) - int(pre[k])
    d['inuse'] = int(post['inuse'])
    d['load'] = post.get('load')
    d['runq'] = post.get('run')
    if 'cpu' in pre and 'cpu' in post:
        d['own'] = d['mut'] + d['gc']
        d['machine'] = (int(post['cpu']) - int(pre['cpu'])) * JIFFY_NS
        d['foreign'] = d['machine'] - d['own']
    return d


def wild_table(path, verbose=False):
    """The instrument's log read per sample, one line a bench.

    The mode exists because Run 17's write-up read these logs BY HAND --
    which by this README's own standing rule is a defect report against
    this script rather than a thing to do twice -- and because Run 18's
    stamp carries three fields no run has yet had a reader for.

    Per bench rather than per sample by default, and the reason is the
    quantum: /proc/stat counts in 10 ms jiffies, so one jiffy landing
    inside a two-millisecond sample reads as several times that sample's
    own work and means nothing. Summed over a bench the quantisation
    averages out, which is why the `foreign` column is a ratio of sums and
    the per-sample maximum is printed beside it as an upper bound and not
    as a reading. `--verbose` prints every sample, for a bench whose
    interior is the question.
    """
    samples, unpaired = read_wild(path)
    if not samples:
        sys.stderr.write('%s: no paired `@@wild` samples here. The log of an'
                         ' uninstrumented half carries none, and neither does'
                         ' one whose process ran without WILDLOG set\n'
                         % os.path.basename(path))
        return 2
    order, per = [], {}
    for nm, d in samples:
        if nm not in per:
            per[nm] = []
            order.append(nm)
        per[nm].append(d)
    have_load = any('foreign' in d for _, d in samples)
    print('%s: %d sample(s) over %d bench(es), from the per-sample instrument'
          % (os.path.basename(path), len(samples), len(order)))
    if not have_load:
        print()
        print('NO LOAD FIELDS in this log, so there is no foreign-CPU column'
              ' below: it')
        print('  was written by an instrument without `load=`, `run=` and'
              ' `cpu=`, which')
        print('  is every stamp before Run 18\'s. The clocks and the'
              ' allocation read as ever.')
    print()
    head = '%-38s %7s %13s %13s %6s' % ('bench', 'samples', 'alloc/iter',
                                        'mut/iter', 'gc%')
    print(head + ('%8s %6s' % ('foreign', 'load') if have_load else ''))
    loud, partial = [], []
    for nm in order:
        ds = per[nm]
        its = sum(d['iters'] for d in ds) or 1
        alloc = sum(d['alloc'] for d in ds) / its
        mut = sum(d['mut'] for d in ds) / its
        gc = sum(d['gc'] for d in ds)
        gcpct = 100.0 * gc / (sum(d['mut'] for d in ds) + gc or 1)
        f_txt, l_txt = '', ''
        if have_load:
            # OVER THE SAMPLES THAT CARRY THE FIELDS, and the ones that do
            # not are counted rather than averaged over: a log spanning an
            # instrument change, or two logs concatenated, otherwise gets a
            # figure over a subset with nothing saying it is one -- the
            # silent narrowing this directory's rules refuse. Marked `*`
            # here and named under the table.
            withf = [d for d in ds if 'foreign' in d]
            if len(withf) != len(ds):
                partial.append((nm, len(withf), len(ds)))
            own = sum(d['own'] for d in withf)
            frn = sum(d['foreign'] for d in withf)
            ratio = frn / own if own else 0.0
            f_txt = fmt_ratio(ratio) + ('*' if len(withf) != len(ds) else ' ')
            loads = [float(d['load']) for d in ds if d.get('load')
                     not in (None, '?')]
            l_txt = '%6.2f' % max(loads) if loads else '     ?'
            if withf and ratio >= WILD_LOUD:
                loud.append((nm, ratio, max(d['foreign'] for d in withf)))
        row = '%-38s %7d %13.0f %13.0f %6.2f' % (nm, len(ds), alloc, mut,
                                                 gcpct)
        print(row + ('%8s %6s' % (f_txt, l_txt) if have_load else ''))
    if partial:
        print()
        print('%d bench(es) marked * have samples WITHOUT the load fields,'
              ' and their' % len(partial))
        print('  foreign figure is over the samples that carry them and not'
              ' over the bench:')
        for nm, k, n in partial:
            print('  %-38s %d of %d sample(s)' % (nm, k, n))
        print('  A log spanning an instrument change, or two logs'
              ' concatenated, reads this way.')
    if have_load:
        print()
        print('`foreign` is the machine\'s busy CPU during a bench\'s samples,'
              ' less this')
        print('  process\'s own mutator+collector, over that own time: 0.00 is'
              ' a machine')
        print('  doing nothing else and 1.00 is one further core busy'
              ' throughout. `load` is')
        print('  the highest 1-minute average any of the bench\'s stamps saw,'
              ' which dates')
        print('  a multi-minute intruder where `foreign` catches a short one.')
        if loud:
            print()
            print('%d bench(es) at or above %.2f foreign, which is an'
                  ' INTRUSION and not a wild'
                  % (len(loud), WILD_LOUD))
            print('  cell -- a wild cell moves the mutator clock with the'
                  ' machine quiet beside it:')
            for nm, ratio, worst in sorted(loud, key=lambda x: -x[1]):
                print('  %-38s %s, worst sample %.1f ms foreign'
                      % (nm, fmt_ratio(ratio).strip(), worst / 1e6))
            # LAST, because the list above is sorted worst-first and a
            # `tail` of this mode therefore reaches the MILDEST offenders.
            # Run 18's write-up read three such lines as "the worst three"
            # and understated the peak by an order of magnitude, 0.35
            # against 5.06, in a sentence about how much a machine's owner
            # had cost the run. A count and a peak on one line cannot be
            # tailed into the opposite claim.
            print('  IN ONE LINE: %d of %d bench(es) at or above %.2f'
                  ' foreign, peak %.2f.'
                  % (len(loud), len(order), WILD_LOUD,
                     max(r for _, r, _ in loud)))
        else:
            print()
            print('NO bench reaches %.2f foreign: nothing else was running on'
                  ' this machine' % WILD_LOUD)
            print('  during any of these samples, so a mutator step in here is'
                  ' the process\'s own.')
    if unpaired:
        print()
        print('%d unpaired stamp(s) dropped -- a `pre` with no `post`, which'
              ' is what a' % unpaired)
        print('  killed process leaves. They are in none of the figures'
              ' above.')
    if verbose:
        print()
        print('every sample, in the order the log carries them:')
        print('%-38s %7s %13s %13s %10s %6s %4s'
              % ('bench', 'iters', 'alloc/iter', 'mut/iter', 'foreign_ms',
                 'load', 'run'))
        for nm, d in samples:
            its = d['iters'] or 1
            print('%-38s %7d %13.0f %13.0f %10s %6s %4s'
                  % (nm, d['iters'], d['alloc'] / its, d['mut'] / its,
                     '%.1f' % (d['foreign'] / 1e6) if 'foreign' in d else '-',
                     d.get('load') or '-', d.get('runq') or '-'))
    return 0


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
# What Run N compares against pastes whole: one table over the main set,
# and since 2026-08-22 one over every stride-class shape with the same
# columns, emitted together when `--classes` names the class JSONs.
# Membership mirrors that section's rule as re-aimed that day --
# `mut-odo-vecdims` and every arm that is the best OUTSIDE the vecdims
# family on at least one shape of the main set or a class -- and it only
# ever GROWS: an arm that has earned a column keeps it, no run drops
# one, and the run writer prunes the header by hand if it gets
# unwieldy. `offtab-scan-rem` joined 2026-08-24. Neither way of
# dropping an arm survives and README says why beside the rule; the
# short of it is that this table holds the members alone, so it cannot
# say who has stopped earning a column. Growth is capped by one
# representative per family: where a qualifying arm is a close variant
# of a member and measures closely, the leading one keeps the column.
# That is a judgement and stays the write-up's; the notice below prices
# it by naming the best member on the shape the newcomer leads. The
# short column heads are the stretch table's convention; the README
# intro above the tables maps them back to full arm names. `install`
# matches a table by its whole header line, so a narrowed emitter and a
# wide table in the README would refuse rather than install.
# Arm and column head are one entry, so a column cannot be added
# without a head or vice versa.
FINGERPRINT = [('mut-odo-vecdims', 'vecdims'),
               ('mut-flat-gm', 'flat-gm'),
               ('bq-scan-rem-gm-mulback', 'scan-rem-gm'),
               ('build', 'build'),
               ('mut-odo', 'mut-odo'),
               ('bq-mut-runs', 'mut-runs'),
               ('bq-mut-runs-gm-mulback', 'runs-gm'),
               ('offtab-scan-rem', 'offtab-rem')]
FINGERPRINT_ARMS = [a for a, _ in FINGERPRINT]
FINGERPRINT_HEADS = '| ' + ' | '.join(h for _, h in FINGERPRINT) + ' |'
FINGERPRINT_TABLES = [
    ('| shape | `sInner` | `l` | `list`, net ' + FINGERPRINT_HEADS,
     True, FINGERPRINT_ARMS),
]
FINGERPRINT_CLASS_HEADER = ('| shape | class | `sInner` | `l` | `list`, net '
                            + FINGERPRINT_HEADS)


def fmt_abs(seconds):
    """A per-call time at reading precision, in README's units.

    A unit is taken as soon as the value ROUNDS to 1 of it, not once it
    reaches 1: at three significant figures 999.7 us prints as `1e+03 us`,
    which `FINGERPRINT_ABS_RE` cannot match, so `--machine` dropped that
    shape from its comparison and said nothing -- and README already
    carries a `1 ms` cell, which is that boundary. `.9995 * scale` is where
    `%.3g` starts rounding up out of the unit below. Found 2026-08-17 by
    review; the seam check in `selftest` samples the boundary now, having
    passed vacuously on four values nowhere near it.
    """
    for unit, scale in (('s', 1), ('ms', 1e-3), ('us', 1e-6),
                        ('ns', 1e-9)):
        if seconds >= scale * .9995:
            return _fig(seconds / scale) + ' ' + unit
    return _fig(seconds) + ' s'


def _fig(v):
    """Three significant figures, and never in exponent form.

    `%.3g` reaches for an exponent above 999 as well as below 0.0001, and
    the top unit has nothing above it to roll into, so a per-call time past
    a thousand seconds wrote `1.5e+03 s` -- which `FINGERPRINT_ABS_RE`
    cannot parse, the same seam the unit boundary broke. Found 2026-08-17
    by a property asked of every time figure in every run on disk.
    """
    out = '%.3g' % v
    return out if 'e' not in out else '%.0f' % v


def fingerprint_table(cells, shapes, strategies, meta, classes=()):
    """The kept per-shape record: dims, `list`'s net per call (absolute,
    so every ratio beside it converts back and the baseline is guarded at
    every shape), and the fingerprint arms' net ratios. Shapes sorted by
    l then name; an arm the run does not carry prints `--`.

    Born checked: pointed at a run without `list` (--exclude list) it
    refuses with exit 1, and its first emitted paste caught two Run 6
    cells still standing in README's hand-carried table --
    `alexnet-L1-55-c3-k11`'s scan-packed column and `stretch-bigstride`'s
    `bq-expand` one -- which is why the intro above the tables says to
    transcribe nothing by hand. `classes` is what `--classes` loaded: one
    (label, cells, shapes, dims) per class JSON, emitted as the second
    table with a `class` column, in the order given."""
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
                # `--` on a SUNK cell as well as an absent one, which is
                # what `time_of` and `worst_of` read on the same condition:
                # a net the forcing term did not leave positive is not a
                # ratio, and dividing anyway publishes a negative or wild
                # figure beside rows that correctly read `--`. It matters
                # more here than anywhere: this table is `--in-place`
                # installed every write-up and is the per-shape record kept
                # once the JSONs are offered for deletion, so a sunk figure
                # here outlives the run that could disprove it.
                row.append('--' if not c or c['net'] <= 0 or base <= 0
                           else '%.3f' % (c['net'] / base))
            print('| ' + ' | '.join(row) + ' |')
    if classes:
        print()
        header = FINGERPRINT_CLASS_HEADER
        print(header)
        print('|---|---' + '|---:' * (header.count('|') - 3) + '|')
        for label, c_cells, c_shapes, c_dims in classes:
            for sh in sorted(c_shapes, key=lambda x: (
                    c_dims[x]['l'] if x in c_dims else float('inf'), x)):
                d = c_dims.get(sh)
                base = c_cells[sh]['list']['net']
                row = ['`%s`' % sh, '`%s`' % label]
                row += [str(d['s_inner']), str(d['l'])] if d else ['?', '?']
                row.append(fmt_abs(base))
                for arm in FINGERPRINT_ARMS:
                    c = c_cells[sh].get(arm)
                    row.append('--' if not c or c['net'] <= 0 or base <= 0
                               else '%.3f' % (c['net'] / base))
                print('| ' + ' | '.join(row) + ' |')
        # The membership rule's data half, read where the data is: every
        # arm that is the best outside the vecdims family on some shape of
        # the main set or a class is a fingerprint arm. There is no
        # converse to check, membership only growing, so this asks one
        # question and asks it of the run in hand -- no previous run is
        # read, and none has to have survived. Said on stderr, where
        # install-tables.sh files what a run owes by hand. The shapes
        # are NAMED and not merely counted, with the best member beside
        # each: the open entry this answered had to read both back off
        # the cells by hand, the notice carrying a count alone.
        best = collections.Counter()
        where = collections.defaultdict(list)
        for p_shapes, p_cells in ([(shapes, cells)]
                                  + [(c[2], c[1]) for c in classes]):
            for sh in p_shapes:
                base = p_cells[sh]['list']['net']
                cands = [(c['net'] / base, st)
                         for st, c in p_cells[sh].items()
                         if st != 'list' and not is_control(st)
                         and not st.startswith(FAMILY)
                         and c['net'] > 0 and base > 0]
                if cands:
                    cands.sort()
                    best[cands[0][1]] += 1
                    near = next((c for c in cands[1:]
                                 if c[1] in FINGERPRINT_ARMS), None)
                    where[cands[0][1]].append(
                        '%s %.3f%s'
                        % (sh, cands[0][0], '' if near is None else
                           ' against `%s` %.3f' % (near[1], near[0])))
        missing = [a for a in best if a not in FINGERPRINT_ARMS]
        for a in missing:
            sys.stderr.write('membership: `%s` is best outside the family on'
                             ' %d shape(s) -- %s -- and is not a fingerprint'
                             ' arm: give it a column unless a member is a'
                             ' close variant measuring this closely, one'
                             ' representative per family being the rule\n'
                             % (a, best[a], '; '.join(where[a])))
        if not missing:
            sys.stderr.write('ok: every arm best outside the family on some'
                             ' shape here has a fingerprint column (%s)\n'
                             % ', '.join('%s %d' % kv
                                         for kv in best.most_common()))


# The three arms the second class property names, in the claims section
# (*The claims Run N should test*, NAMED and deliberately not anchored: that
# heading carries the run number and post-run step 5 renames it every
# write-up, so an anchor here goes dead at each rename -- and stays dead in
# every archived revision, where --audit replays this file against today's
# README and reads its own stale anchors as a --check-doc failure).
# Constants rather than literals
# because the property has been re-aimed twice, and a re-aim that misses one
# use of a name is how a verdict starts disagreeing with the claim it checks.
# The orderings each numbered claim rests on, as pairs, in the claims
# section's own order (named above and not anchored, for the reason there).
# A manifest
# rather than a parser over the prose: the claims are not uniformly
# machine-readable -- claim 2's second half is `offtab` BEHIND `bq-expand`
# rather than an `A < B` ordering, and claim 4 states two readings of
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
    (3, 'a mul-back output pays on the `bq-expand` build',
     [('bq-expand-gm-mulback', 'bq-expand', 'faster')]),
    # THE SECOND HALF STOPPED BEING A TIE ON 2026-08-22, six runs having
    # read it as one and Runs 16 and 17 having broken it identically --
    # 0.8471 at 18 of 24 and p 0.023, then 0.8578 at 18 of 24 and the same
    # p, on a different binary and a different basis half. Run 17's chapter
    # retired it in prose (*the next run inherits an ordering rather than
    # re-reading a tie*) and this line did not follow, so `--claims` went
    # on registering a tie the document had already replaced -- which Run
    # 18 would have broken for a third time and a session rediscovered.
    # Run 17's own verdict stands as recorded, BROKE against the
    # registration then in force; what moves is what the NEXT run inherits.
    (4, 'the scan ties its own build control, and beats `bq-expand`',
     [('bq-scan-rem-gm-mulback', 'bq-expand-gm-mulback', 'tie'),
      ('bq-scan-rem-gm-mulback', 'bq-expand', 'faster')]),
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


READING = collections.namedtuple(
    'READING', 'a b expect g k m p best ok pub')


def claim_readings(cells, shapes, strategies):
    """Every registered ordering's arithmetic and verdict: {claim: [...]}.

    `--claims` prints these and `--claims --in-place` installs them, and
    each computed them for itself -- the same four statistics and the
    same three-way read of the registered expectation, in two loops a
    hundred lines apart. They drifted where copies do: claim 9's two best
    cells were joined in one and indexed in the other, so a one-shape run
    got a line out of the printer and an IndexError out of the installer,
    on the same arithmetic (2026-08-16). What stays with each caller is
    the wording, which is all they ever really differed in.

    `best` is None unless the expectation names two shapes, and a pair
    either half of which this run does not carry is absent, so a claim
    with nothing live has no entry at all.
    """
    out = {}
    for n, _, pairs in CLAIMS:
        for a, b, expect in pairs:
            if a not in strategies or b not in strategies:
                continue
            raw, r = pair_stats(cells, shapes, a, b)
            g, m = geomean(r), len(r)
            k = sum(1 for x in r if x < 1)
            p = sign_p(k, m)
            # The published-column ratio, which only the read-back forms:
            # None where the pair had to be compared raw, there being no
            # corrected time to publish.
            pub = (None if raw else
                   time_of(cells, shapes, a) / time_of(cells, shapes, b))
            best = None
            if isinstance(expect, tuple):
                best = sorted(s for _, s in sorted(zip(r, shapes))[:2])
                ok = best == sorted(expect[1:])
            elif expect == 'tie':
                ok = p >= 0.05
            else:
                ok = (g < 1) if expect == 'faster' else (g > 1)
            out.setdefault(n, []).append(
                READING(a, b, expect, g, k, m, p, best, ok, pub))
    return out


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
    list of seven where the README has nine is how a claim goes unchecked.

    Born checked: run against Run 13's basis, every ordering it prints
    reproduces the figure that run published -- geomean, win count and
    sign p alike -- on all thirteen of them. The verdicts' own
    non-vacuity, 2026-08-14 against that same run: every pair prints HELD,
    and flipping claim 3's expectation to `slower` printed BROKE on the
    same figures, as did swapping claim 9's two registered shapes for
    `stretch-primes` -- so both predicate kinds can fail, and the reverted
    manifest returned thirteen HELDs.
    """
    gone, whole = main_set_gap(shapes, args.main)
    if gone:
        print('NOTE: this run carries %d of the main set\'s %d shapes. The'
              ' claims are registered over the whole of it, so what follows'
              ' is arithmetic and not their verdicts, which is why every'
              ' one below reads PART.' % (whole - gone, whole))
    # One entry per arm, as `install_readings` builds it: an arm the claims
    # list registers several times over -- `bq-expand` is one -- was counted
    # once per registration and named once, so a run filtered to drop it
    # reported more missing arms than it could name. Found 2026-08-17 by
    # review.
    missing = sorted({a for _, _, ps in CLAIMS for p in ps for a in p[:2]
                      if a not in strategies})
    if missing:
        print('NOTE: %d arm(s) of the claims list are not in this run: %s'
              % (len(missing), ', '.join(missing)))
        print('      a filtered run cannot check the claims; use a full one.')
    held = broke = 0
    readings = claim_readings(cells, shapes, strategies)
    for n, label, pairs in CLAIMS:
        print('\nclaim %d -- %s' % (n, label))
        live = [[x.a, x.b] for x in readings.get(n, [])]
        for a, b, _ in pairs:
            if [a, b] not in live:
                print('  %s / %s: not in this run' % (a, b))
        if live:
            pair_table(cells, shapes, strategies, live, quiet=True)
        for x in readings.get(n, []):
            a, b, expect, ok = x.a, x.b, x.expect, x.ok
            if x.best is not None:
                want = 'best two shapes are %s' % ' and '.join(
                    sorted(expect[1:]))
                got = 'they are %s' % ' and '.join(x.best)
            elif expect == 'tie':
                want, got = 'a tie by sign test', 'sign p %.2g' % x.p
            else:
                want = 'A %s (geomean %s 1)' % (expect,
                                                '<' if expect == 'faster'
                                                else '>')
                got = 'geomean %.4f' % x.g
            held += ok
            broke += not ok
            # On a partial population the arithmetic is real and the
            # verdict is not, so the verdict word is what goes. Saying it
            # once at the top was not enough: the BROKE lines are forty
            # lines below it, and a smoke run's two of them read as a
            # broken README to the session that ran it by hand.
            print('  %s  %s / %s: registered %s; %s'
                  % ('PART ' if gone else 'HELD ' if ok else 'BROKE',
                     a, b, want, got))
    if gone:
        print('\nNo verdict: %d of %d shapes. The orderings above are this'
              ' run\'s arithmetic, not the claims\'.' % (whole - gone, whole))
    else:
        print('\n%d of %d registered orderings held.' % (held, held + broke))
        if broke:
            # THE MANIFEST IS THE OTHER HALF OF A RETIREMENT, and forgetting
            # it is not hypothetical: Run 17's chapter retired claim 4's tie
            # in prose -- *the next run inherits an ordering rather than
            # re-reading a tie* -- and `CLAIMS` went on registering the tie
            # for a day, so the next run would have broken it a third time
            # and a session rediscovered a decision already taken. The
            # rewrite obligation was already stated and was the half that
            # got done; this names the half that did not.
            print('  A BROKE obliges the paragraph above its reading to be'
                  ' rewritten rather than')
            print('  requoted -- and where the rewrite RETIRES the'
                  ' registration rather than')
            print('  recording a movement, `CLAIMS` in this script is where'
                  ' that lands. Prose')
            print('  alone leaves the next run testing the prediction this'
                  ' one replaced.')
    print('\nclaim 7 -- allocation: no pair; read it with'
          '\n  ./read-run.py BASIS.json --compare OTHER.json --alloc')
    print('claim 8 -- structural: no pair; read the fast tier off the table'
          '\n  and check the gap to bq-gen is populated.')
    print('\nA verdict answers the registered predicate and nothing more.'
          '\nWhether a HELD margin moved against the run before, and whether'
          '\na movement clears the floor, are still the reading\'s to say.')


CLAIMS_HEAD = re.compile(r'#+ The claims Run \d+ should test')
CLAIMS_FIG = re.compile(r'\b\d+(?:\.\d+)?e-\d+\b|\b\d+\.\d{2,4}\b'
                        # `3 of 3 registered orderings held` is the installed
                        # line's verdict, not one of its win counts.
                        r'|\b(\d+) (?:wins )?of (\d+)\b(?! registered)')
def claims_past(run_now=None):
    """A sentence attributing its figures to a run OTHER than this one.

    `Run \\d+` matched any run number, this one included, so a verdict
    sentence opening "In Run 15, `bq-expand` reads 0.9312" exempted every
    figure in itself -- and a stale CURRENT-run figure, which is the one
    kind this sweep exists to catch, was the kind it could not see. The
    run in hand is excluded when the README names it; with no such heading
    the old behaviour stands, which is a sweep that lists less rather than
    one that lists wrongly. Found 2026-08-17 by review.
    """
    return re.compile((r'Run \d+' if run_now is None
                       else r'Run (?!%d\b)\d+' % run_now)
                      + r'|(?:last|previous|earlier|prior)\s+(?:\w+\s+)?runs?')


def main_set_gap(shapes, main_hs):
    """(missing, total): how far a run falls short of the main set.

    Every claims path is registered over the main set, and until
    2026-08-16 none of them noticed a run that was not it. The arms guard
    does not catch it: a one-shape run keeps all 47 arms. What a smoke run
    produced instead was two BROKE verdicts and a forty-item worklist
    against a README with nothing wrong with it, and, on the install path,
    an `IndexError` out of a `best two cells` that had one -- a crash the
    caller then read as the refusal it was waiting for.
    """
    dims = dims_by_shape(main_hs)[0]
    whole = {s for s, d in dims.items() if d['lst'] in MAIN_LISTS}
    return len(whole - set(shapes)), len(whole)


def claims_section(paras):
    """Where the verdict subsection starts and ends, in a paragraph list.

    The installer and the read-back both need it and neither may guess:
    the restatement below `Restated` carries figures of its own, and a
    paragraph leading with a claim's number occurs outside the section
    too, so a search over the whole README finds the wrong one rather than
    none. Returns (None, None) when either end is missing, which every
    caller reports rather than working around.
    """
    start = next((i for i, p in enumerate(paras)
                  if CLAIMS_HEAD.match(p.lstrip())), None)
    if start is None:
        return None, None
    end = next((i for i in range(start + 1, len(paras))
                if paras[i].lstrip().startswith('Restated')), None)
    return (start, end) if end is not None else (None, None)


def claims_readings(cells, shapes, strategies):
    """Each claim's figures, as the paragraph the README is to carry.

    The claims section was the last figure-bearing block with no
    installer, so a run hand-copied a dozen orderings out of `--claims`
    and the transcription was where the wrong figure got in. What is
    installed is the arithmetic and nothing else -- per link the paired
    geomean, the win count and the sign p, then how many registered
    orderings held -- on the same division the class blocks keep: the
    reader writes the sentence a predicate can write, the author writes
    the comparison with the run before and the judgement of whether a
    movement clears the floor.

    Claim 9's expectation is its two best cells rather than a direction,
    so its reading names them; a claim with no live pair is absent from
    what this returns, having no arithmetic to install.
    """
    out = {}
    for n, live in claim_readings(cells, shapes, strategies).items():
        bits, broke = [], []
        for x in live:
            bit = ('`%s` / `%s` %.4f, %d of %d, sign p %.2g'
                   % (x.a, x.b, x.g, x.k, x.m, x.p))
            if x.best is not None:
                bit += ', best two cells %s' % ' and '.join(
                    '`%s`' % s for s in x.best)
            if not x.ok:
                broke.append('`%s` / `%s`' % (x.a, x.b))
            bits.append(bit)
        verdict = ('%d of %d registered ordering%s held'
                   % (len(bits) - len(broke), len(bits),
                      '' if len(bits) == 1 else 's'))
        if broke:
            verdict += ', BROKE on ' + ' and '.join(broke)
        out[n] = '**Readings:** %s. %s.' % ('; '.join(bits), verdict)
    return out


def install_readings(readme, texts, src, strategies, shapes, main_hs):
    """Install each claim's Readings paragraph under its lead, or refuse.

    The lead is the author's `**Claim N` paragraph and the reading goes
    directly beneath it, which is the class blocks' arrangement and is
    matched the same way -- exactly one lead per claim inside the verdict
    section, or this exits rather than guessing. A claim whose reading is
    missing gets one inserted and said so on the way out, the case five
    class blocks silently lost their per-shape line to.

    A filtered run is refused outright: `--exclude` can leave a claim's
    arms out, and a section installed from it would carry a subset with
    nothing in the README saying so.

    Born checked, 2026-08-16, against a copy, four ways: run twice it
    leaves the file byte-identical the second time; with `**Claim 3 held.`
    renamed it exits 1 naming that claim and writes nothing; with claim 2's
    Readings paragraph deleted it reinserts that one alone and says so,
    restoring the file byte-identical; and under `--exclude bq-mut` it
    exits 1 naming the arm rather than installing six claims of seven.
    """
    missing = sorted({a for _, _, ps in CLAIMS for p in ps for a in p[:2]
                      if a not in strategies})
    if missing:
        sys.exit('--in-place: %d claim arm(s) are not in this run (%s); a'
                 ' filtered run cannot install the claims'
                 % (len(missing), ', '.join(missing)))
    gone, whole = main_set_gap(shapes, main_hs)
    if gone:
        sys.exit('--in-place: this run carries %d of the main set\'s %d'
                 ' shapes; the claims are registered over the whole of it,'
                 ' so a shape-filtered run cannot install them'
                 % (whole - gone, whole))
    with open(readme) as f:
        paras = f.read().split('\n\n')
    flat = [' '.join(p.split()) for p in paras]
    start, end = claims_section(flat)
    if start is None:
        sys.exit('--in-place: no claims verdict section in %s, so there is'
                 ' nothing to install into' % os.path.basename(readme))
    done = added = 0
    for n in sorted(texts):
        lead = [i for i in range(start + 1, end)
                if re.match(r'\*\*Claims? %d\b' % n, flat[i])]
        if len(lead) != 1:
            sys.exit('--in-place: %d paragraph(s) in the claims section lead'
                     ' with **Claim %d, need exactly one' % (len(lead), n))
        i = lead[0]
        if i + 1 < end and flat[i + 1].lstrip('*').startswith('Readings:'):
            if flat[i + 1] != texts[n]:
                paras[i + 1] = flat[i + 1] = texts[n]
                done += 1
        else:
            paras.insert(i + 1, texts[n])
            flat.insert(i + 1, texts[n])
            end += 1
            added += 1
            sys.stderr.write('claim %d: Readings paragraph ADDED, the claim'
                             ' had none\n' % n)
    with open(readme, 'w') as f:
        f.write('\n\n'.join(paras))
    sys.stderr.write('installed at %s from %s, %d claim reading(s) rewritten'
                     ' and %d added, of %d\n'
                     % (os.path.basename(readme), os.path.basename(src),
                        done, added, len(texts)))


def claims_in_doc(readme, cells, shapes, strategies, src, main_hs):
    """Figures in the claims verdicts that this run's readings do not give.

    The installer writes each claim's readings; this asks the other
    question, whether a figure the AUTHOR wrote beside them is this run's.
    On 2026-08-15 a write-up shipped a whole verdict section of the
    previous run's figures with every checker green, and no installer
    reaches that: the sentence is the author's and stays the author's.

    A figure earns its place three ways -- it is one of its own claim's
    readings (paired geomean, published-column ratio, win count, sign p),
    it is a percentage, or its sentence attributes it, naming a run or
    saying "the last two runs". Everything else is listed. Attribution is
    by paragraph lead, so a continuation paragraph is read against the
    claim above it, and a claim with no live pair is skipped whole, its
    figures being the table's rather than a pair's.

    It lists rather than fails, and the summary count is the instrument
    rather than the list: a clean README reproduces nearly everything and
    leaves a handful of table-sourced cells, where a stale one collapses.

    The installed readings are checked too, not skipped as trivially this
    run's: a README whose `Readings:` lines were never reinstalled is exactly
    the failure this exists for, and it is the densest evidence of it.

    Non-vacuity, 2026-08-16, three readings over Run 14's artifacts. The
    README reproduces 44 and lists nothing -- after the one figure it did
    list was fixed, an unattributed Run 13 sign p inside claim 2's
    paragraph, which is this check's first find and exactly the kind the
    README's own convention forbids. Run 13's published README against the same
    artifacts, which is the shape the 2026-08-15 incident had, reproduces
    17 and lists 17. And the control half read in place of the basis
    reproduces 9 and lists 35, which is why the basis is a caller's
    argument here as it is everywhere else in this README.
    """
    gone, whole = main_set_gap(shapes, main_hs)
    if gone:
        print('\nnote: this run carries %d of the main set\'s %d shapes, so'
              ' the README\'s figures are not comparable with it and were not'
              ' read back. Nothing here is a finding about the README.'
              % (whole - gone, whole))
        return
    try:
        doc = open(readme).read()
    except OSError as exc:
        print('\nnote: %s unread, so the claims section went unchecked: %s'
              % (os.path.basename(readme), exc))
        return
    paras = [' '.join(p.split()) for p in doc.split('\n\n')]
    start, end = claims_section(paras)
    if start is None:
        print('\nnote: no claims verdict section in %s, so this check did'
              ' not happen rather than passing'
              % os.path.basename(readme))
        return

    # The same arithmetic the printer and the installer use, and formatted
    # here the way they format it: this check matches the README on the
    # STRING, so a format that moved in the writer and not here would stop
    # the read-back recognising figures it had just written -- or leave it
    # passing while checking a shape nothing emits.
    readings = {}
    for n, live in claim_readings(cells, shapes, strategies).items():
        figs = set()
        for x in live:
            figs.add('%.4f' % x.g)
            figs.add('%d of %d' % (x.k, x.m))
            figs.add('%.2g' % x.p)
            if x.pub is not None:
                figs.add('%.4f' % x.pub)
        readings[n] = figs

    # The paragraphs above the first claim are the section's own summary,
    # and they quote figures too -- the movement that is the run's reading.
    # They are read against every claim's figures rather than one's.
    every = set().union(*readings.values()) if readings else set()
    now = re.search(r'^## About the last run \(Run (\d+)\)$', doc, re.M)
    past_re = claims_past(int(now.group(1)) if now else None)
    ok, listed, skipped, claim = 0, [], set(), None
    for para in paras[start + 1:end]:
        lead = re.match(r'\*\*Claims? (\d+)', para)
        if lead:
            claim = int(lead.group(1))
        if claim is not None and claim not in readings:
            skipped.add(claim)
            continue
        allowed = every if claim is None else readings[claim]
        for sent in re.split(r'(?<=[.!?]) (?=[A-Z*`(])', para):
            past = past_re.search(sent)
            for m in CLAIMS_FIG.finditer(sent):
                if sent[m.end():m.end() + 1] == '%':
                    continue
                fig = ('%s of %s' % (m.group(1), m.group(2))
                       if m.group(1) else m.group(0))
                if fig in allowed:
                    ok += 1
                elif not past:
                    listed.append((claim, fig, sent))
    # Name the file the readings came from. A run pointed at the control
    # half lists two dozen figures as unaccounted, which is what a stale
    # section looks like too -- and the cure for one is to rewrite two
    # dozen correct sentences, so the two must not print alike.
    print('\n%d figure(s) in the verdicts are the readings of %s.'
          % (ok, os.path.basename(src)))
    if skipped:
        print('claim%s %s ha%s no live pair here, so what %s quote%s is the'
              ' table\'s and goes unchecked by this.'
              % ('' if len(skipped) == 1 else 's',
                 ' and '.join(str(n) for n in sorted(skipped)),
                 's' if len(skipped) == 1 else 've',
                 'it' if len(skipped) == 1 else 'they',
                 's' if len(skipped) == 1 else ''))
    if not listed:
        print('note: no unattributed figure left over.')
        return
    print('note: %d figure(s) neither this run\'s nor attributed to another'
          ' run; adjudicate each:' % len(listed))
    for n, fig, sent in listed:
        print('        %-9s %-9s %s'
              % ('summary' if n is None else 'claim %d' % n, fig, sent[:92]))


# The regime 3 fix became `mut-odo-vecdims` by the decision of 2026-08-22
# (README, the ceiling), `bq-expand` the last candidate; the pure/impure
# distinction retired with it, and the summary's pure slot now carries the
# best arm OUTSIDE the vecdims family -- the stride-conditioned redirect's
# candidate per class.
SUMMARY_COLS = ('shapes', 'mut-odo-vecdims', 'worst', 'best outside family',
                'ceiling', 'floor')
FAMILY = 'mut-odo-vecdims'
PROP2_FASTEST = 'mut-odo-vecdims'
FIX = 'mut-odo-vecdims'
LAST_CANDIDATE = 'bq-expand'


BREAK = collections.namedtuple('BREAK', 'g k n p')


def break_margin(cells, shapes, a, b):
    """`a` against `b` paired, or None where a cell is not readable.

    A verdict clause below is a SORT of the published column, and a sort
    answers *which is ahead* with no width at all. Run 15 published seven
    breaks off one and five of them were ties inside their own
    population's floor; a sixth, `revsome`, INVERTED when the two arms
    were read paired -- `bq-scan-rem-gm-mulback` leading at 1.0469 where
    the column had it behind. So the sort stays, the claim being stated
    on the published column, and what it reports is priced beside it.

    Not `pair_stats`: that exits 2 on an unreadable cell, which is right
    for a mode whose whole output is the pair and wrong for one clause of
    a verdict block -- the run would lose its table over a control it was
    not asked about. The reading is dropped instead, and the caller says
    which pair went.
    """
    if any(not cells[s][x]['net'] > 0 for s in shapes for x in (a, b)):
        return None
    r = [cells[s][a]['net'] / cells[s][b]['net'] for s in shapes]
    k = sum(1 for x in r if x < 1)
    return BREAK(geomean(r), k, len(r), sign_p(k, len(r)))


def priced_break(cells, shapes, a, b, floor):
    """The lines that price one break, `a` leading `b` by the column.

    Three readings, and the third is the one a sort cannot give: the
    paired margin, how it compares with this population's own floor, and
    whether the pair reads the other way round from the column. A margin
    inside the floor is a tie the sort settled, which is what five of Run
    15's seven breaks were and what a falling count of them was quoted as
    a trend on.

    It prices and does not rule: INSIDE is a comparison of two numbers,
    and what a tie means for the class's paragraph stays the author's,
    as everything else in this block does.
    """
    m = break_margin(cells, shapes, a, b)
    if m is None:
        return ['     not priced: a cell of `%s` or `%s` has no positive net'
                % (a, b)]
    out = ['     priced: `%s` / `%s` %.4f paired, ahead on %d of %d shapes,'
           ' sign p %.2g' % (a, b, m.g, m.k, m.n, m.p)]
    dev = abs(m.g - 1) * 100
    if floor is None:
        out.append('       margin %.2f%%, against no floor: this run carries'
                   ' no readable A/A pair' % dev)
    else:
        fl = abs(floor.g - 1) * 100
        out.append('       margin %.2f%% against this class\'s floor of'
                   ' %.2f%% (`%s`), so it is %s the floor'
                   % (dev, fl, floor.a, 'INSIDE' if dev < fl else 'OUTSIDE'))
    if m.g > 1:
        out.append('       and the pair INVERTS the column: paired, `%s` is'
                   ' behind `%s`' % (a, b))
    return out


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
    `bcastmid` and `slice`, so it is not a constant. Since 2026-08-22 the
    second clause is gone with the pure slot, and the third reads the last
    candidate behind `mut-odo-vecdims`.

    Every break it reports is PRICED against the population's own floor
    (`priced_break`), which is the difference between a sort and a
    reading: on Run 17's `revsome` the first clause breaks on two arms
    that print 0.049 apiece and read 0.36% apart paired, where that
    class's floor is 18.05%.
    """
    led = table_leaders(cells, shapes, strategies, args)
    if led is None or not led.timed:
        return
    rows, needs, timed, outside = (led.rows, led.needs, led.timed,
                                   led.outside)
    floor = aa_floor(aa_pairs(cells, shapes, strategies))
    unknown = [r.st for r in timed if r.st not in needs
               or needs[r.st].strip() in ('?', '')]
    print()
    print('Verdicts, derived from the cells above; the paragraph is yours:')
    print('  fastest timed arm   %-30s %.3f' % (timed[0][1], timed[0][0]))
    if outside:
        print('  best outside family %-30s %.3f' % (outside[0][1],
                                                     outside[0][0]))
    fix = next((r for r in timed if r[1] == FIX), None)
    if fix:
        print('  %-19s %-30s %.3f   worst %.3f'
              % (FIX, '(the fix)', fix[0], fix[6]))
        print('  property 1, `worst` under 1: %s'
              % ('HOLDS' if fix[6] < 1 else '**BREAKS**'))
        # Priced like the others, on the one cell that breaks it: `worst`
        # is a per-shape ratio and not a pair, so what stands beside the
        # floor is its own excess over 1 rather than a geomean.
        if not fix[6] < 1:
            over = (fix[6] - 1) * 100
            print('     worst is %.2f%% above 1%s'
                  % (over, '' if floor is None else
                     ', against this class\'s floor of %.2f%% (`%s`), so it'
                     ' is %s the floor'
                     % (abs(floor.g - 1) * 100, floor.a,
                        'INSIDE' if over < abs(floor.g - 1) * 100
                        else 'OUTSIDE')))
    clauses = []
    if timed[0][1] != PROP2_FASTEST:
        clauses.append(('fastest is `%s`, not `%s`'
                        % (timed[0][1], PROP2_FASTEST),
                        timed[0][1], PROP2_FASTEST))
    if fix:
        # The third clause since 2026-08-22: the last candidate behind
        # `mut-odo-vecdims`, which is the decision's direction read per
        # class.
        by = dict((r[1], r[0]) for r in timed)
        if LAST_CANDIDATE in by and by[LAST_CANDIDATE] < fix[0]:
            clauses.append(('the last candidate `%s` is AHEAD of `%s`'
                            % (LAST_CANDIDATE, FIX),
                            LAST_CANDIDATE, FIX))
    verdict2 = ('HOLDS' if not clauses
                else '**BREAKS** -- ' + '; '.join(c[0] for c in clauses))
    print('  property 2, top of the table: %s' % verdict2)
    for _, a, b in clauses:
        for line in priced_break(cells, shapes, a, b, floor):
            print(line)
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
             for st in (FIX, LAST_CANDIDATE, 'list')]
    print('  property 3, allocation: %s'
          % ', '.join('%s %s' % (st, '--' if a is None else '%.2fx' % a)
                      for st, a in tiers))
    if unknown:
        print('  `needs` unwritten: %s' % ', '.join(unknown))


def load_other(other, main_hs, shapes, meta):
    """The other run, corrected, or an exit if it is a different population.

    The two `--compare` modes wrote this out identically, exit string and
    all, and `--chapter` had the load without the guard -- and the `b_meta`
    the guard would have used sitting unread, which is how you can tell it
    was meant to be copied along. That mode crossed two populations where
    its siblings refuse, surviving only because the shape intersection
    then comes out empty and it returns after two header lines.

    Correcting always is what `--alloc` used not to do; it reads
    `alloc_bytes` alone, so the correction changes nothing it looks at,
    and a flag for that would be a parameter every caller passes the same.
    """
    b_cells, b_shapes, b_strategies, b_meta = load(other, main_hs)
    # The same hole gate the run in hand gets, and for the same reason one
    # commit later: `--compare`, `--chapter` and `--compare --alloc` index
    # the other run's cells directly, so an interrupted half raised a
    # KeyError -- a traceback where this file's convention is a refusal
    # naming what did not happen. Found 2026-08-17 by review.
    holes = [(sh, st) for sh in b_shapes for st in b_strategies
             if st not in b_cells[sh]]
    if holes:
        sys.stderr.write(
            '%s: %d cell(s) missing, so the comparison did not happen. The'
            ' first few: %s\n'
            % (os.path.basename(other), len(holes),
               '; '.join('%s/%s' % h for h in holes[:5])))
        sys.exit(2)
    apply_correction(b_cells, b_shapes, b_strategies)
    mine = population_of(shapes, meta['dims'])[1]
    theirs = population_of(b_shapes, b_meta['dims'])[1]
    if mine != theirs:
        sys.exit('this run is %s and %s is %s: different populations, and no'
                 ' figure crosses between them'
                 % (mine, os.path.basename(other), theirs))
    return b_cells, b_shapes, b_strategies


LEADERS = collections.namedtuple('LEADERS',
                                 'rows needs timed outside fix')


def table_leaders(cells, shapes, strategies, args):
    """The table's rows and who leads it, or None where there is no table.

    `--block` computes this twice per call -- once for the verdicts it
    prints and once for the summary row it checks -- and the second is
    validating the ranking the first printed, so a drift between the two
    copies would make the check disagree with the paragraph it is there
    to police, silently. Each caller keeps its own early return: the
    verdicts want a timed arm, the summary row wants the best arm outside
    the vecdims family and `mut-odo-vecdims` besides.
    """
    rows, have_list = strategy_rows(cells, shapes, strategies)
    if not have_list:
        return None
    needs = {st: n for st, (_, _, n)
             in readme_rows(args.readme, strategies).items()}
    timed = [r for r in rows if not is_control(r.st) and r.time == r.time]
    return LEADERS(rows, needs, timed,
                   [r for r in timed if not r.st.startswith(FAMILY)],
                   next((r for r in timed if r.st == FIX), None))


def summary_row(cells, shapes, strategies, args, main_hs):
    """Check this class's row of the cross-class summary against the cells.

    The summary is the last figure-bearing table with no installer, and it
    is not getting one: its emphasis is a per-run judgement applied by
    hand and already inconsistent -- `scaled`'s pure arm is bold in Run 14
    and was not in Run 13 on the same arm, and `rev`'s is bold in neither
    while naming the same arm as `bcast`'s, which is -- so a renderer
    would have to invent or drop marks that mean something to somebody.
    What it can have is the check the README already asks for: the summary
    is a transcription from the class tables, cell against table, and
    every cell of it is derivable right here. Eight calls a run, one per
    class, riding the `--block` each class already gets.

    It writes to stderr, where `install-tables.sh` collects what a run
    still owes by hand, and it changes no exit code: a wrong cell is for a
    person to fix, and the table is not this mode's to write.

    A run over part of a class is not checked and says so, since every
    figure in the row is over the whole population -- which is what makes
    the smoke sweep's one-shape `--block` silent here rather than wrong.

    Non-vacuity, 2026-08-16: over Run 14's eight class JSONs every cell of
    every row reproduces, so a row this prints nothing for is a row that
    agrees; changing `rev`'s worst to 0.172 in a copy reported that cell
    alone, naming both figures, and the same break driven through
    `install-tables.sh` came out in the list of what the installs left to
    do by hand, which is where a run will meet it.
    """
    dims = dims_by_shape(main_hs)[0]
    lists = {dims[s]['lst'] for s in shapes if s in dims}
    if len(lists) != 1:
        return
    whole = {s for s, d in dims.items() if d['lst'] in lists}
    label = class_prefix(shapes)
    if set(shapes) != whole:
        sys.stderr.write('summary row `%s` not checked: this run carries %d'
                         ' of the class\'s %d shapes\n'
                         % (label, len(shapes), len(whole)))
        return
    led = table_leaders(cells, shapes, strategies, args)
    if led is None:
        return
    timed, outside, fix = led.timed, led.outside, led.fix
    if not (timed and outside and fix):
        return
    aa = aa_pairs(cells, shapes, strategies)
    if not aa:
        return
    want = ['%d' % len(shapes), '%.3f' % fix.time, '%.3f' % fix.worst,
            '%s %.3f' % (outside[0].st, outside[0].time),
            '%s %.3f' % (timed[0].st, timed[0].time),
            '%.2f%%' % (abs(aa_floor(aa).g - 1) * 100)]
    try:
        doc = open(args.readme).read()
    except OSError as exc:
        sys.stderr.write('summary row `%s` not checked: %s\n' % (label, exc))
        return
    hit = [l for l in doc.split('\n') if l.startswith('| `%s` |' % label)]
    if len(hit) != 1:
        sys.stderr.write('summary row `%s` not checked: %d line(s) in %s'
                         ' start it, need exactly one\n'
                         % (label, len(hit), os.path.basename(args.readme)))
        return
    got = [c.replace('**', '').replace('`', '').strip()
           for c in hit[0].strip('|').split('|')][1:]
    # A row that lost a column would otherwise have its tail compared
    # against nothing at all, `zip` stopping at the shortest of the three
    # -- silently, where both guards above this one report. The width is
    # the first thing to check, not a precondition to assume.
    if len(got) != len(SUMMARY_COLS):
        sys.stderr.write('summary row `%s` not checked: it has %d column(s)'
                         ' where the summary takes %d (%s)\n'
                         % (label, len(got), len(SUMMARY_COLS),
                            ', '.join(SUMMARY_COLS)))
        return
    off = ['%s says %s where the cells give %s' % (col, g, w)
           for col, g, w in zip(SUMMARY_COLS, got, want) if g != w]
    if off:
        sys.stderr.write('summary row `%s` disagrees with this class\'s'
                         ' cells: %s\n' % (label, '; '.join(off)))


LEAD_SHAPE_RE = re.compile(r'`([a-z][\w.-]*)`\s*\(`l`\s*(\d+),'
                           r'\s*`sInner`\s*(\d+)')


def lead_shapes(shapes, args, main_hs):
    """Check a class block's bolded lead against the run it stands over.

    The lead is the author's sentence and everything under it is the
    reader's output, which is the shape every defect in this family has:
    a hand-written line above installed content, going stale under it.
    The five class views that gained a third shape on 2026-08-14 still
    had two-shape leads after Run 14's write-up, while the per-shape line
    `--block` installs beneath them named three, and nothing compared the
    two -- `--block` knew both all along.

    Three readings, all mechanical. WHICH shapes, the lead's set against
    the run's. In WHAT ORDER, because the installed per-shape line labels
    its ratios *in the lead's order* and takes that order from the run:
    a lead listing them differently mislabels figures, which is the one
    of the three that no reading of the block can catch. And each `l` and
    `sInner`, against Main.hs, those being hand-copied numbers with no
    other source in the document.

    Stderr and no exit code, like `summary_row` above and for the same
    reason: a stale lead is for a person to fix, and the lead is
    deliberately not this mode's to write.

    A run over part of a class is not checked and says so, the lead being
    a claim about the whole population -- which is what keeps the smoke
    sweep's one-shape `--block` silent here rather than wrong.
    """
    dims = dims_by_shape(main_hs)[0]
    lists = {dims[s]['lst'] for s in shapes if s in dims}
    label = class_prefix(shapes)
    if len(lists) != 1:
        return
    whole = {s for s, d in dims.items() if d['lst'] in lists}
    if set(shapes) != whole:
        sys.stderr.write('lead `%s` not checked: this run carries %d of the'
                         ' class\'s %d shapes\n'
                         % (label, len(shapes), len(whole)))
        return
    try:
        doc = open(args.readme).read()
    except OSError as exc:
        sys.stderr.write('lead `%s` not checked: %s\n' % (label, exc))
        return
    # The same paragraph unit and the same lead pattern `install-tables.sh`
    # picks the blocks out with, the dash included: a third way of finding
    # a class block is a third thing to keep in step.
    hit = [p for p in doc.split('\n\n')
           if p.lstrip().startswith('**`%s` ---' % label)]
    if len(hit) != 1:
        sys.stderr.write('lead `%s` not checked: %d paragraph(s) in %s open'
                         ' it, need exactly one\n'
                         % (label, len(hit), os.path.basename(args.readme)))
        return
    text = ' '.join(hit[0].split())
    if 'Shapes:' not in text:
        sys.stderr.write('lead `%s` names no shapes at all: it carries no'
                         ' `Shapes:` sentence, so nothing under it is'
                         ' introduced\n' % label)
        return
    named = LEAD_SHAPE_RE.findall(text.split('Shapes:', 1)[1])
    off = []
    missing = [s for s in shapes if s not in [n for n, _, _ in named]]
    extra = [n for n, _, _ in named if n not in shapes]
    if missing:
        off.append('it does not name %s' % ', '.join('`%s`' % s
                                                     for s in missing))
    if extra:
        off.append('it names %s, which this run does not carry'
                   % ', '.join('`%s`' % s for s in extra))
    if not missing and not extra and [n for n, _, _ in named] != list(shapes):
        off.append('it lists them %s where the run order the per-shape line'
                   ' is installed in is %s'
                   % (', '.join('`%s`' % n for n, _, _ in named),
                      ', '.join('`%s`' % s for s in shapes)))
    for n, l, s_inner in named:
        d = dims.get(n)
        if d and (int(l), int(s_inner)) != (d['l'], d['s_inner']):
            off.append('`%s` is written (`l` %s, `sInner` %s) where Main.hs'
                       ' gives (`l` %d, `sInner` %d)'
                       % (n, l, s_inner, d['l'], d['s_inner']))
    if off:
        sys.stderr.write('lead `%s` disagrees with this class\'s run: %s\n'
                         % (label, '; '.join(off)))


CLASS_READING = collections.namedtuple(
    'CLASS_READING', 'label n fix worst out_st out gap gapp '
                     'ceil_st ceil floor floor_pair')


def class_reading(path, main_hs, args):
    """One class's row of the cross-class summary, off its own cells.

    The same six figures `summary_row` checks a written row against, plus
    the two the row does not carry and a superlative about the eight
    keeps being made on: the gap from the regime 3 fix to the best arm
    outside its family, by the published column AND paired. Run 15 called
    one class's gap the widest of the eight on the column where another's
    is wider on the pair, which is a disagreement no single number can
    show.
    """
    cells, shapes, strategies, meta = load(path, main_hs)
    apply_correction(cells, shapes, strategies)
    kind, label, _ = population_of(shapes, meta['dims'])
    if kind != 'class':
        sys.exit('--extremes ranks the stride classes, and %s is %s'
                 % (os.path.basename(path), label))
    led = table_leaders(cells, shapes, strategies, args)
    if led is None or not (led.timed and led.outside and led.fix):
        sys.exit('%s: no `list` baseline, no timed arm outside `%s` or no'
                 ' `%s` at all, so this class has no row'
                 % (os.path.basename(path), FAMILY, FIX))
    out, ceil, fix = led.outside[0], led.timed[0], led.fix
    m = break_margin(cells, shapes, out.st, fix.st)
    aa = aa_floor(aa_pairs(cells, shapes, strategies))
    return CLASS_READING(class_prefix(shapes), len(shapes), fix.time,
                         fix.worst, out.st, out.time,
                         out.time / fix.time,
                         float('nan') if m is None else m.g,
                         ceil.st, ceil.time,
                         float('nan') if aa is None else abs(aa.g - 1) * 100,
                         '--' if aa is None else aa.a)


def extremes_table(paths, main_hs, args):
    """Who holds each extreme across the class populations, sorted not eyed.

    *Widest of the eight*, *best of the eight*, *tightest floor of the
    eight* are claims about every population at once, and until this mode
    nothing printed them: `--block` sees one class, the cross-class table
    is hand-assembled, and the sort was left to the eye. Run 15 got three
    of them wrong in one draft -- a spread called narrowest where another
    class's is, a gap called widest of the eight on the column where
    another's is wider on the pair, and a best class named before it was
    sorted -- every one caught by an independent reader rather than by a
    check.

    It ranks and installs nothing. The cross-class summary stays
    hand-assembled for the reason `summary_row` gives -- its emphasis is
    a per-run judgement -- and a superlative is a sentence, so what this
    owes the author is the sort under it and not the words.

    Where the column and the paired reading name different holders of the
    same extreme, both are printed and the disagreement is said: that is
    the error Run 15 made, and one number cannot show it.
    """
    rows = [class_reading(p, main_hs, args) for p in paths]
    seen = collections.Counter(r.label for r in rows)
    dup = [c for c, n in seen.items() if n > 1]
    if dup:
        sys.exit('%s named twice, so a rank over these files would count one'
                 ' class as two populations: %s'
                 % ('a class is' if len(dup) == 1 else 'classes are',
                    ', '.join(sorted(dup))))
    print('%d class population(s), and every superlative about them has its'
          ' source here.' % len(rows))
    print('`gap` is `%s` over the regime 3 fix -- what a stride-conditioned'
          ' redirect would' % 'best outside the family')
    print('buy in that class -- by the published column and then paired.')
    print()
    print('%-10s %6s %8s %7s %-26s %7s %8s %8s %7s'
          % ('class', 'shapes', 'fix', 'worst', 'best outside family',
             'gap col', 'gap pair', 'ceiling', 'floor'))
    for r in sorted(rows, key=lambda r: r.label):
        print('%-10s %6d %8.3f %7.3f %-26s %7.2f %8.2f %8.3f %6.2f%%'
              % (r.label, r.n, r.fix, r.worst,
                 '%s %.3f' % (r.out_st, r.out), r.gap, r.gapp, r.ceil,
                 r.floor))
    print()
    print('extremes:')
    # Each line names the holder AND its figure, so a sentence can be
    # written off this without going back to the table above -- which is
    # the step at which Run 15's third error was made.
    for what, key, want, fmt in (
            ('tightest floor', lambda r: r.floor, min, '%.2f%%'),
            ('widest floor', lambda r: r.floor, max, '%.2f%%'),
            ('best for the fix', lambda r: r.fix, min, '%.3f'),
            ('worst for the fix', lambda r: r.fix, max, '%.3f'),
            ('highest `worst` cell', lambda r: r.worst, max, '%.3f'),
            ('best outside the family', lambda r: r.out, min, '%.3f'),
            ('fastest ceiling', lambda r: r.ceil, min, '%.3f'),
            ('narrowest gap, column', lambda r: r.gap, min, '%.2f'),
            ('widest gap, column', lambda r: r.gap, max, '%.2f'),
            ('narrowest gap, paired', lambda r: r.gapp, min, '%.2f'),
            ('widest gap, paired', lambda r: r.gapp, max, '%.2f')):
        hit = want(rows, key=key)
        print(('  %-26s %-11s ' + fmt + '%s')
              % (what, '`%s`' % hit.label, key(hit),
                 '  on `%s`' % hit.floor_pair if 'floor' in what else ''))
    for want in (min, max):
        by_col = want(rows, key=lambda r: r.gap)
        by_pair = want(rows, key=lambda r: r.gapp)
        if by_col.label != by_pair.label:
            print('  the %s gap is `%s` on the column and `%s` paired, so'
                  ' a sentence about it has to say which'
                  % ('narrowest' if want is min else 'widest',
                     by_col.label, by_pair.label))
    return 0


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
    kind, label, prefix = population_of(shapes, meta['dims'])
    if kind != 'class':
        sys.exit('--block is for a stride-class run, and this run is %s'
                 % label)
    if 'list' not in strategies:
        sys.exit('--block needs the `list` baseline in the run')
    # --brief drops the table from the TERMINAL: --in-place installs it
    # from this same computation, so a session that is installing has no
    # use for the copy on its terminal, and it is the bulk of what this
    # mode prints. It is therefore still emitted when installing, and
    # `emit_or_install` is what keeps it off stdout there -- dropping it
    # from the computation instead made the very combination the module
    # docstring recommends, `--block --in-place --brief`, exit 1 with
    # `--in-place: this mode emitted no table`. Found 2026-08-17 by review;
    # that call now installs the class's 49 rows over a copy that already
    # carries them, leaving it byte-identical, and prints no table row.
    if args.in_place or args.verbose:
        markdown_table(cells, shapes, strategies, meta, args, terms)
        print()
    aa_table(cells, shapes, strategies, terms, meta, not args.verbose)
    controls_skeleton(cells, shapes, strategies, terms)
    dims = meta['dims']
    anchor = max(shapes, key=lambda sh: dims.get(sh, {}).get('l', 0))
    print()
    print('**Provenance:** elapsed ___, peak ___ MiB in use, ___ MiB max'
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
        print("**Per shape, in the lead's order (%s):**" % ', '.join(shapes))
        for st in bold:
            # `--` on a sunk cell, as the fingerprint and `time_of` do: this
            # paragraph is installed into the README by install-tables.sh, so
            # a ratio taken over a net the forcing term did not leave
            # positive would be published rather than merely printed.
            print('  `%s` %s' % (st, '/'.join(
                '--' if cells[sh][st]['net'] <= 0
                or cells[sh]['list']['net'] <= 0
                else '%.3f' % (cells[sh][st]['net'] / cells[sh]['list']['net'])
                for sh in shapes)))
    # ITEM 5 OF THE FORM, and mechanical to the word: how many of the
    # population's arms move, which way, and the spread. Emitted only
    # when the other half is given, a class block on a run that recorded
    # one half having no such line to write. It also answers the question
    # Run 18 had to notice by hand -- whether `list` moved far enough
    # between the halves that the two columns cannot be differenced at
    # all -- which on that run disqualified four of the eight and was
    # visible in no other output.
    if getattr(args, 'compare', None):
        b_cells, b_shapes, b_strategies = load_other(args.compare,
                                                     args.main, shapes, meta)
        both_sh = [sh for sh in shapes if sh in b_shapes]
        rows, lst = [], None
        for st in strategies:
            if no_net(st) or st not in b_strategies:
                continue
            rs = [cells[sh][st]['net'] / b_cells[sh][st]['net']
                  for sh in both_sh
                  if cells[sh][st]['net'] > 0 and b_cells[sh][st]['net'] > 0]
            if rs:
                g = geomean(rs)
                rows.append((g, st))
                if st == 'list':
                    lst = g
        if rows:
            lo = min(rows)
            hi = max(rows)
            below = sum(1 for g, _ in rows if g < 1)
            print()
            print('**Across the halves:** %d of the %d arms are faster'
                  ' on this half and %d'
                  % (below, len(rows), len(rows) - below))
            print('slower, at a geomean of %.4f, from `%s` at %.4f to `%s`'
                  ' at %.4f,' % (geomean([g for g, _ in rows]), lo[1], lo[0],
                                 hi[1], hi[0]))
            if lst is not None:
                print('with `list` itself at %.4f.' % lst)
                if abs(lst - 1) > 0.007:
                    print('**The baseline moved %.2f%% between the halves,'
                          ' past the 0.7%% that lets two'
                          % (abs(lst - 1) * 100))
                    print('columns be differenced, so this line is NOT read'
                          ' for the pair\'s variable.**')
                    print('The table above is one process\'s and stands;'
                          ' what goes is the comparison.')

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


FIGURE_RE = re.compile(r'\b0\.\d{3}\b|\d+\.\d+\s*[x]\b'
                       r'|\b\d{1,2}\.\d%|\b\d+\.\d{2,}\b')

# A sentence quoting a figure this README no longer publishes. Each has to earn
# its place -- README's own rule is that a superseded NUMBER is cut while a
# superseded DECISION is kept, and the test is whether someone would redo the
# work without it. That is a judgement, so these are listed for adjudication
# rather than failed: the check exists because the rule fires while writing
# and needs something that fires while reviewing. Main.hs comments are swept
# too, since Run 7's write-up put its hard cases exactly there -- the one
# file the sweep did not then read.
# The fingerprint's `list`, net cell, as its own emitter writes it: one
# definition, so that --machine parses what fmt_abs produces and --selftest
# can hold the pair together. A change to either alone is what would leave
# the machine check with nothing to compare and no complaint.
UNIT = {'ns': 1e-9, 'us': 1e-6, 'ms': 1e-3, 's': 1}
FINGERPRINT_ABS_RE = re.compile(r'\|\s*`([^`]+)`\s*\|[^|]*\|[^|]*\|\s*'
                                r'([\d.]+)\s*(ns|us|ms|s)\s*\|')


COMPARATIVE_RE = [re.compile(p, re.I) for p in (
    r'where (?:Failed )?Run \d', r'where it (?:read|had|was)',
    r'\bwas \d+[\d.]*[%x]?\b', r'had (?:read|been|put)',
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


# A tool of this directory, or a mode of one, named inside a comment of an
# indented block. Cabal's and GHC's flags are deliberately absent: a build
# recipe explains those and does not invoke them here.
BURIED_RE = re.compile(r'\./(?:read-run\.py|loop-offsets\.py|run-gate\.sh'
                       r'|run-major\.sh|smoke-sweep\.sh|\$R-)'
                       r'|(?<![\w-])--(?:survey|in-place|para|compare'
                       r'|machine|claims|steps|alloc)(?![\w-])')


def buried_actions(lines):
    """[(line number, comment)] for actions stated only in a comment.

    An operator RUNS the command lines of a checklist and READS the
    comments around them, so an action that appears only in a comment is
    one nobody has to do. Three did on 2026-08-15, in one list: the two
    compiles, `--survey`, and the roster pass. Each was present, each was
    prose, and a session took the list to the end without them.

    Scoped to indented blocks, and satisfied when the same tool or mode
    appears on a command line of the SAME block -- a comment explaining a
    flag the block also runs is explanation and not a buried action, which
    is what keeps `--library` and `--in-place` off this list.

    Listed rather than failed, like the other sweeps here and for the same
    reason: whether a mention instructs or explains is a reading. The rule
    fires while writing and this fires while reviewing.

    Non-vacuous 2026-08-15, against the pre-run list as it stood at
    3dd0060 that morning: four hits, `--survey`, `./run-gate.sh`, the
    gate's two `--compare` readings and `./read-run.py --para`, every one
    of them an action a session had to supply for itself, and nothing else
    anywhere in the file. All four are command lines now and it reads
    zero. What it does NOT reach is the fifth, the compiles: their recipe
    is cabal's and GHC's flags, which are excluded here because a build
    recipe explains those rather than invoking them, and the recipe itself
    lives in the pair note by design. That one was caught by reading.
    """
    out, block, first = [], [], 0
    # The sentinel that flushes a block still open at EOF is None and not
    # '': a blank line is part of an open block, so the empty one was
    # appended to the very block it was there to flush and the flush below
    # never ran. A buried action in a document's last indented block was
    # therefore never reported -- today's README passes this sweep only
    # because it does not end in one. Found 2026-08-17 by review, and
    # non-vacuous the same day: a copy with one such block appended reads
    # one hit here and none through the version before this.
    for i, line in enumerate(lines + [None], 1):
        if line is not None and (line.startswith('    ')
                                 or (not line.strip() and block)):
            if not block:
                first = i
            block.append(line)
            continue
        if block:
            cmds = '\n'.join(l for l in block
                             if not l.lstrip().startswith('#'))
            for j, l in enumerate(block):
                if not l.lstrip().startswith('#'):
                    continue
                for m in BURIED_RE.finditer(l):
                    if m.group(0) not in cmds:
                        out.append((first + j, l.strip()))
                        break
            block = []
    return out


def unwrapped_paragraphs(lines):
    """[(first line, paragraph, spans)] with each paragraph on one line.

    Cached on the text, one `--check-doc` asking for it four times -- once
    in the roster-count block and once per sweep -- and each spawning
    `wrap80` over the whole README. What the cache buys is the one
    definition rather than the milliseconds.

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
    return _unwrapped('\n'.join(lines))


@functools.lru_cache(maxsize=4)
def _unwrapped(text):
    lines = text.split('\n')
    try:
        flat = subprocess.run(['wrap80', '--unwrap'], input=text,
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


# The word count past which an ANSWERED entry has stopped being an answer
# and become an account. LENGTH ALONE, and the history is why: this began
# as length AND the absence of a pointer, on the reasoning that an entry
# naming where its account lives has earned its length. That clause was
# not a filter but an off switch. This README cross-references
# constantly, so every long entry names a link or a file, and the sweep
# flagged NOTHING -- zero of the fourteen entries past 300 words, zero at
# every threshold up to 1400.
#
# It also keyed on the wrong signal. The churn entry is 1818 words of
# SUMMARY whose measurements live in four files it names, which is
# exactly the answer-become-a-chapter the rule was written for, and
# naming those files exempted it: the rule failed on its own motivating
# example. Whether a named file is the account's home or a passing
# mention cannot be decided mechanically, and an undecidable clause in a
# filter means the filter does not filter.
#
# So the pointer went, and 500 with it: 300 lists fourteen of the
# twenty-seven, which is the wall this file's own freshness marks exist
# because of, and 800 lets a chapter through. What carries the standing
# list instead is `sweep`'s NEW-first marking, as it carries the
# superseded-figure and superlative lists -- a write-up owes the ones it
# just wrote, and the run registrations keep their exemption in prose,
# adjudicated once by a reader rather than guessed at here.
ANSWERED_ACCOUNT = 500

# The one family the length rule does not reach, matched on the lead the
# seven of them share. A run registration is long because it is the ONLY
# copy -- the run chapter is replaced every run and the yardstick keeps
# one geomean per strategy per half, where a registration's answers are
# half-against-half and control readings no table here carries -- which
# is the ruling in the open list's preamble and the reason these were
# adjudicated by hand every time the sweep listed them. Skipped and
# COUNTED, never dropped in silence: the count rides with the sweep's
# own line, so a reader sees what the rule did not look at.
#
# Keyed on the lead because the family already had a canonical one and
# six of seven used it verbatim; Run 10's said `Run 10's predictions,
# and how they came out` and was normalised to it, its own text calling
# them registrations. A member that drifts out of the phrasing loses the
# exemption and gets listed, which is the failure a reader can see.
REGISTRATION_RE = re.compile(r'^(?:- |\d+\. )`\w+` \*\*What Run \d+ was'
                             r' built to answer')

# The second exemption, and the one that lets the rule GATE rather than
# list: an answer whose evidence nothing else records has nowhere to be
# moved to, so an entry saying so in a bolded clause is passed over. Bolded
# because the phrase has to be a ruling and not a passing use -- this file's
# own prose says `the only copy there is` about the registrations -- and the
# failure message names the form, so the way out is read off the failure
# rather than guessed at.
ONLY_COPY_RE = re.compile(r'\*\*[^*]*only copy[^*]*\*\*')


def status_entries(lines, tag):
    """[(line number, whole entry)] for each entry of the list tagged TAG.

    An entry is its opening line plus every indented line under it, blank
    lines included where an indented one follows, which is how this README
    writes a multi-paragraph item. Grouped from the raw lines rather
    than from `unwrapped_paragraphs`, because a bullet list with no blank
    lines between its items is ONE paragraph to that function -- the whole
    open list would come back as a single hit, which is the granularity
    this needs least.

    BULLETS AND NUMBERED ITEMS BOTH, since `Recommended tasks after Run
    N` numbers its three: read for bullets alone this saw the parent list
    and neither sublist's neighbour, so the one subsection whose items
    are a checklist was the one no check reached. A numbered item's
    continuations are indented three rather than two, which the test
    below already admits.
    """
    out, i, n = [], 0, len(lines)
    while i < n:
        if not re.match(r'^(?:- |\d+\. )`%s` ' % tag, lines[i]):
            i += 1
            continue
        start, body, j = i + 1, [lines[i]], i + 1
        while j < n:
            if lines[j].startswith('  '):
                body.append(lines[j].strip())
                j += 1
            elif not lines[j].strip():
                k = j
                while k < n and not lines[k].strip():
                    k += 1
                if k < n and lines[k].startswith('  '):
                    j = k
                else:
                    break
            else:
                break
        out.append((start, ' '.join(body)))
        i = j
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
# checkout it sits in, then the sibling this README cites for horde-ad's
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
    slash, which is the whole design: this README backticks criterion bench
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
    nothing. Here it is one check among several about the README's internal
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
        # A prefix, not a character set: `lstrip('./')` ate the leading dot
        # of `.github/workflows/lint.yml` and both levels of `../orthotope`,
        # so the first dotfile or parent-relative path this README cites would
        # have hard-FAILED as a path that does not resolve. Found 2026-08-17
        # by review; neither is in the README today, which is why nothing
        # noticed.
        rel = tok[2:] if tok.startswith('./') else tok
        if TRANSIENT_RE.match(rel):
            out['transient'].append(tok)
            continue
        gone = []
        for root, label in PATH_ROOTS:
            base = os.path.join(here, root)
            if not os.path.isdir(base):
                gone.append(root)
                if not out['unmounted_root']:
                    out['unmounted_root'] = root
                continue
            if os.path.exists(os.path.join(base, rel)):
                out['ok'].append(tok)
                out['in_sibling'] += label == 'horde-ad'
                break
        else:
            # A name searched while a root was missing cannot be told from
            # a name that is simply wrong -- most of the sibling's own
            # files are named without its prefix, so the token says
            # nothing about which root it wanted. So this classifies and
            # `check_doc` REFUSES on the class: an unmounted root blocks
            # the path check rather than excusing what it could not
            # search, which is what a missing sibling used to do silently
            # for every later name, a dead local reference included.
            if gone:
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

    Over HEAD and not over the index, which is what the sentence above
    says and what `git diff` alone does not do: staging README before
    running --check-doc emptied this -- to the empty set, not to
    EVERYTHING -- and all four freshness sweeps then reported "none added
    by this diff" over a diff that had added plenty, which is the failure
    `is_fresh` records having been repaired. Found 2026-08-17 by review,
    and non-vacuous the same day: with a pasted superlative paragraph
    STAGED, `git diff -U0` reads empty where `git diff HEAD -U0` reads the
    paste, and --check-doc prints it under NEW here and not through the
    version before this.

    Returns EVERYTHING when there is no diff to be had -- not a git
    checkout, git absent, or the file untracked -- so the caller falls back
    to the flat listing rather than announcing that nothing is new. The
    last of the three is asked outright, with `ls-files --error-unmatch`,
    because `git diff` does not answer it: pointed at an untracked path it
    exits 0 saying nothing, which is the empty set and not the sentinel,
    so `--check-doc --readme` on an untracked copy -- the way a document
    is worked on before it is added -- called every hit old. The sentence
    above has claimed otherwise since the sentinel was written; measured
    and made true 2026-08-17.

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

    **BOTH SIDES ARE NORMALISED BEFORE THEY ARE COMPARED, and the whole
    attribution used to die without it.** This ran `git diff HEAD` raw,
    which compares a WORKING TREE that --check-doc's own wrap FAIL tells
    you to unwrap against a HEAD that stores the wrapped form -- so every
    paragraph that had spanned more than one line was a line that did not
    exist before, and read as added. Measured on Run 17's document: of 2046
    unwrapped lines, 731 read as added, 82.9% of the 882 paragraphs that had
    been wrapped, and the sweeps then marked 102 of 105 superlatives, 65 of
    75 superseded figures and 27 of 27 absolute times NEW, lines no session
    had touched among them. That is precisely the failure the feature exists
    to prevent, and the docstring above cites Run 11 shipping four false
    superlatives inside a list of 71 because *a wall of 71 gets adjudicated
    as a wall* -- a wall of 102 is no better. So the comparison is at
    PARAGRAPH granularity with whitespace collapsed on each side, which is
    exactly what a re-wrap changes and all it changes: a paragraph merely
    re-wrapped has the same key on both sides and contributes nothing, and
    one whose words moved contributes its own physical lines, in whichever
    form the working tree holds them, so `is_fresh` matches as it always
    did. The working form is now free, which is what the wrap advice
    assumed.

    Coarser than the `-U0` diff it replaces, and deliberately: an edit
    anywhere in a paragraph now marks the whole paragraph. A hit IS a
    paragraph, so the granularity the caller tests at has not changed, and
    the direction of the error is the one this docstring already accepts.

    Non-vacuous, 2026-08-22, on this document in both forms: with one
    paragraph of the Run 17 chapter edited, this returns THAT PARAGRAPH and
    nothing else from either tree -- its four lines from the wrapped one and
    its single line from the unwrapped one -- where the version before this
    returned 2 lines from the wrapped tree and 734 from the unwrapped one,
    the whole document. On the clean tree both versions return the empty
    set, which is the control saying the 734 were the form and not the edit.
    And `added-lines-over-head` is the case that holds the tracked-but-not-
    -in-HEAD branch: it failed the moment `git diff` went, which is how that
    branch was found rather than reasoned about.
    """
    at = os.path.dirname(os.path.abspath(__file__))
    try:
        known = subprocess.run(['git', 'ls-files', '--error-unmatch', '--']
                               + list(paths), cwd=at,
                               capture_output=True, text=True, timeout=20)
        if known.returncode != 0:
            return EVERYTHING
        added = set()
        for path in paths:
            rel = os.path.relpath(os.path.abspath(path), at)
            was = subprocess.run(['git', 'show', 'HEAD:./' + rel], cwd=at,
                                 capture_output=True, text=True, timeout=20)
            # A REFUSAL HERE IS NOT THE SENTINEL'S CASE, because `ls-files
            # --error-unmatch` has already answered above: the file is
            # tracked, so git works and the checkout is real, and the one
            # way `git show HEAD:` can still refuse is that HEAD has no
            # such path -- a file ADDED and not yet committed, whose every
            # paragraph really is new. Its HEAD copy is the empty document
            # and not an unknown. Returning EVERYTHING instead made the
            # `added-lines-over-head` case fail the moment this function
            # stopped calling `git diff`, which reports a whole new file
            # as added and asks nobody.
            head_text = was.stdout if was.returncode == 0 else ''
            with open(path, errors='replace') as f:
                now = f.read()
            old = {k for k, _ in blocks_of(head_text)}
            for key, lines in blocks_of(now):
                if key not in old:
                    added.update(l.strip() for l in lines if l.strip())
    except (OSError, subprocess.SubprocessError):
        return EVERYTHING
    return frozenset(added)


def head_text_of(path):
    """The committed copy of `path`, or None when there is no answer.

    Split out of `added_lines` so a second check can ask the same
    question without inheriting that one's EVERYTHING sentinel, whose
    meaning is *fall back to the flat listing* and not *the file is new*.
    """
    at = os.path.dirname(os.path.abspath(__file__))
    try:
        rel = os.path.relpath(os.path.abspath(path), at)
        known = subprocess.run(['git', 'ls-files', '--error-unmatch', rel],
                               cwd=at, capture_output=True, text=True,
                               timeout=20)
        if known.returncode != 0:
            return None
        was = subprocess.run(['git', 'show', 'HEAD:./' + rel], cwd=at,
                             capture_output=True, text=True, timeout=20)
        return was.stdout if was.returncode == 0 else ''
    except (OSError, subprocess.SubprocessError):
        return None


def chapter_head_blocks(text):
    """The run chapter's own paragraphs: its heading to the first `###`.

    Not the whole chapter, which runs to the end of the document and
    holds the column definitions, the class-block form and the replace
    list -- all of which deliberately outlive a run and would make this
    check a wall. What is scoped here is the part whose closing sentence
    says every word of it is replaced by the next run.
    """
    m = re.search(r'^## About the last run \(Run \d+\)$', text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r'^#{1,3} ', rest, re.M)
    return blocks_of(rest[:nxt.start()] if nxt else rest)


def blocks_of(text):
    """The blank-line-separated blocks of a document, as (key, lines).

    The key is the block with every run of whitespace collapsed to one
    space. That is what makes it a fixed point of wrapping and of nothing
    else: `wrap80` and `wrap80 --unwrap` move line breaks and no other
    byte, so two copies of one paragraph at two widths share a key, while
    any edit to its words gives it a different one.
    """
    out = []
    for block in re.split(r'\n\s*\n', text):
        lines = [l for l in block.split('\n') if l.strip()]
        if lines:
            out.append((' '.join(' '.join(lines).split()), lines))
    return out


LEAD_RE = re.compile(r'\*\*(.+?)\*\*', re.S)

# How many body-matched paragraphs `--para` prints when no lead matches. The
# lead search is exact enough to print every hit; the body search is not, so
# it is capped and says how many it dropped -- a silent cap would read as
# "that is all there is", which is the failure the no-silent-caps rule names.
PARA_BODY_CAP = 6


def splice(readme, anchor, source):
    """Replace the paragraph carrying `anchor` with the text in `source`.

    The write-up's edits are exact-match replacements, and a session
    doing them by hand pays three times for each: locate the passage,
    PRINT it so the old string can be copied, then send both strings
    back. On Run 16 that echoing was the single largest token cost of
    the write-up, and the README's own rule -- anything this reader can
    emit, a session should not read -- had never been applied to
    editing. This does the whole edit without the old text entering a
    transcript at all.

    Refuses rather than guesses, on the same terms as `install`: the
    anchor must occur exactly once IN THE WHOLE FILE, and the unit
    replaced is the paragraph containing it, never a byte range. It
    echoes the extent and the first and last line of what it is about
    to overwrite, so a wrong anchor is loud before it is written and
    the record of what went says what it replaced.

    **A LIST WITH NO BLANK LINE BETWEEN ITS ITEMS IS ONE PARAGRAPH**, so an
    anchor inside one item names the whole list, and it is refused unless
    the anchor is in the FIRST item -- where quoting the list from its
    start is what a caller replacing all of it would do anyway. Measured
    2026-08-22 in this README's own open list: an anchor naming task 3 took
    tasks 1, 2 and 3 and wrote back task 3 alone, at exit 0. The echo below
    had said so, `out, first` naming task 1 where the anchor named task 3,
    and saying so was not enough -- which is the whole difference between a
    warning and a refusal, and the reason this is the second.

    Wrapping is the caller's: this writes the replacement as given, so
    an edit made against an unwrapped file leaves that paragraph on one
    line, which is what the wrap gate reports as mid-edit and not as a
    failure.
    """
    doc = open(readme).read()
    n = doc.count(anchor)
    if n != 1:
        sys.stderr.write('--replace: the anchor occurs %d times, need 1 --'
                         ' quote more of the sentence\n' % n)
        return 1
    paras = doc.split('\n\n')
    hit = [i for i, q in enumerate(paras) if anchor in q]
    if len(hit) != 1:
        sys.stderr.write('--replace: the anchor spans a paragraph break, so'
                         ' there is no one paragraph to replace\n')
        return 1
    old = paras[hit[0]]
    # A LIST WITH NO BLANK LINES BETWEEN ITS ITEMS IS ONE PARAGRAPH, and
    # this replaces paragraphs -- so an anchor inside one item of the open
    # list's numbered tasks took all three items and wrote back one.
    # Measured 2026-08-22: `--replace '3. **Between Run 17 and Run 18'`
    # replaced items 1, 2 and 3 with item 3 alone, at exit 0. The echo
    # below said so, `out, first` naming item 1 where the anchor names
    # item 3, and saying so was not enough -- which is the difference
    # between a warning and a refusal, and the reason this is the second.
    # Pass the whole list as the replacement, or edit the item in place.
    items = [l for l in old.split('\n')
             if re.match(r'\s*(?:\d+\.|[-*])\s', l)]
    if len(items) > 1 and anchor not in old.split('\n')[0]:
        sys.stderr.write(
            '--replace: this paragraph is a %d-item list and the anchor is'
            ' not in its first item, so replacing it would discard the items'
            ' above -- quote the list from its first item, and pass the whole'
            ' list as the replacement, or edit the one item in place\n'
            % len(items))
        return 1
    new = open(source).read().strip('\n')
    ol, nl = old.split('\n'), new.split('\n')
    print('--replace: %d chars -> %d, in %s'
          % (len(old), len(new), os.path.basename(readme)))
    print('  out, first: %s' % ol[0][:78])
    print('  out, last : %s' % ol[-1][-78:])
    print('  in,  first: %s' % nl[0][:78])
    print('  in,  last : %s' % nl[-1][-78:])
    paras[hit[0]] = new
    with open(readme, 'w') as f:
        f.write('\n\n'.join(paras))
    return 0


def paragraphs(readme, pattern):
    r"""Print the paragraphs whose BOLDED LEAD matches, and their line numbers.

    Retrieval, so that reading a paragraph does not mean finding it first.
    A session working through this README otherwise pairs a `grep -n` with a
    `sed -n` for every passage it wants, and both go stale the moment an
    edit above moves the lines -- which every `--in-place` install and every
    prose fix does. Matching the lead rather than the body is what keeps the
    output one paragraph instead of every line that mentions a word.

    **The README does NOT guarantee the precondition this used to claim.**
    It said every paragraph opens with a bolded lead; of the 868 paragraphs
    this function's own splitter returns, 457 carry a bolded span and 411
    carry none, and 37 of those 411 carry a figure. So a third of a percent
    of the README was not the gap -- a run's own material was. The unbolded
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
    deliberate break landed before believing what it proves. The
    link-text check had no live instance to break, the README having none,
    so it was planted both ways on 2026-08-16, inline and through a
    reference definition, each failing alone; its one false positive is
    this README quoting the defect in backticks, in the entry that asked
    for the check, which is why code spans are blanked first. The two
    agreement checks on Main.hs's counts, the same day and each on a
    copy: one roster-size site changed to 1129 failed naming both sites
    and what Main.hs holds; `over 24 shapes` changed to 25 failed naming
    the count that matches no population; and a site reworded out of its
    pattern failed as unlocatable rather than passing on the one site
    left. The figure sweep's Main.hs half: a planted `where Run 6 read
    0.500` comment was
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

    # A link's TEXT against its anchor, which resolving cannot check: the
    # rename step repoints both and Run 14 shipped four reading `[About
    # the last run (Run 13)](#about-the-last-run-run-14)`, every anchor
    # live and every one of them lying, found by a reader. Inline links
    # here and reference definitions with their uses, plus Main.hs, whose
    # `README.md#` references carry text of their own in the comment
    # around them and are left to the eye.
    # Inline code spans go first: this README QUOTES the defect, in the
    # entry that asked for the check, and a quoted link is not a link.
    nocode = re.sub(r'`[^`\n]*`', '``', doc)
    crossed = [(t, a) for t, a in
               re.findall(r'\[([^\]\n]*\bRun (?:\d+)[^\]\n]*)\]'
                          r'\(#([a-z0-9-]+)\)', nocode)
               if re.search(r'run-(\d+)', a)
               and re.search(r'\bRun (\d+)', t).group(1)
               != re.search(r'run-(\d+)', a).group(1)]
    for key, anchor in refs.items():
        m = re.search(r'run-(\d+)', anchor)
        if not m:
            continue
        crossed += [(t, anchor) for t in
                    re.findall(r'\[([^\]\n]*\bRun \d+[^\]\n]*)\]\[%s\]' % key,
                               nocode)
                    if re.search(r'\bRun (\d+)', t).group(1) != m.group(1)]
    if crossed:
        bad.append('%d link(s) whose text and anchor name different runs: %s'
                   % (len(crossed),
                      '; '.join('%s -> #%s' % (t, a) for t, a in crossed)))
    else:
        note.append('every link naming a run agrees with the anchor it points'
                    ' at')

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
        # A FAIL and not a note. These are names nothing searched, and a
        # name that is simply wrong lands here too -- which is how a dead
        # local reference passed a whole run once a sibling was missing.
        # BLOCKED means the check did not happen, never that it passed;
        # mount the root, or say in the write-up which check was blocked.
        # Non-vacuous 2026-08-16: with a root pointed at a directory that
        # does not exist, this exits 1 naming the root and the seven names
        # nothing searched, where before it exited 0 and filed a planted
        # `read-runn.py` among them.
        bad.append('BLOCKED: %s is not mounted, so %d named path(s) were'
                   ' not checked and a wrong one among them cannot be told'
                   ' from a right one: %s'
                   % (p['unmounted_root'], len(p['unmounted']),
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
        # `doc` was read once at the top and nothing above writes the
        # README, so the verdict is read against it rather than through
        # a second handle -- the wallclock_window family, 9e94c9d.
        cur = doc
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
                    # Two causes, one artifact: canonical lines with a long one
                    # among them is what an Edit mid-stretch leaves AND what
                    # hand-lengthening leaves, so this cannot tell them apart
                    # and must name both remedies. Naming the formatter alone
                    # sent a session round wrap-then-edit-then-red five times
                    # in one write-up (2026-08-16): wrapping is the fix when
                    # the document is done, unwrapping when it is not.
                    bad.append('%d paragraph(s) of %s are wrapped by hand --'
                               ' first at line %d; if the document is done,'
                               ' `wrap80 -i %s`; if you are still editing,'
                               ' `wrap80 --unwrap -i %s` and work there.'
                               ' Never re-wrap a line by hand'
                               % (len(hand), os.path.basename(readme), at,
                                  os.path.basename(readme),
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
    # in a ratio, and the block form is this README's rather than a run's to
    # change. And a sentence may run INTO an indented block -- a code sample
    # or an indented table -- leaving the prose before it ending on `of` or a
    # dash with the rest after; three paragraphs of this README do that, so
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

    # This README says of itself that it cites no line and no permalink,
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
    # and exit 0. The claim it enforces was true when written -- the README
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
    buried = [('%s:%d' % (os.path.basename(readme), i), l)
              for i, l in buried_actions(lines)]

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
    if buried:
        sweep(buried, "action(s) named only in a checklist's comment; an"
                      ' operator runs the lines and reads the comments, so'
                      ' promote it to a line of its own or say why not')
    # An ANSWERED entry that grew into the account it should have pointed
    # at. The open list is a QUESTION REGISTER -- its own preamble says an
    # entry is kept so the question is not re-proposed -- while `What is
    # settled, and where` is the pointer layer and says of itself that it
    # carries no figures by design. An answer that runs to a chapter is
    # therefore in the wrong one of the three places this README keeps,
    # and the topical section it duplicates goes on being the one that
    # moves when a run does.
    #
    # A FAIL, unlike the three sweeps above, and it took two goes to earn
    # that. It listed rather than failed while the test was length AND
    # the absence of a pointer, because that pair could not tell an
    # account from an entry that had earned its length -- and then
    # because the run registrations sat in every list it produced, six
    # entries a reader adjudicated by hand each time. Both are answered
    # now: length alone decides, the registrations are exempt by their
    # own lead, and what is left is a document defect with three
    # truthful ways out. Nothing is left to judge, so it gates.
    #
    # THE ONLY-COPY ESCAPE IS WHAT MAKES THE GATE HONEST. An answer whose
    # evidence nothing else records cannot be moved anywhere, and
    # `bq-scan-packed-mulback` is the live instance -- the dead-ideas
    # list takes ideas that died on paper where that one was built,
    # rostered and measured. It sits under the threshold today, so the
    # gate never meets it; a longer one would be failed with no true way
    # to pass, and a gate that forces a lie is worse than a list nobody
    # reads. So a bolded clause carrying `only copy` exempts an entry,
    # and the failure names that as one of the ways out rather than
    # leaving it to be discovered.
    #
    # Both exemptions are COUNTED and said in either branch, the pass
    # included: an exemption nobody is told about is the silent cap this
    # directory refuses everywhere else.
    long_ones = [('%s:%d' % (os.path.basename(readme), i), l)
                 for i, l in status_entries(lines, 'ANSWERED')
                 if len(l.split()) > ANSWERED_ACCOUNT]
    regs = [h for h in long_ones if REGISTRATION_RE.match(h[1])]
    onlys = [h for h in long_ones
             if h not in regs and ONLY_COPY_RE.search(h[1])]
    bloated = [h for h in long_ones if h not in regs and h not in onlys]
    said = ('%d run registration(s) and %d only-copy ruling(s) past it are'
            ' exempt' % (len(regs), len(onlys)))
    if bloated:
        bad.append('%d ANSWERED entry(s) past %d words, which is a chapter'
                   ' in a question register: %s. Move the account to the'
                   ' section that owns it; or give a run registration the'
                   " family's lead, `What Run N was built to answer`; or,"
                   ' where the entry is the only copy there is, say so in a'
                   ' bolded clause carrying `only copy` and the ruling that'
                   ' goes with it. %s'
                   % (len(bloated), ANSWERED_ACCOUNT,
                      '; '.join('%s %s' % (i, l[:56]) for i, l in bloated),
                      said))
    else:
        print('ok:   no ANSWERED entry is past %d words but the exempt ones,'
              ' and %s' % (ANSWERED_ACCOUNT, said))

    # The yardstick table keeps a column for the regime this run is NOT in,
    # which reads like a leftover and is the opposite: it is the only place
    # the previous run's basis survives once this chapter has replaced
    # everything else of it, and a return to that regime would have nothing
    # to read against. Prose asks for it to be kept; this makes the asking
    # stick.
    # `install --in-place` writes `?` into any cell it cannot carry
    # forward -- a row new to the roster -- and says so once, on stderr,
    # hours before anyone reads the table. Twelve reached a published
    # Results table on 2026-08-15 and the write-up shipped with them.
    # A warning nobody re-reads is a gate that does not exist, so this
    # is the gate: no cell of a published table may still be `?`.
    #
    # OUTSIDE the yardstick block below, reading nothing of it: it sat
    # inside, so a renamed yardstick header disabled this gate as well as
    # that one, and the `?` cells the comment above says shipped would
    # have gone unreported for that run. Moved 2026-08-17 by review.
    qmark = [i + 1 for i, ln in enumerate(lines)
             if re.search(r'\|\s*\?\s*\|', ln)]
    if qmark:
        bad.append('%d published table cell(s) still carry the `?` that'
                   ' install writes for a row it cannot carry forward --'
                   ' first at line %d; fill each from the run or from the'
                   ' note written before it'
                   % (len(qmark), qmark[0]))
    else:
        print('ok:   no published table cell is left at install\'s `?`')

    # Every table's rows against its own header. Markdown renders a short
    # row without complaint, filling from the LEFT, so a row that was
    # written when the table was narrower goes on rendering -- with each
    # value now under whichever column later runs pushed it to. That is
    # how the yardstick's four bottom rows came to sit five columns from
    # the runs the prose said they were: they were written at `f42ef4a`,
    # when the table was `| strategy | Run 8 | Run 7 |`, and every run
    # since prepended a column without padding them. No anchor, figure or
    # width check could see it, the rows being well-formed markdown.
    # Recovered from git and repaired 2026-08-20; case
    # `table-row-narrower-than-its-header`.
    ragged = []
    k = 0
    while k < len(lines):
        if (lines[k].startswith('|') and k + 1 < len(lines)
                and re.match(r'^\|[-: |]+\|$', lines[k + 1])):
            want = len(lines[k].split('|')) - 2
            j = k + 2
            while j < len(lines) and lines[j].startswith('|'):
                got = len(lines[j].split('|')) - 2
                if got != want:
                    ragged.append('line %d: %d cell(s) against %d (%s)'
                                  % (j + 1, got, want,
                                     lines[j].split('|')[1].strip()))
                j += 1
            k = j
        else:
            k += 1
    if ragged:
        bad.append('%d table row(s) narrower than its header, so each value'
                   ' renders under whichever column it fills up to: %s'
                   % (len(ragged), '; '.join(ragged[:4])))
    else:
        print('ok:   every table row carries its header\'s cell count')

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
            # every run in the README. Found by a blind walk of the procedure,
            # 2026-08-11.
            halves[run].add(bool(re.search(r'(?<!un)aligned', regime)))
        for run, kinds in sorted(halves.items()):
            if kinds == {True}:
                bad.append('the yardstick names Run %s aligned and nothing'
                           ' else: a paired run publishes a column per half,'
                           ' the other one being named for the build it is'
                           ' -- unaligned, max-skip -- and never folded in'
                           % run)

    # The basis half named in the Results section must be THIS run's. Run
    # 14's write-up left `run13-maxskip` standing in that lead while
    # installing run14-lookrts's tables, and --lint, --check-doc, --selftest
    # and --aa were all green, because no check read that name.
    #
    # The scope is the Results section alone, and deliberately so: the
    # forward-looking sections name the PREVIOUS run's halves on purpose --
    # Run 16's bridge registration is a repetition against run15-a32m, and
    # its pair note is run16-pair.txt, a file and not a half -- so a
    # chapter-wide rule would fail the README for saying what it means. What
    # Results holds is installed from the basis half, so a run number there
    # that is not this chapter's names a half whose figures are not in the
    # tables above it.
    #
    # Non-vacuity, 2026-08-19, both directions on a copy passed with
    # --readme, which is how a copy is read at all -- a path given
    # positionally is a run file, so the first attempt re-checked README.md
    # and credited this with a pass it had not earned. The README as it stands
    # carries exactly one such token in that section, `run15-lookrts` under
    # a Run 15 chapter, and passes; rewriting it to `run14-lookrts` fails
    # naming both the run and the chapter. So the pass is a real pass and
    # the check bites.
    chap = re.search(r'^## About the last run \(Run (\d+)\)', doc, re.M)
    start = next((i for i, ln in enumerate(lines)
                  if ln.startswith('### Results')), None)
    if not chap:
        bad.append('no `## About the last run (Run N)` heading, so no run is'
                   ' current and the half named in Results cannot be checked'
                   ' against one')
    elif start is None:
        bad.append('no `### Results` heading, so the section whose tables are'
                   ' installed from the basis half cannot be located')
    else:
        cur = chap.group(1)
        end = next((j for j in range(start + 1, len(lines))
                    if re.match(r'#{1,6} ', lines[j])), len(lines))
        seen = {m for j in range(start, end)
                for m in re.findall(r'\brun(\d+)-[a-z0-9]+', lines[j])}
        stale = sorted(seen - {cur}, key=int)
        if stale:
            bad.append('the Results section names run %s while this chapter'
                       ' is Run %s: the tables there are installed from this'
                       " run's basis half, so the half named beside them is"
                       ' this run\'s or the two disagree'
                       % (', run '.join(stale), cur))
        else:
            print('ok:   the half named in Results belongs to Run %s, this'
                  " chapter's run" % cur)

    # THE CHAPTER HEAD IS REPLACED WHOLE, and its own closing paragraph
    # says so -- but a write-up is done a paragraph at a time and nothing
    # enumerated them, so Run 18 left FOUR of Run 17's standing inside it,
    # one of them contradicting two paragraphs the same session had just
    # written. An independent checker found them by set-differencing the
    # document; that is this script's job and it is one comparison.
    #
    # Scoped to the chapter HEAD, the heading to the first `###`, and not
    # to the chapter: the chapter runs to the end of the file and holds
    # the column definitions, the class-block form and the replace list,
    # every one of which deliberately outlives a run.
    #
    # Silent once the write-up is committed, which is not a weakness but
    # the only sound reading: with HEAD already carrying this run's
    # chapter, every paragraph matches itself and an unchanged paragraph
    # means nothing. The run NUMBER is what says which case this is.
    # A DOCTORED COPY HAS NO HISTORY, so fall back to the canonical
    # README's committed chapter: what this asks is what the PREVIOUS RUN
    # wrote, which lives in the repo whichever copy is being linted, and
    # without the fallback every planted fixture would answer `no
    # committed copy` and the check could not be cased at all.
    # A REGISTRATION MARKED OPEN WHOSE EVERY ITEM HAS A VERDICT. Run 12's
    # registered four questions, one of them "as a gap rather than a
    # question", and recorded in that item's own body that the debt was
    # PAID on 2026-08-13 -- while its status stayed `OPEN` and its lead
    # went on saying `one still a gap` through six runs of post-run step
    # 10. The family always ends ANSWERED, so an OPEN one all of whose
    # numbered items carry a bolded verdict is a marker nobody updated.
    # The verdict WORD and not an all-caps run: Run 12's third item reads
    # `**The condition was met and the debt is PAID**`, so a pattern
    # keyed on capitalisation misses the one case this exists for -- as
    # the first draft of it did.
    # A VERDICT OPENS A BOLDED SPAN, and the span is the discriminator
    # rather than the word alone. A registration item
    # states its KILL CONDITION in the same vocabulary -- `killed by a
    # BROKE that clears that half's floor` -- so a pattern that only asks
    # whether the word appears near a `**` reads an unadjudicated item as
    # adjudicated, which fires the OPEN arm falsely and silences the
    # ANSWERED one. Measured on Run 18's own registration, whose second
    # item names a BROKE it had not yet met.
    VERDICT_WORDS = (r'ANSWERED|REFUTED|PAID|KILLED|CLEAN|DELIVERED|HELD'
                     r'|BROKE|BROKEN|FAILED|SETTLED|RETIRED|SPENT|SPLIT'
                     r'|UNUSED|NULL|TAKEN|WITHDRAWN')
    # The word has to fall in the FIRST 60 characters of a bolded span,
    # which is where a verdict announces itself and where a kill
    # condition quoted mid-sentence does not. Both styles this file uses
    # pass: `**KILLED, and the registered split...**` after an italic
    # label, and `**The condition was met and the debt is PAID**` opening
    # its own paragraph. The spans are paired off before the word is
    # asked for, so a closing `**` cannot open a match and the text
    # BETWEEN two spans -- where a kill condition ordinarily sits --
    # can never carry one. What remains possible and is not caught is a
    # bolded kill condition naming a verdict word in its own first 60
    # characters; no registration here writes one, and if one is written
    # this reads it as adjudicated.
    #
    # BOTH ARMS PROVEN, 2026-08-23, by breaking the document on purpose.
    # Putting `OPEN` back on Run 17's registration fires the first, naming
    # it and exiting 1; swapping the one word `SPLIT` out of that entry's
    # item 5 fires the second, printing `Run 17's registration is ANSWERED
    # and item(s) 5 carry no verdict`. The undoctored document exits 0 on
    # the same call, which is the control that says the two FAILs were the
    # breaks. The vocabulary is stated in README beside the `verdict:`
    # slot, because a check keyed on a closed word list is useless to a
    # writer who has not been told the list.
    VERDICT_RE = re.compile(r'.{0,60}?\b(?:' + VERDICT_WORDS + r')\b')

    def adjudicated(item):
        """Does this registration item record an outcome?

        Whitespace collapsed first, so a wrap cannot push the verdict
        word out of the span's opening and hide it.
        """
        flat = ' '.join(item.split())
        return any(VERDICT_RE.match(span)
                   for span in re.findall(r'\*\*(.+?)\*\*', flat))
    # BOTH DIRECTIONS. An OPEN registration whose every item is adjudicated
    # is a stale marker; an ANSWERED one with an item that is not is an
    # incomplete adjudication, and Run 17's carried exactly that -- a lead
    # promising `one came apart into a split` over an item 5 with no
    # verdict of any kind, through the whole of Run 18.
    # AN ITEM IS A NUMBERED SPAN, IN EITHER HOUSE FORM. Run 17's are
    # lines, `  5. `; Run 18's are inline, `(5) *The plateau*:`, and
    # stated TWICE in one paragraph -- once registering the question,
    # once adjudicating it -- so the spans are grouped by number and a
    # number is adjudicated if any span under it is. The first draft
    # knew only the line form, parsed Run 18's registration to zero
    # items and skipped it in silence -- the very registration the
    # README's verdict paragraph cites, and it wrote its verdicts in
    # two words (BROKEN, FAILED) the vocabulary did not hold. A
    # registration in a third form still parses to zero items, so the
    # skip now says so instead of continuing bare.
    for m in re.finditer(r'^- `(OPEN|ANSWERED)` \*\*What Run (\d+) was built'
                         r' to answer', doc, re.M):
        rest = doc[m.end():]
        # The entry ends where its own list item does -- a blank line
        # then column-0 text -- or at the next status-marked entry,
        # whichever is first. Run 18's entry is followed by a whole
        # section before the next entry, and the next-entry cut alone
        # took that section's numbered lines for registration items.
        ends = [x.start() for x in (re.search(r'^- `[A-Z]+` ', rest, re.M),
                                    re.search(r'\n\n(?=\S)', rest)) if x]
        body = doc[m.start():m.end() + (min(ends) if ends else len(rest))]
        marks = list(re.finditer(r'^  (\d+)\. |\((\d+)\)\s+(?=\*)',
                                 body, re.M))
        chunks = {}
        for k, mm in enumerate(marks):
            end = marks[k + 1].start() if k + 1 < len(marks) else len(body)
            chunks.setdefault(int(mm.group(1) or mm.group(2)),
                              []).append(body[mm.end():end])
        if not chunks:
            print("note: Run %s's registration numbers its items in"
                  ' neither house form, so its marker is held to nothing'
                  % m.group(2))
            continue
        undone = [n for n, cs in sorted(chunks.items())
                  if not any(adjudicated(c) for c in cs)]
        if m.group(1) == 'OPEN' and not undone:
            bad.append("Run %s's registration is marked OPEN and every one"
                       ' of its %d numbered items carries a verdict: the'
                       ' family always ends ANSWERED, so the marker is'
                       ' stale --- and a stale marker does not merely'
                       ' mislead, it exempts the entry from retirement'
                       % (m.group(2), len(chunks)))
        elif m.group(1) == 'ANSWERED' and undone:
            bad.append("Run %s's registration is ANSWERED and item(s) %s"
                       ' carry no verdict: an answered registration is one'
                       ' where every question was adjudicated, and a lead'
                       ' counting outcomes over an item that records none'
                       ' is a count of something nobody wrote'
                       % (m.group(2), ', '.join(str(n) for n in undone)))

    head_doc = head_text_of(readme)
    if head_doc is None:
        here_readme = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'README.md')
        head_doc = head_text_of(here_readme)
    here = chapter_head_blocks(doc)
    there = chapter_head_blocks(head_doc) if head_doc is not None else None
    was = (re.search(r'^## About the last run \(Run (\d+)\)$',
                     head_doc, re.M) if head_doc else None)
    if head_doc is None:
        print('note: no committed copy of this document, so the chapter'
              " head's paragraphs are not held to the previous run's")
    elif here is None or there is None or not chap or not was:
        # No chapter heading on one side, so there is no pair of chapters
        # to compare and nothing to say. `was` is tested with the rest
        # because the else branch reads its run number.
        pass
    elif was.group(1) == chap.group(1):
        print('ok:   the chapter head is already committed as Run %s, so'
              ' there is no previous run to hold it to' % chap.group(1))
    else:
        old_keys = {k for k, _ in there}
        stale = [ls[0] for k, ls in here if k in old_keys]
        if stale:
            bad.append('%d paragraph(s) of the Run %s chapter head are'
                       ' unchanged from Run %s: the chapter is replaced'
                       ' whole, so each is stale or is standing on purpose'
                       ' and wants rewording to say so -- %s'
                       % (len(stale), chap.group(1), was.group(1),
                          '; '.join(l.strip()[:60] for l in stale)))
        else:
            print('ok:   every paragraph of the Run %s chapter head is new'
                  ' since Run %s' % (chap.group(1), was.group(1)))

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
            written `twenty-three` in this README's prose, which the word map
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

        # The SIX-PAIR figure beside it, held the same way. The eighteen-pair
        # floor has been checked across its sites since 2026-08-14; the
        # restricted one was checked nowhere, and a comprehension read of
        # Run 16 found it quoted 0.39%/0.24% in four places, 0.50% in a
        # fifth -- a run stale -- and rounded to "half a percent" in a
        # sixth, two of them inside one paragraph. Some sites quote the
        # pair and some only the basis half, so both shapes are collected
        # and the singletons are held to the pair's first figure.
        six = [m for p in (
            r'six pairs that carry back to Run 10[^.]*?([\d.]+)% and'
            r' ([\d.]+)%',
            r'([\d.]+)% and ([\d.]+)% (?:are the same over|read on) the six'
            r' pairs') for m in re.findall(p, uw)]
        six_one = re.findall(r'six-pair figure of the half it is read on'
                             r'[^.]*?([\d.]+)%', uw)
        six_one += re.findall(r'\*([\d.]+)% between any two rows of the'
                              r' table\*', uw)
        if len(six) < 2:
            bad.append('could not locate at least two sites quoting the'
                       " run's six-pair floor, so its agreement check did"
                       ' not run -- if the sentences were reworded, this'
                       " check's patterns move with them")
        elif len(set(six)) > 1:
            bad.append('the six-pair figure is quoted differently across its'
                       ' %d sites: %s -- it is the threshold two rows of one'
                       ' table must clear, so one wrong copy retires a'
                       ' margin'
                       % (len(six), '; '.join('%s%%/%s%%' % f
                                             for f in set(six))))
        elif any(o != six[0][0] for o in six_one):
            bad.append('the six-pair figure reads %s%% where it is quoted as'
                       ' a pair and %s where it is quoted alone -- the two'
                       ' are the same number'
                       % (six[0][0], ', '.join(sorted(set(
                           o for o in six_one if o != six[0][0])))))
        else:
            print('ok:   the six-pair floor reads %s%%/%s%% at all %d sites'
                  ' that quote it, and %s%% at the %d that quote one half'
                  % (six[0] + (len(six), six[0][0], len(six_one))))

        # And the A/A population itself. The twelve twins took it from six
        # pairs to eighteen on 2026-08-14 and two sites kept saying six for
        # three runs -- the reader's own section and the floor section's
        # per-population rule -- while every class block printed "N of 18".
        # Nothing compared them, so the stale pair rode three write-ups.
        base = set(re.findall(r'it rests on (six|eighteen) pairs', uw))
        base |= set(re.findall(r'The same (six|eighteen) controls ride every'
                               r' process', uw))
        base |= set(re.findall(r'\*\*(Six|Eighteen)\*\* A/A controls run an'
                               r' existing strategy', uw))
        base = {b.lower() for b in base}
        if not base:
            bad.append("could not locate any site naming the A/A population's"
                       ' size, so that agreement check did not run')
        elif len(base) > 1:
            bad.append('the A/A population is quoted as %s across its sites'
                       ' -- the twelve twins took it to eighteen and every'
                       ' class block prints that, so a site still saying six'
                       ' is three runs stale'
                       % ' and '.join(sorted(base)))
        else:
            print("ok:   the A/A population reads %s pairs everywhere it is"
                  ' named' % base.pop())

        # A CLASS's own floor, which the two checks above do not reach.
        # They hold the RUN's floor pair and the six-pair figure across
        # their sites; a class's floor is quoted inside its own block and
        # was checked by nothing, so a block requoting its predecessor's
        # would have ridden a write-up in silence -- the same failure the
        # six-pair check was written for, one population down. Unlike
        # those two this one has a truth on the page rather than only
        # agreement: the class table's `floor` column is what `--block`
        # installs from the JSON, so the block's prose is checked against
        # its own table row and not against its neighbours.
        #
        # A block that quotes NO floor is not a defect and is counted
        # rather than failed: half of them do not, the figure belonging to
        # the table. What must not happen is a block quoting one that is
        # not its own. Note added 2026-08-22 with the check.
        #
        # Non-vacuous, all three failing branches fired 2026-08-22.
        # `revsome`'s quote moved to 16.55% against its row's 18.05%: FAIL
        # naming both. Every floor quote in the section reworded to `level`:
        # the vacuity FAIL, which is the branch a rewording would otherwise
        # turn into a silent pass. And the table read out of `uw` rather
        # than the raw lines, which is how the row pattern found nothing:
        # the could-not-find FAIL. Unbroken it prints ok at exit 0, which is
        # the control saying the three were the breaks.
        # The table comes off the RAW document and the prose off `uw`:
        # `unwrapped_paragraphs` drops table rows, every other caller
        # wanting prose, so the floor column is not in `uw` to be read.
        cls_head = r'^### The stride classes, run by run$(.*?)^### '
        cls_raw = re.search(cls_head, '\n'.join(lines), re.M | re.S)
        cls_sec = re.search(cls_head, uw, re.M | re.S)
        cls_rows = dict(re.findall(r'^\| `([a-z0-9]+)` \|.*\| ([\d.]+)% \|$',
                                   cls_raw.group(1), re.M)) if cls_raw else {}
        cls_leads = ([(m.start(), m.group(1)) for m in
                      re.finditer(r'^\*\*`([a-z0-9]+)` ---', cls_sec.group(1),
                                  re.M)] if cls_sec else [])
        if not cls_rows or not cls_leads:
            bad.append('could not find the class table\'s floor column or the'
                       ' class block leads under `The stride classes, run by'
                       ' run`, so the per-class floor check did not run')
        else:
            body, off, quoted = cls_sec.group(1), [], 0
            for i, (pos, cls) in enumerate(cls_leads):
                end = (cls_leads[i + 1][0] if i + 1 < len(cls_leads)
                       else len(body))
                blk = body[pos:end]
                # `N% floor` and `this class's floor N%` are the two shapes
                # the blocks use. Neither takes `the repetition's own floor
                # is N%`, which is a different population's figure sitting
                # in the same block and must not be held to this one.
                seen_f = (re.findall(r'\*?\*?([\d.]+)%\*?\*? floor', blk)
                          + re.findall(r"class's floor \*?\*?([\d.]+)%", blk))
                if seen_f:
                    quoted += 1
                for f in seen_f:
                    if cls not in cls_rows:
                        off.append('`%s` has a block and no table row' % cls)
                    elif f != cls_rows[cls]:
                        off.append('`%s` quotes %s%% where its table row'
                                   ' reads %s%%' % (cls, f, cls_rows[cls]))
            if off:
                bad.append('a class block quotes a floor that is not its'
                           " own: %s -- the table's floor column is what"
                           ' `--block` installs from that process\'s own'
                           ' eighteen A/A pairs' % '; '.join(sorted(set(off))))
            elif not quoted:
                bad.append('no class block quotes a floor at all, so the'
                           ' per-class floor check passed vacuously -- if the'
                           " blocks were reworded, this check's patterns move"
                           ' with them')
            else:
                print('ok:   each of the %d class block(s) that quotes a floor'
                      ' quotes its own, against %d row(s) of the class table'
                      ' (%d block(s) quote none, the table carrying it)'
                      % (quoted, len(cls_rows), len(cls_leads) - quoted))

            # The MOVEMENT sentence above the blocks, which neither check
            # reaches. It reads each class's floor against its
            # predecessor's, `X% to Y%` eight times over, so its second
            # figure is a claim about the column printed right above it
            # and its first about a column no longer on the page -- and
            # the whole sentence is written by hand under a table
            # `install-tables.sh` writes. Run 17 installed the new column
            # and left Run 16's paragraph standing under it: every one of
            # its eight `to` figures is the previous run's, and `--lint`,
            # `--check-doc` and both installers were green over it, the
            # numbers being perfectly good figures of the wrong run.
            #
            # Vacuity is guarded STRUCTURALLY and not on the sentence's
            # own words. Keying it on the opening phrase was tried first
            # and is the bug it was written against: rewording that
            # phrase then turned the whole check off in silence, which is
            # the one thing it must not do. What identifies the paragraph
            # instead is what it is -- a line quoting four or more of the
            # classes with a figure apiece -- so a rewording that keeps
            # the content still has to parse, and a run that writes no
            # such paragraph owes nothing and says so.
            #
            # Non-vacuous, all five branches driven 2026-08-22 against
            # copies: the live README FAILs on all eight figures; the same
            # paragraph with Run 17's own column written in passes; that
            # one with the opening phrase reworded passes too, which is
            # what says the guard is not the wording; `to` swapped for
            # `->` FAILs as a rewording rather than passing empty; and the
            # paragraph removed prints the note.
            movers = [ln for ln in body.split('\n')
                      if len(re.findall(r'`[a-z0-9]+` [\d.]+%', ln)) >= 4]
            moved = re.findall(r'`([a-z0-9]+)` ([\d.]+)% to ([\d.]+)%',
                               '\n'.join(movers))
            if not movers:
                print('note: the class section quotes no paragraph of class'
                      ' floors, so there was no movement to hold to the'
                      ' column')
            elif len(moved) < 4:
                bad.append('a paragraph of the class section quotes %d class'
                           ' floors and this check can read %d movement(s)'
                           ' out of it -- if that sentence was reworded, its'
                           ' pattern moves with it'
                           % (len(re.findall(r'`[a-z0-9]+` [\d.]+%',
                                             '\n'.join(movers))), len(moved)))
            else:
                stale = ['`%s` moves to %s%% where the column above it reads'
                         ' %s%%' % (c, now, cls_rows[c])
                         for c, _, now in moved
                         if c in cls_rows and now != cls_rows[c]]
                if stale:
                    bad.append('the floor-movement sentence lands on figures'
                               ' the class table does not carry, so it is'
                               " reading the PREVIOUS run's column: %s"
                               % '; '.join(stale))
                else:
                    print('ok:   all %d floor movement(s) land on the class'
                          " table's own column" % len(moved))

        # Two more of the floor check's shape -- one figure, several
        # sites, must agree -- on the counts Run 14 got wrong in more than
        # one place. Unlike the floor these have a truth outside the README:
        # Main.hs holds the arms and the shape lists, and a count every
        # site agrees on is still wrong after a roster change, which is
        # the case agreement alone cannot see.
        dims = dims_by_shape(main_hs)[0]
        main_shapes = [s for s, d in dims.items() if d['lst'] in MAIN_LISTS]
        class_sizes = {}
        for s, d in dims.items():
            if d['lst'] not in MAIN_LISTS:
                class_sizes.setdefault(d['lst'], set()).add(s)
        want = len(timed) * len(main_shapes)
        seen = [int(m) for p in (r'takes the roster to (\d+) benches',
                                 r'roster is Run \d+\'s (\d+) benches')
                for m in re.findall(p, uw)]
        if len(seen) < 2:
            bad.append('could not locate at least two sites quoting the'
                       ' roster size, so its agreement check did not run --'
                       ' if the sentences were reworded, this check\'s'
                       ' patterns move with them')
        elif set(seen) != {want}:
            bad.append('the roster size reads %s across its %d sites, where'
                       ' Main.hs holds %d timed arms over %d main-set shapes'
                       ' and so %d benches'
                       % ('/'.join(str(s) for s in sorted(set(seen))),
                          len(seen), len(timed), len(main_shapes), want))
        else:
            print('ok:   the roster size reads %d at both sites that quote'
                  ' it, and is what Main.hs holds' % want)

        # `over N shapes` is a population's size wherever it appears; `on
        # N shapes` is a win count and is not this check's, which is why
        # the pattern will not take it.
        pops = {len(main_shapes)} | {len(v) for v in class_sizes.values()}
        quoted = {int(n) for n in re.findall(r'\bover\s+(?:all\s+)?(\d+)'
                                             r' shapes', uw, re.I)}
        if not quoted:
            bad.append('no site quotes a population\'s size as `over N'
                       ' shapes`, so that agreement check did not run')
        elif quoted - pops:
            bad.append('%d shape count(s) quoted as a population\'s size'
                       ' match no population Main.hs defines (%s); the main'
                       ' set has %d shapes and each class %s'
                       % (len(quoted - pops),
                          ', '.join(str(n) for n in sorted(quoted - pops)),
                          len(main_shapes),
                          '/'.join(str(n) for n in
                                   sorted({len(v) for v
                                           in class_sizes.values()}))))
        else:
            print('ok:   every population size quoted in prose is one'
                  ' Main.hs defines: %s'
                  % ', '.join(str(n) for n in sorted(quoted)))

        # Prospective tense about a run that has already happened. An open
        # list entry written before a run says what that run WILL do, and
        # the verdict pass rewrites it -- except when it does not: "Run 13
        # takes it at full budget, and its Results row will come out with
        # `?`" stood for a day after the row was in the table, filled with
        # a different phrase. Only `will` and `is to be` count as
        # prospective: this README narrates finished runs in the historic
        # present ("Run 10 takes it"), so verbs alone cannot tell a stale
        # promise from an idiom, and a sweep that listed every historic
        # present would be one nobody reads. Listed for adjudication, not
        # failed. Non-vacuous 2026-08-14: planting that very sentence in
        # the open list on a copy listed it with its line; the shipped README
        # lists nothing.
        m = re.search(r'^## About the last run \(Run (\d+)\)$', doc, re.M)
        lo = [i for i, l in enumerate(lines, 1)
              if l.startswith('## What is open')]
        hi = [i for i, l in enumerate(lines, 1)
              if l.startswith('## The goal')]
        if m and lo and hi and lo[0] < hi[0]:
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
            # EVERY entry of this section opens with a status, which the
            # section's own preamble states and offers a grep as the use
            # of. It was true of the parent list and false of
            # the sublist: seven of the thirteen non-urgent entries
            # carried no token, four of them closed within the ten days
            # before 2026-08-22, their closure a phrase inside the bolded
            # lead instead. So the grep found the live ones among six
            # entries and left seven to be read, which is what a status is
            # for.
            #
            # A FAIL and not a worklist, alone among the open list's
            # checks: there is no judgement left once an entry has a
            # token, the choice of WHICH token being the author's and
            # made before this ever runs. Sub-bullets are indented and so
            # are not entries; the section carries no other top-level
            # bullet, which is what makes the rule decidable -- measured
            # 2026-08-22, 46 entries and 39 statused.
            #
            # NUMBERED ITEMS COUNT TOO. `Recommended tasks after Run N`
            # numbers its three where both lists bullet theirs, so a
            # bullet-only rule reached the section and skipped the one
            # subsection inside it whose items read as a checklist -- and
            # skipped it silently, the count simply coming out three
            # short. The open list carries no other numbered item,
            # measured the day this was widened, which is what keeps the
            # rule decidable over the looser pattern.
            entries = [(i, l) for i, l in enumerate(lines, 1)
                       if lo[0] <= i < hi[0]
                       and re.match(r'^(?:- |\d+\. )', l)]
            loose = [(i, l) for i, l in entries
                     if not re.match(r'^(?:- |\d+\. )'
                                     r'`(OPEN|PARKED|ANSWERED|STANDING)` ',
                                     l)]
            if not entries:
                bad.append('no top-level entry found between `What is open`'
                           ' and `The goal`, so the status check did not'
                           ' run -- if the list was reshaped, this pattern'
                           ' moves with it')
            elif loose:
                bad.append('%d open-list entry(s) open with no status, so'
                           ' the section\'s own grep cannot find the live'
                           ' ones among them: %s'
                           % (len(loose),
                              '; '.join(
                                  '%s:%d %s'
                                  % (os.path.basename(readme), i,
                                     re.sub(r'^(?:- |\d+\. )', '', l)[:50])
                                  for i, l in loose[:4])))
            else:
                print('ok:   all %d open-list entries open with a status,'
                       ' so the section\'s own grep is complete'
                      % len(entries))
        else:
            # A range this sweep cannot delimit is a sweep that did not
            # run, and its silence read exactly like a clean open list:
            # rename either heading, or move the goal section above the
            # open one -- which renames nothing and so trips no neighbour
            # -- and it printed nothing. Same rule as the wrap and path
            # checks: BLOCKED is not a pass. Found 2026-08-17 by review,
            # the second half of it by proving the first.
            bad.append('BLOCKED: the open list (%s), the goal section (%s)'
                       ' or the chapter heading (%s) could not be located'
                       ' in that order, so no prospective promise was'
                       ' checked'
                       % ('line %d' % lo[0] if lo else 'gone',
                          'line %d' % hi[0] if hi else 'gone',
                          'found' if m else 'gone'))
    else:
        # `lint` fails loudly on the same nothing; this went quiet, and a
        # renamed or re-indented roster -- or a wrong --main -- left the
        # prose counts, the floor agreement, the roster and population
        # sizes and the stale-promise sweep all unrun, with only `ok:`
        # lines and exit 0 to show for it. Found 2026-08-17 by review.
        bad.append('BLOCKED: no roster parsed out of %s, so the prose'
                   ' counts, the floor agreement and the open-list sweep'
                   ' did not happen' % os.path.basename(main_hs))

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
    # `([see the run](#about-the-last-run-run-14))` in the opening
    # paragraph of a copy listed it with its line; the shipped README lists
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
    else:
        # The heading is the sweep's own boundary, so without it there is
        # no "above the chapter" to sweep and the silence read as a README
        # with no decayed links. Found 2026-08-17 by review, with the
        # open-list sweep above it.
        bad.append('BLOCKED: no `## About the last run` heading, so the'
                   ' links into the run chapter were not swept')

    for line in bad:
        print('FAIL: ' + line)
    return 1 if bad else 0


def check_doc_quiet(readme, main_hs):
    """`--check-doc` with the worklists withheld and the verdict kept.

    What this replaces is a `grep FAIL` over the loud form, which a run was
    doing on nearly every call: a grep reads only the spelling it was
    given, so a checker that grew a second kind of stopping line would go
    silently unread, and the pipe throws the exit code away as well. This
    withholds by count and says how many lines it kept back, so a run that
    wants them knows they exist. The verdict is check_doc's own return.

    The withheld line names `--worklists`, the flag that prints
    them, and NOT the absence of `--quiet`, which it said until
    2026-08-22 and which does not work: plain `--check-doc`
    withholds too. A run that followed the old wording got the same
    withheld line back and read the tool as broken -- a message that
    misdirects at exactly the step, post-run 7, that exists to read
    those lists.

    Non-vacuity, 2026-08-16, against a copy: renaming `## About the last
    run (Run 14)` to `(Run 14x)` printed two FAIL lines -- the four dead
    anchors, and the replace-list bullet that no longer covers the section
    -- and exited 1, where the same copy unbroken printed no FAIL and
    exited 0. The withheld counts differ by exactly those two lines, which
    is what promoting them out of the pool should do.
    """
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = check_doc(readme, main_hs)
    lines = [l for l in out.getvalue().split('\n') if l]
    fails = [l for l in lines if l.startswith('FAIL: ')]
    for line in fails:
        print(line)
    print('%d line(s) withheld; rerun with --worklists for them'
          % (len(lines) - len(fails)))
    return rc


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

    def mirrors(entries, resolve, what):
        """Every arm here whose name promises a base it does not run.

        The A/A twins and the Force arms ask this identically -- only the
        name rule and one clause of one message differ -- and the two
        copies were sixteen lines apart with the middle message written
        out twice.

        Both callers proven to still fire, 2026-08-16, on copies of
        Main.hs: `bq-expand-aa-distant` pointed at `fbBQgen` fails naming
        the twin and its base, `mut-flat-gm-nosum` pointed there fails
        the same way for the Force arms, and the unaltered roster fails
        neither.
        """
        off = []
        for n, f in entries:
            base = resolve(n)
            if base is None:
                off.append('%s is %s' % (n, what))
            elif base not in fun:
                off.append('%s names %s, which is not in the roster'
                           % (n, base))
            elif fun[base] != f:
                off.append('%s runs %s where %s runs %s'
                           % (n, f, base, fun[base]))
        return off

    off = mirrors(twins, twin_of, 'an A/A control whose name has no -aa')
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
    off = mirrors(forces, base_of, 'a Force arm whose name has no -nosum')
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
    # data half -- every arm best outside the vecdims family on some shape,
    # since 2026-08-22 -- needs the JSONs, and `--fingerprint --classes`
    # reads it there; here an extra fingerprint arm is fine and a bolded
    # row left out is not.
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

    The two mode checks likewise (2026-08-14): renaming `fmt_abs`'s micro
    unit to `us` fails the machine one, naming the cell it could not parse,
    while dropping the space before the unit does not -- the parser tolerates
    that by design, and a check firing on it would be testing whitespace
    rather than the seam; and shifting the step search's split five samples
    earlier fails the steps one, naming the split it found instead. Both are
    checked against values and series built here, since a run file carries no
    cell known to have a step and no fingerprint figure whose true value is
    known apart from the one printed.

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
        elif not checked:
            # Keyed on `checked` alone. Keyed on `checked and not bad`, a
            # real mismatch took this branch and announced that no shape
            # carries an annotation, beside the FAIL naming the shape
            # whose annotation it had just read.
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
    kind, label, prefix = population_of(shapes, meta['dims'])
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
        # EVERY half, not `halves[0]`: `apply_correction` averages them all
        # and the ok line below claims all of them, so checking one was a
        # narrower test than either sentence around it. A non-positive term
        # also fails the malformed-cell test above, so this branch names
        # the consequence for the correction rather than discovering the
        # cell -- which is why it is not a second discovery. Widened
        # 2026-08-17 by review.
        term_bad = [sh for sh in shapes for h in halves
                    if not 0 < cells[sh][h]['slope']]
        sunk = [(sh, st) for sh in shapes for st in strategies
                if not no_net(st)
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
            if no_net(st):
                continue
            # A cell the forcing term did not leave positive has no log, so
            # this raised `math domain error` and the whole gate printed
            # NOTHING -- no verdict, no FAIL, a traceback where `read-all.sh`
            # reads a verdict. `time_of`, `worst_of` and `pair_stats` each
            # answer for such a cell; this is the fourth site and was the
            # one that could not report. Found 2026-08-17 by review.
            #
            # Asked of the CELLS and not of the quotients, which is the same
            # defect one step earlier: the test read `r <= 0` over ratios
            # the line above had already computed, so a baseline whose own
            # net came out exactly 0 divided by zero before anything could
            # look. `<= 0` had always included 0; only the order kept it out
            # of reach. Found 2026-08-17 on a built run with every arm of a
            # shape sunk, which drives both `sum-only` halves and `list`
            # together and lands the baseline exactly there.
            if any(cells[sh]['list']['net'] <= 0
                   or cells[sh][st]['net'] <= 0 for sh in shapes):
                bad.append('%s: a cell the forcing term did not leave'
                           ' positive, so this row has no geomean to'
                           ' bracket' % st)
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
        # A pair with a cell the term did not leave positive is not one of
        # these: its logs do not exist. The same guard as `aa_pairs` and for
        # the same reason -- this site was the one that took the whole gate
        # down with it, printing no verdict at all. 2026-08-17.
        pairs = [(a, twin_of(a)) for a in strategies
                 if twin_of(a) in strategies
                 and not any(cells[sh][x]['net'] <= 0
                             for sh in shapes
                             for x in (a, twin_of(a), 'list'))]
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

    # The two newest modes, checked against series and values built here
    # rather than against this run -- which is what makes the checks
    # non-vacuous, a run file carrying no cell that is known to have a step
    # and no fingerprint cell whose true value is known apart from the
    # figure printed. What each guards is a seam: --machine parses what
    # `fmt_abs` writes, so a change to either alone would leave the machine
    # check with nothing to compare and no complaint, and --steps is
    # arithmetic that no published column can contradict.
    was = len(bad)
    # The last two are the rounding boundary `fmt_abs` moves a unit at:
    # 999.7 us is `1 ms` and 999.4 us is `999 us`, and the exponent form
    # the first used to take is what this seam cannot parse.
    for x in (3.21e-9, 5.28e-6, 1.23e-3, 2.5, 9.997e-4, 9.994e-4):
        cell = '| `shape` | 3 | 288 | %s | 0.152 |' % fmt_abs(x)
        m = FINGERPRINT_ABS_RE.match(cell)
        if not m:
            bad.append('--machine cannot parse the fingerprint\'s own cell'
                       ' for %g, written %s' % (x, fmt_abs(x)))
        elif abs(float(m.group(2)) * UNIT[m.group(3)] / x - 1) > 0.005:
            bad.append('--machine reads %s as %g, past the three figures it'
                       ' is written with' % (fmt_abs(x), float(m.group(2))
                                             * UNIT[m.group(3)]))
    # `for ... else` with no `break` in the loop, which ran the ok line
    # unconditionally: renaming a unit printed the FAIL and the claim that
    # it cannot happen, side by side. That is the pairing the comment
    # above the shape-parse check forbids, made by a keyword. Both
    # provocations run 2026-08-16 -- ` ms` renamed to ` millis` here, and
    # one l annotation moved by 1 for the shape parse -- and each now
    # prints its FAIL alone. `us` for `us` is NOT a provocation: the
    # pattern takes it, so the first attempt proved nothing.
    if len(bad) == was:
        ok.append('--machine parses what the fingerprint writes, over ns to s')

    if best_step([1.0] * 60) is not None:
        bad.append('--steps finds a step in a constant series')
    planted = ([1.0 + (i % 2) * 1e-4 for i in range(30)]
               + [1.1 + (i % 2) * 1e-4 for i in range(30)])
    got = best_step(planted)
    if not got or abs(got[0] - 10) > 0.5 or got[2] != 30:
        bad.append('--steps does not recover a 10%% step planted at sample'
                   ' 30, reading %r' % (got,))
    else:
        ok.append('--steps recovers a planted 10%% step at its own sample'
                  ' (%+.2f%% at %d) and finds none in a flat series'
                  % (got[0], got[2]))

    # The seam `--compare --alloc` closes on, and the last mode to be left
    # outside this check. That mode prints, as its ruling against choosing a
    # column, that the `alloc` multiple is the fitted bytes over a constant
    # per shape -- true of how `load` derives it and of nothing else, and it
    # would go on printing after an edit that made it false, since both
    # columns come out of the same call. Checked on the run in hand rather
    # than on a constructed series: unlike a step or a fingerprint cell,
    # every cell here carries the quantity. Non-vacuous 2026-08-14, against
    # a copy: dividing `alloc` by `1 + len(strategy) / 1e4` in `load` makes
    # the ratio strategy-dependent, and this fails at a spread of 3.00e-03,
    # where the intact reader on the same file reads 4.4e-16 -- one float
    # round-trip, which is why the bar is 1e-9 and not equality.
    ratios = collections.defaultdict(list)
    for sh in shapes:
        for st in strategies:
            c = cells[sh][st]
            if c['alloc_bytes'] and c['alloc']:
                ratios[sh].append(c['alloc_bytes'] / c['alloc'])
    if not ratios:
        skip.append('no cell of this run carries both a fitted allocation and'
                    ' an alloc multiple, so --alloc\'s one-quantity claim is'
                    ' unexercised here')
    else:
        d, sh, n = max((max(r) / min(r) - 1, s, len(r))
                       for s, r in ratios.items())
        if d > 1e-9:
            bad.append('--alloc prints that the multiple is the fitted bytes'
                       ' over a constant per shape, and %s spreads them by'
                       ' %.2e over %d cell(s)' % (sh, d, n))
        else:
            ok.append('--alloc\'s one-quantity claim holds: bytes over'
                      ' multiple is one constant per shape, worst spread'
                      ' %.1e on %s, over %d shape(s)' % (d, sh, len(ratios)))

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
                   ' (not needed by --lint or --check-doc; a `.log` under'
                   ' --wild)')
    p.add_argument('--main', default=os.path.join(here, 'Main.hs'),
                   help='Main.hs to read shape sizes from'
                        ' (default: alongside)')
    p.add_argument('--shapes', action='store_true')
    p.add_argument('--aa', action='store_true')
    p.add_argument('--cells', action='store_true')
    p.add_argument('--steps', action='store_true')
    p.add_argument('--machine', action='store_true')
    p.add_argument('--deflation', action='store_true',
                   help='the roster cell over its own alone leg, per shape --'
                        ' raw over raw, the legs found from this run\'s name')
    p.add_argument('--wild', action='store_true',
                   help='read the per-sample instrument\'s LOG instead of a'
                        ' JSON: each bench\'s pre/post pair differenced, and'
                        ' the foreign CPU during its samples where the stamp'
                        ' carries the load fields')
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
    p.add_argument('--ci', action='store_true',
                   help='with --compare: each arm\'s CI%% median against'
                        ' the other run\'s, the column\'s own statistic')
    p.add_argument('--bridge', action='store_true',
                   help='with --compare: each arm as a ratio to `list` in'
                        ' its own run, which a box change cannot move')
    p.add_argument('--band', type=float, default=3.3, metavar='PCT',
                   help='with --bridge: the drift band, default 3.3')
    p.add_argument('--markdown', action='store_true')
    p.add_argument('--fingerprint', action='store_true')
    p.add_argument('--classes', nargs='+', metavar='CLASS.json',
                   help='with --fingerprint: the class JSONs whose shapes'
                        ' fill the second table; with --extremes, the'
                        ' populations to rank')
    p.add_argument('--extremes', action='store_true',
                   help='which class holds each extreme -- the tightest'
                        ' floor, the widest gap, the best class for an arm'
                        ' -- over the --classes given; needs no run file,'
                        ' installs nothing, and is the derived source a'
                        ' superlative about the eight has nowhere else')
    p.add_argument('--block', action='store_true')
    # The standing explanations and the installed table are read once and
    # then reprinted on every later call: ten populations of --aa is ~250
    # lines of prose a session has already read, and --block's table is
    # thrown away because --in-place installs it. --brief drops both. It
    # drops nothing computed -- every figure still prints.
    # --brief is now the DEFAULT and --verbose restores what it drops. The
    # standing explanation each mode prints is worth reading once a session,
    # not once a call, and a paired run calls these modes a dozen times: Run
    # 16 remembered the flag on --aa and --block and forgot it on --compare,
    # which then printed 42 arms with their preamble several times over. The
    # flag is kept as a no-op so an old recipe still runs.
    p.add_argument('--brief', action='store_true',
                   help='the default now; kept so older recipes still run')
    p.add_argument('--verbose', action='store_true',
                   help='restore the standing explanation --brief drops;'
                        ' no computed figure differs either way')
    p.add_argument('--in-place', action='store_true',
                   help='install --markdown/--fingerprint/--block tables, or'
                        " --claims' per-claim readings, into README instead"
                        ' of printing them')
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--lint', action='store_true')
    p.add_argument('--check-doc', action='store_true')
    # The note: worklists are write-up material, adjudicated once at the
    # verification step, and they are the bulk of what --check-doc prints.
    # Every other call a run makes reads one bit off it. --quiet keeps that
    # bit and withholds the rest -- by count, since a mode that hides a
    # line without saying so is worse than the reading it saves.
    p.add_argument('--quiet', action='store_true',
                   help='the default now; kept so older recipes still run')
    # Quiet is the default because the procedure says only ONE call in a
    # whole run wants the worklists -- post-run step 7, where they are read
    # and adjudicated -- and every other call is a gate whose verdict is its
    # exit code. The default was the wrong way round and Run 16 ran the loud
    # form out of habit more than once.
    p.add_argument('--worklists', action='store_true',
                   help='with --check-doc: print the superseded-figure,'
                        ' superlative and absolute-time worklists for'
                        ' adjudication -- step 7 wants this, no other call'
                        ' does')
    p.add_argument('--para', metavar='PATTERN',
                   help="print README paragraphs whose bolded lead matches,"
                        " with the line each starts at; needs no run file")
    p.add_argument('--replace', metavar='ANCHOR',
                   help='replace the README paragraph carrying ANCHOR with the'
                        ' text in --with, without printing the old one;'
                        ' refuses unless ANCHOR occurs exactly once')
    p.add_argument('--with', dest='with_', metavar='FILE',
                   help='the replacement text for --replace')
    p.add_argument('--readme', default=os.path.join(here, 'README.md'),
                   help='README.md to check bench names against'
                        ' (default: alongside)')
    p.add_argument('--corr', choices=['sumonly', 'insitu'], default='sumonly',
                   help='which forcing term to subtract: `sumonly`, the'
                        ' published convention, or `insitu`, the term the'
                        ' `-nosum` pairs measure -- for a build where'
                        ' `sum-only` cannot be subtracted at all. Says on'
                        ' stderr which it used; an insitu column is'
                        ' comparable to no figure in README.md')
    p.add_argument('--no-controls', action='store_true')
    p.add_argument('--exclude', action='append', default=[],
                   metavar='STRATEGY')
    p.add_argument('--exclude-shape', action='append', default=[],
                   metavar='SHAPE')
    args = p.parse_args()

    # The dispatch below is an if/elif over mode flags, so a flag that names
    # no reachable branch is not an error there -- it falls through and some
    # other mode prints, exit 0, with nothing saying the flag did nothing.
    # Both --alloc and --chapter are `with --compare` modifiers and both
    # were droppable that way, and they are one line apart in README's
    # write-up checklist, differing in that flag alone: merging the two
    # invocations gives a chapter and a silence where the allocation reading
    # was asked for. Refuse instead, here, where the flags are still visible
    # as flags.
    # `--in-place` is read only inside the four installing modes, so
    # given alone -- or with a reading mode -- it printed a table,
    # wrote nothing and exited 0, which is the silence this loop
    # exists to refuse.
    if args.in_place and not (args.markdown or args.fingerprint
                              or args.block or args.claims):
        p.error('--in-place is a modifier of --markdown, --fingerprint,'
                ' --block or --claims and does nothing alone')
    for flag, needs in (('alloc', 'compare'), ('chapter', 'compare'),
                        ('quiet', 'check_doc')):
        if getattr(args, flag) and not getattr(args, needs):
            p.error('--%s is a modifier of --%s and does nothing alone'
                    % (flag, needs.replace('_', '-')))
    # `--classes` has two owners since --extremes, and had none of this
    # before: given to any other mode it was read by nobody and the mode
    # printed as though the files had not been named. --extremes is the
    # one that cannot proceed without it, so it is refused rather than
    # dropped.
    if args.classes and not (args.fingerprint or args.extremes):
        p.error('--classes is a modifier of --fingerprint and --extremes'
                ' and does nothing alone')
    if args.extremes and not args.classes:
        p.error('--extremes ranks the populations named by --classes, and'
                ' none were given')
    # `--brief` is read inside --aa and --block alone, so `--markdown
    # --brief` printed the full table at exit 0 saying nothing -- the same
    # silence the loop above refuses, one flag it did not cover.
    # The two compatibility flags are READ and not merely accepted: each
    # pins the behaviour that is now the default, so an old recipe keeps
    # working AND keeps meaning what it meant if a default moves again.
    # An accepted-but-unread flag is a defect family this directory's
    # own source lint refuses, and it caught both of these.
    if args.brief:
        args.verbose = False
    if args.quiet:
        args.worklists = False
    if args.verbose and not (args.aa or args.block or args.compare
                             or args.wild):
        p.error('--verbose restores what --aa, --block and --compare drop'
                ' and does nothing alone -- under --wild it adds the'
                ' per-sample dump the per-bench table sums')
    # One mode an invocation. The dispatch below is an if/elif chain, so a
    # second mode was not refused but DROPPED: `--markdown --fingerprint
    # --in-place` installed the Results table, wrote neither fingerprint
    # table and said nothing about it. Both found 2026-08-17 by review.
    modes = [f for f in ('shapes', 'aa', 'pair', 'claims', 'compare',
                         'machine', 'steps', 'cells', 'markdown',
                         'fingerprint', 'block', 'selftest', 'lint',
                         'check_doc', 'para', 'wild', 'deflation',
                         'extremes')
             if getattr(args, f)]
    # --block takes --compare as a SUB-FLAG, the way --chapter and --alloc
    # do, because item 5 of the class-block form is a cross-half line and
    # a block that cannot see the other half cannot write it. The guard
    # exists to catch two MODES asked for at once; this is one mode with
    # its second file.
    if args.block and args.compare and len(modes) == 2:
        modes = ['block']
    # ...but only --compare. Relaxing the guard for one sub-flag put back
    # exactly what it exists to stop: `--block --compare X --chapter` ran
    # the block and dropped --chapter without a word, because --chapter is
    # not itself in `modes`.
    clash = [f for f in ('chapter', 'alloc', 'ci', 'bridge')
             if args.block and getattr(args, f)]
    if clash:
        p.error('--block takes --compare and nothing else; %s %s a reading'
                ' of its own, so run it separately'
                % (', '.join('--' + f for f in clash),
                   'is' if len(clash) == 1 else 'are'))
    if len(modes) > 1:
        p.error('one mode at a time, and %s were all asked for: the'
                ' dispatch runs the first and drops the rest without a'
                ' word' % ', '.join('--' + f.replace('_', '-')
                                    for f in modes))
    # ONE READING an invocation holds among the --compare sub-flags
    # too: the dispatch is an if/elif chain over them, so `--compare X
    # --alloc --ci` ran --alloc and dropped --ci without a word -- the
    # silent drop the one-mode guard above refuses, one level down. The
    # pairwise guards this replaces covered every pair but --ci's,
    # which arrived with the same commit and missed its own roll call.
    subs = [f for f in ('chapter', 'alloc', 'ci', 'bridge')
            if getattr(args, f)]
    if len(subs) > 1:
        p.error('%s are %d readings of --compare, not one: run the'
                ' invocations README\'s checklist spells out, one at a'
                ' time' % (' and '.join('--' + f for f in subs), len(subs)))
    if args.ci and not args.compare:
        p.error('--ci is a reading ACROSS two runs: give it --compare')
    if args.bridge and not args.compare:
        p.error('--bridge is a reading ACROSS two runs: give it --compare')

    if args.replace:
        if not args.with_:
            sys.exit('--replace wants --with FILE, the replacement text')
        sys.exit(splice(args.readme, args.replace, args.with_))
    if args.para:
        sys.exit(paragraphs(args.readme, args.para))
    if args.check_doc:
        sys.exit(check_doc(args.readme, args.main) if args.worklists
                 else check_doc_quiet(args.readme, args.main))
    if args.lint:
        sys.exit(lint(args.main, args.readme))
    if args.extremes:
        missing = [c for c in args.classes if not os.path.exists(c)]
        if missing:
            sys.stderr.write('%s: no such run file(s); the rank did not'
                             ' happen\n' % ', '.join(missing))
            sys.exit(2)
        sys.exit(extremes_table(args.classes, args.main, args))
    if args.run is None:
        p.error('a run file is required for everything but --lint,'
                ' --check-doc and --extremes')
    if not os.path.exists(args.run):
        sys.stderr.write('%s: no such run file; the analysis did not happen\n'
                         % args.run)
        sys.exit(2)
    # ABOVE the JSON load, this mode's argument being the instrument's log:
    # everything below parses `args.run` as criterion output, so a `.log`
    # reaching it dies in `json.load` rather than in a sentence.
    if args.wild:
        if args.run.endswith('.json'):
            sys.stderr.write('%s: --wild reads the `@@wild` stamps, which are'
                             ' on stderr and so in the .log beside this'
                             ' file\n' % os.path.basename(args.run))
            sys.exit(2)
        sys.exit(wild_table(args.run, args.verbose))
    cells, shapes, strategies, meta = load(args.run, args.main)
    shapes = [s for s in shapes if s not in args.exclude_shape]
    strategies = [s for s in strategies if s not in args.exclude]
    # Before --no-controls, so that omitting the controls from the aggregates
    # cannot change what the published column means.
    terms = apply_correction(cells, shapes, strategies, args.corr)
    if args.no_controls:
        # `--aa` and `--block` READ the controls -- the module docstring
        # says they are always listed by --aa -- and this filter reached
        # the list they build their pairs from, so `--aa --no-controls`
        # reported a file carrying eighteen of them as having none, and
        # `--block --no-controls` dropped the Controls paragraph and the
        # summary-row check without a word. It is a modifier of the
        # aggregates and those two are not aggregates. Found 2026-08-17.
        if args.aa or args.block:
            p.error('--no-controls drops the controls from the AGGREGATES,'
                    ' and --aa and --block are what reads them; the two'
                    ' cannot be combined')
        strategies = [s for s in strategies if not is_control(s)]
    if not shapes or not strategies:
        sys.exit('nothing left after --exclude')
    holes = [(sh, st) for sh in shapes for st in strategies
             if st not in cells[sh]]
    if holes:
        # AHEAD OF EVERY MODE, --selftest included. The guard sat below the
        # roster banner, which is below this dispatch, so the one mode
        # `read-all.sh` calls first was the one mode it did not cover --
        # and read-all.sh getting a traceback where a gate verdict belongs
        # is the thing the guard was written for. Found 2026-08-16 by
        # driving the driver, having been proven by hand on a mode that
        # happened to sit on the right side of it.
        sys.stderr.write(
            '%s: %d cell(s) missing, so the analysis did not happen. The'
            ' first few: %s\n'
            % (os.path.basename(args.run), len(holes),
               '; '.join('%s/%s' % h for h in holes[:5])))
        sys.exit(2)

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
    if args.corr != 'sumonly':
        print('corrected by the IN-SITU term (--corr=insitu), not `sum-only`')
    print()
    health(cells, shapes, strategies, terms, args.corr)
    if args.shapes:
        shape_table(cells, shapes, strategies, meta)
    elif args.aa:
        aa_table(cells, shapes, strategies, terms, meta, not args.verbose)
    elif args.pair:
        pair_table(cells, shapes, strategies, args.pair)
    elif args.claims and args.in_place:
        install_readings(args.readme,
                         claims_readings(cells, shapes, strategies),
                         args.run, strategies, shapes, args.main)
    elif args.claims:
        claims_table(cells, shapes, strategies, args)
        claims_in_doc(args.readme, cells, shapes, strategies, args.run,
                      args.main)
    elif args.compare and args.block:
        # --block owns the pair here: --compare is its second file and not
        # a mode of its own, so it has to be tested before the plain
        # --compare arm below claims it.
        block_skeleton(cells, shapes, strategies, meta, args, terms)
    elif args.compare and args.chapter:
        chapter_skeleton(cells, shapes, strategies, meta,
                         args.compare, args.main)
    elif args.compare and args.alloc:
        compare_alloc(cells, shapes, strategies, meta, args.compare,
                      args.main)
    elif args.compare and args.ci:
        sys.exit(compare_ci(cells, shapes, strategies, meta, args.compare,
                            args.main))
    elif args.compare and args.bridge:
        sys.exit(bridge_table(cells, shapes, strategies, meta, args.compare,
                              args.main, args.band))
    elif args.compare:
        compare_table(cells, shapes, strategies, meta, args.compare,
                      args.main, not args.verbose)
    elif args.deflation:
        sys.exit(deflation_table(args.run, cells, shapes, args.main))
    elif args.machine:
        sys.exit(machine_check(cells, shapes, args.readme))
    elif args.steps:
        step_table(args.run, cells, shapes, strategies, meta)
    elif args.cells:
        cell_dump(cells, shapes, strategies)
    elif args.markdown:
        text = capture(markdown_table, cells, shapes, strategies, meta,
                       args, terms)
        emit_or_install(text, args, shapes, meta)
    elif args.fingerprint:
        classes = []
        for path in (args.classes or []):
            c_cells, c_shapes, c_strats, c_meta = load(path, args.main)
            apply_correction(c_cells, c_shapes, c_strats)
            classes.append((class_prefix(c_shapes), c_cells, c_shapes,
                            c_meta['dims']))
        text = capture(fingerprint_table, cells, shapes, strategies, meta,
                       classes)
        emit_or_install(text, args, shapes, meta)
    elif args.block:
        text = capture(block_skeleton, cells, shapes, strategies, meta,
                       args, terms)
        emit_or_install(text, args, shapes, meta, block=True)
        summary_row(cells, shapes, strategies, args, args.main)
        lead_shapes(shapes, args, args.main)
    else:
        strategy_table(cells, shapes, strategies, meta, args, terms)


if __name__ == '__main__':
    main()
