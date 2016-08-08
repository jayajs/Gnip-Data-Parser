'''
Created on Jan 18, 2016

@author: jaya
'''
from tweepy.streaming import StreamListener
from product.com.loggings.log_conf import Logger
from tweepy import OAuthHandler
from tweepy import Stream
from product.com.src.live.ConfigReader import ConfigReader
from examples.streaming import StdOutListener
from product.com.src.live.KeywordParser import KeyWordParser
import os, ConfigParser, time
import product.com.outputs as outputs
import product.com.resources as res
class StdOutListener(StreamListener):
    '''
    Collector class  deals with the collection process for the twitter live data stream
    '''
    KeywordParser = KeyWordParser()
    prefixoutRootDir = ''
    log = Logger.logr
    counter = 0
    output=''
    def on_data(self, data):
        #print data
        self.output.write(data+"\n")
        self.counter+1
        if self.counter >2000:
            self.output.close()
            self.output = open(self.prefixoutRootDir + '\\' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        return True
        

    def on_error(self, status):
        print status
    
    def collect(self,keywords):
        '''
        Start collecting tweets from twitter called from run()
        @param keywords for filtering tweets: 
        '''
        sol = StdOutListener()
        log = Logger.logr
        #####################################################        
        cfgReader = ConfigReader()
        log.debug('starting collector')
        authenticationData = cfgReader.run()
        log.debug("Access token =" +authenticationData.access_token)
        log.debug("Access secret =" +authenticationData.access_token_secret)
        log.debug("consumer key =" +authenticationData.consumer_key)
        log.debug("consumer secret =" +authenticationData.consumer_secret)
        log.debug(keywords)
        auth = OAuthHandler(authenticationData.consumer_key, authenticationData.consumer_secret)
        auth.set_access_token(authenticationData.access_token, authenticationData.access_token_secret)
        stream = Stream(auth, sol)
        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        log.debug('Hooked on API, Starting Live Collection Now.........')
        stream.filter(track=keywords)
    
    def run(self):
        '''
        start the Collector 
        '''
        keyword = self.KeywordParser.getKeywords()
        self.log.debug(keyword)
        self.collect(keyword)
    def __init__(self):
        '''
        '''
        config = ConfigParser.ConfigParser()
        configFilePath = os.path.dirname(res.__file__)
        self.log.debug(configFilePath)
        config.read(os.path.join(configFilePath,'TweetsOutFilePath.cfg'))
        self.prefixoutRootDir = config.get('TweetOutputDir', 'OutputDir')
        self.output = open(self.prefixoutRootDir + '\\' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.log.debug(self.output)

