# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s

@File: %(filename)s

@Software: Spyder
"""

import tkinter as tk
import tkinter.messagebox
import sys
from os import makedirs
from os import path as pt
import cv2
import numpy as np
import random 
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import time
import xlwrite
import xlwt




class GUI():
    def __init__(self, master=None):
        self.root = master
        self.Mainpage()
        
    def Mainpage(self):
        self.root.title("裂纹统计模型")# 设置标题

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.menubar_set()
        self.label_set()
        self.entery_set()
        # self.entery_preentery()
        # self.entery_stick()
        self.button_set()
    
    
    # 主页面的四个格式函数   
    def menubar_set(self):
        # 最上方文件栏
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)    
        
    def label_set(self):
        # 设置标签
        tk.Label(self.root, text='储存文件的路径：').grid(row=0, column=0)# 选项row代表行，column代表列
        tk.Label(self.root, text='文件的前缀名称：').grid(row=1, column=0)
        tk.Label(self.root, text='文件的编号是从：').grid(row=1, column=2)
        tk.Label(self.root, text='到').grid(row=1, column=4)
        tk.Label(self.root, text='水平像素：').grid(row=2, column=0)
        tk.Label(self.root, text='垂直像素：').grid(row=2, column=2)
        tk.Label(self.root, text='比例尺(微米/像素)：').grid(row=3, column=0)
        tk.Label(self.root, text='晶粒尺寸：').grid(row=3, column=2)
        tk.Label(self.root, text='微米').grid(row=3, column=4)
        
    def entery_set(self):
        # 输入框
        self.e1 = tk.Entry(self.root)
        self.e21 = tk.Entry(self.root)
        self.e22 = tk.Entry(self.root)
        self.e23 = tk.Entry(self.root)
        self.e31 = tk.Entry(self.root)
        self.e32 = tk.Entry(self.root)
        self.e41 = tk.Entry(self.root)   
        self.e42 = tk.Entry(self.root)

    # def entery_preentery(self):       
        # 预设文字
        self.e1.insert(0, "E:\\54055\\Documents\\SEM_image")
        self.e21.insert(0, 'ls_')
        self.e22.insert(0, '1')
        self.e23.insert(0, '30')
        self.e31.insert(0, '2560')
        self.e32.insert(0, '1792')
        self.e41.insert(0, '0.9921')
        self.e42.insert(0, '40')
        
    # def entery_stick(self):
        # Grid允许我们使用表格的形式管理组件
        self.e1.grid(row=0, column=1, padx=20, pady=5, ipadx=270, columnspan=5, sticky=tk.W)
        self.e21.grid(row=1, column=1, padx=10, pady=5)
        self.e22.grid(row=1, column=3, padx=10, pady=5)
        self.e23.grid(row=1, column=5, padx=10, pady=5)
        self.e31.grid(row=2, column=1, padx=10, pady=5)
        self.e32.grid(row=2, column=3, padx=10, pady=5)
        self.e41.grid(row=3, column=1, padx=10, pady=5)
        self.e42.grid(row=3, column=3, padx=10, pady=5)
        
    def button_set(self):
        # 使用Button按钮
        tk.Button(self.root, text='开始分析', width=10, command=self.start_cal).grid(row=5, column=1, sticky=tk.E, padx=10, pady=5) # 退出直接调用根窗口的quit方法
        tk.Button(self.root, text='退出程序', width=10, command=self.on_closing).grid(row=5, column=3, sticky=tk.E, padx=10, pady=5) # 退出直接调用根窗口的quit方法
        
    def changeText(self):
        self.text.set("Text updated")    
        
    def start_cal(self):
        self.Pre_process()
        lists = [[] for i in range(0, self.num_b +1)]
        self.book.main.write(2, 8, self.num_s, self.book.style1)
        for k in range(self.num_a, self.num_b +1):
            filename = pt.join(self.path, self.pre + str(k).zfill(3)+ '.tif')                           # 文件名,zfill 用0填充空位数
            image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)                               # 使用灰度形式读入，第三维为单一数值，二位位置数组
            # w,h = image.shape[::-1]
            # print(len(image[image[:,:]==0]))        # black
            # print(len(image[image[:,:]==255]))      # white

            X = self.Position(image)
            eps=3                                                                           # eps步进数，小于这个数被判定为相邻的点
            min_Pts=2
                        
            begin = time.time()
            C = self.dbscan(X, eps, min_Pts)
            end = time.time()
            plt.figure(figsize=(12, 9), dpi=80)
            plt.scatter(X[:,0], X[:,1], c = C)
            plt.xlim(-0.5, 1.5 * self.num_w)
            plt.xlim(-0.5, 1.5 * self.num_h) 
            plt.savefig(self.savedpath + '\\Processed_'+ self.pre + str(k).zfill(3) + '.tif')
            
            new_C = list(set(C))                                                            # 裂纹编号
            new_C.sort(key=C.index)
            #A=[]
            # 数据写入
            self.book.Creat_sheet(k)
            self.Write_sheet(k - self.num_a + 1, len(new_C)-1, len(C))
            
            for i in new_C[:-1]:
                lists[k].append(C.count(i))

        self.Write_result()
        self.book.save(self.savedpath + '\\Crack_stastistics.xls')
        print('over, destroy')
        self.root.destroy()
    
    # 模型中的功能函数
    def Position(self, image):
        Position = [[0,0]]                                                              # 找出黑点位置，并记录在其中
        for i in range(0, self.num_w):
            for j in range(0, self.num_h):
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
       
        
        
    # Excel 数据写入
    def Write_pre(self):
        pass
   
    def Write_sheet(self, k, CC, CLP):
        # 'Fig_num', 'Crack_count', 'Crack_len/pixel',  'Crack_len/um', 'Ave_len/um', 'Plane_density'
        self.book.main.write(k+1, 0, k, self.book.style1)
        self.book.main.write(k+1, 1, CC, self.book.style1)
        self.book.main.write(k+1, 2, CLP, self.book.style1)
        fomula_CL = 'C' + str(k+2) +'*I3'
        fomula_AL = 'D' + str(k+2) +'/B' +str(k+2)
        fomula_PD = 'D' + str(k+2) +'/M4'
        self.book.main.write(k+1, 3, xlwt.Formula(fomula_CL), self.book.style1)
        self.book.main.write(k+1, 4, xlwt.Formula(fomula_AL), self.book.style1)
        self.book.main.write(k+1, 5, xlwt.Formula(fomula_PD), self.book.style1)
    
    def Write_result(self):
        # 图像数和总面积
        self.book.main.write(4, 8, xlwt.Formula('MAX(A3:A999)'), self.book.style_data)
        areaA = str(self.num_h) + '*' + str(self.num_w) + '*I5'
        area0 = '(' + str(self.num_h) + '*' + str(self.num_w) + ')*I3^2'
        self.book.main.write(2, 12, xlwt.Formula(areaA), self.book.style_data)
        self.book.main.write(3, 12, xlwt.Formula('M3*I3^2'), self.book.style_data)
        self.book.main.write(4, 12, xlwt.Formula('M4/10^6'), self.book.style_data)
        self.book.main.write(1, 13, xlwt.Formula(area0), self.book.style_data)
        
        self.book.main.write(2, 9, xlwt.Formula('SUM(D3:D999)'), self.book.style_data)
        self.book.main.write(4, 9, xlwt.Formula('SUM(B3:B999)'), self.book.style_data)
        self.book.main.write(2, 10, xlwt.Formula('J3/M5'), self.book.style_data)
        self.book.main.write(2, 11, xlwt.Formula('J5/M5'), self.book.style_data)
        
        # 误差计算
        self.book.main.write(2, 17, self.GB, self.book.style1)
        self.book.main.write(3, 17, xlwt.Formula('N2/ (PI()*(R3/2)^2)'), self.book.style1)
        self.book.main.write(4, 17, xlwt.Formula('R4*3*I5'), self.book.style1)
        self.book.main.write(5, 17, xlwt.Formula('R5*R3/2'), self.book.style1)
        self.book.main.write(6, 17, xlwt.Formula('J5/R5'), self.book.style1)
        self.book.main.write(7, 17, xlwt.Formula('SQRT(1/R5*(1-R7)/R7)*R7'), self.book.style1)
        self.book.main.write(8, 17, xlwt.Formula('R8/R7'), self.book.style1)
        self.book.main.write(9, 17, xlwt.Formula('1.96*R9'), self.book.style1)
        
        
        self.book.main.write(1, 20, xlwt.Formula('2*I3'), self.book.style1)
        self.book.main.write(2, 20, xlwt.Formula('SQRT(U2^2*J5)/J5'), self.book.style1)
        self.book.main.write(3, 20, xlwt.Formula('1.96*U3'), self.book.style1)
    
    
    
    def Pre_process(self):
        self.get_data()
        self.book = xlwrite.Book()
        self.savedpath = pt.join(self.path, 'Processed')
        folder = pt.exists(self.savedpath)
        if not folder:
        		makedirs(self.savedpath)
    
    def get_data(self):
        self.path = self.e1.get()
        self.pre = self.e21.get()
        
        str_a = self.e22.get()
        str_b = self.e23.get()
        str_x = self.e31.get()
        str_y = self.e32.get()
        str_s = self.e41.get()
        str_GB = self.e42.get()
        
        self.num_a = self.trans_number(str_a)
        self.num_b = self.trans_number(str_b)
        self.num_w = self.trans_number(str_x)
        self.num_h = self.trans_number(str_y)
        self.num_s = self.trans_number_fra(str_s)
        self.GB = self.trans_number_fra(str_GB)
        # print('num_a',num_a, 'num_b',num_b, 'num_x',num_x, 'num_y',num_y, 'num_s',num_s)
        
        # if num_a or num_b or num_x or num_y or num_s == False or '':
        #     tk.messagebox.showerror(title='Warning', message='Number printing is invalid, please insert a integer',)
        #     root.destroy()
        #     sys.exit(0)
        # self.root.destroy()
        # gui = GUI2()
            
    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            # sys.exit(0)
            
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
     
        # try:
        #     import unicodedata
        #     a = unicodedata.numeric(s)
        #     return a
        # except (TypeError, ValueError):
        #     pass
     
        return False

class GUI2():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("裂纹统计模型")# 设置标题
        
        self.text = tk.StringVar()
        self.text.set("正在统计，请耐心等候，此过程较长，关闭程序可能导致意外情况")
        self.label = tk.Label(self.root, textvariable=self.text)
        

        # self.button = tk.Button(self.root,text="Click to change text below",command=self.changeText)
        # self.button.pack()
        self.label.pack()


if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
    # print(app.path)
    
    
    













