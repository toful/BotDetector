import sys
import os
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import codecs
import csv
import pandas as pd

import urllib2
import re

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


def get_user_ids_of_post_likes(post_id):
    try:
        json_data = urllib2.urlopen( 'https://twitter.com/i/activity/favorited_popup?id=' + str(post_id) ).read()
        found_ids = re.findall( r'data-user-id=\\"+\d+', json_data )
        unique_ids = list( set([re.findall(r'\d+', match)[0] for match in found_ids]) )
        return unique_ids
    except urllib2.HTTPError:
        return False

def get_user_ids_of_post_retweets(post_id):
    try:
        json_data = urllib2.urlopen( 'https://twitter.com/i/activity/retweeted_popup?id=' + str(post_id) ).read()
        found_ids = re.findall( r'data-user-id=\\"+\d+', json_data )
        unique_ids = list( set([re.findall(r'\d+', match)[0] for match in found_ids]) )
        return unique_ids
    except urllib2.HTTPError:
        return False


if __name__ == '__main__':

    #NOT USED, USING HTTP REQUESTS INSTEAD OF TWITTER API
    #reading the authetification credentials
    #read_credentials( '../credentials.txt' )
    #This handles Twitter authetification and the connection to Twitter API
    #auth = OAuthHandler( credentials[0], credentials[1] )
    #auth.set_access_token( credentials[2], credentials[3] )   
    #api = tweepy.API( auth, wait_on_rate_limit=True )

    
    if len(sys.argv) < 2:
        print( "ERROR: Few Arguments: [Input File]." )
        exit( 1 )

    #Loading datasets
    #path = os.getcwd() 
    #os.chdir( "/home/toful/Documents/DataSets/" )
    #tweets = pd.read_csv( 'tweets.csv' )
    #os.chdir( path )
    try:
        tweets = pd.read_csv( sys.argv[1] )
    except:
        print("Input file doesn't exists.")
        exit(1)

    if not os.path.exists( 'results' ):
        os.makedirs( 'results' )

    #Generating the Users File
    users = {}
    for user in tweets['user_id']:
        if user in users.keys():
            users[ user ] += 1
        else:
            users[ user ] = 1
    # Open/Create a file to append data
    csvFile = open( 'results/users.csv', 'a' )
    #csvFile = open( 'results_little/users_little.csv', 'a' )
    # Use csv Writer
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'user_id', 'num_tweets' ] )
    for key,value in users.items():
        csvWriter.writerow( [ key, value ] )
    csvFile.close()

    #Generating the Users File and the Retweet links file
    print( "Generating the Users File and the Retweet links file" )
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
            #for retweet in api.retweets( tweet_id, 100000):
            for user_rt in get_user_ids_of_post_retweets( tweet_id ):
                #user_rt = retweet.author.id

                if (user, user_rt) in retweet_links.keys():
                    retweet_links[ (user, user_rt) ] += 1
                else:
                    retweet_links[ (user, user_rt) ] = 1

                if user_rt in users_retweet_links.keys():
                    users_retweet_links[ user_rt ] += 1
                else:
                    users_retweet_links[ user_rt ] = 1
        except:
            print("An exception ocurred with user", user_rt)
    csvFile = open( 'results/users_rt.csv', 'a' )
    #csvFile = open( 'results_little/users_rt_little.csv', 'a' )
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'user_id', 'num_interactions' ] )
    for key,value in users_retweet_links.items():
        csvWriter.writerow( [ key, value ] )
    csvFile.close()
    csvFile = open( 'results/links_rt.csv', 'a' )
    #csvFile = open( 'results_little/links_rt_little.csv', 'a' )
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'user1', 'user2', 'num_interactions' ] )
    for key,value in retweet_links.items():
        csvWriter.writerow( [ key[0], key[1], value ] )
    csvFile.close()

    #Generating the Users File and the Favourite links file
    print( "Generating the Users File and the Favourite links file" )
    users_favourite_links = {}
    favourite_links = {}
    for i in range( 0, len(tweets) ):
        tweet_id = tweets['tweet_id'][i]
        user = tweets['user_id'][i]

        if user in users_favourite_links.keys():
            users_favourite_links[ user ] += 1
        else:
            users_favourite_links[ user ] = 1

        try:
            for user_fav in get_user_ids_of_post_likes( tweet_id ):

                if (user, user_fav) in favourite_links.keys():
                    favourite_links[ (user, user_fav) ] += 1
                else:
                    favourite_links[ (user, user_fav) ] = 1

                if user_fav in users_favourite_links.keys():
                    users_favourite_links[ user_fav ] += 1
                else:
                    users_favourite_links[ user_fav ] = 1
        except:
            print("An exception ocurred with user", user)
    csvFile = open( 'results/users_fav.csv', 'a' )
    #csvFile = open( 'results_little/users_fav_little.csv', 'a' )
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'user_id', 'num_interactions' ] )
    for key,value in users_favourite_links.items():
        csvWriter.writerow( [ key, value ] )
    csvFile.close()
    csvFile = open( 'results/links_fav.csv', 'a' )
    #csvFile = open( 'results_little/links_fav_little.csv', 'a' )
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'user1', 'user2', 'num_interactions' ] )
    for key,value in favourite_links.items():
        csvWriter.writerow( [ key[0], key[1], value ] )
    csvFile.close()

    exit(0)
