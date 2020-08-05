import numpy as np
import cv2
import os,sys,math,time
import cv2.aruco as aruco
import time
from CalibrationClass import CalibrationClass 

def get_img2arm_T(loc_pos,mark_pos):
    loc_pos = np.array(loc_pos).reshape([4,1,2]).astype('float32')
    dst_temp = np.array( [[0,0], [0,500], [500,0], [500,500 ]] ).astype('float32')
    T_cam2loc = cv2.getPerspectiveTransform(loc_pos, dst_temp) 
    #  加载相机与机械臂标定数据
    npz = np.load("board_calib.npz")
    arm_pos = npz['mark_arm_pos'] #标定板上对应的机械臂空间的坐标 
    print('arm_pts[0]:',arm_pos[0,:])
    
    pts = mark_pos.reshape([-1,1,2]).astype('float32') #相机画面下二维码的位置
    img_pos = cv2.perspectiveTransform(pts, T_cam2loc)
    
    arm_pos = arm_pos.T
    img_pos = np.array(img_pos).reshape([-1,2]) 
    img_pos = np.hstack([img_pos,np.ones([img_pos.shape[0],1])]).T
    
    Timg2arm =np.dot(arm_pos,np.linalg.pinv(img_pos))
    #  print("T_cam2loc:",T_cam2loc.shape)
    #  print("Timg2arm:", Timg2arm.shape)
    
    return T_cam2loc, Timg2arm
 
if __name__ == "__main__":
    cali = CalibrationClass()
    cap = cv2.VideoCapture(2)
    print(cap)
    cap.set(3,1280)
    cap.set(4,720)
    while 1:
        time.sleep(0.1)
        ret, img = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('y'):
            break
        
        img = cali.run(img)
        if not img is None:
            cv2.imshow('test',img)
            cv2.waitKey(1)
