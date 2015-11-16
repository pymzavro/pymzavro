__author__ = "marius"


import pprint
import json
import random, string

class Partconverter:
    def __init__(self, xsdDict, check_none_avro_type=False, check_sanity=False, customized_data_translation=None):
        self.typeDict = dict()
        random.seed()
        self.currentNameSpace = []
        self.somedict = self.decideIter(xsdDict)
        #self.pprint()

    # TODO make dict from all generated types to perform lookup when generating schema

    def decideIter(self, iterDict):
        returnList = []
        for key in iterDict:
            currentType = iterDict[key].get("type")
            if currentType is not None:
                if isinstance(currentType, dict):
                    maxOccurs = iterDict[key].get("maxOccurs")
                    if maxOccurs is "unbounded":
                        returnList.append(
                            self.makeArray(
                                key,
                                currentType
                            )
                        )
                    else:
                        returnList.append(
                            self.makeRecord(
                                key,
                                currentType
                            )
                        )
                else:
                    returnList.append(
                        self.makePrimitive(
                            key,
                            currentType
                        )
                    )
            else:
                print("Error, field with type none found")

        return returnList


    def makePrimitive(self, primName, primType):
        self.currentNameSpace.append(primName)
        primitive = {
            "name": primName,
            "type": [primType, "null"]
        }
        self.appendTypeDict(primName, self.currentNameSpace, primType)
        self.currentNameSpace.pop()
        return primitive



    def makeRecord(self, recordName, recordFields):
        fieldsList = []
        currentName = recordName
        self.currentNameSpace.append(recordName)

        for key in recordFields:
            currentType = recordFields[key].get("type")
            if isinstance(currentType, dict):
                if recordFields[key].get("maxOccurs") == "unbounded":
                    fieldsList.append(
                        self.makeArray(
                            key,
                            recordFields[key]["type"],
                        )
                    )
                else:
                    fieldsList.append(
                        self.makeNestedRecord(
                            key,
                            recordFields[key].get("type"),
                        )
                    )
            else:
                fieldsList.append(
                    self.makePrimitive(
                        key,
                        recordFields[key]["type"]
                    )
                )
        self.appendTypeDict(currentName, self.currentNameSpace, "record")
        self.currentNameSpace.pop()
        nameSpaceString = self.makeNameSpaceString(self.currentNameSpace)
        currentRecord = {"name": currentName, "type": "record", "fields": fieldsList, "namespace": nameSpaceString}
        #self.appendTypeDict(currentName, self.currentNameSpace, "record")
        return currentRecord

    # TODO check if the same names can appear twice within the same nested record or create other name

    def makeNestedRecord(self, recordName, recordFields):
        fieldsList = []
        currentName = recordName
        self.currentNameSpace.append(currentName)
        for key in recordFields:
            currentType = recordFields[key].get("type")
            if isinstance(currentType, dict):
                if recordFields[key].get("maxOccurs") == "unbounded":
                    fieldsList.append(
                        self.makeArray(
                            key,
                            recordFields[key]["type"],
                        )
                    )
                else:
                    fieldsList.append(
                        self.makeNestedRecord(
                            key,
                            recordFields[key].get("type"),

                        )
                    )
            else:
                fieldsList.append(
                    self.makePrimitive(
                        key,
                        recordFields[key]["type"],
                    )
                )
        self.appendTypeDict(currentName, self.currentNameSpace, "NestedRecord")
        self.currentNameSpace.pop()
        nameSpaceString = self.makeNameSpaceString(self.currentNameSpace)
        currentRecord = {"name": currentName,
                         "namespace": nameSpaceString,
                         "type": [{"name": currentName, "type": "record", "fields": fieldsList,
                                   "namespace": nameSpaceString}, "null"]}
        #self.appendTypeDict(currentName, self.currentNameSpace, "NestedRecord")
        return currentRecord



    def makeArray(self, arrayName, arrayItems):
        self.currentNameSpace.append(arrayName)
        items = self.makeRecord(arrayName, arrayItems)
        self.appendTypeDict(arrayName, self.currentNameSpace, "array")
        self.currentNameSpace.pop()
        array = {"name": arrayName, "type": [{"type": "array", "items": items}, "null"]}

        return array


    def pprint(self):
        pp = pprint.PrettyPrinter()
        #pp.pprint(self.somedict[0])
        #print(json.dumps(self.somedict[0]))
        #pp.pprint(self.typeDict)

    def makeNameSpaceString(self, nameSpaceList):
        nameSpaceString = ".".join(nameSpaceList)

        return nameSpaceString

    def appendTypeDict(self, name, namespace, currentType):
        currentNameSpace = []
        for name in namespace:
            currentNameSpace.append(name)
        #currentNameSpace.append(name)

        fullName = ".".join(currentNameSpace)
        self.typeDict[fullName] = currentType


    def getfullSchema(self):
        return self.somedict[0]

    def getTypeDict(self):
        return self.typeDict






