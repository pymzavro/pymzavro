__author__ = 'marius'

import pprint


class DictComplex:
    def __init__(self, iteratedDict):
        self.xsdDict = iteratedDict
        self.typeDict = {}
        self.pp = pprint.PrettyPrinter()
        self.extensionFound = True
        self.newDict = self.xsdDict
        self.tempList = []

        #Loop to make sure all extensions are found and replaced (Problems could occur if their was an extension within
        # an extension), maybe should be placed in an extra function
        while self.extensionFound:
            self.extensionFound = False
            self.newDict = self.extensionIter(self.newDict)



        self.complexIter(self.newDict)

        #for testing only
        #self.pp.pprint(self.newDict["mzMLType"])



    #replaces extension types in the dict -> maybe switch to list based method instead of creating a new one
    def extensionIter(self, iteratedDict):
        tempDict = {}
        for key in iteratedDict:
            if "extension" in key:
                regularType = iteratedDict[key]
                regularType = regularType.lstrip("dx:")
                tempDict.update(self.newDict[regularType])
                self.extensionFound = True
            elif isinstance(iteratedDict[key], dict):
                tempDict[key] = self.extensionIter(iteratedDict[key])
            else:
                tempDict.update(iteratedDict)
        return tempDict


    #replaces complex Types by their regular type
    def complexIter(self, iteratedDict):
        tempDict = {}
        for key in iteratedDict:
            if isinstance(iteratedDict[key], dict):
                currentType = iteratedDict[key].get("type")
                if currentType is not None and "dx:" in currentType:
                    attribDict = iteratedDict[key]
                    currentType = currentType.lstrip("dx:")
                    attribDict["type"] = self.newDict[currentType]
                    tempDict.update(attribDict)


                tempDict[key] = self.complexIter(iteratedDict[key])
            else:
                tempDict.update(iteratedDict)
        return tempDict

    def getnewDict(self, rootElement):
        return self.newDict[rootElement]
