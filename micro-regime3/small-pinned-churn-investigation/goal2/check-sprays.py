#!/usr/bin/env python3
"""The saturation assertion for the criterion pair cells (findings2, the
session header's 620k-917k claim): for each pair-cell criterion JSON
given (or every pois-*/vpois-*/AL-pois-* JSON in this directory when run
bare), sum the poison bench's iters over its reportMeasured and flag any
dose under 3e5 sprays as LOW.  The poison bench is cnn-slice-c32/list."""
import glob
import json
import os
import sys

paths = sys.argv[1:]
if not paths:
    here = os.path.dirname(os.path.abspath(__file__))
    for pat in ('pois-*.json', 'vpois-*.json', 'AL-pois-*.json'):
        paths += sorted(glob.glob(os.path.join(here, pat)))
for p in paths:
    try:
        data = json.load(open(p))
        reports = [el for el in data if isinstance(el, dict)
                   and 'reportName' in el]
        for el in data:
            if isinstance(el, list) and el and isinstance(el[0], dict) \
               and 'reportName' in el[0]:
                reports = el
                break
        pois = [r for r in reports
                if r['reportName'] == 'cnn-slice-c32/list']
        if not pois:
            print(f"{p}: NO cnn-slice-c32/list REPORT")
            continue
        ii = pois[0]['reportKeys'].index('iters')
        sprays = sum(m[ii] for m in pois[0]['reportMeasured'])
        flag = 'ok' if sprays >= 3e5 else 'LOW'
        print(f"{os.path.basename(p)}: sprays {sprays:>10.0f} {flag}")
    except Exception as e:
        print(f"{p}: ERROR {e}")
