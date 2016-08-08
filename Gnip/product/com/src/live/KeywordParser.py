'''
Created on Jan 18, 2016

@author: jaya
'''
import product.com.resources as res
from product.com.loggings.log_conf import Logger
import os,ConfigParser,traceback,sys
class KeyWordParser(object):
    '''
    classdocs
    '''
    log = Logger.logr
    keywords = []
    keywordsCfgFilePath = ''
    def getKeywords(self):   
        try:
            rootpath = os.path.dirname(res.__file__)
            self.keywordsCfgFilePath = os.path.join(rootpath,'keywords.cfg')
            self.log.debug('Parsing Keywords CFG file @ '+self.keywordsCfgFilePath)
            config = ConfigParser.ConfigParser()
            config.read(self.keywordsCfgFilePath)
            self.log.debug(config.sections())
            readKeywords = config.get('keywords', 'keywords')
            self.keywords = readKeywords.split(',')
            self.log.debug(self.keywords)
            return  self.keywords
        except Exception :
            self.log.critical("Error Please check the Keyword Config File ( keywords.cfg ) for Errors")
            traceback.print_exc(file=sys.stdout)
    def __init__(self):
        '''
        Constructor
        '''
        self.log.debug( 'Starting Processing of Keywords File')
        self.getKeywords()
#key = KeyWordParser()