'''
Created on May 8, 2013
Copyright: Jev Kuznetsov
License: BSD

Module for downloading historic data from IB

'''

from datetime import datetime as dt

import ib
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message

import pandas as pd
from pandas import DataFrame, Index

import time
from time import sleep

class interactiveBrokerDownloadClass(object):

    def __init__(self,debug=False):                     # ctor

        self.tws = ibConnection()
        self._dataHandler = _HistDataHandler(self.tws)
            
        self.tws.connect() 
        
        self._timeKeeper = TimeKeeper()                 # keep track of past requests
        self._reqId = 1                                 # current request id
        
    def _debugHandler(self,msg):                        # debug
        print('[debug]', msg)
    
    def requestData(self,                               # request data
                    contract,
                    endDateTime,
                    durationStr='1 D',
                    barSizeSetting='30 secs',
                    whatToShow='TRADES',
                    useRTH=1,
                    formatDate=1):  
        
        if isinstance(endDateTime,dt):                  # convert to string
            endDateTime = endDateTime.strftime(timeFormat)
        
        while self._timeKeeper.nrRequests(timeSpan=600) > 59:
            print ('Too many requests done. Waiting... ')
            time.sleep(10)
        
        self._timeKeeper.addRequest()
        self._dataHandler.reset()
        self.tws.reqHistoricalData(self._reqId,contract,endDateTime,durationStr,barSizeSetting,whatToShow,useRTH,formatDate)
        self._reqId+=1
        
        startTime = time.time()                         # wait for data
        timeout = 3
        while not self._dataHandler.dataReady and (time.time()-startTime < timeout):
            sleep(2) 
        
        return self._dataHandler.data  
    
#     def getIntradayData(self,contract, dateTuple ):
#         ''' get full day data on 1-s interval 
#             date: a tuple of (yyyy,mm,dd)
#         '''
#         
#         openTime = dt.datetime(*dateTuple)+dt.timedelta(hours=16)
#         closeTime =  dt.datetime(*dateTuple)+dt.timedelta(hours=22)
#         
#         timeRange = pd.date_range(openTime,closeTime,freq='30min')
#         
#         datasets = []
#         
#         for t in timeRange:
#             datasets.append(self.requestData(contract,t.strftime(timeFormat)))
#         
#         return pd.concat(datasets)
        
    
    def disconnect(self):                               # disconnect
        self.tws.disconnect()    

class _HistDataHandler(object):

    ''' handles incoming messages '''
    def __init__(self,tws):                             # ctor
        tws.register(self.msgHandler)
        self.reset()
    
    def reset(self):                                    # reset

        self.dataReady = False
        self._timestamp = []
        self._data = {'open':[],'high':[],'low':[],'close':[],'volume':[],'count':[],'WAP':[]}
    
    def msgHandler(self,msg):                           # handle messages
        
        if msg.date[:8] == 'finished':

            self.dataReady = True
            return
        
        if len(msg.date) > 8:
            self._timestamp.append(dt.strptime(msg.date,timeFormat))
        else:
            self._timestamp.append(dt.strptime(msg.date,dateFormat))
                        
            
        for k in self._data.keys():
            self._data[k].append(getattr(msg, k))
    
    @property                                           # properties
    
    def data(self):                                     # data
    
        ''' return  downloaded data as a DataFrame '''
        df = DataFrame(data=self._data,index=Index(self._timestamp))
        return df
    
class TimeKeeper(object):                               # timekeeper object
    
    ''' 
    class for keeping track of previous requests, to satify the IB requirements
    (max 60 requests / 10 min)
    
    each time a requiest is made, a timestamp is added to a txt file in the user dir.
    
    '''
    
    def __init__(self):                                 # ctor

        #dataDir = os.path.expanduser('~')+'/twpData'
        #if not os.path.exists(dataDir):
        #    os.mkdir(dataDir)

        #self._timeFormat = "%Y%m%d %H:%M:%S"
        #self.dataFile = os.path.normpath(os.path.join(dataDir,'requests.txt'))
        #self._log.debug('Data file: {0}'.format(self.dataFile))
        return

    def addRequest(self):                               # add a request

        ''' adds a timestamp of current request'''
        #with open(self.dataFile,'a') as f:
        #    f.write(dt.datetime.now().strftime(self._timeFormat)+'\n')
            

    def nrRequests(self, timeSpan = 600):

        ''' return number of requests in past timespan (s) '''
        #delta = dt.timedelta(seconds=timeSpan)
        #now = dt.now()
        requests = 0
        
        #with open(self.dataFile, 'r') as f:
        #    lines = f.readlines()
            
        #for line in lines:
        #    if now-dt.datetime.strptime(line.strip(),self._timeFormat) < delta:
        #        requests+=1
    
        #if requests==0: # erase all contents if no requests are relevant
        #    open(self.dataFile,'w').close() 
            
        return requests