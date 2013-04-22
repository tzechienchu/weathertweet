import serial
import time

arduino = serial.Serial('/dev/ttyACM0',9600,timeout=1)
while True:
    line = arduino.readline()
    print line
    time.sleep(1)
    
    
