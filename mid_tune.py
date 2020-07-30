import numpy as np 


def mid_tune(mid_name,notes_time_list):
    if mid_name == "天空之城.mid":
        notes_time_list_2 = []
        switch_time = []
        for i in range(len(notes_time_list)):
            if notes_time_list[i][0]==24000 and notes_time_list[i][1]==67: 
                notes_time_list[i][0]=23000
            notes_time_list_2.append(notes_time_list[i])

        switch_time = []
        switch_time.append([-1,-1, 67,69,71,72,74,76 ]) #初始情况下拇指在72的位置上 
        switch_time.append([11876,11999, 64,65,67,69,71,72 ]) 
        # switch_time.append([20750,21249, 65,67,69,71,72 ]) 
        # switch_time.append([23201,23999, 60,62,64,65,67 ]) 
        # switch_time.append([25709 ,25749,28208, 69,71,72,74,76 ]) 
        # switch_time.append([3000,4000, 64,65,67,69,71 ]) 
        # switch_time.append([4900,5250, 67,69,71,72,74 ]) 
        # switch_time.append([7300,8000, 62,64,65,67,69 ]) 
        # switch_time.append([9000,9208, 64,65,67,69,71 ]) 
        # switch_time.append([9700,9750, 69,71,72,74,76 ]) 

        return notes_time_list_2,switch_time

    if mid_name == "洋娃娃和小熊跳舞2.mid":
        notes_time_list_2 = []
        for i in range(len(notes_time_list)):
            if notes_time_list[i][0]>9450 and notes_time_list[i][0]<9600: 
                continue
            if notes_time_list[i][0]== 9450  and notes_time_list[i][2] ==1:
                continue
            if notes_time_list[i][0]== 9600  and notes_time_list[i][2] ==0:
                continue

            # if notes_time_list[i][0]== 13050  and notes_time_list[i][2] ==1:
            #     continue
            # if notes_time_list[i][0]== 13200  and notes_time_list[i][2] ==0:
            #     continue

            if notes_time_list[i][0]== 13950  and notes_time_list[i][2] ==1:
                continue
            if notes_time_list[i][0]== 14400  and notes_time_list[i][2] ==0:
                continue

            if notes_time_list[i][0]== 17850  and notes_time_list[i][2] ==1:
                continue
            if notes_time_list[i][0]== 18000  and notes_time_list[i][2] ==0:
                continue

            if notes_time_list[i][0]>28350 and notes_time_list[i][0]<28650: 
                continue
            if notes_time_list[i][0]== 28350  and notes_time_list[i][2] ==1:
                continue
            if notes_time_list[i][0]== 28650  and notes_time_list[i][2] ==0:
                continue


            notes_time_list_2.append(notes_time_list[i])
        
        switch_time = []
        switch_time.append([-1,-1, 72,74,76,77,79 ]) #初始情况下拇指在72的位置上 
        switch_time.append([9450,9600, 74,76,77,79,81]) 
        # switch_time.append([13050,13200, 72,74,76,77,79])
        switch_time.append([13950,14400,74,76,77,79,81])
        switch_time.append([17850,18000,72,74,76,77,79])
        # switch_time.append([9450,9600, 74,76,77,79,81]) 
        return notes_time_list_2,switch_time

def mid_tune_2(note_hand,hand_pos_fg,notes_time_list):
    '''
    note_hand:每个音符对应的手掌位置标号
    hand_pos_fg：每个手掌手指对应的琴键
    notes_time_list：音符时序
    '''
    note_hand = np.array(note_hand)
    print('===================================')
    print('note_hand:',note_hand,len(note_hand))
    print('hand_pos_fg:',hand_pos_fg, len(hand_pos_fg))
    print('notes_time_list:',notes_time_list,len(notes_time_list))

    notes_time_1=[]
    notes_time_0=[]
    for t,k,s in notes_time_list:
        # print('t,k,s:',t,k,s)
        if s == 1:
            notes_time_1.append([t,k,s])
        if s == 0:
            notes_time_0.append([t,k,s])
    # notes_time_1 = np.array(notes_time_1)
    # notes_time_0 = np.array(notes_time_0)
    print('notes_time_1:',notes_time_1)
    print('notes_time_0:',notes_time_0)
    #一般认为音符先响先落
    notes_time_list_2=[]
    n_t_list = []
    # 部分曲目只有按下时间没有弹起时间
    if notes_time_0==[]:
        xx = notes_time_1 
    else:
        xx = notes_time_0
    for i in range(len(xx)):
        if n_t_list==[]:  #第一个
            n_t_list.append(notes_time_1[i])
            if notes_time_0==[]:
                xx = notes_time_1[i].copy()
                xx[0] += 100
                xx[2] = 0
                n_t_list.append(xx)
            else:
                n_t_list.append(notes_time_0[i])
        elif note_hand[i,1]==note_hand[i-1,1]:
            n_t_list.append(notes_time_1[i])
            if notes_time_0==[]:
                xx = notes_time_1[i].copy()
                xx[0] += 100
                xx[2] = 0
                n_t_list.append(xx) 
            else:          
                n_t_list.append(notes_time_0[i])
        elif note_hand[i,1]!=note_hand[i-1,1]:
            n_t_list = np.array(n_t_list)
            notes_time_list_2.append(n_t_list)
            n_t_list = []
            n_t_list.append(notes_time_1[i])
            if notes_time_0==[]:
                xx = notes_time_1[i].copy()
                xx[0] += 100
                xx[2] = 0
                n_t_list.append(xx)
            else:
                n_t_list.append(notes_time_0[i])
    else:
        n_t_list = np.array(n_t_list)
        notes_time_list_2.append(n_t_list)
    # notes_time_list_2 = np.array(notes_time_list_2)
    print('notes_time_list_2:',notes_time_list_2,len(notes_time_list_2))
    notes_time_sort_list = []
    for data in notes_time_list_2: #安装时间排个序
        data = data[data[:,0].argsort()] 
        notes_time_sort_list.append(data)
    print('notes_time_sort_list:',notes_time_sort_list,len(notes_time_sort_list))

    return notes_time_sort_list


