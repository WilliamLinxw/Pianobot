#!/usr/bin/env python3
#!coding=utf-8
import numpy as np
import cv2
import os,sys,math,time
from piano_config import config
debug = 0 

class PianoLoacal(object):
    '''
    通过特征匹配，匹配钢琴四个点
    '''
    def __init__(self):
        
        temp_path = config.model_1
        [temp_point,temp_img] = np.load(temp_path,allow_pickle=True)
        
        self.current_img = None 
        self.qipan_point = None 
        self.temp_img = temp_img
        self.temp_point = temp_point


        self.MIN_MATCH_COUNT = 10
        # 特征提取

        if config.use_cudasift:
            self.sift = CudaSift()
        else:
            self.sift = cv2.xfeatures2d.SIFT_create(int(2000))

        gray1 = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
        keypoints1,descriptor1 = self.sift.detectAndCompute(gray1, None)
        self.keypoints1 = keypoints1
        self.descriptor1 = descriptor1

        # 匹配器
        FLANN_INDEX_KDTREE = 0
        indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        searchParams = dict(checks=50)
        self.flann = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        #self.flann = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
    
    def get_image_callback(self, image):
        current_img= image
        self.current_img = current_img
        img2 = self.current_img.copy()
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        tic = time.time()
        keypoints2,descriptor2 = self.sift.detectAndCompute(gray2, None)
        if debug:
            toc = time.time() - tic
            print("sift time:",toc)
            tic = time.time()
        if (descriptor2 is None) or (len(descriptor2) <4) :
            return [None]
        if debug:
            print( 'descriptor1', self.descriptor1.shape, 'descriptor2', descriptor2.shape)
        matches = self.flann.knnMatch(self.descriptor1, descriptor2, k=2)
        if debug:
            print("matches:", len(matches), len(matches_tiaoqi))
        goodMatch = []
        for m, n in matches:
            if m.distance < 0.8 * n.distance:
                goodMatch.append(m)
        
        toc = time.time() - tic
        #  print("p2 detect time:",toc)

       
        if debug:
            print("goodMatch :", len(goodMatch))
        
        
        if len(goodMatch)>=self.MIN_MATCH_COUNT :
            dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
            src_pts = np.float32([self.keypoints1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)  # img1特征点
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,0.0,maxIters=10000, confidence = 0.9999 )
            if not (M is None):
                matchesMask = mask.ravel().tolist()
                pts = np.float32(self.temp_point).reshape(-1, 1, 2)  # 模板图片上位置点
                dst = np.int32(cv2.perspectiveTransform(pts, M))  # 实际图上的位置

                new_dst = dst.reshape([1,-1])[0].astype('float')
            else:
                new_dst = None
        else:
            new_dst = None
        
        if debug:                  
            print("match time:",toc)
        
        #  toc = time.time() - tic
        #  print("p3 detect time:",toc)


        return new_dst


