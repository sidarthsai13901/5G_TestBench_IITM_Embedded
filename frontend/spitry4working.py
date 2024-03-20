from pyftdi.spi import SpiController
import time

# Create an SPI controller
spi = SpiController()

# Configure the FTDI device as an SPI master at 1MHz
spi.configure('ftdi://ftdi:4232:0ABC01/1')  # Adjust the URL for your device

# Open an SPI connection on the first port (CS0)
slave = spi.get_port(cs=0, mode=0, freq=9600)  # Adjust the mode and frequency as needed

# Data to send
data_to_send = "Hello, SPI!"

# Convert string to bytes
data_to_send_bytes = data_to_send.encode('utf-8')
print(data_to_send)
# Write data to the SPI device
# while(1):
slave.write(data_to_send_bytes)
time.sleep(1)
# Read response, if expected from the device
# Assuming the device echoes the data or sends a response
response = slave.read(len(data_to_send_bytes))
print(type(response))
# Output the received data
print("Received response:", response)

# Wait a bit before closing the SPI (optional, depends on your application)
# time.sleep(1)

# Don't forget to properly close the SPI connection
spi.terminate()