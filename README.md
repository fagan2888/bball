bball
=====

place to do some basketball hacking

## requirements
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
