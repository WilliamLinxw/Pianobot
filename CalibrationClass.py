#!/usr/bin/env python3
#!coding=utf-8
import logging
import numpy as np
import cv2
import cv2.aruco as aruco
import signal
import os,sys,math,time
USE_XARM = 1
if USE_XARM:
    from XarmControl import XarmControl
    
class CalibrationClass(object):
    def __init__(self):
        self.calib_point=[]
        self.img_point=[]
        self.laser_maker=[]
        self.id = []

        self.all_calib_point=[]  #机械臂末端坐标
        self.all_img_point=[]    #图像检测到的末端位置
        self.all_laser_maker=[]
        self.all_id = []
        self.save_dir = './template/'

        self.img_shape =[720,1280] 
        self.y_de = int((self.img_shape[0]-720)/2)
        self.x_de = int((self.img_shape[1]-960)/2)

        if USE_XARM:
            self.arm = XarmControl()
            self.xx_init = 300
            self.yy_init = 64
            self.zz_init = -10
            move_comd = [self.xx_init,self.yy_init,self.zz_init]
            self.pub_uarm_move(move_comd)
        else:
            self.xx_init = 422
            self.yy_init = 64
            self.zz_init = -10

        x_r = [1,2,3,4]
        y_r =[0,1,2,3,4,5]
        # y_r =[0]
        z_r = [0]
        for y in y_r :
            for x in x_r :
                if y==1 and x==0:
                    continue
                for z in z_r:
                    xx = self.xx_init + x*60
                    yy = self.yy_init + y*60
                    zz = self.zz_init + z*50
                    self.calib_point.append([xx,yy,zz])

        self.curr_time = time.time()+5
        self.curr_id = 0
        self.M = None

        self.start_num = 0
        self.start = False
        self.end = False

        self.parameters = aruco.DetectorParameters_create()

   
    def pub_uarm_move(self,move_comd):
        #  move_comd = [100,100,-1,-1]
        dst = np.array(move_comd)
        # new_dst = dst.reshape([1,-1])[0].astype('float')
        print(move_comd)
        if USE_XARM:
            x = move_comd[0]
            y = move_comd[1]
            z = move_comd[2]
            self.arm.set_pos(x,y,z,False)


    def get_mark_pos(self, image):
        gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 选择aruco模块中预定义的字典来创建一个字典对象
        # 这个字典是由250个marker组成的，每个marker的大小为5*5bits
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        #检测出的图像的角的列表（按照原始顺序排列的四个角（从左上角顺时针开始）），检测出的所有maker的id列表
        corners, ids, _ = aruco.detectMarkers(gray2, aruco_dict, parameters = self.parameters)
        if len(corners)==0:
            return [],[]
        corner_center_pos = []
        corner_ids = []
        
        for id,ii in enumerate(ids):
            single_corners = corners[id]
            center_pos = np.mean(single_corners.reshape([4,2]),axis=0).astype("int")
            corner_center_pos.append(center_pos)
            corner_ids.append(ii)

        return [corner_center_pos,corner_ids]   

    
    def get_mark_pos_v2(self,img2):
        '''通过公众号二维码外边框定位'''
        lower_blue = np.array([100, 110, 110])
        upper_blue = np.array([130, 255, 255])
        hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        img_b = cv2.inRange(hsv, lower_blue, upper_blue)
        kernel = np.ones((3,3),np.uint8)  
        # img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        # ret,img =cv2.threshold(img,thresh,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)  
        # img = cv2.erode(img,kernel,1)
        center_pos = []
        _,contours,hierachy=cv2.findContours(img_b,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i,cnt in enumerate(contours):
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and cv2.isContourConvex(cnt):
                # print('!!!!i, cv2.contourArea(cnt):',i, cv2.contourArea(cnt))
                if cv2.contourArea(cnt)>1500 and cv2.contourArea(cnt)<5000: 
                    cnt = cnt.reshape(-1, 2)
                    # max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    # print(cnt)
                    center_pos.append(np.mean(cnt,axis=0))
                    cv2.drawContours(img2, [cnt], -1, (0, 255, 0), 2)

        # print('center_pos:',center_pos)
        if len(center_pos) != 0:
            center_pos = np.array(center_pos)
            center_pos = np.mean(center_pos,axis=0).astype('int')
            img2 = cv2.circle(img2,(center_pos[0],center_pos[1]),10,(0,0,255),-1)

            cv2.imshow('test2',img2)
            cv2.waitKey(1)


            return [center_pos],[0]
        else:
            cv2.imshow('test2',img2)
            cv2.waitKey(1)
            return [],[]

    
    def run(self,img):

        # ret, img = self.cap.read()  # 捕获一帧图像
        # img_shape = img.shape
        # print("img_shape:",img.shape)

        dep = None
        if img is None:
            return None
        
        img = img[self.y_de:self.y_de+720,self.x_de:self.x_de+960,:] 

        img_0 = img.copy()
        while(1): #该循环只执行一次
            img2 = img.copy()
            new_point = np.zeros([4,2])
            img2_line = img2
        
            # 获取机械臂末端位置
            # corner_center_pos, ids = self.get_mark_pos(img)  
            corner_center_pos, ids = self.get_mark_pos_v2(img)  

            armimg_pos = None
            if (corner_center_pos == [])  :
                print("未找到机械臂末端标记！")
                return img_0
            else:
                # print("corner_center_pos:",corner_center_pos)
                armimg_pos = corner_center_pos[0]
                img_0 = cv2.circle(img_0, (armimg_pos[0], armimg_pos[1]), 8, (0,0 ,255), -1)
                img_0 = cv2.putText(img_0, "%d"%ids[0], (armimg_pos[0], armimg_pos[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0,0), 2)

            
            keyval = cv2.waitKey(50)
            #  print('keyval:',keyval)
            if  keyval == ord('s'): #触发开始标记
                self.start = True
                self.start_num += 1
            
            if  keyval == ord('e'): # 触发结束标记
                self.end = True
        
            # 每隔5秒保存机械臂末端位置
            curr_time = time.time()
            if curr_time - self.curr_time > 5:#每隔5秒触发一次末端检测
                if (armimg_pos is None) or(new_point == []):# 确保能够同时检测到激光和机械臂末端标记
                    print('xxxxxx')
                    break
                
                if self.start == False and self.end == False:
                    print("按下s键开始采集数据")
                    break

                if self.end == True:#检测到结束标记,自动保存数据
                    calib_point = np.array(self.all_calib_point) 
                    laser_maker = np.array(self.all_laser_maker)
                    img_maker = np.array(self.all_img_point)
                    arm_id = np.array(self.all_id)
                    
                    print('calib_point :', calib_point.shape,"\n",calib_point) 
                    print('laser_maker:',laser_maker.shape,"\n",laser_maker)
                    print('img_maker :', img_maker.shape,"\n",img_maker) 
                    print('arm_id:',arm_id.shape,"\n",arm_id)

                    save_path = self.save_dir + 'arm_cali'
                    np.savez(save_path,calib_point=calib_point,laser_point=laser_maker,img_point=img_maker, arm_id =arm_id) 
                    print("第{}次标定数据采集完成！！".format(self.start_num))
                    exit(0)

                self.curr_time = curr_time
                print('calib_point: ',len(self.calib_point),self.curr_id)
                
                if self.curr_id>0 and self.curr_id < len(self.calib_point)+1: #记录前一步机械臂在相机下的移动位置
                    
                    self.img_point.append(armimg_pos)
                    marker_pos = new_point.reshape([1,-1])
                    self.laser_maker.append(marker_pos)    
                    self.id.append(self.start_num)    

                if self.curr_id == len(self.calib_point)+1: #最后保存数据
                    move = [self.xx_init, self.yy_init, self.zz_init,-8]
                    self.pub_uarm_move(move)

                    calib_point = np.array(self.calib_point) 
                    laser_maker = np.array(self.laser_maker)
                    img_maker = np.array(self.img_point)
                    arm_id = np.array(self.id)
                    
                    self.all_calib_point += self.calib_point
                    self.all_img_point += self.img_point
                    self.all_laser_maker += self.laser_maker
                    self.all_id += self.id

                    print('calib_point :', calib_point.shape,"\n",calib_point) 
                    print('laser_maker:',laser_maker.shape,"\n",laser_maker)
                    print('img_maker :', img_maker.shape,"\n",img_maker) 
                    print('arm_id:',arm_id.shape,"\n",arm_id)
                    
                    #  self.calib_point=[]
                    self.img_point=[]
                    self.laser_maker=[]
                    self.id = []
                    self.curr_id = 0
                    self.start = False
                    print("第{}次标定数据采集完成！！".format(self.start_num))
                    move = [self.xx_init, self.yy_init, self.zz_init,1]
                    self.pub_uarm_move(move)
                
                   
                if self.curr_id == len(self.calib_point): # 机械臂恢复位置
                    self.curr_id += 1
                    move = [self.xx_init, self.yy_init, self.zz_init,1]
                    #self.pub_uarm_move(move)

                if self.curr_id < len(self.calib_point): # 让机械臂移动到指定位置
                    p = self.calib_point[self.curr_id]
                    move = [p[0],p[1],p[2],1]
                    self.curr_id += 1
                    self.pub_uarm_move(move)
            break
        return img_0
