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

'''
The runner Class
'''
class runner(Tk):
    '''
    This class represents a main controller for the teacher client
    '''
    def frameControl(self, frameInfo):
        '''
        read the info passed back from the front and pass to the handling frame
        
        @param frameInfo:    a dictionary of information to be processed
        @type frameInfo:     a dictionary
        '''
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
    
    

    
