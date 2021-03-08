import wave
import webrtcvad
import numpy as np
import matplotlib.pyplot as plt
from os import path
import os 
import scipy.io.wavfile as wf 

class WebRtcVad():
    
    def __init__(self):
        self.detectedVoice = np.array([])

    def test_process_file(self, path):
        self.dt, self.rate = self.__readWAV(path) 

        with open(path, 'rb') as f:
            data = f.read()
        frame_ms = 30
        n = int(8000 * 2 * 30 / 1000.0)
        frame_len = int(n / 2)
        webrtcvad.valid_rate_and_frame_length(8000, frame_len)
        chunks = list(data[pos:pos + n] for pos in range(0, len(data), n))
        if len(chunks[-1]) != n:
            chunks = chunks[:-1]

        vad = webrtcvad.Vad(1)
        for chunk in chunks:
            voiced = vad.is_speech(chunk, 8000)
            if voiced:
                self.detectedVoice = np.append(self.detectedVoice, 1)
            else:
                self.detectedVoice = np.append(self.detectedVoice, 0)

    def approximation(self):
        count = 0
        start = 0
        hold = int(len(self.detectedVoice) * 0.2)
        isStarted = False
        for i in range(0, len(self.detectedVoice) - 1):
            if self.detectedVoice[i] == 0:
                count = count + 1
                if not isStarted:
                    start = i
                    isStarted = True
            elif self.detectedVoice[i] == 1 and isStarted:
                isStarted = False
                if count < hold:
                    for j in range(start, start + count):
                        self.detectedVoice[j] = 1
                count = 0

    def printOutput(self):
        plt.plot(np.array(self.detectedVoice), label="Detected")
        plt.legend()
        plt.show(block= False)


        
    def cutAndSave(self, pathToSave, startNumber):
        number = startNumber
        count = 0
        start = 0
        end = 0
        cuts = ""
        startsAndCuts = list()
        isStarted = False
        hold = int(len(self.detectedVoice) * 0.03)
        for i in range(0, len(self.detectedVoice) - 1):
            if self.detectedVoice[i] == 1:
                count = count + 1
                if not isStarted:
                    start = i
                    isStarted = True
            elif self.detectedVoice[i] == 0 and isStarted:
                isStarted = False
                end = i
                if count > hold:
                    path = pathToSave + "/" +  str(number) + '.wav'
                    wf.write(path, 44200, self.dt[start * 120:end * 120])
                    cuts += ('\nFound voice activity in range between {} and {}.'.format(start*120/44200, end*120/44200))
                    print('This record is saved as ' + path )
                    number = number + 1
                count = 0

            if  i == len(self.detectedVoice) - 2 and isStarted:
                isStarted = False
                end = i
                if count > hold:
                    path = pathToSave + "/" +  str(number) + '.wav'
                    wf.write(path, 44200, self.dt[start * 120:end * 120])
                    cuts += ('\nFound voice activity in range between {} and {}.'.format(start*120/44200, end*120/44200))
                    print('This record is saved as ' + path )
                    number = number + 1
                count = 0
        return cuts

    def __readWAV(self, wavFile):
        rate, data = wf.read(wavFile)
        channels = len(data.shape)
        filename = wavFile

        # Convert to mono
        if channels == 2 :
            data = np.mean(data, axis=1, dtype=data.dtype)
            channels = 1
        return data, rate