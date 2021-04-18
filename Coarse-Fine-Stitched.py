# -*- encoding: utf-8 -*-
'''
@File    :   Coarse-Fine-Stitched.py
@Author  :   Yixing Lu
@Time    :   2021/04/14 16:25:05
@Software : VS Code
'''

'''
framework
1. line_detect: obtain all the lines of the image and put them into a pool

2. validation: eliminate lines which do not satisfy certain conditions from the pool

3. stitch: stitch these horizon lines
'''

import cv2
import numpy as np
import os
from pylsd import lsd

def read_img(fpath):
    '''
    read the given image and parse it into a matrix

    Parameters

    fpath - the path of your image

    Return:

    img - the matrix of the given image
    '''
    img = cv2.imread(fpath, cv2.IMREAD_COLOR)
    return img


def line_detect(src):
    '''
    detect lines in a given image

    Parameters:

    fpath - the path of your image

    Return:

    properties of detected lines
    '''

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    lines = lsd.lsd(gray)
    # drop the last column
    lines = np.delete(lines, -1, 1)
    '''
    (lines[i, 0], lines[i, 1]): starting point of the line
    (lines[i, 2], lines[i, 3]): ending point of the line
    '''
    return lines


def morphology_filter(lines, beta_max):
    '''
    obtain lines which are approximately horizon

    Parameters:

    lines: include the starting point and ending point of lines

    beta_max: threshold for filtering the lines (the maximum roll angle of USV)

    Return: 
    
    filtered lines
    '''
    # transpose the line matrix
    lines = lines.transpose()
    # compute the scope of each line
    lines_scope = [(lines[3] - lines[1]) / (lines[2] - lines[0])]
    # compute the angle of each line
    line_angle = np.arctan(lines_scope).squeeze()
    # select the lines which satisfy the condition
    threshold = np.deg2rad(beta_max) # degree -> radian
    index = np.where(np.abs(line_angle)<threshold)
    # obtain filtered lines
    res = lines.T[index]
    return res
    

def color_filter(src, lines, t1, t2, t3):
    '''
    filter the lines according to color features
    
    Parameters: 

    src: the given image

    lines: include the starting point and ending point of lines

    t1, t2, t3: thresholds

    Return:

    filtered lines
    '''
    
    pass



if __name__ == '__main__':
    image = read_img('1.png')
    lines = line_detect(image)