from __future__ import print_function

import pymzml #only for this example, can be any mzML parser that can return the spectrum XMl and the decoded data
import pymzavro


def test_write():

	writer = pymzavro.mzMLWriter.mzMLWriter() #create writer

	'''
	File objects needed for writing
	'''
	mzML = open("BSA3.mzML", "r")
	spectrumFile = open("BSA3.avro", "wb")
	metaDataFile = open("BSA3_meta.avro", "wb") #optional for metadata writing
	typeDict = open("typeDict.json", "rb")
	spectrumSchema = open("spectrum.avsc","r")
	metaDataSchema = open("fullSchema.avsc", "r") #optional for metadata writing
	indexFile = "BSA3_index.json"


	#initilizing files for the writer
	writer.init_file(mzML, spectrumFile, typeDict=typeDict, spectrumAvsc=spectrumSchema,\
	 avro_schema=metaDataSchema, metaDataFile=metaDataFile, indexJSON=indexFile)


	writer.writemzAvroMeta()

	#additional initilization of the mzAvroWriter
	writer.initmzAvroWriter()


	reader = pymzml.run.Reader("BSA3.mzML") #reader initilization (not in pymzavro)

	print ("===spectrum write test===")


	i = 0
	for spectrum in reader: #iterator
	    print(i, end="\r")
	    xml = spectrum.xmlTreeIterFree #get the spectrum XML Tree
	    dataDict = {"mzArray" : list(spectrum.mz), "intensityArray" : list(spectrum.i)} #additional information stored in a dictionary
	    writer.mzAvroWriter(xml, dataDict, i) #converts/writes the data to avro
	    i = i+1


	writer.writeOffsetToJson()

print("\t")