def get_arm_finger(notes_time_list,switch_time):
    #获取手臂与手指动作序列:
    finger_mat_list = []
    print('switch_time:',switch_time)
    for i in range(len(switch_time)):
        if i != len(switch_time)-1:
            _, st, *f1 = switch_time[i]
            et, *_ = switch_time[i+1]
        else:
            _, st, *f1 = switch_time[i]
            et = notes_time_list[-1][0]
            
        note_list = []
        if notes_time_list[-1][0] < st:
            break
        for ii in range(len(notes_time_list)):
            nt = notes_time_list[ii]
            if nt[0]>st and nt[0]<et:
                note_list.append(nt)
        print("arm_finger:",i,len(note_list),st,et,f1)
        finger_mat = get_finger(note_list,finger_index=f1 ,time_step=20,use_fixed = True)
        finger_mat_list.append(finger_mat)
    return finger_mat_list

def get_arm_finger_V2(notes_time_list,hand_pos_fg):
    # 加载已知的机械臂运动耗时，重新调整音符序列倍数，似的整体与乐曲保持一致
    save_path = "./cost_time.npy"
    all_cost_time = np.load(save_path)
    # print('all_cost_time:',all_cost_time)
    print('notes_time_list:',notes_time_list)
    note_cost_time = []
    notes_time_list２=[]

    for i,notes in enumerate(notes_time_list):
        data = []
        for ii in range(len(notes)):
            if notes[ii,2]==1:
                data.append([notes[ii,0],notes[ii,1],notes[ii,2]])
        data = np.array(data)
        notes_time_list２.append(data)
        
    print('notes_time_list2:',len(notes_time_list２),len(notes_time_list))

    for i,notes in enumerate(notes_time_list２) :
        if i == 0:
            continue
        t = notes[0,0]
        note_dt = t - notes_time_list２[i-1][-1,0] #上一段最后一个音符时间
        note_cost_time.append(note_dt)
    
    note_cost_time = np.array(note_cost_time)
    arm_move_time = all_cost_time[1:,1]*1000
    print('note_cost_time:',note_cost_time,len(note_cost_time))
    print('arm_move_time:',arm_move_time,len(arm_move_time))
    if len(notes_time_list)!=1:
        r = arm_move_time/note_cost_time
        max_r = np.max(r)
        print('放慢倍率 :',max_r)
        max_r = np.floor(max_r)
        max_r = 1
    else:
        max_r = 1
    
    # 将每段最后停止音符时间提前
    for i,notes in enumerate(notes_time_list):
        data = []
        tt = -1
        for ii in range(len(notes_time_list[i]),0):
            if notes_time_list[i][ii,2] == 0:#找到最后按下的键
                break
        for jj in range(len(notes_time_list[i]),0):
            if notes_time_list[i][jj,1] == notes_time_list[i][ii,1] \
                and notes_time_list[i][jj,2] == 1: #找到最后按下的键的时间
                tt = notes_time_list[i][jj,0]
                break
        if tt!=-1:
            if notes_time_list[i][ii,0] - tt > 250:
                notes_time_list[i][ii,0] = tt + 250 

    # 修改音符序列倍率
    for i,notes in enumerate(notes_time_list):
        data = []
        for ii in range(len(notes_time_list[i])):
            notes_time_list[i][ii,0] = notes_time_list[i][ii,0] * max_r


    # 获取手臂与手指动作序列:
    finger_mat_list = []
    for i in range(len(notes_time_list)):
        f1 = hand_pos_fg[i]
        note_list = notes_time_list[i]
        print('!!!!!!!!!!!!!!!!!!!分段音符序列：',note_list)
        if len(f1) == 5:
            f1 = [0] + f1
        if len(f1) == 3:
            f1 = [0, 0] + f1 + [0]
        if len(f1) == 2:
            f1 = [0, 0] + f1 + [0, 0]
        
        # print("arm_finger:",i,len(note_list),note_list[0,0],note_list[-1,0],f1)
        finger_mat = get_finger(note_list,finger_index=f1 ,time_step=20,use_fixed = False)
        # for i in range(len(finger_mat)):
        #     print(finger_mat[i,:])
        # print("============================")
        finger_mat_list.append(finger_mat)
    return finger_mat_list



