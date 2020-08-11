import datetime
import pandas as pd


info_pars = {'folder': ['.'], 'experiment_name': ['N/A'], 'experiment_date': [datetime.date(1970, 1, 1)],
             'film_id': ['unknown'], 'film_date': [datetime.date(1970, 1, 1)], 'film_thickness': [-1],
             'film_area': [-1], 'film_matrix': ['unknown'], 'film_qds': ['unknown'], 'film_qd_concentration': [-1],
             'film_qd_emission': [-1], 'film_solvent': ['unknown'], 'pv_cell_id': ['unknown'],
             'pv_cell_type': ['unknown'], 'pv_cell_area': [-1], 'setup_location': ['unknown'],
             'setup_calibrated': [datetime.date(1970, 1, 1)], 'setup_suns': [-1], 'setup_pid_setpoint': [-1],
             'room_temperature': [-1], 'room_humidity': [-1]}


class Info:
    def __init__(self, setting_files=None):
        self.files = list() if setting_files is None else setting_files
        self.info = pd.DataFrame(columns=list(info_pars.keys()))

        self.load_data()

    def load_data(self):
        for file in self.files:
            df = pd.read_csv(file)
            idx = len(self.info.index)
            for i, values in enumerate(df.values.tolist()):
                self.info.loc[idx + i] = values[1:]

    def save_data(self, file_path='.'):
        self.info.to_csv(file_path)
