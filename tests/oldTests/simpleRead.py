import pymzavro
import pprint
import pyavroc
import time

pp = pprint.PrettyPrinter()

avroPath = "/home/marius/data/Y1.avro"
#avroMetaPath = "tiny.pwiz.1.1_meta.avro"

avroFile = open(avroPath)
#avroFileMeta = open(avroMetaPath)
reader = pymzavro.reader.PymzAvroReader(avroFile)

start = time.time()
for spec in reader:
    spec.getmzArray()

end =  time.time()
print(end - start)