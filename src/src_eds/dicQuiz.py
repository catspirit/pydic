'''
Created on 2012-11-20

@author: Catspirit
'''
from tkinter import *
from tkinter.filedialog import *
from run_student import *
from src_eds.starter import *

import shutil
import functools
import pyaudio
import wave

'''
The DicEdit Class
'''
class DicQuiz(Frame):
    def __init__(self, root, path, dicId, dicName):
        '''
        This class represents an quiz frame of a single dictionary. 
        The browse functions including browse and play sound of the 
        words in the dictionary. When finished the quiz, a message
        window would pump up to inform the performance of this quiz.
        
        >>> root = Tk()
        >>> DicBrowse(root,"../../resource","0000001","fruit").pack()
        >>> root.mainloop()
        '''
        self.root = root
        Frame.__init__(self,root)
        
        
        self.path = path
        self.dicId = dicId
        self.dicName = dicName
        self.word = ""
        self.wordId = ""
        self.definition = None
        self.currentIndex = 0
        
        
        self.dictionary = {}
        self.answer = {}
        
        #tvs to shown
        self.dicNameTv = StringVar()
        self.wordTv = StringVar()
        self.defTv = StringVar()
        
#        self.dicListB = None 
        self.dicList = []
        self.inits()
    
    def inits(self):
        '''
        main control method for init functions
        '''
        self.initTitle()
        self.initDicList()
        self.initWordFrame()
        if len(self.dicList) > 0:
            value = self.dicList[0]
            self.showWord(word=value, id=self.dictionary[value])
    
    def initTitle(self):
        '''
        Init the title and outer frame of the dictionary frame
        '''
        dicFrame = Frame(self, padx=5, pady=25, bd=1)
        Label(dicFrame, text="Dictionary Name: ", font=('TimesRoman', 18,'bold')).pack(side=LEFT)
        
        self.dicNameTv.set(self.dicName)
        Label(dicFrame, textvariable=self.dicNameTv, font=('TimesRoman', 20,'bold')).pack(side=LEFT)
        dicFrame.grid(row=0,column=0,columnspan=2,sticky="nsew")
        
        btnFrame = Frame(self, padx=20, pady=5)
        Button(btnFrame, text='Finish', width=15, command=self.onFinish).pack(side=RIGHT)
        Button(btnFrame, text='Forward', width=15, command=self.onForward).pack(side=RIGHT)
        Button(btnFrame, text='Backward', width=15, command=self.onBackward).pack(side=RIGHT)
        btnFrame.grid(row=2,column=0,columnspan=2,sticky="nsew")
    
    def initDicList(self):
        '''
        Read the dictionary list from words.cfg if there is one.
        Otherwise, create a new words.cfg file under the dictionary
        directory
        '''
        self.dictionary = {}
        
        try:
            f = open(self.path+"/"+self.dicId+"/words.cfg","r",encoding="utf-32")
        except:
            print("exception?")
            f = open(self.path+"/"+self.dicId+"/words.cfg", 'w',encoding="utf-32")
            self.maxDicNo = "0000001"
            f.write("maxNum,"+self.maxDicNo+"\n")
            return
        
        info = f.readline().replace('\n','').split(',')
        
        if len(info)!=2:
            print(info)
            return
        self.maxDicNo = info[1]
        
        for line in f:
            id, name = line.replace('\n','').split(',')
            self.dictionary[name] = id
            self.dicList.append(name)
#            self.dicListB.insert(END, name)
        
        f.close()
        
    def initWordFrame(self):
        '''
        Init the edit frame for single word in the dictionary
        '''
        wordFrame = Frame(self, padx=10, pady=10, relief=SUNKEN, bd=1)
        
        lbOpts = {'font': ('TimesRoman', 12,'bold')}
        Label(wordFrame, text="Word: ", **lbOpts).grid(row=0,column=0,sticky="w")
        
        Entry(wordFrame, width=15, bg="white", textvariable=self.wordTv, **lbOpts).grid(row=0,column=1,sticky="w")
