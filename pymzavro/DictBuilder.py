__author__ = 'marius'


import xml.etree.ElementTree as ET
import pprint
from DictComplex import DictComplex
from AvscMaker import Partconverter

#Usage: execute xsdParser.py


class DictBuilder:
    def __init__(self):

        self.complexdict = {}

        # not complete, some types that are not present in mzML are missing, not sure how to deal with base64Binary -> maybe decode before putting into avro?
        self.replaceDict = {"xs:string" : "string", "xs:nonNegativeInteger" : "int", "xs:IDREF" : "string", "xs:ID" : "string", "xs:anyURI" : "string", "xs:int": "int", "xs:dateTime" : "string", "xs:base64Binary" : "string"}


    #starting point
    def buildDict(self, xsd):
        tree = ET.parse(xsd)
        root = tree.getroot()

        for child in root:
            #looks for complex Types in child of xsd root, outputs dicts
            if "complexTyp" in child.tag:
                self.complexdict.update({child.attrib["name"] : self.contentMaker(child)})
            else:
                #checks for unhandled tags
                self.rootName = child.attrib["name"]
                pass
        return self.complexdict


    #builds dicts of Complex Types
    def contentMaker(self, child):
        contentNode = child
        dict = {}
        attribDict = {}
        for child in contentNode:
            if "attribute" in child.tag:
                dict.update(self.attribMaker(child.attrib))
            elif "sequence" in child.tag:
                dict.update(self.sequenceMaker(child))
            elif "complexContent" in child.tag:
                dict.update(self.extensionMaker(child))
                #self.extensionMaker(child)
                pass
        return dict

    #builds attributes
    def attribMaker(self, attributes):
        dict = {}
        valuedict = {}
        name = attributes["name"]
        #id has no type, is supposed to be a string
        if "id" in name:
            valuedict.update({"type" : "string"})
        else:
            for myTag in [ 'use', 'maxOccurs']:
                myattribute = attributes.get( myTag, None )
                if myattribute is not None:
                    valuedict[ myTag ] = myattribute

            #handles regular type (like string, id) that are defined in replace dict
            if "xs" in attributes["type"]:
                valuedict['type'] = self.replaceDict[attributes["type"]]

            else:
                valuedict["type"] = attributes["type"]



        dict[name] = valuedict
        return dict


    #builds sequences
    def sequenceMaker(self, sequence):
        dict = {}
        for child in sequence:
            dict.update(self.attribMaker(child.attrib))

        return dict


    #only for printing
    def pprint(self, toPrint):
        pp = pprint.PrettyPrinter()
        pp.pprint(toPrint)


    #handles extensions
    def extensionMaker(self, extension):
        tempDict = {}
        for child in extension:
            tempDict["extension"] = child.attrib["base"]
            extensionNode = child
            #adds attributes and sequences to the extension
            for extensionChild in extensionNode:
                if "attribute" in extensionChild.tag:
                    tempDict.update(self.attribMaker(extensionChild.attrib))
                elif "sequence" in extensionChild.tag:
                    tempDict.update(self.sequenceMaker(extensionChild))

                #check for elements that are not handled before
                else:
                    print("unhandled element")

        return tempDict

    def getRootName(self):
        return self.rootName


    # TODO rewrite this method, only passing

    def removeComplex(self):
        baa = DictComplex(self.complexdict)
        baz = baa.getnewDict("mzMLType")
        #self.pprint(baz)
        bee = {"mzML": {"type" : baz}}
        avscM = Partconverter(bee)