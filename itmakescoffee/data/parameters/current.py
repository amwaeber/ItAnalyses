import numpy as np
from scipy import optimize

from itmakescoffee.data.parameters.parameter import Parameter


class Current(Parameter):
    def __init__(self, data_frames=None):
        super().__init__(data_frames=data_frames)

        self.label = {'raw': 'Current (A)',
                      'average': 'Current (A)',
                      'value': 'Short Circuit Current I_sc (A)',
                      'fitted': 'Short Circuit Current I_sc (A)'}

    def set_value(self, voltage=None):
        for i, ds in enumerate(self.raw_data):
            try:
                self.value[i] = [ds.loc[voltage.raw_data[i].abs().idxmin()], 0]
                self.idx[i] = ds.index[ds == self.value[i][0]][0]
            except IndexError:
                self.value[i] = [0, 0]

    def set_fit(self, n_points=3, voltage=None, m0=-1e-2):
        for i, ds in enumerate(self.raw_data):
            self.idx_range[i] = [0, self.idx[i] + n_points]

            current_df = ds[self.idx_range[i][0]:self.idx_range[i][1]]
            voltage_df = voltage.raw_data[i][self.idx_range[i][0]:self.idx_range[i][1]]

            popt, pcov = optimize.curve_fit(self.linear, voltage_df, current_df,
                                            p0=np.array([self.value[i][0], m0]))
            self.fit[i] = [popt[0], np.sqrt(np.diag(pcov))[0]]

    @staticmethod
    def linear(x, y0, m):
        return y0 + m * x

