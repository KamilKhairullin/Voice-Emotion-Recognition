import os

import librosa
import soundfile as sf


class Trimmer:
    def trimAndSaveFile(self, pathToFile, savePath):
        sampling_rate = 44100
        samples, sample_rate = librosa.load(
            pathToFile, res_type="kaiser_fast", sr=sampling_rate
        )
        samples_trim, index = librosa.effects.trim(samples, top_db=25)
        # librosa.display.waveplot(samples_trim, sr=sample_rate)
        self.__ensure_dir(savePath)
        savePath = os.path.join(savePath, pathToFile.split("/")[-1])
        print(savePath)
        sf.write(savePath, data=samples_trim, samplerate=sampling_rate)
        # plt.show(block=True)

    def trimAndSaveFolder(self, folderPath, savePath):
        for r, d, f in os.walk(folderPath):
            for file in f:
                if file.endswith(".wav"):
                    file = str(r) + "/" + str(file)
                    sp = os.path.join(savePath, r[5:])
                    # print(sp)
                    # print(file)
                    self.trimAndSaveFile(file, sp)
                    sp = ""

    def __ensure_dir(self, file_path):
        if not os.path.exists(file_path) and file_path != "":
            os.makedirs(file_path)
