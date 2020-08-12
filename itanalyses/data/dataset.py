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
    def __init__(self, **kwargs):
        self.file_paths = list()
        if 'folder' in kwargs:
            self.file_paths += self.get_files(kwargs.get('folder'))
        if 'csv_files' in kwargs:
            self.file_paths += kwargs.get('csv_files')
        self.file_paths = list(set(self.file_paths))
        self.file_paths.sort()
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

        self.set_values()

    def new_par_group(self, parameters=None, labels=None):
        self.par_group = ParameterGroup(parameters=parameters, labels=labels)

    def time_zero(self, from_zero=False):
        self.time = Time(data_frames=[df['Time (s)'] for df in self.data], from_zero=from_zero)

    def load_data(self):
        data = [pd.read_csv(path, header=0, index_col=0) for path in self.file_paths]
        return data

    def set_values(self):
        self.current.set_value(voltage=self.voltage)
        self.voltage.set_value(current=self.current)
        self.power.set_value(current=self.current)
        self.fill_factor.set_value(voltage=self.voltage, current=self.current, power=self.power)
        self.time.set_value()
        self.temperature.set_value()
        self.irradiance1.set_value()
        self.irradiance2.set_value()
        self.irradiance2.set_value()
        self.irradiance3.set_value()

    def set_averages(self, **kwargs):
        include = kwargs.get('include', [True for _ in self.file_paths])
        self.current.set_avg_value(include=include)
        self.voltage.set_avg_value(include=include)
        self.power.set_avg_value(include=include)
        self.fill_factor.set_avg_value(include=include)
        self.time.set_avg_value(include=include)
        self.temperature.set_avg_value(include=include)
        self.irradiance1.set_avg_value(include=include)
        self.irradiance2.set_avg_value(include=include)
        self.irradiance2.set_avg_value(include=include)
        self.irradiance3.set_avg_value(include=include)

    @staticmethod
    def get_files(folder):
        files = [os.path.join(folder, f) for f in os.listdir(folder) if
                 f.endswith('.csv') and os.path.basename(f).startswith('IV_Curve_')]
        return files
