import microbit
from microbit import uart
from microbit import *

uart.init(baudrate=1200, bits=8, parity=None, stop=1, tx=None, rx=None)

stable = Image("00000:"
              "00900:"
              "09990:"
              "00900:"
              "00000:")

image_E = Image("00990:"
              "00090:"
              "00009:"
              "00090:"
              "00990:")

image_W = Image("09900:"
              "09000:"
              "90000:"
              "09000:"
              "09900:")

images = {"E":image_E,
          "W": image_W,
          "": stable}

#Start the Loop
while 1:
    #Get Accelerometer Values
    x,y,z  = microbit.accelerometer.get_values()
    direction = ""  
    
    if x>60:
        direction += "E"
    elif x<-60:
        direction += "W"


    if direction != "":
       print(direction)
        
    if button_a.was_pressed():
        print("F")

    if button_b.was_pressed():
        print("R")

    microbit.display.show(images[direction])
        
============================================================= 

import processing.serial.*;
Serial myPort;
int numObjects = 10;

boolean once = true;
boolean left, right, space;

int score;
int oldScore = 0;

float[] positionsX = new float[numObjects];
float[] positionsY = new float[numObjects];
float[] velocitiesX = new float[numObjects];
float[] velocitiesY = new float[numObjects];

float playerX;
float playerY;
float playerSpeed = 8;
ArrayList<PVector> bullets = new ArrayList<PVector>();
float bulletSpeed = 7;
int playerLives = 3;

int hitCooldownFrames = 60;  // number of frames to wait before declaring game over after being hit
int hitCooldownCounter = 0;

int bulletCooldownFrames = 20; // number of frames to wait between 2 consecutive bullets fired
int bulletCooldownCounter = 0;

color playerColor = color(0, 0, 255);  // initial player color

void microbitSetup(){
  println(Serial.list());
  int lastport = Serial.list().length;
  String portName = Serial.list()[lastport-1]; 
 
  myPort = new Serial(this, portName, 1200);
  myPort.bufferUntil('\n');
  once = false;
  
}

void setup() {
  size(1100, 800);
  
  playerX = width/2 - 10;
  playerY = height - 40;
  
  if(once == true){
     microbitSetup();
  }
 
  for (int i = 0; i < numObjects; i++) {
    positionsX[i] = random(width);
    positionsY[i] = random(-height * 4  , -height * 3);
    velocitiesX[i] = random(-2, 2);
    velocitiesY[i] = random(2, 9);
  }
  

}

void draw() {
  background(255);
  
  String inString = myPort.readStringUntil('\n');
  
  if (inString != null && !inString.equals("")) {
    inString = trim(inString);
    print(inString);
    
    
    if(inString.equals("R")){
      if (playerLives == 0) {
        playerLives = 3;  
        score = 0;
        setup();  
    }
       
    }
  
    
    if(inString.equals("F")){
      if(bulletCooldownCounter == 0 && playerLives > 0){
        bullets.add(new PVector(playerX + 20, playerY));
        bulletCooldownCounter = bulletCooldownFrames;
      }
       
    }
    
    if(inString.equals("W")){
      playerX -= playerSpeed;
      if (playerX < 0) {
        playerX = width;  // wrap around to the right side
      }
    }
      
    
    if(inString.equals("E")){
      playerX += playerSpeed;
      if (playerX > width) {
        playerX = 0;  // Wrap around to the left side
      }
    }
      
 
 }
  
  
  
  // Check for collisions with falling objects
  for (int i = 0; i < numObjects; i++) {
    
    float distance = dist(positionsX[i], positionsY[i], playerX + 20, playerY + 10);
    if (distance < 20 && hitCooldownCounter == 0) {
      playerLives--;
      hitCooldownCounter = hitCooldownFrames;
      playerColor = color(255, 0, 0);  // Change player color to red when hit
      if (playerLives <= 0) {
        playerLives = 0;
 
      }
      
    }

    positionsX[i] += velocitiesX[i];
    positionsY[i] += velocitiesY[i];

    if (positionsY[i] > height) {
      positionsY[i] = -20;
      positionsX[i] = random(width);
      
      if(playerLives > 0)
        score++;
    }

    fill(0);
    ellipse(positionsX[i], positionsY[i], 20, 20);
  }

   
   
    // increase the difficulty
    if(score - oldScore > 3){
     
      for (int i = 0; i < numObjects; i++) {
        if(velocitiesY[i] < 10)
          velocitiesY[i]+=0.1 * sqrt(velocitiesY[i]);
        else if(velocitiesY[i] < 12)
          velocitiesY[i]+=0.01 * sqrt(velocitiesY[i]);
        else velocitiesY[i]+=0.001 * sqrt(velocitiesY[i]);  
    }
      
      oldScore = score;
   }

  // Draw player object only if lives > 0
  if (playerLives > 0) {
    fill(playerColor);
    rect(playerX, playerY, 40, 20);
  } else {
       
     textSize(90);
     text("GAME OVER", width/2 - 200, height/2); 

  }

  for (int i = bullets.size() - 1; i >= 0; i--) {
    PVector bullet = bullets.get(i);
    bullet.y -= bulletSpeed;
    fill(255, 0, 0);
    ellipse(bullet.x, bullet.y, 10, 10);
    if (bullet.y < 0) {
      bullets.remove(i);
    }
    
    for (int j = 0; j < numObjects; j++) {  // check collision of bullets with obstacles
      float distance = dist(positionsX[j], positionsY[j], bullet.x, bullet.y);
      
      if(distance<20){
         positionsY[j] = -20;
         positionsX[j] = random(width);
         //bullets.remove(i);
      }
    
    }
    
    
  }

  // Display remaining lives
  fill(255, 0, 0);
  textSize(30);
  text("Lives: " + playerLives, 10, 30);
  text("Score: " + score, 10, 50);

  // Handle hit cooldown
  if (hitCooldownCounter > 0) {
    hitCooldownCounter--;
    if (hitCooldownCounter == 0) {
      playerColor = color(0, 0, 255);  // reset player color after hit cooldown
    }
  }
  
  if(bulletCooldownCounter > 0)
    bulletCooldownCounter--;
 
  
}

void keyPressed() {
 // if (keyCode == 32) {
 //   bullets.add(new PVector(playerX + 20, playerY));
 // } 
  
 if (key == 'R' || key == 'r') {
    // restore lives when 'R' is pressed
    if (playerLives == 0) {
      playerLives = 3;  
      score = 0;
      setup();  
    }
  }
}
