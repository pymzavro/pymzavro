#!//usr/bin/env python


import pydoop.mapreduce.api as api
import pydoop.mapreduce.pipes as pp
from pydoop.avrolib import AvroContext

class Mapper(api.Mapper):

    def map(self, ctx):
        spectrum = ctx.value
        mzsum = sum(spectrum["mzArray"])
        ctx.emit("a", mzsum)

class Reducer(api.Reducer):

    def reduce(self, ctx):
        ctx.emit(ctx.key, sum(ctx.values))

def __main__():
    factory = pp.Factory(mapper_class=Mapper, reducer_class=Reducer)
    pp.run_task(factory, private_encoding=True, context_class=AvroContext)