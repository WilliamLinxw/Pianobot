import numpy as np
import midi
from mid_tune import mid_tune, mid_tune_2,get_arm_finger,get_arm_finger_V2,get_finger

def get_notes_list(filepath = "template/天空之城.mid", r=1,track=1,diffnum = 24,t1 =0,t2 =-1):
    pattern = midi.read_midifile(filepath)
    p = pattern[track]
    # midi.TimeSignatureEvent(tick=0, data=[4, 2, 96, 8]),
    # 4拍为一节, 2分音符为一拍, 一分钟96拍??
    print("resolution",pattern.resolution)
    resolution = pattern.resolution
    #  bpm = 120
    for pp in pattern[0]:
        if type(pp) is type(midi.events.SetTempoEvent()):
            print("bpm:",pp.get_bpm())
            bpm = pp.get_bpm()

    ticktime = (60*1000.0/bpm)/resolution
    print("ticktime:",ticktime)
    pattern.make_ticks_abs()
    #  print(p)
    notes_time_list = []
    for pp in p :
        if t1 !=0:
            if pp.tick * ticktime<t1*1000:
                continue
        if t2 != -1:
            if pp.tick * ticktime>t2*1000:
                break
        if type(pp) is type(midi.events.NoteOnEvent()):
            tim = pp.tick * ticktime *r
            notes_time_list.append([int(tim),pp.data[0],1])
        if type(pp) is type(midi.events.NoteOffEvent()):
            tim = pp.tick * ticktime * r
            notes_time_list.append([int(tim),pp.data[0],0])
    notes_time_list = np.array(notes_time_list)
    if diffnum != 0:
        notes_time_list[:,1] = notes_time_list[:,1] - diffnum
    note_set = set(notes_time_list[:,1])
    for i in range(len(notes_time_list)):
        print(notes_time_list[i,:])

    print("note_set:",note_set)
    states = set(notes_time_list[:,2])
    if len(list(states))==1:
        for i in range(int(len(notes_time_list))):
            if notes_time_list[i,2]==1:
                for ii in range(i+1,len(notes_time_list)):
                    if notes_time_list[i,1]==notes_time_list[ii,1]:
                        notes_time_list[ii,2]=0
                        break

    # 梳理一遍确定每个音符有１必有０
    note_list_1 = []
    note_list_0 = []
    for i in range(len(notes_time_list)):
        if notes_time_list[i,2]==1:
            note_list_1.append(notes_time_list[i,...])
        if notes_time_list[i,2]==0:
            note_list_0.append(notes_time_list[i,...])
    line_num = np.min([len(note_list_0),len(note_list_1)])
    note_list_0 = np.array(note_list_0)
    note_list_1 = np.array(note_list_1)
    print('note_list_0:',note_list_0.shape)
    print('note_list_1:',note_list_1.shape)
    print('line_num:',line_num)
    note_list = np.vstack([note_list_1[0:line_num,:],note_list_0[0:line_num,:]])
    notes_time_list = note_list[note_list[:,0].argsort()] 

    return notes_time_list

# 白键所对应的所有手的位置
def get_white_key_hand_group(finger_num,piano_key):
    '''获取所给钢琴键范围内所有可能的 手-按键分组'''

    hand_key_group=[]
    for i in range(len(piano_key)-finger_num+1):
        key_group = piano_key[i:i+finger_num]
        hand_key_group.append(key_group)
    return hand_key_group

# 黑键所对应的所有手的位置，若两个黑键之间有间隔，则将其分为两组，相邻的两个或三个音只有一种位置，如#D，#E为一组，食指弹#D，中指弹#D
# #F，#G，#A为一组，食指弹#F，中指弹#G，无名指弹#F
def get_black_key_hand_group(black_key_group):
    hand_pos = []
    black_key_hand_group = []
    hand_pos.append(black_key_group[0])
    i = 0
    while True:
        if i == len(black_key_group) - 1:
            black_key_hand_group.append(hand_pos)
            break
        elif black_key_group[i+1] - black_key_group[i] < 3:
            hand_pos.append(black_key_group[i+1])
        else:
            black_key_hand_group.append(hand_pos)
            hand_pos = []
            hand_pos.append(black_key_group[i+1])
        i += 1
    return black_key_hand_group

# 将白键对应的手位置和黑键对应的手位置合并，并且按照位置从左到右排序
def get_hand_key_group(white_key_hand, black_key_hand):
    whole_hand_group = white_key_hand + black_key_hand
    whole_hand_group.sort()
    return whole_hand_group

