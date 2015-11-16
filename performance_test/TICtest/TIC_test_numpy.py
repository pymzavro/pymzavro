__author__ = 'marius'

import pymzavro
import pyopenms
import time
import pymzml
import numpy

import numpy

class TICCalculator:

    def __init__(self):
        self.TIC = 0
        self.size = 0
        self.nr_peaks = 0

    def consumeSpectrum(self,s):
        self.TIC += numpy.sum(s.get_peaks()[1])
        self.size += 1
        self.nr_peaks += s.size()

    def consumeChromatogram(self,s):
        pass

    def setExpectedSize(self, x,y):
        pass

    def setExperimentalSettings(self,e):
        pass

    def printData(self):
        print(self.TIC)
        print(self.size)
        print(self.nr_peaks)

class TICCalculatorAvro:

    def __init__(self):
        self.TIC = 0
        self.size = 0
        self.nr_peaks = 0

    def consumeSpectrum(self,s):
        self.TIC += numpy.sum(s)
        self.size += 1
        self.nr_peaks += len(s)

    def consumeChromatogram(self,s):
        pass

    def setExpectedSize(self, x,y):
        pass

    def setExperimentalSettings(self,e):
        pass

    def printData(self):
        print(self.TIC)
        print(self.size)
        print(self.nr_peaks)


class TestingMethods:
    def __init__(self, avroFile = None, mzMLFile = None):
        self.avrofile = avroFile
        self.mzMLFile = mzMLFile

    def pymzavro(self):
        startTime = time.time()
        TIC = TICCalculatorAvro()
        avroFile = open(self.avrofile)
        reader = pymzavro.reader.PymzAvroReader(avroFile)
        TIC = TICCalculatorAvro()
        for spectrum in reader:
            TIC.consumeSpectrum(spectrum.getIntensityArray())
        endTime = time.time()
        TIC.printData()
        return endTime-startTime

    def pyOpenMSStream(self):
        startTime = time.time()
        functor = TICCalculator()
        pyopenms.MzMLFile().transform(self.mzMLFile, functor)
        endTime = time.time()
        return endTime-startTime

    def pyOpenMSIndexed(self):
        startTime = time.time()
        exp = pyopenms.OnDiscMSExperiment()
        pyopenms.IndexedMzMLFileLoader().load(self.mzMLFile, exp)
        TIC = 0.0
        nr_peaks = 0
        for i in range(exp.getNrSpectra()):
            spec = exp.getSpectrum(i)
            TIC += numpy.sum(spec.get_peaks()[1])
            nr_peaks += spec.size()
        endTime = time.time()

        return endTime-startTime

    def pymzMLTest(self):
        startTime = time.time()
        openFile = open(self.mzMLFile)
        reader = pymzml.run.Reader("", file_object=openFile, build_index_from_scratch=True)
        TIC = 0
        nr_peaks = 0
        for spectrum in reader:
            i = spectrum.i
            TIC += numpy.sum(i)
            nr_peaks += len(i)
        endTime = time.time()
        return endTime-startTime


    def pyOpenMSregular(self):
        starTime = time.time()
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(self.mzMLFile, exp)
        TIC = 0
        nr_peaks = 0
        for spectrum in exp:
            i = spectrum.get_peaks()[1]
            TIC += sum(i)
            nr_peaks += len(i)
        endTime = time.time()

        return (endTime-starTime)

if __name__ == "__main__":
    foo = TestingMethods(avroFile="/home/marius/data/Y/avro/Y1.avro", mzMLFile="/home/marius/data/Y/mzML/Y1.mzML")
    #foo.pymzavro()
    #foo.pyOpenMSStream()
    #foo.pyOpenMSIndexed()
    foo.pymzMLTest()