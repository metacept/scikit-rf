# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 10:21:32 2021

@author: Zaber
"""

import skrf as rf
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

freq = rf.Frequency(8,12, 101, unit ='ghz')

ntwk = rf.Network()

ntwk.frequency = freq
ntwk.s = np.ones((101,1,1))

ntwk.plot_s_im()

new_ntwk= ntwk.delay(101, 'ns')


fig, ax =plt.subplots()
new_ntwk.plot_s_re(axis = ax)


new_new_ntwk = new_ntwk / new_ntwk
new_new_ntwk.plot_s_re(axis = ax)
