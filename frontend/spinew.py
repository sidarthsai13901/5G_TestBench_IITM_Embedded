from pyftdi.spi import SpiController

# Initialize the SPI controller
spi = SpiController()

# Configure the FTDI devices
# Replace 'ftdi://ftdi:232h/1' with your FTDI device URL
spi.configure('ftdi://ftdi:232h:FT9Q27K3/1')

# Select the SPI slave, assuming chip select is connected to the first GPIO (CS=0)
slave = spi.get_port(cs=0, freq=1E6, mode=0)

# Define the register address to read
# Update this value based on your specific device and the register you want to read
register_address = 0x0096

# Some devices require a specific command or sequence to read a register.
# The following example assumes a simple SPI device where you can read directly from an address.
# Replace it with the appropriate command sequence for your device.
# The command to read a register usually includes the register address and might require
# setting a specific bit (e.g., the read bit) depending on your device protocol.
read_command = [register_address]

# Send the read command and read back the register value, adjust the number of bytes (nbytes) as necessary
response = slave.exchange(read_command,2)

# Print the result, assuming the register value is in the first byte of the response
print(response)
print(f"Register value: {response[0]}")
