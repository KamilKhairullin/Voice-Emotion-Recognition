import pyaudio
import wave
import threading


class Dictophone:
	chunk = 1024  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 2
	fs = 44100  # Record at 44100 samples per second
	seconds = 3
	filename = "output.wav"

	def __init__(self):
		self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
		self.stream = self.p.open(format=self.sample_format,
							 channels=self.channels,
							 rate=self.fs,
							 frames_per_buffer=self.chunk,
							 input=True)
		self.frames = []  # Initialize array to store frames
		self.flag = True

	def startrecording(self):
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
								  frames_per_buffer=self.chunk, input=True)
		self.isrecording = True

		print('Recording')
		t = threading.Thread(target=self.record)
		t.start()

	def stoprecording(self):
		self.isrecording = False
		print('recording complete')
		self.filename = "output.wav"
		wf = wave.open(self.filename, 'wb')
		wf.setnchannels(self.channels)
		wf.setsampwidth(self.p.get_sample_size(self.sample_format))
		wf.setframerate(self.fs)
		wf.writeframes(b''.join(self.frames))
		wf.close()

	def record(self):
		while self.isrecording:
			data = self.stream.read(self.chunk)
			self.frames.append(data)
