####################################
#                                  #
# This class has been designed to  #
# download data from yahoo finance #
#                                  #
####################################

from dateutil import parser
import pandas as pd
from datetime import datetime
from matplotlib import finance as fi

class yahooDownloadClass(object):
    
    description = "this class is used to download data from yahoo"
    author = "Jean-Mathieu Vermosen"

    # empty ctor
    def __init__(self):

        return
 
    # returns a dataframe
    def getDataFromYahoo(self, symbol, startDate):      

        hist = fi.fetch_historical_yahoo(symbol, 
                                         startDate, 
                                         datetime.today())
        
        newEntries = []                                 # new container

        for i in hist:                                  # split each line 
            newEntries.append(i[:-1].replace("-","/").split(','))

        try:

            col = newEntries.pop(0)

            for i in newEntries:                        # convert i[0] in datetime
                i[0] = datetime.strptime(i[0], '%Y/%m/%d')

            data = pd.DataFrame(newEntries, columns = col)

        except ValueError as e:
            print (e.trerror)
        return data

    # convert data to a file
    def data2file(self, sym, data, rootdir='your_dir'):

        fid = open('%s/%s'%(rootdir,sym),'w')

        for i in data:
            k = ",".join(i)
            fid.write(",".join([k,'\n']))