import unittest

import pymzavro
import pprint
import pyavroc

from pymzavro.MzAvroConverter import MzConverter


mzMLPath = "tiny.pwiz.1.1.mzML"
avroPath = "tiny.pwiz.1.1.avro"
avroMetaPath = "tiny.pwiz.1.1_meta.avro"

class ConverterTest(unittest.TestCase):


    def test_write(self):
        converter = MzConverter(mzMLPath)
        self.assertEqual(converter.convert(), 1)
        self.assertEqual(self.cvParamTest(), 65)


    def cvParamTest(self):
        avroFile = open(avroPath)
        avroFileMeta = open(avroMetaPath)
        avroReader = pymzavro.reader.PymzAvroReader(avroFile, avroFileMeta)
        cvParamNumber = 0
        timesum = 0
        intensitysum = 0
        for avroSpec in avroReader:
            for cvParam in avroSpec.getMSDict():
                cvParamNumber = cvParamNumber+1
        timesum = timesum + sum(avroSpec.getChromatogram("sic").get("timeArray"))
        timesum = timesum + sum(avroSpec.getChromatogram("tic").get("timeArray"))
        intensitysum = intensitysum + sum(avroSpec.getChromatogram("sic").get("intensityArray"))
        intensitysum = intensitysum + sum(avroSpec.getChromatogram("tic").get("intensityArray"))
        self.assertEqual(timesum, 150)
        self.assertEqual(intensitysum, 175)
        return cvParamNumber

    def test_read(self):
        with open(avroMetaPath) as fp:
            reader = pyavroc.AvroFileReader(fp, types=False)
            for record in reader:
                pass




