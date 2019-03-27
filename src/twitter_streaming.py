#Import the necessary methods from tweepy library
import sys
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import codecs

#Variables that contains the user credentials to access Twitter API 
#   consumer_key
#   consumer_secret
#   access_token
#   access_token
credentials=[]


def read_file(filename):
    global credentials
    i=0
    with codecs.open(filename, encoding='utf-8', mode='r') as fileref:
        for line in fileref.readlines():
            credentials += [ line.splitlines()[0] ]

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

def process_or_store( user ):
    for field in user.keys():
        print field, "\t", user[ field ]
    return True

if __name__ == '__main__':

    read_file( '../credentials.txt' )
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler( credentials[0], credentials[1] )
    auth.set_access_token( credentials[2], credentials[3] )
    
    api = tweepy.API(auth)

    if len(sys.argv) >= 2:
        user = api.get_user( sys.argv[1] )
        print user.screen_name
        process_or_store( user._json )
        print "\tFriends: ", user.followers_count
        for friend in user.friends():
            print "\t", friend.screen_name
        print "\n\tFollowers: ", user.followers_count
        for follower in user.followers():
            print "\t", follower.screen_name

    #stream = Stream(auth, l)
    ##This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(  track=['python', 'javascript', 'ruby'] )