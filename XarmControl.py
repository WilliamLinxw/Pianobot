import time
from xarm.wrapper import XArmAPI
import os
import sys
import numpy as np
from inspire_hand_r import InspireHandR


class XarmControl:
    def __init__(self):
        ip = '192.168.1.217'
        self.arm = XArmAPI(ip, do_not_open=False)
        self.arm.register_error_warn_changed_callback(self.hangle_err_warn_changed)
        print('xArm Version: {}'.format(self.arm.version))
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_state(state=0)
        print('arm.last_used_tcp_acc:',self.arm.last_used_tcp_acc)
        # self.arm.reset(wait=True)
        
        self.xx_init = 422.4
        self.yy_init = -216.9
        self.zz_init = 30
        self.tcp_roll = 17.8
        self.tcp_pitch = 77.4
        self.tcp_yaw = 47.3
        self.init_pos()

        self.zz_init_move = 100
        self.zz_play = 0
        self.hand = InspireHandR()
        self.arm.set_tcp_jerk(10000)

    def init_pos(self):
        
        curr_pos = self.arm.get_position(is_radian=0)[1]

        code = self.arm.set_position(x=curr_pos[0], 
            y=curr_pos[1], 
            z=curr_pos[2]+50, 
            roll=curr_pos[3], 
            pitch=curr_pos[4], 
            yaw=curr_pos[5], 
            speed=200, 
            wait=True)
        code = self.arm.set_position(x=self.xx_init, 
                 y=self.yy_init, 
                 z=self.zz_init, 
                 roll=self.tcp_roll, 
                 pitch=self.tcp_pitch, 
                 yaw=self.tcp_yaw, 
                 speed=200, 
                 wait=True)
    

    
    def play(self,finger_mat,hand,start_time=None):
        '''灵巧手弹琴，手指动作'''
        if start_time is None: 
            finger_mat[:,0] = finger_mat[:,0] - finger_mat[0,0]
            start_time = time.time()
        index = 0
        flag_tumber = 0
        tumber_mat = []   #标记当前时序是采用拇指相邻还是采用拇指间隔
        for i in range(len(finger_mat)):
            if finger_mat[i,5]==1 or finger_mat[i,6]==1:
                if len(tumber_mat)==0:
                    if finger_mat[i,5]==1: 
                        tumber_mat.append([i,1])#拇指相邻
                    elif finger_mat[i,6]==1:
                        tumber_mat.append([i,2])#拇指间隔
                if finger_mat[i,5]==1 and tumber_mat[-1][1]==2:
                    tumber_mat.append([i,1])
                elif finger_mat[i,6]==1 and tumber_mat[-1][1]==1:
                    tumber_mat.append([i,2])
        # print('tumber_mat:',tumber_mat)
        f5_init_pos = hand.f5_init_pos
        f6_init_pos = hand.f6_init_pos
        count = 0
        while 1:
            time.sleep(0.001)
            curr_time = time.time()
            #  print('cost time:', (curr_time - start_time)*1000)
            if (curr_time - start_time)*1000 > finger_mat[index,0]:
                noteoff = 500
                noteon = 1200
                diffn = 500
                pos1 = hand.f1_init_pos + diffn  if finger_mat[index,1] else hand.f1_init_pos  #小拇指伸直0，弯曲2000
                pos2 = hand.f2_init_pos + diffn  if finger_mat[index,2] else hand.f2_init_pos  #无名指伸直0，弯曲2000
                pos3 = hand.f3_init_pos + diffn  if finger_mat[index,3] else hand.f3_init_pos  #中指伸直0，弯曲2000
                pos4 = hand.f4_init_pos + diffn  if finger_mat[index,4] else hand.f4_init_pos  #食指伸直0，弯曲2000
                if finger_mat[index,5] == 1: #大拇指相邻食指活动
                    pos5 = hand.f5_init_pos-100      #大拇指伸直0，弯曲2000
                    pos6 = hand.f6_init_pos + 700 
                    for i in range(len(tumber_mat)-1):
                        if tumber_mat[i][0]==index:# 当前时刻是拇指相邻
                            # f5_init_pos = 800
                            # f6_init_pos = 100
                            if tumber_mat[i+1][1] == 1:  #下一次是拇指位置
                                flag_tumber = 0
                            else:    
                                flag_tumber = 2    #大拇指相邻转为大拇指间隔
                            break
    
                elif finger_mat[index,6] == 1: #大拇指间隔食指活动
                    pos5 = 800      #大拇指伸直0，弯曲2000
                    pos6 = 200 + 700
                    for i in range(len(tumber_mat)-1):
                        if tumber_mat[i][0]==index:
                            # f5_init_pos = hand.f5_init_pos
                            # f6_init_pos = hand.f6_init_pos
                            if tumber_mat[i+1][1] == 2: #下一次拇指位置
                                flag_tumber = 0    #下一次拇指位置不变　
                            else:    
                                flag_tumber = 1   #大拇指间隔转为相邻
                            break
                else:
                    if flag_tumber == 1:   #　下一次转为拇指相邻状态
                        # f5_init_pos = 800
                        # f6_init_pos = 100
                        f5_init_pos = hand.f5_init_pos
                        f6_init_pos = hand.f6_init_pos                       
                        flag_tumber = 0
                    elif flag_tumber ==2: #　下一次转为拇指间隔状态
                        if count < 5:
                            f5_init_pos = 800
                            f6_init_pos = hand.f6_init_pos
                        elif count < 8:          
                            f5_init_pos = 800
                            f6_init_pos = 100
                        else:
                            count = 0
                            flag_tumber = 0
                        count = count + 1

                    pos5 = f5_init_pos
                    pos6 = f6_init_pos
                    # if f5_init_pos==800:
                    #     f6_count += 1
                    #     if f6_count==3:
                    #         f6_count = 0
                    #         f5_init_pos = hand.f5_init_pos

                hand.setpos(pos1,pos2,pos3,pos4,pos5,pos6)
                index = index + 1
                if index == len(finger_mat):
                    break
                    print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
                    hand.reset()
                    # time.sleep(1)
                    start_time = time.time()
                    index = 0
        return
    def hangle_err_warn_changed(self,item):
        print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
        # TODO：Do different processing according to the error code
    def set_xarm_servos(self,values):
        angles = values
        ret = self.arm.set_servo_angle(angle = angles,speed=20,wait=True, is_radian=False)
        return
    def set_pos(self,x,y,z,wait=True):
        code = self.arm.set_position(x=x, 
            y=y, 
            z=z, 
            roll=self.tcp_roll, 
            pitch=self.tcp_pitch, 
            yaw=self.tcp_yaw, 
            speed=100, 
            wait=wait)

    def set_pos_move(self,x,y,wait=True):
        curr_pos = self.arm.get_position(is_radian=0)[1]
        code = self.arm.set_position(x=curr_pos[0], 
            y=curr_pos[1], 
            z=curr_pos[2]+50, 
            roll=curr_pos[3], 
            pitch=curr_pos[4], 
            yaw=curr_pos[5], 
            speed=300, 
            wait=wait)
        code = self.arm.set_position(x=x, 
            y=y, 
            z=self.zz_init_move, 
            roll=self.tcp_roll, 
            pitch=self.tcp_pitch, 
            yaw=self.tcp_yaw, 
            speed=300, 
            wait=wait)

    def set_play_pos(self,x,y):
        
        curr_pos = self.arm.get_position(is_radian=0)[1]

        # code = self.arm.set_position(x=curr_pos[0], 
        #     y=curr_pos[1], 
        #     z=self.zz_play+10, 
        #     roll=self.tcp_roll, 
        #     pitch=self.tcp_pitch, 
        #     yaw=self.tcp_yaw, 
        #     speed=5000, 
        #     wait=False,
        #     mvacc = 5000)  
        # code = self.arm.set_position(x=x, 
        #     y=y, 
        #     z=self.zz_play+10, 
        #     roll=self.tcp_roll, 
        #     pitch=self.tcp_pitch, 
        #     yaw=self.tcp_yaw, 
        #     speed=5000, 
        #     wait=False,
        #     mvacc = 5000)
        code = self.arm.set_position(x=x, 
            y=y, 
            z=self.zz_play, 
            roll=self.tcp_roll, 
            pitch=self.tcp_pitch, 
            yaw=self.tcp_yaw, 
            speed=5000, 
            wait=False,
            mvacc = 5000)  
        while 1:
            time.sleep(0.01)
            res = self.arm.get_position()
            if res[0]==0:
                [x_c,y_c,*_]=res[1]
                # print('x,y:',x,y,'x_c,y_c',x_c,y_c)
                difval = np.abs(x-x_c) +np.abs(y-y_c)
                if difval<0.05 :
                    break
                    

    def get_cost_time(self,hand_pos_fg_f1):
        all_cost_time = []
        key_id,pos = hand_pos_fg_f1[0]

        self.arm.set_position(x=pos[0], 
            y=pos[1], 
            z=self.zz_play, 
            roll=self.tcp_roll, 
            pitch=self.tcp_pitch, 
            yaw=self.tcp_yaw, 
            speed=1000, 
            wait=True,
            mvacc = 1000)
        # return
        all_cost_time.append([key_id,0])
        print("!!!!!!hand_pos_fg_f1:",len(hand_pos_fg_f1))
        count = 0
        for key_id,pos in hand_pos_fg_f1:
            if count==0:
                count +=1
                continue
            start_time = time.time()
            curr_pos = self.arm.get_position(is_radian=0)[1]
            # self.arm.set_position(x=curr_pos[0], 
            #     y=curr_pos[1], 
            #     z=self.zz_play+10, 
            #     roll=self.tcp_roll, 
            #     pitch=self.tcp_pitch, 
            #     yaw=self.tcp_yaw, 
            #     speed=1000, 
            #     wait=False,
            #     mvacc = 1000)
            # self.arm.set_position(x=pos[0], 
            #     y=pos[1], 
            #     z=self.zz_play+10, 
            #     roll=self.tcp_roll, 
            #     pitch=self.tcp_pitch, 
            #     yaw=self.tcp_yaw, 
            #     speed=1000, 
            #     wait=False,
            #     mvacc = 1000)     
            self.arm.set_position(x=pos[0], 
                y=pos[1], 
                z=self.zz_play, 
                roll=self.tcp_roll, 
                pitch=self.tcp_pitch, 
                yaw=self.tcp_yaw, 
                speed=1000, 
                wait=False,
                mvacc = 1000)              
            while 1:
                x = pos[0]
                y = pos[1]
                time.sleep(0.01)
                res = self.arm.get_position()
                if res[0]==0:
                    [x_c,y_c,*_]=res[1]
                    # print('x,y:',x,y,'x_c,y_c',x_c,y_c)
                    difval = np.abs(x-x_c) +np.abs(y-y_c)
                    if difval<0.05 :
                        break
            
            cost_time = time.time() - start_time
            all_cost_time.append([key_id, cost_time])
        
        all_cost_time = np.array(all_cost_time)
        print('all_cost_time:',all_cost_time)
        save_path = "./cost_time.npy"
        np.save(save_path,all_cost_time)

        self.init_pos()

    def set_playmove_test(self,x,y,wait=True,timeout = 2):
        
        # curr_pos = self.arm.get_position(is_radian=0)[1]
        code = self.arm.set_position(x=x, 
            y=y, 
            z=self.zz_play, 
            roll=self.tcp_roll, 
            pitch=self.tcp_pitch, 
            yaw=self.tcp_yaw, 
            radius=1.0,
            speed=5000, 
            wait=wait,
            mvacc = 5000,
            timeout=timeout)



