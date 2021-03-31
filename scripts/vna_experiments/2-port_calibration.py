# =============================================================================
# 12-element calibration on 2 port DUT
# =============================================================================


import skrf as rf
from skrf.vi.vna import PNA
from skrf import Network
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import date

rf.stylely()
# %matplotlib inline
#sweep values


#%% build folder for cal data
today = date.today()
date_str = today.strftime("%Y-%m-%d")
cal_folder_name = 'Cal_TwelveTerm_'+date_str

root_folder = Path('/Users/Zaber/Documents/data/scikit_measurements/')
meas_folder = root_folder / cal_folder_name

meas_folder.mkdir(exist_ok = True)

#%%initialize VNA

f_start = 8E9
f_stop = 12E9
f_npoints = int(101)

vna = PNA(address ='TCPIP0::10.236.73.132::inst0::INSTR')
vna.reset()
vna.scpi.set_trigger_manual
# vna.scpi.set_delete_all()
# vna.scpi.set_display_on(wnum=1,state=True)
meas_channel = 2


#%% SHORT S11 measurement 

meas_name = 'SHORT_11'

vna.create_meas(meas_name,'S11', channel = meas_channel) 

vna.set_frequency_sweep(f_start, 
                        f_stop, 
                        f_npoints, 
                        f_unit = 'Hz',
                        channel = meas_channel, 
                        )
vna.sweep
measurement = vna.get_measurement(mname = meas_name)
print(f'{meas_name} measured')

filename = meas_folder / (meas_name + '.ntwk')
rf.write(str(filename), measurement)


#%% SHORT S22 measurement 

meas_name = 'SHORT_S22'
vna.create_meas(meas_name,'S22', channel = meas_channel)

vna.sweep
measurement = vna.get_measurement(mname = meas_name)
print(f'{meas_name} measured')

filename = meas_folder / (meas_name + '.ntwk')
rf.write(str(filename), measurement)

#%%OPEN S11 measurement 

meas_name = 'OPEN_S11'
vna.create_meas(meas_name,'S11', channel = meas_channel)

vna.sweep
measurement = vna.get_measurement(mname = meas_name)
print(f'{meas_name} measured')

filename = meas_folder / (meas_name + '.ntwk')
rf.write(str(filename), measurement)

#%%OPEN S22 measurement 

meas_name = 'OPEN_S22'
vna.create_meas(meas_name,'S22', channel = meas_channel)

vna.sweep
measurement = vna.get_measurement(mname = meas_name)
print(f'{meas_name} measured')

filename = meas_folder / (meas_name + '.ntwk')
rf.write(str(filename), measurement)

#%%OLOAD S11 measurement 

meas_name = 'LOAD_S11'
vna.create_meas(meas_name,'S11', channel = meas_channel)

vna.sweep
measurement = vna.get_measurement(mname = meas_name)
print(f'{meas_name} measured')

filename = meas_folder / (meas_name + '.ntwk')
rf.write(str(filename), measurement)
#%%Load S22 measurement 

meas_name = 'LOAD_S22'
vna.create_meas(meas_name,'S22', channel = meas_channel)

vna.sweep
measurement = vna.get_measurement(mname = meas_name)
print(f'{meas_name} measured')

filename = meas_folder / (meas_name + '.ntwk')
rf.write(str(filename), measurement)
#%%THRU S21 measurement 

meas_name_S21 = 'THRU_S21'
vna.create_meas(meas_name_S21,'S21', channel = meas_channel)
vna.sweep
measurement = vna.get_measurement(mname = meas_name_S21)
print(f'{meas_name_S21} measured')

filename = meas_folder / (meas_name_S21 + '.ntwk')
rf.write(str(filename), measurement)


##THRU S12
meas_name_S12 = 'THRU_S12'
thru_s12 = vna.create_meas(meas_name_S12,'S12', channel = meas_channel)
vna.sweep
measurement = vna.get_measurement(mname = meas_name_S12)
print(f'{meas_name_S12} measured')

filename = meas_folder / (meas_name_S12 + '.ntwk')
rf.write(str(filename), measurement)


#%%
test_network.frequency.unit = 'GHz'
test_network.plot_s_mag()

rf.write('C:/Users/Zaber/Documents/data/scikit_measurements/test_write.ntwk', test_network)

loaded_ntwk = Network('C:/Users/Zaber/Documents/data/scikit_measurements/test_write.ntwk')

loaded_ntwk.plot_s_mag()
