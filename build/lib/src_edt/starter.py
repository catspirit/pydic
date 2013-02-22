'''
Created on 2012-11-14

@author: Catspirit
'''
from tkinter import *
import functools
from tkinter.filedialog import *
from src_edt.dicEntry import *
from src_edt.dicEdit import *

class starter(Frame):
    def __init__(self, root):
        '''
        >>> root = Tk()
        >>> starter(root).pack()
        >>> root.mainloop()
        '''
        self.root = root
        Frame.__init__(self,root)
        Label(self, text="Select a workspace", font=('TimesRoman', 15,'bold'),justify=LEFT).pack(side=TOP)
        
        pathFr = Frame(self)
        pathFr.pack(side=TOP)
        Label(pathFr, text="Workspace:  ").pack(side=LEFT)
        self.path = StringVar()
        self.path.set("")
        Label(pathFr, textvariable=self.path, width="80", bg="white").pack(side=LEFT)
        Button(pathFr, text='Browse', command=self.askdirectory).pack(side=RIGHT)
        
        controlFr = Frame(self)
        controlFr.pack(side=BOTTOM)
        Button(controlFr, text='Cancel', width=20, command=root.quit).pack(side=RIGHT)
        Button(controlFr, text='ok', width=20, command=self.openEntry).pack(side=RIGHT)
        
        
    def askdirectory(self):
        dirOpts = {}
        dirOpts['mustexist'] = False
        dirOpts['parent'] = self
        dirOpts['title'] = 'This is a title'
        directory = askdirectory(**dirOpts)
        self.path.set(directory)
        print(self.path.get())
        
    def openEntry(self):
#        DicEntry(self.root,self.path.get()).pack()
        frameInfo = {'path': self.path.get(),'frame':'DicEntry'}
        self.root.frameControl(frameInfo)
        self.destroy()
        
        
if __name__=='__main__':
    import doctest
    doctest.testmod() 
    
