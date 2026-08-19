#!/bin/bash
# The pre-filing verification the stretch list carried as goal 3: the
# ISSUE's embedded Repro.hs has never been compiled and run as its
# exact bytes (the comment's program was; the issue's predates the
# padding sessions). Extract the fenced block verbatim from the draft,
# compile on 9.12.4, run the key modes, read the second halves against
# the issue's own table (alone 9.35 / poison 10.36 +10.8% / poisonbig
# 9.24 at -A32m; alone 6.35 / poison 7.12 +12.1% at -A1G).
# Registered lean, judged not remembered: within the issue's own "a few
# percent" run-to-run spread of its table; a mode that fails to
# compile, crashes, or reads a different sign is a filing blocker.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
exec > goal4/a10-issuerepro-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
python3 - <<'EOF'
import re
s = open("/home/mikolaj/r/horde-ad/docs/ghc-issue-small-pinned-churn.md").read()
m = re.findall(r"```haskell\n(.*?)```", s, re.S)
assert len(m) == 1, len(m)
open("goal4/a10-IssueRepro.hs", "w").write(m[0])
print("extracted", len(m[0]), "bytes")
EOF
md5sum goal4/a10-IssueRepro.hs
ghc -O1 -rtsopts -outputdir goal4/a10-objs -o goal4/a10-IssueRepro \
  goal4/a10-IssueRepro.hs || { echo "COMPILE FAILED"; exit 1; }
run() { local name=$1; shift
  ./goal4/a10-IssueRepro "$@" -RTS > goal4/a10-ir-$name.log 2>&1
  echo "== $name: $(grep victim: goal4/a10-ir-$name.log)"
}
run alone-32m     victim +RTS -A32m -I0 -T
run poison-32m    poison victim +RTS -A32m -I0 -T
run poisonbig-32m poisonbig victim +RTS -A32m -I0 -T
run alone-1g      victim +RTS -A1G -I0 -T
run poison-1g     poison victim +RTS -A1G -I0 -T
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A10-ISSUEREPRO
