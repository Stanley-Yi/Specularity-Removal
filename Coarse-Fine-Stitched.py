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

2. validation: eliminate the non-horizon lines from the pool

3. stitch: stitch these horizon lines
'''

import cv2
import numpy as np
import os
from pylsd import lsd

def line_detect(fpath):
    '''
    detect lines in a given image

    Parameters:
    fpath - the path of your image

    Return:
    a image with line marks
    '''

    fullName = fpath
    folder, imgName = os.path.split(fullName)
    src = cv2.imread(fullName, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    lines = lsd.lsd(gray)
    for i in range(lines.shape[0]):
        pt1 = (int(lines[i, 0]), int(lines[i, 1]))
        pt2 = (int(lines[i, 2]), int(lines[i, 3]))
        width = lines[i, 4]
        cv2.line(src, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2)))
    return src


cv2.imshow('image', line_detect('house.png'))
cv2.waitKey(0)
cv2.destroyAllWindows()
