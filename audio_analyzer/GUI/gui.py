from .dictaphone import Dictophone
from tkinter import *
from .action import action
import os


class GUI():
	def __ensure_dir(self, file_path):
		if not os.path.exists(file_path):
			os.makedirs(file_path)

	def mainloop(self):
		self.__ensure_dir('data')
		self.__ensure_dir('data/cutted')
		self.__ensure_dir('data/cuttedAndFiltered')
		self.master = Tk()
		self.master.title = 'Voice recorder'
		self.dictophone = Dictophone()

		self.label1 = Label(self.master, text='Press start to record')
		self.label1.grid(row=0, sticky=W, rowspan=5)

		self.label2 = Label(self.master, text='')
		self.label2.grid(row=2, column=5)

		self.start_b = Button(self.master, text="Start", command=self.__start)
		self.start_b.grid(row=0, column=3, columnspan=2, ipadx = 50, ipady = 50, rowspan=2,
					padx=25, pady=25)

		self.stop_b = Button(self.master, text="Stop", command=self.__stop)
		self.stop_b.grid(row=0, column=5, columnspan=2, ipadx = 50, ipady = 50, rowspan=2,
				padx=25, pady=25)

		self.stop_s = Button(self.master, text="Action", command=self.__action)
		self.stop_s.grid(row=0, column=70, columnspan=2, ipadx = 50, ipady = 50,rowspan=2,
				padx=25, pady=25)

		self.master.mainloop()

		
	def __start(self):
		self.label1.config(text='Recording...')
		self.label2.config(text='')
		self.start_b.config(text='Pause', command=self.__pause)
		self.dictophone.start_recording()


	def __resume(self):
		self.label1.config(text='Recording...')
		self.label2.config(text='')
		self.start_b.config(text='Pause', command=self.__pause)
		self.dictophone.resume_recording()


	def __pause(self):
		self.label1.config(text='Paused')
		self.label2.config(text='')
		self.start_b.config(text='Resume', command=self.__resume)
		self.dictophone.pause_recording()


	def __stop(self):
		self.label1.config(text='Press start to record')
		self.label2.config(text='')
		self.start_b.config(text='Start', command=self.__start)
		self.dictophone.stop_recording()


	def __action(self):
		ans = action()
		self.label2.config(text=ans)
