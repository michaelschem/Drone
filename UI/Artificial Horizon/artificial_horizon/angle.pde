class angle {
  angle() {
  }

  void dispaly(float y) {
    stroke(255);
    strokeWeight(1);
    fill(255);
    for (int i = 9; i >= -9; i--) {
      //angle degree markings
      line(-50, i * 50 + (y * 5), 50, i * 50 + (y * 5) );
      textSize(10);
      text((i * 10) * -1, 70, (i * 50) + (y * 5) );
      text((i * 10) * -1, -80, (i * 50) + (y * 5) );
    }
    //plane
    stroke(45, 255, 0);
    strokeWeight(4);
    line(60, y * 5, 140, y * 5);
    line(-140, y * 5, -60, y * 5);
  }

  void rot(float i) {
    translate(300, 300);
    rotate(i);
  }
}

