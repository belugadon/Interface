import serial
from Tkinter import *

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Interface")

        self.total_label_text = IntVar()
        self.total_label_text.set(0)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:")

        self.label = Label(master, text="Quadcopter Interface")
        self.label.pack()

        self.greet_button = Button(master, text="Log Data", command=self.begin_logging)
        self.greet_button.pack(side=LEFT)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack(side=RIGHT)

    def begin_logging(self):
        file = open("flightdata.csv", 'w')
	file.write("Angular Position \n x:, y:, z:\n")
	ser = serial.Serial('COM6', 9600, timeout=1)  # open serial port
	print(ser.name)         # check which port was really used
	while 1:
		x = ser.read() 
		file.write(x)
		print(x)

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()


	
ser.close()             # close port
