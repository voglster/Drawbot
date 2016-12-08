#include <Servo.h>

#define LMOT_STEP 2
#define LMOT_DIR 5
#define RMOT_STEP 4
#define RMOT_DIR 7
#define ENA_PIN 8

#define MAX_MOT_SPEED 20 //mm per second
#define MACHINE_WIDTH 446.5   //how wide are the motors
#define VERTICAL_OFFSET 110.0 //how far down from horizontal chain is 0,0?

#define STEPS_PER_REVOLUTION 200
#define MICROSTEPPING 32
#define PULLY_DIAMETER 24
#define MM_PER_STEP ((PULLY_DIAMETER * PI)/(STEPS_PER_REVOLUTION * MICROSTEPPING))

#define SERVO_PIN 11
#define DOWN_ANGLE 0
#define UP_ANGLE 90

#define PEN_DOWN 0
#define PEN_UP 1 

#define HALF_MACHINE_WIDTH (MACHINE_WIDTH / 2.0)

#define COMMAND_BUFFER_SIZE              (20)                                   // What is the longest message Arduino can store?
// new constants

#define VERSION              (2)                      // firmware version
#define BAUD                 (115200)                 // How fast is the Arduino talking?(BAUD Rate of Arduino)
#define SERIAL_BUFFER_SIZE   (64)                                   // What is the longest message Arduino can store?
#define STEPS_PER_TURN       (STEPS_PER_REVOLUTION * MICROSTEPPING) // depends on your stepper motor.  most are 200.
#define STEPS_PER_MM         (STEPS_PER_TURN/(PULLY_DIAMETER * PI))                // (400*16)/0.8 with a M5 spindle
#define MAX_FEEDRATE         (1000000)
#define MIN_FEEDRATE         (1)
#define NUM_AXIES            (4)

#define DEBUG 1

typedef struct {
  long delta;  // number of steps to move
  long absdelta;
  long over;  // for dx/dy bresenham calculations
} Axis;

typedef struct {
  long left_steps;
  long right_steps;
  byte pen_state;
  long feed_rate;
  long delay_ms;
} Command;

Command commands[COMMAND_BUFFER_SIZE];

byte current_command_index = 0;
byte next_command_index = 1;

char serial_buffer[SERIAL_BUFFER_SIZE];  // where we store the message until we get a ';'
byte serial_buffer_index;  // how much is in the buffer

void clear_command_buffer(){
  for(int i=0; i < COMMAND_BUFFER; i++){
    commands[i].left_steps  = 0;
    commands[i].right_steps = 0;
    commands[i].pen_state   = PEN_DOWN;
    commands[i].feed_rate   = 0;
    commands[i].delay_ms    = 0;
  }
  location_index = 0;
  next_command_index = 1;
}

int next_command_buffer_index(int last_index){
  last_index++;
  if(last_index == COMMAND_BUFFER_SIZE)
    last_index = 0;
  return last_index;
}

bool another_command_ready(){
  return !(next_command_buffer_index(current_command_index) == next_command_index);
}

bool is_buffer_full(){
  return !(next_command_buffer_index(next_command_index) == current_command_index);
}

void ProcessSerial(){
  if(Serial.available() > 0) {  // if something is available
    char c=Serial.read();  // get it
#ifdef DEBUG
    Serial.print(c);  // repeat it back so I know you got the message
#endif
    if(serial_buffer_index<SERIAL_BUFFER_SIZE-1) serial_buffer[serial_buffer_index++]=c;  // store it
    if(c=='\n') {
      // entire message received
      serial_buffer[serial_buffer_index]=0;  // end the buffer so string functions work right
#ifdef DEBUG
      Serial.print(F("\r\n"));  // echo a return character for humans
#endif
      processCommand();  // do something with the command
      ready();
    }
  }
}

void ready(){
  while(!is_buffer_full())
    Serial.println(F("Ready"));  // echo a return character for humans
}



double last_x = 0;
double last_y = 0;
double lastSpeed = 0;

String command = "";
boolean commandReady = false;
boolean moving = false;

long positions[2];

Servo penServo;

boolean moveComplete = true;

void setup()
{
	clear_command_buffer();
  penServo.attach(SERVO_PIN);
	Serial.begin(115200);
	penDown();
	penUp();
	warp(0, 0);
	Serial.println(F("VogDrawbot v0.1"));
	Serial.print(F("MachineWidth"));
	Serial.println(MACHINE_WIDTH);
	Serial.println("Ready");
}

void loop()
{
  ProcessSerial();
}

void gotoXY(double x, double y) {
	last_x = x;
	last_y = y;
	double ll = pythag(HALF_MACHINE_WIDTH + x, y + VERTICAL_OFFSET);
	double rl = pythag(HALF_MACHINE_WIDTH - x, y + VERTICAL_OFFSET);
	gotoMM(ll, rl);
}

void gotoMM(double lmm, double rmm) {
	positions[0] = convertMMtoSteps(lmm);
	positions[1] = convertMMtoSteps(rmm);
	steppers.moveTo(positions);
	moving = true;
	moveComplete = !steppers.run();
}

long convertMMtoSteps(double mm) {
	return (long)(mm / MM_PER_STEP);
}

double convertStepstoMM(long steps) {
	return (double)(MM_PER_STEP * steps);
}

double pythag(double x, double y) {
	return sqrt(sq(x) + sq(y));
}

