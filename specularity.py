# -*- encoding: utf-8 -*-
'''
@File    :   specularity.py
@Author  :   Yixing Lu
@Time    :   2021/04/12 15:59:49
@Software : VS Code
'''

from cv2 import cv2
import numpy as np

def derive_graym(impath):
    ''' The intensity value m is calculated as (r+g+b)/3, yet 
        grayscalse will do same operation!
        opencv uses default formula Y = 0.299 R + 0.587 G + 0.114 B
    '''
    # return cv2.imread(impath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    return cv2.imread(impath, cv2.IMREAD_GRAYSCALE)

def derive_m(img, rimg):
    ''' Derive m (intensity) based on paper formula '''

    (rw, cl, _) = img.shape
    for r in range(rw):
        for c in range(cl):
            rimg[r,c] = int(np.sum(img[r,c])/3.0)
            
    return rimg

def derive_saturation(img, rimg):
    ''' Derive staturation value for a pixel based on paper formula '''

    s_img = np.array(rimg)
    (r, c) = s_img.shape
    for ri in range(r):
        for ci in range(c):
            #opencv ==> b,g,r order
            s1 = int(img[ri,ci][0]) + int(img[ri,ci][2])
            s2 = 2 * img[ri,ci][1] 
            if  s1 >=  s2:
                s_img[ri,ci] = 1.5 * ((int(img[ri,ci][2]) - int(rimg[ri,ci])))
            else:
                s_img[ri,ci] = 1.5 * ((int(rimg[ri,ci]) - int(img[ri,ci][0])))
    return s_img

def check_pixel_specularity(mimg, simg):
    ''' Check whether a pixel is part of specular region or not'''
    (rw, cl) = simg.shape
    w_index = list(range(int(0.75*rw), rw))
    m_max = np.max(mimg[w_index,:]) * 0.6
    s_max = np.max(simg[w_index, :]) * 0.33
    # initialize all pixels as black
    spec_mask = np.zeros((rw,cl), dtype=np.uint8)
    # The pixel becomes white if it is specularity
    for r in w_index:
        for c in range(cl):
            if mimg[r,c] >= m_max and simg[r,c] <= s_max:
                spec_mask[r,c] = 255
    
    return spec_mask

def enlarge_specularity(spec_mask):
    ''' Use sliding window technique to enlarge specularity
        simply move window over the image if specular pixel detected
        mark center pixel is specular
        win_size = 3x3, step_size = 1
    '''

    win_size, step_size = (3,3), 1
    enlarged_spec = np.array(spec_mask)
    for r in range(0, spec_mask.shape[0], step_size):
        for c in range(0, spec_mask.shape[1], step_size):
            # yield the current window
            win = spec_mask[r:r + win_size[1], c:c + win_size[0]]
            
            if win.shape[0] == win_size[0] and win.shape[1] == win_size[1]:
                if win[1,1] !=0:
                    enlarged_spec[r:r + win_size[1], c:c + win_size[0]] = 255 * np.ones((3,3), dtype=np.uint8)

    return enlarged_spec