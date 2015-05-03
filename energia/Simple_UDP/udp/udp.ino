#include <WiFi.h>
#include <Adafruit_10DOF.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <BMA222.h>

char ssid[] = "Dr1";
char password[] = "theDRONEteam1";
unsigned int localPort = 2390;
char serverIP[] = "192.168.1.102";
int serverPort = 42679;
IPAddress ip;
long rssi;
//GPS Stuff
String gpsBuffer, GPS, LNG, LAT, GPS_ALT, GPS_SPD, GPS_TIME, BARO_ALT;
char GPS_DATA[30][30];
char GPS_DATA2[30][30];
boolean newGPS;

WiFiUDP Udp;
BMA222 mySensor;

/* Assign a unique ID to the sensors */
Adafruit_10DOF                dof   = Adafruit_10DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       bmp   = Adafruit_BMP085_Unified(18001);

/* Update this with the correct SLP for accurate altitude measurements */
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;

/**************************************************************************/
/*!
 @brief  Initialises all the sensors used by this example
 */
/**************************************************************************/
void initSensors()
{
  if(!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while(1);
  }
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while(1);
  }
  if(!bmp.begin())
  {
    /* There was a problem detecting the BMP180 ... check your connections */
    Serial.println("Ooops, no BMP180 detected ... Check your wiring!");
    while(1);
  }
}

void setup()
{
  Serial.begin(9600);
  initSensors();
  newGPS = false;
  mySensor.begin();
  uint8_t chipID = mySensor.chipID();

  WiFi.begin(ssid, password);

  Udp.begin(localPort);
  
  ip = WiFi.localIP();
  rssi = WiFi.RSSI();
}

void loop()
{
  //probeGPS();
  
  //int8_t acclX = mySensor.readXData();
  //int8_t acclY = mySensor.readYData();
  //int8_t acclZ = mySensor.readZData();
  sensors_event_t accel_event;
  sensors_event_t mag_event;
  sensors_event_t bmp_event;
  sensors_vec_t   orientation;

  /* Read the accelerometer and magnetometer */
  accel.getEvent(&accel_event);
  mag.getEvent(&mag_event);

  bmp.getEvent(&bmp_event);

  Udp.beginPacket(serverIP, serverPort);
  Udp.print("{ rssi: \"");
  Udp.print(rssi);
  Udp.print("\", ip: \"");
  Udp.print(ip);
  if (dof.fusionGetOrientation(&accel_event, &mag_event, &orientation))
  {
    Udp.print("\", \"roll\":\"");
    Udp.print(orientation.roll);
    Udp.print("\", \"pitch\":\"");
    Udp.print(orientation.pitch);
    Udp.print("\", \"heading\": \"");
  }
  Udp.print(orientation.heading);
  Udp.print("\", \"Lat\": \"");
  Udp.print(LAT);
  Udp.print("\", \"LNG\": \"");
  Udp.print(LNG);
  Udp.print("\", \"ALT\": \"");
  Udp.print(GPS_ALT);
  if (bmp_event.pressure)
  {
    /* Get ambient temperature in C */
    float temperature;
    bmp.getTemperature(&temperature);
    Udp.print("\", \"BARO_ALT\": \"");
    Udp.print(bmp.pressureToAltitude(seaLevelPressure,bmp_event.pressure,temperature));
    Udp.print("\", \"TEMP\": \"");
    Udp.print(temperature);
  }
  Udp.print("\", GPS_SPD: \"");
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


