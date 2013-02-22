'''
Created on 2012-11-14

@author: Catspirit
'''
from tkinter import *
import functools
from tkinter.filedialog import *
from src_eds.dicEntry import *
from src_eds.dicBrowse import *
from src_eds.dicQuiz import *
from src_eds.starter import *

class runner(Tk):
    def frameControl(self, frameInfo):
        if frameInfo['frame']=='DicEntry':
            DicEntry(self,frameInfo['path']).pack()
        elif frameInfo['frame']=='DicBrowse':
            DicBrowse(self, frameInfo['path'], frameInfo['dicId'], frameInfo['dicName']).pack()
        elif frameInfo['frame']=='DicQuiz':
            DicQuiz(self, frameInfo['path'], frameInfo['dicId'], frameInfo['dicName']).pack()
        
            
            
if __name__=='__main__':
    root = runner()
    starter(root).pack()
    root.mainloop()
    