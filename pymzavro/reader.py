from __future__ import print_function
__author__ = 'marius'

import json

import pprint
import pyavroc
import fastavro


from avroSpectrum import avroSpectrum

class PymzAvroReader(object):
    """
    The pymzAvroReader class is used to give basic access to the stored file data. Its iterable and each iteration returns
    a avroSpectrum object that stores the information of the current spectrum and enables basic access to the data.
    The pymzAvroReader also enables random access to spectra using the rndSeek method.
    To initialize the reader, a spectrum file has to be handed over. Optionally a metadata file can be handed over.
    If a metadatafile is available, the metadata are added to spectrum Object.
    Example:
    #iterating across a whole avromz file and printing the mzArray of each spectrum
        >>> import pymzavro
        >>> spectrumAvroFile = open("file")
        >>> run = pymzAvroReader(spectrumAvroFile)
        >>> for spectrum in run:
        >>>     mzArray = self.getmzArray()
        >>>     print(mzArray)

    #seek for a spectrum with a specific index
        >>> import pymzavro
        >>> spectrumAvroFile = open("file")
        >>> indexFile = indexFilePath
        >>> run = pymzAvroReader(spectrumAvroFile)
        >>> run.rndSeek(index, indexFile)

    More methods that provide provide data access please refer to the avroSpectrum class.

    """
    def __init__(self, avromz, metaDataFile = None, readerType = True, indexFile = "index.json"):
        self.pp = pprint.PrettyPrinter()
        self.isInit = True
        self.avromz = avromz
        self.avro = self.avromz
        self.seq_reader = self.seq_Reader(self.avro, readerType)
        self.avroSpectrum = avroSpectrum()
        self.loadSpectrumIndex(indexFile)

        if metaDataFile is not None:
            self.avroSpectrum.setMetaData(metaDataFile)

    # makes the reader object to iterate, tries to use fastes implementation available
    def seq_Reader(self,avro, readerType):
        seq_reader = pyavroc.AvroFileReader(avro, types = readerType)
        return seq_reader

    #iterator
    def next(self):
        element = next(self.seq_reader, ("end"))
        if element == "end":
            raise StopIteration
        else:
            self.avroSpectrum.setData(element)

        return self.avroSpectrum

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self


    def init_seek(self, seekAvro, indexFile):
        self.loadSpectrumIndex(indexFile)
        self.seek_file = seekAvro
        self.seek_reader = fastavro.reader(self.seek_file)




    #working solution
    def rndSeek(self, index):
        """
        Enables random seek
        :param index: number of the index
        :param avromz: path to the mzavroFile
        :return: dictionary representation of th current spectrum
        """
        #seekavro = open(avromz, "rb")
        #reader = fastavro.reader(self.seek_file)
        indexInfoList = self.startIndexOffsets[str(index)]
        self.seek_file.seek(indexInfoList[0])
        i = 0
        for spectrum in self.seek_reader:
            if i == indexInfoList[1]:
                #why is this necessary?
                foundSpectrum = next(reader)
                self.avroSpectrum.setData(foundSpectrum)
                break
            else:
                i = i + 1
        #TODO switch to spectrum class
        return self.avroSpectrum


    #seeks for spectrum in index
    # TODO buggy, sometimes it stops iterating for unknown reason
    def advSeek(self, avromz, index, readerType = True):
        seekavro = open(avromz)
        seekReader = pyavroc.AvroFileReader(seekavro, types = readerType)
        indexInfoList = self.startIndexOffsets[str(index)]
        print(indexInfoList)
        seekavro.seek(indexInfoList[0])
        i = 0
        for spectrum in seekReader:
            print(i)
            if i == indexInfoList[1]:
                break
            else:
                i = i + 1
        return spectrum

    #currently not used -> test performance on hadoop before
    def spectrumSeek(self, index):
        avro = open(self.avromz)
        reader = self.seq_Reader(avro)
        avro.seek(self.startIndexOffsets[str(index)])

    #loads SpectrumIndex if available
    def loadSpectrumIndex(self, indexFile):
        try:
            jsonFile = json.load(open(indexFile))
            self.startIndexOffsets = jsonFile
        except:
            print("Indexfile not found, no random access available")

