/* MQ-3 Alkohol Snesor Circuit with Arduino */

const int AOUTpin=0;
const int DOUTpin=8 ;
const int ledPin=13;

int limit;
int value;

void setup(){
  Serial.begin(9600); //sets the baud rate
  pinMode(DOUTpin, INPUT); //sets the pin as an input to the arduino
  pinMode(ledPin, OUTPUT); //sets the pin as an output of the arduino
}

void loop(){
  value=analogRead(AOUTpin); // read the analog value from the alkohol sensor AOUT pin
  limit=digitalRead(DOUTpin); // reads the digital value from the alcohol sensor's DOUT pin
  Serial.print("Alcohol value: ");
  Serial.println(value); // prints the alcohol value
  Serial.print("Limit: "); // prints the limit reached as either LOW or HIGH (obove or under)
  Serial.println(limit);
  delay(100);
  if (limit == HIGH){
    digitalWrite(ledPin, HIGH); // limit has been reached LED turns on as status indicator
  }
  else{
    digitalWrite(ledPin, LOW); // if threshold not reached LED remains off
  } 
}
