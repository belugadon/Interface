import serial
from Tkinter import *
import threading
import time
import math


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

        self.alert1 = Label(master, text="Port Closed", foreground="red")
        self.alert2 = Label(master, text="File not found", foreground="red")        
        
        self.Xlabel = Label(master, text="X Axis:")
        self.Xlabel.place(x=40, y=145, width=35, height=20)
        self.Xlabel = Label(master, text="Y Axis:")
        self.Xlabel.place(x=125, y=145, width=35, height=20)
        self.Xlabel = Label(master, text="Z Axis:")
        self.Xlabel.place(x=215, y=145, width=35, height=20)
        self.Xlabel = Label(master, text="Throttle:")
        self.Xlabel.place(x=285, y=145, width=50, height=20)
        
        self.w = Canvas(master, width=350, height=350)
        self.w.create_rectangle(20, 20, 90, 90, fill="blue")
        self.w.create_oval(20, 20, 90, 90, fill="green")
        self.w.create_rectangle(110, 20, 180, 90, fill="blue")
        self.w.create_oval(110, 20, 180, 90, fill="green")
        self.w.create_rectangle(200, 20, 270, 90, fill="blue")
        self.w.create_oval(200, 20, 270, 90, fill="green")   
        self.w.create_line(20, 55, 90, 55, fill="black")
        self.w.create_line(110, 55, 180, 55, fill="black")
        self.w.create_line(200, 55, 270, 55, fill="black")
        self.w.create_line(235, 20, 235, 90, fill="black")
        self.w.create_line(55, 20, 55, 90, fill="black")
        self.w.create_line(145, 20, 145, 90, fill="black")
        self.w.create_line(10, 10, 340, 10, fill="red")
        self.w.create_line(340, 10, 340, 100, fill="red")
        self.w.create_line(340, 10, 340, 116, fill="red")
        self.w.create_line(340, 116, 10, 116, fill="red")
        self.w.create_line(10, 116, 10, 10, fill="red")

        self.w.create_rectangle(290, 20, 330, 90, fill="green")

        self.w.place(x=0, y=160, width=350, height=350)

        self.XNumbDisplay = Label(master)
        self.XNumbDisplay.place(x=45, y=255)
        self.YNumbDisplay = Label(master)
        self.YNumbDisplay.place(x=135, y=255)
        self.ZNumbDisplay = Label(master)
        self.ZNumbDisplay.place(x=225, y=255)
        self.TNumbDisplay = Label(master)
        self.TNumbDisplay.place(x=300, y=255)
        
        self.start_button = Button(master, text="Stream", command=lambda: self.start_background_task1(self.w))
        self.start_button.place(x=0, y=96, width=80, height=20)
        
        self.stop_button = Button(master, text="Stop", command=self.stop_logging)
        self.stop_button.place(x=81, y=96, width=80, height=20)

        self.play_button = Button(master, text="Playback", command=lambda: self.start_background_task2(self.w))
        self.play_button.place(x=0, y=116, width=80, height=20)
        
        self.close_button = Button(master, text="Close", command=self.close_application)
        self.close_button.grid(row=10, column=0, columnspan=1, sticky=S)
        self.close_button.place(x=81, y=116, width=80, height=20)

    def create_bar(self, argv):
        self.bar = Canvas(self, width=300, height=300)
        self.bar.create_line(150, 290, 150, argv, fill="red")

        
    def start_background_task1(self, canvas):
        t = threading.Thread(target=self.begin_logging, args=[canvas])
        t.start()
        
    def start_background_task2(self, canvas):
        t = threading.Thread(target=self.playback, args=[canvas])
        t.start()

    def close_application(self):
        global logging
        logging=False
        root.quit()

    def begin_logging(self, canvas):
        global logging
        value = 0
        i=0
        filename = self.fileref.get()
        if(filename != ''):
            file = open( (str(filename) + ".csv"), 'a+')
            file.write("Angular Position \n x:, y:, z:\n")
        portno = self.entry.get()
        try:
            self.alert1.place(width=0, height=0)
            ser = serial.Serial(('COM' + portno), 9600, timeout=100)  # open serial port
            logging=True
        except serial.SerialException:
            self.alert1.place(x=61, y=76, width=100, height=20)
            logging=False
            return
        print(ser.name)         # check which port was really used
        while logging==True:
            x = ser.read()
            if x=='x':
                while x != '-':
                    x = ser.read()
                    if(x != '-'):
                        value <<= 8
                        value = value + ord(x)
                if(filename != ''):
                    file.write(str(value-180))
                    file.write(',')
                #canvas.delete("linex")
                #canvas.create_arc(20, 20, 90, 90, start=value-100, extent=20, fill="red", tag="linex")
                canvas.delete("linex_1")
                canvas.delete("linex_2")  
                canvas.create_arc(22, 22, 88, 88, start=0-180, extent=(0-value)+180, fill="red", tag="linex_1")
                canvas.create_arc(22, 22, 88, 88, start=0, extent=(0-value)+180, fill="red", tag="linex_2")
                self.XNumbDisplay.config(text = (value-180))
                value = 0
            elif x=='y':
                while x != '-':
                    x = ser.read()
                    if(x != '-'):
                        value <<= 8
                        value = value + ord(x)
                if(filename != ''):
                    file.write(str(value-180))
                    file.write(',')
                #canvas.delete("liney")
                #canvas.create_arc(110, 20, 180, 90, start=value-100, extent=20, fill="red", tag="liney")
                canvas.delete("liney_1")
                canvas.delete("liney_2")  
                canvas.create_arc(112, 22, 178, 88, start=0-180, extent=(0-value)+180, fill="red", tag="liney_1")
                canvas.create_arc(112, 22, 178, 88, start=0, extent=(0-value)+180, fill="red", tag="liney_2")
                self.YNumbDisplay.config(text = (value-180))
                value = 0
            elif x=='z':
                while x != '-':
                    x = ser.read()
                    if(x != '-'):
                        value <<= 8
                        value = value + ord(x)
                if(filename != ''):
                    file.write(str(value-180))
                    file.write(',')
                #canvas.delete("linez")
                #canvas.create_arc(200, 20, 270, 90, start=value-100, extent=20, fill="red", tag="linez")
                canvas.delete("linez_1")
                canvas.delete("linez_2")  
                canvas.create_arc(202, 22, 268, 88, start=0-180, extent=(0-value)+180, fill="red", tag="linez_1")
                canvas.create_arc(202, 22, 268, 88, start=0, extent=(0-value)+180, fill="red", tag="linez_2")
                self.ZNumbDisplay.config(text = (value-180))
                value = 0
            elif x=='t':
                while x != '-':
                    x = ser.read()
                    if(x != '-'):
                        value <<= 8
                        value = value + ord(x)
                if(filename != ''):
                    file.write(str(value))
                    file.write(',')
                    file.write('\n')
                canvas.delete("linet")  
                canvas.create_rectangle(290, (20 + (70 - (value/100))), 330, 90, fill="red", tag="linet")
                self.TNumbDisplay.config(text = (value))
                value = 0
        ser.close() # close port
        if(filename != ''):
            file.closed

    def playback(self, canvas):
        global logging
        logging=True
        sign=False
        value = 0
        filename = self.fileref.get()
        if(filename != ''):
            try:
                file = open((str(filename) + ".csv"), 'r')
                self.alert2.place(width=0, height=0)
                file.readline()
                file.readline()
            except IOError:
                self.alert2.place(x=61, y=36, width=100, height=20)
                logging=False
        elif(filename == ''):
            logging=False
        x = '0'
        while ((logging==True) & (x != '')):
            time.sleep(0.08)
            while x != ',':
                x = file.read(1)
                if x == '':
                    break
                if (x == '-'):
                    sign=True
                if((x != ',') & ((x != '-') & (x != '\n'))):
                    value = value*10
                    value = value + (int(x))
            if (sign==True):
                value = 0 - value
            canvas.delete("linex_1")
            canvas.delete("linex_2")  
            canvas.create_arc(22, 22, 88, 88, start=180, extent=value, fill="red", tag="linex_1")
            canvas.create_arc(22, 22, 88, 88, start=0, extent=value, fill="red", tag="linex_2")
            self.XNumbDisplay.config(text = (value))
            value = 0
            sign=False
            if(x==','):
                x = '0'
            while x != ',':
                x = file.read(1)
                if x == '':
                    break
                if (x == '-'):
                    sign=True
                if ((x != ',') & ((x != '-') & (x != '\n'))):
                    value = value*10
                    value = value + (int(x))
            if (sign==True):
                value = 0 - value
            #canvas.delete("liney")
            #canvas.create_arc(110, 20, 180, 90, start=value+80, extent=20, fill="red", tag="liney")
            canvas.delete("liney_1")
            canvas.delete("liney_2")  
            canvas.create_arc(112, 22, 178, 88, start=180, extent=value, fill="red", tag="liney_1")
            canvas.create_arc(112, 22, 178, 88, start=0, extent=value, fill="red", tag="liney_2")
            self.YNumbDisplay.config(text = (value))
            value = 0
            sign=False
            if(x==','):
                x = '0'
            while x != ',':
                x = file.read(1)
                if x == '':
                    break
                if (x == '\n'):
                    break
                if (x == '-'):
                    sign=True
                if ((x != ',') & ((x != '-') & (x != '\n'))):
                    value = value*10
                    value = value + (int(x))
            if (sign==True):
                value = 0 - value
            #canvas.delete("linez")
            #canvas.create_arc(200, 20, 270, 90, start=value+80, extent=20, fill="red", tag="linez")
            canvas.delete("linez_1")
            canvas.delete("linez_2")  
            canvas.create_arc(202, 22, 268, 88, start=180, extent=value, fill="red", tag="linez_1")
            canvas.create_arc(202, 22, 268, 88, start=0, extent=value, fill="red", tag="linez_2")
            self.ZNumbDisplay.config(text = (value))
            value = 0
            sign=False
            if(x==','):
                x = '0'
            while x != ',':
                x = file.read(1)
                if x == '':
                    break
                if (x == '\n'):
                    break
                if (x == '-'):
                    sign=True
                if ((x != ',') & ((x != '-') & (x != '\n'))):
                    value = value*10
                    value = value + (int(x))
            if (sign==True):
                value = 0 - value
            canvas.delete("linet")  
            canvas.create_rectangle(290, (20 + (70 - (value/100))), 330, 90, fill="red", tag="linet")
            self.TNumbDisplay.config(text = (value))
            value = 0
            sign=False
            if(x==','):
                x = '0'
        if(filename != '') & (logging==True):
            file.closed
        print("finished playback")

        
    def stop_logging(self):
        global logging
        logging=False

root = Tk()
root.geometry("350x290+30+30") 
my_gui = MyFirstGUI(root)
root.mainloop()


	

