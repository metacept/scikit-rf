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
## created necessary data for Calibration class
#setup idea values

n_freq=101
pad_zeros = np.zeros((n_freq, 2, 2)) 
#thru
base_match = rf.Network()
base_match.frequency = rf.Frequency(8,12, n_freq, 'ghz')

s_vals = pad_zeros
s_vals[:,1,0]=1*np.ones(base_match.f.shape)
base_match.s=s_vals
cal85521A_thru_21=base_match.delay(115.881, unit = 'ps')

s_vals = pad_zeros
s_vals[:,0,1]=1*np.ones(base_match.f.shape)
base_match.s=s_vals
cal85521A_thru_12=base_match.delay(115.881, unit = 'ps')

cal85521A_thru_21.plot_s_re(axis = ax)
cal85521A_thru_12.plot_s_re(axis = ax)

#open
base_open = base_match
s_vals = pad_zeros 
s_vals[:,0,0] = 2*np.ones(base_match.f.shape)
base_open.s = s_vals
cal85521A_open_s11 = base_open.delay(31.832, unit = 'ps') 

s_vals = pad_zeros 
s_vals[:,1,1] = 2*np.ones(base_match.f.shape)
base_open.s = s_vals
cal85521A_open_s22 = base_open.delay(31.832, unit = 'ps') 

cal85521A_open_s11.plot_s_re(axis = ax)
cal85521A_open_s22.plot_s_re(axis = ax)

#short
base_short = base_match
s_vals = pad_zeros
s_vals[:,0,0] = np.zeros(base_match.f.shape)
base_short.s = s_vals
cal85521A_short_s11 = base_open.delay(30.581, unit = 'ps')

s_vals[:,1,1] = np.zeros(base_match.f.shape)
base_short.s = s_vals
cal85521A_short_s22 = base_open.delay(30.581, unit = 'ps')

cal85521A_short_s11.plot_s_re(axis = ax)
cal85521A_short_s22.plot_s_re(axis = ax)

#load
base_load = base_match
base_load.s = s_vals
cal85521A_load_s11 = base_load
cal85521A_load_s22 = base_load

cal85521A_load_s11.plot_s_re(axis=ax)
cal85521A_load_s22.plot_s_re(axis=ax)

####

cal_data_folder = Path('/Users/jgollub/Desktop/scikit_measurements/')





# a list of Network types, holding 'ideal' responses
my_ideals = [\
        cal85521A_thru_21,
        cal85521A_thru_12,
        cal85521A_open_s11,
        cal85521A_open_s22,
        cal85521A_short_s11,
        cal85521A_short_s22,
        cal85521A_load_s11,
        cal85521A_load_s11,
        ]

# a list of Network types, holding 'measured' responses
my_measured = [\
        rf.Network('measured/_S11.s1p'),
        rf.Network('measured/open.s1p'),
        rf.Network('measured/load.s1p'),
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