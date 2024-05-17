import time
import math
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from brainflow.data_filter import DataFilter, AggOperations, WaveletTypes, NoiseEstimationLevelTypes, WaveletExtensionTypes, ThresholdTypes, WaveletDenoisingTypes
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, NoiseTypes, DetrendOperations, WindowOperations
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets

# Get raw data
data = DataFilter.read_file('Roy/eegdata.csv')
df = pd.read_csv('Roy/psychoData.csv')

# Parse n1 and n2 data
n1 = df[:][:152]
n2 = df[:][153:299]

# N1 Base Data
n1_hit_data = n1[n1['correct_key'] == n1['Key_one.keys']]
n1_baseline = n1[n1['correct_key'].isnull()]
n1_baseline = n1_baseline[n1_baseline['Key_one.keys'].isnull()]

# N2 Base Data
n2_hit_data = n2[n2['correct_key'] == n2['key_Two.keys']]
n2_baseline = n2[n2['correct_key'].isnull()]
n2_baseline = n2_baseline[n2_baseline['key_Two.keys'].isnull()]

# Get EEG timestamps
n1_eeg_markers_hit = n1_hit_data["eegtime"].tolist()
n1_eeg_markers_base = n1_baseline["eegtime"].tolist()

n2_eeg_markers_hit = n2_hit_data["eegtime"].tolist()
n2_eeg_markers_base = n2_baseline["eegtime"].tolist()
# print(eeg_times.tolist())


# target = df.loc[276]['eegtime']
params = BrainFlowInputParams()
board_id = BoardIds.GALEA_BOARD
board = BoardShim(board_id, params)
channels = board.get_eeg_channels(board_id) #EEG Channels
timestamp_channel = board.get_timestamp_channel(board_id) # Timestamp channel
marker_channel = board.get_marker_channel(board_id) # Marker channel for synchronization
sampling_rate = BoardShim.get_sampling_rate(board_id) # Hz
print(channels)

# Filter raw EEG data
# sampling_rate = 250 # Hertz
x = data[marker_channel] # timestamps
y = data[channels[5]]*1e-3 # third channel 

