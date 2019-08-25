import sys
import os
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import codecs
import csv


#Variables that contains the user credentials to access Twitter API 
#   consumer_key
#   consumer_secret
#   access_token
#   access_token
credentials=[]


def read_credentials(filename):
    global credentials
    i=0
    with codecs.open(filename, encoding='utf-8', mode='r') as fileref:
        for line in fileref.readlines():
            credentials += [ line.splitlines()[0] ]


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener( StreamListener ):
    def __init__( self ):
        # Open/Create a file to append data
        self.csvFile = open( 'tweets.csv', 'a' )
        #Use csv Writer
        self.csvWriter = csv.writer( self.csvFile )
        #Write the data headers
        self.csvWriter.writerow( [ 'tweet_id','user_id','in_replay_tweet_id','in_replay_user_id' ] )

    def on_data(self, data):
        tweet = json.loads(data)
        self.csvWriter.writerow([  tweet['id'],
                                    tweet['user']['id'], 
                                    tweet['in_reply_to_status_id'], 
                                    tweet['in_reply_to_user_id'] ])
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #reading the authetification credentials
    read_credentials( '../credentials.txt' )
    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler( credentials[0], credentials[1] )
    auth.set_access_token( credentials[2], credentials[3] )   
    api = tweepy.API(auth)

    l = StdOutListener()
    stream = Stream( auth, l )
    # This line filter Twitter Streams to capture data containing the hashtag specified by argument
    stream.filter(  track=[ '#Elecciones2019', '#EleccionesMunicipales2019', '#EleccionsMunicipals2019', '#Elecciones26M' ] )
