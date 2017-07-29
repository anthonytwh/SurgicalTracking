//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Note:                                                                                                        //
// This Arduino Code was used for sending raw sensor data to the Serial monitor for Python to process.          //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int PotRead1 = analogRead(A0); //define read values
int PotRead2 = analogRead(A1);
int PotRead3 = analogRead(A2); 
int PotRead4 = analogRead(A3);
int PotRead5 = analogRead(A4); 
int PotRead6 = analogRead(A5); 

void setup() {

delay (500); // .5 second delay to prevent weird inital symbols from printing
Serial.begin(115200); // read serial data at baud rate of 115200
delay (3500); // 3 second delay to prevent weird inital symbols from printing

}


void loop() {

  int PotRead1 = analogRead(A0); // read analogpin input
  int PotRead2 = analogRead(A1);
  int PotRead3 = analogRead(A2);
  int PotRead4 = analogRead(A3);
  int PotRead5 = analogRead(A4);
  int PotRead6 = analogRead(A5);

  Serial.print(PotRead1); // print values to serial monitor
  Serial.print(" , ");
  Serial.print(PotRead2);
  Serial.print(" , ");
  Serial.print(PotRead3);
  Serial.print(" , ");
  Serial.print(PotRead4);
  Serial.print(" , ");
  Serial.print(PotRead5);
  Serial.print(" , ");    
  Serial.println(PotRead6); 
   
  delay(0.05); // delay in value read

}
