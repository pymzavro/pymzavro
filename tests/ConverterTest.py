import unittest

import pymzavro
from pymzavro.MzAvroConverter import MzConverter


mzMLPath = "tiny.pwiz.1.1.mzML"
avroPath = "tiny.pwiz.1.1.avro"
avroMetaPath = "tiny.pwiz.1.1_meta.avro"

class ConverterTest(unittest.TestCase):
    def test_write(self):
        converter = MzConverter(mzMLPath)
        self.assertEqual(converter.convert(), 1)

    def test_read(self):
        self.assertEqual(self.cvParamTest(), 65)

    def cvParamTest(self):
        avroFile = open(avroPath)
        avroFileMeta = open(avroMetaPath)
        avroReader = pymzavro.reader.PymzAvroReader(avroFile, avroFileMeta)
        cvParamNumber = 0
        for avroSpec in avroReader:
            for cvParam in avroSpec.getMSDict():
                cvParamNumber = cvParamNumber+1

        return cvParamNumber




