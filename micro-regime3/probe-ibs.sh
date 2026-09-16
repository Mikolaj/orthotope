#!/usr/bin/env bash
# IBS over one cell on two instances of one binary, 2026-09-16: AMD's
# precise sampler, driven by `perf mem`, tags a load or store with its
# own instruction, data address, latency and data source, which is the
# attribution the counters could not give for the frame term README's
# placement section prices. Records the ORIGINAL and a COPY on the same
# cell and prints, for the instructions of a window of code, the sample
# count, the mean latency and the data-source mix, side by side.
#
# The IBS PMU lives under /sys, which the session wrapper hides, so this
# runs from a plain terminal; if `perf mem record` refuses, prefix it
# with sudo. A probe and never a check: exits 0 whatever it finds.
#
#     bash probe-ibs.sh ./run33-gheadexit /tmp/g \
#       'compose-rev-bcast/mut-odo-vecdims-add-in-leaf-u1' 0x455000 0x455080
#
# The last two are the code window, here the leaf's executing loop and
# its outer loop on HEAD's half; the copy at /tmp/g is the one probe-
# pageflags.py read fast, at the same virtual addresses.
set -u
cd "$(dirname "$0")" || exit 1
# Where the recordings go, per user: root under sudo cannot open a file
# another user left in /tmp (fs.protected_regular), and the stale .err
# then reads as this run's failure. A session sets its own.
export IBS_DIR=${IBS_DIR:-/tmp/ibs-$(id -u)}
mkdir -p "$IBS_DIR" || exit 0
ORIG=${1:?original binary}
COPY=${2:?byte-identical copy}
CELL=${3:?shape/arm}
LO=${4:?window start, hex}
HI=${5:?window end, hex}
for b in "$ORIG" "$COPY"; do
  tag=$(basename "$b")
  echo "== recording $tag"
  # -a: IBS here refuses per-thread mode, so the whole box is sampled
  # (root) and the aggregator keeps the benchmark's own samples by its
  # command name and drops the kernel's by the window; no -U, IBS taking
  # no exclusion modifier; -c 10000: a sample every ten thousand cycles,
  # forty-odd thousand over this cell where the default gave five hundred
  perf mem record -a -c 10000 -o "$IBS_DIR/ibs-$tag.data" -- "$b" classes -m glob "$CELL" -n 1500 > /dev/null 2> "$IBS_DIR/ibs-$tag.err" \
    || { echo "perf mem record failed for $tag:"; cat "$IBS_DIR/ibs-$tag.err"; exit 0; }
  perf script -i "$IBS_DIR/ibs-$tag.data" -F comm,ip,addr,weight,data_src 2> /dev/null > "$IBS_DIR/ibs-$tag.txt"
  echo "   $(wc -l < "$IBS_DIR/ibs-$tag.txt") samples"
done
python3 - "$ORIG" "$COPY" "$LO" "$HI" <<'EOF'
import collections, os, re, sys
orig, copy, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3], 16), int(sys.argv[4], 16)
# perf script prints, whatever order -F names them: the command name, the
# data address, the data source as hex, its decoding between bars, the
# weight, the ip. The command name is what keeps the benchmark's samples
# out of a system-wide recording.
LINE = re.compile(r'^\s*(\S+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+\|(.*\S)\s+(\d+)\s+([0-9a-f]+)\s*$')

def read(tag):
    per = collections.defaultdict(lambda: [0, 0.0, collections.Counter()])
    total = 0
    with open(os.path.join(os.environ.get('IBS_DIR', '/tmp'), f'ibs-{tag}.txt')) as f:
        for line in f:
            m = LINE.match(line)
            if not m or m.group(1) != tag[:15]:    # the kernel truncates comm
                continue
            addr, src, decoded, w, ip = (int(m.group(2), 16), m.group(3), m.group(4),
                                         float(m.group(5)), int(m.group(6), 16))
            total += 1
            if not (lo <= ip < hi):
                continue
            fields = dict(f.strip().split(' ', 1) for f in decoded.split('|') if ' ' in f.strip())
            key = ' '.join(f'{k} {fields[k].strip()}' for k in ('OP', 'LVL', 'TLB') if k in fields)
            r = per[ip]
            r[0] += 1; r[1] += w; r[2][key] += 1
    return total, per

a, b = read(os.path.basename(orig)), read(os.path.basename(copy))
print(f'\nwindow {lo:#x}-{hi:#x}: samples in it {sum(r[0] for r in a[1].values())} of {a[0]} on the original,'
      f' {sum(r[0] for r in b[1].values())} of {b[0]} on the copy')
print(f'{"ip":>10} {"n orig":>7} {"lat orig":>9} {"n copy":>7} {"lat copy":>9}  data source, original | copy')
for ip in sorted(set(a[1]) | set(b[1])):
    ra, rb = a[1].get(ip, [0, 0.0, collections.Counter()]), b[1].get(ip, [0, 0.0, collections.Counter()])
    la = ra[1] / ra[0] if ra[0] else float('nan')
    lb = rb[1] / rb[0] if rb[0] else float('nan')
    sa = ', '.join(f'{k} {v}' for k, v in ra[2].most_common(3))
    sb = ', '.join(f'{k} {v}' for k, v in rb[2].most_common(3))
    print(f'{ip:#10x} {ra[0]:7d} {la:9.1f} {rb[0]:7d} {lb:9.1f}  {sa} | {sb}')
print('\nlatency is perf\'s `weight`, cycles from issue to completion of the sampled op; a store'
      ' carries none on many kernels and prints 0.0. Where the original\'s latency sits above the'
      ' copy\'s on one instruction, that instruction and its data source are the collision.')
EOF
