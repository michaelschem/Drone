class compas {
  void display(float degree) {

    fill(64, 22, 19);
    stroke(64, 22, 19);
    strokeWeight(0);
    ellipse(0, 0, 200, 200);
    
    stroke(255);
    strokeWeight(1);
    line(5,5,-5,-5);
  }

  void rot(float i) {
    translate(300, 450);
    rotate(i);
  }
}
