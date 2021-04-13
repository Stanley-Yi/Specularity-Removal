# -*- encoding: utf-8 -*-
'''
@File    :   video.py
@Author  :   Yixing Lu
@Time    :   2021/04/12 16:00:12
@Software : VS Code
'''


import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import cv2
from processing import processing
 
# read video file
cap = cv2.VideoCapture('ch01.avi')
 
# write video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
 
while(cap.isOpened()):
    ret, frame = cap.read()				    #捕获一帧图像
    if ret==True:
        frame = processing(frame)			# process the img
        out.write(frame)					# store the frame
        # cv2.imshow('frame',frame)  		    # display it
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    else:
        break
 
cap.release()     #close camera
out.release()
cv2.destroyAllWindows()