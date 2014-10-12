#####################################
#                                   #
# This simple procedure aims at     #
# fitting logistic regression       #
# from a simple financial series    #
#                                   #
#####################################

from distutils.sysconfig import get_python_lib

import math
import pandas
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from yahooDownloadClass import yahooDownloadClass as yahoo
from interactiveBrokerDownloadClass import interactiveBrokerDownloadClass as ib

pandas.set_option('display.notebook_repr_html', False)      # Set some Pandas options
pandas.set_option('display.max_columns', 20)
pandas.set_option('display.max_rows', 25)

code = 'MSFT'

# test 1 : IB
df2 = ib().requestData(code, date(2007, 1, 3))

# test 2 : yahoo
df = yahoo().getDataFromYahoo(code,                         # get data set through yahoo class
                              date(2007, 1, 3))    

df.Open = df.Open.replace('-', 'NaN',                       # data formatting
                          regex=True).astype('float')

df.Close = df.Close.replace('-', 'NaN', 
                            regex=True).astype('float')

df.High = df.High.replace('-', 'NaN', 
                          regex=True).astype('float')

df.Low = df.Low.replace('-', 'NaN', 
                        regex=True).astype('float')

df.Volume = df.Volume.replace('-', 'NaN', 
                              regex=True).astype('float')

# dataframe plot
fig = plt.figure(figsize=(8, 8))

df.Close.plot(ax=fig.gca())                                 # volume
plt.title(code, color='black')
plt.show()

# summarize data
print(df.describe())                                        # description
print(df.std())                                             # std


c_diff = df.Close / df.Open                                 # create the difference series
c_bool = (c_diff >= 1.0000000).astype('float')


reg = pandas.concat([c_bool,                                # the variable to explain
                     c_diff.shift(1),                       # the regressors
                     c_diff.shift(2),
                     c_diff.shift(3),
                     df.Volume.shift(1),
                     df.Volume.shift(2),
                     df.Volume.shift(3)], 
                    axis = 1)

reg.columns = ['move', 'diff_1', 'diff_2',                  # rename columns
               'diff_3', 'vol_1', 'vol_2', 
               'vol_3']

reg['intercept'] = 1.0                                      # manually add the intercept

reg = reg.drop(reg.index[:3])                               # drop the first data
#print("generated a clean data set...")
print(reg.head())                                           # print the data in a file

reg.to_csv('test.csv')                                      # convert data into csv
print('matrix rank:')                                       # check for singular values
print(np.linalg.matrix_rank(reg.values))                    # TODO: throw error if rank < nbcol

logit = sm.GLM(reg['move'],                                 # logit regression
               reg.ix[:,'diff_1':], 
               family = sm.families.Binomial(),#link=sm.families.links.log),
               missing = 'drop')

print(logit.fit().summary())                                # fit the regression