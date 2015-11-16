__author__ = 'marius'
import pymzavro

XML = open("small.xml")
typeDict = open("typeDict.json")
avroFile = open("small.avro", "wb")
avroSchema = open("small.avsc")


writer = pymzavro.XMLWriter.Writer()
writer.init_file(XML, avroFile, typeDict, avroSchema)
writer.start()
writer.writeDictToFile()