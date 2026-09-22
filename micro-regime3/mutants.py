"""The mutants of this directory: each check broken on purpose, and caught.

Read by `selftest-mutants.py .`, which copies the tracked files to a temp
directory, applies each mutant there and requires its judge to FAIL on it;
a mutant whose anchor has moved is LOST, not caught. These are the
non-vacuity proofs that used to be dated sentences in docstrings -- "all
three broken deliberately, 2026-08-17" -- which expire the moment the code
under them moves, with nothing to say so. The judges read the runs on disk
through `CORPUS`, since the copy holds tracked files alone; with no run on
disk a judge's baseline is red and its mutants are LOST, which is the honest
reading of a check that needs a run.
"""

COPY = 'tracked'
# The properties over every run on disk are minutes a sweep and the judges
# below sweep three times; a property is shown to fail on a run or two.
ENV = {'CORPUS': '{root}', 'CORPUS_LIMIT': '2'}
TIMEOUT = 900

# The reader's selftest is asked of the first run on disk; the properties
# and the corpus module run from the copy, over the runs on disk.
READER = ('f=$(ls "{root}"/*.json 2>/dev/null | head -1); test -n "$f" '
          '&& python3 "{file}" "$f" --selftest')
PROPS = 'python3 "{dir}/properties.py"'

