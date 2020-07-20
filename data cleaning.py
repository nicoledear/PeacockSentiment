### DATA CLEANING ###

# import libraries

import tweepy
import numpy as np
import pandas as pd

from textblob import TextBlob
from wordcloud import WordCloud

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')

%matplotlib inline

# import data

twitter_data = pd.read_csv('filtered_results.csv', index_col = 0)
twitter_data.columns = ['Timestamp', 'User', 'Location', 'Tweet']

# clean data
# remove URLs and special symbols

def cleanTxt(text):
    text = re.sub(r'https?:\/\/\S+', '', text) #removes URLs
    text = re.sub(r'@', '', text) #remove the at symbol
    #text = re.sub(r'@[A-za-z0-9]+', '', text) #removes @mentions
    text = re.sub(r'#', '', text) #removing the hashtag symbol

    text = re.sub(r"[\!\$\%\^\&\*\(\)\[\]\{\}\;\:\,\/\<\>\?\|\`\~\-\=\_\+\"]", '', text) #remove special characters
    text = re.sub(r"\.\.\.", ' ', text)
    text = re.sub(r"\n", ' ', text)
    text = re.sub(r"amp", '', text)
    text = re.sub(r"  ", ' ', text)
    
    return text

twitter_data['Tweet'] = twitter_data['Tweet'].apply(cleanTxt)

tweets_df = twitter_data.copy()

tweets_df.reset_index(drop = True, inplace = True)

# tokenize

tk = TweetTokenizer()

tweets_df['tokenized text'] = tweets_df['Tweet'].apply(tk.tokenize)

# remove stopwords

stop_words = set(stopwords.words('english'))

tweets_df['tokenized NoStopWords'] = tweets_df['tokenized text'].apply(lambda x: 
                                  [item for item in x if item.lower() not in stop_words])

# remove the words we searched for

other_words = {'peacock', 'tv', 'peacocktv'}

tweets_df['tokenized text'] = tweets_df['tokenized text'].apply(lambda x: 
                                  [item for item in x if item.lower() not in other_words])

# identify and replace emojis
# 'tokenized text' will be used for the polarity analysis
# 'tokenized NoStopWords' will be used to count common words

emojis = pd.read_csv('emojis.csv', index_col = 0)

def cleanEmoji(text):
    text = re.sub(r' ', '', text) #removes spaces
    
    return text

emojis['n'] = emojis['o'].apply(cleanEmoji)

for row in range(0, len(tweets_df)):
    for word in range(0, len(tweets_df['tokenized text'][row])):
        for i in range(0, len(emojis)):
            if tweets_df.iloc[row, 4][word] == emojis.iloc[i,0]:
                tweets_df.iloc[row, 4][word] = emojis.iloc[i,1]
            else:
                pass

for row in range(0, len(tweets_df)):
    for word in range(0, len(tweets_df['tokenized NoStopWords'][row])):
        for i in range(0, len(emojis)):
            if tweets_df.iloc[row, 5][word] == emojis.iloc[i,0]:
                tweets_df.iloc[row, 5][word] = emojis.iloc[i,2]
            else:
                pass

for i in range(0, len(tweets_df)):
    tweets_df['clean text'][i] = ' '.join(tweets_df['tokenized text'][i])

for i in range(0, len(tweets_df)):
    tweets_df['clean NoStop text'][i] = ' '.join(tweets_df['tokenized NoStopWords'][i])

for i in range(0, len(tweets_df)):
    tweets_df.iloc[i, 6] = ' '.join(tk.tokenize(tweets_df.iloc[i, 6].encode('utf-8')))                                                                            

for i in range(0, len(tweets_df)):
    tweets_df.iloc[i, 7] = ' '.join(tk.tokenize(tweets_df.iloc[i, 7].encode('utf-8')))

tweets_df.reset_index(drop = True, inplace = True)

# remove references to peacock since these were used in our initial twitter search
# keep FlockToPeacock, the hashtag used for PeacockTV

def cleanTxtpeacock(text):
    
    text = re.sub('FlockToPeacock', 'FlockToZeacock', text)
    text = re.sub('peacockTV', '', text)
    text = re.sub('PeacockTVCare', '', text)
    text = re.sub('peacocks', '', text)
    text = re.sub('peacock', '', text)
    text = re.sub('Peacocks', '', text)
    text = re.sub('Peacock', '', text)
    text = re.sub('FlockToZeacock', 'FlockToPeacock', text)
    
    return text

tweets_df['clean NoStop text'] = tweets_df['clean NoStop text'].apply(cleanTxtpeacock)

# remove tweets unrelated to Peacock the streaming service (i.e. tweets about the bird)
# see 'sentiment analysis.py' for an alternative way to filter tweets; doesn't require generating a filter column

words1 = ['animal', 'animals', 'bird', 'birds']
words2 = ['nbc', 'NBC', "NBC's", 'Streaming', 'streaming', 'stream', 'Stream', 'app', 'comcast', 'Comcast']

for i in range(0, len(tweets_df)):
    if any(x in tweets_df['tokenized text'][i] for x in words1) and any(x in tweets_df['tokenized text'][i] for x in words2):
        tweets_df.loc[i, 'filter'] = False
    elif any(x in tweets_df['tokenized text'][i] for x in words1):
        tweets_df.loc[i, 'filter'] = True
    else:
        tweets_df.loc[i, 'filter'] = False

filtered_tweets = tweets_df[tweets_df['filter'] == False].drop('filter', axis = 1)
filtered_tweets.reset_index(drop = True, inplace = True)

# save dataframe as csv

FILE_PATH = 'final_data.csv'

filtered_tweets.to_csv(FILE_PATH)                    