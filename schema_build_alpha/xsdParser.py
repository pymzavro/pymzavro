__author__ = 'marius'
from DictBuilder import DictBuilder
from DictComplex import DictComplex
from AvscMaker import Partconverter
import pprint
import json
pp = pprint.PrettyPrinter()


#script for building dict from mzML xsd and to Write Data to Avro


subDictName = "spectrum"
subDictType = "record"
subSchema = None

def writeSchema(schema):
    avscwriter = open("spectrum.json", "w")
    avscwriter.write(json.dumps(schema))

def setSchema(subSchema):
    subSchema = subSchema

def checkForSubDict(checkedDict):
    dictName = checkedDict.get("name")
    dictType = checkedDict.get("type")
    if dictName == subDictName and dictType == subDictType:
        setSchema(checkedDict)
        found = True
    else:
        found = False

    return found




def writeSpectrum(fullDict):
    if isinstance(fullDict, dict):
        if checkForSubDict(fullDict):
            pass
        else:
            if fullDict.get("type") == "record":
                writeSpectrum(fullDict["fields"])
            elif fullDict.get("type") == "array":
                writeSpectrum(fullDict.get("items"))
            else:
                writeSpectrum(fullDict["type"])
    elif isinstance(fullDict, list):
        for item in fullDict:
            if item is not "null":
                writeSpectrum(item)


xsd = "mzML1.1.0.xsd"
profiling = False


foo = DictBuilder()
complexDict = foo.buildDict(xsd)
rootName = foo.getRootName()

complex = DictComplex(complexDict)
newDict = complex.getnewDict("mzMLType")
schema = {rootName:{"type" : newDict}}
avscM = Partconverter(schema)
avscM.writeAVSC()
avscM.writeTypeDictToJSON()
writeSpectrum(avscM.getfullDict())
writeSchema(subSchema)


#foo.removeComplex(subschema)

