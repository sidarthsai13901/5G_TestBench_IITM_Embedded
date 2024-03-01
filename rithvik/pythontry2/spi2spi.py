from pyftdi.spi import SpiController, SpiIOError

# Create an SPI controller
spi = SpiController()

try:
    # Configure the FTDI device as an SPI master
    spi.configure('ftdi://ftdi:232h:0:ff/1')

    # Obtain an SPI port to a slave w/ /CS on A*BUS3 = GPIO3 / D3
    # Adjust the GPIO pin according to your connection
    slave = spi.get_port(cs=0, freq=1, mode=0)  # Configure CS, frequency, and SPI mode

    # Data to be written, replace it with your actual data bytes
    data_to_write = bytearray([0x9A,0x9b,0x3A,0x0A,0x9A,0x9A,0x9A,0x9A,0x9A,0x9A])

    # Perform the write operation
    while(1):
        slave.write(data_to_write)
        # print("Data written successfully")

except SpiIOError as e:
    print(f"SPI communication error: {e}")
finally:
    # Don't forget to properly close the SPI port!
    spi.terminate()
