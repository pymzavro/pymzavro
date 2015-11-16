Installation:
Needed with python 2.7:
    - pymzml
    - pyavroc
pyavroc can cause errors when the spectrum data is too big, so before installing you need to change the size of the
PYAVROC_BLOCK_SIZE.
To do this go to the src directory of pyavroc, open the file filewriter.c and change the line:
#define PYAVROC_BLOCK_SIZE (128 * 1024)
to
#define PYAVROC_BLOCK_SIZE (256 * 2048)

just install pyavroc as shown in the documentation of pyavroc. Please note that dict file writting needs to be enabled
to be able to write data to the file, which is not implemented in older versions.


Read Data:
#import need files
from pyavroReader import pymzAvroReader

#create pymzAvroObject with filename/path to the avro file

reader = pymzAvroReader(file)

reader always returns an object of type avroSpectrum

#to seek for spectrum with index:
reader.advSeek(index)

#to iterate over file:
for spectrum in reader:

#avroSpectrum:
#loads data from cvParam childs in mzML to self.MSDict which can be accessed via Obo Tag:
spectrum.iterOvercvParam() -> loading cvParam data
spectrum.getByAccession(accession) -> returns the data stored in self.MSDict from under the obo tag

#to access mz/i:
spectrum.get_mz 		-> returns mzList
spectrum.get_intensity   	-> returns intensityList


Write Data:
#for mzML Data:
#initilize class pyavroWriter with mzML, avsc and typeDict:
foo = pyavroWriter(mzmlFile, "spectrum.json", "typeDict.json", filename = myFileName)
foo.writefastavro(codec="deflate")
