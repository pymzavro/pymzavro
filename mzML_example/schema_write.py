from __future__ import print_function

__author__ = 'marius'

import pymzavro.SchemaBuilder
import pymzavro
import pymzml


#schema creator

xsd = "mzML1.1.0.xsd"
typeFile = open("typeDict.json", "w")
fullSchemaFile = open("fullSchema.avsc", "w")
spectrumFile = open("spectrum.avsc", "w")

schemabuilder = pymzavro.SchemaBuilder.SchemaBuilder(xsd)
schemabuilder.initFiles(fullSchemaFile=fullSchemaFile, subSchemaFile=spectrumFile, typeDictFile=typeFile)
schemabuilder.autoMake()

