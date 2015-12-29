import os
import shutil
from pymzavro.reader import PymzAvroReader
from pymzavro.MzAvroConverter import MzConverter

def convert():
    mzMLPath = "BSA3.mzML"
    converter = MzConverter(mzMLPath)
    converter.convert()


def readAvro():
    spectrumFile = open("BSA3.avro")
    metaFile = open("BSA3_meta.avro")
    run = PymzAvroReader(spectrumFile, metaFile)
    for spec in run:
        spec.getmzArray()
        spec.getIntensityArray()
        spec.getByAccession("MS:1000509")

def cleanup():
    os.remove("BSA3.avro")
    os.remove("BSA3_index.json")
    os.remove("BSA3_meta.avro")
    shutil.rmtree("schemas/", ignore_errors=False)




convert()
readAvro()
cleanup()
