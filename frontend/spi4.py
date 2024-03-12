from pyftdi.spi import SpiController
import time

spi = SpiController()
spi.configure('ftdi://ftdi:232h:FT9Q27K3/1')
spi.flush()
port = spi.get_port(0)
port.set_frequency(1E6)

WHO_AM_I = 0x0f
WHO_AM_I_ID = 0b00111011
CTRL_REG1 = 0x20
CTRL_REG1_MODE = 0b1100111
OUT_X = 0x29
OUT_Y = 0x2b
OUT_Z = 0x2d
READ_FLAG = 0x80

print(port.exchange([WHO_AM_I | READ_FLAG], 1)[0])