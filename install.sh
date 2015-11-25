#!/bin/bash

#clones pyavroc
git clone https://github.com/MariusDieckmann/pyavroc.git
cd pyavroc
./clone_avro_and_build.sh
python setup.py install

#install fastavro
#pip install fastavro


#install pymzavro
cd ..
python setup.py install

# TODO create errors
#cd /home/marius/Pycharm/pymzavro_test

