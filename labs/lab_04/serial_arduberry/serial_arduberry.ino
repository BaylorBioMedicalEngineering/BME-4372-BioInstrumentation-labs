void setup() 
{
  Serial.begin(57600);  //Start the Serial at 9600 baud
}

void loop() 
{
  for(char i=0; i<6; i++) 
  {
    Serial.println(analogRead(15+i));
  }
  delay(1000);       
}
