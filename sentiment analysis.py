### SENTIMENT ANALYSIS ###

# import libraries

import tweepy
import numpy as np
import pandas as pd

from textblob import TextBlob
from wordcloud import WordCloud

import re
import nltk
from nltk.tokenize import TweetTokenizer

import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')

%matplotlib inline

# import data

filtered_tweets = pd.read_csv('final_data.csv', index_col = 0)

# drop empty tweets

filtered_tweets.dropna(subset = ['clean NoStop text'], inplace = True)
filtered_tweets.reset_index(drop = True, inplace = True)

# prepare data for senitment analysis

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

df = filtered_tweets['clean text']

data = pd.DataFrame({'Tweet': df, 
                     'Subjectivity': df.apply(getSubjectivity), 
                     'Polarity': df.apply(getPolarity)})

# load image to be used for word cloud

from PIL import Image
mask = np.array(Image.open('XXXX.png'))

# prepare data for word cloud

allWords = ' '.join([twts for twts in filtered_tweets['clean NoStop text']])

# generate word cloud

plt.figure(dpi = 1000)
wordCloud = WordCloud(background_color = 'white', width = 800, height = 500, random_state = 21,
                     max_font_size = 200, mask = mask, max_words = 250, collocations = False,
                     relative_scaling = 0.6, colormap = 'Dark2').generate(allWords)
plt.imshow(wordCloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()

# prepare text for count by word

wordCount = [allWords]
df = pd.DataFrame(wordCount,columns=['text'])
count = df.text.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)

count_df = pd.DataFrame(count)
count_df.columns = ['count']
count_df.sort_values(by = 'count', ascending = False, inplace = True)

# exclude symbols and numbers

count_df = count_df[count_df['count'] < 3010]
count_df = count_df.drop(index = "'")
count_df = count_df.drop(index = '2')
top20words = count_df.head(20).reset_index()

# plot top 20 most common words

sns.set_style('whitegrid')
plt.figure(dpi = 1000)
top20words.plot(kind = 'line', x = 'index', legend = None, figsize = (15, 5))
tickLabels = top20words['index']
plt.xticks(range(0, 20), tickLabels, rotation = 90, fontsize = 20)
plt.yticks(fontsize = 18)
plt.title('Top 20 Most Common Words')

# sort tweets into category based on polarity score

def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

data['Analysis'] = data['Polarity'].apply(getAnalysis)

# generate pie chart

plt.figure(dpi = 1000)
plt.pie(x = data.groupby('Analysis').agg('count')['Tweet'], labels = ['Negative', 'Neutral', 'Positive'], 
        autopct='%1.1f%%', colors = ['lightcoral', 'yellowgreen', 'lightskyblue'])

# join tables to combine tweets and polarity scores

left = filtered_tweets.iloc[:,6:]
right = data.copy()
joinDF = pd.concat([left, right], axis = 1)

# get highly negative tweets

neg = joinDF[joinDF['Analysis'] == 'Negative']
neg = neg[neg['Polarity'] <= -0.5]

negWords = ' '.join([twts for twts in neg['clean NoStop text']])
negWordCount = [negWords]
neg_df = pd.DataFrame(negWordCount,columns=['text'])

# get counts of each word

neg_count = neg_df.text.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)
neg_count = pd.DataFrame(neg_count)
neg_count.columns = ['count']
neg_count.sort_values(by = 'count', ascending = False, inplace = True)

# exclude symbols

neg_count = neg_count[neg_count['count'] < 82]
top10neg = neg_count.head(10).reset_index()

# plot top 10 words from negative tweets

plt.figure(dpi = 1000)
top10neg.plot(x = 'index', y = 'count', kind = 'line', legend = None, figsize = (15, 5))
tickLabels = top10neg['index']
plt.xticks(range(0, 10), tickLabels, rotation = 45, fontsize = 20)
plt.yticks(fontsize = 20)
plt.ylim(0, 50)
plt.xlabel('')
plt.ylabel('count')
plt.title('PeacockTV | Negative Tweets: Top 10 Most Common Words')

# get highly positive tweets

pos = joinDF[joinDF['Analysis'] == 'Positive']
pos = pos[pos['Polarity'] > 0.5]

posWords = ' '.join([twts for twts in pos['clean NoStop text']])
posWordCount = [posWords]
pos_df = pd.DataFrame(posWordCount,columns=['text'])

# get counts of each word
pos_count = pos_df.text.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)
pos_count = pd.DataFrame(pos_count)
pos_count.columns = ['count']
pos_count.sort_values(by = 'count', ascending = False, inplace = True)

# exclude symbols

pos_count = pos_count[pos_count['count'] < 116]
top20pos = pos_count.head(10).reset_index()

# plot top 10 words from positive twets

plt.figure(dpi = 1000)
top20pos.plot(x = 'index', y = 'count', kind = 'line', legend = None, figsize = (15, 5))
tickLabels = top20pos['index']
plt.xticks(range(0, 10), tickLabels, rotation = 45, fontsize = 20)
plt.yticks(fontsize = 20)
plt.ylim(0, 100)
plt.xlabel('')
plt.ylabel('count')
plt.title('PeacockTV | Positive Tweets: Top 10 Most Common Words')

# get negative tweets

temp_df = pd.concat([filtered_tweets, data], axis = 1)
temp_df = temp_df[['Tweet', 'tokenized NoStopWords', 'Polarity']]
temp_df = temp_df[temp_df['Polarity'] < -0.5]
temp_df.reset_index(drop = True, inplace = True)

# get negative tweets with the word 'Roku'

index = []

for i in range(0, len(temp_df)):
    if 'Roku' in temp_df.iloc[i, 2]:
        index.append(i)
    else:
        pass

roku_df = temp_df[temp_df.index.isin(index)]

# display tweets

pd.set_option('display.max_colwidth', None)
roku_df = pd.DataFrame(roku_df.iloc[:, 0])
roku_df.reset_index(drop = True, inplace = True)
roku_df.style.set_properties(**{'text-align': 'left'})


# get negative tweets with the word 'NBCSportsSoccer'

index = []

for i in range(0, len(temp_df)):
    if 'NBCSportsSoccer' in temp_df.iloc[i, 2]:
        index.append(i)
    else:
        pass

# display tweets

sports_df = temp_df[temp_df.index.isin(index)]
sports_df = pd.DataFrame(sports_df.iloc[:, 0])
sports_df.reset_index(drop = True, inplace = True)
sports_df.style.set_properties(**{'text-align': 'left'})                        

