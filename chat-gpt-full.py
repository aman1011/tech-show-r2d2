import pygame
import time
import serial
import random
import MD49
from pysabertooth import Sabertooth
from evdev import InputDevice, categorize, ecodes
import logging

# Initialize logging
logging.basicConfig(filename='/home/pi/Desktop/r2d2-application.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define constants
hums = ["/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/hum/HUM1.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/hum/HUM7.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/hum/HUM13.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/hum/HUM17.mp3","/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/hum/HUM23.mp3"]
screams = ["/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/scream/SCREAM1.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/scream/SCREAM2.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/scream/SCREAM3.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/scream/SCREAM4.mp3"]
sents = ["/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/sent/SENT2.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/sent/SENT4.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/sent/SENT5.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/sent/SENT17.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/sent/SENT20.mp3"]
procs = ["/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/proc/PROC2.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/proc/PROC3.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/proc/PROC5.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/proc/PROC13.mp3", "/home/pi/Desktop/r2d2-2023-embedded-controller/new-r2d2-code/2023R2/Jedi/proc/PROC15.mp3"]

# Button mapping
BUTTON_MAPPING = {
    'a': 304,
    'b': 305,
    'x': 307,
    'y': 308,
    'l1': 310,
    'r1': 311,
    'l2': 10,
    'r2': 9,
    'l2_click': 312,
    'r2_click': 313
}

# Joystick axis mapping
AXIS_MAPPING = {
    'lh': 0,
    'lv': 1,
    'rh': 2,
    'rv': 5
}

# Joystick deadzone
DEADZONE = 0.02

# Motor speed limits
MOTOR_MIN_SPEED = 1
MOTOR_MAX_SPEED = 254

# Initialize pygame and joystick
pygame.init()
gamepad = InputDevice('/dev/input/event6')

# Initialize serial connections
serial_port = '/dev/ttyS0' 
baud_rate = 38400
ser = serial.Serial(serial_port, baud_rate, timeout=10)

# Initialize motor controllers
motors = MD49.MotorBoardMD49(uartBus='/dev/ttyS0')
motors.DisableTimeout()
motors.SetSpeed1(128)
motors.SetSpeed2Turn(128)

saber = Sabertooth("/dev/ttyAMA3", timeout=0.1, baudrate=9600, address=128)
saber.drive(1, 0)

def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)

def handle_button_press(event):
    button = next((key for key, value in BUTTON_MAPPING.items() if value == event.code), None)
    if button:
        logger.info(f"Button pressed: {button}")
        # Handle button press actions

def handle_joystick_motion(event):
    axis = next((key for key, value in AXIS_MAPPING.items() if value == event.code), None)
    if axis:
        if axis == 'lv':
            forward_value = translate(event.value, 0, 255, 66, 190)
            motors.SetSpeed1(int(forward_value))
            motors.SetSpeed2Turn(int(forward_value))
        elif axis == 'rh':
            turn_value = translate(event.value, 0, 255, -40, 40)
            saber.drive(1, int(turn_value))

try:
    logger.info("Robot control initialized")
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            handle_button_press(event)
        elif event.type == ecodes.EV_ABS:
            handle_joystick_motion(event)
except Exception as ex:
    logger.error(f"Error: {ex}")
finally:
    # Cleanup
    pygame.quit()
    motors.SetSpeed1(128)
    motors.SetSpeed2Turn(128)
    saber.drive(1, 0)
    logger.info("Robot control stopped")
