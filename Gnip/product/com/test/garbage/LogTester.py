'''
Created on Jan 18, 2016

@author: user
'''
from product.com.loggings.log_conf import Logger
print "Hello"
log = Logger.logr
Logger.logr.debug("Hello")

def run():
    log.debug('In Run')
run()    
    