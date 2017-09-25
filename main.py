import serial
from Tkinter import *
import threading
import time


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

        self.w = Canvas(master, width=300, height=300)
        self.w.create_rectangle(20, 20, 90, 90, fill="blue")
        self.w.create_oval(20, 20, 90, 90, fill="green")
        self.w.create_rectangle(20, 110, 90, 180, fill="blue")
        self.w.create_oval(20, 110, 90, 180, fill="green")
        self.w.create_rectangle(20, 200, 90, 270, fill="blue")
        self.w.create_oval(20, 200, 90, 270, fill="green")
        self.w.create_line(10, 10, 100, 10, fill="red")
        self.w.create_line(100, 10, 100, 280, fill="red")
        self.w.create_line(100, 280, 10, 280, fill="red")
        self.w.create_line(10, 280, 10, 10, fill="red")
        self.w.place(x=175, y=0, width=300, height=300)

        self.start_button = Button(master, text="Log Data", command=lambda: self.start_background_task(self.w))
        self.start_button.place(x=0, y=96, width=80, height=20)
        
        self.stop_button = Button(master, text="Stop Logging", command=self.stop_logging)
        self.stop_button.place(x=81, y=96, width=80, height=20)
        
        self.close_button = Button(master, text="Close", command=self.close_application)
        self.close_button.grid(row=10, column=0, columnspan=1, sticky=S)
        self.close_button.place(x=0, y=116, width=60, height=20)

    def create_bar(self, argv):
        self.bar = Canvas(self, width=300, height=300)
        self.bar.create_line(150, 290, 150, argv, fill="red")

        
    def start_background_task(self, canvas):
        t = threading.Thread(target=self.begin_logging, args=[canvas])
        t.start()

    def close_application(self):
        self.stop_logging()
        my_gui.quit()

    def begin_logging(self, canvas):
        global logging
        logging=True
        Xaxis = ''
        lastXaxis = 0
        Yaxis = ''
        lastYaxis = 0
        Zaxis = ''
        lastZaxis = 0
        value = 0
        #x=''
        i=0
        filename = self.fileref.get()
        file = open((str(filename) + ".csv"), 'a+')
        file.write("Angular Position \n x:, y:, z:\n")
        portno = self.entry.get()
        ser = serial.Serial(('COM' + portno), 19200, timeout=1)  # open serial port
        print(ser.name)         # check which port was really used
        #while 1:
            #canvas.create_line(200, 20, 200, i, fill="red",  tag="line")
            #canvas.place(x=175, y=0, width=300, height=300)
            #i=i+1
            #time.sleep(0.02)
            #if(i > 300):
                #i=0
                #canvas.delete("line")
        while logging==True:
            x = ser.read()
            if x=='x':
                while x != '-':
                    x = ser.read()
                    if(x != '-'):
                        value <<= 8
                        value = value + ord(x)
                    #print(ord(x))
                print('x')    
                print(value)
                canvas.delete("linex")
                canvas.create_arc(20, 20, 90, 90, start=value, fill="red", tag="linex")
                value = 0
            elif x=='y':
                while x != '-':
                    x = ser.read()
                    if(x != '-'):
                        value <<= 8
                        value = value + ord(x)
                    #print(ord(x))
                print('y')
                print(value)
                canvas.delete("liney")
                canvas.create_arc(20, 110, 90, 180, start=value, fill="red", tag="liney")
                value = 0
            elif x=='z':
                while x != '-':
                    x = ser.read()
                    if(x != '-'):
                        value <<= 8
                        value = value + ord(x)
                    #print(ord(x))
                print('z')    
                print(value)
                canvas.delete("linez")
                canvas.create_arc(20, 200, 90, 270, start=value, fill="red", tag="linez")
                value = 0

    def dummycode():
        while logging==True:
                time.sleep(0.01)
                while x != ',':
                    Xaxis = Xaxis + x
                    x = ser.read()
                    print(repr(x))
                    file.write(x)
                x=''
                Xaxis = Xaxis.translate(None, '\n. ,-')
                canvas.delete("linex")
                canvas.create_arc(20, 20, 90, 90, start=(int(Xaxis)/1000), fill="red", tag="linex")
                lastXaxis = int(Xaxis)
                Xaxis = ''
                while x != ',':
                    Yaxis = Yaxis + x
                    x = ser.read()
                    print(repr(x))
                    file.write(x)
                x=''
                Yaxis = Yaxis.translate(None, '\n. ,-')
                canvas.delete("liney")
                canvas.create_arc(20, 110, 90, 180, start=(int(Yaxis)/1000), fill="red", tag="liney")
                lastYaxis = int(Yaxis)
                Yaxis = ''
                while x != '\n':
                    Zaxis = Zaxis + x
                    x = ser.read()
                    print(repr(x))
                    file.write(x)
                x=''
                Zaxis = Zaxis.translate(None, '\n. ,-')
                canvas.delete("linez")
                canvas.create_arc(20, 200, 90, 270, start=(int(Zaxis)/1000), fill="red", tag="linez")
                lastZaxis = int(Zaxis)
                Zaxis = ''
        ser.close()             # close port
        file.close()

    def stop_logging(self):
        global logging
        logging=False

root = Tk()
root.geometry("290x290+30+30") 
my_gui = MyFirstGUI(root)
root.mainloop()


	

