from pyftdi.ftdi import Ftdi

def list_ftdi_devices():
    # Create an Ftdi object
    ftdi = Ftdi()

    # Find all connected FTDI devices
    device_list = ftdi.list_devices()
    print(device_list)

# List FTDI devices
list_ftdi_devices()
