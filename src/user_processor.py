#Import the necessary methods from tweepy library
import sys
import os
import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
import codecs
import csv

import pandas as pd
from sklearn.externals import joblib

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

#builds the prediction dataset input of the given user
def get_dataset( user ):
    df = pd.DataFrame( user._json, index=[0] )
    x = pd.DataFrame()
    #x['id'] = df['id']
    x['lang-en'] = df.apply( lambda row: aux_functions.language (row), axis=1 )
    x['profile_pic'] = df.apply( lambda row: aux_functions.profile_image (row), axis=1 ) #check this feature
    x['def_profile_pic'] = df.apply( lambda row: aux_functions.def_profile_image (row), axis=1 )
    x['has_screen_name'] = df.apply( lambda row: aux_functions.screen_name (row), axis=1 )
    x['30followers'] = df.apply( lambda row: aux_functions.min_followers (row, 30), axis=1 )
    x['1000friends'] = df.apply( lambda row: aux_functions.min_friends (row, 1000), axis=1 )
    x['twice_num_followers'] = df.apply( lambda row: aux_functions.ratio_followers (row), axis=1 )
    x['fifty_FriendsFollowersRatio'] = df.apply( lambda row: aux_functions.ratio_followers2 (row, 50), axis=1 )
    x['hundred_FriendsFollowersRatio'] = df.apply( lambda row: aux_functions.ratio_followers2 (row, 100), axis=1 )
    x['geoloc'] = df.apply( lambda row: aux_functions.location (row), axis=1 )
    x['banner_link'] = df.apply( lambda row: aux_functions.profile_banner (row), axis=1 )
    x['50tweets'] = df.apply( lambda row: aux_functions.tweets_written (row, 50), axis=1 )
    x['20statuses'] = df.apply( lambda row: aux_functions.min_statuses (row, 20), axis=1 )
    x['NeverTweeted'] = df.apply( lambda row: aux_functions.never_tweeted (row ), axis=1 )
    x['has_description'] = df.apply( lambda row: aux_functions.description (row), axis=1 )
    return x


#predicts if the given user is a bot using the given model
def analyze_user( model, user ):
    # getting the user data
    x = get_dataset( user )
    try:
        # prediction
        y_pred_prob = model.predict_proba( x )
        return y_pred_prob[0][1]
    except:
        print( 'Error on analysing the user' )
        return 0

if __name__ == '__main__':

    #import auxiliary functions for the  dataset building 
    sys.path.append( os.getcwd()+'/modules' )
    import aux_functions

    if len(sys.argv) < 3:
        print "ERROR: Few Arguments: [Input File] [Output File]."
        exit( 0 )

    #reading the authetification credentials
    read_credentials( '../credentials.txt' )
    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler( credentials[0], credentials[1] )
    auth.set_access_token( credentials[2], credentials[3] )   
    api = tweepy.API( auth, wait_on_rate_limit=True )

    try:
        model = joblib.load( 'models/randomForest_mix_model.sav' )
    except:
        print( "ERROR: Something wrong when loading the model" )
        exit( 1 )
    try:
        users = pd.read_csv( sys.argv[1] )
    except:
        print( "ERROR: Input file doesn't exists" )
        exit( 1 )
    csvFile = open( sys.argv[2], 'w' )
    csvWriter = csv.writer( csvFile )
    csvWriter.writerow( [ 'user_id', 'user_name', 'num_interactions', 'bot_prob' ] )
    for i in range( 0, len( users ) ):
        if( i % 1000 == 0 ):
            print( i )
        try:
            user = api.get_user( users['user_id'][i] )
            prob = analyze_user( model, user )
            csvWriter.writerow( [ users['user_id'][i], user.screen_name, users['num_interactions'][i], prob ] )
        except:
            print( 'Error on getting the user' )
    csvFile.close()
