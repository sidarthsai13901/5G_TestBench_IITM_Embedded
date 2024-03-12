from pyftdi.spi import SpiController

# Set up the SPI controller

spi = SpiController(cs_count=2)
device = 'ftdi://ftdi:232h:FT9Q27K3/1'
spi.configure(device)

# Assuming you want to communicate with a slave using CS on A*BUS4 (CS=1), mode 2, and 10 MHz frequency
# Note: Adjust 'freq' and 'mode' according to your device's requirements

slave = spi.get_port(cs=1, freq=10E5, mode=2)

# Define the register address you want to read; update this based on your needs


register_address = 0x01  # Example register address
read_command = register_address | 0x80  # Assuming the MSB is set for read operations; adjust if necessary
print(read_command)

# Send the read command and read back the register value
# Assuming you want to read a single byte from the register


write_buf = bytearray([read_command])
read_buf = slave.exchange(write_buf, readlen=1)

print(f"Register value: {read_buf[0]}")
