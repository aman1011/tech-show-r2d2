import serial
import time

# Set the serial port and baud rate based on your configuration
serial_port = '/dev/ttyS0'  # Adjust based on your configuration
baud_rate = 38400  # Baud rate for MD49

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_md49_command(command):
    # Send a command to the MD49
    ser.write(command.encode())

def read_md49_data():
    # Read data from the MD49
    return ser.readline().decode().strip()

try:
    # Send a command to query motor speeds (replace with your specific query command)
    send_md49_command('GET\r')

    # Wait for a moment to allow the MD49 to respond
    time.sleep(0.1)

    # Read and print the response
    response = read_md49_data()
    print("MD49 Response:", response)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
