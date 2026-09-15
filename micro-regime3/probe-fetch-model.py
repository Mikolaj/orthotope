#!/usr/bin/env python3
"""Score the Zen 3 guide's front-end rules against measured cycles, offset by
offset, on generated loops: the experiments README's placement section
registers, run as one probe.

A kernel is generated from a description, its head swept over the 64
residues of a line with `.p2align 6; .skip K`, and per residue four
counters are read per iteration, differenced over two iteration counts:
cycles, op-cache fetch blocks (0x28F), L1 BTB overrides (0x8A) and L2 BTB
overrides (0x8B). From the assembled layout, read off objdump, the probe
predicts each residue's cost under three rules from section 2.8 of the
Zen 3 optimization guide (README, the placement section):

  blocks   one aligned 64-byte fetch block a cycle: a segment of the
           executed path is cut at every line boundary, each piece a block
  lone     a block holding nothing but a conditional branch, alone or
           with its fused flag writer, pays a cycle; one holding only an
           unconditional jmp does not. Read off the fill's jge at 9..13
           against its tail's jmp at 33..42, and a candidate for the
           guide's rule that two branches share a BTB entry only when
           their last bytes share a line
  short    a segment whose first instruction straddles the line leaves an
           empty fetch block behind, the guide's shortened block from
           branching to a line's end, and pays a cycle

and a fourth, the dispatcher's six ops a cycle, as a floor. Predicted
cycles are max(ops / 6, sum over blocks of 1 + penalties), rounded, and
a residue is a MISS where the rounded measurement disagrees. The verdict
of a sweep is how many residues miss and which rule the misses implicate,
which is what the model needs before the shim can carry a cost built on
it.

Kernels:
  straight N W END   N register ops of width W bytes (3 or 6), one loop,
                     ending END: `fused` (dec; jnz), `split` (dec; op; jnz)
                     or `jmp` (jz out early, jmp back), 20M iterations
  fill R             fillStage2's per-run cycle as Run 32 laid it out,
                     runs of R elements (2, 4, 8, ...), 1.8M elements

    ./probe-fetch-model.py straight 12 3 fused | tee probe-fetch-model-s12.txt
    ./probe-fetch-model.py fill 2 --only 5 9 22 32 60
    ./probe-fetch-model.py rescore probe-fetch-model-s12.txt   # rules only

A saved table carries the kernel and its assembled layout, so `rescore`
re-applies the rules as they stand in this file to the measurements
without the machine, which is how a rule is changed and judged.

Needs gcc, objdump and a perf that counts user cycles; exit 2 when one is
missing, 1 when a build fails. Writes only under a temporary directory.
Written 2026-09-15; the rules are the guide's sentences and the scoring
is the probe's own, so a rule that scores is evidence and one that does
not is a rule the sweep refutes on this core.
"""
import argparse
import collections
import os
import re
import shutil
import subprocess
import sys
import tempfile

EVENTS = 'cycles:u,r20000078f:u,r08a:u,r08b:u'
NAMES = ['cyc', 'blocks', 'l1btb', 'l2btb']
REGS = ['%rcx', '%rdx', '%rsi', '%r8', '%r9', '%r10', '%r11', '%r12',
        '%r13', '%r14', '%r15', '%rbx']
REGS32 = ['%ecx', '%edx', '%esi', '%r8d', '%r9d', '%r10d', '%r11d', '%r12d',
          '%r13d', '%r14d', '%r15d', '%ebx']
ELEMS = 1800000
DEBUG = os.environ.get('FETCH_MODEL_DEBUG', '') not in ('', '0')
FUSABLE = {'cmp', 'test', 'add', 'sub', 'and', 'or', 'xor', 'inc', 'dec'}

PROLOGUE = '''
    .text
    .globl kern
    .type kern,@function
kern:
    push %rbx; push %r12; push %r13; push %r14; push %r15
'''
EPILOGUE = '''
    pop %r15; pop %r14; pop %r13; pop %r12; pop %rbx
    ret
    .section .note.GNU-stack,"",@progbits
'''


