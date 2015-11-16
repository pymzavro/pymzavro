#!/usr/bin/env python

import pymzml
import pymzml.minimum
import pymzml.obo

import sys
import xml.etree.ElementTree as ET

noiseThreshold = 0.0
MS1_Precision = 5e-6
MSn_Precision = 20e-6

param = dict()
OT = pymzml.obo.oboTranslator( )
param['MS1_Precision'] = MS1_Precision
param['MSn_Precision'] = MSn_Precision
param['accessions'] = { }

for minimumMS, ListOfvaluesToExtract in pymzml.minimum.MIN_REQ:
    param['accessions'][minimumMS] = {
                                                    'valuesToExtract'   : ListOfvaluesToExtract ,
                                                    'name'              : OT[minimumMS] ,
                                                    'values'            : []
            }
MS_spec = pymzml.spec.Spectrum(measuredPrecision = MS1_Precision, param = param)

specXML = ""
ilen = 0
i = 0
speclen = 0



for line in sys.stdin:
    specXML = specXML + line.strip()
    if "/spectrum" in line:
        specTree = ET.fromstring(specXML)
        MS_spec.initFromTreeObject(specTree)
        iArray = list(MS_spec.i)
        MS_spec.clear()
        specXML = ""
print '%s\t%s' % ("A", "1")



