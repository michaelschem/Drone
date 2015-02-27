class altimeter {
  void display(float alt) {
    fill(255);
    stroke(0);
    rect(500,100,80,400);
    fill(0);
    rect(500,80,80,20);
    fill(50,92,235);
    textSize(20);
    text("ALT",520,98);
    
    
    //draw heights
    fill(0);
    
    for(int i = 0; i < 16; i++) {
      line(500,100 + (i * 25),510,100 + (i * 25));
    }
    strokeWeight(3);
    for(int i = 0; i < 4; i++) {
      line(500,100 + (i * 100),530,100 + (i * 100));
      text(400 - (i * 100), 540, 120 + (i * 100));
    }
    
    rect(490, 500 - alt, 50, 20);
    fill(255);
    textSize(15);
    text(alt, 490, 515 - alt);
    
    //put strokeWeight back
    strokeWeight(1);
  }
  
}
