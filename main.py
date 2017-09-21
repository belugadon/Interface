import serial
import Tkinter

file = open("flightdata.csv", 'w')
file.write("Angular Position \n x:, y:, z:\n")


ser = serial.Serial('COM6', 9600, timeout=1)  # open serial port
print(ser.name)         # check which port was really used
while 1:
	x = ser.read() 
	file.write(x)
	
ser.close()             # close port
