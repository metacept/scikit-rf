# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 12:39:25 2021

@author: Zaber
"""

import cv2
import numpy as np
import glob
 
img_array = []
for filename in glob.glob('C:\Users\Zaber\Documents\data\scikit_measurements\channel4_251pts\extraceted_alpha__vs_voltage_0*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()