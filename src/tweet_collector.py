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


#This is the listener that store received tweets.
class StdOutListener( StreamListener ):
    def __init__( self, csvWriter ):
        self.csvWriter = csvWriter

    def on_data(self, data):
        tweet = json.loads(data)
        self.csvWriter.writerow([  tweet['id'],
                                    tweet['user']['id'], 
                                    tweet['in_reply_to_status_id'], 
                                    tweet['in_reply_to_user_id'] ])
        return True

    def on_error(self, status):
        print( status )


if __name__ == '__main__':

    #reading the authetification credentials
    read_credentials( '../credentials.txt' )
    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler( credentials[0], credentials[1] )
    auth.set_access_token( credentials[2], credentials[3] )   
    api = tweepy.API(auth)

    if len(sys.argv) < 2:
        print( "ERROR: Few Arguments. Args: Hashtag1, Hashtag2, Hashtag3, ..." )
        exit( 1 )

    hashtags = sys.argv[1:]
    #hashtags = [ '#Elecciones2019', '#EleccionesMunicipales2019', '#EleccionsMunicipals2019', '#Elecciones26M' ]

    if not os.path.exists( 'results' ):
        os.makedirs( 'results' )
    # Open/Create a file to append data
    csvFile = open( 'results/tweets.csv', 'a' )
    csvWriter = csv.writer( csvFile )
    #Write the data headers
    csvWriter.writerow( [ 'tweet_id','user_id','in_replay_tweet_id','in_replay_user_id' ] )

    try:
        listener = StdOutListener( csvWriter )
        stream = Stream( auth, listener )
        # This line filter Twitter Streams to capture data containing the hashtag specified by argument
        stream.filter(  track=hashtags ) #, async=True)
    except KeyboardInterrupt:
        print( "\nExit")
        exit(0)
