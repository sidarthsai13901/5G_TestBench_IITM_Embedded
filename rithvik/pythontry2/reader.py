from pyftdi.serialext import serial_for_url

# Open a serial port on the first FTDI device interface
ser = serial_for_url('ftdi://ftdi:4232:0ABC01/1', baudrate=9600)

# Read data from the device
data_read = ser.read(100)  # Read up to 100 bytes, or fewer if less is available
print(data_read)

# Close the serial port
ser.close()