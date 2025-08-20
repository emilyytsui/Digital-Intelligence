# Simple Twit - A simplified interface for accessing twitter through Python
# simple_twit_2-1.py
# Written for Twitters v2 API
# IAE 101, Fall 2024
# Authors: Christopher Kane, Greg Zborovsky

import tweepy
import sys, os, json, webbrowser

# CONSTANTS
VERSION = 2.1 # updated for Twitter APIv2
CONFIG_FILE = "twitter_bot.config"
API = None
CLIENT = None
TWEET_FIELDS = ["author_id","created_at","in_reply_to_user_id","lang","public_metrics"]
USER_FIELDS = ["created_at","description","pinned_tweet_id","public_metrics","url"]
CALLBACK_URL = 'http://127.0.0.1:5000/callback'


#######################################
# GENERAL FUNCTIONS                   #
#######################################

def version():
    res = "simple_twit, version: " + str(VERSION)
    print(res)
    return res
# end def version()

# parameters
#    api_key    : a string, first element of developer credentials
#    api_key_secret : a string, second element of developer credentials
# return value
#    an Tweepy Client object that represents the bots access to the user account 
#    that authorized the bot to act on its behalf.
def create_client(api_key = None, api_key_secret = None):
    usage = "USAGE: create_client(api_key <a string>, api_key_secret <a string>)"
    if api_key == None or api_key == "":
        print("ERROR: You must pass a string api key; it is the first" + 
              " element of the developer credentials shared by the instructor.")
        print(usage)
        return
    if api_key_secret == None or api_key_secret == "":
        print("ERROR: You must pass a string api key secret; it is the second" +
              " element of the developer credentials shared by the instructor.")
        print(usage)
        return
    
    access_token = None
    access_token_secret = None
    verify_access = True
    
    if os.path.exists(CONFIG_FILE):
        print("READING AUTHORIZATION FROM CONFIG FILE")
        f = open(CONFIG_FILE, "r")
        config = json.load(f)
        access_token = config["access_token"]
        access_token_secret = config["access_secret"]
        f.close()
        verify_access = False
    
    # Authentication Methods
    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, callback = "oob")

    if verify_access:
        print("AUTHORIZING THROUGH WEB INTERFACE") 
        try:
            auth_url = auth.get_authorization_url()
        except tweepy.TweepyException as e:
            print("REQUEST VERIFIER URL", e)
            return None
        
        print(auth_url)
        print()
        webbrowser.open_new(auth_url)
        
        verifier = input("Enter Verifier: ")
        try:
            access_token, access_token_secret = auth.get_access_token(verifier)
        except tweepy.TweepyException as e:
            print("REQUEST ACCESS TOKEN:", e)
            return None
        config = {"access_token" : access_token, 
                  "access_secret" : access_token_secret}
        f = open(CONFIG_FILE, "w")
        json.dump(config, f)
        f.close()
        
    if access_token != None:
        auth.set_access_token(access_token, access_token_secret)
    else:
        print("AUTHENTICATION FAILED: EXITING PROGRAM!")
        print()
        sys.exit()

    # Create API object
    global API
    try:
        API = tweepy.API(auth, wait_on_rate_limit = True)
    except tweepy.TweepyException as e:
        print("API CREATION:", e)
        print()
        return None
    # Create Client object
    try:
        client = tweepy.Client(consumer_key = api_key, 
                               consumer_secret = api_key_secret, 
                               access_token = access_token,
                               access_token_secret = access_token_secret)
    except tweepy.TweepyException as e:
        print("Client CREATION:", e)
        print()
        return None
    global CLIENT
    CLIENT = client
    return client
# end def create_client()


#######################################
#     TWEET FUNCTIONS                 #
#######################################

