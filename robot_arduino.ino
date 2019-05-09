#include "CmdMessenger.h"

/* Define available CmdMessenger commands */
enum {
    motor1,
    motor2,
    motor1_value_is,
    motor2_value_is,
    
};


# define EN 8 // stepper motor enable , active low
# define X_DIR 5 // X -axis stepper motor direction control
# define Y_DIR 6 // y -axis stepper motor direction control
# define Z_DIR 7 // z axis stepper motor direction control
# define X_STP 2 // x -axis stepper control
# define Y_STP 3 // y -axis stepper control
# define Z_STP 4 // z -axis stepper control

void step (boolean dir, byte dirPin, byte stepperPin, int steps)
{
    digitalWrite (dirPin, dir);
    //delay (50);
    for (int i = 0; i <steps; i++) 
    {
        digitalWrite (stepperPin, HIGH);
        delayMicroseconds (300);//going below 500 will increase motor speed  and vice versa .But there is a limit.Motor will not move properly at very high or very low delays.
        digitalWrite (stepperPin, LOW);
        delayMicroseconds (300);
    }
}


CmdMessenger c = CmdMessenger(Serial,',',';','/');
float value1,value2;

void on_motor1(void){
    value1 = c.readBinArg<float>();
    float x=value1;
    c.sendBinCmd(motor1_value_is,value1);
   bool dir1=true;
    if (value1<0)
        {dir1=false;
        x=-x;}
    else 
        dir1=true;
   //Serial.println(value1);     
   step (dir1, X_DIR, X_STP, x);  
   //delay(2000);
}

void on_motor2(void){
    value2 = c.readBinArg<float>();
    float y=value2;
    c.sendBinCmd(motor2_value_is,value2);
    bool dir2=true;
    if (value2<0)
        {dir2=false;
        y=-y;}
    else 
        dir2=true;
//   Serial.println(value1);     
   step (dir2, Y_DIR, Y_STP, y);
   //delay(2000);
}

void attach_callbacks(void) { 
  
    c.attach(motor1,on_motor1);
    c.attach(motor2,on_motor2);
}
void setup() {
    Serial.begin(115200);//should be same as set in the python program
    attach_callbacks();   
    pinMode (X_DIR, OUTPUT); pinMode (X_STP, OUTPUT);
    pinMode (Y_DIR, OUTPUT); pinMode (Y_STP, OUTPUT);
    pinMode (Z_DIR, OUTPUT); pinMode (Z_STP, OUTPUT);
    pinMode (EN, OUTPUT);
    digitalWrite(EN, LOW); 
}

void loop() {
     //step (false, X_DIR, X_STP, 8*200);
    c.feedinSerialData();
  
   //step (true, X_DIR, X_STP, 8*200);
  // step (false, Y_DIR, Y_STP, value2*(200/360)); // y axis motor reverse 1 ring, the 200 step is a circle.
    
//   step (false, Z_DIR, Z_STP,value3*(200/360)); // z axis motor reverse 1 ring, the 200 step is a circle.
    
}

