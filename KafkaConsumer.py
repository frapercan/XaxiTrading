#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 20:09:00 2018

@author: xaxipiruli
"""

from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads


consumer = KafkaConsumer(
    'numtest',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8'))
     )


client = MongoClient('localhost:27017')
client = client['crypto']
collection = client['IOT']




for message in consumer:
    message = message.value
    print(message)
    collection.insert(message)
#    consumer.close()
    
    
    
    