def get_notes_hand_key_group(notes_time_list,hand_key_group):
    '''获取每个音符对应的可能的手掌位置'''

    for i in range(len(notes_time_list)):
        print('xxxxxxxxxxxxxxxxxxxxxxxx i:',i,notes_time_list[i,1])
        if notes_time_list[i,1]==61:notes_time_list[i,1]=62
        if notes_time_list[i,1]==63:notes_time_list[i,1]=64
        if notes_time_list[i,1]==66:notes_time_list[i,1]=65
        if notes_time_list[i,1]==68:notes_time_list[i,1]=67
        if notes_time_list[i,1]==70:notes_time_list[i,1]=69

        if notes_time_list[i,1]==73:notes_time_list[i,1]=72
        if notes_time_list[i,1]==75:notes_time_list[i,1]=76
        if notes_time_list[i,1]==78:notes_time_list[i,1]=77
        if notes_time_list[i,1]==80:notes_time_list[i,1]=79
        if notes_time_list[i,1]==82:notes_time_list[i,1]=81
    
    note_key = []
    for i in range(len(notes_time_list)):
        if notes_time_list[i,2]==1: #只找按下时刻的音符时间
            note_key.append([notes_time_list[i,0], notes_time_list[i,1]])
   
    hand_id = []
    # print('@@@@:', len(notes_time_list))
    # print('@@@@:', len(note_key))
    for i in range(len(note_key)):
        note_hand_id = []
        key_note = note_key[i][1]
        for id,hand_key in enumerate(hand_key_group):
            if key_note in hand_key:   # 当前音符在某个手掌的音符组中
                note_hand_id.append(id)
        hand_id.append(note_hand_id)
    # print('@@@@:', len(hand_id))
    for i,hand in enumerate(hand_id):
        print(i,"note_key:",note_key[i],hand)

    return hand_id


def get_note_handid_mat(piano_key,finger_num,hand_id):
    # 求多个音符手掌位置的交集，当交集为空的时候，前一个交集不为空的手掌位置，作为这些音符对应的手掌位置
    hand_ids_set = []
    a = list(range(0,len(piano_key)-finger_num+1))
    for i,ids in enumerate(hand_id):
        a_ = a.copy()
        a = set(a) & set(ids)
        if len(a)==0:
            hand_ids_set.append([i,list(a_)])
            a = ids
        print('i,a',i,a)
    else:
        hand_ids_set.append([i+1,list(a)])
    print("~~~~~~~~~~~~~手掌位置~~~~~~~~~~~~~~~~~~~")
    for i in range(len(hand_ids_set)):
        print(i,hand_ids_set[i])
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # 将多个手掌位置中选择与前一个落差最小的一个
    for i in range(len(hand_ids_set)):
        if len(hand_ids_set[i][1])>1:
            if i == 0: 
                hand_ids_set[i][1] = [hand_ids_set[i][1][0]]
            else:
                last_id = hand_ids_set[i-1][1][0]
                diff = [(last_id-ee) for ee in hand_ids_set[i][1]]   
                diff = np.array([abs(ee) for ee in diff])
                min_id = np.argmin(diff)
                hand_ids_set[i][1] = [hand_ids_set[i][1][min_id]]
        print(i,hand_ids_set[i])

    note_hand = []
    count = 0
    print(hand_ids_set)
    print("----------------")
    for i in range(len(hand_id)):
        if i == hand_ids_set[count][0]:
            count = count + 1
        print(i,count,hand_ids_set[count])
        note_hand.append([i,hand_ids_set[count][1][0]])
    print("~~~~~每个音符对应的手掌位置~~~~")
    for i in range(len(note_hand)):
        print(i,note_hand[i])
    return note_hand


#  notes_time_list = get_notes_list(filepath = "template/小星星2.mid", r=1)

#  notes_time_list = get_notes_list(filepath = "template/致爱丽丝.mid", r=1,track=2, diffnum = -12)
# notes_time_list = get_notes_list(filepath = "template/洋娃娃和小熊跳舞2.mid", r=1,track=1, diffnum = 0,t1 = 0,t2=10)
# print(notes_time_list )
if __name__=="__main__":
    # notes_time_list = get_notes_list(filepath = "template/欢乐颂2.mid", r=1,track=0, diffnum = 12,t1 = 0,t2=20)
    # notes_time_list = get_notes_list(filepath = "template/超级玛丽.mid", r=1,track=0, diffnum = 0,t1 = 0,t2=-1)
    notes_time_list = get_notes_list(filepath = "template/天空之城.mid", r=1,track=0, diffnum = 24,t1 = 0,t2=-1)
    print(notes_time_list)
    piano_key = [60,62,64,65,67,69,71,
                 72,74,76,77,79,81,83,
                 84,86,88,89,91,93,95]
    finger_num = 5
    hand_key_group = get_hand_key_group(finger_num,piano_key)
    hand_id = get_notes_hand_key_group(notes_time_list,hand_key_group)
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

    notes_time_list = mid_tune_2(note_hand,hand_pos_fg,notes_time_list)     