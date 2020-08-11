import os
import pandas as pd
import time

from itanalyses.data.parameters.info import Info
from itanalyses.data.parameters.current import Current
from itanalyses.data.parameters.voltage import Voltage
from itanalyses.data.parameters.power import Power
from itanalyses.data.parameters.fill_factor import FillFactor
from itanalyses.data.parameters.time import Time
from itanalyses.data.parameters.temperature import Temperature
from itanalyses.data.parameters.irradiance import Irradiance
from itanalyses.data.parameters.parameter_group import ParameterGroup


class DataSet:
    def __init__(self, name='Dataset', csv_files=None, *args, **kwargs):
        self.name = name

        self.file_paths = list() if csv_files is None else csv_files
        self.info = Info(setting_files=[file[:-4] + '.dat' for file in self.file_paths])
        self.data = self.load_data()

        # Initialise parameters
        self.current = Current(data_frames=[df['Current (A)'] for df in self.data])
        self.voltage = Voltage(data_frames=[df['Voltage (V)'] for df in self.data])
        self.power = Power(data_frames=[df['Power (W)'] for df in self.data])
        self.fill_factor = FillFactor(data_frames=None, n_frames=len(self.data))
        self.time = Time(data_frames=[df['Time (s)'] for df in self.data])
        self.temperature = Temperature(data_frames=[df['Temperature (C)'] for df in self.data])
        self.irradiance1 = Irradiance(data_frames=[df['Irradiance 1 (W/m2)'] for df in self.data])
        self.irradiance2 = Irradiance(data_frames=[df['Irradiance 2 (W/m2)'] for df in self.data])
        self.irradiance3 = Irradiance(data_frames=[df['Irradiance 3 (W/m2)'] for df in self.data])
        self.irradiance4 = Irradiance(data_frames=[df['Irradiance 4 (W/m2)'] for df in self.data])
        self.par_group = ParameterGroup()

    def new_par_group(self, parameters=None, labels=None):
        self.par_group = ParameterGroup(parameters=parameters, labels=labels)

    def time_zero(self, from_zero=False):
        self.time = Time(data_frames=[df['Time (s)'] for df in self.data], from_zero=from_zero)

    def load_data(self):
        data = list()
        for path in self.file_paths:
            if os.path.basename(path).startswith('IV_Curve_'):  # ItMakesCoffee data
                data.append(pd.read_csv(path, header=0, index_col=0))
            # else:
            #     data.append(self.load_kickstart_data(path))  # Kickstart data
        return data

    @staticmethod
    def load_kickstart_data(path):
        df = pd.read_csv(path, sep=',', header=0, index_col=0, skiprows=33,
                         names=["Time (s)", "Voltage (V)", "Current (A)"])
        exp_time = time.mktime(time.strptime(os.path.basename(path).split(' ')[-1], "%Y-%m-%dT%H.%M.%S.csv"))
        df.index.name = 'Index'
        df['Time (s)'] = df['Time (s)'] + exp_time
        df['Current (A)'] = - df['Current (A)']
        df['Power (W)'] = df['Voltage (V)'] * df['Current (A)']
        for item in ["Temperature (C)", "Irradiance 1 (W/m2)", "Irradiance 2 (W/m2)", "Irradiance 3 (W/m2)",
                     "Irradiance 4 (W/m2)"]:
            df[item] = 0
        return df
