//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Note:                                                                                                        //
// This Arduino Code was made with intention that the Arduio would do the voltage conversion from Raw values.   //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


int PotRead1 = analogRead(A0); //define read values
int PotRead2 = analogRead(A1);
int PotRead3 = analogRead(A2); 
int PotRead4 = analogRead(A3);
int PotRead5 = analogRead(A4); 
int PotRead6 = analogRead(A5); 

const PROGMEM int readNum = 100.0; // set array size
int readIndex = 0; // set read index

int PotArray1[readNum]; // set pot array
int PotArray2[readNum];
int PotArray3[readNum];
int PotArray4[readNum];
int PotArray5[readNum];
int PotArray6[readNum];

float PotTotal1 = 0.0; // set array total
float PotTotal2 = 0.0;
float PotTotal3 = 0.0;
float PotTotal4 = 0.0;
float PotTotal5 = 0.0;
float PotTotal6 = 0.0;

void setup() {

Serial.begin(115200); // read serial data at baud rate of 115200

for (int val = 0; val < readNum; val++) {
  
  PotArray1[readNum] = 0.0;  // initialize Pot1-6 array to 0
  PotArray2[readNum] = 0.0; 
  PotArray3[readNum] = 0.0;
  PotArray4[readNum] = 0.0;
  PotArray5[readNum] = 0.0;
  PotArray6[readNum] = 0.0;

  }
}

void loop() {

// read analog  and calculate avg of values
  PotTotal1 = PotTotal1 - PotArray1[readIndex]; // subtracting previous array value (emptying)
  PotTotal2 = PotTotal2 - PotArray2[readIndex];
  PotTotal3 = PotTotal3 - PotArray3[readIndex];
  PotTotal4 = PotTotal4 - PotArray4[readIndex];
  PotTotal5 = PotTotal5 - PotArray5[readIndex];
  PotTotal6 = PotTotal6 - PotArray6[readIndex];
 
  int PotRead1 = analogRead(A0); // read analogpin input
  int PotRead2 = analogRead(A1);
  int PotRead3 = analogRead(A2);
  int PotRead4 = analogRead(A3);
  int PotRead5 = analogRead(A4);
  int PotRead6 = analogRead(A5);
  
  PotArray1[readIndex] = PotRead1; // add read value to array by index
  PotArray2[readIndex] = PotRead2;
  PotArray3[readIndex] = PotRead3;
  PotArray4[readIndex] = PotRead4;
  PotArray5[readIndex] = PotRead5;
  PotArray6[readIndex] = PotRead6;
  
  PotTotal1 = PotTotal1 + PotArray1[readIndex]; // add new array value
  PotTotal2 = PotTotal2 + PotArray2[readIndex];
  PotTotal3 = PotTotal3 + PotArray3[readIndex];
  PotTotal4 = PotTotal4 + PotArray4[readIndex];
  PotTotal5 = PotTotal5 + PotArray5[readIndex];
  PotTotal6 = PotTotal6 + PotArray6[readIndex];

  readIndex = readIndex + 1;

  if (readIndex >= readNum){  
    
    float PotV1 = (PotTotal1/readNum) * (5.000 / 1024.000); // convert analog reading to voltage (0V to 5V)
    float PotV2 = (PotTotal2/readNum) * (5.000 / 1024.000);
    float PotV3 = (PotTotal3/readNum) * (5.000 / 1024.000);
    float PotV4 = (PotTotal4/readNum) * (5.000 / 1024.000);
    float PotV5 = (PotTotal5/readNum) * (5.000 / 1024.000);
    float PotV6 = (PotTotal6/readNum) * (5.000 / 1024.000);

    Serial.print(PotV1, 5); // print values to serial monitor
    Serial.print(F(" , "));
    Serial.print(PotV2, 5);
    Serial.print(F(" , "));
    Serial.print(PotV3, 5);
    Serial.print(F(" , "));
    Serial.print(PotV4, 5);
    Serial.print(F(" , "));
    Serial.print(PotV5, 5);
    Serial.print(F(" , "));    
    Serial.println(PotV6, 5); 
    
    readIndex = 0;  // reset index to 0 following print 
    
  }
  
  delay(0.000001); // delay in value read

}
