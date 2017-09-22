import serial
from Tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Log Data", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
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
