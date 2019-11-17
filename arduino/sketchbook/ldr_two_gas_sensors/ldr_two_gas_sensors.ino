/*

- LDR
- MQ-3 Alkohol Sensor
- MQ-9 CO, flammable gasses

*/

// analog input pin configuration
const int LDRpin=5;
const int MQ3pin=1;
const int MQ9pin=0;

int value_ldr;
int value_mq3;
int value_mq9;

void setup(void)
{
  Serial.begin(9600);
  pinMode(LDRpin, INPUT); // ldr input pin
  pinMode(MQ3pin, INPUT); //sets the pin as an input to the arduino
  pinMode(MQ9pin, INPUT); //sets the pin as an input to the arduino
}

void loop(void)
{
  value_ldr = analogRead(LDRpin); // read LDR
  value_mq3 = analogRead(MQ3pin); // read MQ-3
  value_mq9 = analogRead(MQ9pin); // read MQ-9
  Serial.print("arduino.LDR:");
  Serial.print(value_ldr, DEC);
  Serial.print(",arduino.MQ3:");
  Serial.print(value_mq3, DEC);
  Serial.print(",arduino.MQ9:");
  Serial.println(value_mq9, DEC);
  delay(1000);
}
