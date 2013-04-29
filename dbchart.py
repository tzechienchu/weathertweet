#Chart
import dbaccess
from GChartWrapper import *

def draw60(dataindex,filename):
    data_id = []
    data_temp = []
    norm_data = []
    allmeas = mytweetdb.getLast60Measurment()
    base = allmeas[-1][0]
    length = len(allmeas)
    for meas in allmeas:
        data_id.append((meas[0]-base))
        data_temp.append(meas[dataindex])
    data_id.reverse()
    data_temp.reverse()

    min_val = float(min(data_temp))
    max_val = float(max(data_temp))
    last_val= float(data_temp[-1])
    for val in data_temp:
        norm_data.append((val-min_val)/(max_val-min_val)*100)
        
    plotdata =[data_id,norm_data]

    #print plotdata
    #print data_temp
    G = Line(norm_data,encoding='text')
    #G.size = (640,480)

    G.color('76A4FB')
    G.line(2)
    G.axes('xy')
    G.axes.range(0,0,60,5)
    G.axes.range(1,min_val,max_val)
    G.save(filename)

mytweetdb = dbaccess.WTdbaccess("weatherdb.db")
draw60(1,'Test1.png')
draw60(2,'Test2.png')
draw60(3,'Test3.png')
        
