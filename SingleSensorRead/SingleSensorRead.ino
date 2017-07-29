//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Note:                                                                                                        //
// This Arduino Code was for testing individual sensors with voltage conversion.                                //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int PotRead1 = analogRead(A0); //define read values
int Pot1 = 0; // define calculated voltages

const int readNum = 100.0; // set array size
int readIndex = 0; // set read index

long PotArray1[readNum];
float PotTotal1 = 0.0;
float PotAvg1 = 0.0;

void setup() {
Serial.begin(115200); // read serial data at baud rate of 115200

for (int val = 0; val < readNum; val++) {
  PotArray1[readNum] = 0.0; // initialize Pot1 array to 0
  // can add other pot resets here
  }
}

void loop() {
// read analog  and calculate avg of values
  PotTotal1 = PotTotal1 - PotArray1[readIndex]; // removes old array value
  
  int PotRead1 = analogRead(A0); // read analogpin input 
  PotArray1[readIndex] = PotRead1;
  PotTotal1 = PotTotal1 + PotArray1[readIndex]; // add new array value
  readIndex = readIndex + 1;

  if (readIndex >= readNum){  
    float PotAvg1 = PotTotal1/readNum;
    float PotV1 = PotAvg1 * (5.000 / 1024.000); // convert analog reading to voltage (0V to 5V)
  
    Serial.println(PotV1, 5); // print values to serial monitor    
    readIndex = 0;
  }
  
  delay(0.5); // delay in value read

}
