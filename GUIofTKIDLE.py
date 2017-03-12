#coding:utf-8
from Tkinter import *
from TKIDLE import *
from tkMessageBox import *

class GUIofTKIDLE:              #GUI界面
    def __init__(self):
        self.root=Tk() 
        self.root.title('TK-IDLE')
        root = self.root
        
        root.geometry('600x400')
        root.resizable(False, False)          
         
        self.createMenuBefore()           #生成菜单
        
        self.root.mainloop()
                    
        
    def createMenuBefore(self):           #生成project菜单，包含New和About两项
        root=self.root
        self.m = Menu(root)
        root.config(menu = self.m)
        self.promenu = Menu(self.m)
        self.m.add_cascade(label = 'Project', menu = self.promenu)
        self.promenu.add_command(label = 'New' , command = self.start)
        self.promenu.add_command(label = 'About' , command = self.about)
        
        
    def start(self):                     #New项新建一个项目，由TKIDLE类来运行                               
        self.promenu.entryconfig(1, state=DISABLED)
        myTKIDLE = TKIDLE(self.root,self.m)
        
        
    def about(self):                    #关于信息
        showinfo('程序设计思想与方法大作业','powered by 李冠宇\n学号：5130209367')
