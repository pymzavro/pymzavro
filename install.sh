#!/bin/bash

# clones pyavroc and applies patch for deflte writing and bigger buffer
git clone https://github.com/Byhiras/pyavroc.git
cp patch.txt pyavroc
cd pyavroc
git apply patch.txt
./clone_avro_and_build.sh
python setup.py install

#install fastavro
pip install fastavro


#install pymzavro
cd ..
python setup.py install

# TODO create errors
#cd /home/marius/Pycharm/pymzavro_test

