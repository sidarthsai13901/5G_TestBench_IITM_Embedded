from pyftdi.spi import SpiController

def read_ad9528_register(ftdi_url: str, register_address: int) -> int:
    # Create an SPI controller
    spi = SpiController()

    # Configure the FTDI device as an SPI master at 10 MHz
    spi.configure(ftdi_url)

    # Open an SPI connection on the first port (CS0)
    slave = spi.get_port(cs=0, mode=0)

    # Instruction for reading, adjust based on the datasheet
    # AD9528 SPI read instruction format could be:
    # 1st byte: 1 (MSB) for read operation, followed by the 7 MSB of the register address
    # 2nd byte: Remaining part of the register address
    read_instruction = [0x80 | (register_address >> 8), register_address & 0xFF]

    # Send the read instruction, then read back the register value
    slave.exchange(read_instruction, duplex=True)
    register_value = slave.read(9)  # Read back 2 bytes (adjust based on register size)

    # Convert byte data to integer
    value = int.from_bytes(register_value, byteorder='big')

    # Properly close the SPI connection
    spi.terminate()

    return value

# Example usage:
ftdi_url = 'ftdi://ftdi:232h:FT9Q27K3/1'  # Adjust based on your FTDI device
register_address = 0x0200 # Example register address, adjust as needed

register_value = read_ad9528_register(ftdi_url, register_address)
print(f"Register value: {register_value}")