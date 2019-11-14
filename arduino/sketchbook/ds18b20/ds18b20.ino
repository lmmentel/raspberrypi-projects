
/*
Code for reading temperature from DS18B20
*/

// include libraries
#include <OneWire.h>
#include <DallasTemperature.h>

// data wire is plugged into pin 2 on the arduino
#define ONE_WIRE_BUS 2

// setup OneWire to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// pass out OneWire reference to Dallas Temperature
DallasTemperature sensors(&oneWire);

void setup(void)
{
  // start serial port
  Serial.begin(9600);
  Serial.println("Dallas Temperature IC Control Library Demo");
  // start up the library
  sensors.begin();
}

void loop(void)
{
  // call sensors.requestTemperature() to issue global temperature request
  // to all devices
  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures();
  Serial.println("Done");
  
  Serial.print("Temperature is: ");
  // temperature from the first 0-index device DS18B20
  Serial.print(sensors.getTempCByIndex(0));
  delay(1000);
}
