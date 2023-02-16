# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 11:28:46 2023

@author: rusha
"""

import pandas as pd
import numpy as np
import yfinance as yf
import sqlalchemy as sal
from sqlalchemy import create_engine
import ta

class Recommender:
    
    def __init__(self,index):
        self.index=index
        self.engine=create_engine(f'mssql://@DESKTOP-AN3LI16\SQLEXPRESS/{self.index}?driver=SQL Server')
        
    def gettables(self):
        query = f'select name from {self.index}.sys.tables'
        df=pd.read_sql(query,self.engine)
        df['Schema'] = self.index
        
        return df
    
    
    
    def getprices(self):
        prices =[]
        for table,Schema in zip(self.gettables().name,self.gettables().Schema):
            prices.append(pd.read_sql( f'select * from {Schema}.dbo.[{table}]',self.engine))
        return prices
    
    def maxdate(self):
        req=self.index+'.dbo.'+ f'[{self.gettables().name[0]}]'
        return pd.read_sql(f"SELECT MAX(Date) FROM {req}",self.engine)
    
    def updateDB(self):
        maxdate = self.maxdate().iloc[0][0]
    
        
        for symbol in self.gettables().name:
            data = yf.download(symbol,start = maxdate)
            data=data[data.index>maxdate]
            data=data.reset_index()
            data.to_sql(symbol,self.engine,if_exists='append')
        print('Successfull')

    def MACDdefination(self,df):
        df['MACD_diff'] = ta.trend.macd_diff(df.Close)
        df['Decision MACD']=np.where((df.MACD_diff>0)&(df.MACD_diff.shift(1)<0) ,True ,False)

    def GoldenCrossdecision(self,df):
        df['SMA20'] = ta.trend.sma_indicator(df.Close,window=20)
        df['SMA50'] = ta.trend.sma_indicator(df.Close,window=50)
        df['Signal'] = np.where(df['SMA20'] > df['SMA50'],True,False)
        df['Decision GC'] = df.Signal.diff()
        
    def RSI_SMAdecision(self,df):
        df['RSI'] = ta.momentum.rsi(df.Close,window=10)
        df['SMA200'] = ta.trend.sma_indicator(df.Close,window=200)
        df['Decision RSI/SMA']=np.where((df.Close>df.SMA200)&(df.RSI<30) ,True ,False)
        
    def applytechnicals(self):
        prices=self.getprices()
        for frame in prices:
            self.MACDdefination(frame)
            self.GoldenCrossdecision(frame)
            self.RSI_SMAdecision(frame)
        return prices
    
    def recommender(self):
        rec = []
        indicators = ['Decision MACD','Decision GC','Decision RSI/SMA']
        for symbol,frame in zip(self.gettables().name, self.applytechnicals()):
            if frame.empty is False:
                for indicator in indicators:
                    if frame[indicator].iloc[-1] == True:
                        rec.append(f"{indicator} buying signal for " + symbol)
        return rec
# nifty = Recommender('Nifty')

# print(nifty.recommender())
# maxdate=nifty.maxdate()





# data.drop(columns = 'index',inplace=True)

# engine=create_engine('mssql://@DESKTOP-AN3LI16\SQLEXPRESS/Nifty?driver=SQL Server')

# data = yf.download('TCS.NS',start = maxdate.iloc[0,0])
# data=data[data.index> maxdate.iloc[0,0]]
# data=data.reset_index()
# data.to_sql('TCS.NS',engine, if_exists='append')





                        