def send_tweet(client = None, msg = ""):
    usage = "USAGE: send_tweet(client <a tweepy client object>, msg <a string>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if msg == "":
        print("ERROR: You must pass a string to this function.")
        print(usage)
        return
    try:
        result = client.create_tweet(text = msg, user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def send_tweet()

# Not documented yet
def send_quote_tweet(client = None, msg = "", tweet_id = None):
    usage = "USAGE: send_quote_tweet(client <a tweepy client object>, msg <a string>, tweet_id <an int>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if msg == "":
        print("ERROR: You must pass a string to this function.")
        #print("ERROR: The msg must include @username for the author of the" +
        #      " tweet to which this is a reply.")
        print(usage)
        return
    if tweet_id == None:
        print("ERROR: You must pass a tweet id in order to quote it.")
    try:
        result = client.create_tweet(text = msg,
                                     quote_tweet_id = tweet_id,
                                     user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def send_quote_tweet()
    

def send_reply_tweet(client = None, msg = "", tweet_id = None):
    usage = "USAGE: send_reply_tweet(client <a tweepy client object>, msg <a string>, tweet_id <an int>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if msg == "": #or "@" not in msg:
        print("ERROR: You must pass a string to this function.")
        #print("ERROR: The msg must include @username for the author of the" +
        #      " tweet to which this is a reply.")
        print(usage)
        return
    if tweet_id == None:
        print("ERROR: You must pass a tweet id in order to send a reply.")
    try:
        result = client.create_tweet(text = msg,
                                     in_reply_to_tweet_id = tweet_id,
                                     user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def send_reply_tweet()

def send_media_tweet(client = None, msg = "", filename = ""):
    usage = "USAGE: send_media_tweet(client <a tweepy client object>, msg <a string>, filename <a string>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if filename == "":
        print("ERROR: you must pass a filename as a string to this function.")
        print(usage)
        return
    try:
        mo = API.media_upload(filename) # Returns a Media Object
        result = client.create_tweet(text = msg,
                                     media_ids = [mo.media_id],
                                     user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def send_media_tweet()

def send_reply_media_tweet(client = None, msg = "", tweet_id = None, filename = ""):
    # Written by Greg Zborovsky, IAE 101, Fall 2021
    # Adapted by CMK for Twitter's 2.0 API
    usage = "USAGE: send_reply_media_tweet(client <a tweepy client object>, msg <a string>,"
    usage += " tweet_id <an int>, filename<a string>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if tweet_id == None:
        print("ERROR: You must pass a tweet id in order to send a reply.")
        print(usage)
        return
    if filename == "":
        print("ERROR: you must pass a filename as a string to this function.")
        print(usage)
        return
    try:
        mo = API.media_upload(filename) # Returns a Media Object
        result = client.create_tweet(text = msg,
                                     in_reply_to_tweet_id = tweet_id,
                                     media_ids = [mo.media_id],
                                     user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def send_reply_media_tweet()

def retweet(client = None, tid = None):
    usage = "USAGE: retweet(client <a tweepy client object>, "
    usage += "tid <numerical id of tweet>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if tid == None:
        print("ERROR: You must pass a numerical tweet id to this function.")
        print(usage)
        return
    try:
        result = client.retweet(tweet_id = tid, user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def retweet()

def get_tweet(client = None, tid = None):
    usage = "USAGE: get_tweet(client <a tweepy client object>, "
    usage += "tid <numerical id of tweet>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if tid == None:
        print("ERROR: You must pass an numerical tweet id to this function.")
        print(usage)
        return
    try:
        result = client.get_tweet(tid, tweet_fields = TWEET_FIELDS, 
                                  user_fields = USER_FIELDS, user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def get_tweet()

# No method for this in the v2 API
# def get_retweets(api, id, count = 1):

def get_retweeters(client = None, tid = None, count = 1):
    usage = "USAGE: get_retweeters(client <a tweepy client object>, "
    usage += "tid <numerical id of tweet>, "
    usage += "count <number of user ids to retrieve>), max = 10"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage) 
        return
    if tid == None:
        print("ERROR: You must pass an numerical tweet id to this function.")
        print(usage)
        return
    if count < 1 or count > 10:
        print("ERROR: count argument must be a positive integer between \
               1 and 10; default = 1.")
        print(usage)
        return
    try:
        results = client.get_retweeters(tid, max_results = count,
                                        tweet_fields = TWEET_FIELDS, 
                                        user_fields = USER_FIELDS, 
                                        user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return results
# end def get_retweeters()


#######################################
#     TIMELINE FUNCTIONS              #
#######################################

def get_home_timeline(client = None, count = 1):
    usage = "USAGE: get_home_timeline(client <a tweepy client object>, "
    usage += "count <number of tweets to retrieve>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if count < 1 or count > 10:
        print("ERROR: count argument must be a positive integer between 1 and 10; default = 1.")
        print(usage)
        return
    try:
        result = client.get_home_timeline(max_results = count,
                                          tweet_fields = TWEET_FIELDS, 
                                          user_fields = USER_FIELDS,
                                          user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def get_home_timeline()
    
def get_users_tweets(client = None, user_name = "", count = 5):
    usage = "USAGE: get_user_timeline(client <a tweepy client object>, "
    usage += "user_id <unique identifier for user's twitter account>, "
    usage += "count <number of tweets to retrieve>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if user_name == "":
        print("ERROR: You must pass an username string to this function.")
        print(usage)
        return
    if count < 5 or count > 10:
        print("ERROR: count argument must be a positive integer between 5 and 10; default = 5.")
        print(usage)
        return
    try:
        temp = client.get_user(username = user_name, user_auth = True)
        result = client.get_users_tweets(temp.data.id, max_results = count,
                                         tweet_fields = TWEET_FIELDS, 
                                         user_fields = USER_FIELDS,
                                         user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def get_users_tweets()

# No method for this in the v2 API
# def get_retweets_of_me(api = None, count = 20):

def get_users_mentions(client = None, user_name = "", count = 5):
    usage = "USAGE: get_mentions(client <a tweepy client object>, "
    usage += "user_id <unique identifier for user's twitter account>, "
    usage += "count <number of tweets to retrieve>)"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if user_name == "":
        print("ERROR: You must pass an username string to this function.")
        print(usage)
        return
    if count < 5 or count > 10:
        print("ERROR: count argument must be a positive integer between 5 and 10; default = 5.")
        print(usage)
        return
    try:
        temp = client.get_user(username = user_name, user_auth = True)
        result = client.get_users_mentions(temp.data.id, max_results = count,
                                           tweet_fields = TWEET_FIELDS, 
                                           user_fields = USER_FIELDS,
                                           user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def get_users_mentions()


#######################################
#     USER FUNCTIONS                  #
#######################################

def get_user(client = None, *, user_name = "", user_id = ""):
    usage = "USAGE: get_user(client <a tweepy client object>, "
    usage += "user_name <screen name of user as a string>), "
    usage += "user_id <unique identifier for user's twitter account>."
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if user_name == "" and user_id == "":
        print("ERROR: You must pass a either user name or user ID to this function.")
        print(usage)
        return
    try:
        if user_name:
            result = client.get_user(username = user_name,
                                     tweet_fields = TWEET_FIELDS, 
                                     user_fields = USER_FIELDS,
                                     user_auth = True)
        else:
            result = client.get_user(id = user_id,
                                     tweet_fields = TWEET_FIELDS, 
                                     user_fields = USER_FIELDS,
                                     user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def get_user()

# This endpoint is only accessible to those with Enterprise access
# def get_users_following(client = None, user_name = ""):

# No method for this in the v2 API
# def get_my_friends(api = None, count = 100):

# This endpoint is only accessible to those with Enterprise access
# def get_users_followers(client = None, user_name = ""):

# end def get_user_followers()

# No method for this in the v2 API
# def get_my_followers(api = None, count = 100):


#######################################
#     FOLLOW and UNFOLLOW             #
#######################################

# I have removed these methods to avoid violating twitter's (x's) constraints on
# automated (bot) behavior.

# def follow_user(api = None, user = ""):

# def unfollow_user(api = None, user = ""):


#######################################
#     Search Functions                #
#######################################

def search_tweets(client = None, query = "", count = 10):
    usage = "USAGE: search_users(client <a tweepy client object>, query <a string query>, "
    usage += "count <number of results to return>"
    if client == None:
        print("ERROR: You must pass a client object to this function.")
        print(usage)
        return
    if query == "":
        print("ERROR: You must pass a string as a query to search on.")
        print(usage)
        return
    if count < 10 or count > 20:
        print("ERROR: count argument must be a positive integer between 10 and 20; default = 1.")
        print(usage)
        return
    try:
        result = client.search_recent_tweets(query, max_results = count,
                                             tweet_fields = TWEET_FIELDS, 
                                             user_fields = USER_FIELDS,
                                             user_auth = True)
    except tweepy.TweepyException as e:
        print(e)
        return
    return result
# end def search()

# No method for this in the v2 API
# def search_users(api = None, query = "", count = 1):
