#
# SQLite 3 DB Access Class
#
import sqlite3 as lite
import sys

class WTdbaccess:
    def __init__(self,dbfile):
        self.con = lite.connect(dbfile)
        self.cur = self.con.cursor()
        
    def dbConnect(self,dbfile):
        self.con = lite.connect(dbfile)
        self.cur = self.con.cursor()
        
    def reCreateAllTable(self):
        with self.con:
            sqlcmd = """
                DROP TABLE IF EXISTS Measurment;
                DROP TABLE IF EXISTS Average;
                DROP TABLE IF EXISTS Diary;
                DROP TABLE IF EXISTS Max;
                DROP TABLE IF EXISTS Min;
                DROP TABLE IF EXISTS Deviation;
                CREATE TABLE Measurment(Id INTEGER PRIMARY KEY ASC,Temperature REAL,Humidity REAL,Pressure INTEGER,Light INTEGER,AirQty INTEGER);
                CREATE TABLE Average(Id INTEGER PRIMARY KEY ASC,FromIdx INTEGER,ToIdx INTEGER,Temperature REAL,Humidity REAL,Pressure INTEGER,Light INTEGER,AirQty INTEGER);                 
                CREATE TABLE Max(Id INTEGER PRIMARY KEY ASC,FromIdx INTEGER,ToIdx INTEGER,Temperature REAL,Humidity REAL,Pressure INTEGER,Light INTEGER,AirQty INTEGER);                 
                CREATE TABLE Min(Id INTEGER PRIMARY KEY ASC,FromIdx INTEGER,ToIdx INTEGER,Temperature REAL,Humidity REAL,Pressure INTEGER,Light INTEGER,AirQty INTEGER);                 
                CREATE TABLE Deviation(Id INTEGER PRIMARY KEY ASC,FromIdx INTEGER,ToIdx INTEGER,Temperature REAL,Humidity REAL,Pressure INTEGER,Light INTEGER,AirQty INTEGER);                 
                CREATE TABLE Diary(Id INTEGER PRIMARY KEY ASC,DateTime TEXT,Operation Text,AtIndex INTEGER)
            """
            self.cur.executescript(sqlcmd)

    def insertDiary(self,datetime,operation):
        with self.con:
            self.cur.execute("SELECT * FROM Measurment ORDER BY Id DESC LIMIT 1")
            rows = self.cur.fetchall()
            if len(rows) == 0:
                self.cur.execute("INSERT INTO Diary (DateTime,Operation,AtIndex) values (?,?,?)",(datetime,operation,1))
            else:
                idex = rows[0][0]
                self.cur.execute("INSERT INTO Diary (DateTime,Operation,AtIndex) values (?,?,?)",(datetime,operation,idex+1))

    def parseMeasurment(self,measurment):
        """
        {'Humidity:': 58.4,
         'sensor_value:': 461,
         'Light:': 33899,
         'AirQuality:': 11,
         'Pressure:': 101194,
         'Temperature:': 26.7}
        """
        if 'Temperature:' in measurment:
            temp  = measurment['Temperature:']
        else:
            return 
        if 'Humidity:' in measurment:
            hum   = measurment['Humidity:']
        else:
            return
        if 'Pressure:' in measurment:
            press = measurment['Pressure:']
        else:
            return
        if 'Light:' in measurment:
            light = measurment['Light:']
        else:
            return
        if 'AirQuality:' in measurment:
            air   = measurment['AirQuality:']
        else:
            return
        return (temp,hum,press,light,air)
        
    def insertMeasurement(self,measurment):
        try:
            (temp,hum,press,light,air) = self.parseMeasurment(measurment)
        except:
            return
        with self.con:
            self.cur.execute("INSERT INTO Measurment (Temperature,Humidity,Pressure,Light,AirQty) values (?,?,?,?,?)",(temp,hum,press,light,air))    
    def insertAverage(self,measurment,fromidx,toidx):
        (temp,hum,press,light,air) = self.parseMeasurment(measurment)
        with self.con:
            self.cur.execute("INSERT INTO Average (FromIdx,ToIdx,Temperature,Humidity,Pressure,Light,AirQty) values (?,?,?,?,?,?,?)",(fromidx,toidx,temp,hum,press,light,air))
    def insertMax(self,measurment,fromidx,toidx):
        (temp,hum,press,light,air) = self.parseMeasurment(measurment)
        with self.con:
            self.cur.execute("INSERT INTO Max (FromIdx,ToIdx,Temperature,Humidity,Pressure,Light,AirQty) values (?,?,?,?,?,?,?)",(fromidx,toidx,temp,hum,press,light,air))
    def insertMin(self,measurment,fromidx,toidx):
        (temp,hum,press,light,air) = self.parseMeasurment(measurment)
        with self.con:
            self.cur.execute("INSERT INTO Min (FromIdx,ToIdx,Temperature,Humidity,Pressure,Light,AirQty) values (?,?,?,?,?,?,?)",(fromidx,toidx,temp,hum,press,light,air))
    def insertDeviation(self,measurment,fromidx,toidx):
        (temp,hum,press,light,air) = self.parseMeasurment(measurment)
        with self.con:
            self.cur.execute("INSERT INTO Deviation (FromIdx,ToIdx,Temperature,Humidity,Pressure,Light,AirQty) values (?,?,?,?,?,?,?)",(fromidx,toidx,temp,hum,press,light,air))

    def printLast60Measurment(self):
        with self.con:
            self.cur.execute("SELECT * FROM Measurment ORDER BY Id DESC LIMIT 60")
            col_name = [tuple[0] for tuple in self.cur.description]
            rows = self.cur.fetchall()
            print col_name
            for row in rows:
                print row
            print col_name         
                      
            
    def getLast60Measurment(self):
        with self.con:
            self.cur.execute("SELECT * FROM Measurment ORDER BY Id DESC LIMIT 60")
            rows = self.cur.fetchall()
            return rows

    def getLastMeasurment(self):
        with self.con:
            self.cur.execute("SELECT * FROM Measurment ORDER BY Id DESC LIMIT 1")
            rows = self.cur.fetchall()
            return rows

    def getMeasurment(self,fromidx,toidx):
        if (fromidx > toidx) :
            return ()
        with self.con:
            self.cur.execute("SELECT * FROM Measurment WHERE Id >= ? AND Id <= ? ORDER BY Id DESC",(fromidx,toidx))
            rows = self.cur.fetchall()
            return rows

    def printMeasurment(self,fromidx,toidx):
        if (fromidx > toidx) :
            return ()
        with self.con:
            self.cur.execute("SELECT * FROM Measurment WHERE Id >= ? AND Id <= ? ORDER BY Id DESC",(fromidx,toidx))
            col_name = [tuple[0] for tuple in self.cur.description]
            rows = self.cur.fetchall()
            print col_name
            for row in rows:
                print row
            print col_name             
        
    def printLast24Average(self):
        with self.con:
            self.cur.execute("SELECT * FROM Average ORDER BY Id DESC LIMIT 24")
            col_name = [tuple[0] for tuple in self.cur.description]
            rows = self.cur.fetchall()
            print col_name
            for row in rows:
                print row
            print col_name

            
    def getLast24Average(self):
        with self.con:
            self.cur.execute("SELECT * FROM Average ORDER BY Id DESC LIMIT 24")
            rows = self.cur.fetchall()
            return rows
    def getLast24Max(self):
        with self.con:
            self.cur.execute("SELECT * FROM Max ORDER BY Id DESC LIMIT 24")
            rows = self.cur.fetchall()
            return rows
    def getLast24Min(self):
        with self.con:
            self.cur.execute("SELECT * FROM Min ORDER BY Id DESC LIMIT 24")
            rows = self.cur.fetchall()
            return rows
    def getLast24Deviation(self):
        with self.con:
            self.cur.execute("SELECT * FROM Deviation ORDER BY Id DESC LIMIT 24")
            rows = self.cur.fetchall()
            return rows        
        
    def getLastAverage(self):
        with self.con:
            self.cur.execute("SELECT * FROM Average ORDER BY Id DESC LIMIT 1")
            rows = self.cur.fetchall()
            return rows        
    def getLastMax(self):
        with self.con:
            self.cur.execute("SELECT * FROM Max ORDER BY Id DESC LIMIT 1")
            rows = self.cur.fetchall()
            return rows
    def getLastMin(self):
        with self.con:
            self.cur.execute("SELECT * FROM Min ORDER BY Id DESC LIMIT 1")
            rows = self.cur.fetchall()
            return rows
    def getLastDeviation(self):
        with self.con:
            self.cur.execute("SELECT * FROM Deviation ORDER BY Id DESC LIMIT 1")
            rows = self.cur.fetchall()
            return rows

        
    def printLast30Diary(self):
        with self.con:
            self.cur.execute("SELECT * FROM Diary ORDER BY Id DESC LIMIT 30")
            col_name = [tuple[0] for tuple in self.cur.description]
            rows = self.cur.fetchall()
            print col_name
            for row in rows:
                print row
            print col_name

              

