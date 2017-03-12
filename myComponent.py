#coding:utf-8
from Tkinter import *

class myComponent:           #各个控件都是myComponent类的子类
    def __init__(self,root,num):
        self.root = root
        root = self.root
        
        #初始化控件的一些基本参数，主要保存在property字典中
        self.property = {}
        self.property['name'] = ''
        self.property['num'] = num
        self.property['x'] = 0
        self.property['y'] = 0
        self.build = False
        self.outline = Frame(root,relief = 'groove',bd = 5)
        
        
        #这是有关于创建控件的方法，左键点击root的空白部分不放，移动鼠标会画出一个框，
        #表示控件的位置与大小，松开鼠标创建控件
        self.moveX = 0
        self.moveY = 0
        self.root.bind('<B1-Motion>',self.drawOutlineStart)
        self.root.bind('<ButtonRelease-1>',self.drawOutlineEnd)
        
        #创建按住鼠标时出现的框 ，代表控件的大小与位置
    def drawOutlineStart(self,event):
        if self.property['x'] == 0 and self.property['y'] == 0:
            self.outline.place(x = event.x, y = event.y, width = 1, height = 1)
            self.property['x'] = event.x
            self.property['y'] = event.y
        else:
            if event.x - self.property['x'] > 1 and event.y - self.property['y'] > 1:
                self.property['width'] = event.x - self.property['x']
                self.property['height'] = event.y - self.property['y']
                self.outline.place(width = self.property['width'],height = self.property['height'])
        
        #松开鼠标时，框消失，创建控件
    def drawOutlineEnd(self,event):
        if event.x - self.property['x'] > 1 and event.y - self.property['y'] > 1:
            self.property['width'] = event.x - self.property['x']
            self.property['height'] = event.y - self.property['y']
            self.outline.place_forget()
            self.createComponennt()
            if self.build:
                self.createRightMenu()
                self.root.bind('<B1-Motion>',self.doNothing)          #取消鼠标左键的绑定
                self.root.bind('<ButtonRelease-1>',self.doNothing)    #取消鼠标左键松开的绑定
                
                self.component.bind('<B1-Motion>',self.move)           #左键拖动控件改变位置
                self.component.bind('<ButtonRelease-1>',self.moveEnd)  #释放左键后改变一些临时值
       
    def move(self,event):          #左键拖动控件改变位置
        if self.moveX == 0 and self.moveY == 0:
            self.moveX = event.x_root 
            self.moveY = event.y_root
            self.initX = self.property['x']
            self.initY = self.property['y']
        else:
            self.property['x'] = self.initX + (event.x_root - self.moveX)
            self.property['y'] = self.initY + (event.y_root - self.moveY)
            self.component.place( x = self.property['x'],y= self.property['y'])
            self.root.update()
            
    def moveEnd(self,event):       #释放左键后改变一些临时值
        self.moveX = 0
        self.moveY = 0
       
        #创建控件后记录属性值        
    def createComponennt(self):
        self.property['font'] = self.component['font']
        self.property['fg'] = self.component['fg']
        
        
        #右键菜单，包括set property、set text、change size、delete四项
    def createRightMenu(self):
        self.rightMenu = Menu(self.root)
        self.rightMenu.add_command(label = 'set property', command = self.setProperty)
        self.rightMenu.add_command(label = 'set text', command = self.setText)
        self.rightMenu.add_command(label = 'change size', command = self.changeSize)
        self.rightMenu.add_command(label = 'delete', command = self.deleteComponent)
        self.component.bind('<Button-3>',self.rightMenuPop)
        
    def rightMenuPop(self,event):
        self.rightMenu.post(event.x_root,event.y_root)
        

        #设置控件显示文字的属性，包括文字，字体 ，颜色
    def setText(self):
        self.tl = Toplevel()
        tl = self.tl
        Label(tl,text='text =').grid()
        self.strText={}
        self.strText['text'] = StringVar()
        textEntry = Entry(tl,textvariable = self.strText['text'])
        textEntry.grid(row=0,column=1)
        self.strText['text'].set(self.property['text'])
        #Entry和Text的文字设置方式不同
        if self.property['kind'] == 'Text' or self.property['kind'] == 'Entry': 
            self.strText['text'].set('请直接在控件中修改')
            textEntry.config(state = 'disabled')
        
        Label(tl,text='font =').grid()
        self.strText['font'] = StringVar()
        Entry(tl,textvariable = self.strText['font']).grid(row=1,column=1)
        self.strText['font'].set(self.property['font'])
        
        Label(tl,text='字体颜色 =').grid()
        self.strText['fg'] = StringVar()
        Entry(tl,textvariable = self.strText['fg']).grid(row=2,column=1)
        self.strText['fg'].set(self.property['fg'])
        
        self.frameBtn = Button(tl,text='确定',command = self.setTextEnd)
        self.frameBtn.grid()
        self.frameBtn.focus_set()
        tl.mainloop()
        
        #设置好控件显示文本参数后，实现修改
    def setTextEnd(self):
        if (self.strText['text'].get() != '') and (self.property['kind'] != 'Text') and self.property['kind'] != 'Entry':
            self.property['text'] = self.strText['text'].get()
            self.component.config(text = self.property['text'])
        if (self.strText['font'].get() != ''):
            self.property['font'] = self.strText['font'].get()
            self.component.config(font = self.property['font'])
        if (self.strText['font'].get() != ''):
            self.property['fg'] = self.strText['fg'].get()
            self.component.config(fg = self.property['fg'])
        self.tl.destroy()
        
        #控件修改大小的方法，在右下角生成一个小方块，拖动小方块实现修改
    def changeSize(self):
        self.corner = Frame(self.root,relief = 'flat',bg = 'red')
        self.cornerX= self.property['x'] + self.property['width']
        self.cornerY = self.property['y'] + self.property['height']
        self.corner.place(x = self.cornerX,y = self.cornerY,anchor = SE,width = 10, height = 10)

        self.corner.bind('<B1-Motion>',self.changeSizeProcess)
        self.corner.bind('<ButtonRelease-1>',self.moveEnd)
        
        #拖动小方块实现大小变化        
    def changeSizeProcess(self,event):
        if self.moveX == 0 and self.moveY == 0:
            self.moveX = event.x_root 
            self.moveY = event.y_root
            self.initX = self.cornerX
            self.initY = self.cornerY
            self.initWidth = self.property['width']
            self.initHeight = self.property['height']
        else:
            self.cornerX = self.initX + (event.x_root - self.moveX)
            self.cornerY = self.initY + (event.y_root - self.moveY)
            self.property['width'] = self.initWidth + (event.x_root - self.moveX)
            self.property['height'] = self.initHeight + (event.y_root - self.moveY)
            self.component.place( width = self.property['width'],height= self.property['height'])
            self.corner.place(x = self.cornerX, y = self.cornerY)
            self.root.bind('<Button-1>',self.changeSizeEnd)
            self.root.update()
        
        #隐藏小方块
    def changeSizeEnd(self,event):
        self.corner.place_forget()
        self.root.bind('<Button-1>',self.doNothing)
        self.component.bind('<B1-Motion>',self.move)
        
        
        #删除控件的方法
    def deleteComponent(self):
        self.component.place_forget()
        self.build = False
        
        
        #通用的方法，让控件输出在.py中的有关代码
    def outputComponent(self,GUIpy):
        if self.build:
            GUIpy.write('       self.' + self.property['name'] + ' = ' + self.property['kind'] + '(self.root)\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(text = \'' + self.property['text'] + '\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(font = \'' + self.property['font'] + '\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(fg = \'' + self.property['fg']+'\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.place( x = ' + str(self.property['x']) + ',y = ' + str(self.property['y']) + ',width = ' + str(self.property['width']) + ',height = ' + str(self.property['height']) + ')\n')
        
        
        #如果控件是radiobutton，则会输出它的variable；否则输出-1。用来在生成的.py方便事先声明variable
    def radioVariable(self):
        if 'variable' in self.property.keys() and self.build and self.property['kind'] == 'Radiobutton':
            return self.property['variable']
        else:
            return -1
            
            
        #用来在.py的后面创建与相关按钮关联的函数
    def outputCommand(self):
        if 'command' in self.property.keys() and self.build:
            return self.property['command']
        else:
            return -1
        
        
        #为了覆盖已经不再需要的bind事件处理，写一个什么也不做的函数
    def doNothing(self,event):
        1
    
    
    
    #按钮的实现类
