__author__ = 'marius'

from boundsumtest import Boundsumtest as TestingMethods
import pprint
import csv
import sys

timeDict = {
        "pymzavro" : []
    }

def pymzavroTest(file):
    timeList = []
    test = TestingMethods(avroFile=file)
    ttime =test.boundavro()

    return ttime

def pyOpenMSStreamTest(file):
    timeList = []
    test = TestingMethods(mzMLFile=file)
    timeList.append(test.pyOpenMSStream())

    return timeList



def pymzMLTest(file):
    timeList = []
    test = TestingMethods(mzMLFile=file)
    timeList.append(test.pymzMLTest())

    return timeList

def pyOpenMSregular(file):
    timeList = []
    test = TestingMethods(mzMLFile=file)
    timeList.append(test.pyOpenMSregular())

    return timeList


def test_all():
    mzMLFile = sys.argv[2]
    avroFile = sys.argv[3]

    print("==Testing pymzavro==")
    #timeDict["pymzavro"].append(pymzavroTest(avroFile))

    print("==Testing pyOpenMSStream==")
    #timeDict["pyOpenMSStream"] = pyOpenMSStreamTest(mzMLFile)

    print("==Testing pymzML==")
    #timeDict["pymzML"] = pymzMLTest(mzMLFile)

    print("==Testing pyOpenMSregular==")
    timeDict["pyOpenMSregular"] = pyOpenMSregular(mzMLFile)

    pp = pprint.PrettyPrinter()
    pp.pprint(timeDict)


def writecsv():
    with open("time.csv", 'wb') as f:
        w = csv.writer(f)
        for key in timeDict:
            curList = [key]
            curList.extend(timeDict[key])
            w.writerow(curList)


iterations = int(sys.argv[1])

for i in range(iterations):
    test_all()
    writecsv()