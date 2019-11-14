
const int potPin=A0;
const int ledPin = 9;      // the pin that the LED is attached to

int readValue;
int writeValue;

void setup()
{
  // initialize the serial communication:
  Serial.begin(9600);
  pinMode(potPin, INPUT);
  // initialize the ledPin as an output:
  pinMode(ledPin, OUTPUT);
}

void loop() {
  
  readValue=analogRead(potPin);
  writeValue = (255.0/1023.0) * readValue;
  analogWrite(ledPin, writeValue);
  Serial.print("Writing the value of: ");
  Serial.println(writeValue);
  
  
}
