import os

from data.data_bundle import DataBundle
from data.kickstart_trace import KickstartTrace
from data.trace import Trace
from utility import folders
from utility.version import __version__


class Experiment(DataBundle):
    def __init__(self, folder_path='.'):
        super().__init__(folder_path=folder_path)

        self.name = os.path.basename(self.folder_path)
        self.file_path = os.path.join(self.folder_path, 'experiment.pkl')

        self.import_from_pickle()
        self.update_plot_categories()

    def import_from_pickle(self):
        n_csv = folders.get_number_of_csv(self.folder_path)
        if os.path.exists(self.file_path):
            try:
                self.version, self.time, self.film_thickness, self.film_area, self.n_traces, self.traces, \
                    self.values, self.average_data, self.reference_path, self.efficiencies = self.load_pickle()
                if any([self.version != __version__, n_csv != self.n_traces]):
                    raise ValueError
            except (ValueError, ModuleNotFoundError):  # mismatch in version or traces, or more parameters added since previous version
                self.import_from_files()
        else:
            self.import_from_files()

    def import_from_files(self):
        self.load_settings()
        self.version = __version__

        self.n_traces = folders.get_number_of_csv(self.folder_path)  # 1st par: new format, 2nd par: kickstart format
        self.traces = {}
        for trace in range(self.n_traces[0]):
            key = 'IV_Curve_%s' % str(trace)
            self.traces[key] = Trace(os.path.join(self.folder_path, key + '.csv'), self.name, key)
        if self.n_traces[1] > 0:  # Import Kickstart files if there are any
            kickstart_files = folders.get_kickstart_paths(self.folder_path)
            for itrace, trace in enumerate(range(self.n_traces[0], self.n_traces[0] + self.n_traces[1])):
                key = 'IV_Curve_%s' % str(trace)
                self.traces[key] = KickstartTrace(os.path.join(self.folder_path, kickstart_files[itrace]),
                                                  self.name, key)
        self.update_average()
        self.update_reference(None)  # set reference and efficiencies to default

    def load_settings(self):
        try:
            with open(os.path.join(self.folder_path, 'Settings.txt')) as f:
                file_contents = f.readlines()
                self.time = file_contents[0].strip('\n')
                if file_contents[2].startswith("Film"):
                    self.film_thickness = file_contents[3].strip('\n').split(' ')[-1]
                    self.film_area = file_contents[4].strip('\n').split(' ')[-1]
                else:
                    self.film_thickness = -1
                    self.film_area = -1
        except FileNotFoundError:
            self.time = folders.get_datetime(self.folder_path)
            self.film_thickness = -1
            self.film_area = -1
