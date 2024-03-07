from pyftdi.spi import SpiController

# ftdi://ftdi:232h:FT9Q27K3/1
####################################
ctrl = SpiController()
ctrl.configure('ftdi://ftdi:232h:FT9Q27K3/0')
spi = ctrl.get_port(0)
spi.set_frequency(1000000)
# send 2 bytes
spi.exchange([0x12, 0x34])
# send 2 bytes, then receive 2 bytes
out = spi.exchange([0x12, 0x34], 2)
# send 2 bytes, then receive 4 bytes, manage the transaction
out = spi.exchange([0x12, 0x34], 2, True, False)
out.extend(spi.exchange([], 2, False, True))



# # READ_COMMAND = 0b00000011  # Hypothetical read command (adjust based on your device)
# REGISTER_ADDRESS = 0x05  # The register address you want to read

# spi = SpiController()
# spi.configure('ftdi://ftdi:232h:0:ff/1') 
# READ_COMMAND = 0b00000010  # Hypothetical read command (adjust based on your device)
# REGISTER_ADDRESS = 0x00 # The register address you want to read

# spi = SpiController()
# spi.configure('ftdi://ftdi:232h:FT9Q27K3/1')  # Adjust as necessary for your device

# try:
#     # Obtain a SPI port to the slave with /CS on pin 0 (adjust if needed)
#     slave = spi.get_port(cs=0, freq=1E6, mode=0)  # Adjust frequency & mode as needed

#     # Prepare the command and address to send (might need adjustment for your device)
#     # Typically, for reading a register, you send the read command followed by the address and then read back the data.
#     to_send = bytes([REGISTER_ADDRESS])

#     # Typically, for reading a register, you send the read command followed by the address
#     # and then read back the data.
#     to_send = bytes([READ_COMMAND, REGISTER_ADDRESS])
    
#     # Send the read command and address, then read back the register value
#     # The number of bytes to read back (e.g., 1 here) depends on how much data the register holds
#     read_data = slave.exchange(to_send, readlen=1)
#     print(f"Read data from register {REGISTER_ADDRESS}: {read_data.hex()}")

# finally:
#     spi.terminate()
