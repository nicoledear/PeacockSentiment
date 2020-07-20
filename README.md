# Sentiment Analysis: PeacockTV

Welcome! This is my first self-motivated independent project. It's also my first hands-on experience with Python and NLP.

# Inspiration

NBC launched a streaming service called PeacockTV on July 15, 2020. One of NBC's strategies to enter a competitve and somewhat saturated market was to offer a free-to-stream basic level in addition to paid premium levels. NBC also announced that they wouldn't be investing nearly as much money in the business and launch as some of their competitors, like Disney+. These specific circumstances piqued my interest. Additionally, the launch of a new brand is a great opportunity to explore how a sentiment analysis could be used to support a new business venture.

# About The Project

This project aims to identify general feelings (negative/positive/neutral) of tweets about PeacockTV on its nationwide launch day. We look at a summary of the polarity analysis, common words, as well as an exploration on how this analysis can be used to advance PeacockTV.

# Getting Started

Language: Python<br/>

## Packages

NumPy, Pandas, Matplotlib.Pyplot, tweepy, re, nltk, wordcloud, textblob

## Prerequisites

Must have Twitter API keys<br/>
1. Create a Twitter account
2. Go to www.developer.twitter.com
3. Create a Twitter Application
4. Get: Consumer Key, Consumer Secret, Access Token, Access Token Secret

# Approach
1. Extract Twitter data using Tweepy<br/>
see: extract twitter data.py
2. Extract emoji list using pandas<br/>
see: extract emojis.py
3. Preprocess data using re<br/>
see: data cleaning.py
4. Analysis: Perform a sentiment analysis using textblob. Generate visualizations with matplotlib.pyplot and wordcloud<br/>
see: sentiment analysis.py

# Findings
https://www.nicoledear.com/post/sentiment-analysis-peacocktv
