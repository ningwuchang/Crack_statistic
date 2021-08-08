# -*- coding: utf-8 -*-
"""
Created on %2021-7-23s

@author: %Nathans

@File: %Starts

@Software: Spyder
"""

import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk
# import sys
import json
from calcthread import CalculateThread



class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
    
        self.title("裂纹统计模型")# 设置标题
        self.geometry("1000x200+0+0")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.foreground = 'black'
        self.background = 'lightgrey'
        self.text_foreground = 'black'
        self.text_background='white'
        
        self.menu_set()
        self.label_set()
        self.entery_set()
        # self.entery_preentery()
        # self.entery_stick()
        self.button_set()
        
        # self.bind_all("<Button-1>", self.on_closing())
    
    
    # 主页面的四个格式函数   
    def menu_set(self):
        # 最上方文件栏
        self.menu = tk.Menu(self, tearoff = 0, bg = 'lightgrey', fg = 'black')
        self.all_menus = [self.menu]
        
        sub_menu_items = ["file", "edit", "tools", "help"]
        self.generate_sub_menus(sub_menu_items)
        
        # self.configure(menu=self.menu)
        # self.filemenu = tk.Menu(self.menu, tearoff=0)
        # self.filemenu.add_command(label="Preference", command=self.Preference)
        # self.filemenu.add_command(label="Exit", command=self.destroy)
        # self.menu.add_cascade(label="File", menu=self.filemenu)
        # self.config(menu=self.menu)    
        
    def generate_sub_menus(self, sub_menu_items):
        window_methods = [method_name for method_name in dir(self)
                          if callable(getattr(self, method_name))]
        tkinter_methods = [method_name for method_name in dir(tk.Tk)
                           if callable(getattr(tk.Tk, method_name))]

        my_methods = [method for method in set(window_methods) - set(tkinter_methods)]
        my_methods = sorted(my_methods)

        for item in sub_menu_items:
            sub_menu = tk.Menu(self.menu, tearoff=0, bg=self.background, fg=self.foreground)
            matching_methods = []
            for method in my_methods:
                if method.startswith(item):
                    matching_methods.append(method)

            for match in matching_methods:
                actual_method = getattr(self, match)
                method_shortcut = actual_method.__doc__.strip()
                friendly_name = ' '.join(match.split('_')[1:])
                sub_menu.add_command(label=friendly_name.title(), command=actual_method, accelerator=method_shortcut)

            self.menu.add_cascade(label=item.title(), menu=sub_menu)
            self.all_menus.append(sub_menu)
            
    def label_set(self):
        # 设置标签
        ttk.Label(self, text='储存文件的路径：').grid(row=0, column=0)# 选项row代表行，column代表列
        ttk.Label(self, text='文件的前缀名称：').grid(row=1, column=0)
        ttk.Label(self, text='文件的编号是从：').grid(row=1, column=2)
        ttk.Label(self, text='到').grid(row=1, column=4)
        ttk.Label(self, text='水平像素：').grid(row=2, column=0)
        ttk.Label(self, text='垂直像素：').grid(row=2, column=2)
        ttk.Label(self, text='比例尺(微米/像素)：').grid(row=3, column=0)
        ttk.Label(self, text='晶粒尺寸：').grid(row=3, column=2)
        ttk.Label(self, text='微米').grid(row=3, column=4)
        
    def entery_set(self):
        # # 值获取
        # self.file_path = tk.StringVar()
        # self.file_pre = tk.StringVar()
        # self.file_start = tk.IntVar()
        # self.file_end = tk.IntVar()
        # self.file_weight = tk.IntVar()
        # self.file_high = tk.IntVar()
        # self.file_scale = tk.DoubleVar()
        # self.grain_size = tk.DoubleVar()
        
        # # 输入框
        # self.e1 = ttk.Entry(self, textvariable = self.file_path)
        # self.e21 = ttk.Entry(self, textvariable = self.file_pre)
        # self.e22 = ttk.Entry(self, textvariable = self.file_start)
        # self.e23 = ttk.Entry(self, textvariable = self.file_end)
        # self.e31 = ttk.Entry(self, textvariable = self.file_weight)
        # self.e32 = ttk.Entry(self, textvariable = self.file_high)
        # self.e41 = ttk.Entry(self, textvariable = self.file_scale)   
        # self.e42 = ttk.Entry(self, textvariable = self.grain_size)
        
        self.e1 = ttk.Entry(self)
        self.e21 = ttk.Entry(self)
        self.e22 = ttk.Entry(self)
        self.e23 = ttk.Entry(self)
        self.e31 = ttk.Entry(self)
        self.e32 = ttk.Entry(self)
        self.e41 = ttk.Entry(self)   
        self.e42 = ttk.Entry(self)

    # def entery_preentery(self):       
        # 预设文字
        with open("main.json", 'r', encoding='UTF-8') as f:
            preference = json.loads(f.read())
        self.e1.insert(0, preference['path'])
        self.e21.insert(0, preference['pre'])
        self.e22.insert(0, preference['start'])
        self.e23.insert(0, preference['end'])
        self.e31.insert(0, preference['weight'])
        self.e32.insert(0, preference['high'])
        self.e41.insert(0, preference['scale'])
        self.e42.insert(0, preference['grain_size'])
        
    # def entery_stick(self):
        # Grid允许我们使用表格的形式管理组件
        self.e1.grid(row=0, column=1, padx=20, pady=5, ipadx=270,
                     columnspan=5, sticky=tk.W)
        self.e21.grid(row=1, column=1, padx=10, pady=5)
        self.e22.grid(row=1, column=3, padx=10, pady=5)
        self.e23.grid(row=1, column=5, padx=10, pady=5)
        self.e31.grid(row=2, column=1, padx=10, pady=5)
        self.e32.grid(row=2, column=3, padx=10, pady=5)
        self.e41.grid(row=3, column=1, padx=10, pady=5)
        self.e42.grid(row=3, column=3, padx=10, pady=5)
        
    def button_set(self):
        # 使用Button按钮
        ttk.Button(self, text='开始分析', width=10, command=self.start_cal
                   ).grid(row=5, column=1, sticky=tk.E, padx=10, pady=5) 
        ttk.Button(self, text='退出程序', width=10, command=self.on_closing
                   ).grid(row=5, column=3, sticky=tk.E, padx=10, pady=5) 
        
    def changeText(self):
        self.text.set("Text updated")    
        
    def start_cal(self):
        # self.Pre_process()
        thread = CalculateThread(self)
        thread.start()
        
    
    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            # sys.exit(0)
            
    def Preference(self):
        preference = PreferenceGUI()
        preference.title('首选项')
        # preference.Button.remove()
        
   

class Processing(GUI):
    def __init__(self):
        self.root = tk.Tk()
        self.title("裂纹统计模型")# 设置标题
        
        self.text = tk.StringVar()
        self.text.set("正在统计，请耐心等候，此过程较长，关闭程序可能导致意外情况")
        self.label = tk.Label(self.root, textvariable=self.text)
        

        # self.button = tk.Button(self.,text="Click to change text below",command=self.changeText)
        # self.button.pack()
        self.label.pack()
        

class PreferenceGUI(GUI):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.title("裂纹统计模型")# 设置标题
        self.geometry("1000x200+0+0")
        self.text = tk.StringVar()
        self.text.set("正在统计，请耐心等候，此过程较长，关闭程序可能导致意外情况")
        self.label = tk.Label(self.root, textvariable=self.text)
        

        # self.button = tk.Button(self.,text="Click to change text below",command=self.changeText)
        # self.button.pack()
        self.label.pack()



if __name__ == '__main__':
    app = GUI()
    app.mainloop()
    # print(app.file_path)
    
    
    













