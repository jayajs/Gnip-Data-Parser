'''
Created on Jan 18, 2016

@author: user
'''
#from product.com.loggings.log_conf  import Logger
class Authentication(object):
    '''
    Class handles all the twitter authentication related params
    '''
    access_token        = "XXXXXXXXXXXXXXXXXXXXXX"
    access_token_secret = "XXXXXXXXXXXXXXXXXXXXXX"
    consumer_key        = "XXXXXXXXXXXXXXXXXXXXXX"
    consumer_secret     = "XXXXXXXXXXXXXXXXXXXXXX"
        
    def __init__(self, params):
        '''
        Constructor
        '''
        
        