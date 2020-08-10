################
# Test DataSet and Parameter classes

from itanalyses.data.dataset import DataSet


ds = DataSet(csv_files=['C:\\Users\\User\\Documents\\temp\\29-07-2020\\0\\IV_Curve_0.csv',
                        'C:\\Users\\User\\Documents\\temp\\29-07-2020\\0\\IV_Curve_1.csv',
                        'C:\\Users\\User\\Documents\\temp\\PV\\IV_Curve_0.csv'])

ds.new_par_group(parameters=[ds.irradiance1, ds.irradiance2, ds.irradiance3, ds.irradiance4],
                 labels=['Irradiance (W/m2)', 'Average Irradiance I_avg (W/m2)'])

ds.current.set_value(voltage=ds.voltage)
ds.voltage.set_value(current=ds.current)
ds.power.set_value(current=ds.current)
ds.fill_factor.set_value(voltage=ds.voltage, current=ds.current, power=ds.power)

ds.current.set_avg_value(include=[True, True, True])
ds.voltage.set_avg_value(include=[True, True, True])
ds.power.set_avg_value(include=[True, True, True])
ds.fill_factor.set_avg_value(include=[True, True, True])

ds.current.set_fit(voltage=ds.voltage)
ds.voltage.set_fit(current=ds.current)
ds.power.set_fit(voltage=ds.voltage, current=ds.current)
ds.fill_factor.set_fit(voltage=ds.voltage, current=ds.current, power=ds.power)
ds.temperature.set_value(idx_range=ds.power.idx_range)
ds.irradiance2.set_value(idx_range=ds.power.idx_range)
ds.par_group.set_value(idx_range=ds.power.idx_range)

ds.current.set_avg_fit(include=[True, True, True])
ds.voltage.set_avg_fit(include=[True, True, True])
ds.power.set_avg_fit(include=[True, True, True])
ds.fill_factor.set_avg_fit(include=[True, True, True])

####################
# Convert old ItMakesCoffee Data and generate Info files

import datetime
import os

from itanalyses.data.files.convert_files import convert_imc
from itanalyses.data.files.save_info import save_info
from itanalyses.utility import folders

folder_path = 'C:\\Users\\User\\Documents\\temp\\29-07-2020\\0'
n_files = folders.get_number_of_csv(path=folder_path)[0]
for i in range(n_files):
    convert_imc(file_path=os.path.join(folder_path, 'IV_Curve_%d.csv' % i),
                save_file=os.path.join(folder_path, 'IV_CurveA_%d.csv' % i))
    save_info(file_path=os.path.join(folder_path, 'IV_CurveA_%d.dat' % i),
              experiment_name=os.path.basename(folder_path),
              experiment_date=datetime.datetime.fromtimestamp(os.path.getctime(
                  os.path.join(folder_path, 'IV_Curve_%d.csv' % i))).date(),
              pv_cell_id='unknown',
              pv_cell_type='mc-Si',
              setup_location='Vinery Way'
              )

####################
# Convert old Kickstart Data and generate Info files

import datetime
import os

from itanalyses.data.files.convert_files import convert_kickstart
from itanalyses.data.files.save_info import save_info
from itanalyses.utility import folders

folder_path = 'C:\\Users\\User\\Documents\\temp\\PV'
file_paths = folders.get_kickstart_paths(path=folder_path)
file_paths.sort()
for i, file in enumerate(file_paths):
    convert_kickstart(file_path=os.path.join(folder_path, file),
                      save_file=os.path.join(folder_path, 'IV_Curve_%d.csv' % i))
    save_info(file_path=os.path.join(folder_path, 'IV_Curve_%d.dat' % i),
              experiment_name=os.path.basename(folder_path),
              experiment_date=file.split(' ')[-1].split('T')[0],
              film_id='None',
              film_date=datetime.date(1970, 1, 1),
              film_thickness=0,
              film_area=0,
              film_matrix='n/a',
              film_qds='n/a',
              film_qd_concentration=0,
              film_qd_emission=0,
              film_solvent='n/a',
              pv_cell_id='unknown',
              pv_cell_type='mc-Si',
              setup_location='Vinery Way'
              )

####################
# Test DataIndex creation
from itanalyses.data.dataindex import DataIndex

folder = 'C:\\Users\\User\\Documents\\temp'
data_index = DataIndex(folder=folder)

####################
# Test data fits

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

from itanalyses.data.trace import Trace

mytrace = Trace(data_path='C:\\Users\\User\\Documents\\temp\\29-07-2020\\0\\IV_Curve_0.csv')

iv_raw = mytrace.data.loc[(mytrace.data['Voltage (V)'] > 0) & (mytrace.data['Current (A)'] > 0)]

