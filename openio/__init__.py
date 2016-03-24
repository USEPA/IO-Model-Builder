import os.path as path
import pandas as pd
import numpy as np


class File(object):
    def __init__(self, io_module, name, description=''):
        self.io_module = io_module
        self.name = name
        self.description = description

    @property
    def path(self):
        return self.io_module + '/' + self.name


USE_TABLE = File('economic', 'use_table.csv',
                 'Use table of the economic module')
MAKE_TABLE = File('economic', 'make_table.csv',
                  'Make table of the economic module')


class Model(object):
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir

    def has_file(self, io_file):
        if type(io_file) is not File:
            raise TypeError('Unknown type: use file constants of the module')
        return path.isfile(self.data_dir + '/' + io_file.path)

    def load_data_frame(self, io_file):
        # TODO: check io_file path
        df = pd.read_csv(self.data_dir + '/' + io_file.path, index_col=0,
                         header=0)
        df.fillna(0.0, inplace=True)
        return df
