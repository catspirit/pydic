
'''
Created on 2012-11-20

@author: Catspirit
'''
from tkinter import *
from src_eds.dicQuiz import *
import unittest

'''
The TestDicQuiz Class
'''
class TestDicQuiz(unittest.TestCase):
        '''
        This class represents a test case for DicQuiz frame
        '''
        def testInit(self):
                '''
                Test opening a window for DicQuiz
                '''
                root = Tk()
                dicQuiz = DicQuiz(root,"../../resource","0000001","fruit")
                self.assertFalse(dicQuiz == None)
                dicQuiz.pack()
                root.mainloop()

if __name__ == "__main__":
        unittest.main()
