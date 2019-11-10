import numpy as np
import os
from network import *
import matplotlib.pyplot as plt
import sklearn
from keras.models import Sequential
from generator import DataGenerator
from sklearn.metrics import r2_score
import scipy as sp
from keras.utils import plot_model

if __name__ == '__main__':
    processed_dir = '../../data_processing/processed'

    if os.path.exists('model.png'):
        os.remove('model.png')

    X = np.load(os.path.join(processed_dir, 'data_arr_X.npy'))
    Y = np.load(os.path.join(processed_dir, 'data_arr_Y.npy'))\

    acc = []
    r = []
    p = []

    i = 0
    while i < 4:

        X, Y = sklearn.utils.shuffle(X, Y)

        split_index = int(X.shape[0] * 0.9)
        print(f'{split_index} samples in training')

        X_train = X[0: split_index]
        Y_train = Y[0: split_index]
        X_test = X[split_index:]
        Y_test = Y[split_index:]

        # Parameters
        params_train = {'dim': (X.shape[1],),
                  'batch_size': 8,
                  'n_channels': 1,
                  'shuffle': True,
                  'aug': True}

        params_val = {'dim': (X.shape[1],),
                  'batch_size': 1,
                  'n_channels': 1,
                  'shuffle': False,
                  'aug': False}

        # Generators
        training_generator = DataGenerator(X_train, Y_train, **params_train)
        validation_generator = DataGenerator(X_test, Y_test, **params_val)

        lr = 1e-4

        #model = get_network_1(initial_filters=32, depth=14, input_shape=(X.shape[1],), dropout=False, lr=lr)
        #model = get_network_2(max_filters=64, depth=8, input_shape=(X.shape[1],), dropout=True, lr=lr)
        model = get_network_3(max_filters=8, depth=3, input_shape=(X.shape[1],), dropout=True, batch_norm=True, dropout_value=0.6, lr=lr)
        model.summary()

        if not os.path.exists('model.png'):
            plot_model(model, to_file='model.png', show_shapes=True)

        #history = model.fit(X_train, Y_train, batch_size=32, epochs=5000, validation_split=0.1)

        diff = []

        if os.path.exists('weights.h5'):
            model.load_weights('weights.h5')
        else:
            # Train model on dataset
            history = model.fit_generator(generator=training_generator,
                                validation_data=validation_generator,
                                validation_steps=1,
                                epochs=120,
                                steps_per_epoch=200)

            #model.save_weights('weights.h5')

            plt.plot(history.history['mse'])
            plt.plot(history.history['val_mse'])
            plt.yscale('log')
            plt.show()

        res = model.evaluate_generator(validation_generator, steps=Y_test.shape[0])
        print(res)

        mse = res[1]

        pred = model.predict_generator(validation_generator, steps=Y_test.shape[0])
        b = np.ones(Y_test.shape[0]) * np.mean(pred)
        c = np.mean(np.absolute(pred - b))
        print(pred)
        print(f'Diff: {c}')
        print(f'min: {np.min(pred)}')
        print(f'max: {np.max(pred)}')
        dist = np.absolute(pred - Y_test)
        #dist = (Y_test - pred) / (Y_test + 1e-8)
        #print(f'dist: {dist}')
        print(f'mean dist: {np.mean(dist)}')
        print(f'mean std: {np.std(dist)}')
        #print(Y_test)
        print(f'min: {np.min(Y_test)}')
        print(f'max: {np.max(Y_test)}')

        #print(abs(np.mean(dist)))
        #print(np.mean(pred))
        #print(np.mean(Y_test))
        #print((np.mean(pred) - np.mean(Y_test)) / np.mean(Y_test))
        print(r2_score(Y_test, pred))

        ttest = sp.stats.ttest_ind(pred, Y_test)

        acc.append(mse)
        r.append(r2_score(Y_test, pred))
        p.append(ttest[1])

        print(f't-test: {ttest[1]}')

        i += 1
    print("\n\nFINAL RES")
    print(f'mse: {np.mean(acc)}')
    print(f'R^2: {np.mean(r)}')
    print(f'p: {np.mean(p)}')
