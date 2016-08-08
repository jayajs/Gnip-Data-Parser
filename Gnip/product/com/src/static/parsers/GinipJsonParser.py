'''
Created on Jan 19, 2016

@author: jaya
'''
import fnmatch, os, json
from   product.com.src.static.downloaders.Gnip import Gnip
from   product.com.loggings.log_conf import Logger
from   csv import writer

class JsonParser(object):
    '''
    Class deals with Json Parsing of the GNIP data 
    '''
    gnip = ''
    log = Logger.logr
    finalOutFileName = ''
    def __init__(self,param1):
        '''
        Constructor
        '''
        self.log.debug("Starting init of GNIP JSON Parsing")
        self.gnip = param1
        self.log.debug("GNIP object @"+str(self.gnip))
        self.log.debug("Started Processing")
        #self.parseJson()

    def parseJson(self):
        #Add Header information
        '''
        Parses the set of json files in the path and retuns the parsed filename 
        
        '''
        pattern = "*.json"
        outfileName = "ParsedCSVData.csv"
        outfile = self.gnip.gnipCSVOutPath + "\\" + outfileName
        #creating a variable for future use
        self.finalOutFileName = outfile
        rootPath = self.gnip.gnipOutputPath
        self.log.debug("The output file will be on :"+outfile)
        self.log.debug("The rottpath defined is as :"+rootPath)
        with open(outfile, 'ab') as myfile:
            self.log.debug("Writing headers on the csv file")
            print >> myfile, 'tweet_id,tweet_posted_time,tweet_author_id,tweet_disp_name,tweet_author_bio,Follower_count,friends_count,tweet_author_location,timezone,Verified,Retweeted_count,Favourite_Count,generator_Name,Object_Type,id,summary,tweet_country,city,tweet_lang,lat,lon,ALTLAT,ALTLON,tweet_text,link'
            self.log.debug("Header write complete .Flushing CSV  and Closing now ")
            myfile.close()
    
        for root, dirs, files in os.walk(rootPath):
            for filename in fnmatch.filter(files, pattern):
                infile = os.path.join(root, filename)
                self.log.debug("Now procesing file named %s"%infile)
                with open(infile) as in_file, \
                        open(outfile, 'ab') as out_file:
                    # print >> out_file, 'tweet_id, tweet_posted_time, tweet_author_id,tweet_author_location, tweet_country,city, tweet_lang,lat,lon,ALTLAT,ALTLON tweet_text,link'
                    self.log.debug("Opened file %s for writing"%outfile)
                    csv = writer(out_file)
                    self.log.debug(csv)
                    tweet_count = 0
                    for line in in_file:
                        tweet_count += 1
                        try:
                            retweeted_count = 0;
                            follower_count = 0;
                            friends_count = 0;
                            retweeted_count = 0;
                            favourite_count = 0
                            tweet = json.loads(line)
                            tweet_id = (tweet.get('id')).split(',')[1]
                            # print tweet_id# tweet_id
                            tweet_posted_time = tweet.get('postedTime')  # tweet_time
                            # tweet['user']['screen_name'],   # tweet_author #followerCount #friendsCount #timezone
                            tweet_actor_id = (tweet['actor'].get('id')).split(':')[2]
                            follower_count = (tweet['actor'].get('followersCount'))
                            actor_disp_name = (tweet['actor'].get('displayName'))
                            author_bio = (tweet['actor'].get('summary'))
                            friends_count = (tweet['actor'].get('friendsCount'))
                            timezone = (tweet['actor'].get('twitterTimeZone'))
                            verified = (tweet['actor'].get('verified'))
                            retweeted_count = (tweet.get('retweetCount'))
                            favourite_count = (tweet.get('retweetCount'))
                            generator = (tweet.get('generator', 'NA'))
                            generator_name = 'NA'
                            if generator != 'NA':
                                generator_name = generator.get('displayName', 'NA')
                            # print tweet_actor_id# tweet_authod_id
                            # get objects as per dict
                            tobject = tweet.get('object', 'NA')
                            summary = 'NA';
                            id = 'NA';
                            objectType = 'NA'
                            if (tobject != 'NA'):
                                objectType = tobject.get('objectType')
                                id = tobject.get('id')
                                summary = tobject.get('summary')
                            location = tweet.get('location', 'na')
                            tweet_country = 'NA'
                            city = 'NA'
                            cords = ['NA', 'NA'];
                            altlat = 'NA';
                            altlon = 'NA'
                            if (location != 'na'):
                                tweet_country = location.get('country_code', 'na')
                                city = location.get('name', 'na')
                                geo = location.get('geo', 'NA')
                                cords = geo.get('coordinates', 'NA')[0][0]
                                altlat = cords[0];
                                altlon = cords[1]
                            # print tweet_country
                            tweet_author_location = tweet['actor'].get('location', 'NA')
                            if (tweet_author_location != 'NA'):
                                tweet_author_location = tweet_author_location.get('displayName', 'NA')
                            # print tweet_author_location
                            tweet_lang = tweet['twitter_lang']  # tweet_language
                            t7 = tweet.get('geo', 'NA')
                            lat = 'NA'
                            lon = 'NA'
                            if (t7 != "NA"):
                                lat = tweet['geo']['coordinates'][0]
                                lon = tweet['geo']['coordinates'][1]
                            tweet_body = tweet.get('body', 'NA')  # tweet_text
                            tweet_link = tweet.get('link', 'NA')
                            # Pull out various data from the tweets
                            row = (tweet_id, tweet_posted_time, tweet_actor_id, actor_disp_name,author_bio,
                                   follower_count, friends_count, tweet_author_location,
                                   timezone, verified, retweeted_count, favourite_count,
                                   generator_name, objectType, id, summary, tweet_country, city,
                                   tweet_lang, lon, lat, altlat, altlon,
                                   tweet_body, tweet_link)
        
                            values = [(value.encode('utf8') if hasattr(value, 'encode') else value) for value in row]
                            # print values #final write to csv data format..Outputting a row at a time
                            self.log.debug("Writing  Record to CSV file for Processing")
                            csv.writerow(values)
                        except Exception as ex:
                            self.log.warning("Parsing of a Record failed.Does this record correspond to GNIP json schema.Please check stack trace")
                            self.log.exception(ex) 
                            self.log.debug("Current tweet Count is "+str(tweet_count))
        return self.finalOutFileName                    
        ###################################################################
        #Flatten the json Schema code######################################
        #Currently the following method remains unused>may be used in Future
        ###################################################################    
    def flattenDict(self,d, result=None):
        '''
        Used to flatten a dictionary $ since json is nothing but a dict 
        $$$Unused ->Loss of information with usage.Do not use
        
        '''
        if result is None:
            result = {}
        for key in d:
            value = d[key]
            if isinstance(value, dict):
                value1 = {}
                for keyIn in value:
                    value1[".".join([key,keyIn])]=value[keyIn]
                self.flattenDict(value1, result)
            elif isinstance(value, (list, tuple)):   
                for indexB, element in enumerate(value):
                    if isinstance(element, dict):
                        value1 = {}
                        index = 0
                        for keyIn in element:
                            newkey = ".".join([key,keyIn])        
                            value1[".".join([key,keyIn])]=value[indexB][keyIn]
                            index += 1
                        for keyA in value1:
                            self.flattenDict(value1, result)   
            else:
                result[key]=value
        return result