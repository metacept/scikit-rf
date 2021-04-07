# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 17:51:54 2021

@author: Zaber
"""
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
#%% build folder for cal data using today's date
today = date.today()
date_str = today.strftime("%Y-%m-%d")
cal_folder_name = 'Cal_eight_Term_test'+date_str

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

fig, (ax1, ax2)  = plt.subplots(2,1)