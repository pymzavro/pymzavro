#!/usr/bin/env python

import json
import sys


isum = 0
ilen = 0
for line in sys.stdin:
	data = json.loads(line)
	iArray = data["intensityArray"]
print '%s\t%s' % ("TIC", [isum, ilen])

