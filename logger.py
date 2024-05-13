import time

import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter


def main():
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()

    # use synthetic board for demo
    board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)

    # real g.tec board
    # board = BoardShim(BoardIds.UNICORN_BOARD.value, params)


    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')

    # Populate the board
    time.sleep(10)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()


    # Getting channels
    eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
    # eeg_channels = BoardShim.get_eeg_channels(BoardIds.UNICORN_BOARD.value)
    df = pd.DataFrame(np.transpose(data))

    # demo for data serialization using brainflow API, we recommend to use it instead pandas.to_csv()
    DataFilter.write_file(data, 'test.csv', 'w')  # use 'a' for append mode
    restored_data = DataFilter.read_file('test.csv')
    restored_df = pd.DataFrame(np.transpose(restored_data))
    print('Data From the File')
    print(restored_df.head(10))


if __name__ == "__main__":
    main()