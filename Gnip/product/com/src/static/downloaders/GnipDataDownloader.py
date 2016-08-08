'''
Created on Jan 19, 2016

@author: jaya
'''
import json
import requests, zipfile, StringIO
import threading
import time,os
#import product.com.resources as res
from   random import randint
from   product.com.src.static.downloaders.Gnip import Gnip
from   product.com.loggings.log_conf import Logger


class DataDownloader(object):
    '''
    class deals with Download of the Data from the URL's shared by the 
    GNIP.Creating an object of this class will trigger hte download from 
    the constructor 
    '''
    log = Logger.logr
    iid_lock = ''
    counter = 0
    threadLimiter = ''
    threads = '' 
    gnip =''
    def getData(self,gnipObj):
        '''
        Method parses the GnipURL json file
        @param gnipObj:A Gnip object 
        '''
        #path = "D:\\File\\MC\\Test_Nukes\\Urls.json"
        path = gnipObj.gnipUrlsJsonPath
        print path
        self.log.debug(path)
        with open(path ,'r') as data_file:  
            data = json.load(data_file)
        print data["urlList"]
        return data
    def retryFailures(self):
        '''
        Method retries for failures that occured during URL preocess and recorded
        in the error file 
        '''
        #read the error file once
        errfilename = "err.txt"
        errfile = self.gnip.gnipErrorPath+"\\"+errfilename
        errfilestat = os.stat(errfile)
        self.log.debug(errfilestat)
        if  errfilestat.st_size != 0:
            #Error has been recorded in err.txt file
            fp = open(errfile,'r')
            for site in fp.readlines():
                try:
                    self.fetch_url(site)
                except:
                    self.log.debug("Unable to Pass the following URL, %s , and was Skipped"%(site))       
        else:
            #no data in error file
            self.log.debug('No Data in Error file Detectd.How did i reach here?')
                  
    def fetch_url(self,site,gnip) :
        '''
        Method Gets the information/Data for a particular URL and then
        goes for Unzipping this data and storage on the disk 
        @param site: url to be processed
        @param gnip:a Gnip object
        
        '''      
        self.threadLimiter.acquire(); 
        try:
            request = requests.get(site)
            #All the random number generation is used to introduce a slight delay to prevent Thread Interference
            #output = self.gnip.gnipOutputPath+"\\"+"GNIP_%s_Results_%s_%s"%(time.time(),randint(0,50000),randint(0,20000))
            output = self.gnip.gnipOutputPath
            zipfiles = zipfile.ZipFile(StringIO.StringIO(request.content))
            zipfiles.extractall(output)
            zipfiles.close()
            request.close()
     
        except Exception:
            print "Missed a URL and this shall be Recorded for further tries"
            time.sleep(1)
            with self.iid_lock:
                errfile = open("D:\\File\\MC\\Test_Nukes\\err.txt", "a")
                errfile.write(site+"\n")
                errfile.close()
                self.gnip.failedUrls = self.gnip.failedUrls + 1
                self.log.debug("Error parsing a URL ,This URL is logged in Error File ,\
                Current Failure Count = %s"% self.gnip.failedUrls)
        finally:
            print
            self.threadLimiter.release()                      
            #save
    def __init__(self):
        '''
        Constructor:Deals with class init
        '''
        newgnip = Gnip().run()
        self.gnip = newgnip
        data = self.getData(newgnip)
        self.log.debug("Got the data as %s"%data)
        self.counter =1
        self.log.debug("Setting Maximum Threads as %s",newgnip.gnipmaxthreads)
        self.iid_lock = threading.Lock()
        self.log.debug(self.iid_lock)
        self.threadLimiter = threading.BoundedSemaphore(int (newgnip.gnipmaxthreads))
        self.log.debug(self.threadLimiter)
        threads = [threading.Thread(target=self.fetch_url, args=(url,newgnip,)) for url in  data["urlList"]]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        #failure Checks  and Retry zone
        self.log.debug("Checking for failures and Will Retry as Required")
        if(self.gnip.failedUrls > 0):
            #Detectd failures
            self.log.debug("Detected failures in URl Parsing .Retrying failed URl's Once")
            self.retryFailures()
        else:
            self.log.debug("No Failures Detected in URL Processing...")
            self.log.debug("Download Complete")
#z = DataDownloader()
