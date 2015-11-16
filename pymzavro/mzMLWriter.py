from __future__ import print_function
from __future__ import division
import pyavroc
import json

try:
    import pymzml
except:
    print("Could not import pymzML, simplemzAvroWriter is disabled, please use mzAvroWriter")


from XMLWriter import Writer
__author__ = 'marius'


class mzMLWriter(Writer):
    """
    Class to convert mzML to avro. Uses pyavroc and pymzML. It is possible that the size of a single record could
    cause problems with the default buffer size of pyavroc. Its recommened to patch the buffer size in datafile.c.

    Example:

    Import pymzavro and pymzml (to iterate)
        >>> import pymzavro
        >>> import pymzml

    Open required files
        >>> mzML = open("/home/marius/data/F/mzML/F04.mzML", "r")
        >>> spectrumFile = open("F04_deflate.avro", "wb")
        >>> spectrumSchema = open("spectrum.avsc","r")
        >>> metaDataFile = open("F04meta_deflate.avro", "wb")
        >>> typeDict = open("typeDict.json", "rb")
        >>> metaDataSchema = open("fullSchema.avsc", "r")
        >>> indexFile = "F04_Indexdeflate.json"

    Create writer object and initialize it correctly
        >>> writer = pymzavro.mzMLWriter.mzMLWriter()

        >>> writer.init_file(mzML, spectrumFile, typeDict=typeDict, spectrumAvsc=spectrumSchema,\
            avro_schema=metaDataSchema, metaDataFile=metaDataFile, indexJSON=indexFile
        >>> writer.initmzAvroWriter()

    Initialize reader (pymzML can be replaced by any other reader that offers the needed informations
        >>> reader = pymzml.run.Reader("BSA3.avro")

    Write metadata (optional), can be used for simple writer as well
        >>> writer.writemzAvroMeta()

    Iterator across the spectra and
    get original XML Tree and decoded m/z and intensity array, arrays are added to a dict (see schema maker):

        >>> for spectrum in reader:
        >>>     xmlSpectrum = spectrum.xmlTreeIterFree
        >>>     mzArray = list(spectrum.mz)
        >>>     iArray = list(spectrum.i)
        >>>     dataDict = {"mzArray" : mzArray, "intensityArray" : iArray}

    Write data to avro
        >>>     writer.mzAvroWriter(xmlSpectrum, dataDict)

    Write index
        >>> writer.writeOffsetToJson()

    """

    def __init__(self):
        Writer.__init__(self)
        self.currentType = None
        self.startOffsetDict = {}
        self.seekCounter = 0
        self.seekCounterList = []

    #initializes files for SpectrumData and Metadata
    def init_file(self,
                  mzML,
                  avroFile,
                  metaDataFile = None,
                  typeDict = None,
                  avro_schema = None,
                  spectrumAvsc = None,
                  indexJSON = "index.json"):

        """
        The init file method is used to provide information about the files the Writer should use. All files should be
        opened file like objects, except for the indexJSON.

            :param mzML: The original mzML files
            :param avroFile: The avro file the spectrumData is written to
            :param typeDict: Needed to find data types
            :param avro_schema: Schema of the whole mzML
            :param metaDataFile: File the to which the metaData is written to
            :param spectrumAvsc: Schema for writing the spectrum Data
            :param specialXML: True if mzML is indexed, False if not
            :param indexJSON: Filename of the index file

        """
        self.XMLFile = mzML
        self.avroFile = avroFile
        self.avroSchema = avro_schema
        self.typeDict = self.makeTypeDictFromJson(typeDict)
        self.metaFile = metaDataFile
        self.spectrumAvsc = spectrumAvsc
        self.indexJSON = indexJSON


        typeDict.seek(0)
        spectrumAvsc.seek(0)

    #writes spectrumData using pymzml, creates Indexdict and count the number of spectra
    def simplemzAvroWriter(self, indexWrite = "advanced"):
        """
        simplemzAvroWriter is used to write spectrum data to an avro file, the information about the files are provided using
        init_file method. The indexWrite option is used to write an index based on the byte offsets of the fileto enable
        random access. The spectrum data is represented by a record that stores all the information that are stored in a
        spectrum child in the original mzML.
        Usage:

            >>> import pymzavro

        Needed files are opened
            >>> mzML = open("/home/marius/data/F/mzML/F04.mzML", "r")
            >>> spectrumFile = open("F04_deflate.avro", "wb")
            >>> spectrumSchema = open("spectrum.avsc","r")

        Initialize writer class
            >>> writer = pymzavro.mzMLWriter.mzMLWriter()
            >>> writer.init_file(mzML, spectrumFile, spectrumAvsc=spectrumSchema)

        start simple conversion
            >>> writer.simplemzAvroWriter()





            :param indexWrite: Used to specify the indexing type that should be used, currently only advanced available
        """

        print("===============Writing Spectrum===============")
        self.indexWrite = indexWrite
        schemaFile = self.spectrumAvsc.read()
        self.spectrumWriter = pyavroc.AvroFileWriter(self.avroFile, schemaFile)
        self.currentType = "spectrum"
        msrun = pymzml.run.Reader("", file_object=self.XMLFile)
        spectrumCount = msrun.getSpectrumCount()
        currentSpectrumCount = 0
        self.currentNameSpace = ['mzML', 'run', 'spectrumList', 'spectrum', "spectrum"]
        self.prevOffset = self.avroFile.tell()

        for spectrum in msrun:
            spectrumXML = spectrum.xmlTreeIterFree
            if "spectrum" in spectrumXML.tag:
                currentSpectrumCount = currentSpectrumCount + 1
                if self.indexWrite is not None:
                    self.decideIndex(currentSpectrumCount)
                percentage = (currentSpectrumCount/int(spectrumCount))*100
                print("SpectrumCount:", currentSpectrumCount, "of", spectrumCount,"|||", percentage,"%", end = "\r")
                dataDict = self.buildDictFromXML(spectrumXML)
                dataDict.update({"mzArray" : list(spectrum.mz)})
                dataDict.update({"intensityArray" : list(spectrum.i)})
                self.xmlDict = dataDict
                #print(dataDict, end="\r")
                self.spectrumWriter.write(self.xmlDict)
            else:
                # chromatograms are stored here
                pass

        self.currentType = None
        self.XMLFile.seek(0)
        print("Finished writing", spectrumCount, "spectra", "\n")

    def initmzAvroWriter(self, indexWrite = "advanced"):
        self.indexWrite = indexWrite
        self.specCount = 0
        schemaFile = self.spectrumAvsc.read()
        self.spectrumWriter = pyavroc.AvroFileWriter(self.avroFile, schemaFile)
        self.currentType = "spectrum"
        self.currentNameSpace = ['mzML', 'run', 'spectrumList', 'spectrum', "spectrum"]
        self.prevOffset = self.avroFile.tell()



    def mzAvroWriter(self, XML, writeDict, index):
        """
        mzAvroWriter takes a spectrum XML as well as additional data stored in a dict that are appended to the file.
        Custom Datafields can be added to the schema using the appendCustomField method in the SchemaBuilder class.
        Usage:
            >>> import pymzml
            >>> import pymzavro
            >>> mzAvroWriter = pymzavro.mzMLWriter.mzMLWriter()
            >>> mzML = open("F04.mzML")
            >>> spectrumFile = open("F04.avro", "wb")
            >>> mzAvroWriter.init_file(mzML, spectrumFile)
            >>> mzAvroWriter.initmzAvroWriter()
            >>> mzMLReader = pymzml.run.Reader("F04.mzML")
            >>> for spectrum in reader:
            >>>     xml = spectrum.xmlTreeIterFree
            >>>     mzAvroWriter.mzAvroWriter(xml, {"mzArray" : spectrum.mz, "intensityArray" : spectrum.i}, spectrum["scan time"])


        :param XML: XML of one spectrum from spectrumlist
        :param writeDict: dict with additional data e.g. decoded data arrays
        """
        if "spectrum" in XML.tag:
            self.specCount = self.specCount + 1
            if self.indexWrite is not None:
                self.decideIndex(index)
            dataDict = self.buildDictFromXML(XML)
            for key in writeDict:
                dataDict.update({key : writeDict[key]})
            self.xmlDict = dataDict
            self.spectrumWriter.write(self.xmlDict)


    #creates Dict from Metadata
    def writemzAvroMeta(self):
        """
        Writes the metaData to the specified meta data avro file. Metadata are defined as all data from mzML that is
        not stored under a spectrum child.
        """
        print("===============Writing Metadata===============", "\n")
        self.currentType = "mzMLmeta"
        self.start()
        self.writeDictToFile(self.metaFile, self.avroSchema)
        self.XMLFile.seek(0)
        print("===========Writing Metadata finished==========", "\n")

    def writeDictToFile(self, currentFile, currentSchema):
        schemaFile = currentSchema.read()
        avroWriter = pyavroc.AvroFileWriter(currentFile, schemaFile)
        avroWriter.write(self.xmlDict)



    #breaks repetitions
    def checkExtra(self, name):
        if name == "spectrum" and self.currentType == "mzMLmeta":
            returnType = False
        else:
            returnType = True
        return returnType


    #checks for special tags prior to writing for example to check weather an mzML is indexed or not
    def checkSpecial(self):
        if "indexedmzML" in self.xmlTree.tag:
            print("Found indexed mzML, iterating to mzML tag","\n")
            indexed = True
        else:
            indexed = False
        return indexed

    def makeStringType(self):
        if self.currentType == "spectrum":
            returnExp = "pass"
        else:
            returnExp = "finalDict.update({name:child.text})"
        return returnExp

    #writes IndexDict to JSON -> only with pyavrocWriter and standard Avro
    def writeOffsetToJson(self):
        """
        Used to write the created index to a dict.
        """
        indexfile = open(self.indexJSON, "wb")
        indexfile.write(json.dumps(self.startOffsetDict))
        indexfile.close()


    def advSeek(self, index):
        """
        This method is used to create an index based on the written blocks. To access a spectrum by index, seek() is
        used to jump to the start of the block and the an iterator goes across the spectra in that block to find the one
        with the given index.
            :param index: The index of the spectrum
        """
        currentOffset = self.avroFile.tell()
        if self.prevOffset == currentOffset:
            self.seekCounter = self.seekCounter + 1
        else:
            self.seekCounterList.append(self.seekCounter)
            self.seekCounter = 0
        self.startOffsetDict[index] = [currentOffset, self.seekCounter]
        self.prevOffset =+ currentOffset


    #does not work, must change pyavroc first
    def syncSeek(self, index):
        self.spectrumWriter()
        self.startOffsetDict[index] = self.avroFile.tell()

    #decides which Indextype to use, currently only adv. search available
    def decideIndex(self, index):
        if self.indexWrite == "advanced":
            self.advSeek(index)
        else:
            pass




