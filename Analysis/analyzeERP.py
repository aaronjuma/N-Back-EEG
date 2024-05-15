import time
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from brainflow.data_filter import DataFilter, AggOperations, WaveletTypes, NoiseEstimationLevelTypes, WaveletExtensionTypes, ThresholdTypes, WaveletDenoisingTypes
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, NoiseTypes, DetrendOperations
from eegnb.analysis.utils import load_data
from eegnb.datasets import fetch_dataset


# Read data from csv
# data = genfromtxt('test.csv', delimiter=',')
data = DataFilter.read_file('eegdata.csv')
df = pd.read_csv('psychoData.csv')

target = df.loc[276]['eegtime']
print(type(target))
# # Get amount of channels
# channels = len(data) - 1

# # Set up figure
fig = plt.figure()
ax = fig.subplots(1)

# # Seperate the time data from EEG channels
x = data[0]
y = data[3]

DataFilter.perform_bandpass(y, 250, 5.0, 60.0, 4, FilterTypes.BESSEL_ZERO_PHASE, 0)
DataFilter.perform_bandstop(y, 250, 58.0, 62.0, 3, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
DataFilter.perform_lowpass(y, 250, 60.0, 5, FilterTypes.CHEBYSHEV_TYPE_1_ZERO_PHASE, 1)
DataFilter.perform_highpass(y, 250, 5.0, 4, FilterTypes.BUTTERWORTH, 0)

ts = np.where(x == target)[0][0]
print(ts)

x_epoch = x[ts-25:ts+200] - x[ts]
y_epoch = y[ts-25:ts+200]

# DataFilter.perform_bandpass(y_epoch, 250, 2, 100.0, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# print(y_epoch)

ax.plot(x_epoch, y_epoch, color = 'g')
ax.vlines(x = x_epoch[25], ymin=min(y_epoch), ymax=max(y_epoch), color = 'b')
plt.show()