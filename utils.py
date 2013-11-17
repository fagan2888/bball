from dateutil import parser as dateparser
from datetime import datetime, timedelta
from pymongo import MongoClient
import time

def get_db():
    conn = MongoClient()
    return conn['nba']

def day_gen(start_day = None):
    """ returns datetime objects for every day between start_day and now """
    if not start_day:
        start_day = '2012-10-13'
    cur = dateparser.parse(start_day)
    stop = datetime.now()

    inc = timedelta(days=1)

    while cur < stop:
        yield cur
        cur += inc

def timeit(fn):
    """
    decorator for timing funcs!
    """
    def timed(*args,**kwargs):
        start = time.time()
        resp = fn(*args,**kwargs)
        print "took %0.3f seconds" % (time.time()-start)
        return resp
    return timed
