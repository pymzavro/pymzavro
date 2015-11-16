__author__ = 'marius'


import time
import pymzavro
import pymzml

class PassTest():
    def __init__(self, avroFile, mzMLFile):
        self.avroFile = avroFile
        self.mzMLFile = mzMLFile


    def pymzavroPass(self):
        startTime = time.time()
        avroFile = open(self.avroFile)
        reader = pymzavro.reader.PymzAvroReader(avroFile, readerType=True)
        for spectrum in reader:
            pass
        endTime = time.time()

        return endTime - startTime

    def pymzavroBasic(self):
        startTime = time.time()
        avroFile = open(self.avroFile)
        reader = pymzavro.reader.PymzAvroReader(avroFile, readerType=True)
        for spectrum in reader:
            iArray = spectrum.getIntensityArray()
        endTime = time.time()


        return endTime - startTime

    def pymzMLPass(self):
        startTime = time.time()
        mzMLFile = open(self.mzMLFile)
        reader = pymzml.run.Reader("", file_object=mzMLFile)
        for spectrum in reader:
            pass
        endTime = time.time()

        return endTime-startTime

    def pymzMLBasic(self):
        startTime = time.time()
        mzMLFile = open(self.mzMLFile)
        reader = pymzml.run.Reader("", file_object=mzMLFile)
        for spectrum in reader:
            iArray = spectrum.i
        endTime = time.time()

        return endTime-startTime



    def testAll(self):
        for i in range(3):
            #avroPassTime = self.pymzavroPass()
            #avroBasicTime = self.pymzavroBasic()
            pymzMLPassTime = self.pymzMLPass()
            #pymzMLBasicTime = self.pymzMLBasic()

            #print(avroPassTime)
            #print(avroBasicTime)
            print(pymzMLPassTime)
            #print(pymzMLBasicTime)




if __name__ == "__main__":
    test = PassTest("/home/marius/data/Y/avro/Y/Y2.avro", "/home/marius/data/Y/mzML/Y2.mzML")
    test.testAll()
