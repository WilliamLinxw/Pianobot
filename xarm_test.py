# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import time
from XarmControl import XarmControl


if __name__ == '__main__':
    arm = XarmControl()
    pos_1 = [[634, 285], [623, 179]]
    pos_np = np.array(pos_1)
    distance = np.sqrt(np.sum((pos_np[0,:] -pos_np[1,:])**2) )
    print('distance:',distance)
    x,y = pos_1[0]
    arm.set_playmove_test(x,y,wait=True,timeout = 2)
    for count in range(10):
        for i, pos in enumerate(pos_1):
            x,y = pos
            t1 = time.time()
            arm.set_playmove_test(x,y,wait=False,timeout = 2)
            while 1:
                time.sleep(0.01)
                res = arm.arm.get_position()
                if res[0]==0:
                    [x_c,y_c,*_]=res[1]
                    # print('x,y:',x,y,'x_c,y_c',x_c,y_c)
                    difval = np.abs(x-x_c) +np.abs(y-y_c)
                    if difval<0.05 :
                        break
            t2 = time.time()
            print('cost time:%.4f, speed:%.4f, difval:%.4f'%(t2-t1,distance/(t2-t1),difval))
    

