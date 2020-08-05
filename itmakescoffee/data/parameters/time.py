import pandas as pd

from itmakescoffee.data.parameters.parameter import Parameter


class Time(Parameter):
    def __init__(self, data_frames=None, from_zero=False):
        super().__init__(data_frames=data_frames)

        self.label = {'raw': 'Time (s)',
                      'average': 'Time (s)',
                      'value': 'Time (s)',
                      'fitted': 'Time (s)'}

        self.from_zero = from_zero
        if from_zero:
            self._set_zero()

    def set_value(self, idx=None):
        if idx is None:
            idx = self.idx
        for i in range(self.n_frames):
            self.value[i] = [self.raw_data[i][idx[i]], 0]

    def set_fit(self, idx=None):
        if idx is None:
            idx = self.idx
        for i in range(self.n_frames):
            self.fit[i] = [self.raw_data[i][idx[i]], 0]

    def _set_zero(self):
        for i in range(self.n_frames):
            self.raw_data[i] = self.raw_data[i] - self.raw_data[i].iloc[0]
        self.avg_data = list() if self.n_frames == 0 else pd.concat(self.raw_data).groupby(level=0).mean()
