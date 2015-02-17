String gpsBuffer;
String GPS;
boolean newGPS;


void setup() {
  Serial.begin(9600);
  newGPS = false;
}

void loop() {
  probeGPS();
  if(newGPS){
    Serial.println(GPS);
    newGPS = false;
  }
}

void probeGPS(){
  while(Serial.available()) {
    char next = Serial.read();
    if(next != '\n'){
      gpsBuffer += next;
    } else {
      //if(gpsBuffer.startsWith("$GPGLL")){
        //Serial.println(gpsBuffer);
        GPS = gpsBuffer;
        newGPS = true;
      //}
      gpsBuffer = "";
    }
  }
}

