# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 18:31:55 2018

@author: xaxi
"""
import pymongo
import pandas as pd
import glob
import os
from sklearn import preprocessing


class warehouse:
    def __init__(self, host,port,name,symbols):
        self.client = pymongo.MongoClient("mongodb://"+host+":"+port+"/")[name]
        self.symbols = symbols
        
        
        
        
    def initialize_db(self,path):

        for symbol in self.symbols:
            collection = self.client[symbol] #collection
            collection.delete_many({})
            data = pd.read_csv(path+symbol+".csv",index_col=None, header=0)
            if 'Date' and 'Timestamp' in data.columns : 
                data['Datetime'] = [pd.to_datetime(str(datetime)+timestamp.replace(':','')) for datetime, timestamp in zip(data['Date'].values,data['Timestamp'].values)]
                data.drop(['Date','Timestamp'],axis=1,inplace = True)
            insert = collection.insert_many(data.to_dict('records'))
            
        
    def get_data(self,start,finish,train_test_split,input_columns,output_columns):
        frames = []
        for symbol in self.symbols:
            collection = self.client[symbol]
            rows_cursor = collection.find({"Datetime" : {"$gte": pd.to_datetime(start),"$lte": pd.to_datetime(finish)}})
            frames.append(pd.DataFrame(list(rows_cursor)).get(list(set(input_columns+output_columns)))) ##añadir nombre simbolo
        df = pd.concat(frames)
        split_index = int(len(df)*train_test_split)
        return df[:split_index],df[split_index:]
        
            
        
