import numpy as np
import os
from network import get_network
import matplotlib.pyplot as plt
import sklearn
from keras.models import Sequential
from generator import DataGenerator

if __name__ == '__main__':
    processed_dir = '../../data_processing/processed'

    X = np.load(os.path.join(processed_dir, 'data_arr_X.npy'))
    Y = np.load(os.path.join(processed_dir, 'data_arr_Y.npy')) * 100

    split_index = int(X.shape[0] * 0.9)

    X_train = X[0: split_index]
    Y_train = Y[0: split_index]
    X_test = X[split_index:]
    Y_test = Y[split_index:]

    # Parameters
    params = {'dim': (X.shape[1],),
              'batch_size': 64,
              'n_channels': 1,
              'shuffle': True}

    # Generators
    training_generator = DataGenerator(X_train, Y_train, **params)
    validation_generator = DataGenerator(X_test, Y_test, **params)

    model = get_network(initial_filters=32, depth=6, input_shape=(X.shape[1],))
    model.summary()

    X_train, Y_train = sklearn.utils.shuffle(X_train, Y_train)

    #history = model.fit(X_train, Y_train, batch_size=32, epochs=5000, validation_split=0.1)

    # Train model on dataset
    history = model.fit_generator(generator=training_generator,
                        validation_data=validation_generator,
                        epochs=10)

    plt.plot(history.history['loss'])
    #plt.plot(history.history['val_loss'])
    plt.show()

    pred = model.predict(X_test) / 100
    print(pred)
    dist = pred - Y_test
    print(dist)
