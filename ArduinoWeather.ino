
#include"AirQuality.h"
#include"Arduino.h"
#include "DHT.h"
#include "Barometer.h"
#include <Wire.h>
#include <Digital_Light_TSL2561.h>
#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE);

AirQuality airqualitysensor;
#include "TM1637.h"
#define CLK 4      
#define DIO 3
TM1637 tm1637(CLK,DIO);

int current_quality =-1;
float temperature;
float pressure;
float atm;
float altitude;
Barometer myBarometer;
void showLED(int data)
{
    int ListDisp[4] = {0,0,0,0};
    if (data <= 9999) {
      ListDisp[3] = data / 1000;
      ListDisp[2] = (data % 1000)/100;
      ListDisp[1] = (data % 100)/10;
      ListDisp[0] = (data % 10);
    } else {
    }
    {
    tm1637.display(0,ListDisp[3]);
    tm1637.display(1,ListDisp[2]); 
    tm1637.display(2,ListDisp[1]);
    tm1637.display(3,ListDisp[0]);  
    }
}
void setup() {
  Wire.begin(); 
  
  Serial.begin(9600); 
  Serial.println("DHTxx test!");
 
  TSL2561.init(); 
  
  tm1637.init();
  tm1637.set(BRIGHT_TYPICAL);//BRIGHT_TYPICAL = 2,BRIGHT_DARKEST = 0,BRIGHTEST = 7;
  
  showLED(0);
  dht.begin();
  airqualitysensor.init(14);
  myBarometer.init();
  showLED(9999);
  delay(1000);
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  unsigned long  Lux;

  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT");
  } else {
    Serial.print("Humidity: "); 
    Serial.print(h);
    Serial.println(" %");
    Serial.print("Temperature: "); 
    Serial.print(t);
    Serial.println(" *C");
  }
  
   temperature = myBarometer.bmp085GetTemperature(myBarometer.bmp085ReadUT()); //Get the temperature, bmp085ReadUT MUST be called first
   pressure = myBarometer.bmp085GetPressure(myBarometer.bmp085ReadUP());//Get the temperature
   altitude = myBarometer.calcAltitude(pressure); //Uncompensated caculation - in Meters 
   atm = pressure / 101325; 
  
  //Serial.print("Temperature: ");
  //Serial.print(temperature, 2); //display 2 decimal places
  //Serial.println(" *C");

  Serial.print("Pressure: ");
  Serial.print(pressure, 0); //whole number only.
  Serial.println(" Pa");

  Serial.print("RAtmosphere: ");
  Serial.println(atm, 4); //display 4 decimal places

  Serial.print("Altitude: ");
  Serial.print(altitude, 2); //display 2 decimal places
  Serial.println(" m");

  Serial.println();
  
  current_quality=airqualitysensor.slope();
  if (current_quality >= 0)// if a valid data returned.
  {
      if (current_quality==0)
          Serial.println("High pollution! Force signal active");
      else if (current_quality==1)
          Serial.println("High pollution!");
      else if (current_quality==2)
          Serial.println("Low pollution!");
      else if (current_quality ==3)
          Serial.println("Fresh air");
  }
  
  TSL2561.getLux();
  Serial.print("Light: ");
  Lux = TSL2561.calculateLux(0,0,1);
  Serial.println(Lux);
    
  Serial.println("-----------------------");
  
  //Show Data On LED and Dealy
  for(int i=0;i<3;i++){
    tm1637.point(POINT_ON);
    showLED(t*100);
    tm1637.point(POINT_ON);
    delay(5000);
    
    tm1637.point(POINT_ON);
    showLED(h*100);
    tm1637.point(POINT_ON);
    delay(5000);  
    
    tm1637.point(POINT_OFF);
    showLED(pressure/100);
    tm1637.point(POINT_OFF);
    delay(5000); 
    
    tm1637.point(POINT_OFF);
    if (current_quality > 0) {
      showLED(current_quality);
    }
    tm1637.point(POINT_OFF);
    delay(2500); 
    
    tm1637.point(POINT_OFF);
    showLED(Lux/10);
    tm1637.point(POINT_OFF);
    delay(2500); 
    
  }
}
ISR(TIMER2_OVF_vect)
{
	if(airqualitysensor.counter==122)//set 2 seconds as a detected duty
	{

			airqualitysensor.last_vol=airqualitysensor.first_vol;
			airqualitysensor.first_vol=analogRead(A0);
			airqualitysensor.counter=0;
			airqualitysensor.timer_index=1;
			PORTB=PORTB^0x20;
	}
	else
	{
		airqualitysensor.counter++;
	}
}
