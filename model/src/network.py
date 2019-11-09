import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Input, Flatten, Dropout

def get_network(initial_filters = 128, depth = 8, activation_func = 'relu', input_shape=(98,)):
    model = Sequential()
    model.add(Dense(initial_filters, activation=activation_func, input_shape=input_shape))
    i = 0
    while i < depth // 2:
        model.add(Dense(initial_filters, activation=activation_func))
        initial_filters *= 2
        i += 1
    initial_filters //= 2
    i = 0
    while i < depth // 2:
        model.add(Dense(initial_filters, activation=activation_func))
        initial_filters //= 2
        i += 1
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='mse', metrics=['mse'], optimizer='adam')

    return model
