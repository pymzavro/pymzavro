import pymzavro
import time
avroFile = open("/home/marius/pydoopTest/Y1.avro")

upperBound = 300
lowerBound = 100

isum = 0

run = pymzavro.reader.PymzAvroReader(avroFile)

startTime = time.time()
for spectrum in run:
    mzArray = spectrum.getmzArray()
    iArray = spectrum.getIntensityArray()
    for i in range(0, len(mzArray)):
        currentMZ = mzArray[i]
        if currentMZ >= lowerBound and currentMZ <= upperBound:
            isum =  isum + iArray[i]


endTime =  time.time()
print(endTime-startTime)
print(isum)
