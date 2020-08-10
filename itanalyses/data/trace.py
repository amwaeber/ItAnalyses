import pandas as pd

from itanalyses.data.data import Data, average_keys


class Trace(Data):
    def __init__(self, data_path='.', experiment=None, key=None):
        super().__init__(data_path=data_path, experiment=experiment, key=key)
        self.csv_import()

    def csv_import(self):
        self.data = pd.read_csv(self.data_path, header=None, index_col=0, skiprows=3,
                                names=["Index", "Time (s)", "Voltage (V)", "Current (A)", "Current Std (A)",
                                       "Resistance (Ohm)", "Power (W)", "Temperature (C)", "Irradiance 1 (W/m2)",
                                       "Irradiance 2 (W/m2)", "Irradiance 3 (W/m2)", "Irradiance 4 (W/m2)"],
                                usecols=[0, 1, 2, 3, 6, 7, 8, 9, 10, 11])
        for col in ["Temperature (C)", "Irradiance 1 (W/m2)", "Irradiance 2 (W/m2)", "Irradiance 3 (W/m2)",
                    "Irradiance 4 (W/m2)"]:
            self.fill_missing_values(col)
        self.time = self.data['Time (s)'].min()
        self.values = {'Open Circuit Voltage V_oc (V)': [self.get_voc(), 0],
                       'Short Circuit Current I_sc (A)': [self.get_isc(), 0],
                       'Maximum Power P_max (W)': [self.get_pmax(), 0],
                       'Fill Factor': [self.get_fill_factor(), 0],
                       'Time (s)': [self.time, 0]}
        for key, col in zip(average_keys[5:], self.data.columns.values[4:]):
            self.values[key] = [self.data[col].mean(), self.data[col].std()]
