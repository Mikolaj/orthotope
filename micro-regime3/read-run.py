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
          not make a cell better measured. `sum-only*`, `*-nosum` and the
          `*-sum` reducing consumers have no corrected time and read `--`:
          each produces nothing to force, so the term measured on
          `sum-only` is not theirs to subtract. The consumers joined them
          2026-09-10, after the correction ran five of their rows entirely
          non-positive; `no_net` is the predicate and its docstring carries
          the case. They are CANDIDATES still, and `is_control` does not
          reach them.
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
  --pair A B --per-shape  and the per-shape ratios the range line is a max
                    and min of, which is where a crossover lives
  --compare OTHER   compare one arm across two runs of the same population,
                    every arm at once -- what a paired run's two halves want.
                    ITS RATIO IS A PLAIN GEOMEAN of the per-shape net
                    ratios, NOT the winsorized one the `time` column above
                    is: the two are different statistics and they part on
                    any arm with a capped cell, and they can part in SIGN:
                    Run 31's `mut-odo-vecdims-add-in-leaf-u2-aa` distant
                    copy reads 0.9981 here against its base and 1.0019
                    winsorized, one calling the copy faster and the other
                    slower, both inside that half's 0.61% floor
  --compare O --alloc   whether the two agree on what each arm allocates,
                    partitioned by size and never by column
  --compare O --bridge  each arm as a ratio to `list` IN ITS OWN RUN, per
                    shape, which cancels a box change exactly where the
                    plain --compare reads absolutes and cannot; given no
                    --compare, O is the same half of the note's COMPARE run
  --compare O --ci  each arm's CI% median against the other run's -- the
                    statistic the column publishes, and not the mean a
                    script over --cells reaches for
  --compare O --chapter the run chapter's own arithmetic, so that writing
                    one need not begin by reading the last one
  --compare O --predictions  adjudicate the registration's `predict:`
                    spans from the two runs, each on the population and
                    half it names, HELD or KILLED with the figure read,
                    and name the items carrying no span or script as
                    yours; `--counts A B` beside it for the count spans
  --carried --others J...  every figure the registration QUOTES from an
                    earlier run, against that run: each `pair A B` span
                    derived on the JSONs given, one per population the
                    items are read on, and the item named where nothing
                    it quotes matches anything its own span produces. The
                    spans are what --predictions adjudicates; the figures
                    beside them in prose were read by nothing, and a
                    wrong one is a plausible number next to a correct arm
  --carry-over      this run's registration against the previous run's as
                    it stood BEFORE that run, item by item, read out of
                    git rather than from its run file, whose copy carries
                    a verdict per item; it names the words that moved and
                    judges none
  --counts SWEEP.txt --pair A B   the other arity: two arms' instruction
                    counts on ONE half, corrected against the shared
                    forcing pass and raw beside it, which is what a
                    registration comparing two arms on one binary turns
                    on. Two sweep files with `--compare` is the cross-half
                    reading and the older one. `--per-shape` adds each
                    shape's raw difference A - B beside how far the
                    sweep's two copies of the forcing pass part, the
                    resolution such a difference is read against
  --series A B SHAPE [DIR]  A over B on SHAPE on every run's main set in
                    DIR, run by run and half by half, each beside that
                    half's floor: one cell's readings as a table rather
                    than a list requoted in prose run after run
  --record [NAME]   a series README keeps as data and not as prose,
                    from series/NAME.tsv, aligned: `floor`, `regime`,
                    `selfloops`; alone, lists them. A write-up appends
                    its run's row, and the prose says what the series
                    shows
  --steps           every cell read at sample level for a mid-bench change
                    of level, which the fitted slope averages away and no
                    other column here can show
  --winsor          each timed row's PLAIN per-shape geomean beside the
                    published winsorized one, with how many cells the
                    cap touched: what the `time` column owes to its own
                    estimator rather than to the arm. A row whose shapes
                    span widely is published at a figure its cells do
                    not average to, and the gap is not stable between
                    runs -- `--compare` carries the cross-run half of
                    the same question
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
                    when the whole baseline moved, and refuses a run its
                    OWN fingerprint, which post-run 5b installs
  --cells           every cell as TSV, for anything not covered above
  --markdown        the run file's Results table, numbers recomputed and
                    the editorial column carried over from the one there --
                    six columns instead for a stride-class run, and none
                    at all for a run spanning two populations
  --fingerprint     the kept per-shape record (What the next run compares
                    against): dims, `list`'s net per call, and per shape
                    the cross-class summary's three cells, as two tables
  --block           a stride-class block's mechanical parts in the form's
                    order: table, controls, provenance/anchor skeleton,
                    a three-shape population's per-shape line, and the
                    three properties' verdicts derived rather than eyeballed
  --in-place        with --markdown, --fingerprint or --block, install the
                    tables into the RUN'S file instead of printing them --
                    never into README.md, which carries none of them:
                    matched by
                    whole line, count asserted, a class table narrowed by
                    its block's lead, and refusing rather than guessing
  --exclude S       drop strategy S from every aggregate (repeatable)
  --exclude-shape H drop shape H likewise (repeatable)
  --pin OTHER.json  keep only the shapes OTHER has too, which is what
                    `match bases before reading any ratio` asks of every
                    cross-run figure -- the predecessor's own column read
                    over this run's population, in one flag instead of one
                    `--exclude-shape` per retired shape. Says on stderr
                    what it kept and what it dropped
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
  --check-doc       anchors, the paths the documents name, replace-list
                    coverage, widths, and a sweep of the superseded figures
                    still quoted -- over README.md AND the run's own file
                    together, and over Main.hs comments -- no run needed.
                    Three counts are held to MAIN.HS and not to the
                    documents' own other sentences: the A/A population,
                    the class-block count and the class table's `shapes`
                    column. Sites agreeing with each other say only that
                    they were edited together
  --checklist WHICH print one of the run chapter's three checklists, pre,
                    run or post, alone and sized -- and `post-a` or
                    `post-b` for the post list's two halves, which are cut
                    at step 6: nothing below that is actionable until 5b's
                    tables are in -- no run needed. Each step prints
                    through its `why:` line and no further; `--full`
                    prints the reasons under it too
  --note PREV       the blocks of a previous pair note that a preparation
                    DECIDES. Three kinds are withheld and the size said
                    -- the handover and the gate, spent with that run,
                    and the `[SAME]` blocks, which --draft carries over, so
                    reading one here is reading a block you will not type
  --note PREV --draft R --halves B,O   and instead the WHOLE note, which
                    is reading-list item 10 as a preparation owes it: each
                    `[SAME]` block from the template, with this pair's
                    names and the previous LAUNCH and RIDERS values put in,
                    or from the note with the names carried over where the
                    template has none; each `[PAIR'S]` block the previous
                    note's, as a model under a `<yours>` line to rewrite;
                    the handover and the gate as slots, and the fill-in
                    block as labels and `<yours>` -- so a note is one file
                    filled in rather than three assembled, and
                    `preflight.sh R --fill-in` derives most of those rows
                    -- no run needed
  --section NAME    print one section's prose by its heading's words,
                    without its tables and naming the size withheld;
                    --with-tables adds them and --with-tables N takes the
                    Nth alone, which is item 4's ONE table -- no run needed
  --para PATTERN    print the paragraphs whose bolded lead matches, from
                    either document, with the file and line each starts
                    at -- no run needed
  --run-doc FILE    the run's own file, `runs/run<N>.md`, which carries
                    everything a run replaces and is what every --in-place
                    install writes; defaults to the newest in runs/

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

**--selftest is the numeric half of that and `defects.py` is the
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
import ast
import collections
import contextlib
import datetime
import difflib
import functools
import glob
import importlib.util
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
import tempfile
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
    the view being neither, and 'mkWindowChannels' image, channels and
    kernel. In every case m = l / sInner is the run count
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

    # four entries are image and kernel; six add the window stride and
    # the kernel dilation, as mkWindow reads them since 2026-09-03
    def window(ds, _):
        h, w, kh, kw = ds[:4]
        s, d = (ds[4], ds[5]) if len(ds) == 6 else (1, 1)
        span = lambda k: (k - 1) * d + 1  # noqa: E731
        out_h, out_w = (h - span(kh)) // s + 1, (w - span(kw)) // s + 1
        return out_h * out_w * kh * kw, kh

    # image, channels and kernel, as mkWindowChannels reads them since
    # 2026-09-09: unstrided and undilated, the channel axis between the
    # output positions and the kernel
    def window_channels(ds, _):
        h, w, c, kh, kw = ds[:5]
        return (h - kh + 1) * (w - kw + 1) * c * kh * kw, kh

    # the run is everything under the outer dim, merged or not
    def runs(ds, _):
        return math.prod(ds), math.prod(ds[1:])

    sh_re = r'(?P<dims>\[[^\]]*\])'
    blocks = [
        ('convShapes', sh_re, strided),
        ('stretchShapes', sh_re, strided),
        ('revShapes', sh_re, strided),
        ('revSomeShapes', r'\[[^\]]*\],\s*' + sh_re, strided),
        ('broadcastShapes', sh_re, listed),
        ('broadcastMidShapes', r'(?P<b>\d+),\s*' + sh_re, bcastmid),
        ('reshape1Shapes', sh_re, reshape1),
        # Same rule: the appended dim is size 1, so sInner is 1 and
        # m = l, and `l` is the dense shape's product either way.
        ('reshape1StridedShapes', sh_re, reshape1),
        ('slicedShapes', sh_re, strided),
        ('windowShapes', sh_re, window),
        # Image, kernel and (stride, dilation): one dims group spanning
        # both, so the six-entry window rule sees them. Its own list, so
        # a reader older than the rule never meets a six-entry row.
        ('windowStridedShapes',
         r'(?P<dims>\[[^\]]*\],\s*\(\d+,\s*\d+\))', window),
        ('windowChannelShapes', sh_re, window_channels),
        ('scaledViews', sh_re + r',\s*Strides\s*\[[^\]]*\]', listed),
        ('runsShapes', sh_re, runs),
        # The four classes of 2026-09-03: each lists the view shape
        # itself, beside reversed dims, an enclosing shape and offset, a
        # regime and strides, or strides and offset.
        ('flipShapes', r'\[[^\]]*\],\s*' + sh_re, listed),
        ('blockViews', sh_re + r',\s*\[[^\]]*\],\s*\d+', listed),
        ('smallViews', r'\d+,\s*' + sh_re + r',\s*Strides\s*\[[^\]]*\]',
         listed),
        ('composeViews', sh_re + r',\s*Strides\s*\[[^\]]*\],\s*\d+', listed),
        # 2026-09-05: a regime, reversed dims, the view shape and an
        # enclosing shape. Its own list, so a reader older than the rule
        # never meets a five-field row.
        ('flipInViews', r'\d+,\s*\[[^\]]*\],\s*' + sh_re + r',\s*\[[^\]]*\]',
         listed),
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
                # `cls` is the population a shape belongs to and `lst`
                 # is merely where it is declared. They were one thing
                 # until 2026-08-25, when `reshape1-strided-r3` needed a
                 # different constructor and so a second list: the
                 # reshape1 class then read as TWO populations, which made
                 # `--block`, `--extremes` and `--markdown` refuse it
                 # outright and made `summary_row` and `lead_shapes`
                 # return in silence. The prefix is what the binary
                 # itself selects a class by (`classes reshape1-`) and
                 # what `class_prefix` and every block lead already use,
                 # so this makes one definition of a class where there
                 # were two.
                out[m.group(1)] = dict(
                    dims=ds, l=l, s_inner=s_inner, lst=start,
                    cls=('main' if start in MAIN_LISTS
                         else m.group(1).split('-')[0]),
                    m=(l // s_inner if s_inner else 0))
                if m.group('ann'):
                    ann[m.group(1)] = int(m.group('ann'))
            elif line.strip() == ']':
                break
    # `retired`: listed for `check` and not timed, a main shape by name
    # and a class shape by its class (2026-09-04). Every consumer of the
    # binary's roster reads it; a run file that timed one is exempted by
    # the provenance bullet's declaration, in check_doc.
    rsh, rcl = retired_shapes(main_hs), retired_classes(main_hs)
    for sh, d in out.items():
        d['retired'] = (sh in rsh if d['cls'] == 'main'
                        else d['cls'] in rcl)
    return out, ann


# The two lists that make up the main set. Every other list dims_by_shape
# reads is one stride-class population, timed one process per class
# (README.md#making-a-major-benchmark-run).
MAIN_LISTS = ('convShapes', 'stretchShapes')


RETIRED_RE = re.compile(r'^retiredClasses\s*=\s*\[([^\]]*)\]', re.M)


def retired_classes(main_hs):
    """The classes Main.hs retires from timing and keeps in `check`.

    `retiredClasses` there, by prefix; the shape lists stay, so
    `dims_by_shape` still reads their shapes and a class count has to take
    these out -- except for a run file that timed them, which README's
    provenance bullet declares as `were retired DATE, after the run`,
    exactly as it declares shapes added after one. Added 2026-09-04.
    """
    try:
        m = RETIRED_RE.search(open(main_hs).read())
    except OSError:
        return set()
    return set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()


RETIRED_SHAPES_RE = re.compile(r'^retiredShapes\s*=\s*\[([^\]]*)\]', re.M)


def retired_shapes(main_hs):
    """The main-set shapes Main.hs retires from timing and keeps in
    `check`: `retiredShapes` there, by name, the lists staying as the
    classes' do. `dims_by_shape` marks them `retired`. Added 2026-09-04."""
    try:
        m = RETIRED_SHAPES_RE.search(open(main_hs).read())
    except OSError:
        return set()
    return set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()


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
            groups.setdefault(d['cls'], []).append(sh)
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
            rows = sorted({r for _, _, r in sunk})
            # THE ROWS AND NOT EVERY CELL. This line used to enumerate
            # each sunk `shape/arm` between the worst cell and the row
            # coverage, which is the same information a second time and
            # is the bulk of it -- seventy pairs on Run 27's main set, on
            # EVERY reader call, where the coverage below is what a
            # reader acts on and `--cells` is where a cell lives. Cut
            # 2026-09-08; the count, the worst cell and the coverage
            # stay, so nothing here is quieter, only shorter.
            out.append('%d cell(s) whose forcing term is not smaller than the'
                       ' cell itself, worst %s/%s -- the arm removed the work'
                       ' there, so each reads `--` and %d row(s) are geomeans'
                       ' over fewer shapes than the rest: %s. The cells'
                       ' themselves are `--cells`, whose net column is'
                       ' non-positive for these and for the `sum-only` and'
                       ' `-nosum` controls this count exempts'
                       % (len(sunk), sh, st,
                          len(rows),
                          ', '.join(
                              '%s over %d of %d' % (r, n, len(shapes)) if n
                              else '%s not readable at all' % r
                              for r, n in
                              ((r, len(live_shapes(cells, shapes, r)))
                               for r in rows))))
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
        # Not readable rather than divided: `--aa` used to die inside
        # `geomean` with `math domain
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
populations. README calls this the carry-back figure, the six-pair figure
until 2026-09-11, and holds it to two sites; before Run 17 it was derived
by hand at the write-up, which is where it was first quoted three ways.
"""

# The middle anchor was `cifar-L2-16-c64-k3` through Run 24, retired
# 2026-09-04; `cnn-L2-24x24-c32` is the same canonical pattern within a
# tenth in run count, and its anchor history starts at Run 25.
ANCHORS = ('cnn-slice-c32', 'cnn-L2-24x24-c32', 'stretch-wide-2xM')
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


def no_forcing_pass(name):
    """The two CONTROL families that never produce a result to force.

    Held apart from `no_net` since 2026-09-10, when the reducing consumers
    joined that predicate: nothing nets them either, but they are
    candidates and stay in the published column, where a control does not.
    One spelling for both callers, which is the whole point of `no_net`
    having been named in the first place.
    """
    return name.startswith('sum-only') or name.endswith('-nosum')


def no_net(name):
    """Has this arm no corrected time? It never ran the forcing pass.

    Named because it was spelled out at eight sites and two of them did
    not spell it alike -- `health` wrote the two halves as separate `not`
    clauses and `selftest` tested membership of its own `sum-only` list --
    so a third control class, or a renamed suffix, had to be found in
    eight places by a grep that missed two of them.

    THE `-sum` CONSUMERS ARE HERE SINCE 2026-09-10, by this predicate's
    own words: a reducing consumer returns a scalar and takes the fold
    into the walk, so it produces nothing to force and no forcing pass was
    ever run for it. Subtracting the term measured on `sum-only`, which
    materialises and then sums, took off them work they never did -- far
    enough that Run 28's roster pass found five rows with EVERY cell
    non-positive, on `bcast` and on `flip`, the arm reading faster than
    the control whose cost was being subtracted (`flip-fwd-rows96` /
    `libunord-stage7-sum` at 0.00074 s against `sum-only-early`'s
    0.00108). Their spans read raw, which is what `pair_stats` does with a
    `no_net` half AND, since dc2bf44, what the `cross` branch of
    `--predictions` does too. This paragraph said instead that every span
    the registrations write over such an arm is a `pair`, which held until
    Run 29's item (3) wrote a `cross` over `libunord-stage7-sum`: the
    branch divided `net` and dropped every shape whose net was not
    positive, reading 0.5854 over 3 shapes of 14 on `runs` where the raw
    ratio over all 14 is 0.9779, and nothing at all on `block`.
    """
    return no_forcing_pass(name) or name.endswith('-sum')


def is_control(name):
    """Excluded from the published column: the A/A twins and the two
    control families.

    NOT `no_net`, which is wider since 2026-09-10. A reducing consumer has
    no corrected time and is still a CANDIDATE; filing it here would drop
    every one of them out of every table and fail `--selftest` besides, whose
    roster check holds an arm this calls a control to a Twin, Term or
    Force role in Main.hs, and Main.hs files them as candidates.
    """
    return '-aa' in name or no_forcing_pass(name)


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


def live_shapes(cells, shapes, strategy):
    """The shapes this row's ratio to `list` can be taken over.

    A cell the forcing term did not leave positive is not a broken
    measurement. It is a fill whose work the arm REMOVED: what is left in
    the bench is the forcing pass, and there is nothing per-element for a
    per-element term to be subtracted from. The canonicalizing arms reach it
    by construction, on the views they turn into regime 1
    (README.md#sum-only-and-the-correction-now-applied) -- so refusing the
    whole row over one such cell left `canon-full` with no `time` figure at
    all on the main set, and three arms with none in `reshape1`, which are
    the arms Run 20 was rostered to read. Measured 2026-08-26 at -L1, before
    that run was paid for.

    So the cell is dropped and SAID, exactly as `aa_pairs` drops a control
    pair and says so: `health` names the cells and the rows that lost one,
    and `--selftest` names them again as a property rather than as a fault.
    What is NOT dropped is a sunk BASELINE cell, which takes every row of its
    shape with it and stays a fault, nor a row left with nothing.

    The cost is the one `time_of` states: two rows of one table may then
    cover different shape sets, so a comparison between them is the reading's
    to make rather than the column's to assert. That is what the printed
    count is for, and why the drop is not silent.
    """
    if any('list' not in cells[s] for s in shapes):
        return []
    # The baseline's own sunk cell is not dropped with the others and is not
    # a shape this row loses: it takes EVERY row of that shape with it, so
    # the row has no readable population at all. Held here rather than at
    # each caller, which is how the first draft of this leaked -- `time_of`
    # kept its own baseline guard and returned nan while the bracket check
    # below took the filtered list and compared that nan against a range,
    # turning one sunk baseline into a FAIL per row. 2026-08-26.
    if any(cells[s]['list']['net'] <= 0 for s in shapes):
        return []
    return [s for s in shapes if cells[s][strategy]['net'] > 0]


def worst_of(cells, shapes, strategy):
    """The strategy's worst shape, as a ratio to `list`.

    A geomean answers "typical" and no robust version of it can answer "how
    bad does this get" -- the two questions want different statistics. For a
    library fallback the second is the disqualifying one: a strategy three
    times its own average on some shape is not shippable whatever its mean
    says. Being a maximum it is also the one figure no estimator choice can
    flatter.

    Reads `--` on exactly what `time_of` reads `--` on, and drops exactly
    what it drops: a sunk cell is left out of the maximum rather than taking
    the row with it (`live_shapes`), and a sunk BASELINE cell reads `--` here
    as there. The two used to disagree -- a shape whose forcing term was not
    smaller than the cell published a plausible `worst` beside a `time --` in
    the same README row -- which is the defect of 2026-08-17 that made them
    share a rule. What changed on 2026-08-26 is the rule and not the sharing.
    """
    if no_net(strategy):
        return float('nan')
    live = live_shapes(cells, shapes, strategy)
    if not live:
        return float('nan')
    return max(cells[s][strategy]['net'] / cells[s]['list']['net']
               for s in live)


def time_of(cells, shapes, strategy):
    """README's `time` column: winsorized geomean of net / `list`'s net.

    Over every shape whose cell the correction can read, which was every
    shape of every run before Run 20. Nothing is dropped for being an
    OUTLIER -- a cell far enough out to distort the mean is capped instead,
    which bounds its influence without deleting its evidence, and 'winsorize'
    records why that beats dropping a cell. What is dropped is a cell the
    forcing term did not leave positive, which is not an outlier but the
    absence of the quantity (`live_shapes`); the row then covers fewer shapes
    than its neighbours, `health` says which rows and over how many, and a
    comparison between two rows of different coverage is the reading's.

    A filtered run need not contain the baseline; then there is no ratio to
    give and the column reads nan rather than the reader stopping. So does a
    `sum-only` or `-nosum` arm, which never ran the forcing pass, a shape
    whose `list` the term did not leave positive, and a row with no readable
    cell left at all.
    """
    if no_net(strategy):
        return float('nan')
    live = live_shapes(cells, shapes, strategy)
    if not live:
        return float('nan')
    logs = [math.log(cells[s][strategy]['net'] / cells[s]['list']['net'])
            for s in live]
    return math.exp(stats.fmean(winsorize(logs)[0]))


def winsor_table(cells, shapes, strategies):
    """What the published `time` column owes to its own estimator.

    The column is a WINSORIZED geomean of net over `list`'s net, capped at
    3 MADs of the log, and both the median and the MAD are that row's own
    and that run's own. So a row whose shapes span widely is published at a
    figure its cells do not average to, and the gap is not stable between
    runs: Run 31 published `lib-stage2-lean-u1` at 0.029 and Run 32 at
    0.025 on an arm that moved 1.6%, the same four cells capped in both and
    the cap they were pulled to halved with the row's MAD.

    This prints the two side by side so the gap is read rather than
    reimplemented -- it was reimplemented by hand on 2026-09-15, which is
    the day this mode was asked for. `--compare` carries the cross-run half
    of the same question, flagging a row whose two published figures divide
    to something the paired ratio does not.
    """
    print('\nwinsorizing, per timed row: the plain per-shape geomean beside'
          ' the published one')
    print('%-38s %9s %9s %8s %7s' % ('strategy', 'plain', 'published',
                                     'gap', 'capped'))
    worst, n_rows = None, 0
    for st in sorted(strategies):
        if no_net(st):
            continue
        live = live_shapes(cells, shapes, st)
        if not live:
            continue
        logs = [math.log(cells[s][st]['net'] / cells[s]['list']['net'])
                for s in live]
        capped, n_capped = winsorize(logs)
        plain = math.exp(stats.fmean(logs))
        pub = math.exp(stats.fmean(capped))
        gap = pub / plain - 1
        n_rows += 1
        if worst is None or abs(gap) > abs(worst[1]):
            worst = (st, gap)
        print('%-38s %9.5f %9.5f %7.1f%% %4d/%-3d'
              % (st, plain, pub, gap * 100, n_capped, len(live)))
    if not n_rows:
        print('  no timed row here, so the column has nothing to winsorize')
        return 2
    print('\nA row whose two columns part is a row whose published figure is'
          ' partly its own')
    print('spread. The widest here is `%s` at %.1f points. Quote the'
          ' published column' % (worst[0], abs(worst[1]) * 100))
    print('for reading the table and `--pair` for a margin; for a row across'
          ' two runs')
    print('quote `--compare`, which flags that division itself.')
    # AND THE CENSUS OVER EVERY PAIR OF THOSE ROWS, since 2026-09-17: two
    # rows' published figures divide to a ratio the paired geomean can
    # part from in SIGN, and a sentence saying which pairs do is a claim
    # about every pair. Run 34 took that census by hand to write `DO NOT
    # DIVIDE`. A pair with a sunk cell is left out and counted, and `list`
    # is left out, its column being the one the table above reads. The
    # widest is relative, column over paired, which a ratio of thirty does
    # not swamp.
    rows = [st for st in sorted(strategies) if st != 'list'
            and not no_net(st) and live_shapes(cells, shapes, st)]
    parted, widest, n_pairs, sunk_pairs = [], None, 0, 0
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            key, sunk = pair_sunk(cells, shapes, a, b)
            if sunk:
                sunk_pairs += 1
                continue
            col = time_of(cells, shapes, a) / time_of(cells, shapes, b)
            paired = geomean([cells[x][a][key] / cells[x][b][key]
                              for x in shapes])
            if col != col:
                continue
            n_pairs += 1
            if (col - 1) * (paired - 1) < 0:
                parted.append((a, b, col, paired))
            if widest is None or (abs(math.log(col / paired))
                                  > abs(math.log(widest[2] / widest[3]))):
                widest = (a, b, col, paired)
    print('\n%d pair(s) of timed rows other than `list`%s: %d part in sign'
          ' between the'
          ' published column\'s ratio and the paired geomean%s'
          % (n_pairs, ', %d more with a sunk cell left out' % sunk_pairs
             if sunk_pairs else '', len(parted),
             ' -- %s' % '; '.join('`%s` over `%s` column %.4f, paired %.4f'
                                  % p_ for p_ in parted[:6])
             + ('; ...' if len(parted) > 6 else '') if parted else ''))
    if widest:
        print('  the widest disagreement: `%s` over `%s`, column %.4f against'
              ' paired %.4f, the column %+.1f%% off it'
              % (widest + ((widest[2] / widest[3] - 1) * 100,)))
    return 0


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



def property_closest(cells, shapes, key, a, b):
    """A property clause's closest shape: ((largest a/b on `key`, its
    shape), shapes read), or None where no shape reads both."""
    rs = [(cells[sh][a][key] / cells[sh][b][key], sh) for sh in shapes
          if cells[sh].get(a, {}).get(key) is not None
          and cells[sh].get(b, {}).get(key) is not None
          and cells[sh][b][key] > 0 and cells[sh][a][key] >= 0]
    return (max(rs), len(rs)) if rs else None


def property_clauses(cells, shapes, strategies):
    """Properties 1 and 2 of the class blocks, read per shape.

    Property 1 is `worst` under 1 and `mut-odo-vecdims` ahead of
    `bq-expand` on every shape, property 2 the same two inequalities in
    allocation, `mut-odo-vecdims` under `list` and under `bq-expand` on
    every shape to within 1%, on the `alloc` multiple each cell carries;
    the set is stated in the run file's properties section and restated there
    on 2026-09-06, when the top-of-the-table ordering that was property 2
    retired, and the margin dates from 2026-09-07, the strict form having
    broken on its first reading on ties of tens of bytes per call where
    both arms allocate one result vector and nothing else, `small-row96`
    the widest at 1.00441. The `worst` clause is the table's own column,
    so this prints the other three, each with its closest shape -- what
    a write-up quotes -- and how many shapes it read, a cell with no
    readable value being dropped as `worst` drops a sunk one. Printed by
    `--block` for a class and by the default mode for the main set, which
    `--block` refuses, so both kinds of population get the same reading.
    """
    def clause(label, key, a, b, bound):
        c = property_closest(cells, shapes, key, a, b)
        if c is None:
            print('  %s: not read, no shape has a readable `%s` for both'
                  ' `%s` and `%s`' % (label, key, a, b))
            return
        (r, sh), n = c
        print('  %s: %s -- closest `%s` at %s, over %d of %d shapes'
              % (label, 'HOLDS' if r < bound else '**BREAKS**', sh,
                 ('%.4f' if key == 'net' else '%.5f') % r, n, len(shapes)))

    clause('property 1, ahead of `bq-expand` on every shape', 'net',
           PLAIN, LAST_CANDIDATE, 1.0)
    clause('property 2, allocation at most 1% over `list` on every shape',
           'alloc', PLAIN, 'list', 1.01)
    clause('property 2, allocation at most 1% over `bq-expand` on every'
           ' shape', 'alloc', PLAIN, LAST_CANDIDATE, 1.01)

def strategy_table(cells, shapes, strategies, meta, args, terms):
    rows, have_list = strategy_rows(cells, shapes, strategies)
    print('%-28s %7s %6s %6s %6s %5s %8s'
          % ('strategy', 'time', 'worst', 'CI%', 'noise', 'smp', 'alloc'))
    for time, st, ci, noise, smp, alloc, worst in rows:
        mark = ' *' if is_control(st) else ''
        a = '%7.2fx' % alloc if alloc is not None else '      --'
        t = '     --' if time != time else '%7.3f' % time
        w = '     --' if worst != worst else '%6.3f' % worst
        c = '    --' if ci != ci else '%6.2f' % ci
        n = '    --' if noise != noise else '%6.2f' % noise
        print('%-28s %s %s %s %s %5.0f %s%s'
              % (st, t, w, c, n, smp, a, mark))
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
                 for st in ('list', PLAIN)}
        known = ' and '.join('%.1f%% of %s' % (100 * v, k)
                             for k, v in share.items() if v == v)
        print('time has the shared forcing pass subtracted from every row;')
        if known:
            print('that term is a median ' + known + ' over shapes.')
        print('The `sum-only` rows are that term, so they read -- rather than')
        print('a figure of a different kind in the same column.')
    print('worst is the row\'s worst shape: how bad it gets, which no average')
    print('answers. time is a winsorized geomean, outliers capped at %.0f MADs'
          % WINSOR_K)
    print('of the log (the MAD scaled by 1.4826, so the cap is in standard')
    print('deviations); a row drops a shape only where the correction leaves')
    print('no work to read, and the warning above names such rows.')
    print('noise is this row\'s CI% against the median CI% of the same shape,')
    print('medianed over shapes: 1.00 is an ordinary bench, and the')
    print('outlier is the bench to suspect of disturbing whatever shares')
    print('its process.')
    if meta['known_l'] < len(shapes):
        print('alloc missing for %d shape(s) Main.hs no longer defines'
              % (len(shapes) - meta['known_l']))
    if have_list:
        print('\nClass properties 1 and 2 on this population, per shape'
              ' (the `worst` column is the other clause of 1):')
        property_clauses(cells, shapes, strategies)


# The two headers `--markdown` emits, and the one `readme_rows` finds the
# Results table by. One literal, so that the emitter and the reader of the
# same table cannot drift apart -- which is a way for the carry-forward to
# stop finding anything and report every row as new.
CLASS_HDR = '| strategy | time | worst | CI% | smp | alloc |'
RESULTS_HDR = '| strategy | time | worst | CI% | smp | alloc | needs |'


def run_doc_mismatch(args, who):
    """Say that the JSON and the run file name different runs, and skip.

    The read half of the --in-place guard: `--block` on run19's JSON with
    run22.md newest judged one run's cells against another run's rows and
    filed the disagreements as hand-work, at exit 0. A JSON whose name
    carries no run number is not held -- there is nothing to compare.
    2026-09-01, by review.
    """
    m = re.match(r'run(\d+)-', os.path.basename(args.run or ''))
    now = run_no_of(want_run_doc(args))
    if m and now is not None and int(m.group(1)) != now:
        sys.stderr.write('%s not checked: %s is run %s\'s JSON and %s is'
                         ' run %d\'s file -- name the right one with'
                         ' --run-doc\n'
                         % (who, os.path.basename(args.run), m.group(1),
                            os.path.basename(want_run_doc(args)), now))
        return True
    return False


def want_run_doc(args):
    """The run file, or a refusal naming what is missing.

    Twelve sites read or write it and none may fall back to README.md: a
    run's tables and its class blocks live in `runs/run<N>.md` and
    nowhere else, so an absent file is a refusal and never a table
    installed over standing prose. `--in-place` with no run file is how
    that would have happened.
    """
    if args.run_doc:
        return args.run_doc
    sys.exit("no run file: this mode reads or writes `%s/run<N>.md`, which"
             " carries the Results table, the fingerprint and the class"
             " blocks, and that directory holds"
             " none. Make the file, or name it with --run-doc." % RUNS_DIR)


def readme_rows(readme, strategies, recognise=None):
    """The run file's Results table, by strategy: (label, style, needs).

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
        # THE `time` CELL TOO, since 2026-09-16: post-run 5a's movement
        # reading compares the published column this install is about to
        # overwrite against the one going in, and after the install it is
        # in git or in the kept JSON only. Carrying it here rather than
        # parsing the table a second time is what keeps the two readings
        # of one table from disagreeing.
        out[bare] = (cell[0], style, cell[-1], cell[1])
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


def flatten_paragraphs(text, only_bolded=False):
    """Blank-line blocks joined to ONE LINE EACH, which is the run file's form.

    Both arms that emit a class block print through this, so there is one
    behaviour and one line for a mutant to break. A caller that joins the
    wrapped form itself is the thing this removes: Run 36 did, a break fell
    inside `lib-stage2-lean-u1`, and `lib- stage2-lean-u1` reached the page.
    `only_bolded` leaves the terminal tables of the --compare arm alone,
    their columns being alignment rather than prose.
    """
    out = []
    for para in text.split('\n\n'):
        if not only_bolded or para.lstrip().startswith('**'):
            para = ' '.join(para.split())
        out.append(para.rstrip('\n'))
    return out


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
        install(want_run_doc(args), table, args.run, after)
    if block:
        sys.stderr.write('the block\'s prose is yours: controls, provenance'
                         ' and the paragraph are not installed\n')
        # FLATTENED TO ONE LINE A PARAGRAPH, which is the form the run file
        # keeps and the form a caller would otherwise produce by hand. Run 36
        # did produce it by hand, joining this output's wrapped lines, and a
        # break that fell inside `lib-stage2-lean-u1` came back as `lib-
        # stage2-lean-u1` -- an arm name that renders wrong, matches no row of
        # the table above it and answers no search for the arm. Printing the
        # paragraph already joined is what removes the seam; the `___` slots
        # stay, and run-status.sh refuses a run file that still carries one.
        prose = '\n'.join(l for l in text.split('\n')
                          if not l.startswith('|'))
        for para in flatten_paragraphs(prose):
            sys.stdout.write((para + '\n\n') if para else '')


def markdown_table(cells, shapes, strategies, meta, args, terms):
    """Emit the run file's Results table, ready to paste over the one there.

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
    # which row is the plain arm and which leads is what a reader looks for,
    # and it is the same row in every population's table.
    editorial = kind != 'class'
    # Read the table by the ROSTER, not by this run's arms, so that a row the
    # run has dropped is still seen and can be reported. See `readme_rows`.
    rostered = {n for n, _, _ in meta['roster']} or set(strategies)
    prev = readme_rows(want_run_doc(args), set(strategies),
                       rostered or set(strategies))
    fresh, gone = [], [n for n in prev if n not in strategies]
    print(RESULTS_HDR if editorial else CLASS_HDR)
    print('|---|---:|---:|---:|---:|---:' + ('|---|' if editorial else '|'))
    for time, st, ci, noise, smp, alloc, worst in rows:
        # --rows NAMES prints those rows and no others, header and rule
        # included so the output is still a table. Added 2026-09-18: a
        # write-up that wants one arm's published figure on one population
        # otherwise renders thirty-five rows to read one, and a paired run
        # does that twice a population. It is a FILTER on the print and
        # not on the computation -- the carry-forward, the fresh/gone
        # reporting and the stderr notes below all still read the whole
        # table, so a narrowed call cannot quietly answer a different
        # question from the full one.
        # getattr AND NOT args.rows: properties.py renders this table
        # through a stand-in args object carrying only the fields it needs,
        # so a new one read directly raises AttributeError and takes every
        # property with it -- which is what a plain `args.rows` did on
        # 2026-09-18, turning six mutants LOST and two MISSED and being
        # mistaken at first for fallout from that day's artifact deletion.
        if getattr(args, 'rows', None) and st not in args.rows:
            continue
        if st in prev:
            label_, style, needs, _ = prev[st]
        else:
            if editorial:
                fresh.append(st)
            label_ = st
            style = 'italic' if is_control(st) else 'plain'
            needs = '?'
        num = ['--' if time != time else '%.3f' % time,
               '--' if worst != worst else '%.3f' % worst,
               '--' if ci != ci else '%.2f' % ci,
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
                         ' %s\n'
                         % (len(fresh),
                            os.path.basename(args.run_doc or ''),
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


def pair_sunk(cells, shapes, a, b):
    """The key a pair is read on, and the cells that stop it being read.

    One test in one place because two callers want opposite things from
    it: `pair_stats` refuses and exits, which is right for a mode whose
    whole output is the pair, and `--predictions` records the span NOT
    READ and walks on, a registration reading many spans over one
    population and one degenerate pair having silenced the rest.
    """
    key = 'slope' if any(no_net(x) for x in (a, b)) else 'net'
    return key, [(s, x) for s in shapes for x in (a, b)
                 if not cells[s][x][key] > 0]


def pair_stats(cells, shapes, a, b):
    """One pair's per-shape ratios, and whether they had to be taken raw.

    The one computation every pair reading shares, held in one place so a
    verdict cannot disagree with the figures beside it.
    Netting an arm that never ran the forcing pass is meaningless, so a
    pair with a `sum-only` or `-nosum` half is compared raw and says so.

    A cell the forcing term did not leave positive is refused rather than
    divided: `time_of` and `worst_of` answer `--` for one and `--selftest`
    fails the file over it, while this divided regardless and handed
    `--pair` a ZeroDivisionError, or a negative ratio and
    then `math domain error` out of `geomean` -- a traceback where this
    file's convention is a refusal that says what did not happen. Found
    2026-08-17 by review.
    """
    raw = any(no_net(x) for x in (a, b))
    key, sunk = pair_sunk(cells, shapes, a, b)
    if sunk:
        sys.stderr.write('%s / %s: %d cell(s) with no positive %s, so this'
                         ' pair is not readable and nothing here is. The'
                         ' first: %s/%s\n'
                         % (a, b, len(sunk), key, sunk[0][0], sunk[0][1]))
        sys.exit(2)
    return raw, [cells[s][a][key] / cells[s][b][key] for s in shapes]


def pair_table(cells, shapes, strategies, pairs, quiet=False,
               per_shape=False):
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
        # THE CELLS THE RANGE IS A MAX AND MIN OF. They were computed here
        # all along and thrown away, so a question about the SHAPE of a
        # pair -- where it crosses, whether it is flat, which end carries
        # it -- wanted a script over --cells, and Run 21 wrote one. What
        # that script found is the run's sharpest reading, `lib-stage1`
        # above the `list` baseline at `runs-2`, and nothing the reader
        # printed would have shown it. Added 2026-08-29.
        if per_shape:
            for ratio, sh in sorted(zip(r, shapes), key=lambda t: t[1]):
                print('%46s   %-24s %.4f' % ('', sh, ratio))
        print('%46s published-column ratio %s%s'
              % ('', '--' if pub != pub else '%.4f' % pub,
                 '; compared RAW, one arm has no corrected time' if raw
                 else ''))
    # A caller printing a dozen of these in one call wants the standing
    # explanation once rather than twelve times; it is the same reasoning
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
            print('  %s half: carry-back figure %.2f%% (%s), over the'
                  ' %d pair(s) that carry back to Run 10'
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


def compare_alloc(cells, shapes, strategies, meta, other, main_hs,
                  per_shape=False):
    """Whether two halves of a pair agree on what each arm allocates.

    Allocation is deterministic per call, so a pair whose halves differ only
    in placement must agree on every cell, and a level that DOES move is a
    code change rather than a slot. That makes this the reading to check
    first
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
    if per_shape:
        # PER ARM, WHICH THE AGREEMENT LINES ABOVE CANNOT GIVE. Those count
        # cells inside 1e-4 and name the worst; a pair whose variable DOES
        # move allocation wants to know by how much, per arm, and the only
        # other route on offer is the `alloc` column -- a MEDIAN over shapes,
        # which must not be divided across halves. Run 36 divided it anyway,
        # in a script: 2.11x over 2.78x gives 0.759 on `bq-expand` where the
        # per-shape geomean below is 0.8119, and that script's own print then
        # took an absolute deviation, so `2 - ratio` reached the page on a
        # third arm and reversed its direction. Both columns print here for
        # that reason: there is no direction left to infer.
        rows = []
        for st in both_st:
            rs = []
            for sh in both_sh:
                a_b = cells[sh][st]['alloc_bytes']
                b_b = b_cells[sh][st]['alloc_bytes']
                if a_b is None or b_b is None or max(a_b, b_b) < FLOOR:
                    continue
                rs.append((b_b / a_b, sh))
            if rs:
                g = math.exp(sum(math.log(r) for r, _ in rs) / len(rs))
                rows.append((g, st, len(rs), min(rs), max(rs)))
        if rows:
            print('\nper arm, over the cells above %d bytes a call: how much'
                  ' the OTHER half allocates' % FLOOR)
            print('  below 1 = %s allocates less, above 1 = it allocates more'
                  % os.path.basename(other))
            print('\n%-42s %8s %8s %5s   %s'
                  % ('arm', 'other/this', 'this/other', 'n', 'range'))
            for g, st, n, lo, hi in sorted(rows):
                print('%-42s %8.4f %8.4f %5d   %.3f (%s) .. %.3f (%s)'
                      % (st, g, 1.0 / g, n, lo[0], lo[1], hi[0], hi[1]))
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
                  brief=True, per_shape=False):
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
    # THE DIRECTION, SAID RATHER THAN LEFT TO BE REMEMBERED. This run is
    # the numerator, so below 1 is THIS run faster -- which the run
    # chapter states and a session writing prose still gets backwards:
    # four paragraphs of Run 24's head were written the wrong way round
    # and were caught by the published columns, not by anything this mode
    # said. It knows both names and the convention.
    # Case: `compare-does-not-name-its-direction`.
    print('  below 1 = this run faster, above 1 = %s faster'
          % os.path.basename(other))
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
    # The reciprocal is printed beside the ratio because a write-up quoting
    # the other half's win inverts the column by hand and gets the direction
    # or the population wrong -- Run 23 quoted `ratio - 1` as the other
    # half's saving twice. Both columns carry the same n.
    print('\n%-34s %8s %8s %8s %10s'
          % ('arm', 'ratio', 'recip', 'faster', 'range'))
    for g, wins, n, st in sorted(rows):
        rs = sorted(cells[sh][st]['net'] / b_cells[sh][st]['net']
                    for sh in both_sh
                    if cells[sh][st]['net'] > 0 and b_cells[sh][st]['net'] > 0)
        print('%-34s %8.4f %8.4f %5d/%-3d %5.3f..%.3f'
              % (st, g, 1 / g, wins, n, rs[0], rs[-1]))
    # THE REDUCING CONSUMERS, ON RAW `slope`, IN A BLOCK OF THEIR OWN and
    # never as rows of the table above: the two are different quantities.
    # Every figure there is a corrected net over a corrected net, while an
    # arm that hands back a scalar runs no forcing pass, so its net is that
    # term subtracted from itself and a ratio of two of them divides two
    # near-zeros -- which is why the loop above skips them.
    # `--predictions` has read a `cross` prior on such an arm since Run 29,
    # on the raw key; nothing else did until 2026-09-15, so a prior quoted
    # for a `-sum` arm could be re-derived only by hand. Run 32's
    # preparation wrote that geomean of slope ratios by hand over two
    # JSONs, and Run 33's could not quote two of the three figures its own
    # note wanted, no span naming those two arms. Same key and same shapes
    # as that branch, so a prior and its re-derivation agree by
    # construction. Case: `compare-reads-no-reducing-consumer`.
    sunk = []
    for st in both_st:
        if not no_net(st):
            continue
        rs = sorted(cells[sh][st]['slope'] / b_cells[sh][st]['slope']
                    for sh in both_sh
                    if cells[sh][st]['slope'] > 0
                    and b_cells[sh][st]['slope'] > 0)
        if rs:
            sunk.append((geomean(rs), sum(1 for r in rs if r < 1),
                         len(rs), st, rs[0], rs[-1]))
    if sunk:
        print('\nreducing consumers, %d arm(s), on RAW `slope` and NOT on'
              ' the corrected net above -- they run no forcing pass, so the'
              ' two are different quantities and never share a table.'
              ' `--predictions` reads a `cross` prior on these the same way,'
              ' so a prior and this agree' % len(sunk))
        print('%-34s %8s %8s %8s %10s'
              % ('arm', 'ratio', 'recip', 'faster', 'range'))
        for g, wins, n, st, lo, hi in sorted(sunk):
            print('%-34s %8.4f %8.4f %5d/%-3d %5.3f..%.3f'
                  % (st, g, 1 / g, wins, n, lo, hi))
    # THE A/A BAR FOR THIS COMPARISON, which is the floor's counterpart
    # here and which no mode printed until 2026-09-15. `--aa` gives the
    # floor WITHIN one half: how far an arm differs from its own duplicate
    # there. A figure ACROSS two files is read against nothing unless the
    # same duplicates are read across them too -- an A/A copy is the same
    # code as its base, so the two owe one ratio, and how far they part is
    # what an arm must clear before its movement is the pair's variable
    # rather than the comparison's own noise. Run 32's head was written
    # without it and called the compiler worth nothing this roster can
    # measure, where three of eight strategies clear 0.81 points.
    # Case: `compare-prints-no-aa-bar`.
    bar, carrier, arms, past = aa_bar(cells, b_cells, both_sh, both_st)
    if carrier is None:
        print('\nNO A/A pair is in both files, so this comparison has no bar'
              ' of its own:\n  read it against the population floor `--aa`'
              ' prints and say which you used')
    else:
        st, a, base, b = carrier
        print('\nA/A bar for this comparison %.2f%%, the widest an arm and'
              ' its own duplicate part here:' % (bar * 100))
        print('  `%s` %.4f against `%s` %.4f' % (st, a, base, b))
        print('  %d of %d non-control arm(s) move further than the bar%s'
              % (len(past), len(arms),
                 ': ' + ', '.join('`%s`' % t for t in past) if past
                 else ', so nothing here is this comparison\'s to claim'))

    # THE PUBLISHED COLUMN'S OWN DRIFT, added the same day. `time` is a
    # WINSORIZED geomean, and the cap is computed per row per run off that
    # row's own spread, so two published figures divide to the paired ratio
    # only where the cap did not move under them. Run 31 published
    # `lib-stage2-lean-u1` at 0.029 and Run 32 at 0.025 -- fourteen points,
    # where the arm moved 1.6 -- the same four cells capped in both and the
    # cap they were pulled to halved. README forbids dividing two ROWS of
    # one table for a margin; this is the other reading a table invites, ONE
    # row down two runs, and nothing warned against it until a write-up had
    # published the division. Case: `compare-does-not-flag-column-drift`.
    drift = []
    for g, _w, _n, st in sorted(rows):
        t_a, t_b = time_of(cells, both_sh, st), time_of(b_cells, both_sh, st)
        if t_a != t_a or t_b != t_b or not t_b:
            continue
        if abs(t_a / t_b - g) > 0.02:
            drift.append((st, t_a / t_b, g))
    if drift:
        print('\npublished-column drift, %d row(s): the `time` column is'
              ' winsorized per row' % len(drift))
        print('  and per run, so dividing one row\'s two published figures'
              ' reports the')
        print('  estimator and not the arm. Quote the paired ratio above.')
        for st, col, g in drift:
            print('  %-34s column %8.4f against paired %8.4f, %5.1f points'
                  % (st, col, g, abs(col - g) * 100))

    if per_shape:
        # One line per arm, the per-shape ratios in the run's shape order,
        # which is what a question about ordering along a class's axis
        # wants -- registration 3's monotone prediction over `runs` was
        # computed from two --cells dumps for want of this (Run 23).
        print('\nper shape, this run / other; `--` where either side has no'
              ' positive net. The columns are the shapes, numbered:')
        for k, sh in enumerate(both_sh, 1):
            print('  %2d %s' % (k, sh))
        nums = ' '.join('%7d' % k for k in range(1, len(both_sh) + 1))
        print('%-34s %s' % ('arm', nums))
        for _g, _w, _n, st in sorted(rows):
            vals = []
            for sh in both_sh:
                a, b = cells[sh][st]['net'], b_cells[sh][st]['net']
                vals.append('%7.4f' % (a / b) if a > 0 and b > 0
                            else '%7s' % '--')
            print('%-34s %s' % (st, ' '.join(vals)))
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


def parse_counts(path):
    """`run-counts.sh`'s artifact: {shape: {arm: instructions an iteration}}.

    One data line a cell -- `shape arm N instructions` -- under `#` headers
    carrying the binary's md5 and the sweep's N. A cell perf could not
    count is a `!!` line, and it is DROPPED rather than read: a zero in a
    geomean does not make an arm's figure wrong, it destroys it, and the
    artifact says outright that such a line is a refusal and not a count.
    Refusals are returned so the caller can name them, an unread line being
    the thing this file refuses to do silently.
    """
    counts, refused, malformed = {}, [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('!!'):
                refused.append(' '.join(line.split()[1:3]))
                continue
            parts = line.split()
            if len(parts) != 4:
                malformed.append(line)
                continue
            sh, arm, _n, ins = parts
            try:
                v = float(ins)
            except ValueError:
                malformed.append(line)
                continue
            if v > 0:
                counts.setdefault(sh, {})[arm] = v
            else:
                refused.append('%s %s' % (sh, arm))
    return counts, refused, malformed


HEAD_PARAGRAPHS = 5      # the run file's head past its preamble

PREDICT_RE = re.compile(r'`predict: ([^`]+)`')


def parse_span(spec):
    """One `predict:` span as --predictions reads it: its kind, its
    positional arguments, and the modifiers -- `within X%`, `excluding
    S,...`, `on views S,...`, `on POP,...` and basis, control or both.
    `within` is 'bad' where it is not a number. Lifted out of
    --predictions on 2026-09-18 so that --lint reads a span by the same
    grammar and can say what the reader will compare."""
    toks = spec.split()
    kind, rest, within, excl, args_ = toks[0], toks[1:], None, [], []
    on_pops = views = half = None
    i = 0
    while i < len(rest):
        if rest[i] == 'within' and i + 1 < len(rest):
            try:
                within = float(rest[i + 1].rstrip('%'))
            except ValueError:
                within = 'bad'
            i += 2
        elif rest[i] == 'excluding' and i + 1 < len(rest):
            excl = rest[i + 1].split(',')
            i += 2
        elif rest[i] == 'on' and i + 2 < len(rest) \
                and rest[i + 1] == 'views':
            views = rest[i + 2].split(',')
            i += 3
        elif rest[i] == 'on' and i + 1 < len(rest):
            on_pops = rest[i + 1].split(',')
            i += 2
        elif rest[i] in ('basis', 'control', 'both'):
            half = rest[i]
            i += 1
        else:
            args_.append(rest[i])
            i += 1
    return kind, args_, within, excl, on_pops, views, half


def span_reads(spec):
    """What the reader will compare for one span, in words: the mode, its
    two operands and their orientation, the key, and which half.

    --lint prints this under an OPEN registration so that the author reads
    every span back against the sentence beside it. The grammar was the
    trap: Run 35's item (3) claimed this run's counts read the PREVIOUS
    run's and wrote `predict: counts ARM 1.0 within 0.1%`, and a `counts`
    span compares the two HALVES -- the compilers -- on which the two
    earlier runs of the pair had read 1.0062 and 1.0063. The span was
    unholdable the day it was written and nothing said so until the run
    had been spent; --lint held its arms to the roster and its scope to
    the class list, and no check held its vocabulary to its sentence.
    """
    kind, args_, within, excl, on_pops, views, half = parse_span(spec)
    if kind == 'cross' and len(args_) == 2:
        key = 'raw slope' if no_net(args_[0]) else 'net'
        what = ('--compare: `%s` on THIS half over the same arm on the'
                ' OTHER, per shape then geomean, on %s -- the pair\'s'
                ' variable' % (args_[0], key))
    elif kind == 'counts' and len(args_) == 2:
        what = ('--compare --counts: `%s`\'s instructions on THIS half\'s'
                ' sweep over the OTHER half\'s, per shape then geomean --'
                ' the two halves compared, never this run against a'
                ' previous one' % args_[0])
    elif kind == 'pair' and len(args_) == 3:
        key = ('raw slope' if no_net(args_[0]) or no_net(args_[1])
               else 'net')
        what = ('--pair: `%s` over `%s` WITHIN one half, per shape then'
                ' geomean, on %s' % (args_[0], args_[1], key))
    elif kind == 'cell' and len(args_) == 4 and args_[1] == 'over':
        what = ('--cells: the one cell `%s` over the one cell `%s` WITHIN'
                ' one half' % (args_[0], args_[2]))
    elif kind == 'countdiff' and len(args_) == 4 and args_[2] == 'under':
        what = ('--counts: `%s`\'s instructions minus `%s`\'s WITHIN one'
                ' half\'s own sweep, per view, every view under %s'
                % (args_[0], args_[1], args_[3]))
    else:
        return 'no mode reads a span of this shape; --predictions says so'
    where = []
    if on_pops:
        where.append('on ' + ', '.join(on_pops))
    if views:
        where.append('views ' + ', '.join(views))
    if half:
        where.append({'basis': 'the basis half', 'control': 'the control'
                      ' half', 'both': 'each half in turn'}[half])
    if excl:
        where.append('excluding ' + ', '.join(excl))
    if kind != 'countdiff':
        if within is not None and within != 'bad':
            where.append('within %g%%' % within)
        elif kind == 'counts':
            where.append('within 0.1%')
        else:
            where.append("within the population's own A/A floor")
    return what + '; ' + ', '.join(where)


# A figure as a registration writes one: two to four places, not a percent,
# not a version, not a date. TWO places at least, which is what the error
# this exists for was written in -- `1.16 to 1.36`; one place alone takes
# `1.0` out of every span's own target. The trailing class refuses a word
# character, which keeps `9.12` inside `9.1204.0` out, but must ALLOW a
# full stop: written `(?![\\w.%])` it dropped every figure ending a
# sentence, which is where a carried figure most often sits -- so the
# period is refused only when a digit follows it.
CARRIED_RE = re.compile(r'(?<![\w.$-])(\d\.\d{2,4})(?![\w%])(?!\.\d)')


SPAN_LINE_RE = re.compile(r'^  \((\S+)\) (.*?)\s+(read -?\d.*|A - B up to .*'
                          r'|out of scope, .*|NOT READ: .*)$')


def predictions_in_place(args):
    """Every span's readings, written under its item in the run file.

    `--predictions` reads one population and one half a call, and post-run
    step 5c looped it over every population on both halves and then
    transcribed each reading beside its item: Run 34's did that for five
    items over eleven populations. This takes the loop -- every `RUN-HALF-POP`
    JSON beside the one given, each half against the other, the two sweeps
    where both are on disk -- and writes one paragraph per item carrying
    spans and no `script:`, led `**Read by --predictions, item (N):**`,
    under that item, replacing the one an earlier call wrote. The item's
    verdict, its kill condition applied across these readings, and the
    tally sentence stay the write-up's. It writes only a registration that
    has moved into the run file, a README entry being the wrong document.
    """
    at = json_run_half(args.run)
    halves = note_halves(at[0]) if at else None
    if not halves:
        sys.stderr.write('--predictions --in-place: %s is not a run\'s'
                         ' RUN-HALF-POP.json beside a note carrying HALVES,'
                         ' so its populations cannot be found\n' % args.run)
        return 2
    doc = want_run_doc(args)
    src, items, _flat = registration_items(args.run, doc, args.readme)
    if src is None:
        return 2
    if os.path.abspath(src) != os.path.abspath(doc):
        sys.stderr.write('--predictions --in-place: the registration is still'
                         ' %s\'s, and its readings go into the run file --'
                         ' move it with --move-registration first\n'
                         % os.path.basename(src))
        return 2
    prefix, base = at[0], os.path.basename(at[0])
    head = '%s-%s-' % (base, halves[0])
    pops = sorted(os.path.basename(f)[len(head):-5]
                  for f in glob.glob('%s-%s-*.json' % (prefix, halves[0])))
    readings = collections.defaultdict(list)
    for pop in pops:
        sfx = '' if pop == 'main' else '-' + pop
        for k, role in ((0, 'basis'), (1, 'control')):
            this = '%s-%s-%s.json' % (prefix, halves[k], pop)
            that = '%s-%s-%s.json' % (prefix, halves[1 - k], pop)
            if not os.path.exists(that):
                continue
            counts = ['%s-counts-%s%s.txt' % (prefix, halves[j], sfx)
                      for j in (k, 1 - k)]
            cells, shapes, strategies, meta = load(this, args.main)
            apply_correction(cells, shapes, strategies, args.corr)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                predictions_table(cells, shapes, strategies, meta, that,
                                  args.main, this, doc, args.readme,
                                  counts if all(map(os.path.exists, counts))
                                  else None)
            for line in buf.getvalue().split('\n'):
                m = SPAN_LINE_RE.match(line)
                if m:
                    readings[(m.group(1), m.group(2))].append(
                        (pop, role, m.group(3)))
    # Stripped of newlines at both ends, a paragraph and the file alike: a
    # file's own final newline, left on its last paragraph, opened the
    # next one written after it with `\n`, and a rerun then missed its lead
    # and wrote the paragraph again.
    # AND EACH PARAGRAPH'S LEADING NEWLINES KEPT BESIDE IT, for the write:
    # a heading after two blank lines splits off as `\n## ...`, and the
    # strip took that newline, so every such heading came back after one
    # blank -- five of Run 39's, found by --check-doc on one and by hand on
    # the rest. Case: `predictions-in-place-keeps-the-headings-two-blanks`.
    raw = open(doc).read().strip('\n').split('\n\n')
    leads = [len(q) - len(q.lstrip('\n')) for q in raw]
    paras = [q.strip('\n') for q in raw]
    sec = next(i for i, q in enumerate(paras) if q.startswith(REG_HEAD))
    end = next((i for i in range(sec + 1, len(paras))
                if paras[i].startswith('## ')), len(paras))
    written = 0
    # IN ITEM ORDER, each placed after its item and after any paragraph an
    # earlier item placed there, so a registration written as one
    # paragraph gets its readings in its own order.
    for num, body in items:
        spans = PREDICT_RE.findall(body)
        if not spans or '`script: ' in body:
            continue
        parts = []
        for sp in spans:
            got = []
            for pop, role, text in readings.get((num, sp), []):
                if text.startswith('out of scope'):
                    continue
                v = re.search(r': (HELD|KILLED)', text)
                if text.startswith('NOT READ'):
                    got.append('NOT READ on %s %s, %s'
                               % (pop, role, text[10:]))
                elif v:
                    got.append('%s on %s %s, %s'
                               % (v.group(1), pop, role,
                                  text[:v.start()]))
            parts.append('`%s`: %s' % (sp, '; '.join(got) if got else
                                       'read on no population and half here'))
        lead = '**Read by --predictions, item (%s):**' % num
        para = '%s %s.' % (lead, ' --- '.join(parts))
        old = [i for i in range(sec, end) if paras[i].startswith(lead)]
        if old:
            paras[old[0]] = para
        else:
            host = next((i for i in range(sec, end)
                         if paras[i].startswith('(%s) *' % num)),
                        next((i for i in range(sec, end)
                              if '(%s) *' % num in paras[i]), None))
            if host is None:
                continue
            at_i = host + 1
            while at_i < end and paras[at_i].startswith(
                    '**Read by --predictions, item ('):
                at_i += 1
            paras.insert(at_i, para)
            leads.insert(at_i, 0)
            end += 1
        written += 1
    open(doc, 'w').write('\n\n'.join('\n' * n + q for n, q in
                                       zip(leads, paras)) + '\n')
    print('wrote %d item paragraph(s) of span readings into %s, over %d'
          ' population(s) on both halves; the verdicts and the tally are'
          ' yours' % (written, os.path.basename(doc), len(pops)))
    return 0


def carried_figures(run, run_doc, readme, others, main_hs, verbose=False):
    """Every figure a registration carries in, against the run it names.

    A registration states its predictions in `predict:` spans, which
    --predictions adjudicates from the artifacts. What it also does, in
    prose beside them, is QUOTE the previous run: *Run 28 reading 0.4951
    and 0.5177*. Nothing read those. They pass --lint, --check-doc and a
    blind reader, because each is a plausible number next to a correct
    arm name, and a wrong one is not wrong in any way a predicate over
    structure can see.

    So: for every `pair A B` span, derive A over B on each JSON given --
    the previous run's, one per population the item is read on -- and
    ask whether ANY figure quoted in that item matches ANY of those
    derivations. It is a warning and never a verdict: an item may quote
    a figure for a third arm, an allocation level, a count. What it
    catches is the item whose quoted figures match NOTHING its own span
    can produce -- a probe's figure wearing a run's name among them,
    which is what it was built for and which reads exactly like a right
    one (2026-09-11).

    The span's own target is not a carried figure and is excluded: it is
    what the coming run must produce, not what the last one did.
    """
    src, items, flat = registration_items(run, run_doc, readme)
    if src is None:
        return 2
    loaded = []
    for path in others:
        cells, shapes, strategies, _ = load(path, main_hs)
        # THE CORRECTION FIRST, as every table here does: `net` is set by
        # it and not by the load, so pair_stats on a raw load raises
        # KeyError('net') for any pair one of whose arms has no corrected
        # time -- which read as `unavailable` and silently emptied the
        # derivations this whole mode is. Watched 2026-09-12 on item (8),
        # whose pair --pair gives as 0.8635.
        apply_correction(cells, shapes, strategies)
        loaded.append((os.path.basename(path), cells, shapes, strategies))
    print('carried figures in %s, against %s'
          % (os.path.basename(src),
             ', '.join(n for n, _, _, _ in loaded) or 'nothing'))
    print('  a WARNING and not a verdict: an item may quote a figure this'
          ' cannot derive. What it names is an item quoting nothing its'
          ' own pair span produces')
    warned = looked = 0
    for num, body in items:
        spans = [sp.split() for sp in PREDICT_RE.findall(body)]
        pairs = []
        for sp in spans:
            if sp and sp[0] == 'pair' and len(sp) >= 3 \
                    and (sp[1], sp[2]) not in pairs:
                pairs.append((sp[1], sp[2]))
        if not pairs:
            continue
        looked += 1
        targets = {sp[3] for sp in spans if sp[0] == 'pair' and len(sp) >= 4}
        quoted = [q for q in CARRIED_RE.findall(body) if q not in targets]
        derived = []
        for name, cells, shapes, strategies in loaded:
            for a, b in pairs:
                if a not in strategies or b not in strategies:
                    derived.append((name, a, b, None))
                    continue
                # A pair whose arms this population cannot correct --
                # a reducing consumer against a fill, `no_net` on one
                # side -- raises out of pair_stats rather than returning
                # empty. Unavailable is not a mismatch, and the loop
                # must not end on it.
                try:
                    _, r = pair_stats(cells, shapes, a, b)
                except (KeyError, ZeroDivisionError):
                    r = []
                derived.append((name, a, b, geomean(r) if r else None))
        got = [d for *_, d in derived if d is not None]
        # Rounded to the places the figure is written in, which is how a
        # registration quotes one: 0.4951 against a derived 0.49512.
        hit = [q for q in quoted
               if any(abs(float(q) - d) < 5 * 10 ** -(len(q.split('.')[1]) + 1)
                      for d in got)]
        if quoted and not hit:
            warned += 1
            # THE SHORTLIST IS THE POINT, and a span derived on every
            # population handed in is not one: eleven populations on two
            # halves put twenty-two derivations on a single line, so the
            # mode's own output buries the item it is flagging. What the
            # reading wants is what the span derived INSTEAD, so the
            # nearest few to a quoted figure come first and the rest are
            # counted. --verbose keeps the whole list, for a span whose
            # population is itself the question (2026-09-13).
            def _near(t):
                return (t[3] is None,
                        min((abs(float(q) - t[3]) for q in quoted),
                            default=0.0) if t[3] is not None else 0.0)
            shown, more = sorted(derived, key=_near), 0
            if not verbose and len(shown) > 6:
                more, shown = len(shown) - 6, shown[:6]
            print('  (%s) quotes %s, and its own pair span derives %s%s'
                  % (num, ', '.join(quoted),
                     ', '.join('%s/%s %s on %s'
                               % (a, b, '--' if d is None else '%.4f' % d, n)
                               for n, a, b, d in shown) or 'nothing',
                     '' if not more
                     else ', and %d more (--verbose for all)' % more))
    print('%d item(s) with a pair span, %d quoting nothing it derives'
          % (looked, warned))
    return 0


# How far back --carry-over walks README's commits for the previous OPEN
# registration. The entry it wants is removed at the previous run's post-run
# step 5, so on the run after it the hit is a few dozen commits down; the cap
# is what keeps a MISSING registration from reading every state of a file with
# hundreds of commits. Once in all, every candidate lead being tested against
# each blob -- a walk per candidate is what the first draft did, and the cap
# then bounded a product rather than a sum.
PREV_REG_SCAN = 400


def _git(root, *args):
    """`git -C root ...`, or None where git or the object is not there."""
    try:
        return subprocess.run(('git', '-C', root) + args, capture_output=True,
                              text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def previous_registration(readme, n):
    """Run <m>'s registration as it stood BEFORE that run, out of git.

    The pre-run form is not in the run file: post-run step 5 MOVES the
    entry there and the write-up then appends a verdict to every item, so
    a carry-over diffed against that copy reports all of them changed --
    which is the reading a session actually made. What dates the pre-run
    form is the commit that REMOVED the OPEN lead from README, step 5
    being the removal; its parent is the last state carrying it.
    """
    root = os.path.dirname(os.path.abspath(readme)) or '.'
    rel = _git(root, 'ls-files', '--full-name', os.path.basename(readme))
    if not rel:
        return None, None, 'git cannot read %s' % readme
    rel = rel.strip()
    # NOT `git log -S`, WHICH FINDS NOTHING HERE: README is kept wrapped,
    # so the lead straddles a line break in every blob and the literal
    # search matches none of them -- the same silence the directory's
    # CLAUDE.md warns of for source and prose alike. Each candidate blob
    # is flattened before it is tested.
    # NEWEST FIRST, and the first hit is the answer: the entry is written
    # before the run and removed at post-run step 5, so the LAST state
    # carrying it is the one wanted. Bounding the walk by the run file's
    # birth instead looks right and is not -- step 5 writes that file, so
    # every state carrying the lead is at or BEFORE it, and `birth^..HEAD`
    # excluded all of them. That draft walked past Run 29 to Run 22 and
    # reported its items as Run 22's, a wrong answer where a refusal was
    # owed.
    # The pathspec is CWD-relative and `rel` is REPO-relative: `git -C
    # micro-regime3 log -- micro-regime3/README.md` names a path that is
    # not there and returns no commits at all, silently, which is what the
    # first draft of this did. `rel` is for `git show`, whose `REV:path`
    # IS repo-relative, and the basename is for the log.
    # ONE WALK FOR EVERY CANDIDATE RUN, not a walk per run: the blob is
    # what costs, so testing all the leads against each blob turns the
    # miss case from PREV_REG_SCAN reads per candidate into PREV_REG_SCAN
    # in all. The draft that walked per run would have read a 500 KB blob
    # some tens of thousands of times before refusing.
    leads = {'What Run %d is built to answer' % m: m for m in range(1, n)}
    revs = (_git(root, 'log', '--format=%H', '--',
                 os.path.basename(readme)) or '').split()
    for rev in revs[:PREV_REG_SCAN]:
        got = _git(root, 'show', '%s:%s' % (rev, rel))
        if not got:
            continue
        flat_blob = ' '.join(got.split())
        # The HIGHEST run number present, for the blob that carries two:
        # an open list holds one OPEN registration at a time, step 5
        # moving each out, but a state caught mid-move would carry both
        # and the later one is this run's predecessor.
        m = max((v for k, v in leads.items() if k in flat_blob), default=0)
        if not m:
            continue
        lead, blob = 'What Run %d is built to answer' % m, got
        with tempfile.NamedTemporaryFile('w', suffix='.md',
                                         delete=False) as fh:
            fh.write(blob)
            tmp = fh.name
        try:
            flat = subprocess.run(['wrap80', '--unwrap', tmp],
                                  capture_output=True, text=True,
                                  check=True).stdout
        except (OSError, subprocess.CalledProcessError) as e:
            os.unlink(tmp)
            return None, None, 'wrap80 --unwrap could not run (%s)' % e
        os.unlink(tmp)
        for line in flat.split('\n'):
            if lead in ' '.join(line.split()):
                return m, items_from_flat(' '.join(line.split())), None
    return None, None, ('no earlier OPEN registration in the last %d commit(s)'
                        ' of %s' % (PREV_REG_SCAN, rel))


def _word_change(a, b, cap=3, clip=60):
    """The runs of words that differ, compactly, in git's word-diff marks."""
    aw, bw = a.split(), b.split()

    def cut(s):
        return s if len(s) <= clip else s[:clip] + '...'

    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw,
                                                       bw).get_opcodes():
        if tag == 'equal':
            continue
        out.append('[-%s-]{+%s+}' % (cut(' '.join(aw[i1:i2])),
                                     cut(' '.join(bw[j1:j2]))))
    return (', '.join(out[:cap])
            + ('' if len(out) <= cap
               else ', and %d more change(s)' % (len(out) - cap)))


def carry_over(run, run_doc, readme):
    """This run's registration against the one it was carried from.

    A registration carried over from the previous run is ordinary here --
    Run 30's eleven items are Run 29's, with one flag name substituted and
    two figures amended by hand -- and whether that is ALL that moved was
    a question nothing answered. A session asked it by writing its own
    splitter against the run file's copy, which carries a verdict per item,
    and got back eleven changed items and no signal at all. The chapter's
    own standing instruction is that a computation a write-up hand-rolls
    is a defect report against the reader, so it is answered here.
    WHAT IT IS NOT is a verdict: a carry-over is SUPPOSED to change where
    the halves are renamed and where an amendment was decided. What it
    hands back is the list of items that moved and the words that moved in
    them, so the reading is which of those were meant.
    """
    src, items, _flat = registration_items(run, run_doc, readme)
    if not items:
        # SAID AND EXIT 2, not a silent 1. `registration_items` says its own
        # piece when it finds no registration AT ALL; this is the other
        # shape, an entry that is there and carries no numbered item yet,
        # which is every registration between the commit that declares the
        # pair and the preparation that predicts. A preparation running the
        # mode there got a bare exit 1 and no line, and 1 is this tree's
        # code for findings, so the empty selection read as a finding it
        # could not see. 2 is the code for a run that did not happen.
        sys.stderr.write(
            '%s: the registration for %s carries no numbered item, so there'
            ' is nothing to compare against the previous one -- this is an'
            ' empty selection and not a clean carry-over. Write the'
            ' `predict:` items first; pre-run step 12a is where they go\n'
            % (os.path.basename(src or 'README.md'), os.path.basename(run)))
        return 2
    m = re.match(r'run(\d+)', os.path.basename(run))
    if not m:
        sys.stderr.write('--carry-over wants a run named run<N>, to know'
                         ' which registration precedes this one\n')
        return 2
    pn, prev, why = previous_registration(readme, int(m.group(1)))
    if prev is None:
        sys.stderr.write('BLOCKED: %s\n' % why)
        return 2
    print('%s\'s registration in %s, against Run %d\'s as it stood BEFORE'
          ' that run (out of git, not from its run file)'
          % (os.path.basename(run), os.path.basename(src), pn))
    mine, theirs = dict(items), dict(prev)
    same = 0
    for num in sorted(set(mine) | set(theirs), key=int):
        a, b = theirs.get(num), mine.get(num)
        if b is None:
            print('  (%s) DROPPED -- in Run %d and not here' % (num, pn))
        elif a is None:
            print('  (%s) NEW -- not in Run %d' % (num, pn))
        elif a == b:
            same += 1
        else:
            print('  (%s) %s' % (num, _word_change(a, b)))
    print('%d item(s) here, %d carried word for word, %d of Run %d\'s'
          % (len(mine), same, len(theirs), pn))
    return 0


def registration_items(run, run_doc, readme):
    """The registration for this run, split into numbered items.

    Lifted out of predictions_table 2026-09-12 so a second reader can
    have it: WHERE a registration lives, and how its items are cut, is
    the same question for anything that reads one, and the two failure
    modes below -- wrap80 blocked, no registration anywhere -- had their
    accounts written once and would have been paraphrased by the second
    caller. Returns (src, items, flat), or (None, None, None) having said
    on stderr why, which every caller turns into its own exit 2.

    The registration is README's OPEN entry for this run where one exists,
    which is the state before post-run step 5's move, and the run file's
    last section after it -- IN THAT ORDER, because a run file copied from
    the previous run's carries THAT run's section until the move.
    """
    text = src = None
    m = re.match(r'run(\d+)', os.path.basename(run))
    if m:
        # One unwrapped line per list item, as --move-registration reads
        # it: the open list's items carry no blank line between them, so
        # a blank-line paragraph would hand back the neighbours too.
        lead = 'What Run %s is built to answer' % m.group(1)
        try:
            flat_readme = subprocess.run(['wrap80', '--unwrap', readme],
                                         capture_output=True, text=True,
                                         check=True).stdout
        except (OSError, subprocess.CalledProcessError) as e:
            # BLOCKED, as the file's two other wrap80 sites say: the
            # fallback read the wrapped README, where a lead spanning a
            # line break matches nothing, and went on to adjudicate the
            # run file's section -- the previous run's, before post-run
            # step 5 -- at a normal exit. Case:
            # `predictions-block-without-wrap80`.
            sys.stderr.write('BLOCKED: wrap80 --unwrap %s could not run (%s),'
                             ' and the registration is read unwrapped, so'
                             ' nothing was adjudicated\n'
                             % (os.path.basename(readme), e))
            return None, None, None
        for line in flat_readme.split('\n'):
            if lead in ' '.join(line.split()):
                text, src = line, readme
                break
    if text is None and run_doc and os.path.exists(run_doc):
        doc = open(run_doc).read()
        i = doc.find(REG_HEAD)
        if i >= 0:
            j = doc.find('\n## ', i + len(REG_HEAD))
            text, src = (doc[i:] if j < 0 else doc[i:j]), run_doc
    if text is None:
        sys.stderr.write('no registration to adjudicate: %s has no `%s`'
                         ' section and %s has no OPEN entry led `What Run N'
                         ' is built to answer`\n'
                         % (run_doc or 'the run file', REG_HEAD, readme))
        return None, None, None
    flat = ' '.join(text.split())
    return src, items_from_flat(flat), flat


def items_from_flat(flat):
    """A registration's items, `[(number, body)]`, off one unwrapped line.

    Split out 2026-09-13 so that --carry-over can read a registration out
    of git with the same hand that reads this run's out of README; before
    that a session comparing the two wrote its own splitter, and the one
    it wrote took the run file's copy, where step 5 has appended a verdict
    to every item, so all eleven read as changed.
    """
    # Items, in either house form: `(n) *lead*` inline, or `n. ` lines.
    marks = [(mm.start(), mm.group(1))
             for mm in re.finditer(r'\((\d+)\) \*', flat)]
    if not marks:
        marks = [(mm.start(), mm.group(1))
                 for mm in re.finditer(r'(?:^| )(\d+)\. \S', flat)]
    items = []
    for k, (at, num) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(flat)
        items.append((num, flat[at:end]))
    # ONE ENTRY PER ITEM NUMBER, the FIRST. The section read here runs
    # from the registration's heading to the next `## `, and after
    # post-run step 5's third act that holds the registration AND a
    # verdict paragraph per item -- so every item was found twice,
    # its span counted twice, and an item whose span is in the
    # registration was listed as having none because the verdict
    # paragraph repeating its number has none. Run 24 read eleven
    # entries for six items. The registration comes first, so the
    # first occurrence is the one that carries the spans.
    # Case: `predictions-enumerates-items-twice`.
    seen_nums = set()
    return [(num, body) for num, body in items
            if not (num in seen_nums or seen_nums.add(num))]


def item_populations(text, available):
    r"""The populations an item's own text names, out of those on disk.

    A registration item states where it is read -- `On \`runs\`, \`block\`
    and \`window\`` or `On the main set and on every class` -- and until
    2026-09-13 nothing read that: `--predictions` adjudicated every span on
    whatever JSON it was handed, so a span registered on `runs` was read on
    the main set and reported KILLED for being asked the wrong question.
    Run 30's write-up hand-rolled the mapping in a throwaway script, which
    is the shape the chapter calls a defect report against the reader.

    `available` is the population names on disk. Returns them in that
    order, so the report follows the roster and not the prose.
    """
    named = set()
    if re.search(r'\bon every class\b|\bevery class\b', text, re.I):
        named |= {p for p in available if p != 'main'}
    if re.search(r'\bthe main set\b', text, re.I):
        named.add('main')
    for p in available:
        if p != 'main' and re.search(r'`%s`' % re.escape(p), text):
            named.add(p)
    return [p for p in available if p in named]


def predictions_table(cells, shapes, strategies, meta, other, main_hs,
                      run, run_doc, readme, counts, pop_paths=()):
    """The registration's `predict:` spans, adjudicated from the artifacts.

    A registration item states a prediction and a kill condition in prose,
    and until 2026-09-02 the verdict beside it was a session's reading of
    the tables -- the step of the write-up that took the most judgement
    and the one least suited to a session prone to error. Where the
    quantity predicted is one this reader computes, the item now carries
    a backticked span stating it, and this prints the verdict:

        `predict: cross ARM X [within P%] [excluding S1,S2]`
            the cross-half geomean of ARM, this run over the other, as
            --compare prints it, read as X
        `predict: counts ARM X [within P%] [excluding S1,S2]`
            the instruction-count ratio of ARM, this run's counts file
            over the other's, read as X; wants --counts A B
        `predict: pair A B X [within P%] [excluding S1,S2]`
            the within-half --pair geomean of A over B, read as X
        `predict: cell SHAPE/ARM over SHAPE/ARM X [within P%]`
            one cell's time over another's on this file's half, read as X
        `predict: countdiff A B under N [on views S1,S2]`
            A's instructions less B's on this file's own sweep, the first
            --counts file, under N on every view named or on every shape

    and every kind takes `on POP[,POP]` and one of `basis`, `control` or
    `both`: the populations and the half it is read on, this file's
    population read off its shapes and its half off its name and its
    run's note. A span outside its scope is printed as such and counted
    apart; one naming no scope is read on every file handed in, which
    `--lint` refuses in an OPEN registration.

    A CROSS-HALF KIND SCOPED `both` IS READ TWICE, ONCE IN EACH HALF'S
    OWN ORIENTATION, so its two readings are RECIPROCALS: `cross` and
    `counts` compare this file's half over the OTHER, which off the
    control file is the basis reading inverted. A target away from 1
    therefore holds on at most one half -- Run 35's item (3) read 1.0062
    on the basis and 0.9938 on the control off one span, its own target
    being 1.0 and so legal here -- so `--lint`
    refuses `both` on a `cross` or `counts` span whose band does not
    reach both orientations, and the author names `basis` or `control`.
    `pair`, `cell` and `countdiff` are within-half and take `both` at any
    target.

    HELD when the figure read is within P points of X, or for countdiff
    when every difference is under N, KILLED otherwise; P defaults to the
    A/A floor of the POPULATION READ for cross, pair and cell -- this
    file's own, which is the main set's only when this file
    is the main set -- and to 0.1 for counts, which are exact to the
    fourth place on a repeat. A span is read once per JSON its scope
    admits. The
    rule and the loop are one README section, whole on the next line so a
    grep for the title finds this too:
        Which population answers a question, and how to ask all of them
    Post-run step 5c is where it runs. WHERE the registration lives, and
    in which order the two places are tried, is `registration_items`,
    which this shares with --carried. An item naming a committed
    `script: NAME` is listed with it, that script being its adjudicator,
    and an item with neither -- a class ordering, a verdict about
    verdicts -- is listed as the session's to adjudicate, by number, so
    that what the
    reader did not decide is not mistaken for decided. A span it cannot
    read is a finding about the document and exits 1; a document with
    no span at all exits 2, nothing having been adjudicated.

    The orientation is printed on every run: the registrations of Run 23
    were written dead-spot over basis, the reciprocal of --compare, and
    a span is written in --compare's orientation or it reads inverted.
    """
    src, items, flat = registration_items(run, run_doc, readme)
    if src is None:
        return 2
    specs = [(num, sp) for num, body in items
             for sp in PREDICT_RE.findall(body)]
    stray = [sp for sp in PREDICT_RE.findall(flat)
             if sp not in [x for _, x in specs]]
    specs += [('?', sp) for sp in stray]
    scripted = [(num, sc) for num, body in items
                for sc in re.findall(r'`script: ([^`]+)`', body)]
    unspanned = [num for num, body in items if not PREDICT_RE.search(body)
                 and num not in [n for n, _ in scripted]]
    if not specs:
        print('%s: no `predict:` span in the registration (%d item(s)), so'
              ' nothing here is adjudicated; every item is yours'
              % (os.path.basename(src), len(items)))
        return 2

    fl = aa_floor(aa_pairs(cells, shapes, strategies))
    floor_pct = abs(fl.g - 1) * 100 if fl else None
    # WHICH POPULATION AND HALF THIS FILE IS, for the spans that name
    # theirs: the population off the shapes, as `population_of` reads it,
    # and the half off the file's name and its run's note.
    pops = {meta['dims'][sh]['cls'] for sh in shapes if sh in meta['dims']}
    this_pop = next(iter(pops)) if len(pops) == 1 else None
    at = json_run_half(run)
    hv = note_halves(at[0]) if at else None
    this_half = (None if not hv or at[1] not in hv
                 else 'basis' if at[1] == hv[0] else 'control')
    print('predictions in %s, read from %s against %s' % (
        os.path.basename(src), os.path.basename(run), os.path.basename(other)))
    print('  cross and counts are THIS RUN over the other, as --compare'
          ' prints; the default tolerance is the A/A floor of the'
          ' population read, which is this file\'s and not the main'
          ' set\'s unless this file is the main set: %s'
          % ('%.2f%%' % floor_pct if floor_pct is not None
             else 'unavailable (no A/A pair)'))
    b_cells = b_shapes = b_strategies = None
    a_counts = b_counts = None
    held = killed = unread = outside = 0
    for num, spec in specs:
        kind, args_, within, excl, on_pops, views, half = parse_span(spec)
        # THE SCOPE FIRST, since 2026-09-17: a span naming its population
        # and half is read there and nowhere else, where a span naming
        # none was read on every file handed in and thirteen of Run 30's
        # main-set spans came back KILLED for being asked on the wrong
        # population. A span with no scope is read everywhere still, and
        # `--lint` refuses one in an OPEN registration.
        if on_pops is not None and this_pop is None:
            unread += 1
            print('  (%s) %-44s NOT READ: this file is no one population,'
                  ' so a span scoped to %s cannot be placed'
                  % (num, spec, ','.join(on_pops)))
            continue
        if half in ('basis', 'control') and this_half is None:
            unread += 1
            print('  (%s) %-44s NOT READ: this file\'s half is not known'
                  ' off its name and its run\'s note, so a %s span cannot'
                  ' be placed' % (num, spec, half))
            continue
        if ((on_pops is not None and this_pop not in on_pops)
                or (half in ('basis', 'control') and half != this_half)):
            outside += 1
            print('  (%s) %-44s out of scope, this file being %s on the %s'
                  ' half' % (num, spec, this_pop, this_half or 'unnamed'))
            continue
        why = None
        g = n = None
        try:
            if within == 'bad':
                why = "'within' wants a number"
            elif kind == 'cross' and len(args_) == 2:
                arm, x = args_[0], float(args_[1])
                if b_cells is None:
                    b_cells, b_shapes, b_strategies = load_other(
                        other, main_hs, shapes, meta)
                if arm not in strategies or arm not in b_strategies:
                    why = 'arm %s is not in both runs' % arm
                else:
                    # THE KEY IS `pair`'s, by `no_net`'s own rule: an arm
                    # that never ran the forcing pass has no corrected time
                    # in either run, so a net ratio over it divides two
                    # meaningless numbers -- and a cell with no positive
                    # value on that key is REFUSED here as `pair_sunk`'s
                    # callers refuse it, where this dropped the shape and
                    # said only how many were left. Run 29's item (3) is the
                    # first `cross` written over a reducing consumer, which
                    # `no_net`'s docstring said would not happen: on `runs`
                    # it read 0.5854 over the 3 shapes of 14 whose net
                    # stayed positive, against 0.9779 raw over all 14, and
                    # on `block` it read none at all and reported NOT READ.
                    key = 'slope' if no_net(arm) else 'net'
                    shs = [sh for sh in shapes
                           if sh in b_shapes and sh not in excl]
                    sunk = [(sh, w) for sh in shs
                            for w, cc in (('this', cells),
                                          ('other', b_cells))
                            if not cc[sh][arm][key] > 0]
                    if sunk:
                        why = ('%d cell(s) of `%s` have no positive %s, the'
                               ' first %s in the %s run -- the span is read'
                               ' over the population the item names or not'
                               ' at all'
                               % (len(sunk), arm, key,
                                  sunk[0][0], sunk[0][1]))
                    else:
                        rs = [cells[sh][arm][key] / b_cells[sh][arm][key]
                              for sh in shs]
                        g, n = (geomean(rs), len(rs)) if rs else (None, 0)
                tol = within if within is not None else floor_pct
            elif kind == 'counts' and len(args_) == 2:
                arm, x = args_[0], float(args_[1])
                if not counts:
                    why = 'a counts span wants --counts THIS.txt OTHER.txt'
                else:
                    if a_counts is None:
                        a_counts = parse_counts(counts[0])[0]
                        b_counts = parse_counts(counts[1])[0]
                    rs = [a_counts[sh][arm] / b_counts[sh][arm]
                          for sh in shapes if sh not in excl
                          and a_counts.get(sh, {}).get(arm)
                          and b_counts.get(sh, {}).get(arm)]
                    g, n = (geomean(rs), len(rs)) if rs else (None, 0)
                tol = within if within is not None else 0.1
            elif kind == 'pair' and len(args_) == 3:
                a, b, x = args_[0], args_[1], float(args_[2])
                if a not in strategies or b not in strategies:
                    why = 'arm %s or %s is not in this run' % (a, b)
                else:
                    shs = [sh for sh in shapes if sh not in excl]
                    key, sunk = pair_sunk(cells, shs, a, b)
                    if sunk:
                        why = ('%d cell(s) of `%s` or `%s` have no positive'
                               ' %s on this population, the first %s/%s --'
                               ' the arm removed the work there, so the'
                               ' span is read where the item says it is'
                               % (len(sunk), a, b, key,
                                  sunk[0][0], sunk[0][1]))
                    else:
                        _raw, rs = (pair_stats(cells, shs, a, b) if shs
                                    else (None, []))
                        g, n = (geomean(rs), len(rs)) if rs else (None, 0)
                tol = within if within is not None else floor_pct
            elif kind == 'cell' and len(args_) == 4 and args_[1] == 'over':
                # One cell over another on this file's half: SHAPE/ARM over
                # SHAPE/ARM, on `net` unless either arm has none.
                if '/' not in args_[0] or '/' not in args_[2]:
                    why = 'a cell is SHAPE/ARM'
                else:
                    (s1, a1), (s2, a2) = (args_[0].split('/', 1),
                                          args_[2].split('/', 1))
                    x = float(args_[3])
                    key = 'slope' if no_net(a1) or no_net(a2) else 'net'
                    v1 = cells.get(s1, {}).get(a1, {}).get(key)
                    v2 = cells.get(s2, {}).get(a2, {}).get(key)
                    if v1 is None or v2 is None:
                        why = 'cell %s or %s is not in this run' % (
                            args_[0], args_[2])
                    elif not (v1 > 0 and v2 > 0):
                        why = 'a cell has no positive %s' % key
                    else:
                        g, n = v1 / v2, 1
                tol = within if within is not None else floor_pct
            elif (kind == 'countdiff' and len(args_) == 4
                  and args_[2] == 'under'):
                # A's instructions less B's, on this file's own sweep --
                # the first --counts file -- per view, under N on every
                # view named, or on every shape where none is: the within-
                # half count clause Run 34 read by hand four times.
                a, b, x = args_[0], args_[1], float(args_[3])
                if not counts:
                    why = ('a countdiff span wants --counts THIS.txt'
                           ' OTHER.txt, and reads the first')
                else:
                    if a_counts is None:
                        a_counts = parse_counts(counts[0])[0]
                        b_counts = parse_counts(counts[1])[0]
                    shs = [sh for sh in (views or shapes) if sh not in excl]
                    ds = [(a_counts[sh][a] - a_counts[sh][b], sh)
                          for sh in shs
                          if a in a_counts.get(sh, {})
                          and b in a_counts.get(sh, {})]
                    lost = sorted(set(shs) - {sh for _, sh in ds})
                    if views and lost:
                        why = ('view(s) with no count for both arms: %s'
                               % ', '.join(lost))
                    elif not ds:
                        why = 'no shape carries both arms\' counts'
                    else:
                        over = [sh for d, sh in ds if d >= x]
                        ok = not over
                        held += ok
                        killed += not ok
                        print('  (%s) %-44s A - B up to %+.0f over %d'
                              ' view(s), under %.0f: %s%s'
                              % (num, spec, max(ds)[0], len(ds), x,
                                 'HELD' if ok else 'KILLED',
                                 '' if ok else '; at or over it on %s'
                                 % ', '.join(over[:6])))
                        continue
            else:
                why = ('not one of cross ARM X, counts ARM X, pair A B X,'
                       ' cell SHAPE/ARM over SHAPE/ARM X, countdiff A B'
                       ' under N (with optional within P%, excluding'
                       ' S,..., on POP,..., on views S,... and basis,'
                       ' control or both)')
        except ValueError:
            why = 'the predicted figure is not a number'
        if why is None and g is None:
            why = 'no shape readable for it'
        if why is None and tol is None:
            why = 'no tolerance: give within P%'
        if why is not None:
            unread += 1
            print('  (%s) %-44s NOT READ: %s' % (num, spec, why))
            continue
        off = abs(g - x) * 100
        ok = off <= tol
        held += ok
        killed += not ok
        # AND THE PUBLISHED COLUMN BESIDE IT, for a `pair` span, because
        # the two are different statistics and can part in SIGN: the
        # `time` column is winsorized per row, so a ratio of two of its
        # entries equals the paired figure only where neither row had a
        # cell capped. Run 26's registration (8) was adjudicated off the
        # paired figure alone and its write-up then read 0.9479 on the
        # MAIN SET while the table above it gave 1.0688 on the same
        # pair and the same population -- a reader
        # following README's own rule for comparing two rows would have
        # reached the opposite conclusion, and nothing here said so. The
        # sign test goes beside it for the same reason: 0.9479 sat at 13
        # of 19, p 0.17. Printed only where it differs enough to matter.
        # Added 2026-09-06.
        extra = ''
        if kind == 'pair' and len(args_) == 3 and a in strategies \
                and b in strategies:
            try:
                pub = time_of(cells, shs, a) / time_of(cells, shs, b)
            except Exception:                              # noqa: BLE001
                pub = None
            if pub is not None and pub == pub:
                wins = sum(1 for q in rs if q < 1)
                extra = ('; published column %.4f%s, %d of %d wins'
                         % (pub,
                            ' -- PARTS IN SIGN from the paired figure,'
                            ' which is the one a margin is judged on'
                            if (g - 1) * (pub - 1) < 0 else '',
                            wins, len(rs)))
        print('  (%s) %-44s read %.4f over %d shape(s), %.2f point(s) off,'
              ' within %.2f%%: %s%s'
              % (num, spec, g, n, off, tol, 'HELD' if ok else 'KILLED',
                 extra))
    print('%d span(s): %d HELD, %d KILLED, %d not read, %d out of scope%s%s'
          % (len(specs), held, killed, unread, outside,
             '; item(s) adjudicated by a committed script: %s'
             % ', '.join('(%s) %s' % s_ for s_ in scripted)
             if scripted else '',
             '; item(s) with no span, yours to adjudicate: %s'
             % ', '.join('(%s)' % u for u in unspanned) if unspanned
             else '; every item carries a span or a script'))
    # WHICH POPULATIONS EACH ITEM IS READ ON, added 2026-09-13. This mode
    # adjudicates an unscoped span on whatever file it is handed, and an item
    # naming `runs` read on the main set comes back KILLED for being asked
    # the wrong question -- thirteen of Run 30's twenty-one main-set spans
    # were exactly that. The item says where it is read; nothing read it,
    # so the write-up hand-rolled the mapping in a throwaway script, which
    # the chapter calls a defect report against the reader. This prints the
    # mapping and the call each population owes; a span is adjudicated one
    # population at a time, which is what the loop below names rather than
    # hides, and `--predictions --in-place` takes that loop itself.
    if pop_paths:
        # The main set is the file the spans above were read on, so it is
        # available whether or not its JSON is among the paths; without
        # it an item saying `on the main set` came back as naming nothing.
        names = ['main']
        for path in pop_paths:
            base = os.path.basename(path)
            m = re.search(r'-([a-z0-9]+)\.json$', base)
            nm = m.group(1) if m else base
            if nm not in names:
                names.append(nm)
        print()
        print('the populations each item names, off its own text --- the'
              ' spans above are this file alone:')
        for num, text in items:
            want = item_populations(text, names)
            print('  (%s) %s' % (num, ', '.join(want) if want
                                 else 'no population named; read by hand'))
        print('  each wants its own call: --compare the other half of that'
              ' population, --predictions, and the item read on THAT output')
    return 1 if unread else 0


def counts_pair(counts_a, pairs, shapes, cells=None, per_shape=False):
    """Two arms' instruction counts on ONE half, corrected and raw.

    `--counts` reads a PAIR of sweep files beside `--compare` and answers
    *did this arm's instructions move between the halves*. Registration 7
    turned on the other question --- *how many instructions does this arm
    execute against that one, on one half* --- and there was no mode, so
    Run 25 hand-rolled the arithmetic, which this file's own standing
    instruction calls a defect report against the reader: where a write-up
    invents the computation it will invent a wrong one, and the next run
    will invent a different wrong one.

    CORRECTED against the shared forcing pass, which is what makes it
    comparable with the `time` column: perf counts the whole bench, so a
    raw ratio of two fills is pulled toward 1 by the pass they both run,
    and on this roster that is a third of a cell. The term is the mean of
    whatever `sum-only*` arms the sweep carries, per shape, exactly as
    `apply_correction` takes it from the JSON. Both figures print, because
    the raw one is what the file holds and the corrected one is what the
    sentence means.

    A shape either arm is missing, or where the correction leaves either
    arm non-positive, is DROPPED and counted in the line below the table
    -- the same rule the time column takes, and for the same reason: a
    cell with no work left in it does not make a ratio wrong, it destroys
    it.
    """
    counts, refused, malformed = parse_counts(counts_a)
    print('\ncounted work within one half, from %s'
          % os.path.basename(counts_a))
    if refused:
        print('  %d cell(s) perf refused, dropped: %s'
              % (len(refused), ', '.join(sorted(refused)[:6])
                 + (', ...' if len(refused) > 6 else '')))
    if malformed:
        print('  %d malformed line(s)' % len(malformed))
    print()
    print('%-52s %9s %9s %7s %7s'
          % ('A / B', 'corrected', 'raw', 'shapes', 'rate'))
    rc = 0
    for a, b in pairs:
        raw, net, gone = [], [], []
        for sh in shapes:
            arms = counts.get(sh, {})
            if a not in arms or b not in arms:
                gone.append(sh)
                continue
            terms = [v for k, v in arms.items() if k.startswith('sum-only')]
            corr = sum(terms) / len(terms) if terms else 0.0
            na, nb = arms[a] - corr, arms[b] - corr
            if arms[b] <= 0 or nb <= 0 or na <= 0:
                gone.append(sh)
                continue
            raw.append(arms[a] / arms[b])
            net.append(na / nb)
        if not net:
            print('%-52s %s'
                  % ('%s / %s' % (a, b),
                     'no shape carries both with work left after the'
                     ' correction'))
            rc = 2
            continue
        gnet = geomean(net)
        rate = '--'
        if cells is not None:
            try:
                _, tr = pair_stats(cells, shapes, a, b)
            except SystemExit:
                tr = None
            if tr:
                t = geomean(tr)
                rate = ('%6.1f%%' % ((1 - t) / (1 - gnet) * 100)
                        if abs(1 - gnet) > 1e-9 else '--')
        print('%-52s %9.4f %9.4f %7d %7s'
              % ('%s / %s' % (a, b), gnet, geomean(raw), len(net), rate))
        if gone:
            print('  %d shape(s) dropped, either arm missing or left without'
                  ' work by the correction: %s'
                  % (len(gone), ', '.join(sorted(gone)[:6])
                     + (', ...' if len(gone) > 6 else '')))
    # PER SHAPE, AS A DIFFERENCE, RAW. The forcing pass cancels in A - B,
    # so no shape is lost to the correction -- Run 34's corrected
    # stage-twelve-over-eleven ratio kept two shapes of nineteen, the
    # reducing consumers being nearly all pass -- and what a difference is
    # read against is how far two copies of that one pass part: the
    # sweep's `sum-only-early` against `sum-only-late`, per shape and at
    # its widest. Run 34 hand-rolled both.
    for a, b in (pairs if per_shape else []):
        print()
        print('per shape, %s - %s in instructions an iteration, raw: the'
              ' forcing pass cancels in a difference' % (a, b))
        print('  %-44s %12s %14s' % ('shape', 'A - B', '|early - late|'))
        diffs, spreads = [], []
        for sh in shapes:
            arms = counts.get(sh, {})
            e, l = arms.get('sum-only-early'), arms.get('sum-only-late')
            spread = abs(e - l) if e is not None and l is not None else None
            if spread is not None:
                spreads.append((spread, sh))
            d = arms[a] - arms[b] if a in arms and b in arms else None
            if d is not None:
                diffs.append((d, sh))
            print('  %-44s %12s %14s'
                  % (sh, '--' if d is None else '%+.0f' % d,
                     '--' if spread is None else '%.0f' % spread))
        if diffs:
            print('  from %+.0f on %s to %+.0f on %s, over %d shape(s)'
                  % (min(diffs) + max(diffs) + (len(diffs),)))
        if spreads:
            print('  the resolution: the two copies of the forcing pass part'
                  ' by up to %.0f, on %s, and a difference inside that is'
                  ' no difference' % max(spreads))
        else:
            print('  the resolution: this sweep carries no `sum-only-early`'
                  ' and `sum-only-late` on one shape, so none is read')
    print()
    print('corrected subtracts the shared forcing pass per shape, the mean')
    print('of the sweep\'s `sum-only*` arms, which is the term the `time`')
    print('column subtracts -- so this figure and a `--pair` time ratio are')
    print('the same quantity on two instruments. raw is what the file holds.')
    print()
    print('rate is (1 - time) / (1 - corrected counts), the share of an')
    print('instruction saving that reaches the clock, and it is here because')
    print('this file quotes it every run and no mode computed it: Runs 26, 27')
    print('and 28 each hand-rolled the arithmetic from two other modes, and')
    print('Run 28 took the RAW column for the corrected one doing so. It is')
    print("NEGATIVE where a saving costs time, which is `-u2-last`'s reading")
    print('and not an error, and `--` where the counts did not move at all,')
    print('a rate over no saving being a division by zero rather than a')
    print('number. The time half is `--pair`\'s paired geomean, the same')
    print('figure that mode prints, so the two cannot disagree.')
    return rc


def counts_table(cells, shapes, strategies, meta, other, main_hs,
                 counts_a, counts_b, brief=True, per_shape=False):
    """The instruction count beside the time, per arm: registration 4.

    The one instrument here that owes criterion nothing. `run-counts.sh`
    counts instructions an iteration from two fixed-`-n` processes a cell,
    so an arm whose time moved between two halves either moved its counts
    with it -- which is codegen -- or did not, which is the runtime or the
    memory. Run 18 read it that way and put the `bq-expand` family's
    movement on its counts and the placement-exposed family's seven percent
    on count ratios of 1.0000.

    It lived as a hand-rolled script for two runs, which this file's own
    standing instruction calls a defect report against the reader: where a
    write-up invents the computation it will invent a wrong one. The
    direction is `--compare`'s throughout -- this run over the other, on
    both columns -- so that the two are read side by side without one of
    them being inverted.

    WHAT THE RESIDUE IS NOT is a like-for-like ratio. perf counts the whole
    bench and `time` is net of the shared forcing pass, so the count column
    is raw-equivalent and the time column is corrected. Over the roster the
    difference is about a point, the forcing term being within half a point
    of the same share on both halves; on a single cell it reaches three,
    which is why the trailing note sends a cell question to `--cells`.
    Found 2026-08-25, by being asked for the largest single cell.
    """
    a_counts, a_refused, a_bad = parse_counts(counts_a)
    b_counts, b_refused, b_bad = parse_counts(counts_b)
    b_cells, b_shapes, _b_strategies = load_other(other, main_hs,
                                                  shapes, meta)

    print('\ncounted work, this run against %s' % os.path.basename(other))
    print('  counts: %s against %s'
          % (os.path.basename(counts_a), os.path.basename(counts_b)))
    for tag, refused in (('this half', a_refused), ('other half', b_refused)):
        if refused:
            print('  %d cell(s) perf refused on the %s, dropped: %s'
                  % (len(refused), tag, ', '.join(sorted(refused)[:6])
                     + (', ...' if len(refused) > 6 else '')))
    for tag, bad in (('this half', a_bad), ('other half', b_bad)):
        if bad:
            print('  %d unreadable line(s) in the %s counts, dropped'
                  % (len(bad), tag))

    counted = {a for sh in a_counts for a in a_counts[sh]}
    counted &= {a for sh in b_counts for a in b_counts[sh]}
    stray = sorted(counted - set(strategies))
    if stray:
        print('  arm(s) in the counts and not in this run, skipped: %s'
              % ', '.join(stray))

    rows = []
    for st in strategies:
        if no_net(st) or st not in counted:
            continue
        crs, trs = [], []
        for sh in shapes:
            if sh not in b_shapes:
                continue
            ca = a_counts.get(sh, {}).get(st)
            cb = b_counts.get(sh, {}).get(st)
            if ca and cb:
                crs.append(ca / cb)
            a, b = cells[sh][st]['net'], b_cells[sh][st]['net']
            if a > 0 and b > 0:
                trs.append(a / b)
        if crs and trs:
            rows.append((geomean(crs), geomean(trs), len(crs), st))

    if not rows:
        print('\nno arm is in both the run and both counts files, so there'
              '\nis nothing to read: check that the counts belong to this'
              '\nroster and this pair.')
        return 2
    print('\n%-34s %8s %8s %12s %6s'
          % ('arm', 'counts', 'time', 'time/counts', 'n'))
    for cr, tr, n, st in sorted(rows, key=lambda r: r[1]):
        print('%-34s %8.4f %8.4f %12.4f %6d' % (st, cr, tr, tr / cr, n))
    if per_shape:
        # Per-shape count ratios, in shape order: the sInner-of-1 mechanism
        # claim (Run 22) and the per-shape pad shares (Run 23) were both
        # computed from the two counts files by hand for want of this.
        sh_order = [sh for sh in shapes if sh in b_shapes]
        print('\ncounts per shape, this run / other. The columns are the'
              ' shapes, numbered:')
        for k, sh in enumerate(sh_order, 1):
            print('  %2d %s' % (k, sh))
        nums = ' '.join('%7d' % k for k in range(1, len(sh_order) + 1))
        print('%-34s %s' % ('arm', nums))
        for _cr, _tr, _n, st in sorted(rows, key=lambda r: r[1]):
            vals = []
            for sh in sh_order:
                ca = a_counts.get(sh, {}).get(st)
                cb = b_counts.get(sh, {}).get(st)
                vals.append('%7.4f' % (ca / cb) if ca and cb else '%7s' % '--')
            print('%-34s %s' % (st, ' '.join(vals)))

    # THE AGGREGATE, AND BOTH POPULATIONS OF IT, BECAUSE THE MODE OWNS THE
    # DEFINITION OR TWO SESSIONS INVENT TWO. A per-class count geomean had
    # no mode until now, so Run 20 took one over every arm its sweep
    # carried and Run 21 took one over the arms this table prints -- and
    # then Run 21 published that Run 20's figure `reproduces from neither
    # set`, of a figure that reproduces exactly over the population Run 20
    # used. Neither had said which population it was. So both are printed
    # and both are named, and a run file quoting one says which.
    # Added 2026-08-29.
    everything = sorted(set(counted) & set(strategies))
    all_rs = []
    for st in everything:
        rs = [a_counts[sh][st] / b_counts[sh][st] for sh in shapes
              if sh in b_shapes and a_counts.get(sh, {}).get(st)
              and b_counts.get(sh, {}).get(st)]
        if rs:
            all_rs.append(geomean(rs))
    print('\ncounts geomean over the %d arm(s) above, which are the arms'
          ' with a\ncorrected time: %.4f'
          % (len(rows), geomean([r[0] for r in rows])))
    if all_rs:
        print('counts geomean over all %d arm(s) the sweep carries, the'
              ' `sum-only`\nand `-nosum` controls included: %.4f'
              % (len(all_rs), geomean(all_rs)))
    print('They differ by the controls alone. QUOTE ONE AND NAME IT: a'
          '\ncross-run comparison of this figure is worthless unless both'
          '\nsides took the same population.')
    if brief:
        return 0
    print('\n`counts` is the geomean over shapes of this half\'s instructions'
          '\nan iteration over the other half\'s, and owes criterion nothing.'
          '\n`time` is the same arm\'s corrected time ratio, the figure'
          '\n--compare prints.'
          '\n'
          '\nTHE TWO ARE NOT OVER THE SAME WORK, and the residue carries'
          '\nthat: perf counts the WHOLE bench, the shared forcing pass'
          '\nincluded, while `time` is net of it. So the count column is'
          '\nraw-equivalent and the one beside it is corrected. Over the'
          '\nroster it hardly matters, the forcing term sitting within half'
          '\na point of the same share on both halves; ON ONE CELL it is'
          '\nworth two to three points -- stretch-tall-Mx2 on'
          '\nbq-odo-gm-mulback reads +9.30% in counts against +7.98% raw'
          '\nand +11.26% net, subtracting a term the halves share'
          '\namplifying what is left. Read the residue for its direction and'
          '\nnot as a magnitude, and go to --cells for a single cell.'
          '\n'
          '\n`time/counts` is the part of the time movement'
          '\nthe instruction count does not explain: near 1 the movement IS'
          '\nthe codegen, and away from 1 it is the runtime or the memory --'
          '\nwhich on a pinned pair is where placement shows, an arm whose'
          '\nloop moved doing the same work in a different number of cycles.'
          '\nBoth columns are this run over the other, so neither is'
          '\ninverted against the other.')
    return 0


def movers_table(cells, shapes, strategies, meta, other, main_hs,
                 pct, brief=True):
    """The arms that moved past a threshold, counted and named together.

    One predicate, used once. The count on the headline and the rows under
    it come from the same comparison, so the two cannot disagree --- which
    is the whole reason this exists, and the defect is a reader's rather
    than this code's. Run 19's independent checker reported twelve arms
    past 3% where eleven move, having taken the count by eye off
    `--chapter`, whose per-arm block lists arms outside ONE percent; a
    2.51% arm sits in the middle of that block looking like a mover. The
    session hand-rolled the same count in awk, twice. A figure a write-up
    quotes and no mode emits is a defect report against the reader, which
    is the rule that built `--counts` the same evening.

    Arms are GROUPED by stripping the A/A suffix, because the sentence a
    write-up wants is usually `N arms in M groups`: three copies of one
    strategy moving together is one finding and not three, and counting
    the groups by eye off a sorted list is the same slip one level up.

    The threshold is printed with the count, so a figure taken off this
    output carries the threshold it was measured at.
    """
    b_cells, b_shapes, b_strategies = load_other(other, main_hs,
                                                 shapes, meta)
    both_sh = [x for x in shapes if x in b_shapes]
    rows = []
    for st in strategies:
        if no_net(st) or st not in b_strategies:
            continue
        rs = [cells[sh][st]['net'] / b_cells[sh][st]['net'] for sh in both_sh
              if cells[sh][st]['net'] > 0 and b_cells[sh][st]['net'] > 0]
        if rs:
            rows.append((geomean(rs), st, len(rs)))
    # ONE MEASURE, used for the cut, the sort and the printed column.
    # Selecting on `abs(g - 1)` and ordering on `abs(log g)` put `bq-gen`
    # at +7.53% two rows BELOW an arm at -7.30% on this run's own output,
    # so a reader taking `the largest mover` off the top row got the
    # wrong arm -- the take-it-by-eye slip this mode exists to prevent,
    # one level down. Linear is the measure kept, because `past PCT
    # percent` in prose means `abs(ratio - 1)` and nothing else; its
    # asymmetry between 0.97 and 1.03 is the asymmetry of the word
    # `percent`, and a log cut would answer a question no sentence here
    # asks.
    lim = pct / 100.0
    past = [(g, st, n) for g, st, n in rows if abs(g - 1) > lim]
    past.sort(key=lambda r: -abs(r[0] - 1))
    groups = {twin_of(st) or st for _, st, _n in past}

    print('\nmovers, this run against %s, past %g%%'
          % (os.path.basename(other), pct))
    if not past:
        print('  no arm moves past %g%% over %d compared arm(s), so there is'
              '\n  nothing to list -- which is a reading and not an empty'
              ' table.' % (pct, len(rows)))
        return 0
    print('  %d of %d arm(s) move past %g%%, in %d group(s); %d within it'
          % (len(past), len(rows), pct, len(groups), len(rows) - len(past)))
    print('\n%-34s %8s %8s %5s  %s'
          % ('arm', 'ratio', 'move', 'n', 'group'))
    for g, st, n in past:
        print('%-34s %8.4f %+7.2f%% %5d  %s'
              % (st, g, (g - 1) * 100, n, twin_of(st) or st))
    if brief:
        return 0
    print('\nBelow 1 means this run is faster, as --compare prints it. The'
          '\ncount, the groups and the rows are one comparison read once, so'
          '\na figure taken off the headline cannot be at a threshold the'
          '\nlist is not. `group` strips the A/A suffix: an arm and its two'
          '\ntwins are one strategy moving, not three. `n` is the shapes'
          '\nbehind the geomean, so one taken over a handful cannot pass for'
          '\none taken over the population.')
    return 0


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


def machine_check(cells, shapes, readme, thresh=3.0, spread=7.0,
                  run=None):
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
    # Post-run 5b installs --fingerprint into the run's OWN file, and the
    # kept fingerprint is read out of whichever run file this is given --
    # so from 5b on the default resolves to the run being read and the
    # check becomes the run against itself. That form is not visibly
    # wrong: it prints the same `inside 3%` verdict, Run 24 reading
    # -0.03% and Run 25's basis +0.00%, off zero only by the installed
    # table's rounding. Refused by NAME rather than by path, since the
    # workaround was a --run-doc a session had to remember. Exit 2 and
    # not 1: the reading did not happen, which is what a 2 means
    # everywhere in this directory, and run-gate.sh words its
    # complaint off that -- a 1 there reads as a moved box.
    mine = re.match(r'run\d+', os.path.basename(run or ''))
    kept = re.match(r'run\d+', os.path.basename(readme or ''))
    if mine and kept and mine.group(0) == kept.group(0):
        print('machine: %s carries %s\'s OWN fingerprint, which post-run 5b'
              ' installed, so the run would be read against its own figures'
              ' and would read about zero whatever the box did. Name the'
              ' PREVIOUS run: --run-doc %s/run<N-1>.md'
              % (os.path.basename(readme), mine.group(0), RUNS_DIR))
        return 2
    want = {}
    for line in open(readme):
        m = FINGERPRINT_ABS_RE.match(line)
        if m:
            want[m.group(1)] = float(m.group(2)) * UNIT[m.group(3)]
    have = [(sh, cells[sh]['list']['net'], want[sh])
            for sh in shapes if sh in want and 'list' in cells[sh]]
    if not have:
        print('machine: no shape of this run is in the run file\'s'
              ' fingerprint, so there is nothing to compare -- which is'
              ' itself worth reading')
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
    # BESIDE THE RUN, as the refusal below says: globbed out of the cwd
    # until 2026-08-28, so a run named through a directory found no leg
    # and was told its riders were never taken. Case:
    # `deflation-legs-beside-the-run-not-the-cwd`.
    at = os.path.dirname(os.path.abspath(run_path))
    legs, sat = {}, {}
    for path in sorted(glob.glob(os.path.join(at, '%s*-r1.json' % pat))):
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
    # THE UNIT IN THE HEADER, because the legend that carries it sits
    # under the last row: on a 490-bench process that is 490 lines below
    # the column, and `gc%` next to it invites the percentage reading.
    # Run 27's step 2 read 0.96 of a core as 0.96%, cleared the intrusion,
    # and had the whole write-up to redo when the checker found it at 6d.
    print(head + ('%9s %6s' % ('fgn/core', 'load') if have_load else ''))
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
        print(row + ('%9s %6s' % (f_txt, l_txt) if have_load else ''))
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
            # AND THE REMEDY, printed rather than left to be assembled:
            # post-run step 3 reruns the populations an intrusion touched,
            # and where a rerun is not taken the reading that stands in
            # for it drops those SHAPES from both halves and re-reads.
            # Run 33 assembled that invocation by hand under a stopped
            # rerun; the shapes are on this very screen, so the mode that
            # names them can name the call. It is the shapes and not the
            # benches: a cell is an arm on a shape, and the comparison
            # this feeds is per shape.
            hurt = sorted({nm.split('/')[0] for nm, _, _ in loud})
            print('  TO READ WITHOUT THEM, both halves, where step 3\'s'
                  ' rerun is not taken:')
            print('    --compare OTHER.json %s'
                  % ' '.join('--exclude-shape %s' % s for s in hurt))
            print('    and the same with the two files swapped. That is a'
                  ' sensitivity reading and not a repair: it says whether'
                  ' a verdict turns on the disturbed cells, and a verdict'
                  ' that does wants the rerun.')
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


# The kept per-shape record's two headers, since 2026-09-04: the cross-class
# summary's columns per shape, computed from the run alone. Until then the
# tables carried one column per FINGERPRINT arm under a membership rule
# (README.md#per-shape-where-the-geomean-hides-the-ordering keeps the ruling
# and why it went); `install` matches a table by its whole header line, so
# the run file's tables carry these lines and a change here changes both.
FINGERPRINT_HEADER = ('| shape | `sInner` | `l` | `list`, net'
                      ' | mut-odo-vecdims | best outside family | ceiling |')
FINGERPRINT_CLASS_HEADER = ('| shape | class | `sInner` | `l` | `list`, net'
                            ' | mut-odo-vecdims | best outside family'
                            ' | ceiling |')


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


def fingerprint_row(sh, sh_cells, d, label=None):
    """One row of the kept per-shape record: dims, `list`'s net per call
    as an absolute, and three cells read as the cross-class summary's
    columns of those names are, per shape rather than per population --
    `mut-odo-vecdims`'s ratio, the best arm outside the vecdims family
    with its ratio, and the ceiling, the family's leading arm with its.
    A sunk cell -- a net the forcing term did not leave positive -- is
    `--` and never a candidate, as `time_of` and `worst_of` read it: a
    negative or wild figure here outlives the run that could disprove
    it, this table being installed every write-up.

    AND AN ARM WITH NO CORRECTED TIME IS NOT A CANDIDATE EITHER, which
    this had to be told on 2026-09-10. It asked `is_control`, which until
    that day WAS `no_net` plus the twins, so the two agreed by
    construction; once the reducing consumers joined `no_net` alone, this
    column went on dividing their nets and named one on every shape of
    Run 28's main set -- `libunord-stage6-sum 0.030` beside a `time --`
    in the same run's table, which is the disagreement the paragraph
    above forbids."""
    base = sh_cells['list']['net']

    def ratio(st):
        c = sh_cells.get(st)
        return (None if not c or c['net'] <= 0 or base <= 0
                else c['net'] / base)
    timed = sorted((r, st) for st in sh_cells
                   if st != 'list' and not is_control(st) and not no_net(st)
                   for r in [ratio(st)] if r is not None)
    outside = next((p for p in timed if not p[1].startswith(FAMILY)), None)
    family = next((p for p in timed if p[1].startswith(FAMILY)), None)
    plain = ratio(PLAIN)
    row = ['`%s`' % sh] + (['`%s`' % label] if label else [])
    row += [str(d['s_inner']), str(d['l'])] if d else ['?', '?']
    row.append(fmt_abs(base))
    row.append('--' if plain is None else '%.3f' % plain)
    for p in (outside, family):
        row.append('--' if p is None else '`%s` %.3f' % (p[1], p[0]))
    return '| ' + ' | '.join(row) + ' |'


def fingerprint_table(cells, shapes, strategies, meta, classes=()):
    """The kept per-shape record, two tables: the main set's and, with a
    `class` column, every class JSON `--classes` loaded, in the order
    given -- one (label, cells, shapes, dims) each. Shapes sorted by l
    then name. Every cell is this run's; nothing is carried from an
    earlier run or from the run file, which is what lets the JSONs go
    once it is installed. Born checked: pointed at a run without `list`
    (--exclude list) it refuses with exit 1."""
    if 'list' not in strategies:
        sys.exit('--fingerprint needs the `list` baseline in the run')
    dims = meta['dims']
    print(FINGERPRINT_HEADER)
    print('|---' + '|---:' * 4 + '|---' * 2 + '|')
    for sh in sorted(shapes, key=lambda x: (
            dims[x]['l'] if x in dims else float('inf'), x)):
        print(fingerprint_row(sh, cells[sh], dims.get(sh)))
    if classes:
        print()
        print(FINGERPRINT_CLASS_HEADER)
        print('|---|---' + '|---:' * 4 + '|---' * 2 + '|')
        for label, c_cells, c_shapes, c_dims in classes:
            for sh in sorted(c_shapes, key=lambda x: (
                    c_dims[x]['l'] if x in c_dims else float('inf'), x)):
                print(fingerprint_row(sh, c_cells[sh], c_dims.get(sh), label))


# The regime 3 fix became the `mut-odo-vecdims` FAMILY by the decision of
# 2026-08-22 (README, the ceiling), narrowed 2026-08-24 to its
# `add-in-leaf-u2` member, which is what ships; `bq-expand` the last
# candidate. The pure/impure distinction retired with the decision, and the
# summary's pure slot now carries the best arm OUTSIDE the vecdims family
# -- what the stride-conditioned redirect, dropped 2026-08-24, would have
# taken per class. `PLAIN` is the family's UNREFINED member, which every
# ratio here is quoted against and which this file used to call `FIX` --
# a name that read as though the plain arm were the shipped code, where it
# is one of the several the shipped member leads.
SUMMARY_COLS = ('shapes', 'mut-odo-vecdims', 'worst', 'best outside family',
                'ceiling', 'floor')
FAMILY = 'mut-odo-vecdims'
PLAIN = 'mut-odo-vecdims'
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

    Properties 1 and 2 are read PER SHAPE since 2026-09-06, when the
    top-of-the-table ordering that was property 2 retired -- broken in
    every class by a route the class's strides favour, so it said which
    arm led and foreclosed nothing -- and `runs/run26.md` restated the
    set: property 1 is `worst` under 1 and `mut-odo-vecdims` ahead of
    `bq-expand` on every shape; property 2 is the same two inequalities
    in allocation to within 1%, `mut-odo-vecdims` at most 1% over `list`
    and over `bq-expand` on every shape, read off the `alloc` multiple
    each cell carries (`property_clauses` says why the margin). Each
    clause prints its closest shape, which is what a write-up quotes, and
    says how many shapes it read, a cell with no readable value being
    dropped as `worst` drops a sunk one. The lead the sort finds is still
    PRICED against the population's own floor (`priced_break`), which is
    the difference between a sort and a reading: on Run 17's `revsome`
    two arms that print 0.049 apiece read 0.36% apart paired, where that
    class's floor is 18.05%. Non-vacuity is a mutant per property in
    `mutants.py`, judged on the newest main-set run on disk.
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
        lead = next((r for r in timed if r[1] == PLAIN), None)
        if lead is not None and outside[0][0] < lead[0]:
            for line in priced_break(cells, shapes, outside[0][1], PLAIN,
                                     floor):
                print(line)
    # The summary's *ceiling* cell, which had no derived line here and was
    # picked by eye off a table printing two family arms at one figure:
    # four of Run 22's cells named the one that trailed. 2026-09-01.
    if led.family:
        print('  ceiling (family)    %-30s %.3f' % (led.family[0].st,
                                                     led.family[0].time))
    # AND WHICH OF THOSE TWO THE SUMMARY BOLDS, which was hand work and is
    # the same lesson as the ceiling line above, one column across. The
    # cross-class summary emphasises the faster of its two named arms, and
    # the rule is that the emphasis follows the COLUMN -- but the column
    # PRINTS three decimals and the two arms tie there often: four of Run
    # 29's ten rows did, and Run 28 got `rev` wrong by breaking such a tie
    # with `--pair`, whose paired geomean is a different statistic and
    # parted from the column the other way. The column decides at full
    # precision, which is what this line reads, and it says when the print
    # cannot show why. Case: `block-names-the-summary-s-bold-column`.
    if outside and led.family:
        a, an = outside[0][0], outside[0][1]
        b, bn = led.family[0].time, led.family[0].st
        col = 'best outside family' if a < b else 'ceiling'
        print('  summary bolds       %-30s (%s)'
              % (col, an if a < b else bn))
        if round(a, 3) == round(b, 3):
            print('    both print %.3f, so the table shows a tie the column'
                  ' resolves at %.6f against %.6f -- do NOT break it with'
                  ' --pair, which is a different statistic'
                  % (round(a, 3), a, b))
    plain = next((r for r in timed if r[1] == PLAIN), None)
    if plain:
        print('  %-19s %-30s %.3f   worst %.3f'
              % (PLAIN, '(the plain arm)', plain[0], plain[6]))
        print('  property 1, `worst` under 1: %s'
              % ('HOLDS' if plain[6] < 1 else '**BREAKS**'))
        # Priced like the others, on the one cell that breaks it: `worst`
        # is a per-shape ratio and not a pair, so what stands beside the
        # floor is its own excess over 1 rather than a geomean.
        if not plain[6] < 1:
            over = (plain[6] - 1) * 100
            print('     worst is %.2f%% above 1%s'
                  % (over, '' if floor is None else
                     ', against this class\'s floor of %.2f%% (`%s`), so it'
                     ' is %s the floor'
                     % (abs(floor.g - 1) * 100, floor.a,
                        'INSIDE' if over < abs(floor.g - 1) * 100
                        else 'OUTSIDE')))
    property_clauses(cells, shapes, strategies)
    tiers = [(st, dict((r[1], r[5]) for r in rows).get(st))
             for st in (PLAIN, LAST_CANDIDATE, 'list')]
    print('  property 3, allocation: %s'
          % ', '.join('%s %s' % (st, '--' if a is None else '%.2fx' % a)
                      for st, a in tiers))
    if unknown:
        print('  `needs` unwritten: %s' % ', '.join(unknown))


def repoint(prev, readme, run_doc):
    """Post-run step 5's repoint, which the chapter says to do site by site.

    Every link into `runs/PREV.md` moves to the newest run file, except a
    link whose OWN TEXT names PREV --- `[in Run 38's own file]`, the delta
    chain's and the ANSWERED entry's --- which is that run's record and
    stays; the Contents entry `- [Run PREV](runs/PREV.md)` is the one
    link naming PREV that moves, renamed with it. Reference definitions
    move too. Run 39's session did this by hand over twenty-six links and
    missed the reference definition on its first pass. Each kept link is
    printed, so the one judgement left is read rather than made.
    """
    m = re.match(r'run(\d+)$', prev)
    now = run_no_of(run_doc)
    if not m or now is None:
        sys.stderr.write('--repoint: wants PREV as runN and a run file'
                         ' named runM.md\n')
        return 2
    pn, new = m.group(1), 'run%d' % now
    text = open(readme, encoding='utf-8').read()
    names_prev = re.compile(r'(?i)\brun[ -]?%s\b' % pn)
    kept, moved = [], [0]
    text = re.sub(r'^(\s*- )\[Run %s\]\(runs/%s\.md\)' % (pn, prev),
                  lambda mm: (moved.__setitem__(0, moved[0] + 1)
                              or '%s[Run %d](runs/%s.md)'
                              % (mm.group(1), now, new)),
                  text, flags=re.M)

    def link(mm):
        if names_prev.search(mm.group(1)):
            # KEPT WITHOUT ITS ANCHOR: --check-doc resolves an anchor into
            # an older run's file as dead, and Run 38's ANSWERED link was
            # met that way; the older run's links name its file whole.
            kept.append(' '.join(mm.group(0).split())
                        + (' (anchor dropped)' if mm.group(2) else ''))
            return '[%s](runs/%s.md)' % (mm.group(1), prev)
        moved[0] += 1
        return '[%s](runs/%s.md%s)' % (mm.group(1), new, mm.group(2))
    text = re.sub(r'\[([^\]]*)\]\(runs/%s\.md([^)]*)\)' % prev, link, text)

    def ref(mm):
        moved[0] += 1
        return '%sruns/%s.md' % (mm.group(1), new)
    text = re.sub(r'^(\[[^\]]+\]: )runs/%s\.md' % prev, ref, text,
                  flags=re.M)
    open(readme, 'w', encoding='utf-8').write(text)
    print('--repoint: %d link(s) moved from runs/%s.md to runs/%s.md in %s'
          % (moved[0], prev, new, os.path.basename(readme)))
    for k in kept:
        print('  kept, its own text naming %s: %s' % (prev, k))
    return 0


def counts_cost(run):
    """What each counts stage took, off the evening's own stamps.

    Provenance quotes the counted work's cost per half, and Run 39's
    session took it by pairing the `start` and `done` stamps in a script
    of its own. A stage the status file shows started and not done is
    named rather than counted.
    """
    status = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '%s-evening.txt' % run)
    if not os.path.exists(status):
        sys.stderr.write('--counts-cost: no %s\n' % os.path.basename(status))
        return 2
    rx = re.compile(r'^=== (\S+) counts (\S+) (\S+): (start|done)')
    began, took, open_ = {}, collections.OrderedDict(), []
    for line in open(status, encoding='utf-8'):
        m = rx.match(line)
        if not m:
            continue
        t = datetime.datetime.fromisoformat(m.group(1))
        key = (m.group(2), m.group(3))
        if m.group(4) == 'start':
            began[key] = t
        elif key in began:
            took[key] = (t - began.pop(key)).total_seconds()
    open_ = sorted('%s %s' % k for k in began)
    if not took:
        sys.stderr.write('--counts-cost: no finished counts stage in %s\n'
                         % os.path.basename(status))
        return 2
    print('counts stages of %s, seconds, off %s'
          % (run, os.path.basename(status)))
    halves = []
    for (h, pop), s in took.items():
        print('  %-14s %-10s %7.0f' % (h, pop, s))
        if h not in halves:
            halves.append(h)
    for h in halves:
        print('total %-14s %7.0f s' % (h, sum(s for (hh, _), s in took.items()
                                             if hh == h)))
    if open_:
        print('started and not done, so not counted: %s' % ', '.join(open_))
    return 0


def compare_cell(cells, shapes, meta, path, other, main_hs, cell):
    """One cell on both halves, on every clock this directory keeps.

    Sizing an intrusion wants the cell on the corrected net the tables
    publish AND on the mutator clock `--wild` reads, the one being what a
    published figure took and the other what the intruder cost the
    process; Run 39's session read the second off two `--wild` tables by
    grep, quoted it alone, and the checker found the net figure two and
    a half to three times larger. `this/other` is this file over the
    `--compare` one.
    """
    sh, _, st = cell.partition('/')
    b_cells, b_shapes, _ = load_other(other, main_hs, shapes, meta)
    if (sh not in cells or st not in cells[sh] or sh not in b_cells
            or st not in b_cells[sh]):
        sys.stderr.write('--cell: %s is not a cell of both files, so nothing'
                         ' is read\n' % cell)
        return 2
    a, b = cells[sh][st], b_cells[sh][st]
    print('cell %s, %s / %s' % (cell, os.path.basename(path),
                                  os.path.basename(other)))
    print('  %-18s %14s %14s %10s' % ('', 'this', 'other', 'this/other'))
    for label, key in (('raw slope, s', 'slope'), ('net, s', 'net')):
        print('  %-18s %14.6g %14.6g %10.4f'
              % (label, a[key], b[key], a[key] / b[key] if b[key] else 0.0))

    def mutator(json_path):
        log = json_path[:-len('.json')] + '.log'
        if not os.path.exists(log):
            return None
        samples, _ = read_wild(log)
        ds = [d for nm, d in samples if nm == cell]
        if not ds:
            return None
        its = sum(d['iters'] for d in ds) or 1
        withf = [d for d in ds if 'foreign' in d]
        own = sum(d['own'] for d in withf)
        return (sum(d['mut'] for d in ds) / its,
                sum(d['foreign'] for d in withf) / own if own else None)
    ma, mb = mutator(path), mutator(other)
    if ma and mb:
        print('  %-18s %14.0f %14.0f %10.4f'
              % ('mutator per iter', ma[0], mb[0],
                 ma[0] / mb[0] if mb[0] else 0.0))
        print('  %-18s %14s %14s'
              % ('foreign, cores', '--' if ma[1] is None else fmt_ratio(ma[1]),
                 '--' if mb[1] is None else fmt_ratio(mb[1])))
    else:
        print('  no @@wild samples for this cell in %s, so the mutator'
              ' clock is not read'
              % ' and '.join(os.path.basename(q[:-5] + '.log')
                             for q, m in ((path, ma), (other, mb)) if not m))
    return 0


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
                                 'rows needs timed outside family plain')


def table_leaders(cells, shapes, strategies, args):
    """The table's rows and who leads it, or None where there is no table.

    `--block` computes this twice per call -- once for the verdicts it
    prints and once for the summary row it checks -- and the second is
    validating the ranking the first printed, so a drift between the two
    copies would make the check disagree with the paragraph it is there
    to police, silently. Each caller keeps its own early return: the
    verdicts want a timed arm, the summary row wants the best arm outside
    the vecdims family, the family's own leader and `mut-odo-vecdims`
    besides.

    `family` is the *ceiling* column, which the run file defines as the
    leading arm OF the family and not the fastest arm on the table: the
    two coincided until outside arms overtook the family, and reading the
    column off `timed[0]` then disagreed with all nine of Run 22's written
    rows at once, and crowned `libunord-stage2` the fastest ceiling in
    `--extremes`. 2026-09-01, by review.
    """
    rows, have_list = strategy_rows(cells, shapes, strategies)
    if not have_list:
        return None
    needs = {st: n for st, (_, _, n, _)
             in readme_rows(want_run_doc(args), strategies).items()}
    timed = [r for r in rows if not is_control(r.st) and r.time == r.time]
    return LEADERS(rows, needs, timed,
                   [r for r in timed if not r.st.startswith(FAMILY)],
                   [r for r in timed if r.st.startswith(FAMILY)],
                   next((r for r in timed if r.st == PLAIN), None))


def summary_row(cells, shapes, strategies, args, main_hs):
    """Check this class's row of the cross-class summary against the cells.

    The summary was the last figure-bearing table with no installer, its
    emphasis applied by hand and inconsistent across runs -- `scaled`'s
    pure arm is bold in Run 14 and was not in Run 13 on the same arm, and
    `rev`'s is bold in neither while naming the same arm as `bcast`'s,
    which is. `install-tables.sh` has installed it since 2026-09-22,
    taking the emphasis off `--block`'s `summary bolds` line, which
    decides on the unrounded values and so ends that drift.
    What this mode adds is the check the README already asks for: the summary
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
    classes = {dims[s]['cls'] for s in shapes if s in dims}
    if len(classes) != 1:
        return
    if run_doc_mismatch(args, 'summary row `%s`' % class_prefix(shapes)):
        return
    whole = {s for s, d in dims.items() if d['cls'] in classes}
    label = class_prefix(shapes)
    if set(shapes) != whole:
        sys.stderr.write('summary row `%s` not checked: this run carries %d'
                         ' of the class\'s %d shapes\n'
                         % (label, len(shapes), len(whole)))
        return
    led = table_leaders(cells, shapes, strategies, args)
    if led is None:
        return
    outside, family, plain = led.outside, led.family, led.plain
    if not (led.timed and outside and family and plain):
        return
    aa = aa_pairs(cells, shapes, strategies)
    if not aa:
        return
    want = ['%d' % len(shapes), '%.3f' % plain.time, '%.3f' % plain.worst,
            '%s %.3f' % (outside[0].st, outside[0].time),
            '%s %.3f' % (family[0].st, family[0].time),
            '%.2f%%' % (abs(aa_floor(aa).g - 1) * 100)]
    try:
        doc = open(want_run_doc(args)).read()
    except OSError as exc:
        sys.stderr.write('summary row `%s` not checked: %s\n' % (label, exc))
        return
    hit = [l for l in doc.split('\n') if l.startswith('| `%s` |' % label)]
    if len(hit) != 1:
        sys.stderr.write('summary row `%s` not checked: %d line(s) in %s'
                         ' start it, need exactly one\n'
                         % (label, len(hit),
                            os.path.basename(args.run_doc or '')))
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
    the run's. In WHAT ORDER: the line takes its order from the RUN
    and, since 2026-09-11, SAYS so instead of calling it the lead's. It
    used to say the lead's while taking the run's, so a lead listing them
    differently mislabelled figures -- which `flip` did the moment
    `flip-fwd-rows96` landed, its lead naming the new view last where the
    run puts it first -- and that was the one of the three readings
    nothing could catch. And each `l` and
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
    classes = {dims[s]['cls'] for s in shapes if s in dims}
    label = class_prefix(shapes)
    if len(classes) != 1:
        return
    whole = {s for s, d in dims.items() if d['cls'] in classes}
    if run_doc_mismatch(args, 'lead `%s`' % label):
        return
    if set(shapes) != whole:
        sys.stderr.write('lead `%s` not checked: this run carries %d of the'
                         ' class\'s %d shapes\n'
                         % (label, len(shapes), len(whole)))
        return
    try:
        doc = open(want_run_doc(args)).read()
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
                         % (label, len(hit),
                            os.path.basename(args.run_doc or '')))
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
    'CLASS_READING', 'label n plain worst out_st out gap gapp '
                     'ceil_st ceil floor floor_pair')


def class_reading(path, main_hs, args):
    """One class's row of the cross-class summary, off its own cells.

    The same six figures `summary_row` checks a written row against, plus
    the two the row does not carry and a superlative about the eight
    keeps being made on: the gap from the family's plain arm to the best
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
    if led is None or not (led.timed and led.outside and led.family
                           and led.plain):
        sys.exit('%s: no `list` baseline, no timed arm outside `%s`, none'
                 ' in it, or no `%s` at all, so this class has no row'
                 % (os.path.basename(path), FAMILY, PLAIN))
    out, ceil, plain = led.outside[0], led.family[0], led.plain
    m = break_margin(cells, shapes, out.st, plain.st)
    aa = aa_floor(aa_pairs(cells, shapes, strategies))
    return CLASS_READING(class_prefix(shapes), len(shapes), plain.time,
                         plain.worst, out.st, out.time,
                         out.time / plain.time,
                         float('nan') if m is None else m.g,
                         ceil.st, ceil.time,
                         float('nan') if aa is None else abs(aa.g - 1) * 100,
                         '--' if aa is None else aa.a)


def run_populations(run):
    """Every timed population JSON a run left, main set and classes, both
    halves -- and NOT the gate's four or the alone legs'.

    Globbed rather than listed because the class set is Main.hs's and moves
    with it: a mode that spelled the eleven names out would answer for ten
    the day one landed. The two exclusions are by artifact kind and not by
    name, the gate being five arms at a gate's budget and an alone leg one
    bench, neither of which is a population.

    THE PREFIX IS GLOBBED WHERE IT POINTS, so a bare `run31` reads the
    working directory -- which every driver here cds to -- and a
    `/tmp/xxx/zz` reads there. That is what lets a case plant a population
    and sweep it without the real artifacts beside it answering instead,
    and it costs a session nothing, `main_hs` being the roster's home and
    not the run's.
    """
    out = []
    for path in sorted(glob.glob('%s-*.json' % run)):
        b = os.path.basename(path)
        base = os.path.basename(run)
        if '-gate-' in b or b.startswith('%s-al-' % base):
            continue
        out.append(path)
    return out


def series_table(a, b, shape, args, where='.'):
    """One cell's reading on every run on disk, run by run and half by half.

    `a` over `b` on SHAPE, on each run's main set on each half, off the
    notes and JSONs in WHERE: the cell's ratio on `net`, or on `slope`
    where either arm has no corrected time, beside that half's
    main-set floor, so whether a reading clears it is read off the
    row. Written 2026-09-17 for `mut-odo-vecdims` over `bq-expand` on
    `stretch-pow2stride`, whose readings Runs 30 to 34 requoted run by run
    in the properties, the head, README's opening and an open entry. A
    reading and not a gate: exit 0, and 2 where no run on disk carries the
    cell.
    """
    def run_no(path):
        return int(re.match(r'run(\d+)', os.path.basename(path)).group(1))
    notes = sorted(glob.glob(os.path.join(where, 'run[0-9]*-pair.txt')),
                   key=run_no)
    print('`%s` over `%s` on `%s`, main set, every run in %s: below 1 is'
          ' `%s` the faster' % (a, b, shape, where, a))
    print()
    print('| run | basis | ratio | floor | control | ratio | floor |')
    print('|---|---|---:|---:|---|---:|---:|')
    read = 0
    for note in notes:
        run = note[:-len('-pair.txt')]
        halves = note_halves(run)
        if not halves:
            continue
        cols = []
        for h in halves:
            path = '%s-%s-main.json' % (run, h)
            ratio = floor = '--'
            if os.path.exists(path):
                cells, shapes, strategies, _meta = load(path, args.main)
                apply_correction(cells, shapes, strategies, args.corr)
                fl = aa_floor(aa_pairs(cells, shapes, strategies))
                floor = '%.2f%%' % (abs(fl.g - 1) * 100) if fl else '--'
                if shape in shapes and a in strategies and b in strategies:
                    key, sunk = pair_sunk(cells, [shape], a, b)
                    if not sunk:
                        ratio = '%.4f' % (cells[shape][a][key]
                                          / cells[shape][b][key])
                        read += 1
            cols += [h, ratio, floor]
        print('| %s | %s | %s | %s | %s | %s | %s |'
              % ((os.path.basename(run),) + tuple(cols)))
    if not read:
        sys.stderr.write('--series: no run in %s carries `%s` and `%s` on'
                         ' `%s`\n' % (where, a, b, shape))
        return 2
    return 0


def floor_pairs(run, args):
    """Every A/A pair of RUN against its original, per population and half,
    each judged against that population's own floor.

    The standing floor-pair registration -- *the A/A copies against their
    originals within the class floor on both halves* -- is the one item a
    run carries every time and the one item no mode adjudicated. Run 32
    read it as sixteen `predict: pair` spans; Run 33's registration wrote
    it as prose with no span at all, so its forty-four readings were taken
    by a script written for the evening and thrown away, which is the
    state every hand-rolled computation here has been recorded in before
    it became a mode.

    IT IS THE READER'S OWN CALIBRATION AND NOT A SECOND ONE: each
    population is loaded and handed to `aa_table`, whose `collect` gives
    back the pairs and the floor it printed, so this mode and `--aa` can
    only ever disagree by disagreeing with themselves. The floor is
    `max |ratio - 1|` over those pairs, so the widest pair EQUALS it by
    construction -- which is the reading, and why a pair reported `carries
    it` is not a pair reported outside.
    """
    paths = sorted(glob.glob('%s-*.json' % run))
    paths = [p for p in paths
             if not os.path.basename(p).startswith('%s-gate-' % run)
             and '-al-' not in os.path.basename(p)]
    if not paths:
        sys.stderr.write('%s: no population JSON here, so the floor pairs'
                         ' were not read\n' % run)
        return 2
    total, read, carriers = 0, 0, collections.Counter()
    print('the A/A copies of %s against their originals, per population'
          ' and half' % run)
    for path in paths:
        cells, shapes, strategies, meta = load(path, args.main)
        apply_correction(cells, shapes, strategies, args.corr)
        pairs = aa_pairs(cells, shapes, strategies)
        if len(pairs) < 2:
            print('\n%s -- NOT READ: fewer than two A/A pairs, so it has'
                  ' no floor of its own' % os.path.basename(path))
            continue
        read += 1
        carrier = aa_floor(pairs)
        floor = abs(carrier.g - 1) * 100
        carriers[carrier.a] += 1
        print('\n%s -- floor %.2f%%, carried by `%s`'
              % (os.path.basename(path), floor, carrier.a))
        for p in pairs:
            total += 1
            print('  %-58s %.4f  %5.2f pts%s'
                  % (p.a + ' / ' + p.b, p.g, abs(p.g - 1) * 100,
                     '  <- the floor' if p is carrier else ''))
    # NO VERDICT COLUMN, and that is the reading rather than a shortfall:
    # the floor IS `max |g - 1|` over these very pairs, so `inside its own
    # population's floor` is true of every one of them by construction and
    # a column saying so would be a silent search. What the registration
    # is really asking -- how wide each half's floor is and WHICH pair
    # carries it -- is what the lines above answer, and Run 32's item (8)
    # asked for the carrier by hand for the same reason. A pair genuinely
    # outside something is a pair read against ANOTHER population's floor
    # or another run's, which is a cross-population claim this chapter
    # does not make.
    print('\n%d pair reading(s) over %d population(s). The floor of each is'
          ' the widest of its own pairs, so no reading here can be outside'
          ' it: what the standing registration asks is how wide it is and'
          ' which pair carries it.' % (total, read))
    for arm, n in carriers.most_common():
        print('  `%s` carries it in %d of %d' % (arm, n, read))
    return 0


def note_halves(run):
    """RUN's halves off its note, `RUN-pair.txt`, as (basis, other), or
    None where there is no note or no HALVES line. RUN is a path prefix,
    `DIR/run<N>`."""
    try:
        text = open('%s-pair.txt' % run).read()
    except OSError:
        return None
    m = re.search(r'^HALVES:\s*basis=(\w+)\s+other=(\w+)', text, re.M)
    return (m.group(1), m.group(2)) if m else None


def note_compare(run):
    """The run RUN's note names on its `COMPARE: run<N>` line, as a path
    prefix beside RUN, or None where the note has no such line.

    It is the earlier run every cross-run reading of the pair goes against,
    and `--movement`, `--bridge` and `--half-movers` default to it. A line
    naming anything but a run exits 2 rather than returning None, since
    None sends each of them back to a default the line was written to
    overrule.
    """
    try:
        text = open('%s-pair.txt' % run).read()
    except OSError:
        return None
    m = re.search(r'^COMPARE:(.*)$', text, re.M)
    if not m:
        return None
    name = m.group(1).strip()
    if not re.fullmatch(r'run\d+', name):
        sys.stderr.write("%s-pair.txt's COMPARE line names '%s', where it"
                         " names a run, 'COMPARE: run<N>'\n" % (run, name))
        sys.exit(2)
    return os.path.join(os.path.dirname(run), name)


def json_run_half(path):
    """A population JSON's run prefix, half and population, off its name
    `DIR/run<N>-HALF-POP.json`, or None."""
    m = re.match(r'(run\d+)-(\w+)-(.+)\.json$', os.path.basename(path))
    if not m:
        return None
    return (os.path.join(os.path.dirname(path), m.group(1)), m.group(2),
            m.group(3))


def half_movers(run, prev, args):
    """Each half of RUN against the same half of PREV, over every population
    both runs have, naming the arms that moved past the population's floor
    on ONE half while the other half stayed inside its own: the half-local
    movers, which a pair's variable cannot make and no within-pair reading
    can see.

    Run 33's basis read `lib-stage2-lean-u1` 29.5% slower than HEAD's over
    `runs`, counts level, and the open list recorded a compiler worth
    that much for a day. Against Run 32, HEAD's half had not moved on any
    of the fourteen shapes and the basis had moved 12 to 19 percent on
    every shape from `runs-7` up -- the same bytes at the same virtual
    addresses, slow in the file the evening ran and fast in a byte-identical
    copy of it, the physical frame the page cache held the fill loop's
    page in being the whole of it (README, the placement section). The
    A/A pairs share the binary and the counts share the code, so this
    cross-run reading per half is the one instrument for that class of
    term, and it was taken by hand on 2026-09-16.

    Halves come off each run's pair note, `HALVES: basis=X other=Y`, basis
    against basis and other against other, so the two halves compared are
    the same recipe with whatever the runs changed between them. The bar
    is `--movers`'s, 3% unless given, since a cross-run reading carries
    the box and the source under both halves and the within-run floor
    does not bound those: read against the floor alone, Run 33 over Run
    32 flagged seventy arms at a percent, most of them HEAD's fills
    gaining what the exit span bought. What is flagged is an arm past the
    bar on one half and not the other, the two halves' readings apart by
    more than the wider of their A/A floors on that population, as `--aa`
    and `--floor-pairs` read them. Counts are read beside the time where
    both runs carry a sweep for the half, `RUN-counts-HALF[-POP].txt`. A
    flagged arm wants the copy test before any attribution -- the half
    copied to a probe name and the cell timed on both, one minute -- and
    `probe-pageflags.py` on the slow instance while it runs. A reading and
    not a gate: exit 0 whatever it finds, 2 where nothing could be read.
    """
    h_run, h_prev = note_halves(run), note_halves(prev)
    for r, h in ((run, h_run), (prev, h_prev)):
        if not h:
            sys.stderr.write('%s-pair.txt: no HALVES line, so the halves'
                             ' were not read and nothing was compared\n' % r)
            return 2
    head = '%s-%s-' % (os.path.basename(run), h_run[0])
    pops = [os.path.basename(p)[len(head):-5]
            for p in sorted(glob.glob('%s-%s-*.json' % (run, h_run[0])))]
    if not pops:
        sys.stderr.write('%s: no population JSON on its basis half, so the'
                         ' half-local movers were not read\n' % run)
        return 2

    def sweep_of(r, half, pop):
        p = '%s-counts-%s%s.txt' % (r, half,
                                    '' if pop == 'main' else '-' + pop)
        return parse_counts(p)[0] if os.path.exists(p) else None

    pct = args.movers if args.movers is not None else 3.0
    lim = pct / 100.0
    print('half-local movers of %s against %s past %g%%: each half over'
          ' the same half of the other run, per population, this run over'
          ' that one'
          % (os.path.basename(run), os.path.basename(prev), pct))
    flagged, both, read = [], 0, 0
    for pop in pops:
        sides = []
        for k in (0, 1):
            this = '%s-%s-%s.json' % (run, h_run[k], pop)
            that = '%s-%s-%s.json' % (prev, h_prev[k], pop)
            if not os.path.exists(this) or not os.path.exists(that):
                sides = None
                break
            cells, shapes, strategies, meta = load(this, args.main)
            apply_correction(cells, shapes, strategies, args.corr)
            b_cells, b_shapes, b_strategies = load_other(that, args.main,
                                                         shapes, meta)
            pairs = aa_pairs(cells, shapes, strategies)
            floor = (abs(aa_floor(pairs).g - 1) if len(pairs) >= 2
                     else None)
            ca = sweep_of(run, h_run[k], pop)
            cb = sweep_of(prev, h_prev[k], pop)
            both_sh = [x for x in shapes if x in b_shapes]
            g, c = {}, {}
            for st in strategies:
                if no_net(st) or st not in b_strategies:
                    continue
                rs = [cells[sh][st]['net'] / b_cells[sh][st]['net']
                      for sh in both_sh
                      if cells[sh][st]['net'] > 0
                      and b_cells[sh][st]['net'] > 0]
                if rs:
                    g[st] = geomean(rs)
                if ca and cb:
                    cs = [ca[sh][st] / cb[sh][st] for sh in both_sh
                          if st in ca.get(sh, {}) and st in cb.get(sh, {})]
                    if cs:
                        c[st] = geomean(cs)
            sides.append((floor, g, c))
        if sides is None:
            print('\n%s -- NOT READ: a half of one run has no JSON for it'
                  % pop)
            continue
        read += 1
        (f0, g0, c0), (f1, g1, c1) = sides
        print('\n%s -- floors %s on %s, %s on %s' % (
            pop,
            'none' if f0 is None else '%.2f%%' % (f0 * 100), h_run[0],
            'none' if f1 is None else '%.2f%%' % (f1 * 100), h_run[1]))
        if f0 is None or f1 is None:
            print('  a half with fewer than two A/A pairs has no floor, so'
                  ' nothing here is flagged')
            continue
        rows = []
        for st in g0:
            if st not in g1:
                continue
            moved = (abs(g0[st] - 1) > lim, abs(g1[st] - 1) > lim)
            # THE RULE: past the bar on one half and not the other, and
            # the two halves' readings apart by more than the wider
            # floor. Both past the bar is the source, the shim or the box
            # moving under both halves and is counted rather than
            # flagged; the floor clause keeps a 2.9 beside a 3.1 out.
            local = (moved[0] != moved[1]
                     and abs(g0[st] / g1[st] - 1) > max(f0, f1))
            if moved[0] and moved[1]:
                both += 1
            if local:
                rows.append((st, g0[st], g1[st], c0.get(st), c1.get(st),
                             h_run[0] if moved[0] else h_run[1]))
        if not rows:
            print('  no half-local mover past %g%% over %d arm(s)'
                  % (pct, len(g0)))
            continue
        print('  %-34s %8s %8s %8s %8s  %s'
              % ('arm', h_run[0], h_run[1], 'counts', 'counts', 'moved on'))
        rows.sort(key=lambda r: -max(abs(r[1] - 1), abs(r[2] - 1)))
        for st, a, b, ka, kb, side in rows:
            print('  %-34s %8.4f %8.4f %8s %8s  %s'
                  % (st, a, b,
                     '--' if ka is None else '%.4f' % ka,
                     '--' if kb is None else '%.4f' % kb, side))
            flagged.append((pop, st, side))
    if not read:
        sys.stderr.write('%s against %s: no population has a JSON on both'
                         ' halves of both runs, so nothing was compared\n'
                         % (os.path.basename(run), os.path.basename(prev)))
        return 2
    print('\n%d half-local mover(s) over %d population(s) read; %d arm(s)'
          ' moved on both halves and are the runs parting, not a half.'
          % (len(flagged), read, both))
    if flagged:
        print('A half-local mover with its counts level is a term of that'
              ' half\'s binary or its file instance and not the pair\'s'
              ' variable: copy the half to a probe name and time the cell'
              ' on both before attributing it, and read the frames with'
              ' probe-pageflags.py while the slow instance runs.')
    return 0

# The count-led offenders a cell reading meets again and again, by arm:
# what the mode says under the table when a cell of that arm is count-led,
# so that the account is met where the figure is read and not only in the
# open list. One entry so far, the latch of GHC
# https://gitlab.haskell.org/ghc/ghc/-/work_items/27799.
KNOWN_COUNT_LED = {
    'lib-stage2-lean-u1':
        "GHC #27799's latch on a rank-1 view, one instruction an element that"
        " the uniques choose and not the compiler; the open list's *A loop's"
        " latch keeps its fall-through* entry, which says where to price"
        " the unrolling instead",
}
# And the time-led one a compiler pair meets on the reducers' short runs,
# by arm suffix, said under a table where such a row reads the basis the
# faster: the shared per-run loop of the `-sum` consumers, whose HEAD half
# lays the exit block inside the cycle.
KNOWN_TIME_LED = {
    '-sum':
        "on three-element runs, HEAD's code order on the shared"
        " per-run loop of the reducers, a taken branch and two fetch blocks"
        " a run more; the placement section's *The two stage arms'"
        " mechanism* paragraph, and not a placement the shim can move",
}


def cell_movers(run, top, args):
    """Every cell of RUN across its two halves, time beside counts, the
    TOP ranked by what the counts do not explain: post-run step 4b.

    Every other reading of a pair is an arm's geomean over its
    population's shapes, and a geomean dilutes one cell by the shape
    count: a cell at 1.25 among seventeen is an arm at 1.01, which no bar
    here flags. Run 34's record was written from those readings and
    carried none of the run's largest cells -- the `mut-odo-vecdims`
    family at 1.23 on one `runs` view with counts level, one branch
    mispredict a run on `compose-zero-mid`, and the latch of GHC
    https://gitlab.haskell.org/ghc/ghc/-/work_items/27799 on
    `lib-stage2-lean-u1`'s rank-1 views, the run's largest count
    differences -- found only when the cells were ranked by hand on
    2026-09-17.

    The direction is `--compare`'s: the basis over the other half, both
    columns, so a row reads without inverting either. The rank is the
    time ratio over the count ratio, or the time ratio alone where the
    half's sweep has no count for the cell. A count-led row is the
    codegen's and `KNOWN_COUNT_LED` names the offender where it has one;
    a time-led row with counts level is one half's binary, instance or
    process, which the copy test of step 4a and the cell in a fresh
    process tell apart, and one whose twins part is bench position. A
    reading and not a gate: exit 0 whatever it finds, 2 where nothing
    could be read.
    """
    h = note_halves(run)
    if not h:
        sys.stderr.write('%s-pair.txt: no HALVES line, so the halves were'
                         ' not read and no cell was compared\n' % run)
        return 2
    head = '%s-%s-' % (os.path.basename(run), h[0])
    pops = [os.path.basename(p)[len(head):-5]
            for p in sorted(glob.glob('%s-%s-*.json' % (run, h[0])))]
    if not pops:
        sys.stderr.write('%s: no population JSON on its basis half, so no'
                         ' cell was compared\n' % run)
        return 2

    def sweep_of(half, pop):
        p = '%s-counts-%s%s.txt' % (run, half,
                                    '' if pop == 'main' else '-' + pop)
        return parse_counts(p)[0] if os.path.exists(p) else None

    rows, read = [], 0
    for pop in pops:
        this = '%s-%s-%s.json' % (run, h[0], pop)
        that = '%s-%s-%s.json' % (run, h[1], pop)
        if not os.path.exists(that):
            print('%s -- NOT READ: no JSON on the %s half' % (pop, h[1]))
            continue
        read += 1
        cells, shapes, strategies, meta = load(this, args.main)
        apply_correction(cells, shapes, strategies, args.corr)
        b_cells, b_shapes, b_strategies = load_other(that, args.main,
                                                     shapes, meta)
        ca, cb = sweep_of(h[0], pop), sweep_of(h[1], pop)
        for sh in shapes:
            if sh not in b_shapes:
                continue
            for st in strategies:
                if (st not in b_strategies or st not in b_cells[sh]
                        or st not in cells[sh]):
                    continue
                key = 'slope' if no_net(st) else 'net'
                a = cells[sh][st].get(key)
                b = b_cells[sh][st].get(key)
                if not a or not b or a <= 0 or b <= 0:
                    continue
                tr = a / b
                cr = None
                if ca and cb and ca.get(sh, {}).get(st) \
                        and cb.get(sh, {}).get(st):
                    cr = ca[sh][st] / cb[sh][st]
                dev = abs(math.log(tr / cr if cr else tr))
                rows.append((dev, pop, sh, st, tr, cr))
    if not rows:
        sys.stderr.write('%s: no cell is on both halves of any population,'
                         ' so nothing was compared\n' % run)
        return 2
    rows.sort(key=lambda r: -r[0])
    print('cell movers of %s: every cell of every population across the'
          ' halves, %s over %s on both columns, the %d of %d ranked by the'
          ' time ratio over the count ratio, or by the time ratio where'
          ' the sweep has no count'
          % (os.path.basename(run), h[0], h[1], min(top, len(rows)),
             len(rows)))
    print('  %-9s %-24s %-40s %8s %8s %12s'
          % ('pop', 'shape', 'arm', 'time', 'counts', 'time/counts'))
    shown = rows[:top]
    for _dev, pop, sh, st, tr, cr in shown:
        print('  %-9s %-24s %-40s %8.4f %8s %12s'
              % (pop, sh, st, tr,
                 '--' if cr is None else '%.4f' % cr,
                 '--' if cr is None else '%.4f' % (tr / cr)))
    # THE COUNT-LED CELLS ARE LISTED WHATEVER THEIR RANK: the table above
    # is the time's, and a count step of a few percent ranked below the
    # reducers' term on Run 34, which is how the latch went
    # unnamed on Run 34 -- the latch's count differences, the run's
    # largest, sat outside every top twenty read by time.
    led = sorted([(abs(math.log(cr)), pop, sh, st, tr, cr)
                  for _d, pop, sh, st, tr, cr in rows
                  if cr is not None and abs(math.log(cr)) > 0.03],
                 key=lambda r: -r[0])
    if led:
        print('\ncount-led cells, the counts past 3%%, the codegen\'s, all'
              ' %d ranked by the counts:' % len(led))
        for _d, pop, sh, st, tr, cr in led:
            print('  %-9s %-24s %-40s %8.4f %8.4f %12.4f'
                  % (pop, sh, st, tr, cr, tr / cr))
        for st in sorted({st for _d, _p, _s, st, _t, _c in led}):
            if st in KNOWN_COUNT_LED:
                print('  %s: %s' % (st, KNOWN_COUNT_LED[st]))
    else:
        print('\nno cell is count-led past 3%.')
    print('\nA time-led cell with its counts level is one half\'s binary,'
          ' file instance or process, which the copy test of step 4a and'
          ' the cell timed in a fresh process tell apart, or bench'
          ' position where the arm\'s twins part from it.')
    for suffix, note in KNOWN_TIME_LED.items():
        if any(st.endswith(suffix) and tr < 1
               for _d, _p, _s, st, tr, _c in shown):
            print('  `%s` arms above: %s' % (suffix, note))
    print('\n%d cell(s) over %d population(s) read.' % (len(rows), read))
    return 0


def movement(path, args):
    """The published column this install is about to overwrite, against the
    one going in -- post-run step 5a, whose window 5b closes.

    A *moved from X to Y* sentence compares against the figures the install
    replaces, and after it they are in git or in the kept JSON only. Two
    runs took that reading by hand: Run 33 wrote a throwaway script over
    the two tables and then published `sixteen points` for a row that had
    moved fourteen, the figure having been read off three decimals rather
    than off the column.

    IT READS THE SAME TWO SOURCES THE INSTALL DOES: `readme_rows` for the
    table in the run file, `strategy_rows` for this run, so the movement
    cannot disagree with what `--markdown` is about to write. And it says
    of every row what the chapter says once: the published column is
    winsorized per row and per run, so a row's movement between runs is
    the estimator's as much as the arm's -- `--compare` against the
    previous run's own JSON is what says how far the ARM moved.
    """
    cells, shapes, strategies, meta = load(path, args.main)
    apply_correction(cells, shapes, strategies, args.corr)
    rows, have_list = strategy_rows(cells, shapes, strategies)
    if not have_list:
        sys.stderr.write('%s: no `list` bench, so every published time is'
                         ' `--` and there is nothing to compare\n'
                         % os.path.basename(path))
        return 2
    doc = want_run_doc(args)
    prev = readme_rows(doc, set(strategies), set(strategies))
    if not prev:
        sys.stderr.write('%s: no Results table to compare against, so the'
                         ' movement reading did not happen\n'
                         % os.path.basename(doc or '(no run doc)'))
        return 2
    print('the published `time` column of %s against the table in %s'
          % (os.path.basename(path), os.path.basename(doc)))
    print('%-44s %8s %8s %9s' % ('strategy', 'there', 'here', 'points'))
    moved = flat = 0
    for r in rows:
        if r.st not in prev:
            continue
        was = prev[r.st][3].strip('*` ')
        try:
            old = float(was)
        except ValueError:
            continue            # `--`: a row with no corrected time
        if r.time != r.time:
            continue
        pts = (r.time / old - 1) * 100 if old else float('nan')
        if abs(pts) < 0.05:
            flat += 1
        else:
            moved += 1
        print('%-44s %8.3f %8.3f %+8.1f%%' % (r.st, old, r.time, pts))
    print('\n`there` is the table\'s own THREE decimals and `here` is'
          ' this run at full precision, so a movement under a point is'
          ' inside that rounding and no reading at all -- which is how a'
          ' hand-rolled form of this reading published `sixteen points`'
          ' for a row that moved fourteen, dividing 0.029 by 0.025.')
    print('%d row(s) moved and %d read the same three decimals. A row'
          ' moving here is the winsorized column moving, which is the'
          ' estimator as much as the arm: what says how far the ARM moved'
          ' is --compare against that run\'s own JSON, and the two have'
          ' parted by fourteen points on one row of one pair.'
          % (moved, flat))
    return 0


def counts_totals(run, args):
    """What each counted leg cost, per population and per half, off the
    counts files' own stamps.

    The pair note's COUNTS block asks a preparation for the PREVIOUS run's
    totals leg by leg -- to set the scale the evening's counted work is
    read against -- and no mode printed them: two preparations in a row
    derived them by hand from the `# end` lines and each recorded the
    improvisation, Run 31's note carrying twenty-two figures gathered that
    way. A scale is a reading and not a prediction, which is why it is a
    mode and not a gate.

    READ OFF EACH FILE'S OWN HEADER and not off its name: the header
    states the half and the class the sweep ran, so a file renamed or
    copied answers for the run it was written by rather than for the name
    it now carries. A leg with no `# end` line is reported UNFINISHED and
    counted in no total -- a killed sweep leaves a file that parses, and
    summing it silently would put a short leg into the scale as though it
    were a fast one.
    """
    paths = sorted(glob.glob('%s-counts-*.txt' % run))
    if not paths:
        sys.stderr.write('%s: no counts file here, so the totals did not'
                         ' happen\n' % run)
        return 2
    legs, halves, unfinished = {}, [], []
    for path in paths:
        head = end = None
        with open(path, errors='replace') as fh:
            for line in fh:
                if head is None and line.startswith('# '):
                    head = line
                elif line.startswith('# end '):
                    end = line
        if head is None:
            unfinished.append((os.path.basename(path), 'no header'))
            continue
        tag = head.split()[1]
        half = tag[len(os.path.basename(run)) + 1:] if '-' in tag else tag
        m = re.search(r'class=(\S+)', head)
        pop = m.group(1) if m else 'main'
        if half not in halves:
            halves.append(half)
        if end is None:
            unfinished.append((os.path.basename(path), 'no `# end` stamp'))
            continue
        m = re.search(r'elapsed=(\d+)s', end)
        if m is None:
            unfinished.append((os.path.basename(path),
                               'no elapsed on `# end`'))
            continue
        legs[(pop, half)] = int(m.group(1))
    pops = sorted({p for p, _ in legs}, key=lambda p: -max(
        v for (q, _), v in legs.items() if q == p))
    total = sum(legs.values())
    print('%s: %d counted leg(s) over %d population(s) and %d hal%s,'
          ' %ds in all'
          % (run, len(legs), len(pops), len(halves),
             'f' if len(halves) == 1 else 'ves', total))
    print('\n%-12s %s'
          % ('population', ' '.join('%8s' % h for h in halves)))
    for pop in pops:
        row = ' '.join('%8s' % ('%ds' % legs[(pop, h)]
                                if (pop, h) in legs else '--')
                       for h in halves)
        print('%-12s %s' % (pop, row))
    print('%-12s %s'
          % ('half total',
             ' '.join('%8s' % ('%ds' % sum(v for (_, q), v in legs.items()
                                           if q == h)) for h in halves)))
    if unfinished:
        print('\n%d leg(s) NOT summed, each reported rather than dropped:'
              % len(unfinished))
        for name, why in unfinished:
            print('  %-38s %s' % (name, why))
        return 1
    return 0


def over_list_sweep(run, args):
    """Every cell where a timed non-control arm is SLOWER than its shape's
    `list`, over every population of a run and both halves.

    The properties section makes an *only* claim about this set every run
    -- that no arm the library would ship is slower than the baseline on
    any shape, and which cells break it -- and nothing printed it: `--block`
    reads property 1 as `mut-odo-vecdims` against `bq-expand` on one
    population, and the baseline clause reaches a row's `worst` column,
    which is a maximum over shapes and not a listing of the cells past 1.
    On Run 31 the write-up hand-rolled this from `--cells` and the
    independent checker hand-rolled it again; the two agreed on three cells,
    which is two sessions deriving one negative with neither able to show
    the other what it had read.

    SO THE DENOMINATOR IS PRINTED WITH THE HITS. A sweep whose silence is
    the finding must say how much it read, or a run with no `list` and a
    run with nothing above it read alike -- which is this README's own rule
    that a grep proves nothing until it is known to find something, and is
    why the count line is not optional and not `--brief`-able.

    A reducing consumer carries no corrected time, so it is counted as
    UNREADABLE and never as clean: `no_net` is the predicate the published
    column drops on, and a claim about arms the library would ship is a
    claim about arms that carry a time to compare.
    """
    paths = run_populations(run)
    if not paths:
        sys.stderr.write('%s: no population JSON here, so the sweep did not'
                         ' happen\n' % run)
        return 2
    hits, read, unreadable, pops, baseless = [], 0, 0, 0, []
    for path in paths:
        cells, shapes, strategies, meta = load(path, args.main)
        apply_correction(cells, shapes, strategies)
        tag = os.path.basename(path)[len(os.path.basename(run)) + 1:
                                    -len('.json')]
        pops += 1
        got = 0
        for sh in shapes:
            base = cells[sh].get('list', {}).get('net')
            if base is None or base <= 0:
                continue
            got += 1
            for st in strategies:
                if st == 'list' or is_control(st):
                    continue
                v = None if no_net(st) else cells[sh].get(st, {}).get('net')
                if v is None:
                    unreadable += 1
                    continue
                read += 1
                if v / base > 1.0:
                    hits.append((tag, sh, st, v / base))
        if not got:
            baseless.append(tag)
    print('%d population(s) read, %d timed non-control cell(s) against their'
          " own shape's `list`, %d with no corrected time to read"
          % (pops, read, unreadable))
    # A POPULATION WITH NO BASELINE COMPARED NOTHING, and counted as read
    # it turned a sweep over nothing into a clean verdict: a filtered
    # probe drops `list`, and this mode's whole job is that its silence
    # be readable. Named here, and a sweep with no baseline anywhere is a
    # 2, which is the exit this directory owes for a run that did not
    # happen. Found 2026-09-14 by asking the mode a question other than
    # the one it was written for.
    if baseless:
        print('%d population(s) have NO readable `list` to compare against,'
              ' so they are read over nothing: %s'
              % (len(baseless), ', '.join(baseless)))
    if not read:
        sys.stderr.write('%s: no population here has a readable `list`, so'
                         ' the sweep compared nothing\n' % run)
        return 2
    if not hits:
        print('NO cell above 1: no timed arm outside the controls is slower'
              " than its shape's `list` anywhere in this run")
        return 0
    print('\n%-22s %-24s %-40s %s'
          % ('process', 'shape', 'arm', 'over `list`'))
    for tag, sh, st, r in sorted(hits, key=lambda h: -h[3]):
        print('%-22s %-24s %-40s %9.4f' % (tag, sh, st, r))
    print('\n%d cell(s) above 1, which is the population this run\'s'
          ' *no arm the library would ship is slower than `list`* claim is'
          ' read over.' % len(hits))
    return 0


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

    It ranks and installs nothing: `install-tables.sh` has installed the
    summary's rows since 2026-09-22, and a superlative is a sentence, so
    what this owes the author is the sort under it and not the words.

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
    print('`gap` is `%s` over the family\'s plain arm -- what the dropped'
          ' stride-conditioned redirect' % 'best outside the family')
    print('would have bought in that class -- by the published column and'
          ' then paired.')
    print('`bold` is which of those two cells the cross-class summary'
          ' EMPHASISES, and it')
    print('is here because the rule behind that emphasis is written nowhere'
          ' a reader of')
    print('the installed table would look. The rule is the'
          ' COLUMN, not the')
    print('paired ratio: the summary prints both cells to three decimals'
          ' and a reader')
    print('compares what is printed, so the faster of `best outside family`'
          ' and `ceiling`')
    print('is emphasised and nothing else decides it. FOUR of Run 28\'s ten'
          ' classes tied')
    print('at three decimals and were broken with `--pair` instead, which'
          ' put the bold on')
    print('the wrong cell of `rev`. THE `bold` COLUMN IS THE ANSWER: the'
          ' two columns')
    print('beside it are printed to three decimals like the summary\'s and'
          ' tie exactly')
    print('as it does, while `bold` is computed on the UNROUNDED values,'
          ' so it separates')
    print('where what you can read does not. Follow it rather than the'
          ' eye or `--pair`.')
    print()
    print('%-10s %6s %8s %7s %-26s %7s %8s %8s %7s %7s'
          % ('class', 'shapes', 'plain', 'worst', 'best outside family',
             'gap col', 'gap pair', 'ceiling', 'floor', 'bold'))
    for r in sorted(rows, key=lambda r: r.label):
        print('%-10s %6d %8.3f %7.3f %-26s %7.2f %8.2f %8.3f %6.2f%% %7s'
              % (r.label, r.n, r.plain, r.worst,
                 '%s %.3f' % (r.out_st, r.out), r.gap, r.gapp, r.ceil,
                 r.floor, 'outside' if r.out < r.ceil else 'ceiling'))
    print()
    print('extremes:')

    def holder(want, key):
        """The extreme over the rows that CARRY the figure. A `nan` -- a
        class with no A/A report, or one whose gap could not be paired --
        sorts wherever `min`/`max` first meet it, so the holder used to
        follow the --classes order: the same two files gave two tightest
        floors. 2026-09-01, by review."""
        live = [r for r in rows if key(r) == key(r)]
        return want(live, key=key) if live else None
    blank = [(r.label, [n for n, v in (('floor', r.floor),
                                        ('gap pair', r.gapp)) if v != v])
             for r in rows]
    blank = [(l, ks) for l, ks in blank if ks]
    if blank:
        print('  not ranked where the figure is missing: '
              + ', '.join('`%s` (%s)' % (l, ', '.join(ks)) for l, ks in blank))
    def gap_size(g):
        """A gap's SIZE is its distance from 1, |log|: while every outside
        arm trailed the plain arm the raw ratio ordered the same way, and
        they led (Run 22) `max` of the ratio named the tightest class the
        widest. `nan` stays `nan` for `holder`. 2026-09-01, by review."""
        if g != g:
            return g
        return abs(math.log(g)) if g > 0 else float('inf')
    # Each line names the holder AND its figure, so a sentence can be
    # written off this without going back to the table above -- which is
    # the step at which Run 15's third error was made. The gap lines rank
    # on `gap_size` and print the ratio.
    for what, key, want, fmt, *show in (
            ('tightest floor', lambda r: r.floor, min, '%.2f%%'),
            ('widest floor', lambda r: r.floor, max, '%.2f%%'),
            ('best for the plain arm', lambda r: r.plain, min, '%.3f'),
            ('worst for the plain arm', lambda r: r.plain, max, '%.3f'),
            ('highest `worst` cell', lambda r: r.worst, max, '%.3f'),
            ('lowest `worst` cell', lambda r: r.worst, min, '%.3f'),
            ('best outside the family', lambda r: r.out, min, '%.3f'),
            ('fastest ceiling', lambda r: r.ceil, min, '%.3f'),
            ('narrowest gap, column', lambda r: gap_size(r.gap), min,
             '%.2f', lambda r: r.gap),
            ('widest gap, column', lambda r: gap_size(r.gap), max,
             '%.2f', lambda r: r.gap),
            ('narrowest gap, paired', lambda r: gap_size(r.gapp), min,
             '%.2f', lambda r: r.gapp),
            ('widest gap, paired', lambda r: gap_size(r.gapp), max,
             '%.2f', lambda r: r.gapp)):
        hit = holder(want, key)
        if hit is None:
            print('  %-26s %-11s no class carries the figure' % (what, '--'))
            continue
        val = (show[0] if show else key)(hit)
        line = ('  %-26s %-11s ' + fmt) % (what, '`%s`' % hit.label, val)
        if 'floor' in what:
            line += '  on `%s`' % hit.floor_pair
        # A holder at zero is the qualifier Run 22 wrote by hand ("of any
        # non-degenerate class"): the sort stays a sort, and the sentence
        # is told the question. 2026-09-01, by review.
        if float((fmt % val).rstrip('%')) == 0:
            line += ('  -- 0 at this precision: say whether the arm counts'
                     ' before quoting')
        print(line)
    # THE FULL ORDER AND NOT ONLY THE HOLDER, added 2026-09-13. Every
    # superlative this mode was built for is answered by its holder line,
    # and the ORDINAL ones are not: *second widest*, *joint lowest*,
    # *third tightest* need the ranking under them. Run 30 wrote four of
    # those and every one was wrong -- two classes called joint lowest on a
    # `worst` another class beats, a floor called tightest that is third,
    # and a `list` move called second widest that is third -- each derived
    # from the arms the sentence was about instead of from a sort. A
    # holder line cannot refute any of them; the orders below refute the
    # three these rows carry, the `list` move being a cross-half figure
    # and `--compare`'s.
    print()
    print('the full order, for the ordinal claims a holder line cannot'
          ' settle:')
    for what, key, rev, fmt in (
            ('floor, tightest first', lambda r: r.floor, False, '%.2f%%'),
            ('`worst`, lowest first', lambda r: r.worst, False, '%.3f'),
            ('the plain arm, best first', lambda r: r.plain, False, '%.3f')):
        live = [r for r in rows if key(r) == key(r)]
        order = sorted(live, key=key, reverse=rev)
        print('  %-26s %s' % (what, ', '.join(('`%s` ' + fmt) % (r.label,
                                                                key(r))
                                              for r in order)))
    for want in (min, max):
        by_col = holder(want, lambda r: gap_size(r.gap))
        by_pair = holder(want, lambda r: gap_size(r.gapp))
        if by_col and by_pair and by_col.label != by_pair.label:
            print('  the %s gap is `%s` on the column and `%s` paired, so'
                  ' a sentence about it has to say which'
                  % ('narrowest' if want is min else 'widest',
                     by_col.label, by_pair.label))
    return 0


def class_says(cells, shapes, strategies, meta, args):
    """Item 6 of the class-block form with its figures in place and `___`
    where the finding goes: properties 1 and 2, `worst` and the allocation
    tiers, the best arm outside the family priced against the plain arm
    and the floor, whether the two columns may be differenced and the
    class geomean across the halves, the A/A bar of that comparison and
    the strategies past it, and the counts geomean where both sweeps are
    given. Run 34 restated every one of those by hand in ten paragraphs;
    what the class says that no reading does stays the author's.
    install-tables.sh installs it where the block's paragraph is the
    carried copy or an unfilled skeleton, and nowhere else.
    """
    led = table_leaders(cells, shapes, strategies, args)
    if led is None or not led.timed:
        return
    floor = aa_floor(aa_pairs(cells, shapes, strategies))
    plain = next((r for r in led.timed if r[1] == PLAIN), None)

    def verdict(*holds):
        if any(h is None for h in holds):
            return 'is not read'
        return 'HOLDS' if all(holds) else 'BREAKS'

    c1 = property_closest(cells, shapes, 'net', PLAIN, LAST_CANDIDATE)
    c2 = [property_closest(cells, shapes, 'alloc', PLAIN, b)
          for b in ('list', LAST_CANDIDATE)]
    p1 = verdict(None if plain is None else plain[6] < 1,
                 None if c1 is None else c1[0][0] < 1)
    p2 = verdict(*[None if c is None else c[0][0] < 1.01 for c in c2])
    tiers = dict((r[1], r[5]) for r in led.rows)
    out = ['**What the class says:** property 1 %s and property 2 %s ---'
           ' `worst` %s, tiers at %s ---'
           % (p1, p2, '--' if plain is None else '%.3f' % plain[6],
              ', '.join('--' if tiers.get(st) is None
                        else '%.2fx' % tiers[st]
                        for st in (PLAIN, LAST_CANDIDATE, 'list')))]
    if led.outside and plain and led.outside[0][0] < plain[0]:
        t, an = led.outside[0][0], led.outside[0][1]
        m = break_margin(cells, shapes, an, PLAIN)
        if m is None or floor is None:
            out.append('and `%s` leads outside the family at %.3f, not'
                       ' priced.' % (an, t))
        else:
            out.append('and `%s` leads outside the family at %.3f, priced'
                       ' against `%s` at %.4f over %d of %d shapes at sign'
                       ' p %.2g, a margin of %.2f%% against this class\'s'
                       ' %.2f%% floor (`%s`).'
                       % (an, t, PLAIN, m.g, m.k, m.n, m.p,
                          abs(m.g - 1) * 100, abs(floor.g - 1) * 100,
                          floor.a))
    elif led.outside:
        out.append('and nothing outside the family is ahead of `%s`, `%s`'
                   ' the best at %.3f.' % (PLAIN, led.outside[0][1],
                                          led.outside[0][0]))
    out.append('___ (what is this class\'s own).')
    rows, lst, partial = cross_half_rows(cells, shapes, strategies,
                                         args.compare, args.main, meta)
    vote = [r for r in rows if r[1] not in partial] or rows
    if vote and lst is not None:
        out.append('Its two columns %s be differenced, `list` having moved'
                   ' %.2f of a point, at a class geomean of %.4f over the'
                   ' %d arms,'
                   % ('MAY' if abs(lst - 1) <= 0.007 else 'may NOT',
                      abs(lst - 1) * 100, geomean([g for g, _ in vote]),
                      len(vote)))
        b_cells, b_shapes, b_strategies = load_other(args.compare, args.main,
                                                     shapes, meta)
        both_sh = [sh for sh in shapes if sh in b_shapes]
        both_st = [st for st in strategies if st in b_strategies]
        bar, carrier, arms, past = aa_bar(cells, b_cells, both_sh, both_st)
        out.append('with %d of %d strategies past an A/A bar of %.2f points.'
                   % (len(past), len(arms), bar * 100) if carrier
                   else 'with no A/A pair in both halves to set a bar.')
    else:
        out.append('No `list` on both halves, so the columns are not'
                   ' differenced.')
    if args.counts and len(args.counts) == 2 and vote:
        a_counts = parse_counts(args.counts[0])[0]
        b_counts = parse_counts(args.counts[1])[0]
        gs = []
        for _g, st in vote:
            rs = [a_counts[sh][st] / b_counts[sh][st] for sh in shapes
                  if a_counts.get(sh, {}).get(st)
                  and b_counts.get(sh, {}).get(st)]
            if rs:
                gs.append(geomean(rs))
        out.append('The counted work reads a counts geomean of %.4f over the'
                   ' same arms, %d of them counted.'
                   % (geomean(gs), len(gs)) if gs
                   else 'The counted work reads no count for these arms.')
    else:
        gs = []
    # THE COUNTS AGAINST THE CLOCK IS ARITHMETIC ON TWO FIGURES THIS
    # PARAGRAPH ALREADY PRINTS, so it is written here where both sweeps are
    # given: Run 39's session divided them by hand for ten classes. Without
    # the sweeps the slot stays, NAMED, as the one above it is: a block
    # used to carry two `___` of which one said what it wanted, and a
    # session that filled the first met a check reporting ten still open
    # (Run 37). Case: `block-writes-the-counts-clause-it-can-compute`.
    if gs and vote:
        k, q = geomean(gs), geomean([g for g, _ in vote])
        if abs(k - 1) < 0.001:
            out.append('Its counted work parts by under a tenth of a point,'
                       ' so no rate is read against its clock, which parts'
                       ' by %.2f.' % ((q - 1) * 100))
        else:
            out.append('Its counted work parts by %.2f points where its'
                       ' clock parts by %.2f, so about %.2f of the'
                       ' instruction saving reaches the clock.'
                       % ((k - 1) * 100, (q - 1) * 100, (q - 1) / (k - 1)))
    else:
        out.append("___ (how this class's counted work compares with its"
                   " clock).")
    print()
    # NOT break_on_hyphens: this paragraph is joined again by the
    # `--brief` arm and by install-tables.sh, and a wrap taken inside
    # `lib-stage2-lean-u1` comes back as `lib- stage2-lean-u1` -- an arm
    # name that renders wrong, matches no row of the table above it and
    # answers no search. Met on Run 38's `small` block, where the fill
    # split both that name and `mut-odo-vecdims`.
    print(textwrap.fill(' '.join(out), width=72, break_on_hyphens=False))


def block_skeleton(cells, shapes, strategies, meta, args, terms):
    """A stride-class block's mechanical parts in one place, in the form's
    order, which the run file's class section keeps: the six-column table,
    the controls off the same computation `--aa` prints, the provenance
    and anchor skeleton -- elapsed time and heap peaks left blank, to be
    copied from the process's stderr line rather than guessed -- and, for
    a three-shape population, the bolded rows' per-shape ratios in run
    order, which is the order the block's lead lists its shapes in. The
    judgement stays with the author: the lead is deliberately not
    scaffolded, and the class's paragraph only in its figures, given the
    other half, with `___` where the finding goes (`class_says`).

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
        rows = readme_rows(want_run_doc(args), strategies)
        bold = [st for st in strategies
                if rows.get(st, ('', '', '', ''))[1] == 'bold']
        print()
        print("**Per shape, in the run's shape order (%s):**"
              % ', '.join(shapes))
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
        rows, lst, partial = cross_half_rows(cells, shapes, strategies,
                                             args.compare, args.main, meta)
        if rows:
            # The same convention as the intro's, or the two part on the
            # one class that has degenerate arms: reshape1's installed
            # line read 1.1441 over all 49 while the intro read 1.0928
            # over the 46 voting. Worded conditionally so a class with
            # none keeps its exact installed text. 2026-09-01.
            vote = [r for r in rows if r[1] not in partial] or rows
            lo = min(vote)
            hi = max(vote)
            below = sum(1 for g, _ in vote if g < 1)
            print()
            print('**Across the halves:** %d of the %d%s arms are faster'
                  ' on this half and %d'
                  % (below, len(vote), ' voting' if partial else '',
                     len(vote) - below))
            print('slower, at a geomean of %.4f, from `%s` at %.4f to `%s`'
                  ' at %.4f,' % (geomean([g for g, _ in vote]), lo[1], lo[0],
                                 hi[1], hi[0]))
            if partial:
                print('%s sitting out as degenerate, a basis cell of'
                      ' theirs not left positive by the correction,'
                      % ', '.join('`%s`' % a for a in sorted(partial)))
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
    if getattr(args, 'compare', None):
        class_says(cells, shapes, strategies, meta, args)


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


# An address of three hex digits or more is a figure too, since 2026-09-04:
# the pinning claim's readings are written as addresses, mod-64 offsets and
# constants, and a cross-run series of them sat in the run chapter, a
# section no replace-list bullet linked, invisible to the coverage check
# that exists to find exactly that. Case:
# `coverage-check-sees-an-address-as-a-figure`.
FIGURE_RE = re.compile(r'\b0\.\d{3}\b|\d+\.\d+\s*[x]\b'
                       r'|\b\d{1,2}\.\d%|\b\d+\.\d{2,}\b'
                       r'|\b0x[0-9a-f]{3,}\b')

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

# THE MODE WHOSE SORTED OUTPUT SETTLES A SUPERLATIVE, by what the sentence
# is about, the first that matches: a sentence about pairs parting in sign
# is --winsor's census, about a floor --floor-pairs's, about movement
# --movers's, about counts --counts's, about classes or populations
# --cross-classes's, and about shapes or cells a sort of --cells. Named
# beside each hit since 2026-09-17: Run 34's quantifiers kept reaching its
# checker and probe unsorted, each settled at last by one mode's output.
SETTLE_BY = [(re.compile(p, re.I), mode) for p, mode in (
    (r'\bpart(?:s|ed|ing)? in sign\b|\bcapped\b|\bwinsori', '--winsor'),
    (r'\bfloors?\b|\bA/A\b', '--floor-pairs'),
    (r'\bmov(?:e|es|ed|er|ers|ing)\b', '--compare --movers'),
    (r'\bcounts?\b|\binstructions?\b', '--compare --counts'),
    (r'\bclass(?:es)?\b|\bpopulations?\b', '--cross-classes'),
    (r'\bshapes?\b|\bcells?\b|\bviews?\b', '--cells, sorted'))]


def settling_mode(line):
    """The mode `SETTLE_BY` names for a superlative's sentence.

    The SENTENCE carrying the hit's first superlative and not the hit, one
    mode a line of the sweep: a hit is a whole unwrapped paragraph, and
    keyed on that, a paragraph naming a floor anywhere sent its every
    superlative to --floor-pairs -- ninety-three of the live documents'
    hundred and seventy-three when this was first run.
    """
    at = min((m.start() for rx in SUPERLATIVE_RE for m in [rx.search(line)]
              if m), default=0)
    start = max(line.rfind('. ', 0, at) + 1, 0)
    end = line.find('. ', at)
    sentence = line[start:end if end >= 0 else len(line)]
    return next((mode for rx, mode in SETTLE_BY if rx.search(sentence)),
                '--compare or --pair --per-shape, sorted')


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
                       r'|machine|steps|alloc)(?![\w-])')


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
                # A `why:` POINTER IS NOT A BURIED ACTION. It names the
                # paragraph behind its step, to be fetched when the step
                # surprises you -- so it is deliberately a comment and
                # deliberately not a line of the sequence, which is the
                # one thing this sweep asks a hit to become. Added with
                # the pointers on 2026-09-01, before twenty-eight of them
                # could teach a reader to skip this worklist.
                if "why: --para '" in l:
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
# copy -- the run chapter is replaced every run and the run file keeps
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


RUNS_DIR = 'runs'
RUN_DOC_RE = re.compile(r'^run(\d+)\.md$')


def run_docs(here=None):
    """Every `runs/run<N>.md` as (N, path), newest run first.

    ONE FILE PER RUN, and the number in the file name and in no heading:
    the run file's sections are `Results`, `What the next run compares
    against`, `The properties the next run should test` and `The stride
    classes, run by run`, none of which carries a numeral, so a write-up
    makes a file and renames one heading -- `Recommended tasks after Run
    N`, which is the open list's and stays in README.md. Four renames were
    what step 5 used to be, and Run 9 left eleven dead anchors doing them.

    The directory accumulates, which is what gives the checks two files to
    compare: a paragraph a run left standing is one identical in the file
    beside it, where it used to be identity against `git show HEAD:` --
    a comparison that said nothing at all once the write-up was committed.
    """
    at = here or os.path.dirname(os.path.abspath(__file__))
    out = []
    try:
        names = os.listdir(os.path.join(at, RUNS_DIR))
    except OSError:
        return []
    for name in names:
        m = RUN_DOC_RE.match(name)
        if m:
            out.append((int(m.group(1)), os.path.join(at, RUNS_DIR, name)))
    return sorted(out, reverse=True)


def current_run_doc(here=None):
    """The file every table and every class block is installed into."""
    docs = run_docs(here)
    return docs[0][1] if docs else None


def _agree_unit(x):
    """A captured figure as the agreement report prints it.

    Every rule in that table read a PERCENTAGE until 2026-09-14, so the
    report appended `%` to whatever it captured -- and the log-count rule
    landed that day capturing the spelled word, which printed as
    `fourteen%`. The unit belongs to the capture and not to the report.
    """
    return '%s%%' % x if re.fullmatch(r'[\d.]+', x) else x


def previous_run_doc(run_doc):
    """The run before `run_doc`, in whatever directory that one sits in.

    Beside it rather than in this script's own `runs/`, so that `--run-doc`
    aims the comparison as it aims everything else: a caller pointing at a
    copy is asking about the copy's neighbours, and answering out of the
    live directory would hold a fixture to the real previous run.
    """
    now = run_no_of(run_doc)
    if now is None:
        return None
    at = os.path.dirname(os.path.abspath(run_doc))
    best = None
    try:
        names = os.listdir(at)
    except OSError:
        return None
    for name in names:
        m = RUN_DOC_RE.match(name)
        if m and int(m.group(1)) < now and (best is None
                                            or int(m.group(1)) > best[0]):
            best = (int(m.group(1)), os.path.join(at, name))
    return best[1] if best else None


INHERITED_RE = re.compile(r'this run|this pair|Run \d+')


def doc_paragraphs_text(text):
    """A document's blank-line paragraphs, each joined to one line.

    Joined so that the comparison below does not turn on where the wrap
    fell: two runs' files sit at the same fixed point today, and a
    document that moved between them would otherwise read as wholly new.

    Split from `doc_paragraphs` 2026-09-18 so that `--stale` can read the
    step-5 copy out of git, which is a string and not a path; one
    implementation, or the two readings would part on the joining.
    """
    out, cur = [], []
    for line in text.split('\n'):
        if line.strip():
            cur.append(line)
        elif cur:
            out.append(' '.join(cur))
            cur = []
    if cur:
        out.append(' '.join(cur))
    return out


def doc_paragraphs(path):
    """The same, off a path."""
    with open(path, encoding='utf-8') as h:
        return doc_paragraphs_text(h.read())


def inherited(run_doc, prev_doc, both=False):
    """The paragraphs this run's file carried whole from the last one.

    Step 5 copies the previous run's file and the write-up edits the copy,
    so the checker's diff base IS that copy: a paragraph the write-up
    changed shows up in the diff, and one it left alone appears nowhere at
    all. That is the run file's characteristic defect and it is invisible
    to both passes by construction -- Run 27 shipped nine such paragraphs
    past them, its comprehension probe found those by reading the document
    whole, and two survived even that, one comparing the run to the run
    before the previous one and one dating its own tables to four days
    before the evening.

    So this is the probe's reading, mechanised: identical text, kept where
    it says `this run` or `this pair` or names a run, which is what parts
    the standing apparatus a run file re-carries every time from a claim
    about the run in front of it. On Run 27's own write-up at step 6b
    this names 39 of the 62 paragraphs carried whole and every one of
    the five later found stale is among them -- 62 and not the 123 a
    first measurement counted, that one having taken a LINE for a
    paragraph where this joins a blank-line block into one. It PRINTS
    and never refuses: which of them is a claim is a reading, and a
    gate that fired on the
    apparatus would be turned off by the second run.
    """
    if not prev_doc:
        sys.stderr.write('--inherited: no earlier run file beside %s, so'
                         ' there is nothing to compare it with and this'
                         ' reading did not happen\n'
                         % os.path.basename(run_doc))
        return 2
    before = set(doc_paragraphs(prev_doc))
    now = doc_paragraphs(run_doc)
    carried = [p for p in now if p in before and INHERITED_RE.search(p)]
    same = len([p for p in now if p in before])
    print('%d paragraph(s) carried whole from %s that name a run or call'
          ' themselves this run\'s, out of %d identical in all:'
          % (len(carried), os.path.basename(prev_doc), same))
    # HOW LATE THIS READING IS, said rather than left to be noticed. The
    # step asks for it BEFORE the first paragraph, because after the
    # prose is written every hit below is a rewrite; run late it still
    # finds them and costs more to act on. No threshold: the number is
    # the statement, and a session that means to run it early sees a
    # small one. Run 37 ran it with most of the write-up already
    # written and rewrote six of its hits.
    print('   %d of %d paragraph(s) already differ from %s, so this is'
          ' being read after that much of the write-up -- each hit below'
          ' is a rewrite rather than a draft, and the step asks for it'
          ' before the first paragraph.'
          % (len(now) - same, len(now), os.path.basename(prev_doc)))
    for p in carried:
        # The LEAD and the TRIGGER, because the stale clause is rarely
        # the opening: this mode's own non-vacuity check was misread once
        # by grepping a truncated print for a phrase that sat mid-
        # paragraph. Two lines a paragraph is what a worklist of forty
        # costs, and the paragraph itself is `--para`'s to print.
        m = INHERITED_RE.search(p)
        print('  %s' % (p[:110] + (' ...' if len(p) > 110 else '')))
        print('      names: ...%s...'
              % p[max(0, m.start() - 45):m.end() + 45])
    print('Each is either the apparatus every run re-carries or last run\'s'
          ' claim standing under this run\'s name, and only reading says'
          ' which. The diff cannot: its base is the copy.')
    # THE OTHER HALF, added 2026-09-16: a paragraph the write-up CHANGED
    # that still names the previous run. The carried half above is what a
    # diff cannot see at all; this is what a diff shows and a reader
    # skims past, because the line that changed looks like the work being
    # done. Run 33's floor paragraph had its lead rewritten for the run
    # and its body left as Run 32's -- carriers, closed thresholds, wild
    # cells, a registration number and a fifteen-run series, every one of
    # them that run's -- and its class-property entry had an updated head
    # over an un-updated tail that contradicted it. Both were in the diff
    # and both survived a checker pass that read that diff; what found
    # them was the second pass reading the finished document.
    # It PRINTS and never refuses, as the half above does: naming the
    # previous run in a changed paragraph is ordinary -- a delta bullet,
    # a comparison, a series -- so the reading is which of them is a
    # claim left standing rather than a claim made.
    # THE SECOND LIST IS BEHIND --all SINCE 2026-09-18, and the reason is
    # the ratio the two printed on Run 35: SIX paragraphs carried whole,
    # of which one was stale, against THIRTY-SEVEN changed ones naming the
    # previous run, of which none was -- naming it being what a delta
    # bullet, a comparison and a series all do. A reading whose signal is
    # a sixth of its output is one a session skims, and this mode's whole
    # purpose is the class of defect no other pass can see. The list is
    # kept, not cut: Run 33's floor paragraph was in it.
    prev_n = run_no_of(prev_doc) if both else None
    if prev_n is not None:
        pat = re.compile(r'\bRun %d\b' % prev_n)
        touched = [p for p in doc_paragraphs(run_doc)
                   if p not in before and pat.search(p)]
        print('\n%d paragraph(s) this run CHANGED that still name Run %d,'
              ' out of %d changed in all:'
              % (len(touched), prev_n,
                 len([p for p in doc_paragraphs(run_doc)
                      if p not in before])))
        for p in touched:
            m = pat.search(p)
            print('  %s' % (p[:110] + (' ...' if len(p) > 110 else '')))
            print('      names: ...%s...'
                  % p[max(0, m.start() - 45):m.end() + 45])
        print('A lead rewritten over a body left alone reads as done and'
              ' is in the diff, which is why both checker passes can pass'
              ' it. Read each: is Run %d the subject, or the leftover?'
              % prev_n)
    return 0


# A MEASURED FIGURE, which is what the default view leads with: a decimal, a
# percentage, an integer of two digits or more, or a WORD numeral from ten
# up. The words were excluded until 2026-09-18 and the exclusion made this
# mode's own justification false: of the four figures Run 35 shipped stale,
# `thirty-four` rows and `ten` consumers are words, so two of the four sat
# in the bucket only --all prints while the docstring said the mode printed
# them. `one` to `nine` stay out, being ordinary prose rather than a figure
# a run moves -- which is the distinction the first draft was reaching for
# and drew in the wrong place.
MEASURED_RE = re.compile(
    r'^(?:\d+\.\d+%?|\d\d+%?|\d+%|ten|eleven|twelve|thirteen|fourteen'
    r'|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty'
    r'|fifty|sixty|seventy|eighty|ninety|hundred|thousand)$', re.I)

NUMERAL_RE = re.compile(
    r'\b(?:\d+(?:\.\d+)?%?|one|two|three|four|five|six|seven|eight|nine|ten'
    r'|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen'
    r'|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety'
    r'|hundred|thousand)\b', re.I)


def step5_copy(path, mode):
    """A document as step 5's commit added it, with that commit's hash.

    THE ROOT COMES FROM GIT AND NOT FROM THE PATH: `git show COMMIT:PATH`
    resolves its path from the repository root whatever `-C` says, so a
    root guessed by climbing two directories reads every blob as absent
    and the caller reports itself as not having run -- which is what
    `--stale` did when first written.

    Returns `(repo, rel, sha, text)`, or the exit status the caller owes: 2,
    since a reading that could not resolve its base did not happen. Shared
    by `--stale` and `--lost`, which read the same commit for different
    questions -- a figure that survived an edit, and a paragraph that
    survived nothing.
    """
    try:
        repo = subprocess.run(['git', '-C',
                               os.path.dirname(os.path.abspath(path)),
                               'rev-parse', '--show-toplevel'],
                              capture_output=True, text=True,
                              check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        sys.stderr.write('%s: %s is not inside a git checkout, so there is'
                         ' no step-5 copy to read it against and this'
                         ' reading did not happen\n' % (mode, path))
        return 2
    rel = os.path.relpath(os.path.abspath(path), repo)
    try:
        adds = subprocess.run(['git', '-C', repo, 'log', '--format=%H',
                               '--diff-filter=A', '--', rel],
                              capture_output=True, text=True, check=True)
        first = adds.stdout.split()[-1]
        copy = subprocess.run(['git', '-C', repo, 'show',
                               '%s:%s' % (first, rel)],
                              capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, IndexError, FileNotFoundError,
            OSError):
        sys.stderr.write('%s: %s has no commit that ADDED it, so there is'
                         ' no step-5 copy to read it against and this'
                         ' reading did not happen\n' % (mode, rel))
        return 2
    return repo, rel, first, copy.stdout


def lost_paragraphs(run_doc, ratio=0.45):
    """Paragraphs step 5's copy had that this tree has no counterpart for.

    THE ONLY READING THAT SEES A DELETION. Every gate here is a predicate
    over what is PRESENT -- a link that resolves, a figure that agrees, a
    heading spaced -- so a paragraph removed by a scripted edit leaves its
    neighbours joining seamlessly and passes all of them. Post-run step 6e
    asks for this comparison and supplied no tool, so every run hand-rolls
    it; Run 38 did, in a script it wrote twice.

    BOTH DOCUMENTS, against ONE commit: the run file's own step-5 copy.
    README's first commit is years back and is not this run's base, so it
    is read at the sha that ADDED the run file, which is what 6e means by
    `step 5's copy`.

    A rewritten paragraph is not a lost one, so the test is similarity and
    not identity: a base paragraph with no survivor above `ratio` is
    reported, and a lead rewritten around the same body is not. Tables,
    code and link definitions are skipped, being installed or mechanical.
    """
    got = step5_copy(run_doc, '--lost')
    if isinstance(got, int):
        return got
    repo, rel, sha, run_copy = got
    readme = os.path.join(os.path.dirname(os.path.abspath(run_doc)),
                          '..', 'README.md')
    readme = os.path.normpath(readme)
    pairs = [(rel, run_copy, run_doc)]
    if os.path.exists(readme):
        rrel = os.path.relpath(readme, repo)
        try:
            base = subprocess.run(['git', '-C', repo, 'show',
                                   '%s:%s' % (sha, rrel)],
                                  capture_output=True, text=True,
                                  check=True).stdout
            pairs.append((rrel, base, readme))
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            sys.stderr.write('--lost: %s is not in %s, so only the run file'
                             ' was read\n' % (rrel, sha[:7]))
    skip = ('|', '#', '[', '    ')
    print('--lost: both documents against step 5\'s copy at %s' % sha[:7])
    total = 0
    for name, base_text, path in pairs:
        before = [p for p in doc_paragraphs_text(base_text)
                  if not p.startswith(skip)]
        now = [p for p in doc_paragraphs(path) if not p.startswith(skip)]
        gone = []
        # A WORD-SET PRE-FILTER, precomputed once. Two paragraphs sharing
        # few words share few characters in order, so this drops most
        # pairs before any matching. It is a heuristic where the length
        # bound below is exact, and it is safe in the one direction that
        # matters: dropping a true counterpart ADDS a candidate to the
        # listing and can never hide a paragraph that went, which the
        # count catches regardless.
        words = {t: set(t.lower().split()) for t in set(before) | set(now)}
        now_set = set(now)
        for q in before:
            # AN UNCHANGED PARAGRAPH IS ITS OWN COUNTERPART, and most of
            # README's are: the membership test settles them before any
            # matching runs, where the loop below would scan the whole
            # document to rediscover an identity.
            if q in now_set:
                continue
            best, wq = 0.0, words[q]
            for r in now:
                wr = words[r]
                if not wq or not wr:
                    continue
                if len(wq & wr) / min(len(wq), len(wr)) < 0.25:
                    continue
                # AN EXACT BOUND BEFORE ANY MATCHING: the ratio is
                # 2M/T with M at most the shorter length, so two
                # paragraphs of very different lengths cannot reach the
                # threshold whatever they share. Skipping those took this
                # mode from two and a half minutes to seconds over the
                # README's five hundred paragraphs.
                if 2.0 * min(len(q), len(r)) / (len(q) + len(r)) < ratio:
                    continue
                m = difflib.SequenceMatcher(None, q, r)
                # QUICK_RATIO IS AN UPPER BOUND AND NOT THE SIMILARITY: it
                # compares character multisets, so two unrelated English
                # paragraphs of a length clear any threshold worth using.
                # It is a pre-filter here and the real ratio decides --
                # written the other way first, the case's deleted
                # paragraph found a `counterpart` it shares no sentence
                # with and the mode reported nothing lost.
                if m.quick_ratio() < ratio:
                    continue
                sim = m.ratio()
                if sim > best:
                    best = sim
                    if best >= ratio:
                        break
            if best < ratio:
                gone.append((best, q))
        # THE COUNT IS THE CHECK AND THE LISTING IS CANDIDATES. A
        # write-up REPLACES paragraphs wholesale -- post-run step 6a asks
        # for exactly that, from the reader's output and not by editing
        # the copy -- so a low similarity is the ordinary case in a run
        # file and says nothing on its own. What a deletion cannot hide
        # from is the count.
        went = len(before) - len(now)
        if went > 0:
            total += went
            print('  %s: %d paragraph(s) then, %d now -- %d WENT BY COUNT,'
                  ' which is a loss and not a rewrite'
                  % (name, len(before), len(now), went))
        else:
            print('  %s: %d paragraph(s) then, %d now -- none went by count'
                  % (name, len(before), len(now)))
        print('    %d with no close counterpart, which in a run file is'
              ' mostly the write-up replacing paragraphs as 6a asks:'
              % len(gone))
        for best, q in gone[:10]:
            print('      %.2f alike at best: %s' % (best, q[:92]))
        if len(gone) > 10:
            print('      ... and %d more' % (len(gone) - 10))
    if not total:
        print('  no paragraph went by count in either document')
    return 0


def stale_figures(run_doc, ratio=0.55, verbose=False):
    """Figures a write-up left where the PREVIOUS run put them.

    Step 5 copies the last run's file and the write-up edits that copy, so
    the run file's characteristic defect is a paragraph whose prose was
    rewritten around numbers that were not. `--inherited` catches the
    paragraph nobody touched; this catches the one that WAS touched and
    kept a figure, which neither checker pass can see either: their base is
    the copy, so an edited paragraph shows as changed and a numeral that
    survived inside it shows as context.

    Run 35 is the measurement. Its write-up shipped four such figures past
    both mechanical gates and a figure-checking agent: a floor pair left at
    the previous run's 0.51% and 0.49%, a row count left at thirty-four, a
    reference run left at 33, and a consumer count left at ten. Every one
    is a numeral the paragraph shares with its counterpart in the copy.

    WORD NUMERALS COUNT, two of those four being words. The counterpart is
    found by similarity over the whole paragraph rather than by its lead,
    because a write-up rewrites leads: matching on the lead would have
    missed the row count, whose lead is where its edit fell.

    It PRINTS and never refuses. A surviving numeral is ordinary -- the
    shape count, the pair count, a threshold the run did not move -- so the
    reading is which of them the run moved and the prose did not, and a
    gate on it would be turned off by the second run.
    """
    got = step5_copy(run_doc, '--stale')
    if isinstance(got, int):
        return got
    _repo, rel, first, copy_text = got
    skip = ('|', '#', '[', '    ')
    # THE INSTALLED PARAGRAPHS CANNOT BE STALE BY HAND, so they are not
    # read here: `--block --in-place` rewrites a class block's Controls,
    # Provenance, per-shape and cross-half lines whole every run, and
    # `--fingerprint` its table. A figure surviving in one of those is the
    # installer's doing and not a write-up's, and they are half of what a
    # first draft of this mode printed.
    installed = ('**Controls:**', '**Provenance:**', '**Per shape,',
                 '**Across the halves:**')
    before = [p for p in doc_paragraphs_text(copy_text)
              if not p.startswith(skip)]
    now = doc_paragraphs(run_doc)
    same = set(doc_paragraphs_text(copy_text))
    print('--stale: %s against its step-5 copy at %s' % (rel, first[:7]))
    found, rows = 0, []
    for p in now:
        if p in same or p.startswith(skip) or p.startswith(installed):
            continue
        best, score = None, 0.0
        for q in before:
            m = difflib.SequenceMatcher(None, p, q)
            if m.quick_ratio() < ratio:
                continue
            r = m.ratio()
            if r > score:
                best, score = q, r
        if best is None or score < ratio:
            continue
        kept = [n for n in dict.fromkeys(NUMERAL_RE.findall(p))
                if re.search(r'\b%s\b' % re.escape(n), best, re.I)]
        if not kept:
            continue
        # TWO TIERS, because the first draft printed sixty-two paragraphs
        # and its four real findings sat among four hundred ordinary
        # numerals -- `two`, `one`, a shape count, a cache line. A
        # MEASURED figure is a decimal, a percentage, an integer of two
        # digits or more, or a word numeral from ten up -- the shape of a
        # figure a run moves, where `one` to `nine` are ordinary prose;
        # those lead. MEASURED_RE above carries the rule and why.
        # The rest are counted and listed only under --all, so nothing is
        # hidden without saying so.
        measured = [n for n in kept if MEASURED_RE.match(n)]
        rows.append((score, p, kept, measured))
    # MOST-EDITED FIRST, and that ordering is the reading: a paragraph
    # 98% identical to the copy has barely been touched and its numerals
    # are expected to stand, while one rewritten by half that kept a
    # decimal is the shape of the defect -- a lead rewritten over a body
    # left alone.
    rows.sort(key=lambda r: r[0])
    quiet_only, over = 0, 0
    LIMIT = 20
    for score, p, kept, measured in rows:
        if not measured and not verbose:
            quiet_only += 1
            continue
        if found >= LIMIT and not verbose:
            over += 1
            continue
        found += 1
        print('  %s' % (p[:100] + (' ...' if len(p) > 100 else '')))
        show = measured or kept
        print('      kept from the copy (%d%% alike): %s'
              % (round(score * 100), ', '.join(show[:12])
                 + (' ...' if len(show) > 12 else '')))
    print('%d edited paragraph(s) keep a MEASURED figure the copy also'
          ' carries -- a decimal, a percentage, a two-digit count or a'
          ' word from ten up. Each is'
          ' a threshold this run did not move, or last run\'s number under'
          ' this run\'s prose --- only reading says which.' % found)
    if over:
        print('%d further paragraph(s) beyond the twenty most edited; --all'
              ' prints them.' % over)
    if quiet_only:
        print('%d more keep only a single digit or a word under ten;'
              ' --all lists them.'
              % quiet_only)
    return 0

BRIEF = 'checker-brief.txt'


def _brief_substitutions(run, where='.'):
    """RUN, BASIS, OTHER, PREV and the previous run's two half names.

    Every driver reads the halves through `pair-halves.sh`, so this does
    too rather than parsing the note a second way; PREV comes from the same
    call's COMPARE, and PREVBASIS/PREVSAME are that run's basis half read
    out of ITS note. Returns {} when the note cannot be read, so the caller
    says the block was not written instead of writing a guess.
    """
    def halves(name):
        try:
            out = subprocess.run([os.path.join(where, 'pair-halves.sh'), name],
                                 capture_output=True, text=True, check=True,
                                 cwd=where).stdout
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            return {}
        return dict(kv.split('=', 1) for kv in
                    (p_.strip() for p_ in out.strip().split(';')) if '=' in kv)
    mine = halves(run)
    if not mine.get('BASIS'):
        return {}
    subs = {'RUN': run, 'BASIS': mine['BASIS'], 'OTHER': mine.get('OTHER', '')}
    prev = mine.get('COMPARE')
    if prev:
        subs['PREV'] = prev
        theirs = halves(prev)
        if theirs.get('BASIS'):
            subs['PREVBASIS'] = '%s-%s' % (prev, theirs['BASIS'])
            subs['PREVSAME'] = '%s-%s' % (prev, theirs['BASIS'])
    return subs


def _brief_tips(run, where='.'):
    """PRETIP and RUNTIP as CANDIDATES. They are still not written.

    The refusal above is right and stays -- a wrong tip silently rescopes
    a pass's diff, so the run decides them -- but a session that has to
    reverse-engineer them from the brief's own diff commands sets them
    from memory instead, which is the worse failure. Run 37 did exactly
    that. So git is asked, and the answer is printed beside the write for
    a person to accept or refuse: the commit that ADDED the run file,
    which is step 5's copy, and the newest commit whose subject names
    this run and a step, which is what 6d leaves behind. An empty string
    where git cannot say, never a guess.
    """
    def git(*args):
        try:
            done = subprocess.run(('git', '-C', where) + args,
                                  capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            return ''
        return done.stdout.strip() if done.returncode == 0 else ''

    added = git('log', '--diff-filter=A', '--format=%h', '--',
                'runs/%s.md' % run)
    pre = added.split('\n')[-1] if added else ''
    want = re.compile(r'\bRun %s\b.*\bstep\b'
                      % re.escape(run[3:] if run.startswith('run') else run),
                      re.I)
    tip = ''
    for line in git('log', '--format=%h %s', '-40').split('\n'):
        if want.search(line):
            tip = line.split(' ', 1)[0]
            break
    return pre, tip


def brief_update(run, readings_dir=None, brief=None, where='.'):
    """Paste the run's own facts into the checker brief, rather than retype.

    The brief's two THIS RUN ONLY items are the half of it that goes stale,
    and a stale brief looks exactly like a used one: both checker passes
    read it as given and neither can tell that its figures are the run
    before's. `read-all.sh --brief-facts` already writes them paste-ready
    into `log-read-<run>/for-brief.txt`, under a marker saying so, and the
    chapter already says to paste rather than retype -- which leaves the
    pasting itself as the one step nothing checks.

    So this does the paste: the two items, and the substitution block's
    RUN, BASIS, OTHER, PREV, PREVBASIS and PREVSAME, which come off the
    pair note through `pair-halves.sh` and off the note's COMPARE line.
    PRETIP and RUNTIP are NOT written here -- they are commits, the run
    decides them, and a wrong one silently rescopes a pass's diff.

    The `<yours>` slots the facts file leaves -- the pair's variable and
    the run's largest finding -- are carried across untouched and counted
    on stdout beside the write, so an unfilled brief is loud rather than
    plausible. Stdout and not stderr: a refusal is stderr's and this is a
    report on a write that happened.
    """
    # BOTH PATHS ARE RESOLVED UNDER `where`, which is the directory the
    # run's artifacts and its brief sit in and defaults to the working
    # one. A case runs this against a fixture elsewhere, and with the
    # paths hard-wired relative to the cwd both of its cases took the
    # missing-directory branch -- the refusal one PASSING for the wrong
    # reason, which is a case proving nothing while reading green.
    d = readings_dir or os.path.join(where, 'log-read-%s' % run)
    brief = brief or os.path.join(where, BRIEF)
    facts = os.path.join(d, 'for-brief.txt')
    if not os.path.exists(facts):
        sys.stderr.write('--brief-update: no %s, which post-run-readings.sh'
                         ' writes LAST, so there is nothing to paste and the'
                         ' brief is untouched\n' % facts)
        return 2
    if not os.path.exists(brief):
        sys.stderr.write('--brief-update: no %s here\n' % brief)
        return 2
    text = open(facts, encoding='utf-8').read()
    marker = 'paste over checker-brief.txt items 5 and 6'
    if marker not in text:
        sys.stderr.write('--brief-update: %s carries no `%s` marker, so the'
                         ' items it holds cannot be told from the rest of'
                         ' it; the brief is untouched\n' % (facts, marker))
        return 2
    tail = text.split(marker, 1)[1].split('\n', 1)[1]
    items = {}
    cur = None
    for line in tail.split('\n'):
        m = re.match(r' ([56])\. ', line)
        if m:
            cur = m.group(1)
            items[cur] = [line]
        elif cur and (line.startswith('    ') or not line.strip()):
            items[cur].append(line)
        elif cur:
            cur = None
    if sorted(items) != ['5', '6']:
        sys.stderr.write('--brief-update: %s holds item(s) %s after its'
                         ' marker, not 5 and 6; the brief is untouched\n'
                         % (facts, ', '.join(sorted(items)) or 'none'))
        return 2
    out, wrote, n = [], set(), 0
    was = open(brief, encoding='utf-8').read().count('<yours')
    # AN ITEM IS ITS HEADER AND ITS INDENTED BODY, and both go: replacing
    # the header line alone left the old body under the new item, so from
    # Run 36 to Run 39 the brief carried every run's items one under
    # another, found by Run 39's first checker pass. Case:
    # `brief-update-replaces-each-item-whole`.
    skipping = False
    for line in open(brief, encoding='utf-8').read().split('\n'):
        if skipping and line.startswith('    '):
            continue
        skipping = False
        m = re.match(r' ([56])\. THIS RUN ONLY', line)
        if m:
            block = '\n'.join(items[m.group(1)]).rstrip('\n')
            out.append(block)
            wrote.add(m.group(1))
            n += 1
            skipping = True
            continue
        out.append(line)
    if wrote != {'5', '6'}:
        sys.stderr.write('--brief-update: %s has no ` 5. THIS RUN ONLY` and'
                         ' ` 6. THIS RUN ONLY` line to replace (found %s);'
                         ' the brief is untouched\n'
                         % (brief, ', '.join(sorted(wrote)) or 'neither'))
        return 2
    # THE SUBSTITUTION BLOCK TOO, which the docstring promised and the code
    # did not write until 2026-09-18 -- found by re-opening the claim rather
    # than by any gate, the mode's output having matched its code and not
    # its purpose. Its values come from `pair-halves.sh`, which is where
    # every driver gets them, and from the previous run's own note; PRETIP
    # and RUNTIP are NOT written, being commits the run decides.
    subs = _brief_substitutions(run, where)
    if subs:
        for i, line in enumerate(out):
            for key, val in subs.items():
                if re.match(r'\s*%s=' % key, line) or (
                        key in line and '=' in line):
                    line = re.sub(r'\b%s=\S+' % key, '%s=%s' % (key, val),
                                  line)
            out[i] = line
    # THE PASTE IS NOT IDEMPOTENT, and until 2026-09-20 it did not say so.
    # It re-pastes items 5 and 6 from the facts file, whose `<yours>` slots
    # come back empty -- so a second run over a brief whose prose was
    # written DISCARDS that prose, silently, and the only sign is the slot
    # count below going up. Run 37 filled the two, ran this again while
    # testing something else, and found the loss by reading its own diff.
    # Refusing is wrong: the numbers above it do want re-pasting when a
    # reading is retaken. Saying so is enough, and git holds what went.
    now = sum(line.count('<yours') for line in out)
    open(brief, 'w', encoding='utf-8').write('\n'.join(out))
    print('--brief-update: %s items 5 and 6 written from %s' % (brief, facts))
    if now > was:
        print('AND IT RE-OPENED %d SLOT(S) THAT WERE FILLED: this paste'
              ' brings the facts file\'s empty `<yours>` back over prose'
              ' that stood there. What it overwrote is in git --'
              ' `git diff -- %s` -- and is yours to write back.'
              % (now - was, os.path.basename(brief)))
    if subs:
        print('and the substitution block: %s. PRETIP and RUNTIP are'
              ' untouched, being commits.'
              % ', '.join('%s=%s' % kv for kv in sorted(subs.items())))
    else:
        print('the substitution block was NOT written: pair-halves.sh could'
              ' not read %s-pair.txt, so RUN, BASIS, OTHER and PREV stand as'
              ' they were and are yours to check.' % run)
    # AFTER that pair and not inside it: inserted between the `if subs`
    # and its `else` on 2026-09-20, this took the `else` over, so a run
    # with no substitutions but a tip to offer printed no warning, and
    # one with both printed the warning beside the block it denies.
    # Found by a blind reader of the diff, no gate seeing it.
    pre, tip = _brief_tips(run, where)
    if pre or tip:
        print('and git offers them, to accept or refuse rather than to'
              ' reverse-engineer: PRETIP=%s, the commit that ADDED'
              ' runs/%s.md and so step 5\'s copy; RUNTIP=%s, the newest'
              ' commit whose subject names this run and a step, which'
              ' at 6e is 6d\'s. Neither is written.'
              % (pre or '?', run, tip or '?'))
    left = sum(1 for line in out for _ in re.finditer(r'<yours', line))
    if left:
        print('%d `<yours>` slot(s) left, which are prose and not facts:'
              ' the pair\'s variable and the run\'s largest finding. A brief'
              ' handed to a checker with one standing is a brief that says'
              ' less than it looks like.' % left)
    return 0

def prose_facts(run, readings_dir=None):
    """The figures a write-up quotes, gathered from the readings already taken.

    `post-run-readings.sh` writes some two hundred and seventy files into
    `log-read-<run>/`, and the write-up quotes perhaps eighty figures out of
    them. Run 35 spent about a third of its write-up's tokens finding those
    eighty by grep, and several of its defects were transcription between a
    reading file and a sentence -- a floor pair quoted at the previous run's
    figures, a consumer count off by one, a depth ranked against the wrong
    population.

    So this reads those files rather than the JSONs: one labelled sheet, per
    population and per half, of the figures the prose actually uses. It
    derives no figure of its own: each is grabbed verbatim out of a
    reading file and only the span tally is counted here. A figure here
    that disagrees with a reading file is
    this mode's bug; a figure here that disagrees with the JSONs is that
    reading file's, and `--compare` is where it is settled.

    What it does NOT gather is the box-and-window half -- the plateau, the
    windows, the intrusion verdict, the md5s -- which `read-all.sh
    --brief-facts` already writes whole into `for-brief.txt` beside these
    files, and which this names rather than copies.
    """
    d = readings_dir or 'log-read-%s' % run
    if not os.path.isdir(d):
        sys.stderr.write('--prose-facts: no %s/, which post-run-readings.sh'
                         ' writes; nothing was gathered\n' % d)
        return 2
    halves = sorted({os.path.basename(f).split('-')[-2]
                     for f in glob.glob(os.path.join(d, '*-compare.txt'))})
    pops, rows = [], []
    for f in sorted(glob.glob(os.path.join(d, '*-counts-cmp.txt'))):
        pops.append(os.path.basename(f)[:-len('-counts-cmp.txt')])
    for pop in pops:
        counts = _grab(os.path.join(d, '%s-counts-cmp.txt' % pop),
                       r'corrected time: ([\d.]+)')
        for half in halves:
            cmpf = os.path.join(d, '%s-%s-compare.txt' % (pop, half))
            if not os.path.exists(cmpf):
                continue
            bar = _grab(cmpf, r'A/A bar for this comparison ([\d.]+%)')
            clear = _grab(cmpf, r'(\d+) of \d+ non-control arm\(s\) move'
                                r' further than the bar')
            rows.append((pop, half, bar, clear, counts))
    print('prose facts for %s, gathered from %s/ and deriving no figure'
          ' of its own'
          % (run, d))
    print('\n%-10s %-11s %-9s %-7s %s'
          % ('population', 'half', 'A/A bar', 'clear', 'counts geomean'))
    for pop, half, bar, clear, counts in rows:
        print('%-10s %-11s %-9s %-7s %s'
              % (pop, half, bar or '--', clear or '--', counts or '--'))
    print('\nthe registration, span by span, in scope only:')
    seen = 0
    for f in sorted(glob.glob(os.path.join(d, '*-pred.txt'))):
        pop = os.path.basename(f)[:-len('-pred.txt')]
        for line in open(f, encoding='utf-8'):
            if not line.startswith('  (') or 'out of scope' in line:
                continue
            seen += 1
            verdict = 'KILLED' if 'KILLED' in line else (
                'HELD' if 'HELD' in line else '?')
            item = line.strip()[:3]
            read = re.search(r'read ([\d.]+)|A - B up to (-?\d+)', line)
            print('  %-22s %-4s %-7s %s'
                  % (pop, item, verdict,
                     (read.group(1) or read.group(2)) if read else ''))
    print('%d span reading(s) in scope. The box-and-window facts --- the'
          ' plateau, the windows, the intrusion verdict, the md5s, the'
          ' floors --- are in %s/for-brief.txt, written whole by'
          ' read-all.sh --brief-facts and not copied here.' % (seen, d))
    return 0


def _grab(path, pattern):
    """The first capture of `pattern` in `path`, or None."""
    try:
        text = open(path, encoding='utf-8').read()
    except OSError:
        return None
    m = re.search(pattern, text)
    return m.group(1) if m else None

def modes_table(path=None):
    """Every mode this reader dispatches on, read off its own source.

    Written because a one-line summary drifted and cost two runs the same
    hour: `--counts`'s help said *with --compare*, which is one of its two
    arities, and the other -- `--counts SWEEP.txt --pair A B`, the
    within-half instruction ratio -- was hand-rolled by Run 26's write-up
    and again by Run 27's, each time from that summary. A table written by
    hand would drift the same way, so nothing here is written: it is the
    `if` tests of `main` in the order the program reads them, each with
    what the branch calls. A flag with two dispatch sites therefore has
    two rows, which is the fact the summary could not carry.
    """
    tree = ast.parse(open(path or __file__, encoding='utf-8').read())
    fn = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef) and n.name == 'main'), None)
    if fn is None:
        sys.stderr.write('--modes: no `main` in %s, so the dispatch could'
                         ' not be read and this table is not it\n'
                         % (path or __file__))
        return 2
    print('the modes `main` dispatches on, in the order it reads them,'
          ' off this file\'s own source:')
    n = guards = 0
    for node in ast.walk(fn):
        if not isinstance(node, ast.If):
            continue
        named = sorted({a.attr for a in ast.walk(node.test)
                        if isinstance(a, ast.Attribute)
                        and isinstance(a.value, ast.Name)
                        and a.value.id == 'args'})
        if not named:
            continue
        # THE BODY AND NOT THE SUBTREE: `ast.walk` takes the `orelse`
        # with it, so the first test of an if/elif chain reported every
        # call the whole chain makes and the column read as a mode calling
        # eleven functions. A branch that names no function of this file
        # is a refusal rather than a mode, and is counted apart.
        calls = [c.func.id for b in node.body for c in ast.walk(b)
                 if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                 and c.func.id not in ('len', 'print', 'sorted', 'set',
                                       'list', 'str', 'int', 'sys')]
        if not calls:
            guards += 1
            continue
        n += 1
        print('  L%-6d %-46s -> %s'
              % (node.lineno, ast.unparse(node.test)[:46],
                 ', '.join(dict.fromkeys(calls))[:46]))
    print('%d dispatch site(s) and %d refusal(s) around them. A FLAG WITH'
          ' TWO ROWS HAS TWO ARITIES, and its own --help line names'
          ' whichever one was written down.' % (n, guards))
    return 0


def run_no_of(path):
    """The run number a run file's NAME carries, or None."""
    m = RUN_DOC_RE.match(os.path.basename(path or ''))
    return int(m.group(1)) if m else None




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

# The revision the freshness sweeps and the reworked-sections check read
# the committed copies from. HEAD until check_doc finds a run file, and
# then the commit that ADDED that file -- post-run step 5's verbatim copy
# -- so that "added by this diff" means added by this write-up: against
# HEAD every line of a committed write-up read as old, which is exactly
# when step 6e reads the worklists (Run 23, 2026-09-02).
BASE_REV = 'HEAD'


def base_rev_for(run_doc):
    """The commit that added `run_doc`, or None where git cannot say."""
    at = os.path.dirname(os.path.abspath(__file__))
    try:
        rel = os.path.relpath(os.path.abspath(run_doc), at)
        got = subprocess.run(['git', 'log', '--diff-filter=A', '-1',
                              '--format=%H', '--', rel], cwd=at,
                             capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    rev = got.stdout.strip()
    return rev if got.returncode == 0 and rev else None


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
            was = subprocess.run(['git', 'show', BASE_REV + ':./' + rel],
                                 cwd=at, capture_output=True, text=True,
                                 timeout=20)
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
        was = subprocess.run(['git', 'show', BASE_REV + ':./' + rel], cwd=at,
                             capture_output=True, text=True, timeout=20)
        return was.stdout if was.returncode == 0 else ''
    except (OSError, subprocess.SubprocessError):
        return None


def replaced_section_blocks(text, covered):
    """Figure-bearing blocks of the sections the replace list names.

    Keyed as `check_doc` keys the run file's own, and for the same
    reason: a block's key is its text with whitespace collapsed, a fixed
    point of wrapping and of nothing else, so *unchanged* means unchanged
    and never merely re-wrapped.

    THIS IS THE CHAPTER-HEAD CHECK APPLIED WIDER, and it exists because
    the narrow one was the only thing that worked. Run 19 rewrote the
    fifteen paragraphs that check named and left SIX of Run 18's standing
    elsewhere -- three closing Results while the table above them was Run
    19's, one of them contradicting the same write-up's headline
    allocation figure in three other places, and a `1.84x` in the ceiling
    ruling carried forward from Run 11 through eight write-ups. Every
    mechanical gate passed over all six; an independent checker found them
    by reading, two hours in.

    A run-name heuristic was tried first and refused: naming an old run
    beside a figure is the normal state of this document, and the sweep
    returned 100 paragraphs for the four that mattered. Identity against
    the committed copy has no such problem, because a paragraph a run
    replaced is not identical to the one it replaced.

    Scoped OUT is what a run does not replace: headings, table rows and
    indented blocks. The run's own file is out of scope too, and by
    construction -- these are README.md's sections, and the run file is
    held to its predecessor rather than to a committed copy.
    """
    out = []
    if not covered:
        return out
    parts = re.split(r'^(#{1,6} .*)$', text, flags=re.M)
    for i in range(1, len(parts), 2):
        head = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ''
        t = re.sub(r'[`*_]', '', head.lstrip('# ').strip().lower())
        slug = re.sub(r'[^a-z0-9 -]', '', t).strip().replace(' ', '-')
        if slug not in covered:
            continue
        for key, lines in blocks_of(body):
            first = lines[0]
            if first.lstrip().startswith('|') or first.startswith('    '):
                continue
            if FIGURE_RE.search(' '.join(lines)):
                out.append((slug, key, lines))
    return out


def held_in_reworked_sections(now, was, covered, churn=0.5):
    """Blocks a run left standing in a section it otherwise rewrote.

    Identity against the committed copy, scoped by how much of each
    section the run actually reworked. Sections
    a run replaces wholesale run 67% to 100% new and normally hold nothing
    of the previous run's; the reference chapters -- the open list, the
    placement chapter, the ceiling ruling -- run 0% to 11% new, and what
    they hold is dated history that outlives every run. Measured over Run
    19's write-up: six sections above the threshold holding four blocks
    between them, against fifteen below it holding 146.

    So the threshold is doing the work a maintained list of
    replaced-wholesale sections would do, without being one -- the replace
    list was rewritten once to stop enumerating, and this keeps that.

    WHAT IT DOES NOT CATCH, stated because a gate believed to be complete
    is worse than one known to be partial: a stale paragraph in a
    low-churn section. Run 19 left four of those -- a `1.84x` in the
    ceiling ruling carried from Run 11 through eight write-ups, two
    calibration paragraphs in the placement chapter, and a sighting count
    in the open list -- and none is reachable this way, because the
    sections holding them are 90% unchanged every run by design. Those
    want the reading the tasks entry describes and no checker has.
    """
    old = {}
    for s, k, _ in replaced_section_blocks(was, covered):
        old.setdefault(s, set()).add(k)
    per = {}
    for s, k, lines in replaced_section_blocks(now, covered):
        d = per.setdefault(s, {'held': [], 'new': 0})
        if k in old.get(s, set()):
            d['held'].append(lines[0])
        else:
            d['new'] += 1
    out = []
    for s, d in sorted(per.items()):
        total = d['new'] + len(d['held'])
        if total and d['new'] / total >= churn:
            out.extend((s, l) for l in d['held'])
    return out


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


def flat(s):
    """One space for each run of whitespace, so a wrapped document and an
    unwrapped one answer the same anchor.

    The anchor modes match a paragraph, and a paragraph's line breaks are
    the formatter's rather than the text's: `wrap80` puts them wherever
    the width falls and moves them on the next edit above. Matching the
    bytes therefore made every anchor spanning a break fail on exactly
    one of the two forms, which is why the write-up used to be done
    unwrapped and re-wrapped at each commit -- a whole precondition, in
    a chapter that had to state it, for a distinction the caller never
    meant. `--para` had always flattened its lead; `--replace` and
    `--delete` did not, and now do.
    """
    return ' '.join(s.split())


def splice(docs, anchor, source):
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

    **BOTH DOCUMENTS ARE SEARCHED**, README.md and the run's own file, and
    the count that has to be 1 is the count across the pair. A caller
    naming a paragraph does not know which file holds it -- that is the
    search this mode exists to replace -- and an anchor that occurs in both
    is refused naming each, which is the state a phrase shared between
    standing prose and a run's write-up puts it in.
    """
    if isinstance(docs, str):
        docs = [docs]
    seen = []
    for path in docs:
        try:
            text = open(path).read()
        except OSError as e:
            sys.stderr.write('--replace: %s\n' % e)
            return 2
        seen.append((path, text, flat(text).count(flat(anchor))))
    total = sum(k for _, _, k in seen)
    if total != 1:
        sys.stderr.write('--replace: the anchor occurs %d times across %s,'
                         ' need 1 -- quote more of the sentence\n'
                         % (total, ', '.join('%s (%d)'
                                             % (os.path.basename(p), k)
                                             for p, _, k in seen)))
        return 1
    readme, doc, _ = next(t for t in seen if t[2])
    paras = doc.split('\n\n')
    hit = [i for i, q in enumerate(paras) if flat(anchor) in flat(q)]
    if len(hit) != 1:
        sys.stderr.write('--replace: the anchor spans a paragraph break, so'
                         ' there is no one paragraph to replace\n')
        return 1
    old = paras[hit[0]]
    # A HEADING THE DOCUMENT DID NOT SEPARATE FROM THE PARAGRAPH ABOVE IT
    # is part of that paragraph, so replacing the paragraph deletes the
    # heading. Run 24 lost `## Results` from its own file that way, the
    # committed copy having no blank line before it, and met the loss two
    # gates later as `no Results heading`. The echo below did say so on
    # its `out, last` line, and saying so was not enough -- the same
    # difference the list guards below are the second of. A run file's
    # headings are what every install and every link resolve against.
    # Case: `replace-takes-an-abutting-heading`.
    # NOT the first line: a heading there is the block a caller named,
    # where one BELOW the prose is the one the paragraph swallowed.
    heads = [l for l in old.split('\n')[1:] if re.match(r'#{1,6} ', l)]
    if heads:
        sys.stderr.write('--replace: this paragraph carries the heading'
                         ' %s, which no blank line separates from it, so'
                         ' replacing the paragraph would delete the'
                         ' heading -- put a blank line above the heading'
                         ' first, then replace\n' % heads[0].strip())
        return 1
    # A TABLE ABUTTING A PARAGRAPH IS PART OF IT, and this is the THIRD of
    # the same shape: every class block in a run file is a bolded lead with
    # its installed table on the next line and no blank between them, which
    # `--block --in-place` writes that way, so an anchor naming the lead
    # takes the table too. Run 29 lost the `flip` class's 38 rows that way
    # at exit 0, and `--check-doc` passed immediately afterwards -- it holds
    # a table it FINDS to the JSONs and cannot miss one that is gone, so
    # this failure is quieter than the heading's, which a later gate named.
    # The echo below said so on its `out, last` line, which is how it was
    # caught, and saying so was not enough, exactly as it was not for the
    # heading and the list. A caller replacing a lead passes prose; a table
    # is `--block --in-place`'s to write and never a replacement's.
    # Case: `replace-takes-an-abutting-table`.
    rows = [l for l in old.split('\n')[1:] if l.lstrip().startswith('|')]
    if rows:
        sys.stderr.write('--replace: this paragraph carries a %d-line table'
                         ' that no blank line separates from it, so replacing'
                         ' the paragraph would delete the table -- replace'
                         ' the prose above it by quoting only that AND THEN'
                         ' --delete the table, or the old one stands below'
                         ' the new; or install it with --block --in-place\n'
                         % len(rows))
        return 1
    # A LIST WITH NO BLANK LINES BETWEEN ITS ITEMS IS ONE PARAGRAPH, and
    # this replaces paragraphs -- so an anchor inside one item of the open
    # list's numbered tasks took all three items and wrote back one.
    # Measured 2026-08-22: `--replace '3. **Between Run 17 and Run 18'`
    # replaced items 1, 2 and 3 with item 3 alone, at exit 0. The echo
    # below said so, `out, first` naming item 1 where the anchor names
    # item 3, and saying so was not enough -- which is the difference
    # between a warning and a refusal, and the reason this is the second.
    # Pass the whole list as the replacement, or edit the item in place.
    ol = old.split('\n')
    marks = [i for i, l in enumerate(ol)
             if re.match(r'\s*(?:\d+\.|[-*])\s', l)]
    items = [ol[i] for i in marks]
    # THE FIRST ITEM, not the first LINE: on a wrapped document an item
    # runs over several lines and the anchor a caller quotes from its
    # start lands on the second, which read as an anchor from the middle
    # of the list and was refused.
    first_item = '\n'.join(ol[:marks[1]]) if len(marks) > 1 else old
    if len(items) > 1 and flat(anchor) not in flat(first_item):
        sys.stderr.write(
            '--replace: this paragraph is a %d-item list and the anchor is'
            ' not in its first item, so replacing it would discard the items'
            ' above -- quote the list from its first item, and pass the whole'
            ' list as the replacement, or edit the one item in place\n'
            % len(items))
        return 1
    new = open(source).read().strip('\n')
    # AND THE OTHER HALF OF THAT, which the guard above has the wrong
    # premise about. It exempts an anchor in the FIRST item, on the theory
    # that quoting a list from its start is what a caller replacing the
    # whole list would do -- and it is also exactly what a caller EDITING
    # THE FIRST ITEM does. Measured 2026-08-25 on this README's non-urgent
    # TODO list: an anchor naming its first entry replaced all nine items
    # with one, 8859 characters for 656, at exit 0, with the echo below
    # saying so and read past. What separates the two intentions is the
    # REPLACEMENT: a caller who means the list hands a list back. Dropping
    # a spent item is still allowed -- the post-run procedure removes a
    # spent task from exactly such a list every run -- and so is replacing
    # a whole list with prose, which is what the control beside this case
    # asserts. What is refused is the ONE shape the two intentions differ
    # in: a replacement that is ITSELF a list item and carries fewer items
    # than the paragraph, which is a caller editing one item and nothing
    # else. Cases: `replace-shrinks-a-list-to-one-item`, and the two
    # controls `replace-takes-a-whole-list-for-a-whole-list` and
    # `replace-a-whole-list-from-its-first-item`.
    ITEM = r'\s*(?:\d+\.|[-*])\s'
    new_items = [l for l in new.split('\n') if re.match(ITEM, l)]
    if (len(items) > 1 and len(new_items) < len(items)
            and re.match(ITEM, new.split('\n')[0])):
        sys.stderr.write(
            '--replace: this paragraph is a %d-item list and the replacement'
            ' carries %d item(s), so the rest would go with it -- pass the'
            ' whole list as the replacement, or edit the one item in place\n'
            % (len(items), len(new_items)))
        return 1
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


def aa_bar(cells, b_cells, both_sh, both_st):
    """This comparison's A/A bar: (bar, carrier, arms, past).

    `bar` is the widest an A/A copy and its base part ACROSS the two files,
    `carrier` that pair as (copy, its figure, base, its figure) or None
    where no pair is in both, `arms` every non-control arm's distance from
    1, and `past` the arms further than the bar. Lifted out of --compare
    on 2026-09-17 for the class paragraph's skeleton, which quotes it.
    """
    def cross(st):
        rs = [cells[sh][st]['net'] / b_cells[sh][st]['net'] for sh in both_sh
              if cells[sh][st]['net'] > 0 and b_cells[sh][st]['net'] > 0]
        return geomean(rs) if rs else None

    # `carrier is None` MEANS NO PAIR IS HERE and never `every pair agreed
    # exactly`: initialised at a bar of 0.0 with a strict `>`, two files
    # whose A/A copies match to the digit -- which is what a synthetic pair
    # is, and what a repetition would be -- set no carrier and reported the
    # pairs as absent. Caught by `compare-prints-no-aa-bar` the day the
    # line was written.
    bar, carrier = 0.0, None
    for st in both_st:
        base = twin_of(st)
        if base is None or base not in both_st:
            continue
        a, b = cross(st), cross(base)
        if not a or not b:
            continue
        if carrier is None or abs(a / b - 1) > bar:
            bar, carrier = abs(a / b - 1), (st, a, base, b)
    arms = [(abs(cross(t) - 1), t) for t in both_st
            if not is_control(t) and not no_net(t) and cross(t)]
    past = sorted(t for d, t in arms if d > bar)
    return bar, carrier, arms, past


def cross_half_rows(cells, shapes, strategies, other, main, meta):
    """One population's per-arm basis/control geomeans, and `list`'s own.

    Factored out so the class section's aggregate and the per-class lines
    it aggregates cannot disagree. They did: Run 20 assembled its own
    population for the intro twice -- once dropping whole arms on one bad
    shape, once excluding a class the sentence said it covered -- and both
    readings shipped before a comprehension probe caught the second. The
    figures now come from one computation called nine times.
    """
    b_cells, b_shapes, b_strategies = load_other(other, main, shapes, meta)
    both_sh = [sh for sh in shapes if sh in b_shapes]
    rows, lst, partial = [], None, set()
    for st in strategies:
        if no_net(st) or st not in b_strategies:
            continue
        rs = [cells[sh][st]['net'] / b_cells[sh][st]['net']
              for sh in both_sh
              if cells[sh][st]['net'] > 0 and b_cells[sh][st]['net'] > 0]
        if rs:
            g = geomean(rs)
            rows.append((g, st))
            # DEGENERATE: a basis cell the correction did not leave
            # positive -- the work removed, so the arm's ratio is not a
            # movement. The basis half alone decides, deliberately: a
            # control-half sink narrows the ratio's coverage but does not
            # change what the basis measured, and widening the test to
            # both halves takes `lib-stage2` 2.6120 -- the published high
            # extreme, read at length in Run 22's file -- out of the
            # intro. Decided here so the intro and the block's own line
            # are one computation. 2026-09-01.
            if any(cells[sh][st]['net'] <= 0 for sh in both_sh):
                partial.add(st)
            if st == 'list':
                lst = g
    return rows, lst, partial


def cross_class_summary(basis, others, main):
    """The class section's intro figures, from the eight cross-half lines.

    Every number the paragraph above the class blocks states -- the
    comparison count, the faster/slower split, the range of the eight
    geomeans with the class at each end, and the arm holding each extreme
    -- aggregated from the SAME `cross_half_rows` the blocks print, so the
    intro and the blocks cannot part.

    They parted twice on Run 20. A population assembled here gave 398
    comparisons at 272/126 where the reader's own is 376 at 259/117; and
    the high end was quoted as `rev`'s 1.0970 when `reshape1`'s
    `offtab-aa-distant` reads 1.1133, because the first attempt had
    excluded that class's degenerate arms wholesale rather than naming
    them. So the degenerate cells are NAMED and kept out of the extremes
    rather than silently dropped or silently included: an arm whose basis
    cells are not all positive cannot be a movement, and
    `reshape1`'s canonicalizing arms return O(1) on three of its four
    shapes.

    Since 2026-09-01 they also sit out the faster/slower vote and the
    class geomeans -- a degenerate arm's ratio is over only the shapes it
    kept work on, one of `reshape1`'s four, the least-grounded number in
    the table -- while the comparison COUNT stays the blocks' own, which
    is what Run 20's wholesale exclusion broke, and the vote line says
    how many sat out.
    """
    if len(basis) != len(others):
        sys.stderr.write('--cross-classes: %d basis file(s) against %d other'
                         ' -- they pair up or nothing does\n'
                         % (len(basis), len(others)))
        return 2
    tot = voted = below = 0
    per, degenerate = [], []
    for b, o in zip(basis, others):
        cells, shapes, strategies, meta = load(b, main)
        # The correction, which `load` does not apply and every caller
        # does: `net` is the slope less that shape's forcing term, and
        # the ratios below are net over net as the blocks' are.
        apply_correction(cells, shapes, strategies, 'sumonly')
        rows, lst, partial = cross_half_rows(cells, shapes, strategies, o,
                                             main, meta)
        if not rows:
            sys.stderr.write('--cross-classes: %s and %s share no arm\n'
                             % (os.path.basename(b), os.path.basename(o)))
            return 1
        name = population_of(shapes, meta['dims'])[1]
        clean = [(g, st) for g, st in rows if st not in partial]
        drop = sorted(partial)
        if drop:
            degenerate.append((name, sorted(drop)))
        tot += len(rows)
        voted += len(clean)
        below += sum(1 for g, _ in clean if g < 1)
        per.append((name, geomean([g for g, _ in (clean or rows)]),
                    min(clean or rows), max(clean or rows), lst))
    print('cross-half, over %d class population(s)' % len(per))
    print('  %d arm-comparison(s), %d degenerate and not voted: %d put the'
          ' first half faster, %d slower'
          % (tot, tot - voted, below, voted - below))
    lo_c = min(per, key=lambda t: t[1])
    hi_c = max(per, key=lambda t: t[1])
    print('  geomeans %.4f on %s to %.4f on %s; all below 1: %s'
          % (lo_c[1], lo_c[0], hi_c[1], hi_c[0],
             'yes' if all(t[1] < 1 for t in per) else 'NO'))
    lo = min(per, key=lambda t: t[2][0])
    hi = max(per, key=lambda t: t[3][0])
    print('  extremes, degenerate arms excluded: `%s` %.4f on %s .. `%s`'
          ' %.4f on %s' % (lo[2][1], lo[2][0], lo[0], hi[3][1], hi[3][0],
                           hi[0]))
    lows = {}
    for name, _, l, _, _ in per:
        lows.setdefault(l[1], []).append(name)
    top = max(lows.items(), key=lambda kv: len(kv[1]))
    print('  the low extreme is `%s` in %d of %d population(s)'
          % (top[0], len(top[1]), len(per)))
    for name, arms in degenerate:
        print('  DEGENERATE on %s, kept out of the extremes, the vote and'
              ' the geomeans: %s'
              % (name, ', '.join('`%s`' % a for a in arms)))
    off = [(n, l) for n, _, _, _, l in per if l is not None
           and abs(l - 1) > 0.007]
    if off:
        print('  `list` past the 0.7%% bar, so NOT read for the pair\'s'
              ' variable: %s'
              % ', '.join('%s %.4f' % (n, l) for n, l in off))
    return 0


def section(docs, name, with_tables=None):
    """Print one section's prose, by heading name, WITHOUT its tables.

    The reading a run owes is enumerated -- of the compares-against
    section the paragraphs settling the regime and the basis and NOT its
    figures, of the class blocks the form and one example and not the
    other seven -- and until this mode there was no way to obey it. A
    session opens a document with `sed -n 'A,Bp'`, the tables sit between
    the paragraphs it is told to read, and line numbers go stale at every
    install and every rewrap besides. So the enumeration was advice and
    "read it whole" was the instruction that got acted on: Run 20 ingested
    38 KB of the previous run's tables, 24% of that file, every byte of it
    named as skippable one sentence later.

    Tables are what a run does NOT read: the reader emits them, --in-place
    installs them, and a checker recomputes them from the JSONs. They are
    withheld with their size, so what was skipped is visible rather than
    silent, and --with-tables prints them for the one case that wants them
    -- the run's own two-column geomeans, which are hand-edited. A NUMBER
    takes one of them: reading-list item 4 is "the ONE table read", and
    all-or-nothing made that unobeyable, Run 25 taking its 36 lines of
    prose with 82 lines of fingerprint attached. A number past the end
    refuses, silence there reading exactly like a section with no table.

    Matching is on the heading TEXT, case-insensitively, across both
    documents; several matches print an index rather than all of them, as
    --para does, since a wrong section is a wrong read and not a wrong
    line. The span runs to the next heading of the same level or higher,
    so asking for a chapter gets its subsections and asking for one of
    those does not get its siblings.
    """
    if isinstance(docs, str):
        docs = [docs]
    # A FILE: qualifier narrows the search to one document, for the two
    # headings both carry -- `Provenance` -- which used to be reachable in
    # the run file only by awk (Run 23, 2026-09-02). And `head` is the run
    # file's untitled block above its first `##`, which no heading names:
    # asking for the title heading printed the whole file's prose, 136 KB.
    m = re.match(r'([^/:]+\.md):(.+)$', name)
    if m:
        want = [d for d in docs if os.path.basename(d) == m.group(1)]
        if not want:
            sys.stderr.write('--section: no document named %s among %s\n'
                             % (m.group(1), ', '.join(os.path.basename(q)
                                                     for q in docs)))
            return 1
        docs, name = want, m.group(2)
    if name.lower() == 'head':
        run = [d for d in docs if RUN_DOC_RE.match(os.path.basename(d))]
        if not run:
            sys.stderr.write('--section head: wants a run file, and none is'
                             ' among %s\n' % ', '.join(os.path.basename(q)
                                                      for q in docs))
            return 1
        try:
            lines = open(run[-1]).read().split('\n')
        except OSError as e:
            sys.stderr.write('--section: %s\n' % e)
            return 2
        end = next((j for j, ln in enumerate(lines)
                    if re.match(r'##\s', ln)), len(lines))
        out = '\n'.join(lines[:end]).rstrip('\n')
        print('%s: head, the %d paragraph(s) above its first ## -- %d KB'
              % (os.path.basename(run[-1]),
                 sum(1 for q in out.split('\n\n') if q.strip()),
                 len(out) // 1024))
        print()
        print(out)
        return 0
    hits = []
    for path in docs:
        try:
            lines = open(path).read().split('\n')
        except OSError as e:
            sys.stderr.write('--section: %s\n' % e)
            return 2
        for i, ln in enumerate(lines):
            m = re.match(r'(#{1,6})\s+(.*?)\s*$', ln)
            if m and name.lower() in m.group(2).lower():
                hits.append((path, lines, i, len(m.group(1)), m.group(2)))
    if not hits:
        # A BOLDED LEAD IS NOT A HEADING, and half the chapter's named
        # subjects are leads: *Which two halves a pair has* is one, and
        # note-check's own roll message sends a reader there by that name.
        # Refusing outright sent Run 36's preparation to `grep` for a tag
        # and `sed` for a window, which is the path into the chapter this
        # mode exists to avoid. So fall back to the lead and say which it
        # was. Case: `section-falls-back-to-a-bolded-lead`.
        leads = []
        for path in docs:
            try:
                lines = open(path).read().split('\n')
            except OSError:
                continue
            for first, para, _sp in unwrapped_paragraphs(lines):
                if re.match(r'\*\*', para.lstrip()) \
                        and name.lower() in para[:400].lower():
                    leads.append((path, first, para))
        # NARROWED LIKE THE HEADING BRANCH and never guessed: the first
        # draft of this fallback printed the first match and returned 0, so
        # `--section 'the note'` handed back one of a dozen leads and read
        # as an answer. A wrong paragraph that looks right is the one
        # outcome this mode must not have. Case: `section-lead-is-narrowed`.
        if len(leads) == 1:
            path, first, para = leads[0]
            print('%s:%d: no heading of that name -- this is a BOLDED LEAD,'
                  ' printed whole; `--para` is the mode for one'
                  % (os.path.basename(path), first))
            print()
            print(para)
            return 0
        if leads:
            print('no heading matches %r, and %d bolded lead(s) do; narrow'
                  ' it to one, or read them with `--para`:'
                  % (name, len(leads)))
            for path, first, para in leads:
                print('  %s:%d  %s'
                      % (os.path.basename(path), first,
                         para.lstrip()[:96].replace('\n', ' ')))
            return 1
        sys.stderr.write("--section: no heading and no bolded lead matches"
                         " %r in %s -- `--para PATTERN` searches every"
                         " paragraph\n"
                         % (name, ', '.join(os.path.basename(q)
                                            for q in docs)))
        return 1
    if len(hits) > 1:
        print('%d heading(s) match %r; narrow it to one:' % (len(hits), name))
        for path, _, i, lvl, text in hits:
            print('  %s:%d  %s %s'
                  % (os.path.basename(path), i + 1, '#' * lvl, text))
        return 1
    path, lines, i, lvl, text = hits[0]
    end = next((j for j in range(i + 1, len(lines))
                if re.match(r'#{1,%d}\s' % lvl, lines[j])), len(lines))
    body = '\n'.join(lines[i:end])
    # A TABLE IS ITS OWN PARAGRAPH HERE, EVEN WHERE THE DOCUMENT DOES NOT
    # SEPARATE IT FROM ITS LEAD. Markdown lets a table follow its
    # introducing sentence with no blank line between them, and this
    # counted a paragraph as a table only when the paragraph STARTED with
    # `|` -- so such a table printed whatever was asked, and the
    # compares-against section's two-column table, which is the one the
    # reading list sends `--with-tables 1` for, could not be selected at
    # all: the only two selectable paragraphs there were the per-shape
    # fingerprints, and `--with-tables 1` released one of those instead.
    # Found by Run 32's carrier, fixed 2026-09-15.
    # Case: `section-splits-a-table-from-its-lead`.
    paras, seg, was = [], [], None
    for para in body.split('\n\n'):
        for line in para.split('\n'):
            now = line.lstrip().startswith('|')
            if seg and now != was:
                paras.append('\n'.join(seg))
                seg = []
            seg.append(line)
            was = now
        if seg:
            paras.append('\n'.join(seg))
            seg, was = [], None
    tabs = [k for k, para in enumerate(paras)
            if para.lstrip().startswith('|')]
    if with_tables and with_tables > len(tabs):
        print('--with-tables %d: this section carries %d table(s)'
              % (with_tables, len(tabs)))
        return 1
    if with_tables is None:
        want = set()
    elif with_tables == 0:
        want = set(tabs)
    else:
        want = {tabs[with_tables - 1]}
    kept, held, held_bytes = [], 0, 0
    for k, para in enumerate(paras):
        if k in tabs and k not in want:
            held += 1
            held_bytes += len(para)
            continue
        kept.append(para)
    out = '\n\n'.join(kept)
    print('%s: %s %s -- %d KB of prose'
          % (os.path.basename(path), '#' * lvl, text, len(out) // 1024))
    if held:
        print('  %d table paragraph(s) withheld of %d here, %d KB --'
              ' --with-tables prints them and --with-tables N the Nth alone,'
              ' numbered down the section; the reading list wants the FIRST,'
              ' which is the two-column table'
              % (held, len(tabs), held_bytes // 1024))
    print()
    print(out)
    return 0


REG_HEAD = '## What this run was built to answer, and what it answered'

# A PAIR NOTE, read for the NEXT pair rather than for the run it served.
# Item 10 of this chapter's reading list says a preparation reads the
# previous note MINUS its handover -- "about a third of a note and none of
# it yours" -- and names the blocks; until 2026-09-03 that skip was a
# sentence a session had to hold while reading the file in windows, and
# Run 24's preparation read all of them because `sed` has no idea which
# third it is looking at. The names below are that sentence, executable.
NOTE_HANDOVER = (
    'ENTRY POINT FOR THE SESSION THAT RUNS THIS',
    'WHAT THE PREPARATION LEARNED',
    'GREEN AFTER THE LAST EDIT',
    'GATE VERDICT',
)
# `GATE: NOT RUN` is the template's own line and IS owed -- it is what
# says the pair has no gate. `GATE: run <date>` is run-gate.sh's appended
# block, which is that run's progress.
NOTE_HANDOVER_PREFIX = ('GATE: run',)
# Inside the fill-in block, the lines recording that run's own progress
# rather than what its BUILD said. The build lines are what this run's own
# build is compared against, which is why the block is not skipped whole.
NOTE_PROGRESS = ('counts', 'sequence', 'riders', 'gates', 'named fills',
                 'straddle owners')
FILL_LABEL = re.compile(r'  (\S(?:.*?\S)?)\s{2,}\S')


def _note_title(lead):
    """A block's name: its lead without the marker and without the sentence."""
    t = re.split(r"\[SAME|\[PAIR'S", lead)[0].strip().rstrip(':,. ')
    return t or lead[:40].strip()


def _template_blocks(near):
    """{title: paragraph} of pair-note-template.txt beside the note.

    The template is the only statement of what each block owes, so a draft
    that emits a `[PAIR'S]` slot can carry that guidance with it instead of
    sending the writer to a third file. Absent template, absent guidance:
    the slot still prints, which is the half that matters.
    """
    out = {}
    try:
        text = open(os.path.join(near or '.', 'pair-note-template.txt')).read()
    except OSError:
        return out
    for para in text.split('\n\n'):
        lead = para.lstrip('\n').split('\n', 1)[0]
        if '[PAIR' in lead or '[SAME in shape' in lead:
            out[_note_title(lead)] = para
    return out


def _template_gate(near):
    """The template's `GATE: NOT RUN` paragraph, or that line alone.

    Live text and not scaffolding: the note's gate line is what
    run-status.sh reads for step 14 and what run-gate.sh appends beneath,
    so a draft that commented it out would hand over a note with no gate.
    """
    try:
        text = open(os.path.join(near or '.', 'pair-note-template.txt')).read()
    except OSError:
        return 'GATE: NOT RUN.'
    for para in text.split('\n\n'):
        if para.lstrip('\n').startswith('GATE: NOT RUN'):
            return para.rstrip('\n')
    return 'GATE: NOT RUN.'


def _template_same(near):
    """{title: paragraph} of the template's `[SAME]` blocks, or {}.

    Since 2026-09-23 these, and not the previous note's, are what a draft
    carries: a note's `[SAME]` blocks had grown by a run's worth of figures
    and continuity clauses at every copy, which each preparation re-read
    and rewrote by hand. The template's are short and name the run by `$R`
    and the halves by `<basis>` and `<other>`, so they are current by
    construction.
    """
    out = {}
    try:
        text = open(os.path.join(near or '.', 'pair-note-template.txt')).read()
    except OSError:
        return out
    for para in text.split('\n\n'):
        lead = para.lstrip('\n').split('\n', 1)[0]
        if '[SAME]' in lead:
            out[_note_title(lead)] = para.strip('\n')
    return out


def _same_filled(para, run, new, env, machine):
    """A template `[SAME]` block with this pair's names and values in it.

    `machine` maps a machine line's key -- LAUNCH, RIDERS -- to the whole
    line the previous note carried, which replaces the template's
    placeholder line of that key: those are values the pair holds, not
    prose, and run-evening.sh reads them.
    """
    para = (para.replace('$R', run).replace('<basis>', new[0])
                .replace('<other>', new[1]))
    # A RIDER LINE TAKES THE LAUNCH VALUES LESS SATURATE: run-evening.sh
    # unsets it for a clean leg, but these lines are also the hand form,
    # and run-alonelegs.sh passes an inherited SATURATE through.
    clean = ' '.join(t for t in env.split() if not t.startswith('SATURATE'))

    def put(m):
        e = clean if 'run-alonelegs' in m.group(2) else env
        return m.group(1) + ('%s ' % e if e else '') + m.group(2)
    para = re.sub(r'^( *)<env> *(.*)$', put, para, flags=re.M)
    for key, line in machine.items():
        para = re.sub(r'^%s:.*$' % key, lambda _m: line, para, flags=re.M)
    return para


def _scaffold(para):
    """The template's guidance for a block, as `#` lines to delete.

    Commented rather than plain so that scaffolding can never be mistaken
    for the note's own prose, and so that a note still carrying it is
    obvious at a glance rather than only to a reader who knows the
    template by heart.
    """
    if not para:
        return '#  (pair-note-template.txt has no block of this name)'
    return '\n'.join('#  ' + l if l.strip() else '#'
                     for l in para.rstrip('\n').split('\n'))


def _fill_skeleton(para):
    """The fill-in block as labels and `<yours>`, carrying no observation.

    Its shape is the template's and its content is this pair's, which is
    what `[SAME in shape, PAIR'S in content]` means: carrying a previous
    pair's md5 or .text forward under this pair's heading is the one
    copying error the marker exists to prevent.
    """
    # The lead carries the previous pair's BUILD DATE, which no rename
    # touches; back to the template's placeholder, since the block's own
    # rule is that each line is dated when it is written.
    out = [re.sub(r'\d{4}-\d\d-\d\d', 'YYYY-MM-DD',
                  para.lstrip('\n').split('\n', 1)[0])]
    for line in para.split('\n')[1:]:
        m = FILL_LABEL.match(line)
        if m:
            out.append('  %-16s  <yours>' % m.group(1))
    return '\n'.join(out)


def _note_kind(lead):
    """The kind a paragraph ANNOUNCES, or None where it continues one.

    A note's blocks run on past their own paragraph -- ENTRY POINT carries
    SPENT, INHERITED and STILL OWED beneath it; HOW EACH HALF IS BUILT
    carries the two recipes; REGISTERED BEFORE IT RAN carries the item
    clauses -- so a classification lead by lead reads only the first
    paragraph of each and treats the rest as unmarked. That is what made
    `--note` report "1 KB of handover withheld" of a handover the chapter
    calls about a third of a note, and what made a whole-note `--draft`
    carry a previous pair's recipes and its `GATE: SOUND` verdict into the
    next note (both 2026-09-07). The state is sticky; this says where it
    changes.

    THE MACHINE CHECK IS THE GATE'S, and is named here for the same reason
    the verdict is: it is `run-gate.sh --machine`'s answer, written above
    the gate's own block and spent with that run. Unnamed it classified as
    nothing, so `--draft` carried it verbatim -- Run 27's reading of its
    own box move arrived in Run 28's draft under a lead beginning AND IT
    FIRED, in a note whose gate the same call had reset to NOT RUN
    (2026-09-09).
    """
    if any(lead.startswith(h) for h in NOTE_HANDOVER):
        return 'handover'
    if (any(lead.startswith(h) for h in NOTE_HANDOVER_PREFIX)
            or lead.startswith('GATE:')
            or lead.startswith("THE GATE'S VERDICT")
            or lead.startswith('THE MACHINE CHECK')):
        return 'gate'
    if lead.startswith('Verified when built'):
        return 'fill'
    if "[PAIR'S" in lead:
        return 'pairs'
    if '[SAME' in lead:
        return 'same'
    return None


def _note_blocks(text):
    """(paragraph, kind, announced) per block, in the note's own order.

    THE FILL-IN BLOCK IS ONE PARAGRAPH AND AN INTERRUPTION, so what
    follows it RESUMES what it interrupted rather than starting fresh.
    Returning to `plain` there is what let a whole pair's spent gate out
    of the withholding: a gate verdict is written above the fill-in block
    and its own continuations -- the palindrome's spread, the arm that
    crosses 1, the machine check -- are written BELOW it, so they came
    back `plain`, `--note` printed them as blocks a preparation decides,
    and `--draft` carried five of them into the next note with the tag
    substitution applied. Run 33's draft opened with Run 32's gate
    reading and named `run33-gate-nospec-a`, a process no run will ever
    write (2026-09-15). Case: `note-blocks-resume-after-the-fill`.
    """
    out = []
    state, announced, before_fill = 'plain', True, 'plain'
    for para in text.split('\n\n'):
        lead = para.lstrip('\n').split('\n', 1)[0]
        k = _note_kind(lead)
        announced = k is not None
        if announced:
            if k == 'fill':
                before_fill = state
            state = k
        elif state == 'fill':
            state = before_fill
        out.append((para, state, announced))
    return out


def _fill_trimmed(para):
    """(kept text, characters dropped) for the fill-in block.

    The count is of the TEXT removed and not of the labels naming it: the
    size line exists so a reader can see the skip was worth taking, and a
    label count made it read as 40 bytes.
    """
    kept, dropped, skipping = [], 0, False
    for line in para.split('\n'):
        m = FILL_LABEL.match(line)
        if m:
            label = m.group(1).rstrip(':').strip().lower()
            skipping = label in NOTE_PROGRESS
        elif not line.startswith(' ' * 3):
            skipping = False
        if skipping:
            dropped += len(line) + 1
        else:
            kept.append(line)
    return '\n'.join(kept), dropped


def note_check(path, readme, run_doc=None):
    """The note's own PROSE, checked mechanically.

    Until 2026-09-15 the note was the one artifact here with no such pass:
    preflight's 10c reads the paths it names and 10d its recipes against
    the HALVES line, and both are predicates over structure -- neither
    reads a sentence. What a note's prose gets wrong is not structural. It
    is carried: `--draft` brings every `[SAME]` block over with the RUN
    and the HALF names substituted and nothing else, so the figures, the
    run numbers and the item numbers inside them are the previous pair's
    until a hand re-reads them, which the draft's own header asks for and
    which is where a preparation is tired.

    Run 33's preparation re-read those blocks and rewrote a statement in
    every one of them; these are the three kinds a machine can have: a
    range ending at the run before the previous one (`as Runs 20 to 31`
    in a note whose previous
    run is 32, twice), an item number above what the registration carries
    ((10), (15) and (16) against a registration of seven), and a half tag
    missing from the note's own roll of them (neither `exit` nor
    `gheadexit` was on it, under a carried clause saying both were
    already). The other three wanted a reader. Case:
    `note-check-reads-the-carried-blocks`.
    """
    try:
        text = open(path).read()
    except OSError as e:
        sys.stderr.write('--note-check: %s\n' % e)
        return 2
    base = os.path.basename(path)
    m = re.match(r'(run(\d+))-pair\.txt$', base)
    if not m:
        sys.stderr.write('--note-check wants a $R-pair.txt, not %r\n' % base)
        return 2
    run, n = m.group(1), int(m.group(2))
    at = os.path.dirname(os.path.abspath(path))
    older = [int(q.group(1))
             for f in os.listdir(os.path.join(at, RUNS_DIR))
             for q in [re.match(r'run(\d+)\.md$', f)] if q
             and int(q.group(1)) < n]
    if not older:
        sys.stderr.write('--note-check: no runs/run<N>.md below %s, so the'
                         ' previous run cannot be resolved and the stale'
                         ' ranges cannot be read\n' % run)
        return 2
    prev = max(older)
    lines = text.split('\n')
    found = []

    # 1. A CONTINUITY CLAIM THAT STOPS SHORT OF THE PREVIOUS RUN. What is
    # checked is the CLAIM and not the range: `as Runs 20 to 31` says
    # every run from 20 to now did this, so an upper bound below the
    # previous run dates the sentence to the note it was carried from.
    # A bare range is history and is left alone -- `was not Runs 29 to
    # 31's` names the three flag pairs and is right at any distance,
    # which is what a version of this keyed on the range alone flagged
    # twice on a correct note.
    # OVER THE WHOLE TEXT AND NOT LINE BY LINE, the note being wrapped at
    # about seventy columns: `as it\nheld Runs 25 to 31` is the shape the
    # carried blocks actually take, and a line-scanning version of this
    # check missed exactly that one of four planted errors while catching
    # the other three -- which is this repo's own rule about searching the
    # unwrapped form, met again in a checker.
    # AND THE RANGE'S OWN TAIL COUNTS. `as they were on Runs 24 to 30 and
    # 32` reaches the previous run by naming it after the range, so the
    # claim is whole and the bound alone reads it short -- which is the
    # one false positive this check had on a note believed correct.
    for q in re.finditer(r'\bas (?:\S+\s+){0,3}Runs\s+(\d+)\s+to\s+(\d+)'
                         r'((?:(?:,|\s+and)\s+\d+)*)', text):
        reach = max([int(q.group(2))]
                    + [int(x) for x in re.findall(r'\d+', q.group(3))])
        if reach < prev:
            found.append((text.count('\n', 0, q.start()) + 1,
                          'a continuity claim reaching only Run %d where the'
                          ' previous run is %d: %r'
                          % (reach, prev, ' '.join(q.group(0).split()))))

    # 2. AN ITEM NUMBER ABOVE WHAT THE REGISTRATION CARRIES, the shape a
    # shrunk registration leaves: Run 32's sixteen items became Run 33's
    # seven, and a carried block went on naming three that no longer
    # exist. Four-digit parentheses are dates and are not items.
    src, items, _flat = registration_items(
        run, run_doc or os.path.join(at, RUNS_DIR, '%s.md' % run), readme)
    if items is None:
        return 2
    top = max([int(k) for k, _ in items] or [0])
    # A REGISTRATION THAT PARSES NO ITEM DISABLES THIS CHECK rather than
    # firing it on every reference: at a `top` of zero the comparison is
    # true of every `(N)` in the note, which reports the PARSE and calls
    # it the note's fault. The summary line prints the count either way.
    for i, ln in enumerate(lines, 1) if top else ():
        for q in re.finditer(r'\((\d{1,2})\)', ln):
            if int(q.group(1)) > top:
                found.append((i, 'item %s, where the registration in %s'
                                 ' carries %d'
                              % (q.group(0), os.path.basename(src), top)))

    # 3. A HALF TAG MISSING FROM THE ROLL OF THEM. The roll moved into
    # README's *Which two halves a pair has* on 2026-09-18 -- two copies
    # is how it drifted, `g914` missing from one and the template's four
    # tags short of the notes' -- so the tags are held to the CHAPTER's
    # roll where the chapter has one, and to the note's where it does not,
    # which is every note written before the move. The note keeps its
    # NAMING THE HALVES block either way: it is now the pointer.
    # THE CHAPTER IS WRAPPED, so the roll's own sentence can fall across a
    # line break and a plain search of it finds nothing; the paragraphs
    # are read with their whitespace flattened, which is the same reason
    # every search of prose here reads the unwrapped form.
    roll = next((p for p in text.split('\n\n')
                 if p.lstrip('\n').startswith('NAMING THE HALVES')), None)
    chapter_roll = None
    try:
        rtext = io.open(readme, encoding='utf-8').read()
    except (OSError, TypeError):
        rtext = ''
    for p in re.split(r'\n\s*\n', rtext):
        flat = re.sub(r'\s+', ' ', p)
        if 'The roll of tags this chapter has used' in flat:
            chapter_roll = flat
            break
    halves = re.search(r'^HALVES: basis=(\S+) other=(\S+)\s*$',
                       text, re.M)
    if roll is None:
        found.append((0, 'no paragraph led NAMING THE HALVES, which is'
                         " where a note points at the chapter's roll of"
                         ' the halves this chapter has used'))
    elif halves:
        where = chapter_roll if chapter_roll is not None else roll
        what = ("README's *Which two halves a pair has*"
                if chapter_roll is not None else 'NAMING THE HALVES')
        for tag in (halves.group(1), halves.group(2)):
            if '`%s`' % tag not in where:
                found.append((text[:text.index(roll)].count('\n') + 1,
                              'the half `%s` is not on the roll in %s,'
                              ' which this run appends to --'
                              " `./read-run.py --para 'The roll of tags'`"
                              ' prints the roll itself, the section'
                              ' named above opening three paragraphs'
                              ' earlier'
                              % (tag, what)))

    # 4. AND AN ENTRY POINT THE EXECUTING SESSION CAN READ IN A MINUTE.
    # Run list step 13 tells that session to read the note's `[EXEC]`
    # blocks -- the ones it ACTS on -- `or the whole note where a
    # preparation left none`. Run 33's preparation left none and the
    # executing session read all 745 lines, which is the branch being
    # taken rather than a shortfall in the instruction: a note is the
    # preparation's record and an entry point is what makes it usable
    # by anyone else. One block, naming what is spent and what is owed,
    # is thirty lines of reading instead of seven hundred.
    if '[EXEC]' not in text:
        found.append((0, 'no [EXEC] block, so run list step 13 falls back'
                         ' to reading the whole note -- 745 lines on Run'
                         ' 33. Mark the block the executing session ACTS'
                         ' on, what is spent and what is still owed'))

    # 5. A BLOCK THE HEAD PROMISES AND THE BODY LACKS. Run 37's note said
    # its post-run step 9 half was `at the foot of this note under
    # LEARNED` and carried no such block; that half met the same list a
    # day earlier and went with the session, so nothing could recover it
    # and no pass looked. Keyed on the phrase that NAMES a block rather
    # than on `under NAME`, which over the seven notes on disk also
    # catches `under WILDLOG`, `under CORPUS_RUN` and `under HEAD` --
    # environment variables and ordinary words. Read flattened, a note
    # being hand-wrapped and the phrase able to straddle a break.
    for q in re.finditer(r'(?:at|near) the foot of this note under'
                         r' ([A-Z][A-Z0-9_]{3,})', re.sub(r'\s+', ' ', text)):
        name = q.group(1)
        if not re.search(r'^%s\b' % re.escape(name), text, re.M):
            found.append((text[:text.index(name)].count('\n') + 1
                          if name in text else 0,
                          'the head promises a block `%s` at the foot of'
                          ' this note and no line of it begins `%s` --'
                          ' write the block or drop the promise, since what'
                          " it holds is the preparation's half of post-run"
                          ' step 9 and reaches the executing session only'
                          ' here' % (name, name)))

    if not found:
        print('note-check %s: clean -- %d line(s), previous run %d,'
              ' registration of %d item(s)' % (base, len(lines), prev, top))
        return 0
    print('note-check %s: %d finding(s), previous run %d, registration of'
          ' %d item(s)' % (base, len(found), prev, top))
    for i, why in sorted(found):
        print('  %s:%d  %s' % (base, i, why))
    return 1


def pair_note(path, draft=None, halves=None):
    """A previous pair note, read as the next preparation owes it.

    Two readings, and they answer different questions. Plain, this prints
    what item 10 asks for and withholds the handover, saying how much it
    withheld -- the size line is the point, since a skip nobody can see is
    a skip nobody believes was taken. With `--draft`, it prints the whole
    note: each `[SAME]` block from the template where the template has
    one, with this pair's names and the previous note's LAUNCH and RIDERS
    values put in, and from the previous note with the names carried over
    where it has not -- retyping them is where a copying error gets in.
    A `[PAIR'S]` block comes back as a MODEL under a `<yours>`
    line, the previous pair's text for this preparation to rewrite: those
    are the decisions, and the marker is what keeps a copied decision
    from passing for one, run-status.sh's 2c counting it as a slot until
    the line is deleted. The handover and the fill-in block's content
    never cross. A block marked `[SAME in shape]` is listed as yours too,
    which is the safe direction: its shape carries over and its CONTENT
    is this pair's, so a draft emitting it would hand back the last
    pair's observations under this pair's heading.
    """
    try:
        text = open(path).read()
    except OSError as e:
        sys.stderr.write('--note: %s\n' % e)
        return 2
    prev = os.path.basename(path).split('-pair.txt')[0]
    m = re.search(r'^HALVES:\s*basis=(\w+)\s+other=(\w+)', text, re.M)
    if not m:
        sys.stderr.write('--note: %s has no HALVES line, so neither its'
                         ' halves nor a rename can be read from it\n' % path)
        return 1
    old = (m.group(1), m.group(2))
    blocks = _note_blocks(text)

    if draft is None:
        kept, held, carried = [], 0, []
        for para, kind, announced in blocks:
            # What item 10 asks a preparation for is the other axis from
            # the handover: the two recipes, what the pair measured and why
            # its basis was that recipe, the roster, the compiler, the shim
            # and the fill-in block's observations. That is `pairs`, `fill`
            # and the header. The handover and the gate are spent, and a
            # `[SAME]` block is --draft's to carry over with the names
            # changed, so a preparation that READS one here reads a block
            # it will never type. Withholding all three is what makes this
            # a skip at all: until 2026-09-07 it withheld the handover's
            # first paragraph alone and said so as "59 KB of 60 KB".
            if kind in ('handover', 'gate', 'same'):
                held += len(para)
                if announced:
                    # Named by WHY it is withheld and not in one list: a
                    # `[SAME]` block comes back under --draft and a
                    # handover does not, so one label over both would send
                    # a reader looking for a block that is simply spent.
                    carried.append((kind, _note_title(
                        para.lstrip('\n').split('\n', 1)[0])))
                continue
            if para.lstrip().startswith('Verified when built'):
                para, dropped = _fill_trimmed(para)
                held += dropped
            kept.append(para)
        body = '\n\n'.join(kept)
        print('%s: the blocks a PREPARATION DECIDES, %d KB of %d KB; %d KB'
              ' withheld -- the handover, which item 10 names and does not'
              ' owe, and the [SAME] blocks, which --draft carries over'
              % (os.path.basename(path), len(body) // 1024,
                 len(text) // 1024, held // 1024))
        # The `[SAME]` blocks are NAMED, since --draft brings each back and
        # a reader wants to know which. The handover and the gate are
        # counted and not named: their leads are the spent text itself, so
        # echoing one here reprints a slice of the thing being withheld --
        # which a case caught on 2026-09-07, `ENTRY POINT FOR THE SESSION`
        # appearing in a mode whose whole job is to drop it.
        got = [t for kind, t in carried if kind == 'same']
        if got:
            print('  carried over by --draft, not read here: %s'
                  % '; '.join(t[:44] for t in got))
        for k, label in (('handover', "the last run's handover"),
                         ('gate', "that pair's gate")):
            n = sum(1 for kind, _ in carried if kind == k)
            if n:
                print('  %s, spent with that run: %d block(s), unnamed here'
                      ' so that this mode does not reprint what it drops'
                      % (label, n))
        print()
        print(body.rstrip('\n'))
        return 0

    names = [h.strip() for h in (halves or '').split(',')]
    if len(names) != 2 or names[0] == names[1] \
            or not all(re.fullmatch(r'\w+', h) for h in names):
        sys.stderr.write('--draft wants --halves basis,other: exactly TWO'
                         ' distinct names of [A-Za-z0-9_], not %r; a third'
                         ' would otherwise be taken as part of the second\n'
                         % (halves,))
        return 1
    new = tuple(names)
    # THE WHOLE NOTE IN THE PREVIOUS NOTE'S OWN ORDER, since 2026-09-07,
    # where this emitted the `[SAME]` blocks alone. A preparation then
    # assembled its note out of three files -- this output, the template
    # and the previous note -- and the assembling is where a block gets
    # dropped or a heading gets typed without its content. Now every slot
    # is present and the writing is filling them in: a `[SAME]` block is
    # carried over, a `[PAIR'S]` block prints its TITLE and a `<yours>`
    # line with the previous pair's block beneath it as a model, and the
    # fill-in block prints its labels with `<yours>` for
    # `preflight.sh --fill-in` to replace or a hand to write.
    # A `[PAIR'S]` BLOCK'S CONTENT CROSSES AS A MODEL, since 2026-09-23,
    # where until then only its title did. The ruling it replaces was that
    # copying one forward is how a note comes to describe the run before
    # it; what it cost was a second read of the previous note, 35 KB on
    # Run 39's preparation, taken only to see how each block had been
    # written. The `<yours>` line under the title is what keeps the
    # ruling's point: run-status.sh counts it as an owed slot until the
    # preparation deletes it, so a block carried and never rewritten
    # leaves 2c NOT DONE rather than passing as this pair's.
    # The handover and the gate still cross as a slot and nothing else.
    pairs, out, gate_done, handover_done = [], [], False, False
    guide = _template_blocks(os.path.dirname(os.path.abspath(path)))
    # A `[SAME]` BLOCK COMES FROM THE TEMPLATE WHERE THE TEMPLATE HAS ONE
    # OF THAT TITLE, since 2026-09-23 -- see `_template_same`. What the
    # previous note held that a script reads is carried into it: the
    # LAUNCH and RIDERS lines, and the LAUNCH values in front of each
    # command. The template's text goes in AFTER the renames below, as a
    # placeholder until then, so that a tag this pair reuses from the
    # last one cannot rename the template's own. A paragraph that ran on
    # under a replaced block is dropped and NAMED in the header, being
    # the one thing this could otherwise lose unseen. A `[SAME]` block the
    # template lacks is carried from the note as before.
    tsame = _template_same(os.path.dirname(os.path.abspath(path)))
    machine = {k: m.group(0) for k in ('LAUNCH', 'RIDERS')
               for m in [re.search(r'^%s:.*$' % k, text, re.M)] if m}
    env = ''
    if 'LAUNCH' in machine:
        env = machine['LAUNCH'].split(':', 1)[1].strip()
        env = '' if env in ('none', '') else env
    fills, from_template, dropped, replacing = {}, [], [], False
    for para, kind, announced in blocks:
        lead = para.lstrip('\n').split('\n', 1)[0]
        title = _note_title(lead)
        if kind == 'same':
            if announced:
                replacing = title in tsame
                if replacing:
                    key = '\x00SAME%d\x00' % len(fills)
                    fills[key] = tsame[title]
                    out.append(key)
                    from_template.append(title)
                else:
                    out.append(para)
            elif replacing:
                dropped.append((title, lead.strip()[:60]))
            else:
                out.append(para)
            # THE HALVES AND COMPARE LINES SURVIVE A REPLACED BLOCK: every
            # driver reads the first through pair-halves.sh, and a note
            # whose block carried it would otherwise draft without one.
            if replacing:
                keep = [l for l in para.split('\n')
                        if re.match(r'(HALVES|COMPARE):', l)]
                if keep:
                    out.append('\n'.join(keep))
            continue
        if kind == 'pairs':
            if announced:
                out.append("%s [PAIR'S]: <yours> -- the previous pair's"
                           ' block follows as a model: rewrite it for this'
                           ' pair and delete this line\n%s' % (title, para))
                pairs.append(title)
            else:
                out.append(para)
            continue
        if kind in ('handover', 'gate'):
            # ONE SLOT PER BLOCK, not one per paragraph, and never its
            # CONTENT: a handover is spent with its run, and the previous
            # pair's gate verdict sits under GATE:.
            if not announced:
                continue
            if kind == 'gate':
                # The template's own GATE paragraph, VERBATIM and not as
                # scaffolding: `GATE: NOT RUN` is a live line of the note,
                # which run-status.sh and run-gate.sh both read, so
                # commenting it out would leave the draft's note with no
                # gate line at all. ONCE, however many gate blocks the
                # previous note accumulated -- Run 26's had three, its own
                # `GATE:` line, the hand verdict and run-gate.sh's appended
                # block, and one slot each would have given the new note
                # three gate lines to reconcile.
                if not gate_done:
                    gate_done = True
                    out.append(_template_gate(
                        os.path.dirname(os.path.abspath(path))))
                continue
            if kind == 'handover':
                # ONCE, however many handover blocks the previous note
                # accumulated -- the rule the gate keeps just above, for
                # the same reason and missed here because the slot NAME is
                # fixed rather than the title's, so the duplicates come out
                # identical and read as a template asking to be filled in
                # three places. A handover is ONE block of the note; the
                # previous note's runs to several paragraphs, and the
                # splitter announces more than one of them -- Run 29's
                # handover is a single heading over nine paragraphs, three
                # of which arrived here announced, so Run 30's draft opened
                # with the same slot and the same scaffolding three times
                # (2026-09-13).
                if handover_done:
                    continue
                handover_done = True
            slot = ('ENTRY POINT FOR THE SESSION THAT RUNS THIS'
                    if kind == 'handover' else title)
            out.append('%s [PAIR\'S]: <yours>\n%s'
                       % (slot, _scaffold(guide.get(slot))))
            pairs.append(slot)
        elif kind == 'fill':
            # THE GATE LINE GOES IN FRONT OF THE FILL-IN BLOCK IF NOTHING
            # HAS EMITTED IT, which is where the template puts it. Driving
            # it off the previous note's gate blocks alone made it
            # conditional on that note having had one, so a previous note
            # written before run-gate.sh ever appended -- or one whose gate
            # line somebody removed -- would have drafted a note with NO
            # gate at all, which is the one line run-status.sh reads for
            # step 14 and the one that says the pair has no gate yet.
            if not gate_done:
                gate_done = True
                out.append(_template_gate(
                    os.path.dirname(os.path.abspath(path))))
            out.append(_fill_skeleton(para))
        else:
            out.append(para)          # [SAME] and the unmarked header lines
    if not gate_done:
        out.append(_template_gate(os.path.dirname(os.path.abspath(path))))
    body = '\n\n'.join(out)
    # The header line carries the previous run's NUMBER and its build DATE,
    # which no rename touches and which would otherwise be the one place a
    # draft states something false about this pair. Back to the template's
    # own placeholders, so they read as slots.
    body = re.sub(r"Run \d+'s, written by hand \d{4}-\d\d-\d\d",
                  "Run NN's, written by hand YYYY-MM-DD", body)
    log = []
    # ONE PASS PER FAMILY, longest pattern first, because renaming in turn
    # feeds each result to the next rename: with old (g912, spot) and new
    # (spot, ghead), `g912` became `spot` and the second rename took that
    # to `ghead`, collapsing BOTH halves onto one name in a note carried
    # over silently. Found 2026-09-03 by trying a pair that reuses a name.
    ren = {'%s-%s' % (prev, o): '%s-%s' % (draft, n)
           for o, n in zip(old, new)}
    ren[prev] = draft
    seen = {}
    ren_rx = re.compile('|'.join(re.escape(k) for k in
                                 sorted(ren, key=len, reverse=True)))
    body = ren_rx.sub(
        lambda mo: (seen.__setitem__(mo.group(0),
                                     seen.get(mo.group(0), 0) + 1),
                    ren[mo.group(0)])[1], body)
    log += ['%s -> %s (%d)' % (k, ren[k], c)
            for k, c in seen.items() if ren[k] != k]
    bare = {o: n for o, n in zip(old, new) if o != n}
    if bare:
        # NOT a plain word boundary: `-` is one, so a bare `spot` would
        # match inside `dead-spot` and rename the FORM the pair varies.
        # A BACKTICK BOUNDS IT TOO, and for a different reason: a `[SAME]`
        # block names a half because this PAIR has it, spelled bare, and
        # names one because the chapter once did, spelled in backticks --
        # the roll under NAMING THE HALVES being the second kind. Renamed,
        # that roll comes back a well-formed list with two members
        # replaced by tags that did not exist before this run, which no
        # checker reads and the next draft carries again. Run 29's
        # preparation caught it by reading the substitution log; the
        # boundary makes it mechanical (2026-09-12).
        bseen = {}
        body = re.compile(r'(?<![\w`-])(%s)(?![\w`-])'
                          % '|'.join(re.escape(o) for o in
                                     sorted(bare, key=len, reverse=True))).sub(
            lambda mo: (bseen.__setitem__(mo.group(1),
                                          bseen.get(mo.group(1), 0) + 1),
                        bare[mo.group(1)])[1], body)
        log += ['bare %s -> %s (%d)' % (k, bare[k], c)
                for k, c in bseen.items()]
    body = re.sub(r'^HALVES:.*$', 'HALVES: basis=%s other=%s' % new,
                  body, flags=re.M)
    # THE COMPARE LINE IS NEVER CARRIED. It names the earlier run a pair is
    # read against, which is the run drafted from unless a ruling picks
    # another, and a ruling is that pair's: Run 34's `COMPARE: run32` was.
    # So the draft names the run it is drafted from, under HALVES where
    # the old note had no line, and the scan below skips the line.
    if re.search(r'^COMPARE:', body, re.M):
        body = re.sub(r'^COMPARE:.*$', 'COMPARE: %s' % prev, body,
                      flags=re.M)
    else:
        body = re.sub(r'^(HALVES:.*)$', r'\1\nCOMPARE: %s' % prev, body,
                      count=1, flags=re.M)
    # A CARRIED BLOCK THAT NAMES ANOTHER RUN IS FLAGGED WHERE IT SITS.
    # The renames above map the PREVIOUS run onto this one and touch no
    # other number, so a `[SAME]` block quoting `run26-g912` as the
    # previous build of a recipe, or Run 26's counts totals, or the
    # fingerprint's run, comes through pointing one run too far back --
    # and it reads as carried-over-correctly, every name in it having
    # been substituted. Run 28's preparation caught three that way by
    # reading, which is what the header asks for and not what it can
    # count on; this makes the same finding mechanical. Marked and never
    # changed: which of them is stale is the preparation's to decide,
    # a block MAY name an older run rightly, and a draft that edited
    # prose would be deciding for it (2026-09-10).
    # PLURAL AND RANGE FORMS TOO. `[Rr]un ?(\d+)` alone reads nothing out
    # of `as Runs 24 to 27 were`, so a block whose only older-run mention
    # is plural went unflagged and a flagged block's list was short of
    # what it names (2026-09-10).
    # AND A CARRIED BLOCK THAT ASSERTS A COMPILE OPTION IS FLAGGED TOO,
    # which the run-number test does not reach and which fails differently:
    # an old run number points one run too far back and may be right, where
    # a flag name in a carried block is a claim about THIS pair's regime and
    # goes false the moment the variable changes. Run 31's draft carried
    # `NEITHER half carries -fspec-constr` onto a pair whose other half is
    # built at -O2, which turns that pass on -- false of the pair it was
    # carried to, and reached by no test of its own, its block being flagged
    # for its run numbers instead (2026-09-14). Marked and never changed, as
    # above. RTS options are deliberately NOT matched, reaching the runtime
    # and not the optimiser -- which is a design point and not a case this
    # has met: no `[SAME]` block of run30-pair.txt names one.
    mine = re.search(r'(\d+)', draft)
    mine = mine.group(1) if mine else draft
    flagged = []
    for para in body.split('\n\n'):
        lead = para.lstrip('\n').split('\n', 1)[0]
        if '[SAME' not in lead:
            continue
        nums = set(re.findall(r'run(\d+)',
                              re.sub(r'^COMPARE:.*$', '', para, flags=re.M)))
        for m in re.finditer(r'[Rr]uns?\s+\d+(?:\s*(?:to|and|,|--)\s*\d+)*',
                             para):
            nums |= set(re.findall(r'\d+', m.group(0)))
        old_runs = sorted({n for n in nums if n != mine}, key=int)
        opts = sorted(set(re.findall(r'(?<![-\w])-(?:f[a-z][\w-]*|O\d)',
                                     para)))
        if old_runs or opts:
            # AND THE LINES THEMSELVES, not the block alone. A flagged
            # block runs to a dozen lines and what is stale in it is one
            # clause or two, so a preparation told only the title reads
            # the whole block back looking for what this notice has
            # already located. Run 35's draft flagged five blocks and
            # every rewrite it wanted was a sentence inside one
            # (2026-09-18). Located and never changed, as above: which
            # line is stale is still the preparation's to decide.
            # BOTH SPELLINGS, since the two fail differently: `Run 33`
            # in prose, where the number stands alone, and `run33-exit`
            # in a name, where it is preceded by a word character and a
            # bare-number pattern never fires -- which is the half a
            # carried block quotes a previous build by.
            hits = [l.strip() for l in para.split('\n')
                    if any(('run%s' % n) in l
                           or re.search(r'(?<![\w.])%s(?![\w.])' % n, l)
                           for n in old_runs)
                    or any(o in l for o in opts)]
            flagged.append((_note_title(lead), old_runs, opts, hits))
    if flagged:
        rows = []
        for t, r, o, hits in flagged:
            why = []
            if r:
                why.append('names %s %s'
                           % ('Runs' if len(r) > 1 else 'Run', ', '.join(r)))
            if o:
                why.append('asserts %s' % ', '.join(o))
            rows.append('#   %-44s %s' % (t[:44], ' and '.join(why)))
            for h in hits[:4]:
                rows.append('#     | %s' % h[:64])
            if len(hits) > 4:
                rows.append('#     | ... and %d more line(s) in that block'
                            % (len(hits) - 4))
        marks = '\n'.join(rows)
        body = ('# CHECK THESE CARRIED BLOCKS: each names a run this draft'
                ' did not rename, or\n# asserts a compile option -- so a'
                ' figure in it may be one run too far back,\n# and a clause'
                ' about the regime may be false for this pair. Read them\n#'
                ' against this pair before deleting this notice.\n%s\n\n%s'
                % (marks, body))
    for key, para in fills.items():
        body = body.replace(key, _same_filled(para, draft, new, env, machine))
    if from_template:
        notice = ['# FROM THE TEMPLATE and not from %s: %s. The previous'
                  ' note\'s LAUNCH and RIDERS values are carried into them.'
                  % (os.path.basename(path), '; '.join(from_template))]
        if dropped:
            notice.append('# DROPPED WITH THEIR BLOCK, the paragraphs that'
                          ' ran on under one the template replaced -- move'
                          ' any that is this pair\'s into a [PAIR\'S] block:')
            notice += ['#   %-28s | %s' % (t[:28], l) for t, l in dropped]
        body = '\n'.join(notice) + '\n\n' + body
    print('# DRAFT for %s-pair.txt, the WHOLE note: [SAME] blocks from the'
          ' template or %s,' % (draft, os.path.basename(path)))
    print('# each [PAIR\'S] block under a <yours> line with the previous'
          ' pair\'s text as a')
    print('# model, the handover and the fill-in empty. Redirect it, rewrite'
          ' each model and')
    print('# delete its <yours> line, fill the rest, delete the `#`'
          ' scaffolding, and that')
    print('# is the note -- one file edited rather than three assembled.')
    print('# READ EVERY LINE CARRIED FROM THE NOTE: it is a copy with names'
          ' changed, to be')
    print('# re-read rather than re-decided; where one no longer holds, the'
          ' note says why.')
    print('#')
    print('# Substituted: %s' % ('; '.join(log) or 'nothing'))
    print('#')
    print('# YOURS TO WRITE, each a <yours> slot below -- the decisions,'
          ' which no')
    # THE SAME RENAME THE BODY GOT, and not the run number's alone: the
    # titles here are the PREVIOUS note's, so a block led `THE BASIS IS
    # run29-spec` came out of this list as `THE BASIS IS run30-spec` --
    # a half this pair does not have -- while the body's own heading, two
    # lines down in the same output, read `run30-nospec`. One map, applied
    # in both places (2026-09-13).
    print('# draft may carry: %s'
          % ('; '.join(ren_rx.sub(lambda mo: ren[mo.group(0)], p)[:56]
                       for p in pairs) or 'none'))
    print('# The fill-in block is <yours> per row too, and'
          ' `preflight.sh %s --fill-in`' % draft)
    print('# derives most of them off the binaries once they are built.')
    print()
    print(body.rstrip('\n'))
    return 0


# The run chapter's three checklists, each an indented block, found by
# its own first line rather than by a heading or a line number: the lists
# are what a session executes and the prose around them is the reasons,
# so this prints one list alone, sized, the way --section prints a
# section without its tables. Run 23 read the lists inside 2600 lines of
# chapter for want of it (2026-09-02).
CHECKLISTS = {
    'pre': "# READ THIS LIST AND THE LAST RUN'S FILE, AND START.",
    'run': 'grep -i gate $R-pair.txt',
    'post': '#   0. NAME THE FILL GROUPS',
    # The list of what a session READS, which every step names by item
    # number and which sat among the reasons at the chapter's foot. Case:
    # `checklist-prints-the-readings-list`.
    'readings': "1. this chapter's three checklists",
}

# THE POST LIST'S EXECUTION ORDER, which is not the order it prints in.
# The numbers are stable on purpose -- pointers in both documents and in
# several tools resolve to them -- so a step that runs out of turn keeps
# its number and each says why in its own text: 0 after 1, 2 and 3 by
# its `FIRST MEANS BEFORE 11 AND NOT BEFORE 1`, 9 and 10 before 6d by
# their own first words, 10a with the readings of 4, which is where
# post-run-readings.sh takes it and where step 4 says it is taken.
# Saying it once here is what a session gets BEFORE step 0 rather
# than at step 9. Declared and not derived: the reasons are
# prose and no pattern reads them. Added 2026-09-20, after Run 37 took
# 9 and 10 in printed order and recorded the deviation in its own
# post-mortem.
POST_EXEC = ['1', '2', '3', '0', '4', '4a', '4b', '10a', '5', '5a',
             '5b', '5c', '9', '10', '6', '6a', '6b', '6c', '6d', '6e',
             '7', '7a', '8', '10b', '10c', '11']


def _exec_order(block, whole=False):
    """The post list's execution order against its printed one.

    Returns (order, moved, mismatch). `moved` is the smallest set of
    steps that has to move, read off the longest common subsequence of
    the two orders rather than by comparing positions, which would name
    most of the list. A step in the block and not in POST_EXEC, or the
    reverse, comes back in `mismatch` and the banner is not printed:
    this is a second statement of the list's shape, so it fails loudly
    when the list moves under it instead of printing a stale order.
    """
    printed = []
    for line in block:
        m = re.search(r'#\s{0,4}(\d+[a-z]?)\.\s', line)
        if m and m.group(1) not in printed:
            printed.append(m.group(1))
    want = [n for n in POST_EXEC if n in printed]
    # BOTH DIRECTIONS, and only the second needs `whole`: a half prints
    # part of the list, so POST_EXEC holding steps it lacks is ordinary
    # there and a fault on the whole list. Until 2026-09-20 the test was
    # `printed` against a subset of itself, which could only ever catch
    # a step ADDED to the README and never one deleted from it, while
    # the sentence above claimed both.
    gone = set(POST_EXEC) - set(printed) if whole else set()
    if set(printed) - set(POST_EXEC) or gone:
        return None, None, sorted((set(printed) - set(POST_EXEC)) | gone)
    sm = difflib.SequenceMatcher(None, printed, want)
    kept = set()
    for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
        if tag == 'equal':
            kept.update(printed[i1:i2])
    return want, [n for n in want if n not in kept], []

# The post list alone is longer than the other two together, and it has a
# seam: nothing from step 6 on is actionable until 5b's tables are in, so a
# session reading it whole reads half of it hours before it can act. `post-a`
# stops where the installs end and `post-b` starts at the walk. Both are cut
# out of the one block, so there is no second copy to keep in step, and
# `post` still prints it entire for a reader who wants it. Added 2026-09-05,
# after Run 25 read 412 lines at once and then re-read most of them at their
# steps.
POST_SPLIT = '    #   6. walk the replace list under Provenance'

# THE PRE LIST HAS THE SAME SEAM AND IT WAS NOT CUT until 2026-09-13: its
# steps 0 to 10 decide the pair, build it and check it, and nothing from 11
# on can be started until preflight's 4,5 has passed on binaries that exist
# -- so a preparation reading the whole 578 lines at step 0 reads the sweeps
# and the registration before it has a note. Cut where the machine time
# starts, which is the same place the half's own length is decided.
PRE_SPLIT = '    ./smoke-sweep.sh $R '

SPLITS = {'pre': PRE_SPLIT, 'post': POST_SPLIT}

# THE DOCSTRING IS READ IN PARTS, which is what the run chapter's pre-run
# step 7 asks for: it names `the Modes list, --para, --section and the two
# gates`, and the whole docstring was the only way to the PROSE of any of
# them, which a preparation then carries for the rest of its session.
# `--help` is the other route and reaches the mode NAMES, so what this
# saves is measured rather than total: `--doc modes` is the smallest of the
# three, under `--help`, which is itself well under the docstring entire.
# The cuts are the docstring's OWN lead lines, so that no part is named for
# a heading it does not open, `intro` being what stands before the first
# cut and named for that; a paragraph moved across a
# cut moves its part with it, and a lead that is no longer there refuses at
# 2 rather than silently merging two parts, since a part that quietly
# absorbed its neighbour reads exactly like a part that was always that
# long (2026-09-14).
DOC_PARTS = [
    ('intro', None),
    ('definitions', 'Definitions, once:'),
    ('modes', 'Modes:'),
    ('partial', 'A run artifact is made when a question needs it'),
    ('validation', 'Validation:'),
]


def doc_part(which=None):
    """Print one named part of this script's docstring, or list them."""
    lines = (__doc__ or '').split('\n')
    starts = []
    for name, lead in DOC_PARTS:
        if lead is None:
            starts.append((name, 0))
            continue
        at = next((i for i, ln in enumerate(lines)
                   if ln.startswith(lead)), None)
        if at is None:
            print('--doc: the part `%s` is cut at `%s`, which the docstring'
                  ' no longer carries; the parts are stale' % (name, lead),
                  file=sys.stderr)
            return 2
        starts.append((name, at))
    parts = []
    for i, (name, at) in enumerate(starts):
        end = starts[i + 1][1] if i + 1 < len(starts) else len(lines)
        parts.append((name, '\n'.join(lines[at:end]).strip('\n')))
    if not which:
        print("read-run.py's docstring in parts; --doc NAME prints one,"
              ' and the two gates are in `modes`')
        for name, text in parts:
            print('  %-12s %2d paragraph(s), %5d chars'
                  % (name, text.count('\n\n') + 1, len(text)))
        return 0
    for name, text in parts:
        if name == which:
            print(text)
            return 0
    print('--doc: no part `%s`; --doc alone lists them' % which,
          file=sys.stderr)
    return 2


def checklist(readme, which, steps_only=False):
    """Print one of the run chapter's three checklists, and nothing else."""
    half = None
    if which[-2:] in ('-a', '-b') and which[:-2] in SPLITS:
        which, half = which[:-2], which[-1]
    if which not in CHECKLISTS:
        sys.stderr.write('--checklist: one of %s, not %r\n'
                         % ('|'.join(list(CHECKLISTS)
                                     + [k + h for k in SPLITS
                                        for h in ('-a', '-b')]), which))
        return 1
    try:
        lines = open(readme).read().split('\n')
    except OSError as e:
        sys.stderr.write('--checklist: %s\n' % e)
        return 2
    first = CHECKLISTS[which]
    starts = [i for i, l in enumerate(lines)
              if l.startswith('    ') and l.strip().startswith(first)]
    if len(starts) != 1:
        sys.stderr.write('--checklist %s: its first line %r occurs %d times in'
                         ' %s, need 1\n' % (which, first, len(starts),
                                            os.path.basename(readme)))
        return 1
    i = starts[0]
    # Back up to the block's own first line, then run to its last: an
    # indented block ends at the first line that is neither indented nor
    # blank, and trailing blanks are not part of it.
    while i > 0 and lines[i - 1].startswith('    '):
        i -= 1
    j = i
    while j + 1 < len(lines) and (lines[j + 1].startswith('    ')
                                  or lines[j + 1] == ''):
        j += 1
    while lines[j] == '':
        j -= 1
    block = lines[i:j + 1]
    label = {'pre': 'pre-run', 'run': 'run', 'post': 'post-run',
             'readings': 'readings'}[which]
    steps = ''
    if half:
        cut = [k for k, l in enumerate(block) if l.startswith(SPLITS[which])]
        if len(cut) != 1:
            sys.stderr.write('--checklist %s-%s: its seam %r occurs %d'
                             ' times in the %s list, need 1\n'
                             % (which, half, SPLITS[which].strip(), len(cut),
                                which))
            return 1
        if half == 'a':
            block, j = block[:cut[0]], i + cut[0] - 1
        else:
            block, i = block[cut[0]:], i + cut[0]
        # read off the half rather than naming its ends here, a step
        # added or renumbered otherwise leaving this label behind
        # A STEP IS NOT ALWAYS AT THE LINE'S HEAD: the pre list writes
        # 4 and 11 after their commands, so anchoring at column five
        # read pre-b as starting at 12 when it starts at 11.
        nums = [m.group(1) for l in block
                for m in [re.search(r'# {1,3}(\d+[a-z]?)\.', l)]
                if l.startswith('    ') and m]
        if nums:
            steps = ', steps %s to %s' % (nums[0], nums[-1])
    print('%s: the %s checklist%s, %d lines, %d KB, README.md lines %d to %d'
          % (os.path.basename(readme), label, steps, len(block),
             len('\n'.join(block)) // 1024, i + 1, j + 1))
    print()
    # THE DEFAULT IS THE IMPERATIVE FORM, and --full the annotated one.
    # A step is what its lines say before its `why:` line, which prints
    # as the pointer to the reasons; the lines after it are the reasons
    # and are skipped until the next step's head or a command line. The
    # lines before a list's first step print too, which is where a list
    # states its rules. The run chapter keeps each step's action above
    # its `why:` so that this cut is the whole of the derivation. Cases:
    # `checklist-steps-prints-the-imperative-half`,
    # `checklist-default-stops-at-why`.
    if steps_only:
        kept, quiet = [], False
        for l in block:
            if not l.strip():
                continue
            if (re.match(r'^ {4}#? {0,3}\d+[a-z]?\.', l)
                    or not l.strip().startswith('#')):
                quiet = False
            if not quiet:
                kept.append(l)
            if re.match(r'^ {4}#\s+why:', l):
                quiet = True
        block = kept
        if which == 'post':
            order, moved, mismatch = _exec_order(block, whole=half is None)
            if mismatch:
                sys.stderr.write(
                    '--checklist %s: POST_EXEC and the list'
                    ' disagree on %s, so no execution order is printed --'
                    ' a step moved and this constant did not\n'
                    % (which, ', '.join(mismatch)))
            else:
                print('    # EXECUTION ORDER, which is NOT the order below:')
                print('    #   %s' % ' '.join(order))
                if moved:
                    print('    #   %s %s out of printed turn, saying why in'
                          ' its own text.'
                          % (', '.join(moved),
                             'runs' if len(moved) == 1 else 'run'))
                print()
    print('\n'.join(block))
    return 0


# The series README kept as prose, one run's reading appended per run:
# data in series/*.tsv, each opening with `#` lines that say what its
# columns are, and the prose saying what the series shows. Case:
# `record-prints-a-series-aligned`.
SERIES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'series')


def record(name):
    """Print series/NAME.tsv aligned, or list the series with none."""
    try:
        names = sorted(f[:-4] for f in os.listdir(SERIES_DIR)
                       if f.endswith('.tsv'))
    except OSError as e:
        sys.stderr.write('--record: %s\n' % e)
        return 2
    if not name:
        print('series/, one table per series; --record NAME prints one')
        for n in names:
            print('  ' + n)
        return 0
    if name not in names:
        sys.stderr.write('--record: no series/%s.tsv; one of %s\n'
                         % (name, ', '.join(names)))
        return 2
    notes, rows = [], []
    for line in open(os.path.join(SERIES_DIR, name + '.tsv')):
        line = line.rstrip('\n')
        if line.startswith('#'):
            notes.append(line)
        elif line:
            rows.append(line.split('\t'))
    ragged = [r[0] for r in rows[1:] if len(r) != len(rows[0])]
    if not rows or ragged:
        sys.stderr.write('--record %s: rows %s do not have the header\'s'
                         ' %d columns\n' % (name, ', '.join(ragged),
                                             len(rows[0]) if rows else 0))
        return 1
    widths = [max(len(r[k]) for r in rows) for k in range(len(rows[0]))]
    print('\n'.join(notes))
    for r in rows:
        print('  '.join(c.rjust(w) for c, w in zip(r, widths)).rstrip())
    return 0


def move_registration(readme, run_doc):
    """Move the run's registration from README's open list into the run
    file's last section, leaving the ANSWERED stub in its place.

    The registration is written into the open list before the run, where
    a prediction has to be public, and lives in the run file after it,
    with its verdicts -- so every write-up hand-copied six predictions
    and their figures from one to the other, which is the two-copies
    problem the open list's own pointer form was meant to avoid (Run 23,
    2026-09-02). This does the move: the entry's text, less its lead,
    becomes the section's body under a one-line preface, and the entry
    becomes the stub every ANSWERED run entry has -- lead, pointer, and a
    `___` where the clause of verdicts goes. It refuses unless exactly
    one OPEN entry names this run, and prints what it moved.
    """
    n = run_no_of(run_doc)
    if n is None:
        sys.stderr.write('--move-registration: %s is not a run file\n'
                         % run_doc)
        return 1
    try:
        rd = open(readme).read()
        doc = open(run_doc).read()
    except OSError as e:
        sys.stderr.write('--move-registration: %s\n' % e)
        return 2
    lead = ('- `OPEN` **What Run %d is built to answer, registered before'
            ' it runs.**' % n)
    # The open list's items are not blank-line separated, so the unit is
    # a LINE of the unwrapped form, one item apiece; the form the file
    # was in is restored on the way out.
    def wrap80(text, unwrap):
        cmd = ['wrap80', '--unwrap'] if unwrap else ['wrap80']
        got = subprocess.run(cmd, input=text, capture_output=True,
                             text=True)
        if got.returncode != 0:
            sys.exit('--move-registration: %s exited %d: %s'
                     % (' '.join(cmd), got.returncode, got.stderr.strip()))
        return got.stdout
    # A wrapped document is wrap80's fixed point, so the form is read by
    # asking the tool rather than by a line length, which a table row
    # exceeds in either form.
    was_wrapped = wrap80(rd, unwrap=False) == rd
    lines = wrap80(rd, unwrap=True).split('\n')
    hit = [i for i, q in enumerate(lines) if q.startswith(lead)]
    if len(hit) != 1:
        sys.stderr.write('--move-registration: %d OPEN entr%s for Run %d in'
                         ' %s, need 1 -- the lead is %r\n'
                         % (len(hit), 'y' if len(hit) == 1 else 'ies', n,
                            os.path.basename(readme), lead))
        return 1
    body = lines[hit[0]][len(lead):].strip()
    # The registration is AUTHORED where a bare `](#section)` resolves and
    # READ one directory down, where it does not. Nothing else knows the
    # text crossed a directory, so the move repoints them: --check-doc
    # catches what is left, which costs a minute a run rather than a run.
    body = body.replace('](#', '](../%s#' % os.path.basename(readme))
    # ONE PARAGRAPH PER ITEM since 2026-09-11. The registration arrived as a
    # single line -- 35,160 characters on Run 28, which the mode's own
    # `chars moved` line reports -- while every class block
    # and every verdict cites `registration (N)`, so looking one up was a
    # scan of the whole with nothing to jump to. Run 28's comprehension
    # probe raised it as its one structural finding and that run's own
    # write-up raised it independently, which is two readers on the same
    # defect and the reason it is fixed at the MOVE rather than by hand
    # afterwards: the hand copy is what this mode exists to abolish.
    # Split before each ` (N) *`, the form an item's lead has taken since
    # Run 18. A body carrying no such marker is left WHOLE, so a
    # registration written some other way is moved exactly as it was
    # rather than mangled by a pattern that does not fit it.
    if re.search(r' \(\d+\) \*', body):
        body = '\n\n'.join(q.strip() for q in
                            re.split(r'(?= \(\d+\) \*)', body) if q.strip())
    if REG_HEAD not in doc:
        sys.stderr.write('--move-registration: %s has no `%s` heading\n'
                         % (os.path.basename(run_doc), REG_HEAD))
        return 1
    if doc.count(REG_HEAD) != 1:
        sys.stderr.write('--move-registration: the heading occurs %d times'
                         ' in %s\n' % (doc.count(REG_HEAD),
                                        os.path.basename(run_doc)))
        return 1
    head_at = doc.index(REG_HEAD)
    old_tail = doc[head_at + len(REG_HEAD):]
    preface = ('Registered in README\'s open list on the date the entry'
               ' carries, before the run, and moved here whole at post-run'
               ' step 5; the verdicts are the write-up\'s to add beside each'
               ' prediction, and the summary sentence its to write.')
    new_doc = (doc[:head_at] + REG_HEAD + '\n\n' + preface + '\n\n' + body
               + '\n')
    stub = ('- `ANSWERED` **What Run %d was built to answer, registered'
            ' before it ran --- and what it answered.** The registrations,'
            ' their kill conditions and their verdicts are [in Run %d\'s own'
            ' file](%s/run%d.md#what-this-run-was-built-to-answer-and-what-it'
            '-answered), where a run\'s registrations have lived since'
            ' 2026-08-29; in a clause each: ___.' % (n, n, RUNS_DIR, n))
    lines[hit[0]] = stub
    out = '\n'.join(lines)
    if was_wrapped:
        out = wrap80(out, unwrap=False)
    with open(run_doc, 'w') as f:
        f.write(new_doc)
    with open(readme, 'w') as f:
        f.write(out)
    print('--move-registration: %d chars moved from %s to %s'
          % (len(body), os.path.basename(readme), os.path.basename(run_doc)))
    print('  the run file\'s last section replaced, %d chars out, the'
          ' registration in under a one-line preface' % len(old_tail))
    print('  README\'s entry is the ANSWERED stub with `___` for the verdict'
          ' clause; --check-doc holds the stub to the same word limit as'
          ' every other')
    return 0


def excise(docs, anchor, limit=1500):
    """Delete the paragraph carrying `anchor`, refusing anything larger.

    `--replace` exists so a paragraph is NAMED rather than sliced, and
    deletion had no such mode -- so removing one fell back to hand-rolled
    index arithmetic, `s.find(lead)` for the start and `s.find('\n\n')`
    for the end. That is the one shape the user-scope rules call
    unwatchable: a range splice between two markers deletes everything
    between them, however much that turns out to be, and every checker
    here is a predicate over what is PRESENT, so none can see what went.

    Measured 2026-08-26, in this reader's own run file: an end anchor
    that matched a later paragraph took **148936 characters**, leaving 41
    lines of a 908-line document, and the script printed the extent and
    the last line it was about to cut -- text from a different paragraph
    entirely -- and was read past. The echo was not enough, exactly as it
    was not enough for the list guard above; this is the refusal that
    replaces it.

    So: the anchor must occur exactly once across the pair of documents,
    the unit is the blank-line paragraph containing it, and the paragraph
    must be under `limit` characters. A list is refused outright -- a
    numbered list is one paragraph, and dropping one item is an edit, not
    a deletion. What it prints is what it removed, first line and last.
    """
    if isinstance(docs, str):
        docs = [docs]
    seen = []
    for path in docs:
        try:
            text = open(path).read()
        except OSError as e:
            sys.stderr.write('--delete: %s\n' % e)
            return 2
        seen.append((path, text, flat(text).count(flat(anchor))))
    total = sum(k for _, _, k in seen)
    if total != 1:
        sys.stderr.write('--delete: the anchor occurs %d times across %s,'
                         ' need 1 -- quote more of the sentence\n'
                         % (total, ', '.join('%s (%d)'
                                             % (os.path.basename(q), k)
                                             for q, _, k in seen)))
        return 1
    path, doc, _ = next(t for t in seen if t[2])
    paras = doc.split('\n\n')
    hit = [i for i, q in enumerate(paras) if flat(anchor) in flat(q)]
    if len(hit) != 1:
        sys.stderr.write('--delete: the anchor spans a paragraph break, so'
                         ' there is no one paragraph to delete\n')
        return 1
    old = paras[hit[0]]
    items = [l for l in old.split('\n')
             if re.match(r'\s*(?:\d+\.|[-*])\s', l)]
    if len(items) > 1:
        sys.stderr.write(
            '--delete: this paragraph is a %d-item list, and dropping one'
            ' item is an edit rather than a deletion -- use --replace with'
            ' the whole list\n' % len(items))
        return 1
    if len(old) > limit:
        sys.stderr.write(
            '--delete: REFUSED, the paragraph is %d characters and the bar'
            ' is %d. A deletion this size is a section, not a paragraph;'
            ' if it is really meant, say so with --delete-limit\n'
            % (len(old), limit))
        return 1
    ol = old.split('\n')
    print('--delete: %d chars, from %s' % (len(old), os.path.basename(path)))
    print('  out, first: %s' % ol[0][:78])
    print('  out, last : %s' % ol[-1][-78:])
    del paras[hit[0]]
    with open(path, 'w') as f:
        f.write('\n\n'.join(paras))
    return 0


def paragraph_at(docs, where):
    """Resolve FILE:LINE to the paragraph holding it, and print its HANDLE.

    A line number into prose is perishable: the formatter rewraps at every
    commit, an `--in-place` install moves everything under it, and a Stop
    hook can move it between one turn and the next. A bolded lead is not,
    which is why `--para` matches leads -- but `--para` needs a lead the
    caller already knows, and a caller who has just grepped has a LINE
    NUMBER and nothing else. That gap is why sessions keep pairing `grep
    -n` with `sed -n`: not because the chapter fails to recommend `--para`
    but because the thing in hand is not what `--para` takes. This mode is
    the converter, and its output is the handle rather than the passage --
    what a caller should carry forward instead of the number it arrived
    with.

    The line is counted in the file AS IT IS ON DISK, which is what a grep
    reports, and the paragraph is what `wrap80 --unwrap` says it is, which
    is what every sweep here reads; `spans` is the map between them and
    already existed for placing a match.
    """
    if isinstance(docs, str):
        docs = [docs]
    m = re.match(r'(.+):(\d+)$', where)
    if not m:
        sys.stderr.write('--para-at wants FILE:LINE, e.g. README.md:2799;'
                         ' got %r\n' % where)
        return 2
    want, no = m.group(1), int(m.group(2))
    cands = [d for d in docs if os.path.basename(d) == os.path.basename(want)]
    if not cands:
        cands = [d for d in docs if want in d]
    if len(cands) != 1:
        sys.stderr.write('--para-at: %r names %d of the documents this'
                         ' reads (%s)\n'
                         % (want, len(cands), ', '.join(docs)))
        return 2
    path = cands[0]
    try:
        lines = open(path).read().split('\n')
    except OSError as e:
        sys.stderr.write('--para-at: %s\n' % e)
        return 2
    if not 1 <= no <= len(lines):
        sys.stderr.write('--para-at: %s has %d lines, so %d is outside it\n'
                         % (os.path.basename(path), len(lines), no))
        return 2
    paras_all = []
    for d in docs:
        try:
            dl = open(d).read().split('\n')
        except OSError:
            continue
        paras_all += [(d, f, q) for f, q, _ in unwrapped_paragraphs(dl)]
    for first, para, spans in unwrapped_paragraphs(lines):
        nums = [n for n, _ in spans] or [first]
        if min(nums) <= no <= max(nums):
            lead = LEAD_RE.search(para)
            flat = ' '.join(lead.group(1).split()) if lead else ''
            print('%s:%d is in the paragraph starting at line %d, which'
                  ' spans %d line(s).' % (os.path.basename(path), no,
                                          min(nums), len(nums)))
            # THE HANDLE IS BUILT TO BE USED, not merely quoted: it is
            # fed back to `--para`, which takes a REGEX, so a lead's
            # backticks and asterisks are dropped -- `--para` strips them
            # from the lead before matching, and left in a pattern a `*`
            # is a quantifier -- and the trailing punctuation of a cut
            # phrase goes with them. Then it is LENGTHENED until it
            # matches one lead and no other, because a handle that
            # retrieves four paragraphs has not replaced the line number
            # it was meant to replace.
            src = flat or para
            words = re.sub(r'[`*]', '', src).split()
            # STARTS AT WHAT THERE IS, not at six: a lead of three words
            # -- and the shortest here is two -- left `short` unset and
            # handed back `--para ''`, which matches every paragraph in
            # both documents. An empty handle is worse than the line
            # number it replaces, the line number at least being wrong
            # only later.
            short = ' '.join(words).rstrip(' ,;:.-')
            for k in range(min(6, len(words)), min(len(words), 20) + 1):
                short = ' '.join(words[:k]).rstrip(' ,;:.-')
                try:
                    rx2 = re.compile(short, re.I)
                except re.error:
                    continue
                hits = 0
                for _p, _f, q in paras_all:
                    ld = LEAD_RE.search(q)
                    if ld and rx2.search(' '.join(ld.group(1).split())):
                        hits += 1
                if hits <= 1:
                    break
            if flat:
                print("  lead:   %s" % flat)
                print("  handle: --para %r" % short)
                print('  The handle survives a rewrap and an install; the'
                      ' line number survives neither. Carry it instead.')
            else:
                print('  lead:   none -- this paragraph carries no bolded'
                      ' lead, which many of the README\'s do not.')
                print("  handle: --para %r" % short)
                print('  `--para` falls back to the body when no lead'
                      ' matches, so that pattern still retrieves it.')
            print()
            print(para)
            return 0
    sys.stderr.write('--para-at: line %d of %s is in no paragraph -- a blank'
                     ' line, a heading or a table row, which the splitter'
                     ' drops\n' % (no, os.path.basename(path)))
    return 1


def _para_item(para, n):
    """One `(n)` item of a paragraph, or the whole of it and a note why.

    The items of a registration are `(1)` to `(11)` inline in one
    paragraph, so the span of item n runs to the `(n+1)` that follows it
    or to the paragraph's end. A paragraph with no such item is handed
    back WHOLE rather than empty: the caller asked for a passage and a
    silent nothing is the worst answer to that.
    """
    # THE ITALIC TITLE IS WHAT MAKES IT AN ITEM, and the reason to try it
    # first is that a registration's own PREAMBLE cites its items by
    # number: Run 30's opens by naming the two it amended, `(7) to within
    # 3%, and (11) re-based`, so a bare `\(7\)` matches the preamble and
    # returns the whole entry from there. Items read `(7) *Stage ten where
    # neither fires.*`; the loose form stays as a fallback for a paragraph
    # whose items carry no title, and is only reached when the titled form
    # matches nothing at all.
    def at(k, frm=0):
        return (re.compile(r'\(%d\)\s+\*' % k).search(para, frm)
                or re.compile(r'\(%d\)\s' % k).search(para, frm))
    k = int(n)
    start = at(k)
    if not start:
        return ('%s\n\n[--para: no item (%s) in this paragraph, so the whole'
                ' of it is above]' % (para, n))
    nxt = at(k + 1, start.end())
    return para[start.start():nxt.start() if nxt else len(para)].rstrip()


def _para_leads(paras, rx):
    """The paragraphs whose bolded lead matches, with and without markup."""
    hits = []
    for path, first, para in paras:
        lead = LEAD_RE.search(para)
        if not lead:
            continue
        flat = ' '.join(lead.group(1).split())
        if rx.search(flat) or rx.search(re.sub(r'[`*]', '', flat)):
            hits.append((path, first, para, flat))
    return hits


def paragraphs(docs, pattern, every=False):
    r"""Print the paragraphs whose BOLDED LEAD matches, and their line numbers.

    Retrieval, so that reading a paragraph does not mean finding it first.
    A session working through this README otherwise pairs a `grep -n` with a
    `sed -n` for every passage it wants, and both go stale the moment an
    edit above moves the lines -- which every `--in-place` install and every
    prose fix does. Matching the lead rather than the body is what keeps the
    output one paragraph instead of every line that mentions a word.

    **The README does NOT guarantee the precondition this used to claim.**
    It said every paragraph opens with a bolded lead; measured once, WELL
    OVER A THIRD carry none and dozens of those carry a figure. The four
    numerals that stood here are gone rather than maintained: nothing
    checks them, every run moves them -- the run written the day this
    sentence was rewritten added a hundred-odd paragraphs to README -- and
    the argument needs the SHARE and not the count. So a third of a percent
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

    **BOTH DOCUMENTS**, README.md and the run's own file, searched in that
    order and each hit labelled with the file it is in. Which of the two
    holds a paragraph is exactly what a caller does not know and must not
    have to find out first.
    """
    if isinstance(docs, str):
        docs = [docs]
    # `PATTERN#N` PRINTS ONE NUMBERED ITEM OF THE MATCHED PARAGRAPH, which
    # is what a registration wants: eleven items are ONE paragraph here, so
    # every look at item (7) costs the other ten, and a preparation looks
    # several times. An argument form rather than a flag, as `--para-at
    # FILE:LINE` is -- and `#` is the boundary because a lead may carry
    # anything else. N is the item's OWN number, the `(7)` a caller reads,
    # not an ordinal into the list (2026-09-13).
    item = None
    m = re.search(r'#(\d+)$', pattern)
    if m:
        item, pattern = m.group(1), pattern[:m.start()]
    # A LEAD PASTED VERBATIM IS THE ORDINARY CALL, and this argument is a
    # REGEX, so the two collide wherever a lead carries brackets -- which
    # every registration item's does. Compiled, `(9) *The floor...` matches
    # nothing and exits 0, reporting no such paragraph for one that is
    # demonstrably there; truncated to `(11` it raised re.error with a
    # stack. Try the pattern, fall back to the literal, and refuse a
    # pattern that is neither. Cases: `para-traceback-on-a-bracketed-lead`,
    # `para-refuses-an-uncompilable-pattern`.
    try:
        rx = re.compile(pattern, re.I)
    except re.error as e:
        try:
            rx = re.compile(re.escape(pattern), re.I)
        except re.error:
            sys.stderr.write('--para: %r is neither a usable regex (%s) nor'
                             ' matchable literally\n' % (pattern, e))
            return 2
    paras = []
    for path in docs:
        try:
            lines = open(path).read().split('\n')
        except OSError as e:
            sys.stderr.write('--para: %s\n' % e)
            return 2
        paras += [(path, first, para)
                  for first, para, _ in unwrapped_paragraphs(lines)]
    # AND IF THE REGEX MATCHES NOTHING, RETRY IT AS A LITERAL. A bracketed
    # lead compiles -- so the try above never fires -- and then matches
    # nothing, which is the quieter half of this defect: the caller is told
    # no such paragraph exists for one that is demonstrably there.
    lead_hits = _para_leads(paras, rx)
    if not lead_hits and re.escape(pattern) != pattern:
        lead_hits = _para_leads(paras, re.compile(re.escape(pattern), re.I))
        # MATCHED WITH ITS MARKUP AND WITHOUT IT. A caller quoting a lead
        # types what it reads, and a lead carrying backticks or italics
        # renders without them -- so `--para 'the three script-check
        # steps'` found nothing and fell through to the body, where it
        # matched the pointer line that named it and nothing else. The
        # pattern is a regex, so it is the LEAD that is stripped rather
        # than the pattern: stripping a `*` out of a pattern would eat a
        # quantifier.
    # ONE MATCH PRINTS WHOLE; SEVERAL PRINT AN INDEX. Retrieval is what this
    # mode is for, and a unique match is retrieved -- printing it costs the
    # caller nothing and a second call would cost a round trip for nothing.
    # Several matches are a different thing: the caller asked for one
    # passage and named a pattern that reaches four, so what it wants back
    # is which one to ask for. Run 19's `--para 'What Run'` returned four
    # registration entries whole, thousands of characters each, to be read
    # for one lead -- the largest single avoidable read of that session.
    #
    # And the index makes a trap visible that the wall of prose hid: this
    # mode matches open-list leads, so a run whose registrations live
    # elsewhere gets back its PREDECESSORS' and nothing of its own, which
    # reads as an empty registration. Four leads with run numbers in them
    # say that at a glance where four entries did not.
    if len(lead_hits) > 1 and not every:
        print('%d paragraph(s) whose lead matches %r; --all prints them,'
              ' or narrow the pattern to one:'
              % (len(lead_hits), pattern))
        for path, first, _para, lead in lead_hits:
            print('  %s:%d  %s'
                  % (os.path.basename(path), first, lead[:88]))
        return 0
    for path, first, para, _lead in lead_hits:
        print('%s:%d' % (os.path.basename(path), first))
        print(_para_item(para, item) if item else para)
        print()
    if lead_hits:
        return 0

    body = [(path, first, para) for path, first, para in paras
            if rx.search(para)]
    # THE LITERAL RETRY REACHES THE BODY TOO. A registration item's
    # paragraph opens with `(9) *The floor ...*` and no bolded lead at all,
    # so a caller pasting that lands here -- and as a regex it matches
    # nothing, which is the silent failure this fallback exists to end.
    if not body and re.escape(pattern) != pattern:
        lit = re.compile(re.escape(pattern), re.I)
        body = [(path, first, para) for path, first, para in paras
                if lit.search(para)]
    if not body:
        print('no paragraph whose bolded lead or body matches %r' % pattern)
        return 1
    print('no bolded lead matches %r; falling back to the body, where %d'
          ' paragraph(s) match:' % (pattern, len(body)))
    for path, first, para in body[:PARA_BODY_CAP]:
        print('%s:%d (body)' % (os.path.basename(path), first))
        print(para)
        print()
    if len(body) > PARA_BODY_CAP:
        print('... and %d more, not printed; narrow the pattern rather than'
              ' reading past the cap' % (len(body) - PARA_BODY_CAP))
    return 0


def heading_spacing_verdict(path, cur, bad, note):
    """Is every heading of one document preceded by TWO blank lines.

    The project's spacing, and a gate rather than a nicety because of
    what NONE costs: `--replace`'s unit is a blank-line paragraph, so a
    heading with no blank line above it belongs to the paragraph above
    it and goes out with it. That is the defect the open list records
    fixed on 2026-09-03, and Run 27 put it back into README with an
    off-by-one insert -- for a whole write-up, past --lint, --check-doc,
    every case and mutant, two independent checker passes and a
    comprehension probe. None of them could see it: the wrap pass asks
    about line length INSIDE a paragraph and never about what separates
    two, and the probe reads rendered prose, where the blank line is
    invisible. It was found by eye.

    ONE EXEMPTION AND NO OTHER: a heading on the document's first line,
    which has nothing to be preceded by. A heading directly under
    another is not exempt -- neither document has one, and if one lands
    it wants the same two lines as any other.
    """
    lines = cur.split('\n')
    for i, line in enumerate(lines):
        if i == 0 or not re.match(r'^#{1,6} ', line):
            continue
        n = 0
        j = i - 1
        while j >= 0 and lines[j] == '':
            n += 1
            j -= 1
        if n != 2:
            bad.append('%s:%d is preceded by %d blank line(s) and this'
                       ' project separates a heading by two: %s%s'
                       % (os.path.basename(path), i + 1, n, line[:60],
                          '' if n else ' -- with none it is part of the'
                          ' paragraph above it, which --replace would'
                          ' take out with it'))
            return
    note.append('every heading of %s is preceded by two blank lines'
                % os.path.basename(path))


def wrap_verdict(path, cur, bad, note):
    """Is one document as `wrap80` leaves it, paragraph by paragraph.

    ASKED OF EACH DOCUMENT SEPARATELY, README.md and the run's file,
    because being wrapped is a property of a file and the joined pair is
    not one: the two ends meet at a blank line that neither file has and
    neither would produce.
    """
    try:
        want = subprocess.run(['wrap80', path], capture_output=True,
                              text=True, check=True).stdout
        flat = subprocess.run(['wrap80', '--unwrap', path],
                              capture_output=True, text=True,
                              check=True).stdout
    except OSError:
        # A check that did not run must not read as one that passed.
        bad.append('BLOCKED: wrap80 is not on PATH, so the wrapping of'
                   ' %s was not checked at all' % os.path.basename(path))
    except subprocess.CalledProcessError as e:
        bad.append('BLOCKED: wrap80 failed (%d), so the wrapping of %s'
                   ' was not checked at all'
                   % (e.returncode, os.path.basename(path)))
    else:
        # `doc` was read once at the top and nothing above writes the
        # document, so the verdict is read against it rather than through
        # a second handle -- the wallclock_window family, 9e94c9d.
        if want == cur:
            note.append('no paragraph of %s is wrapped by hand'
                        % os.path.basename(path))
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
                    # in one write-up (2026-08-16), and naming `wrap80 -i` as
                    # the done-case fix taught the next to wrap for a check:
                    # the remedy is the unwrap, and the commit hook wraps a
                    # tracked document back (2026-09-02).
                    # AND THE LINE ITSELF, since 2026-09-22. `wrapped by
                    # hand` names the usual cause and not the only one: a
                    # line is flagged when it is in NEITHER form, and a
                    # long line can be in neither -- Run 38's open entry
                    # quoted a regex holding two literal spaces, which
                    # `--unwrap` collapses, so the line the file had was
                    # not the line either fixed point produces. The
                    # remedy named is right in both cases; the message
                    # sent a session hunting a wrapped paragraph that did
                    # not exist. Quoting the offender ends that in one read.
                    # `ok` above is the LOOP's, and by here it holds the
                    # last block's, not this one's -- so the set is rebuilt
                    # for the block being named. Watched 2026-09-22: the
                    # leaked binding named a line that holds nothing
                    # either form would change.
                    hb = hand[0]
                    hok = set(wp[hb].split('\n')) | set(fp[hb].split('\n'))
                    # Non-empty by construction: the block entered `hand`
                    # because a line of it was outside this very set.
                    off = [l for l in cp[hb].split('\n') if l not in hok]
                    bad.append('%d paragraph(s) of %s are wrapped by hand --'
                               ' first at line %d, whose first line in'
                               ' neither form is %r; unwrap it (`wrap80'
                               ' --unwrap -i %s`) and work there, the commit'
                               ' hook wrapping it back; `wrap80 -i` is for a'
                               ' file with no commit. Never re-wrap a line by'
                               ' hand'
                               % (len(hand), os.path.basename(path), at,
                                  off[0][:60] + ('...' if len(off[0]) > 60
                                                  else ''),
                                  os.path.basename(path)))
                else:
                    note.append('no paragraph of %s is wrapped by'
                                ' hand; %d still on one line, so it is'
                                ' mid-edit'
                                % (os.path.basename(path), len(loose)))
            else:
                # Diffed rather than compared by position: one inserted line
                # shifts every line under it, and reporting the whole file as
                # changed hides the one line worth looking at.
                d = list(difflib.unified_diff(cur.split('\n'),
                                              want.split('\n'),
                                              lineterm='', n=0))
                n = sum(1 for l in d
                        if l[:1] in '+-' and not l.startswith(('---', '+++')))
                at = next((m.group(1) for l in d
                           for m in [re.match(r'@@ -(\d+)', l)] if m), '?')
                bad.append('%s is not as wrap80 leaves it and its blocks do'
                           ' not line up with the formatter\'s (%d line(s),'
                           ' from line %s) -- unwrap it (`wrap80 --unwrap -i'
                           ' %s`) and the commit hook wraps it back'
                           % (os.path.basename(path), n, at,
                              os.path.basename(path)))


def check_doc(readme, main_hs, run_doc=None, prev_doc=None):
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
    form the scan reads. The two-column check: deleting one half's column
    from that table failed with the regime it still named, and deleting
    the table's header failed with the other message.

    TWO DOCUMENTS, read as one. The run's own write-up is
    `runs/run<N>.md` -- the chapter head, Results, what the next run
    compares against, the properties it should test and the class blocks
    -- and README.md is what stands between runs. Nearly every check here
    is a sweep over prose or a figure quoted in several places, and those
    places now fall either side of the split, so the sweeps read the pair
    joined and report `file:line`. What cannot be joined is said per
    document: which anchors a link may reach, and whether a file is as
    `wrap80` leaves it. A run file that is absent is a BLOCKED, never a
    quiet pass over half the figures a run publishes.

    The four checks the split brought, each broken deliberately and each
    kept as a case in `defects.py` rather than as an assertion
    here. A run file put beside a predecessor that is it verbatim names
    every figure-bearing paragraph of its head and exits 1
    (`chapter-head-carries-a-previous-run`), where the same file over a
    predecessor whose leads are marked names none, the two differing in
    the predecessor alone (`run-file-head-new-says-nothing`). A `runs/`
    holding one file says so in words rather than passing quietly
    (`run-file-alone-is-held-to-nothing`). A README link renumbered to
    the run before fails naming it, which is the one thing the four
    heading renames became and the one thing no anchor check can see, the
    older file being really there (`link-into-a-run-file-that-is-not-this-
    run`). And with no run file at all -- measured by hand 2026-08-25, a
    copy of the two documents in a directory whose runs/ is empty -- the
    BLOCKED above heads the output and the two-column table, the Results basis
    and the class floors each report their own absence, where the
    concatenation without it would have exited 0 over a README alone.
    """
    try:
        readme_doc = open(readme).read()
        main = open(main_hs).read()
        run_text = open(run_doc).read() if run_doc else None
        prev_text = open(prev_doc).read() if prev_doc else None
    except OSError as e:
        sys.stderr.write('check-doc: %s\n' % e)
        return 2
    docs = [(readme, readme_doc)]
    if run_doc is not None:
        docs.append((run_doc, run_text))
    doc = '\n'.join(t for _, t in docs)
    lines = doc.split('\n')
    span, at = [], 0
    for path, t in docs:
        k = len(t.split('\n'))
        span.append((at, at + k, os.path.basename(path)))
        at += k

    def where(i):
        """`file:line` for a 1-based line of the joined document."""
        for lo, hi, name in span:
            if lo < i <= hi:
                return '%s:%d' % (name, i - lo)
        return '?:%d' % i

    per_doc = {path: headings_of(t) for path, t in docs}
    anchors = {}
    for path, _t in docs:
        anchors.update(per_doc[path])
    bad, note = [], []

    # EVERY `--para` POINTER IN THE CHECKLISTS RESOLVES, or the list's own
    # instruction -- come back to a paragraph when a step surprises you --
    # names a paragraph that is not there. The chapter's fixed cost is the
    # reading, and the list says so: reading the prose front to back before
    # beginning is the largest waste available here. What makes skipping it
    # safe is that a surprised session can fetch the ONE paragraph its step
    # hangs on, which needs the step to name it -- and a named lead is
    # exactly the thing a later edit renames in silence, every other check
    # here staying green while the pointer aims at nothing. So the pointers
    # are checked the way the anchors are.
    # `why: --para '...'` and not a bare `--para`, which the prose also
    # writes when it is talking ABOUT the mode rather than pointing with
    # it: the first draft of this check read three such mentions as dead
    # pointers, one of them a placeholder in a command line.
    pointers = set(re.findall(r"why: --para '([^']+)'", readme_doc))
    if pointers:
        leads = []
        for _first, para, _spans in unwrapped_paragraphs(readme_doc
                                                         .split('\n')):
            m = LEAD_RE.search(para)
            if m:
                leads.append(' '.join(m.group(1).split()))
        # MARKUP IS NOT PART OF THE POINTER: a lead carrying backticks or
        # italics would otherwise have to be quoted with them, and a
        # later edit that merely emphasises a word would break a pointer
        # naming the same paragraph. Both sides are stripped of ` and *.
        def bare(t):
            return re.sub(r'[`*]', '', t).lower()
        dead = sorted(q for q in pointers
                      if sum(1 for l in leads if bare(q) in bare(l)) != 1)
        if dead:
            bad.append('%d --para pointer(s) resolve to no paragraph lead,'
                       ' or to several: %s'
                       % (len(dead), '; '.join(dead)))
        else:
            note.append('every --para pointer in the checklists names one'
                        ' paragraph (%d)' % len(pointers))
    # A GATE THE CHAPTER PIPES OR CHAINS. The chapter's recipes are what
    # a session copies, and a pipe reports its LAST command's status: Run
    # 27 read `check-all | tail`'s exit 0, ran the whole suite again, and
    # then chained `--predictions` behind `&&` in the very call testing
    # the rule it was writing about that. The rule is in the chapter now;
    # this holds the chapter's own lines to it. A READING may be filtered
    # and is not matched -- what is matched is the gate names, each of
    # which carries its verdict in its status and nowhere else.
    gate = re.compile(r'(--lint|--check-doc|check-all|defect-run\.py'
                      r'|selftest-mutants\.py|--selftest)\b[^|&\n]*(\||&&)')
    # COMMANDS AND NOT THE PROSE AROUND THEM: the chapter explains
    # this rule by quoting the mistake, `check-all | tail`, and a
    # first draft of the check failed the document on its own
    # explanation. A `#` line is comment, whatever it contains.
    piped = [l.strip() for l in open(readme, encoding='utf-8')
             if l.startswith('    ') and not l.lstrip().startswith('#')
             and gate.search(l)]
    if piped:
        bad.append('%d chapter line(s) pipes or chains a gate, whose'
                   ' status is then the last command\'s: %s'
                   % (len(piped), '; '.join(x[:60] for x in piped[:3])))
    else:
        note.append('no chapter recipe pipes or chains a gate')
    # THE RECOMMENDED-TASKS HEADING KEEPS THREE RUNS' BLOCKS. Post-run
    # step 5 retires the oldest to MARGINALIA; that rule stood unexecuted
    # while seven blocks piled up, 2026-09-23. Case:
    # `check-doc-refuses-a-fourth-cheaper-block`.
    cheaper = re.findall(r'^\*\*What Run (\d+) made cheaper',
                         open(readme, encoding='utf-8').read(), re.M)
    if len(cheaper) > 3:
        bad.append('%d `What Run N made cheaper` blocks (Runs %s) where the'
                   ' heading keeps three: post-run step 5 moves the oldest'
                   ' to MARGINALIA' % (len(cheaper), ', '.join(cheaper)))
    else:
        note.append('the recommended-tasks heading keeps %d run block(s)'
                    % len(cheaper))
    if run_doc is None:
        bad.append('BLOCKED: no run file in %s/, so the Results table, the'
                   ' fingerprint and the class blocks'
                   ' were not checked at all -- everything a run publishes'
                   ' is in that file and none of it was read' % RUNS_DIR)

    # WHERE A LINK RESOLVES DEPENDS ON WHICH FILE HOLDS IT. README.md
    # reaches the run's file as `runs/run<N>.md#...`, the run file reaches
    # back as `../README.md#...`, and a bare `#anchor` means the document
    # it is written in -- so resolving against one merged anchor set would
    # pass a link that GitHub renders dead. The third answer is the one the
    # split adds: a link into `runs/run18.md` resolves on disk, runs/
    # keeping every run, while promising figures this run replaced.
    # BY THE DOCUMENT A LINK NAMES, not by where the file it is in
    # happens to sit: a checker case points `--readme` at a copy in a temp
    # directory, and resolving `runs/run19.md#results` against THAT
    # directory would call every link into the run file dead. What a link
    # names is a ROLE -- the README, this run's file, some other run's --
    # and the role is in the name.
    def role_of(target):
        rel = target.partition('#')[0]
        if not rel:
            return 'same'
        base = os.path.basename(rel)
        if base == 'README.md':
            return 'readme'
        if re.match(r'^run\d+\.md$', base) and RUNS_DIR + '/' in rel:
            return ('run' if run_doc is not None
                    and base == os.path.basename(run_doc) else 'other-run')
        return 'elsewhere'

    def resolve(src, target):
        if re.match(r'^[a-z][a-z0-9+.-]*://', target):
            return True
        frag = target.partition('#')[2]
        if not frag:
            return True
        role = role_of(target)
        if role == 'same':
            return frag in per_doc[src]
        if role == 'readme':
            return frag in per_doc[readme]
        if role == 'run':
            return frag in per_doc[run_doc]
        if role == 'other-run':
            return None
        return True     # another document, which `check_paths` answers for

    # AND A LINK'S PATH, which the fragment check above cannot see and
    # `check_paths` does not read -- it resolves BACKTICKED names, and a
    # link target is not one. The gap is the split's own shape of defect:
    # a paragraph carrying `[...](runs/run<N>.md)` moved out of README
    # into that very file, where the path means `runs/runs/run<N>.md`. It
    # has no fragment, so nothing above judged it, and it ends in the
    # current basename, so the every-link-names-this-run check passed it
    # too. Resolved from each document's CANONICAL directory rather than
    # from wherever a copy is being linted, as the fragments are.
    # Cases: `link-path-resolves-nowhere`, with its live-file control.
    at_dir = {readme: os.path.dirname(os.path.abspath(__file__))}
    if run_doc is not None:
        at_dir[run_doc] = os.path.join(at_dir[readme], RUNS_DIR)

    def path_of(src, target):
        rel = target.partition('#')[0]
        if not rel or re.match(r'^[a-z][a-z0-9+.-]*://', target):
            return None
        return os.path.normpath(os.path.join(at_dir[src], rel))

    astray = []
    for src, text in docs:
        for target in re.findall(r'\]\(([^)\s]+)\)', text):
            where_ = path_of(src, target)
            if where_ is not None and not os.path.exists(where_):
                astray.append('%s -> %s' % (os.path.basename(src), target))
    if astray:
        bad.append('%d link target(s) resolve to no file: %s -- a path is'
                   ' read from the document holding the link, so one'
                   ' written for the other document lands nowhere'
                   % (len(astray), ', '.join(sorted(set(astray)))))
    else:
        note.append('every link target that names a path resolves')

    refs, dead = {}, []
    for src, text in docs:
        base = os.path.basename(src)
        mine = dict(re.findall(r'^\[([a-z0-9-]+)\]:\s*(\S+)\s*$', text,
                               re.M))
        refs.update(mine)
        # A well-formed fragment only: this README quotes `](#...)` in
        # the entry that asked for the check, and a quoted link is not one.
        for target in re.findall(r'\]\(([^)\s]*#[a-z0-9-]+)\)', text):
            got = resolve(src, target)
            if got is False:
                dead.append('%s -> %s' % (base, target))
            elif got is None:
                dead.append('%s -> %s (this run is %s)'
                            % (base, target,
                               os.path.basename(run_doc or 'absent')))
        for k, target in sorted(mine.items()):
            got = resolve(src, target)
            if got is False:
                dead.append('[%s]: %s in %s' % (k, target, base))
            elif got is None:
                dead.append('[%s]: %s in %s (this run is %s)'
                            % (k, target, base,
                               os.path.basename(run_doc or 'absent')))
        dead += ['%s (used in %s, defined nowhere in it)' % (u, base)
                 for u in sorted(set(re.findall(r'\]\[([a-z0-9-]+)\]',
                                                text)))
                 if u not in mine]
    dead += ['Main.hs -> README.md#' + m
             for m in re.findall(r'README\.md#([a-z0-9-]+)', main)
             if m not in per_doc[readme]]
    me = open(os.path.abspath(__file__)).read()
    dead += ['read-run.py -> README.md#' + m
             for m in re.findall(r'README\.md#([a-z0-9-]+)', me)
             if m not in per_doc[readme]]
    if dead:
        # DEDUPED, which the one-document form did not need: a link into
        # the run's file occurs two dozen times over four anchors, so
        # listing occurrences printed the same four names twenty-four
        # times and the reader met a wall instead of a list.
        bad.append('%d dead anchor(s), %d distinct: %s'
                   % (len(dead), len(set(dead)),
                      ', '.join(sorted(set(dead)))))
    else:
        note.append('every anchor resolves, in %s, in %s and in this script'
                    % (' and '.join(os.path.basename(p) for p, _ in docs),
                       os.path.basename(main_hs)))

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
    # AND THE SAME QUESTION OF THE FILE NAME, which is where a run number
    # lives now: `[Run 19](runs/run18.md)` resolves, reads right and is
    # wrong, and no anchor check can see it because the anchor is the whole
    # file. This is the form the four-heading rename used to fail as dead
    # anchors.
    crossed += [(t, tg) for t, tg in
                re.findall(r'\[([^\]\n]*\bRun (?:\d+)[^\]\n]*)\]'
                           r'\(([^)\s]*%s/run\d+\.md[^)\s]*)\)' % RUNS_DIR,
                           nocode)
                if re.search(r'\bRun (\d+)', t).group(1)
                != re.search(r'%s/run(\d+)\.md' % RUNS_DIR, tg).group(1)]
    if crossed:
        bad.append('%d link(s) whose text and target name different runs: %s'
                   % (len(crossed),
                      '; '.join('%s -> %s'
                                % (t, a if '/' in a else '#' + a)
                                for t, a in crossed)))
    else:
        note.append('every link naming a run agrees with the anchor or the'
                    ' file it points at')

    # EVERY LINK INTO runs/ NAMES THIS RUN, UNLESS ITS TEXT NAMES ANOTHER.
    # The directory accumulates, so a link left at the run before still
    # resolves and still renders -- which is the whole of what the rename
    # step now has to get right, and the only thing that replaces the four
    # heading renames it used to be.
    #
    # The exemption is for a DELIBERATE link into an older run's file, which
    # the run-file split made possible and Run 10's registrations made real
    # on 2026-08-29: an account that belongs to one run lives in that run's
    # file and is cited from README for good. Such a link says whose it is
    # in its own text --- `[Run 10's file](runs/run10.md)` --- and the check
    # above already holds text and target to naming the SAME run, so the
    # pair cannot drift apart. A link the rename missed looks nothing like
    # it: its text names this run's content, or no run at all, while its
    # target names the run before, and that is still caught here.
    if run_doc is not None:
        want = '%s/%s' % (RUNS_DIR, os.path.basename(run_doc))
        pair = re.compile(r'\[([^\]]*)\]\(([^)\s]*%s/run(\d+)\.md'
                          r'[^)\s]*)\)' % RUNS_DIR)
        old = sorted({t for _, text in docs
                      for txt, t, n in pair.findall(text)
                      if not t.split('#')[0].endswith(
                          os.path.basename(run_doc))
                      and not re.search(r'\bRun\s+%s\b' % n, txt)})
        if old:
            bad.append('%d link(s) point at a run file that is not this'
                       " run's: %s -- runs/ keeps every run, so a link the"
                       ' rename missed resolves and renders and promises'
                       ' figures %s replaced'
                       % (len(old), ', '.join(old), want))
        else:
            note.append('every link into %s/ names %s, this run'
                        % (RUNS_DIR, os.path.basename(run_doc)))

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
        # BLOCKED and not a note: the comment above forecloses exactly the
        # wrapping-dependence this fallback reintroduces, and the sibling
        # unwrap failure is already BLOCKED. 2026-09-01, by review.
        bad.append('BLOCKED: wrap80 could not run, so this pass read the'
                   ' working copy, whose answer depends on how it is'
                   ' wrapped -- the canonical form went unchecked')

    # Which section each line sits in, for both the coverage check and the
    # figure sweep.
    sec, cur = [], '(preamble)'
    for line in canon:
        m = re.match(r'^#+\s+(.*)$', line)
        if m:
            cur = m.group(1)
        sec.append(cur)
    replace_covered = None
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
        covered = set(re.findall(r'\]\([^)\s#]*#([a-z0-9-]+)\)', block))
        covered |= {refs[k].partition('#')[2]
                    for k in re.findall(r'\]\[([a-z0-9-]+)\]', block)
                    if k in refs and '#' in refs[k]}
        # THE RUN FILE IS COVERED WHOLE by the bullet naming it, and its
        # sections are not a list to keep. The file IS what a run replaces
        # -- that is the whole of why it is a file -- so giving each of its
        # sections a bullet would put run-scoped anchors back into a list
        # this one was rewritten to stop enumerating, and would leave the
        # coverage check able to fail for a section that cannot go stale
        # without the file going with it.
        if run_doc is not None and re.search(
                r'\]\([^)\s]*%s/%s' % (RUNS_DIR,
                                        re.escape(os.path.basename(run_doc))),
                block):
            covered |= set(per_doc[run_doc])
        slug = {v: k for k, v in anchors.items()}
        replace_covered = covered
        gaps = []
        # `Provenance` is exempt by heading text, so BOTH are: README's,
        # whose figures are the delta chain's and belong to the runs it
        # names rather than to this one, and the run file's, which the
        # whole-file rule above has already covered. The second is
        # redundant rather than a hole -- a replace list that did not link
        # the run file would fail on its four other sections first.
        # AN INDENTED LINE IS CODE ONLY INSIDE A BLOCK A BLANK LINE OPENED,
        # which is Markdown's own rule. Taking every four-space line as code
        # took every wrapped list continuation with it -- `canon` is the
        # wrapped form, and wrap80 indents an item's continuation six -- so
        # a figure past an item's first line was unseen anywhere in the
        # README, and the run chapter's two decimals sit on such lines.
        # Case: `coverage-check-sees-a-figure-on-a-wrapped-continuation`.
        in_code, prev_blank = False, True
        for i, line in enumerate(canon):
            indented = line.startswith('    ')
            if indented and prev_blank and not in_code:
                in_code = True
            elif in_code and line.strip() and not indented:
                in_code = False
            prev_blank = not line.strip()
            if (line.lstrip().startswith('|') or in_code
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
    # the commit hook wraps it and there is nothing left to adjudicate. Asking
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
    for _path, _text in docs:
        wrap_verdict(_path, _text, bad, note)
        heading_spacing_verdict(_path, _text, bad, note)

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
        bad.append('%d prose paragraph(s) stop mid-sentence -- first at %s,'
                   ' ending "%s". A scripted rewrite that anchors on a'
                   ' prefix replaces the whole paragraph, including the part'
                   ' you did not read; quote the full old text instead'
                   % (len(cut), where(cut[0][0]), cut[0][1][-48:]))
    else:
        note.append('every prose paragraph of both documents ends a'
                    ' sentence')

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
        bad.append('%d line citation(s) and %d pinned permalink(s) where the'
                   ' README says it carries neither: %s -- name a phrase, a'
                   ' heading or an arm, which a reflow cannot move'
                   % (len(cited), len(pinned),
                      ', '.join((cited + pinned)[:4])))
    else:
        note.append('neither document cites a line or a pinned permalink, as'
                    ' the README says of itself')

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

    comparatives = [(where(i), l)
                    for i, l in prose_hits(lines, COMPARATIVE_RE)]
    comparatives += [('%s:%d' % (os.path.basename(main_hs), i),
                      l.split('--', 1)[1].strip())
                     for i, l in enumerate(main.split('\n'), 1)
                     if '--' in l
                     and any(p.search(l.split('--', 1)[1])
                             for p in COMPARATIVE_RE)]
    foreign = [(i, l) for i, l in prose_hits(lines, [MS_RE])
               if not lines[i - 1].startswith('    ')]
    superlatives = [(where(i), l)
                    for i, l in prose_hits(lines, SUPERLATIVE_RE)]
    buried = [(where(i), l)
              for i, l in buried_actions(lines)]

    global BASE_REV
    base = base_rev_for(run_doc) if run_doc else None
    if base:
        BASE_REV = base
        print('note: freshness is read against %s, the commit that added %s,'
              ' so "added by this diff" means added by this write-up'
              % (base[:7], os.path.basename(run_doc)))
    added = added_lines(*([readme, main_hs]
                          + ([run_doc] if run_doc else [])))

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

    def sweep(hits, headline, settle=None):
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
        judged = [(h, is_fresh(h[1], added)) for h in hits]
        fresh = [h for h, f in judged if f]
        old_ = [h for h, f in judged if not f]
        if added is EVERYTHING:
            print('note: %d %s' % (len(hits), headline))
        elif fresh:
            print('note: %d %s -- %d ADDED BY THIS DIFF, listed first and'
                  ' the only ones this write-up owes:' % (len(hits), headline,
                                                          len(fresh)))
        else:
            print('note: %d %s -- none added by this diff:'
                  % (len(hits), headline))
        tail = (lambda l: '  -- settle by %s' % settle(l)) if settle \
            else (lambda l: '')
        for i, l in fresh:
            print('    NEW %s: %s%s' % (i, l[:60], tail(l)))
        for i, l in old_:
            print('        %s: %s%s' % (i, l[:60], tail(l)))

    for line in note:
        print('ok:   ' + line)
    if comparatives:
        sweep(comparatives, 'superseded figure(s) quoted; each has to earn'
              ' its place by the redo test, so adjudicate rather than assume'
              ' -- and a NEW entry is a paragraph the working tree changed,'
              " which step 5's repoint of every link into runs/ does to a few"
              ' dozen carrying figures it never touched')
    if superlatives:
        sweep(superlatives, 'superlative(s) in prose; each is a claim about'
              ' the whole table, so derive it by sorting rather than from'
              ' the arms the sentence is about', settle=settling_mode)
    if foreign:
        sweep([(where(i), l)
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
    long_ones = [(where(i), l)
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

    # `--move-registration` leaves `___` where the ANSWERED stub's clause of
    # verdicts goes, and until 2026-09-11 nothing read it. Run 28's entry
    # reached the SECOND checker pass with the bare placeholder standing,
    # every mechanical gate having passed over it, and it was found by an
    # agent opening README beside the run file rather than by anything here.
    # The mode that writes a placeholder is the one whose output most wants
    # a gate: what writes it is a script and what fills it is a person, so
    # the two are a handover with nobody on the far side. run-status.sh
    # checks the RUN FILE for the same token and not README, which is why
    # this sits here rather than there. Case: `answered-stub-keeps-its-slot`.
    stubs = [(where(i), l) for i, l in status_entries(lines, 'ANSWERED')
             if '___' in l]
    if stubs:
        bad.append('%d ANSWERED entry(s) still carry `___`, the placeholder'
                   ' --move-registration leaves for the verdict clause: %s.'
                   ' Write the verdicts in a clause each, as the entry under'
                   ' it does, or the run publishes an entry that answers'
                   ' nothing'
                   % (len(stubs), '; '.join('%s %s' % (i, l[:56])
                                            for i, l in stubs)))
    else:
        print("ok:   no ANSWERED entry carries --move-registration's `___`")

    # The run file's own two-column table keeps a column for each half,
    # including the regime this run's tables are NOT published from, which
    # reads like a leftover and is the opposite: a return to that regime
    # would otherwise have nothing to read against. It used to be the only
    # place the previous run's basis survived; since 2026-08-29 every run
    # from 7 on has a file of its own, so what this now protects is the
    # pairing rather than the record. Prose asks for it; this makes the
    # asking stick.
    # `install --in-place` writes `?` into any cell it cannot carry
    # forward -- a row new to the roster -- and says so once, on stderr,
    # hours before anyone reads the table. Twelve reached a published
    # Results table on 2026-08-15 and the write-up shipped with them.
    # A warning nobody re-reads is a gate that does not exist, so this
    # is the gate: no cell of a published table may still be `?`.
    #
    # OUTSIDE the two-column block below, reading nothing of it: it sat
    # inside, so a renamed header disabled this gate as well as
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
    # how the old yardstick's four bottom rows came to sit five columns from
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
        bad.append("the run file's two-column geomeans are gone: no"
                   ' `| strategy |` header naming the run and its halves,'
                   ' so the next run has no basis to be read against')
    else:
        regimes = set(re.findall(r'\(([^)]*)\)', yard[0]))
        if len(regimes) < 2:
            bad.append('the two-column table names one regime (%s); a'
                       ' paired run publishes a column per half and neither'
                       ' is folded into the other'
                       % (', '.join(sorted(regimes)) or 'none'))
        else:
            print('ok:   the run file keeps a column per regime (%s)'
                  % ' / '.join(sorted(regimes)))

        # A paired run puts two columns here, one per half, and neither may
        # be dropped or folded into the other: an aligned build is a regime
        # and not a second reading of the one beside it. Keyed off the run
        # number so this holds for any later pairing and not just Run 10.
        # Its control was Run 10's two columns in the yardstick until that
        # table went on 2026-08-29: no live run names a half aligned any
        # more, so nothing in these documents can make this branch fire and
        # the pass above is vacuous on its own. Its control is planted now,
        # `checkdoc-paired-run-aligned-with-no-counterpart` in
        # defects.py, which renames both halves of the run file's own
        # table aligned and expects the message below; proved able to fail
        # the day it was written, by breaking its expectation. Before Run 10
        # landed it could not fire either and was exercised by hand only.
        # The run that would have published an aligned
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
                bad.append('the run file names Run %s aligned and nothing'
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
    # --run-doc, which is how a copy is read at all -- a path given
    # positionally is a run JSON, so the first attempt re-checked the live
    # document and credited this with a pass it had not earned. The run
    # file as it stands carries exactly one such token in that section and
    # passes; renumbering it to the run before fails, naming both the run
    # and the file. So the pass is a real pass and the check bites, and
    # the case is `results-names-an-older-basis-half`.
    # THE RUN NUMBER COMES OFF THE FILE NAME, which is the only place it
    # is written now: `runs/run19.md`. It used to come off `## About the
    # last run (Run N)`, one of four headings a write-up renamed by hand.
    # A PARAGRAPH DEFERRED UNTIL A MEASUREMENT LANDS carries `[[TODO]]`,
    # and the token fails the document until it is written: a deferral
    # with no marker was forgotten until an end-to-end read caught it
    # (Run 23, the comparison section's first paragraph). Not `TODO`
    # bare, which README's own TODO list names.
    for path, text in docs:
        k = len(re.findall(r'(?<!`)\[\[TODO\]\](?!`)', text))
        if k:
            bad.append('%d `[[TODO]]` marker(s) in %s: a deferred paragraph'
                       ' is written before the document passes'
                       % (k, os.path.basename(path)))
    cur = str(run_no_of(run_doc)) if run_doc else None
    start = next((i for i, ln in enumerate(lines)
                  if re.match(r'#{1,6} Results\s*$', ln)), None)
    if cur is None:
        pass                # the BLOCKED at the top of this function said it
    elif start is None:
        bad.append('no `Results` heading in %s, so the section whose tables'
                   ' are installed from the basis half cannot be located'
                   % os.path.basename(run_doc))
    else:
        end = next((j for j in range(start + 1, len(lines))
                    if re.match(r'#{1,6} ', lines[j])), len(lines))
        # A REPETITION NAMES ITS PREDECESSOR'S HALF ON PURPOSE -- `is
        # run22-g912 byte for byte` -- and that is not the stale name this
        # catches, so a token with `byte for byte` in the eighty characters
        # after it is exempt; Run 23 reworded to lose the artifact name.
        sec = '\n'.join(lines[start:end])
        seen = {m.group(1) for m in re.finditer(r'\brun(\d+)-[a-z0-9]+', sec)
                if 'byte for byte' not in sec[m.end():m.end() + 80]}
        stale = sorted(seen - {cur}, key=int)
        if stale:
            bad.append('the Results section names run %s while the file is'
                       " Run %s's: the tables there are installed from this"
                       " run's basis half, so the half named beside them is"
                       ' this run\'s or the two disagree'
                       % (', run '.join(stale), cur))
        else:
            print('ok:   the half named in Results belongs to Run %s, whose'
                  ' file this is' % cur)

    # THE RUN FILE MUST OUTLIVE THE ARTIFACTS, which is what makes it a
    # file: post-run step 11 offers the JSONs, the logs, the wall-clock
    # file, both binaries and the pair note for deletion, so a sentence in
    # the run's own document that NAMES one of those is a promise that dies
    # with the offer. Run 20 wrote two -- "the superseded artifacts are
    # parked as `probe-run20-exposed/`" -- and then kept the directory
    # BECAUSE the prose cited it, which is the dependency running
    # backwards. A binary named as a build ("`run19-g912` held it at") is a
    # fact about a compile and not a path, so only extensions are matched.
    if cur is not None and run_doc:
        # ITS OWN artifacts only. A past run's are history -- `run17`'s
        # repetition is named in a rule about the namespace, and the tree
        # at launch is recorded with the untracked paths it carried -- and
        # history does not die with this run's deletion offer. What does is
        # `run<cur>-*.json|log|txt` and any `probe-run<cur>-` of its own.
        doomed = sorted({m.group(0) for m in re.finditer(
            r'`(?:probe-run%s-[A-Za-z0-9._-]+/?'
            r'|run%s-[A-Za-z0-9._-]+\.(?:json|log|txt))`' % (cur, cur),
            run_text)})
        if doomed:
            bad.append('%d artifact path(s) named in %s, which step 11 offers'
                       ' for deletion -- the run file outlives them, so state'
                       ' the fact rather than the file: %s'
                       % (len(doomed), os.path.basename(run_doc),
                          ', '.join(doomed[:6])))
        else:
            print('ok:   the run file names no artifact the deletion offer'
                  ' covers, so it survives the offer being accepted')

    # A BOLDED CLASS NAME AT A LINE START IS HOW A CLASS BLOCK IS FOUND,
    # so one anywhere else is read as a ninth block with no table under it.
    # install-tables.sh then refuses naming a JSON that is present all
    # along. Run 20 wrote `**`reshape1` sits apart at 0.9995**` into the
    # chapter head; unwrapped it sat mid-line and was harmless, and the
    # wrap made it a line start, so the defect appeared at a moment when
    # nothing had been edited. The rule is unwritable -- no author will
    # remember it -- so it is a check.
    # THE RUN FILE'S OWN LINES, not the concatenated pair: `lines` is
    # README followed by the run doc, and README carries its own heading
    # `The stride classes and what they cover`, so a search over the pair
    # finds that one first and the prefix examined is README's alone.
    rlines = run_text.split('\n') if run_doc else []
    cstart = next((i for i, ln in enumerate(rlines)
                   if re.match(r'#{1,6} The stride classes', ln)), None)
    # AND WHERE THAT SECTION ENDS, because the sweep below reads the file
    # outside it and not merely its opening -- which is what its own message
    # has always said. The blocks carry no headings of their own, so the next
    # level-1-or-2 heading is the end. Everything after it, Provenance, went
    # unread: 153 lines of run20.md, rewritten every run, naming the classes
    # throughout, where `install-tables.sh` greps the whole file and would
    # have counted a stray there as a further block. Proved by planting one
    # stray before Results and one in Provenance against the narrow form --
    # the first caught, the second missed.
    # Case: `rundoc-has-a-stray-class-lead-in-provenance`.
    cend = (next((i for i, ln in enumerate(rlines[cstart + 1:], cstart + 1)
                  if re.match(r'#{1,2} ', ln)), len(rlines))
            if cstart is not None else None)
    # The block names come from the section's own leads rather than from a
    # literal, so a class added or renamed moves this with it and there is
    # nothing to keep in sync. Bounded by `cend` for the same reason the
    # sweep is: a ` --- ` lead sitting in Provenance is a stray to report,
    # never a name to take the roster from.
    blocks = {m.group(1) for ln in (rlines[cstart:cend] if cstart is not None
                                    else [])
              for m in [re.match(r'\*\*`([a-z0-9]+)` ---', ln)] if m}
    if cur is not None and run_doc and blocks:
        stray = []
        for ln in rlines[:cstart] + rlines[cend:]:
            m = re.match(r'\*\*`([a-z0-9]+)`', ln)
            if m and m.group(1) in blocks:
                stray.append('%s ... %s' % (m.group(1), ln[:58]))
        if stray:
            bad.append('%d paragraph(s) outside the class section begin a'
                       ' line with a bolded class name, which is how a class'
                       ' block is located -- install-tables.sh will read each'
                       ' as a block with no table: %s'
                       % (len(stray), '; '.join(stray[:3])))
        else:
            print('ok:   no bolded class-name lead outside the class section,'
                  ' so every block install finds is a block')

        # AND INSIDE THE SECTION THE PREDICATE IS DUPLICATE, NOT STRAY,
        # which is the region the sweep above deliberately excludes: there
        # a bolded class-name lead is how a block legitimately starts, so
        # what cannot be right is the same class leading twice. Each class
        # has exactly one block, so a repeat is either a second lead for
        # one class or a paragraph imitating one, and both reach
        # `install-tables.sh` the same way -- its loose grep counts the
        # repeat, `comm` leaves the name over, and it refuses with the
        # `no run<N>-<basis>-*.json` message naming a file that is present,
        # which is the whole defect this pair of checks exists against.
        # Measured 2026-08-26 by planting a duplicate `rev` lead mid-block:
        # the sweep above said `ok` and the loose grep read nine leads for
        # eight classes. The LOOSE pattern is used, without the dash, so a
        # repeat that lost its ` --- ` is caught here rather than becoming
        # the two-patterns-disagree refusal one step later.
        # Case: `rundoc-repeats-a-class-lead`.
        repeats = sorted(
            n for n, c in collections.Counter(
                m.group(1)
                for ln in (rlines[cstart:cend] if cstart is not None else [])
                for m in [re.match(r'\*\*`([a-z0-9]+)`', ln)] if m
            ).items() if c > 1)
        if repeats:
            bad.append('%d class name(s) lead more than one paragraph inside'
                       ' the class section (%s); each class has exactly one'
                       ' block, so install-tables.sh counts the repeat and'
                       ' refuses naming a JSON that is present'
                       % (len(repeats), ', '.join(repeats)))
        else:
            print('ok:   no class leads twice inside the class section, so'
                  ' the block count install finds is the class count')

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

    # THE RUN'S FILE AGAINST THE ONE BEFORE IT, which is what a run file
    # is for. A run replaces its file whole, so a figure-bearing paragraph
    # byte-identical to one in the predecessor's file is stale, or is
    # standing on purpose and wants rewording to say so. A write-up is
    # done a paragraph at a time and nothing enumerates them: Run 18 left
    # FOUR of Run 17's standing in the chapter head, one contradicting two
    # paragraphs the same session had just written, and Run 19 left six
    # more outside it. An independent checker found each set by
    # set-differencing the document, which is this script's job and is one
    # comparison.
    #
    # WHAT THIS REPLACES, and why it is better than what it replaces. The
    # same question used to be asked of README.md against `git show
    # HEAD:README.md`, which has two faults a second file does not. It went
    # quiet the moment the write-up was committed -- the check printed
    # `there is no previous run to hold it to` and passed -- so a run that
    # committed early was never held to anything. And it had to be scoped
    # by hand, first to the chapter head and then, when Run 19 left six of
    # Run 18's paragraphs standing outside it, by a churn threshold over
    # the sections the replace list names. Two files need neither: nothing
    # in this one outlives the run, so the scope is the file, and the
    # comparison is a diff between two paths that owes git nothing.
    #
    # A key is a paragraph with its whitespace collapsed, so a re-wrap is
    # not a change. Tables, indented blocks, headings and reference
    # definitions are not paragraphs a run writes, and a paragraph with no
    # figure in it is the file's own front matter or a form.
    #
    # The HEAD FAILS and the rest is a worklist, which is the split the two
    # checks this replaces had between them: the head is a handful of
    # paragraphs and every one is written from this run's numbers, while a
    # class block's form and a property's restatement can legitimately
    # repeat.
    def figure_blocks(text, figures_only=True):
        # `figures_only` is FALSE for the HEAD, which a run replaces
        # WHOLE: there, any paragraph the run before also had is
        # suspect, whatever kind of figure it carries. FIGURE_RE
        # matches a decimal and nothing else, so a paragraph whose
        # figures are a hex address, a byte count or a count spelled
        # in words is invisible to it -- and Run 24 replaced every
        # one of the twenty paragraphs this named while three MORE
        # were still Run 23's, carrying 0x4205aa, 2408930 bytes and
        # `23 of 24` between them. Only the end-to-end read found
        # them. The filter stays for the REST of the file, where a
        # form or a restatement legitimately stands.
        # Case: `stale-head-check-sees-only-decimals`.
        out = {}
        for key, ls in blocks_of(text):
            first = ls[0].lstrip()
            if (ls[0].startswith('    ') or first.startswith('|')
                    or re.match(r'#{1,6} |\[[^\]]+\]:', first)):
                continue
            if figures_only and not FIGURE_RE.search(' '.join(ls)):
                continue
            out[key] = ls[0]
        return out

    def head_and_rest(text):
        m = re.search(r'^## ', text, re.M)
        return (text[:m.start()], text[m.start():]) if m else (text, '')

    # THE HEAD IS AT MOST FIVE PARAGRAPHS past the preamble, since
    # 2026-09-17: the pair and its headline, what the registration was built
    # to show, the registration tally, anomalies and what the next run
    # takes. An upper bound and not a form check: which paragraph is which
    # stays the reading's. Run 34's ran to twenty-one, most of them restating
    # Provenance or a class block -- the gate, the window, intrusion,
    # repetition, `.text`, the regime, the straddlers and the
    # decomposition -- each restatement one more site two copies of a
    # figure could part across. Case: `head-is-five-paragraphs`.
    if run_text:
        n_head = len(figure_blocks(head_and_rest(run_text)[0],
                                   figures_only=False)) - 1
        if n_head > HEAD_PARAGRAPHS:
            bad.append("%s's head carries %d paragraphs past its preamble,"
                       ' and the form is at most %d: the pair and its'
                       ' headline, what the registration was built to show,'
                       ' the registration tally, anomalies and what the next'
                       ' run takes -- the gate, window, intrusion,'
                       ' repetition, `.text`, regime, straddlers and'
                       " decomposition are Provenance's"
                       % (os.path.basename(run_doc), n_head,
                          HEAD_PARAGRAPHS))
        else:
            print("ok:   %s's head is %d paragraphs past its preamble"
                  % (os.path.basename(run_doc), n_head))

    if run_doc is None:
        pass                # the BLOCKED at the top of this function said it
    elif prev_doc is None:
        print('note: %s/ holds one run file, so %s is held to no'
              ' predecessor -- this check is a diff between two run files'
              ' and there is only one'
              % (RUNS_DIR, os.path.basename(run_doc)))
    else:
        was_run = run_no_of(prev_doc)
        now_head, now_rest = head_and_rest(run_text)
        was_head, _was_rest = head_and_rest(prev_text)
        # THE PREAMBLE IS THE ONE PARAGRAPH OF THE HEAD A RUN DOES NOT
        # REPLACE: the paragraph under the title says what a run file
        # IS, and it stands every run by design, so holding it to the
        # rule below would ask each run to reword a form statement to
        # no end. Dropped by position -- the first surviving block of
        # the head, the title itself being skipped as a heading -- and
        # dropped from BOTH sides, so a run that does reword it is not
        # thereby held to the run before's.
        def head_blocks(text):
            got = figure_blocks(text, figures_only=False)
            return dict(list(got.items())[1:])
        old_head = head_blocks(was_head)
        old_all = figure_blocks(prev_text)
        stale = [l for k, l in head_blocks(now_head).items()
                 if k in old_head]
        if stale:
            bad.append("%d paragraph(s) of Run %s's head are unchanged from"
                       ' Run %s: the file is replaced whole, so each is'
                       ' stale or is standing on purpose and wants rewording'
                       ' to say so -- %s'
                       % (len(stale), cur, was_run,
                          '; '.join(l.strip()[:60] for l in stale)))
        else:
            print("ok:   every paragraph of Run %s's head is new since"
                  ' Run %s' % (cur, was_run))
        held = [l for k, l in figure_blocks(now_rest).items()
                if k in old_all]
        # AND THE BODY IS GATED TOO, on the NARROW predicate. The head's
        # refusal above is by POSITION, and Run 29 cleared the head, saw
        # this gate go green, and left thirty carried paragraphs standing
        # in the body -- of which its checker returned thirteen, among them
        # a cross-run paragraph every figure of which was the run before's
        # and a paragraph asserting that the two columns MAY be differenced
        # where the run's whole finding is that they may not. What parts a
        # stale paragraph from the apparatus is not where it sits but what
        # it says about itself: `this run`, `this pair`, or the CURRENT
        # run's own number is a claim about the run in front of it, while
        # `Run 8 re-ran every class` is the standing apparatus and re-carries
        # every run. `--inherited` reports the wide predicate and stays a
        # reading; this is the narrow half of it, and it refuses.
        # Case: `carried-body-paragraph-calls-itself-this-runs`.
        mine = re.compile(r"this run\b|this pair\b|\bRun %s\b"
                          % re.escape(cur))
        claims = [l for l in held if mine.search(l)]
        rest = [l for l in held if l not in claims]
        if claims:
            bad.append('%d carried paragraph(s) of %s call themselves this'
                       " run's or name Run %s while being Run %s's file"
                       ' unchanged -- each is stale or wants rewording to say'
                       ' it stands on purpose: %s'
                       % (len(claims), os.path.basename(run_doc), cur, was_run,
                          '; '.join(l.strip()[:60] for l in claims)))
        if rest:
            # NAME THE MODE THAT LISTS THEM. A count with no route to
            # its own members is one a session reads past: Run 30 met
            # this note, did not run --inherited, wrote its head, and
            # had a checker return twelve stale carried paragraphs
            # that the one command lists. Case:
            # `carried-note-does-not-name-inherited`.
            print('note: %d paragraph(s) of %s are unchanged from Run %s and'
                  ' name only an EARLIER run -- `--inherited` lists them'
                  ' and post-run 6a runs it BEFORE the prose is written;'
                  ' each is stale or is standing on'
                  ' purpose, and the ones that stand are usually a form or a'
                  ' restatement:'
                  % (len(rest), os.path.basename(run_doc), was_run))
            for line in rest:
                print('        %s' % line.strip()[:76])
        if not held:
            print('ok:   %s holds no figure-bearing paragraph of Run %s'
                  % (os.path.basename(run_doc), was_run))

    # AND THE SAME QUESTION OF README.md, which the run file does not
    # answer: the sections a run reaches OUTSIDE its own file -- the floor
    # section, the opening's headline ratios, the ceiling and Lemire
    # rulings -- are replaced by a run too, and a paragraph left standing
    # there is what Run 19 shipped four of. Identity against the committed
    # copy is all there is here, README.md having no predecessor to be
    # diffed against, and the churn threshold is what keeps the reference
    # chapters out of it. See `held_in_reworked_sections`.
    head_doc = head_text_of(readme)
    if head_doc is None:
        print('note: no committed copy of %s, so its own replaced sections'
              ' are not held to anything' % os.path.basename(readme))
    else:
        held = held_in_reworked_sections(readme_doc, head_doc,
                                         replace_covered)
        if held:
            print('note: %d paragraph(s) of %s unchanged since it was'
                  ' committed, in section(s) this run otherwise rewrote;'
                  ' each is stale or is standing on purpose, and the ones'
                  ' that stand are usually a column definition or a form:'
                  % (len(held), os.path.basename(readme)))
            for sec_, line in held:
                print('    [%s] %s' % (sec_[:34], line.strip()[:58]))
        elif replace_covered:
            print('ok:   the %s sections this run rewrote hold no paragraph'
                  ' of its committed copy' % os.path.basename(readme))

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
        # A CLASS SHAPE ADDED AFTER THE RUN. The run file's class table
        # and its `over N shapes` figures describe the roster its run
        # measured, and the two checks below hold them to Main.hs as it is
        # now -- so a class shape added between runs failed the newest
        # run file's TRUE count, and the only edit that passed was one
        # that made Run 21 claim a population it never timed. README's
        # provenance bullet already declares such additions for arms;
        # the same sentence declares them for shapes, and the names in it
        # that are class shapes are taken out of what the run file is
        # held to. The declaration lives in the provenance bullet and
        # leaves with it at the next run's write-up; left standing, it
        # would hold that run's true table to the reduced count, which
        # is why a mismatch under an exclusion names both numbers:
        #     `runs-256` and `runs-512` were added 2026-08-30, after the run
        # Added 2026-08-30. Case:
        # `class-shapes-added-after-the-run-are-exempt`.
        added_after = set()
        for m in re.finditer(r'((?:`[\w.-]+`(?:,\s+(?:and\s+)?|\s+and\s+))*'
                             r'`[\w.-]+`)\s+(?:was|were) added'
                             r' \d{4}-\d{2}-\d{2}, after the run', uw):
            added_after |= set(re.findall(r'`([\w.-]+)`', m.group(1)))
        # A class retired from timing (Main.hs `retiredClasses`) is out of
        # the class counts likewise, unless this run file timed it, which
        # the same bullet declares as `were retired DATE, after the run`.
        # Added 2026-09-04. Case:
        # `retired-classes-timed-by-the-run-are-exempt`.
        retired_after = set()
        for m in re.finditer(r'((?:`[\w.-]+`(?:,\s+(?:and\s+)?|\s+and\s+))*'
                             r'`[\w.-]+`)\s+(?:was|were) retired'
                             r' \d{4}-\d{2}-\d{2}, after the run', uw):
            retired_after |= set(re.findall(r'`([\w.-]+)`', m.group(1)))
        retired = retired_classes(main_hs) - retired_after
        aa = [n for n, r, _ in roster if r == 'Twin']
        controls = [n for n, r, _ in roster if r in ('Twin', 'Term', 'Force')]
        timed = [n for n, r, _ in roster if r != 'Only']
        twinned = {twin_of(n) for n in aa}
        facts = [
            (r'are ([a-z\d-]+) controls: ([a-z\d-]+) A/A arms',
             (len(controls), len(aa)), "the controls sentence"),
            # ARMS, not benches: this compares against the TIMED ROSTER
            # and a reader met `the run is 53 benches` beside `1272
            # benches` and had to work out they count different things.
            # The word moved in both places at once, 2026-08-26.
            (r'with the controls the run is ([a-z\d]+) arms',
             (len(timed),), 'the timed-arm count'),
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

        # THE FIGURES THAT MUST AGREE WHEREVER THEY APPEAR, as a table
        # rather than one hand-written check apiece. Both rows below were
        # written separately, and the second only after Run 16 shipped its
        # six-pair figure three ways -- 0.39%/0.24% in four places, 0.50%
        # in a fifth and rounded to "half a percent" in a sixth, two of
        # them inside one paragraph. That is what a check-per-figure
        # costs: a quantity gets one only after it has already been got
        # wrong somewhere. A row is cheaper than a check, so the next
        # quantity to need this is a row and not a fourth copy of the
        # gather-compare-report below.
        #
        # `pats` are the sites quoting the PAIR; `alone` the sites quoting
        # one half of it, which are held to the pair's first figure. A row
        # whose patterns stop matching says so rather than passing: a
        # sweep that silently narrows is the failure this file is written
        # against, and a reworded sentence moves a pattern with it.
        #
        # AND A SELF-AIMING FIXTURE ANCHOR HAS TO LAND INSIDE ONE OF THESE
        # SITES. `defects.py`'s `readme_six_pair_perturbed` finds the
        # sentence by its own shape so a requote does not leave a fixture
        # that will not build -- but a shape that is not one of the
        # patterns above perturbs text this check never reads, and the
        # case then builds, runs and cannot fire, which is the one
        # outcome a corpus must not have. Run 25 reworded the six-pair
        # sentence truthfully, the anchor followed it out of the site,
        # and the case went green on a check that had seen nothing. When
        # a pattern here moves, move that anchor with it.
        AGREEING = (
            ('floor pair',
             (r'a noise floor this run measures at ([\d.]+)%[^.]*?'
              r' and ([\d.]+)%',
              r'floor is ([\d.]+)% on the basis half and ([\d.]+)%'
              r' on the (?:control|other half|[a-z-]+ half)',
              r'no A/A pair further than \*{0,2}([\d.]+)%\*{0,2} from 1 on'
              r' the basis half or \*{0,2}([\d.]+)%\*{0,2} on the'
              r' (?:control|other half|[a-z-]+ half)',
              # FOUR MORE PHRASINGS, added 2026-09-06 after this check saw
              # TWO of the ten sites Run 26 carries and the pass that found
              # the other eight was an agent's. The check is worth only the
              # sites it can see, so a phrasing that recurs run after run
              # belongs here rather than in a reviewer's head. Three
              # phrasings became seven, and it now reads all TEN.
              # NON-VACUITY, BY HAND AND NOT BY A MUTANT, 2026-09-06:
              # planting 0.33% in README's floor lead -- a site only these
              # four reach -- makes this report the disagreement across ten
              # sites, and disabling all four makes it report that it found
              # fewer than two sites and did not run. A mutant was written
              # for that and REMOVED rather than left LOST: its judge's
              # baseline is red inside `selftest-mutants.py`'s tracked-only
              # copy, where this FAIL does not reproduce, and four shapes of
              # judge (cwd set and unset, --main given and not, the plant
              # whitespace-tolerant for the wrapped form) all failed the same
              # way. What defeats it was not established; do not re-attempt
              # without first finding why check-doc's floor FAIL is absent in
              # that copy.
              r'floor is \*{0,2}([\d.]+)%\*{0,2} on the basis(?: half)? and'
              r' \*{0,2}([\d.]+)%\*{0,2} on the control',
              r'\*{0,2}([\d.]+)%\*{0,2} and \*{0,2}([\d.]+)%\*{0,2} read on'
              r' the six pairs',
              r'\*{0,2}([\d.]+)%\*{0,2} and \*{0,2}([\d.]+)%\*{0,2} are the'
              r' widest an arm differs',
              r'SIX A/A pairs Run \d+ read\*{0,2}, \*{0,2}([\d.]+)%\*{0,2}'
              r' and \*{0,2}([\d.]+)%\*{0,2}'),
             (),
             'the head of the run chapter carries the measurement, so'
             ' requote the others'),
            # THE CROSS-HALF `list` MOVE, added 2026-09-13. It is quoted at
            # six sites across the two documents and nothing held them
            # together: Run 30 wrote 17.18 where its own class block and
            # `--compare` both say 17.26, and the wrong figure stood in five
            # places in the run file, one in README and two in the checker's
            # brief until a checker pass sorted the ten classes. The floor
            # pair earned this treatment the same way, and the comment above
            # says what a recurring phrasing owes: a row here rather than a
            # reviewer's memory.
            ('cross-half `list` move',
             (r'`list` having moved \*{0,2}([\d.]+) points\*{0,2} on this'
              r" run's main set",
              r'`list` is ([\d.]+) points faster WITH the flag',
              r'`list` moves by about a \w+ everywhere, ([\d.]+)% at its'
              r' narrowest',
              r'`list` moves between the halves by ([\d.]+)% at its'
              r' narrowest'),
             # NOT the delta chain's `Its `list` moved N points between the
             # halves`: that chain keeps one bullet per run and each carries
             # its OWN figure, so the pattern matched Run 29's 12.12 beside
             # Run 30's 17.10 and called legitimate history a disagreement.
             # A site belongs here only where `this run` scopes it.
             (),
             'the main set is one number and the class range another, so a'
             ' site quoting the first is quoting this one'),
            ('carry-back figure',
             (r'pairs that carry back to Run 10[^.]*?\*{0,2}([\d.]+)%\*{0,2}'
              r' and \*{0,2}([\d.]+)%',
              r'\*{0,2}([\d.]+)%\*{0,2} and \*{0,2}([\d.]+)%\*{0,2}'
              r' (?:are the same over|read on) the [a-z]+ pairs'),
             (r'carry-back figure of the half it is read on[^.]*?([\d.]+)%',
              r'\*([\d.]+)% between any two rows of the table\*'),
             'it is the threshold two rows of one table must clear, so one'
             ' wrong copy retires a margin'),
        )
        for name, pats, alone_pats, why in AGREEING:
            sites = [m for p in pats for m in re.findall(p, uw)]
            alone = [m for p in alone_pats for m in re.findall(p, uw)]
            if len(sites) < 2:
                # AND IT SAYS WHAT IT LOOKED FOR, added 2026-09-15. The
                # abstention is loud, which is right, but it used to leave
                # the author to find the patterns in this file: a write-up
                # reworded four of these paragraphs in one stretch and paid
                # a round of reading source to learn which sentence shapes
                # the check wanted. Printing them turns the FAIL into an
                # instruction. Case: `check-doc-abstention-names-its-patterns`.
                #
                # REFUSED, THE SAME DAY: keying these on the NOUN instead of
                # the phrasing, which is what this file's own rule for a
                # sweep asks for. A noun-keyed matcher over prose cannot
                # tell THIS run's figure from the series of earlier runs'
                # figures quoted in the same paragraph, and the floor
                # section is made of exactly that -- earlier runs'
                # readings carried back beside this run's own, in one
                # paragraph, every one of them a percent adjacent to
                # the word `floor`. The
                # phrasings stay, and what a rewording costs is now one
                # message rather than one reading of this file.
                # AND IT SAYS WHAT IT DID FIND, added 2026-09-16: with two
                # sites wanted and one matched, the author's question is
                # which sentence already matches, and the patterns alone
                # do not answer it -- Run 33 reworded four of these and
                # grepped for the surviving site each time. The figure is
                # enough to find it, the documents quoting each of these
                # in two places and no more.
                bad.append('could not locate at least two sites quoting the'
                           " run's %s, so its agreement check did not run --"
                           " if the sentences were reworded, this check's"
                           ' patterns move with them. It found %d: %s. It'
                           ' looked for: %s'
                           % (name, len(sites),
                              '; '.join('/'.join(_agree_unit(x) for x in
                                                 (s if isinstance(s, tuple)
                                                  else (s,)))
                                        for s in sites) or 'nothing',
                              '; '.join(repr(x) for x in pats)))
            elif len(set(sites)) > 1:
                bad.append('the %s is quoted differently across its %d'
                           ' sites: %s -- %s'
                           % (name, len(sites),
                              '; '.join('/'.join(_agree_unit(x) for x in
                                                  (f if isinstance(f, tuple)
                                                   else (f,)))
                                        for f in set(sites)),
                              why))
            elif any(o != (sites[0][0] if isinstance(sites[0], tuple)
                           else sites[0]) for o in alone):
                bad.append('the %s reads %s%% where it is quoted as a pair'
                           ' and %s where it is quoted alone -- the two are'
                           ' the same number'
                           % (name, (sites[0][0] if isinstance(sites[0], tuple)
                                     else sites[0]),
                              ', '.join(sorted(set(
                                  o for o in alone
                                  if o != (sites[0][0]
                                           if isinstance(sites[0], tuple)
                                           else sites[0]))))))
            elif alone_pats:
                one = sites[0] if isinstance(sites[0], tuple) else (sites[0],)
                print('ok:   the %s reads %s at all %d sites that'
                      ' quote it, and %s%% at the %d that quote one half'
                      % (name, '/'.join('%s%%' % x for x in one),
                         len(sites), one[0], len(alone)))
            else:
                one = sites[0] if isinstance(sites[0], tuple) else (sites[0],)
                print('ok:   the %s reads %s at all %d sites that quote it'
                      % (name, '/'.join('%s%%' % x for x in one),
                         len(sites)))

        # And the A/A population itself. The twelve twins took it from six
        # pairs to eighteen on 2026-08-14 and two sites kept saying six for
        # three runs -- the reader's own section and the floor section's
        # per-population rule -- while every class block printed "N of 18".
        # Nothing compared them, so the stale pair rode three write-ups.
        # `sixteen` joined on 2026-08-29, the parking of `offtab` having
        # removed its two twins: a size this vocabulary does not carry makes
        # the check find NOTHING and say so, which is why the empty case is
        # a FAIL and not a pass -- met the moment the roster moved.
        # Non-vacuity, 2026-08-29, both branches proved by hand on README:
        # one site changed to `eighteen` while the rest read `sixteen`
        # FAILs naming both; changing every site to a word outside the
        # vocabulary FAILs with the could-not-locate message; restoring
        # exits 0. So neither branch passes vacuously.
        # The vocabulary is closed on purpose: a word it does not carry
        # makes `base` empty and stops this check biting, so it is widened
        # in the same edit that first needs it -- `eight` on 2026-09-09,
        # when the shipped fill's A/A pair took the population from six.
        WORD = r'(six|eight|sixteen|eighteen)'
        base = set(re.findall(r'it rests on ' + WORD + r' pairs', uw))
        base |= set(re.findall(r'The same ' + WORD
                               + r' controls ride every process', uw))
        base |= set(re.findall(r'\*\*' + WORD.title()
                               + r'\*\* A/A controls run an existing strategy',
                               uw))
        base = {b.lower() for b in base}
        # AGAINST THE ROSTER, not only against each other. Agreement between
        # sites says they were edited together and nothing about whether any
        # is right: the parking of 2026-08-28 took the population to sixteen
        # and every site still read eighteen, in agreement and wrong. The
        # roster is the authority and Main.hs carries it, so this costs no
        # artifact and survives their deletion. Added 2026-08-29.
        # Non-vacuity, 2026-08-29, all three branches: every site moved to
        # `eighteen` together FAILs naming the roster where the older
        # site-against-site check passed (corpus case
        # `aa-population-agrees-with-itself-and-not-the-roster`); a roster
        # doctored to 21 Twin arms FAILs with the no-word message; and the
        # live documents exit 0.
        WORDS = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
                 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11,
                 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
                 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
                 'nineteen': 19, 'twenty': 20, 'twenty-two': 22,
                 'twenty-four': 24}
        want = len(aa)
        named = sorted(w for w, v in WORDS.items() if v == want)
        # A roster count this vocabulary cannot SPELL is the checker's gap
        # and not the document's, so it says so rather than failing prose
        # that may be perfectly right. Same shape as the empty-search FAIL
        # above: a check that cannot run says it did not run.
        if not named:
            bad.append('the roster has %d Twin arm(s) and this check has no'
                       ' word for that count, so it could not be compared'
                       ' -- teach WORDS the spelling in the same edit that'
                       ' first uses it' % want)
        for b in sorted(base) if named else []:
            if WORDS.get(b) != want:
                bad.append('the A/A population is named `%s` where the roster'
                           ' has %d Twin arm(s)%s -- Main.hs is the authority,'
                           ' and sites agreeing with each other is not'
                           ' evidence that any of them is right'
                           % (b, want, ', which is `%s`' % named[0]
                              if named else ''))
        if not base:
            bad.append("could not locate any site naming the A/A population's"
                       ' size, so that agreement check did not run')
        elif len(base) > 1:
            bad.append('the A/A population is quoted as %s across its sites'
                       ' -- the roster fixes it and every class block prints'
                       ' that count, so a site naming another is stale'
                       % ' and '.join(sorted(base)))
        else:
            print("ok:   the A/A population reads %s pairs everywhere it is"
                  ' named' % base.pop())

        # A CLASS's own floor, which the two checks above do not reach.
        # They hold the RUN's floor pair and the carry-back figure across
        # their sites; a class's floor is quoted inside its own block and
        # was checked by nothing, so a block requoting its predecessor's
        # would have ridden a write-up in silence -- the same failure the
        # carry-back check was written for, one population down. Unlike
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
        # The section is last in the run file, so it ends at the next
        # heading OR at the end of the document -- where it used to end at
        # `### Provenance`, which was the next heading in README and is now
        # a chapter of its own there.
        cls_head = (r'^#{1,6} The stride classes, run by run$'
                    r'(.*?)(?=^#{1,6} |\Z)')
        cls_raw = re.search(cls_head, '\n'.join(lines), re.M | re.S)
        cls_sec = re.search(cls_head, uw, re.M | re.S)
        cls_rows = dict(re.findall(r'^\| `([a-z0-9]+)` \|.*\| ([\d.]+)% \|$',
                                   cls_raw.group(1), re.M)) if cls_raw else {}
        cls_leads = ([(m.start(), m.group(1)) for m in
                      re.finditer(r'^\*\*`([a-z0-9]+)` ---', cls_sec.group(1),
                                  re.M)] if cls_sec else [])
        if not cls_rows or not cls_leads:
            bad.append('could not find the class table\'s floor column or'
                       ' the class block leads under `The stride classes,'
                       ' run by run` in %s, so the per-class floor check did'
                       ' not run' % os.path.basename(run_doc or 'no run file'))
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

            # AND THE CLASS COUNTS, against Main.hs rather than against
            # the document's own other sentences. Run 21 added a ninth class
            # and shipped five stale `eight`s plus a summary table nobody
            # held to the shape lists; a class count and a per-class shape
            # count are both derivable with no artifact, so they survive the
            # JSONs being deleted. Structural, not textual: the blocks are
            # counted and the table's own `shapes` column is read, so no
            # phrasing carries the check and rewording cannot silence it.
            # Added 2026-08-29.
            try:
                cdims = dims_by_shape(main_hs)[0]
                want = collections.Counter(
                    class_prefix([sh]) for sh, d in cdims.items()
                    if d['lst'] not in MAIN_LISTS and sh not in added_after
                    and class_prefix([sh]) not in retired)
                full = collections.Counter(
                    class_prefix([sh]) for sh, d in cdims.items()
                    if d['lst'] not in MAIN_LISTS
                    and class_prefix([sh]) not in retired)
            except Exception as exc:                       # noqa: BLE001
                want = None
                bad.append('could not derive the classes from %s (%s), so'
                           ' the class-count checks did NOT run'
                           % (os.path.basename(str(main_hs)), exc))
            if want:
                if len(cls_leads) != len(want):
                    bad.append('the run file carries %d class block(s) where'
                               ' Main.hs defines %d class(es): %s'
                               % (len(cls_leads), len(want),
                                  ', '.join(sorted(want))))
                shape_rows = dict(re.findall(
                    r'^\| `([a-z0-9]+)` \| (\d+) \|', cls_raw.group(1), re.M))
                if not shape_rows:
                    bad.append("the class table's `shapes` column did not"
                               ' parse, so the per-class shape check did NOT'
                               ' run')
                shp = ['`%s` says %s where Main.hs defines %d'
                       % (c, shape_rows[c], want[c])
                       + ('' if full[c] == want[c] else
                          ' (%d defined, %d declared added after the run)'
                          % (full[c], full[c] - want[c]))
                       for c in sorted(shape_rows)
                       if c in want and int(shape_rows[c]) != want[c]]
                if shp:
                    bad.append('the class table\'s shape counts disagree with'
                               ' Main.hs: %s' % '; '.join(shp))
                elif shape_rows and not shp and len(cls_leads) == len(want):
                    print('ok:   %d class block(s) and their table\'s shape'
                          ' counts match the %d class(es) Main.hs defines'
                          % (len(cls_leads), len(want)))

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
        main_shapes = [s for s, d in dims.items()
                       if d['lst'] in MAIN_LISTS and not d['retired']]
        # A main shape retired after this run is back in the population
        # sizes it was timed in, by the same declaration that exempts an
        # added one; the roster-size sites stay today's. 2026-09-04. Case:
        # `retired-shapes-timed-by-the-run-are-exempt`.
        retired_main_after = sorted(
            s for s in retired_after
            if s in dims and dims[s]['lst'] in MAIN_LISTS
            and dims[s]['retired'])
        # The main set as the newest run file measured it: a main-set shape
        # the provenance bullet declares added after the run is exempt from
        # the population sizes below, exactly as a class shape is from the
        # class counts, since 2026-09-02 -- two main-set shapes landed for
        # Run 24 and held Run 23's `over 24 shapes` to Main.hs's 26. The
        # roster-size sites stay held to today's main set, being sentences
        # about the roster as it stands. Case:
        # `main-shapes-added-after-the-run-are-exempt`.
        main_at_run = ([s for s in main_shapes if s not in added_after]
                       + retired_main_after)
        class_sizes = {}
        for s, d in dims.items():
            if (d['cls'] != 'main' and s not in added_after
                    and d['cls'] not in retired):
                class_sizes.setdefault(d['cls'], set()).add(s)
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
        #
        # THIS ONE ASKS FOR EVERY FIGURE AND THE CLASS PROCESS COUNT BELOW
        # ASKS FOR ONE, and the difference is deliberate rather than an
        # oversight in either: `over N shapes` is a convention, so a subset
        # reading is written `on N of the 24` and a figure here that names
        # no population is a sentence to rephrase -- flagging it is the
        # check working. `N class processes` is no such convention, and a
        # run reruns subsets of them, so requiring every figure there fails
        # right prose. Told apart 2026-08-26 by planting a subset mention
        # into each.
        pops = ({len(main_shapes), len(main_at_run)}
                | {len(v) for v in class_sizes.values()})
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

        # THE CLASS PROCESS COUNT, which is the one of Run 14's four wrong
        # subjects that turned out to have both a truth and a phrasing.
        # A run spends one process per class per half, so the figure is
        # len(blocks) times one or two and nothing else -- a structural
        # count, where the carry-back figure and the floor pair are only
        # cross-site agreement and can be uniformly stale.
        #
        # THE BARE TOTAL RESISTED AND IS NOT CHECKED, measured 2026-08-26
        # over both run files rather than argued: `N processes` carries
        # `eighteen`, `nine`, `four` and `fourteen` in run20.md alone --
        # the sequence, one half, the reruns and what survived them, every
        # one correct -- so a set-membership sweep over it would flag right
        # prose or admit anything. `N class processes` reads `sixteen` in
        # run19.md and run20.md, one value in one sentence shape, which is
        # the whole reason this half is checkable and that one is not.
        #
        # IT ASKS FOR AGREEMENT SOMEWHERE, NOT EVERYWHERE, which is the
        # difference between this and the bare total it refused. Requiring
        # every quoted figure to be the structural one fails a run that
        # names a SUBSET, and a run has subsets to name: Run 20 reran four
        # of its class processes, and writing that as `those four class
        # processes were rerun` -- one word from what it does say -- failed
        # the check on right prose, measured 2026-08-26. So a stale total
        # is a run where NO site quotes the figure, which is what staleness
        # means, and a subset beside a correct total is not a defect.
        # Case: `rundoc-miscounts-its-class-processes`.
        #
        # THE RUN FILE'S OWN TEXT, not the concatenated pair, for the reason
        # the stray-lead check above states: README argues about the classes
        # constantly and reads `two class processes add one each` of Run 10's
        # A/A cells, which is right and is not this figure.
        if blocks:
            run_uw = '\n'.join(' '.join(p.split())
                               for p in (run_text or '').split('\n\n'))
            cq = {num(t) for t in
                  re.findall(r'\b([\w-]+)\s+class processes\b',
                             run_uw, re.I)}
            cq.discard(None)
            want = {len(blocks), 2 * len(blocks)}
            if not cq:
                bad.append('no site quotes the class process count as `N'
                           ' class processes`, so that check did not run;'
                           ' a run spends one per class per half, so with'
                           ' %d blocks it is %d or %d'
                           % (len(blocks), len(blocks), 2 * len(blocks)))
            elif not cq & want:
                bad.append('no class process count quoted in prose is one'
                           ' per class per half; the quoted figure(s) are'
                           ' %s, and this run has %d class blocks, so it is'
                           ' %d unpaired or %d paired'
                           % (', '.join(str(n) for n in sorted(cq)),
                              len(blocks), len(blocks), 2 * len(blocks)))
            else:
                print('ok:   the class process count reads %s, which is one'
                      ' process per class per half over %d blocks'
                      % ('/'.join(str(n) for n in sorted(cq & want)),
                         len(blocks)))

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
        m = run_no_of(run_doc)
        lo = [i for i, l in enumerate(lines, 1)
              if l.startswith('## What is open')]
        hi = [i for i, l in enumerate(lines, 1)
              if l.startswith('## The goal')]
        if m and lo and hi and lo[0] < hi[0]:
            run_now = m
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
                    print('        %s: %s' % (where(first), para[:60]))
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
                                  '%s %s'
                                  % (where(i),
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
                       ' or the run number (%s) could not be located'
                       ' in that order, so no prospective promise was'
                       ' checked'
                       % ('line %d' % lo[0] if lo else 'gone',
                          'line %d' % hi[0] if hi else 'gone',
                          m or 'no run file'))
    else:
        # `lint` fails loudly on the same nothing; this went quiet, and a
        # renamed or re-indented roster -- or a wrong --main -- left the
        # prose counts, the floor agreement, the roster and population
        # sizes and the stale-promise sweep all unrun, with only `ok:`
        # lines and exit 0 to show for it. Found 2026-08-17 by review.
        bad.append('BLOCKED: no roster parsed out of %s, so the prose'
                   ' counts, the floor agreement and the open-list sweep'
                   ' did not happen' % os.path.basename(main_hs))

    # Links from standing prose into the run's file. The file is
    # replaced by the next run, so such a link keeps resolving -- step 5
    # re-points it -- while the content it promised leaves: five links
    # reading "the head of the run chapter" decayed exactly that way,
    # their targets' substance having moved to the floor section when Run
    # 11's chapter was replaced. Listed for adjudication at every check,
    # not only at the rename, because the decay happens at the replacement
    # and nothing else looks then. README.md alone is swept, links inside
    # the run's own file being the run's and dying with it; a bare link
    # bullet -- the Contents map's entry -- promises no content beyond the
    # heading and is exempt, or the map would head this list at every
    # check and teach readers to skim it. THE EXEMPTION IS ON THE BULLET
    # ENDING IN THE LINK, so a gloss after it -- `- [Run 19](...), the
    # last run` -- loses it and the map returns to the list; measured
    # 2026-08-25, when the split's own Contents entry did exactly that.
    # Non-vacuous 2026-08-14: planting a bare link into the opening
    # paragraph of a copy listed it with its line; the shipped README
    # lists the replace-list bullet and nothing else, its Contents entry
    # being the exemption's own subject.
    # Scoped to links naming the run file and NO section of it, which is
    # what "the head of the run chapter" was and is the shape that promises
    # unspecified content. A link to a named section promises that section,
    # and the section outlives the run even where its figures do not; a
    # sweep over every link into the file returns two dozen at every check,
    # which is a wall and gets adjudicated as one.
    if run_doc is not None:
        whole = re.compile(r'\]\([^)\s#]*%s/%s\)'
                           % (RUNS_DIR,
                              re.escape(os.path.basename(run_doc))))
        into = [(i, l.strip())
                for i, l in enumerate(readme_doc.split('\n'), 1)
                if whole.search(l)
                and not (l.strip().startswith('- [')
                         and l.strip().endswith(')'))]
        if into:
            print('note: %d link(s) from standing prose into %s as a whole;'
                  ' each is re-verified when the run file is replaced, its'
                  ' content going with it:'
                  % (len(into), os.path.basename(run_doc)))
            for i, l in into:
                print('        %s:%d: %s'
                      % (os.path.basename(readme), i, l[:60]))
        else:
            print('ok:   no standing prose promises content of %s beyond'
                  ' a named section of it' % os.path.basename(run_doc))

    for line in bad:
        print('FAIL: ' + line)
    # LAST LINE, ALWAYS, so that a run piped into `tail` still shows the
    # answer. A pipeline exits with its LAST command's status, so a
    # `| tail` reports tail's 0 whatever this returned -- the rule
    # against piping a verification command is stated three times in
    # these documents and was broken anyway on 2026-08-29. A verdict
    # that survives the pipe is cheaper than a fourth copy of the rule.
    print('VERDICT: %s (exit %d)' % ('FAIL' if bad else 'PASS',
                                     1 if bad else 0))
    return 1 if bad else 0


def check_doc_loud(readme, main_hs, run_doc=None, prev_doc=None):
    """`--check-doc --worklists`, with a tally a truncated read still sees.

    The worklists are what post-run step 6e adjudicates, and a note that
    carries one prints its count on its FIRST line and its items under it,
    so the count leaves the screen before the items do. A session that
    pipes this through `head` or `tail` therefore adjudicates whatever
    survived the pipe and reads it as the whole list -- which is exactly
    what happened on 2026-09-06, when a `tail -30` cut nine stale
    paragraphs out of a worklist of twenty-two and the run cleared the
    thirteen it could see. The nine were then found by a checker agent at
    several hundred thousand tokens.

    So this prints, after everything and before the verdict, one line
    counting the indented worklist items the run emitted. It does not stop
    anyone piping; it makes a pipe that drops items visible in the part a
    `tail` keeps, which is the only place a warning can still be read.
    `check_doc_quiet` has put the verdict last for the same reason since
    2026-08-29.

    Non-vacuity: delete an item from a worklist a document currently
    carries and the tally falls by one; the tally line is the only line
    in this output that changes.
    """
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = check_doc(readme, main_hs, run_doc, prev_doc)
    lines = out.getvalue().split('\n')
    items = [l for l in lines if l.startswith('        ') and l.strip()]
    verdict = [l for l in lines if l.startswith('VERDICT: ')]
    for line in lines:
        if line.startswith('VERDICT: '):
            continue
        if line or line == '':
            print(line)
    print('worklist tally: %d listed item(s) above, under the notes that'
          ' carry lists -- a `head` or `tail` over this output drops some'
          ' of them silently, so read it whole (2026-09-06)' % len(items))
    for line in verdict:
        print(line)
    return rc


def check_doc_quiet(readme, main_hs, run_doc=None, prev_doc=None):
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

    Non-vacuity, 2026-08-16, against a copy: renaming the run chapter's
    heading printed two FAIL lines -- the dead anchors, and the
    replace-list bullet that no longer covers the section -- and exited 1,
    where the same copy unbroken printed no FAIL and exited 0. The withheld
    counts differ by exactly those two lines, which is what promoting them
    out of the pool should do. That heading is now a file name, and the
    same break is renaming `runs/run<N>.md` under the links that reach it.
    """
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = check_doc(readme, main_hs, run_doc, prev_doc)
    lines = [l for l in out.getvalue().split('\n') if l]
    fails = [l for l in lines if l.startswith('FAIL: ')]
    verdict = [l for l in lines if l.startswith('VERDICT: ')]
    rest = [l for l in lines if l not in fails and l not in verdict]
    for line in fails:
        print(line)
    print('%d line(s) withheld; rerun with --worklists for them' % len(rest))
    # The verdict goes LAST here as it does unpiped, for the same reason:
    # this mode is the one a session pipes, and a withheld count is not an
    # answer. Added 2026-08-29.
    for line in verdict:
        print(line)
    return rc


PROPERTIES_HEAD = re.compile(r'#+ The properties the next run should test')


def property_items(text):
    """The properties section's numbered items, as (number, line, body).

    A run returns a verdict on each. The prose between and after them is
    deliberately NOT included: that is where retirements are recorded, and
    a retirement names the arm it retires, so a check over the section
    would fire on every one of them.
    """
    lines = text.split('\n')
    try:
        i = next(k for k, l in enumerate(lines) if PROPERTIES_HEAD.match(l))
    except StopIteration:
        return []
    end = next((k for k, l in enumerate(lines[i + 1:], i + 1)
                if l.startswith('## ')), len(lines))
    out, cur = [], None
    for k in range(i, end):
        l = lines[k]
        m = re.match(r'^(\d[\d, ]*)\. ', l)
        if m:
            if cur:
                out.append(cur)
            cur = [m.group(1), k + 1, l[m.end():]]
        elif cur is not None:
            if l.startswith('   ') and l.strip():
                cur[2] += ' ' + l.strip()
            else:
                out.append(cur)
                cur = None
    if cur:
        out.append(cur)
    return [tuple(c) for c in out]


def lint(main_hs, readme, run_doc=None, quiet=False):
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

    **THE DOCUMENTATION IS THE PAIR**, README.md and the run's own file:
    an arm's only mention is often a row of the Results table or of a class
    block, and those are in the run file. Reading README alone would have
    reported some twenty arms as documented nowhere, which is a check that
    fails for being pointed at half its subject.
    """
    try:
        main = open(main_hs).read()
        doc = open(readme).read()
        run_text = open(run_doc).read() if run_doc else ''
        if run_doc:
            doc += '\n' + run_text
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
    where_ = ('README and %s' % os.path.basename(run_doc) if run_doc
              else 'README (and no run file was given)')
    if undocumented:
        bad.append('%d roster arm(s) named nowhere in %s: %s'
                   % (len(undocumented), where_, ', '.join(undocumented)))
    else:
        print('ok:   all %d roster arms are named somewhere in %s, %d of'
              ' them timed' % (len(names), where_, len(timed)))

    unrostered = sorted(defined - rostered)
    if unrostered:
        bad.append('%d strategy function(s) defined but absent from the'
                   ' roster, so neither timed nor checked: %s'
                   % (len(unrostered), ', '.join(unrostered)))
    else:
        print('ok:   every fb function defined in Main.hs is in the roster'
              ' (%d of them, one of which is the reference)' % len(rostered))

    # ONE SITE FOR THE PARKED SET, which the properties check below and the
    # registration check under it both ask for. It was computed twice,
    # once in each, which is `two-spellings` in a file whose own corpus
    # tracks that family -- harmless while the two expressions agreed and
    # exactly the shape that stops agreeing.
    untimed = set(names) - set(timed)

    # A LIVE PROPERTY MAY NOT NAME AN ARM THE ROSTER NO LONGER TIMES, or
    # it cannot be read on this run at all, and nothing else here sees
    # that. A retired item is exempt by the marker it already carries,
    # `**Retired` opening its body, so retiring one in prose is what
    # clears it, and that coupling is what this check exists to force.
    # The rule is stricter than the parking that prompts it: an item may
    # not name an untimed arm even to say that it is untimed, that half
    # belonging in the prose beside the item, where every reading does.
    # Loosening it to exempt a self-declaring clause is refused -- the
    # predicate would be `does the sentence admit it`, which is the
    # noise-for-signal shape this file refuses elsewhere.
    # AND A MUTANT'S JUDGE MAY NOT NAME ONE EITHER: a judge runs against
    # the newest run's own files, so an arm the roster parked reads red
    # before any mutation, which selftest-mutants.py counts as `could not
    # be applied` and not as a catch -- the rate column's judge named the
    # -u1 leaf after c870e1e parked it, and only a check-all over Run 39's
    # write-up met it. Case: `lint-refuses-a-mutant-judge-naming-a-parked-arm`.
    mpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'mutants.py')
    if os.path.exists(mpath):
        spec = importlib.util.spec_from_file_location('mutants_lint', mpath)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        judged = []
        for mut in getattr(mod, 'MUTANTS', []):
            # Hyphenated names only: `build`, an untimed arm, is also an
            # English word, and a judge's prose carried it as one.
            gone = sorted(a for a in untimed if '-' in a
                          and re.search(r'(?<![\w-])%s(?![\w-])'
                                       % re.escape(a), mut[4]))
            if gone:
                judged.append('%s: %s' % (mut[0], ', '.join(gone)))
        if judged:
            bad.append('%d mutant judge(s) name arms the roster no longer'
                       ' times, so each reads red unmutated:\n        %s'
                       % (len(judged), '\n        '.join(judged)))
        else:
            print('ok:   no mutant judge names an untimed arm (%d read)'
                  % len(getattr(mod, 'MUTANTS', [])))

    if run_doc:
        items = property_items(run_text)
        stale = []
        for num, ln, body in items:
            if body.lstrip().startswith('**Retired'):
                continue
            gone = sorted(set(re.findall(r'`([A-Za-z][A-Za-z0-9-]*)`', body))
                          & untimed)
            if gone:
                stale.append('property %s (%s:%d): %s'
                             % (num, os.path.basename(run_doc), ln,
                                ', '.join(gone)))
        if stale:
            bad.append('%d live propert(y/ies) name arms the roster no'
                       ' longer times, so the property cannot be read on'
                       ' this run -- retire it or re-aim it:\n        %s'
                       % (len(stale), '\n        '.join(stale)))
        elif items:
            print('ok:   every arm a live property names is still timed'
                  ' (%d item(s) read, %d untimed arm(s) to avoid)'
                  % (len(items), len(untimed)))
        else:
            # An `ok` over zero items is the vacuous pass this file refuses
            # everywhere else, and it is reachable: a run file whose
            # properties section has not been written yet parses to no
            # items at all. Proved by `--run-doc /dev/null`, which read 0
            # and said `ok` until this branch existed.
            print('skip: no properties section in %s, so no live property'
                  ' was held to the roster' % os.path.basename(run_doc))
    else:
        # `--run-doc` defaults to the newest in runs/, so this fires only
        # where that directory is empty -- and a check that says nothing
        # there would be a silent search, which this file refuses.
        print('skip: no run file, so no live property was held to the'
              ' roster')

    # THE REGISTRATION, WHICH NOTHING HERE READ UNTIL 2026-09-04. The check
    # above holds a live PROPERTY to the timed roster. A REGISTRATION is
    # the same shape of promise about the same arms -- written before the
    # run where a property is written after it -- and no check reached it
    # at all,
    # which the open list has said outright since Run 24 lost a clause of
    # one to an arm the same commit parked. Two questions, both answerable
    # off the document and neither needing a run:
    #
    #   every arm an OPEN registration names is TIMED, so its prediction can
    #   be read on the run it was registered for; and
    #   every `task N` it defers to RESOLVES to a numbered task under the
    #   run-scoped tasks heading, so a deferral points at something; and
    #   THAT TASK'S OWN ARMS are timed too, since 2026-09-05, a deferral
    #   being a second population the registration is answerable for.
    #
    # WHAT IT DOES NOT ASK is whether the task it resolves to still carries
    # a prediction. Run 25's registration deferred its item (4) to task 10,
    # whose own item for the two window views had been withdrawn that same
    # day: the pointer resolved and the sentence around it was false. `is
    # this still a prediction` has no cheap predicate -- the withdrawal is
    # prose -- so it stays pre-run step 12b's, a reading, and this check
    # names what it covers rather than implying the rest.
    #
    # ARMS ARE READ AS THE PROPERTIES CHECK READS THEM: a backticked token
    # that
    # the roster carries as `Only`. A registration is thick with backticks
    # that are not arms -- `predict: cross list 1.0 within 0.7%`,
    # `LOOP_DEADSPOT=1`, section names -- and intersecting with the parked
    # set is what keeps those out without a vocabulary to maintain. What it
    # also keeps out is an arm named by its SUFFIX, `-u1` for
    # `mut-odo-vecdims-add-in-leaf-u1`, which a registration writes once it
    # has spelled the name out: a parked arm named that way alone passes.
    # THE README ALONE, and not `doc`, which carries the run file appended
    # to it. A registration lives in the open list while its run is in
    # hand and MOVES INTO runs/$R.md at post-run step 5 -- so scanning the
    # pair would hold a FINISHED run's registration to today's roster,
    # whose whole point is that it has moved since. Run 24's own
    # registration names arms this prune parked, and would fail this check
    # the moment its file used the open list's form. It does not today,
    # which is the form saving the scope rather than the scope saving
    # itself. The skip line below names the README because the README is
    # what was read.
    paras = [t for _, t, _ in unwrapped_paragraphs(
        open(readme).read().split('\n'))]
    regs = [t for t in paras
            if re.match(r'- `OPEN` \*\*What Run \d+ is built to answer', t)]
    # ANY heading closes the tasks section, not `###` alone: the section
    # is followed by another `###` today, so a `##` guard would have been
    # indistinguishable from this until the day a section moved and every
    # numbered paragraph after it counted as a task on offer.
    tasks, in_tasks = {}, False
    for t in paras:
        if t.startswith('#'):
            in_tasks = t.startswith('### Recommended tasks after Run')
        elif in_tasks:
            m = re.match(r'(\d+)\.\s+`', t)
            if m:
                tasks[m.group(1)] = t
    if not regs:
        # No OPEN registration is the normal state between runs -- the
        # entry moves into the run's own file at post-run step 5 and the
        # open list keeps an ANSWERED pointer -- so this is a skip and not
        # a pass. Saying `ok` here would be the vacuous read this file
        # refuses of every other search.
        print('skip: no OPEN registration in %s, so none was held to the'
              ' roster' % os.path.basename(readme))
    else:
        trouble = []
        for t in regs:
            num = re.search(r'What Run (\d+)', t).group(1)
            reads = []
            # THE LEAD IS THE MOVER'S KEY, held here because nothing held
            # it where it is written. `--move-registration` matches the
            # bold lead WHOLE -- `...is built to answer, registered before
            # it runs.**` -- and refuses anything else, so a registration
            # whose lead carries one clause more is a refusal at post-run
            # step 5, a day or a week after the entry was committed and
            # with the hours already spent. Run 33 declared its pair with
            # `--- declared 2026-09-15 evening by request, the recipes in
            # [Run 32's file](...)` inside the bold span; `--lint` and
            # `--check-doc` both passed it at pre-run 7, and the mover
            # refused it after the run. The clause belongs in the body,
            # where it moves into the run file with the rest.
            want = ('- `OPEN` **What Run %s is built to answer, registered'
                    ' before it runs.**' % num)
            if not t.startswith(want):
                trouble.append("Run %s's registration lead is not the form"
                               ' --move-registration matches, so the move at'
                               ' post-run step 5 will refuse it: it wants'
                               ' %r and the entry opens %r'
                               % (num, want[-44:], t[:len(want) + 12]))
            gone = sorted(set(re.findall(r'`([A-Za-z][A-Za-z0-9-]*)`', t))
                          & untimed)
            if gone:
                trouble.append('Run %s\'s registration names arms the roster'
                               ' does not time: %s' % (num, ', '.join(gone)))
            # `[Tt]ask`, because a registration opens its deferral with
            # the word capitalised -- `Task 10's, read there` -- and the
            # lower-case pattern this was written with found nothing on the
            # one document it exists for. Caught by breaking it, 2026-09-04,
            # which is the whole of why the break is taken.
            # ONE findall, and the mutant that breaks it is why: the
            # deferral set is read once and both checks below take their
            # halves of it, where two copies of the pattern left
            # `--lint stops resolving a registration's task pointers`
            # with an anchor occurring twice and so unappliable -- a
            # mutant that proves nothing either way, which is worse than
            # one that fails (2026-09-05).
            deferred = set(re.findall(r'\b[Tt]ask (\d+)', t))
            # EVERY ITEM ADJUDICABLE, since 2026-09-17: a `predict:` span
            # carrying its scope, a `script:` committed beside it, or a
            # deferral to a task, which the checks below hold. Run 34's
            # registration left four items' clauses to be read by hand off
            # --cells and the counts files, and one of its spans named no
            # half, so its verdict and the item's prose disagreed.
            for inum, body in items_from_flat(' '.join(t.split())):
                spans = PREDICT_RE.findall(body)
                scripts = re.findall(r'`script: ([^`]+)`', body)
                for sp in spans:
                    _k, _a, _w, _x, pops, _v, half = parse_span(sp)
                    reads.append('(%s) `predict: %s`\n'
                                 '              -> %s'
                                 % (inum, sp, span_reads(sp)))
                    # AN `on` NAMING A POPULATION, and not the `on` of
                    # `on views S,...`, which names shapes: the first form
                    # of this test took either, so a countdiff span naming
                    # views and no population passed and was read on
                    # every file. Case: `registration-views-are-no-
                    # population-scope`.
                    if not pops or not half:
                        trouble.append("Run %s's item (%s) span `predict:"
                                       " %s` carries no scope: it wants"
                                       ' `on POP,...` and basis, control or'
                                       ' both, or it is read on every file'
                                       ' handed in' % (num, inum, sp))
                    # AND `both` ON A CROSS-HALF KIND WHOSE TARGET IS
                    # NOT RECIPROCAL-SAFE, refused since 2026-09-19:
                    # `cross` and `counts` read this half over the other,
                    # so `both` reads them once each way and the two
                    # figures are reciprocals. A target away from 1 holds
                    # on at most one half, which is Run 35's item (3) in
                    # a new dress -- and Run 36's registration wanted
                    # `cross list 1.2974`, where `both` would have
                    # killed half its spans by construction. Nothing
                    # said so: the grammar admits it and the arms-and-
                    # scope checks above cannot see it. Case:
                    # `registration-both-on-a-non-unity-cross`.
                    if half == 'both' and _k in ('cross', 'counts') \
                            and len(_a) == 2:
                        try:
                            x = float(_a[1])
                        except ValueError:
                            x = None
                        band = _w if isinstance(_w, float) else (
                            0.1 if _k == 'counts' else 1.0)
                        if x and x > 0 and abs(1.0 / x - x) * 100 > band:
                            trouble.append(
                                "Run %s's item (%s) span `predict: %s` is"
                                ' scoped `both` on a cross-half kind with'
                                ' a target away from 1: it will be read'
                                ' %.4f on the basis and %.4f on the'
                                ' control, which %s points apart cannot'
                                ' both be within %s. Name `basis` or'
                                ' `control`'
                                % (num, inum, sp, x, 1.0 / x,
                                   round(abs(1.0 / x - x) * 100, 2),
                                   ('%g%%' % _w) if isinstance(_w, float)
                                   else 'the default band'))
                for sc in scripts:
                    name = sc.split()[0]
                    # The committed MODE as well: a registration says to run
                    # its script as `./NAME`, and Run 39's named one
                    # committed at 100644, which that refuses. Case:
                    # `registration-script-not-executable`.
                    staged = subprocess.run(
                        ['git', 'ls-files', '-s', '--', name],
                        cwd=os.path.dirname(os.path.abspath(main_hs)),
                        capture_output=True, text=True).stdout.split()
                    if not staged:
                        trouble.append("Run %s's item (%s) names script %s,"
                                       ' which is not committed, so the'
                                       ' clause it reads is read by nothing'
                                       ' a later session can run'
                                       % (num, inum, name))
                    elif staged[0] != '100755':
                        trouble.append("Run %s's item (%s) names script %s,"
                                       ' which is committed without its'
                                       ' executable bit, so `./%s` refuses'
                                       ' to run it' % (num, inum, name, name))
                if not spans and not scripts \
                        and not re.search(r'\b[Tt]ask \d+', body):
                    trouble.append("Run %s's item (%s) carries neither a"
                                   ' `predict:` span nor a committed'
                                   ' `script:`, so nothing adjudicates it'
                                   ' but a reading by hand' % (num, inum))
                # AND A PRIOR NAMES WHAT DERIVED IT, since 2026-09-22. A
                # span whose target is not 1.0 quotes a FIGURE from an
                # earlier run, and the error no pass here can see is a
                # figure quoted against the wrong mode IN AN ITEM'S PROSE:
                # `--carried` derives what a `pair` span quotes, so a
                # span's own figures are read, and the sentence beside a
                # span is read by nothing -- Run 38's item (1)
                # called 0.51 an A/A floor where `--aa` gives 0.59% and the
                # 0.51 is `--compare`'s widest arm-to-duplicate gap. That
                # registration stated its provenance ONCE, at the head, for
                # every prior at once, which is exactly what let it through:
                # a collective claim is checked against no item. A 1.0 span
                # quotes nothing and is exempt, which is what keeps the null
                # families out of this.
                # IT IS A FLOOR AND NOT THE TIE: a mode or a file named
                # ANYWHERE in the item satisfies it, so an item calling
                # 0.51 `the floor --aa gives` passes. What it buys is that
                # provenance is stated per item, where a collective claim
                # at the head is checked against none; tying a figure to
                # its mode stays pre-run 12b's reading.
                quoted = [sp for sp in spans if re.search(
                    r'\s(?!1\.0\b)\d+\.\d+\s+within', sp)]
                if quoted and not re.search(
                        r'`--[a-z][a-z-]*`|[\w-]+\.(?:json|txt)', body):
                    trouble.append(
                        "Run %s's item (%s) quotes a prior and names neither"
                        ' the mode nor the file that derives it, so a figure'
                        ' read off the wrong mode is invisible here'
                        % (num, inum))
            lost = sorted(deferred - set(tasks))
            if lost:
                trouble.append("Run %s's registration defers to task(s) that"
                               ' are not under the tasks heading: %s'
                               % (num, ', '.join(lost)))
            # AND THE ARMS OF WHAT THE DEFERRAL LANDS ON, which is a
            # second population and was read by nothing until
            # 2026-09-05. Run 25's item (4) deferred to task 10, three
            # of whose four class predictions are stated against
            # `lib-stage2` and `canon-vecdims`, parked the day after
            # they were written: three predictions of four unreadable
            # before the machine was started, past a check that had
            # reported the pointer good. Same intersection as the
            # registration's own arms, one indirection along.
            for n in sorted(deferred & set(tasks)):
                away = sorted(set(re.findall(r'`([A-Za-z][A-Za-z0-9-]*)`',
                                             tasks[n])) & untimed)
                if away:
                    trouble.append("Run %s's registration defers to task %s,"
                                   ' which names arms the roster does not'
                                   ' time: %s' % (num, n, ', '.join(away)))
            # THE PREVIOUS RUN FILE MUST NAME THIS REGISTRATION, since
            # 2026-09-18. Two committed documents declared Run 35 for
            # different pairs -- the open list registered Run 34's compiler
            # pair rebuilt from the moved source, and runs/run34.md's
            # compares-against went on declaring the two -O2 passes -- and
            # every mechanical pass here stayed green, this one reading a
            # registration's ARMS and not its pair. A preparation reads
            # what the pair varies in that section and what the run
            # answers in the registration, so where both exist the section
            # points at the registration; which of them is right stays the
            # owner's, and this only refuses the silence.
            prev_doc = os.path.join(os.path.dirname(os.path.abspath(readme)),
                                    'runs', 'run%d.md' % (int(num) - 1))
            if os.path.exists(prev_doc):
                try:
                    txt = io.open(prev_doc, encoding='utf-8').read()
                except OSError:
                    txt = ''
                m = re.search(r'^## What the next run compares against$'
                              r'(.*?)(?=^## |\Z)', txt, re.M | re.S)
                if m and not re.search(r'\[registered[^\]]*\]\[open\]',
                                       m.group(1)):
                    trouble.append(
                        "Run %s is registered in the open list and"
                        " runs/run%d.md's compares-against section names no"
                        " registration -- the two can declare DIFFERENT"
                        " pairs with every check here green, which is what"
                        " Run 35 met. Point the section at it, as"
                        " `[registered <date>][open]`"
                        % (num, int(num) - 1))
            # AND A COUNT PRIOR NO ARTIFACT HERE CAN RE-DERIVE, which is a
            # note and not a refusal: the sweep may be a probe's, kept
            # elsewhere or not kept at all, and the prior may be quoted
            # from a run whose files are gone. Run 35's items (2) and (3)
            # quoted a plain build's instruction counts and no counts file
            # here named the arm, so pre-run 12b read their times back and
            # not their instructions -- the reading, not the figure, is
            # what goes missing.
            arms = {a for pair in
                    re.findall(r'predict:\s+count(?:diff)?\s+([\w-]+)'
                               r'(?:\s+([\w-]+))?', t)
                    for a in pair if a}
            if arms:
                have = set()
                for f in sorted(glob.glob(os.path.join(
                        os.path.dirname(os.path.abspath(readme)),
                        '*counts*.txt'))):
                    try:
                        have |= {a for a in arms
                                 if a in io.open(f, encoding='utf-8',
                                                 errors='replace').read()}
                    except OSError:
                        pass
                    if have >= arms:
                        break
                lost = sorted(arms - have)
                if lost:
                    print('note: Run %s quotes a count prior for %s, and no'
                          ' counts file here names %s -- the sweep behind it'
                          ' is not on disk, so pre-run 12b can read the'
                          ' times back and not the instructions'
                          % (num, ', '.join(lost),
                             'them' if len(lost) > 1 else 'it'))
            # WHAT EACH SPAN COMPARES, since 2026-09-18, for the author
            # to read against the sentence beside it at pre-run 12b:
            # the mode, the operands and their orientation. The
            # arms-and-scope checks above cannot see a span that asks
            # a question its sentence does not, which is what killed
            # Run 35's item (3) before it ran; span_reads says why.
            if reads:
                print("      Run %s's %d span(s), each as --predictions will"
                      ' compare it; read every line against the sentence'
                      ' beside its span:' % (num, len(reads)))
                for r in reads:
                    print('          ' + r)
        if trouble:
            bad.append('%d problem(s) in the OPEN registration(s), which no'
                       ' other check here reads:\n        %s'
                       % (len(trouble), '\n        '.join(trouble)))
        else:
            print('ok:   every arm the OPEN registration(s) name is timed,'
                  ' and so is every arm of every task they defer to, which'
                  ' resolves; every item carries a scoped span, a committed'
                  ' script or a deferral (%d registration(s), %d task(s) on'
                  ' offer)'
                  % (len(regs), len(tasks)))

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
        print('      timed, each with the reason at its entry:'
              if not quiet else
              '      timed, each with the reason at its entry; --worklists'
              ' names them')
        # Not at hyphens: every one of these names carries them, and a name
        # split across two lines is one no grep of this output can find.
        # WITHHELD UNDER --quiet, 2026-09-18: this block is four fifths of
        # what --lint prints and it answers one question, which arms are
        # checked and not timed. A run calls --lint for its VERDICT and for
        # the roster counts on the first line; Run 35 called it for two
        # numbers and read thirty-four lines of names. The count line
        # stays, so nothing is hidden without saying so.
        if not quiet:
            for line in textwrap.wrap(', '.join(only), 66,
                                      break_on_hyphens=False,
                                      break_long_words=False):
                print('        ' + line)
    for line in bad:
        print('FAIL: ' + line)
    # LAST LINE, ALWAYS, so that a run piped into `tail` still shows the
    # answer. A pipeline exits with its LAST command's status, so a
    # `| tail` reports tail's 0 whatever this returned -- the rule
    # against piping a verification command is stated three times in
    # these documents and was broken anyway on 2026-08-29. A verdict
    # that survives the pipe is cheaper than a fourth copy of the rule.
    print('VERDICT: %s (exit %d)' % ('FAIL' if bad else 'PASS',
                                     1 if bad else 0))
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
        base_sunk = [sh for sh in shapes if 'list' in cells[sh]
                     and cells[sh]['list']['net'] <= 0]
        # A sunk BASELINE cell is still a fault and still fails the file: it
        # takes every row of its shape with it, so nothing that shape carries
        # is readable. A sunk cell of any other arm is not, and calling it one
        # was what failed a whole run over the canonicalizing arms doing what
        # they were rostered to do -- `live_shapes` has the ruling, taken
        # 2026-08-26. Named and counted here rather than passed in silence.
        if term_bad or base_sunk:
            bad.append('correction: %d shape(s) with a non-positive forcing'
                       ' term and %d whose `list` it did not leave positive,'
                       ' which takes every row of those shapes with it'
                       % (len(term_bad), len(base_sunk)))
        elif sunk:
            rows = sorted({st for _, st in sunk})
            ok.append('correction: the forcing term is positive on all %d'
                      ' shape(s), from %d half/halves, and leaves %d cell(s)'
                      ' of %d row(s) non-positive -- work the arm removed,'
                      ' dropped from those rows and named by `health`: %s'
                      % (len(shapes), len(halves), len(sunk), len(rows),
                         ', '.join('%s/%s' % (sh, st) for sh, st in sunk[:5])))
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
        capped = short = 0
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
            live = live_shapes(cells, shapes, st)
            if not live:
                bad.append('%s: a cell the forcing term did not leave'
                           ' positive, so this row has no geomean to'
                           ' bracket' % st)
                continue
            if len(live) < len(shapes):
                short += 1
            ratios = [cells[sh][st]['net'] / cells[sh]['list']['net']
                      for sh in live]
            capped += winsorize([math.log(r) for r in ratios])[1]
            got = time_of(cells, shapes, st)
            if not min(ratios) - TOL <= got <= max(ratios) + TOL:
                bad.append('%s: winsorized geomean %.6g outside the per-shape'
                           ' range %.6g..%.6g' % (st, got, min(ratios),
                                                  max(ratios)))
        ok.append('winsorizing: every row covers all %d shapes%s, and every'
                  ' geomean lands inside its own per-shape range (%d cell(s)'
                  ' capped in all)'
                  % (len(shapes),
                     '' if not short else
                     ' but %d, which cover fewer, the sunk cells `health`'
                     ' names' % short,
                     capped))

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
    # LAST LINE, ALWAYS, so that a run piped into `tail` still shows the
    # answer. A pipeline exits with its LAST command's status, so a
    # `| tail` reports tail's 0 whatever this returned -- the rule
    # against piping a verification command is stated three times in
    # these documents and was broken anyway on 2026-08-29. A verdict
    # that survives the pipe is cheaper than a fourth copy of the rule.
    print('VERDICT: %s (exit %d)' % ('FAIL' if bad else 'PASS',
                                     1 if bad else 0))
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
    p.add_argument('--cell', metavar='SHAPE/ARM',
                   help='with --compare, one cell on both halves: raw and'
                   ' corrected slope, and the mutator clock and foreign CPU'
                   ' off each half\'s log where it carries @@wild samples')
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
    p.add_argument('--per-shape', action='store_true',
                   help='with --pair, the per-shape ratios the range'
                        ' line is a max and min of; with --pair and ONE'
                        ' --counts sweep, each shape\'s instruction'
                        ' difference beside the sum-only-early/late'
                        ' spread; with --compare or'
                        ' --compare --counts, one line per arm of the'
                        ' per-shape ratios in shape order; with'
                        ' --compare --alloc, how much the OTHER half'
                        ' ALLOCATES per arm, both directions printed,'
                        ' which is the reading the `alloc` column'
                        ' cannot give, being a median that must not be'
                        ' divided across halves')
    p.add_argument('--pair', nargs=2, action='append', default=[],
                   metavar=('A', 'B'))
    p.add_argument('--compare', metavar='OTHER.json',
                   help='this run against another of the same population,'
                        ' one arm at a time')
    p.add_argument('--chapter', action='store_true',
                   help='with --compare: the run chapter\'s mechanical'
                        ' figures, as --block does for a class')
    p.add_argument('--alloc', action='store_true',
                   help='with --compare: allocation agreement instead of'
                        ' times, on the multiple the alloc column publishes')
    p.add_argument('--movers', nargs='?', type=float, const=3.0,
                   metavar='PCT',
                   help='with --compare: the arms whose geomean moved past'
                        ' PCT percent (default 3), counted and grouped by'
                        ' the same comparison that lists them')
    p.add_argument('--counts', nargs='+', metavar='SWEEP.txt',
                   help='TWO sweep files with --compare: run-counts.sh\'s'
                        ' instruction counts beside the time ratio, per arm'
                        ' -- the count column owes criterion nothing, so time'
                        ' moving with counts is codegen and time moving'
                        ' without them is the runtime or the memory. ONE'
                        ' sweep file with --pair A B: the corrected'
                        ' instruction ratio of that pair WITHIN one half,'
                        ' beside the raw one -- which is the question a'
                        ' registration derived from a count ratio asks, and'
                        ' the arity a reader of this line alone has twice'
                        ' hand-rolled instead')
    p.add_argument('--ci', action='store_true',
                   help='with --compare: each arm\'s CI%% median against'
                        ' the other run\'s, the column\'s own statistic')
    p.add_argument('--bridge', action='store_true',
                   help='with --compare: each arm as a ratio to `list` in'
                        ' its own run, which a box change cannot move')
    p.add_argument('--winsor', action='store_true',
                   help='the plain per-shape geomean beside the published'
                        ' winsorized one, per timed row, with how many cells'
                        ' the cap touched -- what the `time` column owes to'
                        ' its own estimator rather than to the arm')
    p.add_argument('--band', type=float, default=3.3, metavar='PCT',
                   help='with --bridge: the drift band, default 3.3')
    p.add_argument('--markdown', action='store_true')
    p.add_argument('--fingerprint', action='store_true')
    p.add_argument('--classes', nargs='+', metavar='CLASS.json',
                   help='with --fingerprint: the class JSONs whose shapes'
                        ' fill the second table; with --extremes, the'
                        ' populations to rank')
    p.add_argument('--counts-totals', dest='counts_totals',
                   metavar='RUN',
                   help='what each counted leg of RUN cost, per'
                        ' population and half, off the counts files'
                        " own `# end` stamps -- the scale a pair"
                        ' note asks for leg by leg')
    p.add_argument('--movement', action='store_true',
                   help="the published `time` column of this run against"
                        " the table in --run-doc, the note's COMPARE run's"
                        ' file unless given, row by row -- post-run'
                        ' step 5a, whose window the install closes')
    p.add_argument('--floor-pairs', dest='floor_pairs', metavar='RUN',
                   help="every A/A copy of RUN against its original, per"
                        ' population and half, judged against that'
                        " population's own floor -- the standing"
                        ' floor-pair registration, read in one call')
    p.add_argument('--series', nargs='+', metavar='ARG',
                   help='A B SHAPE [DIR]: A over B on SHAPE on every run'
                        "'s main set in DIR, run by run and half by half,"
                        " each beside that half's floor -- one cell's"
                        ' readings as a table, where prose requoted them')
    p.add_argument('--repoint', metavar='PREV',
                   help='post-run step 5: move README\'s links into'
                   ' runs/PREV.md to the run file --run-doc names (the newest'
                   ' by default), keeping the ones whose own text names PREV')
    p.add_argument('--counts-cost', dest='counts_cost', metavar='RUN',
                   help='each counts stage\'s duration off RUN-evening.txt,'
                   ' per population and per half, with each half\'s total')
    p.add_argument('--over-list', dest='over_list', metavar='RUN',
                   help='every timed non-control cell of RUN slower'
                        " than its shape's `list`, over every"
                        ' population and both halves, with the count'
                        ' it read so the silence is a reading')
    p.add_argument('--half-movers', dest='half_movers', nargs='+',
                   metavar='RUN',
                   help='RUN [PREV]: each half of RUN against the same half'
                        " of PREV, the note's COMPARE run unless given,"
                        ' over every population both have, naming the'
                        ' arms past the floor on ONE half and inside it'
                        ' on the other -- the term a file instance or a'
                        ' binary carries, which no within-pair reading'
                        ' sees; post-run step 4a')
    p.add_argument('--cell-movers', dest='cell_movers', nargs='+',
                   metavar='RUN',
                   help='RUN [N]: every cell of RUN across its halves,'
                        ' time beside counts over every population,'
                        ' the N (default 20) ranked by what the counts'
                        ' do not explain -- the single cell an arm'
                        ' geomean dilutes, and the count-led offender'
                        ' named where it has a name; post-run step 4b')
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
    p.add_argument('--predictions', action='store_true',
                   help="with --compare: adjudicate the registration's"
                        ' `predict:` spans, HELD or KILLED each, and name'
                        ' the items carrying none as yours')
    p.add_argument('--brief', action='store_true',
                   help='the default now; kept so older recipes still run')
    p.add_argument('--verbose', action='store_true',
                   help='restore the standing explanation --brief drops;'
                        ' no computed figure differs either way')
    p.add_argument('--in-place', action='store_true',
                   help='install --markdown/--fingerprint/--block tables'
                        " into the run's own file instead of printing"
                        ' them')
    p.add_argument('--prose-facts', metavar='RUN',
                   help='the figures a write-up quotes, gathered'
                        ' from log-read-RUN/ and computed nowhere:'
                        ' per population and half the A/A bar, how'
                        ' many arms clear it and the counted work,'
                        ' and every in-scope span with its verdict.'
                        ' The box-and-window half is for-brief.txt,'
                        ' which it names rather than copies')
    p.add_argument('--brief-dir', metavar='DIR', default='.',
                   help='with --brief-update: the directory holding'
                        ' log-read-RUN/ and checker-brief.txt, the'
                        ' working one by default')
    p.add_argument('--brief-update', metavar='RUN',
                   help="paste the run's own facts into"
                        ' checker-brief.txt from'
                        ' log-read-RUN/for-brief.txt -- its two THIS'
                        ' RUN ONLY items, which are the half that'
                        ' goes stale and the half a checker cannot'
                        ' tell is stale. PRETIP and RUNTIP stay'
                        ' yours: they are commits')
    p.add_argument('--lost', action='store_true',
                   help='the paragraphs step 5\'s copy had that this tree'
                        ' has no counterpart for, over BOTH documents --'
                        ' the one reading that sees a deletion, every'
                        ' gate here being a predicate over what is'
                        ' present. Post-run step 6e. A reading, not a gate')
    p.add_argument('--stale', action='store_true',
                   help="the figures this run's file KEPT from the"
                        ' step-5 copy inside paragraphs it edited --'
                        ' the defect --inherited cannot see, an'
                        ' edited paragraph being in the diff and its'
                        ' surviving numeral reading as context.'
                        ' Word numerals count. A reading, not a gate')
    p.add_argument('--rows', nargs='+', metavar='ARM',
                   help='with --markdown: print only these rows, header'
                        ' and rule included. The table is computed whole'
                        ' and filtered on the way out, so the notes and'
                        ' the carry-forward still read every row')
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--lint', action='store_true')
    p.add_argument('--check-doc', action='store_true')
    p.add_argument('--imperative', action='store_true',
                   help="with --checklist: the default form, each step"
                        " through its `why:` line; accepted so that older"
                        ' invocations keep working')
    p.add_argument('--full', action='store_true',
                   help="with --checklist: the reasons under each step's"
                        ' `why:` line too')
    p.add_argument('--record', nargs='?', const='', metavar='NAME',
                   help='print series/NAME.tsv aligned; alone, list them')
    p.add_argument('--modes', action='store_true',
                   help="every mode `main` dispatches on, read off"
                        " this file's source: the `if` tests in the"
                        ' order the program reads them, so a flag'
                        ' with two arities has two rows. Needs no'
                        ' run file')
    p.add_argument('--inherited', action='store_true',
                   help="the paragraphs this run's file carried"
                        " WHOLE from the previous run's and which"
                        ' name a run or call themselves this run\'s'
                        ' -- the class of defect the two checker'
                        " passes cannot see, their diff base being"
                        ' the copy step 5 made. A reading, not a'
                        ' gate: it never refuses. --all adds the'
                        ' second list, the CHANGED paragraphs that'
                        ' still name the previous run, which is'
                        ' ordinary in a delta bullet or a series and'
                        ' so runs six times the length at a fraction'
                        ' of the signal')
    # The note: worklists are write-up material, adjudicated once at the
    # verification step, and they are the bulk of what --check-doc prints.
    # Every other call a run makes reads one bit off it. --quiet keeps that
    # bit and withholds the rest -- by count, since a mode that hides a
    # line without saying so is worse than the reading it saves.
    p.add_argument('--quiet', action='store_true',
                   help='the default now; kept so older recipes still run')
    # Quiet is the default because the procedure says only ONE call in a
    # whole run wants the worklists -- post-run step 6e, where they are read
    # and adjudicated -- and every other call is a gate whose verdict is its
    # exit code. The default was the wrong way round and Run 16 ran the loud
    # form out of habit more than once.
    p.add_argument('--worklists', action='store_true',
                   help='with --check-doc: print the superseded-figure,'
                        ' superlative and absolute-time worklists for'
                        ' adjudication -- post-run 6e wants this, no other'
                        ' does')
    p.add_argument('--para', metavar='PATTERN',
                   help="print the paragraph, in either document, whose"
                        " bolded lead matches, with the line it starts at;"
                        " where several"
                        " match, print their leads and locations instead;"
                        " PATTERN#N prints item (N) of the matching"
                        " paragraph alone; needs no run file")
    p.add_argument('--para-at', metavar='FILE:LINE',
                   help='resolve a line number in either document to the'
                        ' paragraph holding it and print that paragraph\'s'
                        ' bolded lead as a --para handle -- what to carry'
                        ' forward from a grep, a line number surviving'
                        ' neither a rewrap nor an install; needs no run file')
    p.add_argument('--all', dest='all_paras', action='store_true',
                   help='with --para: print every matching paragraph whole'
                        ' rather than indexing them, for the reading that'
                        ' wants the set and not one of it')
    p.add_argument('--replace', metavar='ANCHOR',
                   help='replace the paragraph, in either document, carrying'
                        ' ANCHOR with the text in --with, without printing the'
                        ' old one;'
                        ' refuses unless ANCHOR occurs exactly once')
    p.add_argument('--cross-classes', action='store_true',
                   help="the class section's intro figures, aggregated from"
                        ' the same per-class cross-half readings the blocks'
                        ' print; wants --classes for the basis half and'
                        ' --others for the control')
    p.add_argument('--others', nargs='+', default=[], metavar='JSON',
                   help='the control half of each --classes file, in order')
    p.add_argument('--carried', action='store_true',
                   help='every figure the registration quotes from an'
                        ' earlier run, against that run: --others gives'
                        ' its JSONs, one per population the items are'
                        ' read on')
    p.add_argument('--carry-over', action='store_true',
                   help="this run's registration against the previous"
                        " run's as it stood BEFORE that run, item by item,"
                        ' read out of git rather than from its run file,'
                        ' whose copy carries a verdict per item')
    p.add_argument('--move-registration', action='store_true',
                   help="move this run's OPEN registration from README's"
                        " open list into the run file's last section,"
                        ' leaving the ANSWERED stub; post-run step 5')
    p.add_argument('--note', metavar='PREV-pair.txt',
                   help="a previous pair note read as the NEXT preparation"
                        ' owes it: the handover withheld and its size said')
    p.add_argument('--note-check', dest='note_check', metavar='$R-pair.txt',
                   help="THIS run's note, read mechanically: a range ending"
                        ' at the run before the previous one, an item number'
                        ' above what the registration carries, and a half'
                        ' tag missing from the roll -- the three carried-block'
                        ' errors a machine can have. preflight runs it as 10e')
    p.add_argument('--draft', metavar='RUN',
                   help="with --note: print the whole next note for RUN,"
                        ' each [SAME] block from the template and each'
                        " [PAIR'S] block as a model under a <yours> line;"
                        ' wants --halves')
    p.add_argument('--halves', metavar='BASIS,OTHER',
                   help="with --note --draft: the new pair's two names")
    p.add_argument('--checklist', metavar='pre|run|post[-a|-b]|readings',
                   help="print one of the run chapter's three checklists"
                        ' alone, which is what a session executes, or the'
                        ' readings list the steps name by item; the prose'
                        ' around them is the reasons')
    p.add_argument('--doc', nargs='?', const='', metavar='PART',
                   help="print one part of this script's own docstring --"
                        ' `modes` is the Modes list with the two gates in'
                        " it, which the pre-run list's step 7 asks for;"
                        ' alone it lists the parts and their sizes')
    p.add_argument('--section', metavar='NAME',
                   help="print one section's prose by heading name, without"
                        ' its tables, so the reading a run owes can be taken'
                        ' as enumerated rather than whole')
    p.add_argument('--with-tables', dest='with_tables', nargs='?', type=int,
                   const=0, default=None, metavar='N',
                   help='--section prints the tables too, or with N only the'
                        ' Nth of them; the reading list names ONE table and'
                        ' this is how it is taken')
    p.add_argument('--delete', metavar='ANCHOR',
                   help='delete the paragraph carrying ANCHOR, refusing a'
                        ' list or anything past --delete-limit; the deletion'
                        ' counterpart of --replace, so that removing a'
                        ' paragraph never means slicing a byte range')
    p.add_argument('--delete-limit', type=int, default=1500, metavar='N',
                   help='the size bar --delete refuses past (default 1500)')
    p.add_argument('--with', dest='with_', metavar='FILE',
                   help='the replacement text for --replace')
    p.add_argument('--readme', default=None,
                   help='README.md to check bench names against'
                        ' (default: alongside). It is NOT what --in-place'
                        ' writes: a run publishes into its own file, which'
                        ' is --run-doc')
    p.add_argument('--run-doc', dest='run_doc', metavar='FILE',
                   help="the run's own file, `runs/run<N>.md`, which carries"
                        ' the Results table, the fingerprint tables'
                        ' and the class blocks --'
                        ' everything a run replaces. Every --in-place'
                        ' install writes it and no other document'
                        ' (default: the newest in runs/)')
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
    p.add_argument('--pin', metavar='OTHER.json',
                   help="restrict this run's aggregates to the shapes OTHER"
                        ' also has, which is what a cross-run figure owes')
    args = p.parse_args()
    # RESOLVED ONCE, HERE, so that every mode below reads the same run and a
    # session cannot install one run's tables while reading another's
    # figures back. The default is the newest file in runs/ rather than a
    # literal, so the write-up that adds `runs/run20.md` re-aims every mode
    # by creating it.
    # A COPY POINTED AT BY `--readme` DOES NOT AIM AN INSTALL, and saying
    # so is the difference between a refusal and a table written over the
    # real run's. Every install used to take `--readme`, so a caller aiming
    # one at a copy -- which is how this script's own corpus drives them --
    # aimed the whole call; now it aims half of it, and the other half
    # would silently find the newest file in runs/. Measured on 2026-08-25,
    # when the corpus wrote eleven tables into the live run file that way.
    if (args.in_place and args.readme is not None and args.run_doc is None
            and (args.markdown or args.fingerprint or args.block)):
        p.error('--in-place writes the run\'s own file, not --readme:'
                ' name it with --run-doc, or drop --readme')
    if args.readme is None:
        args.readme = os.path.join(here, 'README.md')
    run_doc_named = args.run_doc is not None
    if args.run_doc is None:
        args.run_doc = current_run_doc(here)
        # AND THE DEFAULT IS HELD TO THE RUN NAMED. The newest file in
        # runs/ is right for the run being written up and wrong for every
        # other, and the refusal above fires for --readme alone: a bare
        # `--in-place` on `run19-g912-rev.json` with run22.md newest wrote
        # run19's block into run22.md at exit 0. install-tables.sh names
        # its document and never met this. 2026-09-01, by review.
        if args.in_place and args.run_doc:
            named = {int(m.group(1))
                     for f in [args.run] + (args.classes or []) if f
                     for m in [re.match(r'run(\d+)-', os.path.basename(f))]
                     if m}
            now = run_no_of(args.run_doc)
            if named and now is not None and named != {now}:
                p.error('--in-place would write %s, the newest in runs/,'
                        ' for a run named run%s: name the document with'
                        ' --run-doc'
                        % (os.path.basename(args.run_doc),
                           '/'.join(str(n) for n in sorted(named))))

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
                              or args.block or args.predictions):
        p.error('--in-place is a modifier of --markdown, --fingerprint,'
                ' --block or --predictions and does nothing alone')
    def asked(v):
        """Was this flag given? False and 0 are given; None is not."""
        return v is not None and v is not False
    # `--counts` is NOT in this table since 2026-09-05: it has two
    # arities and one owner apiece -- two sweep files modify `--compare`,
    # one modifies `--pair` -- so a single `needs` here would refuse the
    # arity it does not name. Its own pair of refusals is at the dispatch,
    # written to say which arity was given and what that one wants, which
    # is more than this loop can say.
    for flag, needs in (('alloc', 'compare'), ('cell', 'compare'),
                        ('chapter', 'compare'),
                        ('movers', 'compare'),
                        ('predictions', 'compare'), ('quiet', 'check_doc')):
        # `is not None` and NOT truthiness: --movers takes a NUMBER, and
        # `--movers 0` is falsy, so a truth test let one value of one flag
        # through both this guard and the dispatcher -- printing the
        # default table at exit 0, which is the silence this loop exists
        # to refuse. Found by an independent checker reading the code,
        # 2026-08-25, on a mode added beside the case written for exactly
        # this family.
        if (flag == 'movers' and asked(args.half_movers)):
            continue            # its second owner since 2026-09-16: the bar
        if asked(getattr(args, flag)) and not asked(getattr(args, needs)):
            p.error('--%s is a modifier of --%s and does nothing alone'
                    % (flag, needs.replace('_', '-')))
    # `--classes` has two owners since --extremes, and had none of this
    # before: given to any other mode it was read by nobody and the mode
    # printed as though the files had not been named. --extremes is the
    # one that cannot proceed without it, so it is refused rather than
    # dropped.
    if args.classes and not (args.fingerprint or args.extremes
                             or args.cross_classes or args.predictions):
        p.error('--classes is a modifier of --fingerprint, --extremes,'
                ' --cross-classes and --predictions and does nothing alone')
    if args.cross_classes and not (args.classes and args.others):
        p.error('--cross-classes wants --classes for the basis half and'
                ' --others for the control, in the same order')
    if args.others and not (args.cross_classes or args.carried):
        p.error('--others is a modifier of --cross-classes and --carried'
                ' and does nothing alone')
    if args.carried and not args.others:
        p.error('--carried reads the registration against an EARLIER run,'
                ' whose JSONs are --others; with none there is nothing to'
                ' derive and every quoted figure would read as unmatched')
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
                             or args.wild or args.carried):
        p.error('--verbose restores what --aa, --block and --compare drop'
                ' and does nothing alone -- under --wild it adds the'
                ' per-sample dump the per-bench table sums, and under'
                ' --carried the derivations its shortlist caps')
    # One mode an invocation. The dispatch below is an if/elif chain, so a
    # second mode was not refused but DROPPED: `--markdown --fingerprint
    # --in-place` installed the Results table, wrote neither fingerprint
    # table and said nothing about it. Both found 2026-08-17 by review.
    # `inherited` and `modes` joined the roll call 2026-09-08, an hour
    # after they were written: a mode added outside this list is exactly
    # the silent drop the list exists to refuse, and `--inherited --lint`
    # printed the report and said nothing of the lint it never ran. Six
    # more joined 2026-09-18, by review, having sat in the same chain
    # outside it since they were written: `--stale --lint` printed the
    # stale report at exit 0 and ran no lint.
    modes = [f for f in ('shapes', 'aa', 'pair', 'compare',
                         'machine', 'steps', 'cells', 'markdown',
                         'fingerprint', 'block', 'selftest', 'lint',
                         'check_doc', 'para', 'wild', 'deflation',
                         'extremes', 'inherited', 'modes', 'stale',
                         'brief_update', 'prose_facts', 'series',
                         'cell_movers', 'movement', 'winsor')
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
    subs = [f for f in ('chapter', 'alloc', 'ci', 'bridge', 'counts',
                        'movers', 'predictions') if asked(getattr(args, f))]
    # --predictions READS --counts for its `counts` spans rather than
    # clashing with it, so that pair is one reading. It was in none of the
    # three roll calls until 2026-09-04: alone it was absorbed, and beside
    # --alloc it dropped the allocation reading without a word. Cases:
    # `predictions-alone-is-refused`,
    # `predictions-and-alloc-are-two-readings`.
    if sorted(subs) == ['counts', 'predictions']:
        subs = ['predictions']
    if len(subs) > 1:
        p.error('%s are %d readings of --compare, not one: run the'
                ' invocations README\'s checklist spells out, one at a'
                ' time' % (' and '.join('--' + f for f in subs), len(subs)))
    if args.counts and not (args.compare or args.pair):
        p.error('--counts is a modifier: ONE sweep file with `--pair A B`'
                ' for the within-half reading, TWO with `--compare` for the'
                ' cross-half one, and it does nothing alone')
    if args.counts and args.compare and len(args.counts) != 2:
        p.error('--counts with --compare is the cross-half reading and takes'
                ' TWO sweep files, this run\'s and the other half\'s, not %d'
                % len(args.counts))
    if args.ci and not args.compare:
        p.error('--ci is a reading ACROSS two runs: give it --compare')
    # A CROSS-RUN READING GIVEN NO EARLIER RUN takes the note's COMPARE
    # run: --bridge the same half of it by role, --movement its run file.
    # Named explicitly, --compare and --run-doc win.
    if args.bridge and not args.compare and args.run:
        at = json_run_half(args.run)
        cmp_run = note_compare(at[0]) if at else None
        if cmp_run:
            mine, theirs = note_halves(at[0]), note_halves(cmp_run)
            if not mine or at[1] not in mine or not theirs:
                p.error('--bridge: %s names COMPARE %s, and the halves of'
                        ' %s are not both readable off the two notes'
                        % (at[0] + '-pair.txt', os.path.basename(cmp_run),
                           os.path.basename(args.run)))
            args.compare = '%s-%s-%s.json' % (
                cmp_run, theirs[mine.index(at[1])], at[2])
            sys.stderr.write('--bridge: against %s, the same half of the'
                             " note's COMPARE run\n"
                             % os.path.basename(args.compare))
    if args.bridge and not args.compare:
        p.error('--bridge is a reading ACROSS two runs: give it --compare,'
                " or a COMPARE line to the run's note")

    # BOTH DOCUMENTS, in reading order. `--para` and `--replace` are
    # retrieval, and a session that had to say which file a paragraph is in
    # before asking for it would be doing the search this mode exists to
    # replace -- so they take the pair and the answer says which file it
    # came from. `--replace` refuses an anchor that occurs in both.
    docs = [args.readme] + ([args.run_doc] if args.run_doc else [])
    if args.replace:
        if not args.with_:
            sys.exit('--replace wants --with FILE, the replacement text')
        sys.exit(splice(docs, args.replace, args.with_))
    if args.cross_classes:
        sys.exit(cross_class_summary(args.classes, args.others, args.main))
    if args.section:
        sys.exit(section(docs, args.section, args.with_tables))
    if args.doc is not None:
        sys.exit(doc_part(args.doc))
    # Absorbed without effect is the silent-option family this tree
    # counts, and these two flags mean nothing on their own: --draft
    # without --note fell through to "a run file is required", naming the
    # wrong thing, and --halves without --draft was taken and ignored.
    if (args.draft or args.halves) and not args.note:
        sys.exit('--draft and --halves are --note\'s; there is nothing to'
                 ' carry over without a note to carry it from')
    if args.halves and not args.draft:
        sys.exit('--halves is --draft\'s: without it the note is READ and'
                 ' not carried over, so the new names have nowhere to go')
    if (args.imperative or args.full) and not args.checklist:
        # p.error, so the status is 2: this is usage, which the tree reads
        # as `the run did not happen`. The two refusals above exit 1
        # through sys.exit, which predates that convention.
        p.error('--%s is --checklist\'s: it chooses how much of each step'
                ' prints, and there are no steps without a list to'
                ' print. Taken alone it was read and ignored'
                % ('imperative' if args.imperative else 'full'))
    if args.imperative and args.full:
        p.error('--imperative is the default form and --full the other;'
                ' pass one')
    if args.note_check:
        sys.exit(note_check(args.note_check, args.readme, args.run_doc))
    if args.note:
        sys.exit(pair_note(args.note, args.draft, args.halves))
    if args.checklist:
        sys.exit(checklist(args.readme, args.checklist, not args.full))
    if args.record is not None:
        sys.exit(record(args.record))
    if args.carried:
        sys.exit(carried_figures(args.run or '', want_run_doc(args),
                                 args.readme, args.others, args.main,
                                 args.verbose))
    if args.carry_over:
        sys.exit(carry_over(args.run or '', want_run_doc(args), args.readme))
    if args.move_registration:
        sys.exit(move_registration(args.readme, want_run_doc(args)))
    if args.delete:
        sys.exit(excise(docs, args.delete, args.delete_limit))
    if args.para_at:
        sys.exit(paragraph_at(docs, args.para_at))
    if args.para:
        sys.exit(paragraphs(docs, args.para, args.all_paras))
    if args.modes:
        sys.exit(modes_table())
    if args.inherited:
        doc = want_run_doc(args)
        sys.exit(inherited(doc, previous_run_doc(doc), args.all_paras))
    if args.lost:
        sys.exit(lost_paragraphs(want_run_doc(args)))
    if args.stale:
        sys.exit(stale_figures(want_run_doc(args), verbose=args.all_paras))
    if args.brief_update:
        sys.exit(brief_update(args.brief_update,
                              where=args.brief_dir))
    if args.prose_facts:
        sys.exit(prose_facts(args.prose_facts))
    if args.check_doc:
        prev = previous_run_doc(args.run_doc)
        sys.exit(check_doc_loud(args.readme, args.main, args.run_doc, prev)
                 if args.worklists
                 else check_doc_quiet(args.readme, args.main, args.run_doc,
                                      prev))
    if args.lint:
        sys.exit(lint(args.main, args.readme, args.run_doc,
                      quiet=not args.worklists))
    if args.counts_totals:
        sys.exit(counts_totals(args.counts_totals, args))
    if args.series:
        if len(args.series) not in (3, 4):
            p.error('--series takes A B SHAPE and an optional DIR')
        sys.exit(series_table(*args.series[:3], args=args,
                              where=(args.series[3:] or ['.'])[0]))
    if args.floor_pairs:
        sys.exit(floor_pairs(args.floor_pairs, args))
    if args.half_movers:
        if len(args.half_movers) > 2:
            p.error('--half-movers takes RUN and at most one PREV')
        run = args.half_movers[0]
        prev = args.half_movers[1] if args.half_movers[1:] else None
        if prev is None:
            prev = note_compare(run)
            if prev is None:
                sys.stderr.write('--half-movers %s: no PREV given and no'
                                 ' COMPARE line in %s-pair.txt, so there is'
                                 ' no earlier run to read against -- name'
                                 ' one, or add the line\n' % (run, run))
                sys.exit(2)
        sys.exit(half_movers(run, prev, args))
    if args.cell_movers:
        if len(args.cell_movers) > 2:
            p.error('--cell-movers takes RUN and at most one N')
        top = int(args.cell_movers[1]) if args.cell_movers[1:] else 20
        sys.exit(cell_movers(args.cell_movers[0], top, args))
    if args.movement:
        at = json_run_half(args.run or '')
        cmp_run = (note_compare(at[0])
                   if at and not run_doc_named else None)
        if cmp_run:
            args.run_doc = os.path.join(os.path.dirname(cmp_run) or '.',
                                        RUNS_DIR,
                                        os.path.basename(cmp_run) + '.md')
            if not os.path.exists(args.run_doc):
                sys.stderr.write("--movement: the note's COMPARE run has no"
                                 ' file at %s\n' % args.run_doc)
                sys.exit(2)
        sys.exit(movement(args.run, args))
    if args.counts_cost:
        sys.exit(counts_cost(args.counts_cost))
    if args.repoint:
        sys.exit(repoint(args.repoint, args.readme, args.run_doc))
    if args.over_list:
        sys.exit(over_list_sweep(args.over_list, args))
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
    # --pin BEFORE --exclude-shape, and both before anything reads a
    # figure: pinning is a restriction like the other and the two compose,
    # so `--pin` the population and `--exclude-shape` a shape inside it is
    # the reading a run takes of a predecessor whose extra shapes are gone
    # AND one of whose kept shapes is degenerate.
    #
    # WHY IT IS A MODE. A cross-run figure is read over the shapes the two
    # runs share -- the chapter's `match bases before reading any ratio` --
    # and until 2026-09-05 that was `--exclude-shape` once per shape, typed
    # out. Run 24's write-up improvised it with two flags and recorded the
    # improvisation as a task; Run 25 improvised it with EIGHT, and every
    # cross-run figure it published needed them: the predecessor's whole
    # column, its allocation levels, its correction
    # terms. Two runs is the bar this file uses for making something a
    # mode, and a hand-typed list is a place to drop a shape silently.
    if args.pin:
        try:
            keep = set(load(args.pin, args.main)[1])
        except (OSError, ValueError, KeyError) as e:
            sys.stderr.write('--pin: %s: %s\n'
                             % (os.path.basename(args.pin), e))
            sys.exit(2)
        dropped = [s for s in shapes if s not in keep]
        shapes = [s for s in shapes if s in keep]
        if not shapes:
            sys.stderr.write('--pin: %s and %s share no shape, so there is'
                             ' nothing to read\n'
                             % (os.path.basename(args.run),
                                os.path.basename(args.pin)))
            sys.exit(2)
        # SAID OUT LOUD, on stderr with the rest of the warnings: a pinned
        # figure is a figure over a population the file's own head does not
        # name, and a reader who cannot see which shapes went cannot check
        # it. Silence here would make the mode worse than the flags it
        # replaces, those at least being visible in the command.
        sys.stderr.write('pinned to the %d shape(s) %s also has%s\n'
                         % (len(shapes), os.path.basename(args.pin),
                            (', dropping ' + ', '.join(sorted(dropped)))
                            if dropped else ' -- it drops none'))
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
    # THE BANNER GOES TO STDERR UNDER --cells AND NOWHERE ELSE. Every mode
    # says its population in its first line, which is this file's rule and
    # stays -- but `--cells` is the TSV the post-run list sends a caller to
    # precisely so a figure is not read by counting fields off a human
    # table, and a banner and a blank line above the header defeat that:
    # Run 29's write-up parsed this output twice with the header at the
    # wrong offset, once taking line 1 for it and once line 2. On stderr
    # the population is still said, and stdout is a header and its rows.
    say = (lambda t='': print(t, file=sys.stderr)) if args.cells else print
    say('%s: criterion %s, %d reports = %s%s%s'
        % (os.path.basename(args.run), meta['version'], meta['reports'],
           roster,
           '  (RAGGED: some cells missing)' if meta['ragged'] else '',
           '' if len(shapes) > 1 else '  (one shape: nothing to spread)'))
    if args.corr != 'sumonly':
        say('corrected by the IN-SITU term (--corr=insitu), not `sum-only`')
    say()
    health(cells, shapes, strategies, terms, args.corr)
    if args.shapes:
        shape_table(cells, shapes, strategies, meta)
    elif args.aa:
        aa_table(cells, shapes, strategies, terms, meta, not args.verbose)
    elif args.pair and args.counts:
        # BEFORE the time reading, because `--pair` names the two arms for
        # both instruments and the sweep file is what says which was asked
        # for. One file is the within-half count reading; two is the
        # cross-half one and belongs to `--compare`, which is refused here
        # rather than silently read as this.
        if len(args.counts) != 1:
            sys.stderr.write('--counts with `--pair` is the WITHIN-HALF'
                             ' reading and takes ONE sweep file, not %d;'
                             ' two files are the cross-half reading and want'
                             ' `--compare OTHER.json`\n' % len(args.counts))
            sys.exit(2)
        sys.exit(counts_pair(args.counts[0], args.pair, shapes, cells,
                             per_shape=args.per_shape))
    elif args.pair:
        pair_table(cells, shapes, strategies, args.pair,
                   per_shape=args.per_shape)
    elif args.compare and args.block:
        # --block owns the pair here: --compare is its second file and not
        # a mode of its own, so it has to be tested before the plain
        # --compare arm below claims it.
        # FLATTENED AS THE PLAIN ARM'S IS, and this is the arm that
        # matters: install-tables.sh installs Controls, Provenance and the
        # per-shape line one line each, and the other two paragraphs of
        # the form -- `Across the halves` and `What the class says` --
        # exist only WITH the second JSON and are the session's to place.
        # They came out wrapped, so Run 36 joined them in a script and
        # `lib-stage2-lean-u1` reached the page as `lib- stage2-lean-u1`,
        # in a `What the class says` paragraph. Printing is all that
        # changes: this arm honours no --in-place and did not before.
        text = capture(block_skeleton, cells, shapes, strategies, meta,
                       args, terms)
        for para in flatten_paragraphs(text, only_bolded=True):
            sys.stdout.write(para + '\n\n')
    elif args.compare and args.chapter:
        chapter_skeleton(cells, shapes, strategies, meta,
                         args.compare, args.main)
    elif args.compare and args.movers is not None:
        sys.exit(movers_table(cells, shapes, strategies, meta, args.compare,
                              args.main, args.movers, not args.verbose))
    elif args.compare and args.predictions and args.in_place:
        sys.exit(predictions_in_place(args))
    elif args.compare and args.predictions:
        rd = args.run_doc
        if not rd:
            mm = re.match(r'run\d+', os.path.basename(args.run))
            cand = mm and os.path.join(RUNS_DIR, mm.group(0) + '.md')
            if cand and os.path.exists(cand):
                rd = cand
        sys.exit(predictions_table(cells, shapes, strategies, meta,
                                   args.compare, args.main, args.run, rd,
                                   args.readme, args.counts, args.classes))
    elif args.compare and args.counts and not args.block:
        # Before the plain --compare arm below, as every other second-file
        # mode is: --counts is a reading OF a comparison and not a mode
        # beside one, both its columns being this run over the other.
        sys.exit(counts_table(cells, shapes, strategies, meta, args.compare,
                              args.main, args.counts[0], args.counts[1],
                              not args.verbose,
                              per_shape=args.per_shape))
    elif args.compare and args.cell:
        sys.exit(compare_cell(cells, shapes, meta, args.run, args.compare,
                              args.main, args.cell))
    elif args.compare and args.alloc:
        compare_alloc(cells, shapes, strategies, meta, args.compare,
                      args.main, args.per_shape)
    elif args.compare and args.ci:
        sys.exit(compare_ci(cells, shapes, strategies, meta, args.compare,
                            args.main))
    elif args.compare and args.bridge:
        sys.exit(bridge_table(cells, shapes, strategies, meta, args.compare,
                              args.main, args.band))
    elif args.compare:
        compare_table(cells, shapes, strategies, meta, args.compare,
                      args.main, not args.verbose,
                      per_shape=args.per_shape)
    elif args.winsor:
        sys.exit(winsor_table(cells, shapes, strategies))
    elif args.deflation:
        sys.exit(deflation_table(args.run, cells, shapes, args.main))
    elif args.machine:
        sys.exit(machine_check(cells, shapes, want_run_doc(args),
                               run=args.run))
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
