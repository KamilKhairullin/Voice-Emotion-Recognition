from sklearn.model_selection import train_test_split
import os.path
import numpy as np
import librosa
import librosa.display
import soundfile
import matplotlib.pyplot as plt

class DataLoader():
    x_data = []
    y_data = []

    emotions={
    #  '01':'neutral',
    #  '02':'calm',
      '03':'happy',
      '04':'sad',
    #  '05':'angry',
    #  '06':'fearful',
    #  '07':'disgust',
    #  '08':'surprised'
    }

    def __init__(self, path, testSize):
        self.path = path
        self.testSize = testSize

    def extractFeature(self, fileName, mfcc, chroma, mel):
        with soundfile.SoundFile(fileName) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate=sound_file.samplerate
            result=np.array([])
            if chroma:
                stft=np.abs(librosa.stft(X))
                chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
                result=np.hstack((result, chroma))        
            if mfcc:
                mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
                result=np.hstack((result, mfccs))
            if mel:
                mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
                result=np.hstack((result, mel))
        return result


    def loadData(self):
        progressCount = 0
        fullSize = self.__dirSize()
        print("Data loading started..")
        for r, d, f in os.walk(self.path):
            progressCount = progressCount + len(f)
            self.__printProgress(progressCount, fullSize)
            for file in f:
                if not self.__loadFile(r, file):
                    continue
        print("Data loading ended.")
        return train_test_split(np.array(self.x_data), self.y_data, test_size=self.testSize)

    def __loadFile(self, r, file):
        if file.endswith(".wav"):
            emotion = file.split("-")[2]
            if emotion not in self.emotions:
                return False
            try:
                emotion = self.emotions[emotion]
                feature = self.extractFeature(os.path.join(r,file), mfcc=True, chroma=True, mel=True)
                self.x_data.append(feature)
                self.y_data.append(emotion)
                return True
            except:
                print(file + " has incorrect format")
                return False

    def __printProgress(self, currentSize, fullSize):
        print("Progress: {0:.2f} %".format((currentSize / fullSize) * 100))

    def __dirSize(self):
        count = 0
        for r, d, f in os.walk(self.path):
            count = count + len(f)
        return count

