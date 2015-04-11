#include <WiFi.h>

char ssid[] = "Beaconx";
char pass[] = "password";

void setup()
{
  //bit 1
  pinMode(10, OUTPUT);
  digitalWrite(10, HIGH);
  pinMode(30, INPUT);
  
  //bit 2
  pinMode(9, OUTPUT);
  digitalWrite(9, HIGH);
  pinMode(29, INPUT);
  
  //bit 3
  pinMode(8, OUTPUT);
  digitalWrite(8, HIGH);
  pinMode(28, INPUT);
  
  delay(1000);
  
  int bit1 = digitalRead(30);
  int bit2 = digitalRead(29);
  int bit3 = digitalRead(28);
  
  int beaconNumber = 1*bit1 + 2*bit2 + 4*bit3;
  ssid[6] = beaconNumber+48;
  
//  Serial.begin(9600);
//  Serial.print("Setting up Access Point named ");
//  Serial.println(ssid);
  
  WiFi.beginNetwork(ssid, pass);
//  while(WiFi.localIP() == INADDR_NONE)
//  {
//    Serial.print('.');
//    delay(300);
//  }
//   
//  Serial.println("Access Point is Active");
}

void loop()
{
  delay(1000);
}
