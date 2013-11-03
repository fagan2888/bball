from dateutil import parser as dateparser
from datetime import datetime, timedelta
from pymongo import MongoClient

def get_db():
    conn = MongoClient()
    return conn['nba']

def day_gen(start_day = '20121030'):
    """ returns datetime objects for every day between start_day and now """
    cur = dateparser.parse(start_day)
    stop = datetime.now()

    inc = timedelta(days=1)

    while cur < stop:
        yield cur
        cur += inc


            

    
