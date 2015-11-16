import pymzavro
file = open("BSA3.avro", "rb")
run = pymzavro.reader.PymzAvroReader(file)

for spectrum in run:
    #print(sum(spectrum.getmzArray()))
    print (spectrum.getByAccession("MS:1000016"))