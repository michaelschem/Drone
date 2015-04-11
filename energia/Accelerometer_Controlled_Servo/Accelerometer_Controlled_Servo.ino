#include <Wire.h>
#include <BMA222.h>
#include <Servo.h>

BMA222 mySensor;
Servo myservo;  // create servo object to control a servo
                // a maximum of eight servo objects can be created
int pos = 0;    // variable to store the servo position

void setup()
{
  myservo.attach(2);  // attaches the servo on Port pin 2; can have 8 servos
  Serial.begin(115200); //baud

  mySensor.begin();
  uint8_t chipID = mySensor.chipID();
  Serial.print("chipID: ");
  Serial.println(chipID);
}

void loop()
{
  // accelerometer data
  int8_t x = mySensor.readXData();
  Serial.print("X: ");
  Serial.print(x);

  int8_t y = mySensor.readYData();
  Serial.print(" Y: ");
  Serial.print(y);

  int8_t z = mySensor.readZData();
  Serial.print(" Z: ");
  Serial.println(z);

  // servo control
  if (y < -5)
  {
    // nose is down
    // rotate cw
    pos = 180;
    myservo.write(pos);
  }
  else if (y > 5)
  {
    // nose is up
    // rotate ccw
    pos = 0;
    myservo.write(pos);
  }
  else if (y > -5 && y < 5)
  {
    // neutral position
    pos = 90;
    myservo.write(pos);
  }

  delay(10);
}