if __name__ == "__main__":
    mytweetdb = WTdbaccess("weatherdb.db")
    
    '''
    mytweetdb.reCreateAllTable()
    meas = {'Humidity:': 58.4, 'sensor_value:': 461, 'Light:': 33899, 'AirQuality:': 11, 'Pressure:': 101194, 'Temperature:': 26.7}
    mytweetdb.insertMeasurement(meas)
    mytweetdb.insertMeasurement(meas)
    mytweetdb.insertMeasurement(meas)
    mytweetdb.insertDiary('2013-04-26 10:00:15','Measurment')
    mytweetdb.insertMeasurement(meas)
    mytweetdb.insertMeasurement(meas)
    mytweetdb.insertMeasurement(meas)
    mytweetdb.insertDiary('2013-04-26 10:00:15','Average30')
    mytweetdb.insertAverage(meas,1,20) 
    mytweetdb.insertMax(meas,1,20)
    mytweetdb.insertMin(meas,1,20)
    mytweetdb.insertDeviation(meas,1,20) 
    '''
    
    mytweetdb.printLast60Measurment()
    mytweetdb.printLast30Diary()
    mytweetdb.printLast24Average()
    print mytweetdb.getLastMax()
    print mytweetdb.getLastMin()
    print mytweetdb.getLastDeviation()
    #mytweetdb.getMeasurment(0,5)
    #mytweetdb.printMeasurment(1229,1288)

    
    
        
