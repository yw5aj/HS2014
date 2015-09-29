import pickle
import numpy as np
import os
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # %% Load data
    for fname in os.listdir('.'):
        if fname.endswith('.pkl'):
            with open(fname, 'r') as f:
                globals()[fname[:-4]] = pickle.load(f)
    # %% Plot
    plt.plot(mcncNodeCoordinates.T[0][1:],
             mcncNodeDict['stressMinPrincipal'].T[3][1:])