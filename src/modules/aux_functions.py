
# is language english
def language( row ):
    if row['lang'] == 'en':
        return 1
    else:
        return 0

# has profile image
def profile_image (row):
    if row['profile_image_url'] == '':
        return 1
    else:
        return 0

# egg avatar, default profile image
def def_profile_image (row):
    if row['default_profile_image'] == '':
        return 0
    else:
        return 1

# has screen name
def screen_name (row):
    if row['name'] == '':
        return 1
    else:
        return 0

# has NUM followers
def min_followers (row, num):
    if row['followers_count'] < num:
        return 1
    else:
        return 0

# is geolocalized
def location (row):
    if row['geo_enabled'] == '':
        return 1
    else:
        return 0

# profile banner contains a link ('http') from profile_banner_url
# change to if the description contains
def profile_banner (row):
    if row['profile_banner_url'] == '':
        return 0
    else:
        return 1

# has done NUM tweets
def tweets_written (row, num):
    if row['statuses_count'] > num:
        return 0
    else:
        return 1

# 2* num followers >= # of friends
def ratio_followers (row):
    if 2*row['followers_count'] >= row['friends_count']:
        return 0
    else:
        return 1

# NUM:1 friends/followers
def ratio_followers2 ( row, num ):
    if num*row['followers_count'] <= row['friends_count']:
        return 1
    else:
        return 0

# does not have NUM of friends, spambot
def min_friends (row, num):
    if row['friends_count'] > num:
        return 1
    else:
        return 0

# sent less than NUM tweets, spambot
def min_statuses (row, num):
    if row['statuses_count'] < num:
        return 1
    else:
        return 0

# Never tweeted
def never_tweeted (row):
    if row['statuses_count'] == 0:
        return 1
    else:
        return 0

# profile contains a description
def description (row):
    if row['description'] == '':
        return 1
    else:
        return 0

# known bot
def knownbot (row):
    if row['knownbot'] == 1:
        return 1
    else:
        return 0

