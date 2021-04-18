# -*- encoding: utf-8 -*-
'''
@File    :   processing.py
@Author  :   Yixing Lu
@Time    :   2021/04/12 16:00:31
@Software : VS Code
'''

import cv2
import numpy as np
import specularity as spc
  
def processing(img):
    img = cv2.resize(img, (640, 480))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.resize(gray_img, (640, 480))
    r_img = m_img = np.array(gray_img)
    rimg = spc.derive_m(img, r_img)
    s_img = spc.derive_saturation(img, rimg)
    spec_mask = spc.check_pixel_specularity(rimg, s_img)
    enlarged_spec = spc.enlarge_specularity(spec_mask)

    # use opencv's inpaint methods to remove specularity
    radius = 12
    # two inpaint（修补） methods
    telea = cv2.inpaint(img, enlarged_spec, radius, cv2.INPAINT_TELEA)
    # ns = cv2.inpaint(img, enlarged_spec, radius, cv2.INPAINT_NS)
    # cv2.imwrite('figs/Impainted_telea.png',telea)
    # cv2.imwrite('figs/Impainted_ns.png',ns)
    return telea

if __name__ == '__main__':
    img = cv2.imread('1.png')
    res = processing(img)
    cv2.imshow('image', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()