class myButton(myComponent):
    def __init__(self,root,num):
        myComponent.__init__(self,root,num)
       
    def createComponennt(self):
        self.property['name'] = 'Button' + str(self.property['num'])
        self.property['text'] = self.property['name']
        self.property['kind'] = 'Button'
        self.TKButton = Button(self.root,text = self.property['text'])
        
        self.TKButton.place( x = self.property['x'],y= self.property['y'],width = self.property['width'],height = self.property['height'])
        self.component = self.TKButton
        
        myComponent.createComponennt(self)
        self.property['command'] = self.property['name'] + 'command'
        
        self.build = True
        
        
        #设置按钮的属性，名字和关联的函数名
    def setProperty(self):
        self.tl = Toplevel()
        tl = self.tl
        Label(tl,text='name =').grid()
        self.newName = StringVar()
        Entry(tl,textvariable = self.newName).grid(row=0,column=1)
        self.newName.set(self.property['name'])
        
        Label(tl,text='command =').grid()
        self.newCommand = StringVar()
        Entry(tl,textvariable = self.newCommand).grid(row=1,column=1)
        self.newCommand.set(self.property['command'])
        
        Label(tl,text='请符合python变量命名规则').grid(columnspan = 2)
        
        self.frameBtn = Button(tl,text='确定',command = self.setPropertyEnd)
        self.frameBtn.grid()
        self.frameBtn.focus_set()
        tl.mainloop()
    
        #实现按钮属性的更改
    def setPropertyEnd(self):
        if (self.newName.get() != ''):
            self.property['name'] = self.newName.get()
        if (self.newCommand.get() != ''):
            self.property['command'] = self.newCommand.get()
        self.tl.destroy()
            
        
        #按钮输出.py需要额外输出关联命令的代码
    def outputComponent(self,GUIpy):
        myComponent.outputComponent(self,GUIpy)
        if self.build:
            GUIpy.write('       self.' + self.property['name'] + '.config(command = self.' + self.property['command'] + ')\n')
            
        
       #实现Text的类 
