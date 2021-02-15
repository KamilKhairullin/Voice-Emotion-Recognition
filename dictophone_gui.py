from tkinter import *
from dictophone import Dictophone


master = Tk()
master.title = 'Voice recorder'
dictophone = Dictophone()

label1 = Label(master, text='Press start to record')
label1.grid(row=0, sticky=W, rowspan=5)

start_b = Button(master, text="Start", command=dictophone.startrecording)
start_b.grid(row=0, column=3, columnspan=2, rowspan=2,
       padx=5, pady=5)

stop_b = Button(master, text="Stop", command=dictophone.stoprecording)
stop_b.grid(row=0, column=5, columnspan=2, rowspan=2,
       padx=5, pady=5)
master.mainloop()
