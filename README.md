# Robot-Sketcher-5-bar-parallel-manipulator-
An amazing robot sketcher based on the 5 bar parallel manipulator mechanism
Video: https://www.youtube.com/watch?v=lMgfEUtLZQk
Setup: https://media.licdn.com/dms/image/C5122AQF-zxRBTb_B7w/feedshare-shrink_8192/0?e=1560384000&v=beta&t=cHfHhS5IaVnR7p2J9EBDRgsTshWLVX9Vb7uatsUTYjQ

To understand the kinematics of the mechanism visit: https://www.academia.edu/10259240/Kinematic_Analysis_of_Five_Bar_Mechanism_in_Industrial_Robotics

* The "robot_main.py" runs on the computer and "robot_arduino.ino" is for the arduino

HARDWARE REQUIRMENTS:
1.Arduino Uno
2.CNC shield (like the one at :https://www.electronicscomp.com/cnc-shield-v3-3d-printer-a4988-expansion-board?gclid=EAIaIQobChMIlLCC3vCO4gIVlQsrCh2Urw_xEAQYAiABEgL_j_D_BwE)
3.Two Stepper motor
4.Two stepper motor drivers(Model: A4988)
5.12V adapter
6.Plywood/Aluminium or whatever you use to make the links
7.Bearings(optional;the first version if this robot had links joined using nut and bot and it worked pretty fine)

SOFTWARE REQUIRMENTS:
1.Python 3.6(and for library requirments see "robot_main.py" file)
2.Arduino IDE
3.Inkscape for making vector image
4. For vector to g-code visit: jscut.org

Note: while making vector image using inkscape make all dimentions in mm also make sure the drawing is on the positive x and y axis.
      because the python program neglects negative coordinates.The image can be shifted to the negative axes of the robot's workspace 
      by assigning shifts in mm to "xerr" and "yerr" variable in the main python program.

