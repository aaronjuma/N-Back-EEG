import time
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import atexit

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, AggOperations, WaveletTypes, NoiseEstimationLevelTypes, WaveletExtensionTypes, ThresholdTypes, WaveletDenoisingTypes

class EEGController:

    # Initializer
    def __init__(self):

        # Setting up the board
        params = BrainFlowInputParams()
        params.serial_number = 'UN-2022.04.20'
        self.board_id = BoardIds.UNICORN_BOARD
        # self.board_id = BoardIds.GALEA_BOARD
        # self.board_id = BoardIds.SYNTHETIC_BOARD
        self.board = BoardShim(self.board_id, params)

        # Getting specific board details
        self.channels = self.board.get_eeg_channels(self.board_id) #EEG Channels
        self.timestamp_channel = self.board.get_timestamp_channel(self.board_id) # Timestamp channel
        self.marker_channel = self.board.get_marker_channel(self.board_id) # Marker channel for synchronization
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id) # Hz

        # Start recording/collecting data
        self.board.prepare_session()
        self.board.start_stream ()

        # Populate the board, will crash if not
        time.sleep(0.2)
        start = self.board.get_current_board_data(200)

        # Get timestamp data
        self.initial_time = start[self.timestamp_channel,0] #Get the initial timestamp data

        # Reseting Marker
        self.marker_id = -1

        atexit.register(self.close)

    # Return timestamp data
    def setMarker(self):
        self.marker_id = self.marker_id + 1
        self.board.insert_marker(self.marker_id)
        return self.marker_id
    

    def close(self):
        # Get EEG data from board and stops EEG session
        data = self.board.get_board_data()
        self.board.stop_stream()
        self.board.release_session()

        # Get x and y data
        x = data[self.timestamp_channel] - self.initial_time
        new_data = np.array(x)
        y = data[self.channels[0] : self.channels[-1] + 1]
        new_data = np.vstack((x, y))
        new_data = np.vstack((new_data, data[self.marker_channel]))

        np.savetxt("test.csv", np.transpose(new_data), delimiter=",")
        print("HELLLOOOOOOOOO IT SAVESS")

# # Running the program
# if __name__ == '__main__':
#     eeg = EEG()
#     time.sleep(5)
#     times = []
#     times.append(eeg.getTimestamp())
#     time.sleep(3)
#     times.append(eeg.getTimestamp())
#     eeg.close()

#     # Read data from csv
#     data = genfromtxt('test.csv', delimiter=',')

#     # Turn columns to row (easier to manipulate)
#     data = np.transpose(data)

#     # Get amount of channels
#     channels = len(data) - 1

#     # Set up figure
#     fig = plt.figure()
#     ax = fig.subplots(channels+1)

#     # Seperate the time data from EEG channels
#     x = data[0]
#     y = data[1:channels+1]

#     ts = np.where(x == times[0])[0][0]
#     print(ts)

#     # Plot
#     # for i in range(channels):
#     #     ax[i].plot(x, y[i], color = 'tab:red')
#     #     ax[i].vlines(x = times, ymin = min(y[i]), ymax = max(y[i]), color = 'b')

#     ax[channels].plot(x[ts-25:ts+200], y[0,ts-25:ts+200], color = 'g')
#     ax[channels].vlines(x = x[ts], ymin=min(y[0,ts-25:ts+200]), ymax=max(y[0,ts-25:ts+200]), color = 'b')
#     plt.show()

