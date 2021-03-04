import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
from NeuralNetworks.MLPC import MLPC
from DataLoading.DataLoader import DataLoader
#from NeuralNetworks.CNN import CNN
from Preprocessing.ButterworthFilter import ButterworthFilter
from Preprocessing.Trimmer import Trimmer
import numpy as np
from Preprocessing.VoiceActivityDetection import VAD
import os

from Preprocessing.LibVAD import WebRtcVad
from GUI.Dictophone import Dictophone
from tkinter import *

def runCNNExample(pathToData):
    cnn = CNN(4)
    dataLoader = DataLoader(pathToData, 0.25)
    x_train,x_test,y_train,y_test = dataLoader.loadData()
    x_train,x_test,y_train,y_test = cnn.prepareData(x_train,x_test,y_train,y_test)
    cnn.fit(x_train, y_train, 45)
    y_pred = cnn.predict(x_test)
    cnn.printStats(y_test, y_pred)

def runMLPCExample(pathToData):
    mlpc = MLPC()
    dataLoader = DataLoader(pathToData, 0.25)
    x_train,x_test,y_train,y_test = dataLoader.loadData()
    mlpc.fit(x_train, y_train)
    y_pred = mlpc.predict(x_test)
    mlpc.printStats(y_test, y_pred)
    mlpc.saveModel('model.pkl')
    return mlpc

def runVADExapmle(pathToWav):
    vad = VAD(pathToWav)
    vad.run()
    vad.smoothSpeechDetection()
    vad.approximation()
    vad.printOutput()
    return vad 



def start():
	global label1, dictophone, start_b
	label1.config(text='Recording...')
	start_b.config(text='Pause', command=pause)
	dictophone.start_recording()


def resume():
	global label1, dictophone, start_b
	label1.config(text='Recording...')
	start_b.config(text='Pause', command=pause)
	dictophone.resume_recording()


def pause():
	global label1, dictophone, start_b
	label1.config(text='Paused')
	start_b.config(text='Resume', command=resume)
	dictophone.pause_recording()


def stop():
	global label1, dictophone, start_b
	label1.config(text='Press start to record')
	start_b.config(text='Start', command=start)
	dictophone.stop_recording()

def action():
    pathToRecord = 'DataFiles/Testing/record1.wav'
    pathToCutted = 'DataFiles/Testing/cutted'
    pathToModel = 'DataFiles/model.pkl'
    pathToCuttedAndFiltered = 'DataFiles/Testing/cuttedAndFiltered'
    dataLoader = DataLoader('', 0.15)
    model = MLPC()
    a = ButterworthFilter()

    model.loadModel(pathToModel)

    print('Processing Voice activity detection...')
    #x = WebRtcVad()
    #x.test_process_file(pathToRecord)
    #x.approximation()
    #x.printOutput()
    #x.cutAndSave(pathToCutted, 0)
    print('Voice activity detection completed. Voice cutted and saved.')

    for r, d, f in os.walk(pathToCutted):
        for file in f:
            tmpFile = pathToCutted + '/' + file
            tmpSave = pathToCuttedAndFiltered + '/' + file
            print('Removing noise...')
            a.removeNoise(tmpFile, tmpSave)
            #runVADExapmle(tmpSave)
            print('Noise removed.')

            test = dataLoader.extractFeature(tmpSave, mfcc=True, chroma=True, mel=True)
            test = test.reshape(1, 180)
            p = model.predict(np.array(test))
            p = np.squeeze(p)
            if(p[0] > p[1]):
                print('This is happy with probability {:.2f} %'.format(p[0] * 100))
            else:
                print('This is sad with probability {:.2f} %'.format(p[1] * 100))


master = Tk()
master.title = 'Voice recorder'
dictophone = Dictophone()

label1 = Label(master, text='Press start to record')
label1.grid(row=0, sticky=W, rowspan=5)

start_b = Button(master, text="Start", command=start)
start_b.grid(row=0, column=3, columnspan=2, ipadx = 50, ipady = 50, rowspan=2,
			 padx=25, pady=25)

stop_b = Button(master, text="Stop", command=stop)
stop_b.grid(row=0, column=5, columnspan=2, ipadx = 50, ipady = 50, rowspan=2,
			padx=25, pady=25)

stop_s = Button(master, text="Action", command=action)
stop_s.grid(row=0, column=70, columnspan=2,ipadx = 50, ipady = 50,rowspan=2,
			padx=25, pady=25)
master.mainloop()

