import hypermedia.net.*;

int map_width = 12011;
int map_height = 8738;
int map_zoom = 10;
int map_x_offset = map_width/2;
int map_y_offset = map_height/2;

angle a1;
compas c1;
altimeter a2;
speed s1;
compass_deg c2;
UDP udp;

PImage image;

JSONObject json;

int history = 1;
int gain = 5;

float lastPitch[] = new float[history];
float lastRoll[] = new float[history];

float pitchAngle = 0, rollAngle = 0, headingAngle = 0, temperature, baro_alt = 0, heading = 0, baro_spd = 0;
float time, last_time, fps, last_fps;

void setup() {
  size(1200, 600);

  image = loadImage("/home/mac/Drone/UI/artificial_horizon/data/test.jpg");
  //image = loadImage("/home/mac/Drone/UI/artificial_horizon/data/map_big.jpg");
  last_time = second() + (minute() * 60);

  udp = new UDP( this, 42679 );  
  udp.log( false );
  udp.listen( true );

  a1 = new angle();
  c1 = new compas();
  a2 = new altimeter();
  s1 = new speed();
  c2 = new compass_deg();
}

void draw() {
  reset();

  pushMatrix();
  pushMatrix();
  pushMatrix();
  a1.rot(radians(rollAngle));
  a1.dispaly(pitchAngle);

  popMatrix();

  c1.rot(radians(heading));
  c1.display(heading);


  popMatrix();
  c2.display(heading);
  a2.display(baro_alt);

  popMatrix();
  s1.display(baro_spd);
}

void receive( byte[] data ) {
  fps++;
  String input = new String(data);
  // Check for inputs and adjust for noise
  if (!getElement(input, "roll").equals("false")) {
//    pitchAngle = threshold(input, lastPitch[history-1], "pitch");
    pitchAngle = - removeNoise(avg(input, lastPitch, "roll"));
  }
  if (!getElement(input, "pitch").equals("false")) {
//    rollAngle = threshold(input, lastRoll[history-1], "roll");
    rollAngle = removeNoise(avg(input, lastRoll, "pitch"));
  }
  if (!getElement(input, "BARO_ALT").equals("false")) baro_alt = (Float.parseFloat(getElement(input, "BARO_ALT")) + baro_alt)/2;
  if (!getElement(input, "TEMP").equals("false")) temperature = (Float.parseFloat(getElement(input, "TEMP")) + temperature)/2;
  if (!getElement(input, "heading").equals("false")) heading = Float.parseFloat(getElement(input, "heading"));
  if (!getElement(input, "BARO_SPD").equals("false")) baro_spd = Float.parseFloat(getElement(input, "BARO_SPD"));
}

float removeNoise(float raw) {
  raw = (int)raw;
  //print("raw: " + raw + " nonoise: " + (raw + (gain % raw)));
  return (int)raw + (int)(gain % raw);
}

float threshold(String input, float prevInput, String element) {
 float thresh = Float.parseFloat(getElement(input, element));
 float diff = abs(thresh - prevInput);
 if (diff < 1) 
   return (int) prevInput;
 else 
   return (int) thresh;
}

String getElement(String json, String element) {
  String val = "false";
  json = json.replaceAll(" ", "");
  println(json);

  if (json.indexOf(element) != -1) {
    String first = json.substring(json.indexOf("\"" + element + "\":") + element.length() + 4, json.length());
    val = first.substring(0, first.indexOf("\""));
  }

  return val;
}

void reset() {

  image(image, -20, -100, map_width/map_zoom, map_height/map_zoom );

  stroke(0);
  strokeWeight(0);
  fill(39, 118, 239);
  rect(0, 0, 600, 300);
  fill(138, 71, 1);
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

float avg(String input, float last[], String element) {
  last[0] = Float.parseFloat(getElement(input, element));
  float avg = 0;
  for (int i = 0; i < history; i++) {
    avg += last[i];
  }

  for (int i = 1; i < history; i++) {
    last[i] = last[i - 1];
  }

  return avg/history;
}


