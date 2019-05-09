#Read the readme first
"""Software Requirments: Python(3.6)
                         Arduino IDE
         Python Library: RegEx
                         PyCmdMessebger
   Hardware requirements: "see readme"
pycmdMessenger library is used to send values to Arduino over the serial port(USB).
RegEx library is used to read coordinates from the gcode file."""
import re
import PyCmdMessenger
import math
import time
# Initialize an ArduinoBoard instance.  This is where you specify the baud rate and
# serial port.  If you are using a non ATmega328 board, you might also need
# to set the data sizes (bytes for integers, longs, floats, and doubles).  
arduino = PyCmdMessenger.ArduinoBoard("COM9",baud_rate=115200)
"""IMPORTANT NOTE:1. The available baud rates can be seen in Arduino IDE serial monitor.
                2.Increasing the baud rate increases drawing speed(with little impact on accuracy)
                but increasing the baud rate too much will cause things to not work as arduino will not be able to cope up. Motors need some time to move"""
      

# List of commands and their associated argument formats. These must be in the
# same order as in the sketch.
commands = [["motor1","f"],
            ["motor2","f"],
	    ["motor1_value_is","f"],
            ["motor2_value_is","f"]]

# Initialize the messenger
c = PyCmdMessenger.CmdMessenger(arduino,commands)





