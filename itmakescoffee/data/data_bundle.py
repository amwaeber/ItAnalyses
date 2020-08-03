import numpy as np
import os
import pandas as pd
import pickle

from itmakescoffee.data.data import average_keys
from itmakescoffee.utility.version import __version__


efficiency_keys = ['Delta V_oc', 'Delta I_sc', 'Delta P_max', 'Delta Fill Factor', 'Delta T_avg', 'Delta I_1_avg',
                   'Delta I_2_avg', 'Delta I_3_avg', 'Delta I_4_avg']


class DataBundle:
    def __init__(self, *args, **kwargs):
        self.is_reference = False
        self.is_plotted = False

        self.file_path = os.path.normpath(kwargs.get('file_path', '../utility'))
        self.folder_path = os.path.normpath(kwargs.get('folder_path', '../utility'))
        self.name = 'default'

        self.version = __version__
        self.time = 0
        self.film_thickness = -1
        self.film_area = -1

        self.n_traces = 0
        self.traces = {}
        self.average_data = pd.DataFrame(columns=['Index', 'Time (s)', 'Voltage (V)', 'Current (A)', 'Power (W)',
                                                  'Temperature (C)', 'Irradiance 1 (W/m2)', 'Irradiance 2 (W/m2)',
                                                  'Irradiance 3 (W/m2)', 'Irradiance 4 (W/m2)'])
        self.values = {key: [0, 0] for key in average_keys}

        self.reference_path = ''
        self.efficiencies = {key: [0, 0] for key in efficiency_keys}

        self.plot_categories = {'Experiment': str(self.name),
                                'Film Thickness': str(self.film_thickness),
                                'Film Area': str(self.film_area),
                                'Time': str(self.time)
                                }

    def import_from_pickle(self, *args, **kwargs):
        pass

    def import_from_files(self, *args, **kwargs):
        pass

    def update_average(self):
        combined_data = pd.concat((trace.data for trace in self.traces.values() if trace.is_included))
        self.average_data = combined_data.groupby(combined_data.index).mean()
        self.values = {key: self.get_average(key) for key in average_keys}

    def get_average(self, key):
        trace_values = [trace.values[key][0] for trace in self.traces.values() if trace.is_included]
        if key == 'Time (s)':
            return [trace_values[0], 0]
        else:
            return [np.mean(trace_values), np.std(trace_values)]

    def update_reference(self, ref_experiment):
        if not ref_experiment:
            self.reference_path = ''
            self.efficiencies = {key: [0, 0] for key in efficiency_keys}
        else:
            self.reference_path = ref_experiment.folder_path
            self.efficiencies = {key: self.get_efficiency(ref_experiment, avg_key) for key, avg_key in
                                 zip(efficiency_keys, average_keys[1:])}

    def get_efficiency(self, ref_experiment, key):
        if ref_experiment.values[key][0] == 0:
            return [0, 0]
        else:
            return [100 * (self.values[key][0] - ref_experiment.values[key][0]) / ref_experiment.values[key][0],
                    100 * self.values[key][1] / ref_experiment.values[key][0]]

    def update_plot_categories(self):
        self.plot_categories = {'Experiment': str(self.name),
                                'Film Thickness': str(self.film_thickness),
                                'Film Area': str(self.film_area),
                                'Time': str(self.time)
                                }

    def save_pickle(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump([self.version, self.time, self.film_thickness, self.film_area, self.n_traces, self.traces,
                         self.values, self.average_data, self.reference_path, self.efficiencies], f, protocol=-1)

    def load_pickle(self):
        with open(self.file_path, 'rb') as f:
            return pickle.load(f)
