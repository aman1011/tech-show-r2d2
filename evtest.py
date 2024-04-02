from evdev import InputDevice, categorize, ecodes
import logging
import time
from pysabertooth import Sabertooth
import json
import MD49
# Configure logging
logging.basicConfig(filename='/home/pi/Desktop/ev-test.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger
logger = logging.getLogger(__name__)

# Enums for button code variables
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308

# Mapping for back-side buttons
l1Btn = 310
r1Btn = 311
l2Trig = 10
r2Trig = 9

# Mapping for Left Axis
lhaxis = 0
lvaxis = 1

# Mapping for right Axis
rhaxis = 2
rvaxis = 5

# Click mode for l2 and r2 trig, which needs to be ignored.
clickL2Trig = 312
clickR2Trig = 313

logger.info("Starting with evdev logs ....")
gamepad = None

while gamepad is None:
	try:
		gamepad = InputDevice('/dev/input/event6')
	except Exception as ex:
		logging.info("Waiting for 2 seconds ....")
		time.sleep(2)
	
logging.info("Device initialized ....")
print(gamepad)
logging.info(gamepad)

motors = None
try:
    # MD49 at 
    motors = MD49.MotorBoardMD49(uartBus='/dev/ttyS0')
    print(motors)
    motors.DisableTimeout()

    motors.SetSpeed1(140)
    motors.SetSpeed2Turn(140)
    time.sleep(2)
    motors.SetSpeed1(128)
    motors.SetSpeed2Turn(128)
        #motors.SetSpeed2Turn(128)
        #version = motors.GetVersion()
        #print(f"version is {version} ....")
        #time.sleep(5)
except Exception as ex:
    print(f"Could not connect to MD49 {ex}")

while True:
	if gamepad is None:
		logging.info("Trying to reconnect ....")
		try:
			gamepad = InputDevice('/dev/input/event6')
		except Exception as ex:
			logging.info("Waiting for 2 seconds ....")
			time.sleep(2)
	else:
		for event in gamepad.read_loop():
			if event.type == ecodes.EV_KEY:
				if event.value == 1:
					if event.code == aBtn:
						print("A")
						logging.info("A")
						try:
							# Sabretooth at ttyAMA2.
							saber = Sabertooth("/dev/ttyAMA3", timeout=0.1, baudrate=9600, address=128)
							saber.drive(1,0)
							logging.info("Connected to Sabretooth controller ....")
						except Exception as ex:
							logging.info(f"Could not connect to sabretooth {ex} ....")
							sys.exit(0)
					elif event.code == bBtn:
						logging.info("B")
					elif event.code == xBtn:
						logging.info("X")
					elif event.code == yBtn:
						logging.info("Y")
					elif event.code == l1Btn:
						logging.info("L1")
					elif event.code == r1Btn:
						logging.info("R1")
					elif event.code == clickL2Trig or event.code == clickR2Trig:
						pass
					else:
						logging.info(f"Unsupported button. Event is {event} ....")
						
				else:
					if event.code == clickL2Trig or event.code == clickR2Trig:
						pass
					else:
						logging.info(f"Event in else of value == 1 is {event} ....")
			elif event.type == ecodes.EV_ABS:
				if event.code == lhaxis:
					logging.info("Left Horizontal axis ....")
				elif event.code == lvaxis:
					logging.info("Left veritical axis ....")
					logging.info(f"Event is {event} ....")
					if event.value != 128:
						forwardValue = 140
					else:
						forwardValue = 128
					logging.info("Setting speed ....") 
					motors.SetSpeed1(forwardValue)
					motors.SetSpeed2Turn(forwardValue)
				elif event.code == rhaxis:
					logging.info("Right Horizontal axis ....")
				elif event.code == rvaxis:
					logging.info("Right vertical axis ....")
				elif event.code == l2Trig:
					logging.info("Left trigger button ....")
				elif event.code == r2Trig:
					logging.info("Right trigger button ....")
				else:
					logging.info(f"Unsupported button ....")
					logging.info(f"event is {event} ....")
	
