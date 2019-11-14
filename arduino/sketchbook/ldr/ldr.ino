/* LDR */

const int AOUTpin=2;
int ldr;

void setup(void)
{
  Serial.begin(9600);
  pinMode(AOUTpin, INPUT);

void loop(void)
{
  ldr = analogRead(AOUTpin);
  Serial.print("LDR: ");
  Serial.println(ldr);
  delay(1000);
}
