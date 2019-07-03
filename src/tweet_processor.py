import sys
import os
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import codecs
import csv
import pandas as pd

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

if __name__ == '__main__':

    #reading the authetification credentials
    read_credentials( '../credentials.txt' )
    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler( credentials[0], credentials[1] )
    auth.set_access_token( credentials[2], credentials[3] )   
    api = tweepy.API(auth)

    #Loading datasets
    path = os.getcwd() 
    os.chdir( "/home/toful/Documents/DataSets/" )

    #tweets = pd.read_csv( 'tweets.csv' )
    tweets = pd.read_csv( 'tweets_little.csv' )
    os.chdir( path )

    #Generating the Users File
    users = {}
    for user in tweets['user_id']:
        if user in users.keys():
            users[ user ] += 1
        else:
            users[ user ] = 1
    # Open/Create a file to append data
    csvFile = open( 'results/users.csv', 'a' )
    # Use csv Writer
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'user_id', 'num_tweets' ] )
    for key,value in users.items():
        csvWriter.writerow( [ key, value ] )
    csvFile.close()


    #Generating the Users File and the Retweet links file
    users_retweet_links = {}
    retweet_links = {}
    for i in range( 0, len(tweets) ):
        tweet_id = tweets['tweet_id'][i]
        user = tweets['user_id'][i]

        if user in users_retweet_links.keys():
            users_retweet_links[ user ] += 1
        else:
            users_retweet_links[ user ] = 1

        try:
            for retweet in api.retweets( tweet_id, 100000):
                user_rt = retweet.author.id

                if (user, user_rt) in retweet_links.keys():
                    retweet_links[ (user, user_rt) ] += 1
                else:
                    retweet_links[ (user, user_rt) ] = 1

                if user_rt in users_retweet_links.keys():
                    users_retweet_links[ user_rt ] += 1
                else:
                    users_retweet_links[ user_rt ] = 1
        except:
            print("An exception ocurred")

    csvFile = open( 'results/users_rt.csv', 'a' )
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'user_id', 'num_rt' ] )
    for key,value in users_retweet_links.items():
        csvWriter.writerow( [ key, value ] )
    csvFile.close()
    csvFile = open( 'results/links_rt.csv', 'a' )
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'link', 'num_interactions' ] )
    for key,value in retweet_links.items():
        csvWriter.writerow( [ key, value ] )
    csvFile.close()





    





