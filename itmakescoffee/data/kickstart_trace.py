import os
import time

import pandas as pd

from itmakescoffee.data.data import Data


class KickstartTrace(Data):
    def __init__(self, data_path='.', experiment=None, key=None):
        super().__init__(data_path=data_path, experiment=experiment, key=key)
        self.csv_import()

    def csv_import(self):
        self.data = pd.read_csv(self.data_path, sep=',', header=0, index_col=0, skiprows=33,
                                names=["Time (s)", "Voltage (V)", "Current (A)"])
        self.time = time.mktime(time.strptime(os.path.basename(self.data_path).split(' ')[-1], "%Y-%m-%dT%H.%M.%S.csv"))
        self.data.index.name = 'Index'
        self.data['Time (s)'] = self.data['Time (s)'] + self.time
        self.data['Current (A)'] = - self.data['Current (A)']
        self.data['Power (W)'] = self.data['Voltage (V)'] * self.data['Current (A)']
        for item in ["Temperature (C)", "Irradiance 1 (W/m2)", "Irradiance 2 (W/m2)", "Irradiance 3 (W/m2)",
                     "Irradiance 4 (W/m2)"]:
            self.data[item] = -1
        self.values['Open Circuit Voltage V_oc (V)'] = [self.get_voc(), 0]
        self.values['Short Circuit Current I_sc (A)'] = [self.get_isc(), 0]
        self.values['Maximum Power P_max (W)'] = [self.get_pmax(), 0]
        self.values['Fill Factor'] = [self.get_fill_factor(), 0]
        self.values['Time (s)'] = [self.time, 0]