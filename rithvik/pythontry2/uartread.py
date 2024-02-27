import serial

# Replace 'COM3' with the COM port assigned to your FT232H device
com_port = 'COM6'
baud_rate = 9600  # Adjust as needed

# Open serial port
ser = serial.Serial(com_port, baud_rate, timeout=1)  # Set a read timeout

try:
    print("Listening for incoming data...")
    while True:
        data_in = ser.readline()  # Read a line of data from the UART
        if data_in:
            # Decode byte string to UTF-8 and strip newline characters
            message = data_in.decode('utf-8').rstrip('\r\n')
            print(f"Received: {message}")
finally:
    ser.close()
