# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import time
from midi_parse import get_notes_list
from piano_config import config
from piano_match import PianoLoacal
from piano_std import GetStdPiano
from T_arm import T_Cam2Arm
from XarmControl import XarmControl
from mid_tune import mid_tune,get_arm_finger,get_finger
class MeanValue(object):
    def __init__(self,init_value,type_str = "float32",size=5):
        self.sh = list(init_value.shape)+[size]
        self.buff = np.zeros(self.sh)
        self.count = 0
        self.size = size
        self.type_str = type_str
    def buff_mean(self,value):
        self.count = self.count+1
        if self.count ==self.size:
            self.count = 0
        self.buff[...,self.count] = value
        mean_value =np.mean(self.buff,axis=len(self.sh)-1) 
        mean_value =mean_value.astype(self.type_str)
        return mean_value


if __name__ == '__main__':

    arm = XarmControl()
    mean_value = MeanValue(np.ones([4,2]),"int32")
    #  notes_time_list = get_notes_list(filepath = "template/小星星2.mid", r=1.3)
    # notes_time_list = get_notes_list(filepath = "template/天空之城.mid", r=1,track=0, diffnum = 12,t1 = 0,t2=30)
    #  notes_time_list = get_notes_list(filepath = "template/致爱丽丝.mid", r=1,track=2, diffnum = -12)
    #  notes_time_list = get_notes_list(filepath = "template/summer.mid", r=2,track=1, diffnum = -12)
    # mid_name = "洋娃娃和小熊跳舞2.mid"
    # notes_time_list = get_notes_list(filepath = "template/"+mid_name, r=1,track=1, diffnum = 0,t1 = 0,t2=28.8)
    mid_name = "天空之城.mid"
    notes_time_list = get_notes_list(filepath = "template/"+mid_name, r=3,track=0, diffnum = 24,t1 = 0,t2=8)
    for i in range(len(notes_time_list)):
        print(notes_time_list[i],"~~~~~~~~~~~~",i)
    notes_time_list,switch_time = mid_tune(mid_name,notes_time_list)  #按手在不同位置时,手指对应的琴键编码
    # print(notes_time_list)
    # exit(0)
    finger_mat_list = get_arm_finger(notes_time_list,switch_time)
    for i in range(len(finger_mat_list)):
        print("=======================i",i,len(finger_mat_list[i]) )
        for sf in finger_mat_list[i]:
            print(sf)
    # exit()
    
    Tcam2arm = T_Cam2Arm()

    piano_loc = PianoLoacal()
    piano_std = GetStdPiano()
    cap = cv2.VideoCapture(8)
    cap.set(4, 720)
    cap.set(3, 1280)    
    
    newimg = 0

    while (True): 
        ret, img = cap.read()  # 捕获一帧图像
        img_shape = img.shape
        #  print("img_shape:",img_shape)
        x_de =int( (img_shape[1] - config.h)/2 )
        y_de = int((img_shape[0] - config.w)/2)
        img = img[-config.w: ,x_de:x_de+config.h,:]
        
        pos = piano_loc.get_image_callback(img)
        if not pos is None:
            pos = pos.reshape([4,2]).astype('int32')
            pos = mean_value.buff_mean(pos)
            img,keypoint = piano_std.get_std_piano(img,pos) 
            for i in range(4):
                img = cv2.circle(img,(pos[i,0],pos[i,1]),5,(0,0,255),-1)
        cv2.imshow('Labeling', img)
        # 按下Y键开始弹琴
        if cv2.waitKey(1) & 0xFF == ord('y'):
            break
    
    # 将钢琴上音符位置与对应的机械臂坐标
    key_pos, note_number = keypoint 
    arm_pos = Tcam2arm.T_img2arm_points(key_pos)
    note2arm = dict(zip(note_number,arm_pos))
    
    #将mid音符序列转为机械臂坐标序列
    print("note2arm", note2arm)
    midi_arm_time = []
    for tick,note,down in notes_time_list:
        if down == 1 and (note in piano_std.notes) : 
            armpos = note2arm[note]
            midi_arm_time.append([tick,armpos[0], armpos[1]])
    midi_arm_time = np.array(midi_arm_time)
    print("时序坐标", midi_arm_time)
    
    _,_,*fg = switch_time[0]
    f1 = fg[2]#食指对应的琴键
    f1_pos = note2arm[f1]
    arm.set_pos_move(f1_pos[0], f1_pos[1])   
    while 1:
        _,_,*fg = switch_time[0]
        f1 = fg[2]#食指对应的琴键
        f1_pos = note2arm[f1]
        # arm.set_play_pos(f1_pos[0], f1_pos[1])
        arm.set_play_pos(f1_pos[0], f1_pos[1],wait=True,timeout=2)

        for i in range(len(switch_time)):
        # for i in range(2):
            _,_,*fg = switch_time[i]
            f1 = fg[2]#食指对应的琴键
            f1_pos = note2arm[f1]
            t11 = time.time()
            arm.set_play_pos(f1_pos[0], f1_pos[1],wait=True,timeout=2)
            t22 = time.time()
            print("t22 - t11:",t22-t11)
            if i>=len(finger_mat_list):
                break
            finger_mat = finger_mat_list[i]
            arm.play(finger_mat,arm.hand)

    if 1:    
        while (True):
            ret, img = cap.read()  # 捕获一帧图像
            img_shape = img.shape
            #  print("img_shape:",img_shape)
            x_de =int( (img_shape[1] - config.h)/2 )
            y_de = int((img_shape[0] - config.w)/2)
            img = img[-config.w: ,x_de:x_de+config.h,:]
            img,keypoint = piano_std.get_std_piano(img,pos) 
            cv2.imshow('Labeling', img)
            cv2.waitKey(1)






