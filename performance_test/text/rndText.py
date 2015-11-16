__author__ = 'marius'
import random
random.seed

filewriter = open("text.txt", "w")

for i in range(100000000):
    filewriter.write(chr(random.randint(0,100)))
    filewriter.write(" ")