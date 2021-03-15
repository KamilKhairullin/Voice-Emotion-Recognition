from audio_analyzer.preprocessing.voice_activity_detection import VAD
from audio_analyzer.preprocessing.lib_vad import WebRtcVad
from audio_analyzer.preprocessing.butterworth_filter import ButterworthFilter
from audio_analyzer.neural_networks.MLPC import MLPC
from audio_analyzer.data_loading.data_loader import DataLoader
import numpy as np
import os
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=RuntimeWarning)


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


def runMLPCExample(pathToData):
    mlpc = MLPC()
    dataLoader = DataLoader(pathToData, 0.25)
    x_train, x_test, y_train, y_test = dataLoader.loadData()
    mlpc.fit(x_train, y_train)
    y_pred = mlpc.predict(x_test)
    mlpc.printStats(y_test, y_pred)
    mlpc.saveModel("threeEmotions")


def action():
    """
    path = 'dataset'
    pathToSave = 'normalizedDataset'
    a = ButterworthFilter()
    for r, d, f in os.walk(pathToSave):
        for file in f:
            tmpFile = r + '/' + file
            tmpSave = pathToSave + '/' + r.split(os.sep)[1] + '/' + file
            #a.normalize(tmpFile, tmpSave)
            a.emphasis(tmpFile, tmpFile)
            print(tmpSave)
    """
    pathToRecord = "data/record1.wav"
    pathToCutted = "data/cutted"

    pathToModel = "model.pkl"
    pathToCuttedAndFiltered = "data/cuttedAndFiltered"
    dataLoader = DataLoader("", 0.15)
    model = MLPC()
    a = ButterworthFilter()

    model.loadModel(pathToModel)

    print("Processing Voice activity detection...")
    x = WebRtcVad()
    x.test_process_file(pathToRecord)
    x.approximation()
    x.printOutput()
    cuts = x.cutAndSave(pathToCutted, 0)
    emotions = ""
    print("Voice activity detection completed. Voice cutted and saved.")

    for r, d, f in os.walk(pathToCutted):
        for file in f:
            tmpFile = pathToCutted + "/" + file
            tmpSave = pathToCuttedAndFiltered + "/" + file
            print("Removing noise...")
            # runVADExapmle(tmpFile)
            a.normalize(tmpFile, tmpSave)
            # a.emphasis(tmpSave, tmpSave)
            print("Noise removed.")

            test = dataLoader.extractFeature(
                tmpSave, mfcc=True, chroma=True, mel=True)
            test = test.reshape(1, 180)
            prediction = model.predict(np.array(test))
            emotions += "\n" + str(prediction[0])
    deleteFiles(pathToCutted)
    deleteFiles(pathToCuttedAndFiltered)
    return [cuts, emotions]
