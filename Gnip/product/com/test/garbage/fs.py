'''
Created on Jan 20, 2016

@author: user
'''
from   product.com.loggings.log_conf import Logger
from product.com.utils.mongoDb import DB
import  pymongo
import json,csv
import io,sys
import pandas as pd

class DbHelper(object):
    '''
    Class behaves as a helper to interface betwwen caller and MongoDB.
    Class handles two methods import_collection ,used to import a csv file into the mongoDB
    export_collection is used to flush the MongoDB contents to a csv file on to the local storage.
    
    @todo: Removal of HardCoded Filepath
    '''
    log = Logger.logr
    dbname = ''
    db = ''
    MONGO_FIELDS = ['tweet_id', 'tweet_posted_time',
                    'tweet_author_id','tweet_disp_name','tweet_author_bio',
                    'Follower_count','friends_count','tweet_author_location',
                    'timezone','Verified','Retweeted_count','Favourite_Count',
                    'generator_Name','Object_Type','id','summary','tweet_country',
                    'city', 'tweet_lang','lat','lon','ALTLAT','ALTLON','tweet_text',
                    'link']
    
    def import_content(self,filename):
        db_name         = self.db.db_name
        host            = self.db.host
        port            = int(self.db.port)
        username        = self.db.username
        password        = self.db.password
        collection_name = self.db.collection_name
        mng_client = pymongo.MongoClient(host, port)
        mng_db = mng_client[db_name] # Replace mongo db name
        self.log.debug(mng_db.authenticate(username, password,mechanism='SCRAM-SHA-1'))
        #collection_name = 'mc' # Replace mongo db collection name
        db_cm = mng_db[collection_name]
        file_res = "D:\\File\\MC\\Test_Nukes\\ParsedCSVData.csv"
        data = pd.read_csv(file_res)
        #self.log.debug(data)
        data_json = json.loads(data.to_json(orient='records'))
        db_cm.insert(data_json)
        mng_client.close()  
        
    def createHeader(self,header):
        preHeader = (",".join(header))
        procHeader = preHeader.replace("'","")
        return procHeader
        
    def export_content(self,filename):
        #print pymongo.version
        sys.getdefaultencoding()
        reload(sys)
        sys.setdefaultencoding('utf-8')
        db_name         = self.db.db_name
        mng_client      = pymongo.MongoClient(self.db.host, int(self.db.port))
        mng_db          = mng_client[db_name]                                                # Replace mongo db name
        self.log.debug(mng_db.authenticate(self.db.username, self.db.password,mechanism='SCRAM-SHA-1'))
        collection_name = self.db.collection_name                                                      # Replace mongo db collection name
        db_cm           = mng_db[collection_name]
        self.log.debug(db_cm.find())
        ############################
        ############################
        ############################
        #self.log.debug(reduce(lambda all_keys, rec_keys: all_keys | set(rec_keys), map(lambda d: d.keys(), db_cm.find()), set()))
        doc=db_cm.find_one();
        self.MONGO_FIELDS=[]
        for key in doc :
            self.MONGO_FIELDS.append(key);
        cursor          = db_cm.find({},{'_id':0})   
        with open(filename, 'w+') as fp:
            fields = self.MONGO_FIELDS
            writer = csv.DictWriter(fp, fieldnames=fields,lineterminator = '\n')
            writer.writeheader()
            for r in cursor:
                print r
                writer.writerow(r)
    def __init__(self):
        self.db = DB()
        self.log.debug( self.db )

d = DbHelper()
#d.import_content(filename="D:\\File\\MC\\Test_Nukes\\ParsedCSVData.csv")
d.export_content(filename="D:\\File\\mongoData.csv")