import sys
import serial
import time
import datetime
import dbaccess
import math

keywords = ('Temperature:','Humidity:','Pressure:','Light:','AirQuality:')
measure={}
startstr = '---'

def readWeatherBox():
    global ready
    lines = arduino.readlines()
    measure = {}
    if lines.count > 0:
        for line in lines:
            data = line.split(' ')
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

    if len(measure) > 1 :
        nowstr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mytweetdb.insertMeasurement(measure)
        print nowstr,measure

def statistics(allmeas):
    sumlist = [0.0,0.0,0,0,0]
    maxlist = [0.0,0.0,0,0,0]
    minlist = [1000.0,1000.0,999999,999999,999999]
    varlist = [0.0,0.0,0,0,0]

    dataleng = len(allmeas)
    fromidx = allmeas[0][0]
    toidx = allmeas[dataleng-1][0]
    print fromidx,toidx
    
    for meas in allmeas:
        #print meas
        for ix in range(5):
            sumlist[ix] += meas[ix+1]
            if (maxlist[ix] < meas[ix+1]):
                maxlist[ix] = meas[ix+1]
            if (minlist[ix] > meas[ix+1]):
                minlist[ix] = meas[ix+1]

            
    #print sumlist
    measure = {}
    for ix in range(5):
        print ix,sumlist[ix]
        sumlist[ix] = sumlist[ix]/dataleng
        if ix == 0:
            measure[keywords[ix]]=int(sumlist[ix]*10)/10.0
            continue
        if ix == 1:
            measure[keywords[ix]]=int(sumlist[ix]*10)/10.0
        else:
            measure[keywords[ix]]=int(sumlist[ix])
            
    #cal Dev
    for meas in allmeas:
        for ix in range(5):
            varlist[ix] += ((meas[ix+1]-sumlist[ix])*(meas[ix+1]-sumlist[ix]))
        for ix in range(5):
            varlist[ix] = varlist[ix]/dataleng
            varlist[ix] = math.sqrt(varlist[ix])
            varlist[ix] = int(varlist[ix]*1000)/1000.0

    measuremin = {}
    measuremax = {}
    measurevar = {}
    for ix in range(5):
        measuremin[keywords[ix]]= minlist[ix]
        measuremax[keywords[ix]]= maxlist[ix]
        measurevar[keywords[ix]]= varlist[ix]

    return (measure,measuremin,measuremax,measurevar,fromidx,toidx)
            
def calAvg(fromidx,toidx):
    allmeas = mytweetdb.getMeasurment(fromidx,toidx)
    
    (measure,measuremin,measuremax,measurevar,fromidx,toidx) = statistics(allmeas)

    mytweetdb.insertAverage(measure,fromidx,toidx)
    mytweetdb.insertMax(measuremax,fromidx,toidx)
    mytweetdb.insertMin(measuremin,fromidx,toidx)
    mytweetdb.insertDeviation(measurevar,fromidx,toidx)
    
    nowstr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mytweetdb.insertDiary(nowstr,'A30')
    print nowstr,fromidx,toidx
    print measure
    print measuremax
    print measuremin
    print measurevar
    
def calAvg60():

    allmeas = mytweetdb.getLast60Measurment()
    (measure,measuremin,measuremax,measurevar,fromidx,toidx) = statistics(allmeas)
                
    mytweetdb.insertAverage(measure,fromidx,toidx)
    mytweetdb.insertMax(measuremax,fromidx,toidx)
    mytweetdb.insertMin(measuremin,fromidx,toidx)
    mytweetdb.insertDeviation(measurevar,fromidx,toidx)
    
    nowstr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mytweetdb.insertDiary(nowstr,'A60')
    print nowstr,fromidx,toidx
    print measure
    print measuremax
    print measuremin
    print measurevar    

def checkPreviousAvg():
    lastavg = mytweetdb.getLastAverage()
    lastmeas = mytweetdb.getLastMeasurment()
    lastid = lastmeas[0][0]
    if (len(lastavg) == 1):
        fromindx = lastavg[0][0]
        toindx = lastavg[0][1]
        if (lastid == toindx):
            pass
        else:
            print fromindx,toindx,lastid
            calAvg60()
    else:
        print "No Average"
        calAvg60()

if (len(sys.argv) > 1):        
    if (sys.argv[1] == 'newdb'):
        mytweetdb = dbaccess.WTdbaccess("weatherdb.db")
        mytweetdb.reCreateAllTable()
else:
    mytweetdb = dbaccess.WTdbaccess("weatherdb.db")
    checkPreviousAvg() 

#calAvg60()

nowstr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
mytweetdb.insertDiary(nowstr,'Startup')

try:
    arduino = serial.Serial('/dev/ttyACM0',9600,timeout=1)
except:
    print "COM ERROR"

#Startup Check Last Average
count = 0
while True:
    readWeatherBox()
    print count
    time.sleep(60)
    count += 1
    if count > 30:
        calAvg60()      
        count = 0
       
        
    
    

    
    