DataFilter.detrend(y, DetrendOperations.CONSTANT.value)
DataFilter.perform_lowpass(y, sampling_rate, 40, 3, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
DataFilter.perform_highpass(y, sampling_rate, 0.5, 3, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# DataFilter.perform_bandstop(y, sampling_rate, 49.0, 51.0, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# DataFilter.perform_bandstop(y, sampling_rate, 59.0, 61.0, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# DataFilter.perform_bandstop(y, sampling_rate, 24.0, 28.0, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# DataFilter.perform_bandstop(y, sampling_rate, 10, 15, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# DataFilter.perform_bandstop(y, sampling_rate, 37.0, 41.0, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# DataFilter.remove_environmental_noise(y, sampling_rate, NoiseTypes.FIFTY.value)
# DataFilter.remove_environmental_noise(y, sampling_rate, NoiseTypes.SIXTY.value)
# DataFilter.perform_rolling_filter(y, 3, AggOperations.MEAN.value)
# DataFilter.perform_rolling_filter(y, 3, AggOperations.MEDIAN.value)
# DataFilter.perform_wavelet_denoising(y, WaveletTypes.BIOR3_9, 3,
#                                         WaveletDenoisingTypes.SURESHRINK, ThresholdTypes.HARD,
#                                         WaveletExtensionTypes.SYMMETRIC, NoiseEstimationLevelTypes.FIRST_LEVEL)


# Filtering hits and baseline data
n1_hits = []
n1_bases = []

n2_hits = []
n2_bases = []

# print(n1_eeg_markers_hit)
for i in n1_eeg_markers_hit:
    print(f'{i} + {np.where(x == i)}')
    tg = np.where(x== i)
    if tg[0].size != 0:
        n1_hits.append(tg[0][0])

for i in n1_eeg_markers_base:
    # print(f'{i} + {np.where(x == i)}')
    tg = np.where(x== i)
    if tg[0].size != 0 and not math.isnan(i):
        n1_bases.append(tg[0][0])
        # print(f'{i} + {np.where(x == i)}')

for i in n2_eeg_markers_hit:
    # print(f'{i} + {np.where(x == i)}')
    tg = np.where(x== i)
    if tg[0].size != 0:
        n2_hits.append(tg[0][0])

for i in n2_eeg_markers_base:
    # print(f'{i} + {np.where(x == i)}')
    tg = np.where(x== i)
    if tg[0].size != 0 and not math.isnan(i):
        n2_bases.append(tg[0][0])
        # print(f'{i} + {np.where(x == i)}')


# # # Seperate the time data from EEG channels
# x = data[0] # Timestamp?
# y = data[3] # No clue

# ts = np.where(x == target)[0][0]
# print(ts)

fig = plt.figure()
ax = fig.subplots(2)

n1_hit_avg = np.zeros(250)
n1_base_avg = np.zeros(250)
n2_hit_avg = np.zeros(250)
n2_base_avg = np.zeros(250)

x_epoch = np.linspace(-0.1, 0.9, 250)


n1_valid_hits = 0
for i in n1_hits:
    y_epoch = y[i-25:i+225] # write that down
    # ax.plot(x_epoch, y_epoch, color = 'g')
    # if max(y_epoch) < 100 and min(y_epoch) > -100:
    # ax.plot(x_epoch, y_epoch, color = 'r')
    n1_hit_avg += y_epoch
    n1_valid_hits += 1


n1_valid_bases = 0
for i in n1_bases:
    y_epoch = y[i-25:i+225] # write that down
    # if max(y_epoch) < 100 and min(y_epoch) > -100:
    # ax.plot(x_epoch, y_epoch, color = 'r')
    n1_base_avg += y_epoch
    n1_valid_bases += 1
        # ax.plot(x_epoch, y_epoch, color = 'g')

n2_valid_hits = 0
for i in n2_hits:
    y_epoch = y[i-25:i+225] # write that down
    # if max(y_epoch) < 100 and min(y_epoch) > -100:
    # ax.plot(x_epoch, y_epoch, color = 'r')
    n2_hit_avg += y_epoch
    n2_valid_hits += 1


n2_valid_bases = 0
for i in n2_bases:
    y_epoch = y[i-25:i+225] # write that down
    # if max(y_epoch) < 100 and min(y_epoch) > -100:
    # ax.plot(x_epoch, y_epoch, color = 'r')
    n2_base_avg += y_epoch
    n2_valid_bases += 1
        # ax.plot(x_epoch, y_epoch, color = 'g')


n1_hit_avg = n1_hit_avg/n1_valid_hits
n1_base_avg = n1_base_avg/n1_valid_bases
n2_hit_avg = n2_hit_avg/n2_valid_hits
n2_base_avg = n2_base_avg/n2_valid_bases


n1_erp = -1*(n1_hit_avg - n1_base_avg)
n2_erp = -1*(n2_hit_avg - n2_base_avg)
# print(type(y_epoch))
# # DataFilter.perform_bandpass(y_epoch, 250, 2, 100.0, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
# # print(y_epoch)

nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
psd = DataFilter.get_psd_welch(y, nfft, nfft // 2, sampling_rate, WindowOperations.BLACKMAN_HARRIS.value)
print(psd)


ax[0].set_title("n-Back ERP in Fz using GALEA")
ax[0].plot(x_epoch, n1_erp, color = '#E69F00', label = 'n1')
ax[0].plot(x_epoch, n2_erp, color = '#009E73', label = 'n2')
ax[0].vlines(x = x_epoch[25], ymin = -200, ymax = 200, color = 'b', linestyles ="dashed", label = 'Stimulus')
ax[0].set_xlabel("Time (seconds)")
ax[0].set_ylabel("Amplitudes (mV)")
ax[0].legend(loc="lower right")



ax[1].set_title("Frequency Plot of Fz in GALEA")
ax[1].plot(psd[1], psd[0])
ax[1].set_xlim([0, 40])
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_ylabel("FFT Amplitude")
# ax.vlines(x = x_epoch[25], ymin = -15, ymax = 15, color = 'b')
# ax.plot(np.linspace(0, 10, 250*10), y[0:2500], color = 'g')
# plt.xticks(np.arange(-0.1, 0.9, step=0.1))
plt.tight_layout()
plt.show()