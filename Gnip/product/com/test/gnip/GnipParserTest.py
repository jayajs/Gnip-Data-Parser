'''
Created on Jan 20, 2016

@author: jaya
'''
from    product.com.src.static.downloaders.Gnip         import Gnip
from    product.com.src.static.parsers.GinipJsonParser  import JsonParser
from    product.com.loggings.log_conf                   import Logger
from    product.com.utils.DbHelper                      import  DbHelper
import  Timing as monitor
from time import clock
tstart = clock()
log = Logger.logr
log.debug("starting Test of GNIP Parser")            
g = Gnip().run()
log.debug(g)
gnip_json_parser  = JsonParser(g)
filename = gnip_json_parser.parseJson()
tstop = clock()
log.critical("Processing complete in %s",monitor.secondsToStr(tstop-tstart))
dbhelper = DbHelper()
print filename
dbhelper.import_content(filename)
dbhelper.export_content("D:\\exportedMongo.csv")