class myText(myComponent):
    def __init__(self,root,num):
        myComponent.__init__(self,root,num)
       
    def createComponennt(self):
        self.property['name'] = 'Text' + str(self.property['num'])
        self.property['text'] = self.property['name']
        self.property['kind'] = 'Text'
        self.TKText = Text(self.root)
        self.TKText.insert(END,self.property['name'])
        
        self.TKText.place( x = self.property['x'],y= self.property['y'],width = self.property['width'],height = self.property['height'])
        self.component = self.TKText
        
        myComponent.createComponennt(self)
        
        self.build = True
              
        #设置Text的属性，控件的名字
    def setProperty(self):
        self.tl = Toplevel()
        tl = self.tl
        Label(tl,text='name =').grid()
        self.newName = StringVar()
        Entry(tl,textvariable = self.newName).grid(row=0,column=1)
        self.newName.set(self.property['name'])
        
        Label(tl,text='请符合python变量命名规则').grid(columnspan = 2)
        
        self.frameBtn = Button(tl,text='确定',command = self.setPropertyEnd)
        self.frameBtn.grid()
        self.frameBtn.focus_set()
        tl.mainloop()
        
        #实现控件属性的更改    
    def setPropertyEnd(self):
        if (self.newName.get() != ''):
            self.property['name'] = self.newName.get()
        self.tl.destroy()
        
        #Text控件输出.py的代码需要保留其默认的文本    
    def outputComponent(self,GUIpy):
        if self.build:
            GUIpy.write('       self.' + self.property['name'] + ' = ' + self.property['kind'] + '(self.root)\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(font = \'' + self.property['font'] + '\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(fg = \'' + self.property['fg']+'\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.place( x = ' + str(self.property['x']) + ',y = ' + str(self.property['y']) + ',width = ' + str(self.property['width']) + ',height = ' + str(self.property['height']) + ')\n')
            
            self.property['text'] = self.component.get('1.0',END)
            self.property['text'] = self.property['text'][0:len(self.property['text'])-1]
            GUIpy.write('       self.' + self.property['name'] + '.insert(END,\'' + self.property['text'] + '\')\n')
            
        
        #Entry的实现
