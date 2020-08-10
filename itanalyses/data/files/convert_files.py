import numpy as np
import os
import pandas as pd
import time


def convert_kickstart(file_path='.', save_file='.'):
    df = pd.read_csv(file_path, sep=',', header=0, index_col=0, skiprows=33,
                     names=["Time (s)", "Voltage (V)", "Current (A)"])
    exp_time = time.mktime(time.strptime(os.path.basename(file_path).split(' ')[-1], "%Y-%m-%dT%H.%M.%S.csv"))
    df.index.name = 'Index'
    df['Time (s)'] = df['Time (s)'] + exp_time
    df['Current (A)'] = - df['Current (A)']
    df['Power (W)'] = df['Voltage (V)'] * df['Current (A)']
    for item in ["Temperature (C)", "Irradiance 1 (W/m2)", "Irradiance 2 (W/m2)", "Irradiance 3 (W/m2)",
                 "Irradiance 4 (W/m2)"]:
        df[item] = 0

    df.to_csv(save_file)


def convert_imc(file_path='.', save_file='.'):
    df = pd.read_csv(file_path, header=None, index_col=0, skiprows=1,
                                names=["Index", "Time (s)", "Voltage (V)", "Current (A)", "Current Std (A)",
                                       "Resistance (Ohm)", "Power (W)", "Temperature (C)", "Irradiance 1 (W/m2)",
                                       "Irradiance 2 (W/m2)", "Irradiance 3 (W/m2)", "Irradiance 4 (W/m2)"],
                                usecols=[0, 1, 2, 3, 6, 7, 8, 9, 10, 11])
    for col in ["Temperature (C)", "Irradiance 1 (W/m2)", "Irradiance 2 (W/m2)", "Irradiance 3 (W/m2)",
                "Irradiance 4 (W/m2)"]:
        df[col].replace([0, -1], np.nan, inplace=True)
        df[col].fillna(method='backfill', inplace=True)
        df[col].fillna(method='pad', inplace=True)
        df[col].fillna(value=0, inplace=True)

    df.to_csv(save_file)
