import datetime
import os

from itmakescoffee.data.data_bundle import DataBundle
from itmakescoffee.data.kickstart_trace import KickstartTrace
from itmakescoffee.data.trace import Trace
from itmakescoffee.utility.version import __version__


class Group(DataBundle):
    def __init__(self, file_path='.', trace_paths=None):
        super().__init__(file_path=file_path)

        self.folder_path = os.path.dirname(self.file_path)
        self.name = os.path.splitext(os.path.basename(self.file_path))[0]

        self.import_from_pickle(trace_paths)
        self.update_plot_categories()

    def import_from_pickle(self, trace_paths):
        if os.path.exists(self.file_path):
            try:
                self.version, self.time, self.film_thickness, self.film_area, self.n_traces, self.traces, \
                    self.values, self.average_data, self.reference_path, self.efficiencies = self.load_pickle()
            except (ValueError, ModuleNotFoundError):  # mismatch in version or traces, or more parameters added since previous version
                self.failed_import()
        else:
            self.import_from_files(trace_paths)

    def failed_import(self):
        print('Could not import %s.' % self.file_path)

    def import_from_files(self, trace_paths=None, *args, **kwargs):
        self.version = __version__
        self.n_traces = [len(trace_paths)]  # 1st par: new format, 2nd par: kickstart format
        self.traces = {}
        for itrace, trace_path in enumerate(trace_paths):
            key = 'IV_Curve_%s' % str(itrace)
            if os.path.basename(trace_path).startswith('IV_Curve_'):
                self.traces[key] = Trace(trace_path, self.name, key)
            else:
                self.traces[key] = KickstartTrace(trace_path, self.name, key)
            if itrace == 0:
                self.time = self.traces[key].time
                self.film_thickness = self.traces[key].film_thickness
                self.film_area = self.traces[key].film_area
            else:
                self.time = min([self.time, self.traces[key].time])
                self.film_thickness = -1 if self.film_thickness != self.traces[key].film_thickness \
                    else self.film_thickness
                self.film_area = -1 if self.film_area != self.traces[key].film_area else self.film_area
        self.time = datetime.datetime.fromtimestamp(self.time).strftime("%Y-%m-%d %H:%M:%S")
        self.update_average()
        self.update_reference(None)  # set reference and efficiencies to default
