'''
Created on Feb 4, 2016

@author: jaya
'''
from   product.com.loggings.log_conf import Logger
from   product.com.loggings import Chrono
from   product.com.utils.mongoDb import DB
from   time import clock
import pymongo
import json,csv
import sys
import pandas as pd
import traceback
#import Timing

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
    #This MONGO_FIELDS is being overridden!
    MONGO_FIELDS = ['tweet_id', 'tweet_posted_time',
                    'tweet_author_id','tweet_disp_name','tweet_author_bio',
                    'Follower_count','friends_count','tweet_author_location',
                    'timezone','Verified','Retweeted_count','Favourite_Count',
                    'generator_Name','Object_Type','id','summary','tweet_country',
                    'city', 'tweet_lang','lat','lon','ALTLAT','ALTLON','tweet_text',
                    'link']
    
    def import_content(self,filename):
        '''
        import the contents to the MongoDB
        CSV file is the only supported type as of now
        @param filename:The filename which contains the data to be imported to Mongo.
                        Should be a csv file
        '''
        try:
            tstart = clock()
            self.log.debug("Importing Contents into Mongo")
            reload(sys)
            sys.setdefaultencoding("utf-8")
            db_name         = self.db.db_name
            host            = self.db.host
            port            = int(self.db.port)
            username        = self.db.username
            password        = self.db.password
            collection_name = self.db.collection_name
            mng_client = pymongo.MongoClient(host, port)
            mng_db     = mng_client[db_name] # Replace mongo db name
            #self.log.debug(mng_db.authenticate(username, password,mechanism='SCRAM-SHA-1'))
            try:
                auth = (mng_db.authenticate(self.db.username, self.db.password,mechanism='SCRAM-SHA-1'))
                if(auth):
                    self.log.debug("MongoDB authentication Successful.Import will now Continue")
            except:
                self.log.debug("Database Authentication Failure.Incorrect Username/and or Password.")
                exit()
            #collection_name = 'mc' # Replace mongo db collection name
            db_cm = mng_db[collection_name]
            file_res = "D:\\File\\MC\\Test_Nukes\\ParsedCSVData.csv"
            data = pd.read_csv(file_res)
            #self.log.debug(data)
            data_json = json.loads(data.to_json(orient='records'))
            db_cm.insert(data_json)
            mng_client.close()
            tstop = clock()
            self.log.debug("Import took %s",Chrono.secondsToStr(tstop-tstart)) 
        except :
            traceback.print_exc()
        
    def createHeader(self,header):
        '''
        create a header list from the MONGO_HEADER
        '''
        
        preHeader = (",".join(header))
        procHeader = preHeader.replace("'","")
        return procHeader
        
    def export_content(self,filename):
        '''
        Exports the content of the MongoDB in the specified collection to a CSV file format
        Only CSV formats are supported as of Now
        
        '''
        #print pymongo.version
        #Encoding change is global.Need a better solution
        tstart = clock()
        self.log.debug("Exporting MongoDB Data to a CSV file")
        reload(sys)
        sys.setdefaultencoding("utf-8")
        ##################################################
        db_name         = self.db.db_name
        mng_client      = pymongo.MongoClient(self.db.host, int(self.db.port))
        mng_db          = mng_client[db_name]                                                          # Replace mongo db name
        try:
            auth = (mng_db.authenticate(self.db.username, self.db.password,mechanism='SCRAM-SHA-1'))
            if(auth):
                self.log.debug("MongoDB authentication Successful.Export will now continue")
        except:
            self.log.debug("Database Authentication Failure.Incorrect Username/and or Password.")
            exit()
        collection_name = self.db.collection_name                                                      # Replace mongo db collection name
        db_cm           = mng_db[collection_name]
        self.log.debug(db_cm.find())
        #############################
        #self.log.debug(reduce(lambda all_keys, rec_keys: all_keys | set(rec_keys), map(lambda d: d.keys(), db_cm.find()), set()))
        #############################
        try:
            doc=db_cm.find_one();
            self.MONGO_FIELDS=[]
            for key in doc :
                self.MONGO_FIELDS.append(key);
            cursor          = db_cm.find({},{'_id':0})   
            with open(filename, 'w+') as fp:
                fields = self.MONGO_FIELDS
                writer = csv.DictWriter(fp, fieldnames=fields,lineterminator = '\n',quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for r in cursor:
                    print r
                    writer.writerow(r)
            self.log.critical("Export Complete!Flushing CSV file and closing sockets.")
            tstop = clock()
            self.log.debug("Export took %s",Chrono.secondsToStr(tstop-tstart))
        except Exception as ex:
            self.log.debug("Failed to obtain the collection from DataBase.Is the Database service running?")
            traceback.print_exc()
            mng_client.close()
            
    def __init__(self):
        self.log.debug("Initializing a MongoInstance from the Configuration file..")
        self.db = DB()
        self.log.debug( self.db )
        

#d = DbHelper()
#d.import_content(filename="D:\\File\\MC\\Test_Nukes\\ParsedCSVData.csv")
#d.export_content(filename="D:\\File\\mongoData5.csv")