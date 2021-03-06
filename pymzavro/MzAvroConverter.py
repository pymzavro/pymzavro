from __future__ import print_function

__author__ = 'marius'

import os
import tempfile


import pymzavro.SchemaBuilder
import pymzavro

try:
    import pymzml
except:
    print("pymzML not found")

chromalistSchema = []



class MzConverter():
    """
    Class to perform conversion of mzML files to mzavro files.
    """
    def __init__(self, mzMLFile, avroFile=None, avroMetaFile=None, indexFile=None, xsdFile="mzML1.1.0.xsd"):
        self.mzMLPath = mzMLFile
        self.mzMLFileMeta = open(self.mzMLPath, "r")
        self.mzMLFile = open(self.mzMLPath, "r")
        self.avroFile = avroFile
        self.avroMetaFile = avroMetaFile
        self.indexFile = indexFile
        self.xsdFile = xsdFile

        self.chromaList = []

    def createmzAvroFiles(self):
        self.mzMLPath = os.path.abspath(self.mzMLFile.name)
        if self.avroFile is None:
            self.avroFile = open(self.mzMLPath.rsplit(".", 1)[0] + ".avro", "wb")

        if self.avroMetaFile is None:
            self.avroMetaFile = open(self.mzMLPath.rsplit(".", 1)[0] + "_meta.avro", "wb")

        if self.indexFile is None:
            self.indexFile = self.mzMLPath.rsplit(".", 1)[0] + "_index.json"

    def convert(self):
        self.createmzAvroFiles()
        self.makeSchema()
        self.writeSpectrum()
        self.writeMetaFile()

        return 1


    def makeSchema(self):
        xsd = open(self.xsdFile, "rb")
        if not (os.path.exists("schemas")):
            os.makedirs("schemas")
        self.typeFile = open("schemas/typeFile.json", "w")
        self.fullSchemaFile = open("schemas/metaSchema.avsc", "w")
        self.spectrumFile = open("schemas/spectrumSchema.avsc", "w")

        schemabuilder = pymzavro.SchemaBuilder.SchemaBuilder(xsd)
        schemabuilder.initFiles(fullSchemaFile=self.fullSchemaFile, subSchemaFile=self.spectrumFile,
                                typeDictFile=self.typeFile)
        schemabuilder.autoMake()

        self.typeFile = open("schemas/typeFile.json", "rb")
        self.typeFileMeta = open("schemas/typeFile.json", "rb")
        self.fullSchemaFile = open("schemas/metaSchema.avsc", "rb")
        self.spectrumFile = open("schemas/spectrumSchema.avsc", "rb")

    def writeSpectrum(self):
        avroSchemaTmp =  tempfile.TemporaryFile()
        avroMetaFileTmp = tempfile.TemporaryFile()

        reader = pymzml.run.Reader(self.mzMLFile, file_object=self.mzMLFile)
        writer = pymzavro.mzMLWriter.mzMLWriter()

        writer.init_file(self.mzMLFile, self.avroFile, typeDict=self.typeFile, spectrumAvsc=self.spectrumFile, \
                         avro_schema=avroSchemaTmp, metaDataFile=avroMetaFileTmp, indexJSON=self.indexFile)

        writer.initmzAvroWriter()

        i = 0
        for spectrum in reader:  # iterator
            xml = spectrum.xmlTreeIterFree
            if "spectrum" in xml.tag:
                print(i, end="\r")
                xml = spectrum.xmlTreeIterFree  # get the spectrum XML Tree
                dataDict = {"mzArray": list(spectrum.mz),
                            "intensityArray": list(spectrum.i)}  # additional information stored in a dictionary
                writer.mzAvroWriter(xml, dataDict, i)  # converts/writes the data to avro
                i = i + 1
            elif "chromatogram" in xml.tag:
                self.chromaList.append(
                    {
                        "name": xml.attrib.get("id"),
                        "intensityArray": list(spectrum.i),
                        "timeArray": list(spectrum.mz)
                    }
                )

        writer.writeOffsetToJson()


    def writeMetaFile(self):
        spectrumSchemaTmp = tempfile.TemporaryFile()
        indexJSONTmp = tempfile.TemporaryFile()
        avroFileTmp = tempfile.TemporaryFile()


        writer = pymzavro.mzMLWriter.mzMLWriter()
        writer.init_file(self.mzMLFileMeta, avroFileTmp, typeDict=self.typeFileMeta, spectrumAvsc=spectrumSchemaTmp, \
                avro_schema=self.fullSchemaFile, metaDataFile=self.avroMetaFile, indexJSON=indexJSONTmp)#

        writer.writemzAvroMeta(self.chromaList)
