class compas {
  void display(int degree) {

    fill(64, 22, 19);
    stroke(64, 22, 19);
    strokeWeight(0);
    ellipse(0, 0, 200, 200);

    fill(000);
    stroke(255);
    rect(-25, -145, 50, 20);

    fill(255);
    stroke(255);
    triangle(-10, -125, 10, -125, 0, -95);
  }

  void rot(float i) {
    translate(300, 450);
    rotate(i);
  }
}
