import sys
import serial
import time
import datetime
import dbaccess

keywords = ('Humidity:','Temperature:','Pressure:','sensor_value:','AirQuality:','Light:')
measure={}
ready = 0
startstr = '---'

if (sys.argv[1] == 'newdb'):
    mytweetdb = dbaccess.TWdbaccess("weatherdb.db")
    mytweetdb.reCreateAllTable()
else:
    mytweetdb = dbaccess.TWdbaccess("weatherdb.db")

try:
    arduino = serial.Serial('/dev/ttyACM0',9600,timeout=1)
except:
    print "COM ERROR"
    
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

    if len(measure) > 1 :
        measure['Datetime:'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mytweetdb.insertMeasurement(measure)
        print measure
        
    time.sleep(30)
    measure = {}
    
    
