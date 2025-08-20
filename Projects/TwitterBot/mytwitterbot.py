# mytwitterbot.py
# IAE 101, Fall 2024
# Project 04 - Building a Twitterbot

import sys
import time, random
import simple_twit

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from datetime import datetime

# Assign the string values that represent your developer credentials to
# each of these variables; credentials provided by the instructor.
# If you have your own developer credentials, then this is where you add
# them to the program.
# API Key, also known as Consumer Key
API_KEY = "73bhKtdDcWRplCnM0FRD7TYif"

# API Key Secret, also known as Consumer Secret
API_KEY_SECRET = "vUMYiTh7rBy1JS4vWOuXD1WxWrsaYiL3fJOBN58XzvC7rhFOe4"

#For Spotify
SPOTIPY_CLIENT_ID = "62a1cd991f2d40568cb488d0a6556a43"
SPOTIPY_CLIENT_SECRET = "f3b602d2781247d78fb787bcedcea354"

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Project 04 Exercises
    
# Exercise 1 - Get and print 3 tweets from your home timeline
# For each tweet, print:
#   the tweet ID,
#   the author ID, 
#   the tweet creation date, and
#   the tweet text
def exercise1(client):
    tweets = (simple_twit.get_home_timeline(client, 3)).data

    for tweet in tweets:
        print("\nTweet ID: " + str(tweet.id))
        print("\nAuthor ID: " + str(tweet.author_id))
        print("\nTweet Creation Date: " + str(tweet.created_at))
        print("\nTweet text: " + tweet.text)
        time.sleep(60)


# Exercise 2 - Get and print 5 tweets from another user
# For each tweet, print:
#   the tweet ID,
#   the author ID,
#   the tweet creation date, and
#   the tweet text
def exercise2(client):
    tweets = (simple_twit.get_users_tweets(client, "IAE101_ckane", 5)).data

    for tweet in tweets:
        print("\nTweet ID: " + str(tweet.id))
        print("\nAuthor ID: " + str(tweet.author_id))
        print("\nTweet Creation Date: " + str(tweet.created_at))
        print("\nTweet text: " + tweet.text)
        time.sleep(60)


# Exercise 3 - Post 1 tweet to your timeline.
def exercise3(client):
    simple_twit.send_tweet(client, "Hello World!")


# Exercise 4 - Post 1 media tweet to your timeline.
def exercise4(client):
    simple_twit.send_media_tweet(client, "Duck says: ", "hello.gif")

# End of Project 04 Exercises


# YOUR BOT CODE GOES IN HERE
def twitterbot(client):
    # while True:

    playlist_id = "0ipL5e7EE3DW8xMUlhAFLj"
    playlist_tracks = sp.playlist_tracks(playlist_id)

    track = random.choice(playlist_tracks['items'])['track']
    song_name = track['name']
    artist_name = ', '.join(artist['name'] for artist in track['artists'])
    song_link = track['external_urls']['spotify']
    # image = track['album']['images'][0]['url']
    
    todays_date = datetime.now()
    date_text = str(todays_date.month) + "/" + str(todays_date.day) + "/" + str(todays_date.year)

    text = "\U0001F3B6 " + date_text + "'s Song of the Day: \"" + song_name + "\" by " + artist_name + " \U0001F3B6" + "\n" + song_link

    simple_twit.send_tweet(client, text)

    # print(text)
    # print(image)
        
        # time.sleep(86400)


if __name__ == "__main__":
    # This call to simple_twit.create_client will create the Tweepy Client 
    # object that Tweepy needs in order to make authenticated requests to 
    # Twitter's API.
    # Do not remove or change this function call.
    # Pass the variable "client" holding this Tweepy Client object as the first
    # argument to simple_twit functions.
    simple_twit.version()
    print()
    
    try:
        client = simple_twit.create_client(API_KEY, API_KEY_SECRET)
    except Exception as e:
        print("ERROR:", e)
    
    print(client)

    # Once you are satisified that your exercises are completed correctly
    # you may comment out these function calls.
    # exercise1(client)
    # exercise2(client)
    # exercise3(client)
    # exercise4(client)

    # This is the function call that executes the code you defined above
    # for your twitterbot.
    twitterbot(client)