#        Button(wordFrame, text="Play", command=self.onPlay, **lbOpts).grid(row=0,column=2,sticky="e",padx=5)
        
        Label(wordFrame, text="Def: ", **lbOpts).grid(row=1,column=0,sticky="wsen",pady=5)
        Label(wordFrame, textvariable=self.defTv, bg="white", width = 50, **lbOpts).grid(row=1,column=1,columnspan=3,sticky="nsew",pady=5)
        
        
        
        photo = PhotoImage()
        self.imageLb = Label(wordFrame, image=photo, height=320, width=400)
        self.imageLb.photo = photo  
        self.imageLb.pack_propagate(0) # don't shrink
        self.imageLb.grid(row=2,column=0,columnspan=4,sticky="s",padx=5,pady=10)


        wordFrame.grid(row=1,column=1,sticky="nsew")
        
    def showWord(self, word="", id=""):
        '''
        Show the word in word frame
        
        @param word:    name to be shown on the word frame
        @type word:     a string
        @param id:    the path of dictionary workspace
        @type id:     a string
        '''
        self.word = word
        try:
            self.wordTv.set(self.answer[word])
        except:
            self.wordTv.set("")
        self.wordId = id
        
        try:
            f = open(self.path+"/"+self.dicId+"/"+id+"/def","r",encoding="utf-32")
            self.definition = f.readline()
            self.defTv.set(self.definition)
        except:
            self.defTv.set("")
        
        try:
            imagePath = self.path +"/"+self.dicId+ "/"+id+"/pic.gif"
            photo = PhotoImage(file=imagePath)
        except:
            photo = PhotoImage()
            
        try:
            self.WAVE_OUTPUT_FILENAME = self.path +"/"+self.dicId+ "/"+id+"/record.wav"
        except:
            self.WAVE_OUTPUT_FILENAME = ""
        
        self.imageLb.configure(image = photo)
        self.imageLb.image = photo
        self.newImagepath = None
        
        
    def onFinish(self):
        '''
        pump out with the information of the performance of the quiz
        '''
        message = "solution\t\t\tyour answer \n"
        correct = 0
        
        keylist = self.dictionary.keys()
            
        for name in keylist:
            if name in self.answer:
                if name == self.answer[name]:
                    correct +=1
                message += name+'\t\t\t'+self.answer[name]+'\n'
            else:
                message += name+'\t\n'
        
        message += "\nYou've make "+str(correct)+" correct out of "+str(len(self.dictionary))
        
        self.alert = Tk()
        Message(self.alert, text=message, width=400).pack(side=TOP, pady=20)
        Button (self.alert, text="ok", command=self.onReturn, width=15).pack()
    
    def onReturn(self):
        '''
        Pass the frame back to the main entry with edited value
        '''
        self.alert.destroy()
        frameInfo = {'path': self.path,'frame':'DicEntry'}
        self.root.frameControl(frameInfo)
        self.destroy()
    
    def onForward(self):
        '''
        browse the next word on the list
        '''
        self.answer[self.dicList[self.currentIndex]] = self.wordTv.get()
        
        if self.currentIndex < len(self.dicList)-1:
            self.currentIndex += 1
        else:
            self.currentIndex = 0
        
        
        value = self.dicList[self.currentIndex]
        self.showWord(word=value, id=self.dictionary[value])
            
    
    def onBackward(self):
        '''
        browse the former word on the list
        '''
        self.answer[self.dicList[self.currentIndex]] = self.wordTv.get()
        
        if self.currentIndex > 0:
            self.currentIndex -= 1
        else:
            self.currentIndex = len(self.dicList)-1
            
        value = self.dicList[self.currentIndex]
        self.showWord(word=value, id=self.dictionary[value])
    
        
if __name__=='__main__':
        import doctest
        doctest.testmod()
    
