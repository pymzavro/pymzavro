__author__ = 'marius'

import sys
import pprint
import csv

from TIC_test import TestingMethods


def pymzavroTest(iterations, file):
    timeList = []
    for i in range(iterations):
        test = TestingMethods(avroFile=file)
        timeList.append(test.pymzavro())

    return timeList

def pyOpenMSStreamTest(iterations, file):
    timeList = []
    for i in range(iterations):
        test = TestingMethods(mzMLFile=file)
        timeList.append(test.pyOpenMSStream())

    return timeList


def pymzMLTest(iterations, file):
    timeList = []
    for i in range(iterations):
        test = TestingMethods(mzMLFile=file)
        timeList.append(test.pymzMLTest())

    return timeList

def pyOpenMSregular(iterations, file):
    timeList = []
    for i in range(iterations):
        test = TestingMethods(mzMLFile=file)
        timeList.append(test.pyOpenMSregular())

    return timeList


def test_all():
    timeDict = {}
    iterations = int(sys.argv[1])
    mzMLFile = sys.argv[2]
    avroFile = sys.argv[3]

    print("==Testing pymzavro==")
    timeDict["pymzavro"] = pymzavroTest(iterations, avroFile)

    print("==Testing pyOpenMSStream==")
    timeDict["pyOpenMSStream"] = pyOpenMSStreamTest(iterations, mzMLFile)

    print("==Testing pymzML==")
    timeDict["pymzML"] = pymzMLTest(iterations, mzMLFile)

    #print("==Testing pyOpenMSregular==")
    #timeDict["pyOpenMSregular"] = pyOpenMSregular(iterations, mzMLFile)

    pp = pprint.PrettyPrinter()
    pp.pprint(timeDict)

    with open('mycsvfile.csv', 'wb') as f:
        w = csv.writer(f)
        for key in timeDict:
            curList = [key]
            curList.extend(timeDict[key])
            w.writerow(curList)


test_all()
