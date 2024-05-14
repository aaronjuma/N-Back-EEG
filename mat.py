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
        self.board_id = BoardIds.UNICORN_BOARD
        # self.board_id = BoardIds.SYNTHETIC_BOARD
        self.board = BoardShim(self.board_id, BrainFlowInputParams())
        self.channels = self.board.get_eeg_channels(self.board_id)

        # Sets up the figure
        self.fig = plt.figure()
        self.ax = self.fig.subplots(len(self.channels))

        # Setting up the window sizes
        self.window_size = 5 # Seconds
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id) # Hz
        self.bin_size = self.window_size*self.sampling_rate

        # Start recording/collecting data
        self.board.prepare_session()
        self.board.start_stream ()

        # Populate the board, will crash if not
        time.sleep(self.window_size)
        start = self.board.get_current_board_data(self.bin_size)
        self.initial_time = start[self.board.get_timestamp_channel(self.board_id),0] #Get the initial timestamp data


    # Update function
    def animate(self, i):

        # Get EEG data from board
        data = self.board.get_current_board_data(self.bin_size)

        # Get x and y data
        x = data[self.board.get_timestamp_channel(self.board_id)] - self.initial_time
        y = data[self.channels[0] : self.channels[-1] + 1]

        # Updates plot
        plt.cla()
        for i in self.channels:
            self.ax[i-1].clear()

            #Add Processing Code Here:
            DataFilter.detrend(y[i-1], DetrendOperations.CONSTANT.value)
            DataFilter.perform_bandpass(y[i-1], self.sampling_rate, 2.0, 60.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            # DataFilter.perform_bandstop(data[channel], self.sampling_rate, 48.0, 52.0, 2,
            #                             FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(y[i-1], self.sampling_rate, 58.0, 62.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_rolling_filter(y[i-1], 3, AggOperations.MEAN.value)
            DataFilter.perform_rolling_filter(y[i-1], 3, AggOperations.MEDIAN.value)
            DataFilter.perform_wavelet_denoising(y[i-1], WaveletTypes.BIOR3_9, 3,
                                        WaveletDenoisingTypes.SURESHRINK, ThresholdTypes.HARD,
                                        WaveletExtensionTypes.SYMMETRIC, NoiseEstimationLevelTypes.FIRST_LEVEL)
            
            # Plot the graph
            self.ax[i-1].plot(x, y[i-1], color = 'tab:red')

        # Add at the bottom
        self.ax[self.channels[-1]-1].set_xlabel('Time (s)')
        
        # Finishing touch ups on the graph
        plt.xticks(rotation=45, ha='right')
        # plt.title('EEG Real-Time Data')

    def close(self, event):
        # Get EEG data from board
        data = self.board.get_board_data()

        # Get x and y data
        x = data[self.board.get_timestamp_channel(self.board_id)] - self.initial_time
        new_data = np.array(x)
        y = data[self.channels[0] : self.channels[-1] + 1]
        new_data = np.vstack((x, y))
        # print(new_data)

        np.savetxt("test.csv", np.transpose(new_data), delimiter=",")
        self.board.release_session()


    # Plot it in real time
    def plot(self):

        # Plots the graph in real time
        self.fig.canvas.mpl_connect('close_event', self.close)
        ani = animation.FuncAnimation(self.fig, self.animate, interval=50, cache_frame_data=False)
        plt.show()


# Running the program
if __name__ == '__main__':
    graph = Graph()
    graph.plot()