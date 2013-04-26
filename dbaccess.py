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
                CREATE TABLE Measurment(Id INTEGER PRIMARY KEY ASC,Temperature REAL,Humidity REAL,Pressure INTEGER,Light INTEGER,AirQty INTEGER);
                CREATE TABLE Average(Id INTEGER PRIMARY KEY ASC,FromIdx INTEGER,ToIdx INTEGER,Temperature REAL,Humidity REAL,Pressure INTEGER,Light INTEGER,AirQty INTEGER);                 
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

    def insertMeasurement(self,measurment):
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
        #datetime = measurment['Datetime:']

        with self.con:
            self.cur.execute("INSERT INTO Measurment (Temperature,Humidity,Pressure,Light,AirQty) values (?,?,?,?,?)",(temp,hum,press,light,air))
                  
    def insertAverage(self,measurment,fromidx,toidx):
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
        #datetime = measurment['Datetime:']
        
        with self.con:
            self.cur.execute("INSERT INTO Average (FromIdx,ToIdx,Temperature,Humidity,Pressure,Light,AirQty) values (?,?,?,?,?,?,?)",(fromidx,toidx,temp,hum,press,light,air))

    def printLast30Measurment(self):
        with self.con:
            self.cur.execute("SELECT * FROM Measurment ORDER BY Id DESC LIMIT 30")
            col_name = [tuple[0] for tuple in self.cur.description]
            rows = self.cur.fetchall()
            print col_name
            for row in rows:
                print row
            print col_name
                      
            
    def getLast30Measurment(self):
        with self.con:
            self.cur.execute("SELECT * FROM Measurment ORDER BY Id DESC LIMIT 30")
            rows = self.cur.fetchall()
            return rows

    def printLast30Average(self):
        with self.con:
            self.cur.execute("SELECT * FROM Average ORDER BY Id DESC LIMIT 30")
            col_name = [tuple[0] for tuple in self.cur.description]
            rows = self.cur.fetchall()
            print col_name
            for row in rows:
                print row
            print col_name
            
    def getLast30Average(self):
        with self.con:
            self.cur.execute("SELECT * FROM Average ORDER BY Id DESC LIMIT 30")
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

    mytweetdb.printLast30Measurment()
    mytweetdb.printLast30Diary()
    mytweetdb.printLast30Average()

    
    
        
