String gpsBuffer;

void setup() {
  Serial.begin(9600);
}

void loop() {
  probeGPS();
}

void probeGPS(){
  if(Serial.available()) {
    char next = Serial.read();
    if(next != '\n'){
      gpsBuffer += next;
    } else {
      if(gpsBuffer.startsWith("$GPGLL")){
        Serial.println(gpsBuffer);
      }
      gpsBuffer = "";
    }
  }
}

