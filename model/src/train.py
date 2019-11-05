import numpy as np
import os

if __name__ == '__main__':
    processed_dir = '../../data_processing/processed'

    a = np.load(os.path.join(processed_dir, 'data_arr.npy'))

    for l in a:
        print(l)
