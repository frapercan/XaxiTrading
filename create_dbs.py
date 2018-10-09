#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 14:49:41 2018

@author: xaxipiruli
"""

import pandas as pd
import pymongo
import glob
import os

symbols = ['BTC','IOT','ZEC']
intervals = ['15t','1h','1d']

class create_cryptodb():
    def __init__(host='localhost',port='27017',symbol = 'BTC',interval = '15t'):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        client = client["crypto"]
        collection = client[symbol+interval] #collection
        collection.delete_many({})
        data = cargar_datos(symbol,interval)
#        print(data)
        insert = collection.insert_many(data.to_dict('records'))


def cargar_datos(symbol,interval):
    path =r'/home/xaxipiruli/Documents/data/'+symbol+'/'+interval # use your path
    allFiles = glob.glob(os.path.join(path, "*"))  
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
        frame = pd.concat(list_,ignore_index = True)
    return frame
     

for symbol in symbols:
    for interval in intervals:
        print('rebuilding: ' + symbol + ' ' +'interval' + interval )
        create_cryptodb(symbol = symbol, interval = interval)






#x = collection.find_one()




