# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import skrf as rf
from skrf.vi.vna import PNA
from skrf import Network
import matplotlib.pyplot as plt
rf.stylely()
# %matplotlib inline
#sweep values
f_start = 8E9
f_stop = 12E9
f_npoints = int(101)

vna = PNA(address ='TCPIP0::10.236.73.132::inst0::INSTR')
vna.reset()
vna.set_frequency_sweep(f_start, f_stop, f_npoints, channel = 1, f_unit = 'Hz', sweep_type = 'lin')

#%% SHORT measurement setup VNA measurement

S11 = vna.create_meas('SHORT','S11', channel =1)
# vna.display_trace('REMOTE', channel = 1, window_n =2, trace_n = 2, display_format = 'MLOG') 

vna.sweep
meas_thru = vna.get_measurement(mname = 'THRU')



#%% Thru measurement setup VNA measurement

network_meas = vna.create_meas('THRU','S21', channel =1)
# vna.display_trace('REMOTE', channel = 1, window_n =2, trace_n = 2, display_format = 'MLOG') 

vna.sweep
meas_thru = vna.get_measurement(mname = 'THRU')

#%%
test_network.frequency.unit = 'GHz'
test_network.plot_s_mag()

rf.write('C:/Users/Zaber/Documents/data/scikit_measurements/test_write.ntwk', test_network)

loaded_ntwk = Network('C:/Users/Zaber/Documents/data/scikit_measurements/test_write.ntwk')

loaded_ntwk.plot_s_mag()
