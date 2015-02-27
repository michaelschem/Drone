import hypermedia.net.*;

angle a1;
compas c1;
altimeter a2;
speed s1;
UDP udp;
JSONObject json;

float pitchAngle = 0, rollAngle = 0, headingAngle = 0, temperature;
float time, last_time, fps, last_fps;

void setup() {
  last_time = second() + (minute() * 60);
  size(600, 600);

  udp = new UDP( this, 42679 );  
  udp.log( false );
  udp.listen( true );

  a1 = new angle();
  c1 = new compas();
  a2 = new altimeter();
  s1 = new speed();
}

void receive( byte[] data ) {
  fps++;
  String input = new String(data);

  pitchAngle = (Float.parseFloat(getElement(input, "pitch")) + pitchAngle)/2;
  rollAngle = (Float.parseFloat(getElement(input, "roll")) + rollAngle)/2;
  headingAngle = (Float.parseFloat(getElement(input, "BARO_ALT")) + headingAngle)/2;
  temperature = (Float.parseFloat(getElement(input, "TEMP")) + temperature)/2;
}

String getElement(String json, String element) {

  json = json.replaceAll(" ", "");
  println(json);
  String first = json.substring(json.indexOf("\"" + element + "\":") + element.length() + 4, json.length());
  String val = first.substring(0, first.indexOf("\""));

  return val;
}

void reset() {
  stroke(0);
  background(39, 118, 239);
  fill(138, 71, 1);
  strokeWeight(0);
  rect(0, 300, 600, 300);
  strokeWeight(1);

  //FPS CALCULATION
  time = second() + (minute() * 60);
  if (time != last_time) {
    last_fps = fps;
    fps = 0;
    last_time = second() + (minute() * 60);
  }

  textSize(12);
  text("FPS: " + last_fps, 10, 10);
  text("TEMP: " + temperature, 10, 20);
}

void draw() {
  reset();

  pushMatrix();
  pushMatrix();
  pushMatrix();
  a1.rot(radians(rollAngle));
  a1.dispaly(pitchAngle);

  popMatrix();
  c1.rot(radians(0));
  c1.display(0);

  popMatrix();
  a2.display(0);
  
  popMatrix();
  s1.display(0);
}
