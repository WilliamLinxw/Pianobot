import os

class PianoConfig(object):
    curr_dir =os.getcwd() + "/template"
    model_1 = curr_dir + "/piano_20200716_162539.npy"    # 特征点匹配，匹配模板
    arm_cali = curr_dir + "/arm_cali.npz"
    loc_pos = curr_dir + "/locxy.npy"
    use_cudasift = False                             #是否使用cuda加速版本sift
    w=720                                          # 分辨率
    h=960  

config = PianoConfig()










