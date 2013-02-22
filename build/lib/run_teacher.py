'''
Created on 2012-11-14

@author: Catspirit
'''
from tkinter import *
import functools
from tkinter.filedialog import *
from src_edt.dicEntry import *
from src_edt.dicEdit import *
from src_edt.starter import *

class runner(Tk):
    def frameControl(self, frameInfo):
        if frameInfo['frame']=='DicEntry':
            DicEntry(self,frameInfo['path']).pack()
        elif frameInfo['frame']=='DicEdit':
            DicEdit(self, frameInfo['path'], frameInfo['dicId'], frameInfo['dicName']).pack()
        elif frameInfo['frame']=='DicEntryChanged':
            w =  DicEntry(self,frameInfo['path'])
            w.onChanged(frameInfo['origin'], frameInfo['updated'])
            w.pack()
            
            
if __name__=='__main__':
    root = runner()
    starter(root).pack()
    root.mainloop()
    
    

    
