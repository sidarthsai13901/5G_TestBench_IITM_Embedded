<<<<<<< HEAD
1
=======
from pyftdi.i2c import I2cController


# sa=0x6C

# print(type(sa))

#j5 is i2c0

slave_addr = 0x48
# int(input("Slave address: "),16)
print(type(slave_addr))
register_addr = int(input("Register add: "),16)
print(type(register_addr))

# slave_addr = 0x6C
# register_addr = 0x0B



i2c = I2cController()
try:
    
    i2c.configure('ftdi://ftdi:232h:FT9Q27K3/1')
    slave = i2c.get_port(slave_addr)
    slave.write([register_addr], False)
    data = slave.read(1)
    print(f"Read from register {hex(register_addr)}: {hex(data[0])+hex(data[1])}")
finally:
    i2c.terminate()
>>>>>>> 16b4bf3392d93c9305c9f4fc10616dc68e4d6860
