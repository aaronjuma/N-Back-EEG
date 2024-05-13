import argparse
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets


def main():
    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.UNICORN_BOARD, params)

    board.prepare_session()
    board.start_stream ()
    time.sleep(10)
    data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    # data = board.get_board_data()  # get all data and remove it from internal buffer
    board.stop_stream()
    board.release_session()
    # print(data)
    # x = pd.read_csv('data.csv')
    fig, ax = plt.subplots()
    # print(x['EEG 1'].to_numpy())
    # ax.plot(x['EEG 1'].to_numpy())
    ax.plot(data[0])
    plt.show()


if __name__ == "__main__":
    main()