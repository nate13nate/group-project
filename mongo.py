import pymongo

try:
    mongo = pymongo.MongoClient(
        host = 'localhost',
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.local
    mongo.server_info() #trigger exception if cannot connect to db
except:
    print('Error -connect to db')
