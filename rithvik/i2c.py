from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController, SpiIOError 

spi = SpiController()

spi.configure('ftdi://ftdi:4232:16501/2')

slave = spi.get_port(cs=0, freq=12E6, mode=0)

gpio = spi.get_gpio()
gpio.set_direction(0x30, 0x10)

gpio.write(0x10)
var=b"hello world!"
slave.write(var)
gpio.write(0x00)
pin = bool(gpio.read() & 0x20)

print("written",var)