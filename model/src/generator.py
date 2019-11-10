import numpy as np
import keras
import random

def add_noise_scalar(s, fraction_of_mean):
    return np.random.normal(s, 1, 1)[0]

def add_noise_vector(S, fraction_of_mean):
    for s in S:
        s = add_noise_scalar(s, fraction_of_mean)
    return S

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, Xs, labels, batch_size=256, dim=(110), n_channels=1, shuffle=True, aug=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.Xs = Xs
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.aug = aug
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
        y = np.empty((self.batch_size), dtype='float32')

        # Generate data
        n = np.random.randint(0, len(self.Xs) - 1, self.batch_size)
        # Store sample
        X = self.Xs[n]

        if self.aug:
            i = 0
            while i < len(X):
                X[i] = add_noise_vector(X[i], 0.15)
                i += 1


        # Store class
        y = self.labels[n]

        return X, y
