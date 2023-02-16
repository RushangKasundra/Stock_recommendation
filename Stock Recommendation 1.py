# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 11:57:30 2023

@author: rusha
"""
###get Data
import pypyodbc as odbc
import pandas as pd
import yfinance as yf
import sqlalchemy as sal
from sqlalchemy import create_engine

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=DESKTOP-AN3LI16\SQLEXPRESS;'
    r'DATABASE=project;'
    r'Trusted_Connection=yes;'
)
cnxn = odbc.connect(conn_str, autocommit=True)
cursor=cnxn.cursor()
print(cnxn)
# query = 'CREATE DATABASE Nifty'
# cursor.execute(query)

engine=create_engine('mssql://@DESKTOP-AN3LI16\SQLEXPRESS/Nifty?driver=SQL Server')
con=engine.connect()


nifty=pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[1]
nifty=nifty.Symbol.to_list()

nifty_50 = [i+'.NS' for i in nifty]




# df=yf.download(nifty_50[1],start='2020-01-01')
# df=df.reset_index()
# df.to_sql(nifty_50[1], engine)


for symbol in nifty_50:
    df=yf.download(symbol,start='2020-01-01')
    df=df.reset_index()
    df.to_sql(symbol, engine)
    

