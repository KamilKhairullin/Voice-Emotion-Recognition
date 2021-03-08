import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
from audio_analyzer.neural_networks import MLPC
from audio_analyzer.data_loading import DataLoader
from audio_analyzer.preprocessing.butterworth_filter import ButterworthFilter
from audio_analyzer.preprocessing.voice_activity_detection import VAD
from audio_analyzer.preprocessing.lib_vad import WebRtcVad
import numpy as np
import os


def deleteFiles(path):
    for r, d, f in os.walk(path):
        for file in f:
            os.remove(r + "/" + file)

def runVADExapmle(pathToWav):
    vad = VAD(pathToWav)
    vad.run()
    vad.smoothSpeechDetection()
    vad.approximation()
    vad.printOutput()
    return vad 


def action():
    pathToRecord = 'data/record1.wav'
    pathToCutted = 'data/cutted'
    pathToModel = 'model.pkl'
    pathToCuttedAndFiltered = 'data/cuttedAndFiltered'
    dataLoader = DataLoader('', 0.15)
    model = MLPC()
    a = ButterworthFilter()

    model.loadModel(pathToModel)

    print('Processing Voice activity detection...')
    x = WebRtcVad()
    x.test_process_file(pathToRecord)
    x.approximation()
    #x.printOutput()
    x.cutAndSave(pathToCutted, 0)
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
                return 'This voice is happy with probability {:.2f} %'.format(p[0] * 100)
            else:
                return 'This voice is sad with probability {:.2f} %'.format(p[1] * 100)
    deleteFiles(pathToCutted)
    deleteFiles(pathToCuttedAndFiltered)