l1=80#length of link 1 in milimeters
l2=120#length of link 2 in milimeters
l3=120#you now know what it is
l4=80#same
l5=58#same
firstloop=0
th_prev1=90#Initial position of link 1(angle) 
th_prev2=0#Initial position of link 4(angle)
xerr=0#X-direction shift of sketch from the origin
yerr=0#Y-direction shift of sketch from the origin
inc=0.1#increment.The distance the pen will move in each step. Increasing this will result in a not so smooth line but will increase sketching speed and vice versa.
dist=0
start= time. time()
with open('shelby.gcode') as gcode:#shelby.gcode is the name of the gcode file to be used. This file should be in the same folder as this python file
     for line in gcode:
        line = line.strip()
        coordx = re.findall(r'X\d+.\d+', line)
        coordy = re.findall(r'Y\d+.\d+', line)
        if coordx and coordy:
            firstloop=firstloop+1
            #print("{}-{}".format(coord[0],coord[1]))
            x = coordx[0]
            xe = float(x[1:])
            xe=xe+xerr
            #print(xe)
            y = coordy[0]
            ye = float(y[1:])
            ye=ye+yerr
            #print(ye)
            if (firstloop==1): #this needs to run only once.For pen to move to the starting position
                xc=xe
                yc=ye
                xprev=xc  
                yprev=yc
                A1=xc
                B1=yc
                C1=(l1*l1 - l2*l2 + xc*xc +yc*yc)/(2*l1)

                A2=xc-l5
                B2=yc
                C2=(l4*l4 +l5*l5 -l3*l3-2*xc*l5+xc*xc+yc*yc)/(2*l4)
    
                check1=(A1*A1 + B1*B1 -C1*C1)
                check2=(A2*A2 + B2*B2 -C2*C2)
                y1b=B1
                if(check1<0 or check2<0):
                    print("The point is beyond the workspace")
        
                else:
                    y1a=math.sqrt(A1*A1 + B1*B1 -C1*C1)
                    th12=2*math.atan((-y1b-y1a)/(-A1-C1))
                    th12=(180/(22/7))*th12
        
	
                    y2a=math.sqrt(A2*A2 + B2*B2 -C2*C2)
                    y2b=B2
	
                    th22=2*math.atan((-y2b+y2a)/(-A2-C2))
                    th22=(180/(22/7))*th22
                    #print("th11={0}" .format(th11))
                    #print("th12={0}" .format(th12))
                    #print("th21={0}" .format(th21))
                    #print("th22={0}" .format(th22))
                    if(th12<0):
                        th12=360+th12
       
                    th12_new=th12-th_prev1
                    th22_new=th22-th_prev2

                     #Calculating steps for motor 1

                    steps1=th12_new*8.888888889#Here 8.8888 is the number of steps the stepper motor need to move 1 degree.Stepper motor is 1.8 degree per step.Running in 1/16 microstepping mode.So 8.888 steps=1 degree
                    steps1=round(steps1)#but the motor can move only interger number of steps(obviously)
                    if(steps1!=0):
                        c.send("motor1",steps1)
                        msg = c.receive()
                        #print(msg)
                    th12_new=steps1*0.1125#the actual angle the motor moved
                    th_prev1=th_prev1+th12_new#keeping track of the last position of the links


                  #Calculating steps for motor 2

                    steps2=th22_new*8.888888889
                    steps2=round(steps2)
                    if(steps2!=0):
                        c.send("motor2",steps2)
                        msg = c.receive()
                        #print(msg)
                    th22_new=steps2*0.1125
                    th_prev2=th_prev2+th22_new
                    print("Drawing...")
                    




          
             
            dist=math.sqrt((xprev-xe)*(xprev-xe)+(yprev-ye)*(yprev-ye))
            if(dist>inc):
            
                while(dist>=inc and firstloop>1):
                   
                    delx=xprev-xe   #finding the travel is more on which axis
                    if(delx<0):
                       delx=-delx
                    dely=yprev-ye
                    if(dely<0):
                       dely=-dely

                    if(delx>=dely): #if travel more in x then it is better to have the straight line eqn in x to avoid infinite slope condition and vice versa
                   
                       if (xe>xprev):
                          xc=xc+inc
                       else:
                          xc=xc-inc
                       yc=((yprev-ye)/(xprev-xe))*(xc-xprev)+yprev#finding points with distance=inc from the previous from the previous coordinate(using coordinate geometry)   
                    else:
                   
                       if (ye>yprev):
                          yc=yprev+inc
                       else:
                          yc=yprev-inc
                       xc=((xprev-xe)/(yprev-ye))*(yc-yprev)+xprev
                    dist=math.sqrt((xc-xe)*(xc-xe)+(yc-ye)*(yc-ye))
                    xprev=xc
                    yprev=yc

                    A1=xc
                    B1=yc
                    C1=(l1*l1 - l2*l2 + xc*xc +yc*yc)/(2*l1)

                    A2=xc-l5
                    B2=yc
                    C2=(l4*l4 +l5*l5 -l3*l3-2*xc*l5+xc*xc+yc*yc)/(2*l4)
    
                    check1=(A1*A1 + B1*B1 -C1*C1)
                    check2=(A2*A2 + B2*B2 -C2*C2)
                    y1b=B1
                    if(check1<0 or check2<0):
                        print("The point is beyond the workspace")
        
                    else:
                        y1a=math.sqrt(A1*A1 + B1*B1 -C1*C1)
                        #th11=2*math.atan((-y1b+y1a)/(-A1-C1))
                        th12=2*math.atan((-y1b-y1a)/(-A1-C1))
                        th12=(180/(22/7))*th12
        
	
                        y2a=math.sqrt(A2*A2 + B2*B2 -C2*C2)
                        y2b=B2
	
                        th22=2*math.atan((-y2b+y2a)/(-A2-C2))
                        #th22=2*math.atan((-y2b-y2a)/(-A2-C2))
                        th22=(180/(22/7))*th22
                        #print("th11={0}" .format(th11))
                        #print("th12={0}" .format(th12))
                        #print("th21={0}" .format(th21))
                        #print("th22={0}" .format(th22))
                        if(th12<0):
                            th12=360+th12
                        #if(th22<0):
                        #   th22=360+th22



                        # Send
                        th12_new=th12-th_prev1
                        th22_new=th22-th_prev2



                        steps1=th12_new*8.888888889
                        steps1=round(steps1)
                        if(steps1!=0):
                            c.send("motor1",steps1)
                            msg = c.receive()
                            #print(msg)
                        th12_new=steps1*0.1125
                        th_prev1=th_prev1+th12_new

                        #time.sleep(0.002)

                        steps2=th22_new*8.888888889
                        steps2=round(steps2)
                        if(steps2!=0):
                            c.send("motor2",steps2)
                            msg = c.receive()
                            #print(msg)
                        th22_new=steps2*0.1125
                        th_prev2=th_prev2+th22_new

        
            
                        #time.sleep(0.002)
                        
                        
                xprev=xe
                yprev=ye
print("Drawing Finished")
end = time. time()
print("Total Time(min): ",((end - start)/60)) 
