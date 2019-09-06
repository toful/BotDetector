#Import the necessary methods from tweepy library
import sys
import os
import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
import codecs

import pandas as pd
import joblib

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

#Drops all the information of the input user
def print_user( user ):
    print( user.screen_name )
    user_json = user._json
    for field in user_json.keys():
        print( field, "\t", user_json[ field ] )

    print( "\tFriends: ", user.friends_count )
    for friend in user.friends():
        print( "\t", friend.screen_name )
    print( "\n\tFollowers: ", user.followers_count )
    for follower in user.followers():
        print( "\t", follower.screen_name )
    return True

#builds the prediction dataset input of the given user
def get_user_data( user ):
    df = pd.DataFrame( user._json, index=[0] )
    x = pd.DataFrame()
    #x['id'] = df['id']
    x['profile_pic'] = df.apply( lambda row: aux_functions.profile_image (row), axis=1 ) #check this feature
    x['def_profile_pic'] = df.apply( lambda row: aux_functions.def_profile_image (row), axis=1 )
    x['has_screen_name'] = df.apply( lambda row: aux_functions.screen_name (row), axis=1 )
    x['30followers'] = df.apply( lambda row: aux_functions.min_followers (row, 30), axis=1 )
    x['1000followers'] = df.apply( lambda row: aux_functions.min_followers2 (row, 1000), axis=1 )
    x['1000friends'] = df.apply( lambda row: aux_functions.min_friends (row, 1000), axis=1 )
    x['30friends'] = df.apply( lambda row: aux_functions.min_friends2 (row, 30), axis=1 )
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
    x = get_user_data( user )
    try:
        # prediction
        y_pred = model.predict( x )
        y_pred_prob = model.predict_proba( x )
        if y_pred: aux = ' is a Bot'
        else: aux = ' is not a Bot'
        print('User ', user.screen_name, aux,'\n\tProbability of being a Bot: ', float("{0:.2f}".format( y_pred_prob[0][1]*10 )),'/ 10')
    except:
        print( 'ERROR: something happend with user ', user.screen_name )

if __name__ == '__main__':

    try:
        #import auxiliary functions for the  dataset building 
        sys.path.append( os.getcwd()+'/modules' )
        import aux_functions
    except:
        print("ERROR importing auxiliary functions.")
        exit(1)

    #reading the authetification credentials
    read_credentials( '../credentials.txt' )
    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler( credentials[0], credentials[1] )
    auth.set_access_token( credentials[2], credentials[3] )   
    api = tweepy.API(auth)

    # Fix Python 2.x.
    try: input = raw_input
    except NameError: pass

    if len(sys.argv) < 2:
        print( "ERROR: Twitter account needed." )
        exit( 1 )
    user_name = sys.argv[1]
    
    try:
        user = api.get_user( user_name )
    except:
        print("ERROR: User doesn't exists or it has a private account.")
        exit( 1 )


    #print_user( user )
    # load the model from disk
    models_string = "1-\tRandom Forest FakeFollowers model\n2-\tRandom Forest SpamBots model\n3-\tRandom Forest FFandSB model\n"
    try:
        mode = int( input( models_string+'Select the model you want to use: ' ) )
    except ValueError:
        print( "ERROR: Not a number" )
        exit( 1 )
    if mode > 3 or mode < 1:
        print( "ERROR: Not a valid option" )
        exit( 1 )

    switcher = {
        1: 'models/randomForest_fakeFollowers_model.sav',
        2: 'models/randomForest_mix_model.sav',
        3: 'models/randomForest_spamBots_model.sav'
    }
    model = joblib.load( switcher.get(mode, "Invalid value") )

    # analyzing the user with the loaded model
    analyze_user( model, user )

    mode = input( 'Do you want to analyze all your fiends too?(Y/N)' )
    if mode == 'Y' or mode == 'y':
        for friend in user.friends( count=200 ):
            analyze_user( model, friend )
    exit(0)