# TWO JUDGES BELOW FAILED OPEN UNTIL 2026-09-18 and now exit 2 instead:
# the emphasis and rate columns' both glob a `g912` half, which no run
# after 28 carries, and both answered `sys.exit(0)` when the glob came
# back empty -- a PASS for a judge that did not run. Deleting Runs 24 to
# 30's artifacts that day emptied it and the two mutants read MISSED,
# which at least says something; a judge that had also been mutated into
# passing would have read `ok`. Exit 2 is this toolset's `the run did not
# happen`, and selftest-mutants.py reports it as LOST, which is the
# honest answer. The rate judge's THIRD guard, `if not t`, is left at 0
# deliberately: it fires when the reader's --pair output does not match,
# which a mutation can cause, so raising it would report the mutant
# caught by the regex rather than by the defect. The same goes for the two judges that name run27 and
# run29 outright: they are LOST with those runs' artifacts and the suite
# says so rather than quietly proving less.
MUTANTS = [
    # THE PALINDROME READ AS TWO PAIRS AND NOT AS FOUR LEGS: the driver
    # emits each half over its own two legs beside the two cross-half
    # passes, because a spread between the passes is the pair disagreeing
    # or one half moving against itself, and the pairs alone cannot tell
    # those apart. Run 36 needed it and ran it by hand inside the window
    # where nothing else may run. The judge builds the same shadow the
    # case does, out of the MUTATED text, and greps the driver's own OUT
    # file: defect-run.py cannot be the judge here. What was MEASURED is
    # that it exits 2 in the copy and the mutant reads LOST, which is
    # this toolset's `the run did not happen`; the siblings below lay
    # that on the copy being in no git repository and this judge did not
    # test the cause, so it says what it saw (2026-09-19).
    ('the gate reads the pair and not each half against itself',
     'run-evening.sh',
     '    ./read-run.py "$R-gate-$OTHER-a.json" --compare'
     ' "$R-gate-$OTHER-b.json"',
     '    :',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess,'
     ' sys, tempfile\n'
     'spec = importlib.util.spec_from_file_location(\'d\','
     ' \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     't = tempfile.mkdtemp()\n'
     'at = m.shadow_dir(t, \'run-evening.sh\', open(\'{file}\').read(),'
     ' extra=m.evening_fixture(\'zzmu\', md5=False))\n'
     'e = dict(os.environ, MAXBUSY=\'100\', FAKE_SATURATE=\'1\','
     ' ONLY=m.main_shapes()[0])\n'
     'subprocess.run([os.path.join(at, \'run-evening.sh\'), \'zzmu\'],'
     ' cwd=at, env=e, capture_output=True, text=True)\n'
     'p = os.path.join(at, \'zzmu-evening-out.txt\')\n'
     'out = open(p).read() if os.path.exists(p) else \'\'\n'
     'sys.exit(0 if out.count(\'per arm, over\') >= 4 else 1)"'),
    # THE CLASS BLOCK'S PROSE EMITTED WRAPPED, which is the form Run 36 had
    # to join by hand and the join is what broke an arm name in half. The
    # mutant puts the line-at-a-time write back; the judge plants a synthetic
    # class beside a copy of the newest run file and fails when a span of the
    # Provenance boilerplate too long to survive an eighty-column wrap is not
    # contiguous.
    ('a class block\'s prose is emitted wrapped for a caller to join',
     'read-run.py',
     "            para = ' '.join(para.split())",
     "            para = para + ''",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile,'
     ' subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\','
     ' \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     't = tempfile.mkdtemp()\n'
     'run = m.synth_json(t, \'rev\', name=\'a.json\')\n'
     'doc = m.write_rundoc(t, open(m.RUNDOC).read())\n'
     'r = subprocess.run([sys.executable, \'{file}\', run, \'--block\','
     ' \'--brief\', \'--in-place\', \'--run-doc\', doc],'
     ' capture_output=True, text=True)\n'
     'want = \'MiB max residency (copy from the process\'\n'
     'sys.exit(0 if want in r.stdout else 1)"'),
    # THE PER-ARM ALLOCATION READING, BLINDED THE WAY RUN 36 BLINDED IT BY
    # HAND: that run needed the size of an allocation move per arm, had no
    # mode for it, computed it in a script, and the script's print took an
    # ABSOLUTE deviation -- so `2 - ratio` reached the page and one arm's
    # direction was published backwards in three places. The mutant is that
    # arithmetic, `1 + |g-1|`, put where the geomean belongs; a pair whose
    # flagged half allocates 0.8 of the other then reads 1.2000, which is
    # the same number of points the wrong way round. The judge plants the
    # skewed pair through defects.py's own builder and runs the MUTATED
    # copy on it, rather than going through defect-run.py, which would run
    # the tree's reader.
    ('the per-arm allocation ratio reads its own distance from 1',
     'read-run.py',
     '                g = math.exp(sum(math.log(r) for r, _ in rs) / len(rs))',
     '                g = 1.0 + abs(math.exp(sum(math.log(r) for r, _ in rs)'
     ' / len(rs)) - 1.0)',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile,'
     ' subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\','
     ' \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'out = m.plant_alloc_skewed_pair(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', out[\'run\'],'
     ' \'--compare\', out[\'other\'], \'--alloc\', \'--per-shape\'],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'0.8000\' in r.stdout + r.stderr else 1)"'),
    # THE BAR NAMES THE ARMS THAT CLEAR IT, or it is a number a reader has
    # to apply by hand -- which is what a session did on Run 32, whose head
    # claimed the compiler worth nothing this roster can measure while
    # three of eight strategies cleared its own A/A bar. The mutant leaves
    # the bar printed and empties the list.
    ('the A/A bar names no arm that clears it',
     'read-run.py',
     '    past = sorted(t for d, t in arms if d > bar)',
     '    past = []',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\na = d.synth_json(t, \'main\', name=\'a.json\')\nb = d.synth_json(t, \'main\', name=\'b.json\', skew=[(d.main_shapes()[0], \'lib-stage1\', 4)])\nr = subprocess.run([sys.executable, \'{file}\', a, \'--compare\', b], capture_output=True, text=True)\nsys.exit(0 if \'move further than the bar: \' in r.stdout and \'lib-stage1\' in r.stdout else 1)"'),

    # THE DRIFT LINE FIRES ON A ROW WHOSE TWO PUBLISHED FIGURES DIVIDE TO
    # SOMETHING THE ARM DID NOT DO. Raising the threshold past any real gap
    # is the same as not having written it, which is the state Runs 31 and
    # 32 were both published in.
    ('the published-column drift threshold catches nothing',
     'read-run.py',
     '        if abs(t_a / t_b - g) > 0.02:',
     '        if abs(t_a / t_b - g) > 99:',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\na = d.synth_json(t, \'main\', name=\'a.json\')\nb = d.synth_json(t, \'main\', name=\'b.json\', skew=[(d.main_shapes()[0], \'lib-stage1\', 40), (d.main_shapes()[1], \'lib-stage1\', 30)])\nr = subprocess.run([sys.executable, \'{file}\', a, \'--compare\', b], capture_output=True, text=True)\nsys.exit(0 if \'published-column drift\' in r.stdout else 1)"'),

    # AND --winsor ACTUALLY WINSORIZES. With the cap removed the two
    # columns are one column and every gap reads 0.0%, which is a mode
    # answering the question it was written to ask with `nothing`.
    ('--winsor publishes the plain geomean as the published one',
     'read-run.py',
     '        capped, n_capped = winsorize(logs)',
     '        capped, n_capped = logs, 0',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\na = d.synth_json(t, \'main\', name=\'a.json\', skew=[(d.main_shapes()[0], \'lib-stage1\', 40), (d.main_shapes()[1], \'lib-stage1\', 30)])\nr = subprocess.run([sys.executable, \'{file}\', a, \'--winsor\'], capture_output=True, text=True)\nrows = [l for l in r.stdout.splitlines() if l.startswith(\'lib-stage1 \')]\nsys.exit(0 if rows and \'0.0%\' not in rows[0] else 1)"'),

    # AND --inherited READS THE CHANGED PARAGRAPHS AS WELL AS THE CARRIED
    # ONES. The carried half catches what a diff cannot see; this half
    # catches what a diff SHOWS and a reader skims past, a lead rewritten
    # over a body left alone. Dropping the membership test empties it, so
    # a half-updated paragraph reads as fully updated -- the state Run
    # 33's floor paragraph was in when a checker pass read its diff and
    # passed it. The judge plants that shape and asks for the count.
    ('--inherited stops reading the changed paragraphs',
     'read-run.py',
     '                   if p not in before and pat.search(p)]',
     '                   if False and pat.search(p)]',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nf = d.inherited_pair(t, half=True)\nr = subprocess.run([sys.executable, \'{file}\', \'--inherited\', \'--all\', \'--run-doc\', f[\'doc\']], capture_output=True, text=True)\nsys.exit(0 if \'1 paragraph(s) this run CHANGED\' in r.stdout else 1)"'),

    # AND --stale READS THE FIGURES AN EDITED PARAGRAPH KEPT. --inherited
    # above catches the paragraph nobody touched; this catches the one
    # touched around a number that was not, which no checker pass sees
    # either -- an edited paragraph is IN the diff and its surviving
    # numeral reads as context. Run 35 shipped four of them past both
    # gates and a figure-checking agent: a floor pair, a row count, a
    # reference run and a consumer count. Emptying the membership test
    # leaves the mode printing nothing and reporting zero, which is what
    # a clean run looks like. The judge plants one and asks for the
    # count; the fixture's control, `kept=False`, is the same edit with
    # the figure moved and reports zero honestly.
    ('--stale stops reading the figures an edited paragraph kept',
     'read-run.py',
     "                if re.search(r'\\b%s\\b' % re.escape(n), best, re.I)]",
     '                if False]',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nf = d.stale_pair(t)\nr = subprocess.run([sys.executable, \'{file}\', \'--stale\', \'--run-doc\', f[\'doc\']], capture_output=True, text=True)\nsys.exit(0 if \'1 edited paragraph(s) keep a MEASURED\' in r.stdout else 1)"'),

    # AND --lint HOLDS THE REGISTRATION'S LEAD TO THE MOVER'S KEY.
    # `--move-registration` matches that lead whole and refuses anything
    # else, so a lead carrying one clause more is a refusal at post-run
    # step 5 with the hours already spent -- Run 33's was, a day after
    # both gates passed it. Making the test vacuous puts it back.
    ('--lint stops holding the registration lead to the mover', 'read-run.py',
     "            if not t.startswith(want):",
     "            if False:",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nr = subprocess.run([sys.executable, \'{file}\', \'--lint\', \'--readme\', d.readme_with_a_registration(t, lead_extra=\'declared by request\')], capture_output=True, text=True)\nsys.exit(0 if \'not the form --move-registration matches\' in r.stdout + r.stderr else 1)"'),

    # AND --floor-pairs NAMES THE PAIR THAT CARRIES THE FLOOR. The mode
    # prints and never judges -- the floor is the widest of the pairs it
    # lists -- so the carrier IS its answer, and a carrier read off the
    # first pair instead of the widest is a mode agreeing with itself and
    # with nothing else. The judge plants one population and asks that the
    # named carrier be the pair furthest from 1.
    ('--floor-pairs names a carrier that does not carry the floor',
     'read-run.py',
     '        carrier = aa_floor(pairs)\n        floor = abs(carrier.g - 1) * 100',
     '        carrier = pairs[0]\n        floor = abs(carrier.g - 1) * 100',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, re, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nd.synth_json(t, \'main\', name=\'run95-x-main.json\', skew=[(d.main_shapes()[0], \'mut-odo-vecdims-add-in-leaf-u2-aa-distant\', 12)])\nr = subprocess.run([sys.executable, \'{file}\', \'--floor-pairs\', os.path.join(t, \'run95\')], capture_output=True, text=True)\nrows = [l for l in r.stdout.splitlines() if re.search(r\' ([0-9.]+) pts\', l)]\nwidest = max(rows, key=lambda l: float(re.search(r\' ([0-9.]+) pts\', l).group(1)))\nsys.exit(0 if \'<- the floor\' in widest else 1)"'),

    # AND THE INTRUSION VERDICT NAMES THE SHAPES AND NOT THE BENCHES.
    # What stands in for post-run step 3's rerun drops the disturbed
    # SHAPES from both halves; a remedy naming the bench cannot be typed
    # into `--exclude-shape` at all. The mutant names the whole bench and
    # the judge asks for the shape.
    ('the intrusion remedy names the bench instead of the shape',
     'read-run.py',
     "            hurt = sorted({nm.split('/')[0] for nm, _, _ in loud})",
     "            hurt = sorted({nm for nm, _, _ in loud})",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\np = os.path.join(t, \'w.log\')\nopen(p, \'w\').write(d.WILD_LOUD_LOG)\nr = subprocess.run([sys.executable, \'{file}\', p, \'--wild\'], capture_output=True, text=True)\nsys.exit(0 if \'--exclude-shape shp\\n\' in r.stdout or \'--exclude-shape shp\' in r.stdout.replace(\'--exclude-shape shp/arm\', \'\') else 1)"'),

    # AND --movement READS THE TABLE IT IS ABOUT TO OVERWRITE, not the
    # one already installed. The whole of post-run 5a is that the old
    # figures are gone after 5b, so a movement read off the NEW table is
    # every row moving by nothing -- a reading that cannot fail and says
    # nothing, which is the state the step was in when no mode did it.
    ('--movement compares this run against itself', 'read-run.py',
     "    prev = readme_rows(doc, set(strategies), set(strategies))",
     "    prev = {}",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nj = d.synth_json(t, \'main\')\ndoc = d.rundoc_with_a_results_table(t)\nr = subprocess.run([sys.executable, \'{file}\', j, \'--movement\', \'--run-doc\', doc], capture_output=True, text=True)\nsys.exit(0 if \'lib-stage2-lean\' in r.stdout and \'row(s) moved\' in r.stdout else 1)"'),

    # AND --half-movers FLAGS AN ARM THAT MOVED ON ONE HALF ALONE. The
    # rule is the one reading that separates a file instance's term from
    # the pair's variable -- Run 33's basis carried 29.5% on one arm of
    # `runs` that the open list credited to a compiler for a day -- and
    # with it switched off the mode prints its floors and flags nothing,
    # which reads exactly like a run with no such term.
    ('--half-movers flags nothing', 'read-run.py',
     "            local = (moved[0] != moved[1]",
     "            local = (False",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nsk = [(sh, \'lib-stage1\', 1.3) for sh in d.class_shapes(\'runs\')]\nd.synth_json(t, \'runs\', name=\'r0-a-runs.json\')\nd.synth_json(t, \'runs\', name=\'r0-b-runs.json\')\nd.synth_json(t, \'runs\', name=\'r1-a-runs.json\', skew=sk)\nd.synth_json(t, \'runs\', name=\'r1-b-runs.json\')\nfor r in (\'r0\', \'r1\'):\n    open(os.path.join(t, r + \'-pair.txt\'), \'w\').write(\'HALVES: basis=a other=b\\n\')\nr = subprocess.run([sys.executable, \'{file}\', \'--half-movers\', os.path.join(t, \'r1\'), os.path.join(t, \'r0\')], capture_output=True, text=True)\nsys.exit(0 if \'1 half-local mover(s)\' in r.stdout and \'lib-stage1\' in r.stdout else 1)"'),

    # AND --cell-movers RANKS THE CELLS, or it is the per-shape table
    # again with the reader left to find the row -- which is the reading
    # Run 34's record did not take, its arm geomeans hiding a cell of
    # 1.25 in an arm near 1. The judge skews one cell of one arm
    # on the last shape of `runs` and wants it first; with the rank
    # switched off the first row is whatever came first.
    ('--cell-movers stops ranking', 'read-run.py',
     '    rows.sort(key=lambda r: -r[0])',
     '    rows.sort(key=lambda r: 0)',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nlast = d.class_shapes(\'runs\')[-1]\nd.synth_json(t, \'runs\', name=\'r1-a-runs.json\', skew=[(last, \'lib-stage1\', 1.3)])\nd.synth_json(t, \'runs\', name=\'r1-b-runs.json\')\nopen(os.path.join(t, \'r1-pair.txt\'), \'w\').write(\'HALVES: basis=a other=b\\n\')\nr = subprocess.run([sys.executable, \'{file}\', \'--cell-movers\', os.path.join(t, \'r1\'), \'3\'], capture_output=True, text=True)\nrows = [l for l in r.stdout.splitlines() if l.startswith(\'  runs \')]\nsys.exit(0 if rows and last in rows[0] and \'lib-stage1\' in rows[0] else 1)"'),

    # AND --note-check WANTS THE NOTE'S ENTRY POINT. Run list step 13
    # reads the [EXEC] blocks, and its `or the whole note` branch was
    # taken by both runs that met it -- eight hundred lines and 745.
    # Dropping the test puts the branch back with nothing saying so.
    ('--note-check stops wanting an [EXEC] block', 'read-run.py',
     "    if '[EXEC]' not in text:",
     '    if False:',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nn = d.note_for_the_check(t)\nrm = d.readme_with_a_registration(t)\nr = subprocess.run([sys.executable, \'{file}\', \'--note-check\', n, \'--readme\', rm], capture_output=True, text=True)\nsys.exit(0 if \'no [EXEC] block\' in r.stdout + r.stderr else 1)"'),

    # `CORPUS_RUN=newest` narrows `check-all`'s corpus to one run, so a
    # narrowing that keeps the wrong runs would put the suite back where it
    # was while reading as narrowed. The judge asks the selection directly
    # rather than through a sweep -- exactly one run number survives -- so
    # it costs no minutes; LOST rather than green with no run on disk, as
    # every corpus judge here is.
    # AND IT READS THE NUMBER AS properties.py DOES, anywhere in the name.
    # Anchored at the head it found nothing whenever the newest run is
    # represented by its smoke sweep alone -- `smoke-l1-run28-main.json`
    # and no `run28-*` yet -- which is the state of every preparation, and
    # the judge's own baseline went red there and took the mutant LOST
    # with it. The narrowing it judges says why in its own comment: a run's
    # sweeps and probes carry the number in the middle (2026-09-10).
    ('the newest-run narrowing keeps every run but the newest',
     'properties.py',
     "    return [f for f, x in zip(js, ns) if x is None or x == top]",
     "    return [f for f, x in zip(js, ns) if x is None or x != top]",
     'python3 -c "import os,re,sys,importlib.util; os.environ[\'CORPUS\']=\'{root}\'; os.environ[\'CORPUS_RUN\']=\'newest\'; spec=importlib.util.spec_from_file_location(\'p\',\'{file}\'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); ns=set(int(x.group(1)) for x in (re.search(r\'run(\\\\d+)[-.]\',os.path.basename(f)) for f in m.runs_on_disk()) if x); sys.exit(0 if len(ns)==1 else 1)"'),
    # The populations block's whole judgement is what item_populations
    # returns, so returning nothing is a mutant of the reader: every item
    # then reads `no population named; read by hand`. The judge plants the
    # fixture of predictions-name-the-main-set-an-item-reads-on itself,
    # through defects.py's own builders, and runs the mutated copy on it
    # -- defect-run.py would run the tree's reader and not the copy.
    ('the populations block names no population',
     'read-run.py',
     "    return [p for p in available if p in named]",
     "    return []",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\nspec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\nd = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(d)\nt = tempfile.mkdtemp()\nb = chr(96)\nrun = d.synth_json(t)\nother = d.synth_json(t, name=\'other.json\')\nruns = d.synth_json(t, pop=\'runs\', name=\'x-runs.json\')\ndoc = d.write(os.path.join(t, \'r.md\'), \'# Run 99\\n\\n## What this run was built to answer, and what it answered\\n\\n(1) *a* On \' + b + \'runs\' + b + \': \' + b + \'predict: cross list 1.0 within 1%\' + b + \'.\\n\')\nr = subprocess.run([sys.executable, \'{file}\', run, \'--compare\', other, \'--predictions\', \'--run-doc\', doc, \'--classes\', runs], capture_output=True, text=True)\nsys.exit(0 if \'(1) runs\' in r.stdout else 1)"'),
    # The per-view floor's whole judgement is one comparison, so inverting
    # it is a mutant of the tool. The judge reads every star's own
    # annotation back on the newest run on disk -- `ARM P% against F%`,
    # the view's spread against its class floor -- and wants P above F
    # on all of them and at least one star; inverted, the stars land on
    # the views UNDER the floor. It named Run 27's `flip-last-rows` until
    # 2026-09-18, when that run's artifacts were deleted and it read LOST.
    ('the per-view floor stars a view no wider than its class', 'view-floor.py',
     '                over = b in floor and sp > a.factor * floor[b]',
     '                over = b in floor and sp < a.factor * floor[b]',
     'R=$(ls {root}/run*-*-main.json | sed "s|.*/\\(run[0-9]*\\)-.*|\\1|" | sort -V | tail -1); python3 "{file}" $R -d "{root}" -c flip | python3 -c "import re, sys\np = re.findall(r\'([0-9.]+)% against ([0-9.]+)%\', sys.stdin.read())\nsys.exit(0 if p and all(float(a) > float(b) for a, b in p) else 1)"'),
    # The class paragraph wrapped narrow and at hyphens again, which is
    # the defect Run 38 met: a name split by the wrap is joined back with
    # a space by the `--brief` arm and by install-tables.sh, and
    # `prop_block_keeps_a_name_whole` reads it off the reader's own prose.
    # Width 40 rather than the 72 the defect fell at, so the break lands
    # inside a name on any class rather than on the one whose figures
    # happened to put it there.
    ('the class paragraph splits arm names at the wrap', 'read-run.py',
     "    print(textwrap.fill(' '.join(out), width=72,"
     " break_on_hyphens=False))",
     "    print(textwrap.fill(' '.join(out), width=40))",
     # NOT the shared PROPS: the env's CORPUS_LIMIT=2 bounds the runs
     # OPENED, and the two that sort first are main sets with no class
     # paragraph in them, so this judge reads the newest run's own
     # twenty-two JSONs instead -- twenty of them stride classes.
     'CORPUS_RUN=newest CORPUS_LIMIT=0 python3 "{dir}/properties.py"'),
    # The health line enumerating again: the cells go back in front of the
    # count, which is the shape the cut of 2026-09-08 removed, and
    # `prop_health_names_rows_not_cells` fails on the first run on disk
    # that has a sunk cell -- both probe files do, so the bound of two
    # runs the env sets is enough to show it.
    ('the sunk-cell warning enumerates every cell again', 'read-run.py',
     "            out.append('%d cell(s) whose forcing term is not smaller",
     "            out.append(', '.join('%s/%s' % (q, r) for _, q, r in sunk)"
     "\n                       + '%d cell(s) whose forcing term is not smaller",
     PROPS),
    # The reader's own invariants: a shape parse compared the wrong way
    # round fails the first check on every shape it finds in Main.hs.
    ('read-run selftest stops checking the shape parse', 'read-run.py',
     "            if d['l'] != want:", "            if d['l'] == want:", READER),
    # The emphasis column deciding the cross-class summary's bold, with
    # its comparison reversed. The summary is assembled BY HAND and the
    # rule was written nowhere a session assembling it would look, so Run
    # 28 inferred it from the previous run's table, broke four ties with
    # `--pair` instead of the column, and bolded the wrong cell of `rev`.
    # The judge reads the column back against the two figures printed
    # beside it on every row where they differ at the printed precision,
    # so a reversal shows on six of ten rows. It takes the NEWEST run's
    # classes alone: `--extremes` refuses a class named twice, so a glob
    # spanning two runs on disk makes its own baseline red.
    ('the emphasis column bolds the slower of the two cells', 'read-run.py',
     "                 r.floor, 'outside' if r.out < r.ceil else 'ceiling'))",
     "                 r.floor, 'outside' if r.out > r.ceil else 'ceiling'))",
     'PATH="{bin}:$PATH" python3 -c "import glob, os, re, subprocess, sys\nms = [m for m in glob.glob(os.path.join(\'{root}\', \'run*-*-main.json\')) if re.match(r\'run\\d+-[a-z0-9]+-main\\.json$\', os.path.basename(m))]\nif not ms: sys.exit(2)\nms.sort(key=lambda m: int(re.match(r\'run(\\d+)\', os.path.basename(m)).group(1)))\nrun, half = re.match(r\'(run\\d+)-([a-z0-9]+)-main\', os.path.basename(ms[-1])).groups()\ncs = sorted(glob.glob(os.path.join(\'{root}\', run + \'-\' + half + \'-*.json\')))\ncs = [c for c in cs if not re.search(r\'-(main|gate|al)[-.]\', c)]\nif len(cs) < 3: sys.exit(2)\nr = subprocess.run([sys.executable, \'{file}\', \'--extremes\', \'--classes\'] + cs, capture_output=True, text=True).stdout\nrows = re.findall(r\'^(\\w+)\\s+\\d+\\s+[\\d.]+\\s+[\\d.]+\\s+\\S+ ([\\d.]+)\\s+[-\\d.]+\\s+[-\\d.]+\\s+([\\d.]+)\\s+[\\d.]+%\\s+(outside|ceiling)\', r, re.M)\nif len(rows) < 3: sys.exit(1)\nbad = [n for n, o, c, b in rows if float(o) != float(c)\n       and b != (\'outside\' if float(o) < float(c) else \'ceiling\')]\nsys.exit(1 if bad else 0)"'),
    # The rate column taking the RAW count ratio where the CORRECTED one
    # belongs -- not hypothetical: Run 28 hand-rolled this arithmetic
    # before the column existed, read the raw field by an off-by-one into
    # the row, and got 41.2% where the answer is 21.9%. The judge
    # recomputes the rate from the corrected column the same output prints
    # and `--pair`'s own time geomean, so it catches the swap AND a column
    # blinded to `--`; it exits 0 with no run on disk, which is LOST
    # rather than caught, as every corpus judge here is.
    ('the rate column prices a saving against the raw counts', 'read-run.py',
     "                rate = ('%6.1f%%' % ((1 - t) / (1 - gnet) * 100)",
     "                rate = ('%6.1f%%' % ((1 - t) / (1 - geomean(raw)) * 100)",
     'PATH="{bin}:$PATH" python3 -c "import glob, os, re, subprocess, sys\nsw = [f for f in glob.glob(os.path.join(\'{root}\', \'run*-counts-*.txt\')) if re.match(r\'run\\d+-counts-[a-z0-9]+\\.txt$\', os.path.basename(f))]\nif not sw: sys.exit(2)\nsw.sort(key=lambda f: int(re.match(r\'run(\\d+)\', os.path.basename(f)).group(1)))\nrun, half = re.match(r\'(run\\d+)-counts-([a-z0-9]+)\\.txt\', os.path.basename(sw[-1])).groups()\njs = os.path.join(\'{root}\', run + \'-\' + half + \'-main.json\')\nif not os.path.exists(js): sys.exit(2)\nA = [\'mut-odo-vecdims-add-in-leaf-u2\', \'mut-odo-vecdims-add-in-leaf-u1\']\nrd = lambda e: subprocess.run([sys.executable, \'{file}\', js] + e, capture_output=True, text=True).stdout\no = rd([\'--counts\', sw[-1], \'--pair\'] + A)\nm = re.search(r\'([0-9.]+)\\s+([0-9.]+)\\s+([0-9]+)\\s+(-?[0-9.]+)%\', o)\nif not m: sys.exit(1)\nt = re.search(A[0] + \' / \' + A[1] + r\'\\s+([0-9.]+)\', rd([\'--pair\'] + A))\nif not t: sys.exit(0)\nw = (1 - float(t.group(1))) / (1 - float(m.group(1))) * 100\nsys.exit(0 if abs(w - float(m.group(4))) < 0.15 else 1)"'),
    # The ANSWERED stub's `___` gate, blinded: the comprehension keeps no
    # entry, so a README whose newest run entry is still the bare
    # placeholder passes. That is the state Run 28 reached the second
    # checker pass in, and the judge plants exactly it -- the fixture of
    # `answered-stub-keeps-its-slot` -- and fails when the message is
    # ABSENT, which is the direction a blinded check breaks in. It plants
    # the fixture itself rather than going through defect-run.py, which
    # refuses a copy that is in no git repository, as its siblings below do.
    ('check-doc stops reading the ANSWERED stub for its placeholder',
     'read-run.py',
     "             if '___' in l]",
     "             if False]",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'out = m.readme_answered_stub_unfilled(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--check-doc\', \'--quiet\','
     ' \'--readme\', out],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'still carry\' in r.stdout + r.stderr else 1)"'),
    # The population check's exemption for main-set shapes declared added
    # after the run: dropped, the fixture of the case
    # `main-shapes-added-after-the-run-are-exempt` fails on `match no
    # population`. The judge plants that fixture itself and runs the check,
    # rather than going through defect-run.py, which refuses a copy that
    # is in no git repository -- this one is not.
    ('check-doc holds the run file to today\'s main set', 'read-run.py',
     '        main_at_run = ([s for s in main_shapes if s not in added_after]',
     '        main_at_run = (main_shapes',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'out = m.plant_main_shapes_exempt(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--check-doc\', \'--quiet\','
     ' \'--readme\', out[\'readme\'], \'--run-doc\', out[\'rundoc\']],'
     ' capture_output=True, text=True)\n'
     'sys.exit(1 if \'match no population\' in r.stdout + r.stderr else 0)"'),
    # The population sizes' exemption for main shapes retired after the
    # run: dropped, the fixture of `retired-shapes-timed-by-the-run-are-
    # exempt` fails on `match no population`, the newest run file having
    # timed the shape the fixture retires.
    ('check-doc holds the run file to today\'s timed main set', 'read-run.py',
     '            s for s in retired_after\n',
     '            s for s in ()\n',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'out = m.plant_retired_shape_exempt(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--check-doc\', \'--quiet\','
     ' \'--readme\', out[\'readme\'], \'--main\', out[\'main\']],'
     ' capture_output=True, text=True)\n'
     'sys.exit(1 if \'match no population\' in r.stdout + r.stderr else 0)"'),
    # The class count's exemption for classes retired after the run:
    # dropped, the fixture of `retired-classes-timed-by-the-run-are-exempt`
    # fails on `class block(s) where Main.hs defines`, the newest run file
    # having timed the class the fixture retires.
    ('check-doc holds the run file to today\'s timed classes', 'read-run.py',
     '        retired = retired_classes(main_hs) - retired_after',
     '        retired = retired_classes(main_hs)',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'out = m.plant_retired_class_exempt(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--check-doc\', \'--quiet\','
     ' \'--readme\', out[\'readme\'], \'--main\', out[\'main\']],'
     ' capture_output=True, text=True)\n'
     'sys.exit(1 if \'class block(s) where Main.hs defines\' in r.stdout + r.stderr else 0)"'),
    # --draft's half rename, loosened to a plain word boundary: `-` is one,
    # so renaming the half `spot` then also renames `dead-spot`, the FORM
    # the pair varies, inside every [SAME] block it carries forward. The
    # judge plants the stub note whose block spells the trap out.
    ('--draft renames the half with a plain word boundary', 'read-run.py',
     "        body = re.compile(r'(?<![\\w`-])(%s)(?![\\w`-])'",
     "        body = re.compile(r'\\b(%s)\\b'",
     'python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'out = m.stub_pair_note(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--note\','
     ' out[\'note\'], \'--draft\', \'run24\', \'--halves\','
     ' \'g912,ghead\'], capture_output=True, text=True)\n'
     'sys.exit(0 if \'dead-spot\' in r.stdout else 1)"'),
    # The same rename with the BACKTICK boundary dropped, which is the form
    # it had until 2026-09-12. A `[SAME]` block spells a live half bare and
    # a historical one in backticks, so without that boundary the roll of
    # every half on record comes back with this run's tags standing where
    # two older ones were -- a well-formed list no checker reads, carried
    # again by the next draft. The judge writes its own note, that roll
    # being what the stub lacks.
    ('--draft rewrites a backticked roll of half names', 'read-run.py',
     "        body = re.compile(r'(?<![\\w`-])(%s)(?![\\w`-])'",
     "        body = re.compile(r'(?<![\\w-])(%s)(?![\\w-])'",
     # NO LITERAL BACKTICK IN THIS JUDGE: it is a shell string, and a
     # backtick inside one is command substitution, so a roll spelled out
     # here is executed rather than compared and the mutant reads as
     # MISSED. Built from chr(96) instead (2026-09-12).
     'python3 -c "import sys, tempfile, subprocess, os\n'
     'b = chr(96)\n'
     'roll = \'(\' + b + \'aligned\' + b + \', \' + b + \'g912\' + b'
     ' + \', \' + b + \'ghead\' + b + \', \' + b + \'spot\' + b + \')\'\n'
     'd = tempfile.mkdtemp(); n = os.path.join(d, \'run29-pair.txt\')\n'
     'open(n, \'w\').write(chr(10).join([\'hdr\', \'\','
     ' \'A [SAME]: g912 leads, ghead follows. Roll \' + roll + \'.\','
     ' \'HALVES: basis=g912 other=ghead\', \'\']))\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--note\', n,'
     ' \'--draft\', \'run30\', \'--halves\', \'spec,nospec\'],'
     ' capture_output=True, text=True)\n'
     'sys.exit(1 if roll not in r.stdout else 0)"'),
    # The carried-figure pattern with the full stop back in its trailing
    # class, which is how it was first written: every figure ENDING A
    # SENTENCE is then dropped, and that is where a carried figure most
    # often sits -- the fixture's own 0.4242 among them, so the mode reads
    # a registration and warns about nothing. The judge plants the case's
    # registration and requires the warning.
    ('--carried drops a figure that ends a sentence', 'read-run.py',
     "CARRIED_RE = re.compile(r'(?<![\\w.$-])(\\d\\.\\d{2,4})(?![\\w%])(?!\\.\\d)')",
     "CARRIED_RE = re.compile(r'(?<![\\w.$-])(\\d\\.\\d{2,4})(?![\\w.%])')",
     'python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     't = tempfile.mkdtemp()\n'
     'out = m.rundoc_carried_figures(t)\n'
     'j = m.synth_json(t, \'main\', name=\'b.json\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', j, \'--carried\','
     ' \'--others\', j, \'--run-doc\', out[\'rundoc\']],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'(1) quotes 0.4242\' in r.stdout else 1)"'),
    # The carried-block flag switched off: a `[SAME]` block naming a run
    # the rename does not touch comes through pointing one run too far
    # back and reads as correctly carried, every name in it having been
    # substituted. The judge plants the case's own note -- one block
    # naming run21, which no rename reaches, and one naming run23, which
    # becomes run24 -- and requires the notice.
    ('--draft stops flagging a block that names another run', 'read-run.py',
     "    if flagged:\n        rows = []",
     "    if False and flagged:\n        rows = []",
     'python3 -c "import importlib.util, sys, tempfile, subprocess, os\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'tmp = tempfile.mkdtemp()\n'
     'note = os.path.join(tmp, \'run23-pair.txt\')\n'
     'open(note, \'w\').write(\'hdr\\n\\nOLD [SAME]: against'
     ' run21-g912, the previous build.\\n\\nMINE [SAME]: run23-g912'
     ' leads.\\nHALVES: basis=g912 other=spot\\n\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--note\', note,'
     ' \'--draft\', \'run24\', \'--halves\', \'g912,ghead\'],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'CHECK THESE CARRIED BLOCKS\' in r.stdout else 1)"'),
    # The machine check unnamed again, which is the state Run 28's draft
    # met: the lead classifies as nothing, the block inherits `fill` from
    # the fill-in block above it, and `_fill_skeleton` passes a paragraph
    # with no rows through unchanged -- so the previous run's box move
    # arrives in the next note under a gate the same call reset to NOT RUN.
    # The judge plants the note whose ORDER is the trap and requires the
    # carried figure to be absent.
    ('the machine check is no longer named as the gate\'s', 'read-run.py',
     "            or lead.startswith(\"THE GATE'S VERDICT\")\n"
     "            or lead.startswith('THE MACHINE CHECK')):",
     "            or lead.startswith(\"THE GATE'S VERDICT\")):",
     'python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'out = m.stub_pair_note_machine_check(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--note\','
     ' out[\'note\'], \'--draft\', \'run24\', \'--halves\','
     ' \'g912,ghead\'], capture_output=True, text=True)\n'
     'sys.exit(0 if \'-3.66%\' not in r.stdout else 1)"'),
    # The three properties, each broken as its 2026-08-17 proof did: every
    # unit labelled `ns` fails the round-trip on every figure, a column test
    # widened by one fails the read-back on every row, and a reader that
    # refuses every run fails the third on every run.
    ('fmt_abs labels every unit ns', 'read-run.py',
     "            return _fig(seconds / scale) + ' ' + unit",
     "            return _fig(seconds / scale) + ' ns'", PROPS),
    ('readme_rows widens its column test by one', 'read-run.py',
     '        if len(cell) != 7:\n            continue\n        bare = re.sub',
     '        if len(cell) != 8:\n            continue\n        bare = re.sub',
     PROPS),
    ('the reader refuses every run', 'read-run.py',
     'def load(path, main_hs):\n    """(cells, shapes, strategies, meta); orders follow the run, not\n    the file."""\n',
     'def load(path, main_hs):\n    """(cells, shapes, strategies, meta); orders follow the run, not\n    the file."""\n    raise SystemExit(3)\n', PROPS),
    # The empty-corpus refusal: over a directory with no run, every property
    # must say it proved nothing, at exit 1.
    ('properties pass over an empty corpus', 'properties.py',
     '        if not n:', '        if False:',
     'd=$(mktemp -d); CORPUS="$d" python3 "{dir}/properties.py" >/dev/null 2>&1; test $? -eq 1'),
    # The shadow's one guard: a program cd-ing to an absolute path would run
    # for real from a shadow, and did once, overwriting a recorded run.
    # The registration check's two arms, each broken on its own. The judge
    # plants the synthetic registration from defects.py and requires the
    # FAIL: the fixture appends its own OPEN entry rather than editing the
    # live one, so neither judge depends on a registration being in hand.
    ('--lint stops holding a registration to the timed roster', 'read-run.py',
     "r'`([A-Za-z][A-Za-z0-9-]*)`', t))\n                          & untimed)",
     "r'`([A-Za-z][A-Za-z0-9-]*)`', t))\n                          & set())",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.readme_with_a_registration(tempfile.mkdtemp(), arm=m.parked_arm())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--lint\', \'--readme\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'does not time\' in r.stdout + r.stderr else 1)"'),
    # AND --lint REFUSES `both` ON A CROSS-HALF SPAN AWAY FROM 1, since
    # 2026-09-19. `cross` and `counts` read THIS half over the other, so
    # `both` reads one span twice and the two figures are reciprocals: a
    # target away from 1 holds on at most one half. Run 36's registration
    # wanted `cross list 1.2974`, where `both` would have killed half its
    # spans the day they were written. NOT Run 35's item (3), whose target
    # was 1.0 and which this refusal allows; that one died of its band.
    ('--lint stops refusing `both` on a cross span away from 1',
     'read-run.py',
     "                        if x and x > 0 and abs(1.0 / x - x) * 100 > band:",
     "                        if x and x > 0 and abs(1.0 / x - x) * 100 < band:",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.readme_with_a_registration(tempfile.mkdtemp(), cross_both_target=\'1.2974\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--lint\', \'--readme\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'on a cross-half kind with a target away from 1\' in r.stdout + r.stderr else 1)"'),
    ('--lint stops saying what a span compares', 'read-run.py',
     "            if reads:\n                print(\"      Run %s's %d span(s)",
     "            if not reads:\n                print(\"      Run %s's %d span(s)",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.readme_with_a_registration(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--lint\', \'--readme\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'on THIS half over the same arm\' in r.stdout + r.stderr else 1)"'),
    ('--lint stops resolving a registration\'s task pointers', 'read-run.py',
     "re.findall(r'\\b[Tt]ask (\\d+)', t)",
     "re.findall(r'\\bnosuchword (\\d+)', t)",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.readme_with_a_registration(tempfile.mkdtemp(), task=\'999\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--lint\', \'--readme\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'not under the tasks heading\' in r.stdout + r.stderr else 1)"'),
    # The deferral target's arms, unread: the registration's own arms are
    # still held to the roster and the task it points at is not, which is
    # the state Run 25 lost three predictions of four to. The judge plants
    # a task 99 naming a parked arm and defers to it.
    ('--lint stops reading the arms of a task a registration defers to',
     'read-run.py',
     "away = sorted(set(re.findall(r'`([A-Za-z][A-Za-z0-9-]*)`',\n"
     "                                             tasks[n])) & untimed)",
     "away = sorted(set(re.findall(r'`([A-Za-z][A-Za-z0-9-]*)`',\n"
     "                                             tasks[n])) & set())",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.readme_with_a_registration(tempfile.mkdtemp(), task_arm=m.parked_arm())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--lint\', \'--readme\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'which names arms the roster does not time\' in r.stdout + r.stderr else 1)"'),
    # The self-fingerprint refusal, removed: post-run 5b installs the
    # fingerprint into the run's own file, so from 5b the check reads the
    # run against itself and still says the box is fine. The judge builds
    # a run98 JSON beside a run98 fingerprint and asks for the refusal.
    ('--machine stops refusing a run its own fingerprint', 'read-run.py',
     '    if mine and kept and mine.group(0) == kept.group(0):',
     '    if False:',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess, os\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     't = tempfile.mkdtemp(); fp = os.path.join(t, \'run98.md\')\n'
     'j = m.synth_json(t, \'main\', name=\'run98-g-main.json\', fingerprint=fp)\n'
     'r = subprocess.run([sys.executable, \'{file}\', j, \'--machine\','
     ' \'--run-doc\', fp], capture_output=True, text=True)\n'
     'sys.exit(0 if \'OWN fingerprint\' in r.stdout + r.stderr else 1)"'),

    # THE PLATEAU GATE, made blind to the state it now reads. Until Run 29
    # this gate banded the preamble victim's ms/iter, which is timed with
    # `list`, so a pair whose variable moves `list` failed on its own
    # variable; the gate is the `inuse`/`keep` the same line carries now.
    # Collapsing the distinct-state key makes every process look alike and
    # the gate never fire. The judge plants the newest run on disk beside
    # the mutated driver -- the only fixture with the logs AND the JSONs
    # this driver needs -- and moves one process's `inuse` on its
    # `@@saturate` line, so it is LOST rather than green with no run on
    # disk, which is the honest reading of a check that needs a run; it
    # named Run 29 until 2026-09-18, when that run's artifacts were
    # deleted. read-all.sh had no mutant at all before this, which is why
    # the gate could be rewritten without one.
    ('the plateau gate cannot tell two states apart', 'read-all.sh',
     'NF >= 3 { n++; k[$2 " " $3] = 1 }',
     'NF >= 3 { n++; k["one"] = 1 }',
     'R=$(ls {root}/run*-*-main.json | sed "s|.*/\\(run[0-9]*\\)-.*|\\1|" | sort -V | tail -1); ln -s {root}/$R-*.json "{dir}/" 2>/dev/null; cp {root}/$R-*.log {root}/$R-pair.txt "{dir}/" 2>/dev/null; L=$(ls "{dir}"/$R-*-rev.log | head -1); sed -i "/^@@saturate /s/inuse=[0-9]*/inuse=7/" "$L"; {file} $R 2>&1 | grep -q "did not assert ONE state"'),

    # The heading-spacing gate, made blind: `n != 2` becomes `False`, so
    # a heading run straight into the paragraph above it passes -- the
    # state README was in for the whole of Run 27's write-up, past every
    # other gate, both checker passes and the comprehension probe. The
    # judge plants a run file with one blank line before its second
    # heading and asks for the refusal.
    ('check-doc stops holding a heading to two blank lines', 'read-run.py',
     '        if n != 2:', '        if False:',
     'printf \'# Run 97\\n\\nA head paragraph.\\n\\n## Results\\n\\nA para.\\n\''
     ' > "{dir}/run97.md"; '
     '{file} --check-doc --quiet --run-doc "{dir}/run97.md" 2>&1'
     ' | grep -q "is preceded by 1 blank"'),
    # Step 2c's comment skip, removed: `<yours>` inside a `#` line counts
    # as a slot the note still owes. That is not hypothetical -- --draft's
    # own header explains the marker and so carries it twice, and a
    # session makes its note by redirecting that header, so without the
    # skip every freshly drafted note reports two owed slots it does not
    # owe. The judge plants a note whose ONLY marker is in a comment and
    # asks for the clean verdict.
    ('run-status counts a marker inside a comment', 'run-status.sh',
     "SLOTS=$(grep -v '^[[:space:]]*#' \"$NOTE\" | grep -F '<yours>' || true)",
     "SLOTS=$(grep -F '<yours>' \"$NOTE\" || true)",
     'printf \'a stand-in pair note.\\nHALVES: basis=lookrts other=a1g\\n'
     '# a header explaining <yours>\\n\' > "{dir}/run97-pair.txt"; '
     '{file} run97 2>&1 | grep -q "no <yours> slot left"'),
    # The instance gate swaps a slow launch draw for its copy; the mutant
    # raises the bar past any ratio, so nothing is ever redrawn. The judge
    # plants a stand-in pair in the copy's own directory as the mount,
    # fakes a launch instance 10% slower than its copy, and wants the swap.
    ('instance-gate never redraws a slow launch instance', 'instance-gate.sh',
     "'BEGIN{exit !(r > 1 + bar / 100)}'",
     "'BEGIN{exit !(r > 2 + bar / 100)}'",
     'printf \'a stand-in pair note.\\nHALVES: basis=lookrts other=a1g\\n\''
     ' > "{dir}/zzig-pair.txt"; cp /bin/true "{dir}/zzig-lookrts";'
     ' cp /bin/true "{dir}/zzig-a1g";'
     ' INSTANCE_DIR=. INSTANCE_FAKE=1100,1000 {file} zzig 2>&1 | grep -q REDRAWN'),
    # The reaper refusal reads the switch; the mutant makes it never fire.
    # The judge launches under a fake harness marker with the switch empty
    # and wants the refusal named.
    ('run-evening starts under the harness without the reaper switch',
     'run-evening.sh',
     '   [ "${CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP:-}" != 1 ]; then',
     '   [ "${CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP:-}" = 2 ]; then',
     'CLAUDE_CODE_SESSION_ID=zz CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP= '
     '{file} zznone 2>&1 | grep -q "PRESSURE_REAP=1"'),
    # A refused gate is a row UNCHECKED and not a row dropped: --show
    # exits before printing on a missing binary, and the mutant puts back
    # the `if gf:` that left `want` without the row at a PASS. The judge
    # plants a note carrying the row and no binaries, so the gate refuses.
    ('--figures drops a refused gate row instead of leaving it unchecked',
     'preflight.sh',
     "want.append(('gate arms', gf or ['']))",
     "want.append(('gate arms', gf)) if gf else None",
     'printf \'a stand-in pair note.\\nHALVES: basis=lookrts other=a1g\\n\\n'
     'Verified when built, 2026-09-18:\\n  gate arms        7 arms, expect 21'
     ' benches\\n\' > "{dir}/zzpf-pair.txt"; '
     '{file} zzpf --figures 2>&1 | grep -q "gate arms .*gave nothing to check"'),
    # A refused --compare is a row of the delta bullet's range, and the
    # mutant makes it the silence it was. The judge shadows the run whose
    # rev JSON sorts last with both such JSONs cut off mid-file, so
    # --compare refuses that population; LOST with no rev JSON on disk,
    # as every corpus judge.
    ('a refused --compare drops its population from the delta range in silence',
     'read-all.sh',
     '      || echo "!! $pop: --compare gave no list line, so the range omits it"',
     '      || :',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, os, subprocess, sys, tempfile\n'
     'spec = importlib.util.spec_from_file_location(\'d\', os.path.join(\'{root}\', \'defects.py\'))\n'
     'd = importlib.util.module_from_spec(spec)\n'
     'spec.loader.exec_module(d)\n'
     'revs = sorted(f for f in os.listdir(\'{root}\') if f.startswith(\'run\') and f.endswith(\'-rev.json\') and not f.startswith(\'runzz\'))\n'
     'if not revs: sys.exit(2)\n'
     'run = revs[-1].split(\'-\')[0]\n'
     'extra = []\n'
     'for f in revs:\n'
     '    if f.startswith(run + \'-\'):\n'
     '        whole = open(os.path.join(\'{root}\', f)).read()\n'
     '        extra.append((f, whole[:len(whole) // 2]))\n'
     'sd = d.shadow_dir(tempfile.mkdtemp(), \'read-all.sh\', open(\'{file}\').read(), extra=extra)\n'
     'r = subprocess.run([os.path.join(sd, \'read-all.sh\'), run, \'--brief-facts\'], capture_output=True, text=True)\n'
     'sys.exit(0 if \'!! rev: --compare gave no list line\' in r.stdout else 1)"'),
    # The out-of-range refusal, removed: a table number past the section
    # falls through to an index that is not there. Silence and a traceback
    # both read like a section carrying no table, which is the reading
    # --section exists to make visible. The judge asks for table 9 of 3.
    # The chapter's monitor arming line, no longer held to `-n +1`: the
    # flag was dropped once on a live run and prose alone did not hold it,
    # so the check that replaced the prose has to be shown to bite. The
    # judge plants a README with the flag removed and asks the mutated
    # reader for the failure line. NO LITERAL BACKTICK: it is a shell
    # string, so the match is on the words either side of the flag.
    ('the arming line may drop the monitor replay flag', 'read-run.py',
     "    lost = [l for l in arming if '-n +1' not in l]",
     "    lost = []",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile,'
     ' subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\','
     ' \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.edited_readme(tempfile.mkdtemp(), (\'tail -F -n +1 \','
     ' \'tail -F \'))\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--check-doc\','
     ' \'--worklists\', \'--readme\', f], capture_output=True, text=True)\n'
     'sys.exit(0 if \'monitor arming line(s) drop\' in r.stdout + r.stderr'
     ' else 1)"'),

    ('--section stops refusing a table number past the end', 'read-run.py',
     '    if with_tables and with_tables > len(tabs):',
     '    if False and with_tables > len(tabs):',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.doc_with_a_table(tempfile.mkdtemp(), 3)\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--section\', \'Middle\','
     ' \'--with-tables\', \'9\', \'--readme\', f], capture_output=True, text=True)\n'
     'sys.exit(0 if \'this section carries 3 table\' in r.stdout + r.stderr else 1)"'),
    # The survey's reachability guard, removed: the ninth saved site's
    # table word counts as a self-loop again. The judge plants the listing
    # from defects.py and asks the survey for its count. Over the first
    # listing until 2026-09-18, whose body the zero tell's instruction form
    # refuses too since that day, so this mutant survived it; the ninth is
    # the shape the flow test refuses alone.
    ('survey counts a data word as a loop again', 'loop-offsets.py',
     '        if not reaches(insns, k, n):\n            continue\n',
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom8_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'0 self-loops of at most\' in r.stdout else 1)"'),
    # THREE TABLE TELLS dropped: the continuation the sweep decoded out of
    # step counts as a straddling loop again, over the second listing. It
    # takes all three because they COINCIDE on that site -- its body
    # carries a `(bad)`, a run of six zero bytes and a `rex.RB clc` -- so
    # dropping the `(bad)` tell alone leaves the zero-run tell to refuse it
    # and this mutant survived, caught by this suite the day the second
    # tell landed (2026-09-11), and dropping those two leaves the stray-REX
    # tell to, caught the day that one landed (2026-09-18). No site on
    # record separates them; what proves the zero-run tell bites on its
    # own is the mutant below, whose listing carries no `(bad)`, and the
    # stray-REX tell the sixth listing's, whose body carries neither.
    ('survey counts a swallowed jump as a loop again', 'loop-offsets.py',
     "        if any(i[3] == '(bad)' for i in insns[k:n + 1]):\n            continue\n"
     "        # Nor does it carry a run of zero bytes, or an instruction of two:\n"
     "        # such a body IS a table, the third site in `reaches`.\n"
     "        if zero_run(insns, k, n):\n            continue\n"
     "        # Nor a stray REX prefix, `rex.*` in the mnemonic column: the sweep\n"
     "        # entered an instruction mid-way, a fifth shape, the sixth site in\n"
     "        # defects.py (2026-09-18), which carries the totals it moves.\n"
     "        if any(i[3].startswith('rex.') for i in insns[k:n + 1]):\n            continue\n",
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom2_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'still straddling   : 0\' in r.stdout else 1)"'),
    # The zero-run tell dropped: the info table whose own words are the
    # body counts as a straddling loop again, over the third listing.
    ('survey counts a table body as a loop again', 'loop-offsets.py',
     '        if zero_run(insns, k, n):\n            continue\n',
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom3_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'still straddling   : 0\' in r.stdout else 1)"'),
    # The pad-head tell dropped: the pad and the table word after it count
    # as a six-byte self-loop again, over the fifth listing.
    ('survey counts a nop pad and its table word as a loop again', 'loop-offsets.py',
     "        if PAD.match(insns[k][3] + ' ' + insns[k][4]):\n            continue\n",
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom4_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'0 self-loops of at most\' in r.stdout else 1)"'),
    # The stray-REX tell, removed: the sixth site's continuation push
    # reads as a seven-byte loop again.
    ('survey counts a return-address word as a loop again', 'loop-offsets.py',
     "        if any(i[3].startswith('rex.') for i in insns[k:n + 1]):\n            continue\n",
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom5_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'0 self-loops of at most\' in r.stdout else 1)"'),
    # The zero tell's instruction form dropped, its run of four kept: the
    # seventh site's two table bytes and their word read as a four-byte
    # loop again.
    ('survey counts a table word pair as a loop again', 'loop-offsets.py',
     "    return any(i[2] == '0000' for i in insns[k:n + 1])\n",
     "    return False\n",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom6_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'0 self-loops of at most\' in r.stdout else 1)"'),
    # The pad tell narrowed back to the `nop` spelling alone: the eighth
    # site's `xchg %ax,%ax` pad and its table word read as a four-byte loop
    # again.
    ('survey counts a two-byte pad and its table word as a loop again', 'loop-offsets.py',
     "        if PAD.match(insns[k][3] + ' ' + insns[k][4]):\n            continue\n",
     "        if insns[k][3].startswith('nop'):\n            continue\n",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom7_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'0 self-loops of at most\' in r.stdout else 1)"'),
    # The continuation line dropped from `parse` again: the tenth site's
    # loop, holding an eight-byte push, falls one byte short of its span and
    # the survey counts nothing.
    ('the survey drops a body with an eight-byte instruction again', 'loop-offsets.py',
     "            m = CONT.match(line)\n            if m and insns:\n",
     "            m = None\n            if m and insns:\n",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.longinsn_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'1 self-loops of at most\' in r.stdout else 1)"'),
    # The flow test answering yes to everything: the eleventh site's
    # branch into an exit block counts as a straddling loop again.
    ('the survey counts a branch into an exit block as a loop again', 'loop-offsets.py',
     "    return live[n - k]\n",
     "    return True\n",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.exitblock_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'0 self-loops of at most\' in r.stdout else 1)"'),
    # The blanket form of 2026-09-04 back, refusing any unconditional
    # transfer inside a body: the twelfth site's loop, closed by a jmp to
    # its head, is lost again.
    ('the survey refuses a loop closed by a jmp again', 'loop-offsets.py',
     "    return live[n - k]\n",
     "    return live[n - k] and not any(UNCOND.match(i[3]) for i in insns[k:n + 1])\n",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.rotated_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'1 self-loops of at most\' in r.stdout else 1)"'),
    # The exit-span count's two halves, each broken on its own over the
    # fourth listing: the crossing test dropped, so the stepping loop at
    # residue 9 with its exit ending at byte 65 reads as in line; and the
    # unconditional-edge skip dropped, so the pair's `jmp` back edge grows
    # an exit span through the next block, the pre-f1a5adb shim's reading.
    ('the survey reads every exit span as in line', 'loop-offsets.py',
     "                   and f['mod'] + spans[f['start']] > LINE),\n",
     "                   and False),\n",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.exitspan_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'exit spans astride : 1\' in r.stdout else 1)"'),
    ('the survey reads an exit span past a jmp back edge', 'loop-offsets.py',
     "        if UNCOND.match(insns[n][3]):\n            continue\n",
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.exitspan_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'exit spans astride : 1\' in r.stdout and \'exit span 57 B\' not in r.stdout else 1)"'),
    # --delta's three readings, each broken on its own over the listings
    # defects.py builds for it: preservation reported whatever moved, the
    # selection taken of the OLD side alone again, and the libraries read
    # into the tracked groups again.
    ('--delta reports every offset preserved whatever moved', 'loop-offsets.py',
     '        if oo == nn:\n            preserved += 1\n',
     '        if True:\n            preserved += 1\n',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'o = m.delta_listings(tempfile.mkdtemp(), \'moves\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--delta\', o[\'old\'], o[\'new\']],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'offsets MOVED\' in r.stdout else 1)"'),
    ('--delta selects on the OLD side alone again', 'loop-offsets.py',
     '    keys = [k for k in og\n'
     '            if len(og[k]) >= min_copies or len(ng.get(k, ())) >= min_copies]\n',
     '    keys = [k for k in og if len(og[k]) >= min_copies]\n',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'o = m.delta_listings(tempfile.mkdtemp(), \'grows\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--delta\', o[\'old\'], o[\'new\']],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'1 -> 2 copies\' in r.stdout else 1)"'),
    ('--delta reads the libraries into the tracked groups again', 'loop-offsets.py',
     "            if want in (f['sym'] or ''):\n",
     '            if True:\n',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'o = m.delta_listings(tempfile.mkdtemp(), \'library\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--delta\', o[\'old\'], o[\'new\']],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'1 group(s) read\' in r.stdout else 1)"'),
    # The coverage check's two widenings of 2026-09-04, each reverted: the
    # indented-line exclusion taking every four-space line as code again,
    # and the figure regex wanting a decimal again. The judge plants the
    # README with an uncovered section from defects.py and requires the gap.
    ('check-doc takes a wrapped list continuation as code again', 'read-run.py',
     '            if indented and prev_blank and not in_code:\n'
     '                in_code = True\n',
     '            if indented:\n'
     '                in_code = True\n',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.readme_with_an_uncovered_figure(tempfile.mkdtemp(), \'wrapped\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--check-doc\', \'--quiet\', \'--readme\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if any(\'Zz coverage probe\' in l and \'bullet links\' in l for l in (r.stdout + r.stderr).split(chr(10))) else 1)"'),
    ('check-doc wants a decimal to see a figure again', 'read-run.py',
     "                       r'|\\b0x[0-9a-f]{3,}\\b')",
     "                       )",
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.readme_with_an_uncovered_figure(tempfile.mkdtemp(), \'hex\')\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--check-doc\', \'--quiet\', \'--readme\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if any(\'Zz coverage probe\' in l and \'bullet links\' in l for l in (r.stdout + r.stderr).split(chr(10))) else 1)"'),
    # THE THREE CHECKS RUN 26 ADDED OR WIDENED, 2026-09-06.
    # The worklist tally, which exists because a `tail -30` over
    # `--worklists` cut nine stale paragraphs out of a list of
    # twenty-two and the run adjudicated the remainder: count the
    # indented items and the tally must move with them.
    ('check-doc --worklists stops tallying its listed items', 'read-run.py',
     "    items = [l for l in lines if l.startswith('        ') and l.strip()]",
     "    items = []",
     'python3 -c "import subprocess, sys\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--check-doc\', \'--worklists\'],'
     ' cwd=\'{dir}\', capture_output=True, text=True)\n'
     'ok = any(l.startswith(\'worklist tally: \') and not l.startswith(\'worklist tally: 0 \')'
     ' for l in r.stdout.split(chr(10)))\n'
     'sys.exit(0 if ok else 1)"'),
    # The floor-pair agreement check, widened from one phrasing to five
    # after it saw two of the six sites Run 26 carries: drop the four
    # added phrasings and it falls back to fewer than two sites, which
    # is the state where it reports that it did not run.
    ('shadow_dir holds a program that cds to an absolute path', 'defects.py',
     '''    if re.search(r'^\\s*(cd|pushd)\\s+(--\\s+)?["\\']?(/|~|\\$HOME)', text, re.M):''',
     '    if False:',
     'python3 -c "import importlib.util, sys, tempfile\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{file}\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'try:\n    m.shadow_dir(tempfile.mkdtemp(), \'probe-areacurve.sh\', \'cd /nowhere-zz\\n\')\n'
     'except AssertionError:\n    sys.exit(0)\nsys.exit(1)"'),
    # The note's declaration turned into a blanket pass: every run then
    # reads its state split as expected, declared or not, and the one
    # gate that can see a process which saturated somewhere else is off
    # for everybody. The declaration is meant to cost a sentence in a
    # note; this is what it looks like when it costs nothing.
    ('the pair note\'s EXPECT line becomes a blanket pass', 'read-all.sh',
     '  case " $EXPECTED " in *" $1 "*) return 0 ;; esac\n'
     '  return 1',
     '  return 0',
     'python3 -c "import importlib.util, sys, tempfile, subprocess, os\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'tmp = tempfile.mkdtemp()\n'
     'd = os.path.dirname(os.path.abspath(\'{file}\'))\n'
     'f = m.synthetic_run(tmp, plateau=[\'16.4\', \'19.1\'],'
     ' states=[1, 2], into=d)\n'
     'r = subprocess.run([\'{file}\', f[\'tag\']],'
     ' capture_output=True, text=True, cwd=d)\n'
     'sys.exit(0 if r.returncode != 0 else 1)"'),

    # --counts-totals' unfinished branch made silent: the killed leg is
    # then dropped from the table AND from the totals with nothing said,
    # so the scale a preparation reads is short by whatever that leg
    # would have cost and nothing on the screen says which. Summing it
    # would be loud; dropping it is not, which is why this is the branch
    # worth a mutant rather than the arithmetic.
    ('--counts-totals stops naming a leg that never ended', 'read-run.py',
     "        if end is None:\n"
     "            unfinished.append((os.path.basename(path),"
     " 'no `# end` stamp'))\n"
     '            continue',
     "        if end is None:\n"
     '            continue',
     'python3 -c "import importlib.util, sys, tempfile, subprocess, os\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'tmp = tempfile.mkdtemp()\n'
     'm.counts_leg(tmp, \'zz\', \'a\', elapsed=300)\n'
     'm.counts_leg(tmp, \'zz\', \'b\', ended=False)\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--counts-totals\','
     ' os.path.join(tmp, \'zz\')], capture_output=True, text=True)\n'
     'sys.exit(0 if \'NOT summed\' in r.stdout else 1)"'),

    # --over-list's comparison switched off: the sweep then reports its
    # denominator and no hits, which is exactly what a clean run reads
    # like -- the failure the mode exists to make impossible. ITS CONTROL
    # PLANTS ITS OWN POPULATION rather than reading the newest run on
    # disk: a control that a run's own finding can retire is not a
    # control, which is what the property-1 mutant below cost on Run 31,
    # and the mutants copy holds tracked files alone in any case.
    ('--over-list stops comparing an arm with its shape\'s list',
     'read-run.py',
     '                if v / base > 1.0:',
     '                if False:',
     'python3 -c "import importlib.util, sys, tempfile, subprocess, os\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'tmp = tempfile.mkdtemp()\n'
     'sh = m.main_shapes()[0]\n'
     'm.synth_json(tmp, \'main\', name=\'zz-a-main.json\','
     ' skew=[(sh, m._reader().PLAIN, 100)])\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--over-list\','
     ' os.path.join(tmp, \'zz\')], capture_output=True, text=True)\n'
     'sys.exit(0 if \'cell(s) above 1\' in r.stdout else 1)"'),

    # THE TWO PER-SHAPE PROPERTY CLAUSES OF 2026-09-06, judged on the
    # newest main-set run on disk through the default mode, which prints
    # them for the main set as --block does for a class. Each mutant
    # swaps a clause's two arms, so a run on which it holds reads BREAKS.
    # Under pipefail since 2026-09-18: the status was grep's alone, so a
    # reader that printed HOLDS and then died read as a clean baseline.
    ('property 1 stops reading mut-odo-vecdims against bq-expand', 'read-run.py',
     "    clause('property 1, ahead of `bq-expand` on every shape', 'net',\n"
     "           PLAIN, LAST_CANDIDATE, 1.0)",
     "    clause('property 1, ahead of `bq-expand` on every shape', 'net',\n"
     "           LAST_CANDIDATE, PLAIN, 1.0)",
     'set -o pipefail; f=$(ls "{root}"/run[0-9]*-rev.json 2>/dev/null | tail -1); test -n "$f" '
     '&& python3 "{file}" "$f" --block 2>/dev/null | grep -q "property 1, ahead of .bq-expand. on every shape: HOLDS"'),
    ('property 2 stops reading mut-odo-vecdims against list', 'read-run.py',
     "    clause('property 2, allocation at most 1% over `list` on every shape',\n"
     "           'alloc', PLAIN, 'list', 1.01)",
     "    clause('property 2, allocation at most 1% over `list` on every shape',\n"
     "           'alloc', 'list', PLAIN, 1.01)",
     'set -o pipefail; f=$(ls "{root}"/run[0-9]*-main.json 2>/dev/null | tail -1); test -n "$f" '
     '&& python3 "{file}" "$f" 2>/dev/null | grep -q "property 2, allocation at most 1% over .list. on every shape: HOLDS"'),
    # THE EXECUTION ORDER GOING STALE UNDER THE LIST. POST_EXEC is a
    # second statement of the post list's shape, so the one way it can
    # lie is a step moving and the constant not; _exec_order compares
    # the two SETS and prints nothing when they part, naming the step.
    # Mutated by dropping 10a, which is exactly what a renumbering
    # would do. Judged on the banner's presence and not its content:
    # the order itself is prose-derived and a judge reading it would
    # be asserting this constant against itself.
    ('the execution order goes stale under a renumbered list',
     'read-run.py',
     "'4b', '10a', '5', '5a',",
     "'4b', '5', '5a',",
     'set -o pipefail; python3 "{file}" --checklist post --imperative'
     ' --readme "{dir}/README.md" 2>/dev/null | grep -q "EXECUTION ORDER"'),
    # THE NOTE PROMISING A BLOCK IT DOES NOT CARRY. Run 37's note put
    # its post-run step 9 half `at the foot of this note under
    # LEARNED` and carried none; that half is one session's and went
    # with it. Mutated by making the presence test vacuous, which is
    # how such a check usually dies. Judged on a stand-in note built
    # in the copy, so it does not go LOST with the run's own note at
    # post-run 11's deletion offer.
    ('note-check stops asking whether a promised block is there',
     'read-run.py',
     "        if not re.search(r'^%s\\b' % re.escape(name), text, re.M):",
     "        if False:",
     # NO pipefail here: --note-check exits 1 whenever it finds
     # anything, which a stand-in note always does, so a pipefail
     # pipeline reads red on the UNMUTATED file and the mutant is
     # LOST. The status is split from the grep instead.
     ' printf \'A stand-in pair note [EXEC].\\nWHAT THE PREPARATION'
     ' LEARNED is at the foot of this note under LEARNED.\\nHALVES:'
     ' basis=gheadnospec other=gheadtwopass\\n\' >'
     ' "{dir}/run97-pair.txt";'
     ' python3 "{file}" --note-check "{dir}/run97-pair.txt"'
     ' > "{dir}/nc.out" 2>/dev/null;'
     ' grep -q "promises a block" "{dir}/nc.out"'),
    # THE BRIEF'S PASTE DISCARDING PROSE WITHOUT SAYING SO. It
    # re-pastes items 5 and 6 from the facts file, whose `<yours>`
    # slots are empty, so a second run over a filled brief silently
    # overwrites what a session wrote there -- Run 37 did it while
    # testing something else and found it by reading its own diff.
    # Refusing would be wrong, the figures above wanting the paste,
    # so the guard only SAYS it; mutated by making it vacuous.
    ('the brief re-opens filled slots without saying so',
     'read-run.py',
     '    if now > was:',
     '    if False:',
     'set -o pipefail; d="{dir}/briefmut";'
     ' mkdir -p "$d/log-read-run97";'
     ' printf \' 5. THIS RUN ONLY\\n    A FILLED SENTENCE.\\n'
     ' 6. THIS RUN ONLY\\n    ANOTHER FILLED ONE.\\n\''
     ' > "$d/checker-brief.txt";'
     ' printf \'paste over checker-brief.txt items 5 and 6\\n'
     ' 5. THIS RUN ONLY\\n    <yours: a>\\n 6. THIS RUN ONLY\\n'
     '    <yours: b>\\n\' > "$d/log-read-run97/for-brief.txt";'
     ' cd "$d" && python3 "{file}" --brief-update run97'
     ' --brief-dir . 2>&1 | grep -q "RE-OPENED"'),
]
