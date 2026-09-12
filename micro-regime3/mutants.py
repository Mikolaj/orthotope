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

MUTANTS = [
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
    # The per-view floor's whole judgement is one comparison, so inverting
    # it is a mutant of the tool. The judge greps for the finding the tool
    # was written to make -- `flip-last-rows` starred in the
    # `mut-odo-vecdims` group on Run 27's HEAD half, 6.14% against a 0.32%
    # class floor -- and a mutant that stops the star fails it. LOST rather
    # than green with no run on disk, as every corpus judge here is.
    ('the per-view floor stars a view no wider than its class',
     'view-floor.py',
     '                over = b in floor and sp > a.factor * floor[b]',
     '                over = b in floor and sp < a.factor * floor[b]',
     'python3 "{file}" run27 -d "{root}" -c flip | '
     'grep -q "flip-last-rows.*mut-odo-vecdims 6\\."'),
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
    ('the emphasis column bolds the slower of the two cells',
     'read-run.py',
     "                 r.floor, 'outside' if r.out < r.ceil else 'ceiling'))",
     "                 r.floor, 'outside' if r.out > r.ceil else 'ceiling'))",
     'PATH="{bin}:$PATH" python3 -c "import glob, os, re, subprocess, sys\nms = sorted(glob.glob(os.path.join(\'{root}\', \'run*-g912-main.json\')))\nif not ms: sys.exit(0)\nrun = os.path.basename(ms[-1]).split(\'-g912-\')[0]\ncs = sorted(glob.glob(os.path.join(\'{root}\', run + \'-g912-*.json\')))\ncs = [c for c in cs if not re.search(r\'-(main|gate|al)[-.]\', c)]\nif len(cs) < 3: sys.exit(0)\nr = subprocess.run([sys.executable, \'{file}\', \'--extremes\', \'--classes\'] + cs, capture_output=True, text=True).stdout\nrows = re.findall(r\'^(\\\\w+)\\\\s+\\\\d+\\\\s+[\\\\d.]+\\\\s+[\\\\d.]+\\\\s+\\\\S+ ([\\\\d.]+)\\\\s+[-\\\\d.]+\\\\s+[-\\\\d.]+\\\\s+([\\\\d.]+)\\\\s+[\\\\d.]+%\\\\s+(outside|ceiling)\', r, re.M)\nif len(rows) < 3: sys.exit(1)\nbad = [n for n, o, c, b in rows if float(o) != float(c)\n       and b != (\'outside\' if float(o) < float(c) else \'ceiling\')]\nsys.exit(1 if bad else 0)"'),
    # The rate column taking the RAW count ratio where the CORRECTED one
    # belongs -- not hypothetical: Run 28 hand-rolled this arithmetic
    # before the column existed, read the raw field by an off-by-one into
    # the row, and got 41.2% where the answer is 21.9%. The judge
    # recomputes the rate from the corrected column the same output prints
    # and `--pair`'s own time geomean, so it catches the swap AND a column
    # blinded to `--`; it exits 0 with no run on disk, which is LOST
    # rather than caught, as every corpus judge here is.
    ('the rate column prices a saving against the raw counts',
     'read-run.py',
     "                rate = ('%6.1f%%' % ((1 - t) / (1 - gnet) * 100)",
     "                rate = ('%6.1f%%' % ((1 - t) / (1 - geomean(raw)) * 100)",
     'PATH="{bin}:$PATH" python3 -c "import glob, os, re, subprocess, sys\nsw = sorted(glob.glob(os.path.join(\'{root}\', \'run*-counts-g912.txt\')))\nif not sw: sys.exit(0)\nrun = os.path.basename(sw[-1]).split(\'-counts-\')[0]\njs = os.path.join(\'{root}\', run + \'-g912-main.json\')\nif not os.path.exists(js): sys.exit(0)\nA = [\'mut-odo-vecdims-add-in-leaf-u1-ptr\', \'mut-odo-vecdims-add-in-leaf-u1\']\nrd = lambda e: subprocess.run([sys.executable, \'{file}\', js] + e, capture_output=True, text=True).stdout\no = rd([\'--counts\', sw[-1], \'--pair\'] + A)\nm = re.search(r\'([0-9.]+)\\\\s+([0-9.]+)\\\\s+([0-9]+)\\\\s+(-?[0-9.]+)%\', o)\nif not m: sys.exit(1)\nt = re.search(A[0] + \' / \' + A[1] + r\'\\\\s+([0-9.]+)\', rd([\'--pair\'] + A))\nif not t: sys.exit(0)\nw = (1 - float(t.group(1))) / (1 - float(m.group(1))) * 100\nsys.exit(0 if abs(w - float(m.group(4))) < 0.15 else 1)"'),
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
     "    if flagged:\n        marks = ",
     "    if False and flagged:\n        marks = ",
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
    # era_main_hs's trim, dropped: the captured-run cases read `--claims`
    # against a Main.hs trimmed to the run's own shapes, and untrimmed the
    # population gate fires and suppresses every figure -- which is the
    # state those cases were in on 2026-09-02, two red and one passing
    # vacuously. The judge plants the control fixture and requires the
    # figure to be listed, reaching the run through CORPUS because the
    # copy holds tracked files alone. Since the retirement of 2026-09-04
    # every captured run carries today's whole timed main set, so the trim
    # had nothing to remove and this mutant survived: the judge now plants
    # a timed shape no run has into the copy's Main.hs first, which the
    # trim removes and the untrimmed gate fires on, whatever the roster.
    # Planted into a Main.hs of the judge's own and never into the copy's:
    # written there, nothing restored it, and every later judge read two
    # probe entries (2026-09-04).
    ('era_main_hs stops trimming the main set', 'defects.py',
     "        src = src[:i] + '\\n'.join(kept) + src[j:]",
     "        src = src[:i] + '\\n'.join(entries) + src[j:]",
     'python3 -c "import importlib.util, os, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     's = open(os.path.join(\'{dir}\', \'Main.hs\')).read()\n'
     'i = s.index(\'\\nstretchShapes =\\n\'); j = s.index(\'\\n  ]\', i)\n'
     's = s[:j] + \'\\n  , (\\"zz-era-probe\\", [3, 3, 3])  -- 27\' + s[j:]\n'
     'm.MAIN = os.path.join(tempfile.mkdtemp(), \'Main.hs\')\n'
     'open(m.MAIN, \'w\').write(s)\n'
     'run = os.path.join(os.environ[\'CORPUS\'], \'run25-g912-main.json\')\n'
     'doc = m.rundoc_retirement_sentence(tempfile.mkdtemp(), False)\n'
     'main = m.era_main_hs(tempfile.mkdtemp(), run)\n'
     'r = subprocess.run([sys.executable, \'{dir}/read-run.py\', run,'
     ' \'--claims\', \'--run-doc\', doc, \'--main\', main],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'0.8271\' in r.stdout else 1)"'),
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
    # The digest check, made unconditional: every ITEM block reads present
    # whether or not the carrier returned one, which is the state the
    # three steps were in before 2026-09-05 -- a delegated reading not
    # taken reading the same as one taken. The judge asks an unstarted
    # run, whose digest cannot exist, for the refusal.
    # THE PLATEAU GATE, made blind to the state it now reads. Until Run 29
    # this gate banded the preamble victim's ms/iter, which is timed with
    # `list`, so a pair whose variable moves `list` failed on its own
    # variable; the gate is the `inuse`/`keep` the same line carries now.
    # Collapsing the distinct-state key makes every process look alike and
    # the gate never fire. The judge plants a real run beside the mutated
    # driver -- the only fixture with the logs AND the JSONs this driver
    # needs -- and moves one process's `inuse`, so it is LOST rather than
    # green once those artifacts are deleted, which is the honest reading
    # of a check that needs a run. read-all.sh had no mutant at all before
    # this, which is why the gate could be rewritten without one.
    ('the plateau gate cannot tell two states apart', 'read-all.sh',
     'NF >= 3 { n++; k[$2 " " $3] = 1 }',
     'NF >= 3 { n++; k["one"] = 1 }',
     'ln -s {root}/run29-*.json "{dir}/" 2>/dev/null; '
     'cp {root}/run29-*.log "{dir}/" 2>/dev/null; '
     'sed -i "s/inuse=95420416/inuse=7/" "{dir}/run29-spec-rev.log"; '
     '{file} run29 2>&1 | grep -q "did not assert ONE state"'),
    ('run-status stops wanting the carrier digest', 'run-status.sh',
     'if grep -qE "^ITEM ${it}([^0-9]|\\$)" "$READINGS" 2>/dev/null; then',
     'if true; then',
     '{file} run98 2>&1 | grep -q "no ITEM 5 block"'),
    # The end-of-line half of that same pattern, taken back out: a header
    # reading `ITEM N` and nothing after it stops matching, which is the
    # form the chapter asks for and the one Run 27's carrier wrote, where
    # Run 26's carried a title. The judge plants bare headers and asks for
    # the present verdict.
    ('run-status wants a title after the ITEM number', 'run-status.sh',
     'if grep -qE "^ITEM ${it}([^0-9]|\\$)" "$READINGS" 2>/dev/null; then',
     'if grep -q "^ITEM ${it}[^0-9]" "$READINGS" 2>/dev/null; then',
     'printf \'ITEM 2\\nITEM 4\\nITEM 5\\nITEM 6\\n\' > "{dir}/run97-readings.txt"; '
     '{file} run97 2>&1 | grep -q "carries the ITEM 5 block"'),
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
    # The out-of-range refusal, removed: a table number past the section
    # falls through to an index that is not there. Silence and a traceback
    # both read like a section carrying no table, which is the reading
    # --section exists to make visible. The judge asks for table 9 of 3.
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
    # The survey's reachability guard, removed: the saved site's data word
    # counts as a straddling loop again. The judge plants the listing from
    # defects.py and asks the survey for its straddle count.
    ('survey counts a data word as a loop again', 'loop-offsets.py',
     '        if not reaches(insns, k, n, targets):\n            continue\n',
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'still straddling   : 0\' in r.stdout else 1)"'),
    # BOTH TABLE TELLS dropped: the continuation the sweep decoded out of
    # step counts as a straddling loop again, over the second listing. It
    # takes both because they COINCIDE on that site -- its body carries a
    # `(bad)` and a run of six zero bytes -- so dropping the `(bad)` tell
    # alone leaves the zero-run tell to refuse it and this mutant survived,
    # caught by this suite the day the second tell landed (2026-09-11). No
    # site on record separates them; what proves the zero-run tell bites on
    # its own is the mutant below, whose listing carries no `(bad)`.
    ('survey counts a swallowed jump as a loop again', 'loop-offsets.py',
     "        if any(i[3] == '(bad)' for i in insns[k:n + 1]):\n            continue\n"
     "        # Nor does it carry a run of zero bytes: such a body IS a table,\n"
     "        # the third site in `reaches`.\n"
     "        if zero_run(body):\n            continue\n",
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
     '        if zero_run(body):\n            continue\n',
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom3_listing(tempfile.mkdtemp())[\'dis\']\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--survey\', f],'
     ' capture_output=True, text=True)\n'
     'sys.exit(0 if \'still straddling   : 0\' in r.stdout else 1)"'),
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
    # THE TWO PER-SHAPE PROPERTY CLAUSES OF 2026-09-06, judged on the
    # newest main-set run on disk through the default mode, which prints
    # them for the main set as --block does for a class. Each mutant
    # swaps a clause's two arms, so a run on which it holds reads BREAKS.
    ('property 1 stops reading mut-odo-vecdims against bq-expand', 'read-run.py',
     "    clause('property 1, ahead of `bq-expand` on every shape', 'net',\n"
     "           PLAIN, LAST_CANDIDATE, 1.0)",
     "    clause('property 1, ahead of `bq-expand` on every shape', 'net',\n"
     "           LAST_CANDIDATE, PLAIN, 1.0)",
     'f=$(ls "{root}"/run[0-9]*-main.json 2>/dev/null | tail -1); test -n "$f" '
     '&& python3 "{file}" "$f" 2>/dev/null | grep -q "property 1, ahead of .bq-expand. on every shape: HOLDS"'),
    ('property 2 stops reading mut-odo-vecdims against list', 'read-run.py',
     "    clause('property 2, allocation at most 1% over `list` on every shape',\n"
     "           'alloc', PLAIN, 'list', 1.01)",
     "    clause('property 2, allocation at most 1% over `list` on every shape',\n"
     "           'alloc', 'list', PLAIN, 1.01)",
     'f=$(ls "{root}"/run[0-9]*-main.json 2>/dev/null | tail -1); test -n "$f" '
     '&& python3 "{file}" "$f" 2>/dev/null | grep -q "property 2, allocation at most 1% over .list. on every shape: HOLDS"'),
]
