class compass_deg {
  void display(float degree) {

    fill(255);
    stroke(255);
    triangle(285, 320, 315, 320, 300, 355);
    
    fill(000);
    stroke(255);
    rect(275, 320, 50, 20);

    fill(255);
    textSize(18);
    text(floor(180 + degree), 280, 337);
    textSize(12);
    text("o",315,330);
  }
}

