'''
Created on 2012-11-20

@author: Catspirit
'''
from tkinter import *
from tkinter.filedialog import *
from run_teacher import *

import shutil
import zipfile
import functools

class DicEntry(Frame):
    def __init__(self, root, path):
        '''
        >>> root = Tk()
        >>> DicEntry(root,"../../resource").pack()
        '''
        self.root = root    
        Frame.__init__(self,root)
        
        self.maxDicNo = None
        self.path = path
        self.dictionary = {}
        self.dicId = None
        self.dicName = None
        
        Label(self, text="List of Dictionaries", font=('TimesRoman', 20,'bold'),justify=LEFT).pack(side=TOP, pady=10)
        
        self.initDicListFrame()
        self.initEditFrame()
        
    
    def initDicListFrame(self):
        listFrame = Frame(self, padx=5, pady=5)
        
        self.dicListB = Listbox(listFrame, height=10, width=30, font=('TimesRoman', 20))
        self.dicListB.bind("<Double-Button-1>", self.onSelect)
        
        scroll = Scrollbar(listFrame, command=self.dicListB.yview)
        self.dicListB.configure(yscrollcommand=scroll.set)
        self.dicListB.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)        
        
        listFrame.pack(side=LEFT)
        self.initDicList()
        
    def initDicList(self):
        self.dicListB.delete(0, END)
        self.dictionary = {}
        
        try:
            f = open(self.path+"/directory.cfg","r",encoding="utf-32")
            info = f.readline().replace('\n','').split(',')
        except:
            f = open(self.path+"/directory.cfg", 'w',encoding="utf-32")
            self.maxDicNo = "%07d" % 1
            
            return
            
        if len(info)!=2:
            print(info)
            return
        self.maxDicNo = info[1]
        
        for line in f:
            id, name = line.replace('\n','').split(',')
            self.dictionary[name] = id
            self.dicListB.insert(END, name)
        
    def initEditFrame(self):
        btnFrame = Frame(self)
        
        # options for buttons
        btnOpts = {'fill': constants.BOTH, 'padx': 20, 'pady': 5}
        
        Button(btnFrame, text='Create', command=self.onCreate, width=20, font=('TimesRoman', 15)).pack(**btnOpts)
        Button(btnFrame, text='Edit', command=self.onEdit, width=20, font=('TimesRoman', 15)).pack(**btnOpts)
        Button(btnFrame, text='Delete', command=self.onDelete, width=20, font=('TimesRoman', 15)).pack(**btnOpts)
        Label(btnFrame).pack(**btnOpts)
        Button(btnFrame, text='Import', command=self.onImport, width=20, font=('TimesRoman', 15)).pack(**btnOpts)
        Button(btnFrame, text='Export', command=self.onExport, width=20, font=('TimesRoman', 15)).pack(**btnOpts)
        Button(btnFrame, text='Quit', command=self.root.quit, width=20, font=('TimesRoman', 15)).pack(**btnOpts)
        
        btnFrame.pack(side=RIGHT)
    
    def onSelect(self,event):
        # Note here that Tkinter passes an event object to onSelect()
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.dicId = self.dictionary[value]
        self.dicName = value
        print('You dicId item %d: "%s"' % (index, value))
    
    def onDelete(self):
        try:
            dirName = self.path +"/"+self.dicId+ "/"
        except:
            alert = Tk()
            Message(alert, text="Please double click to select your dictionary!", width=400).pack(side=TOP, pady=20)
            Button (alert, text="ok", command=alert.destroy, width=15).pack()
            return
            
        shutil.rmtree(dirName)
        
        self.dictionary.pop(self.dicName)
        self.rewriteDicCfg()
        self.initDicList()
        
        self.dicId = None
        self.dicName = None
    
    def onCreate(self):
        self.dicId = self.maxDicNo
        self.maxDicNo = "%07d" %(int(self.maxDicNo)+1)
        self.dicName = "newDic"+self.dicId
        
        i=1
        while self.dicName in self.dictionary:
            self.dicName += "(+"+str(i)+")"
            i += 1

        self.dictionary[self.dicName] = self.dicId
        
        dirName = self.path +"/"+self.dicId+ "/"
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        
        self.rewriteDicCfg()
        self.onEdit()
    
    def onEdit(self):
