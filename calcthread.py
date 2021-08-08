# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s

@File: %(filename)s

@Software: Spyder
"""
import threading
from os import makedirs, path
import cv2
import numpy as np
import random
from matplotlib import use
use('agg')
import matplotlib.pyplot as plt
import time
import xlwrite



class CalculateThread(threading.Thread):
    def __init__(self, master):
        super().__init__()
        self.master = master

    
    def run(self):
        self.get_data()
        self.book = xlwrite.Book()
        self.savedpath = path.join(self.file_path, 'Processed')
        folder = path.exists(self.savedpath)
        if not folder:
        	makedirs(self.savedpath)
        self.run_mod()
        del self.master.thread
        return
    
    def run_mod(self):
        lists = [[] for i in range(0, self.file_end +1)]
        self.book.main.write(2, 8, self.file_scale, self.book.style1)
        for k in range(self.file_start, self.file_end +1):
            filename = path.join(self.file_path,
                                  self.file_pre + str(k).zfill(3)+ '.tif')                    # 文件名,zfill 用0填充空位数
            image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)                               # 使用灰度形式读入，第三维为单一数值，二位位置数组
            # w,h = image.shape[::-1]
            # print(len(image[image[:,:]==0]))        # black
            # print(len(image[image[:,:]==255]))      # white

            X = self.Position(image)
            eps=3                                                                           # eps步进数，小于这个数被判定为相邻的点
            min_Pts=2
                        
            # begin = time.time()
            C = self.dbscan(X, eps, min_Pts)
            # end = time.time()
            plt.figure(figsize=(12, 9), dpi=80)
            
            x_coord = [i[0] for i in X]
            y_coord = [i[1] for i in X]
            plt.scatter(x_coord, y_coord, c = C)
            # plt.scatter(X[:,0], X[:,1], c = C)
            plt.xlim(-0.5, 1.5 * self.file_weight)
            plt.xlim(-0.5, 1.5 * self.file_high) 
            plt.savefig(self.savedpath + '\\Processed_'+ self.file_pre + str(k).zfill(3) + '.tif')
            plt.close()
            
            new_C = list(set(C))                                                            # 裂纹编号
            new_C.sort(key=C.index)
            #A=[]
            # 数据写入
            self.book.Creat_sheet(k)
            self.book.Write_sheet(k - self.file_start + 1, len(new_C)-1, len(C))
            
            for i in new_C[:-1]:
                lists[k].append(C.count(i))

        self.book.Write_result(self.file_high, self.file_weight, self.grain_size)
        self.book.save(self.savedpath + '\\Crack_stastistics.xls')
        print('over, destroy')
        self.master.destroy()
    
    def Position(self, image):
        Position = [[0,0]]                                                              # 找出黑点位置，并记录在其中
        for i in range(0, self.file_weight):
            for j in range(0, self.file_high):
                if image[j,i]==0:
                    Position = np.append(Position, [[i,j]], axis=0)
        return Position[1:-1]
    
    def findNeighbor(self, j, X, eps):
        N=[]
        for p in range(X.shape[0]):          # find all objects
            temp = abs(X[j][0]-X[p][0]) + abs(X[j][1]-X[p][1])            # np.sqrt(np.sum(np.square(X[j]-X[p])))    # Distance
            if(temp<=eps):
                N.append(p)
        return N
    
    def dbscan(self, X, eps, min_Pts):
        k=-1
        NeighborPts = []          # array,all objects in a domain
        # Ner_NeighborPots = []
        fil = []                  # initially, the list of accessed objectes is empty 
        gama = [x for x in range(len(X))] #initially, all objects is unaccessed
        cluster = [-1 for y in range(len(X))]
        while len(gama)>0:
            j = random.choice(gama)               #random.choice(gama),gama[0]
            gama.remove(j)           # remove from unaccessed list
            fil.append(j)            # add in accessed list
            NeighborPts = self.findNeighbor(j, X, eps)
            if len(NeighborPts)<min_Pts:                                                # 周围最小点个数
                pass
            else:
                k=k+1
                cluster[k]=k
                for i in NeighborPts:
                    if i not in fil:
                        gama.remove(i)
                        fil.append(i)
                        Ner_NeighborPts = self.findNeighbor(i, X, eps)
                        if len(Ner_NeighborPts) >= min_Pts:
                            for a in Ner_NeighborPts:
                                if a not in NeighborPts:
                                    NeighborPts.append(a)
                        if cluster[i] == -1:
                            cluster[i]=k
        return cluster
    
    def get_data(self):
        self.file_path = self.master.e1.get()
        self.file_pre = self.master.e21.get()
        
        str_a = self.master.e22.get()
        str_b = self.master.e23.get()
        str_x = self.master.e31.get()
        str_y = self.master.e32.get()
        str_s = self.master.e41.get()
        str_grain_size = self.master.e42.get()
        
        self.file_start = self.trans_number(str_a)
        self.file_end = self.trans_number(str_b)
        self.file_weight = self.trans_number(str_x)
        self.file_high = self.trans_number(str_y)
        self.file_scale = self.trans_number_fra(str_s)
        self.grain_size = self.trans_number_fra(str_grain_size)
    
    def trans_number(self,s):
        try:
            a = int(s)
            return a
        except ValueError:
            pass
    
        return False

    def trans_number_fra(self,s):
        try:
            a = float(s)
            return a
        except ValueError:
            pass
         
        return False