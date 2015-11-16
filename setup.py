from __future__ import print_function

#!/usr/bin/env python3
__author__ = 'marius'

from distutils.core import setup


setup(
    name = "pymzavro",
    version = "0.3",
    packages = ["pymzavro"],
    package_dir = {'pymzavro': 'pymzavro'},
    #data_files=[("/usr/local/lib/python2.7/dist-packages/pymzavro/data", \
    #             ["data/typeDict.json", "data/mzMLFull.avsc", "data/spectrum.avsc"])]
)

print("Finished installing pymzavro")


