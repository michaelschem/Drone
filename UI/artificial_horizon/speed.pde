class speed {

  void display(float speed) {
    fill(255);
    stroke(0);
    rect(20, 100, 80, 400);
    fill(0);
    rect(20, 80, 80, 20);
    fill(50, 92, 235);
    textSize(20);
    text("SPD", 40, 98);


    //draw heights
    fill(0);

    for (int i = 0; i < 16; i++) {
      line(70, 100 + (i * 25), 80, 100 + (i * 25));
    }
    strokeWeight(3);
    for (int i = 0; i < 4; i++) {
      line(70, 100 + (i * 100), 100, 100 + (i * 100));
      text(100 - (i * 25), 25, 120 + (i * 100));
    }

    rect(60, 500 - speed, 50, 20);
    fill(255);
    textSize(15);
    text((int)speed, 65, 515 - speed);
  }
}
