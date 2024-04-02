from pysabertooth import Sabertooth
import time

try:
    # Initialize Sabertooth controller
    saber = Sabertooth("/dev/ttyAMA3", timeout=0.1, baudrate=9600, address=128)
    
    # Drive motor 1 forward
    saber.drive(0, 85)  # Command motor 1 to drive forward at full speed (127)
    time.sleep(5)  # Run motor forward for 5 seconds
    
    # Stop motor 1
    saber.drive(0, 0)  # Command motor 1 to stop
    time.sleep(2)  # Wait for 2 seconds before reversing
    
    # Drive motor 1 backward
    saber.drive(1, 85)  # Command motor 1 to drive backward at full speed (127)
    time.sleep(5)  # Run motor backward for 5 seconds
    
    # Stop motor 1
    saber.drive(1, 0)  # Command motor 1 to stop
    
    print("Motor control completed successfully")
    
except Exception as ex:
    print(f"Error: {ex}")
