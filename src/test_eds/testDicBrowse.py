'''
Created on 2012-11-20

@author: Catspirit
'''
from src_eds.dicBrowse import *
from tkinter import *
import unittest

'''
The TestDicBrowse Class
'''
class TestDicBrowse(unittest.TestCase):
        '''
        This class represents a test case for DicBrowse frame
        '''
        def test_dicBrowse(self):
            '''
            Test opening a window for dicBrowse
            '''
            root = Tk()
            dicBrowse = DicBrowse(root,"../../resource","0000001","fruits")
            dicBrowse.pack()
            root.mainloop()

if __name__ == '__main__':
        unittest.main()
