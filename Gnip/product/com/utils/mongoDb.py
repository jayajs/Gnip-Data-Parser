'''
Created on Feb 3, 2016

@author: jaya
'''
import product.com.resources.db as res
import os
import ConfigParser,sys
import traceback
from   product.com.loggings.log_conf import Logger

class DB(object):
    '''
    Class to represent an instance of a mongoDB
    
    '''
    log = Logger.logr
    username = ""
    password = ""
    db_name = ""
    collection_name = ""
    host = ""
    port = ""
    def parseNow(self):
        '''
        Function extracts the  required parameters for mongoDB connection from a cfg file
        '''
        try:
            cfgFileName = "mongo.cfg"
            self.configFilePath = os.path.dirname(res.__file__)
            self.log.debug('Starting parsing of MongoDB Configuration file %s',cfgFileName)
            config = ConfigParser.ConfigParser()
            #self.log.debug(os.path.dirname(res.__file__))
            self.log.debug(os.path.join(self.configFilePath,cfgFileName))
            config.read(os.path.join(self.configFilePath,cfgFileName))
            self.log.debug(config.sections())
            #############################################################################
            self.db_name                = config.get('MongoDBConfig', 'db_name')
            self.collection_name        = config.get('MongoDBConfig', 'collection_name')
            self.username               = config.get('MongoDBConfig', 'user_name')
            self.host                   = config.get('MongoDBConfig', 'host')
            self.port                   = config.get('MongoDBConfig', 'port')
            self.password               = config.get('MongoDBConfig', 'password')
            self.log.debug("MongoDB Configurations are :")
            self.log.debug("collection_name ="+self.db_name)
            self.log.debug("username = "+self.username)
            self.log.debug("host = "+self.host)
            self.log.debug("port = "+self.port)
            self.log.debug("password = "+self.password)
            self.log.debug("db_name = "+self.db_name)
            ###############################################################################
        except Exception :
            self.log.critical("Error Please check the Authentication Config File ( mongo.cfg ) for Errors")
            traceback.print_exc(file=sys.stdout)
    def __init__(self):
        '''
        Constructor
        '''
        db = self.parseNow()
        return db
