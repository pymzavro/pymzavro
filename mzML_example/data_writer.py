import pymzavro
import pymzml

#writer
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

print("======writing data==========")
reader = pymzml.run.Reader("BSA3.mzML") #reader initilization (not in pymzavro)

index = 0
for spectrum in reader: #iterator
    #print(i, end="\r")
    xml = spectrum.xmlTreeIterFree #get the spectrum XML Tree
    dataDict = {"mzArray" : list(spectrum.mz), "intensityArray" : list(spectrum.i)} #additional information stored in a dictionary
    writer.mzAvroWriter(xml, dataDict, index) #converts/writes the data to avro, i =
    index = index+1


writer.writeOffsetToJson()