'''
Created on Jan 20, 2016

@author: user
'''
dbname = "mc"
dataPath = "C:\\data\\db"
from pymongo import MongoClient
import time
#import subprocess
time.sleep(10)
client = MongoClient()
#client.mc.authenticate('jayajs', 'jaya', mechanism='SCRAM-SHA-1')
print client
db = client.mc
print(db.authenticate('jayajs', 'jaya',mechanism='SCRAM-SHA-1'))
cursor= db.collections.find()
print cursor
for document in cursor:
    print(document)
client.close()