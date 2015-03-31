class compas {
  PImage compass; 
  
  void display(float degree) {
    compass = loadImage("/home/mac/Drone/UI/artificial_horizon/data/compass.png");

    fill(64, 22, 19);
    stroke(64, 22, 19);
    strokeWeight(0);
    ellipse(0, 0, 200, 200);
    
    stroke(255);
    strokeWeight(1);
    line(5,5,-5,-5);
    image(compass, -100, -100, 200, 200);
  }

  void rot(float i) {
    
    translate(300, 450);
    rotate(-i);
  }
}
