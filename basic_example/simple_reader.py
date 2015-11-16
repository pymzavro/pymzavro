import pyavroc

avroFile = open("small.avro")

reader = pyavroc.AvroFileReader(avroFile, types=True)
for datum in reader:
    for cv in datum.cvList.cv:
        print cv.id
