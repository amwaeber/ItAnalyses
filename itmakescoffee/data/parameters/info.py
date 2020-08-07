import datetime
import pandas as pd


class Info:
    def __init__(self, setting_files=None):
        self.files = list() if setting_files is None else setting_files

        # Experiment
        self.experiment_name = ['N/A' for _ in setting_files]
        self.experiment_date = [datetime.date(1970, 1, 1) for _ in setting_files]

        # Film
        self.film_id = ['unknown' for _ in setting_files]
        self.film_date = [datetime.date(1970, 1, 1) for _ in setting_files]
        self.film_thickness = [-1 for _ in setting_files]
        self.film_area = [-1 for _ in setting_files]
        self.film_matrix = ['unknown' for _ in setting_files]
        self.film_qds = ['unknown' for _ in setting_files]
        self.film_qd_concentration = [-1 for _ in setting_files]
        self.film_qd_emission = [-1 for _ in setting_files]
        self.film_solvent = ['unknown' for _ in setting_files]

        # PV cell
        self.pv_cell_id = ['unknown' for _ in setting_files]
        self.pv_cell_type = ['unknown' for _ in setting_files]
        self.pv_cell_area = [-1 for _ in setting_files]

        # Setup
        self.setup_location = ['unknown' for _ in setting_files]
        self.setup_calibrated = [datetime.date(1970, 1, 1) for _ in setting_files]
        self.setup_suns = [-1 for _ in setting_files]
        self.setup_pid_setpoint = [-1 for _ in setting_files]
        self.room_temperature = [-1 for _ in setting_files]
        self.room_humidity = [-1 for _ in setting_files]

        self.load_data()

    def load_data(self):
        for i, file in enumerate(self.files):
            df = pd.read_csv(file, header=0, index_col=0)

            # Experiment
            self.experiment_name[i] = df['experiment_name'][0]
            self.experiment_date[i] = df['experiment_date'][0]

            # Film
            self.film_id[i] = df['film_id'][0]
            self.film_date[i] = df['film_date'][0]
            self.film_thickness[i] = df['film_thickness'][0]
            self.film_area[i] = df['film_area'][0]
            self.film_matrix[i] = df['film_matrix'][0]
            self.film_qds[i] = df['film_qds'][0]
            self.film_qd_concentration[i] = df['film_qd_concentration'][0]
            self.film_qd_emission[i] = df['film_qd_emission'][0]
            self.film_solvent[i] = df['film_solvent'][0]

            # PV cell
            self.pv_cell_id[i] = df['pv_cell_id'][0]
            self.pv_cell_type[i] = df['pv_cell_type'][0]
            self.pv_cell_area[i] = df['pv_cell_area'][0]

            # Setup
            self.setup_location[i] = df['setup_location'][0]
            self.setup_calibrated[i] = df['setup_calibrated'][0]
            self.setup_suns[i] = df['setup_suns'][0]
            self.setup_pid_setpoint[i] = df['setup_pid_setpoint'][0]
            self.room_temperature[i] = df['room_temperature'][0]
            self.room_humidity[i] = df['room_humidity'][0]
