'''
Created on 2012-11-20

@author: Catspirit
'''

from tkinter import *
from src_eds.dicEntry import*
import unittest

'''
The TestDicEntry Class
'''
class TestDicEntry(unittest.TestCase):
        '''
        This class represents a test case for DicEntry frame
        '''
        def testInitDicEntry(self):
                '''
                Test opening a window for dicEntry
                '''
                root = Tk()
                dicEntry = DicEntry(root,"../../resource")
                dicEntry.pack()
                self.failIf(dicEntry == None)
                root.mainloop()
        
        def testAskdirectory(self):
                '''
                Test pumping up a window to choose directory
                '''
                root = Tk()
                dicEntry = DicEntry(root,"../../resource")
                dicEntry.pack()
                root.mainloop()
                path = dicEntry.askdirectory()
                self.failIf(path == None)

        def testAskopenfile(self):
                '''
                Test pumping up a window to choose file end with ".dicbook"
                '''
                root = Tk()
                dicEntry = DicEntry(root,"../../resource")
                dicEntry.pack()
                root.mainloop()
                path = dicEntry.askopenfilename()
                self.failIf(path == None)

if __name__=="__main__":
        unittest.main()
