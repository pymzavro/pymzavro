__author__ = 'marius'

import os

class MzConverter():
    def __init__(self, mzMLFile, avroFile = None, avroMetaFile = None):
        self.mzMLFile = mzMLFile
        self.avroFile = avroFile
        self.avroMetaFile = avroMetaFile
        self.createmzAvroFiles()

    def createmzAvroFiles(self):
        mzMLPath = os.path.abspath(self.mzMLFile.name)
        if self.avroFile is None:
            self.avroFile = open(mzMLPath.rsplit(".", 1)[0] + ".avro", "wb")

        if self.avroMetaFile is None:
            self.avroFile = open(mzMLPath.rsplit(".", 1)[0] + "_meta.avro", "wb")




