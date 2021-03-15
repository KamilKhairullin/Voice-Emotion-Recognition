import scipy.signal
import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from pydub import AudioSegment, effects

class ButterworthFilter():

    def printSpectogram(self, path):
        sig, fs = librosa.load(path)
        S = librosa.feature.melspectrogram(y=sig, sr=fs)
        librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
        plt.show(block=True)

    def removeNoise(self, pathToFile, pathToSave):
        sampling_rate = 44100
        lowcut = 0.0
        highcut = 125.0
        sample, sample_rate = librosa.load(pathToFile,
                                    sr=sampling_rate, dtype = np.float64)
        a, b = scipy.signal.butter(4, 320. / (sampling_rate / 2.), 'low')
        sample_butterworth = scipy.signal.filtfilt(a, b, sample)
        sf.write(pathToSave, data = sample_butterworth, samplerate = sampling_rate)

    def normalize(self, pathToFile  , pathToSave):
        rawsound = AudioSegment.from_file(pathToFile, "wav")
        normalizedsound = effects.normalize(rawsound)
        normalizedsound.export(pathToSave, format="wav")

    def emphasis(self, pathToFile, pathToSave):
        print(pathToFile)
        y, sr = librosa.load(pathToFile)
        y_filt = librosa.effects.preemphasis(y)
        #S_orig = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        #S_preemph = librosa.amplitude_to_db(np.abs(librosa.stft(y_filt)), ref=np.max)
        #librosa.output.write_wav(pathToSave, y_filt, sr)
        sf.write(pathToSave, y_filt, sr)
