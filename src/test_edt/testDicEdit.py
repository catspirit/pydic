'''
Created on 2012-11-20

@author: Catspirit
'''
from src_edt.dicEdit import *
from tkinter import *
import unittest

'''
The TestDicEdit Class
'''
class TestDicEdit(unittest.TestCase):
        '''
        This class represents a test case for DicEdit frame
        '''
        def test_dicEdit(self):
            '''
            Test opening a window for DicEdit
            ''' 
            root = Tk()
            dicEdit = DicEdit(root,"../../resource","0000001","fruits")
            dicEdit.pack()
            self.assertFalse(dicEdit==None)
            root.mainloop()

if __name__ == '__main__':
        unittest.main()
