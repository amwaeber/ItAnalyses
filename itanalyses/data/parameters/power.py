import numpy as np
from scipy import optimize

from itanalyses.data.parameters.parameter import Parameter


class Power(Parameter):
    def __init__(self, data_frames=None):
        super().__init__(data_frames=data_frames)

        self.label = {'raw': 'Power (W)',
                      'average': 'Power (W)',
                      'value': 'Maximum Power P_max (W)',
                      'fitted': 'Maximum Power P_max (W)'}

    def set_value(self, current=None):
        for i, ds in enumerate(self.raw_data):
            if any(current.raw_data[i] > 0):
                try:
                    self.value[i] = [ds.loc[current.raw_data[i] > 0].max(), 0]
                    self.idx[i] = ds.index[ds == self.value[i][0]][0]
                except IndexError:
                    self.value[i] = [0, 0]
            else:
                self.value[i] = [0, 0]

    def set_fit(self, n_points=10, voltage=None, current=None, i00=5e-5, vt0=7.5e-2, rsh0=150):
        for i, ds in enumerate(self.raw_data):
            self.idx_range[i] = [self.idx[i] - n_points, self.idx[i] + n_points]

            voltage_df = voltage.raw_data[i][self.idx_range[i][0]:self.idx_range[i][1]]
            current_df = current.raw_data[i][self.idx_range[i][0]:self.idx_range[i][1]]

            popt, pcov = optimize.curve_fit(self.shockley, voltage_df, current_df,
                                            p0=np.array([current.raw_data[i].iloc[0], i00, vt0, rsh0]))
            voltage_pmax = optimize.minimize_scalar(lambda v: - v * self.shockley(v, *popt)).x
            self.fit[i] = [voltage_pmax * self.shockley(voltage_pmax, *popt), 0]

    @staticmethod
    def shockley(v, iph, i0, vt, rsh):
        return iph - i0 * np.exp(v / vt) - v / rsh
