#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:55:27 2021

@author: jgollub
"""

import numpy as np
from pathlib import Path
import skrf as rf
from skrf.calibration import OnePort

import matplotlib.pyplot as plt
rf.stylely


fig, ax = plt.subplots()

# %matplotlib inline
## created calibration class using 

n_freq=101
pad_zeros = np.zeros((n_freq, 2, 2)) 

#%% Define Ideal Cals from Agilent 85521A Mechanical Cal Kit
#thru
base_match = rf.Network()
base_match.frequency = rf.Frequency(8,12, n_freq, 'ghz')

s_vals = pad_zeros
s_vals[:,1,0]=1*np.ones(base_match.f.shape)
base_match.s=s_vals
THRU_S21_85521A=base_match.delay(115.881, unit = 'ps')

s_vals = pad_zeros
s_vals[:,0,1]=1*np.ones(base_match.f.shape)
base_match.s=s_vals
THRU_S12_85521A=base_match.delay(115.881, unit = 'ps')

THRU_S21_85521A.plot_s_re(axis = ax)
THRU_S12_85521A.plot_s_re(axis = ax)

#open
base_open = base_match
s_vals = pad_zeros 
s_vals[:,0,0] = 2*np.ones(base_match.f.shape)
base_open.s = s_vals
OPEN_S11_85521A = base_open.delay(31.832, unit = 'ps') 

s_vals = pad_zeros 
s_vals[:,1,1] = 2*np.ones(base_match.f.shape)
base_open.s = s_vals
OPEN_S22_85521A = base_open.delay(31.832, unit = 'ps') 

OPEN_S11_85521A.plot_s_re(axis = ax)
OPEN_S22_85521A.plot_s_re(axis = ax)

#short
base_short = base_match
s_vals = pad_zeros
s_vals[:,0,0] = np.zeros(base_match.f.shape)
base_short.s = s_vals
SHORT_S11_85521A = base_open.delay(30.581, unit = 'ps')

s_vals[:,1,1] = np.zeros(base_match.f.shape)
base_short.s = s_vals
SHORT_S22_85521A = base_open.delay(30.581, unit = 'ps')

SHORT_S11_85521A.plot_s_re(axis = ax)
SHORT_S22_85521A.plot_s_re(axis = ax)

#load
base_load = base_match
base_load.s = s_vals
LOAD_S11_85521A = base_load
LOAD_S22_85521A = base_load

LOAD_S11_85521A.plot_s_re(axis=ax)
LOAD_S22_85521A.plot_s_re(axis=ax)

####

#list of Network types, holding 'ideal' responses ORDER MUST BE SAME AS THOSE ENTERED BELOW IN MEASUREMENTS
my_ideals = [\
        SHORT_S11_85521A,
        SHORT_S22_85521A,
        OPEN_S11_85521A,
        OPEN_S22_85521A,
        LOAD_S11_85521A,
        LOAD_S22_85521A,
        THRU_S21_85521A,
        THRU_S12_85521A,
        ]

    
#%% Measured response from Mechanical Cal (85521A)

cal_folder_name = 'eight_term_2021-04-02'

measurement_root_folder = Path('/Users/Zaber/Documents/data/scikit_measurements/')
meas_folder = measurement_root_folder / cal_folder_name

SHORT_S11 = meas_folder / 'SHORT_S11.ntwk'
SHORT_S22 = meas_folder / 'SHORT_S22.ntwk'
OPEN_S11 = meas_folder / 'OPEN_S11.ntwk'
OPEN_S22 = meas_folder / 'OPEN_S22.ntwk'
LOAD_S11 = meas_folder / 'LOAD_S11.ntwk'
LOAD_S22 = meas_folder / 'LOAD_S22.ntwk'
THRU_S21 = meas_folder / 'THRU_S21.ntwk'
THRU_S12 = meas_folder / 'THRU_S12.ntwk'
 
# my_measured_ntwk = [\
#         rf.Network(SHORT_S11.as_posix()),
#         rf.Network(SHORT_S22.as_posix()),
#         rf.Network(OPEN_S11.as_posix()),
#         rf.Network(OPEN_S22.as_posix()),
#         rf.Network(LOAD_S11.as_posix()),
#         rf.Network(LOAD_S22.as_posix()),
#         rf.Network(THRU_S21.as_posix()),
#         rf.Network(THRU_S12.as_posix()),
#         ]
    
my_measured = [\
        np.load(SHORT_S11.as_posix(), allow_pickle = True),
        np.load(SHORT_S22.as_posix(), allow_pickle = True),
        np.load(OPEN_S11.as_posix(), allow_pickle = True),
        np.load(OPEN_S22.as_posix(), allow_pickle = True),
        np.load(LOAD_S11.as_posix(), allow_pickle = True),
        np.load(LOAD_S22.as_posix(), allow_pickle = True),
        np.load(THRU_S21.as_posix(), allow_pickle = True),
        np.load(THRU_S12.as_posix(), allow_pickle = True),
        ]
    

## create a Calibration instance
cal = rf.OnePort(\
        ideals = my_ideals,
        measured = my_measured,
        )


## run, and apply calibration to a DUT

# run calibration algorithm
cal.run()

# apply it to a dut
dut = rf.Network('my_dut.s1p')
dut_caled = cal.apply_cal(dut)
dut_caled.name =  dut.name + ' corrected'

# plot results
dut_caled.plot_s_db()
# save results
dut_caled.write_touchstone()

#%%
rf.Network(SHORT_S11.as_posix())