# Getting p_max
# Select slice of data
n_data = 10
pmax_idx = iv_raw['Power (W)'].idxmax()
pmax_df = iv_raw.iloc[pmax_idx - n_data:pmax_idx + n_data]


def shockley(v, iph, i0, vt, rsh):
    return iph - i0 * np.exp(v / vt) - v / rsh


popt, _ = optimize.curve_fit(shockley, pmax_df['Voltage (V)'], pmax_df['Current (A)'],
                             p0=np.array([iv_raw['Current (A)'].iloc[0], 5e-5, 7.5e-2, 150]))

fig, ax = plt.subplots()
ax2 = ax.twinx()
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax.plot(pmax_df['Voltage (V)'], pmax_df['Current (A)'])
ax.plot(pmax_df['Voltage (V)'], shockley(pmax_df['Voltage (V)'], *popt), color='r', ls='--')
ax2.plot(pmax_df['Voltage (V)'], pmax_df['Current (A)'] - shockley(pmax_df['Voltage (V)'], *popt), color='r', ls=':')
fig.show()


# pmax fit
def shockley_power(v):
    return - v * shockley(v, *popt)


vpmax_sim1 = optimize.minimize_scalar(lambda v: - v * shockley(v, *popt)).x

vpmax_sim = optimize.minimize_scalar(shockley_power).x

pmax_raw = (iv_raw['Voltage (V)'] * iv_raw['Current (A)']).max()
pmax_pnt = (iv_raw['Voltage (V)'] * shockley(iv_raw['Voltage (V)'], *popt)).max()
pmax_sim = vpmax_sim * shockley(vpmax_sim, *popt)
pmax_sim1 = vpmax_sim1 * shockley(vpmax_sim1, *popt)

print('Pmax_Raw: %f' % pmax_raw)
print('Pmax_Pnt: %f' % pmax_pnt)
print('Pmax_Sim: %f' % pmax_sim)
print('Pmax_Sim1: %f' % pmax_sim1)


# Getting isc
# Select slice of data
n_data = 3
isc_idx = mytrace.data.index[mytrace.data['Voltage (V)'].idxmin()]
isc_df = mytrace.data.iloc[0:isc_idx + n_data]


def linear(x, y0, m):
    return y0 + m * x


popt, pcov = optimize.curve_fit(linear, isc_df['Voltage (V)'], isc_df['Current (A)'],
                                p0=np.array([pmax_df['Current (A)'].iloc[2], -1e-2]))

fig, ax = plt.subplots()
ax2 = ax.twinx()
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax.plot(isc_df['Voltage (V)'], isc_df['Current (A)'])
ax.plot(isc_df['Voltage (V)'], linear(isc_df['Voltage (V)'], *popt), color='r', ls='--')
ax2.plot(isc_df['Voltage (V)'], isc_df['Current (A)'] - linear(isc_df['Voltage (V)'], *popt), color='r', ls=':')
fig.show()

isc_sim = popt[0]
isc_sim_stdev = np.sqrt(np.diag(pcov))[0]

print('Isc_Raw: %f' % mytrace.values['Short Circuit Current I_sc (A)'][0])
print('Isc_Sim: %f pm %f' % (isc_sim, isc_sim_stdev))


# Getting voc
# Select slice of data
n_data = 5
voc_idx = mytrace.data.index[mytrace.data['Current (A)'].abs().idxmin()]
voc_df = mytrace.data.iloc[voc_idx - n_data:voc_idx + n_data]


def parabola(x, y0, a, b):
    return y0 + a * x + b * x**2


popt, pcov = optimize.curve_fit(parabola, voc_df['Current (A)'], voc_df['Voltage (V)'],
                                p0=np.array([1, 1, 1]))

fig, ax = plt.subplots()
ax2 = ax.twinx()
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax.plot(voc_df['Current (A)'], voc_df['Voltage (V)'])
ax.plot(voc_df['Current (A)'], parabola(voc_df['Current (A)'], *popt), color='r', ls='--')
ax2.plot(voc_df['Current (A)'], voc_df['Voltage (V)'] - parabola(voc_df['Current (A)'], *popt), color='r', ls=':')
fig.show()

voc_sim = popt[0]
voc_sim_stdev = np.sqrt(np.diag(pcov))[0]

print('Voc_Raw: %f' % mytrace.values['Open Circuit Voltage V_oc (V)'][0])
print('Voc_Sim: %f pm %f' % (voc_sim, voc_sim_stdev))


ff_sim = pmax_sim / (isc_sim * voc_sim)

print('FF_Raw: %f' % mytrace.values['Fill Factor'][0])
print('FF_Sim: %f' % ff_sim)
