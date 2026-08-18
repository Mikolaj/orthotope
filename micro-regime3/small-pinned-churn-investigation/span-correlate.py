#!/usr/bin/env python3
"""Correlate each shape's measured live span against every structural property."""
import re, functools, operator, sys, math
SH = {
 'cnn-L1-6x6-c1':[6,6,1,3,3],'cnn-L1-24x24-c1':[24,24,1,3,3],'cnn-L2-24x24-c32':[24,24,32,3,3],
 'cnn-slice-c32':[32,3,3],'lenet-L1-28-c1-k5':[28,28,1,5,5],'cifar-L2-16-c64-k3':[16,16,64,3,3],
 'vgg-14-c512-k3':[14,14,512,3,3],'alexnet-L1-55-c3-k11':[55,55,3,11,11],
 'alexnet-L2-27-c48-k5':[27,27,48,5,5],'conv1d-24':[24,3,3,24],'gather48-src-50':[50,3,3,50],
 'stretch-rank10':[3]*10,'stretch-rank12':[2]*12,'stretch-square-1341':[1341,1341],
 'stretch-inner1':[1,500000],'stretch-wide-2xM':[2,900000],'stretch-tall-Mx2':[900000,2],
 'stretch-bigstride':[3,3,200000],'stretch-tab7MB':[900,2,1000],'stretch-pow2stride':[54,64,512],
 'stretch-inner256':[7,256,977],'stretch-r5-8x432':[8,8,8,8,432],'stretch-primes':[97,89,29],
 'stretch-coprime-r7':[2,3,5,7,11,13,2]}
AREAS=[('4m',4),('8m',8),('16m',16),('32m',32),('64m',64),('128m',128)]
def props(d):
    l=functools.reduce(operator.mul,d)
    sw=d[:-2]+[d[-1],d[-2]] if len(d)>=2 else list(d)
    sInner=sw[-1]; m=l//sInner if sInner else 0
    return dict(l=l, rank=len(d), sInner=sInner, m=m,
                res_B=8*l, offsets_B=24*m, run_B=8*sInner,
                inner2=(d[-1]*d[-2] if len(d)>=2 else d[-1]),
                sq=int(len(d)>=2 and d[-1]==d[-2]), maxdim=max(d),
                outer=l//(d[-1]*d[-2]) if len(d)>=2 and d[-1]*d[-2] else 1)
def parse(path):
    out={}
    for ln in open(path):
        f=ln.split()
        if len(f)<8 or f[0] not in SH: continue
        vals=[float(x) for x in f[1:7]]
        peak=max(vals); span=None
        for (a,mb),v in zip(AREAS,vals):
            if peak>1e5 and v<1e4: span=mb; break     # collapsed here
        out[f[0]]=(vals,span,peak)
    return out
def spearman(xs,ys):
    def rank(v):
        o=sorted(range(len(v)), key=lambda i:v[i]); r=[0]*len(v)
        for j,i in enumerate(o): r[i]=j
        return r
    rx,ry=rank(xs),rank(ys); n=len(xs)
    if n<3: return float('nan')
    mx,my=sum(rx)/n,sum(ry)/n
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    den=math.sqrt(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))
    return num/den if den else float('nan')
def main(path):
    d=parse(path)
    print('%-24s %9s %12s   %s' % ('shape','span MB','prom@4m','promotes heavily?'))
    for sh,(v,span,peak) in sorted(d.items(), key=lambda kv:-kv[1][2]):
        print('%-24s %9s %12.4g   %s' % (sh, span if span else ('>128' if peak>1e5 else '--'), v[0],
                                          'YES' if peak>1e5 else 'no'))
    heavy=[(sh,span) for sh,(v,span,peak) in d.items() if peak>1e5 and span]
    print('\nshapes with a finite measured span: %d' % len(heavy))
    if len(heavy)>=3:
        print('\nSpearman of span against each structural property:')
        for k in ('l','rank','sInner','m','res_B','offsets_B','run_B','inner2','maxdim','outer'):
            xs=[props(SH[sh])[k] for sh,_ in heavy]; ys=[sp for _,sp in heavy]
            print('   %-12s rho = %+.3f' % (k, spearman(xs,ys)))
        print('\nexact ratios span/property, looking for a constant:')
        for k in ('res_B','offsets_B'):
            print('   %s:' % k, ['%s=%.2f' % (sh, sp*1e6/props(SH[sh])[k]) for sh,sp in heavy])
if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else '/tmp/spansweep.out')
