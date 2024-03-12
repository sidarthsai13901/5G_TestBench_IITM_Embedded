# Instantiate a SPI controller
# We need want to use A*BUS4 for /CS, so at least 2 /CS lines should be
# reserved for SPI, the remaining IO are available as GPIOs.


from pyftdi.spi import SpiController, SpiIOError
from struct import *



ctrl= SpiController()#spi
ctrl.configure('ftdi://ftdi:232h/1')  # Assuming there is only one FT232H.
spi = ctrl.get_port(cs=0, freq=1E6, mode=0)# Assuming D3 is used for chip select.    
write_buf = b'hello'


# spi.write(write_buf,True,False)

# read_1= spi.read(2, start=False, stop=True)

id = spi.exchange(b'5',2, duplex=True)
# print(read_1)
print(id)
