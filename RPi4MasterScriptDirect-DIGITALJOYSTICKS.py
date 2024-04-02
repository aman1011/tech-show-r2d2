#!/usr/bin/env python3

"""
CronTab:        https://www.makeuseof.com/how-to-run-a-raspberry-pi-program-script-at-startup/
Make HC06 work: https://dev.to/ivanmoreno/how-to-connect-raspberry-pi-with-hc-05-bluetooth-module-arduino-programm-3h7a
"""

import pygame
import time
import atexit
# Communicate with serial ports on Raspberry Pi.
import serial
import random
# Motor controllers for the feet and head, respectively.
import MD49
from pysabertooth import Sabertooth
# Stuff for the LCD display.
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
#import rf24 libraries
from pyrf24 import RF24, RF24_PA_LOW

#List of selected sounds
hums = ["Jedi/hum/HUM1.mp3", "Jedi/hum/HUM7.mp3", "Jedi/hum/HUM13.mp3", "Jedi/hum/HUM17.mp3","Jedi/hum/HUM23.mp3"]
screams = ["Jedi/scream/SCREAM1.mp3", "Jedi/scream/SCREAM2.mp3", "Jedi/scream/SCREAM3.mp3", "Jedi/scream/SCREAM4.mp3"]
sents = ["Jedi/sent/SENT2.mp3", "Jedi/sent/SENT4.mp3", "Jedi/sent/SENT5.mp3", "Jedi/sent/SENT17.mp3", "Jedi/sent/SENT20.mp3"]
procs = ["Jedi/proc/PROC2.mp3", "Jedi/proc/PROC3.mp3", "Jedi/proc/PROC5.mp3", "Jedi/proc/PROC13.mp3", "Jedi/proc/PROC15.mp3"]

# Initialize the pygame window. Key inputs will be picked up by
# it and get translated into commands.
pygame.init()
screen = pygame.display.set_mode((400,400))

# Test if the motors work, giving them a little jolt.
try:
    # MD49 at 
    motors = MD49.MotorBoardMD49(uartBus='/dev/ttyAMA2')
    motors.DisableTimeout()
    motors.SetSpeed1(128)
    motors.SetSpeed2Turn(128)
    # Sabretwwwwsdsppooiiipuupoouooth at ttyAMA1.
    saber = Sabertooth("/dev/ttyAMA1", timeout=0.1, baudrate=9600, address=128)
    saber.drive(1,0)
    print("Connected to MD49 motor controller and Sabretooth controller")
except:
    print("Could not connect to MD49")

# Attempt to establish a link with the head via bluetooth.
arduinoHead = RF24(22, 0)
headAddress  = b"00001"

arduinoHead.begin()
arduinoHead.open_tx_pipe(headAddress)
arduinoHead.print_details()

# Define LCD screen
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

