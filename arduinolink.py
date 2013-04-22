import serial
import time

arduino = serial.Serial('/dev/ttyACM0',9600,timeout=1)
keywords = ('Humidity:','Temperature:','Pressure:','sensor_value:','AirQuality:','Light:')
measure={}
ready = 0
startstr = '---'
while True:
    lines = arduino.readlines()
    if lines.count > 0:
        for line in lines:
            if ready == 0:
                print line
            data = line.split(' ')
            if ready == 1:
                if (len(data) > 1) :
                    #print line
                    if (data[0] in keywords):
                        data[1] = data[1].strip()
                        if '.' in data[1]:
                            measure[data[0]]= float(data[1])
                        else:
                            measure[data[0]]= int(data[1])
                        #measure[data[0]]=data[1].strip()
                        #print data[0],data[1]
            if startstr in data[0]:
                ready =1
                    
    print measure
    time.sleep(30)
    measure = {}
    
    
