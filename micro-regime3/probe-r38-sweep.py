#!/usr/bin/env python3
"""Sweep Run 38's run loop over every residue of a cache line, and over
the lines of a page at a fixed residue: probe-entries-sweep.py's `fill`
kernel with the bytes the Run 38 halves emit for `fillStage2Axes` (and
`fillStage2`, which emits the same loop) in place of Run 32's, read
off `objdump` of run38-gheadnospec at 0x44cf84, instruction for
instruction and register for register, so that every encoding is the
binary's own -- the source-base reload at the head is gone and the
base sits in %r8, which is the one instruction Run 38's count lost
against Run 37's.

    ./probe-r38-sweep.py                     # 64 residues, ~2 min
    ./probe-r38-sweep.py --only 0 4 9        # a few residues
    ./probe-r38-sweep.py --only 4 --lines 0 1 2 5 62   # residue 4 at
                                             # these lines of a page

`--lines` puts the head's line at that index within a 4 KiB page, the
kernel being page-aligned and then skipped by that many lines, which is
what separates the two Run 38 halves' copies of this loop: same bytes,
same residue 4, line 62 of its page in the basis and line 5 in the
control. Three counters a run, differenced over two iteration counts
so the process's startup cancels: cycles, op-cache fetches (raw 0x28F)
and cycles with the op queue empty (raw 0xA9). A probe, run by hand;
writes only under a temporary directory. 2026-09-22. Exit 2 when gcc,
perf, objdump or nm is missing or perf stops answering, 1 when a build
fails, 0 otherwise.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def die(msg):
    """Exit 2 -- did not run -- rather than `sys.exit(str)`'s 1, which is
    the code a finding gets (2026-09-25, by review)."""
    sys.stderr.write(msg.rstrip('\n') + '\n')
    sys.exit(2)


RUNS = 900000
FILL = r'''
    .text
    .globl kern
    .type kern,@function
kern:
    push %rbx; push %r12; push %r13; push %r14; push %r15
    sub $0x48,%rsp
    mov %rcx,%rax
    mov %r8,%r9
    mov %rdi,%rcx
    mov %rsi,%r8
    mov %rdx,%r10
    mov $2,%rdx
    xor %edi,%edi
    xor %r11d,%r11d
    xor %esi,%esi
    mov $2,%rbx
    jmp L2
    .p2align 12
    .skip LINES*64, 0x90
    .p2align 6
    .skip K, 0x90
head:
    movsd (%r8,%r11,8),%xmm0
    movsd %xmm0,(%rcx,%rsi,8)
    add %rax,%r11
    movsd (%r8,%r11,8),%xmm0
    lea 1(%rsi),%r14
    movsd %xmm0,(%rcx,%r14,8)
    add %rax,%r11
    add $2,%rsi
L2: lea 1(%rsi),%r14
    cmp %rbx,%r14
    jl head
    cmp %rbx,%rsi
    jge L3
    movsd (%r8,%r11,8),%xmm0
    movsd %xmm0,(%rcx,%rsi,8)
L3: add %r9,%rdi
    dec %r10
    mov %rbx,%rsi
    test %r10,%r10
    jle done
    mov %rsi,%rbx
    add %rdx,%rbx
    mov %rdi,%r11
    jmp L2
done:
    add $0x48,%rsp
    pop %r15; pop %r14; pop %r13; pop %r12; pop %rbx
    ret
    .section .note.GNU-stack,"",@progbits
'''
FILL_MAIN = r'''
#include <stdlib.h>
#include <stdio.h>
extern void kern(double *out, double *v, long n, long stride, long st);
int main(int argc, char **argv) {
  long reps = atol(argv[1]), n = %d;
  double *out = malloc(2 * n * sizeof(double));
  double *v = malloc(2 * n * sizeof(double));
  for (long i = 0; i < 2 * n; i++) v[i] = i;
  for (long r = 0; r < reps; r++) kern(out, v, n, n, 1);
  printf("%%f\n", out[3]);
  return 0;
}
''' % RUNS
EVENTS = 'cycles:u,r20000078f:u,r0a9:u'


def build(tmp, k, lines):
    s, c, b = (os.path.join(tmp, f) for f in ('k.S', 'main.c', 'k%d_%d' % (k, lines)))
    with open(s, 'w') as f:
        f.write(FILL)
    with open(c, 'w') as f:
        f.write(FILL_MAIN)
    # -no-pie: gcc's default here is PIE, under which every process runs
    # the loop at a random page. Linked fixed, a row is one address; what
    # a fragile residue still shows between processes of one binary, 5.5
    # to 7.1 cycles a run at residue 4 over eight of them, ASLR on or off
    # (2026-09-22), is therefore not the address's.
    got = subprocess.run(['gcc', '-O1', '-no-pie', '-DK=%d' % k,
                          '-DLINES=%d' % lines, c, s, '-o', b],
                         capture_output=True, text=True)
    if got.returncode:
        print('probe-r38-sweep: gcc failed at K=%d LINES=%d: %s'
              % (k, lines, got.stderr.strip().split('\n')[-1]), file=sys.stderr)
        return None
    return b


def counts(binary, arg):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        out = f.name
    ran = subprocess.run(['perf', 'stat', '-x,', '-e', EVENTS, '-o', out,
                          binary, str(arg)], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    if ran.returncode:
        os.unlink(out)
        return None
    vals = []
    with open(out) as f:
        for line in f:
            p = line.split(',')
            if len(p) > 3 and p[0].strip().isdigit():
                vals.append(int(p[0]))
    os.unlink(out)
    return vals if len(vals) == 3 else None


def head_address(binary):
    got = subprocess.run(['nm', binary], capture_output=True, text=True,
                         check=True)
    for line in got.stdout.split('\n'):
        p = line.split()
        if len(p) == 3 and p[2] == 'head':
            return int(p[0], 16)
    return -1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--only', type=int, nargs='+', metavar='K',
                    help='these head residues only (default all 64)')
    ap.add_argument('--lines', type=int, nargs='+', metavar='N', default=[0],
                    help='line of the page the head sits in (default 0)')
    ap.add_argument('--pairs', type=int, default=2,
                    help='differenced pairs per cell, the least taken')
    args = ap.parse_args()
    for tool in ('gcc', 'perf', 'objdump', 'nm'):
        if shutil.which(tool) is None:
            die('probe-r38-sweep: %s is not on PATH; nothing ran' % tool)
    if counts('/bin/true', '') is None:
        die('probe-r38-sweep: perf does not count %s here; nothing ran'
            % EVENTS)
    ks = args.only or list(range(64))
    tmp = tempfile.mkdtemp(prefix='r38-sweep-')
    print(' K line   head      cycles/run  fetches/run  queue-empty/run')
    try:
        for lines in args.lines:
            for k in ks:
                b = build(tmp, k, lines)
                if b is None:
                    return 1
                readings = []
                for _ in range(args.pairs):
                    hi, lo = counts(b, 200), counts(b, 100)
                    if hi is None or lo is None:
                        die('probe-r38-sweep: perf stopped counting at'
                            ' K=%d; the rows above stand' % k)
                    readings.append(tuple((h - l) / 100 / RUNS
                                          for h, l in zip(hi, lo)))
                cyc = min(r[0] for r in readings)
                opc = min(r[1] for r in readings)
                emp = min(r[2] for r in readings)
                print('%2d %4d  %#x  %10.2f  %11.2f  %15.2f'
                      % (k, lines, head_address(b), cyc, opc, emp), flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
