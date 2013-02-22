'''
Created on 2012-11-20

@author: Catspirit
'''
from tkinter import *
from tkinter.filedialog import *
from run_teacher import *
from src_edt.starter import *
from src_edt.elements import *

import shutil
import functools
import pyaudio
import wave

'''
The DicEdit Class
'''
class DicEdit(Frame):
    '''
    This class represents an edit frame of a single dictionary. 
    The edit functions including add/delete words, edit and view
    name, definition, picture and record of words. Also, the name
    of dictionary can is edible through this class.
    '''
    
    def __init__(self, root, path, dicId, dicName):
        '''
        initialize the class
        
        @param root:    the parent container of this frame
        @type root:     a Tk widget
        @param path:    the path of dictionary workspace
        @type path:     a string
        @param dicId:   the id of current dictionary to edit
        @type dicId:    a string
        @param dicName: the name of current dictionary to edit
        @type dicName:  a string
        
        >>> root = Tk()
        >>> dicEdit = DicEdit(root,"../../resource","0000001","fruits")
        >>> dicEdit.pack()
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
        
        self.dictionary = {}
        
        #tvs to shown
        self.dicNameTv = StringVar()
        self.wordTv = StringVar()
        self.defTv = StringVar()
        self.infoTv = StringVar()
        
        
        self.dicListB = None
        self.newImagePath = None
        self.maxDicNo =None
        self.recorder =None
        
        self.inits()
    
    def inits(self):
        '''
        main control method for init functions
        '''
        self.initTitle()
        self.initDicListFrame()
        self.initWordFrame()
    
    def initTitle(self):
        '''
        Init the title and outer frame of the dictionary edit frame
        '''
        dicFrame = Frame(self, padx=5, pady=25, bd=1)
        Label(dicFrame, text="Dictionary Name: ", font=('TimesRoman', 18,'bold')).pack(side=LEFT)
        
        self.dicNameTv.set(self.dicName)
        Entry(dicFrame, textvariable=self.dicNameTv, font=('TimesRoman', 20,'bold')).pack(side=LEFT)
        dicFrame.grid(row=0,column=0,columnspan=2,sticky="nsew")
        
        btnFrame = Frame(self, padx=20, pady=5)
        Button(btnFrame, text='Cancel', width=15, command=self.onDicReturn).pack(side=RIGHT)
        Button(btnFrame, text='Ok', width=15, command=self.onOk).pack(side=RIGHT)
        Button(btnFrame, text='Add', width=10, command=self.onAddWord).pack(side=LEFT)
        Button(btnFrame, text='Delete', width=10, command=self.onDelete).pack(side=LEFT)
        btnFrame.grid(row=2,column=0,columnspan=2,sticky="nsew")
    
    def initDicListFrame(self):
        '''
        Init the frame for word list in dictionary
        '''
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
        '''
        Read the dictionary list from words.cfg if there is one.
        Otherwise, create a new words.cfg file under the dictionary
        directory
        '''
        self.dicListB.delete(0, END)
        self.dictionary = {}
        
        try:
            f = open(self.path+"/"+self.dicId+"/words.cfg","r",encoding = "utf-32")
        except:
            print("exception?")
            f = open(self.path+"/"+self.dicId+"/words.cfg", 'w',encoding = "utf-32")
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
        '''
        Init the edit frame for single word in the dictionary
        '''
        wordFrame = Frame(self, padx=10, pady=10, relief=SUNKEN, bd=1)
        
        lbOpts = {'font': ('TimesRoman', 12,'bold')}
        Label(wordFrame, text="Word: ", **lbOpts).grid(row=0,column=0,sticky="w")
        
        Entry(wordFrame, width=15, textvariable=self.wordTv, **lbOpts).grid(row=0,column=1,sticky="w")
        Button(wordFrame, text="Play", command=self.onPlay, **lbOpts).grid(row=0,column=2,sticky="e",padx=5)
        self.recorder = Recorder(wordFrame, self.infoTv)
        self.recorder.grid(row=0,column=3,sticky="w")   
        
        Label(wordFrame, text="Def: ", **lbOpts).grid(row=1,column=0,sticky="wsen",pady=5)
        Entry(wordFrame, textvariable=self.defTv, width = 50, **lbOpts).grid(row=1,column=1,columnspan=3,sticky="nsew",pady=5)
        
        
        
        photo = PhotoImage()
        self.imageLb = Label(wordFrame, image=photo, height=320, width=400)
        self.imageLb.photo = photo  
        self.imageLb.pack_propagate(0) # don't shrink
        self.imageLb.grid(row=2,column=0,columnspan=4,sticky="s",padx=5,pady=10)
        Button(wordFrame, text='Change Image', width=15, command=self.onChangePic).grid(row=3,column=0,columnspan=2, sticky="w")
        
        controlFr = Frame(wordFrame)
        Button(controlFr, text='Cancel', width=15, command=self.onWordCancel).pack(side=RIGHT)
        Button(controlFr, text='Apply', width=15, command=self.onWordApply).pack(side=RIGHT)
        controlFr.grid(row=4,column=3)
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
        self.wordTv.set(word)
        self.wordId = id
        
        try:
            f = open(self.path+"/"+self.dicId+"/"+id+"/def","r",encoding = "utf-32")
            self.definition = f.readline()
            self.defTv.set(self.definition)
        except:
            self.defTv.set("")
        
        try:
            imagePath = self.path +"/"+self.dicId+ "/"+id+"/pic.gif"
            photo = PhotoImage(file=imagePath)
        except:
            photo = PhotoImage()
            
        
        self.recorder.setPath(self.path +"/"+self.dicId+ "/"+id)
        
        self.imageLb.configure(image = photo)
        self.imageLb.image = photo
        self.newImagepath = None
    
    def onSelect(self,event):
        ''' 
        process the word that is selected in the listbox and pass to
        showWord function to show in word frame
        
        @param event: the action happened on tkinter
        @type event: an event        
        '''
        w = event.widget
        if len(w.curselection())<1:
            return
        index = int(w.curselection()[0])
        value = w.get(index)
        self.showWord(word=value, id=self.dictionary[value])
        
        print('You selected item %d: "%s"' % (index, value))
        print(self.dictionary[value])
        
        
    def onOk(self):
        '''
        Pass the frame back to the main entry with edited value
        '''
        if self.dicNameTv.get()!= self.dicName:
            frameInfo = {'path': self.path,'frame':'DicEntryChanged','origin':self.dicName,'updated':self.dicNameTv.get()}
        else:
            frameInfo = {'path': self.path,'frame':'DicEntry'}
            
        self.root.frameControl(frameInfo)
        self.destroy()
    
    def onDelete(self):
        '''
        Delete the word that is currently selected
        '''
        dirName = self.path +"/"+self.dicId+ "/"+self.wordId+"/"
        shutil.rmtree(dirName)
        
        self.dictionary.pop(self.word)
        self.rewriteWordCfg()
        self.initDicList()
        self.showWord()
        
    
    def onDicReturn(self):
        '''
        return to dictionary entry without any change
        '''
        frameInfo = {'path': self.path,'frame':'DicEntry'}
        self.root.frameControl(frameInfo)
        self.destroy()
    
    def onPlay(self):
        '''
        play the record
        '''
        self.recorder.onPlay()
    
    def onAddWord(self):
        '''
        set up for the new word and shown in the word frame to edit
        '''
        self.word = "new word"
        self.wordId = self.maxDicNo
        self.maxDicNo = "%07d" %(int(self.maxDicNo)+1)
#        self.maxDicNo =str(int(self.maxDicNo)+1)
        
        self.dictionary[self.word] = self.wordId
        self.rewriteWordCfg()
        
        dirName = self.path +"/"+self.dicId+ "/"+self.wordId+"/"
        os.makedirs(dirName)
        open( dirName+"def", 'w',encoding="utf-32").close
            
        self.showWord(self.word, self.wordId)
    
    def onChangePic(self):
        '''
        select the new gif picture for the word
        '''
        #set import filter
        impOpts = {}
        impOpts['defaultextension'] = '.gif'
        impOpts['filetypes'] = [('graph files', '.gif'),  ]
        impOpts['title'] = 'Import gif Picture'
        
        filename = askopenfilename(**impOpts)
        if not filename=="":
            photo = PhotoImage(file=filename)
            self.imageLb.configure(image = photo)
            self.imageLb.image = photo
            self.newImagePath = filename
    
    def onWordCancel(self):
        '''
        restore the change
        '''
        self.wordTv.set(self.word)
        self.defTv.set(self.definition)
        
        try:
            imagePath = self.path +"/"+self.dicId+ "/"+self.wordId+"/pic.gif"
            photo = PhotoImage(file=imagePath)
        except:
            photo = PhotoImage()
            
        self.imageLb.configure(image = photo)
        self.imageLb.image = photo
        self.newImagePath = imagePath
        
        self.recorder.onCancel()
    
    def onWordApply(self):
        '''
        apply and store the changes made to current word
        '''
        recorded = False
        #empty name not allowed
        if self.wordTv.get() == "":
            print("Word cannot be empty!")
            return
                
        #apply word name
        if self.word != self.wordTv.get():
            if self.wordTv.get() in self.dictionary:
                print("Word name already existed!")
                return
            elif self.word in self.dictionary: 
                self.dictionary.pop(self.word)
            
            #new word on initial
            if self.wordId == "":
                self.wordId = self.maxDicNo
                self.maxDicNo = "%07d" %(int(self.maxDicNo)+1)
                #create directory if it does not exist
                dirName = self.path +"/"+self.dicId+ "/"+self.wordId+"/"
                if not os.path.exists(dirName):
                    os.makedirs(dirName)
                self.recorder.onSaveNew(dirName)
                recorded = True
                
            self.word = self.wordTv.get()
            self.dictionary[self.word] = self.wordId
            
            self.rewriteWordCfg()
        
        #apply record if there is change
        if not recorded:
            self.recorder.onSave() 
        
               
        self.initDicList()
        
        #apply def
        if self.definition != self.defTv.get():
            print("Change happend on definition!")
            #create directory if it does not exist
            defFile = open( self.path +"/"+self.dicId+ "/"+self.wordId+"/"+"def", 'w',encoding="utf-32")
            defFile.write(self.defTv.get())
            defFile.close()
            
        #apply pic if there is change
        if self.newImagePath != None: 
            src = self.newImagePath
            dst = self.path +"/"+self.dicId+ "/"+self.wordId+"/pic.gif"
            shutil.copy(src, dst)
            self.newImagePath = None 
        
        self.showWord(self.word, id=self.dictionary[self.word])
        
    
    def rewriteWordCfg(self):
        '''
        rewrite configure file according to current directory
        '''
        wordFile = open(self.path+"/"+self.dicId+"/words.cfg", 'w',encoding="utf-32")
        wordFile.write("maxNum,"+self.maxDicNo+"\n")
            
        keylist = sorted(self.dictionary.keys())
            
        for name in keylist:
            wordFile.write(self.dictionary[name]+","+name+"\n")
        print("Change happend on word!")
            
        wordFile.close()
        
if __name__=='__main__':
   import doctest
   doctest.testmod()
    
