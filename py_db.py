import pymongo

MONGODB_URI= 'mongodb://evasilev:12345678@ds049456.mlab.com:49456/py_db'
client = pymongo.MongoClient(MONGODB_URI)
