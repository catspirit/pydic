'''
Created on 2012-11-21

@author: Catspirit
'''
import pyaudio
import wave
import shutil

from tkinter import *
from tkinter.filedialog import *

#class Dictionary():
#    def __init__(self, id, name):
#        self.id = id
#        self.name = name
#        self.words = {}
    

#class World():
#    def __init__(self, id, name):
#        self.id = id
#        self.name = name

class Recorder(Frame):
    def __init__(self, root, infoTv):
        super().__init__(root)
        
        self.recordingNum = 1
        self.CHUNK = 1024
        self.RECORD_SECONDS = 3
        
        self.path = ""
        self.WAVE_OUTPUT_FILENAME = self.path + "/newRecord.wav"
        
        self.infoTv = infoTv
        self.initRecorder()
        
    def initRecorder(self):         
        saveFrame = Frame(self)
        saveFrame.pack(side=LEFT, pady=2)
        
        recordFrame = Frame(self,relief=RIDGE, bd=1)
        
        Entry(recordFrame, textvariable=self.infoTv, width=40, relief=GROOVE, bd=1).pack(side=LEFT, padx=2)
        Button(recordFrame, text="Start Recording", command=self.startRecord, width=12).pack(side=LEFT, pady=2)        
        recordFrame.pack(side=LEFT, padx=5, pady=2 )
    
    def setPath(self, path):
        self.recordingNum = 1
        self.infoTv.set("Please enter desired seconds to record")
        self.WAVE_OUTPUT_FILENAME = path + "/record.wav"
        self.path = path
    
    def startRecord(self):
        value = self.infoTv.get()
        try:
            self.RECORD_SECONDS = float(value)
        except:
            self.infoTv.set("Invalid Input!")
            return
        self.WAVE_OUTPUT_FILENAME = self.path + "/newRecord.wav"
        self.stepRecording()
        
        
    def stepRecording(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
        print("* recording")
        
        frames = []
        
        for i in range(0, int(RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        
        self.infoTv.set("done recording "+str(self.recordingNum))
        print("* done recording")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        self.recordingNum += 1
        
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    def onPlay(self):
        try:
            wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'rb')
        except:
            self.infoTv.set("No Recorded File!")
            return
            
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        data = wf.readframes(self.CHUNK)
        
        while data != '':
            stream.write(data)
            data = wf.readframes(self.CHUNK)
        
        stream.stop_stream()
        stream.close()
        
        p.terminate()
    
    def onSave(self):
        print("save Record!")
        if self.recordingNum >1:
            try:
                os.remove(self.path+"/record.wav")
            except:
                pass
            os.rename(self.path+"/newRecord.wav", self.path+"/record.wav")
        self.WAVE_OUTPUT_FILENAME = self.path + "/record.wav"
        
    def onSaveNew(self, path):
        print("save Record New!")
        if self.recordingNum > 1:
            print("TO SAVE!")
            print(self.path+"/record.wav")
            shutil.move(self.path+"/newRecord.wav", path+"/newRecord.wav")
            os.rename(path+"/newRecord.wav",path+"/record.wav")
        self.WAVE_OUTPUT_FILENAME = self.path + "/record.wav"
            
        
    def onCancel(self):
        try:
            os.remove(self.path+"/newRecord.wav")
        except:
            pass