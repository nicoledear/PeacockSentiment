### EXTRACT EMOJIS ###

# load libraries

import pandas as pd

# import data

df = pd.read_html('https://unicode.org/emoji/charts/full-emoji-list.html')
df_1 = pd.DataFrame(df[0])
df_1.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']

# delete unnecessary columns
df_1 = df_1[['c', 'o']]

# keep the first 249 emojis

df_1 = df_1.iloc[0:300, :]

# save dataframe as csv

FILE_PATH = 'emojis.csv'

df_1.to_csv(FILE_PATH)