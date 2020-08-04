import numpy as np
import pandas as pd


class Parameter:
    def __init__(self, data_frames=None, *args, **kwargs):

        self.label = {'raw': 'Raw Data',
                      'average': 'Averaged Data',
                      'value': 'Discrete Value',
                      'fitted': 'Fitted Value'}

        self.n_frames = 0 if data_frames is None else len(data_frames)

        self.raw_data = list() if self.n_frames == 0 else data_frames
        self.value = [[0, 0]] * len(self.raw_data)
        self.fit = [[0, 0]] * len(self.raw_data)

        self.avg_data = list() if self.n_frames == 0 else pd.concat(self.raw_data).groupby(level=0).mean()
        self.avg_value = [0, 0]
        self.avg_fit = [0, 0]

        self.idx_range = [[self.raw_data[i].first_valid_index(), self.raw_data[i].last_valid_index()]
                          for i in range(self.n_frames)]
        self.idx = [i[0] for i in self.idx_range]

    def set_value(self, *args, **kwarg):
        self.value = [[0, 0]] * len(self.raw_data)

    def set_fit(self, *args, **kwarg):
        self.fit = [[0, 0]] * len(self.raw_data)

    def set_avg_value(self, include=None):
        if include is None:
            include = [False]
        if any(include):
            self.avg_value = [np.mean([val[0] for i, val in enumerate(self.value) if include[i]]),
                              np.std([val[0] for i, val in enumerate(self.value) if include[i]])]
        else:
            self.avg_value = [0, 0]

    def set_avg_fit(self, include=None):
        if include is None:
            include = [False]
        if any(include):
            self.avg_fit = [np.mean([val[0] for i, val in enumerate(self.fit) if include[i]]),
                            np.std([val[0] for i, val in enumerate(self.fit) if include[i]])]
        else:
            self.avg_fit = [0, 0]
