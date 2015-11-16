from __future__ import print_function
import xml.etree.cElementTree as ET
import pprint
import json
import pyavroc
import time

__author__ = 'marius'


class Writer:
    def __init__(self):
        self.pp = pprint.PrettyPrinter()
        self.currentNameSpace = []
        self.specialType = None

    #init essential data
    # TODO switch to dict based?
    def init_file(self, xml, avroFile, typeDict, avro_schema):
        #self.xsd = xsd
        self.XMLFile = xml
        self.avroFile = avroFile
        self.avroSchema = avro_schema
        self.typeDict = self.makeTypeDictFromJson(typeDict)
        #self.specialXML = specialXML

    #starts iterating across XML using
    def start(self):
        self.xmlTree = ET.parse(self.XMLFile)
        self.xmlTree = self.xmlTree.getroot()
        self.specialXML = self.checkSpecial()

        if self.specialXML == False:
            self.currentNameSpace.append(self.xmlTree.tag.split("}")[1])
            self.xmlDict = self.buildDictFromXML(self.xmlTree)

        # change to function -> function is defined in the child class
        else:
            for child in self.xmlTree:
                if "mzML" in child.tag:
                    self.currentNameSpace.append(child.tag.split("}")[1])
                    self.xmlDict = self.buildDictFromXML(child)

    #iterates recursevly across XML, returns corrosponding dict according to AVSC Schema
    def buildDictFromXML(self, subXML):
        finalDict = {}
        finalDict.update(self.makeAttribDict(subXML.attrib))
        for child in subXML:
            name = child.tag
            name = name.split("}")[1]
            currentType = self.searchType(name, self.currentNameSpace)
            self.currentNameSpace.append(name)
            if self.checkExtra(name) is True:
                if "NestedRecord" in currentType:
                    tempDict = {}
                    tempDict.update(self.makeAttribDict(child.attrib))
                    tempDict.update(self.buildDictFromXML(child))
                    finalDict[name] = tempDict

                elif "record" in currentType:
                    finalDict.update(self.makeAttribDict(child.attrib))
                    finalDict.update(self.buildDictFromXML(child))

                elif "array" in currentType:
                    tempList = []
                    self.currentNameSpace.append(name)
                    check = finalDict.get(name)
                    checkAttrib = child.attrib
                    recordCheck = False
                    for foo in child:
                        recordCheck = True
                    if check is not None:
                        if checkAttrib is not None:
                            finalDict[name].append(self.makeAttribDict(child.attrib))
                        if recordCheck == True:
                            finalDict[name].append(self.buildDictFromXML(child))
                    else:
                        if checkAttrib is not None:
                            finalDict[name] = [self.makeAttribDict(child.attrib)]
                            if recordCheck == True:
                                finalDict[name].append(self.buildDictFromXML(child))
                        else:
                            if recordCheck == True:
                                finalDict[name] = [self.buildDictFromXML(child)]
                    self.currentNameSpace.pop()
                    #used to deal with encoded data
                elif "string" in currentType:
                    exec(self.makeStringType())
            else:
                self.currentNameSpace.pop()
                break

            self.currentNameSpace.pop()
        return finalDict

    def makeStringType(self):
        return "finalDict.update({name:child.text})"


    def searchType(self, name, nameSpace):
        fullName = ""
        thisNameSpace = []
        thisNameSpace.extend(nameSpace)
        thisNameSpace.append(name)
        fullName = ".".join(thisNameSpace)
        return self.typeDict.get(fullName)

    def makeAttribDict(self, dataDict):
        attribDict = {}
        for dataName in dataDict:
            if dataName.startswith("{"):
                dataName = dataName.split("}")[1]
            currentType = self.searchType(dataName, self.currentNameSpace)
            if currentType is not None:
                if "string" in currentType:
                    attribDict[dataName] = dataDict[dataName]
                elif "int" in currentType:
                    attribDict[dataName] = int(dataDict[dataName])
                else:
                    print("error non-handled type")
        return attribDict



    def makeTypeDictFromJson(self, typeDictJSON):
        typeDict = json.load(typeDictJSON)
        return typeDict

    def writeDictToFile(self):
        schemaFile = self.avroSchema.read()
        avroWriter = pyavroc.AvroFileWriter(self.avroFile, schemaFile)
        print(self.xmlDict)
        avroWriter.write(self.xmlDict)

    def checkExtra(self, name):
        return True

    def checkSpecial(self):
        return False

#aas
