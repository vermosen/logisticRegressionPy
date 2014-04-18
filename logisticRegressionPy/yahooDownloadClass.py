from dateutil import parser
import numpy as np
from array import array
from datetime import date, timedelta
from matplotlib import finance

class yahooDownloadClass(object):
    """description of class"""

    def __init__(self):
        return
 
    def getDataFromYahoo(symbol,firstDate): 
        man = "%s, %s, %s" %(firstDate[0],firstDate[1],firstDate[2])
        startDate = parser.parse(man) + timedelta(1)
        #print startDate, date.today()
        hist = finance.fetch_historical_yahoo(symbol,startDate,date.today())
        newEntries = []
        for i in hist: newEntries.append(i[:-1].replace("-",",").split(','))
        return newEntries[1:]
 
    def data2file(sym,data,rootdir='your_dir'):
        fid = open('%s/%s'%(rootdir,sym),'w')
        for i in data:
            k = ",".join(i)
            fid.write(",".join([k,'\n']))
 
 
        if __name__ == "__main__":
 
            print self.getDataFromYahoo('AUD=X',[2006,1,1]) 
            sym = 'EWA'
            price = getDataFromYahoo(sym,[2005,1,1])
            data2file(sym,price)

