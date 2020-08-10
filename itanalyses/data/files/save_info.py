import datetime
import pandas as pd


def save_info(file_path='.',
              experiment_name='N/A',
              experiment_date=datetime.date(1970, 1, 1),
              film_id='unknown',
              film_date=datetime.date(1970, 1, 1),
              film_thickness=-1,
              film_area=-1,
              film_matrix='unknown',
              film_qds='unknown',
              film_qd_concentration=-1,
              film_qd_emission=-1,
              film_solvent='unknown',
              pv_cell_id='unknown',
              pv_cell_type='unknown',
              pv_cell_area=-1,
              setup_location='unknown',
              setup_calibrated=datetime.date(1970, 1, 1),
              setup_suns=-1,
              setup_pid_setpoint=-1,
              room_temperature=-1,
              room_humidity=-1):

    df = pd.DataFrame({
        'experiment_name': experiment_name,
        'experiment_date': experiment_date,
        'film_id': film_id,
        'film_date': film_date,
        'film_thickness': film_thickness,
        'film_area': film_area,
        'film_matrix': film_matrix,
        'film_qds': film_qds,
        'film_qd_concentration': film_qd_concentration,
        'film_qd_emission': film_qd_emission,
        'film_solvent': film_solvent,
        'pv_cell_id': pv_cell_id,
        'pv_cell_type': pv_cell_type,
        'pv_cell_area': pv_cell_area,
        'setup_location': setup_location,
        'setup_calibrated': setup_calibrated,
        'setup_suns': setup_suns,
        'setup_pid_setpoint': setup_pid_setpoint,
        'room_temperature': room_temperature,
        'room_humidity': room_humidity},
        index=[0])

    df.to_csv(file_path)
