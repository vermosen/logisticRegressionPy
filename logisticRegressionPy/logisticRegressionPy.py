#####################################
#                                   #
# This simple procedure aims at     #
# fitting logistic regression       #
# from a simple financial series    #
#                                   #
#####################################

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from yahooDownloadClass import yahooDownloadClass  as yahoo

pd.set_option('display.notebook_repr_html', False)          # Set some Pandas options
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 25)

df = yahoo().getDataFromYahoo("AUD=X",                      # get data set through yahoo class
                              date(2007, 1, 3))    

# data formatting
df.Open = df.Open.replace('-', 
                          'NaN', 
                          regex=True).astype('float')

df.Close = df.Close.replace('-', 
                            'NaN', 
                            regex=True).astype('float')

# dataframe plot
fig = plt.figure(figsize=(8, 8))

df.Open.plot(ax=fig.gca())                                  # open
plt.title('open', color='black')
plt.show()

df.Close.plot(ax=fig.gca())                                 # close
plt.title('close', color='black')
plt.show()

# create a clean data fram for the regression


# read the data from the internet
df2 = pd.read_csv("http://www.ats.ucla.edu/stat/data/binary.csv")
 
df2.columns = ["admit",          # rename columns
              "gre", 
              "gpa", 
              "prestige"]

#summarize data
print(df2.describe())            # description
print(df2.std())                 # std
print(pd.crosstab(df2['admit'],  # crosstab
                  df2['prestige'], 
                  rownames=['admit']))

# create a clean data frame for the regression
dummy_ranks = pd.get_dummies(   # dummify rank
                  df2['prestige'], 
                  prefix='prestige')

cols_to_keep = ['admit', 'gre', 'gpa']
data = df2[cols_to_keep].join(   # merge with existing data
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

df2.hist()                       # prints histogram