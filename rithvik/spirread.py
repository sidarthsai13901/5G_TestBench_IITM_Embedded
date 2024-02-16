
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController, SpiIOError 


spi = SpiController()

# Configure the first interface (IF/1) of the first FTDI device as a
# SPI master
spi.configure('ftdi://ftdi:4232:16501/1')

# Get a SPI port to a SPI slave w/ /CS on A*BUS3
slave = spi.get_port(cs=0,mode=0,freq=9600)

# write 6 first bits of a byte buffer
# slave.write(b'\xff', droptail=2)

# read only 13 bits from a slave (13 clock cycles)
# only the 5 MSBs of the last byte are valid, 3 LSBs are force to zero
while(True):
    var1=slave.read(2, droptail=3)

    var2=str(var1)
    print(var2[13:16])
    # print(int.from_bytes(var1, "big"))
    # print("read:",str(var1))

    # if var1=="bytearray(b'\xff\xf8')":
    #     print(1)
    # else:
    #     print(0)

