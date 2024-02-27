from pyftdi.i2c import I2cController

slave_addr = 0x6C
register_addr = 0x0C

i2c = I2cController()
try:
    
    i2c.configure('ftdi://ftdi:232h:FT9Q27K3/1')
    slave = i2c.get_port(slave_addr)
    slave.write([register_addr], False)
    data = slave.read(1)
    print(f"Read from register 0x{register_addr:02X}: {data[0]}")
finally:
    i2c.terminate()
