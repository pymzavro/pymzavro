#!/usr/bin/env python
__author__ = 'marius'


import pprint
import pyavroc
import fastavro

class avroSpectrum(object):
    """
    Stores basic information about current spectra and and makes it accessible
    """
    def __init__(self):
        """
        :param:
        :return:
        """
        self.pp = pprint.PrettyPrinter()
        self.createcvParamList()
        self.spectrum = None
        self.metaData = None
        self.metaDataFile = None
        self.cvParamDict = {}
        self.metacvDict = {}
        self.setMSPropDict()
        self.chromaDict = {}

    def setData(self, avroSpectrum):
        """
        Loads the current spectrum data to the avroSpectrum class
            :param avroSpectrum: Avro spectrum class

        """
        if isinstance(avroSpectrum, dict):
            self.spectrum = avroSpectrum
            self.setFromDict(avroSpectrum)
        else:
            self.spectrum = avroSpectrum
            self.iterOvercvParam()

    def setMetaData(self, metaData):
        self.metaDataFile = metaData
        self.readMetaData()



    #used to get data stored in cvParams
    def iterOvercvParam(self):
        """
        Reads cvParams specified in cvParamLocList and stores them with their accession number in a dictionary called
        MSDict

        """
        self.clearMSDict()
        for item in self.cvParamLocList:
            self.currentIter = iter(item)
            currentType = self.spectrum
            self.getFromAVType(currentType, self.currentIter.next())
        self.MSDict["MS:1000514"] = self.spectrum.mzArray
        self.MSDict["MS:1000515"] = self.spectrum.intensityArray

    #iterator to access a specific cvParamList defined in cvParamLocList
    def getFromAVType(self, currentType, attribName):
        if attribName == "cvParam":
            cvParamList = getattr(currentType, attribName, None)
            if cvParamList is not None:
                for cvParam in cvParamList:
                    accession = getattr(cvParam, "accession", None)
                    if self.MSPropDict.get(accession) is not None:
                        dataField = self.MSPropDict[accession][1]
                        self.MSDict[accession] = getattr(cvParam, dataField)
                    else:
                        cvAttr = getattr(cvParam, "value")
                        self.MSDict[accession] = cvAttr

        else:
            currentObj = getattr(currentType, attribName)
            if currentObj is not None:
                if isinstance(currentObj, list):
                    nextAttrib  = self.currentIter.next()
                    for attrib in currentObj:
                        if attrib is not None:
                            self.getFromAVType(attrib, nextAttrib)
                else:
                    self.getFromAVType(currentObj, self.currentIter.next())

    #returns a dictionary that stores data from cvParams (and optionally userParams), the keys are the Obo tags
    def getMSDict(self):
        """
        Used to return a dict with all the cvParam informations extracted
            :rtype: dict
            :return: Returns the  dict with all extracted cvParam informations
        """
        return self.MSDict

    # returns the data from self.MSDict with a specific accession key
    def getByAccession(self, accession):
        """
        Returns the value for the accession (obo Tag) from MSDict
            :param accession: OBO Accession number, e.g.: "MS:1000014"
            :return: value from cvParam for current accession
        """

        cvParam  = self.MSDict.get(accession)
        if cvParam is None:
            cvParam = self.metacvDict.get(accession)
        return cvParam

    #returns the mzArray
    def getmzArray(self):

        """
        Returns a list of mz values, thevalues come from pymzML.spectrum.mz, so if they were decoded in the original
        mzML file, they are decoded by mzML and then written to the avro file.
        :rtype: list
        :return: List of mzValues from the current spectrum
        """
        return self.MSDict["MS:1000514"]

    #returns the intensityArray
    def getIntensityArray(self):
        """
        Returns a list of intensity values of the current spectum, the values come from pymzML.spectrum.i,
        so if they were decoded in the original
        mzML file, they are decoded by mzML and then written to the avro file.
        :rtype: list
        :return: List of intensity values from the current spectrum
        """
        return self.MSDict["MS:1000515"]



    #stores some needed informations about Obo tags for minimum Obo list, derived from pymzML minimum Obo,
    # TODO: write Obo parser/use obo parser from pymzML?
    def setMSPropDict(self):
        """
        Sets minimum OBO list derived from pymzML minimum OBO, used to know wich attribute to get from cvParam
            :return:
        """
        self.MSPropDict = {
            'MS:1000016' : [False, "value", "scan time"], #scan time
            'MS:1000040' : [False, "value", "m/z"], #"m/z"
            'MS:1000041' : [False,  "value", "charge state"], #"charge state"
            'MS:1000127' : [False, "value", "centroid spectrum"], #"centroid spectrum"
            'MS:1000128' : [False, "name", "profile spectrum"], #"profile spectrum"
            'MS:1000133' : [False, "name", "collision-induced dissociation"], #"collision-induced dissociation"
            'MS:1000285' : [False, "value", "total ion current"], #"total ion current"
            'MS:1000422' : [False, "name", "high-energy collision-induced dissociation"], #"high-energy collision-induced dissociation"
            'MS:1000511' : [False, "value", "ms level"], #"ms level"
            'MS:1000512' : [False, "name", "filter string"], #"filter string"
            'MS:1000514' : [False, "name", "m/z array"], #"m/z array"
            'MS:1000515' : [False, "name", "intensity array"], #"intensity array"
            'MS:1000521' : [False, "name", "32-bit float"], #"32-bit float"
            'MS:1000523' : [False, "name", "64-bit float"], #"64-bit float"
            'MS:1000744' : [False, "value", "legacy precursor mz value "]  #legacy precursor mz value ...
        }
    def clearMSDict(self):
        self.MSDict = {}


    def createcvParamList(self):
        self.cvParamLocList = [
            ["cvParam"],
            ["scanList","cvParam"],
            ["scanList","scan","cvParam"],
            ["scanList","scan","scanWindowList", "scanWindow","cvParam"],
            ["precursorList", "cvParam"],
            ["precursorList","precursor", "cvParam"],
            ["precursorList","precursor","isolationWindow", "cvParam"],
            ["precursorList","precursor","selectedIonList", "cvParam"],
            ["precursorList","precursor","selectedIonList","selectedIon", "cvParam"],
            ["precursorList","precursor","activation", "cvParam"],
            ["binaryDataArrayList", "cvParam"],
            ["binaryDataArrayList","binaryDataArray" ,"cvParam"]

        ]

    def addcvParamLocList(self, addList):
        """
        Used to add a list as a path to a cvParam to get cvParam data from there
            :param
                addList: list with the path to the access target, currently only additional cvParams are enabled
        """
        self.cvParamLocList.append(addList)

    def setFromDict(self, currentDict):
        """
        Function to build MSDict from a dictionary (e.g. for seeking)
        :param currentDict: Dict that represents the data of the spectrum
        :return:
        """
        self.clearMSDict()
        self.spectrum = currentDict
        self.seekDict(currentDict)
        self.MSDict["MS:1000514"] = currentDict.get("mzArray")
        self.MSDict["MS:1000515"] = currentDict.get("intensityArray")


    #used to iterate over dict
    def seekDict(self, currentDict):
        for key in currentDict:
            if key == "cvParam" and currentDict.get(key) is not None:
                for cvParam in currentDict[key]:
                    accession = cvParam.get("accession")
                    self.MSDict[accession] = cvParam

            elif isinstance(currentDict[key], dict):
                self.seekDict(currentDict[key])
            elif isinstance(currentDict[key], list) and key != "mzArray" and key != "intensityArray":
                for element in currentDict[key]:
                    self.seekDict(element)

    def getSpectrum(self):
        """
        Returns a representation of the currently loaded spectrum, either object or dictionary, depending on datasource
        (iterating returns object, seeking returns dictionary)
        :return: self.spectrum
        """
        return self.spectrum

    def getChromatogram(self, id):
        return self.chromaDict.get(id)


    def readMetaData(self):
        metaReader = pyavroc.AvroFileReader(self.metaDataFile, types=False)
        for item in metaReader:
            self.metaData = item
        self.metaDatatoDict(self.metaData)
        self.createChromaDict()


    def metaDatatoDict(self, metaData):
        for item in metaData:
            if item == "cvParam":
                if isinstance(metaData[item], list):
                    for cvParam in metaData[item]:
                        self.metacvDict[cvParam.get("accession")] = cvParam
                if isinstance(metaData[item], dict):
                    self.metacvDict[metaData[item].get("accession")] = metaData[item]

                else:
                    try:
                        for cvParam in metaData[item]:
                            self.metacvDict[cvParam.get("accession")] = cvParam
                    except:
                        pass
            elif isinstance(metaData[item], dict):
                self.metaDatatoDict(metaData[item])
            elif isinstance(metaData[item], list) and item not in ["timeArray", "intensityArray"]:
                for data in metaData[item]:
                    if isinstance(data, dict):
                        self.metaDatatoDict(data)
                    else:
                        print("Non handled data: ", data)

    def createChromaDict(self):
        if self.metaData.get("chromalist") is not None:
            for data in self.metaData.get("chromalist"):
                self.chromaDict[data.get("name")] = self.metaData.get("chromalist")