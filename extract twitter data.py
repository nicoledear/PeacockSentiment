### EXTRACT DATA FROM TWITTER ###

# import libraries

import tweepy
import numpy as np
import pandas as pd

# connect to twitter (replace XXXX with your info)

auth = tweepy.auth.OAuthHandler('XXXX', 'XXXX')
auth.set_access_token('XXXX-XXXX', 'XXXX')

# create empty dataframe to hold twitter data

tweets_df = pd.DataFrame()

# extract tweets

search_terms = 'peacock streaming OR peacocktv OR peacock AND -filter:retweets'

for tweet in tweepy.Cursor(api.search, q = search_terms, since = "2020-07-15", until = "2020-07-16",
                           tweet_mode = 'extended', lang = 'en').items():

    created = tweet.created_at
    name = tweet.user.screen_name
    loc = tweet.user.location
    text = tweet.full_text
    
    row = [created, name, loc, text]
    row = np.transpose(pd.DataFrame(row))
    tweets_df = tweets_df.append(row)
    tweets_df.reset_index(drop = True, inplace = True)    

# save dataframe to csv

FILE_PATH = 'results.csv'

tweets_df.to_csv(FILE_PATH)