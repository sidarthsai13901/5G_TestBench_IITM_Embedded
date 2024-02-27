import serial
import time

# Replace 'COM3' with the COM port assigned to your FT232H device
com_port = 'COM6'
baud_rate = 9600  # Adjust as needed

# Open serial port
ser = serial.Serial(com_port, baud_rate)

try:
    while True:
        message = "Hello, World!\n"
        ser.write(message.encode('utf-8'))
        print(f"Sent: {message}")
        time.sleep(1)  # Send a message every second
finally:
    ser.close()
