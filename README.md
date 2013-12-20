bball
=====

place to do some basketball hacking

requirements
------------
+ python
    * requests
	* beautifulsoup 4
    * flask
	* pymongo
	* numpy
	* matplotlib
+ mongodb

To install the required python modules, use pip.

mongo
-----
set it up...

to query by shot position, we should set up a 2dim index in the mongo 
collection.

db.shots.ensureIndex({"pos":"2d"})

http://docs.mongodb.org/manual/reference/operator/query/center/

files
-----
+ `epsn.py`
    * populate mongodb database `nba` with shot, game data from ESPN website
    * imports
        - `utils.py`
+ `api.py`
    * flask-based web app to interact with mongodb
    * imports
        - `utils.py`
        - `shot_filters.py`: filters for mongodb interaction
        - `shotchart.py`: create shot chart

TODO
----
match game / shot data to teams
create game filter:
  * filter by day
  * filter by month
  * filter by season
  * filter by reg season v playoffs
  * filter by team?
prettify shotcharts
add some basic auth to mongo
