// Bounce.pde
// -*- mode: C++ -*-
//
// Make a single stepper bounce from one limit to another
//
// Copyright (C) 2012 Mike McCauley
// $Id: Random.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

#include <AccelStepper.h>
#include <MultiStepper.h>

#define LMOT_STEP 2
#define LMOT_DIR 5
#define RMOT_STEP 4
#define RMOT_DIR 7
#define ENA_PIN 8

#define MAX_MOT_SPEED 10 //mm per second
#define MACHINE_WIDTH 350.0   //how wide are the motors
#define VERTICAL_OFFSET 215.0 //how far down from horizontal chain is 0,0?

#define STEPS_PER_REVOLUTION 200
#define MICROSTEPPING 32
#define PULLY_DIAMETER 24
#define MM_PER_STEP (1.0 * (PULLY_DIAMETER * PI)/(STEPS_PER_REVOLUTION * MICROSTEPPING))

const double HALF_MACHINE_WIDTH = MACHINE_WIDTH/2.0;
double last_x = 0;
double last_y = 0;
double lastSpeed = 0;

String command = "";
boolean commandReady = false;
boolean moving = false;

long positions[2];

// Define a stepper and the pins it will use
AccelStepper lmot(AccelStepper::DRIVER, LMOT_STEP, LMOT_DIR);
AccelStepper rmot(AccelStepper::DRIVER, RMOT_STEP, RMOT_DIR);

//MultiStepper
MultiStepper steppers;

boolean moveComplete = true;

void setup()
{  
  setupSteppers();
  Serial.begin(115200);
  warp(0,0);
  Serial.println(F("VogDrawbot v0.1"));
  Serial.print(F("MachineWidth"));
  Serial.println(MACHINE_WIDTH);
  Serial.println("Ready");
}
void loop()
{
    if (moveComplete && commandReady){
      handleCommand(command);
    } 
    if(moveComplete && moving){
      moving = false;
      Serial.println("Ok");
      showCurrentPosition();
    }

    moveComplete = !steppers.run();
}

void setSpeed(float mm){
  lastSpeed = mm;
  lmot.setMaxSpeed((long)(mm/MM_PER_STEP));
  rmot.setMaxSpeed((long)(mm/MM_PER_STEP));
}

void setupSteppers(){
  lmot.setEnablePin(ENA_PIN);
  lmot.setPinsInverted(false,false,true);
  setSpeed(MAX_MOT_SPEED);
  steppers.addStepper(lmot);
  steppers.addStepper(rmot);
  copyMotorPositions();
}

void copyMotorPositions(){
  positions[0] = lmot.currentPosition();
  positions[1] = rmot.currentPosition();
}

void gotoMM(double lmm,double rmm){
  positions[0] = convertMMtoSteps(lmm);
  positions[1] = convertMMtoSteps(rmm);
  steppers.moveTo(positions);
  moving = true;
  moveComplete = !steppers.run();
}

void gotoXY(double x, double y){
  last_x = x;
  last_y = y;
  double ll = pythag(HALF_MACHINE_WIDTH+x,y+VERTICAL_OFFSET);
  double rl = pythag(HALF_MACHINE_WIDTH-x,y+VERTICAL_OFFSET);
  gotoMM(ll,rl);
}



void warp(double x,double y){
  last_x = x;
  last_y = y;
  y += (double)VERTICAL_OFFSET;
  if(x == 0){
    if(y == 0){
      //horizontal... should never happen?
      long steps = convertMMtoSteps(HALF_MACHINE_WIDTH);
      setPosition(steps,steps);
      return; 
    }
    //on centerline... both left and right are the same
    double mm = pythag(HALF_MACHINE_WIDTH,y);
    long steps = convertMMtoSteps(mm);
    setPosition(steps,steps);
    return;
  }
  if(y == 0){
    setPosition(convertMMtoSteps(HALF_MACHINE_WIDTH+x),convertMMtoSteps(HALF_MACHINE_WIDTH-x));
    return;
  }
  //x and y are not zero have to calc
  double ll = pythag(HALF_MACHINE_WIDTH+x,y);
  double rl = pythag(HALF_MACHINE_WIDTH-x,y);
  setPosition(convertMMtoSteps(ll),convertMMtoSteps(rl));
}

double pythag(double x, double y){
  return sqrt(sq(x) + sq(y));
}

void setPosition(long ls,long rs){
  lmot.setCurrentPosition(ls);
  rmot.setCurrentPosition(rs);
}

void enableSteppers(){
  lmot.enableOutputs();
}

void disableSteppers(){
  lmot.disableOutputs();
}

void showCurrentPosition(){
  Serial.print(F("Current step position "));
  Serial.print(lmot.currentPosition());
  Serial.print(",");
  Serial.println(rmot.currentPosition());
}

void showTargetPosition(){
  Serial.print(F("Target step position "));
  Serial.print(lmot.targetPosition());
  Serial.print(",");
  Serial.println(rmot.targetPosition());
}

void showMaxSpeeds(){
  Serial.print(F("Current speeds "));
  Serial.print(lmot.maxSpeed());
  Serial.print(",");
  Serial.println(rmot.maxSpeed());
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    command += inChar;
    if (inChar == '\n') {
      command.toUpperCase();
      int idx = command.indexOf(' ');
      while(idx != -1){
        command.remove(idx);
      }
      commandReady = true;
    }
  }
}