def straight(n, width, end):
    if width == 3:
        ops = ['    mov %%rax,%s' % REGS[i % len(REGS)] for i in range(n)]
    else:
        ops = ['    and $0x7fffffff,%s' % REGS32[i % len(REGS32)]
               for i in range(n)]
    body = '\n'.join(ops)
    if end == 'fused':
        tail = '    dec %edi\n    jnz head'
        pre = ''
    elif end == 'split':
        tail = '    dec %edi\n    mov %rax,%rcx\n    jnz head'
        pre = ''
    else:
        pre = '    dec %edi\n    jz out\n'
        tail = '    jmp head'
    return (PROLOGUE + '    .p2align 6\n    .skip K, 0x90\nhead:\n' + pre
            + body + '\n' + tail + '\nout:' + EPILOGUE)


FILL = '''
    sub $0x48,%rsp
    mov %rsi,0x40(%rsp)
    mov %rcx,%r9
    mov %rdi,%rcx
    mov %rdx,%r10
    mov $R,%rdx
    xor %edi,%edi
    xor %ebx,%ebx
    xor %esi,%esi
    mov $R,%rax
    jmp L2
    .p2align 6
    .skip K, 0x90
head:
    mov 0x40(%rsp),%r11
    movsd (%r11,%rbx,8),%xmm0
    movsd %xmm0,(%rcx,%rsi,8)
    add %r9,%rbx
    movsd (%r11,%rbx,8),%xmm0
    lea 1(%rsi),%r14
    movsd %xmm0,(%rcx,%r14,8)
    add %r9,%rbx
    add $2,%rsi
L2: lea 1(%rsi),%r11
    cmp %rax,%r11
    jl head
    cmp %rax,%rsi
    jge L3
    mov 0x40(%rsp),%r11
    movsd (%r11,%rbx,8),%xmm0
    movsd %xmm0,(%rcx,%rsi,8)
L3: add %r8,%rdi
    dec %r10
    mov %rax,%rsi
    test %r10,%r10
    jle done
    mov %rsi,%rax
    add %rdx,%rax
    mov %rdi,%rbx
    jmp L2
done:
    add $0x48,%rsp
'''
FILL_MAIN = '''
#include <stdlib.h>
#include <stdio.h>
extern void kern(double *out, double *v, long n, long stride, long st);
int main(int argc, char **argv) {
  long reps = atol(argv[1]), n = %d, r = %d;   /* n runs of r elements */
  double *out = malloc(r * n * sizeof(double));
  double *v = malloc(r * n * sizeof(double));
  for (long i = 0; i < r * n; i++) v[i] = i;
  for (long r = 0; r < reps; r++) kern(out, v, n, n, 1);
  printf("%%f\\n", out[3]);
  return 0;
}
'''
STRAIGHT_MAIN = 'extern void kern(long);\nint main(void){kern(20000000);return 0;}\n'


def build(tmp, asm, cmain, k):
    s, c, b = (os.path.join(tmp, f) for f in ('k.S', 'main.c', 'k%d' % k))
    with open(s, 'w') as f:
        f.write(asm)
    with open(c, 'w') as f:
        f.write(cmain)
    got = subprocess.run(['gcc', '-O1', '-DK=%d' % k, c, s, '-o', b],
                         capture_output=True, text=True)
    if got.returncode:
        print('probe-fetch-model: gcc failed at K=%d: %s'
              % (k, got.stderr.strip().split('\n')[-1]), file=sys.stderr)
        return None
    return b


