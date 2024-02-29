from pyftdi.serialext import serial_for_url

# Open a serial port on the first FTDI device interface
<<<<<<< HEAD
ser = serial_for_url('ftdi://ftdi:4232:0ABC03/1', baudrate=9600)
=======
ser = serial_for_url('ftdi://ftdi:4232:0ABC01/1', baudrate=9600)
>>>>>>> 16b4bf3392d93c9305c9f4fc10616dc68e4d6860

# Read data from the device
while(1):
    data_read = ser.read(100)  # Read up to 100 bytes, or fewer if less is available
    print(data_read)

# Close the serial port
ser.close()