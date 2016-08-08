'''
Created on Jan 28, 2016

@author: user
'''

import re
#import pandas as pd
class PreProcessor(object):
    '''
    PreProcessor class to clean the tweets
    Core PreProcessing Logic Goes in processTweet Function
    The function should return the Pandas column it got when the func 
    was called
    '''
    def processTweet(self,tweet):
        # process the tweets
        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
        return tweet
        #end
#what data type am i expecting here 
p = PreProcessor()
tweets = "RT @businessinsider: Why Samsung Pay could gain an early lead in mobile payments http://t.co/N8pQqKst1u http://t.co/iAI0iWJgeu"
print (p.processTweet(tweets))