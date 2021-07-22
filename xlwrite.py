# -*- coding: utf-8 -*-
"""
Created on %2021-7-20s

@author: %Nathans

@File: %xlwrites

@Software: Spyder

E:\program_data\testprintout\saved.xls

"""

import xlwt

class Book():
    def __init__(self):
        self.wb = xlwt.Workbook()
        self.main = self.wb.add_sheet('main')
        self.Title_style()
        self.Main_title()
    
    # 设置几种字体
    def Title_style(self):
        
        font_title = xlwt.Font()
        font0 = xlwt.Font()
        font1 = xlwt.Font()
        font_data = xlwt.Font()
        
        font0.name = 'Times New Roman'
        font0.bold = True
        font0.height = 20*11
        
        font1.name = 'Times New Roman'
        font1.height = 20*10
        
        font_title.name = 'Arial'
        font_title.bold = True
        font_title.height = 20*16
        
        center = xlwt.Alignment() # Create Alignment
        center.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
        center.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED

        
        
        self.style0 = xlwt.XFStyle()
        self.style0.font = font0
        
        self.style_title = xlwt.XFStyle()
        self.style_title.font = font_title
        self.style_title.alignment = center # Add Alignment to Style
        
        self.style1 = xlwt.XFStyle()
        self.style1.font = font1
        
        self.style_data = xlwt.XFStyle()
        self.style1.font = font1
        self.style_title.alignment = center # Add Alignment to Style
    
    # 主页面抬头
    def Main_title(self):
        self.main.write_merge(0, 0, 0, 5, 'Crack Statistics -- Figure List', self.style_title)
        self.main.col(0).width = 2333
        self.main.col(1).width = 3333
        self.main.col(2).width = 3600
        self.main.col(3).width = 3333
        self.main.col(4).width = 3333
        self.main.col(5).width = 3333
        
        self.main.col(8).width = 3333
        self.main.col(9).width = 3333
        self.main.col(10).width = 6666
        self.main.col(11).width = 5555
        self.main.col(12).width = 3333
        self.main.col(13).width = 2333
        
        self.main.col(16).width = 9999
        self.main.col(17).width = 3333
        self.main.col(19).width = 9999
        self.main.col(20).width = 2333
        # headline
        self.main.write(1, 0, 'Fig_num', self.style0)
        self.main.write(1, 1, 'Crack_count', self.style0)
        self.main.write(1, 2, 'Crack_len(pixel)', self.style0)
        # self.main.write(1, 3, '总像素点', self.style0) #这个统计是否有必要
        self.main.write(1, 3, 'Crack_len(um)', self.style0)
        self.main.write(1, 4, 'Ave_len(um/n)', self.style0)
        self.main.write(1, 5, 'Plane_density', self.style0)
        
        self.main.write_merge(0, 0, 8, 13, 'Result_Calculation', self.style_title)
        self.main.write(1, 8, 'Scale(um/n)', self.style0)
        self.main.write(3, 8, 'Images', self.style0)
        self.main.write(1, 9, 'Lenth(um)', self.style0)
        self.main.write(3, 9, 'Number/n', self.style0)
        self.main.write(1, 10, 'Crack_length/area(um/mm^2)', self.style0)    #crack_len/area
        self.main.write(1, 11, 'Crack_density(n/mm^2)', self.style0)        #crack_num/area
        self.main.write(1, 12, 'Area', self.style0)
        self.main.write(2, 13, 'pixel^2', self.style1)
        self.main.write(3, 13, 'microns^2', self.style1)
        self.main.write(4, 13, 'mm^2', self.style1)
        
        
        self.main.write_merge(0, 0, 16, 17, 'Density Error Calculation', self.style_title)
        self.main.write(2, 16, 'N = 1/(stdev/p)^2 * (1-p)/p', self.style0)
        
        self.main.write(1, 16, 'Grain size/um', self.style1)
        self.main.write(3, 16, '# of grains/image = area of an image / area of a grain', self.style1)
        self.main.write(4, 16, "N = # of GB's = # of grains/image*3 * #of images", self.style1)
        self.main.write(5, 16, 'GB Length', self.style1)
        self.main.write(6, 16, 'p = number of cracks / # of GBs', self.style1)
        self.main.write(7, 16, 'sigma_p', self.style1)
        self.main.write(8, 16, 'Fractional error = sigma/p', self.style1)
        self.main.write(9, 16, '95% fractional error = 1.96*sigma/p', self.style1)
        
        
        self.main.write_merge(0, 0, 19, 20, 'Lenth Error Calculation', self.style_title)
        self.main.write(1, 19, 'sigma crack = 2 pixels', self.style1)
        self.main.write(2, 19, 'sigma avg = sqrt (sigma crack^2 * # of cracks) / # of cracks', self.style1)
        self.main.write(3, 19, '95% confidence interval', self.style1)
        
        

        
        
    def Write_sheet(self, namenum = 0):
        self.main.write(str(namenum))
        
    # 建新页面
    def Creat_sheet(self, namenum = 0): #sheetname show in excel, nameum used in this code
        exec('self.sheet = self.wb.add_sheet("sheet{}")'.format(namenum))
        title = 'Crack Statistics -- Figure ' + str(namenum)
        self.sheet.write_merge(0, 0, 0, 5, title, self.style_title)
        self.sheet.col(0).width = 3000
        self.sheet.col(1).width = 3333
        self.sheet.col(2).width = 3333
        self.sheet.col(3).width = 3333
        # headline
        self.sheet.write(1, 0, 'Crack_num', self.style0)
        self.sheet.write(1, 1, 'X', self.style0)
        self.sheet.write(1, 2, 'Y', self.style0)
        self.sheet.write(1, 3, 'lenth', self.style0)
        
    # 保存，使用小写save（）
    def save(self, address = r'Book_saved'):
        self.wb.save(address)
        
#     def name_sheet(self, )   
# for i in range(a,b+1):
#     exec('var{} = {}'.format(i, i))

if __name__ == '__main__':
    book = Book()
    book.save(r'E:\program_data\testprintout\saved.xls')







