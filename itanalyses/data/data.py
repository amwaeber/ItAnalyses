import os

import numpy as np
import pandas as pd


average_keys = ['Time (s)', 'Open Circuit Voltage V_oc (V)', 'Short Circuit Current I_sc (A)',
                'Maximum Power P_max (W)', 'Fill Factor', 'Average Temperature T_avg (C)',
                'Average Irradiance I_1_avg (W/m2)', 'Average Irradiance I_2_avg (W/m2)',
                'Average Irradiance I_3_avg (W/m2)', 'Average Irradiance I_4_avg (W/m2)']


class Data:
    def __init__(self, data_path='.', *args, **kwargs):
        self.data_path = os.path.normpath(data_path)
        self.name = kwargs.get('key', 'default')
        self.experiment = kwargs.get('experiment', 'none')
        self.is_included = True

        self.film_thickness = -1
        self.film_area = -1
        self.load_settings()
        self.data = pd.DataFrame(columns=['Index', 'Time (s)', 'Voltage (V)', 'Current (A)', 'Power (W)',
                                          'Temperature (C)', 'Irradiance 1 (W/m2)', 'Irradiance 2 (W/m2)',
                                          'Irradiance 3 (W/m2)', 'Irradiance 4 (W/m2)'])
        self.time = 0
        self.values = {key: [0, 0] for key in average_keys}

    def load_settings(self):
        try:
            with open(os.path.join(os.path.dirname(self.data_path), 'Settings.txt')) as f:
                file_contents = f.readlines()
                if file_contents[2].startswith("Film"):
                    self.film_thickness = file_contents[3].strip('\n').split(' ')[-1]
                    self.film_area = file_contents[4].strip('\n').split(' ')[-1]
                else:
                    self.film_thickness = -1
                    self.film_area = -1
        except FileNotFoundError:
            self.film_thickness = -1
            self.film_area = -1

    def fill_missing_values(self, column=None):  # To fix temporarily the missing first sensor values issue
        self.data[column].replace([0, -1], np.nan, inplace=True)
        self.data[column].fillna(method='backfill', inplace=True)
        self.data[column].fillna(method='pad', inplace=True)
        self.data[column].fillna(value=0, inplace=True)

    def get_voc(self):
        try:
            voc = self.data.loc[self.data['Current (A)'].abs() == self.data['Current (A)'].abs().min(),
                                ['Voltage (V)']].values[0, 0]
        except IndexError:
            voc = 0
        return voc

    def get_isc(self):
        try:
            isc = self.data.loc[self.data['Voltage (V)'].abs() == self.data['Voltage (V)'].abs().min(),
                                ['Current (A)']].values[0, 0]
        except IndexError:
            isc = 0
        return isc

    def get_pmax(self):
        try:
            if any(self.data['Current (A)'] > 0):
                pmax = self.data.loc[self.data['Current (A)'] > 0]['Power (W)'].max()
            else:
                pmax = 0
        except IndexError:
            pmax = 0
        return pmax

    def get_fill_factor(self):
        vocisc = self.get_voc() * self.get_isc()
        if vocisc <= 0:
            return 0
        else:
            return abs(self.get_pmax() / vocisc)
