from pyftdi.serialext import serial_for_url

# Open a serial port on the first FTDI device interface
ser = serial_for_url('ftdi://ftdi:4232:0ABC01/1', baudrate=9600)

# Write a string to the device
data_to_write = b'it works!!!!'
while(1):
    ser.write(data_to_write)

# Close the serial port
ser.close()
