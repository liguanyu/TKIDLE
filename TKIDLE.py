#coding:utf-8
from Tkinter import *
from myComponent import *
from tkMessageBox import *
import os

class TKIDLE:           #TKIDLE类，包含主要程序
    def __init__(self,root,m):
        self.root = root
        self.m = m
        
        self.w = 600         #界面宽
        self.h = 400         #界面高
        
        self.createMenuAfter()
        
    def setRootTl(self):     #设置界面的高与宽的窗口界面
        self.roottl = Toplevel()
        tl = self.roottl
        Label(tl,text='width =').grid()
        Label(tl,text='height =').grid()
        self.wstr = StringVar()
        Entry(tl,textvariable = self.wstr).grid(row=0,column=1)
        self.wstr.set('600')
        self.hstr = StringVar()
        Entry(tl,textvariable = self.hstr).grid(row=1,column=1)
        self.hstr.set('400')
        self.frameBtn = Button(tl,text='确定',command = self.setRoot)
        self.frameBtn.grid(row=2,column=1)
        self.frameBtn.focus_set()
        tl.mainloop()
        
    def setRoot(self):       #设置界面的高与宽
        if (self.wstr.get() != '') and (self.hstr.get() != ''):
            self.w = eval(self.wstr.get())
            self.h = eval(self.hstr.get())
            self.root.geometry(str(self.w)+'x'+str(self.h))
            
            
            
    def createMenuAfter(self):         #创建菜单
        self.commenu = Menu(self.m)         #创建菜单，包含添加控件与设置界面长宽
        self.m.add_cascade(label = 'Component', menu = self.commenu)
        self.commenu.add_command(label = 'set width&height', command = self.setRootTl)
        self.commenu.add_command(label = 'add Button', command = self.addButton)
        self.commenu.add_command(label = 'add Label', command = self.addLabel)
        self.commenu.add_command(label = 'add Text', command = self.addText)
        self.commenu.add_command(label = 'add Entry', command = self.addEntry)
        self.commenu.add_command(label = 'add Checkbutton', command = self.addCheckbutton)
        self.commenu.add_command(label = 'add Radiobutton', command = self.addRadiobutton)
        self.allComponent = []
        
        self.outmenu = Menu(self.m)         #添加输出.py的菜单
        self.m.add_cascade(label = 'Output', menu = self.outmenu)
        self.outmenu.add_command(label = 'Output GUIofProject.py', command = self.outputPy)
        
    def addButton(self):                 #添加Button，创建一个myButton实例
        btn = myButton(self.root,len(self.allComponent))
        self.allComponent.append(btn)
        
    def addText(self):                   #添加Text，创建一个myText实例
        txt = myText(self.root,len(self.allComponent))
        self.allComponent.append(txt)
        
    def addEntry(self):                  #添加Entry,创建myEntry实例
        entry = myEntry(self.root,len(self.allComponent))
        self.allComponent.append(entry)
        
    def addLabel(self):                  #添加Label，创建myLabel实例
        lbl = myLabel(self.root,len(self.allComponent))
        self.allComponent.append(lbl)
        
    def addCheckbutton(self):            #添加checkbutton，创建myCheckbutton实例
        cbt = myCheckbutton(self.root,len(self.allComponent))
        self.allComponent.append(cbt)        
        
    def addRadiobutton(self):            #添加radiobutton，创建myRadiobutton实例
        rbt = myRadiobutton(self.root,len(self.allComponent))
        self.allComponent.append(rbt)        
        
        
    def outputPy(self):                  #输出.py文件
        #在目录下创建一个project文件夹，再创建或打开一个GUIofProject.py文件
        path = os.getcwd()               
        path = path + '\\project'
        if not os.path.exists(path):
            os.makedirs(path)
        self.GUIpy = open(path+'\\'+'GUIofProject.py','w')
        GUIpy = self.GUIpy
        
        #写.py文件的开头部分
        GUIpy.write('#coding:utf-8\n')
        GUIpy.write('from Tkinter import *\n')
        GUIpy.write('\nclass GUIofProject:\n')
        GUIpy.write('   def __init__(self):\n')
        GUIpy.write('       self.root = Tk()\n')
        GUIpy.write('       self.root.title(\'GUIofProject\')\n')
        GUIpy.write('       self.root.geometry(\''+str(self.w)+'x'+str(self.h)+'\')\n\n')
        
        
        #先创建所有Radiobutton所关联的variable变量
        self.allvariable = {}
        for cpnt in self.allComponent:
            variable = cpnt.radioVariable()
            if variable != -1:
                if not variable in self.allvariable.keys():
                    self.allvariable[variable] = 1
                    GUIpy.write('       self.' + variable + ' = IntVar()\n')
                    
        GUIpy.write('\n')
                
        #创建各个控件的代码，调用各控件的outputComponent函数
        for cpnt in self.allComponent:
            cpnt.outputComponent(self.GUIpy)
            
            variable = cpnt.radioVariable()       #如果该控件是Radiobutton，创建关于其variable的有关代码
            if variable != -1:
                GUIpy.write('       self.' + cpnt.property['name'] + '.config(variable = self.' + cpnt.property['variable'] + ',value = ' + str(self.allvariable[variable]) + ')\n')
                self.allvariable[variable] = self.allvariable[variable] + 1
               
            GUIpy.write('\n')
            
        GUIpy.write('       self.root.mainloop()\n')
            
        #创建各个button所调用的函数的代码   
        self.allCommand = []
        for cpnt in self.allComponent:
            command = cpnt.outputCommand()
            if command != -1:
                if not command in self.allCommand:
                    self.allCommand.append(command)
                    GUIpy.write('\n')
                    GUIpy.write('   def ' + command + '(self):\n')
                    GUIpy.write('       1#在此输入' + cpnt.property['name'] + '按钮功能\n')

            
        
        GUIpy.write('\n\na = GUIofProject()')
        
        GUIpy.close()
        
        showinfo('Output','输出成功，请查看本目录下project文件夹，并尽快拷贝以免后续输出覆盖')