from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController, SpiIOError 

Ftdi.show_devices()
spi = SpiController()

# for interface_number in range(1, 5):
#     try:
#         spi.configure(f'ftdi://ftdi:4232:2:c/{interface_number}')
#         print(f"Using interface {interface_number} for MPSSE.")
#         break
#     except pyftdi.ftdi.FtdiMpsseError as e:
#         print(f"Interface {interface_number} does not support MPSSE for SPI: {e}")
# else:
#     print("No MPSSE-capable interfaces found.")
#     exit()

spi.configure(f'ftdi://ftdi:4232:2:12/1')


slave = spi.get_port(cs=0, freq=9600, mode=0)
data_to_write = [1,2,3]

while(True):
    slave.write(data_to_write)


# slave.write(data_to_write)
print("written", data_to_write)
spi.terminate()
