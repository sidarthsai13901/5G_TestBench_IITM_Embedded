from pyftdi.spi import SpiController
import sys

def spi_read_register(register_address, length):
    spi = SpiController(cs_count=1)
    spi.configure('ftdi://ftdi:232h/1')
    slave = spi.get_port(cs=0, freq=1E6, mode=0)

    command = [register_address] 
    response = slave.exchange(command, length)

    return response

# Example usage
if __name__ == '__main__':
    register_address = 0x04  # Update this with the actual register address
    length_to_read = 2  # Update this with the number of bytes you expect to read

    try:
        data = spi_read_register(register_address, length_to_read)
        print(f"Read data: {data.hex()}")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
