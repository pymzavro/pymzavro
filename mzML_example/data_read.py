import pymzavro
import time
import pprint
baa = 0;
pp = pprint.PrettyPrinter()
startTime = time.time()
avroFile = open("/home/marius/F04.avro")
reader = pymzavro.reader.PymzAvroReader(avroFile)
for spectrum in reader:
    foo = spectrum.getmzArray()
    baa = baa + sum(foo)
endTime = time.time()
print(baa)

print(endTime-startTime)

'''
seekFile = open("BSA3.avro")
indexReader = pymzavro.reader.PymzAvroReader(seekFile, indexFile="BSA3_index.json")
spectrum = indexReader.rndSeek(694, "BSA3.avro")
mzArray = spectrum.getmzArray()
'''