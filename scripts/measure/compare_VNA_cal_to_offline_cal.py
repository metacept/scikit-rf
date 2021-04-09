"""
Created on Thu Apr  8 17:27:12 2021

@author: Zaber
"""

import skrf as rf
from skrf.vi.vna import PNA
from skrf import Network
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import date


#import 2 port data

DUT_Agilent_corrected =rf.Network('C:\\Users\\Zaber\\Documents\\data\\scikit_measurements\\Agilent Cal\\Calibrated_DUT.s2p')

#%%
vna.sweep

measurement_S11 = vna.get_measurement(mname = meas_S11)
measurement_S22 = vna.get_measurement(mname = meas_S22)
measurement_S21 = vna.get_measurement(mname = meas_S21)
measurement_S12 = vna.get_measurement(mname = meas_S12)


measurement = rf.two_port_reflect(measurement_S11, measurement_S22)
measurement.s[:,0,1] = measurement_S12.s[:,0,0]
measurement.s[:,1,0] = measurement_S21.s[:,0,0]

measurement_corrected = cal.apply_cal(measurement)


#%%
%matplotlib inline
fig, (ax1, ax2) =plt.subplots(2,1)
ax1.set_title('VNA versus Offline Calibration')

measurement_corrected.plot_s_re(ax = ax1, linestyle = '--')
measurement_corrected.plot_s_im(ax = ax2, linestyle = '--')

DUT_Agilent_corrected.plot_s_re(ax = ax1)
DUT_Agilent_corrected.plot_s_im(ax = ax2)


rf.Freespace