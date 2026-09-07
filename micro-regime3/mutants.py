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
    # The reader's own invariants: a shape parse compared the wrong way
    # round fails the first check on every shape it finds in Main.hs.
    ('read-run selftest stops checking the shape parse', 'read-run.py',
     "            if d['l'] != want:", "            if d['l'] == want:", READER),
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
     "        body = re.compile(r'(?<![\\w-])(%s)(?![\\w-])'",
     "        body = re.compile(r'\\b(%s)\\b'",
     'python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'out = m.stub_pair_note(tempfile.mkdtemp())\n'
     'r = subprocess.run([sys.executable, \'{file}\', \'--note\','
     ' out[\'note\'], \'--draft\', \'run24\', \'--halves\','
     ' \'g912,ghead\'], capture_output=True, text=True)\n'
     'sys.exit(0 if \'dead-spot\' in r.stdout else 1)"'),
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
    ('run-status stops wanting the carrier digest', 'run-status.sh',
     'if grep -q "^ITEM ${it}[^0-9]" "$READINGS" 2>/dev/null; then',
     'if true; then',
     '{file} run98 2>&1 | grep -q "no ITEM 5 block"'),
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
    # The `(bad)` tell dropped: the continuation the sweep decoded out of
    # step counts as a straddling loop again, over the second listing.
    ('survey counts a swallowed jump as a loop again', 'loop-offsets.py',
     "        if any(i[3] == '(bad)' for i in insns[k:n + 1]):\n            continue\n",
     '',
     'PATH="{bin}:$PATH" python3 -c "import importlib.util, sys, tempfile, subprocess\n'
     'spec = importlib.util.spec_from_file_location(\'d\', \'{dir}/defects.py\')\n'
     'm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n'
     'f = m.phantom2_listing(tempfile.mkdtemp())[\'dis\']\n'
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
