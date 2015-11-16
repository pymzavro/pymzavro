#!/usr/bin/env python

import sys

isum = 0.0
ilen = 0.0

for line in sys.stdin:
    count, XML = line.split("\t")
    XML = eval(XML)
    isum = isum + float(XML[0])
    ilen = ilen + float(XML[1])
print(isum, ilen)
