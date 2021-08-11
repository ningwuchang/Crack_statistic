# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s

@File: %(filename)s

@Software: Spyder
"""

import pandas as pd  #导入pandas库
import os
import matplotlib.pyplot as plt
# os.chdir(r'd:\Python\test')   #更改路径

data = pd.read_excel(r'E:\54055\Documents\test.xlsx',sheet_name = 'Data')         #注意后缀是xls还是xlsx

temp = data[['Avg LVDT (micron)', 'LVDT 2 (micron)', 
            'Stress1 (MPa)', 'Stress2 (MPa)', 
            'Stress3 (MPa)', 'Stress4 (MPa)'
            ]]
temp = temp.rename(columns={'Avg LVDT (micron)':'LVDT', 'LVDT 2 (micron)':'LVDT2', 
            'Stress1 (MPa)':'Stress1', 'Stress2 (MPa)':'Stress2', 
            'Stress3 (MPa)':'Stress3', 'Stress4 (MPa)':'Stress4'
            })

# 数据提取与清洗
temp = temp.drop(temp.loc[temp['Stress1'] == 0].index, axis = 0, inplace = False)
temp.reset_index(drop = True, inplace = True)

temp['LVDT'] = temp['LVDT'].map(lambda x: (3804.75 - x)/15000)
temp['LVDT2'] = temp['LVDT2'].map(lambda x: (3962.81 - x)/15000)

# 设置Trigger
period = 20
temp['Trigger'] = temp.index%period == period-1
LVDT = temp.LVDT.rolling(window=period, min_periods=0).agg(['mean'])
LVDT2 = temp.LVDT2.rolling(window=period, min_periods=0).agg(['mean'])
Stress1 = temp.Stress1.rolling(window=period, min_periods=0).agg(['mean'])
Stress2 = temp.Stress2.rolling(window=period, min_periods=0).agg(['mean'])
Stress3 = temp.Stress3.rolling(window=period, min_periods=0).agg(['mean'])
Stress4 = temp.Stress4.rolling(window=period, min_periods=0).agg(['mean'])

temp.loc[(temp.Trigger == True), ['mean']] = LVDT
temp = temp.rename(columns={'mean':'LVDT_means'})
temp.loc[(temp.Trigger == True), ['mean']] = LVDT2
temp = temp.rename(columns={'mean':'LVDT2_means'})
temp.loc[(temp.Trigger == True), ['mean']] = Stress1
temp = temp.rename(columns={'mean':'Stress1_means'})
temp.loc[(temp.Trigger == True), ['mean']] = Stress2
temp = temp.rename(columns={'mean':'Stress2_means'})
temp.loc[(temp.Trigger == True), ['mean']] = Stress3
temp = temp.rename(columns={'mean':'Stress3_means'})
temp.loc[(temp.Trigger == True), ['mean']] = Stress4
temp = temp.rename(columns={'mean':'Stress4_means'})

temp = temp.drop(temp.loc[temp['Trigger'] == False].index, axis = 0, inplace = False)


# 设置图框的大小
fig = plt.figure(figsize = (10,6))
# 绘图
plt.plot(temp.LVDT2_means, # x轴数据
         temp.Stress1_means, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'steelblue', # 折线颜色
        label = 'Stress1')
# 添加标题和坐标轴标签
plt.plot(temp.LVDT2_means, # x轴数据
         temp.Stress2_means, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'darkorange', # 折线颜色
         label = 'Stress2')
# 添加标题和坐标轴标签
plt.plot(temp.LVDT2_means, # x轴数据
         temp.Stress3_means, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'limegreen', # 折线颜色
         label = 'Stress3')
# 添加标题和坐标轴标签
plt.plot(temp.LVDT2_means, # x轴数据
         temp.Stress4_means, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'darkgray', # 折线颜色
         label = 'Stress4')
plt.legend()

# 添加标题和坐标轴标签
plt.title('Stress-Strain Curve')
plt.xlabel('Strain(%)')
plt.ylabel('Stress(MPa)')

# 剔除图框上边界和右边界的刻度
# plt.tick_params(top = 'off', right = 'off')

# 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
fig.autofmt_xdate(rotation = 45)

# 显示图形
plt.show()

