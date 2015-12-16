import pymzavro
import pprint
import pyavroc
import time

pp = pprint.PrettyPrinter()

avroPath = "/home/marius/F04.avro"
avroMetaPath = "tiny.pwiz.1.1_meta.avro"

avroFile = open(avroPath)
avroFileMeta = open(avroMetaPath)
reader = pymzavro.reader.PymzAvroReader(avroFile, avroFileMeta)
#reader = pyavroc.AvroFileReader(avroFile, types=True)

start = time.time()
for spec in reader:
    #pp.pprint(spec.getMSDict())
    spec.getmzArray()
    break

end =  time.time()
print(end - start)