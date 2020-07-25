# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import time
from midi_parse import get_notes_list
from inspire_hand_r import InspireHandR

def get_finger(notes_time_list):
    time_step = 50
    data = np.array(notes_time_list)
    n = int(data[-1,0] / time_step)+1
    finger_mat = np.zeros([n,6])
    # 小指 无名指 中指 食指 大拇指
    # 79   77     76   74   72
    for i in range(n):
        finger_mat[i,0] = i*time_step 
    # 小指
    index = np.where(data[:,1]==79)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:
            start_id = np.where(finger_mat[:,0] == data[index[i],0] )[0][0]
            end_id = np.where(finger_mat[:,0] == data[index[i+1],0] )[0][0]
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,1] = 1
            else:
                finger_mat[start_id:end_id,1] = 0
    # 无名指    
    index = np.where(data[:,1]==77)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:
            start_id = np.where(finger_mat[:,0] == data[index[i],0] )[0][0]
            end_id = np.where(finger_mat[:,0] == data[index[i+1],0] )[0][0]
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,2] = 1
            else:
                finger_mat[start_id:end_id,2] = 0

    # 中指 
    index = np.where(data[:,1]==76)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:
            start_id = np.where(finger_mat[:,0] == data[index[i],0] )[0][0]
            end_id = np.where(finger_mat[:,0] == data[index[i+1],0] )[0][0]
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,3] = 1
            else:
                finger_mat[start_id:end_id,3] = 0
    # 食指 
    index = np.where(data[:,1]==74)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:
            start_id = np.where(finger_mat[:,0] == data[index[i],0] )[0][0]
            end_id = np.where(finger_mat[:,0] == data[index[i+1],0] )[0][0]
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,4] = 1
            else:
                finger_mat[start_id:end_id,4] = 0
    # 大拇指 
    index = np.where(data[:,1]==72)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:
            start_id = np.where(finger_mat[:,0] == data[index[i],0] )[0][0]
            end_id = np.where(finger_mat[:,0] == data[index[i+1],0] )[0][0]
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,5] = 1
            else:
                finger_mat[start_id:end_id,5] = 0
    finger_mat = finger_mat.astype('int')
    return finger_mat


def play(finger_mat,hand):
    start_time = time.time()
    index = 0
    while 1:
        time.sleep(0.001)
        curr_time = time.time()
        #  print('cost time:', (curr_time - start_time)*1000)
        if (curr_time - start_time)*1000 > finger_mat[index,0]:
            noteoff = 500
            noteon = 1200
            diffn = 200
            pos1 = hand.f1_init_pos + diffn  if finger_mat[index,1] else hand.f1_init_pos  #小拇指伸直0，弯曲2000
            pos2 = hand.f2_init_pos + diffn  if finger_mat[index,2] else hand.f2_init_pos  #无名指伸直0，弯曲2000
            pos3 = hand.f3_init_pos + diffn  if finger_mat[index,3] else hand.f3_init_pos  #中指伸直0，弯曲2000
            pos4 = hand.f4_init_pos + diffn  if finger_mat[index,4] else hand.f4_init_pos  #食指伸直0，弯曲2000
            pos5 = hand.f5_init_pos      #大拇指伸直0，弯曲2000
            pos6 = hand.f6_init_pos + 800 if finger_mat[index,5] else hand.f6_init_pos      #大拇指转向掌心 2000
            hand.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
            index = index + 1
            if index == len(finger_mat):
                print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
                hand.reset()
                time.sleep(1)
                start_time = time.time()
                index = 0

if __name__ == '__main__':
    hand = InspireHandR()
    notes_time_list = get_notes_list(filepath = "template/洋娃娃和小熊跳舞2.mid", r=1,track=1, diffnum = 0,t1 = 0,t2=9)
    for notelist in notes_time_list:
        print(notelist)
    
    #  print(notes_time_list )
    time_step = 50
    n = int(notes_time_list[-1][0] / time_step)+1
    print("n=",n)
    
    # 小指 无名指 中指 食指 大拇指
    # 79   77     76   74   72
    finger_mat  = get_finger(notes_time_list)
    for i in range(len(finger_mat)):
        print(finger_mat[i,:] )
    play(finger_mat,hand)
    hand.reset_0()
    #  while 1:
        #  for i in range(len(cmd_list)) :
            #  time.sleep(0.04)
            #  print(cmd_list[i] )
            #  noteoff = 500
            #  noteon = 1200
            #  diffn = 500
            #  pos1 = 500 + diffn  if cmd_list[i][1] else 500  #小拇指伸直0，弯曲2000
            #  pos2 = 500 + diffn  if cmd_list[i][2] else 500  #无名指伸直0，弯曲2000
            #  pos3 = 450 + diffn  if cmd_list[i][3] else 450  #中指伸直0，弯曲2000
            #  pos4 = 500 + diffn   if cmd_list[i][4] else 500  #食指伸直0，弯曲2000
            #  pos5 = 1000      #大拇指伸直0，弯曲2000
            #  pos6 = 2000  if cmd_list[i][5] else 500      #大拇指转向掌心 2000
            #  hand.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
#
    # hand.reset()
#
#






    










