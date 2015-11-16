#!/usr/bin/env python

import json
import sys

isum = 0
ilen = 04

for line in sys.stdin:
    name, count = line.split('\t')
    count = eval(count)
    isum = isum + float(count[0])
    ilen = ilen + float(count[1])
print isum, ilen
