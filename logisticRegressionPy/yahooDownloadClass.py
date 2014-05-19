from dateutil import parser
import pandas as pd
from datetime import datetime
from matplotlib import finance

class yahooDownloadClass(object):
    
    description = "this class is used to download data from yahoo"
    author = "Jean-Mathieu Vermosen"

    def __init__(self):

        return
 
    def getDataFromYahoo(self, symbol, firstDate): 

        man = "%s, %s, %s" %(firstDate[0],
                             firstDate[1],
                             firstDate[2])

        startDate = parser.parse(man) + timedelta(1)
        return getDataFromYahoo(symbol, startDate)
 
    def getDataFromYahoo(self, symbol, startDate):      # returns a dataframe

        hist = finance.fetch_historical_yahoo(symbol, 
                                              startDate, 
                                              datetime.today())
        
        newEntries = []                                 # container

        for i in hist: 
            newEntries.append(i[:-1].replace("-","/").split(','))

        try:

            col = newEntries.pop(0)

            for i in newEntries:                        # TODO: regroup the 2 for loops...
                i[0] = datetime.strptime(i[0], '%Y/%m/%d')

            data = pd.DataFrame(newEntries, columns = col)

        except ValueError as e:
            print (e.trerror)
        return data

    def data2file(self, sym, data, rootdir='your_dir'):

        fid = open('%s/%s'%(rootdir,sym),'w')

        for i in data:
            k = ",".join(i)
            fid.write(",".join([k,'\n']))
