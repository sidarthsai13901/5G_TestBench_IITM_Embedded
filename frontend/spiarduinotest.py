from pyftdi.spi import SpiController

# Instantiate a SPI controller
spi = SpiController()

# Configure the FTDI device as an SPI master
spi.configure('ftdi://ftdi:232h:FT9Q27K3/1')

# Get a SPI port to a slave w/ /CS on A*BUS3 = GPIO3
slave = spi.get_port(cs=0)

# Transmit data (0x01, 0x02) and receive 2 bytes
while(1):
    data_to_send = [0x00, 0x04]
    response = slave.exchange(data_to_send, duplex=True)

    print(f'Response: {response}')
