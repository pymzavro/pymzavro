from __future__ import print_function

#!/usr/bin/env python
__author__ = 'marius'

from distutils.core import setup


setup(
    name = "pymzavro",
    version = "0.3",
    packages = ["pymzavro"],
    package_dir = {'pymzavro': 'pymzavro'},
    package_data={'data': ['data/mzML1.1.0.xsd']},

)

print("Finished installing pymzavro")


