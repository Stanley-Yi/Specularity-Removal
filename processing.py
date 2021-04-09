# Detection and removal based on study [1].
# Note that notations (r_, m_, s_) are adapted from the paper.
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