import numpy as np
import keras
import random

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, Xs, labels, batch_size=32, dim=(110), n_channels=1, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.Xs = Xs
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.Xs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'

        # Generate data
        X, y = self.__data_generation()

        return X, y

    def on_epoch_end(self):
        pass

    def __data_generation(self):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim))
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        i = 0
        while i < self.batch_size:
            n = random.randint(0, len(self.Xs) - 1)
            # Store sample
            X[i] = np.reshape(self.Xs[n], (110))


            # Store class
            y[i] = self.labels[n]
            i += 1

        return X, y
