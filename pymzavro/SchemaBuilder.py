__author__ = 'marius'

import pprint
import json

from DictBuilder import DictBuilder
from DictComplex import DictComplex
from AvscMaker import Partconverter

pp = pprint.PrettyPrinter()

intensityDict = {"name" : "intensityArray", "type":[{
      "type" : "array", "items" : ["double", "float"]
    }, "null"]}

mzDict = {"name" : "mzArray", "type":[{
      "type" : "array", "items" : ["double", "float"]
    }, "null"]}

chromalist = {
    "name" : "chromalist",
    "type" : [
        {
            "type" : "array",
            "items" : [
                {
                    "name" : "chromatogram",
                    "type" : "record",
                    "fields" : [
                        {
                            "name" : "name",
                            "type" : "string"
                        },
                        {
                            "name" : "intensityArray",
                            "type" : {
                                "type" : "array",
                                "items" : ["double", "float"]
                            }
                        },
                        {
                            "name" : "timeArray",
                            "type" : {
                                "type" : "array",
                                "items" : ["double", "float"]
                            }
                        }
                    ]
                }
            ]
        }, "null"
    ]
}



class SchemaBuilder:
    def __init__(self, xsd):
        """

        :param xsd: path to the xsd
        :return:
        """
        self.xsd = xsd
        self.fullSchema = None
        self.subSchema = None
        self.typeDict = None
        self.subDictName = "spectrum"
        self.subDictType = "record"

    def initFiles(self, fullSchemaFile = None, typeDictFile = None, subSchemaFile = None):
        """
        Sets the files the data of the schemas and the typeDict is written to
        :param fullSchemaFile: opened file the fullSchema is written to
        :param typeDictFile: opened file the typeDict is written to
        :param subSchemaFile: opened file the subSchema is written (currently the spectrum schema)
        :return:
        """
        self.fullSchemaFile = fullSchemaFile
        self.typeDictFile = typeDictFile
        self.subSchemaFile = subSchemaFile

    def createFullSchema(self):
        """
        Used to create the full schema according to the xsd
        :return:
        """
        dictbuilder = DictBuilder()
        complexDict = dictbuilder.buildDict(self.xsd)
        rootName = dictbuilder.getRootName()

        dictcomplex = DictComplex(complexDict)
        newDict = dictcomplex.getnewDict("mzMLType")
        schema = {rootName: {"type" : newDict}}
        AvscMaker = Partconverter(schema)
        self.fullSchema = AvscMaker.getfullSchema()
        self.typeDict = AvscMaker.getTypeDict()



    def initSpectrumCreation(self):
        """
        Used to create the spectrum schema \
        (or any other subSchema as well, if a different subDictName and subDictType is set)
        :return: 0 if successfull
        """
        self.createSpectrum(self.fullSchema)

    def createSpectrum(self, fullDict):
        if isinstance(fullDict, dict):
            if self.checkForSubDict(fullDict):
                pass
            else:
                if fullDict.get("type") == "record":
                    self.createSpectrum(fullDict["fields"])
                elif fullDict.get("type") == "array":
                    self.createSpectrum(fullDict.get("items"))
                else:
                    self.createSpectrum(fullDict["type"])
        elif isinstance(fullDict, list):
            for item in fullDict:
                if item is not "null":
                    self.createSpectrum(item)

    def checkForSubDict(self, checkedDict):
        dictName = checkedDict.get("name")
        dictType = checkedDict.get("type")
        if dictName == self.subDictName and dictType == self.subDictType:
            self.setSubSchema(checkedDict)
            found = True
        else:
            found = False

        return found

    def appendCustomFieldFull(self, customSchema):
        """
        Appends an additional schema to the fields list of the outer record of the full schema
        :param customSchema: additional schema part that is added to the fields list
        :return:
        """
        self.fullSchema["fields"].append(customSchema)

    def setSubSchema(self, subSchema):
        self.subSchema = subSchema

    def appendDecodedArray(self):
        """
        Appends the standard mz and intensity Array fields
        :return:
        """
        self.subSchema["fields"].append(mzDict)
        self.subSchema["fields"].append(intensityDict)

    def appendCustomField(self, customSchema):
        """
        Appends an additional schema to the fields list of the outer record of the sub schema
        :param customSchema: additional schema part that is added to the fields list
        :return:
        """
        self.subSchema["fields"].append(customSchema)

    def appendChromaList(self):
        self.fullSchema["fields"].append(chromalist)



    def writeSubSchema(self):
        """
        writes the sub schema to the file provided in initfile()
        :return:
        """
        self.subSchemaFile.write(json.dumps(self.subSchema))

    def writeFullSchema(self):
        """
        writes the full schema to the file provided in initfile()
        :return:
        """
        self.fullSchemaFile.write(json.dumps(self.fullSchema))

    def writeTypeDict(self):
        """
        writes the type dict to the file provided in initfile()
        :return:
        """
        self.typeDictFile.write(json.dumps(self.typeDict))

    def autoMake(self):
        """
        Creates all three files required for writing, can be used as input files of the examples given
        :return:
        """
        self.createFullSchema()
        self.initSpectrumCreation()
        self.appendDecodedArray()
        self.appendChromaList()
        self.writeFullSchema()
        self.writeSubSchema()
        self.writeTypeDict()

    def getFullSchema(self):
        """

        :return: returns the full schema dictionary
        """
        return self.fullSchema

    def getSubSchema(self):
        """

        :return: returns the sub schema dictionary
        """
        return self.subSchema

    def getTypeDict(self):
        """

        :return: returns the type dict
        """
        return self.typeDict



if __name__ == "__main__":
    xsd = "small.xsd"
    typeFile = open("typeDict.json", "w")
    fullSchemaFile = open("fullSchema.avsc", "w")
    spectrumFile = open("spectrum.json", "w")


    schemabuilder = SchemaBuilder(xsd)
    schemabuilder.initFiles(fullSchemaFile=fullSchemaFile, subSchemaFile=spectrumFile, typeDictFile=typeFile)
    schemabuilder.createFullSchema()
    schemabuilder.writeFullSchema()
    schemabuilder.writeTypeDict()
    #schemabuilder.autoMake()