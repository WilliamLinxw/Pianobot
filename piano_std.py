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
        self.notes_black = [61,63,66,68,70,
                            73,75,78,80,82,
                            85,87,90,92,94]

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
        
        # 生成白健的位置并显示在矩形图像中，其中 key_pos_white 为映射所用坐标，2为矩形画面中画图所需坐标
        key_pos_white = []
        key_pos_white_2 = []
        start_pos_white = white_pos_line[1]
        for i in range(self.white_key_num):
            key_pos_white.append([start_pos_white[0]-dx_white*i - dx_white*0.5 ,start_pos_white[1]-dy_white*i-100])
            key_pos_white_2.append([start_pos_white[0]-dx_white*i - dx_white*0.5 ,start_pos_white[1]-dy_white*i+10])
            # print(key_pos[i])
            img2_std = cv2.circle(img2_std, (int(key_pos_white_2[i][0]) ,int(key_pos_white_2[i][1])), 5, (255,0,255), -1)

        # 生成黑键的位置并显示在矩形图像中，黑键位置定义为两个白键之间
        # 第一个for循环删去了可能有的两个黑键之间的间隔，第二个for循环将其位置显示在画面中用于后续的坐标变换
        # 其中 key_pos_black 为映射所用坐标，2为矩形画面中画图所需坐标
        key_pos_black = []
        key_pos_black_2 = []
        black_pos_line = h_line[7]
        img2_std = cv2.line(img2_std, tuple(black_pos_line[0]), tuple(black_pos_line[1]), (0,255,0), 1, 4)
        dy_black = abs((black_pos_line[0][1] - black_pos_line[1][1])/self.black_key_pos_num)
        start_pos_black = black_pos_line[1]
        for i in range(self.black_key_pos_num):
            if i==2 or i==6 or i==9 or i==13 or i==16:
                continue
            else:
                key_pos_black.append([(int(key_pos_white[i][0])+int(key_pos_white[i+1][0]))/2, start_pos_black[1] - dy_black*i - 180])
                key_pos_black_2.append([(int(key_pos_white_2[i][0])+int(key_pos_white_2[i+1][0]))/2, start_pos_black[1] - dy_black*i ])
                
        # 实际上黑键并不在两个白键的正中间，加入偏移从而使黑键的定位更精确，第一部分对矩形画面进行处理，第二部分对需要映射的画面进行处理
        key_pos_black[0][0] += 5
        key_pos_black[2][0] += 8
        key_pos_black[3][0] += 2
        key_pos_black[5][0] += 5
        key_pos_black[7][0] += 8
        key_pos_black[8][0] += 2
        key_pos_black[9][0] -= 3
        key_pos_black[10][0] += 3
        key_pos_black[11][0] -= 2
        key_pos_black[12][0] += 3
        key_pos_black[14][0] -= 6

        key_pos_black_2[0][0] += 5
        key_pos_black_2[2][0] += 8
        key_pos_black_2[3][0] += 2
        key_pos_black_2[5][0] += 5
        key_pos_black_2[7][0] += 8
        key_pos_black_2[8][0] += 2
        key_pos_black_2[9][0] -= 3
        key_pos_black_2[10][0] += 3
        key_pos_black_2[11][0] -= 2
        key_pos_black_2[12][0] += 3
        key_pos_black_2[14][0] -= 6

        for i in range(len(key_pos_black_2)):
            img2_std = cv2.circle(img2_std, (int(key_pos_black_2[i][0]), int(key_pos_black_2[i][1])), 5, (255,0,255), -1)
        cv2.imshow("std_piano",img2_std)

        # 合并黑键白键列表
        key_position_total = key_pos_white + key_pos_black

        # 按照横坐标大小对黑白键进行排序，以对应音符
        key_position_total.sort(reverse=True)

        # 将黑白键的定位从矩形画面映射回相机实际画面
        M_inv = np.linalg.pinv(M)
        pts_s = np.float32(key_position_total).reshape(-1, 1, 2)
        cam_s_pos = cv2.perspectiveTransform(pts_s, M_inv)
        cam_s_pos = cam_s_pos.reshape([-1, 2])
        for i in range(len(key_position_total)):
            img = cv2.circle(img, (int(cam_s_pos[i,0]) ,int(cam_s_pos[i,1]) ), 5, (255, 0, 255), -1)
        
        # 将琴键位置与音符一一对应
        keypos = [cam_s_pos, self.notes]
        return img, keypos


    def get_std_piano(self,img,pos):
        img = self.plan_line(img, pos)
        # 计算琴格中点位置
        img,key_pos = self.get_key_pos(img, pos)
        return img,key_pos















