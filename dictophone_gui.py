from tkinter import *
from dictophone import Dictophone


def start():
	global label1, dictophone, start_b
	label1.config(text='Recording...')
	start_b.config(text='Pause', command=pause)
	dictophone.start_recording()


def resume():
	global label1, dictophone, start_b
	label1.config(text='Recording...')
	start_b.config(text='Pause', command=pause)
	dictophone.resume_recording()


def pause():
	global label1, dictophone, start_b
	label1.config(text='Paused')
	start_b.config(text='Resume', command=resume)
	dictophone.pause_recording()


def stop():
	global label1, dictophone, start_b
	label1.config(text='Press start to record')
	start_b.config(text='Start', command=start)
	dictophone.stop_recording()


master = Tk()
master.title = 'Voice recorder'
dictophone = Dictophone()

label1 = Label(master, text='Press start to record')
label1.grid(row=0, sticky=W, rowspan=5)

start_b = Button(master, text="Start", command=start)
start_b.grid(row=0, column=3, columnspan=2, rowspan=2,
			 padx=5, pady=5)

stop_b = Button(master, text="Stop", command=stop)
stop_b.grid(row=0, column=5, columnspan=2, rowspan=2,
			padx=5, pady=5)
master.mainloop()
