'''
Created on Jan 18, 2016

@author: user
'''
import logging.config
import os
import product.com.resources as res
def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

@singleton
class Logger():
    logConfigFilePath = ''
    def __init__(self):
        self.logConfigFilePath = os.path.dirname(res.__file__)
        logging.config.fileConfig(os.path.join(self.logConfigFilePath,'Logging.conf'))
        self.logr = logging.getLogger('root')