#        DicEdit(self.root, self.path, self.dicId).pack()
        try:
            frameInfo = {'path': self.path,'frame':'DicEdit', 'dicId':self.dicId, 'dicName':self.dicName}
            print(frameInfo)
            self.root.frameControl(frameInfo)
            self.destroy()
        except :
            alert = Tk()
            Message(alert, text="Please double click to select your dictionary!", width=400).pack(side=TOP, pady=20)
            Button (alert, text="ok", command=alert.destroy, width=15).pack()
    
    def onExport(self):
        if self.dicId == None or self.dicName == None:
            alert = Tk()
            Message(alert, text="Please double click to select your dictionary!", width=400).pack(side=TOP, pady=20)
            Button (alert, text="ok", command=alert.destroy, width=15).pack()
            return
        
        try:
            dicDir = self.path +"/"+self.dicId
        except:
            alert = Tk()
            Message(alert, text="Please double click to select your dictionary!", width=400).pack(side=TOP, pady=20)
            Button (alert, text="ok", command=alert.destroy, width=15).pack()
            return
    
        dst = self.askdirectory()
        if dst == "":
            return
        dicFile = open(dicDir+"/dicInfo.dicInfo", 'w',encoding="utf-32")
        dicFile.write(self.dicName)
        dicFile.close()
        
        self.create_zip(dicDir, "dicContent", self.dicId+".dicbook")

        src = os.getcwd()+"\\"+self.dicId+".dicbook"
        src = src.replace("\\",'/')
        print(src)
        
        shutil.move(src, dst)
        
        os.remove(dicDir+"/dicInfo.dicInfo")
    
    def onImport(self):
        zipfilepath = self.askopenfilename()
        
        if zipfilepath == "":
            return
        
        zip = zipfile.ZipFile(zipfilepath)
        zip.extractall(path=self.path)
        
        f = open(self.path+"/dicContent/dicInfo.dicInfo","r",encoding="utf-32")
        newDicName = f.readline().replace('\n','')
        f.close()
        
        if newDicName in self.dictionary:
            print("Identical dicName!")
            shutil.rmtree(self.path+"/dicContent")
            return
            
        newDicId = self.maxDicNo
        self.maxDicNo = "%07d" %(int(self.maxDicNo)+1)
        
        self.dictionary[newDicName] = newDicId
        os.remove(self.path+"/dicContent/dicInfo.dicInfo")
        os.rename(self.path+"/dicContent", self.path+"/"+newDicId)
        
        self.rewriteDicCfg()
        self.initDicList()
    
    def onChanged(self, origin, updated):
        if origin in self.dictionary:
            # for existing 
            id = self.dictionary.pop(origin)
            self.dictionary[updated] = id
        else:
            print("dictionary does not exist!")
            
        
        self.rewriteDicCfg()
        self.initDicList()
        
    def rewriteDicCfg(self):
        #rewrite configure file according to directory
        dicFile = open(self.path+"/directory.cfg", 'w',encoding="utf-32")
        dicFile.write("maxNum,"+self.maxDicNo+"\n")
            
        keylist = sorted(self.dictionary.keys())
            
        for name in keylist:
            dicFile.write(self.dictionary[name]+","+name+"\n")
        print("Change happened on Dictionary!")
            
        dicFile.close()
    
    def zipfolder(self, path, relname, archive):
        paths = os.listdir(path)
        for p in paths:
            p1 = os.path.join(path, p) 
            p2 = os.path.join(relname, p)
            if os.path.isdir(p1): 
                self.zipfolder(p1, p2, archive)
            else:
                archive.write(p1, p2) 

    def create_zip(self, path, relname, archname):
        archive = zipfile.ZipFile(archname, "w", zipfile.ZIP_DEFLATED)
        if os.path.isdir(path):
            self.zipfolder(path, relname, archive)
        else:
            archive.write(path, relname)
        archive.close()
    
    def askdirectory(self):
        '''
        >>> root = Tk()
        >>> dicEntry = DicEntry(root,"../../resource")
        >>> dicEntry.pack()
        >>> dicEntry != None
        True
        >>> path  = dicEntry.askdirectory() # doctest: +ELLIPSIS
        [...]
        >>> path != None
        True
        '''
        dirOpts = {}
        dirOpts['mustexist'] = False
        dirOpts['parent'] = self
        dirOpts['title'] = 'This is a title'
        directory = askdirectory(**dirOpts)
        print(directory)
        
        return directory
    
    def askopenfilename(self):
        '''
        >>> root = Tk()
        >>>  
        >>> dicEntry = DicEntry(root,"../../resource")
        >>> dicEntry.pack()
        >>> dicEntry != None
        True
        >>> path = dicEntry.askopenfilename() # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE  
        [...]
        >>> path != None
        True
        '''
        fileOpts = {}        
        fileOpts['defaultextension'] = '.dicbook'
        fileOpts['filetypes'] = [('dictionary', '.dicbook')]
        fileOpts['title'] = 'Import Dictionary'
    
        output = askopenfilename(**fileOpts)
        return output
        
if __name__=='__main__':
    import doctest
    OC = doctest.OutputChecker
    class AEOutputChecker(OC):
        def check_output(self, want, got, optionflags):
                from re import sub
                if optionflags & doctest.ELLIPSIS:
                        want = sub(r'\[\.\.\.\]', '...', want)
                return OC.check_output(self, want, got, optionflags)
    doctest.OutputChecker = AEOutputChecker
    doctest.testmod()
