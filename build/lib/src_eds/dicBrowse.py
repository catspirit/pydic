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

class DicBrowse(Frame):
    def __init__(self, root, path, dicId, dicName):
        '''
        >>> from dicBrowse import *
        >>> root = Tk()
        >>> dicBrowse = DicBrowse(root,"../../resource","0000001","fruits")
        >>> dicBrowse.pack()
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
        self.currentIndex = -1
        
        
        self.dictionary = {}
        
        #tvs to shown
        self.dicNameTv = StringVar()
        self.wordTv = StringVar()
        self.defTv = StringVar()
        
        self.dicListB = None 
        self.inits()
    
    def inits(self):
        self.initTitle()
        self.initDicListFrame()
        self.initWordFrame()
    
    def initTitle(self):
        dicFrame = Frame(self, padx=5, pady=25, bd=1)
        Label(dicFrame, text="Dictionary Name: ", font=('TimesRoman', 18,'bold')).pack(side=LEFT)
        
        self.dicNameTv.set(self.dicName)
        Label(dicFrame, textvariable=self.dicNameTv, font=('TimesRoman', 20,'bold')).pack(side=LEFT)
        dicFrame.grid(row=0,column=0,columnspan=2,sticky="nsew")
        
        btnFrame = Frame(self, padx=20, pady=5)
        Button(btnFrame, text='Ok', width=15, command=self.onOk).pack(side=RIGHT)
        Button(btnFrame, text='Forward', width=15, command=self.onForward).pack(side=RIGHT)
        Button(btnFrame, text='Backward', width=15, command=self.onBackward).pack(side=RIGHT)
        btnFrame.grid(row=2,column=0,columnspan=2,sticky="nsew")
    
    def initDicListFrame(self):
        listFrame = Frame(self, padx=5, pady=5, relief=SUNKEN, bd=1)
        
        self.dicListB = Listbox(listFrame, height=27, width=20, font=('TimesRoman', 12))
        self.dicListB.bind("<Double-Button-1>", self.onSelect)
        
        scroll = Scrollbar(listFrame, command=self.dicListB.yview)
        self.dicListB.configure(yscrollcommand=scroll.set)
        self.dicListB.pack(side=LEFT,fill=X)
        scroll.pack(side=RIGHT, fill=Y)        
        
        listFrame.grid(row=1,column=0,sticky="nsew")
        
        self.initDicList()
        
    def initDicList(self):
        self.dicListB.delete(0, END)
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
            self.dicListB.insert(END, name)
        
        f.close()
        
    def initWordFrame(self):
        wordFrame = Frame(self, padx=10, pady=10, relief=SUNKEN, bd=1)
        
        lbOpts = {'font': ('TimesRoman', 12,'bold')}
        Label(wordFrame, text="Word: ", **lbOpts).grid(row=0,column=0,sticky="w")
        
        Label(wordFrame, width=15, bg="white", textvariable=self.wordTv, **lbOpts).grid(row=0,column=1,sticky="w")
        Button(wordFrame, text="Play", command=self.onPlay, **lbOpts).grid(row=0,column=2,sticky="e",padx=5)
        
        Label(wordFrame, text="Def: ", **lbOpts).grid(row=1,column=0,sticky="wsen",pady=5)
        Label(wordFrame, textvariable=self.defTv, bg="white", width = 50, **lbOpts).grid(row=1,column=1,columnspan=3,sticky="nsew",pady=5)
        
        
        
        photo = PhotoImage()
        self.imageLb = Label(wordFrame, image=photo, height=320, width=400)
        self.imageLb.photo = photo  
        self.imageLb.pack_propagate(0) # don't shrink
        self.imageLb.grid(row=2,column=0,columnspan=4,sticky="s",padx=5,pady=10)


        wordFrame.grid(row=1,column=1,sticky="nsew")
        

        
    def showWord(self, word="", id=""):
        self.word = word
        self.wordTv.set(word)
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
    
    def onSelect(self,event):
        # Note here that Tkinter passes an event object to onSelect()
        w = event.widget
        if len(w.curselection())<1:
            return
        index = int(w.curselection()[0])
        value = w.get(index)
        self.showWord(word=value, id=self.dictionary[value])
        
        self.currentIndex = index
        print('You selected item %d: "%s"' % (index, value))
        print(self.dictionary[value])
        
        
    def onOk(self):
        frameInfo = {'path': self.path,'frame':'DicEntry'}
        self.root.frameControl(frameInfo)
        self.destroy()
    
    def onPlay(self):
        CHUNK = 1024

        try:
            wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'rb')
        except:
            return
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        data = wf.readframes(CHUNK)
        
        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)
        
        stream.stop_stream()
        stream.close()
        
        p.terminate()
    
    def onForward(self):
        if self.currentIndex < self.dicListB.size()-1:
            self.currentIndex += 1
        else:
            self.currentIndex = 0
            
        value = self.dicListB.get(self.currentIndex)
        self.showWord(word=value, id=self.dictionary[value])
            
    
    def onBackward(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
        else:
            self.currentIndex = self.dicListB.size()-1
            
        value = self.dicListB.get(self.currentIndex)
        self.showWord(word=value, id=self.dictionary[value])
    
        
if __name__=='__main__':
    #root = runner()
    #DicBrowse(root,"E:/Workspace/EclipsePython/Educational Dictionary/s../../resource","0000001","fruit").pack()
    #root.mainloop()
    import doctest
    doctest.testmod()
    
    
