import usb.core
import usb.util

def find_ftdi_device():
    # Find FTDI devices using vendor and product IDs
    vendor_id = 0x0403  # FTDI vendor ID
    product_id = 0x6014  # FTDI product ID

    # Find devices
    device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

    if device is not None:
        # Detach kernel driver if it's attached
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)

        # Set configuration
        device.set_configuration()

        # Get the first (and only) interface
        interface = 0

        # Claim the interface
        usb.util.claim_interface(device, interface)

        # Get the device address
        device_address = device.address

        # Release the interface
        usb.util.release_interface(device, interface)

        return device_address

    return None

device_address = find_ftdi_device()

if device_address:
    print(f"FTDI chip found at device address: {device_address}")
else:
    print("No FTDI chip found.")