#include <WiFi.h>
#include <Wire.h>
#include <BMA222.h>

char ssid[] = "private";
char password[] = "vastcartoon245";
unsigned int localPort = 2390;
char serverIP[] = "192.168.20.2";
//char serverIP[] = "192.168.2.197";
int serverPort = 42679;
IPAddress ip;
long rssi;
//GPS Stuff
String gpsBuffer, GPS, LNG, LAT, GPS_ALT, GPS_SPD, GPS_TIME;
char GPS_DATA[30][30];
char GPS_DATA2[30][30];
boolean newGPS;

WiFiUDP Udp;
BMA222 mySensor;

void setup()
{
  newGPS = false;
  mySensor.begin();
  uint8_t chipID = mySensor.chipID();

  //pinMode(RED_LED, OUTPUT); 
  //pinMode(YELLOW_LED, OUTPUT);
  //pinMode(GREEN_LED, OUTPUT);

  //digitalWrite(RED_LED, LOW);
  //digitalWrite(YELLOW_LED, LOW);
  //digitalWrite(GREEN_LED, LOW);

  Serial.begin(9600);

  WiFi.begin(ssid, password);

  Udp.begin(localPort);
}

void loop()
{
  //probeGPS();
  ip = WiFi.localIP();
  rssi = WiFi.RSSI();
  int8_t acclX = mySensor.readXData();
  int8_t acclY = mySensor.readYData();
  int8_t acclZ = mySensor.readZData();

  Udp.beginPacket(serverIP, serverPort);
  Udp.print("{ rssi: \"");
  Udp.print(rssi);
  Udp.print("\", ip: \"");
  Udp.print(ip);
  Udp.print("\", \"x\":\"");
  Udp.print(acclX);
  Udp.print("\", \"y\":\"");
  Udp.print(acclY);
  Udp.print("\", accl_z: \"");
  Udp.print(acclZ);
  Udp.print("\", Lat: \"");
  Udp.print(LAT);
  Udp.print("\", LNG: \"");
  Udp.print(LNG);
  Udp.print("\", ALT: \"");
  Udp.print(GPS_ALT);
  Udp.print("', GPS_SPD: '");
  Udp.print(GPS_SPD);
  Udp.print("' }");
  Udp.endPacket();
  delay(10);
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
  } else if(GPS.startsWith("$GPRMC")) {
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
  //LAT = GPS.substring(GPS.indexOf(",N,") - 10, GPS.indexOf(",N,"));
  //LNG = GPS.substring(GPS.indexOf(",W,") - 11, GPS.indexOf(",W,"));
  //GPS_ALT = GPS.substring(GPS.indexOf(",M,") - 5, GPS.indexOf(",M,"));
  //GPS_SPD = GPS.substring(GPS.indexOf("
}

