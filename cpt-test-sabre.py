import serial
import time

# Define the serial port and baud rate
serial_port = '/dev/ttyS0'  # Use '/dev/ttyAMA0' for Raspberry Pi 3 and earlier
baud_rate = 9600

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        # Send a command to Sabertooth for communication check
        ser.write(b'@')  # You can adjust the command based on the Sabertooth documentation

        # Read the response from Sabertooth
        response = ser.read(1)
        print(response)
        time.sleep(2)

        if response == b'\r':
            print("Sabertooth motor driver is communicating!")
        else:
            print("Sabertooth motor driver is not communicating.")

        # Wait for a short period before checking again
        time.sleep(1)

except KeyboardInterrupt:
    # Close the serial connection on Ctrl+C exit
    ser.close()
