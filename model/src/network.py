import tensorflow as tf
import keras.backend as K
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Input, Flatten, Dropout, BatchNormalization, PReLU, ReLU
from sklearn.metrics import r2_score

def cust_metric_1(y_true, y_pred):
    dist = y_pred - y_true
    return K.abs(K.mean(dist))

def coeff_determination(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred ))
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) )
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

def get_network_1(initial_filters = 128, depth = 8, activation_func = 'tanh', input_shape=(98,), dropout=True, lr=1e-4):
    #tf.keras.backend.set_floatx('float64')
    model = Sequential()
    model.add(Dense(initial_filters, activation=activation_func, input_shape=input_shape))
    model.add(BatchNormalization())
    if dropout:
        model.add(Dropout(0.3))
    i = 0
    while i < depth // 2:
        model.add(Dense(initial_filters, activation=activation_func))
        model.add(BatchNormalization())
        if dropout:
            model.add(Dropout(0.3))
        initial_filters *= 2
        i += 1
    initial_filters //= 2
    i = 0
    while i < depth // 2:
        model.add(Dense(initial_filters, activation=activation_func))
        model.add(BatchNormalization())
        if dropout and i != depth // 2 - 1:
            model.add(Dropout(0.3))
        initial_filters //= 2
        i += 1
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss=tf.keras.losses.logcosh, metrics=['mse'], optimizer=tf.optimizers.Adam(lr=lr))

    return model

def get_network_2(max_filters = 2048, depth = 8, activation_func = 'tanh', input_shape=(98,), dropout=True, lr=1e-4):
    #tf.keras.backend.set_floatx('float64')

    if not max_filters // 2**(depth // 2 - 2) > 2:
        raise Exception("max filters must be higher for given depth")

    model = Sequential()
    i = 0
    while i < depth // 2:
        if i == 0:
            #model.add(Dense(max_filters, activation=activation_func, input_shape=input_shape))
            model.add(Dense(max_filters, input_shape=input_shape))
        else:
            #model.add(Dense(max_filters, activation=activation_func, input_shape=input_shape))
            model.add(Dense(max_filters, input_shape=input_shape))
        model.add(PReLU())
        model.add(BatchNormalization())
        if dropout:
            model.add(Dropout(0.3))
        max_filters //= 2
        i += 1
    max_filters *= 2
    i = 0
    while i < depth // 2:
        #model.add(Dense(max_filters, activation=activation_func))
        model.add(Dense(max_filters))
        model.add(PReLU())
        model.add(BatchNormalization())
        if dropout and i != depth // 2 - 1:
            model.add(Dropout(0.3))
        max_filters *= 2
        i += 1
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='mean_squared_logarithmic_error', metrics=['mse'], optimizer=tf.optimizers.Adam(lr=lr))

    return model

def get_network_3(max_filters = 2048, depth = 8, activation_func = 'relu', input_shape=(98,), dropout=True, batch_norm=True, dropout_value=0.3, lr=1e-4):
    #tf.keras.backend.set_floatx('float64')

    if not max_filters // 2**(depth - 2) > 2:
        raise Exception("max filters must be higher for given depth")

    model = Sequential()
    i = 0
    while i < depth:
        #Block layer 1
        if i == 0:
            #model.add(Dense(max_filters, activation=activation_func, input_shape=input_shape))
            model.add(Dense(max_filters, input_shape=input_shape))
        else:
            #model.add(Dense(max_filters, activation=activation_func, input_shape=input_shape))
            model.add(Dense(max_filters, input_shape=input_shape))
        model.add(PReLU())
        #model.add(ReLU(threshold=0.5))
        #model.add(ReLU())
        if batch_norm:
            model.add(BatchNormalization())
        if dropout and i != depth - 1:
            model.add(Dropout(dropout_value))

        #Block layer 2
        model.add(Dense(max_filters, input_shape=input_shape))
        model.add(PReLU())
        #model.add(ReLU(threshold=0.2))
        #model.add(ReLU())
        if batch_norm:
            model.add(BatchNormalization())
        if dropout and i != depth - 1:
            model.add(Dropout(dropout_value))
        max_filters //= 2
        i += 1

    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='mean_squared_logarithmic_error', metrics=['mse'], optimizer=tf.optimizers.Adam(lr=lr))

    return model
