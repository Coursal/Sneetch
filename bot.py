import tweepy
import time
import os
import discord
from discord.ext import commands


API_KEY = "your_api_key_from_twitter"
API_SECRET = "your_api_secret_key_from_twitter"
ACCESS_KEY = "your_access_key_from_twitter"
ACCESS_SECRET = "your_access_secret_key_from_twitter"

USER_TO_SNITCH = "the_username_of_the_twitter_account_you_want_to_check_up_on"

DISCORD_BOT_TOKEN = "the_bot_token_from_discord"
CHANNEL_ID = "the_ID_of_a_server's_channel_WHICH_CAN_BE_ONLY_AN_INTEGER_DONT_PUT_A_STRING_HERE"


auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)
user = api.get_user(screen_name = USER_TO_SNITCH)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print("Starting to fetch the last tweet from the " + USER_TO_SNITCH + " account")

    last_tweet = '0'

    while True:
        current_last_tweet = api.user_timeline(screen_name=USER_TO_SNITCH, count=1, include_rts = False, tweet_mode = 'extended')[0]
        print('---')
        if  (int(current_last_tweet.id_str) > int(last_tweet)) and (not current_last_tweet.full_text.startswith('RT')) and (not current_last_tweet.full_text.startswith('@')):
            last_tweet = current_last_tweet.id_str
            print()
            print(current_last_tweet.full_text)
            print('FOLLOWERS: ', current_last_tweet.user.followers_count)
            print(time.ctime())
            print('https://twitter.com/' + USER_TO_SNITCH + '/status/' + current_last_tweet.id_str)
            print('\n')
            msg = '_' + current_last_tweet.full_text + '_ \n **' + str(current_last_tweet.user.followers_count) + '** followers\nhttps://twitter.com/' + USER_TO_SNITCH + '/status/' + current_last_tweet.id_str 
            await client.get_channel(CHANNEL_ID).send(msg)

        time.sleep(60)

client.run(DISCORD_BOT_TOKEN)
