__author__ = 'marius'

import time
import pymzavro

def pymzavro(self):
    avroFile = "/home/marius/Y1.avro"
    sum = 0
    startTime = time.time()
    avroFile = open(self.avrofile)
    reader = pymzavro.reader.PymzAvroReader(avroFile, readerType=True)
    for spectrum in reader:
        iArray = spectrum.getIntensityArray()
        sum =  sum + sum(iArray)
    endTime = time.time()
    avroFile.close()
    print(endTime-startTime)



if __name__ == "__main__":
    pymzavro()