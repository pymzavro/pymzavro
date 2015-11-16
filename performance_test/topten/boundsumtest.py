__author__ = 'marius'
import pymzavro
import time
import pyopenms
import pymzml
import numpy

class Bounder:
    def __init__(self):
        self.mzsum = 0
        self.upperLimit = 400
        self.lowerLimit = 300

    def consumeSpectrum(self,s):
        mzArray = s.get_peaks()[0]
        for mz in mzArray:
            if self.lowerLimit <= mz <= self.upperLimit:
                self.mzsum = self.mzsum + mz
        return self.mzsum

    def consumeChromatogram(self,s):
        pass

    def setExpectedSize(self, x,y):
        pass

    def setExperimentalSettings(self,e):
        pass

    def printsum(self):
        print(self.mzsum)


class Boundsumtest():
    def __init__(self, avroFile = None, mzMLFile = None ):
        self.avroFile = avroFile
        self.mzMLFile = mzMLFile

        self.upperLimit = 400
        self.lowerLimit = 300

    def sumBounds(self, mzArray):
        mzsum = 0
        for mz in mzArray:
            if self.lowerLimit <= mz <= self.upperLimit:
                mzsum = mzsum + mz

        return mzsum

    def boundavro(self):
        startTime = time.time()
        avroFile = open(self.avroFile)
        reader = pymzavro.reader.PymzAvroReader(avroFile, readerType=True)
        mzsum = 0
        for spectrum in reader:
            mzArray = spectrum.getmzArray()
            mzsum = mzsum + self.sumBounds(mzArray)
        endTime = time.time()
        avroFile.close()
        return endTime-startTime


    def pyOpenMSStream(self):
        startTime = time.time()
        functor = Bounder()
        pyopenms.MzMLFile().transform(self.mzMLFile, functor)
        endTime = time.time()
        return endTime-startTime

    def pymzMLTest(self):
        startTime = time.time()
        openFile = open(self.mzMLFile)
        reader = pymzml.run.Reader("", file_object=openFile)
        TIC = 0
        nr_peaks = 0
        for spectrum in reader:
            if "spectrum" in next(spectrum.xmlTree).tag:
                mzArray = spectrum.mz
                self.sumBounds(mzArray)
        endTime = time.time()
        return endTime-startTime

    def pyOpenMSregular(self):
        mzsum = 0
        starTime = time.time()
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(self.mzMLFile, exp)
        TIC = 0
        nr_peaks = 0
        for spectrum in exp:
            mzArray = spectrum.get_peaks()[0]
            mzsum = mzsum + self.sumBounds(mzArray)
        endTime = time.time()
        return (endTime-starTime)


