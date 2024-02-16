import pyftdi.serialext

# Open a serial port on the second FTDI device interface (IF/2) @ 3Mbaud
port = pyftdi.serialext.serial_for_url('ftdi://ftdi:4232:16501/1', baudrate=3000000)

# Send bytes

var=b'Hello World'
port.write(var)
print("written",var)

# Receive bytes
print("Reading now")
data = port.read(1)
