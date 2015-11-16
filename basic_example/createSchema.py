import pymzavro.SchemaBuilder

xsd = "small.xsd"
typeFile = open("typeDict.json", "w")
fullSchemaFile = open("fullSchema.avsc", "w")
spectrumFile = open("spectrum.json", "w")

schemabuilder = pymzavro.SchemaBuilder.SchemaBuilder(xsd)
schemabuilder.initFiles(fullSchemaFile=fullSchemaFile, subSchemaFile=spectrumFile, typeDictFile=typeFile)
schemabuilder.createFullSchema()
schemabuilder.writeFullSchema()
schemabuilder.writeTypeDict()
