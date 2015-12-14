import pymzavro

def test_read():
    print("======sequential read test======")
    avroFile = open("BSA3.avro")
    avroFileMeta = open("BSA3_meta.avro")
    reader = pymzavro.reader.PymzAvroReader(avroFile, avroFileMeta)

    isum = 0
    ms_level = 0
    for spectrum in reader:
        isum = isum +  sum(spectrum.getIntensityArray())
        ms_level = ms_level + int(spectrum.getByAccession("MS:1000511"))
    print (isum)
    print (ms_level)

    print("=====index seek======")
    try:
        avroFileSeek = open("BSA3.avro")
        indexReader = pymzavro.reader.PymzAvroReader(avroFileSeek, indexFile="BSA3_index.json")
        spectrum = indexReader.rndSeek(694)
        print(sum(spectrum.getIntensityArray()))
    except:
        print("Could not test file seek")


    return 1