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
                CREATE TABLE Measurment(Id INTEGER PRIMARY KEY ASC,DTime TEXT,Temperature REAL,Humidity REAL,Pressure INTEGER,Light INTEGER,AirQty INTEGER);     
            """
            self.cur.executescript(sqlcmd)
                    
    def insertMeasurement(self,measurment):
        """
        {'Humidity:': 58.4,
         'sensor_value:': 461,
         'Light:': 33899,
         'AirQuality:': 11,
         'Pressure:': 101194,
         'Temperature:': 26.7}
        """
        temp  = measurment['Temperature:']
        hum   = measurment['Humidity:']
        press = measurment['Pressure:']
        light = measurment['Light:']
        air   = measurment['AirQuality:']
        datetime = measurment['Datetime:']
        
        with self.con:
            self.cur.execute("INSERT INTO Measurment (DTime,Temperature,Humidity,Pressure,Light,AirQty) values (?,?,?,?,?,?)",(datetime,temp,hum,press,light,air))

    def printColname(self):
        with self.con:
            col_name = [tuple[0] for tuple in self.cur.description]
        
    def printMeasureAll(self):
        with self.con:
            self.cur.execute("SELECT * FROM Measurment ORDER BY Id DESC LIMIT 20")
            col_name = [tuple[0] for tuple in self.cur.description]
            rows = self.cur.fetchall()
            print col_name
            for row in rows:
                print row
            print col_name

    #15min Average
    #6Hr Average
    #Daily Average

if __name__ == "__main__":
    mytweetdb = WTdbaccess("weatherdb.db")
    '''
    mytweetdb.reCreateAllTable()
    meas = {'Datetime:': '2013-04-22 09:01:13','Humidity:': 58.4, 'sensor_value:': 461, 'Light:': 33899, 'AirQuality:': 11, 'Pressure:': 101194, 'Temperature:': 26.7}
    mytweetdb.insertMeasurement(meas)
    mytweetdb.insertMeasurement(meas)
    mytweetdb.insertMeasurement(meas)
    '''
    mytweetdb.printMeasureAll()

    
    
        
