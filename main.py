import serial
from Tkinter import *
import threading


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Quadcopter Interface")

        self.total_label_text = IntVar()
        self.total_label_text.set(0)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.filelabel = Label(master, text="Log File Name:")
        self.filelabel.place(x=0, y=18, width=80, height=15)

        self.fileref = Entry(master)
        self.fileref.grid(row=1, column=0, columnspan=1, sticky=W)
        self.fileref.place(x=81, y=16, width=81, height=20)
        
        self.label = Label(master, text="Enter Port #:")
        self.label.place(x=0, y=58, width=80, height=15)

        self.entry = Entry(master)
        self.entry.place(x=81, y=56, width=50, height=20)

        self.start_button = Button(master, text="Log Data", command=self.start_background_task)
        self.start_button.place(x=0, y=96, width=80, height=20)
        
        self.stop_button = Button(master, text="Stop Logging", command=self.stop_logging)
        self.stop_button.place(x=81, y=96, width=80, height=20)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.grid(row=10, column=0, columnspan=1, sticky=S)
        self.close_button.place(x=0, y=116, width=60, height=20)

        self.w = Canvas(master, width=300, height=300)
        self.w.create_rectangle(20, 20, 280, 280, fill="blue")
        self.w.create_line(10, 10, 290, 10, fill="red")
        self.w.create_line(290, 10, 290, 290, fill="red")
        self.w.create_line(290, 290, 10, 290, fill="red")
        self.w.create_line(10, 290, 10, 10, fill="red")
        self.w.place(x=175, y=0, width=300, height=300)

    def create_bar(self):
        self.bar = Canvas(self, width=300, height=300)
    def start_background_task(self):
        t = threading.Thread(target=self.begin_logging)
        t.start()

    def end_background_task(self):
        threading.start_new_thread(self.stop_logging, ())

    def begin_logging(self):
        global logging
        logging=True
        value = ''
        filename = my_gui.fileref.get()
        file = open((str(filename) + ".csv"), 'a+')
        file.write("Angular Position \n x:, y:, z:\n")
        portno = my_gui.entry.get()
        ser = serial.Serial(('COM' + portno), 9600, timeout=1)  # open serial port
        print(ser.name)         # check which port was really used
        #bar_display = Canvas(self, width=280, height=280)
        while logging==True:
                x = ser.read()
                if (x=='\n'):
                    while x != ',':
                        x = ser.read()
                        value = value + x
                    print (value)

                        
                        
                    
                file.write(x)
        ser.close()             # close port

    def stop_logging(self):
        global logging
        logging=False

root = Tk()
root.geometry("475x300+30+30") 
my_gui = MyFirstGUI(root)
root.mainloop()


	

