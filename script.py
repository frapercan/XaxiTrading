#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:00:10 2018

@author: xaxi
"""

import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
import json
import os
from core.datawarehouse_gateway import warehouse
from core.datagenerator import DataGenerator
from keras.layers import Dense, Activation, Dropout, CuDNNLSTM
from core.model import Model
from PyEMD import EMD
# Parameters
#params = {'dim': (32,32,32),
#          'n_classes': 6,
#          'n_channels': 1,
#          'shuffle': True,
#          }
configs = json.load(open('config.json', 'r'))
initialization = configs['initialization']
mongo_params = configs['mongo_request']
data_selection_params = configs['data_selection']
training_configs = configs['training']
model_params = configs['model']

batch_size = training_configs['batch_size']
sequence_lenght = training_configs['sequence_lenght']
steps_ahead = training_configs['steps_ahead']
if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
#
#

# Datasets
data_warehouse = warehouse(**mongo_params)

if initialization["first_execution"]:
    data_warehouse.initialize_db(initialization["path"])
train_data,test_data = data_warehouse.get_data(**data_selection_params)




    
# Generators
train_generator = DataGenerator(train_data,data_selection_params['input_columns'],data_selection_params['output_columns'],batch_size,sequence_lenght,steps_ahead,training_configs['normalise'])
validation_generator = DataGenerator(test_data,data_selection_params['input_columns'],data_selection_params['output_columns'],batch_size,sequence_lenght,steps_ahead,training_configs['normalise'])

# Model
model = Model()
model.build_model(configs)

#Trainning model
history = model.model.fit_generator(generator=train_generator,epochs=training_configs['epochs'],validation_data=validation_generator)






