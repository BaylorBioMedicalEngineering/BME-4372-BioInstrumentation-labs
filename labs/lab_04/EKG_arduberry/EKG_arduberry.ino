void setup() 
{
  Serial.begin(115200);  //Start the Serial at 9600 baud
}

void loop() 
{
  if(Serial.read()=='s') //If 's' is recieved, send the data back 
  {
    int sensorValue0 = analogRead(A0);
    //Serial.print("A");
    Serial.print(sensorValue0);
    Serial.print("\n");
  }
  //delay(1);       
}
