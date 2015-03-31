#include <WiFi.h>

char ssid[] = "Dr1";
char password[] = "theDRONEteam1";
unsigned int localPort = 2390;
char serverIP[] = "192.168.1.100";
int serverPort = 42679;
IPAddress ip;

String gpsBuffer, GPS, LNG, LAT, GPS_ALT, GPS_SPD, GPS_TIME;
char GPS_DATA[30][30];
char GPS_DATA2[30][30];
boolean newGPS;

WiFiUDP Udp;

void setup() {
  Serial.begin(9600);

  newGPS = false;

  WiFi.begin(ssid, password);

  Udp.begin(localPort);
  
  Udp.beginPacket(serverIP, serverPort);
  Udp.print("connected");
  Udp.endPacket();

}

void loop()
{
  probeGPS();

  if(newGPS) {
    Udp.beginPacket(serverIP, serverPort);
    Udp.print("{ \"Lat\": \"");
    Udp.print(LAT);
    Udp.print("\", \"LNG\": \"");
    Udp.print(LNG);
    Udp.print("\", \"ALT\": \"");
    Udp.print(GPS_ALT);
    Udp.print("\", GPS_SPD: \"");
    Udp.print(GPS_SPD);
    Udp.print("' }");
    Udp.endPacket();
    newGPS = false;
  } 
  
  int numSsid = WiFi.scanNetworks();
  Udp.beginPacket(serverIP, serverPort);
  Udp.print("{");
  for (int thisNet = 0; thisNet < numSsid; thisNet++) 
  {
    Udp.print(WiFi.SSID(thisNet));
    Udp.print(":");
    Udp.print(WiFi.RSSI(thisNet));
    Udp.print(",");
  }
  Udp.print("}");
  Udp.endPacket();

}

void probeGPS(){
  while(Serial.available()) {
    char next = Serial.read();
    if(next != '\n'){
      gpsBuffer += next;
    } 
    else {
      if(gpsBuffer.startsWith("$GPGGA") || gpsBuffer.startsWith("$GPRMC")){
        GPS = gpsBuffer;
        formatGPS();
        newGPS = true;
      }
      gpsBuffer = "";
    }
  }
}

void formatGPS() {
  if(GPS.startsWith("$GPGGA")) {
    int curr = 0;
    int counter = 0;
    for(int i = 0; i < GPS.length(); i++) {
      if(GPS.charAt(i) == ',') {
        curr++;
        counter = 0;
      } 
      else {
        GPS_DATA[curr][counter++] = GPS.charAt(i);
      }
    }
  } 
  else if(GPS.startsWith("$GPRMC")) {
    int curr2 = 0;
    int counter2 = 0;
    for(int i = 0; i < GPS.length(); i++) {
      if(GPS.charAt(i) == ',') {
        curr2++;
        counter2 = 0;
      } 
      else {
        GPS_DATA2[curr2][counter2++] = GPS.charAt(i);
      }
    }
  }
  GPS_SPD = GPS_DATA2[7];
  GPS_TIME = GPS_DATA[1];
  LAT = GPS_DATA[1];
  LNG = GPS_DATA[3];
  GPS_ALT = GPS_DATA[9];
}

