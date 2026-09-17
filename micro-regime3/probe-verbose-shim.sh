#!/bin/sh
# Probe shim for Run 35's preparation: the basis recipe's assembler pass with
# ALIGN_AS_VERBOSE=1, whose per-module `verified:` line counts the exit spans
# the planner left astride. cabal shows no shim stderr, so it is appended to
# probe-verbose-run35.err here. This script is kept with the tree as the
# reproducer for that reading; the .err log goes with the run's artifacts.
D=$(dirname "$0")
ALIGN_AS_VERBOSE=1 exec "$D/align-as.py" "$@" 2>>"$D/probe-verbose-run35.err"
