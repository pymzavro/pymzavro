__author__ = 'marius'

import pymzavro
import pyopenms
import time
import pymzml


class TICCalculator:

    def __init__(self):
        self.TIC = 0
        self.size = 0
        self.nr_peaks = 0

    def consumeSpectrum(self,s):
        self.TIC += sum(s.get_peaks()[1])
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
        self.TIC += sum(s)
        self.size += 1
        self.nr_peaks += len(s)

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
        reader = pymzavro.reader.PymzAvroReader(avroFile, readerType=True)
        for spectrum in reader:
            TIC.consumeSpectrum(spectrum.getIntensityArray())
        endTime = time.time()
        avroFile.close()
        TIC.printData()
        return endTime-startTime

    def pyOpenMSStream(self):
        startTime = time.time()
        functor = TICCalculator()
        pyopenms.MzMLFile().transform(self.mzMLFile, functor)
        endTime = time.time()
        return endTime-startTime


    def pymzMLTest(self):
        sumFunc = TICCalculatorAvro()
        startTime = time.time()
        openFile = open(self.mzMLFile)
        reader = pymzml.run.Reader("", file_object=openFile)

        for spectrum in reader:
            iArray = spectrum.i
            sumFunc.consumeSpectrum(iArray)
        endTime = time.time()
        return endTime-startTime


    def pyOpenMSregular(self):
        sumFunc = TICCalculatorAvro()
        starTime = time.time()
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(self.mzMLFile, exp)

        for spectrum in exp:
            iArray = spectrum.get_peaks()[1]
            sumFunc.consumeSpectrum(iArray)
        endTime = time.time()
        return (endTime-starTime)
