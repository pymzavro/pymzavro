import pymzml #only for this example, can be any mzML parser that can return the spectrum XMl and the decoded data
import pymzavro

writer = pymzavro.mzMLWriter.mzMLWriter() #create writer


'''
File objects needed for writing
'''
mzML = open("BSA3.mzML", "r")
spectrumFile = open("BSA3.avro", "wb")
metaDataFile = open("BSA3meta.avro", "wb") #optional for metadata writing
typeDict = open("typeDict.json", "rb")
spectrumSchema = open("spectrum.avsc","r")
metaDataSchema = open("fullSchema.avsc", "r") #optional for metadata writing
indexFile = "BSA3index.json"


#initilizing files for the writer
writer.init_file(mzML, spectrumFile, typeDict=typeDict, spectrumAvsc=spectrumSchema,\
 avro_schema=metaDataSchema, metaDataFile=metaDataFile, indexJSON=indexFile)


writer.writemzAvroMeta()

#additional initilization ofr the mzAvroWriter
writer.initmzAvroWriter()


reader = pymzml.run.Reader("BSA3.mzML") #reader initilization (not in pymzavro)

for spectrum in reader: #iterator
	xml = spectrum.xmlTreeIterFree #get the spectrum XML Tree
	dataDict = {"mzArray" : list(spectrum.mz), "intensityArray" : list(spectrum.i)} #additional information stored in a dictionary
	writer.mzAvroWriter(xml, dataDict) #converts/writes the data to avro


writer.writeOffsetToJson()