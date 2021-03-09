from os import path
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wf 
import os

class VAD():

    def __init__(self, fileName):
        self.data, self.rate = self.__readWAV(fileName) 
        self.speechRatioList = []
        self.detectedVoice = []
        self.meanData = []

        self.SAMPLE_START = 0
        self.SPEECH_START_BAND = 300
        self.SPEECH_END_BAND = 3000
        self.SAMPLE_WINDOW = 960
        self.SAMPLE_OVERLAP = 480
        self.THRESHOLD = 0.25

        self.SPEECH_WINDOW = 24000
        self.window = 960

    def run(self):
        while (self.SAMPLE_START < (len(self.data) - self.SAMPLE_WINDOW)):
            # Select only the region of the data in the window
            SAMPLE_END = self.SAMPLE_START + self.SAMPLE_WINDOW
            if SAMPLE_END >= len(self.data): 
                SAMPLE_END = len(self.data)-1
            dataWindow = self.data[int(self.SAMPLE_START):int(SAMPLE_END)]
            self.meanData.append(np.mean(dataWindow))
            # Full energy
            energyFreq = self.__connectEnergyWithFrequencies(dataWindow)
            sumFullEnergy = sum(energyFreq.values())
    
            # Voice energy
            sumVoiceEnergy = self.__sumEnergyInBand(energyFreq)
            # Speech ratio
            speechRatio = sumVoiceEnergy/sumFullEnergy
            self.speechRatioList.append(speechRatio)
            self.detectedVoice.append(int(speechRatio > self.THRESHOLD))
    
            self.SAMPLE_START += self.SAMPLE_OVERLAP

        return self.detectedVoice

    def printOutput(self):
        fig, axs = plt.subplots(3)
        fig.suptitle('Voice Activity Detection')
        print(len(self.data) / len(self.speechRatioList))
        axs[0].plot(self.speechRatioList)
        axs[0].axhline(self.THRESHOLD, c='r')
        axs[0].set_title("Speech ratio list vs. THRESHOLD")

        axs[1].plot(np.array(self.detectedVoice), label="Detected")
        axs[1].legend()
        axs[1].set_title("Detected vs. non-detected region")
        
        axs[2].plot(np.array(self.meanData), alpha=0.4, label="Not detected")
        axs[2].plot(np.array(self.detectedVoice) * np.array(self.meanData), label="Detected")
        axs[2].legend()
        axs[2].set_title("Detected vs. non-detected region")

        plt.show(block=False)

    def __readWAV(self, wavFile):
        rate, data = wf.read(wavFile)
        channels = len(data.shape)
        filename = wavFile

        # Convert to mono
        if channels == 2 :
            data = np.mean(data, axis=1, dtype=data.dtype)
            channels = 1
        return data, rate

    def __calculateFrequencies(self, audioData):
        dataFreq = np.fft.fftfreq(len(audioData),1.0/self.rate)
        dataFreq = dataFreq[1:]
        return dataFreq

    def __calculateEnergy(self, audioData):
        dataAmpl = np.abs(np.fft.fft(audioData))
        dataAmpl = dataAmpl[1:]
        return dataAmpl ** 2

    def __connectEnergyWithFrequencies(self, data):
    
        dataFreq = self.__calculateFrequencies(data)
        dataEnergy = self.__calculateEnergy(data)
    
        energyFreq = {}
        for (i, freq) in enumerate(dataFreq):
            if abs(freq) not in energyFreq:
                energyFreq[abs(freq)] = dataEnergy[i] * 2
        return energyFreq

    def __sumEnergyInBand(self, energyFrequencies):
        sumEnergy = 0
        for f in energyFrequencies.keys():
            if self.SPEECH_START_BAND < f < self.SPEECH_END_BAND:
                sumEnergy += energyFrequencies[f]
        return sumEnergy

    def __medianFilter (self, x, k):
        assert k % 2 == 1, "Median filter length must be odd."
        assert x.ndim == 1, "Input must be one-dimensional."
        k2 = (k - 1) // 2
    
        y = np.zeros((len(x), k), dtype=x.dtype)
        y[:,k2] = x
        for i in range (k2):
            j = k2 - i
            y[j:,i] = x[:-j]
            y[:j,i] = x[0]
            y[:-j,-(i+1)] = x[j:]
            y[-j:,-(i+1)] = x[-1]
        return np.median(y, axis=1)

    def smoothSpeechDetection(self):
        medianWindow=int(self.SPEECH_WINDOW/self.window)
        if medianWindow % 2 == 0 : 
            medianWindow = medianWindow - 1
        medianEnergy = self.__medianFilter(np.array(self.detectedVoice), medianWindow)
    
        self.detectedVoice = medianEnergy

    def approximation(self):
        count = 0
        start = 0
        hold = int(len(self.detectedVoice) * 0.03)
        isStarted = False
        for i in range(0, len(self.detectedVoice) - 1):
            if self.detectedVoice[i] == 0:
                count = count + 1
                if not isStarted:
                    start = i
                    #print('Started at ', i)
                    isStarted = True
            elif self.detectedVoice[i] == 1 and isStarted:
                isStarted = False
                #print('Ended at ', i)
                if count < hold:
                    #print('Editing from {} to {}'.format(start, start + count))
                    for j in range(start, start + count):
                        self.detectedVoice[j] = 1
                count = 0
        
    def cutAndSave(self, pathToSave, startNumber):
        number = startNumber
        count = 0
        start = 0
        end = 0
        startsAndCuts = list()
        isStarted = False
        for i in range(0, len(self.detectedVoice) - 1):
            if self.detectedVoice[i] == 1:
                count = count + 1
                if not isStarted:
                    start = i
                    #print('Started at ', i)
                    isStarted = True
            elif self.detectedVoice[i] == 0 and isStarted:
                isStarted = False
                end = i
                #print('Ended at ', i)
                if count > 100:
                    path = os.path.join(pathToSave, str(number) + '.wav')
                    startsAndCuts.append((start, end))
                    wf.write(path, 44200, self.data[start * 480:end * 480].astype(np.int16))
                    print(path + ' cutted and saved.')
                    number = number + 1
                count = 0
        print(startsAndCuts)


                