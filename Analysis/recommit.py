import time
import math
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
# print(df["stimuli_letter"])


n1 = df[:][:152]
# n2 = df[:][153:299]

# N1
positives = n1[n1['target'] == 'Y']
positives = n1[n1['correct_key'] == n1['Key_one.keys']]
baseline = n1[n1['correct_key'].isnull()]
baseline = baseline[baseline['Key_one.keys'].isnull()]

eeg_times = positives["eegtime"].tolist()
eeg_base = baseline["eegtime"].tolist()
# print(eeg_times.tolist())


# target = df.loc[276]['eegtime']
targets = []
bases = []
sampling_rate = 250 # Hertz
x = data[0] # timestamps
y = data[7] # third channel

DataFilter.perform_lowpass(y, sampling_rate, 40.0, 4, FilterTypes.BUTTERWORTH, 0)
DataFilter.perform_highpass(y, sampling_rate, 0.1, 4, FilterTypes.BUTTERWORTH, 0)
# DataFilter.remove_environmental_noise(y, sampling_rate, NoiseTypes.SIXTY.value)
# DataFilter.perform_rolling_filter(y, 3, AggOperations.MEAN.value)
# DataFilter.perform_rolling_filter(y, 3, AggOperations.MEDIAN.value)
# DataFilter.perform_wavelet_denoising(y, WaveletTypes.BIOR3_9, 3,
#                                         WaveletDenoisingTypes.SURESHRINK, ThresholdTypes.HARD,
#                                         WaveletExtensionTypes.SYMMETRIC, NoiseEstimationLevelTypes.FIRST_LEVEL)

for i in eeg_times:
    print(f'{i} + {np.where(x == i)}')
    tg = np.where(x== i)
    if tg[0].size != 0:
        targets.append(tg[0][0])

for i in eeg_base:
    # print(f'{i} + {np.where(x == i)}')
    tg = np.where(x== i)
    if tg[0].size != 0 and not math.isnan(i):
        bases.append(tg[0][0])
        # print(f'{i} + {np.where(x == i)}')

# # # Seperate the time data from EEG channels
# x = data[0] # Timestamp?
# y = data[3] # No clue

# ts = np.where(x == target)[0][0]
# print(ts)

fig = plt.figure()
ax = fig.subplots(1)

pos_avg = np.zeros(250)
bas_avg = np.zeros(250)

x_epoch = np.linspace(-0.1, 0.9, 250)


valid_target = 0
for i in targets:
    y_epoch = y[i-25:i+225] # write that down
    if max(y_epoch) < 150 and min(y_epoch) > -150:
    # ax.plot(x_epoch, y_epoch, color = 'r')
        pos_avg += y_epoch
        valid_target += 1


valid_bases = 0
for i in bases:
    y_epoch = y[i-25:i+225] # write that down
    if max(y_epoch) < 150 and min(y_epoch) > -150:
    # ax.plot(x_epoch, y_epoch, color = 'r')
        bas_avg += y_epoch
        valid_bases += 1
        # ax.plot(x_epoch, y_epoch, color = 'g')


pos_avg = pos_avg/valid_target
bas_avg = bas_avg/valid_bases

erp = -1*(pos_avg - bas_avg)
# print(type(y_epoch))
# # DataFilter.perform_bandpass(y_epoch, 250, 2, 100.0, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# # print(y_epoch)

ax.plot(x_epoch, erp, color = 'g')
ax.vlines(x = x_epoch[25], ymin=min(erp), ymax=max(erp), color = 'b')
plt.xticks(np.arange(-0.1, 0.9, step=0.1))
plt.minorticks_on()
plt.show()