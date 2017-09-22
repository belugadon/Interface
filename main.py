import serial
from Tkinter import *
import thread

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Interface")

        self.total_label_text = IntVar()
        self.total_label_text.set(0)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Quadcopter Interface")
        self.label.place(x=0, y=0, width=125, height=15)

        self.filelabel = Label(master, text="Log File Name:")
        self.filelabel.place(x=0, y=16, width=100, height=15)

        self.fileref = Entry(master)
        self.fileref.grid(row=1, column=0, columnspan=1, sticky=W)
        self.fileref.place(x=0, y=31, width=100, height=20)
        
        self.label = Label(master, text="Enter Port #:")
        self.label.place(x=0, y=55, width=80, height=15)

        self.entry = Entry(master)
        self.entry.place(x=0, y=76, width=50, height=20)

        self.greet_button = Button(master, text="Log Data", command=self.start_background_task)
        self.greet_button.place(x=0, y=96, width=60, height=20)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.grid(row=10, column=0, columnspan=1, sticky=S)
        self.close_button.place(x=0, y=116, width=60, height=20)

    def start_background_task(self):
        thread.start_new_thread(begin_logging, ())

def begin_logging():
    filename = my_gui.fileref.get()
    file = open((str(filename) + ".csv"), 'w')
    file.write("Angular Position \n x:, y:, z:\n")
    portno = my_gui.entry.get()
    ser = serial.Serial(('COM' + portno), 9600, timeout=1)  # open serial port
    print(ser.name)         # check which port was really used
    while 1:
	    x = ser.read() 
	    file.write(x)
	    print(x)
    ser.close()             # close port

root = Tk()
root.geometry("250x200+30+30") 
my_gui = MyFirstGUI(root)
root.mainloop()


	

