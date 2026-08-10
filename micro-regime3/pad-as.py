#!/usr/bin/env python3
"""A null stand-in assembler: adds padding and aligns nothing.

`align-as.py` grows a module's text, which moves every library linked after
it, so an aligned build and a plain one differ in the libraries' cache-line
offsets as well as in the alignment being measured -- 856 of 867 library
symbols carrying a short loop moved between the first such pair built here.
This makes the unaligned half of that pair the same size and, more to the
point, the same *phase*, so the two differ in Main's loop alignment and in
nothing else that an offset can see.

    PAD_BYTES=N cabal build micro \\
      --ghc-options="-pgma /path/to/pad-as.py -fforce-recomp"

`make-pair.py` does all of this and verifies the result; what follows is what
it automates, kept because the two steps are the reason the number is not a
constant. N is measured per pair of builds, because it depends on how much
padding the aligning shim happened to insert:

  1. Build both halves, the aligned one with `align-as.py` and the other with
     this at `PAD_BYTES` equal to the aligned build's `.text` growth
     (`size -A`). That equalises the size.
  2. Read the commonest address delta between the two binaries' library loops
     -- `loop-offsets.py` and a counter over `A[sym] - X[sym]` does it -- and
     add `delta mod 64` to `PAD_BYTES`. Rebuild. The delta becomes a whole
     number of lines and the offsets match.

Measured 2026-08-10 on `Main.hs` at 2b41e53: the growth is 12288, which left
a delta of 416 and 3% of library loops in phase; 12288 + 32 = 12320 left a
delta of 384, six whole lines, and **95% of them in phase, 98% with the same
straddle state**. Step 2 is what does the work: matching the size alone is
not enough and is the version to skip, since 416 is congruent to 32 mod 64,
which is the worst offset a shift can have.

The padding goes at the end of the module's text, so the module's own code
keeps every offset it had: the pair built this way reads the same fills at
[3, 53, 59, 45] and [16, 0, 36, 36] as the unpadded build did, and the same
115 short loops with 50 straddling.

  PAD_BYTES   bytes of padding to add, default 0, which makes this a no-op
  REAL_AS     the real assembler, default /usr/bin/gcc
"""
import os
import subprocess
import sys

REAL = os.environ.get('REAL_AS', '/usr/bin/gcc')
PAD = int(os.environ.get('PAD_BYTES', '0'))

for a in sys.argv[1:]:
    if a.endswith('.s') and os.path.exists(a) and PAD:
        with open(a, 'a') as f:
            f.write(f'\n\t.section .text\n\t.p2align 3\n\t.space {PAD}, 0x90\n')
        PAD = 0        # one module's worth per invocation, not one per file

sys.exit(subprocess.call([REAL] + sys.argv[1:]))
