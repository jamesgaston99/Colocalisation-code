#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 23:24:38 2021

@author: jamesgaston
"""

import numpy as np
import czifile 
import os

#load in directory
directory= '/Users/jamesgaston/Desktop/Honours/Lab analysis/21-06-02/Biotin_no_biotin_test_02-06'

coloc_name=[]
coloc_vec=[]   
i = 0

# run functions for mean and std
for filename in os.listdir(directory):
    filepath = os.path.join(directory,filename)
    if filename.endswith(".czi"):
        sourceimage= czifile.imread(filepath)
        print(filename)
        [chan1, chan2] = splitchans(sourceimage)
        mean_and_std =  mean_std(chan1, chan2)
        coloc_name.append(filename)
        coloc_vec.append(mean_and_std)
        i = i + 1
    else:
        continue

# run functions for max intensity
max_name=[]
max_vec=[]
i = 0

for filename in os.listdir(directory):
    filepath = os.path.join(directory,filename)
    if filename.endswith(".czi"):
        sourceimage= czifile.imread(filepath)
        print(filename)
        [chan1, chan2] = splitchans(sourceimage)
        max_intense =  max_int(chan1, chan2)
        max_name.append(filename)
        max_vec.append(max_intense)
        i = i + 1
    else:
        continue
 
    # run functions for mean liposome intensity + threshold level
lipo_name=[]
lipo_vec=[]
i = 0

for filename in os.listdir(directory):
    filepath = os.path.join(directory,filename)
    if filename.endswith(".czi"):
        sourceimage= czifile.imread(filepath)
        print(filename)
        [chan1, chan2] = splitchans(sourceimage)
        [thresh1,thresh2] = threshmask(chan1,chan2)
        lipo_mean =  mean_lipo(chan1, chan2, thresh1, thresh2)
        lipo_name.append(filename)
        lipo_vec.append(lipo_mean)
        i = i + 1
    else:
        continue

# split channels function
def splitchans(sourceimage):
    chan1= sourceimage[0,0,0,0,:,:,0]
    chan2= sourceimage[0,1,0,0,:,:,0]
    return chan1, chan2

# mean and standard dev function
def mean_std(chan1, chan2):
   chan1mean = np.mean(chan1)
   chan1std = np.std(chan1)
   print(chan1mean)
   print (chan1std)
   chan2mean = np.mean(chan2)
   chan2std = np.std(chan2)
   print(chan2mean)
   print(chan2std)
   return chan1mean, chan1std, chan2mean, chan2std

# defines max intensity across an image array
def max_int(chan1, chan2):
   chan1max = np.max(chan1)
   print(chan1max)
   chan2max = np.max(chan2)
   print(chan2max)
   return chan1max, chan2max


# creates the threshold
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

# calculates threshold level number and mean intensity above threshold
def mean_lipo(thresh1, thresh2, chan1, chan2):
    thresharray1 = chan1 * thresh1
    array1_nan = np.nanmean(np.where(thresharray1!=0,thresharray1,np.nan),1)
    print(np.nanmean(array1_nan))
    thresharray2 = chan2 * thresh2
    array2_nan = np.nanmean(np.where(thresharray2!=0,thresharray2,np.nan),1)
    print(np.nanmean(array2_nan))
    return array1_nan, array2_nan