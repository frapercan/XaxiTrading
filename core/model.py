import os
import math
import numpy as np
import datetime as dt
from numpy import newaxis
from core.utils import Timer
from keras.layers import Dense, Activation, Dropout, CuDNNLSTM
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

class Model():
    """A class for an building and inferencing an lstm model"""
    def __init__(self):
        self.model = Sequential()

    def load_model(self, filepath):
        print('[Model] Loading model from file %s' % filepath)
        self.model = load_model(filepath)

    def build_model(self, configs):
        timer = Timer()
        timer.start()

        for layer in configs['model']['layers']:
            neurons = layer['neurons'] if 'neurons' in layer else None
            dropout_rate = layer['rate'] if 'rate' in layer else None
            activation = layer['activation'] if 'activation' in layer else None
            return_seq = layer['return_seq'] if 'return_seq' in layer else None
            input_timesteps = layer['input_timesteps'] if 'input_timesteps' in layer else None
            input_dim = layer['input_dim'] if 'input_dim' in layer else None

            if layer['type'] == 'dense':
                self.model.add(Dense(neurons, activation=activation))
            if layer['type'] == 'lstm':
                self.model.add(CuDNNLSTM(neurons, input_shape=(input_timesteps, input_dim), return_sequences=return_seq))
            if layer['type'] == 'dropout':
                self.model.add(Dropout(dropout_rate))

        self.model.compile(loss=configs['model']['loss'], optimizer=configs['model']['optimizer'])

        print('[Model] Model Compiled')
        timer.stop()
        
        
#    def predict_point_by_point(self,data_generator):
#        k = self.model.predict_generator(data_generator)
#        plt.plot(k)
#        outputs = []
#        for i in data_generator:
#            outputs.append(i[1])
#            
#        shape = np.array(outputs).shape
#        print(shape)
#        plt.plot(np.array(outputs).reshape([shape[0]*shape[1],]))
#        plt.show()
#        return outputs
#
#    def predict_multiple(self,data_generator,batch_size,sequence_lenght,steps_ahead):
#        k = self.model.predict_generator(data_generator) #(384,3)
#        print(np.array(k).shape)
#        
#        for i,predictions in enumerate(k):
#            for step_ahead in range(steps_ahead):
#                plt.plot(i+step_ahead,predictions[step_ahead])
#        plt.show()
            
            
            
        

