import pandas as pd
import statsmodels.api as sm
import numpy as np
import pylab as pl
import talib as ta

from datetime import date, timedelta
from yahooDownloadClass import yahooDownloadClass  as yahoo
 
# testing yahoo class
df2 = yahoo().getDataFromYahoo("AUD=X", date(2007, 1, 3))

# read the data from the internet
df = pd.read_csv("http://www.ats.ucla.edu/stat/data/binary.csv")
 
df.columns = ["admit",          # rename columns
              "gre", 
              "gpa", 
              "prestige"]

#summarize data
print(df.describe())            # description
print(df.std())                 # std
print(pd.crosstab(df['admit'],  # crosstab
                  df['prestige'], 
                  rownames=['admit']))

# create a clean data frame for the regression
dummy_ranks = pd.get_dummies(   # dummify rank
                  df['prestige'], 
                  prefix='prestige')

cols_to_keep = ['admit', 'gre', 'gpa']
data = df[cols_to_keep].join(   # merge with existing data
           dummy_ranks.ix[:, 'prestige_2':])

data['intercept'] = 1.0         # manually add the intercept

print("generates a clean data set...")
print(data.head())              # print the fina data set

train_cols = data.columns[1:]
# Index([gre, gpa, prestige_2, prestige_3, prestige_4], dtype=object)
 
logit = sm.Logit(data['admit'], data[train_cols])
 
# fit the model
result = logit.fit()

print(result.summary())

df.hist()                       # prints histogram
pl.show()