import hypermedia.net.*;

angle a1;
UDP udp;
JSONObject json;

int pitchAngle = 0;
int rollAngle = 0;
int time;

void setup() {
  size(300, 300);

  udp = new UDP( this, 6000 );  
  udp.log( false );
  udp.listen( true );

  a1 = new angle();
}

void receive( byte[] data ) {
  String input = new String(data);

  pitchAngle = Integer.parseInt(getElement(input, "x"));
  rollAngle = Integer.parseInt(getElement(input, "y"));
}

String getElement(String json, String element) {

  json = json.replaceAll(" ", "");
  String first = json.substring(json.indexOf("\"" + element + "\":") + 5, json.length());
  String val = first.substring(0, first.indexOf("\""));

  return val;
}

void reset() {
  stroke(0);
  background(39, 118, 239);
  fill(138, 71, 1);
  strokeWeight(0);
  rect(0, 150, 300, 300);
  stroke(255);
  strokeWeight(4);
  line(0, 148, 300, 148);
  strokeWeight(1);
}

void draw() {
  reset();
  a1.rot(radians(rollAngle));
  a1.dispaly(pitchAngle);
}

