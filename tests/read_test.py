import pymzavro



def test_read():
	print("======sequential read test======")
	avroFile = open("BSA3.avro")
	reader = pymzavro.reader.PymzAvroReader(avroFile)

	isum = 0
	ms_level = 0
	for spectrum in reader:
		isum = isum +  sum(spectrum.getIntensityArray())
		ms_level = ms_level + int(spectrum.getByAccession("MS:1000511"))
	print (isum)
	print (ms_level)


	print("=====index seek======")
	avroFileSeek = open("BSA3.avro")
	indexReader = pymzavro.reader.PymzAvroReader(avroFileSeek, indexFile="BSA3_index.json")

	spectrum = indexReader.rndSeek(694, "BSA3.avro")
	print(sum(spectrum.getIntensityArray()))

	return 1