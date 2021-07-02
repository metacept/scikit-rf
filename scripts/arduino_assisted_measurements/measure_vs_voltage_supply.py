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
from skrf.vi.vna import PNA
from skrf.calibration import OnePort

#Communicate with Power Supply
import pyvisa as visa

rf.stylely

# %matplotlib inline
## created calibration class using 

plt.rcParams['axes.prop_cycle'] = cycler(color=['b', 'r', 'g', 'y'])
# plt.rcParams['axes.prop_cycle'] = cycler(color=[.1, , 'r', 'y'])

#%% keysight power supply

#%% Measured response from TRL Cal 

measurement_root_folder = Path('/Users/Zaber/Documents/data/scikit_measurements/')
cal_folder_name = 'TRL2021-05-26'

meas_folder = measurement_root_folder / cal_folder_name

THRU_S11 = np.load(meas_folder / 'THRU_S11.ntwk', allow_pickle = True)
THRU_S22 = np.load(meas_folder / 'THRU_S22.ntwk', allow_pickle = True)
THRU_S21 = np.load(meas_folder / 'THRU_S21.ntwk', allow_pickle = True)
THRU_S12 = np.load(meas_folder / 'THRU_S12.ntwk', allow_pickle = True)

REFLECT_S11 = np.load(meas_folder / 'REFLECT_S11.ntwk', allow_pickle = True)
REFLECT_S22 = np.load(meas_folder / 'REFLECT_S22.ntwk', allow_pickle = True)
REFLECT_S21 = np.load(meas_folder / 'REFLECT_S21.ntwk', allow_pickle = True)
REFLECT_S12 = np.load(meas_folder / 'REFLECT_S12.ntwk', allow_pickle = True)

LINE_S11 = np.load(meas_folder / 'LINE_S11.ntwk', allow_pickle = True)
LINE_S22 = np.load(meas_folder / 'LINE_S22.ntwk', allow_pickle = True)
LINE_S21 = np.load(meas_folder / 'LINE_S21.ntwk', allow_pickle = True)
LINE_S12 = np.load(meas_folder / 'LINE_S12.ntwk', allow_pickle = True)

SWITCH_TERMS = np.load(meas_folder / 'SWITCH_TERMS.ntwk', allow_pickle = True)

THRU = rf.two_port_reflect(THRU_S11, THRU_S22)
n_freq = len(THRU.f)
pad_zeros = np.zeros((n_freq, 2, 2)) 

THRU.s[:,0,1] = THRU_S12.s[:,0,0]
THRU.s[:,1,0] = THRU_S21.s[:,0,0]
THRU.z0  = (50+0j)*np.ones((n_freq, 4)) 


REFLECT = rf.two_port_reflect(REFLECT_S11, REFLECT_S22)
REFLECT.s[:,0,1] = REFLECT_S12.s[:,0,0]
REFLECT.s[:,1,0] = REFLECT_S21.s[:,0,0]
REFLECT.z0 = (50+0j)*np.ones((n_freq, 4))

LINE = rf.two_port_reflect(LINE_S11, LINE_S22)
LINE.s[:,0,1] = LINE_S12.s[:,0,0]
LINE.s[:,1,0] = LINE_S21.s[:,0,0]
LINE.z0 = (50+0j)*np.ones((n_freq, 4))

my_ideals = [None, -1, None]

my_measured = [\
               THRU,
               REFLECT,
               LINE,
        ]
    

#%%
    
    
## create a Calibration instance
trl = rf.TRL(\
        measured = my_measured,
        ideals = my_ideals,
        estimate_line = True,
        switch_terms = SWITCH_TERMS,
        )

# run calibration algorithm
trl.run()

#%% setup measurements


f_start = THRU.f[0]
f_stop = THRU.f[-1]
f_npoints = len(THRU.f)

# f_start = 8E9
# f_stop = 12E9
# f_npoints = int(101)

vna = PNA(address ='TCPIP0::10.236.73.132::inst0::INSTR')
vna.reset()
vna.scpi.set_trigger_manual
# vna.scpi.set_display_on(wnum=1,state=True)


meas_channel = 2


meas_S11 = 'S11'
vna.create_meas(meas_S11,'S11', channel = meas_channel) 
meas_S22 = 'S22'
vna.create_meas(meas_S22,'S22', channel = meas_channel) 
meas_S21 = 'S21'
vna.create_meas(meas_S21,'S21', channel = meas_channel) 
meas_S12 = 'S12'
vna.create_meas(meas_S12,'S12', channel = meas_channel) 

vna.set_frequency_sweep(f_start, 
                        f_stop, 
                        f_npoints, 
                        f_unit = 'Hz',
                        channel = meas_channel, 
                        )


#%% set voltages with arduino and take measurements

set_data_folder = Path('/Users/Zaber/Documents/data/scikit_measurements/power_supply_256pts/')
set_data_folder.mkdir(exist_ok = True)

fig, (ax1,ax2)= plt.subplots(2,1)
Vref = 5 #volts

voltage_values = np.linspace(0,Vref,256)

#Connect to Power Supply
rm = visa.ResourceManager()
inst = rm.open_resource("COM3")

# When sending command to E3631A, The "Rmt" and "Adrs" icon are on the display
# panel. All input from panel are inactived, until you press "Store/Local" button.

