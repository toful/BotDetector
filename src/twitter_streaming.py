#Import the necessary methods from tweepy library
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
        self.csvFile = open( 'full_tweets.csv', 'a' )
        #Use csv Writer
        self.csvWriter = csv.writer( self.csvFile )
        self.csvFile = open( 'tweets.csv', 'a' )
        self.csvWriter2 = csv.writer( self.csvFile )

    def on_data(self, data):
        tweet = json.loads(data)
        #print tweet['user']['screen_name'], tweet['text'].encode('ascii', 'ignore')
        self.csvWriter.writerow([   tweet['id'], 
                                    tweet['user']['id'],
                                    tweet['user']['screen_name'], 
                                    tweet['retweet_count'], 
                                    tweet['favorite_count'], 
                                    tweet['in_reply_to_status_id'], 
                                    tweet['in_reply_to_user_id'],
                                    tweet['in_reply_to_screen_name'],
                                    tweet['entities']['hashtags'], 
                                    tweet['entities']['user_mentions'],
                                    tweet['created_at'],
                                    tweet['text'].encode('ascii', 'ignore') ])
        self.csvWriter2.writerow([   tweet['id'],
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
    stream.filter(  track=[ '#Elecciones2019', '#Municipales2019' ] )


    #for tweet in tweepy.Cursor( api.search, q='#Elecciones2019', count=100 ).items(1):
        #print tweet._json
        #print ( tweet.id, tweet.author.id, tweet.retweet_count, tweet.favorite_count, tweet.in_reply_to_status_id, tweet.created_at )
