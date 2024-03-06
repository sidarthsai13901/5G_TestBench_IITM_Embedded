from pyftdi.ftdi import Ftdi

def generate_ftdi_url():
    # Initialize context for FTDI devices
    ftdi = Ftdi()
    
    # Find all FTDI devices
    devices = ftdi.find_all([(0x0403, 0x6014)], nocache=True)

    # Loop through connected devices
    for device in devices:
        # Extract device information
        vendor, product, serial, index, interface = device
        
        # Determine device type
        # For FT232H, the product ID is 0x6014. Adjust accordingly for different types.
        if product == 0x6014:
            device_type = '232h'
        else:
            # You can extend this logic for other types
            device_type = 'unknown'
        
        # Construct the URL
        url = f"ftdi://ftdi:{device_type}:{serial}/{interface}"
        
        return url
    
    return "No FTDI device found"

# Print generated URL
url = generate_ftdi_url()
print(url)