import numpy as np
import time
import cv2
import os,sys

class GetStdPiano(object):
    def __init__(self):
        # 初始化参数
        self.qipan_point = None
        self.g_qipan_pos = np.zeros([4,1,2])
        self.current_img = None
        self.white_key_num = 21
        self.black_key_pos_num = 20 # Virtual number of black keys, there are gaps between them
        self.notes = [60,61,62,63,64,65,66,
                      67,68,69,70,71,72,73,
                      74,75,76,77,78,79,80,
                      81,82,83,84,85,86,87,
                      88,89,90,91,92,93,94,
                      95]
        self.notes_black = [61,63,66,68,70,73,75,
                            78,80,82,85,87,90,92,
                            94]
        # self.notes = [72,74,76,77,79,81,83,
        #               84,86,88,89,91,93,95,
        #               96,98,100,101,103,105,107]#C5在最左边，一共21个白键
    def plan_line(self, img, pos):
        #画框
        img = cv2.line(img, (pos[0,0],pos[0,1]), (pos[1,0],pos[1,1]), (0, 255, 0)) #左上角到右上角,琴盘底部,白键
        img = cv2.line(img, (pos[2,0],pos[2,1]), (pos[3,0],pos[3,1]), (0, 255, 0)) #左下角到右下角，琴盘顶部
        img = cv2.line(img, (pos[0,0],pos[0,1]), (pos[2,0],pos[2,1]), (0, 255, 0)) #左上角到左下角,琴盘右边
        img = cv2.line(img, (pos[1,0],pos[1,1]), (pos[3,0],pos[3,1]), (0, 255, 0)) #右上角到右下角,琴盘左边
        return img
    
    def get_key_pos(self, img, pos):
        w = 640
        h = 240  #554
        da = 0
        thda = (h-2*da)/4.
        twda = (w-2*da)/3.

        # 将实际图片中的棋盘抠出,并变形为矩形
        dst_temp = np.float32([[0, 0], 
                               [w, 0], 
                               [0, h],
                               [w, h]])
        src_temp = pos.reshape([4,1,2]).astype('float32')
        # 生成透视变换矩阵
        M = cv2.getPerspectiveTransform(src_temp, dst_temp)
        # 进行透视变换
        img2_std = cv2.warpPerspective(img, M, (w, h))
        
        
        #  lu_point = pos[0]
        #  ru_point = pos[1]
        #  ld_point = pos[2]
        #  rd_point = pos[3]
        lu_point =[0,0] 
        ru_point = [w, 0]
        ld_point = [0, h]
        rd_point = [w, h] 

        # 将得到的矩形图像水平和竖直等分
        linenum = 15
        y_ma_l = (ld_point[1] - lu_point[1]) * 1.0 / (linenum - 1)
        x_ma_l = (ld_point[0] - lu_point[0]) * 1.0 / (linenum - 1)
        y_ma_r = (rd_point[1] - ru_point[1]) * 1.0 / (linenum - 1)
        x_ma_r = (rd_point[0] - ru_point[0]) * 1.0 / (linenum - 1)
        h_line = []
        for i in range(linenum):
            x_h_l = lu_point[0] + int(i * x_ma_l)
            y_h_l = lu_point[1] + int(i * y_ma_l)
            x_h_r = ru_point[0] + int(i * x_ma_r)
            y_h_r = ru_point[1] + int(i * y_ma_r)
            h_line.append([np.array([x_h_l,y_h_l]),np.array([x_h_r,y_h_r])])
        i = 1
        white_pos_line = h_line[i]
        dy_white = abs((white_pos_line[0][1] - white_pos_line[1][1])/self.white_key_num)
        dx_white = abs((white_pos_line[0][0] - white_pos_line[1][0])/self.white_key_num)
        img2_std = cv2.line(img2_std, tuple(white_pos_line[0]), tuple(white_pos_line[1]), (0,255,0), 1, 4)
        
        # 生成白健的位置并显示在矩形图像中
        key_pos_white = []
        key_pos_white_2 = []
        start_pos_white = white_pos_line[1]
        for i in range(self.white_key_num):
            key_pos_white.append([start_pos_white[0]-dx_white*i - dx_white*0.5 ,start_pos_white[1]-dy_white*i-0 ])
            key_pos_white_2.append([start_pos_white[0]-dx_white*i - dx_white*0.5 ,start_pos_white[1]-dy_white*i+10 ])
            # print(key_pos[i])
            img2_std = cv2.circle(img2_std, (int(key_pos_white_2[i][0]) ,int(key_pos_white_2[i][1])), 5, (255,0,255), -1)

        # 生成黑键的位置并显示在矩形图像中，黑键位置定义为两个白键之间
        # 第一个for循环删去了可能有的两个黑键之间的间隔，第二个for循环将其位置显示在画面中用于后续的坐标变换
        key_pos_black = []
        black_pos_line = h_line[7]
        img2_std = cv2.line(img2_std, tuple(black_pos_line[0]), tuple(black_pos_line[1]), (0,255,0), 1, 4)
        dy_black = abs((black_pos_line[0][1] - black_pos_line[1][1])/self.black_key_pos_num)
        start_pos_black = black_pos_line[1]
        for i in range(self.black_key_pos_num):
            if i==2 or i==6 or i==9 or i==13 or i==16:
                continue
            else:
                key_pos_black.append([(int(key_pos_white_2[i][0])+int(key_pos_white_2[i+1][0]))/2, start_pos_black[1] - dy_black*i])
        for i in range(len(key_pos_black)):
            img2_std = cv2.circle(img2_std, (int(key_pos_black[i][0]), int(key_pos_black[i][1])), 5, (255,0,255), -1)

        # Merge the black key list and white key list
        key_position_total = key_pos_white_2 + key_pos_black

        # Sort the key to make sure the key's sequence is right
        key_position_total.sort(reverse=True)

        # Map the key positions in the rectangular frame back to the camera frame
        M_inv = np.linalg.pinv(M)
        pts_s = np.float32(key_position_total).reshape(-1, 1, 2)
        cam_s_pos = cv2.perspectiveTransform(pts_s, M_inv)
        cam_s_pos = cam_s_pos.reshape([-1, 2])
        for i in range(len(key_position_total)):
            img = cv2.circle(img, (int(cam_s_pos[i,0]) ,int(cam_s_pos[i,1]) ), 5, (255, 0, 255), -1)


        # # 将得到的黑白键坐标映射回相机坐标系
        # # 映射白键
        # M_inv_white = np.linalg.pinv(M)
        # pts_s_white = np.float32(key_pos_white_2).reshape(-1, 1, 2)
        # cam_s_pos_white = cv2.perspectiveTransform(pts_s_white, M_inv_white) # 相机坐标下位置
        # cam_s_pos_white = cam_s_pos_white.reshape([-1, 2])
        # for i in range(self.white_key_num):
        #     img = cv2.circle(img, (int(cam_s_pos_white[i,0]) ,int(cam_s_pos_white[i,1]) ), 5, (255, 0, 255), -1)
        # # 映射黑键
        # M_inv_black = np.linalg.pinv(M)
        # pts_s_black = np.float32(key_pos_black).reshape(-1, 1, 2)
        # cam_s_pos_black = cv2.perspectiveTransform(pts_s_black, M_inv_black)
        # cam_s_pos_black = cam_s_pos_black.reshape([-1, 2])
        # for i in range(len(key_pos_black)):
        #     img = cv2.circle(img, (int(cam_s_pos_black[i,0]) ,int(cam_s_pos_black[i,1]) ), 5, (255, 0, 255), -1)
        
        keypos = [cam_s_pos, self.notes]
        cv2.imshow("std_piano",img2_std)
        cv2.imshow('img1', img) 

        return img, keypos


    def get_std_piano(self,img,pos):
        img = self.plan_line(img, pos)
        # 计算琴格中点位置
        img,key_pos = self.get_key_pos(img, pos)
        return img,key_pos