lcd = I2cLcd(1, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
# Testing LCD
lcd.clear()
lcd.putstr("R2D2 Online!")
lcd.move_to(0,1)

# Function for clearing the second line of the display.
def clearLCDLine():
    i = 0
    while i < I2C_NUM_COLS:
        lcd.move_to(i, 1)
        lcd.putchar(" ")
        i += 1
    lcd.move_to(0, 1)
    

time.sleep(1)

# Initialize variables that describe the states of flaps and arms and stuff
# openFlap1 = True
# openFlap2 = True
# openFlap3 = True
# openFlap4 = True
try:
    # An event loop in Pygame is where the majority of the program happens.
    # This is where we take key inputs and make the robot do things.
    while True:
        for event in pygame.event.get():
            # If a button is pushed:
            if event.type == pygame.KEYDOWN:
                
                # Triangle on PS3
                if event.key == pygame.K_i:
                    print("pygame.K_i | HUM")
                    clearLCDLine()
                    lcd.putstr("SOUND: HUM")
                    # For playing a sound, we initialize the pygame audio mixer
                    pygame.mixer.init()
                    # Choose a random sound
                    soundChoice = random.randint(0, 4)
                    # Load into memory and play.
                    # Same logic will apply every time we play a sound from now on.
                    pygame.mixer.music.load(hums[soundChoice])
                    pygame.mixer.music.play()
                
                # Square on PS3
                elif event.key == pygame.K_u:
                    print("pygame.K_u | PROC")
                    clearLCDLine()
                    lcd.putstr("SOUND: PROC")
                    pygame.mixer.init()
                    soundChoice = random.randint(0, 4)
                    pygame.mixer.music.load(procs[soundChoice])
                    pygame.mixer.music.play()
                
                # Cross on PS3
                elif event.key == pygame.K_p:
                    print("pygame.K_p | SENT")
                    clearLCDLine()
                    lcd.putstr("SOUND: SENT")
                    pygame.mixer.init()
                    soundChoice = random.randint(0, 4)
                    pygame.mixer.music.load(sents[soundChoice])
                    pygame.mixer.music.play()
                
                # Circle on PS3
                elif event.key == pygame.K_o:
                    print("pygame.K_o | SCREAM")
                    clearLCDLine()
                    lcd.putstr("SOUND: SCREAM")
                    pygame.mixer.init()
                    soundChoice = random.randint(0, 3)
                    pygame.mixer.music.load(screams[soundChoice])
                    pygame.mixer.music.play()
                    
                elif event.key == pygame.K_1:
                    print("pygame.K_1 | D-PAD UP")
                    toSend = 1
                    result = arduinoHead.write(toSend.to_bytes(5, 'little'))
                    if not result:
                        print("Transaction failed")
                    else:
                        print("Transaction successful")
                    time.sleep(1)
                    
                elif event.key == pygame.K_2:
                    print("pygame.K_2 | D-PAD LEFT")
                    toSend = 2
                    result = arduinoHead.write(toSend.to_bytes(5, 'little'))
                    if not result:
                        print("Transaction failed")
                    else:
                        print("Transaction successful")
                    time.sleep(1)
                
                elif event.key == pygame.K_3:
                    print("pygame.K_3 | D-PAD DOWN")
                    toSend = 3
                    result = arduinoHead.write(toSend.to_bytes(5, 'little'))
                    if not result:
                        print("Transaction failed")
                    else:
                        print("Transaction successful")
                    time.sleep(1)
                    
                elif event.key == pygame.K_4:
                    print("pygame.K_4 | D-PAD RIGHT")
                    toSend = 4
                    result = arduinoHead.write(toSend.to_bytes(5, 'little'))
                    if not result:
                        print("Transaction failed")
                    else:
                        print("Transaction successful")
                    time.sleep(1)
                    
                elif event.key == pygame.K_5:
                    print("pygame.K_5 | CANTINA")
                    clearLCDLine()
                    lcd.putstr("SOUND: CANTINA")
                    pygame.mixer.init()
                    pygame.mixer.music.load("Jedi/mix/CANTINA.mp3")
                    pygame.mixer.music.play()
                
                elif event.key == pygame.K_6:
                    print("pygame.K_6 | ANNOYED")
                    pygame.mixer.init()
                    pygame.mixer.music.load("Jedi/mix/ANNOYED.mp3")
                    pygame.mixer.music.play()
                    
                elif event.key == pygame.K_7:
                    print("pygame.K_7 | SHORT CIRCUIT")
                    clearLCDLine()
                    lcd.putstr("SOUND: SH.CIRC")
                    pygame.mixer.init()
                    pygame.mixer.music.load("Jedi/mix/SHORTCKT.mp3")
                    pygame.mixer.music.play()
                
                # R2 moves slowly with the joystick, but can go faster with L2 and R2.
                elif event.key == pygame.K_MINUS:
                    print("pygame.K_MINUS | SPEED BOOST FORWARD")
                    clearLCDLine()
                    lcd.putstr("SPEED: FORWARD")
                    # These functions can be found in the MD49 library we linked to.
                    motors.SetSpeed1(255)
                    motors.SetSpeed2Turn(255)
                    
                elif event.key == pygame.K_EQUALS:
                    print("pygame.K_EQUALS | SPEED BOOST BACKWARD")
                    clearLCDLine()
                    lcd.putstr("SPEED: BACKWARD")
                    motors.SetSpeed1(0)
                    motors.SetSpeed2Turn(0)
                    
                # The idea here was to have 2 states based on the start/select button so you could use more types of sounds but never got implemented
                # but I just like using copyrighted music so I set it to that for now
                # ADDENDUM 2023: Why?
                elif event.key == pygame.K_9:
                    print("pygame.K_9 | Audio Set 1")
                    pygame.mixer.init()
                    pygame.mixer.music.load("Sunshine.ogg")
                    pygame.mixer.music.play()
                    
                elif event.key == pygame.K_0:
                    print("pygame.K_0 | Audio Set 2")
                    pygame.mixer.init()
                    pygame.mixer.music.load("/home/pi/Desktop/Someday.ogg")
                    pygame.mixer.music.play()
                
                # WASD is mapped to the left joystick
                elif event.key == pygame.K_w:
                    print("pygame.K_w")
                    clearLCDLine()
                    lcd.putstr("BODY: FORWARD")
                    motors.SetSpeed1(50)
                    motors.SetSpeed2Turn(50)
                    
                elif event.key == pygame.K_a:
                    print("pygame.K_a")
                    clearLCDLine()
                    lcd.putstr("BODY: LEFT")
                    motors.SetSpeed1(50)
                    motors.SetSpeed2Turn(200)
                
                elif event.key == pygame.K_s:
                    print("pygame.K_s")
                    clearLCDLine()
                    lcd.putstr("BODY: BACKWARD")
                    motors.SetSpeed1(200)
                    motors.SetSpeed2Turn(200)
                    
                elif event.key == pygame.K_d:
                    print("pygame.K_d")
                    clearLCDLine()
                    lcd.putstr("BODY: RIGHT")
                    motors.SetSpeed1(200)
                    motors.SetSpeed2Turn(50)
                    
                elif event.key == pygame.K_RIGHT:
                    print("pygame.K_RIGHT")
                    clearLCDLine()
                    lcd.putstr("HEAD: RIGHT")
                    # This function can be found in the Sabretooth library we linked to.
                    saber.drive(1, -70)
                    
                elif event.key == pygame.K_LEFT:
                    print("pygame.K_LEFT")
                    clearLCDLine()
                    lcd.putstr("HEAD: LEFT")
                    saber.drive(1, 70)
                
                #The original plan here was to be able to tilt a camera up and down using one of the 'eyes' in the R2D2 head
                elif event.key == pygame.K_UP:
                    print("pygame.K_UP")
                    #Tilt head up
                    
                elif event.key == pygame.K_DOWN:
                    print("pygame.K_DOWN")
                    #Tilt head up
            
            # Whenever a key is lifted (stops being pressed)
            if event.type == pygame.KEYUP:
                # All of these are either forwards or backwards body movement
                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_MINUS or event.key == pygame.K_EQUALS:
                    motors.SetSpeed1(128)
                    motors.SetSpeed2Turn(128)
                    print('Stopping forward/backward movement')
                    clearLCDLine()
                    lcd.putstr("HALTING FOR/BACK")
                # Likewise, left or right body movement
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    motors.SetSpeed1(128)
                    motors.SetSpeed2Turn(128)
                    print('Stopping sideways movement')
                    clearLCDLine()
                    lcd.putstr("HALTING SIDEWAY")
                # For the head turning
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    saber.drive(1, 0)
                    print('Stopping head turning')
                    clearLCDLine()
                    lcd.putstr("STOPPING HEAD")
            # Kill everything when you press X.
            if event.type == pygame.QUIT:
                saber.stop()
                pygame.quit()
                # Notify user
                lcd.clear()
                lcd.move_to(0,0)
                lcd.putstr("R2D2 offline!")
                quit()
except:
    saber.stop()
    motors.SetSpeed1(128)
    motors.SetSpeed2Turn(128)
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("R2D2 offline!")
    lcd.move_to(0,1)
    lcd.putstr("Fatal crash")
pygame.quit()
saber.drive(1, 0)
quit()

