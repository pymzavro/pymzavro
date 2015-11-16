#!/usr/bin/env python

import json
import sys


isum = 0
ilen = 0
specCount = 0

for line in sys.stdin:
	data = json.loads(line)
	iArray = data["intensityArray"]
	isum = isum + sum(iArray)
	ilen = ilen + sum(iArray)
	specCount = specCount + 1
print '%s\t%s' % ("TIC", [isum, ilen])

