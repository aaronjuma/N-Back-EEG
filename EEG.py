import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, AggOperations, WaveletTypes, NoiseEstimationLevelTypes, WaveletExtensionTypes, ThresholdTypes, WaveletDenoisingTypes

class Graph:

    # Initializer
    def __init__(self):

        # Setting up the board
        # self.board_id = BoardIds.UNICORN_BOARD
        # self.board_id = BoardIds.GALEA_BOARD
        self.board_id = BoardIds.SYNTHETIC_BOARD
        self.board = BoardShim(self.board_id, BrainFlowInputParams())
        self.channels = self.board.get_eeg_channels(self.board_id)

        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id) # Hz

        # Start recording/collecting data
        self.board.prepare_session()
        self.board.start_stream ()

        # Populate the board, will crash if not
        start = self.board.get_current_board_data(200)

        self.timestamp_channel = self.board.get_timestamp_channel(self.board_id)
        self.initial_time = start[self.timestamp_channel,0] #Get the initial timestamp data

    def getTimestamp(self):
        data = self.board.get_current_board_data(1)
        return data[self.timestamp_channel,0] - self.initial_time

    def close(self):
        # Get EEG data from board
        data = self.board.get_board_data()

        # Get x and y data
        x = data[self.timestamp_channel] - self.initial_time
        new_data = np.array(x)
        y = data[self.channels[0] : self.channels[-1] + 1]
        new_data = np.vstack((x, y))

        np.savetxt("test.csv", np.transpose(new_data), delimiter=",")


# Running the program
if __name__ == '__main__':
    graph = Graph()
    time.sleep(5)
    print(graph.getTimestamp())
    time.sleep(3)
    print(graph.getTimestamp())
    graph.close()

