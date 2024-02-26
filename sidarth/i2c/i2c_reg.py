from pyftdi.i2c import I2cController
import time

# Create an instance of the I2C controller
i2c = I2cController()

# Configure the FTDI device
url = 'ftdi://ftdi:4232h/1'  # Adjust the URL to match your FTDI device

try:
    # Initialize the I2C controller with the specified URL
    i2c.configure(url)

    # Slave device address (7-bit format)
    slave_address = 0x6C

    # Attempt to communicate with the slave device to check if it's recognized
    # This creates a proxy to the slave device
    slave = i2c.get_port(slave_address)

    # Perform a dummy write operation to check for slave acknowledgment
    # We don't actually need to send data, so we'll try to write an empty buffer
    # The write operation will fail if the slave does not acknowledge its address
    try:
        slave.write([])
        print("Slave device recognized.")
    except Exception as e:
        print(f"Failed to recognize slave device: {e}")
        exit(1)

    # Continue with your operations, e.g., read from a register
    register_address = 0x0B
    # Write the register address you want to read from
    slave.write([register_address])
    # Read a byte from the slave
    read_data = slave.read(1)
    print(f"Read from register 0x{register_address:02X}: 0x{read_data[0]:02X}")

finally:
    # Ensure the I2C controller is properly closed on exit
    i2c.terminate()