# identify instrument
inst.query("*IDN?")

# power on
inst.write("OUTP ON")

# initalize channel, voltage, current
inst.write("APPL P6V, 0.0, 0.1")

count = 0


for v_indx in voltage_values:    
    inst.write("VOLT {}".format(v_indx))     # change voltage

    vna.sweep
    # S11
    s11 = vna.get_measurement(mname = meas_S11)
    # print(f'{meas_S11} measured')
    filename = meas_folder / ('THRU_' + meas_S11 + '.ntwk')
    # rf.write(str(filename), measurement)
    # measurement.frequency.units = 'ghz'
    # measurement.plot_s_db(ax = ax1, label ='THRU S11')
    
    #S22
    s22 = vna.get_measurement(mname = meas_S22)
    # print(f'{meas_S22} measured')
    filename = meas_folder / ('THRU_' + meas_S22 + '.ntwk')
    # rf.write(str(filename), measurement)
    # measurement.frequency.units = 'ghz'
    # measurement.plot_s_db(ax = ax2, label ='THRU S22')
    
    #S21
    s21 = vna.get_measurement(mname = meas_S21)
    # print(f'{meas_S21} measured')
    filename = meas_folder / ('THRU_' + meas_S21 + '.ntwk')
    # rf.write(str(filename), measurement)
    # measurement.frequency.units = 'ghz'
    # measurement.plot_s_db(ax = ax1, label ='THRU S21')
    
    #S12
    s12 = vna.get_measurement(mname = meas_S12)
    # print(f'{meas_S12} measured')
    
    filename = meas_folder / ('THRU_' + meas_S12 + '.ntwk')
    # rf.write(str(filename), measurement)
    # measurement.frequency.units = 'ghz'
    # measurement.plot_s_db(ax = ax2, label ='THRU S12')
    
    dut_raw = rf.two_port_reflect(s11, s22)
    
    dut_raw.s[:,0,1] = s12.s[:,0,0]
    dut_raw.s[:,1,0] = s21.s[:,0,0]
    dut_raw.z0 = (50+0j)*np.ones((n_freq, 4))
    
    # dut_raw.plot_s_db(ax = ax)
    # dut_corrected.write_touchstone()

# apply it to a dut

    dut_raw.name = 'voltage_indx_' + str(count)
    dut_corrected = trl.apply_cal(dut_raw)
    dut_corrected.name =  'trl_corrected_' + dut_raw.name
    
    # plot results
    # fig, (ax1,ax2)= plt.subplots(2,1)
    # dut_corrected.frequency.unit = 'ghz'
    
    # dut_corrected.plot_s_deg(ax = ax1)
    # dut_corrected.plot_s_db(ax = ax2)

    # save results
    
    dut_corrected.write_touchstone(dut_corrected.name, set_data_folder)
    
    count += 1
    
# power off
inst.write("OUTP OFF")

 #%%
# dict_o_ntwks = rf.read_all(set_data_folder, contains = 's2p')

# a0 = 14E-3
# b0 = 0.762E-3

# waveguide = rf.RectangularWaveguide(frequency = dict_o_ntwks[0].frequency, a = a0, b = b0, ep_r = 3.45, nports =1)
# left= waveguide.line(5E-3, 'm')
# right = left

# alpha = np.zeros((len(dut_corrected.f), 256), dtype = complex)
# for ii in range(256):
#     temp =dict_o_ntwks['trl_corrected_voltage_indx_' + str(ii)]
#     temp.z0 = waveguide.z0
#     element = left.inv ** temp ** right.inv  
#     alpha_temp = -a0*b0*(1+element.s[:,0,0]-element.s[:,1,0])/waveguide.k0
#     alpha[:,ii] = alpha_temp/np.amax(np.abs(alpha_temp))
# # set up subplot grid

#%%
dict_o_ntwks = rf.read_all(set_data_folder, contains = '.s2p')

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
alpha_max = (np.amax(np.abs(alpha), axis =(1)))
alpha_max = alpha_max[:,np.newaxis]

alpha = alpha/alpha_max


#%%
f_indx = 125
for f_indx in list(range(0,251,2)):
    print(f'freq = {first_ntwk.f[f_indx]}')
    alpha_temp  = alpha[f_indx,:]
    
    fig = plt.figure(f_indx)
    
    gridspec.GridSpec(2,2)
    plt.subplot2grid((2,2), (0,0))
    plt.plot(range(256), np.abs(alpha_temp))
    plt.title('Polarizability Mag (dB)', fontsize = 10)
    plt.tight_layout()
    
    plt.subplot2grid((2,2), (1,0))
    plt.plot(range(256), np.degrees(np.angle(alpha_temp)))
    plt.title('Polarizability Phase (deg)',fontsize = 10)
    plt.ylim(-180,180)
    plt.tight_layout()
    
    plt.subplot2grid((2,2), (0,1), colspan = 1, rowspan = 2)
    plt.scatter(np.real(alpha_temp), np.imag(alpha_temp))
    # plt.axis('equal')
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.title(f'Polarizability Real vs Imaginary, f= {first_ntwk.f[f_indx]/1E9: .2f} GHz', fontsize = 10)
    plt.tight_layout()
    filename = set_data_folder / f'extraceted_alpha__vs_voltage_{f_indx}.png'
    plt.savefig(filename)



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