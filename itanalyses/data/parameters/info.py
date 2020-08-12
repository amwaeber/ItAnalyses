import datetime
import os
import pandas as pd


info_pars = {'folder': ['.'], 'experiment_name': ['N/A'], 'experiment_date': [datetime.date(1970, 1, 1)],
             'film_id': ['unknown'], 'film_date': [datetime.date(1970, 1, 1)], 'film_thickness': [-1],
             'film_area': [-1], 'film_matrix': ['unknown'], 'film_qds': ['unknown'], 'film_qd_concentration': [-1],
             'film_qd_emission': [-1], 'film_solvent': ['unknown'], 'pv_cell_id': ['unknown'],
             'pv_cell_type': ['unknown'], 'pv_cell_area': [-1], 'setup_location': ['unknown'],
             'setup_calibrated': [datetime.date(1970, 1, 1)], 'setup_suns': [-1], 'setup_pid_setpoint': [-1],
             'room_temperature': [-1], 'room_humidity': [-1]}


class Info:
    def __init__(self, setting_files=None, index_file=None):

        self.info = pd.DataFrame(columns=list(info_pars.keys()))
        self.files = list()

        if setting_files:
            self.load_data(files=setting_files)
        elif index_file:
            self.load_data(index_file=index_file)

    def load_data(self, files=None, index_file=None):
        if index_file:
            self.info = pd.read_csv(index_file, index_col=0)
            self.files = [os.path.join(folder, 'IV_Curve_0.dat') for folder in self.info['folder'].values.tolist()]
        else:
            self.files += files
            for file in files:
                df = pd.read_csv(file)
                idx = len(self.info.index)
                for i, values in enumerate(df.values.tolist()):
                    self.info.loc[idx + i] = [os.path.dirname(file)] + values[2:]

    def drop_data(self, files=None):
        for file in files or []:
            self.files.remove(file)
            self.info.drop(self.info[self.info['folder'] == os.path.dirname(file)].index, inplace=True)
            self.info.reset_index(drop=True, inplace=True)

    def save_data(self, file_path='info.dat'):
        self.info.to_csv(file_path)
