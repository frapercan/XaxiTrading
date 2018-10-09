#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 20:07:59 2018

@author: xaxipiruli

"""

from time import sleep
from json import dumps
from kafka import KafkaProducer
import bitfinex


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

for e in range(10):
    data = bitfinex.ticker()
    producer.send('numtest', value=data)
    sleep(5)