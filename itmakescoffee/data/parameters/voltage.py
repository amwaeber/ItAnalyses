import numpy as np
from scipy import optimize

from itmakescoffee.data.parameters.parameter import Parameter


class Voltage(Parameter):
    def __init__(self, data_frames=None):
        super().__init__(data_frames=data_frames)

        self.label = {'raw': 'Voltage (V)',
                      'average': 'Voltage (V)',
                      'value': 'Open Circuit Voltage V_oc (V)',
                      'fitted': 'Open Circuit Voltage V_oc (V)'}

    def set_value(self, current=None):
        for i, ds in enumerate(self.raw_data):
            try:
                self.value[i] = [ds.loc[current.raw_data[i].abs().idxmin()], 0]
            except IndexError:
                self.value[i] = [0, 0]

    def set_fit(self, n_points=5, current=None, y00=1, a0=1, b0=1):
        for i, ds in enumerate(self.raw_data):
            voc_idx = ds.index[ds == self.value[i][0]]
            voltage_df = ds.iloc[voc_idx[0] - n_points:voc_idx[0] + n_points]
            current_df = current.raw_data[i].iloc[voc_idx[0] - n_points:voc_idx[0] + n_points]

            popt, pcov = optimize.curve_fit(self.parabola, current_df, voltage_df,
                                            p0=np.array([y00, a0, b0]))
            self.fit[i] = [popt[0], np.sqrt(np.diag(pcov))[0]]

    @staticmethod
    def parabola(x, y0, a, b):
        return y0 + a * x + b * x ** 2
