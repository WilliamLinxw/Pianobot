# -*- coding: utf-8 -*-
'''
该脚本为钢琴模板标注脚本
1 启动脚本后将棋盘放置于相机下,屏幕中尽量只包含棋盘,可以参考template中的模板图片
2 按下键盘L键, 画面停止,鼠标双击画面上棋盘四角,与左右边缘中间棋格点位置(注意,中间棋格点是楚河汉界两边的点,左右各点一个即可,
  不要完全对称,否则算法无法区分不同视角下棋盘前后位置关系)
  点击顺序为: 左上 右上 左下 右下 左中 右中!
3 双击完六个点后,画面上会叠加点击位置,按Q键退出, 模板数据会保存到template文件夹,以时间命名. 其中*.npy为模板数据,运行棋盘识别必须要有
  *.jpg为可视化图片,表示该模板是什么样子的,没啥用,可以丢掉!

'''
import cv2
import numpy as np
import os
import time
from _datetime import datetime

save_path = "template/"
key_point=[]
#mouse callback function
def draw_circle(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDBLCLK:
        print(x,y)
        key_point.append([x,y])
        # cv2.circle(frame,(x,y),20,(0,0,255),-1)

if __name__ == '__main__':
    cap = cv2.VideoCapture(2)
    w = int(cap.get(3))
    h = int(cap.get(4))

    # 创建图像与窗口并将窗口与回调函数绑定
    cv2.namedWindow('Labeling')
    cv2.setMouseCallback('Labeling', draw_circle)
    newimg = 0
    while (True):
        ret, img = cap.read()  # 捕获一帧图像
        cv2.imshow('Labeling', img)
        # 判断按键，如果按键为l，暂停图像
        if cv2.waitKey(1) & 0xFF == ord('l'):
            while(True):
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)

                    # 保存匹配点与原图数据
                    if len(newimg) >1 :
                        str = "piano_%s"%time.strftime("%Y%m%d_%H%M%S")
                        cv2.imwrite(save_path + "%s.jpg"%str,newimg)
                        np.save(save_path + "%s"%str,[key_point,img])
                    exit(0)
                if len(key_point)>0:
                    newimg = img.copy()
                    for x,y in key_point:
                        newimg = cv2.circle(newimg, (x, y), 5, (0, 0, 255), -1)
                    cv2.imshow('Labeling', newimg)











