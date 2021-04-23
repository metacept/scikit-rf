#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:55:27 2021

@author: jgollub
"""
#general
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import date
from cycler import cycler
import matplotlib.gridspec as gridspec
from contextlib import ExitStack

#s-parameter networks
import skrf as rf
from skrf.calibration import OnePort

#arduino control
# import serial

rf.stylely

# %matplotlib inline
## created calibration class using 

plt.rcParams['axes.prop_cycle'] = cycler(color=['b', 'r', 'g', 'y'])
# plt.rcParams['axes.prop_cycle'] = cycler(color=[.1, , 'r', 'y'])


# #%%
# a0 = 14E-3
# b0 = 0.762E-3
# waveguide = rf.RectangularWaveguide(frequency = dut_corrected.frequency, a = a0, b = b0, ep_r = 3.45, nports =1)
# left= waveguide.line(5E-3, 'm')
# right = left

# dict_o_ntwks = rf.read_all(set_data_folder, contains = 's2p')
# alpha = np.zeros((len(dut_corrected.f), 256), dtype = complex)
# for ii in range(256):
#     temp =dict_o_ntwks['trl_corrected_voltage_indx_' + str(ii)]
#     temp.z0 = waveguide.z0
#     element = left.inv ** temp ** right.inv  
#     alpha_temp = -a0*b0*(1+element.s[:,0,0]-element.s[:,1,0])/waveguide.k0
#     alpha[:,ii] = alpha_temp/np.amax(np.abs(alpha_temp))
# # set up subplot grid
#%%

data_folder = Path('/Users/jgollub/Dropbox (Duke Electric & Comp)/scikit_measurements/channel3/')

Vref = 5
voltage_settings = list(range(256)) #0-255 states
voltage_values =Vref*np.array(voltage_settings)/255
voltage_dict = dict(zip(voltage_settings, voltage_values))

dict_o_ntwks = rf.read_all(data_folder, contains = '.s2p')

a0 = 14E-3
b0 = 0.762E-3

first_ntwk = dict_o_ntwks['trl_corrected_voltage_indx_0']
waveguide = rf.RectangularWaveguide(frequency = first_ntwk.frequency, 
                                    a = a0, 
                                    b = b0, 
                                    ep_r = 3.45, 
                                    nports =2,
                                    )
left= waveguide.line(5E-3, 'm')
right = left
alpha = np.zeros((len(first_ntwk.f), 256), dtype = complex)
for ii in range(256):
    meas_ntwk =dict_o_ntwks['trl_corrected_voltage_indx_' + str(ii)]

    s11_prime = meas_ntwk.s[:,0,0]/(np.exp(-1j*waveguide.k0*1E-2))
    s21_prime = meas_ntwk.s[:,1,0]/(np.exp(-1j*waveguide.k0*1E-2))                            
    alpha_temp = -a0*b0*1j*(1+s11_prime-s21_prime)/waveguide.k0
    # alpha_temp = -1j*(1+s11_prime-s21_prime)/waveguide.k0
    
    alpha[:,ii] = alpha_temp

alpha = alpha/(np.amax(np.abs(alpha), axis =(0,1)))
# set up subplot grid

#%%
f_indx = 38
print(f'freq = {first_ntwk.f[f_indx]}')
alpha_at_freq  = alpha[f_indx,:]

fig = plt.figure(1)

gridspec.GridSpec(2,2)
plt.subplot2grid((2,2), (0,0))
plt.plot(voltage_values, np.abs(alpha_at_freq))
plt.title('Polarizability Mag', fontsize = 10)
plt.xlabel('Volts')
plt.ylabel('Mag (a.u)')
plt.tight_layout()

plt.subplot2grid((2,2), (1,0))
plt.plot(voltage_values, np.degrees(np.unwrap(np.angle(alpha_at_freq))))
plt.title('Polarizability Phase (deg)',fontsize = 10)
plt.xlabel('Volts')
plt.ylabel('Phase (deg)')

plt.ylim(-270,270)
plt.tight_layout()

plt.subplot2grid((2,2), (0,1), colspan = 1, rowspan = 2)
plt.scatter(np.real(alpha_at_freq), np.imag(alpha_at_freq))
# plt.axis('equal')
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.title('Polarizability Real vs Imaginary ', fontsize = 10)
plt.xlabel('Real(alpha)')
plt.ylabel('Imag(alpha)')

plt.tight_layout()


#%%
fig, ax =plt.subplots()
voltage_indx = 200

test_ntwk =dict_o_ntwks['trl_corrected_voltage_indx_'+str(voltage_indx)]
test_ntwk.frequency.units = 'ghz'

# test_ntwk.frequency.units = 'ghz'
test_ntwk.plot_s_db(ax = ax)
print(f'{voltage_dict[voltage_indx]}')

#%%
# waveguide = rf.RectangularWaveguide(frequency = dut_corrected.frequency, a = 14E-3, b = 0.762E-3, ep_r = 3.45, nports =2)
# left= waveguide.line(0E-3, 'm', z0 = 50, embed=True)
# right = left
# point_alpha = left.inv ** dut_corrected ** right.inv

# alpha = -(1+point_alpha.s[:,0,0]-point_alpha.s[:,1,0])/waveguide.k0
# alpha =alpha/np.amax(np.abs(alpha))

# fig = plt.figure(1)
# # set up subplot grid
# gridspec.GridSpec(2,2)
# plt.subplot2grid((2,2), (0,0))
# plt.plot(dut_corrected.f, np.abs(alpha))
# plt.title('Polarizability Mag (dB)', fontsize = 10)
# plt.tight_layout()

# plt.subplot2grid((2,2), (1,0))
# plt.plot(dut_corrected.f, np.angle(alpha))
# plt.title('Polarizability Phase (deg)',fontsize = 10)
# plt.tight_layout()

# plt.subplot2grid((2,2), (0,1), colspan = 1, rowspan = 2)
# plt.scatter(np.real(alpha), np.imag(alpha))
# # plt.axis('equal')
# plt.xlim(-1,1)
# plt.ylim(-1,1)
# plt.title('Polarizability Real vs Imaginary ', fontsize = 10)
# plt.tight_layout()