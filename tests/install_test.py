__author__ = 'marius'
import os
import schemawrite_test
import write_test
import read_test


def smallTest():
    schemawrite_test.schema_creator()
    write_test.test_write()
    data = read_test.test_read()
    delete_files()
    print(data)
    return 1

def delete_files():
    os.remove ("BSA3.avro")
    os.remove ("BSA3_meta.avro")
    os.remove ("BSA3_index.json")
    os.remove("fullSchema.avsc")
    os.remove("spectrum.avsc")
    os.remove("typeDict.json")


def test_answer():
	assert smallTest() == 1


test_answer()