long convertMMtoSteps(double mm){
  return (long)(mm/MM_PER_STEP);
}

double convertStepstoMM(long steps){
  return (double)(MM_PER_STEP * steps);
}

void handleCommand(String &command){
  commandReady = false;
  parseCommand(command);
  command = "";
}

void parseCommand(String &command){
  command.toUpperCase();
  if(command.charAt(0) == 'G')
    parseGCommand(command);
  else
    parseMCommand(command);
}

void parseMCommand(String &com){
  if(com.charAt(1) == '1' and com.charAt(2) == '7'){
    enableSteppers();
    Serial.println("Ok");
  }else if(com.charAt(1) == '1' and com.charAt(2) == '8') {
    disableSteppers();
    Serial.println("Ok");
  }else if(com.charAt(1) == '1' and com.charAt(2) == '1' and com.charAt(3) == '4') {
    Serial.print("X");
    Serial.print(last_x);
    Serial.print("Y");
    Serial.print(last_y);
    Serial.print("F");
    Serial.println(lastSpeed);
    Serial.println("Ok");
  }else{
    Serial.println("Err Unknown Command" + com);
  }
}

void parseGCommand(String &com){
  if(com.charAt(1) == '1' or com.charAt(1) == '0'){
    float tgt_x = -9999;
    float tgt_y = -9999;
    float tgt_f = -9999;
    
    int xidx = com.indexOf('X');
    int yidx = com.indexOf('Y');
    int fidx = com.indexOf('F');
    if(xidx != -1){
      //we have a x index
      if(yidx == -1 and fidx == -1){
        //only x just read it in
        tgt_x = com.substring(xidx+1).toFloat();
      }else{
        if(yidx == -1){
          //no y but there must be a f
          if(fidx < xidx){
            //f before x
            tgt_f = com.substring(fidx+1,xidx).toFloat();
            tgt_x = com.substring(xidx+1).toFloat();
          }else{
            //x before f
            tgt_x = com.substring(xidx+1,fidx).toFloat();
            tgt_f = com.substring(fidx+1).toFloat();
          }
        }else if(fidx == -1){
          //x and y defined, missing f
          if(yidx < xidx){
            //y before x
            tgt_y = com.substring(yidx+1,xidx).toFloat();
            tgt_x = com.substring(xidx+1).toFloat();
          }else{
            //x before y
            tgt_x = com.substring(xidx+1,fidx).toFloat();
            tgt_y = com.substring(yidx+1).toFloat();
          }
        }else{
          //all defined lets get order
          //{f,y,x}
          if(xidx < yidx and yidx < fidx){
            //order x,y,f
            tgt_x = com.substring(xidx+1,yidx).toFloat();
            tgt_y = com.substring(yidx+1,fidx).toFloat();
            tgt_f = com.substring(fidx+1).toFloat();
          }else if(yidx < xidx and xidx < fidx){
            //order y,x,f
            tgt_y = com.substring(yidx+1,xidx).toFloat();
            tgt_x = com.substring(xidx+1,fidx).toFloat();
            tgt_f = com.substring(fidx+1).toFloat();
          }else if(yidx < fidx and fidx < xidx){
            //order y,f,x
            tgt_y = com.substring(yidx+1,fidx).toFloat();
            tgt_f = com.substring(fidx+1,xidx).toFloat();
            tgt_x = com.substring(xidx+1).toFloat();
          }else if(xidx < fidx and fidx < yidx){
            //order x,f,y
            tgt_x = com.substring(xidx+1,fidx).toFloat();
            tgt_f = com.substring(fidx+1,yidx).toFloat();
            tgt_y = com.substring(yidx+1).toFloat();
          }else if(fidx < xidx and xidx < yidx){
            //order f,x,y
            tgt_f = com.substring(fidx+1,xidx).toFloat();
            tgt_x = com.substring(xidx+1,yidx).toFloat();
            tgt_y = com.substring(yidx+1).toFloat();
          }else{
            //order f,y,x
            tgt_f = com.substring(fidx+1,yidx).toFloat();
            tgt_y = com.substring(yidx+1,xidx).toFloat();
            tgt_x = com.substring(xidx+1).toFloat();
          }
        }
        
      }
    }else{
      //x not defined
      if(fidx == -1){
        //only y defined
        tgt_y = com.substring(yidx+1).toFloat();
      }else if(yidx == -1){
        //only f defined
        tgt_f = com.substring(fidx+1).toFloat();
      }else{
        //f and y defined
        if(fidx < yidx){
          tgt_f = com.substring(fidx+1,yidx).toFloat();
          tgt_y = com.substring(yidx+1).toFloat();  
        }else{
          tgt_y = com.substring(yidx+1,fidx).toFloat();
          tgt_y = com.substring(fidx+1).toFloat();  
        }
      }      
    }
    if(tgt_f != -9999)
      setSpeed(tgt_f);
    if(tgt_x == -9999){
      tgt_x = last_x;
    }
    if(tgt_y == -9999){
      tgt_y = last_y;
    }
    gotoXY(tgt_x,tgt_y);
    
  }else{
    if(com.charAt(1) == '9' and com.charAt(2) == '2'){
      warp(0,0);
      Serial.println(F("Ok")); 
    }
    else{
      Serial.print(F("Err Unknown Command"));
      Serial.println(com);  
    }
  }
}
