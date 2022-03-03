#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 21:20:54 2021

@author: jamesgaston
"""
# input directory
directory= '/Users/jamesgaston/Desktop/Honours/Lab analysis/21-03-17/2021-03-17 DiD DiO incubations'

# create loop for errors and run functions
error_name=[]
error_vec=[]   
i = 0

for filename in os.listdir(directory):
    filepath = os.path.join(directory,filename)
    if filename.endswith(".czi"):
        sourceimage= czifile.imread(filepath)
        print(filename)
        [chan1, chan2] = splitchans(sourceimage)
        [thresh1,thresh2] = threshmask(chan1,chan2)
        [thresh1high, thresh2high] = threshmaskhigh(chan1, chan2)
        [thresh1low, thresh2low] = threshmasklow(chan1, chan2)
        error = errorcalc(thresh1,thresh2, thresh1high, thresh1low, thresh2high, thresh2low)
        print(error)
        error_name.append(filename)
        error_vec.append(error)
        i = i + 1
    else:
        continue


# split chans
#sourceimage= czifile.imread('Both_B_pre1.czi')
def splitchans(sourceimage):
    chan1= sourceimage[0,0,0,0,:,:,0]
    chan2= sourceimage[0,1,0,0,:,:,0]
    return chan1, chan2
[chan1, chan2] = splitchans(sourceimage)


# convert boolian true/false array for mask 1 into a float 1/0 array
def boolstr_to_floatstr(mask):
    if mask == 'True':
        return '1'
    elif mask == 'False':
        return '0'
    else:
        return mask


# make a mask for image 1, 2
def threshmask(chan1, chan2):
    Thresh = np.mean(chan1)+2 * np.std(chan1)
    if Thresh < 2033:
        Thresh = 2033
    else:
        Thresh = np.mean(chan1)+2 * np.std(chan1)
    mask1 = chan1 > Thresh
    thresh1= np.vectorize(boolstr_to_floatstr)(mask1).astype(float)
    mask2 = chan2 > Thresh
    thresh2= np.vectorize(boolstr_to_floatstr)(mask2).astype(float)
    return thresh1, thresh2

# make mask that is 5% higher
def threshmaskhigh(chan1, chan2):
    Thresh = np.mean(chan1)+2.1 * np.std(chan1)
    if Thresh < 2033:
        Thresh = 2033
    else:
        Thresh = np.mean(chan1)+2.1 * np.std(chan1)
    mask1 = chan1 > Thresh
    thresh1high= np.vectorize(boolstr_to_floatstr)(mask1).astype(float)
    mask2 = chan2 > Thresh
    thresh2high= np.vectorize(boolstr_to_floatstr)(mask2).astype(float)
    return thresh1high, thresh2high

# make mask that is 5% lower
def threshmasklow(chan1, chan2):
    Thresh = np.mean(chan1)+1.9 * np.std(chan1)
    if Thresh < 2033:
        Thresh = 2033
    else:
        Thresh = np.mean(chan1)+1.9 * np.std(chan1)
    mask1 = chan1 > Thresh
    thresh1low= np.vectorize(boolstr_to_floatstr)(mask1).astype(float)
    mask2 = chan2 > Thresh
    thresh2low= np.vectorize(boolstr_to_floatstr)(mask2).astype(float)
    return thresh1low, thresh2low

# run delta method calc for error
def errorcalc(thresh1, thresh2, thresh1high, thresh1low, thresh2high, thresh2low):
    intersection= np.sum(thresh1 * thresh2)
    intersectionhigh= np.sum(thresh1high * thresh2high)
    intersectionlow= np.sum(thresh1low * thresh2low)
    pixeltotal= np.sum(thresh1)+np.sum(thresh2)
    pixeltotalhigh= np.sum(thresh1high)+np.sum(thresh2high)
    pixeltotallow= np.sum(thresh1low)+np.sum(thresh2low)
    deltint= (intersectionlow - intersectionhigh)/2 
    deltall= (pixeltotallow - pixeltotalhigh)/2
    deltcolocsq= (deltint/intersection)**2 + (deltall/pixeltotal)**2
    deltcoloc= (intersection/pixeltotal) * math.sqrt(deltcolocsq)
    return deltcoloc

# output error
error = errorcalc(thresh1,thresh2, thresh1high, thresh1low, thresh2high, thresh2low)
