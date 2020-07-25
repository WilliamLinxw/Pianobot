# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import time
from midi_parse import get_notes_list,get_hand_key_group,get_notes_hand_key_group,get_note_handid_mat
from piano_config import config
from piano_match import PianoLoacal
from piano_std import GetStdPiano
from T_arm import T_Cam2Arm
from XarmControl import XarmControl
from mid_tune import mid_tune, mid_tune_2,get_arm_finger,get_arm_finger_V2,get_finger
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
    # 　从mid文件中获取音符序列，1倍速
    notes_time_list = get_notes_list(filepath = "template/"+mid_name, r=1,track=0, diffnum = 24,t1 = 0,t2=32)
    # mid_name = "yyjjxq.mid"
    # notes_time_list = get_notes_list(filepath = "template/yyjjxq.mid", r=1,track=0, diffnum = 0,t1 = 0,t2=15)
    # notes_time_list = get_notes_list(filepath = "template/欢乐颂2.mid", r=1,track=0, diffnum = 12,t1 = 0,t2=25)
    # notes_time_list = get_notes_list(filepath = "template/中国解放军进行曲_单钢琴.mid", r=1,track=0, diffnum = 0,t1 = 0,t2=20)
    # notes_time_list = get_notes_list(filepath = "template/茉莉花.mid", r=1,track=0, diffnum = 1,t1 = 0,t2=30)
    # notes_time_list = get_notes_list(filepath = "template/超级玛丽.mid", r=1,track=0, diffnum = 0,t1 = 0,t2=10)

    # 钢琴按键范围
    piano_key = [60,62,64,65,67,69,71,
                 72,74,76,77,79,81,83,
                 84,86,88,89,91,93,95]
    finger_num = 5
    # 钢琴按键所有手掌位置
    hand_key_group = get_hand_key_group(finger_num,piano_key)
    # 获取每个音符对应的可能的手掌位置
    hand_id = get_notes_hand_key_group(notes_time_list,hand_key_group)
    # 求多个音符手掌位置的交集，当交集为空的时候，前一个交集不为空的手掌位置，作为这些音符对应的手掌位置
    note_hand = get_note_handid_mat(piano_key,finger_num,hand_id)
    
    # 获取手掌位置变化的几个位置
    hand_pos = []
    hand_pos.append(note_hand[0][1])
    for hd in note_hand:
        if hd[1]!=hand_pos[-1]:
            hand_pos.append(hd[1])
    print('hand_pos:',hand_pos)
    
    # 获取不同位置的手指对应的琴键
    hand_pos_fg = []
    for i in hand_pos:
        hand_pos_fg.append(hand_key_group[i])
    
    print('手掌位置对应钢琴键:',hand_pos_fg,len(hand_pos_fg))

    # for i in range(len(notes_time_list)):
        # print(notes_time_list[i],"~~~~~~~~~~~~",i)
    # notes_time_list,switch_time = mid_tune(mid_name,notes_time_list)  #按手在不同位置时,手指对应的琴键编码
    # print(notes_time_list)
    # exit(0)
    # finger_mat_list = get_arm_finger(notes_time_list,switch_time)
    # for i in range(len(finger_mat_list)):
    #     print("=======================i",i,len(finger_mat_list[i]) )
    #     for sf in finger_mat_list[i]:
    #         print(sf)

    #　将整段音符序列，按照手掌位置分割为不同段落
    notes_time_list = mid_tune_2(note_hand,hand_pos_fg,notes_time_list)     
    Tcam2arm = T_Cam2Arm()
    print("################################",len(notes_time_list),len(hand_pos_fg))

    piano_loc = PianoLoacal()
    piano_std = GetStdPiano()
    cap = cv2.VideoCapture(2)
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
        
        # 返回键盘四个角的位置，用于定位两个八度的键盘
        pos = piano_loc.get_image_callback(img)
        if not pos is None:
            pos = pos.reshape([4,2]).astype('int32')
            pos = mean_value.buff_mean(pos)
            img,keypoint = piano_std.get_std_piano(img,pos) 
            for i in range(4):
                img = cv2.circle(img,(pos[i,0],pos[i,1]),5,(0,0,255),-1)
        cv2.imshow('Labeling', img)

        # 按下Y键开始弹琴
        keyval = cv2.waitKey(10)
        if  keyval == ord('y'):

            break
        if  keyval == ord('c'):
            # 将钢琴上音符位置与对应的机械臂坐标
            key_pos, note_number = keypoint 
            arm_pos = Tcam2arm.T_img2arm_points(key_pos)

            save_path = 'key_pos'
            np.savez(save_path,key_pos=key_pos,arm_pos=arm_pos) 
            
            note2arm = dict(zip(note_number,arm_pos))
            hand_pos_fg_f1 = []
            for fg_id in hand_pos_fg:
                hand_pos_fg_f1.append([fg_id[1], note2arm[fg_id[1]]]) #食指位置
            # 机械臂按照顺序移动到几个手掌位置，并统计移动时间，保存移动时间
            arm.get_cost_time(hand_pos_fg_f1)
    
    # 将钢琴上音符位置与对应的机械臂坐标
    key_pos, note_number = keypoint 
    arm_pos = Tcam2arm.T_img2arm_points(key_pos)

    npz = np.load('key_pos.npz')   
    key_pos= npz['key_pos']  
    arm_pos=npz['arm_pos']  
    
    note2arm = dict(zip(note_number,arm_pos))
    
    # 获取每个手掌位置期间　手指运动的序列
    finger_mat_list = get_arm_finger_V2(notes_time_list,hand_pos_fg)
    # for i in range(len(finger_mat_list)):
    #     print("=========指法序列==============i",i,len(finger_mat_list[i]) )
    #     for sf in finger_mat_list[i]:
    #         print(sf)

    # _,_,*fg = switch_time[0]
    # f1 = fg[2]#食指对应的琴键
    
    # 手掌移动位置对应食指所在位置
    hand_pos_fg_f1 = []
    for fg_id in hand_pos_fg:
        hand_pos_fg_f1.append([fg_id[1], note2arm[fg_id[1]]]) #食指位置
    
    key_id,pos = hand_pos_fg_f1[0]# 第一个手掌所在位置－食指所在位置
    f1_pos = pos
    arm.set_pos_move(f1_pos[0], f1_pos[1]) # 移动开始位置   
    while 1:
        key_id,pos = hand_pos_fg_f1[0]
        f1_pos = pos #食指对应的琴键
        # arm.set_play_pos(f1_pos[0], f1_pos[1])
        arm.set_play_pos(f1_pos[0], f1_pos[1])# 移动到弹奏高度
        time.sleep(1)
        for i in range(len(hand_pos_fg)):
            key_id,pos = hand_pos_fg_f1[i]
            f1_pos = pos #食指对应的琴键
            t11 = time.time()
            arm.set_play_pos(f1_pos[0], f1_pos[1])
            t22 = time.time()
            print("t22 - t11:",t22-t11)
            if i>=len(finger_mat_list):
                break
            finger_mat = finger_mat_list[i]
            arm.play(finger_mat,arm.hand)
        key_id,pos = hand_pos_fg_f1[0]# 第一个手掌所在位置－食指所在位置
        f1_pos = pos
        arm.set_pos_move(f1_pos[0], f1_pos[1]) # 移动开始位置 
        time.sleep(2)

        print("============================================")



