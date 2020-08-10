import pandas as pd


info_pars = ['experiment_name', 'experiment_date', 'film_id', 'film_date', 'film_thickness', 'film_area',
             'film_matrix', 'film_qds', 'film_qd_concentration', 'film_qd_emission', 'film_solvent', 'pv_cell_id',
             'pv_cell_type', 'pv_cell_area', 'setup_location', 'setup_calibrated', 'setup_suns', 'setup_pid_setpoint',
             'room_temperature', 'room_humidity']


class Info:
    def __init__(self, setting_files=None):
        self.files = list() if setting_files is None else setting_files
        self.info = pd.DataFrame(columns=info_pars)

        self.load_data()

    def load_data(self):
        for file in self.files:
            df = pd.read_csv(file)
            idx = len(self.info.index)
            for i, values in enumerate(df.values.tolist()):
                self.info.loc[idx + i] = values[1:]