def get_finger(notes_time_list,finger_index=[71,72,74,76,77,79],time_step=50,use_fixed = False):
    '''finger_index 为大拇指-小拇指对应的音符 '''
    
    f1_1 = finger_index[0] #大拇指间隔食指
    f1_2 = finger_index[1] #大拇指相邻食指
    f2 = finger_index[2] #食指
    f3 = finger_index[3] #中指
    f4 = finger_index[4] #无名指
    f5 = finger_index[5] #小拇指
    # time_step = 50
    data = np.array(notes_time_list)
    n = int((data[-1,0] - data[0,0] ) / time_step)+1

    finger_mat = np.zeros([n,7])
    # 小指 无名指 中指 食指 大拇指相邻　大拇指间隔
    # 79   77     76   74   72　　　71
    for i in range(n):
        finger_mat[i,0] = data[0,0] + i*time_step 
    
    # 小指
    index = np.where(data[:,1]==f5)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:# 不考虑最后一个
            for ii in range(n):
                if data[index[i],0]-finger_mat[ii,0]>=0 and data[index[i],0]-finger_mat[ii,0]<time_step:
                    start_id  = ii
                if data[index[i+1],0]-finger_mat[ii,0]>=0 and data[index[i+1],0]-finger_mat[ii,0]<time_step:
                    end_id  = ii
            if use_fixed: end_id = int(start_id+ (end_id - start_id)*1./3)
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,1] = 1
            else:
                finger_mat[start_id:end_id,1] = 0

    # 无名指    
    index = np.where(data[:,1]==f4)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:# 不考虑最后一个
            for ii in range(n):
                if data[index[i],0]-finger_mat[ii,0]>=0 and data[index[i],0]-finger_mat[ii,0]<time_step:
                    start_id  = ii
                if data[index[i+1],0]-finger_mat[ii,0]>=0 and data[index[i+1],0]-finger_mat[ii,0]<time_step:
                    end_id  = ii
            if use_fixed: end_id = int(start_id+ (end_id - start_id)*1./3)
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,2] = 1
            else:
                finger_mat[start_id:end_id,2] = 0

    # 中指 
    index = np.where(data[:,1]==f3)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:# 不考虑最后一个
            for ii in range(n):
                if data[index[i],0]-finger_mat[ii,0]>=0 and data[index[i],0]-finger_mat[ii,0]<time_step:
                    start_id  = ii
                if data[index[i+1],0]-finger_mat[ii,0]>=0 and data[index[i+1],0]-finger_mat[ii,0]<time_step:
                    end_id  = ii
            if use_fixed: end_id = int(start_id+ (end_id - start_id)*1./3)
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,3] = 1
            else:
                finger_mat[start_id:end_id,3] = 0

    # 食指 
    index = np.where(data[:,1]==f2)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:# 不考虑最后一个
            for ii in range(n):
                if data[index[i],0]-finger_mat[ii,0]>=0 and data[index[i],0]-finger_mat[ii,0]<time_step:
                    start_id  = ii
                if data[index[i+1],0]-finger_mat[ii,0]>=0 and data[index[i+1],0]-finger_mat[ii,0]<time_step:
                    end_id  = ii
            if use_fixed: end_id = int(start_id+ (end_id - start_id)*1./3)
            if data[index[i], 2] == 1:
                finger_mat[start_id:end_id,4] = 1
            else:
                finger_mat[start_id:end_id,4] = 0

    # 大拇指_相邻食指
    index = np.where(data[:,1]==f1_2)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:# 不考虑最后一个
            for ii in range(n):
                if data[index[i],0]-finger_mat[ii,0]>=0 and data[index[i],0]-finger_mat[ii,0]<time_step:
                    start_id  = ii
                if data[index[i+1],0]-finger_mat[ii,0]>=0 and data[index[i+1],0]-finger_mat[ii,0]<time_step:
                    end_id  = ii
            if use_fixed: end_id = int(start_id+ (end_id - start_id)*1./3)
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,5] = 1
            else:
                finger_mat[start_id:end_id,5] = 0

    # 大拇指_间隔食指
    index = np.where(data[:,1]==f1_1)[0]
    for i in range(len(index)) :
        if index[i] !=index[-1]:# 不考虑最后一个
            for ii in range(n):
                if data[index[i],0]-finger_mat[ii,0]>=0 and data[index[i],0]-finger_mat[ii,0]<time_step:
                    start_id  = ii
                if data[index[i+1],0]-finger_mat[ii,0]>=0 and data[index[i+1],0]-finger_mat[ii,0]<time_step:
                    end_id  = ii
            if use_fixed: end_id = int(start_id+ (end_id - start_id)*1./3)
            if data[ index[i], 2] == 1:
                finger_mat[start_id:end_id,6] = 1
            else:
                finger_mat[start_id:end_id,6] = 0

    finger_mat = finger_mat.astype('int')
    return finger_mat


        

