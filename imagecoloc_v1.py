# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy as np
from PIL import Image
from numpy import asarray
import czifile 
import cv2 
import glob
import os
import csv
from subprocess import Popen
# Loading in directory of .czi images we are looking at


directory= '/Users/jamesgaston/Desktop/Standard_curve_15-11'


# Establishing loop that will run through 
coloc_name=[]
coloc_vec=[]   
i = 0

# coloc_actual_vec = np.zeros(shape = (len(os.listdir(directory)),1))

# Running all the functions for colocalisation
# Need to first load in all these functions before running this loop
for filename in os.listdir(directory):
    filepath = os.path.join(directory,filename)
    if filename.endswith(".czi"):
        sourceimage= czifile.imread(filepath)
        print(filename)
        [chan1, chan2] = splitchans(sourceimage)
        [thresh1,thresh2] = threshmask(chan1,chan2)
        coloc_temp = percentcoloc(thresh1,thresh2)
        print(coloc_temp)
        coloc_name.append(filename)
        coloc_vec.append(coloc_temp)
        coloc_actual_vec[i] = coloc_temp
        i = i + 1
    else:
        continue
#sum(coloc_actual_vec*coloc_actual_vec)
    

# code for trying to readout into an excel, can work on later

# with open('coloc.csv', 'w', encoding='utf8') as csv_out:
#    writer = csv.writer(csv_out)
 #   rows = [
#        ['coloc_name'],
 #       ['coloc_vec']
#]
 #   writer.writerows(rows)

#p = Popen('coloc.csv', shell=True)

# splitting into red and green channels
def splitchans(sourceimage):
    chan1= sourceimage[0,0,0,0,:,:,0]
    chan2= sourceimage[0,1,0,0,:,:,0]
    return chan1, chan2

# convert boolian true/false array for mask 1 into a float 1/0 array
def boolstr_to_floatstr(mask):
    if mask == 'True':
        return '1'
    elif mask == 'False':
        return '0'
    else:
        return mask

#determine intersection, pixel total, and percent coloc
def percentcoloc(thresh1, thresh2):
    intersection= np.sum(thresh1 * thresh2)
    pixeltotal= np.sum(thresh1)+np.sum(thresh2)
    percentfluorophore= intersection/pixeltotal
    return percentfluorophore


# make a mask for image 1, 2
def threshmask(chan1, chan2):
    Thresh = np.mean(chan1)+2 * np.std(chan1)
    if Thresh < 2033:
        Thresh = 2033
    else:
        Thresh = np.mean(chan1)+2 * np.std(chan1)
    print(Thresh)
    mask1 = chan1 > Thresh
    thresh1= np.vectorize(boolstr_to_floatstr)(mask1).astype(float)
    mask2 = chan2 > Thresh
    thresh2= np.vectorize(boolstr_to_floatstr)(mask2).astype(float)
    return thresh1, thresh2

# mean and standard dev function
def mean_image(chan1, chan2):
   chan1mean = np.mean(chan1)
   print(chan1mean)
   chan2mean = np.mean(chan2)
   print(chan2mean)
   return chan1mean, chan2mean



    
#showing channel 2 image
#Image.fromarray(c2im)

#def scrambler(c1im):
    #size(c1im)



