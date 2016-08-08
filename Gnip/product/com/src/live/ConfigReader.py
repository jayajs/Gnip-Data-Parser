'''
Created on Jan 18, 2016

@author: jaya
'''
import ConfigParser,os
import product.com.src.live.TwitterAuth as TwitterAuth
from   product.com.loggings.log_conf import Logger
import sys,traceback
import product.com.resources as res
class ConfigReader(object):
    log = Logger.logr
    configFilePath = ''
    '''
    '''
    def parseNow(self):
        try:
            self.configFilePath = os.path.dirname(res.__file__)
            self.log.debug('Starting parsing of Authentication Configuration file')
            config = ConfigParser.ConfigParser()
            #self.log.debug(os.path.dirname(res.__file__))
            self.log.debug(os.path.join(self.configFilePath,'AuthConfig.cfg'))
            config.read(os.path.join(self.configFilePath,'AuthConfig.cfg'))
            self.log.debug(config.sections())
            access_token        = config.get('Authentication_Section', 'access_token')
            self.log.debug("Token ="+ access_token)
            access_token_secret = config.get('Authentication_Section', 'access_token_secret')
            consumer_key        = config.get('Authentication_Section', 'consumer_key')
            consumer_secret     = config.get('Authentication_Section', 'consumer_secret')
            #create an objrct here
            twiiter_auth_details = TwitterAuth
            twiiter_auth_details.access_token        = access_token
            twiiter_auth_details.access_token_secret = access_token_secret
            twiiter_auth_details.consumer_key        = consumer_key
            twiiter_auth_details.consumer_secret     = consumer_secret
            return twiiter_auth_details
        except Exception :
            self.log.critical("Error Please check the Authentication Config File ( AuthConfig.cfg ) for Errors")
            traceback.print_exc(file=sys.stdout)
    def run (self):
        twitterauth = self.parseNow()
        return twitterauth
configreader = ConfigReader()
configreader.run()



        
        