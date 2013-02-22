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

'''
The runner Class
'''
class runner(Tk):
    '''
    This class represents a main controller for the student client
    '''
    def frameControl(self, frameInfo):
        '''
        read the info passed back from the front and pass to the handling frame
        
        @param frameInfo:    a dictionary of information to be processed
        @type frameInfo:     a dictionary
        '''
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
    