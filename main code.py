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