def counts(binary, arg):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        out = f.name
    subprocess.run(['perf', 'stat', '-x,', '-e', EVENTS, '-o', out, binary,
                    str(arg)], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    vals = []
    with open(out) as f:
        for line in f:
            p = line.split(',')
            if len(p) > 3 and p[0].strip().isdigit():
                vals.append(int(p[0]))
    os.unlink(out)
    return vals if len(vals) == len(NAMES) else None


def layout(binary):
    """[(abs address, length, mnemonic, label-or-None)] from head to ret."""
    out = subprocess.run(['objdump', '-d', binary], capture_output=True,
                         text=True).stdout
    sec = out[out.index('<head>:'):]
    sec = sec[:sec.index('\tret')]
    rows, label = [], 'head'
    for line in sec.split('\n'):
        m = re.match(r'^[0-9a-f]+ <(\w+)>:', line)
        if m:
            label = m.group(1)
            continue
        m = re.match(r'^\s*([0-9a-f]+):\t([0-9a-f ]+?)\t(\S+)', line)
        if not m:
            continue
        rows.append((int(m.group(1), 16), len(m.group(2).split()),
                     m.group(3), label))
        label = None
    return rows


def path_straight(rows, end):
    """The executed path as segments, each a list of instruction indices
    ending in a taken branch: head through the backward jump, the
    epilogue after `out` excluded; under `jmp` the jz is not taken."""
    out = next(i for i, row in enumerate(rows) if row[3] == 'out')
    return [list(range(out))]


def path_fill(rows, r):
    lab = {row[3]: i for i, row in enumerate(rows) if row[3]}
    head, l2, l3 = lab['head'], lab['L2'], lab['L3']
    jl = next(i for i in range(l2, len(rows)) if rows[i][2] == 'jl')
    jge = next(i for i in range(jl, len(rows)) if rows[i][2] == 'jge')
    jmp = next(i for i in range(l3, len(rows)) if rows[i][2] == 'jmp')
    entry = list(range(l2, jl + 1))                    # lea; cmp; jl taken
    body_taken = list(range(head, jl + 1))             # ... jl taken
    body_exit = list(range(head, jge + 1))             # jl not taken; jge taken
    tail = list(range(l3, jmp + 1))
    return [entry] + [body_taken] * (r // 2 - 1) + [body_exit, tail]


def predict(rows, segs, k, head_addr):
    """-> (ops, blocks, split, short, predicted cycles) for head offset k."""
    ops = 0
    blocks = split = short = 0
    for seg in segs:
        # ops: instructions less fused pairs inside the segment
        n = len(seg)
        for a, b in zip(seg, seg[1:]):
            if rows[a][2] in FUSABLE and rows[b][2].startswith('j'):
                n -= 1
        ops += n
        # cut into blocks by the line each instruction ENDS in
        pieces = collections.OrderedDict()
        for i in seg:
            off = rows[i][0] - head_addr + k
            end_line = (off + rows[i][1] - 1) // 64
            pieces.setdefault(end_line, []).append(i)
        # a block that holds nothing but a conditional branch, alone or
        # with the flag writer it fuses with, pays a cycle: the fill's jge
        # at 9..13 and the straight loop's jnz at 25..28. A block holding
        # only an unconditional jmp does not: the fill's tail at 33..42.
        for ins in pieces.values():
            blocks += 1
            mn = [rows[i][2] for i in ins]
            if mn[-1].startswith('j') and mn[-1] != 'jmp' and (
                    len(mn) == 1 or (len(mn) == 2 and mn[0] in FUSABLE)):
                split += 1
        # a segment entered in a line's last bytes, its first instruction
        # ending in the next line: the predictor's block for the entry
        # line holds no whole instruction, a shortened fetch block that is
        # a block and a short one, and no piece above stands for it
        j = seg[0]
        first_off = rows[j][0] - head_addr + k
        if first_off // 64 != (first_off + rows[j][1] - 1) // 64:
            blocks += 1
            short += 1
        if DEBUG:
            print('#   K=%d seg: ' % k + ' | '.join(
                'L%d:%s' % (line, ','.join(rows[i][2] for i in ins))
                for line, ins in pieces.items()), file=sys.stderr)
    pred = max(ops / 6.0, blocks + split + short)
    return ops, blocks, split, short, pred


def rescore(path):
    """Re-apply the rules to a saved table: the layout line rebuilds the
    rows, the kernel line the path, and every K row is scored again, so a
    rule can be changed and judged without the machine."""
    rows, kernel, args, meas = [], None, [], []
    for line in open(path):
        if line.startswith('# kernel:'):
            p = line.split()[2:]
            kernel, args = p[0], p[1:]
        elif line.startswith('# layout:'):
            for tok in line.split()[2:]:
                lab = None
                if ':' in tok:
                    lab, tok = tok.split(':', 1)
                mn, rest = tok.rsplit('+', 1)
                off, ln = rest.split('/')
                rows.append((int(off), int(ln), mn, lab))
        elif line[:1].isdigit() or line[:2].strip().isdigit():
            f = line.split()
            if len(f) >= 5 and f[0].isdigit():
                meas.append((int(f[0]), float(f[1]), float(f[2]),
                             float(f[3]), float(f[4])))
    if not rows or not meas:
        sys.exit('probe-fetch-model: %s carries no layout or no rows' % path)
    if kernel == 'fill':
        segs = path_fill(rows, int(args[0]) if args else 2)
    else:
        segs = path_straight(rows, args[2])
    miss = []
    print('# rescored %s: %s %s' % (path, kernel, ' '.join(args)))
    for k, cyc, blk, l1, l2 in meas:
        ops, blocks, split, short, pred = predict(rows, segs, k, 0)
        ok = round(cyc) == round(pred)
        if not ok:
            miss.append(k)
        print('%2d %6.2f %6.2f %6.2f %6.2f | %4d %6d %5d %5d %6.2f %s'
              % (k, cyc, blk, l1, l2, ops, blocks, split, short, pred,
                 'ok' if ok else 'MISS'))
    print('# %d of %d residues miss%s' % (len(miss), len(meas),
          ': ' + ' '.join(map(str, miss)) if miss else ''))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('kernel', choices=['straight', 'fill', 'rescore'])
    ap.add_argument('args', nargs='*')
    ap.add_argument('--only', type=int, nargs='+', metavar='K')
    ap.add_argument('--pairs', type=int, default=2)
    a = ap.parse_args()
    if a.kernel == 'rescore':
        return rescore(a.args[0])
    for tool in ('gcc', 'perf', 'objdump'):
        if shutil.which(tool) is None:
            sys.exit('probe-fetch-model: %s is not on PATH; nothing ran' % tool)
    if counts('/bin/true', '') is None:
        sys.exit('probe-fetch-model: perf does not count %s here; nothing ran'
                 % EVENTS)
    if a.kernel == 'straight':
        n, w, end = int(a.args[0]), int(a.args[1]), a.args[2]
        asm, cmain, per, iters = straight(n, w, end), STRAIGHT_MAIN, 20000000, (2, 1)
        title = 'straight N=%d W=%d %s' % (n, w, end)
    else:
        r = int(a.args[0]) if a.args else 2
        asm = PROLOGUE + FILL.replace('$R', '$%d' % r) + EPILOGUE
        cmain, per, iters = FILL_MAIN % (ELEMS // r, r), ELEMS // r, (200, 100)
        title = 'fill R=%d' % r
    ks = a.only or list(range(64))
    tmp = tempfile.mkdtemp(prefix='fetch-model-')
    print('# %s; per iteration: measured cycles, fetch blocks, L1 and L2 BTB'
          ' overrides; predicted ops, blocks, lone, short, cycles' % title)
    print('%2s %6s %6s %6s %6s | %4s %6s %5s %5s %6s %s'
          % ('K', 'cyc', 'blk', 'l1', 'l2', 'ops', 'blocks', 'lone',
             'short', 'pred', 'verdict'))
    miss = []
    try:
        for k in ks:
            b = build(tmp, asm, cmain, k)
            if b is None:
                return 1
            reads = []
            for _ in range(a.pairs):
                hi, lo = counts(b, iters[0]), counts(b, iters[1])
                if hi is None or lo is None:
                    sys.exit('probe-fetch-model: perf stopped counting at K=%d' % k)
                if a.kernel == 'fill':
                    reads.append(tuple((h - l) / 100 / per for h, l in zip(hi, lo)))
                else:
                    reads.append(tuple(h / per for h in hi))
            m = [min(r[i] for r in reads) for i in range(len(NAMES))]
            rows = layout(b)
            head_addr = rows[0][0]
            if k == ks[0]:
                print('# kernel: %s %s' % (a.kernel, ' '.join(a.args)))
                print('# layout: ' + ' '.join('%s%s+%d/%d' % (
                    (row[3] + ':') if row[3] else '', row[2],
                    row[0] - head_addr, row[1]) for row in rows))
            if a.kernel == 'fill':
                segs = path_fill(rows, r)
            else:
                segs = path_straight(rows, end)
            ops, blocks, split, short, pred = predict(rows, segs, k, head_addr)
            ok = round(m[0]) == round(pred)
            if not ok:
                miss.append(k)
            print('%2d %6.2f %6.2f %6.2f %6.2f | %4d %6d %5d %5d %6.2f %s'
                  % (k, m[0], m[1], m[2], m[3], ops, blocks, split, short,
                     pred, 'ok' if ok else 'MISS'), flush=True)
        print('# %s: %d of %d residues miss%s'
              % (title, len(miss), len(ks),
                 ': ' + ' '.join(map(str, miss)) if miss else ''))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