class myEntry(myComponent):
    def __init__(self,root,num):
        myComponent.__init__(self,root,num)
       
    def createComponennt(self):
        self.property['name'] = 'Entry' + str(self.property['num'])
        self.property['text'] = self.property['name']
        self.property['kind'] = 'Entry'
        self.entryStr = StringVar()
        self.TKEntry = Entry(self.root,textvariable = self.entryStr)
        self.entryStr.set(self.property['text'])
                
        self.TKEntry.place( x = self.property['x'],y= self.property['y'],width = self.property['width'],height = self.property['height'])
        self.component = self.TKEntry
        
        myComponent.createComponennt(self)
        self.property['textvariable'] = self.property['name'] + 'textvariable'
        
        self.build = True
        
        #修改Entry的属性，控件名称与关联的字符串变量
    def setProperty(self):
        self.tl = Toplevel()
        tl = self.tl
        Label(tl,text='name =').grid()
        self.newName = StringVar()
        Entry(tl,textvariable = self.newName).grid(row=0,column=1)
        self.newName.set(self.property['name'])
        
        Label(tl,text='textvariable =').grid()
        self.newTextvariable = StringVar()
        Entry(tl,textvariable = self.newTextvariable).grid(row=1,column=1)
        self.newTextvariable.set(self.property['textvariable'])
        
        Label(tl,text='请符合python变量命名规则').grid(columnspan = 2)        
        
        self.frameBtn = Button(tl,text='确定',command = self.setPropertyEnd)
        self.frameBtn.grid()
        self.frameBtn.focus_set()
        tl.mainloop()
        
        #实现Entry的属性修改
    def setPropertyEnd(self):
        if (self.newName.get() != ''):
            self.property['name'] = self.newName.get()
        if (self.newTextvariable.get() != ''):
            self.property['textvariable'] = self.newTextvariable.get()
        self.tl.destroy()
            
        #Entry在.py中的输出需要包含与字符串变量的关联
    def outputComponent(self,GUIpy):
        if self.build:
            GUIpy.write('       self.' + self.property['name'] + ' = ' + self.property['kind'] + '(self.root)\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(font = \'' + self.property['font'] + '\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(fg = \'' + self.property['fg']+'\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.place( x = ' + str(self.property['x']) + ',y = ' + str(self.property['y']) + ',width = ' + str(self.property['width']) + ',height = ' + str(self.property['height']) + ')\n')
            
            GUIpy.write('       self.' + self.property['textvariable'] + ' = StringVar()\n')        
            GUIpy.write('       self.' + self.property['name'] + '.config(textvariable = self.' + self.property['textvariable'] + ')\n')
            GUIpy.write('       self.' + self.property['textvariable'] + '.set(\'' + self.entryStr.get() + '\')')

        #Label类的实现
class myLabel(myComponent):
    def __init__(self,root,num):
        myComponent.__init__(self,root,num)
       
    def createComponennt(self):
        self.property['name'] = 'Label' + str(self.property['num'])
        self.property['text'] = self.property['name']
        self.property['kind'] = 'Label'
        self.TKLabel = Label(self.root,text = self.property['text'])
        
        self.TKLabel.place( x = self.property['x'],y= self.property['y'],width = self.property['width'],height = self.property['height'])
        self.component = self.TKLabel
        
        myComponent.createComponennt(self)
        
        self.build = True
        
        #修改Label的属性，控件名字
    def setProperty(self):
        self.tl = Toplevel()
        tl = self.tl
        Label(tl,text='name =').grid()
        self.newName = StringVar()
        Entry(tl,textvariable = self.newName).grid(row=0,column=1)
        self.newName.set(self.property['name'])
        
        Label(tl,text='请符合python变量命名规则').grid(columnspan = 2)
        
        self.frameBtn = Button(tl,text='确定',command = self.setPropertyEnd)
        self.frameBtn.grid()
        self.frameBtn.focus_set()
        tl.mainloop()
    
        #实现控件属性的更改
    def setPropertyEnd(self):
        if (self.newName.get() != ''):
            self.property['name'] = self.newName.get()
        self.tl.destroy()
            

        
       #checkbutton的实现的类 
