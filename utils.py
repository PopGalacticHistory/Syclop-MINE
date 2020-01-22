#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:13:16 2020

@author: michael
"""


'''
Parameters
----------
image : ndarray
    Input image data. Will be converted to float.
mode : str
    One of the following strings, selecting the type of noise to add:

    'gauss'     Gaussian-distributed additive noise.
    'poisson'   Poisson-distributed noise generated from the data.
    's&p'       Replaces random pixels with 0 or 1.
    'speckle'   Multiplicative noise using out = image + n*image,where
                n is uniform noise with specified mean & variance.

'''

import numpy as np
import os
from skimage.transform import rescale, resize, downscale_local_mean, rotate
import skimage.segmentation as seg
from skimage.transform import swirl
import torch
import matplotlib.pyplot as plt 


def noisy(noise_typ,image, rotation = 45, swirl_rate = 5):
   if noise_typ == "gauss":
      row,col, ch = image.shape
      mean = 0
      var = 0.1
      sigma = var**0.5
      gauss = np.random.normal(mean,sigma,(row,col,ch))
      gauss = gauss.reshape(row,col,ch)
      noisy = image + gauss
      return noisy
  
   elif noise_typ == "s&p":
      row,col = image.shape
      s_vs_p = 0.5
      amount = 0.004
      out = np.copy(image)
      # Salt mode
      num_salt = np.ceil(amount * image.size()[0] * s_vs_p)
      coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape]
      out[coords] = 1
      # Pepper mode
      num_pepper = np.ceil(amount* image.size()[0] * (1. - s_vs_p))
      coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
      out[coords] = 0
      return out

   elif noise_typ =="speckle":
      row,col = image.shape
      gauss = np.random.randn(row,col)
      gauss = gauss.reshape(row,col)        
      noisy = image + image * gauss
      return noisy
   
   elif noise_typ == "rotate":
       noisy = rotate(image, rotation)
       return noisy
   
   elif noise_typ == "seg-fel":
       noisy = seg.felzenszwalb(image)
       return noisy
   
   elif noise_typ == "seg-swirl": 
       noisy = swirl(image, rotation=0, strength=5, radius=120)
       return noisy
   
    
def create_z(orig_data, noise_list = ['gauss','seg-swirl'], limit = True):
    z = []
    for index, image in enumerate(orig_data):
        if limit:
            if index>19:
                break
        temp_image = image[0]
        for noise in noise_list:
            temp_image = (noisy(noise,temp_image))
        z.append(temp_image)

    return z 