import subprocess
import re

def find_ftdi_device():
    try:
        # Run the lsusb command and capture the output
        result = subprocess.check_output(["lsusb"]).decode("utf-8")
        
        # Use regular expression to find FTDI devices in the output
        pattern = re.compile(r'(\d+:\d+)\s+FTDI', re.IGNORECASE)
        match = pattern.search(result)

        if match:
            return match.group(1)

    except subprocess.CalledProcessError:
        pass

    return None

device_address = find_ftdi_device()

if device_address:
    print(f"FTDI chip found at device address: {device_address}")
else:
    print("No FTDI chip found.")