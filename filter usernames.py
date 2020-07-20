### FILTER TWITTER RESULTS ###

# load libraries

import tweepy
import numpy as np
import pandas as pd

# import data

df = pd.read_csv('results.csv', index_col = 0)
df.columns = ['Timestamp', 'User', 'Location', 'Tweet']

# remove tweets from users related to NBC

df = df[df['User'] != 'PeacockTVCare']
df = df[df['User'] != 'nbc']
df = df[df['User'] != 'peacockTV']
df = df[df['User'] != 'NBCUinterns']
df = df[df['User'] != 'NBCNews']
df = df[df['User'] != 'MSNBC']

# save dataframe as csv

FILE_PATH = 'filtered_results.csv'

df.to_csv(FILE_PATH)