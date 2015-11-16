__author__ = 'marius'


import pymzavro
file = open("BSA3.avro", "rb")
seekFile = open("BSA3.avro", "rb")
index  = "BSA3index.json"
run = pymzavro.reader.PymzAvroReader(file, indexFile=index)

run.init_seek(seekFile, "BSA3index.json")

mzsum = 0
for i in range(1,1000):
    print(i)
    spectrum = run.rndSeek(i)
    mzsum = mzsum + sum(spectrum.getmzArray())