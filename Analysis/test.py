import argparse
import time
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets


def main():
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()

    board = BoardShim(BoardIds.SYNTHETIC_BOARD, params)
    board.prepare_session()

    board.start_stream()

    channels = board.get_eeg_channels(BoardIds.SYNTHETIC_BOARD)
    timestamp_channel = board.get_timestamp_channel(BoardIds.SYNTHETIC_BOARD)
    marker_channel = board.get_marker_channel(BoardIds.SYNTHETIC_BOARD)

    start = board.get_current_board_data(200)
    initial_time = start[timestamp_channel,0] #Get the initial timestamp data


    for i in range(10):
        time.sleep(1)
        board.insert_marker(i + 1)

    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    # Get x and y data
    x = data[timestamp_channel] - initial_time
    new_data = np.array(x)
    y = data[channels[0] : channels[-1] + 1]
    new_data = np.vstack((x, y))
    new_data = np.vstack((new_data, data[marker_channel]))

    np.savetxt("test.csv", np.transpose(new_data), delimiter=",")
    print("HELLLOOOOOOOOO IT SAVESS")

if __name__ == "__main__":
    main()