import unittest

import pymzml
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
        self.cvParamTest()

    def cvParamTest(self):
        avroFile = open(avroPath)
        avroFileMeta = open(avroMetaPath)
        avroReader = pymzavro.reader.PymzAvroReader(avroFile, avroFileMeta)
        mzMLReader = pymzml.run.Reader(mzMLPath)

        for avroSpec in avroReader:
            mzMLSpec = mzMLReader.next()
            for cvParam in avroSpec.getMSDict():
                print(cvParam)
            print("__new__")
            break




