import pyaudio
import wave
import threading
import os


class Dictophone():
	chunk = 1024  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 2
	fs = 44100  # Record at 44100 samples per second
	seconds = 3
	filename = "output"

	def __init__(self):
		self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
		self.stream = self.p.open(format=self.sample_format,
							 channels=self.channels,
							 rate=self.fs,
							 frames_per_buffer=self.chunk,
							 input=True)
		self.frames = []  # Initialize array to store frames
		self.flag = True
		self.is_recording = None

	def __get_num_of_outputs(self):
		files = [f for f in os.listdir('') if os.path.isfile(f)]
		max_index = 0
		for f in files:
			if 'output' in f:
				if f[6:-4] != 'None':
					if int(f[6:-4]) > max_index:
						max_index = int(f[6:-4])
		return max_index + 1

	def start_recording(self):
		self.t = threading.Thread(target=self.record)
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
								  frames_per_buffer=self.chunk, input=True)
		self.is_recording = True

		print('Recording')

		self.t.start()

	def pause_recording(self):
		self.is_recording = False
		self.t.join()

	def resume_recording(self):
		self.is_recording = True
		self.t = threading.Thread(target=self.record)
		self.t.start()

	def stop_recording(self):
		self.is_recording = False
		print('recording complete')
		self.filename = 'data/record' + str(self.__get_num_of_outputs())
		wf = wave.open(self.filename + '.wav', 'wb')
		wf.setnchannels(self.channels)
		wf.setsampwidth(self.p.get_sample_size(self.sample_format))
		wf.setframerate(self.fs)
		wf.writeframes(b''.join(self.frames))
		wf.close()
		self.frames = []

	def record(self):
		while self.is_recording:
			data = self.stream.read(self.chunk)
			self.frames.append(data)
