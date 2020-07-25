import cv2
import numpy as np
from piano_config import config

class T_Cam2Arm(object):
    def __init__(self):
        # 相机到局部坐标系

        #局部坐标系到机械臂坐标系
        npz = np.load(config.arm_cali)   # 加载相机与机械臂标定数据
        calib_point= npz['calib_point']  # 机械臂坐标系下机械臂末端位置
        laser_maker=npz['laser_point']   # 相机画面上局部标定坐标，在这里采用静态标定，这个没啥用
        img_point=npz['img_point'].astype('float32')       # 相机画面上机械臂末端位置
        arm_id =npz['arm_id']            # 机械臂移动位置标号
        img_point_in_laser = []


        print('img_point',img_point)

        # [loc_pos, _] = np.load(config.loc_pos)
        loc_pos = [img_point[19],img_point[3],img_point[16],img_point[0]]
        loc_pos = np.array(loc_pos).reshape([4,1,2]).astype('float32')
        dst_temp = np.array( [[0,0], [0,500], [500,0], [500,500 ]] ).astype('float32')
        self.T_cam2loc = cv2.getPerspectiveTransform(loc_pos, dst_temp)
        print('T_cam2loc',self.T_cam2loc )


        for arm_id_ in set(arm_id):
            calib_point_part = [calib_point[s,...] for s in range(len(calib_point)) if arm_id[s]==arm_id_]
            calib_point_part = np.array(calib_point_part)
            laser_maker_part = [laser_maker[s,...] for s in range(len(laser_maker)) if arm_id[s]==arm_id_]
            laser_maker_part = np.array(laser_maker_part)
            img_point_part = [img_point[s,...] for s in range(len(img_point)) if arm_id[s]==arm_id_]
            img_point_part = np.array(img_point_part)
            
            laser_maker_mean = laser_maker_part.mean(axis = 0)
            for i in range(len(img_point_part)):
                cam_pos = img_point[i,:].reshape([-1,2])
                pts = cam_pos.reshape([1,1,2])
                pts = cv2.perspectiveTransform(pts, self.T_cam2loc) #将相机画面上的点映射到局部坐标系上 
                maped_point = pts.reshape([-1,2])
                #  maped_point = self.calcul_map(laser_maker_mean,img_point_part[i,:])
                img_point_in_laser.append(maped_point)
        img_map_point = np.array(img_point_in_laser).reshape([-1,2]) 
        arm_pos =  calib_point[:,0:2]  #只要xy轴，不考虑高度
        print("arm_pos:",arm_pos,arm_pos.shape)
        print("img_pos:",img_map_point,img_map_point.shape)
        arm_pos = arm_pos.T
        img_pos = np.hstack([img_map_point,np.ones([img_map_point.shape[0],1])]).T
        self.T_loc2arm =np.dot(arm_pos,np.linalg.pinv(img_pos))
        #  self.Tarm2img = np.dot(img_pos,np.linalg.pinv(arm_pos))
        print("Timg2arm:",self.T_loc2arm,self.T_loc2arm.shape)


    def T_img2arm_points(self,pos):
        
       
        pts = pos.reshape([-1,1,2])
        pts = cv2.perspectiveTransform(pts, self.T_cam2loc) #相机下的坐标转局部坐标系坐标  
        loc_pos = pts.reshape([-1,2])
        #  print('loc_pos',loc_pos)

        loc_pos_ex = np.hstack( [loc_pos, np.ones([len(loc_pos),1]) ]).T
        #  print('loc_pos',loc_pos_ex.shape)
        arm_pos = np.dot(self.T_loc2arm,loc_pos_ex).T  # 机械臂下坐标
        #  print("armpos:",arm_pos,arm_pos.shape)

        loc_s_pos = loc_pos[0,:]
        img_pos = np.array([loc_s_pos[0],loc_s_pos[1],1]).reshape([-1,1])
        arm_pos_e = np.dot(self.T_loc2arm,img_pos).reshape([1,-1])
        #  print("test:",arm_pos_e)

        return arm_pos
