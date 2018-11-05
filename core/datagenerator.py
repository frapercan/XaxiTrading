import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, X,input_columns, output_columns, batch_size, sequence_lenght,steps_ahead,normalise):
        'Initialization'
        self.batch_size = batch_size
        self.X = X
        self.input_columns = input_columns
        self.output_columns = output_columns
        self.sequence_lenght = sequence_lenght
        self.steps_ahead = steps_ahead
        self.on_epoch_end()
        self.normalise = normalise

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor((len(self.X)-self.sequence_lenght)/self.batch_size))

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.X))
        
    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate samples of the batch
        data_windows = []
        for i in range(self.batch_size):
            data_window = self.X[index*self.batch_size+i:index*self.batch_size+i+self.sequence_lenght]
            data_windows.append(data_window)
        # Generate data
        X,y = self.__data_generation(data_windows)

        return X,y


    def __data_generation(self, data_windows,):
        'Generates data containing batch_size samples' # X : (n_samples, lenght, input dim) Y :(n_samples,output_dim)
        # Initialization

        X = np.empty((self.batch_size, self.sequence_lenght-self.steps_ahead, len(self.input_columns)))
        y = np.empty((self.batch_size,self.steps_ahead), dtype=float)
        # Generate data
        for i,window in enumerate(data_windows):
            if self.normalise:
                for j,column in enumerate(window.columns):
                    normalized_window = [((float(p) / float(window.get(column).values[0])) - 1) for p in window.get(column).values]
#                    print(np.mean(normalized_window))
#                    print(np.std(normalized_window))
                    X[i,:,j] = normalized_window[:-self.steps_ahead]
                    if column in self.output_columns:
                        y[i] = normalized_window[-(self.steps_ahead):]
            else:
                
                X[i,:,:] = window.values[:self.steps_ahead]
                y[i] = window.get(self.output_columns).values[-self.steps_ahead]

                    

        return X,y