class myCheckbutton(myComponent):
    def __init__(self,root,num):
        myComponent.__init__(self,root,num)
       
    def createComponennt(self):
        self.property['name'] = 'Checkbutton' + str(self.property['num'])
        self.property['text'] = self.property['name']
        self.property['kind'] = 'Checkbutton'
        self.TKCheckbutton = Checkbutton(self.root,text = self.property['text'])
        
        self.TKCheckbutton.place( x = self.property['x'],y= self.property['y'],width = self.property['width'],height = self.property['height'])
        self.component = self.TKCheckbutton
        
        myComponent.createComponennt(self)
        self.property['variable'] = self.property['name'] + 'variable'
        
        self.build = True
        
        #checkbutton的属性修改，控件名字与关联的variable变量
    def setProperty(self):
        self.tl = Toplevel()
        tl = self.tl
        Label(tl,text='name =').grid()
        self.newName = StringVar()
        Entry(tl,textvariable = self.newName).grid(row=0,column=1)
        self.newName.set(self.property['name'])
        
        Label(tl,text='variable =').grid()
        self.newVariable = StringVar()
        Entry(tl,textvariable = self.newVariable).grid(row=1,column=1)
        self.newVariable.set(self.property['variable'])
        
        Label(tl,text='请符合python变量命名规则').grid(columnspan = 2)
        
        self.frameBtn = Button(tl,text='确定',command = self.setPropertyEnd)
        self.frameBtn.grid()
        self.frameBtn.focus_set()
        tl.mainloop()
        
        #实现控件属性的更改
    def setPropertyEnd(self):
        if (self.newName.get() != ''):
            self.property['name'] = self.newName.get()
        if (self.newVariable.get() != ''):
            self.property['variable'] = self.newVariable.get()
        self.tl.destroy()
        
        #checkbutton输出到.py的代码需要额外实现与variable变量的关联    
    def outputComponent(self,GUIpy):
        if self.build:
            GUIpy.write('       self.' + self.property['name'] + ' = ' + self.property['kind'] + '(self.root)\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(font = \'' + self.property['font'] + '\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(fg = \'' + self.property['fg']+'\')\n')
            GUIpy.write('       self.' + self.property['name'] + '.place( x = ' + str(self.property['x']) + ',y = ' + str(self.property['y']) + ',width = ' + str(self.property['width']) + ',height = ' + str(self.property['height']) + ')\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(text = \'' + self.property['text'] + '\')\n')
            
            GUIpy.write('       self.' + self.property['variable'] + ' = IntVar()\n')
            GUIpy.write('       self.' + self.property['name'] + '.config(variable = self.' + self.property['variable'] + ')\n')

        
        
class myRadiobutton(myComponent):
    def __init__(self,root,num):
        myComponent.__init__(self,root,num)
       
    def createComponennt(self):
        self.property['name'] = 'Radiobutton' + str(self.property['num'])
        self.property['text'] = self.property['name']
        self.property['kind'] = 'Radiobutton'
        self.TKRadiobutton = Radiobutton(self.root,text = self.property['text'])
        
        self.TKRadiobutton.place( x = self.property['x'],y= self.property['y'],width = self.property['width'],height = self.property['height'])
        self.component = self.TKRadiobutton
        
        myComponent.createComponennt(self)
        self.property['variable'] = self.property['name'] + 'variable'
        
        self.build = True
        
        #radiobutton的属性修改，控件名字与关联的variable变量
    def setProperty(self):
        self.tl = Toplevel()
        tl = self.tl
        Label(tl,text='name =').grid()
        self.newName = StringVar()
        Entry(tl,textvariable = self.newName).grid(row=0,column=1)
        self.newName.set(self.property['name'])
        
        Label(tl,text='variable =').grid()
        self.newVariable = StringVar()
        Entry(tl,textvariable = self.newVariable).grid(row=1,column=1)
        self.newVariable.set(self.property['variable'])
        
        Label(tl,text='请符合python变量命名规则\nvariable相同的单选按钮为一组').grid(columnspan = 2)
        
        self.frameBtn = Button(tl,text='确定',command = self.setPropertyEnd)
        self.frameBtn.grid()
        self.frameBtn.focus_set()
        tl.mainloop()
    
        #实现radiobutton的属性修改
    def setPropertyEnd(self):
        if (self.newName.get() != ''):
            self.property['name'] = self.newName.get()
        if (self.newVariable.get() != ''):
            self.property['variable'] = self.newVariable.get()
        self.tl.destroy()
            