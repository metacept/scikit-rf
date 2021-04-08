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
from cycler import cycler


import matplotlib.pyplot as plt
rf.stylely




# %matplotlib inline
## created calibration class using 

n_freq=101
pad_zeros = np.zeros((n_freq, 2, 2)) 

plt.rcParams['axes.prop_cycle'] = cycler(color=['b', 'r', 'g', 'y'])
# plt.rcParams['axes.prop_cycle'] = cycler(color=[.1, , 'r', 'y'])

#%% Define Ideal Cals from Agilent 85521A Mechanical Cal Kit
###########################################################################
##Ideal Thru


base_match = rf.Network()
base_match.frequency = rf.Frequency(8,12, n_freq, 'ghz')

base_match.s = pad_zeros
base_match.s[:,0,1] = 1*np.ones(base_match.f.shape)
base_match.s[:,1,0] = 1*np.ones(base_match.f.shape)

THRU_85521A=base_match.delay(115.881, unit = 'ps')

fig, ax = plt.subplots()
THRU_85521A.plot_s_re(axis =ax, linewidth= 2)
THRU_85521A.plot_s_im(axis =ax, linestyle='--', linewidth= 2)
ax.set_title('Thru measurement')

# THRU_S21_85521A=base_match.delay(115.881, unit = 'ps')
# THRU_S12_85521A=base_match.delay(115.881, unit = 'ps')

# THRU_S21_85521A.plot_s_re(axis = ax)
# THRU_S12_85521A.plot_s_re(axis = ax)

#%% Ideal Open

base_open = base_match
base_open.s = 2*np.ones(base_match.f.shape)
OPEN_S11_85521A = base_open.delay(31.832, unit = 'ps') 
OPEN_S22_85521A = OPEN_S11_85521A 


# OPEN_S11_85521A.plot_s_re(axis = ax)
# OPEN_S22_85521A.plot_s_re(axis = ax)

OPEN_85521A = rf.two_port_reflect(OPEN_S11_85521A, OPEN_S22_85521A)

fig, ax = plt.subplots()
OPEN_85521A.plot_s_re(axis =ax, linewidth= 2)
OPEN_85521A.plot_s_im(axis =ax, linestyle='--', linewidth= 2)
#%% Ideal Short

base_short = base_match
base_short.s = -2*np.ones(base_match.f.shape)
SHORT_S11_85521A = base_short.delay(30.581, unit = 'ps')
SHORT_S22_85521A = SHORT_S11_85521A

SHORT_85521A = rf.two_port_reflect(SHORT_S11_85521A,SHORT_S22_85521A)

fig, ax = plt.subplots()
SHORT_85521A.plot_s_re(axis =ax, linewidth= 2)
SHORT_85521A.plot_s_im(axis =ax, linestyle='--', linewidth= 2)
# SHORT_S11_85521A.plot_s_re(axis = ax)
# SHORT_S22_85521A.plot_s_re(axis = ax)
#%% Ideal Load
LOAD_85521A = base_match
LOAD_85521A.s = pad_zeros

fig, ax = plt.subplots()
LOAD_85521A.plot_s_re(axis =ax, linewidth= 2)
LOAD_85521A.plot_s_im(axis =ax, linestyle='--', linewidth= 2)
#%%


#list of Network types, holding 'ideal' responses ORDER MUST BE SAME AS THOSE ENTERED BELOW IN MEASUREMENTS
my_ideals = [\
        SHORT_85521A,
        OPEN_85521A,
        LOAD_85521A,
        THRU_85521A,
        ]
    
#%% Measured response from Mechanical Cal (85521A)

cal_folder_name = 'eight_term_2021-04-02'

measurement_root_folder = Path('/Users/Zaber/Documents/data/scikit_measurements/')
meas_folder = measurement_root_folder / cal_folder_name

SHORT_S11 = np.load(meas_folder / 'SHORT_S11.ntwk', allow_pickle = True)
SHORT_S22 = np.load(meas_folder / 'SHORT_S22.ntwk', allow_pickle = True)
OPEN_S11 = np.load(meas_folder / 'OPEN_S11.ntwk', allow_pickle = True)
OPEN_S22 = np.load( meas_folder / 'OPEN_S22.ntwk', allow_pickle = True)
LOAD_S11 = np.load(meas_folder / 'LOAD_S11.ntwk', allow_pickle = True)
LOAD_S22 = np.load(meas_folder / 'LOAD_S22.ntwk', allow_pickle = True)

THRU_S11 = np.load(meas_folder / 'THRU_S11.ntwk', allow_pickle = True)
THRU_S22 = np.load(meas_folder / 'THRU_S22.ntwk', allow_pickle = True)
THRU_S21 = np.load(meas_folder / 'THRU_S21.ntwk', allow_pickle = True)
THRU_S12 = np.load(meas_folder / 'THRU_S12.ntwk', allow_pickle = True)
 


SHORT = rf.two_port_reflect(SHORT_S11,SHORT_S22)
OPEN = rf.two_port_reflect(OPEN_S11,OPEN_S22)
LOAD = rf.two_port_reflect(LOAD_S11,LOAD_S22)

THRU = rf.two_port_reflect(THRU_S11, THRU_S22)
THRU.s[:,0,1] = THRU_S12.s[:,0,0]
THRU.s[:,1,0] = THRU_S21.s[:,0,0]

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
               SHORT,
               OPEN,
               LOAD,
               THRU
        ]
    

## create a Calibration instance
cal = rf.SOLT(\
        ideals = my_ideals,
        measured = my_measured,
        )

# run calibration algorithm
cal.run()
#%%
# apply it to a dut
dut = THRU
dut.name = 'test'
dut_caled = cal.apply_cal(dut)
dut_caled.name =  dut.name + 'corrected'

# plot results
dut_caled.frequency.unit = 'ghz'
dut_caled.plot_s_deg()
# save results
dut_caled.write_touchstone()

#%%
# rf.Network(SHORT_S11.as_posix())
