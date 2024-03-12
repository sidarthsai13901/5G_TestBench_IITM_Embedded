from pyftdi.spi import SpiController

# Instantiate a SPI controller
spi = SpiController()

# Configure the FTDI device as an SPI master
spi.configure('ftdi://ftdi:232h:FT9Q27K3/1')

# Get a SPI port to a slave w/ /CS on A*BUS3 = GPIO3
slave = spi.get_port(cs=0,freq=1E6, mode=1)

# Read 2 bytes from the slave
response = slave.read(2)

print(f'Response: {response}')
