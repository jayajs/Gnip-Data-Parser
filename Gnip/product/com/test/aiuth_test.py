'''
Created on Jan 18, 2016

@author: user
'''
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 

consumer_key = 'yFiCcXjAC4pOv0OeAQrZxOfWj'
consumer_secret = 'Wg94DEtSc7Y8NrjFD8PB1vkvEKrrNvrZdye0ktWZYUzYhv6dbi'
access_token = '593499886-bvHxwzN5W3stlBnmXZTSjPIkw8VcjoSqhLmAKsqD'
access_token_secret = 'KOpukMNHqcNwlyxkK4KlS6SsRAwxGReLaRIwyOubl0n9t'
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
