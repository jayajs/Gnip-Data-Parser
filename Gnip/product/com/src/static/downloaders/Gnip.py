'''
Created on Jan 19, 2016

@author: jaya
'''
import ConfigParser,os,sys,traceback
import product.com.resources as res
from   product.com.loggings.log_conf import Logger

class Gnip(object):
    gnipUrlsJsonPath = ''
    gnipOutputPath =''
    gnipErrorPath = ''
    gnipCSVOutPath = ''
    tempPath=''
    failedUrls = 0
    gnipmaxthreads =1
    log = Logger.logr
    #################
    #################
    def parse(self):
        try:
            self.failedUrls = 0
            self.tempPath = os.path.dirname(res.__file__)
            self.log.debug('Starting parsing of GNIP Configuration file')
            config = ConfigParser.ConfigParser()

            config.read(os.path.join(self.tempPath,'GnipConfigs.cfg'))
            self.log.debug(config.sections())
            self.gnipUrlsJsonPath      = config.get('GNIP', 'urlsJsonPath')
            self.gnipOutputPath        = config.get('GNIP', 'outputJsonPath')
            self.gnipErrorPath         = config.get('GNIP', 'ErrorFilePath')
            self.gnipmaxthreads        = config.get('GNIP', 'MaxThreadCount')
            self.gnipCSVOutPath        = config.get('GNIP', 'ParsedCSVFilePath')
            #log possible errors
            self.log.debug(self.gnipUrlsJsonPath)
            self.log.debug(self.gnipOutputPath)
            self.log.debug(self.gnipErrorPath)
        except Exception,e:
            self.log.error("Critical Error During Configuration Parsing.Please Check Gnip Config file for Errors..Exiting")
            self.log.exception(e)
            
    def run(self):
        g = Gnip()
        g.parse()
        self.log.debug("Returning  gnipUrlsJsonPath As "+g.gnipUrlsJsonPath)
        self.log.debug("Returning  gnipUrlsJsonPath As "+g.gnipOutputPath)
        self.log.debug("Returning  gnipUrlsJsonPath As "+g.gnipErrorPath)
        #self.log.debug("Returning  gnipUrlsJsonPath As "+self.gnipUrlsJsonPath)
        return g