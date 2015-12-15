from __future__ import print_function

import pymzml  # only for this example, can be any mzML parser that can return the spectrum XMl and the decoded data
import pymzavro
import pprint


pp = pprint.PrettyPrinter()

def test_write():
    writer = pymzavro.mzMLWriter.mzMLWriter()  # create writer

    '''
	File objects needed for writing
	'''
    mzML = open("tiny.pwiz.1.1.mzML", "r")
    spectrumFile = open("BSA3.avro", "wb")
    metaDataFile = open("BSA3_meta.avro", "wb")  # optional for metadata writing
    typeDict = open("typeDict.json", "rb")
    spectrumSchema = open("spectrum.avsc", "r")
    metaDataSchema = open("fullSchema.avsc", "r")  # optional for metadata writing
    indexFile = "BSA3_index.json"


    chromaList = []

    # initilizing files for the writer
    writer.init_file(mzML, spectrumFile, typeDict=typeDict, spectrumAvsc=spectrumSchema, \
                     avro_schema=metaDataSchema, metaDataFile=metaDataFile, indexJSON=indexFile)

    test = {
        "chromalist": [
            {
                "name" : "foo",
                "intensityArray" : [1.0,2.0],
                "timeArray" : [4.0]
            }
        ]
    }

    #writer.writemzAvroMeta(test)

    # additional initilization of the mzAvroWriter
    writer.initmzAvroWriter()

    reader = pymzml.run.Reader("/home/marius/Downloads/tiny.pwiz.1.1.mzML")  # reader initilization (not in pymzavro)

    print("===spectrum write test===")

    i = 0
    for spectrum in reader:  # iterator
        xml = spectrum.xmlTreeIterFree
        if "spectrum" in xml.tag:
            print(i, end="\r")
            xml = spectrum.xmlTreeIterFree  # get the spectrum XML Tree
            dataDict = {"mzArray": list(spectrum.mz),
                    "intensityArray": list(spectrum.i)}  # additional information stored in a dictionary
            writer.mzAvroWriter(xml, dataDict, i)  # converts/writes the data to avro
            i = i + 1
        elif "chromatogram" in xml.tag:
            chromaList.append(
                {
                    "name" : xml.attrib.get("id"),
                    "intensityArray" : list(spectrum.i),
                    "timeArray" : list(spectrum.mz)
                }
            )


    writer.writeOffsetToJson()

    mzML = open("tiny.pwiz.1.1.mzML", "r")
    spectrumFile = open("BSA3as.avro", "wb")
    metaDataFile = open("BSA3_meta.avro", "wb")  # optional for metadata writing
    typeDict = open("typeDict.json", "rb")
    spectrumSchema = open("spectrum.avsc", "r")
    metaDataSchema = open("fullSchema.avsc", "r")  # optional for metadata writing
    indexFile = "BSA3_index.json"

    metaWriter = pymzavro.mzMLWriter.mzMLWriter()
    metaWriter.init_file(mzML, spectrumFile, typeDict=typeDict, spectrumAvsc=spectrumSchema, \
                     avro_schema=metaDataSchema, metaDataFile=metaDataFile, indexJSON=indexFile)



    metaWriter.writemzAvroMeta(chromaList)


print("\t")
